# -*- coding: utf-8 -*-
"""
Generate 10-Year Global Multi-Asset Star Schema Datasets
Spanning 2015 to 2025/2026 across major world equity markets:
- US Mega-Tech & Wall Street
- Indian NSE Blue Chips
- European Industry Leaders
- Asia-Pacific Semiconductors & Manufacturing
- Global Macro Commodities & Safe Havens
- Digital Assets & Cryptocurrencies
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

output_dir = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\data"
os.makedirs(output_dir, exist_ok=True)

# 1. Dim_GlobalMarket.csv
markets = [
    {"market_key": 1, "market_code": "US", "exchange_name": "NASDAQ / NYSE", "country": "United States", "region": "North America", "currency": "USD", "trading_hours": "09:30 - 16:00 EST"},
    {"market_key": 2, "market_code": "NSE", "exchange_name": "National Stock Exchange of India", "country": "India", "region": "Asia-Pacific", "currency": "INR", "trading_hours": "09:15 - 15:30 IST"},
    {"market_key": 3, "market_code": "EUR", "exchange_name": "Euronext / Deutsche Börse / LSE", "country": "European Union / UK", "region": "Europe", "currency": "EUR/GBP", "trading_hours": "08:00 - 16:30 GMT"},
    {"market_key": 4, "market_code": "APAC", "exchange_name": "Tokyo / Taiwan / Hong Kong", "country": "Japan / Taiwan / HK", "region": "Asia-Pacific", "currency": "JPY/TWD/HKD", "trading_hours": "09:00 - 15:00 JST"},
    {"market_key": 5, "market_code": "MACRO", "exchange_name": "NYMEX / COMEX / Treasury", "country": "Global", "region": "Global Macro", "currency": "USD", "trading_hours": "24 Hours Global"},
    {"market_key": 6, "market_code": "CRYPTO", "exchange_name": "Decentralized Liquidity & Global CEX", "country": "Global Digital", "region": "Global Digital", "currency": "USD", "trading_hours": "24/7/365 Continuous"},
]
df_markets = pd.DataFrame(markets)
df_markets.to_csv(os.path.join(output_dir, "Dim_GlobalMarket.csv"), index=False)
print("Saved Dim_GlobalMarket.csv")

# 2. Dim_Company_10Y.csv
companies = [
    # US Tech & Mega-Caps
    {"symbol": "NVDA", "company_name": "NVIDIA Corporation", "sector": "Semiconductors & AI", "market_code": "US", "region": "North America", "market_cap_b": 3420.0, "currency": "USD", "ten_year_cagr": 49.1, "max_drawdown": -66.4, "ten_year_return": 5326.0, "sharpe": 1.48},
    {"symbol": "AAPL", "company_name": "Apple Inc.", "sector": "Technology & Hardware", "market_code": "US", "region": "North America", "market_cap_b": 3520.0, "currency": "USD", "ten_year_cagr": 24.8, "max_drawdown": -38.5, "ten_year_return": 818.0, "sharpe": 1.15},
    {"symbol": "MSFT", "company_name": "Microsoft Corporation", "sector": "Software & Cloud", "market_code": "US", "region": "North America", "market_cap_b": 3150.0, "currency": "USD", "ten_year_cagr": 26.2, "max_drawdown": -37.1, "ten_year_return": 925.0, "sharpe": 1.22},
    {"symbol": "AMZN", "company_name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "market_code": "US", "region": "North America", "market_cap_b": 2210.0, "currency": "USD", "ten_year_cagr": 25.1, "max_drawdown": -56.2, "ten_year_return": 840.0, "sharpe": 0.98},
    {"symbol": "GOOGL", "company_name": "Alphabet Inc.", "sector": "Communication Services", "market_code": "US", "region": "North America", "market_cap_b": 2180.0, "currency": "USD", "ten_year_cagr": 20.4, "max_drawdown": -44.6, "ten_year_return": 540.0, "sharpe": 1.05},
    {"symbol": "TSLA", "company_name": "Tesla Inc.", "sector": "Automotive & Energy", "market_code": "US", "region": "North America", "market_cap_b": 1120.0, "currency": "USD", "ten_year_cagr": 42.5, "max_drawdown": -73.6, "ten_year_return": 3120.0, "sharpe": 0.88},
    {"symbol": "JPM", "company_name": "JPMorgan Chase & Co.", "sector": "Financial Services", "market_code": "US", "region": "North America", "market_cap_b": 690.0, "currency": "USD", "ten_year_cagr": 16.8, "max_drawdown": -43.6, "ten_year_return": 372.0, "sharpe": 0.82},

    # Indian Equities (NSE)
    {"symbol": "RELIANCE.NS", "company_name": "Reliance Industries Ltd", "sector": "Energy & Conglomerate", "market_code": "NSE", "region": "Asia-Pacific", "market_cap_b": 220.0, "currency": "INR", "ten_year_cagr": 20.3, "max_drawdown": -44.2, "ten_year_return": 535.6, "sharpe": 0.95},
    {"symbol": "TCS.NS", "company_name": "Tata Consultancy Services", "sector": "Information Technology", "market_code": "NSE", "region": "Asia-Pacific", "market_cap_b": 175.0, "currency": "INR", "ten_year_cagr": 17.5, "max_drawdown": -30.5, "ten_year_return": 402.0, "sharpe": 1.02},
    {"symbol": "HDFCBANK.NS", "company_name": "HDFC Bank Ltd", "sector": "Financial Services", "market_code": "NSE", "region": "Asia-Pacific", "market_cap_b": 162.0, "currency": "INR", "ten_year_cagr": 16.2, "max_drawdown": -38.2, "ten_year_return": 350.0, "sharpe": 0.89},
    {"symbol": "INFY.NS", "company_name": "Infosys Ltd", "sector": "Information Technology", "market_code": "NSE", "region": "Asia-Pacific", "market_cap_b": 88.0, "currency": "INR", "ten_year_cagr": 16.9, "max_drawdown": -36.8, "ten_year_return": 378.0, "sharpe": 0.92},
    {"symbol": "ICICIBANK.NS", "company_name": "ICICI Bank Ltd", "sector": "Financial Services", "market_code": "NSE", "region": "Asia-Pacific", "market_cap_b": 110.0, "currency": "INR", "ten_year_cagr": 18.9, "max_drawdown": -46.5, "ten_year_return": 465.0, "sharpe": 0.88},
    {"symbol": "BHARTIARTL.NS", "company_name": "Bharti Airtel Ltd", "sector": "Telecommunications", "market_code": "NSE", "region": "Asia-Pacific", "market_cap_b": 125.0, "currency": "INR", "ten_year_cagr": 19.4, "max_drawdown": -42.0, "ten_year_return": 488.0, "sharpe": 0.91},

    # European Blue Chips
    {"symbol": "ASML", "company_name": "ASML Holding NV", "sector": "Semiconductors (Lithography)", "market_code": "EUR", "region": "Europe", "market_cap_b": 380.0, "currency": "EUR", "ten_year_cagr": 29.6, "max_drawdown": -54.2, "ten_year_return": 1236.8, "sharpe": 1.12},
    {"symbol": "SAP.DE", "company_name": "SAP SE", "sector": "Enterprise Software", "market_code": "EUR", "region": "Europe", "market_cap_b": 280.0, "currency": "EUR", "ten_year_cagr": 15.8, "max_drawdown": -48.5, "ten_year_return": 334.0, "sharpe": 0.78},
    {"symbol": "MC.PA", "company_name": "LVMH Moët Hennessy", "sector": "Luxury Goods & Consumer", "market_code": "EUR", "region": "Europe", "market_cap_b": 360.0, "currency": "EUR", "ten_year_cagr": 18.2, "max_drawdown": -41.0, "ten_year_return": 432.0, "sharpe": 0.86},
    {"symbol": "SHEL.L", "company_name": "Shell plc", "sector": "Energy & Oil", "market_code": "EUR", "region": "Europe", "market_cap_b": 210.0, "currency": "GBP", "ten_year_cagr": 8.4, "max_drawdown": -64.5, "ten_year_return": 124.0, "sharpe": 0.45},

    # Asia-Pacific Titans
    {"symbol": "TSM", "company_name": "Taiwan Semiconductor Mfg", "sector": "Semiconductor Foundry", "market_code": "APAC", "region": "Asia-Pacific", "market_cap_b": 980.0, "currency": "USD", "ten_year_cagr": 28.5, "max_drawdown": -58.2, "ten_year_return": 1135.0, "sharpe": 1.08},
    {"symbol": "005930.KS", "company_name": "Samsung Electronics", "sector": "Memory & Electronics", "market_code": "APAC", "region": "Asia-Pacific", "market_cap_b": 320.0, "currency": "KRW", "ten_year_cagr": 11.2, "max_drawdown": -44.0, "ten_year_return": 189.0, "sharpe": 0.58},
    {"symbol": "7203.T", "company_name": "Toyota Motor Corp", "sector": "Automotive", "market_code": "APAC", "region": "Asia-Pacific", "market_cap_b": 280.0, "currency": "JPY", "ten_year_cagr": 10.5, "max_drawdown": -35.2, "ten_year_return": 171.0, "sharpe": 0.62},
    {"symbol": "BHP.AX", "company_name": "BHP Group Ltd", "sector": "Materials & Mining", "market_code": "APAC", "region": "Asia-Pacific", "market_cap_b": 150.0, "currency": "AUD", "ten_year_cagr": 9.8, "max_drawdown": -58.0, "ten_year_return": 155.0, "sharpe": 0.52},

    # Global Macro & Commodities
    {"symbol": "^GSPC", "company_name": "S&P 500 Index (Benchmark)", "sector": "Global Equity Benchmark", "market_code": "MACRO", "region": "Global Macro", "market_cap_b": 48000.0, "currency": "USD", "ten_year_cagr": 12.1, "max_drawdown": -34.0, "ten_year_return": 212.2, "sharpe": 0.85},
    {"symbol": "^NSEI", "company_name": "NIFTY 50 Index (Benchmark)", "sector": "Indian Benchmark", "market_code": "MACRO", "region": "Global Macro", "market_cap_b": 4200.0, "currency": "INR", "ten_year_cagr": 12.6, "max_drawdown": -38.4, "ten_year_return": 228.4, "sharpe": 0.82},
    {"symbol": "GC=F", "company_name": "Gold Commodity Futures", "sector": "Precious Metals Safe Haven", "market_code": "MACRO", "region": "Global Macro", "market_cap_b": 16000.0, "currency": "USD", "ten_year_cagr": 11.6, "max_drawdown": -21.5, "ten_year_return": 198.4, "sharpe": 0.86},
    {"symbol": "CL=F", "company_name": "Crude Oil (WTI)", "sector": "Energy Commodities", "market_code": "MACRO", "region": "Global Macro", "market_cap_b": 2500.0, "currency": "USD", "ten_year_cagr": 3.8, "max_drawdown": -120.0, "ten_year_return": 45.0, "sharpe": 0.22},

    # Digital Assets
    {"symbol": "BTC-USD", "company_name": "Bitcoin Core Treasury", "sector": "Decentralized Digital Gold", "market_code": "CRYPTO", "region": "Global Digital", "market_cap_b": 1880.0, "currency": "USD", "ten_year_cagr": 55.4, "max_drawdown": -84.0, "ten_year_return": 8122.5, "sharpe": 1.25},
    {"symbol": "ETH-USD", "company_name": "Ethereum Smart Contracts", "sector": "Decentralized Computing", "market_code": "CRYPTO", "region": "Global Digital", "market_cap_b": 380.0, "currency": "USD", "ten_year_cagr": 64.2, "max_drawdown": -94.0, "ten_year_return": 14200.0, "sharpe": 1.15},
]
df_companies = pd.DataFrame(companies)
df_companies.to_csv(os.path.join(output_dir, "Dim_Company_10Y.csv"), index=False)
print("Saved Dim_Company_10Y.csv")

# 3. Fact_10Y_PerformanceSummary.csv
df_companies.to_csv(os.path.join(output_dir, "Fact_10Y_PerformanceSummary.csv"), index=False)
print("Saved Fact_10Y_PerformanceSummary.csv")

# 4. Dim_Date_10Y.csv (2015 to 2026 weekly/daily calendar)
start_date = datetime(2015, 1, 1)
end_date = datetime(2026, 11, 21)
date_range = pd.date_range(start=start_date, end=end_date, freq="W-FRI")

date_records = []
for idx, d in enumerate(date_range):
    date_records.append({
        "date_key": int(d.strftime("%Y%m%d")),
        "full_date": d.strftime("%Y-%m-%d"),
        "year": d.year,
        "quarter": f"Q{(d.month - 1) // 3 + 1}",
        "month": d.month,
        "month_name": d.strftime("%B"),
        "week_number": d.isocalendar()[1],
        "is_stress_crisis_period": 1 if (
            (d.year == 2015 and d.month >= 8) or
            (d.year == 2020 and d.month in [2, 3, 4]) or
            (d.year == 2022 and d.month in [1, 2, 3, 4, 5, 6, 9, 10])
        ) else 0,
        "crisis_label": (
            "2015-16 Oil Deflation & Yuan Shock" if (d.year == 2015 and d.month >= 8) else
            "2020 COVID-19 Flash Crash" if (d.year == 2020 and d.month in [2, 3, 4]) else
            "2022 Global Inflation & Rate Hike Shock" if (d.year == 2022 and d.month in [1, 2, 3, 4, 5, 6, 9, 10]) else
            "Nominal Expansion"
        )
    })
df_dates = pd.DataFrame(date_records)
df_dates.to_csv(os.path.join(output_dir, "Dim_Date_10Y.csv"), index=False)
print("Saved Dim_Date_10Y.csv")

print("All 10-Year Global Lakehouse Datamarts compiled successfully!")
