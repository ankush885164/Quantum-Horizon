# Databricks notebook source
# MAGIC %md
# MAGIC # Layer 1: Bronze Ingestion — Raw Data Landing to Delta Lake
# MAGIC **Financial Market Intelligence Pipeline**
# MAGIC
# MAGIC ### Objectives:
# MAGIC 1. Ingest raw market price CSV files and company profile JSON metadata from Databricks Unity Catalog Volumes.
# MAGIC 2. Enforce strict bronze schema definitions with raw data preservation.
# MAGIC 3. Append metadata audit columns (`_ingestion_timestamp`, `_source_file`, `_ingestion_batch_id`).
# MAGIC 4. Persist into Delta Lake Bronze tables:
# MAGIC    - `bronze_stock_prices`
# MAGIC    - `bronze_company_metadata`

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Parameter Configuration & Environment Setup

# COMMAND ----------

# Setup interactive widgets or parameters for environment agility
dbutils.widgets.text("catalog_name", "fin_intel", "1. Unity Catalog Name")
dbutils.widgets.text("schema_name", "bronze", "2. Target Bronze Schema")
dbutils.widgets.text("volume_base_path", "/Volumes/financial_market_intelligence/raw", "3. UC Volume Base Path")
dbutils.widgets.text("execution_date", "", "4. Optional Partition Date (YYYY-MM-DD)")

CATALOG_NAME = dbutils.widgets.get("catalog_name")
SCHEMA_NAME = dbutils.widgets.get("schema_name")
VOLUME_BASE_PATH = dbutils.widgets.get("volume_base_path")
EXECUTION_DATE = dbutils.widgets.get("execution_date")

print(f"Executing Bronze Ingestion:")
print(f"Catalog: {CATALOG_NAME}")
print(f"Schema:  {SCHEMA_NAME}")
print(f"Volume:  {VOLUME_BASE_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Database and Catalog Initialization

# COMMAND ----------

# Enable Unity Catalog and create schema if not exists
spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG_NAME}")
spark.sql(f"USE CATALOG {CATALOG_NAME}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME} COMMENT 'Raw Ingestion Zone for Financial Market Intelligence'")
spark.sql(f"USE SCHEMA {SCHEMA_NAME}")

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType,
    DoubleType, LongType, TimestampType
)
import uuid

BATCH_ID = str(uuid.uuid4())
print(f"Generated Audit Batch ID: {BATCH_ID}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Ingestion of Raw Market Prices (OHLCV Timeseries)

# COMMAND ----------

# Define strict Schema for Raw Prices
price_schema = StructType([
    StructField("symbol", StringType(), False),
    StructField("trade_date", StringType(), False),
    StructField("open", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("close", DoubleType(), True),
    StructField("adj_close", DoubleType(), True),
    StructField("volume", LongType(), True),
    StructField("dividends", DoubleType(), True),
    StructField("stock_splits", DoubleType(), True)
])

# Resolve prices path
if EXECUTION_DATE.strip():
    prices_raw_path = f"{VOLUME_BASE_PATH}/raw_market_prices/{EXECUTION_DATE}/*.csv"
else:
    prices_raw_path = f"{VOLUME_BASE_PATH}/raw_market_prices/*/*.csv"

print(f"Scanning raw prices from path: {prices_raw_path}")

try:
    df_raw_prices = (
        spark.read
        .format("csv")
        .option("header", "true")
        .schema(price_schema)
        .load(prices_raw_path)
    )
    
    # Enrich with audit trail attributes
    df_bronze_prices = (
        df_raw_prices
        .withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_file", F.input_file_name())
        .withColumn("_batch_id", F.lit(BATCH_ID))
    )
    
    target_prices_table = f"{CATALOG_NAME}.{SCHEMA_NAME}.bronze_stock_prices"
    
    # Save to Bronze Delta Table (Append mode)
    (
        df_bronze_prices.write
        .format("delta")
        .mode("append")
        .option("mergeSchema", "true")
        .saveAsTable(target_prices_table)
    )
    
    print(f"Successfully ingested {df_bronze_prices.count()} records into {target_prices_table}")
    
except Exception as e:
    print(f"Warning / Error during price ingestion: {e}")
    print("If testing on a local simulation directory, verify the volume path.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Ingestion of Raw Company Metadata & Fundamentals

# COMMAND ----------

meta_schema = StructType([
    StructField("symbol", StringType(), False),
    StructField("company_name", StringType(), True),
    StructField("sector", StringType(), True),
    StructField("industry", StringType(), True),
    StructField("currency", StringType(), True),
    StructField("exchange", StringType(), True),
    StructField("market_cap", DoubleType(), True),
    StructField("enterprise_value", DoubleType(), True),
    StructField("pe_ratio", DoubleType(), True),
    StructField("forward_pe", DoubleType(), True),
    StructField("peg_ratio", DoubleType(), True),
    StructField("dividend_yield", DoubleType(), True),
    StructField("beta", DoubleType(), True),
    StructField("fifty_two_week_high", DoubleType(), True),
    StructField("fifty_two_week_low", DoubleType(), True),
    StructField("extracted_at", StringType(), True)
])

metadata_raw_path = f"{VOLUME_BASE_PATH}/raw_company_metadata/*.json"
print(f"Scanning metadata JSON files from: {metadata_raw_path}")

try:
    df_raw_meta = (
        spark.read
        .format("json")
        .schema(meta_schema)
        .option("multiline", "true")
        .load(metadata_raw_path)
    )
    
    df_bronze_meta = (
        df_raw_meta
        .withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_file", F.input_file_name())
        .withColumn("_batch_id", F.lit(BATCH_ID))
    )
    
    target_meta_table = f"{CATALOG_NAME}.{SCHEMA_NAME}.bronze_company_metadata"
    
    (
        df_bronze_meta.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_meta_table)
    )
    
    print(f"Successfully ingested {df_bronze_meta.count()} records into {target_meta_table}")
    
except Exception as e:
    print(f"Warning / Error during metadata ingestion: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Bronze Data Audit & Quality Verification

# COMMAND ----------

# Preview Bronze Tables
try:
    display(spark.table(f"{CATALOG_NAME}.{SCHEMA_NAME}.bronze_stock_prices").limit(10))
    display(spark.table(f"{CATALOG_NAME}.{SCHEMA_NAME}.bronze_company_metadata").limit(10))
except Exception as e:
    print(f"Display preview: {e}")

# COMMAND ----------

# Delta Table Optimization
spark.sql(f"OPTIMIZE {CATALOG_NAME}.{SCHEMA_NAME}.bronze_stock_prices ZORDER BY (symbol, trade_date)")
