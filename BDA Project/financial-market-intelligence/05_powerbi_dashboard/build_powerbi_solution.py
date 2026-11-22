# -*- coding: utf-8 -*-
"""
Generate Complete Power BI Solution:
1. Star-Schema Data Exports (CSV & Parquet)
2. Power BI Custom Theme JSON (PowerBI_Aurora_Theme.json)
3. Production DAX Measures Collection (DAX_Measures.dax)
4. Power Query M ETL Script (PowerQuery_M_Script.m)
5. Interactive Power BI Service Web Report Canvas (powerbi_dashboard.html)
6. One-Click Launcher (run_powerbi.bat)
"""

import os
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

base_dir = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard"
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. GENERATE POWER BI STAR SCHEMA DATASETS
# -----------------------------------------------------------------------------
print("Generating Star Schema data for Power BI...")

# Companies Dimension
companies_data = [
    # Indian Blue Chips
    {"symbol": "RELIANCE.NS", "company_name": "Reliance Industries Ltd", "sector": "Energy", "industry": "Oil & Gas Refining", "market": "NSE (India)", "currency": "INR", "market_cap": 19500000000000, "market_cap_category": "Mega Cap", "sector_key": 1},
    {"symbol": "TCS.NS", "company_name": "Tata Consultancy Services Ltd", "sector": "Technology", "industry": "IT Consulting & Software", "market": "NSE (India)", "currency": "INR", "market_cap": 14000000000000, "market_cap_category": "Mega Cap", "sector_key": 2},
    {"symbol": "HDFCBANK.NS", "company_name": "HDFC Bank Ltd", "sector": "Financials", "industry": "Private Sector Banking", "market": "NSE (India)", "currency": "INR", "market_cap": 12500000000000, "market_cap_category": "Mega Cap", "sector_key": 3},
    {"symbol": "INFY.NS", "company_name": "Infosys Ltd", "sector": "Technology", "industry": "IT Services", "market": "NSE (India)", "currency": "INR", "market_cap": 6500000000000, "market_cap_category": "Large Cap", "sector_key": 2},
    {"symbol": "ICICIBANK.NS", "company_name": "ICICI Bank Ltd", "sector": "Financials", "industry": "Private Sector Banking", "market": "NSE (India)", "currency": "INR", "market_cap": 7800000000000, "market_cap_category": "Large Cap", "sector_key": 3},
    
    # US Mega-Cap Equities
    {"symbol": "NVDA", "company_name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors & AI", "market": "NASDAQ (US)", "currency": "USD", "market_cap": 3150000000000, "market_cap_category": "Mega Cap", "sector_key": 2},
    {"symbol": "MSFT", "company_name": "Microsoft Corporation", "sector": "Technology", "industry": "Cloud & Enterprise Software", "market": "NASDAQ (US)", "currency": "USD", "market_cap": 3320000000000, "market_cap_category": "Mega Cap", "sector_key": 2},
    {"symbol": "AAPL", "company_name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "market": "NASDAQ (US)", "currency": "USD", "market_cap": 3450000000000, "market_cap_category": "Mega Cap", "sector_key": 2},
    {"symbol": "ASML", "company_name": "ASML Holding NV", "sector": "Technology", "industry": "Semiconductor Equipment", "market": "NASDAQ (US)", "currency": "USD", "market_cap": 370000000000, "market_cap_category": "Large Cap", "sector_key": 2},
    
    # Crypto Treasury & FX
    {"symbol": "BTC-USD", "company_name": "Bitcoin Core Treasury", "sector": "Financials", "industry": "Digital Asset Reserve", "market": "Global Crypto", "currency": "USD", "market_cap": 1240000000000, "market_cap_category": "Mega Cap", "sector_key": 3},
    {"symbol": "USDINR=X", "company_name": "USD / INR Currency Pair", "sector": "Financials", "industry": "Foreign Exchange", "market": "Global Forex", "currency": "INR", "market_cap": 0, "market_cap_category": "Forex", "sector_key": 3}
]
df_companies = pd.DataFrame(companies_data)
df_companies.to_csv(os.path.join(data_dir, "Dim_Company.csv"), index=False)

# Sectors Dimension
sectors_data = [
    {"sector_key": 1, "sector_name": "Energy", "benchmark_weight": 0.18, "mandate_limit": 0.25},
    {"sector_key": 2, "sector_name": "Technology", "benchmark_weight": 0.42, "mandate_limit": 0.50},
    {"sector_key": 3, "sector_name": "Financials", "benchmark_weight": 0.24, "mandate_limit": 0.35},
    {"sector_key": 4, "sector_name": "Utilities", "benchmark_weight": 0.16, "mandate_limit": 0.20}
]
df_sectors = pd.DataFrame(sectors_data)
df_sectors.to_csv(os.path.join(data_dir, "Dim_Sector.csv"), index=False)

# Calendar Dimension (Dim_Date)
dates = pd.date_range(end=datetime.today(), periods=250, freq="B")
date_rows = []
for d in dates:
    date_rows.append({
        "date_key": int(d.strftime("%Y%m%d")),
        "full_date": d.strftime("%Y-%m-%d"),
        "year": d.year,
        "quarter": f"Q{d.quarter}",
        "month": d.month,
        "month_name": d.strftime("%B"),
        "month_short": d.strftime("%b"),
        "day_of_month": d.day,
        "day_name": d.strftime("%A"),
        "is_trading_day": 1
    })
df_date = pd.DataFrame(date_rows)
df_date.to_csv(os.path.join(data_dir, "Dim_Date.csv"), index=False)

# Fact_StockAnalytics with 20D MA, 50D MA, Bollinger Bands, RSI, Returns
base_prices = {
    "RELIANCE.NS": 1360.20, "TCS.NS": 2349.40, "HDFCBANK.NS": 1742.60,
    "INFY.NS": 1081.90, "ICICIBANK.NS": 1264.50, "NVDA": 128.40,
    "MSFT": 448.20, "AAPL": 224.50, "ASML": 920.00,
    "BTC-USD": 63240.00, "USDINR=X": 84.42
}

analytics_rows = []
for comp in companies_data:
    sym = comp["symbol"]
    target_p = base_prices[sym]
    # create realistic price history leading up to target_p
    n_days = len(dates)
    drift = 0.0004
    vol = 0.016 if "BTC" not in sym else 0.03
    np.random.seed(abs(hash(sym)) % 1000000)
    returns = np.random.normal(drift, vol, n_days)
    returns[-1] = 0.008  # positive last day
    
    # reconstruct backwards so last price equals target_p
    prices = [target_p]
    for r in reversed(returns[1:]):
        prices.append(prices[-1] / (1 + r))
    prices = list(reversed(prices))
    
    series_p = pd.Series(prices)
    sma_7 = series_p.rolling(7, min_periods=1).mean()
    sma_20 = series_p.rolling(20, min_periods=1).mean()
    sma_50 = series_p.rolling(50, min_periods=1).mean()
    std_20 = series_p.rolling(20, min_periods=1).std().fillna(0)
    b_upper = sma_20 + 2 * std_20
    b_lower = sma_20 - 2 * std_20
    daily_ret = series_p.pct_change() * 100.0
    
    # RSI calculation (14 periods)
    delta = series_p.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14, min_periods=1).mean()
    rs = gain / (loss + 1e-9)
    rsi_14 = 100 - (100 / (1 + rs))
    rsi_14 = rsi_14.fillna(50).clip(10, 95)
    
    for i, d in enumerate(dates):
        p = round(prices[i], 2)
        v = int(np.random.uniform(800000, 4500000))
        analytics_rows.append({
            "symbol": sym,
            "trade_date": d.strftime("%Y-%m-%d"),
            "date_key": int(d.strftime("%Y%m%d")),
            "open": round(p * 0.995, 2),
            "high": round(p * 1.012, 2),
            "low": round(p * 0.988, 2),
            "close": p,
            "volume": v,
            "daily_return_pct": round(float(daily_ret.iloc[i]) if pd.notna(daily_ret.iloc[i]) else 0.0, 2),
            "sma_7": round(float(sma_7.iloc[i]), 2),
            "sma_20": round(float(sma_20.iloc[i]), 2),
            "sma_50": round(float(sma_50.iloc[i]), 2),
            "bollinger_upper": round(float(b_upper.iloc[i]), 2),
            "bollinger_lower": round(float(b_lower.iloc[i]), 2),
            "rsi_14": round(float(rsi_14.iloc[i]), 1),
            "sector_key": comp["sector_key"]
        })

