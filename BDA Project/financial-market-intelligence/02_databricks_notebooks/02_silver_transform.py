# Databricks notebook source
# MAGIC %md
# MAGIC # Layer 2: Silver Transformation — Cleansing, Schema Enforcement & Deduplication
# MAGIC **Financial Market Intelligence Pipeline**
# MAGIC
# MAGIC ### Objectives:
# MAGIC 1. Read raw datasets from Bronze Delta tables (`bronze_stock_prices` & `bronze_company_metadata`).
# MAGIC 2. Perform rigorous schema enforcement and strict data type casting (Dates, Decimals, Longs).
# MAGIC 3. Filter invalid records (e.g., negative volume, high < low, non-positive close).
# MAGIC 4. Deduplicate across `(symbol, trade_date)` retaining the latest ingestion batch.
# MAGIC 5. Standardize sector definitions and categorize market cap tiers.
# MAGIC 6. Upsert cleaned records into Silver Delta tables with Delta Lake MERGE statements.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Parameter Configuration & Setup

# COMMAND ----------

dbutils.widgets.text("catalog_name", "fin_intel", "1. Unity Catalog Name")
dbutils.widgets.text("bronze_schema", "bronze", "2. Source Bronze Schema")
dbutils.widgets.text("silver_schema", "silver", "3. Target Silver Schema")

CATALOG_NAME = dbutils.widgets.get("catalog_name")
BRONZE_SCHEMA = dbutils.widgets.get("bronze_schema")
SILVER_SCHEMA = dbutils.widgets.get("silver_schema")

