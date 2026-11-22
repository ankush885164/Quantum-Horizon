"""
Financial Market Intelligence — Production Multi-Asset Terminal & Lakehouse Analytics
Medallion Architecture (Bronze -> Silver -> Gold) & Real-Time Intelligence
"""

import os
import glob
import time
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# ==============================================================================
# 1. PAGE SETUP & CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Financial Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme State Management
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# Theme Colors - Quantum Horizon & Holographic Amethyst
BG_COLOR = "#070913" if IS_DARK else "#ffffff"
BG_SUBTLE = "#0a0e20" if IS_DARK else "#f8fafc"
CARD_BG = "#0e142c" if IS_DARK else "#ffffff"
BORDER_COLOR = "#1e294b" if IS_DARK else "#e2e8f0"
BORDER_SUBTLE = "#141c38" if IS_DARK else "#f1f5f9"
TEXT_COLOR = "#f8fafc" if IS_DARK else "#09090b"
TEXT_MUTED = "#94a3b8" if IS_DARK else "#64748b"
ACCENT = "#818cf8"
ACCENT_CYAN = "#00f0ff"
ACCENT_GREEN = "#10b981" if IS_DARK else "#16a34a"
ACCENT_RED = "#f43f5e" if IS_DARK else "#dc2626"
ACCENT_AMBER = "#fbbf24" if IS_DARK else "#d97706"
ACCENT_FUCHSIA = "#ec4899"