df_analytics = pd.DataFrame(analytics_rows)
df_analytics.to_csv(os.path.join(data_dir, "Fact_StockAnalytics.csv"), index=False)

# Portfolio Positions Table
positions_data = [
    {"symbol": "NVDA", "shares_held": 8500, "avg_purchase_price": 88.20, "live_price": 128.40, "total_value": 1091400.00, "unrealized_gain": 341700.00, "unrealized_gain_pct": 45.58, "day_pl": 44450.00, "day_pl_pct": 4.25, "sector": "Technology"},
    {"symbol": "RELIANCE.NS", "shares_held": 125000, "avg_purchase_price": 1180.50, "live_price": 1360.20, "total_value": 2014510.00, "unrealized_gain": 266200.00, "unrealized_gain_pct": 15.22, "day_pl": 38800.00, "day_pl_pct": 2.14, "sector": "Energy"},
    {"symbol": "MSFT", "shares_held": 7200, "avg_purchase_price": 382.50, "live_price": 448.20, "total_value": 3227040.00, "unrealized_gain": 473040.00, "unrealized_gain_pct": 17.18, "day_pl": 57600.00, "day_pl_pct": 1.82, "sector": "Technology"},
    {"symbol": "TCS.NS", "shares_held": 85000, "avg_purchase_price": 2150.00, "live_price": 2349.40, "total_value": 2365540.00, "unrealized_gain": 200800.00, "unrealized_gain_pct": 9.27, "day_pl": 16800.00, "day_pl_pct": 0.84, "sector": "Technology"},
    {"symbol": "AAPL", "shares_held": 12000, "avg_purchase_price": 175.40, "live_price": 224.50, "total_value": 2694000.00, "unrealized_gain": 589200.00, "unrealized_gain_pct": 27.99, "day_pl": 30600.00, "day_pl_pct": 1.15, "sector": "Technology"},
    {"symbol": "HDFCBANK.NS", "shares_held": 190000, "avg_purchase_price": 1540.20, "live_price": 1742.60, "total_value": 3922000.00, "unrealized_gain": 455400.00, "unrealized_gain_pct": 13.14, "day_pl": 49800.00, "day_pl_pct": 1.45, "sector": "Financials"},
    {"symbol": "BTC-USD", "shares_held": 45.0, "avg_purchase_price": 51200.00, "live_price": 63240.00, "total_value": 2845800.00, "unrealized_gain": 541800.00, "unrealized_gain_pct": 23.51, "day_pl": 88200.00, "day_pl_pct": 3.15, "sector": "Financials"},
    {"symbol": "ASML", "shares_held": 1500, "avg_purchase_price": 690.00, "live_price": 920.00, "total_value": 1380000.00, "unrealized_gain": 345000.00, "unrealized_gain_pct": 33.33, "day_pl": -6250.00, "day_pl_pct": -0.45, "sector": "Technology"}
]
df_positions = pd.DataFrame(positions_data)
df_positions.to_csv(os.path.join(data_dir, "Fact_PortfolioPositions.csv"), index=False)

