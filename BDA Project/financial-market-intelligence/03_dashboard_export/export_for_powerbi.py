"""
Financial Market Intelligence — Dashboard Export Engine
Author: Data Engineering Team
Description:
    Exports and shapes Databricks Gold Layer Delta Tables into star-schema,
    analytics-optimized Parquet and CSV extracts formatted specifically for
    Microsoft Power BI Desktop, Power BI Service, and Tableau.

Features:
    - Generates Fact and Dimension tables adhering to Dimensional Modeling (Kimball Star Schema):
        * Fact_StockAnalytics
        * Fact_SectorPerformance
        * Fact_MarketSummary
        * Dim_Company
        * Dim_Sector
        * Dim_Date (Pre-built fiscal and calendar calendar dimension)
    - Emits ready-to-paste DAX measure definitions and Tableau calculated field formulas.
    - Provides automatic fallbacks for running inside Databricks clusters,
      via Delta tables on disk, or using local extraction outputs.
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional

import pandas as pd
import numpy as np

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [DashboardExporter]: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("DashboardExporter")


def generate_date_dimension(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Constructs an enterprise-grade calendar dimension table (Dim_Date)
    optimized for time intelligence calculations in Power BI (DAX) and Tableau.
    """
    logger.info(f"Generating Dim_Date between {start_date} and {end_date}...")
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    
    df_date = pd.DataFrame({"full_date": dates})
    df_date["date_key"] = df_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    df_date["date_str"] = df_date["full_date"].dt.strftime("%Y-%m-%d")
    df_date["year"] = df_date["full_date"].dt.year
    df_date["quarter"] = df_date["full_date"].dt.quarter
    df_date["quarter_name"] = "Q" + df_date["quarter"].astype(str) + " " + df_date["year"].astype(str)
    df_date["month"] = df_date["full_date"].dt.month
    df_date["month_name"] = df_date["full_date"].dt.strftime("%B")
    df_date["month_short"] = df_date["full_date"].dt.strftime("%b")
    df_date["year_month"] = df_date["full_date"].dt.strftime("%Y-%m")
    df_date["week_of_year"] = df_date["full_date"].dt.isocalendar().week.astype(int)
    df_date["day_of_month"] = df_date["full_date"].dt.day
    df_date["day_of_week"] = df_date["full_date"].dt.dayofweek + 1  # 1 = Monday, 7 = Sunday
    df_date["day_name"] = df_date["full_date"].dt.strftime("%A")
    df_date["is_weekend"] = df_date["day_of_week"].isin([6, 7]).astype(int)
    df_date["is_trading_day"] = (~df_date["is_weekend"].astype(bool)).astype(int)
    
    # Indian Fiscal Year (April 1 to March 31)
    df_date["fiscal_year"] = np.where(
        df_date["month"] >= 4,
        df_date["year"].astype(str) + "-" + (df_date["year"] + 1).astype(str).str[-2:],
        (df_date["year"] - 1).astype(str) + "-" + df_date["year"].astype(str).str[-2:]
    )
    df_date["fiscal_quarter"] = np.where(
        df_date["month"] >= 4,
        "FQ" + ((df_date["month"] - 4) // 3 + 1).astype(str),
        "FQ" + ((df_date["month"] + 8) // 3 + 1).astype(str)
    )
    
    return df_date


def get_gold_data_from_spark(
    catalog: str,
    gold_schema: str
) -> Dict[str, pd.DataFrame]:
    """
    Reads Gold tables directly from Databricks Spark session when running within Databricks.
    """
    logger.info("Attempting to connect to active SparkSession...")
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
        
        tables = {
            "Fact_StockAnalytics": spark.table(f"{catalog}.{gold_schema}.gold_stock_analytics").toPandas(),
            "Fact_SectorPerformance": spark.table(f"{catalog}.{gold_schema}.gold_sector_performance").toPandas(),
            "Fact_MarketSummary": spark.table(f"{catalog}.{gold_schema}.gold_market_summary").toPandas()
        }
        logger.info("Successfully loaded Gold datasets from Databricks Spark catalog.")
        return tables
    except Exception as e:
        logger.warning(f"Could not load via active SparkSession: {e}")
        return {}


def simulate_or_load_local_gold(input_landing_dir: str) -> Dict[str, pd.DataFrame]:
    """
    Fallback mechanism: Reads local landing extracts or mock inputs and computes
    Gold-equivalent datasets for standalone local dashboard export without requiring Databricks.
    """
    logger.info(f"Looking for local landing files in: {input_landing_dir}")
    prices_files = []
    
    if os.path.exists(input_landing_dir):
        for root, _, files in os.walk(input_landing_dir):
            for file in files:
                if file.endswith(".csv") and "market_prices" in file:
                    prices_files.append(os.path.join(root, file))
                    
    if prices_files:
        logger.info(f"Loading prices from local files: {prices_files}")
        df_prices = pd.concat([pd.read_csv(f) for f in prices_files], ignore_axis=True)
    else:
        logger.info("No local landing files found. Generating sample production benchmark dataset...")
        # Create robust benchmark sample for demonstration & validation
        symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "NTPC.NS"]
        dates = pd.date_range(end=datetime.today(), periods=250, freq="B")
        rows = []
        base_prices = {"RELIANCE.NS": 2800.0, "TCS.NS": 3900.0, "HDFCBANK.NS": 1650.0,
                       "INFY.NS": 1500.0, "ICICIBANK.NS": 1100.0, "NTPC.NS": 350.0}
        
        for sym in symbols:
            p = base_prices[sym]
            for d in dates:
                pct = np.random.normal(0.0005, 0.015)
                p = max(10.0, p * (1 + pct))
                high = p * (1 + abs(np.random.normal(0, 0.008)))
                low = p * (1 - abs(np.random.normal(0, 0.008)))
                open_p = (high + low) / 2
                vol = int(np.random.uniform(500000, 5000000))
                rows.append({
                    "symbol": sym,
                    "trade_date": d.strftime("%Y-%m-%d"),
                    "open": round(open_p, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(p, 2),
                    "adj_close": round(p, 2),
                    "volume": vol
                })
        df_prices = pd.DataFrame(rows)

    # Basic company metadata mapping
    sector_lookup = {
        "RELIANCE.NS": ("Reliance Industries Ltd", "Energy", "Oil & Gas Refining", 19500000000000),
        "TCS.NS": ("Tata Consultancy Services Ltd", "Information Technology", "IT Services", 14000000000000),
        "HDFCBANK.NS": ("HDFC Bank Ltd", "Financial Services", "Private Banking", 12500000000000),
        "INFY.NS": ("Infosys Ltd", "Information Technology", "IT Services", 6500000000000),
        "ICICIBANK.NS": ("ICICI Bank Ltd", "Financial Services", "Private Banking", 7800000000000),
        "NTPC.NS": ("NTPC Ltd", "Utilities", "Power Generation", 3400000000000)
    }

    df_prices["symbol"] = df_prices["symbol"].str.upper().str.strip()
    df_prices["trade_date"] = pd.to_datetime(df_prices["trade_date"])
    df_prices = df_prices.sort_values(["symbol", "trade_date"]).reset_index(drop=True)

    # Computations for technical indicators
    df_prices["daily_return_pct"] = df_prices.groupby("symbol")["close"].pct_change() * 100.0
    df_prices["log_return"] = np.log(df_prices["close"] / df_prices.groupby("symbol")["close"].shift(1))
    
    # Moving Averages
    df_prices["sma_7"] = df_prices.groupby("symbol")["close"].transform(lambda x: x.rolling(7, min_periods=1).mean().round(2))
    df_prices["sma_20"] = df_prices.groupby("symbol")["close"].transform(lambda x: x.rolling(20, min_periods=1).mean().round(2))
    df_prices["sma_21"] = df_prices.groupby("symbol")["close"].transform(lambda x: x.rolling(21, min_periods=1).mean().round(2))
    df_prices["sma_50"] = df_prices.groupby("symbol")["close"].transform(lambda x: x.rolling(50, min_periods=1).mean().round(2))
    df_prices["sma_200"] = df_prices.groupby("symbol")["close"].transform(lambda x: x.rolling(200, min_periods=1).mean().round(2))
    
    # Bollinger Bands
    rolling_std = df_prices.groupby("symbol")["close"].transform(lambda x: x.rolling(20, min_periods=1).std().fillna(0))
    df_prices["bollinger_upper"] = (df_prices["sma_20"] + 2 * rolling_std).round(2)
    df_prices["bollinger_lower"] = (df_prices["sma_20"] - 2 * rolling_std).round(2)

    # 30-Day Rolling Annualized Volatility
    ann_factor = np.sqrt(252)
    vol_rolling = df_prices.groupby("symbol")["daily_return_pct"].transform(lambda x: x.rolling(30, min_periods=1).std().fillna(0))
    df_prices["annualized_volatility_30d"] = (vol_rolling * ann_factor).round(2)

    # Simple RSI 14
    def calc_rsi(series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period, min_periods=1).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50).round(2)

    df_prices["rsi_14"] = df_prices.groupby("symbol")["close"].transform(calc_rsi)

    # Metadata enrichment
    df_prices["company_name"] = df_prices["symbol"].apply(lambda s: sector_lookup.get(s, (s, "Other", "Other", 0))[0])
    df_prices["sector"] = df_prices["symbol"].apply(lambda s: sector_lookup.get(s, (s, "Other", "Other", 0))[1])
    df_prices["industry"] = df_prices["symbol"].apply(lambda s: sector_lookup.get(s, (s, "Other", "Other", 0))[2])
    df_prices["market_cap"] = df_prices["symbol"].apply(lambda s: sector_lookup.get(s, (s, "Other", "Other", 0))[3])
    df_prices["market_cap_category"] = "Large Cap"
    
    # Sector performance summary
    df_sector = df_prices.groupby(["trade_date", "sector"]).agg(
        constituent_count=("symbol", "count"),
        sector_mean_return_pct=("daily_return_pct", lambda x: round(x.mean(), 4)),
        total_sector_volume=("volume", "sum"),
        avg_sector_volatility_30d=("annualized_volatility_30d", lambda x: round(x.mean(), 4))
    ).reset_index()

    # Market summary
    df_summary = df_prices.groupby("trade_date").agg(
        total_traded_stocks=("symbol", "count"),
        advancers_count=("daily_return_pct", lambda x: (x > 0).sum()),
        decliners_count=("daily_return_pct", lambda x: (x < 0).sum()),
        unchanged_count=("daily_return_pct", lambda x: (x == 0).sum()),
        market_avg_return_pct=("daily_return_pct", lambda x: round(x.mean(), 4)),
        market_total_volume=("volume", "sum")
    ).reset_index()

    return {
        "Fact_StockAnalytics": df_prices,
        "Fact_SectorPerformance": df_sector,
        "Fact_MarketSummary": df_summary
    }


def export_star_schema(
    gold_data: Dict[str, pd.DataFrame],
    output_dir: str,
    formats: List[str]
) -> Dict[str, str]:
    """
    Shapes Gold tables into Kimball Star Schema dimensions and facts,
    and writes optimized extracts in Parquet and CSV.
    """
    os.makedirs(output_dir, exist_ok=True)
    df_fact_stock = gold_data["Fact_StockAnalytics"].copy()
    
    # 1. Standardize Dates & Date Key
    df_fact_stock["trade_date"] = pd.to_datetime(df_fact_stock["trade_date"])
    df_fact_stock["date_key"] = df_fact_stock["trade_date"].dt.strftime("%Y%m%d").astype(int)
    
    # 2. Build Dim_Date
    min_date = df_fact_stock["trade_date"].min().strftime("%Y-%m-%d")
    max_date = df_fact_stock["trade_date"].max().strftime("%Y-%m-%d")
    df_dim_date = generate_date_dimension(min_date, max_date)

    # 3. Build Dim_Sector
    sectors = df_fact_stock["sector"].dropna().unique()
    df_dim_sector = pd.DataFrame({
        "sector_key": range(1, len(sectors) + 1),
        "sector_name": sorted(sectors)
    })
    sector_key_map = dict(zip(df_dim_sector["sector_name"], df_dim_sector["sector_key"]))
    df_fact_stock["sector_key"] = df_fact_stock["sector"].map(sector_key_map).fillna(0).astype(int)

    # 4. Build Dim_Company
    cols_comp = ["symbol", "company_name", "sector", "industry", "market_cap", "market_cap_category"]
    available_comp_cols = [c for c in cols_comp if c in df_fact_stock.columns]
    df_dim_company = df_fact_stock[available_comp_cols].drop_duplicates(subset=["symbol"]).reset_index(drop=True)
    df_dim_company["sector_key"] = df_dim_company["sector"].map(sector_key_map).fillna(0).astype(int)

    # 5. Format Fact_SectorPerformance & Fact_MarketSummary with DateKey
    df_fact_sector = gold_data["Fact_SectorPerformance"].copy()
    df_fact_sector["trade_date"] = pd.to_datetime(df_fact_sector["trade_date"])
    df_fact_sector["date_key"] = df_fact_sector["trade_date"].dt.strftime("%Y%m%d").astype(int)
    df_fact_sector["sector_key"] = df_fact_sector["sector"].map(sector_key_map).fillna(0).astype(int)

    df_fact_market = gold_data["Fact_MarketSummary"].copy()
    df_fact_market["trade_date"] = pd.to_datetime(df_fact_market["trade_date"])
    df_fact_market["date_key"] = df_fact_market["trade_date"].dt.strftime("%Y%m%d").astype(int)

    # Catalog of all Star Schema tables
    star_tables = {
        "Fact_StockAnalytics": df_fact_stock,
        "Fact_SectorPerformance": df_fact_sector,
        "Fact_MarketSummary": df_fact_market,
        "Dim_Company": df_dim_company,
        "Dim_Sector": df_dim_sector,
        "Dim_Date": df_dim_date
    }

    manifest = {}
    logger.info("Persisting Star Schema Tables...")
    for name, df in star_tables.items():
        # Clean Datetime representation for CSV exports
        df_export = df.copy()
        for col in df_export.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns:
            df_export[col] = df_export[col].dt.strftime("%Y-%m-%d")

        if "parquet" in formats:
            parquet_path = os.path.join(output_dir, f"{name}.parquet")
            df_export.to_parquet(parquet_path, index=False, engine="pyarrow")
            manifest[f"{name}_parquet"] = parquet_path
            logger.info(f"Exported {name} -> {parquet_path} ({len(df)} rows)")

        if "csv" in formats:
            csv_path = os.path.join(output_dir, f"{name}.csv")
            df_export.to_csv(csv_path, index=False, encoding="utf-8")
            manifest[f"{name}_csv"] = csv_path
            logger.info(f"Exported {name} -> {csv_path} ({len(df)} rows)")

    return manifest


def generate_dax_and_tableau_guide(output_dir: str):
    """
    Generates a documentation guide with pre-computed DAX measures and
    Tableau calculated fields for instant dashboard creation.
    """
    guide_path = os.path.join(output_dir, "POWERBI_TABLEAU_INTEGRATION_GUIDE.md")
    content = """# Power BI & Tableau Integration & Data Modeling Guide

## 1. Star Schema Relationship Architecture
Connect the tables in Power BI Model View or Tableau Data Source Canvas with the following cardinalities:

| From Table (Dimension) | From Column | To Table (Fact) | To Column | Cardinality | Cross Filter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Date` | `date_key` | `Fact_StockAnalytics` | `date_key` | 1 to Many (1:*) | Single (`Dim_Date` filters Fact) |
| `Dim_Company` | `symbol` | `Fact_StockAnalytics` | `symbol` | 1 to Many (1:*) | Single (`Dim_Company` filters Fact) |
| `Dim_Sector` | `sector_key` | `Dim_Company` | `sector_key` | 1 to Many (1:*) | Single |
| `Dim_Date` | `date_key` | `Fact_SectorPerformance`| `date_key` | 1 to Many (1:*) | Single |
| `Dim_Sector` | `sector_key` | `Fact_SectorPerformance`| `sector_key` | 1 to Many (1:*) | Single |
| `Dim_Date` | `date_key` | `Fact_MarketSummary` | `date_key` | 1 to Many (1:*) | Single |

---

## 2. Essential Power BI DAX Measures

### A. Closing Price & Latest Trading Session
```dax
Latest Close Price = 
CALCULATE(
    MAX(Fact_StockAnalytics[close]),
    LASTNONBLANK(Dim_Date[full_date], CALCULATE(COUNTROWS(Fact_StockAnalytics)))
)
```

### B. Cumulative Return (Base 100 Index)
```dax
Cumulative Return Index = 
VAR InitialClose = 
    CALCULATE(
        FIRSTNONBLANKVALUE(Dim_Date[full_date], MAX(Fact_StockAnalytics[close])),
        ALLSELECTED(Dim_Date)
    )
VAR CurrentClose = [Latest Close Price]
RETURN
    DIVIDE(CurrentClose - InitialClose, InitialClose, 0) * 100
```

### C. 30-Day Realized Volatility
```dax
Avg Realized Volatility 30D = 
AVERAGE(Fact_StockAnalytics[annualized_volatility_30d])
```

### D. Golden Cross Indicator (Bullish Signal)
```dax
Golden Cross Signal = 
VAR Sma50 = AVERAGE(Fact_StockAnalytics[sma_50])
VAR Sma200 = AVERAGE(Fact_StockAnalytics[sma_200])
RETURN
    IF(
        ISBLANK(Sma50) || ISBLANK(Sma200),
        "Insufficient History",
        IF(Sma50 > Sma200, "Bullish (Golden Cross)", "Bearish (Death Cross)")
    )
```

### E. RSI Status (Overbought / Oversold)
```dax
RSI Status = 
VAR CurrentRSI = AVERAGE(Fact_StockAnalytics[rsi_14])
RETURN
    SWITCH(
        TRUE(),
        CurrentRSI >= 70, "Overbought (>= 70)",
        CurrentRSI <= 30, "Oversold (<= 30)",
        "Neutral"
    )
```

### F. Advance / Decline Line (Market Breadth)
```dax
Net Advances = 
SUM(Fact_MarketSummary[advancers_count]) - SUM(Fact_MarketSummary[decliners_count])
```

---

## 3. Tableau Calculated Fields Reference

- **Daily Return %:** `([Close] - LOOKUP(ATTR([Close]), -1)) / LOOKUP(ATTR([Close]), -1) * 100`
- **Bollinger Band Width:** `([Bollinger Upper] - [Bollinger Lower]) / [Sma 20]`
- **Trading Volume (Millions):** `[Volume] / 1000000`
- **Market Cap (INR Lakh Crores):** `[Market Cap] / 1000000000000`
"""
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Generated Power BI & Tableau Integration Guide at: {guide_path}")


def main():
    parser = argparse.ArgumentParser(description="Export Gold Layer tables for Power BI and Tableau")
    parser.add_argument("--catalog", type=str, default="fin_intel", help="Unity Catalog name")
    parser.add_argument("--gold-schema", type=str, default="gold", help="Gold schema name")
    parser.add_argument("--landing-dir", type=str, default="./landing_volume", help="Local landing directory fallback")
    parser.add_argument("--output-dir", type=str, default="./dashboard_exports", help="Destination export folder")
    parser.add_argument("--format", nargs="+", default=["parquet", "csv"], choices=["parquet", "csv"], help="Export formats")
    
    args = parser.parse_args()
    
    logger.info(f"Initiating Dashboard Export Pipeline -> Target: {args.output_dir}")
    
    # Try reading from Databricks Spark first
    gold_data = get_gold_data_from_spark(args.catalog, args.gold_schema)
    
    # Fallback to local files if Spark session is not present
    if not gold_data:
        logger.info("Operating in standalone/local mode. Loading and computing datasets from landing files...")
        gold_data = simulate_or_load_local_gold(args.landing_dir)
        
    manifest = export_star_schema(
        gold_data=gold_data,
        output_dir=args.output_dir,
        formats=args.format
    )
    
    # Emit BI DAX and Tableau integration guide
    generate_dax_and_tableau_guide(args.output_dir)
    
    print("\n--- Dashboard Export Complete ---")
    print(f"Destination Folder: {os.path.abspath(args.output_dir)}")
    print(f"Generated Files: {len(manifest)} extracts")
    for k, v in manifest.items():
        print(f"  * {k}: {v}")


if __name__ == "__main__":
    main()
