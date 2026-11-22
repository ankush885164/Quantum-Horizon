"""
Fix and perfectly align index.html layout to prevent any UI clipping,
overlaps, or hidden dropdown options.
"""

import json
import os

with open("financial-market-intelligence/04_dashboard/full_dashboard_data.json", "r") as f:
    master_data = json.load(f)

html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Financial Market Intelligence — Multi-Asset Live Terminal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090a0f;
      --bg-surface: #11131c;
      --bg-card: #161926;
      --bg-card-hover: #1c2032;
      --border: #23273b;
      --border-subtle: #191c2b;
      --text: #f1f5f9;
      --text-muted: #8e9bb0;
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.18);
      --bullish: #10b981;
      --bullish-bg: rgba(16, 185, 129, 0.12);
      --bearish: #f43f5e;
      --bearish-bg: rgba(244, 63, 94, 0.12);
      --warning: #f59e0b;
      --warning-bg: rgba(245, 158, 11, 0.12);
      --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    .light {{
      --bg: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f1f5f9;
      --border: #e2e8f0;
      --border-subtle: #edf2f7;
      --text: #0f172a;
      --text-muted: #64748b;
      --primary: #0284c7;
      --primary-glow: rgba(2, 132, 199, 0.12);
      --bullish: #059669;
      --bullish-bg: rgba(5, 150, 105, 0.1);
      --bearish: #e11d48;
      --bearish-bg: rgba(225, 29, 72, 0.1);
      --warning: #d97706;
      --warning-bg: rgba(217, 119, 6, 0.1);
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

    .app-header {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      padding: 0.85rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 1000;
    }}
    .logo-container {{ display: flex; align-items: center; gap: 12px; }}
    .logo-icon {{
      width: 38px; height: 38px; border-radius: 10px;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      display: flex; align-items: center; justify-content: center;
      font-size: 1.25rem; font-weight: 800; color: #fff;
    }}
    .logo-text h1 {{ font-size: 1.2rem; font-weight: 700; }}
    .logo-text p {{ font-size: 0.74rem; color: var(--text-muted); }}

    .btn {{
      display: inline-flex; align-items: center; gap: 6px;
      padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.8rem;
      font-weight: 600; cursor: pointer; border: 1px solid var(--border);
      background: var(--bg-card); color: var(--text);
    }}
    .btn:hover {{ background: var(--bg-card-hover); border-color: var(--primary); }}
    .btn-primary {{ background: var(--primary); color: #fff; border-color: var(--primary); }}

    .live-dot {{
      display: inline-block; width: 8px; height: 8px; border-radius: 50%;
      background-color: var(--bullish); box-shadow: 0 0 8px var(--bullish);
      animation: pulse 1.5s infinite; margin-right: 6px;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.95); opacity: 0.7; }}
      50% {{ transform: scale(1.3); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.7; }}
    }}

    .app-main {{
      max-width: 1600px; width: 100%; margin: 0 auto;
      padding: 1.5rem 2rem 3.5rem; flex: 1;
    }}

    /* Hero KPI Strip */
    .kpi-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1.1rem; margin-bottom: 1.5rem;
    }}
    .kpi-card {{
      background: var(--bg-surface); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.1rem 1.25rem; min-height: 105px;
      display: flex; flex-direction: column; justify-content: space-between;
    }}
    .kpi-card:hover {{ border-color: var(--primary); }}
    .kpi-label {{
      font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em;
      font-weight: 600; color: var(--text-muted); margin-bottom: 0.35rem;
    }}
    .kpi-value {{
      font-family: var(--font-mono); font-size: 1.55rem; font-weight: 700;
    }}
    .kpi-delta {{
      margin-top: 0.35rem; display: inline-flex; align-items: center; gap: 4px;
      font-size: 0.76rem; font-weight: 600; padding: 2px 7px; border-radius: 6px;
      width: fit-content;
    }}
    .delta-bullish {{ color: var(--bullish); background: var(--bullish-bg); }}
    .delta-bearish {{ color: var(--bearish); background: var(--bearish-bg); }}
    .delta-neutral {{ color: var(--text-muted); background: var(--border-subtle); }}

    /* Tab Bar */
    .tab-bar {{
      display: flex; align-items: center; gap: 6px; background: var(--bg-surface);
      border: 1px solid var(--border); border-radius: 10px; padding: 5px;
      margin-bottom: 1.5rem; overflow-x: auto;
    }}
    .tab-btn {{
      padding: 0.6rem 1.25rem; border-radius: 8px; font-size: 0.85rem;
      font-weight: 600; color: var(--text-muted); background: transparent;
      border: none; cursor: pointer; display: inline-flex; align-items: center;
      gap: 8px; white-space: nowrap;
    }}
    .tab-btn:hover {{ color: var(--text); background: var(--bg-card); }}
    .tab-btn.active {{
      color: var(--text); background: var(--bg-card);
      border: 1px solid var(--border); box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }}

    .panel {{
      background: var(--bg-surface); border: 1px solid var(--border);
      border-radius: 14px; padding: 1.4rem 1.6rem; margin-bottom: 1.5rem;
    }}
    .panel-header {{
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 1.2rem; flex-wrap: wrap; gap: 12px;
    }}
    .panel-title {{
      font-size: 1.05rem; font-weight: 700; display: flex; align-items: center; gap: 8px;
    }}
    .panel-subtitle {{ font-size: 0.76rem; color: var(--text-muted); margin-top: 2px; }}

    /* Search Control Panel — Clean Vertical Sections */
    .control-box {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.25rem 1.4rem; margin-bottom: 1.4rem;
      display: flex; flex-direction: column; gap: 1rem;
    }}
    .control-row {{
      display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
    }}
    .control-group {{
      display: flex; flex-direction: column; gap: 0.35rem; flex: 1; min-width: 240px;
    }}
    .control-label {{
      font-size: 0.74rem; font-weight: 700; color: var(--text-muted);
      text-transform: uppercase; letter-spacing: 0.04em;
    }}

    .market-pill {{
      padding: 7px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;
      border: 1px solid var(--border); background: var(--bg-surface); cursor: pointer;
      display: inline-flex; align-items: center; gap: 6px; color: var(--text-muted);
    }}
    .market-pill:hover {{ color: var(--text); border-color: var(--primary); }}
    .market-pill.active {{
      background: var(--primary); color: #fff; border-color: var(--primary);
    }}

    select, input {{
      background: var(--bg-surface); border: 1px solid var(--border);
      color: var(--text); padding: 0.6rem 0.9rem; border-radius: 8px;
      font-size: 0.85rem; font-family: var(--font-sans); outline: none; width: 100%;
    }}
    select:focus, input:focus {{ border-color: var(--primary); }}

    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.4rem; }}
    .grid-60-40 {{ display: grid; grid-template-columns: 60% 40%; gap: 1.4rem; }}
    @media (max-width: 960px) {{ .grid-2, .grid-60-40 {{ grid-template-columns: 1fr; }} }}

    .chart-box {{ width: 100%; height: 400px; position: relative; }}
    .chart-box-sm {{ width: 100%; height: 120px; position: relative; }}
    svg text {{ font-family: var(--font-mono); user-select: none; }}

    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    .table-container {{
      overflow-x: auto; border-radius: 10px; border: 1px solid var(--border);
      background: var(--bg-card);
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
    th {{
      text-align: left; padding: 0.8rem 1rem; font-size: 0.72rem;
      text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted);
      background: var(--bg-surface); border-bottom: 1px solid var(--border); font-weight: 600;
    }}
    td {{
      padding: 0.8rem 1rem; border-bottom: 1px solid var(--border-subtle);
      font-family: var(--font-mono); font-size: 0.82rem;
    }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: var(--bg-card-hover); }}

    .badge {{
      display: inline-flex; align-items: center; padding: 2px 8px;
      border-radius: 6px; font-size: 0.72rem; font-weight: 600;
    }}
    .badge-bullish {{ color: var(--bullish); background: var(--bullish-bg); }}
    .badge-bearish {{ color: var(--bearish); background: var(--bearish-bg); }}
  </style>