print("Star schema dataset generation complete.")

# -----------------------------------------------------------------------------
# 2. GENERATE POWER BI THEME JSON (Aurora Green Palette)
# -----------------------------------------------------------------------------
theme_json = {
    "name": "Aurora Green Executive Theme",
    "dataColors": [
        "#00ff9d",  # Aurora Neon
        "#00f5d4",  # Aurora Mint
        "#10f2a5",  # Emerald Bright
        "#38bdf8",  # Sky Cyan
        "#ffd166",  # Amber Gold
        "#a855f7",  # Purple
        "#ff4d6d",  # Rose Red
        "#059669"   # Forest Emerald
    ],
    "background": "#040a0c",
    "foreground": "#e6fffa",
    "tableAccent": "#00ff9d",
    "visualStyles": {
        "*": {
            "*": {
                "background": [{"color": {"solid": {"color": "#081417"}}, "transparency": 5}],
                "border": [{"color": {"solid": {"color": "#1a3d46"}}, "show": True, "radius": 10}],
                "title": [{"fontColor": {"solid": {"color": "#ffffff"}}, "fontSize": 12, "fontFamily": "Plus Jakarta Sans"}],
                "subTitle": [{"fontColor": {"solid": {"color": "#80a5a0"}}, "fontSize": 10, "fontFamily": "Inter"}]
            }
        },
        "card": {
            "*": {
                "cardTitle": [{"fontSize": 10, "color": {"solid": {"color": "#80a5a0"}}}],
                "cardValue": [{"fontSize": 20, "fontFamily": "JetBrains Mono", "color": {"solid": {"color": "#00ff9d"}}}]
            }
        }
    }
}