print(f"Executing Silver Transformations:")
print(f"Catalog:       {CATALOG_NAME}")
print(f"Bronze Schema: {BRONZE_SCHEMA}")
print(f"Silver Schema: {SILVER_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Initialize Silver Schema

# COMMAND ----------

spark.sql(f"USE CATALOG {CATALOG_NAME}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SILVER_SCHEMA} COMMENT 'Conformed & Cleaned Silver Layer for Financial Market Intelligence'")
spark.sql(f"USE SCHEMA {SILVER_SCHEMA}")

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import (
    DateType, DoubleType, LongType, StringType, DecimalType
)
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Silver Price Transformation (Cleaning, Validation & Deduplication)

# COMMAND ----------

bronze_prices_table = f"{CATALOG_NAME}.{BRONZE_SCHEMA}.bronze_stock_prices"
df_bronze_prices = spark.table(bronze_prices_table)

# 1. Type casting & Canonical Column Standardizations
df_prices_cast = (
    df_bronze_prices
    .withColumn("symbol", F.upper(F.trim(F.col("symbol"))))
    .withColumn("trade_date", F.to_date(F.col("trade_date"), "yyyy-MM-dd"))
    .withColumn("open", F.col("open").cast(DecimalType(14, 4)))
    .withColumn("high", F.col("high").cast(DecimalType(14, 4)))
    .withColumn("low", F.col("low").cast(DecimalType(14, 4)))
    .withColumn("close", F.col("close").cast(DecimalType(14, 4)))
    .withColumn("adj_close", F.col("adj_close").cast(DecimalType(14, 4)))
    .withColumn("volume", F.coalesce(F.col("volume").cast(LongType()), F.lit(0)))
    .withColumn("dividends", F.coalesce(F.col("dividends").cast(DoubleType()), F.lit(0.0)))
    .withColumn("stock_splits", F.coalesce(F.col("stock_splits").cast(DoubleType()), F.lit(0.0)))
)

# 2. Financial Integrity Filters
# - High must be >= Low
# - Close and Open must be positive
# - Volume must be >= 0
# - Trade date must not be null
condition_valid = (
    F.col("trade_date").isNotNull() &
    (F.col("close") > 0) &
    (F.col("open") > 0) &
    (F.col("high") >= F.col("low")) &
    (F.col("high") >= F.col("close")) &
    (F.col("low") <= F.col("open")) &
    (F.col("volume") >= 0)
)

df_prices_validated = (
    df_prices_cast
    .withColumn("is_valid_integrity", condition_valid)
    .filter(F.col("is_valid_integrity") == True)
)

# 3. Window-based Deduplication: Keep most recent record if duplicate (symbol, trade_date)
dedup_window = (
    Window.partitionBy("symbol", "trade_date")
    .orderBy(F.col("_ingestion_timestamp").desc())
)

df_prices_deduped = (
    df_prices_validated
    .withColumn("row_rank", F.row_number().over(dedup_window))
    .filter(F.col("row_rank") == 1)
    .drop("row_rank", "is_valid_integrity")
    .withColumn("_silver_processed_timestamp", F.current_timestamp())
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Persist Silver Stock Prices Table (Delta MERGE)

# COMMAND ----------

silver_prices_table_name = f"{CATALOG_NAME}.{SILVER_SCHEMA}.silver_daily_stock_prices"

# Create table if not exists
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {silver_prices_table_name} (
    symbol STRING NOT NULL,
    trade_date DATE NOT NULL,
    open DECIMAL(14,4),
    high DECIMAL(14,4),
    low DECIMAL(14,4),
    close DECIMAL(14,4),
    adj_close DECIMAL(14,4),
    volume BIGINT,
    dividends DOUBLE,
    stock_splits DOUBLE,
    _ingestion_timestamp TIMESTAMP,
    _source_file STRING,
    _batch_id STRING,
    _silver_processed_timestamp TIMESTAMP
)
USING DELTA
PARTITIONED BY (symbol)
COMMENT 'Cleaned, validated and deduplicated daily equity market prices';
""")

# Merge updates into Silver table
silver_delta_table = DeltaTable.forName(spark, silver_prices_table_name)

(
    silver_delta_table.alias("target")
    .merge(
        source=df_prices_deduped.alias("source"),
        condition="target.symbol = source.symbol AND target.trade_date = source.trade_date"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

print(f"Upsert into {silver_prices_table_name} successfully executed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Silver Company Profile Standardization

# COMMAND ----------

bronze_meta_table = f"{CATALOG_NAME}.{BRONZE_SCHEMA}.bronze_company_metadata"
df_bronze_meta = spark.table(bronze_meta_table)

# Standardize company attributes and compute market cap category (INR Scale)
# Large Cap: Market Cap >= 20,000 Cr (200 Billion INR)
# Mid Cap: 5,000 Cr to 20,000 Cr
# Small Cap: < 5,000 Cr
df_silver_profiles = (
    df_bronze_meta
    .withColumn("symbol", F.upper(F.trim(F.col("symbol"))))
    .withColumn("company_name", F.coalesce(F.col("company_name"), F.col("symbol")))
    .withColumn("sector", F.coalesce(F.trim(F.col("sector")), F.lit("Unclassified")))
    .withColumn("industry", F.coalesce(F.trim(F.col("industry")), F.lit("Unclassified")))
    .withColumn("exchange", F.coalesce(F.col("exchange"), F.lit("NSE")))
    .withColumn("market_cap_category", (
        F.when(F.col("market_cap") >= 200_000_000_000, "Large Cap")
        .when((F.col("market_cap") >= 50_000_000_000) & (F.col("market_cap") < 200_000_000_000), "Mid Cap")
        .when(F.col("market_cap") > 0, "Small Cap")
        .otherwise("Undetermined")
    ))
    .withColumn("_silver_processed_timestamp", F.current_timestamp())
)

silver_profiles_table_name = f"{CATALOG_NAME}.{SILVER_SCHEMA}.silver_company_profiles"

(
    df_silver_profiles.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_profiles_table_name)
)

print(f"Updated {silver_profiles_table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6. Data Verification and Performance Optimization

# COMMAND ----------

# Display summary statistics
display(
    spark.table(silver_prices_table_name)
    .groupBy("symbol")
    .agg(
        F.count("*").alias("total_trading_days"),
        F.min("trade_date").alias("earliest_date"),
        F.max("trade_date").alias("latest_date"),
        F.avg("close").alias("avg_closing_price")
    )
)

# Run Delta optimize
spark.sql(f"OPTIMIZE {silver_prices_table_name} ZORDER BY (trade_date)")
spark.sql(f"OPTIMIZE {silver_profiles_table_name}")