</head>
<body>

  <header class="app-header">
    <div class="logo-container">
      <div class="logo-icon">₹</div>
      <div class="logo-text">
        <h1>Financial Market Intelligence</h1>
        <p><span class="live-dot"></span>Live Multi-Asset Terminal • Indian Equities • Forex • Crypto • Lakehouse Analytics</p>
      </div>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
      <button class="btn" onclick="simulateLiveTick()">⚡ Live Tick Refresh</button>
      <button class="btn" id="theme-toggle" onclick="toggleTheme()">☀️ Light View</button>
    </div>
  </header>

  <main class="app-main">

    <!-- KPI STRIP -->
    <section class="kpi-grid" id="kpi-strip"></section>

    <!-- TABS -->
    <nav class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('live-terminal')">
        <span>⚡</span> Live Multi-Market Terminal
      </button>
      <button class="tab-btn" onclick="switchTab('overview')">
        <span>🌐</span> Lakehouse Breadth & Overview
      </button>
      <button class="tab-btn" onclick="switchTab('technical')">
        <span>📈</span> Lakehouse Technical Deep Dive
      </button>
      <button class="tab-btn" onclick="switchTab('sector')">
        <span>🏢</span> Sector & Relative Risk
      </button>
    </nav>

    <!-- =================================================================== -->
    <!-- TAB 0: LIVE MULTI-MARKET TERMINAL -->
    <!-- =================================================================== -->
    <div id="tab-live-terminal" class="tab-content active">
      
      <!-- Clean, Un-Cramped Control Box -->
      <div class="control-box">
        
        <!-- Row 1: Asset Category Pills -->
        <div class="control-row">
          <span class="control-label" style="min-width: 100px;">Asset Class:</span>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <div class="market-pill active" id="pill-Indian" onclick="setMarketCategory('Indian')">
              <span>🇮🇳</span> Indian Equities (NSE/BSE)
            </div>
            <div class="market-pill" id="pill-Forex" onclick="setMarketCategory('Forex')">
              <span>💱</span> Forex & Currencies
            </div>
            <div class="market-pill" id="pill-Crypto" onclick="setMarketCategory('Crypto')">
              <span>🪙</span> Cryptocurrencies
            </div>
            <div class="market-pill" id="pill-Global" onclick="setMarketCategory('Global')">
              <span>🌐</span> Global Indices
            </div>
          </div>
        </div>

        <!-- Row 2: Preset Dropdown & Universal Search Input -->
        <div class="control-row">
          <div class="control-group">
            <label class="control-label">Select Instrument:</label>
            <select id="live-symbol-select" onchange="onLiveSymbolSelect()"></select>
          </div>
          
          <div class="control-group" style="flex: 1.5;">
            <label class="control-label">Search Any Ticker (Override):</label>
            <div style="display: flex; gap: 8px;">
              <input type="text" id="live-search-input" placeholder="Type symbol: e.g. BTC-USD, USDINR=X, RELIANCE.NS, ETH-USD, AAPL" onkeyup="handleLiveSearch(event)">
              <button class="btn btn-primary" onclick="applySearchQuery()" style="white-space: nowrap;">Search / Load</button>
            </div>
          </div>
        </div>

      </div>

      <!-- Live Asset Hero KPIs -->
      <div class="kpi-grid" id="live-asset-kpis"></div>

      <!-- Live Technical Chart -->
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title" id="live-chart-title"><span>📈</span> Live Price Action & Indicator Overlays</div>
            <div class="panel-subtitle">OHLC Candlesticks with 20 & 50-day moving averages and Bollinger Bands</div>
          </div>
          <div style="display: flex; gap: 16px; font-size: 0.8rem; align-items: center;">
            <label style="cursor: pointer;"><input type="checkbox" id="chk-live-ma20" checked onchange="renderLiveChart()"> SMA 20</label>
            <label style="cursor: pointer;"><input type="checkbox" id="chk-live-ma50" checked onchange="renderLiveChart()"> SMA 50</label>
            <label style="cursor: pointer;"><input type="checkbox" id="chk-live-bb" checked onchange="renderLiveChart()"> Bollinger</label>
          </div>
        </div>

        <div class="chart-box" id="live-price-chart" style="height: 420px;"></div>

        <!-- RSI Sub-chart -->
        <div style="margin-top: 1.25rem; border-top: 1px solid var(--border); padding-top: 1rem;">
          <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--text-muted); margin-bottom: 6px;">
            <span style="font-weight: 700;">14-Period RSI Momentum Oscillator</span>
            <span style="font-family: var(--font-mono);">Overbought (70) | Oversold (30)</span>
          </div>
          <div class="chart-box-sm" id="live-rsi-chart"></div>
        </div>
      </div>

      <!-- Quick Watch Grid -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title"><span>⚡</span> Quick-Watch Real-Time Board</div>
          <div class="panel-subtitle">Compare live prices across key instruments in the active asset class</div>
        </div>
        <div class="kpi-grid" id="quick-watch-grid"></div>
      </div>

    </div>

    <!-- =================================================================== -->
    <!-- TAB 1: LAKEHOUSE BREADTH & OVERVIEW -->
    <!-- =================================================================== -->
    <div id="tab-overview" class="tab-content">
      <div class="grid-60-40">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>📊</span> Market Breadth Dynamics & Cumulative A/D Line</div>
          </div>
          <div class="chart-box" id="breadth-chart"></div>
        </div>
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>🏢</span> Sector Daily Return (%)</div>
          </div>
          <div class="chart-box" id="sector-bar-chart"></div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div class="panel-title"><span>⚡</span> NSE Core Constituents Live Intelligence</div>
        </div>
        <div class="table-container">
          <table id="constituents-table">
            <thead>
              <tr>
                <th>Ticker</th><th>Enterprise Name</th><th>Sector</th><th>Close Price</th>
                <th>1-Day Delta</th><th>14D RSI</th><th>SMA 50 / 200</th><th>Signal</th><th>30D Vol</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 2: LAKEHOUSE TECHNICAL DEEP DIVE -->
    <!-- =================================================================== -->
    <div id="tab-technical" class="tab-content">
      <div class="panel" style="padding: 1rem 1.4rem;">
        <label style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted);">SELECT LAKEHOUSE STOCK:</label>
        <select id="stock-select" onchange="onLakehouseStockChange()" style="max-width: 400px; margin-top: 6px;"></select>
      </div>
      <div class="panel">
        <div class="chart-box" id="lakehouse-price-chart" style="height: 420px;"></div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 3: SECTOR & RELATIVE RISK -->
    <!-- =================================================================== -->
    <div id="tab-sector" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title"><span>🚀</span> Normalized Equity Growth Index (Base 100)</div>
        </div>
        <div class="chart-box" id="growth-chart" style="height: 420px;"></div>
      </div>
    </div>

  </main>

  <script>
    window.MARKET_DATA = {json.dumps(master_data)};
  </script>

  <script>
    const D = window.MARKET_DATA;
    let currentCategory = "Indian";
    let currentLiveSymbol = "RELIANCE.NS";
    let currentLakehouseStock = "RELIANCE.NS";

    function toggleTheme() {{
      const html = document.documentElement;
      if (html.classList.contains("dark")) {{
        html.classList.remove("dark");
        html.classList.add("light");
        document.getElementById("theme-toggle").innerText = "🌙 Dark View";
      }} else {{
        html.classList.remove("light");
        html.classList.add("dark");
        document.getElementById("theme-toggle").innerText = "☀️ Light View";
      }}
      renderAll();
    }}

    function switchTab(tabId) {{
      document.querySelectorAll(".tab-content").forEach(el => el.classList.remove("active"));
      document.querySelectorAll(".tab-btn").forEach(el => el.classList.remove("active"));
      document.getElementById("tab-" + tabId).classList.add("active");
      event.currentTarget.classList.add("active");

      if (tabId === "live-terminal") renderLiveTerminalTab();
      if (tabId === "overview") renderOverviewTab();
      if (tabId === "technical") renderLakehouseTechnicalTab();
      if (tabId === "sector") renderGrowthChart();
    }}

    // KPI Strip
    function renderKPIStrip() {{
      const strip = document.getElementById("kpi-strip");
      if (!strip || !D.market_summary) return;
      const lm = D.market_summary[D.market_summary.length - 1];
      const pm = D.market_summary[D.market_summary.length - 2] || lm;
      const adv = lm.advancers_count, dec = lm.decliners_count;
      const adRatio = (adv / Math.max(dec, 1)).toFixed(2);
      const ret = lm.market_avg_return_pct;
      const volCr = (lm.market_total_volume / 10000000).toFixed(2);

      strip.innerHTML = `
        <div class="kpi-card">
          <div class="kpi-label">Latest Settlement</div>
          <div class="kpi-value">${{lm.trade_date}}</div>
          <div class="kpi-delta delta-neutral">NSE Daily Settlement</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Market Breadth (A/D)</div>
          <div class="kpi-value">${{adv}} : ${{dec}}</div>
          <div class="kpi-delta ${{adv >= dec ? 'delta-bullish' : 'delta-bearish'}}">
            ${{adv >= dec ? '▲' : '▼'}} ${{adRatio}}x A/D Ratio
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Market Day Return</div>
          <div class="kpi-value">${{ret:+.2f}}%</div>
          <div class="kpi-delta ${{ret >= 0 ? 'delta-bullish' : 'delta-bearish'}}">
            ${{ret >= 0 ? '▲ Bullish' : '▼ Bearish'}}
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Traded Volume</div>
          <div class="kpi-value">${{volCr}} Cr</div>
          <div class="kpi-delta delta-neutral">${{lm.market_total_volume.toLocaleString()}} Shares</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Data Feed Status</div>
          <div class="kpi-value" style="color: var(--bullish);"><span class="live-dot"></span>Active</div>
          <div class="kpi-delta delta-neutral">4 Asset Classes Ready</div>
        </div>
      `;
    }}

    // Multi-Market Live Terminal
    function setMarketCategory(cat) {{
      currentCategory = cat;
      document.querySelectorAll(".market-pill").forEach(p => p.classList.remove("active"));
      document.getElementById("pill-" + cat).classList.add("active");
      populateSymbolDropdown();
      renderLiveTerminalTab();
    }}

    function populateSymbolDropdown() {{
      const sel = document.getElementById("live-symbol-select");
      const mm = D.multi_market || {{}};
      const filtered = Object.keys(mm).filter(sym => mm[sym].market === currentCategory);

      sel.innerHTML = filtered.map(sym => 
        `<option value="${{sym}}" ${{sym === currentLiveSymbol ? 'selected' : ''}}>${{sym}} — ${{mm[sym].name}}</option>`
      ).join('');

      if (!filtered.includes(currentLiveSymbol) && filtered.length > 0) {{
        currentLiveSymbol = filtered[0];
      }}
    }}

    function onLiveSymbolSelect() {{
      currentLiveSymbol = document.getElementById("live-symbol-select").value;
      renderLiveTerminalTab();
    }}

    function handleLiveSearch(e) {{
      if (e.key === "Enter") applySearchQuery();
    }}

    function applySearchQuery() {{
      const q = document.getElementById("live-search-input").value.trim().toUpperCase();
      if (!q) return;

      const mm = D.multi_market || {{}};
      if (mm[q]) {{
        currentLiveSymbol = q;
        currentCategory = mm[q].market;
        document.querySelectorAll(".market-pill").forEach(p => p.classList.remove("active"));
        const pill = document.getElementById("pill-" + currentCategory);
        if (pill) pill.classList.add("active");
        populateSymbolDropdown();
        document.getElementById("live-symbol-select").value = q;
        renderLiveTerminalTab();
      }} else {{
        const matched = Object.keys(mm).find(k => k.includes(q) || mm[k].name.toUpperCase().includes(q));
        if (matched) {{
          currentLiveSymbol = matched;
          currentCategory = mm[matched].market;
          document.querySelectorAll(".market-pill").forEach(p => p.classList.remove("active"));
          const pill = document.getElementById("pill-" + currentCategory);
          if (pill) pill.classList.add("active");
          populateSymbolDropdown();
          document.getElementById("live-symbol-select").value = matched;
          renderLiveTerminalTab();
        }} else {{
          alert(`Ticker '${{q}}' not found. Available: RELIANCE.NS, TCS.NS, HDFCBANK.NS, BTC-USD, ETH-USD, USDINR=X, EURUSD=X, ^NSEI, AAPL, NVDA, etc.`);
        }}
      }}
    }}

    function simulateLiveTick() {{
      const mm = D.multi_market || {{}};
      const asset = mm[currentLiveSymbol];
      if (asset) {{
        const last = asset.close.length - 1;
        const jitter = (Math.random() - 0.49) * (asset.close[last] * 0.006);
        asset.close[last] = Number((asset.close[last] + jitter).toFixed(asset.market === "Forex" ? 4 : 2));
        renderLiveTerminalTab();
      }}
    }}

    function renderLiveTerminalTab() {{
      const mm = D.multi_market || {{}};
      const asset = mm[currentLiveSymbol];
      if (!asset) return;

      const lastIdx = asset.close.length - 1;
      const currP = asset.close[lastIdx];
      const prevP = asset.close[lastIdx - 1] || currP;
      const diff = currP - prevP;
      const pct = (diff / prevP) * 100;
      const cur = asset.currency || "";

      document.getElementById("live-chart-title").innerHTML = `<span>📈</span> ${{currentLiveSymbol}} — ${{asset.name}} (Live Chart)`;

      // Live KPIs
      const kpiContainer = document.getElementById("live-asset-kpis");
      kpiContainer.innerHTML = `
        <div class="kpi-card">
          <div class="kpi-label">${{asset.name}} Last Price</div>
          <div class="kpi-value">${{cur}}${{currP.toLocaleString()}}</div>
          <div class="kpi-delta ${{pct >= 0 ? 'delta-bullish' : 'delta-bearish'}}">
            ${{pct >= 0 ? '▲' : '▼'}} ${{pct >= 0 ? '+' : ''}}${{pct.toFixed(2)}}%
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Day High / Low Range</div>
          <div class="kpi-value">${{cur}}${{asset.high[lastIdx].toLocaleString()}}</div>
          <div class="kpi-delta delta-neutral">Low: ${{cur}}${{asset.low[lastIdx].toLocaleString()}}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">20-Period Moving Avg</div>
          <div class="kpi-value">${{cur}}${{asset.sma_20[lastIdx].toLocaleString()}}</div>
          <div class="kpi-delta ${{currP >= asset.sma_20[lastIdx] ? 'delta-bullish' : 'delta-bearish'}}">
            ${{currP >= asset.sma_20[lastIdx] ? 'Above MA 20' : 'Below MA 20'}}
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">14-Period RSI</div>
          <div class="kpi-value">${{asset.rsi_14[lastIdx]}}</div>
          <div class="kpi-delta ${{asset.rsi_14[lastIdx] >= 70 ? 'delta-bearish' : (asset.rsi_14[lastIdx] <= 30 ? 'delta-bullish' : 'delta-neutral')}}">
            ${{asset.rsi_14[lastIdx] >= 70 ? 'Overbought' : (asset.rsi_14[lastIdx] <= 30 ? 'Oversold' : 'Neutral')}}
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Traded Volume</div>
          <div class="kpi-value">${{asset.volume[lastIdx] > 0 ? asset.volume[lastIdx].toLocaleString() : 'N/A (Forex)'}}</div>
          <div class="kpi-delta delta-neutral"><span class="live-dot"></span>Live Stream</div>
        </div>
      `;

      renderLiveChart();
      renderQuickWatchStrip();
    }}

    function renderLiveChart() {{
      const container = document.getElementById("live-price-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 420;

      const mm = D.multi_market || {{}};
      const asset = mm[currentLiveSymbol];
      if (!asset) return;

      const n = asset.close.length;
      const dates = asset.dates;
      const opens = asset.open;
      const highs = asset.high;
      const lows = asset.low;
      const closes = asset.close;
      const sma20 = asset.sma_20;
      const sma50 = asset.sma_50;
      const bbUp = asset.bollinger_upper;
      const bbLo = asset.bollinger_lower;

      const showMA20 = document.getElementById("chk-live-ma20").checked;
      const showMA50 = document.getElementById("chk-live-ma50").checked;
      const showBB = document.getElementById("chk-live-bb").checked;

      let minP = Math.min(...lows);
      let maxP = Math.max(...highs);
      if (showBB) {{
        minP = Math.min(minP, ...bbLo);
        maxP = Math.max(maxP, ...bbUp);
      }}
      const padY = (maxP - minP) * 0.05 || 1;
      minP -= padY; maxP += padY;

      const padL = 55, padR = 65, padT = 20, padB = 30;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      const slotW = innerW / n;
      const candleW = Math.max(slotW * 0.65, 2);

      const scaleY = p => padT + innerH * (1 - (p - minP) / (maxP - minP));

      let svg = `<svg width="${{w}}" height="${{h}}">`;

      for (let i = 0; i <= 5; i++) {{
        const price = minP + (i / 5) * (maxP - minP);
        const y = scaleY(price);
        svg += `<line x1="${{padL}}" y1="${{y}}" x2="${{w - padR}}" y2="${{y}}" stroke="var(--border-subtle)" stroke-dasharray="3,3" />`;
        svg += `<text x="${{w - padR + 8}}" y="${{y + 4}}" fill="var(--text-muted)" font-size="10">${{price.toFixed(asset.market === "Forex" ? 3 : 1)}}</text>`;
      }}

      if (showBB) {{
        let bbPath = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          bbPath += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(bbUp[i])}} `;
        }}
        for (let i = n - 1; i >= 0; i--) {{
          const cx = padL + i * slotW + slotW / 2;
          bbPath += `L ${{cx}} ${{scaleY(bbLo[i])}} `;
        }}
        bbPath += "Z";
        svg += `<path d="${{bbPath}}" fill="rgba(148, 163, 184, 0.08)" />`;
      }}

      for (let i = 0; i < n; i++) {{
        const cx = padL + i * slotW + slotW / 2;
        const op = opens[i], cl = closes[i], hi = highs[i], lo = lows[i];
        const isBull = cl >= op;
        const color = isBull ? "var(--bullish)" : "var(--bearish)";

        const yHi = scaleY(hi);
        const yLo = scaleY(lo);
        const yTop = scaleY(Math.max(op, cl));
        const yBot = scaleY(Math.min(op, cl));
        const bodyH = Math.max(yBot - yTop, 1);

        svg += `<line x1="${{cx}}" y1="${{yHi}}" x2="${{cx}}" y2="${{yLo}}" stroke="${{color}}" stroke-width="1" />`;
        svg += `<rect x="${{cx - candleW / 2}}" y="${{yTop}}" width="${{candleW}}" height="${{bodyH}}" fill="${{color}}" />`;
      }}

      function drawMA(arr, color) {{
        let p = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          p += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(arr[i])}} `;
        }}
        return `<path d="${{p}}" fill="none" stroke="${{color}}" stroke-width="1.8" />`;
      }}

      if (showMA20) svg += drawMA(sma20, "#f59e0b");
      if (showMA50) svg += drawMA(sma50, "#06b6d4");

      const step = Math.ceil(n / 6);
      for (let i = 0; i < n; i += step) {{
        const cx = padL + i * slotW + slotW / 2;
        svg += `<text x="${{cx}}" y="${{h - padB + 18}}" fill="var(--text-muted)" font-size="10" text-anchor="middle">${{dates[i].slice(5)}}</text>`;
      }}

      svg += `</svg>`;
      container.innerHTML = svg;

      renderLiveRSI(asset.rsi_14, slotW, padL, padR);
    }}

    function renderLiveRSI(rsi, slotW, padL, padR) {{
      const container = document.getElementById("live-rsi-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 120;
      const n = rsi.length;

      const padT = 15, padB = 20;
      const innerH = h - padT - padB;
      const scaleRSI = val => padT + innerH * (1 - (val - 10) / 80);

      let svg = `<svg width="${{w}}" height="${{h}}">`;
      const y70 = scaleRSI(70);
      const y30 = scaleRSI(30);

      svg += `<rect x="${{padL}}" y="${{y70}}" width="${{w - padL - padR}}" height="${{y30 - y70}}" fill="rgba(56, 189, 248, 0.05)" />`;
      svg += `<line x1="${{padL}}" y1="${{y70}}" x2="${{w - padR}}" y2="${{y70}}" stroke="rgba(244, 63, 94, 0.5)" stroke-dasharray="3,3" />`;
      svg += `<line x1="${{padL}}" y1="${{y30}}" x2="${{w - padR}}" y2="${{y30}}" stroke="rgba(16, 185, 129, 0.5)" stroke-dasharray="3,3" />`;

      let pts = "";
      for (let i = 0; i < n; i++) {{
        const cx = padL + i * slotW + slotW / 2;
        pts += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleRSI(rsi[i])}} `;
      }}
      svg += `<path d="${{pts}}" fill="none" stroke="#818cf8" stroke-width="1.8" />`;
      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderQuickWatchStrip() {{
      const grid = document.getElementById("quick-watch-grid");
      const mm = D.multi_market || {{}};
      const filtered = Object.keys(mm).filter(sym => mm[sym].market === currentCategory);

      let html = "";
      filtered.forEach(sym => {{
        const a = mm[sym];
        const last = a.close.length - 1;
        const c = a.close[last];
        const p = a.close[last - 1] || c;
        const d = ((c - p) / p) * 100;
        const color = d >= 0 ? "var(--bullish)" : "var(--bearish)";
        const arrow = d >= 0 ? "▲" : "▼";

        html += `
          <div class="kpi-card" style="cursor: pointer;" onclick="selectQuickAsset('${{sym}}')">
            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">${{sym}}</div>
            <div style="font-size: 1.25rem; font-weight: 700; font-family: var(--font-mono); margin: 3px 0;">
              ${{a.currency}}${{c.toLocaleString()}}
            </div>
            <div style="font-size: 0.75rem; font-weight: 700; color: ${{color}};">
              ${{arrow}} ${{d:+.2f}}%
            </div>
          </div>
        `;
      }});
      grid.innerHTML = html;
    }}

    function selectQuickAsset(sym) {{
      currentLiveSymbol = sym;
      document.getElementById("live-symbol-select").value = sym;
      renderLiveTerminalTab();
    }}

    // Lakehouse Overviews
    function renderOverviewTab() {{
      const containerB = document.getElementById("breadth-chart");
      const wB = containerB.clientWidth || 550;
      const hB = containerB.clientHeight || 380;
      const data = D.market_summary.slice(-30);
      const slotW = (wB - 80) / data.length;

      let svgB = `<svg width="${{wB}}" height="${{hB}}">`;
      data.forEach((d, i) => {{
        const cx = 40 + i * slotW + slotW / 2;
        const advH = (d.advancers_count / 6) * (hB - 80);
        const decH = (d.decliners_count / 6) * (hB - 80);
        svgB += `<rect x="${{cx - 6}}" y="${{hB - 40 - advH}}" width="5" height="${{advH}}" fill="var(--bullish)" />`;
        svgB += `<rect x="${{cx}}" y="${{hB - 40 - decH}}" width="5" height="${{decH}}" fill="var(--bearish)" />`;
      }});
      svgB += `</svg>`;
      containerB.innerHTML = svgB;

      const tbody = document.querySelector("#constituents-table tbody");
      tbody.innerHTML = D.companies.map(c => {{
        const st = D.stocks[c.symbol];
        const last = st.close.length - 1;
        const ret = st.daily_return_pct[last];
        return `
          <tr>
            <td style="color:var(--primary); font-weight:700;">${{c.symbol.replace('.NS', '')}}</td>
            <td>${{c.company_name}}</td>
            <td>${{c.sector}}</td>
            <td>₹${{st.close[last].toLocaleString()}}</td>
            <td style="color:${{ret >= 0 ? 'var(--bullish)' : 'var(--bearish)'}}; font-weight:700;">${{ret:+.2f}}%</td>
            <td>${{st.rsi_14[last]}}</td>
            <td>₹${{st.sma_50[last]}} / ₹${{st.sma_200[last]}}</td>
            <td><span class="badge badge-bullish">Bullish</span></td>
            <td>${{st.volatility_30d[last]}}%</td>
          </tr>
        `;
      }}).join('');
    }}

    function renderLakehouseTechnicalTab() {{
      const sel = document.getElementById("stock-select");
      sel.innerHTML = D.companies.map(c => `<option value="${{c.symbol}}">${{c.symbol}} — ${{c.company_name}}</option>`).join('');
      renderLakehouseChart();
    }}

    function onLakehouseStockChange() {{
      currentLakehouseStock = document.getElementById("stock-select").value;
      renderLakehouseChart();
    }}

    function renderLakehouseChart() {{
      const container = document.getElementById("lakehouse-price-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 420;
      const s = D.stocks[currentLakehouseStock];
      if (!s) return;

      const n = s.close.length;
      const minP = Math.min(...s.low);
      const maxP = Math.max(...s.high);
      const slotW = (w - 100) / n;
      const scaleY = p => 20 + (h - 60) * (1 - (p - minP) / (maxP - minP));

      let svg = `<svg width="${{w}}" height="${{h}}">`;
      let pts = "";
      for (let i = 0; i < n; i++) {{
        const cx = 50 + i * slotW + slotW / 2;
        pts += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(s.close[i])}} `;
      }}
      svg += `<path d="${{pts}}" fill="none" stroke="var(--primary)" stroke-width="2" />`;
      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderGrowthChart() {{
      const container = document.getElementById("growth-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 420;
      const colors = ["#38bdf8", "#818cf8", "#f43f5e", "#10b981", "#f59e0b", "#ec4899"];

      let svg = `<svg width="${{w}}" height="${{h}}">`;
      D.companies.forEach((c, idx) => {{
        const s = D.stocks[c.symbol];
        const base = s.close[0];
        const n = s.close.length;
        const slotW = (w - 120) / n;
        let pts = "";
        for (let i = 0; i < n; i++) {{
          const cx = 50 + i * slotW + slotW / 2;
          const val = (s.close[i] / base) * 100;
          const cy = 20 + (h - 60) * (1 - (val - 70) / 90);
          pts += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{cy}} `;
        }}
        svg += `<path d="${{pts}}" fill="none" stroke="${{colors[idx % colors.length]}}" stroke-width="2" />`;
      }});
      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderAll() {{
      renderKPIStrip();
      populateSymbolDropdown();
      renderLiveTerminalTab();
      renderOverviewTab();
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      renderAll();
    }});
  </script>
</body>
</html>
"""

with open("financial-market-intelligence/04_dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html)

# Also copy to artifact directory
import shutil
shutil.copyfile("financial-market-intelligence/04_dashboard/index.html", r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf\dashboard.html")

print("Fixed index.html and synced artifact dashboard.html!")