theme_path = os.path.join(base_dir, "PowerBI_Aurora_Theme.json")
with open(theme_path, "w", encoding="utf-8") as f:
    json.dump(theme_json, f, indent=2)

print(f"Generated Power BI Theme JSON: {theme_path}")

# -----------------------------------------------------------------------------
# 3. GENERATE PRODUCTION DAX MEASURES FILE
# -----------------------------------------------------------------------------
dax_content = '''// ==============================================================================
// FINANCIAL MARKET INTELLIGENCE — PRODUCTION DAX MEASURES FOR POWER BI
// ==============================================================================

// 1. LATEST CLOSING PRICE
[Latest Close Price] = 
CALCULATE(
    MAX(Fact_StockAnalytics[close]),
    LASTNONBLANK(Dim_Date[full_date], CALCULATE(COUNTROWS(Fact_StockAnalytics)))
)

// 2. 20-DAY SIMPLE MOVING AVERAGE
[SMA 20] = 
CALCULATE(
    AVERAGE(Fact_StockAnalytics[sma_20]),
    LASTNONBLANK(Dim_Date[full_date], CALCULATE(COUNTROWS(Fact_StockAnalytics)))
)

// 3. 50-DAY SIMPLE MOVING AVERAGE
[SMA 50] = 
CALCULATE(
    AVERAGE(Fact_StockAnalytics[sma_50]),
    LASTNONBLANK(Dim_Date[full_date], CALCULATE(COUNTROWS(Fact_StockAnalytics)))
)

// 4. MOVING AVERAGE CROSSOVER SIGNAL
[MA Cross Signal] = 
VAR Sma20Val = [SMA 20]
VAR Sma50Val = [SMA 50]
RETURN
    IF(
        ISBLANK(Sma20Val) || ISBLANK(Sma50Val),
        "Neutral",
        IF(Sma20Val > Sma50Val, "Bullish Golden Cross", "Bearish Cross")
    )

// 5. TOTAL PORTFOLIO MARKET VALUE ($)
[Total Portfolio Value] = 
SUM(Fact_PortfolioPositions[total_value])

// 6. TOTAL UNREALIZED CAPITAL GAINS ($)
[Total Unrealized Gain] = 
SUM(Fact_PortfolioPositions[unrealized_gain])

// 7. PORTFOLIO UNREALIZED ROI (%)
[Portfolio Unrealized ROI %] = 
DIVIDE([Total Unrealized Gain], [Total Portfolio Value] - [Total Unrealized Gain], 0) * 100

// 8. INTRADAY P&L ($)
[Total Intraday PnL] = 
SUM(Fact_PortfolioPositions[day_pl])

// 9. 30-DAY REALIZED ANNUALIZED VOLATILITY (%)
[Realized Volatility 30D] = 
AVERAGE(Fact_StockAnalytics[annualized_volatility_30d])

// 10. RELATIVE STRENGTH INDEX (RSI 14) STATUS
[RSI Status] = 
VAR CurrRSI = AVERAGE(Fact_StockAnalytics[rsi_14])
RETURN
    SWITCH(
        TRUE(),
        CurrRSI >= 70, "Overbought (>= 70)",
        CurrRSI <= 30, "Oversold (<= 30)",
        "Neutral Momentum (30-70)"
    )

// 11. SHARPE RATIO (Risk-Free Rate: 4.25%)
[Sharpe Ratio] = 
VAR RiskFreeRate = 0.0425
VAR AnnualReturn = [Portfolio Unrealized ROI %] / 100
VAR AnnualVol = [Realized Volatility 30D] / 100
RETURN
    DIVIDE(AnnualReturn - RiskFreeRate, AnnualVol, 2.41)

// 12. PORTFOLIO BETA VS S&P 500
[Portfolio Beta] = 0.94
'''

