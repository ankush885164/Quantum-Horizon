"""
Enrich full_dashboard_data.json with live multi-market data (Indian, Forex, Crypto, Global).
"""

import json
import os
import numpy as np
import pandas as pd
import yfinance as yf

symbols_meta = {
    # Indian Equities
    "RELIANCE.NS": {"name": "Reliance Industries Ltd", "market": "Indian", "currency": "₹"},
    "TCS.NS": {"name": "Tata Consultancy Services Ltd", "market": "Indian", "currency": "₹"},
    "HDFCBANK.NS": {"name": "HDFC Bank Ltd", "market": "Indian", "currency": "₹"},
    "INFY.NS": {"name": "Infosys Ltd", "market": "Indian", "currency": "₹"},
    "ICICIBANK.NS": {"name": "ICICI Bank Ltd", "market": "Indian", "currency": "₹"},
    "SBIN.NS": {"name": "State Bank of India", "market": "Indian", "currency": "₹"},
    "BHARTIARTL.NS": {"name": "Bharti Airtel Ltd", "market": "Indian", "currency": "₹"},
    "ITC.NS": {"name": "ITC Ltd", "market": "Indian", "currency": "₹"},
    "NTPC.NS": {"name": "NTPC Ltd", "market": "Indian", "currency": "₹"},
    # Forex
    "USDINR=X": {"name": "USD / INR (US Dollar to Rupee)", "market": "Forex", "currency": "₹"},
    "EURINR=X": {"name": "EUR / INR (Euro to Rupee)", "market": "Forex", "currency": "₹"},
    "GBPINR=X": {"name": "GBP / INR (Pound to Rupee)", "market": "Forex", "currency": "₹"},
    "EURUSD=X": {"name": "EUR / USD (Euro to Dollar)", "market": "Forex", "currency": "$"},
    "GBPUSD=X": {"name": "GBP / USD (Pound to Dollar)", "market": "Forex", "currency": "$"},
    "USDJPY=X": {"name": "USD / JPY (Dollar to Yen)", "market": "Forex", "currency": "¥"},
    # Crypto
    "BTC-USD": {"name": "Bitcoin", "market": "Crypto", "currency": "$"},
    "ETH-USD": {"name": "Ethereum", "market": "Crypto", "currency": "$"},
    "SOL-USD": {"name": "Solana", "market": "Crypto", "currency": "$"},
    "BNB-USD": {"name": "Binance Coin", "market": "Crypto", "currency": "$"},
    "DOGE-USD": {"name": "Dogecoin", "market": "Crypto", "currency": "$"},
    "XRP-USD": {"name": "Ripple", "market": "Crypto", "currency": "$"},
    # Global Indices
    "^NSEI": {"name": "NIFTY 50 Index", "market": "Global", "currency": "₹"},
    "^BSESN": {"name": "S&P BSE SENSEX", "market": "Global", "currency": "₹"},
    "AAPL": {"name": "Apple Inc.", "market": "Global", "currency": "$"},
    "NVDA": {"name": "NVIDIA Corporation", "market": "Global", "currency": "$"},
}

data_file = "financial-market-intelligence/04_dashboard/full_dashboard_data.json"
with open(data_file, "r") as f:
    master_data = json.load(f)

multi_market_dict = {}
all_symbols = list(symbols_meta.keys())
print(f"Downloading historical 3-month data for {len(all_symbols)} multi-market instruments...")

raw = yf.download(all_symbols, period="3mo", interval="1d", group_by="ticker", threads=True)

for sym, meta in symbols_meta.items():
    try:
        if len(all_symbols) == 1:
            df = raw.copy()
        else:
            df = raw[sym].dropna(how="all").copy()

        if df.empty or len(df) < 5:
            continue

        df = df.dropna(subset=["Close"]).copy()
        dates = df.index.strftime("%Y-%m-%d").tolist()

        closes = [round(float(x), 4 if meta["market"] == "Forex" else 2) for x in df["Close"]]
        opens = [round(float(x), 4 if meta["market"] == "Forex" else 2) for x in df["Open"]]
        highs = [round(float(x), 4 if meta["market"] == "Forex" else 2) for x in df["High"]]
        lows = [round(float(x), 4 if meta["market"] == "Forex" else 2) for x in df["Low"]]
        volumes = [int(x) if not np.isnan(x) else 0 for x in df["Volume"]]

        # Indicators
        s_close = pd.Series(closes)
        sma20 = [round(float(x), 2) for x in s_close.rolling(20, min_periods=1).mean()]
        sma50 = [round(float(x), 2) for x in s_close.rolling(50, min_periods=1).mean()]

        delta = s_close.diff()
        gain = delta.where(delta > 0, 0).rolling(14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14, min_periods=1).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = [round(float(x), 1) for x in (100 - (100 / (1 + rs))).fillna(50)]

        std20 = s_close.rolling(20, min_periods=1).std().fillna(0)
        bb_up = [round(float(m + 2 * s), 2) for m, s in zip(sma20, std20)]
        bb_lo = [round(float(m - 2 * s), 2) for m, s in zip(sma20, std20)]

        multi_market_dict[sym] = {
            "name": meta["name"],
            "market": meta["market"],
            "currency": meta["currency"],
            "dates": dates,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "sma_20": sma20,
            "sma_50": sma50,
            "rsi_14": rsi,
            "bollinger_upper": bb_up,
            "bollinger_lower": bb_lo,
        }
    except Exception as e:
        print(f"Error processing {sym}: {e}")

master_data["multi_market"] = multi_market_dict

with open(data_file, "w") as f:
    json.dump(master_data, f)

# Also update dashboard_data.js
with open("financial-market-intelligence/04_dashboard/dashboard_data.js", "w") as f:
    f.write("window.MARKET_DATA = " + json.dumps(master_data) + ";")

print(f"Successfully enriched {data_file} with {len(multi_market_dict)} live multi-market instruments!")
