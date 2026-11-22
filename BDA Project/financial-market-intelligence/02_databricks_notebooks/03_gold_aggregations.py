# Databricks notebook source
# MAGIC %md
# MAGIC # Layer 3: Gold Aggregations — Financial Metrics, Indicators & Dimensional Models
# MAGIC **Financial Market Intelligence Pipeline**
# MAGIC
# MAGIC ### Objectives:
# MAGIC 1. Read validated time-series from `silver_daily_stock_prices` and `silver_company_profiles`.
# MAGIC 2. Calculate core quantitative and technical indicators via PySpark Window functions:
# MAGIC    - **Moving Averages:** 7, 21, 50, and 200-day Simple Moving Averages (SMA).
# MAGIC    - **Daily & Log Returns:** Day-over-day price delta and logarithmic returns.
# MAGIC    - **Rolling Volatility:** 30-day rolling annualized standard deviation ($\sigma \times \sqrt{252}$).
# MAGIC    - **Bollinger Bands:** 20-day SMA $\pm 2\sigma$.
# MAGIC    - **RSI (14-day):** Relative Strength Index indicator.
# MAGIC 3. Aggregate **Sector Performance Metrics** and **Market Breadth Summaries**.
# MAGIC 4. Produce star-schema analytics tables in Gold Delta Lake:
# MAGIC    - `gold_stock_analytics`
# MAGIC    - `gold_sector_performance`
# MAGIC    - `gold_market_summary`

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Parameter Configuration & Setup

# COMMAND ----------

dbutils.widgets.text("catalog_name", "fin_intel", "1. Unity Catalog Name")
dbutils.widgets.text("silver_schema", "silver", "2. Source Silver Schema")
dbutils.widgets.text("gold_schema", "gold", "3. Target Gold Schema")

CATALOG_NAME = dbutils.widgets.get("catalog_name")
SILVER_SCHEMA = dbutils.widgets.get("silver_schema")
GOLD_SCHEMA = dbutils.widgets.get("gold_schema")

print(f"Executing Gold Analytics:")
print(f"Catalog:       {CATALOG_NAME}")
print(f"Silver Schema: {SILVER_SCHEMA}")
print(f"Gold Schema:   {GOLD_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Initialize Gold Schema

# COMMAND ----------

spark.sql(f"USE CATALOG {CATALOG_NAME}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA} COMMENT 'Curated Gold Layer for Business Intelligence & Reporting'")
spark.sql(f"USE SCHEMA {GOLD_SCHEMA}")

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType, DecimalType
import math

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Read Silver Datasets

# COMMAND ----------

df_silver_prices = spark.table(f"{CATALOG_NAME}.{SILVER_SCHEMA}.silver_daily_stock_prices")
df_silver_profiles = spark.table(f"{CATALOG_NAME}.{SILVER_SCHEMA}.silver_company_profiles")

# Join prices with company metadata to get sector, industry, and capitalization tier
df_joined = df_silver_prices.join(
    df_silver_profiles.select(
        "symbol", "company_name", "sector", "industry", "market_cap", "market_cap_category"
    ),
    on="symbol",
    how="left"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Compute Technical Indicators & Return Metrics

# COMMAND ----------

# Window partitioned by symbol, ordered by trade_date ascending
win_sym_asc = Window.partitionBy("symbol").orderBy("trade_date")

# Windows for moving averages
win_rows_7   = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-6, 0)
win_rows_20  = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-19, 0)
win_rows_21  = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-20, 0)
win_rows_50  = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-49, 0)
win_rows_200 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-199, 0)
win_rows_30  = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-29, 0)

# Step 1: Returns Calculation
df_returns = (
    df_joined
    .withColumn("prev_close", F.lag("close", 1).over(win_sym_asc))
    .withColumn(
        "daily_return_pct",
        F.when(F.col("prev_close").isNotNull() & (F.col("prev_close") > 0),
               ((F.col("close") - F.col("prev_close")) / F.col("prev_close")) * 100.0)
        .otherwise(0.0)
    )
    .withColumn(
        "log_return",
        F.when(F.col("prev_close").isNotNull() & (F.col("prev_close") > 0),
               F.log(F.col("close") / F.col("prev_close")))
        .otherwise(0.0)
    )
)

# Step 2: Moving Averages & Rolling Statistics
annualization_factor = math.sqrt(252)

df_indicators = (
    df_returns
    # Simple Moving Averages
    .withColumn("sma_7", F.round(F.avg("close").over(win_rows_7), 4))
    .withColumn("sma_20", F.round(F.avg("close").over(win_rows_20), 4))
    .withColumn("sma_21", F.round(F.avg("close").over(win_rows_21), 4))
    .withColumn("sma_50", F.round(F.avg("close").over(win_rows_50), 4))
    .withColumn("sma_200", F.round(F.avg("close").over(win_rows_200), 4))
    
    # Bollinger Bands (20 periods, 2 standard deviations)
    .withColumn("stddev_20", F.stddev("close").over(win_rows_20))
    .withColumn("bollinger_upper", F.round(F.col("sma_20") + (F.lit(2.0) * F.coalesce(F.col("stddev_20"), F.lit(0.0))), 4))
    .withColumn("bollinger_lower", F.round(F.col("sma_20") - (F.lit(2.0) * F.coalesce(F.col("stddev_20"), F.lit(0.0))), 4))
    
    # 30-day Rolling Volatility (annualized)
    .withColumn("daily_stddev_30d", F.stddev("daily_return_pct").over(win_rows_30))
    .withColumn("annualized_volatility_30d", F.round(F.col("daily_stddev_30d") * F.lit(annualization_factor), 4))
    
    # High / Low Spread
    .withColumn("daily_range", F.round(F.col("high") - F.col("low"), 4))
    .withColumn("daily_range_pct", F.round(((F.col("high") - F.col("low")) / F.col("low")) * 100.0, 4))
)

