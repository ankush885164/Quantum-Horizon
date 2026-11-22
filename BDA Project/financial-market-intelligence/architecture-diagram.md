# Financial Market Intelligence — End-to-End Architecture Diagram

## 1. Architectural Overview

The **Financial Market Intelligence** data engineering platform is designed following the industry-standard **Medallion Architecture (Bronze → Silver → Gold)** implemented on **Databricks**, **Delta Lake**, and **Apache Spark**, with unified governance via **Databricks Unity Catalog**.

Data is ingested from Indian Equity Markets (National Stock Exchange - NSE) via financial data APIs, staged into Unity Catalog Volumes, incrementally processed and cleaned through Delta Lake tables, and served as analytics-ready star schema dimensional models for downstream consumption in Power BI and Tableau.

---

## 2. Mermaid.js System Architecture Diagram

```mermaid
flowchart TB
    subgraph EXT["Layer 0: Ingestion & Extraction Layer"]
        direction TB
        EXT_SRC["External Market Data Sources<br/>(Yahoo Finance API / NSE / BSE)"]
        EXT_SCRIPT["01_extraction/extract_market_data.py<br/>(Python, yfinance, requests, pandas)"]
        EXT_SRC -->|REST API Requests / TLS| EXT_SCRIPT
    end

    subgraph UC_VOL["Storage Layer 1: Unity Catalog Landing Volume"]
        direction TB
        RAW_PRICES["Landing: Raw Daily Stock Prices<br/><code>/Volumes/fin_intel/landing/market_data/YYYY-MM-DD/</code><br/>Format: Raw CSV / JSON"]
        RAW_META["Landing: Raw Company & Sector Metadata<br/><code>/Volumes/fin_intel/landing/company_profiles/</code><br/>Format: JSON"]
        EXT_SCRIPT -->|Batch Write Raw Dumps| RAW_PRICES
        EXT_SCRIPT -->|Batch Write Raw Dumps| RAW_META
    end

    subgraph MEDALLION["Databricks ETL Pipeline (Apache Spark & Delta Lake)"]
        direction TB

        subgraph BRONZE["Bronze Layer (Raw Ingestion & Audit)"]
            B_PRICES["bronze_stock_prices<br/>Delta Table<br/>+ Ingestion Timestamp<br/>+ Source File Metadata"]
            B_META["bronze_company_metadata<br/>Delta Table<br/>+ Raw Schema Preservation"]
        end

        subgraph SILVER["Silver Layer (Cleansing & Conformance)"]
            S_PRICES["silver_daily_stock_prices<br/>Delta Table<br/>- Null imputation & Deduplication<br/>- Data type casting & Timezone (IST)<br/>- High/Low/Close integrity validation"]
            S_PROFILES["silver_company_profiles<br/>Delta Table<br/>- Standardized Sector / Industry<br/>- Capitalization classifications"]
        end

        subgraph GOLD["Gold Layer (Analytics & Dimensional Marts)"]
            G_ANALYTICS["gold_stock_analytics (Fact)<br/>- SMA 7/21/50/200, EMA 12/26<br/>- RSI (14), Volatility (30D Rolling)<br/>- Daily & Cumulative Returns<br/>- Bollinger Bands (Upper/Lower)"]
            G_SECTOR["gold_sector_performance<br/>- Equal & Cap-Weighted Returns<br/>- Sector Momentum & Volatility"]
            G_SUMMARY["gold_market_summary<br/>- Market Breadth (Advancers/Decliners)<br/>- Top Gainers & Losers"]
        end

        RAW_PRICES -->|01_bronze_ingestion.py| B_PRICES
        RAW_META -->|01_bronze_ingestion.py| B_META

        B_PRICES -->|02_silver_transform.py| S_PRICES
        B_META -->|02_silver_transform.py| S_PROFILES

        S_PRICES & S_PROFILES -->|03_gold_aggregations.py| G_ANALYTICS
        S_PRICES & S_PROFILES -->|03_gold_aggregations.py| G_SECTOR
        S_PRICES -->|03_gold_aggregations.py| G_SUMMARY
    end

    subgraph SERVING["Layer 3: Visualization & Business Intelligence"]
        direction TB
        EXP_SCRIPT["03_dashboard_export/export_for_powerbi.py<br/>(Delta → Optimized Parquet / CSV)"]
        BI_PBI["Microsoft Power BI Desktop / Service<br/>(Direct Lake / Import Mode)"]
        BI_TAB["Tableau Desktop / Server<br/>(Hyper Extract / Live Connection)"]

        G_ANALYTICS & G_SECTOR & G_SUMMARY -->|Spark Read / Export Pipeline| EXP_SCRIPT
        EXP_SCRIPT -->|Star Schema Parquet / CSV Extracts| BI_PBI
        EXP_SCRIPT -->|Curated Extracts & Data Dictionary| BI_TAB
    end

    %% Styles
    classDef extract fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#000;
    classDef storage fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#000;
    classDef bronze fill:#EFEBE9,stroke:#4E342E,stroke-width:2px,color:#000;
    classDef silver fill:#ECEFF1,stroke:#455A64,stroke-width:2px,color:#000;
    classDef gold fill:#FFFDE7,stroke:#F57F17,stroke-width:2px,color:#000;
    classDef bi fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#000;

    class EXT,EXT_SRC,EXT_SCRIPT extract;
    class UC_VOL,RAW_PRICES,RAW_META storage;
    class B_PRICES,B_META bronze;
    class S_PRICES,S_PROFILES silver;
    class G_ANALYTICS,G_SECTOR,G_SUMMARY gold;
    class SERVING,EXP_SCRIPT,BI_PBI,BI_TAB bi;
```