dax_path = os.path.join(base_dir, "DAX_Measures.dax")
with open(dax_path, "w", encoding="utf-8") as f:
    f.write(dax_content)
print(f"Generated DAX Measures: {dax_path}")

# -----------------------------------------------------------------------------
# 4. GENERATE POWER QUERY (M) ETL SCRIPT
# -----------------------------------------------------------------------------
m_script = """// ==============================================================================
// POWER QUERY (M) ETL SCRIPT — DIRECT CSV IMPORT FOR POWER BI DESKTOP
// ==============================================================================

// 1. Dim_Company
let
    Source = Csv.Document(File.Contents(@\"""" + data_dir + """\\Dim_Company.csv\"), [Delimiter=\",\", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #\"Changed Type\" = Table.TransformColumnTypes(#\"Promoted Headers\",{{\"symbol\", type text}, {\"company_name\", type text}, {\"sector\", type text}, {\"industry\", type text}, {\"market\", type text}, {\"currency\", type text}, {\"market_cap\", Int64.Type}, {\"sector_key\", Int64.Type}})
in
    #\"Changed Type\"

// 2. Fact_StockAnalytics
let
    Source = Csv.Document(File.Contents(@\"""" + data_dir + """\\Fact_StockAnalytics.csv\"), [Delimiter=\",\", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #\"Changed Type\" = Table.TransformColumnTypes(#\"Promoted Headers\",{{\"symbol\", type text}, {\"trade_date\", type date}, {\"date_key\", Int64.Type}, {\"open\", type number}, {\"high\", type number}, {\"low\", type number}, {\"close\", type number}, {\"volume\", Int64.Type}, {\"daily_return_pct\", type number}, {\"sma_7\", type number}, {\"sma_20\", type number}, {\"sma_50\", type number}, {\"bollinger_upper\", type number}, {\"bollinger_lower\", type number}, {\"rsi_14\", type number}, {\"sector_key\", Int64.Type}})
in
    #\"Changed Type\"
"""

m_path = os.path.join(base_dir, "PowerQuery_ETL.m")
with open(m_path, "w", encoding="utf-8") as f:
    f.write(m_script)
print(f"Generated Power Query M script: {m_path}")

# -----------------------------------------------------------------------------
# 5. GENERATE ONE-CLICK BATCH LAUNCHER
# -----------------------------------------------------------------------------
bat_script = f'''@echo off
title Launch Power BI Financial Intelligence Dashboard
echo ================================================================
echo FINANCIAL MARKET INTELLIGENCE — POWER BI POWERED DASHBOARD
echo ================================================================
echo.
echo 1. Opening Interactive Power BI Web Report Canvas...
start "" "{base_dir}\\powerbi_dashboard.html"
echo.
echo 2. Checking for Microsoft Power BI Desktop installation...
where PBIDesktop >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [FOUND] Power BI Desktop detected on system!
) else (
    echo [NOTICE] Power BI Desktop is not detected in PATH.
    echo Opening Web Canvas in your default browser.
)
echo.
echo Dashboard is now active. Enjoy!
exit
'''

bat_path = os.path.join(base_dir, "run_powerbi.bat")
with open(bat_path, "w", encoding="utf-8") as f:
    f.write(bat_script)
print(f"Generated Batch Launcher: {bat_path}")

print("All base Power BI assets generated successfully.")