# Step 3: Relative Strength Index (RSI - 14 Days Approximation)
win_rows_14 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-13, 0)

df_rsi_calc = (
    df_indicators
    .withColumn("price_change", F.col("close") - F.col("prev_close"))
    .withColumn("gain", F.when(F.col("price_change") > 0, F.col("price_change")).otherwise(0.0))
    .withColumn("loss", F.when(F.col("price_change") < 0, F.abs(F.col("price_change"))).otherwise(0.0))
    .withColumn("avg_gain_14", F.avg("gain").over(win_rows_14))
    .withColumn("avg_loss_14", F.avg("loss").over(win_rows_14))
    .withColumn(
        "rs",
        F.when(F.col("avg_loss_14") == 0, 100.0)
        .otherwise(F.col("avg_gain_14") / F.col("avg_loss_14"))
    )
    .withColumn(
        "rsi_14",
        F.round(
            F.when(F.col("avg_loss_14") == 0, 100.0)
            .otherwise(F.lit(100.0) - (F.lit(100.0) / (F.lit(1.0) + F.col("rs")))),
            2
        )
    )
    .drop("price_change", "gain", "loss", "avg_gain_14", "avg_loss_14", "rs")
    .withColumn("_gold_calculated_timestamp", F.current_timestamp())
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Save Table 1: `gold_stock_analytics` (Primary Fact Table)

# COMMAND ----------

gold_stock_table = f"{CATALOG_NAME}.{GOLD_SCHEMA}.gold_stock_analytics"

(
    df_rsi_calc.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(gold_stock_table)
)

print(f"Persisted Fact Table {gold_stock_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6. Compute Table 2: `gold_sector_performance`

# COMMAND ----------

# Aggregating daily performance by Sector
df_sector_perf = (
    df_rsi_calc
    .filter(F.col("sector").isNotNull() & (F.col("sector") != "Unclassified"))
    .groupBy("trade_date", "sector")
    .agg(
        F.count("symbol").alias("constituent_count"),
        F.round(F.avg("daily_return_pct"), 4).alias("sector_mean_return_pct"),
        F.round(F.stddev("daily_return_pct"), 4).alias("sector_return_dispersion"),
        F.sum("volume").alias("total_sector_volume"),
        F.round(F.avg("annualized_volatility_30d"), 4).alias("avg_sector_volatility_30d")
    )
    .withColumn("_gold_calculated_timestamp", F.current_timestamp())
)

gold_sector_table = f"{CATALOG_NAME}.{GOLD_SCHEMA}.gold_sector_performance"

(
    df_sector_perf.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(gold_sector_table)
)

print(f"Persisted Summary Table {gold_sector_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7. Compute Table 3: `gold_market_summary` (Market Breadth & Extremes)

# COMMAND ----------

# Market Breadth: Count of Advancers, Decliners, and Unchanged per trading day
df_market_breadth = (
    df_rsi_calc
    .groupBy("trade_date")
    .agg(
        F.count("symbol").alias("total_traded_stocks"),
        F.sum(F.when(F.col("daily_return_pct") > 0.0, 1).otherwise(0)).alias("advancers_count"),
        F.sum(F.when(F.col("daily_return_pct") < 0.0, 1).otherwise(0)).alias("decliners_count"),
        F.sum(F.when(F.col("daily_return_pct") == 0.0, 1).otherwise(0)).alias("unchanged_count"),
        F.round(F.avg("daily_return_pct"), 4).alias("market_avg_return_pct"),
        F.sum("volume").alias("market_total_volume")
    )
    .withColumn(
        "advance_decline_ratio",
        F.round(F.col("advancers_count") / F.when(F.col("decliners_count") == 0, 1).otherwise(F.col("decliners_count")), 3)
    )
    .withColumn("_gold_calculated_timestamp", F.current_timestamp())
)

gold_summary_table = f"{CATALOG_NAME}.{GOLD_SCHEMA}.gold_market_summary"

(
    df_market_breadth.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(gold_summary_table)
)

print(f"Persisted Summary Table {gold_summary_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 8. Gold Layer Data Verification & Optimization

# COMMAND ----------

display(spark.table(gold_stock_table).select("symbol", "trade_date", "close", "sma_50", "sma_200", "rsi_14", "annualized_volatility_30d").limit(10))
display(spark.table(gold_sector_table).orderBy(F.col("trade_date").desc()).limit(10))
display(spark.table(gold_summary_table).orderBy(F.col("trade_date").desc()).limit(10))

# Optimize Gold tables
spark.sql(f"OPTIMIZE {gold_stock_table} ZORDER BY (symbol, trade_date)")
spark.sql(f"OPTIMIZE {gold_sector_table} ZORDER BY (sector, trade_date)")
spark.sql(f"OPTIMIZE {gold_summary_table} ZORDER BY (trade_date)")