---

## 3. Layer-by-Layer Architectural Specifications

### Layer 0: Ingestion & Extraction Layer
- **Source:** Yahoo Finance API (`yfinance`), NSE historical price feeds.
- **Coverage:** Blue-chip and high-impact Indian equities across core sectors:
  - Financials: `HDFCBANK.NS`, `ICICIBANK.NS`, `SBIN.NS`
  - Information Technology: `TCS.NS`, `INFY.NS`, `WIPRO.NS`
  - Energy & Utilities: `RELIANCE.NS`, `NTPC.NS`, `ONGC.NS`
  - Consumer / Auto: `HINDUNILVR.NS`, `TATAMOTORS.NS`
- **Output:** Raw CSV OHLCV timeseries files and company metadata JSON documents.

### Storage Layer 1: Databricks Unity Catalog Volume (Landing Zone)
- **Path Pattern:** `/Volumes/<catalog>/<schema>/landing/market_data/`
- **Characteristics:** Immutable, append-only raw file landing zone. Preserves untouched raw payloads for auditability, lineage tracking, and zero-loss reprocessing.

### ETL Layer 2: Apache Spark & Delta Lake (Databricks)
1. **Bronze Layer:**
   - Append-only raw Delta tables with complete audit metadata (`_ingestion_timestamp`, `_source_file`).
   - ACID transaction guarantees, schema validation on write.
2. **Silver Layer:**
   - Deduplicated on `(symbol, trade_date)`.
   - Data cleaning: NULL handling, invalid price elimination (e.g. Low $\le$ High, Volume $\ge$ 0).
   - Datetime casting: Standardized IST/UTC dates.
   - Enriched with standard company profile attributes (Sector, Industry, Market Cap Category).
3. **Gold Layer:**
   - Star schema design tailored for high-performance financial analytics.
   - Windowing analytics:
     - Simple Moving Averages (7, 21, 50, 200 sessions).
     - Exponential Moving Averages (12, 26 sessions).
     - Relative Strength Index (RSI - 14 session Wilders/Standard approximation).
     - 30-day Rolling Volatility (annualized with $\sqrt{252}$).
     - Daily percentage price change and log returns.
     - Sector performance benchmarks (equal-weight and capitalization-weighted return indices).

### Visualization Layer 3: Serving & Business Intelligence
- **Consumers:** Power BI Desktop / Service, Tableau Desktop / Cloud.
- **Data Model:** Star Schema:
  - Fact: `Fact_StockAnalytics`
  - Dimensions: `Dim_Date`, `Dim_Company`, `Dim_Sector`
- **Export Formats:** Columnar Apache Parquet (snappy compression) & UTF-8 clean CSV with formatted headers.
