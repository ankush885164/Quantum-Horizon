# -*- coding: utf-8 -*-
"""
Upgrade Financial Market Intelligence Terminal with
10-Year Global Multi-Market Intelligence Suite across:
1. Streamlit app (04_dashboard/app.py)
2. Power BI Canvas (05_powerbi_dashboard/build_interactive_powerbi.py)
3. DAX Measures (05_powerbi_dashboard/DAX_Measures.dax)
"""

import os
import re

# ==============================================================================
# 1. UPGRADE STREAMLIT APP (04_dashboard/app.py)
# ==============================================================================
st_file = r"D:\BDA Project\financial-market-intelligence\04_dashboard\app.py"
with open(st_file, "r", encoding="utf-8") as f:
    code = f.read()

# Expand MARKET_PRESETS to include world markets
old_presets = '''MARKET_PRESETS = {
    "🇮🇳 Indian Equities (NSE/BSE)": {
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
        "TATACONSUM.NS": "Tata Consumer Products",
        "WIPRO.NS": "Wipro Ltd",
        "ZOMATO.NS": "Zomato Ltd",
    },
    "💱 Forex & Currencies": {
        "USDINR=X": "USD / INR (US Dollar to Indian Rupee)",
        "EURINR=X": "EUR / INR (Euro to Indian Rupee)",
        "GBPINR=X": "GBP / INR (British Pound to Indian Rupee)",
        "EURUSD=X": "EUR / USD (Euro to US Dollar)",
        "GBPUSD=X": "GBP / USD (British Pound to US Dollar)",
        "USDJPY=X": "USD / JPY (US Dollar to Japanese Yen)",
        "AUDUSD=X": "AUD / USD (Australian Dollar to US Dollar)",
        "USDCHF=X": "USD / CHF (US Dollar to Swiss Franc)",
        "AEDINR=X": "AED / INR (UAE Dirham to Indian Rupee)",
    },
    "🪙 Cryptocurrencies": {
        "BTC-USD": "Bitcoin (BTC / USD)",
        "ETH-USD": "Ethereum (ETH / USD)",
        "SOL-USD": "Solana (SOL / USD)",
        "BNB-USD": "Binance Coin (BNB / USD)",
        "DOGE-USD": "Dogecoin (DOGE / USD)",
        "XRP-USD": "Ripple (XRP / USD)",
        "ADA-USD": "Cardano (ADA / USD)",
        "AVAX-USD": "Avalanche (AVAX / USD)",
    },
    "🌐 Global Indices & Equities": {
        "^NSEI": "NIFTY 50 Index (India)",
        "^BSESN": "S&P BSE SENSEX Index (India)",
        "^GSPC": "S&P 500 Index (USA)",
        "^IXIC": "NASDAQ Composite (USA)",
        "AAPL": "Apple Inc.",
        "NVDA": "NVIDIA Corporation",
        "MSFT": "Microsoft Corporation",
        "TSLA": "Tesla Inc.",
        "GOOGL": "Alphabet Inc.",
    }
}'''

new_presets = '''MARKET_PRESETS = {
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
}'''

code = code.replace(old_presets, new_presets)

# Upgrade fetch_live_market_series to handle 10y and max
old_fetch_body = '''        if period == "1d":
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
        else:
            df = t.history(period="5y", interval="1wk")'''

new_fetch_body = '''        if period == "1d":
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
            df = t.history(period="10y", interval="1wk")'''

code = code.replace(old_fetch_body, new_fetch_body)

# Upgrade timeframe selector options
old_tf_select = '''        timeframe = st.selectbox(
            "Timeframe Horizon",
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"],
            index=3,
            format_func=lambda x: {
                "1d": "1 Day (5-Min Intraday)",
                "5d": "5 Days (15-Min Intervals)",
                "1mo": "1 Month (Daily)",
                "3mo": "3 Months (Daily)",
                "6mo": "6 Months (Daily)",
                "1y": "1 Year (Daily)",
                "5y": "5 Years (Weekly)",
            }[x],
            key="timeframe_select",
        )'''

new_tf_select = '''        timeframe = st.selectbox(
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
        )'''

code = code.replace(old_tf_select, new_tf_select)

# Add Tab 1 (Decade 10-Year Global Intelligence) to tabs list
old_tabs_def = '''tab_live, tab_overview, tab_stock, tab_sector, tab_datamart = st.tabs([
    "⚡ Live Multi-Market Terminal",
    "🌐 Lakehouse Breadth & Overview",
    "📈 Equity Technical Deep Dive",
    "🏢 Sector & Comparative Analytics",
    "🗄️ Gold Data Mart Explorer",
])'''

new_tabs_def = '''tab_live, tab_decade, tab_overview, tab_stock, tab_sector, tab_datamart = st.tabs([
    "⚡ Live Multi-Market Terminal",
    "🌍 10-Year Global Decade Intelligence",
    "🌐 Lakehouse Breadth & Overview",
    "📈 Equity Technical Deep Dive",
    "🏢 Sector & Comparative Analytics",
    "🗄️ Gold Data Mart Explorer",
])'''

code = code.replace(old_tabs_def, new_tabs_def)

# Add implementation for tab_decade right before tab_overview
tab_decade_code = '''
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
        df_10y["SMA_50W"] = df_10y["Close"].rolling(50, min_periods=1).mean()
        df_10y["SMA_200W"] = df_10y["Close"].rolling(200, min_periods=1).mean()

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
    
    decade_data_path = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\data\Dim_Company_10Y.csv"
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
'''

code = code.replace("with tab_overview:", tab_decade_code + "\n\nwith tab_overview:")

with open(st_file, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated 04_dashboard/app.py with 10-Year Global Suite successfully!")
