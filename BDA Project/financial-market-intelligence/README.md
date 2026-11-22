# Financial Market Intelligence — Production Data Engineering Pipeline

[![Data Architecture: Medallion](https://img.shields.io/badge/Architecture-Medallion%20(Bronze%20%7C%20Silver%20%7C%20Gold)-blue.svg)](#medallion-architecture-breakdown)
[![Platform: Databricks](https://img.shields.io/badge/Platform-Databricks%20%26%20Unity%20Catalog-FF3621.svg)](#tech-stack--environment)
[![Engine: Apache Spark](https://img.shields.io/badge/Engine-Apache%20Spark%20%26%20Delta%20Lake-E25A1C.svg)](#tech-stack--environment)
[![Serving: Power BI & Tableau](https://img.shields.io/badge/BI-Power%20BI%20%7C%20Tableau-F2C811.svg)](#layer-3-dashboard-serving--exports)

## 1. Project Overview & Objective

The **Financial Market Intelligence** data engineering platform is an enterprise-grade, end-to-end analytical pipeline designed to ingest, clean, standardize, and analyze Indian equity market data (NSE/BSE). Built upon a **3-layer Medallion Architecture** using **Databricks**, **Apache Spark**, and **Delta Lake**, it processes multi-year historical prices, corporate actions, and fundamental valuation metrics for prominent Indian large-cap enterprises across diverse sectors (e.g., Reliance, TCS, HDFC Bank, Infosys, ICICI Bank, NTPC).

### Core Business Objectives:
- **Trend & Volatility Analysis:** Compute real-time and multi-year rolling moving averages (7, 21, 50, 200 sessions), exponential moving averages, and 30-day annualized realized volatility.
- **Momentum & Technical Indicators:** Calculate Relative Strength Index (RSI - 14 period), Bollinger Bands ($\pm 2\sigma$), and day-over-day price delta/log returns.
- **Sector Growth & Momentum:** Aggregate market performance across industry verticals to contrast Financial Services, Information Technology, Energy, FMCG, and Utilities.
- **Market Breadth:** Monitor daily advance/decline ratios, volume dynamics, and top gainers/losers.
- **BI & Executive Serving:** Deliver dimensional Star Schema tables directly consumable by Microsoft Power BI and Tableau.

---

## 2. Tech Stack & Environment

| Component | Technology | Role & Description |
| :--- | :--- | :--- |
| **Extraction Language** | Python 3.10+, `yfinance`, `pandas`, `requests` | Pulls multi-year historical OHLCV data, corporate actions, and fundamental company profiles. |
| **Storage Layer 1 (Landing)**| Databricks Unity Catalog Volumes | Secure, audited volume path (`/Volumes/fin_intel/landing/`) staging raw CSV and JSON dumps. |
| **ETL Engine Layer 2** | Apache Spark (PySpark 3.4+) & Delta Lake 3.0+ | Distributed data transformation, schema validation, ACID transactions, windowing, and Z-Order optimization. |
| **Lakehouse Governance** | Databricks Unity Catalog | Fine-grained data access control, column-level lineage, schema registry, and metadata discovery. |
| **Visualization Layer 3** | Power BI Desktop, Tableau Desktop / Cloud | Analytical dashboards, executive KPI cards, candlestick and sector correlation visualizations. |
| **Orchestration** | Databricks Workflows / Jobs | Multi-task DAG orchestration from bronze landing to gold aggregations. |

---

## 3. Directory Structure

```text
financial-market-intelligence/
│
├── README.md                           # Comprehensive project documentation & instructions
├── architecture-diagram.md             # Mermaid.js architecture diagram (Layer 1 to Layer 3)
│
├── 01_extraction/
│   ├── requirements.txt                # Python dependencies (yfinance, pandas, pyspark, etc.)
│   └── extract_market_data.py          # Script to fetch multi-year historical data & indicators for Indian stocks
│
├── 02_databricks_notebooks/
│   ├── 01_bronze_ingestion.py          # PySpark notebook code to ingest raw storage files into Bronze Delta tables
│   ├── 02_silver_transform.py          # PySpark notebook code for cleaning, null handling, type casting, schema enforcement, and deduplication
│   └── 03_gold_aggregations.py         # PySpark notebook computing financial indicators (MAs, Returns, Volatility, Sector Performance)
│
└── 03_dashboard_export/
    └── export_for_powerbi.py           # Script to shape & export Gold tables into clean Star-Schema CSV/Parquet for Power BI / Tableau
```

---

## 4. Medallion Architecture Breakdown

```
       +-------------------------------------------------------------+
       | Layer 0: Raw Ingestion (Python, yfinance, REST API)         |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       | Storage: Unity Catalog Volume (/Volumes/fin_intel/landing/) |
       +-------------------------------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
| BRONZE LAYER (Raw Delta Lake Tables)                                      |
|  - Table: bronze_stock_prices (OHLCV raw time-series)                    |
|  - Table: bronze_company_metadata (Fundamental profiles & company info)   |
|  - Features: Schema enforcement, audit timestamps, source file tracking   |
+---------------------------------------------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
| SILVER LAYER (Cleaned & Conformed Delta Lake Tables)                      |
|  - Table: silver_daily_stock_prices                                       |
|  - Table: silver_company_profiles                                         |
|  - Features: Deduplication, High >= Low check, IST Date parsing,          |
|              Capitalization categorization (Large / Mid / Small Cap)      |
+---------------------------------------------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
| GOLD LAYER (Curated Analytics Marts & Dimensional Star Schema)             |
|  - Fact Table: gold_stock_analytics (MAs, Volatility, RSI, Bollinger)     |
|  - Aggregation Table: gold_sector_performance                             |
|  - Summary Table: gold_market_summary (Advance/Decline, Market Breadth)   |
+---------------------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       | Serving Layer: Power BI / Tableau Star-Schema Extracts      |
       +-------------------------------------------------------------+
```

### Bronze Layer (`bronze`)
- Ingests raw data from Unity Catalog volume files (`.csv`, `.json`).
- Appends operational lineage: `_ingestion_timestamp`, `_source_file`, `_batch_id`.
- Preserves raw source schema verbatim for regulatory auditability and re-processing.

### Silver Layer (`silver`)
- **Deduplication:** Window partition across `(symbol, trade_date)` ordered by `_ingestion_timestamp DESC`.
- **Integrity Checks:** Filters out anomalies: non-positive prices, $High < Low$, $Low > Open$, negative volume.
- **Data Typing:** Enforces `DateType` on `trade_date`, `DecimalType(14, 4)` on prices, `LongType` on volume.
- **Normalization:** Enriches company metadata with normalized market-cap categories (Large Cap $\ge$ 20,000 Cr INR).
- **ACID Operations:** Executed using Delta Lake `MERGE INTO` operations.

### Gold Layer (`gold`)
- **Quantitative Metrics Computed:**
  - **7-day & 21-day SMA:** Short-term trend detection.
  - **50-day & 200-day SMA:** Medium- and long-term trend filters for Golden Cross / Death Cross signals.
  - **30-Day Rolling Annualized Volatility:** $\sigma_{30d} \times \sqrt{252}$.
  - **14-Day Relative Strength Index (RSI):** Overbought ($\ge 70$) and Oversold ($\le 30$) momentum bounds.
  - **Bollinger Bands:** $SMA_{20} \pm 2 \times \sigma_{20}$.
  - **Sector Summaries:** Equal-weight sector mean return, volume dispersion, and sector volatility.
  - **Market Breadth:** Advancers vs. Decliners, advance/decline ratio, and aggregate traded volume.

---

## 5. End-to-End Execution Guide

### Step 1: Market Data Extraction
```bash
# Navigate to extraction directory
cd 01_extraction

# Install Python requirements
pip install -r requirements.txt

# Run extraction (Defaults to top Indian blue chips: RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, NTPC)
python extract_market_data.py --period 5y --volume-path /Volumes/financial_market_intelligence/raw
```
*Note: If running on a local workstation without access to Databricks Volume paths, the script automatically defaults to `./landing_volume/`.*

### Step 2: Databricks Pipeline Execution
Import the files in `02_databricks_notebooks/` into your Databricks workspace or run as a multi-task Databricks Workflow job:
1. **01_bronze_ingestion:** Reads the landed files from `/Volumes/financial_market_intelligence/raw/` into `fin_intel.bronze.bronze_stock_prices` and `fin_intel.bronze.bronze_company_metadata`.
2. **02_silver_transform:** Reads bronze tables, validates, deduplicates, and MERGEs into `fin_intel.silver.silver_daily_stock_prices` and `fin_intel.silver.silver_company_profiles`.
3. **03_gold_aggregations:** Computes rolling window statistics, technical indicators, and sector aggregations into `fin_intel.gold.*`.

### Step 3: Export for Power BI & Tableau
```bash
# Navigate to dashboard export directory
cd 03_dashboard_export

# Run export script to shape Star Schema and produce Parquet and CSV files
python export_for_powerbi.py --output-dir ./dashboard_exports --format parquet csv
```
This produces:
- `Fact_StockAnalytics.parquet` & `Fact_StockAnalytics.csv`
- `Fact_SectorPerformance.parquet` & `Fact_SectorPerformance.csv`
- `Fact_MarketSummary.parquet` & `Fact_MarketSummary.csv`
- `Dim_Company.parquet` & `Dim_Company.csv`
- `Dim_Sector.parquet` & `Dim_Sector.csv`
- `Dim_Date.parquet` & `Dim_Date.csv`
- `POWERBI_TABLEAU_INTEGRATION_GUIDE.md` (DAX measures & relationships)

---

## 6. Data Dictionary

### Fact Table: `Fact_StockAnalytics` (`gold_stock_analytics`)
| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `symbol` | STRING | Stock ticker symbol (e.g., `RELIANCE.NS`) |
| `trade_date` | DATE | Official NSE trading date (`YYYY-MM-DD`) |
| `date_key` | INTEGER | Surrogate key matching `Dim_Date.date_key` (`YYYYMMDD`) |
| `open` | DECIMAL(14,4) | Opening market price in INR |
| `high` | DECIMAL(14,4) | Intraday high price in INR |
| `low` | DECIMAL(14,4) | Intraday low price in INR |
| `close` | DECIMAL(14,4) | Official closing price in INR |
| `adj_close` | DECIMAL(14,4) | Closing price adjusted for splits and dividends |
| `volume` | BIGINT | Total daily traded volume (shares) |
| `daily_return_pct` | DOUBLE | Day-over-day percentage return: $\frac{Close_t - Close_{t-1}}{Close_{t-1}} \times 100$ |
| `log_return` | DOUBLE | Natural log return: $\ln(Close_t / Close_{t-1})$ |
| `sma_7` | DOUBLE | 7-day Simple Moving Average |
| `sma_20` | DOUBLE | 20-day Simple Moving Average |
| `sma_21` | DOUBLE | 21-day Simple Moving Average |
| `sma_50` | DOUBLE | 50-day Simple Moving Average |
| `sma_200` | DOUBLE | 200-day Simple Moving Average |
| `bollinger_upper` | DOUBLE | Upper Bollinger Band ($SMA_{20} + 2\sigma$) |
| `bollinger_lower` | DOUBLE | Lower Bollinger Band ($SMA_{20} - 2\sigma$) |
| `annualized_volatility_30d`| DOUBLE | 30-day rolling annualized volatility ($\sigma_{30} \times \sqrt{252}$) |
| `rsi_14` | DOUBLE | 14-period Relative Strength Index (0 to 100) |
| `daily_range` | DOUBLE | Absolute intraday high minus low |
| `daily_range_pct` | DOUBLE | Percentage intraday spread: $\frac{High - Low}{Low} \times 100$ |

### Dimension Table: `Dim_Company`
| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `symbol` | STRING | Primary Key ticker symbol |
| `company_name` | STRING | Full corporate legal name |
| `sector_key` | INTEGER | Foreign key referencing `Dim_Sector` |
| `sector` | STRING | Broad industrial classification (e.g., Financial Services) |
| `industry` | STRING | Specific sub-industry vertical |
| `market_cap` | DOUBLE | Market capitalization in INR |
| `market_cap_category` | STRING | Capitalization tier (`Large Cap`, `Mid Cap`, `Small Cap`) |

### Dimension Table: `Dim_Date`
| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `date_key` | INTEGER | Primary Key (`YYYYMMDD`) |
| `full_date` | DATE | Standard date |
| `year` | INTEGER | Calendar year |
| `quarter_name` | STRING | Calendar quarter label (e.g., `Q1 2026`) |
| `month_name` | STRING | Full month name (e.g., `November`) |
| `fiscal_year` | STRING | Indian Fiscal Year (e.g., `2026-27`) |
| `fiscal_quarter` | STRING | Indian Fiscal Quarter (`FQ1`, `FQ2`, `FQ3`, `FQ4`) |
| `is_trading_day` | INTEGER | 1 if weekday, 0 if weekend |

---

## 7. Executive Market Intelligence Report Skeleton

Below is the standard reporting template for summarizing findings generated by this pipeline:

```markdown
# Executive Market Intelligence Report: Indian Equity Markets
**Reporting Period:** 5-Year Longitudinal Study
**Target Universe:** NIFTY Core Representatives (Financials, IT, Energy, FMCG, Utilities)

### 1. Executive Summary
- **Macro Market Trajectory:** Overview of multi-year market direction across Indian equities.
- **Top Capital Performers:** Best performing tickers by cumulative return over 1-year, 3-year, and 5-year periods.
- **High-Alpha Sectors:** Sectors exhibiting superior risk-adjusted returns (Sharpe ratio proxy).

### 2. Sectoral Performance Breakdown
| Sector | Constituent Stocks Analyzed | 1-Year Mean Return | 3-Year CAGR | Avg 30D Annualized Volatility |
| :--- | :--- | :--- | :--- | :--- |
| Financial Services | HDFCBANK, ICICIBANK, SBIN | +XX.X% | +XX.X% | XX.X% |
| Information Technology | TCS, INFY | +XX.X% | +XX.X% | XX.X% |
| Energy & Utilities | RELIANCE, NTPC | +XX.X% | +XX.X% | XX.X% |

### 3. Risk and Volatility Spectrum
- **Most Resilient Stocks (Lowest Beta & Volatility):**
  - Identification of low-volatility defensive stalwarts.
- **High-Beta / High-Volatility Leaders:**
  - Evaluation of momentum engines during expansionary cycles.
- **Correlation Matrix:**
  - Cross-sector price return correlation matrix findings.

### 4. Technical Indicator & Momentum Signals
- **Golden Cross Formations ($SMA_{50} > SMA_{200}$):** Current stocks in confirmed long-term bull territory.
- **RSI Extremes:** Tickers entering overbought conditions (RSI > 70) or oversold consolidation (RSI < 30).
- **Bollinger Band Squeezes:** Stocks displaying volatility contraction indicative of upcoming breakout moves.

### 5. Market Breadth & Liquidity Dynamics
- **Advance/Decline Ratio Trend:** Historical proportion of advancing vs. declining equities.
- **Volume Concentration:** Distribution of liquidity across top 3 vs. bottom 3 constituents.

### 6. Strategic Takeaways & Recommendations
- Quantitative signals for portfolio rebalancing.
- Sector rotation triggers observed from relative moving average divergence.
```

---

## 8. License & Governance
Distributed under the **MIT License**. Unity Catalog access policies, row-level filtering, and column masking can be configured on top of the `fin_intel` catalog to safeguard institutional proprietary data feeds.
