# ⚡ QUANTUM HORIZON
### Financial Market Intelligence & Big Data Analytics

<p align="center">
  <strong>Turning market data into actionable financial intelligence</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Architecture-Medallion%20Lakehouse-blue" alt="Medallion Architecture">
  <img src="https://img.shields.io/badge/Processing-Apache%20Spark-orange?logo=apachespark" alt="Apache Spark">
  <img src="https://img.shields.io/badge/Platform-Databricks-red?logo=databricks" alt="Databricks">
  <img src="https://img.shields.io/badge/BI-Power%20BI-yellow?logo=powerbi" alt="Power BI">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white" alt="Python">
</p>

---

## 📌 About the Project

**Quantum Horizon** is a financial market intelligence and Big Data analytics project that combines market-data extraction, large-scale data processing, quantitative analysis, and interactive dashboards.

The project organizes its data-engineering workflow around the **Bronze → Silver → Gold Medallion Architecture**. Python is used for data extraction and supporting analytics, while Apache Spark / PySpark and Delta Lake support distributed transformation and curated data preparation. Dashboard assets provide an interactive view of financial metrics and market trends.

## ✨ Key Capabilities

- Market data extraction and historical price analysis
- Bronze, Silver, and Gold data-processing layers
- Data cleaning, validation, standardization, and deduplication
- Financial indicators such as moving averages, RSI, Bollinger Bands, returns, and volatility
- Sector-level performance and market-breadth analysis
- Dashboard views for financial KPIs, portfolio metrics, and market trends
- Power BI-oriented reporting and dimensional data preparation

## 📊 Dashboard Gallery

The repository includes dashboard screenshots and HTML dashboard implementations.

<p align="center">
  <img src="Assets/Dashboard%20png%201.jpeg" alt="Quantum Horizon dashboard preview 1" width="90%">
</p>

<p align="center">
  <img src="Assets/Dashboard%20png%202.jpeg" alt="Quantum Horizon dashboard preview 2" width="90%">
</p>

<p align="center">
  <img src="Assets/Dashboard%20png%203.jpeg" alt="Quantum Horizon dashboard preview 3" width="90%">
</p>

<p align="center">
  <img src="Assets/Dashboard%20png%204.jpeg" alt="Quantum Horizon dashboard preview 4" width="90%">
</p>

### Explore the dashboard files

- [Interactive dashboard (HTML)](BDA%20Project/financial-market-intelligence/04_dashboard/index.html)
- [Power BI-style dashboard (HTML)](BDA%20Project/financial-market-intelligence/05_powerbi_dashboard/index.html)
- [Dashboard source and supporting files](BDA%20Project/financial-market-intelligence/04_dashboard/)
- [Power BI dashboard assets](BDA%20Project/financial-market-intelligence/05_powerbi_dashboard/)

*Note: These are repository-hosted HTML files. To use them as a live website, enable GitHub Pages or run the files locally as described in the project documentation.*

## 🏗️ Data Engineering Architecture

```text
Market Data Sources
        |
        v
Python Data Extraction
        |
        v
Raw Data / Landing Zone
        |
        v
BRONZE  - Raw data ingestion
        |
        v
SILVER  - Cleaning, validation & standardization
        |
        v
GOLD    - Curated analytics & reporting tables
        |
        v
Power BI / Dashboard Consumption
```

| Layer | Purpose |
|---|---|
| **Bronze** | Ingests and preserves raw source data with ingestion metadata. |
| **Silver** | Cleans, validates, standardizes, and deduplicates records. |
| **Gold** | Produces curated analytical datasets, indicators, and reporting outputs. |

For the detailed design, data dictionary, architecture diagram, and execution instructions, visit the [Financial Market Intelligence documentation](BDA%20Project/financial-market-intelligence/README.md) and [architecture diagram](BDA%20Project/financial-market-intelligence/architecture-diagram.md).

## 🛠️ Technology Stack

| Area | Technologies |
|---|---|
| Programming & extraction | Python, yfinance, pandas, requests |
| Distributed processing | Apache Spark, PySpark, Spark SQL |
| Lakehouse storage | Delta Lake |
| Data platform | Databricks, Unity Catalog |
| Analytics | NumPy, pandas, SciPy, scikit-learn |
| Business intelligence | Microsoft Power BI, Tableau |
| Dashboard / visualization | Streamlit, Plotly, Chart.js, HTML |

## 🗂️ Repository Structure

```text
Quantum-Horizon/
├── README.md
├── Assets/
│   ├── Dashboard png 1.jpeg
│   ├── Dashboard png 2.jpeg
│   ├── Dashboard png 3.jpeg
│   └── Dashboard png 4.jpeg
└── BDA Project/
    └── financial-market-intelligence/
        ├── README.md
        ├── architecture-diagram.md
        ├── 01_extraction/
        ├── 02_databricks_notebooks/
        ├── 03_dashboard_export/
        ├── 04_dashboard/
        ├── 05_powerbi_dashboard/
        └── supporting Python scripts and notebooks
```

## 🚀 Getting Started

1. Open the [Financial Market Intelligence project folder](BDA%20Project/financial-market-intelligence/).
2. Read the [detailed project guide](BDA%20Project/financial-market-intelligence/README.md).
3. Review the [architecture diagram](BDA%20Project/financial-market-intelligence/architecture-diagram.md).
4. Follow the prerequisites and execution steps in the detailed guide.
5. Explore the dashboard HTML files linked above.

> **Important:** The pipeline uses Databricks-specific storage and execution paths. Follow the detailed documentation and adjust the configuration for your own Databricks workspace or local environment.

## 👥 Project Team

| Name | Role | Responsibilities |
|---|---|---|
| Sanyam Sharma | Project Lead & UI/UX Engineer | Streamlit, Plotly, Chart.js |
| Ankush Sangwan | Lead Data Architect | PySpark, Databricks, Delta Lake |
| Vikash Kumar | Quantitative Modeling & AI Lead | Python, NumPy, SciPy, Scikit-Learn |
| Yash Kumar Gautam | Power BI & Dimensional Modeling Architect | Power BI, DAX, Power Query |

## ⚠️ Disclaimer

This project is intended for educational and analytical purposes. Quantitative indicators and model-generated outputs are informational and should not be treated as personalized investment advice.

---

<p align="center">
  <strong>QUANTUM HORIZON</strong><br>
  Big Data • Financial Intelligence • Quantitative Analytics
</p>