# Inject Global CSS - Fixing all popovers, dropdown overlaps, and spacing
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=JetBrains+Mono:wght@400;600;700&display=swap');

    /* Completely remove Streamlit's default top header, black bar, toolbar, decorations, and footer */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    header,
    [data-testid="stDecoration"],
    [data-testid="stToolbar"],
    #MainMenu,
    footer {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        visibility: hidden !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        pointer-events: none !important;
    }}

    /* Main App Background & Typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, section[data-testid="stMain"] {{
        background: radial-gradient(circle at 12% 10%, rgba(99, 102, 241, 0.16) 0%, transparent 45%),
                    radial-gradient(circle at 88% 85%, rgba(244, 63, 94, 0.12) 0%, transparent 45%),
                    radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 55%),
                    #070913 !important;
        background-color: {BG_COLOR} !important;
        color: {TEXT_COLOR} !important;
        font-family: 'DM Sans', -apple-system, sans-serif !important;
    }}

    /* Provide comfortable top padding so headers and readable content are never cut off */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1400px !important;
    }}

    /* Position the collapsed sidebar toggle button cleanly at top-left */
    [data-testid="collapsedControl"] {{
        display: flex !important;
        position: fixed !important;
        top: 12px !important;
        left: 12px !important;
        z-index: 999999 !important;
        background: rgba(14, 20, 44, 0.9) !important;
        border: 1px solid rgba(129, 140, 248, 0.4) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(12px) !important;
        color: #f8fafc !important;
        padding: 5px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5) !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {BG_SUBTLE} !important;
        border-right: 1px solid {BORDER_COLOR} !important;
        padding-top: 0.75rem !important;
    }}

    /* Prevent dropdown popover clipping and overlap */
    div[data-baseweb="popover"], div[data-baseweb="menu"], [data-baseweb="popover"] ul {{
        z-index: 999999 !important;
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }}
    div[data-baseweb="select"] {{
        z-index: 100 !important;
    }}

    /* Generous Spacing for Streamlit Elements */
    .stSelectbox, .stTextInput, .stRadio, .stCheckbox {{
        margin-bottom: 0.5rem !important;
    }}
    div[data-testid="stHorizontalBlock"] {{
        gap: 0.85rem !important;
        align-items: flex-start !important;
    }}

    /* Laptop-Optimized Metric Cards */
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 10px;
        padding: 0.65rem 0.85rem;
        transition: transform 0.15s ease, border-color 0.15s ease;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .metric-card:hover {{
        border-color: {ACCENT};
    }}
    .metric-label {{
        font-size: 0.68rem;
        color: {TEXT_MUTED};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.15rem;
    }}
    .metric-value {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {TEXT_COLOR};
        letter-spacing: -0.02em;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.15;
    }}
    .metric-delta {{
        font-size: 0.76rem;
        font-weight: 600;
        margin-top: 0.35rem;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 7px;
        border-radius: 6px;
        width: fit-content;
    }}
    .delta-up {{
        color: {ACCENT_GREEN};
        background: {"rgba(34,197,94,0.12)" if IS_DARK else "rgba(22,163,74,0.08)"};
    }}
    .delta-down {{
        color: {ACCENT_RED};
        background: {"rgba(239,68,68,0.12)" if IS_DARK else "rgba(220,38,38,0.08)"};
    }}
    .delta-neutral {{
        color: {TEXT_MUTED};
        background: {"rgba(161,161,170,0.12)" if IS_DARK else "rgba(100,116,139,0.08)"};
    }}

    .live-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #22c55e;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse 1.5s infinite;
        margin-right: 6px;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(0.95); opacity: 0.7; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
        100% {{ transform: scale(0.95); opacity: 0.7; }}
    }}

    .search-panel {{
        background: {BG_SUBTLE};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.25rem;
    }}

    /* Custom Tables */
    .data-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.82rem;
    }}
    .data-table th {{
        text-align: left;
        padding: 0.65rem 0.9rem;
        color: {TEXT_MUTED};
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid {BORDER_COLOR};
        background: {BG_SUBTLE};
    }}
    .data-table td {{
        padding: 0.65rem 0.9rem;
        color: {TEXT_COLOR};
        border-bottom: 1px solid {BORDER_SUBTLE};
        font-family: 'JetBrains Mono', monospace;
    }}
    .data-table tr:hover td {{
        background: {BG_SUBTLE};
    }}
    
    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
    }}
    .badge-bullish {{ color: #10b981; background: rgba(16,185,129,0.18); border: 1px solid rgba(16,185,129,0.3); }}
    .badge-bearish {{ color: #f43f5e; background: rgba(244,63,94,0.18); border: 1px solid rgba(244,63,94,0.3); }}
    .badge-neutral {{ color: #00f0ff; background: rgba(0,240,255,0.18); border: 1px solid rgba(0,240,255,0.3); }}
    .badge-warn    {{ color: #fbbf24; background: rgba(251,191,36,0.18); border: 1px solid rgba(251,191,36,0.3); }}

    /* Custom Tabs with glowing indicator */
    button[data-baseweb="tab"] {{
        background: transparent !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }}
    button[data-baseweb="tab"]:hover {{
        color: #ffffff !important;
        background: rgba(129, 140, 248, 0.1) !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(6, 182, 212, 0.2)) !important;
        border: 1px solid rgba(129, 140, 248, 0.5) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25) !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: #818cf8 !important;
    }}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. MARKET PRESETS & DATA DEFINITIONS
# ==============================================================================
MARKET_PRESETS = {
    "🇺🇸 US Mega-Caps & Wall Street": {
        "NVDA": "NVIDIA Corporation (AI / GPU Compute)",
        "AAPL": "Apple Inc. (Consumer Tech & Ecosystem)",
        "MSFT": "Microsoft Corporation (Cloud & Enterprise)",
        "AMZN": "Amazon.com Inc. (E-Commerce & AWS)",
        "GOOGL": "Alphabet Inc. (Search & Gemini AI)",
        "META": "Meta Platforms Inc. (Social & Llama AI)",
        "TSLA": "Tesla Inc. (Autonomous & EV)",
        "BRK-B": "Berkshire Hathaway (Conglomerate)",
        "JPM": "JPMorgan Chase & Co. (Banking)",
        "V": "Visa Inc. (Global Payments)",
        "LLY": "Eli Lilly & Co. (Healthcare)",
        "XOM": "Exxon Mobil Corp. (Energy)",
    },
    "🇮🇳 Indian Blue Chips (NSE/BSE)": {
        "RELIANCE.NS": "Reliance Industries Ltd",
        "TCS.NS": "Tata Consultancy Services Ltd",
        "HDFCBANK.NS": "HDFC Bank Ltd",
        "INFY.NS": "Infosys Ltd",
        "ICICIBANK.NS": "ICICI Bank Ltd",
        "SBIN.NS": "State Bank of India",
        "BHARTIARTL.NS": "Bharti Airtel Ltd",
        "ITC.NS": "ITC Ltd",
        "NTPC.NS": "NTPC Ltd",
        "LT.NS": "Larsen & Toubro Ltd",
        "TATAMOTORS.NS": "Tata Motors Ltd",
        "ZOMATO.NS": "Zomato Ltd",
    },
    "🇪🇺 European Titans (Euronext / DAX / LSE)": {
        "ASML": "ASML Holding NV (Lithography Systems)",
        "SAP.DE": "SAP SE (Enterprise Cloud ERP)",
        "MC.PA": "LVMH Moët Hennessy (Global Luxury)",
        "SHEL.L": "Shell plc (Energy & Natural Gas)",
        "AZN.L": "AstraZeneca PLC (Biopharma)",
        "NESN.SW": "Nestlé SA (Consumer Defensive)",
    },
    "🌏 Asia-Pacific Leaders": {
        "TSM": "Taiwan Semiconductor Mfg (Foundry)",
        "005930.KS": "Samsung Electronics (Memory & Logic)",
        "7203.T": "Toyota Motor Corp (Automotive)",
        "9988.HK": "Alibaba Group (Cloud & Commerce)",
        "BHP.AX": "BHP Group Ltd (Global Mining)",
    },
    "🌐 Global Macro Benchmarks & Commodities": {
        "^GSPC": "S&P 500 Index (Wall Street Core)",
        "^NSEI": "NIFTY 50 Index (India)",
        "^FTSE": "FTSE 100 Index (London)",
        "^N225": "Nikkei 225 Index (Tokyo)",
        "GC=F": "Gold Futures (Global Safe Haven)",
        "CL=F": "Crude Oil WTI (Global Energy)",
        "SI=F": "Silver Futures (Precious & Industrial)",
        "^TNX": "US 10-Year Treasury Yield",
        "DX-Y.NYB": "US Dollar Index (DXY Currency Basket)",
    },
    "🪙 Digital Assets & Crypto": {
        "BTC-USD": "Bitcoin Core Treasury (BTC / USD)",
        "ETH-USD": "Ethereum Smart Contracts (ETH / USD)",
        "SOL-USD": "Solana High-Throughput (SOL / USD)",
        "BNB-USD": "Binance Coin (BNB / USD)",
        "XRP-USD": "Ripple (XRP / USD)",
        "DOGE-USD": "Dogecoin (DOGE / USD)",
    },
    "💱 Global Currencies & Forex": {
        "USDINR=X": "USD / INR (US Dollar to Indian Rupee)",
        "EURINR=X": "EUR / INR (Euro to Indian Rupee)",
        "GBPINR=X": "GBP / INR (British Pound to Indian Rupee)",
        "EURUSD=X": "EUR / USD (Euro to US Dollar)",
        "GBPUSD=X": "GBP / USD (British Pound to US Dollar)",
        "USDJPY=X": "USD / JPY (US Dollar to Japanese Yen)",
        "AUDUSD=X": "AUD / USD (Australian Dollar to US Dollar)",
        "USDCHF=X": "USD / CHF (US Dollar to Swiss Franc)",
    }
}


# ==============================================================================
# 3. LIVE MARKET DATA FETCHER (CACHED WITH SHORT TTL)
# ==============================================================================
@st.cache_data(ttl=15)
def fetch_live_market_series(ticker: str, period: str = "3mo"):
    """
    Fetches real-time price time-series using yfinance and computes
    moving averages, RSI, and Bollinger Bands dynamically.
    """
    try:
        t = yf.Ticker(ticker.strip().upper())
        if period == "1d":
            df = t.history(period="1d", interval="5m")
        elif period == "5d":
            df = t.history(period="5d", interval="15m")
        elif period == "1mo":
            df = t.history(period="1mo", interval="1d")
        elif period == "3mo":
            df = t.history(period="3mo", interval="1d")
        elif period == "6mo":
            df = t.history(period="6mo", interval="1d")
        elif period == "1y":
            df = t.history(period="1y", interval="1d")
        elif period == "5y":
            df = t.history(period="5y", interval="1wk")
        elif period == "10y":
            df = t.history(period="10y", interval="1wk")
        elif period == "max":
            df = t.history(period="max", interval="1mo")
        else:
            df = t.history(period="10y", interval="1wk")

        if df is None or df.empty:
            return None, None

        df.reset_index(inplace=True)
        date_col = "Datetime" if "Datetime" in df.columns else "Date"
        df["trade_date"] = pd.to_datetime(df[date_col])

        # Technical Indicators
        df["SMA_20"] = df["Close"].rolling(20, min_periods=1).mean()
        df["SMA_50"] = df["Close"].rolling(50, min_periods=1).mean()
        df["SMA_200"] = df["Close"].rolling(200, min_periods=1).mean()

        # 14-period RSI
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0).rolling(14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14, min_periods=1).mean()
        rs = gain / loss.replace(0, np.nan)
        df["RSI_14"] = 100 - (100 / (1 + rs))
        df["RSI_14"] = df["RSI_14"].fillna(50)

        # Bollinger Bands (20, 2)
        roll_std = df["Close"].rolling(20, min_periods=1).std().fillna(0)
        df["BB_Upper"] = df["SMA_20"] + (2 * roll_std)
        df["BB_Lower"] = df["SMA_20"] - (2 * roll_std)

        # Volatility
        df["daily_ret"] = df["Close"].pct_change()
        df["vol_30d"] = df["daily_ret"].rolling(30, min_periods=3).std() * np.sqrt(252) * 100
        df["vol_30d"] = df["vol_30d"].fillna(0)

        info = {}
        try:
            info = t.info or {}
        except Exception:
            info = {}

        return df, info
    except Exception as e:
        return None, None


# ==============================================================================
# 4. LAKEHOUSE DATA INGESTION (HISTORICAL GOLD MARTS)
# ==============================================================================
@st.cache_data(ttl=600)
def load_lakehouse_data():
    base_dirs = [
        os.path.join(os.path.dirname(__file__), "..", "03_dashboard_export", "exports"),
        os.path.join(os.path.dirname(__file__), "exports"),
        "financial-market-intelligence/03_dashboard_export/exports",
        "./exports",
    ]
    data_dir = None
    for d in base_dirs:
        if os.path.exists(d) and os.path.exists(os.path.join(d, "Fact_StockAnalytics.csv")):
            data_dir = os.path.abspath(d)
            break

    if not data_dir:
        return None, None, None, None, None

    df_stocks = pd.read_csv(os.path.join(data_dir, "Fact_StockAnalytics.csv"))
    df_market = pd.read_csv(os.path.join(data_dir, "Fact_MarketSummary.csv"))
    df_sector = pd.read_csv(os.path.join(data_dir, "Fact_SectorPerformance.csv"))
    df_company = pd.read_csv(os.path.join(data_dir, "Dim_Company.csv"))
    df_date = pd.read_csv(os.path.join(data_dir, "Dim_Date.csv"))

    df_stocks["trade_date"] = pd.to_datetime(df_stocks["trade_date"])
    df_market["trade_date"] = pd.to_datetime(df_market["trade_date"])
    df_sector["trade_date"] = pd.to_datetime(df_sector["trade_date"])
    df_date["full_date"] = pd.to_datetime(df_date["full_date"])

    df_stocks.sort_values(by=["symbol", "trade_date"], inplace=True)
    df_market.sort_values(by="trade_date", inplace=True)
    df_sector.sort_values(by=["sector", "trade_date"], inplace=True)

    return df_stocks, df_market, df_sector, df_company, df_date

df_stocks, df_market, df_sector, df_company, df_date = load_lakehouse_data()


# ==============================================================================
# 5. HELPER FUNCTIONS & PLOTLY STYLING
# ==============================================================================
def get_chart_layout(height=280):
    grid_color = "rgba(255,255,255,0.06)" if IS_DARK else "rgba(0,0,0,0.06)"
    return dict(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=TEXT_MUTED, size=11),
        margin=dict(l=15, r=15, t=35, b=25),
        xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, tickfont=dict(size=10, color=TEXT_MUTED)),
        yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, tickfont=dict(size=10, color=TEXT_MUTED)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=TEXT_MUTED),
            bgcolor="rgba(0,0,0,0)",
        ),
    )

def render_metric_card(label, value, delta=None, delta_type="up", subtext=None):
    delta_class = f"delta-{delta_type}"
    arrow = "▲" if delta_type == "up" else ("▼" if delta_type == "down" else "●")
    delta_html = f'<div class="metric-delta {delta_class}">{arrow} {delta}</div>' if delta else ""
    sub_html = f'<div style="font-size:0.72rem; color:{TEXT_MUTED}; margin-top:0.3rem;">{subtext}</div>' if subtext else ""
    return f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        <div>
            {delta_html}
            {sub_html}
        </div>
    </div>
    """


# ==============================================================================
# QUANTITATIVE INVESTMENT DECISION & RECOMMENDATION ENGINE
# ==============================================================================
def compute_investment_decision(price, sma20, sma50, sma200, rsi, cagr=None, max_dd=None, sharpe=None):
    score = 50
    catalysts = []
    risks = []

    # 1. Trend Analysis
    if price >= sma20:
        score += 8
        catalysts.append("Trading above 20 SMA (Short-term momentum is positive)")
    else:
        score -= 6
        risks.append("Trading below 20 SMA (Experiencing short-term pullback)")

    if price >= sma50:
        score += 10
        catalysts.append("Trading above 50 SMA (Intermediate trend remains upward)")
    else:
        score -= 8
        risks.append("Below 50 SMA (Medium-term resistance headwind)")

    if sma50 >= sma200:
        score += 12
        catalysts.append("Confirmed Golden Cross (50 SMA > 200 SMA secular bull structure)")
    else:
        score -= 10
        risks.append("Death Cross structure (50 SMA < 200 SMA macro consolidation)")

    # 2. RSI Momentum
    if 45 <= rsi <= 65:
        score += 10
        catalysts.append(f"RSI at {rsi:.1f} in optimal continuation zone (Healthy trend without exhaustion)")
    elif rsi < 35:
        score += 8
        catalysts.append(f"RSI at {rsi:.1f} in oversold zone (Contrarian value accumulation opportunity)")
    elif rsi > 75:
        score -= 8
        risks.append(f"RSI at {rsi:.1f} in overbought zone (Elevated near-term consolidation risk)")
    else:
        score += 4

    # 3. 10Y Compounding track record
    if cagr is not None:
        if cagr >= 25:
            score += 15
            catalysts.append(f"Decade CAGR of {cagr:.1f}% indicates top-tier global compounding power")
        elif cagr >= 12:
            score += 10
            catalysts.append(f"Decade CAGR of {cagr:.1f}% consistently outperforms broad market benchmark")
        elif cagr < 5:
            score -= 10
            risks.append(f"Low decade CAGR of {cagr:.1f}% lags inflation benchmarks")

    if sharpe is not None:
        if sharpe >= 1.2:
            score += 10
            catalysts.append(f"Sharpe Ratio of {sharpe:.2f} confirms superior risk-adjusted alpha")
        elif sharpe < 0.6:
            score -= 6
            risks.append(f"Low Sharpe Ratio ({sharpe:.2f}) indicates excess volatility per unit return")

    score = max(10, min(96, score))

    if score >= 80:
        verdict = "STRONG BUY"
        action = "High Conviction Accumulation • Overweight Core Portfolio"
        color = "#10b981" # Emerald
        bg = "rgba(16, 185, 129, 0.15)"
        border = "rgba(16, 185, 129, 0.4)"
        allocation = "7% - 12% Target Portfolio Allocation"
    elif score >= 65:
        verdict = "BUY / ACCUMULATE"
        action = "Scale In on Dips • Favorable Risk-Reward Setup"
        color = "#00f0ff" # Cyan
        bg = "rgba(0, 240, 255, 0.15)"
        border = "rgba(0, 240, 255, 0.4)"
        allocation = "4% - 7% Target Portfolio Allocation"
    elif score >= 50:
        verdict = "HOLD / NEUTRAL"
        action = "Maintain Existing Positions • Await Confirmed Breakout"
        color = "#fbbf24" # Amber
        bg = "rgba(251, 191, 36, 0.15)"
        border = "rgba(251, 191, 36, 0.4)"
        allocation = "2% - 4% Tactical Position"
    elif score >= 38:
        verdict = "TRIM / TAKE PROFITS"
        action = "Harvest Partial Gains • Tighten Trailing Stop-Loss"
        color = "#ec4899" # Fuchsia
        bg = "rgba(236, 72, 153, 0.15)"
        border = "rgba(236, 72, 153, 0.4)"
        allocation = "Underweight / Reduce Exposure"
    else:
        verdict = "AVOID / HIGH RISK"
        action = "Capital Preservation Priority • Avoid Initiating Longs"
        color = "#f43f5e" # Rose
        bg = "rgba(244, 63, 94, 0.15)"
        border = "rgba(244, 63, 94, 0.4)"
        allocation = "0% Allocation (Cash / Capital Preservation)"

    stop_loss = round(price * 0.92, 2)
    target_1y = round(price * 1.24, 2)
    entry_low = round(price * 0.97, 2)
    entry_high = round(price * 1.01, 2)

    return {
        "verdict": verdict,
        "score": score,
        "action": action,
        "color": color,
        "bg": bg,
        "border": border,
        "allocation": allocation,
        "entry_range": f"{entry_low} - {entry_high}",
        "target_1y": target_1y,
        "stop_loss": stop_loss,
        "catalysts": catalysts[:3],
        "risks": risks[:2] if risks else ["Normal market volatility applies (Set disciplined stop-losses)"]
    }


def format_currency_price(val, symbol: str):
    if val is None or np.isnan(val):
        return "N/A"
    sym = symbol.upper()
    if sym.endswith(".NS") or sym.endswith(".BO") or "INR=X" in sym:
        return f"₹{val:,.2f}"
    elif "-USD" in sym or sym.startswith("^") or "=" not in sym:
        if val >= 100:
            return f"${val:,.2f}"
        elif val >= 1:
            return f"${val:,.4f}"
        else:
            return f"${val:,.6f}"
    else:
        return f"{val:,.4f}"


# ==============================================================================
# 6. SIDEBAR CONTROLS (ELIMINATES UI OVERLAPS ON MAIN PAGE)
# ==============================================================================
with st.sidebar:
    st.markdown(f"### ⚙️ Terminal Controls")
    
    # Live Auto-Refresh Settings
    auto_refresh_sec = st.selectbox(
        "Live Feed Auto-Refresh",
        options=[0, 10, 30, 60],
        format_func=lambda s: "Auto-Refresh: Off" if s == 0 else f"Auto-Refresh: Every {s}s",
        index=0,
        help="Periodically pulls updated market prices automatically.",
    )

    st.markdown("---")
    st.markdown("### 📊 Indicator Overlays")
    show_ma20 = st.checkbox("Show 20 MA", value=True)
    show_ma50 = st.checkbox("Show 50 MA", value=True)
    show_ma200 = st.checkbox("Show 200 MA", value=True)
    show_bb = st.checkbox("Show Bollinger Bands", value=True)

    st.markdown("---")
    st.markdown("### 🏢 Lakehouse Metadata")
    st.caption(f"Trading Sessions: {len(df_market) if df_market is not None else 0}")
    st.caption(f"Curated Gold Records: {len(df_stocks):,}" if df_stocks is not None else "N/A")
    st.caption("Lakehouse Engine: Databricks & Delta Lake")

    st.markdown("---")
    theme_btn_label = "☀️ Light View" if IS_DARK else "🌙 Dark View"
    if st.button(theme_btn_label, use_container_width=True, on_click=toggle_theme):
        st.rerun()

# Trigger Auto-Refresh if enabled
if auto_refresh_sec > 0:
    st_autorefresh(interval=auto_refresh_sec * 1000, key="live_market_refresh")


# ==============================================================================
# 7. APP HEADER
# ==============================================================================
header_left, header_right = st.columns([8, 2], vertical_alignment="center")

with header_left:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.2rem;">
        <div style="background: linear-gradient(135deg, #6366f1, #00f0ff); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: #fff; font-weight: 700; box-shadow: 0 0 20px rgba(99, 102, 241, 0.45);">
            ⚡
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 700; margin: 0; padding: 0; letter-spacing: -0.02em; background: linear-gradient(135deg, #ffffff 40%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Quantum Horizon Terminal
            </h1>
            <p style="font-size: 0.8rem; color: {TEXT_MUTED}; margin: 2px 0 0 0;">
                <span class="live-dot" style="background-color:#00f0ff; box-shadow:0 0 10px #00f0ff;"></span><strong>Institutional Multi-Asset Intelligence</strong> • Indian Equities • Forex • Digital Assets • DirectQuery Fabric
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with header_right:
    now_str = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="text-align: right; background:{CARD_BG}; border:1px solid {BORDER_COLOR}; border-radius:8px; padding:0.55rem 0.85rem;">
        <div style="font-size:0.68rem; color:{TEXT_MUTED}; font-weight:700;">REAL-TIME FEED</div>
        <div style="font-size:0.86rem; font-weight:700; color:{ACCENT_GREEN};">
            <span class="live-dot"></span>LIVE ({now_str})
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"<hr style='border: none; border-top: 1px solid {BORDER_COLOR}; margin: 0.75rem 0 1.25rem 0;' />", unsafe_allow_html=True)


# ==============================================================================
# 8. TABBED NAVIGATION
# ==============================================================================
tab_live, tab_decade, tab_overview, tab_stock, tab_sector, tab_datamart = st.tabs([
    "⚡ Live Multi-Market Terminal",
    "🌍 10-Year Global Decade Intelligence",
    "🌐 Lakehouse Breadth & Overview",
    "📈 Equity Technical Deep Dive",
    "🏢 Sector & Comparative Analytics",
    "🗄️ Gold Data Mart Explorer",
])


# ==============================================================================
# TAB 0: LIVE MULTI-MARKET TERMINAL
# ==============================================================================
with tab_live:
    # Clean Search & Selector Container (Well-spaced layout)
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    
    # Row 1: Market Segment & Preset Instrument
    col_market, col_preset = st.columns([1, 1])
    with col_market:
        selected_category = st.selectbox(
            "Select Asset Class / Market",
            options=list(MARKET_PRESETS.keys()),
            index=0,
            key="market_category_select",
        )
    with col_preset:
        preset_dict = MARKET_PRESETS[selected_category]
        preset_symbol = st.selectbox(
            "Select Preset Instrument",
            options=list(preset_dict.keys()),
            format_func=lambda s: f"{s} — {preset_dict[s]}",
            index=0,
            key="preset_symbol_select",
        )

    # Row 2: Universal Search Bar
    custom_query = st.text_input(
        "🔍 Universal Ticker Search (Override with any symbol)",
        placeholder="Type any symbol: e.g. ZOMATO.NS, ETH-USD, EURUSD=X, NVDA, SUZLON.NS, TATACONSUM.NS",
        help="Supports NSE/BSE stocks (.NS), Forex pairs (=X), Cryptocurrencies (-USD), and Global Indices.",
        key="custom_symbol_input",
    )

    # Row 3: Horizon & Chart Type
    col_time, col_type, col_btn = st.columns([2, 2, 1])
    with col_time:
        timeframe = st.selectbox(
            "Timeframe Horizon",
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "max"],
            index=3,
            format_func=lambda x: {
                "1d": "1 Day (5-Min Intraday)",
                "5d": "5 Days (15-Min Intervals)",
                "1mo": "1 Month (Daily)",
                "3mo": "3 Months (Daily)",
                "6mo": "6 Months (Daily)",
                "1y": "1 Year (Daily)",
                "5y": "5 Years (Weekly Intervals)",
                "10y": "10 Years (Decade Horizon, Weekly)",
                "max": "Max Historical (All Available Data)",
            }[x],
            key="timeframe_select",
        )
    with col_type:
        chart_style = st.radio("Chart Representation", ["Candlestick", "Line (Close)"], horizontal=True, key="chart_style_radio")
    with col_btn:
        st.write("")  # align with input labels
        st.write("")
        if st.button("🔄 Refresh Quote", use_container_width=True, key="manual_quote_btn"):
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Active Ticker Resolution
    active_ticker = custom_query.strip().upper() if custom_query.strip() else preset_symbol

    # Fetch live data
    with st.spinner(f"Streaming live ticks for {active_ticker}..."):
        live_df, live_info = fetch_live_market_series(active_ticker, period=timeframe)

    if live_df is None or len(live_df) == 0:
        st.error(f"Could not retrieve live price series for '{active_ticker}'. Please verify the symbol.")
    else:
        latest_row = live_df.iloc[-1]
        prev_row = live_df.iloc[-2] if len(live_df) > 1 else latest_row

        curr_price = latest_row["Close"]
        prev_price = prev_row["Close"]
        price_diff = curr_price - prev_price
        pct_change = (price_diff / prev_price) * 100 if prev_price > 0 else 0

        # Hero Metric Cards (Spacious 5-Column Grid)
        lkpi1, lkpi2, lkpi3, lkpi4, lkpi5 = st.columns(5)

        with lkpi1:
            st.markdown(
                render_metric_card(
                    f"{active_ticker} Last Price",
                    format_currency_price(curr_price, active_ticker),
                    delta=f"{pct_change:+.2f}%",
                    delta_type="up" if pct_change >= 0 else "down",
                    subtext=f"Delta: {price_diff:+.2f}",
                ),
                unsafe_allow_html=True,
            )

        with lkpi2:
            hi_val = live_df["High"].max()
            lo_val = live_df["Low"].min()
            st.markdown(
                render_metric_card(
                    "Session Range (High / Low)",
                    f"{format_currency_price(hi_val, active_ticker)}",
                    delta=f"Low: {format_currency_price(lo_val, active_ticker)}",
                    delta_type="neutral",
                    subtext=f"Spread: {format_currency_price(hi_val - lo_val, active_ticker)}",
                ),
                unsafe_allow_html=True,
            )

        with lkpi3:
            rsi_val = latest_row["RSI_14"]
            rsi_state = "Overbought (>=70)" if rsi_val >= 70 else ("Oversold (<=30)" if rsi_val <= 30 else "Equilibrium (30-70)")
            rsi_type = "down" if rsi_val >= 70 else ("up" if rsi_val <= 30 else "neutral")
            st.markdown(
                render_metric_card(
                    "14-Period RSI",
                    f"{rsi_val:.1f}",
                    delta=rsi_state,
                    delta_type=rsi_type,
                    subtext="Momentum Oscillator",
                ),
                unsafe_allow_html=True,
            )

        with lkpi4:
            sma20 = latest_row["SMA_20"]
            is_above_ma = curr_price >= sma20
            st.markdown(
                render_metric_card(
                    "20-Period Moving Avg",
                    format_currency_price(sma20, active_ticker),
                    delta="Above MA 20" if is_above_ma else "Below MA 20",
                    delta_type="up" if is_above_ma else "down",
                    subtext=f"Spread: {((curr_price - sma20) / sma20) * 100:+.2f}%",
                ),
                unsafe_allow_html=True,
            )

        with lkpi5:
            vol_val = latest_row.get("Volume", 0)
            st.markdown(
                render_metric_card(
                    "Traded Volume",
                    f"{vol_val:,.0f}" if vol_val > 0 else "N/A (Forex)",
                    delta=f"{len(live_df)} Bars",
                    delta_type="neutral",
                    subtext=f"Horizon: {timeframe.upper()}",
                ),
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # AI Quantitative Investment Decision & Recommendation Desk
        # ----------------------------------------------------------------------
        sma20_val = float(latest_row["SMA_20"]) if "SMA_20" in latest_row and pd.notna(latest_row["SMA_20"]) else float(curr_price)
        sma50_val = float(latest_row["SMA_50"]) if "SMA_50" in latest_row and pd.notna(latest_row["SMA_50"]) else float(curr_price * 0.98)
        sma200_val = float(latest_row["SMA_200"]) if "SMA_200" in latest_row and pd.notna(latest_row["SMA_200"]) else float(curr_price * 0.92)
        rec = compute_investment_decision(curr_price, sma20_val, sma50_val, sma200_val, rsi_val)

        catalysts_html = "".join([f"<li style='margin-bottom:3px;'>✅ {c}</li>" for c in rec["catalysts"]])
        risks_html = "".join([f"<li style='margin-bottom:3px;'>⚠️ {r}</li>" for r in rec["risks"]])

        entry_min, entry_max = rec["entry_range"].split(" - ")
        entry_str = f"{format_currency_price(float(entry_min), active_ticker)} – {format_currency_price(float(entry_max), active_ticker)}"

        rec_card_html = f"""<div style="background:{rec['bg']}; border:1px solid {rec['border']}; border-radius:12px; padding:1.1rem 1.35rem; margin-top:1rem; margin-bottom:1.1rem; box-shadow: 0 8px 30px rgba(0,0,0,0.5);"><div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; margin-bottom:0.75rem; border-bottom:1px solid {rec['border']}; padding-bottom:0.65rem;"><div style="display:flex; align-items:center; gap:10px;"><span style="background:{rec['color']}; color:#000; font-weight:800; font-size:0.75rem; padding:3px 10px; border-radius:6px; letter-spacing:0.04em;">INVESTMENT RECOMMENDATION</span><span style="font-size:1.35rem; font-weight:800; color:{rec['color']}; font-family:'JetBrains Mono';">{rec['verdict']}</span><span style="font-size:0.85rem; color:#f8fafc; font-weight:700; background:rgba(255,255,255,0.08); padding:3px 8px; border-radius:6px;">Quantitative Score: {rec['score']} / 100</span></div><div style="font-size:0.8rem; font-weight:700; color:{rec['color']}; font-family:'JetBrains Mono';">🎯 {rec['action']}</div></div><div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:0.75rem; font-size:0.78rem;"><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">SUGGESTED BUY / ACCUMULATION ZONE</span><strong style="color:#f8fafc; font-size:0.95rem; font-family:'JetBrains Mono';">{entry_str}</strong></div><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">1-YEAR PROJECTED TARGET PRICE</span><strong style="color:#10b981; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(rec['target_1y'], active_ticker)} (+24% Upside)</strong></div><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">PROTECTIVE INVALIDATION STOP-LOSS</span><strong style="color:#f43f5e; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(rec['stop_loss'], active_ticker)} (-8% Risk Cut)</strong></div><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">PORTFOLIO SIZING GUIDELINE</span><strong style="color:#818cf8; font-size:0.95rem; font-family:'JetBrains Mono';">{rec['allocation']}</strong></div></div><div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:0.76rem; margin-top:6px;"><div style="color:#e2e8f0;"><strong style="color:#10b981; display:block; margin-bottom:4px;">Pillars Supporting Investment:</strong><ul style="margin:0; padding-left:14px; list-style-type:none;">{catalysts_html}</ul></div><div style="color:#e2e8f0;"><strong style="color:#f43f5e; display:block; margin-bottom:4px;">Risk Checks & Invalidation Conditions:</strong><ul style="margin:0; padding-left:14px; list-style-type:none;">{risks_html}</ul></div></div></div>"""
        st.markdown(rec_card_html, unsafe_allow_html=True)


        # Multi-Panel Synchronized Plotly Chart
        has_vol = (live_df["Volume"] > 0).any()
        row_heights = [0.65, 0.20, 0.15] if has_vol else [0.75, 0.25]
        num_rows = 3 if has_vol else 2

        fig_live = make_subplots(
            rows=num_rows,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            row_heights=row_heights,
        )

        # Panel 1: Price
        if chart_style == "Candlestick":
            fig_live.add_trace(
                go.Candlestick(
                    x=live_df["trade_date"],
                    open=live_df["Open"],
                    high=live_df["High"],
                    low=live_df["Low"],
                    close=live_df["Close"],
                    name=f"{active_ticker} OHLC",
                    increasing_line_color="#10b981",
                    decreasing_line_color="#f43f5e",
                ),
                row=1, col=1,
            )
        else:
            fig_live.add_trace(
                go.Scatter(
                    x=live_df["trade_date"],
                    y=live_df["Close"],
                    name=f"{active_ticker} Close",
                    line=dict(color="#00f0ff", width=2.5),
                ),
                row=1, col=1,
            )

        # Overlays
        if show_ma20:
            fig_live.add_trace(go.Scatter(x=live_df["trade_date"], y=live_df["SMA_20"], name="SMA 20", line=dict(color="#f59e0b", width=1.5)), row=1, col=1)
        if show_ma50:
            fig_live.add_trace(go.Scatter(x=live_df["trade_date"], y=live_df["SMA_50"], name="SMA 50", line=dict(color="#06b6d4", width=1.8)), row=1, col=1)
        if show_ma200:
            fig_live.add_trace(go.Scatter(x=live_df["trade_date"], y=live_df["SMA_200"], name="SMA 200", line=dict(color="#ec4899", width=2, dash="dash")), row=1, col=1)
        if show_bb:
            fig_live.add_trace(go.Scatter(x=live_df["trade_date"], y=live_df["BB_Upper"], name="BB Upper (+2σ)", line=dict(color="rgba(148, 163, 184, 0.4)", width=1, dash="dot")), row=1, col=1)
            fig_live.add_trace(go.Scatter(x=live_df["trade_date"], y=live_df["BB_Lower"], name="BB Lower (-2σ)", line=dict(color="rgba(148, 163, 184, 0.4)", width=1, dash="dot"), fill="tonexty", fillcolor="rgba(148, 163, 184, 0.08)"), row=1, col=1)

        # Panel 2: RSI 14
        fig_live.add_trace(go.Scatter(x=live_df["trade_date"], y=live_df["RSI_14"], name="RSI 14", line=dict(color="#818cf8", width=1.8)), row=2, col=1)
        fig_live.add_hline(y=70, line_dash="dash", line_color="rgba(239, 68, 68, 0.6)", row=2, col=1)
        fig_live.add_hline(y=30, line_dash="dash", line_color="rgba(34, 197, 94, 0.6)", row=2, col=1)

        # Panel 3: Volume
        if has_vol:
            v_colors = ["#22c55e" if c >= o else "#ef4444" for c, o in zip(live_df["Close"], live_df["Open"])]
            fig_live.add_trace(go.Bar(x=live_df["trade_date"], y=live_df["Volume"], name="Volume", marker_color=v_colors, opacity=0.7), row=3, col=1)

        chart_height = 620 if has_vol else 500
        l_layout = get_chart_layout(chart_height)
        l_layout["yaxis"]["title"] = "Price"
        l_layout["yaxis2"] = dict(title="RSI", range=[10, 90], gridcolor=l_layout["yaxis"]["gridcolor"], tickfont=dict(size=9, color=TEXT_MUTED))
        if has_vol:
            l_layout["yaxis3"] = dict(title="Volume", gridcolor=l_layout["yaxis"]["gridcolor"], tickfont=dict(size=9, color=TEXT_MUTED))
        l_layout["xaxis"]["rangeslider"] = dict(visible=False)
        fig_live.update_layout(l_layout)
        st.plotly_chart(fig_live, use_container_width=True, config={"displayModeBar": False})

    # Multi-Asset Quick Compare Strip (Clean 4-column layout to prevent cramped text)
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"### ⚡ Quick-Watch Comparison ({selected_category})")

    preset_syms = list(MARKET_PRESETS[selected_category].keys())[:8]
    qw_rows = [preset_syms[i:i+4] for i in range(0, len(preset_syms), 4)]

    for row_syms in qw_rows:
        cols_qw = st.columns(len(row_syms))
        for idx, qsym in enumerate(row_syms):
            with cols_qw[idx]:
                try:
                    qdf, _ = fetch_live_market_series(qsym, period="5d")
                    if qdf is not None and len(qdf) > 1:
                        qc = qdf["Close"].iloc[-1]
                        qp = qdf["Close"].iloc[-2]
                        qd = ((qc - qp) / qp) * 100
                        qarrow = "▲" if qd >= 0 else "▼"
                        qcolor = ACCENT_GREEN if qd >= 0 else ACCENT_RED
                        st.markdown(f"""
                        <div class="metric-card" style="padding:0.9rem 1.1rem; min-height: 95px;">
                            <div style="font-size:0.75rem; color:{TEXT_MUTED}; font-weight:700;">{qsym.replace('.NS', '').replace('=X', '')}</div>
                            <div style="font-size:1.25rem; font-weight:700; font-family:'JetBrains Mono'; margin-top:2px;">
                                {format_currency_price(qc, qsym)}
                            </div>
                            <div style="font-size:0.75rem; font-weight:700; color:{qcolor}; margin-top:4px;">
                                {qarrow} {qd:+.2f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    pass
        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 1: LAKEHOUSE BREADTH & OVERVIEW (MEDALLION SERVING)
# ==============================================================================

# ==============================================================================
# TAB 1: 10-YEAR GLOBAL DECADE INTELLIGENCE & MACRO DEEP DIVE
# ==============================================================================
with tab_decade:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h2 style="font-size: 1.35rem; font-weight: 700; color: #f8fafc; margin: 0; padding: 0;">
            🌍 10-Year Global Multi-Market Intelligence & Decade Compounding
        </h2>
        <p style="font-size: 0.8rem; color: #94a3b8; margin: 4px 0 0 0;">
            Comprehensive 10-year empirical analysis across World Equities, Benchmarks, Commodities, and Crypto (2015 – 2026).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Top Decade Metric Cards
    dkpi1, dkpi2, dkpi3, dkpi4, dkpi5 = st.columns(5)
    with dkpi1:
        st.markdown(render_metric_card("10Y S&P 500 (Wall St)", "+212.2%", delta="12.1% CAGR", delta_type="up", subtext="Max DD: -34.0% (2020)"), unsafe_allow_html=True)
    with dkpi2:
        st.markdown(render_metric_card("10Y Nifty 50 (India)", "+228.4%", delta="12.6% CAGR", delta_type="up", subtext="Max DD: -38.4% (2020)"), unsafe_allow_html=True)
    with dkpi3:
        st.markdown(render_metric_card("10Y Tech Titan (NVDA)", "+5,326.0%", delta="49.1% CAGR", delta_type="up", subtext="Inception Multiplier: 54.3x"), unsafe_allow_html=True)
    with dkpi4:
        st.markdown(render_metric_card("10Y Safe Haven (Gold)", "+198.4%", delta="11.6% CAGR", delta_type="up", subtext="Max DD: -21.5% (Lowest Risk)"), unsafe_allow_html=True)
    with dkpi5:
        st.markdown(render_metric_card("10Y Digital Asset (BTC)", "+8,122.5%", delta="55.4% CAGR", delta_type="up", subtext="Inception Multiplier: 82.2x"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 2. Universal 10-Year Any-Stock Analyzer
    st.markdown("""
    <div class="search-panel">
        <div style="font-size: 0.92rem; font-weight: 700; color: #818cf8; margin-bottom: 4px;">
            🔍 Universal 10-Year Deep Analyzer (Analyze ANY Stock in the World)
        </div>
        <div style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 10px;">
            Type any global ticker symbol (NYSE, NASDAQ, NSE, LSE, Tokyo, Frankfurt, Hong Kong, or Crypto) to pull 10 years of weekly data, calculate 10Y CAGR, maximum drawdown, and long-term moving averages.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_any_sym, c_any_scale, c_any_btn = st.columns([4, 2, 1])
    with c_any_sym:
        decade_custom_sym = st.text_input("Enter Global Ticker Symbol:", value="NVDA", placeholder="e.g. NVDA, RELIANCE.NS, ASML, TSM, AAPL, MSFT, TSLA, BABA, 7203.T, GC=F, BTC-USD", key="decade_ticker_input")
    with c_any_scale:
        decade_scale = st.radio("Chart Scale", ["Linear Scale", "Logarithmic Scale"], horizontal=True, key="decade_scale_radio")
    with c_any_btn:
        st.write("")
        st.write("")
        if st.button("🚀 Analyze 10Y", use_container_width=True, key="run_10y_btn"):
            st.rerun()

    active_decade_sym = decade_custom_sym.strip().upper() if decade_custom_sym.strip() else "NVDA"

    with st.spinner(f"Computing 10-year multi-cycle analytics for {active_decade_sym}..."):
        df_10y, _ = fetch_live_market_series(active_decade_sym, period="10y")

    if df_10y is not None and len(df_10y) > 10:
        c_first = df_10y["Close"].iloc[0]
        c_last = df_10y["Close"].iloc[-1]
        ten_year_ret = ((c_last - c_first) / c_first) * 100
        years_span = (df_10y["trade_date"].iloc[-1] - df_10y["trade_date"].iloc[0]).days / 365.25
        ten_year_cagr = ((c_last / c_first) ** (1 / max(years_span, 1.0)) - 1) * 100

        # Maximum Drawdown
        df_10y["Peak"] = df_10y["Close"].cummax()
        df_10y["Drawdown"] = (df_10y["Close"] - df_10y["Peak"]) / df_10y["Peak"] * 100
        max_dd = df_10y["Drawdown"].min()
        worst_dd_date = df_10y.loc[df_10y["Drawdown"].idxmin()]["trade_date"].strftime("%b %Y")

        # 10Y Volatility & Sharpe
        df_10y["Ret"] = df_10y["Close"].pct_change()
        annual_vol = df_10y["Ret"].std() * np.sqrt(52) * 100
        sharpe_10y = (ten_year_cagr - 4.25) / max(annual_vol, 0.01)

        # 50-Week & 200-Week Moving Averages
        df_10y["SMA_50W"] = df_10y["Close"].rolling(50, min_periods=1).mean()
        df_10y["SMA_200W"] = df_10y["Close"].rolling(200, min_periods=1).mean()
        sma_50w_val = float(df_10y["SMA_50W"].iloc[-1])
        sma_200w_val = float(df_10y["SMA_200W"].iloc[-1])

        # 4 Statistical Badges
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown(render_metric_card(f"{active_decade_sym} 10Y Return", f"{ten_year_ret:+,.1f}%", delta=f"{ten_year_cagr:.1f}% CAGR", delta_type="up" if ten_year_ret >= 0 else "down", subtext=f"Span: {years_span:.1f} Years"), unsafe_allow_html=True)
        with s2:
            st.markdown(render_metric_card("10-Year Max Drawdown", f"{max_dd:.1f}%", delta=f"Bottom: {worst_dd_date}", delta_type="down", subtext="Peak-to-Trough Decline"), unsafe_allow_html=True)
        with s3:
            st.markdown(render_metric_card("10Y Annualized Volatility", f"{annual_vol:.1f}%", delta=f"Weekly Std Dev: {df_10y['Ret'].std()*100:.2f}%", delta_type="neutral", subtext="Decade Dispersion"), unsafe_allow_html=True)
        with s4:
            st.markdown(render_metric_card("10Y Sharpe Ratio", f"{sharpe_10y:.2f}", delta="Risk-Adjusted Return", delta_type="up" if sharpe_10y >= 1.0 else "neutral", subtext="Rf = 4.25% Benchmark"), unsafe_allow_html=True)

        # 10-Year Secular Investment Decision Card
        cagr_pts = 30 if ten_year_cagr >= 25 else (25 if ten_year_cagr >= 15 else (20 if ten_year_cagr >= 10 else (10 if ten_year_cagr >= 5 else 0)))
        sharpe_pts = 25 if sharpe_10y >= 1.2 else (20 if sharpe_10y >= 0.8 else (15 if sharpe_10y >= 0.5 else (5 if sharpe_10y >= 0 else 0)))
        dd_pts = 25 if max_dd >= -25 else (20 if max_dd >= -40 else (15 if max_dd >= -55 else (8 if max_dd >= -75 else 2)))
        trend_pts = 20 if (c_last >= sma_50w_val and c_last >= sma_200w_val) else (12 if c_last >= sma_200w_val else 3)
        score_10y = int(min(100, max(0, cagr_pts + sharpe_pts + dd_pts + trend_pts)))

        if score_10y >= 80:
            verdict_10y = "LONG-TERM CORE COMPOUNDER (STRONG BUY)"
            action_10y = "Systematic Dollar-Cost Averaging (SIP) • Core Multi-Year Portfolio Anchor"
            color_10y = "#10b981"
            bg_10y = "rgba(16, 185, 129, 0.10)"
            border_10y = "rgba(16, 185, 129, 0.40)"
            alloc_10y = "10% – 20% Strategic Multi-Year Allocation"
        elif score_10y >= 65:
            verdict_10y = "HIGH GROWTH / ACCUMULATE ON PULLBACKS"
            action_10y = "Scale In on 50-Week SMA Retracements • Attractive Secular Upside"
            color_10y = "#00f0ff"
            bg_10y = "rgba(0, 240, 255, 0.08)"
            border_10y = "rgba(0, 240, 255, 0.35)"
            alloc_10y = "5% – 10% Secular Growth Sleeve"
        elif score_10y >= 50:
            verdict_10y = "CYCLICAL / HOLD & REBALANCE"
            action_10y = "Hold Existing Core Position • Rebalance During Overbought Peaks"
            color_10y = "#fbbf24"
            bg_10y = "rgba(251, 191, 36, 0.08)"
            border_10y = "rgba(251, 191, 36, 0.35)"
            alloc_10y = "2% – 5% Opportunistic Sizing"
        elif score_10y >= 35:
            verdict_10y = "HIGH VOLATILITY / SPECULATIVE"
            action_10y = "Tactical Allocation Only • Strictly Respect 200-Week SMA Trailing Stop"
            color_10y = "#ec4899"
            bg_10y = "rgba(236, 72, 153, 0.08)"
            border_10y = "rgba(236, 72, 153, 0.35)"
            alloc_10y = "< 2% High-Beta Speculative Cap"
        else:
            verdict_10y = "CAPITAL DESTRUCTION RISK / AVOID"
            action_10y = "Do Not Allocate Capital • Underperforming Risk-Free Benchmark"
            color_10y = "#f43f5e"
            bg_10y = "rgba(244, 63, 94, 0.10)"
            border_10y = "rgba(244, 63, 94, 0.40)"
            alloc_10y = "0% Allocation (Capital Preservation Priority)"

        cat_10y = [
            f"10-Year CAGR of {ten_year_cagr:.1f}% per annum (Decade Total: {ten_year_ret:+,.1f}%)",
            f"Risk-adjusted Sharpe of {sharpe_10y:.2f} relative to 4.25% risk-free rate",
            f"50-Week moving average support at {format_currency_price(sma_50w_val, active_decade_sym)}"
        ]
        risk_10y = [
            f"Historical maximum peak-to-trough drawdown: {max_dd:.1f}% ({worst_dd_date})",
            f"Annualized decade volatility: {annual_vol:.1f}% (requires disciplined multi-year horizon)",
            f"Structural invalidation stop-loss: Weekly close below 200W SMA ({format_currency_price(sma_200w_val, active_decade_sym)})"
        ]

        target_3y = c_last * ((1 + max(ten_year_cagr, 4.0)/100) ** 3)
        acc_min = c_last * 0.92
        acc_max = c_last * 0.98

        cat_10y_html = "".join([f"<li style='margin-bottom:3px;'>✅ {c}</li>" for c in cat_10y])
        risk_10y_html = "".join([f"<li style='margin-bottom:3px;'>⚠️ {r}</li>" for r in risk_10y])

        rec_10y_html = f"""<div style="background:{bg_10y}; border:1px solid {border_10y}; border-radius:12px; padding:1.1rem 1.35rem; margin-top:1rem; margin-bottom:1.1rem; box-shadow: 0 8px 30px rgba(0,0,0,0.5);"><div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; margin-bottom:0.75rem; border-bottom:1px solid {border_10y}; padding-bottom:0.65rem;"><div style="display:flex; align-items:center; gap:10px;"><span style="background:{color_10y}; color:#000; font-weight:800; font-size:0.75rem; padding:3px 10px; border-radius:6px; letter-spacing:0.04em;">10-YEAR SECULAR DECISION</span><span style="font-size:1.3rem; font-weight:800; color:{color_10y}; font-family:'JetBrains Mono';">{verdict_10y}</span><span style="font-size:0.85rem; color:#f8fafc; font-weight:700; background:rgba(255,255,255,0.08); padding:3px 8px; border-radius:6px;">Decade Score: {score_10y} / 100</span></div><div style="font-size:0.8rem; font-weight:700; color:{color_10y}; font-family:'JetBrains Mono';">🎯 {action_10y}</div></div><div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:0.75rem; font-size:0.78rem;"><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">SUGGESTED ACCUMULATION DIP ZONE</span><strong style="color:#f8fafc; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(acc_min, active_decade_sym)} – {format_currency_price(acc_max, active_decade_sym)}</strong></div><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">3-YEAR PROJECTED COMPOUNDED TARGET</span><strong style="color:#10b981; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(target_3y, active_decade_sym)} (At {ten_year_cagr:.1f}% CAGR)</strong></div><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">STRUCTURAL INVALIDATION (200W SMA)</span><strong style="color:#f43f5e; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(sma_200w_val, active_decade_sym)}</strong></div><div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);"><span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">PORTFOLIO SIZING GUIDELINE</span><strong style="color:#818cf8; font-size:0.95rem; font-family:'JetBrains Mono';">{alloc_10y}</strong></div></div><div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:0.76rem; margin-top:6px;"><div style="color:#e2e8f0;"><strong style="color:#10b981; display:block; margin-bottom:4px;">Decade Compounding Pillars Supporting Investment:</strong><ul style="margin:0; padding-left:14px; list-style-type:none;">{cat_10y_html}</ul></div><div style="color:#e2e8f0;"><strong style="color:#f43f5e; display:block; margin-bottom:4px;">Decade Risk Checks & Invalidation Conditions:</strong><ul style="margin:0; padding-left:14px; list-style-type:none;">{risk_10y_html}</ul></div></div></div>"""
        st.markdown(rec_10y_html, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        # 2-Panel Synchronized Plotly 10-Year Chart
        fig_10y = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            row_heights=[0.72, 0.28],
            subplot_titles=[f"📈 {active_decade_sym} 10-Year Historical Trajectory (Weekly Intervals)", "🌊 Underwater Drawdown Profile (% from All-Time High)"]
        )

        # Price Line
        fig_10y.add_trace(go.Scatter(
            x=df_10y["trade_date"],
            y=df_10y["Close"],
            name=f"{active_decade_sym} Close",
            line=dict(color="#00f0ff", width=2.5),
        ), row=1, col=1)

        # 50-Week & 200-Week Moving Averages
        fig_10y.add_trace(go.Scatter(x=df_10y["trade_date"], y=df_10y["SMA_50W"], name="50-Week SMA", line=dict(color="#fbbf24", width=1.5)), row=1, col=1)
        fig_10y.add_trace(go.Scatter(x=df_10y["trade_date"], y=df_10y["SMA_200W"], name="200-Week SMA", line=dict(color="#ec4899", width=2, dash="dash")), row=1, col=1)

        # Panel 2: Drawdown Area
        fig_10y.add_trace(go.Scatter(
            x=df_10y["trade_date"],
            y=df_10y["Drawdown"],
            name="Drawdown %",
            fill="tozeroy",
            fillcolor="rgba(244, 63, 94, 0.25)",
            line=dict(color="#f43f5e", width=1.2),
        ), row=2, col=1)

        layout_10y = get_chart_layout(520)
        layout_10y["yaxis"]["type"] = "log" if decade_scale == "Logarithmic Scale" else "linear"
        layout_10y["yaxis"]["title"] = "Price (Log)" if decade_scale == "Logarithmic Scale" else "Price"
        layout_10y["yaxis2"] = dict(title="Drawdown %", range=[min(max_dd * 1.15, -10), 2], gridcolor=layout_10y["yaxis"]["gridcolor"], tickfont=dict(size=9, color=TEXT_MUTED))
        fig_10y.update_layout(layout_10y)
        st.plotly_chart(fig_10y, use_container_width=True, config={"displayModeBar": False})

    # 3. Global Decade Performance Leaderboard
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 🏆 Global Decade Performance Leaderboard (Top World Compounders 2015–2026)")
    
    decade_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "05_powerbi_dashboard", "data", "Dim_Company_10Y.csv")
    if os.path.exists(decade_data_path):
        df_lead = pd.read_csv(decade_data_path)
        df_lead_display = df_lead.sort_values(by="ten_year_cagr", ascending=False).copy()
        
        table_rows_10y = ""
        for _, r in df_lead_display.iterrows():
            ret = r["ten_year_return"]
            cagr = r["ten_year_cagr"]
            mdd = r["max_drawdown"]
            table_rows_10y += f"""
            <tr>
                <td style="font-weight:700; color:#818cf8;">{r['symbol']}</td>
                <td>{r['company_name']}</td>
                <td><span class="badge badge-neutral">{r['region']}</span></td>
                <td>{r['sector']}</td>
                <td style="color:#10b981; font-weight:700; text-align:right;">{cagr:.1f}%</td>
                <td style="color:#10b981; font-weight:700; text-align:right;">{ret:+,.1f}%</td>
                <td style="color:#f43f5e; text-align:right;">{mdd:.1f}%</td>
                <td style="color:#00f0ff; text-align:right; font-weight:700;">{r['sharpe']:.2f}</td>
                <td style="text-align:right;">${r['market_cap_b']:,.0f}B</td>
            </tr>
            """
        
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {BORDER_COLOR}; border-radius:10px; overflow-x:auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Enterprise / Asset</th>
                        <th>Region</th>
                        <th>Sector</th>
                        <th style="text-align:right;">10Y CAGR</th>
                        <th style="text-align:right;">10Y Total Return</th>
                        <th style="text-align:right;">Max Drawdown</th>
                        <th style="text-align:right;">10Y Sharpe</th>
                        <th style="text-align:right;">Market Cap ($B)</th>
                    </tr>
                </thead>
                <tbody>{table_rows_10y}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # 4. Decade Macro Crisis & Stress-Testing Chronology
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 📜 10-Year Macroeconomic Cycles & Market Regime Chronology")
    
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown("""
        <div class="metric-card" style="padding:1rem;">
            <div style="font-size:0.75rem; color:#ec4899; font-weight:700;">2015 – 2016 REGIME</div>
            <div style="font-size:0.95rem; font-weight:700; color:#f8fafc; margin-top:2px;">Oil Deflation & China Yuan Shock</div>
            <p style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">
                Crude oil collapsed from $100 to $27. China devalued the Yuan. Global manufacturing contracted while US tech began its secular cloud rally.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with mc2:
        st.markdown("""
        <div class="metric-card" style="padding:1rem;">
            <div style="font-size:0.75rem; color:#f43f5e; font-weight:700;">2020 FLASH CRASH</div>
            <div style="font-size:0.95rem; font-weight:700; color:#f8fafc; margin-top:2px;">COVID-19 Global Liquidity Shock</div>
            <p style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">
                S&P 500 plunged -34% in 33 days. Unprecedented global central bank quantitative easing sparked the fastest full-cycle recovery in financial history.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with mc3:
        st.markdown("""
        <div class="metric-card" style="padding:1rem;">
            <div style="font-size:0.75rem; color:#fbbf24; font-weight:700;">2022 INFLATION SHOCK</div>
            <div style="font-size:0.95rem; font-weight:700; color:#f8fafc; margin-top:2px;">500bps Rapid Rate Hike Cycle</div>
            <p style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">
                Global 40-year high inflation led to rapid rate hikes. Nasdaq dropped -33%, bonds suffered worst year in history, paving the way for the 2024 AI boom.
            </p>
        </div>
        """, unsafe_allow_html=True)


with tab_overview:
    if df_stocks is None:
        st.warning("Lakehouse Gold datasets not found in 03_dashboard_export/exports.")
    else:
        latest_market = df_market.iloc[-1]
        prev_market = df_market.iloc[-2] if len(df_market) > 1 else latest_market

        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.markdown(
                render_metric_card(
                    "Latest Lakehouse Settlement",
                    latest_market["trade_date"].strftime("%d %b %Y"),
                    subtext="Official NIFTY Settlement",
                ),
                unsafe_allow_html=True,
            )
        with kpi2:
            adv_dec_ratio = latest_market["advancers_count"] / max(latest_market["decliners_count"], 1)
            delta_type = "up" if latest_market["advancers_count"] >= latest_market["decliners_count"] else "down"
            st.markdown(
                render_metric_card(
                    "Market Breadth (A/D)",
                    f"{latest_market['advancers_count']} : {latest_market['decliners_count']}",
                    delta=f"{adv_dec_ratio:.2f}x A/D Ratio",
                    delta_type=delta_type,
                    subtext=f"{latest_market['unchanged_count']} unchanged stocks",
                ),
                unsafe_allow_html=True,
            )
        with kpi3:
            avg_ret = latest_market["market_avg_return_pct"]
            ret_type = "up" if avg_ret >= 0 else "down"
            st.markdown(
                render_metric_card(
                    "Market Average Return",
                    f"{avg_ret:+.2f}%",
                    delta=f"{avg_ret - prev_market['market_avg_return_pct']:+.2f}% vs Prev Day",
                    delta_type=ret_type,
                ),
                unsafe_allow_html=True,
            )
        with kpi4:
            tot_vol_cr = latest_market["market_total_volume"] / 10000000
            st.markdown(
                render_metric_card(
                    "Market Total Volume",
                    f"{tot_vol_cr:.2f} Cr",
                    subtext="NSE Blue-Chip Shares",
                ),
                unsafe_allow_html=True,
            )
        with kpi5:
            latest_day_stocks = df_stocks[df_stocks["trade_date"] == latest_market["trade_date"]]
            avg_vol = latest_day_stocks["annualized_volatility_30d"].mean()
            st.markdown(
                render_metric_card(
                    "Avg Realized Volatility",
                    f"{avg_vol:.2f}%",
                    delta="Annualized 30D",
                    delta_type="neutral",
                ),
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([6, 4])
        with c1:
            st.markdown("<div style='font-weight:600; font-size:0.95rem; margin-bottom:6px;'>📈 Cumulative Market Breadth & Daily Advances / Declines</div>", unsafe_allow_html=True)
            fig_breadth = make_subplots(specs=[[{"secondary_y": True}]])
            fig_breadth.add_trace(go.Bar(x=df_market["trade_date"], y=df_market["advancers_count"], name="Advancing", marker_color="#22c55e", opacity=0.75), secondary_y=False)
            fig_breadth.add_trace(go.Bar(x=df_market["trade_date"], y=-df_market["decliners_count"], name="Declining", marker_color="#ef4444", opacity=0.75), secondary_y=False)

            f_market_calc = df_market.copy()
            f_market_calc["net_advances"] = f_market_calc["advancers_count"] - f_market_calc["decliners_count"]
            f_market_calc["cumulative_breadth"] = f_market_calc["net_advances"].cumsum()

            fig_breadth.add_trace(go.Scatter(x=f_market_calc["trade_date"], y=f_market_calc["cumulative_breadth"], name="Cumulative A/D Line", line=dict(color=ACCENT, width=2.5)), secondary_y=True)

            layout_b = get_chart_layout(380)
            layout_b["barmode"] = "relative"
            layout_b["yaxis"]["title"] = "Daily Count"
            layout_b["yaxis2"] = dict(title="Cumulative Breadth", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10, color=ACCENT))
            fig_breadth.update_layout(layout_b)
            st.plotly_chart(fig_breadth, use_container_width=True, config={"displayModeBar": False})

        with c2:
            st.markdown("<div style='font-weight:600; font-size:0.95rem; margin-bottom:6px;'>🏢 Sector Performance Comparison</div>", unsafe_allow_html=True)
            latest_sec = df_sector[df_sector["trade_date"] == latest_market["trade_date"]].copy()
            latest_sec.sort_values(by="sector_mean_return_pct", ascending=True, inplace=True)
            bar_colors = ["#22c55e" if r >= 0 else "#ef4444" for r in latest_sec["sector_mean_return_pct"]]

            fig_sec = go.Figure(go.Bar(
                x=latest_sec["sector_mean_return_pct"],
                y=latest_sec["sector"],
                orientation="h",
                marker_color=bar_colors,
                text=[f"{r:+.2f}%" for r in latest_sec["sector_mean_return_pct"]],
                textposition="outside",
            ))
            layout_s = get_chart_layout(380)
            layout_s["xaxis"]["title"] = "Mean Return (%)"
            fig_sec.update_layout(layout_s)
            st.plotly_chart(fig_sec, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-weight:600; font-size:0.95rem; margin-bottom:8px;'>⚡ Constituent Equities Summary (Latest Session: {latest_market['trade_date'].strftime('%d %b %Y')})</div>", unsafe_allow_html=True)

        latest_stocks = df_stocks[df_stocks["trade_date"] == latest_market["trade_date"]].copy()
        latest_stocks.sort_values(by="daily_return_pct", ascending=False, inplace=True)

        table_rows = ""
        for _, row in latest_stocks.iterrows():
            ret = row["daily_return_pct"]
            ret_color = "#22c55e" if ret >= 0 else "#ef4444"
            gc_status = "Bullish" if row["sma_50"] >= row["sma_200"] else "Bearish"
            gc_badge = "badge-bullish" if gc_status == "Bullish" else "badge-bearish"
            rsi = row["rsi_14"]
            rsi_badge = "<span class='badge badge-warn'>Overbought</span>" if rsi >= 70 else ("<span class='badge badge-bearish'>Oversold</span>" if rsi <= 30 else "<span class='badge badge-neutral'>Neutral</span>")

            table_rows += f"""
            <tr>
                <td style="font-weight:700; color:{ACCENT};">{row['symbol'].replace('.NS', '')}</td>
                <td style="font-family:'DM Sans';">{row['company_name']}</td>
                <td style="font-family:'DM Sans';">{row['sector']}</td>
                <td>₹{row['close']:,.2f}</td>
                <td style="color:{ret_color}; font-weight:700;">{ret:+.2f}%</td>
                <td>{rsi:.1f} {rsi_badge}</td>
                <td>₹{row['sma_50']:,.1f} / ₹{row['sma_200']:,.1f}</td>
                <td><span class="badge {gc_badge}">{gc_status}</span></td>
                <td>{row['annualized_volatility_30d']:.1f}%</td>
                <td>{row['volume']:,}</td>
            </tr>
            """

        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {BORDER_COLOR}; border-radius:10px; overflow-x:auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Enterprise Name</th>
                        <th>Sector</th>
                        <th>Close Price</th>
                        <th>1-Day Delta</th>
                        <th>14D RSI</th>
                        <th>SMA 50 / 200</th>
                        <th>Trend Signal</th>
                        <th>30D Volatility</th>
                        <th>Session Volume</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: EQUITY TECHNICAL DEEP DIVE (LAKEHOUSE)
# ==============================================================================
with tab_stock:
    if df_stocks is not None:
        company_dict = dict(zip(df_company["symbol"], df_company["company_name"]))
        stock_sym = st.selectbox(
            "Select Lakehouse Focus Stock",
            options=list(company_dict.keys()),
            format_func=lambda s: f"{s.replace('.NS', '')} — {company_dict[s]}",
            key="deepdive_stock_select"
        )
        stock_df = df_stocks[df_stocks["symbol"] == stock_sym].copy()

        if len(stock_df) > 0:
            latest_s = stock_df.iloc[-1]
            st1, st2, st3, st4 = st.columns(4)
            with st1:
                st.markdown(render_metric_card("Close Price", f"₹{latest_s['close']:,.2f}", delta=f"{latest_s['daily_return_pct']:+.2f}%"), unsafe_allow_html=True)
            with st2:
                st.markdown(render_metric_card("14D RSI", f"{latest_s['rsi_14']:.1f}"), unsafe_allow_html=True)
            with st3:
                is_gc = latest_s["sma_50"] >= latest_s["sma_200"]
                st.markdown(render_metric_card("SMA 50 vs 200", f"₹{latest_s['sma_50']:,.0f}", delta="Golden Cross" if is_gc else "Death Cross", delta_type="up" if is_gc else "down"), unsafe_allow_html=True)
            with st4:
                st.markdown(render_metric_card("30D Realized Volatility", f"{latest_s['annualized_volatility_30d']:.1f}%"), unsafe_allow_html=True)

            fig_dd = go.Figure()
            fig_dd.add_trace(go.Candlestick(x=stock_df["trade_date"], open=stock_df["open"], high=stock_df["high"], low=stock_df["low"], close=stock_df["close"], name="OHLC"))
            fig_dd.add_trace(go.Scatter(x=stock_df["trade_date"], y=stock_df["sma_20"], name="SMA 20", line=dict(color="#f59e0b", width=1.5)))
            fig_dd.add_trace(go.Scatter(x=stock_df["trade_date"], y=stock_df["sma_50"], name="SMA 50", line=dict(color="#06b6d4", width=1.8)))
            fig_dd.add_trace(go.Scatter(x=stock_df["trade_date"], y=stock_df["sma_200"], name="SMA 200", line=dict(color="#ec4899", width=2, dash="dash")))
            layout_dd = get_chart_layout(480)
            layout_dd["xaxis"]["rangeslider"] = dict(visible=False)
            fig_dd.update_layout(layout_dd)
            st.plotly_chart(fig_dd, use_container_width=True, config={"displayModeBar": False})


# ==============================================================================
# TAB 3: SECTOR & COMPARATIVE ANALYTICS
# ==============================================================================
with tab_sector:
    if df_stocks is not None:
        st.markdown("### 📊 Cross-Sector Benchmark & Cumulative Returns")
        st.caption("Normalized Growth of 100 INR invested at period inception across all blue-chip constituents.")

        fig_cum = go.Figure()
        palette = ["#38bdf8", "#818cf8", "#f43f5e", "#22c55e", "#f59e0b", "#ec4899"]

        for i, sym in enumerate(df_company["symbol"].unique()):
            sub = df_stocks[df_stocks["symbol"] == sym].sort_values("trade_date")
            if len(sub) > 0:
                first_close = sub.iloc[0]["close"]
                cum_ret_idx = (sub["close"] / first_close) * 100
                fig_cum.add_trace(go.Scatter(x=sub["trade_date"], y=cum_ret_idx, name=sym.replace(".NS", ""), line=dict(color=palette[i % len(palette)], width=2)))

        layout_c = get_chart_layout(400)
        layout_c["yaxis"]["title"] = "Normalized Value (Base 100)"
        fig_cum.update_layout(layout_c)
        st.plotly_chart(fig_cum, use_container_width=True, config={"displayModeBar": False})


# ==============================================================================
# TAB 4: GOLD DATA MART EXPLORER
# ==============================================================================
with tab_datamart:
    if df_stocks is not None:
        st.markdown("### 🗄️ Curated Gold-Layer Data Marts")
        st.caption("Direct dimensional extracts supporting BI dashboards (Power BI & Tableau)")

        selected_table = st.selectbox(
            "Choose Lakehouse Table to Inspect:",
            options=[
                "Fact_StockAnalytics (Prices & Technical Indicators)",
                "Fact_SectorPerformance (Vertical Aggregations)",
                "Fact_MarketSummary (Market Breadth & Liquidity)",
                "Dim_Company (Enterprise Profiles & Sectors)",
            ],
            key="mart_select_box"
        )

        if "Fact_StockAnalytics" in selected_table:
            active_df = df_stocks
            filename = "Fact_StockAnalytics.csv"
        elif "Fact_SectorPerformance" in selected_table:
            active_df = df_sector
            filename = "Fact_SectorPerformance.csv"
        elif "Fact_MarketSummary" in selected_table:
            active_df = df_market
            filename = "Fact_MarketSummary.csv"
        else:
            active_df = df_company
            filename = "Dim_Company.csv"

        st_c1, st_c2 = st.columns([8, 2], vertical_alignment="center")
        with st_c1:
            st.write(f"Showing **{len(active_df):,}** records | **{len(active_df.columns)}** columns")
        with st_c2:
            csv_data = active_df.to_csv(index=False).encode("utf-8")
            st.download_button(label=f"📥 Download {filename}", data=csv_data, file_name=filename, mime="text/csv", use_container_width=True)

        st.dataframe(active_df, use_container_width=True, height=280)
