"""
Generate standalone index.html dashboard for Financial Market Intelligence.
Embeds comprehensive market data and provides interactive SVG charts,
technical indicators, sector performance, and star schema table explorer.
"""

import json
import os

with open(os.path.join(os.path.dirname(__file__), "full_dashboard_data.json"), "r") as f:
    market_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Financial Market Intelligence — Executive Analytics Dashboard</title>
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
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
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
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.2s, color 0.2s;
    }}
    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}

    /* Layout */
    .app-header {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      padding: 0.85rem 1.75rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
      backdrop-filter: blur(8px);
    }}
    .logo-container {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo-icon {{
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 0 15px var(--primary-glow);
    }}
    .logo-text h1 {{
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .logo-text p {{
      font-size: 0.72rem;
      color: var(--text-muted);
      letter-spacing: 0.02em;
    }}
    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      transition: all 0.15s ease;
      text-decoration: none;
    }}
    .btn:hover {{
      background: var(--bg-card-hover);
      border-color: var(--primary);
    }}
    .btn-primary {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}
    .btn-primary:hover {{
      opacity: 0.9;
    }}

    /* Main Container */
    .app-main {{
      max-width: 1560px;
      width: 100%;
      margin: 0 auto;
      padding: 1.5rem 1.75rem 3rem;
      flex: 1;
    }}

    /* Hero KPI Strip */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }}
    .kpi-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.1rem 1.25rem;
      position: relative;
      overflow: hidden;
      transition: transform 0.15s, border-color 0.15s;
    }}
    .kpi-card:hover {{
      border-color: var(--primary);
      transform: translateY(-2px);
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 2px;
      background: linear-gradient(90deg, transparent, var(--primary), transparent);
      opacity: 0;
      transition: opacity 0.2s;
    }}
    .kpi-card:hover::before {{
      opacity: 1;
    }}
    .kpi-label {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 0.35rem;
    }}
    .kpi-value {{
      font-family: var(--font-mono);
      font-size: 1.6rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .kpi-delta {{
      margin-top: 0.4rem;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.76rem;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 6px;
    }}
    .delta-bullish {{ color: var(--bullish); background: var(--bullish-bg); }}
    .delta-bearish {{ color: var(--bearish); background: var(--bearish-bg); }}
    .delta-neutral {{ color: var(--text-muted); background: var(--border-subtle); }}

    /* Tabs Bar */
    .tab-bar {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 4px;
      margin-bottom: 1.5rem;
      overflow-x: auto;
    }}
    .tab-btn {{
      padding: 0.55rem 1.1rem;
      border-radius: 7px;
      font-size: 0.84rem;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      transition: all 0.15s ease;
    }}
    .tab-btn:hover {{
      color: var(--text);
      background: var(--bg-card);
    }}
    .tab-btn.active {{
      color: var(--text);
      background: var(--bg-card);
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      border: 1px solid var(--border);
    }}

    /* Card Panels */
    .panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
    }}
    .panel-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.1rem;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .panel-title {{
      font-size: 1rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .panel-subtitle {{
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* Badges */
    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.02em;
    }}
    .badge-bullish {{ color: var(--bullish); background: var(--bullish-bg); }}
    .badge-bearish {{ color: var(--bearish); background: var(--bearish-bg); }}
    .badge-neutral {{ color: var(--primary); background: var(--primary-glow); }}
    .badge-warning {{ color: var(--warning); background: var(--warning-bg); }}

    /* Data Tables */
    .table-container {{
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--bg-card);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
    }}
    th {{
      text-align: left;
      padding: 0.75rem 1rem;
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      font-weight: 600;
    }}
    td {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-subtle);
      font-family: var(--font-mono);
      font-size: 0.8rem;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    tr:hover td {{
      background: var(--bg-card-hover);
    }}
    .col-text {{
      font-family: var(--font-sans) !important;
    }}

    /* Form Controls */
    select, input {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0.45rem 0.85rem;
      border-radius: 8px;
      font-size: 0.82rem;
      font-family: var(--font-sans);
      outline: none;
      transition: border-color 0.15s;
    }}
    select:focus, input:focus {{
      border-color: var(--primary);
    }}

    /* Grid Layouts */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.25rem;
    }}
    .grid-60-40 {{
      display: grid;
      grid-template-columns: 60% 40%;
      gap: 1.25rem;
    }}
    @media (max-width: 960px) {{
      .grid-2, .grid-60-40 {{
        grid-template-columns: 1fr;
      }}
    }}

    /* SVG Chart Containers */
    .chart-box {{
      width: 100%;
      height: 380px;
      position: relative;
    }}
    .chart-box-sm {{
      width: 100%;
      height: 180px;
      position: relative;
    }}
    svg text {{
      font-family: var(--font-mono);
      user-select: none;
    }}

    /* Interactive Crosshair & Tooltip */
    .chart-tooltip {{
      position: absolute;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      pointer-events: none;
      z-index: 100;
      opacity: 0;
      transition: opacity 0.1s;
    }}

    /* Tab views */
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}

    /* Architecture Flow Diagram */
    .arch-flow {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin: 1.5rem 0;
    }}
    .arch-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.1rem;
      position: relative;
    }}
    .arch-card h4 {{
      font-size: 0.88rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .arch-badge {{
      font-size: 0.68rem;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      font-weight: 700;
      background: var(--border);
    }}
    .arch-card ul {{
      list-style: none;
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 0.5rem;
    }}
    .arch-card li {{
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .arch-card li::before {{
      content: '▸';
      color: var(--primary);
    }}
    @media (max-width: 900px) {{
      .arch-flow {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <!-- APP HEADER -->
  <header class="app-header">
    <div class="logo-container">
      <div class="logo-icon">₹</div>
      <div class="logo-text">
        <h1>Financial Market Intelligence</h1>
        <p>Enterprise Medallion Gold Analytics • NSE Blue-Chip Equities</p>
      </div>
    </div>
    <div class="header-actions">
      <span class="badge badge-bullish" style="font-size: 0.75rem;">● NSE Active Settlement</span>
      <button class="btn" id="theme-toggle" onclick="toggleTheme()">☀️ View</button>
    </div>
  </header>

  <!-- APP MAIN -->
  <main class="app-main">

    <!-- HERO KPIS -->
    <section class="kpi-grid" id="kpi-strip"></section>

    <!-- NAVIGATION TABS -->
    <nav class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('overview')">
        <span>🌐</span> Market Overview & Breadth
      </button>
      <button class="tab-btn" onclick="switchTab('technical')">
        <span>📈</span> Equity Technical Deep Dive
      </button>
      <button class="tab-btn" onclick="switchTab('sector')">
        <span>🏢</span> Sector & Relative Risk
      </button>
      <button class="tab-btn" onclick="switchTab('architecture')">
        <span>🏗️</span> Medallion Architecture & Marts
      </button>
    </nav>

    <!-- =================================================================== -->
    <!-- TAB 1: MARKET OVERVIEW -->
    <!-- =================================================================== -->
    <div id="tab-overview" class="tab-content active">
      
      <!-- Charts Row: Advance/Decline & Sector Mean Return -->
      <div class="grid-60-40">
        
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title"><span>📊</span> Market Breadth Dynamics & Cumulative A/D Line</div>
              <div class="panel-subtitle">Daily advancing vs declining constituents with cumulative net breadth indicator</div>
            </div>
          </div>
          <div class="chart-box" id="breadth-chart"></div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title"><span>🏢</span> Sector Daily Return (%)</div>
              <div class="panel-subtitle">Mean performance by industrial sector for latest trading session</div>
            </div>
          </div>
          <div class="chart-box" id="sector-bar-chart"></div>
        </div>

      </div>

      <!-- Blue-Chip Constituent Equities Table -->
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title"><span>⚡</span> NSE Core Constituents Live Intelligence</div>
            <div class="panel-subtitle">Comprehensive financial metrics, moving average signals, and 14-period momentum</div>
          </div>
        </div>
        <div class="table-container">
          <table id="constituents-table">
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Enterprise Name</th>
                <th>Sector</th>
                <th>Closing Price</th>
                <th>1-Day Delta</th>
                <th>14D RSI</th>
                <th>SMA 50 / 200</th>
                <th>Trend Signal</th>
                <th>30D Volatility</th>
                <th>Traded Volume</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- =================================================================== -->
    <!-- TAB 2: EQUITY TECHNICAL DEEP DIVE -->
    <!-- =================================================================== -->
    <div id="tab-technical" class="tab-content">
      
      <!-- Equity Selector Bar -->
      <div class="panel" style="padding: 0.9rem 1.25rem; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <label style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Select Equity:</label>
            <select id="stock-select" onchange="onStockSelectChange()"></select>
          </div>
          
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">Timeframe:</span>
            <button class="btn btn-sm" id="tf-1m" onclick="setTimeframe(20)">1M</button>
            <button class="btn btn-sm" id="tf-3m" onclick="setTimeframe(60)">3M</button>
            <button class="btn btn-sm" id="tf-6m" onclick="setTimeframe(120)">6M</button>
            <button class="btn btn-sm btn-primary" id="tf-1y" onclick="setTimeframe(250)">1Y</button>
          </div>

          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.78rem;">
            <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
              <input type="checkbox" id="show-sma-20" checked onchange="renderTechnicalChart()"> SMA 20
            </label>
            <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
              <input type="checkbox" id="show-sma-50" checked onchange="renderTechnicalChart()"> SMA 50
            </label>
            <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
              <input type="checkbox" id="show-sma-200" checked onchange="renderTechnicalChart()"> SMA 200
            </label>
            <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
              <input type="checkbox" id="show-bollinger" checked onchange="renderTechnicalChart()"> Bollinger Bands
            </label>
            <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
              <input type="checkbox" id="chart-mode-candle" checked onchange="renderTechnicalChart()"> Candlestick
            </label>
          </div>
        </div>
      </div>

      <!-- Technical Signal Indicators Cards -->
      <div class="kpi-grid" id="stock-kpis" style="margin-bottom: 1rem;"></div>

      <!-- Main Price & Indicators Chart -->
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title" id="tech-chart-title"><span>📈</span> Candlestick Price Action & Technical Overlays</div>
            <div class="panel-subtitle">Interactive chart with crosshair: OHLC prices, Moving Averages (20, 50, 200) & Bollinger Bands</div>
          </div>
          <div id="chart-legend" style="display: flex; gap: 12px; font-size: 0.72rem; font-family: var(--font-mono);"></div>
        </div>
        
        <div class="chart-box" id="price-chart" style="height: 420px;"></div>
        
        <!-- RSI Sub-chart -->
        <div style="margin-top: 1rem; border-top: 1px solid var(--border); padding-top: 0.8rem;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">
            <span style="font-weight: 700;">14-Period Relative Strength Index (RSI)</span>
            <span style="font-family: var(--font-mono);">Overbought (70) | Oversold (30)</span>
          </div>
          <div class="chart-box-sm" id="rsi-chart" style="height: 120px;"></div>
        </div>

        <!-- Volume Sub-chart -->
        <div style="margin-top: 0.8rem; border-top: 1px solid var(--border); padding-top: 0.8rem;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">
            <span style="font-weight: 700;">Daily Traded Volume</span>
            <span id="volume-latest-val" style="font-family: var(--font-mono);"></span>
          </div>
          <div class="chart-box-sm" id="volume-chart" style="height: 100px;"></div>
        </div>

      </div>

    </div>

    <!-- =================================================================== -->
    <!-- TAB 3: SECTOR & RELATIVE RISK -->
    <!-- =================================================================== -->
    <div id="tab-sector" class="tab-content">
      
      <!-- Cumulative Return Comparison (Base 100) -->
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title"><span>🚀</span> Normalized Equity Growth Index (Base 100)</div>
            <div class="panel-subtitle">Relative capital appreciation of 100 INR invested at period inception across all blue chips</div>
          </div>
        </div>
        <div class="chart-box" id="growth-chart" style="height: 400px;"></div>
      </div>

      <div class="grid-2">
        
        <!-- Risk vs Return Scatter Plot -->
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title"><span>⚖️</span> Risk-Return Spectrum</div>
              <div class="panel-subtitle">30-Day Realized Annualized Volatility vs Cumulative Return (%)</div>
            </div>
          </div>
          <div class="chart-box" id="risk-return-chart"></div>
        </div>

        <!-- Sector Volume Breakdown -->
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title"><span>🥧</span> Market Liquidity & Volume Allocation</div>
              <div class="panel-subtitle">Traded share volume distribution by industrial sector</div>
            </div>
          </div>
          <div class="chart-box" id="sector-donut-chart"></div>
        </div>

      </div>

    </div>

    <!-- =================================================================== -->
    <!-- TAB 4: ARCHITECTURE & DATA MARTS -->
    <!-- =================================================================== -->
    <div id="tab-architecture" class="tab-content">
      
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title"><span>🏗️</span> Lakehouse Medallion Pipeline Architecture</div>
            <div class="panel-subtitle">End-to-end data lineage from raw REST ingestion to Unity Catalog Star-Schema serving</div>
          </div>
        </div>

        <div class="arch-flow">
          <div class="arch-card">
            <h4><span class="arch-badge" style="color: #f59e0b; border: 1px solid #f59e0b;">Layer 0</span> Landing Volume</h4>
            <div style="font-size: 0.72rem; color: var(--primary); font-family: var(--font-mono);">/Volumes/fin_intel/landing/</div>
            <ul>
              <li>Raw multi-year OHLCV dumps</li>
              <li>yfinance & REST JSON payloads</li>
              <li>Idempotent file-based staging</li>
            </ul>
          </div>

          <div class="arch-card">
            <h4><span class="arch-badge" style="color: #cd7f32; border: 1px solid #cd7f32;">Bronze</span> Raw Delta</h4>
            <div style="font-size: 0.72rem; color: var(--primary); font-family: var(--font-mono);">fin_intel.bronze.*</div>
            <ul>
              <li>Schema enforcement on read</li>
              <li>Audit columns & batch lineage</li>
              <li>`bronze_stock_prices`</li>
              <li>`bronze_company_metadata`</li>
            </ul>
          </div>

          <div class="arch-card">
            <h4><span class="arch-badge" style="color: #94a3b8; border: 1px solid #94a3b8;">Silver</span> Cleaned Mart</h4>
            <div style="font-size: 0.72rem; color: var(--primary); font-family: var(--font-mono);">fin_intel.silver.*</div>
            <ul>
              <li>Deduplication window MERGE</li>
              <li>Price anomaly filters (H >= L)</li>
              <li>Market cap tier categorization</li>
              <li>`silver_daily_stock_prices`</li>
            </ul>
          </div>

          <div class="arch-card">
            <h4><span class="arch-badge" style="color: #eab308; border: 1px solid #eab308;">Gold</span> Curated Star</h4>
            <div style="font-size: 0.72rem; color: var(--primary); font-family: var(--font-mono);">fin_intel.gold.*</div>
            <ul>
              <li>Rolling MAs (7, 20, 50, 200)</li>
              <li>Bollinger Bands & 14D RSI</li>
              <li>30D Annualized Volatility</li>
              <li>Power BI & Tableau Serving</li>
            </ul>
          </div>
        </div>

      </div>

      <!-- Data Marts Explorer -->
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title"><span>🗄️</span> Curated Gold-Layer Data Mart Explorer</div>
            <div class="panel-subtitle">Inspect underlying Star-Schema dimensions and fact tables</div>
          </div>
          <div style="display: flex; gap: 8px;">
            <select id="mart-table-select" onchange="renderMartTable()">
              <option value="Fact_StockAnalytics">Fact_StockAnalytics (Prices & Technical Indicators)</option>
              <option value="Fact_SectorPerformance">Fact_SectorPerformance (Sector Aggregations)</option>
              <option value="Fact_MarketSummary">Fact_MarketSummary (Market Breadth & Liquidity)</option>
              <option value="Dim_Company">Dim_Company (Enterprise Profiles & Sectors)</option>
            </select>
            <button class="btn" onclick="exportActiveTableCSV()">📥 Export CSV</button>
          </div>
        </div>

        <div style="margin-bottom: 0.6rem; font-size: 0.75rem; color: var(--text-muted);" id="mart-stats"></div>
        <div class="table-container" style="max-height: 480px; overflow-y: auto;">
          <table id="mart-data-table">
            <thead><tr id="mart-headers"></tr></thead>
            <tbody id="mart-rows"></tbody>
          </table>
        </div>

      </div>

    </div>

  </main>

  <!-- EMBEDDED MARKET DATA PAYLOAD -->
  <script>
    window.MARKET_DATA = {json.dumps(market_data)};
  </script>

  <!-- DASHBOARD ENGINE LOGIC -->
  <script>
    const D = window.MARKET_DATA;
    let currentStock = "RELIANCE.NS";
    let currentTimeframe = 250; // default full year

    function toggleTheme() {{
      const html = document.documentElement;
      if (html.classList.contains("dark")) {{
        html.classList.remove("dark");
        html.classList.add("light");
        document.getElementById("theme-toggle").innerText = "🌙 Dark";
      }} else {{
        html.classList.remove("light");
        html.classList.add("dark");
        document.getElementById("theme-toggle").innerText = "☀️ Light";
      }}
      renderAll();
    }}

    function switchTab(tabId) {{
      document.querySelectorAll(".tab-content").forEach(el => el.classList.remove("active"));
      document.querySelectorAll(".tab-btn").forEach(el => el.classList.remove("active"));
      
      document.getElementById("tab-" + tabId).classList.add("active");
      event.currentTarget.classList.add("active");
      
      if (tabId === "overview") renderOverviewTab();
      if (tabId === "technical") renderTechnicalTab();
      if (tabId === "sector") renderSectorTab();
      if (tabId === "architecture") renderMartTable();
    }}

    function setTimeframe(n) {{
      currentTimeframe = n;
      document.querySelectorAll("[id^='tf-']").forEach(b => b.classList.remove("btn-primary"));
      if (n === 20) document.getElementById("tf-1m").classList.add("btn-primary");
      if (n === 60) document.getElementById("tf-3m").classList.add("btn-primary");
      if (n === 120) document.getElementById("tf-6m").classList.add("btn-primary");
      if (n === 250) document.getElementById("tf-1y").classList.add("btn-primary");
      renderTechnicalChart();
    }}

    function onStockSelectChange() {{
      currentStock = document.getElementById("stock-select").value;
      renderTechnicalTab();
    }}

    function viewStockInDeepDive(sym) {{
      currentStock = sym;
      document.getElementById("stock-select").value = sym;
      const techTabBtn = document.querySelectorAll(".tab-btn")[1];
      techTabBtn.click();
    }}

    // =========================================================================
    // 1. KPI STRIP
    // =========================================================================
    function renderKPIStrip() {{
      const latestMarket = D.market_summary[D.market_summary.length - 1];
      const prevMarket = D.market_summary[D.market_summary.length - 2];
      
      const adv = latestMarket.advancers_count;
      const dec = latestMarket.decliners_count;
      const adRatio = (adv / Math.max(dec, 1)).toFixed(2);
      
      const avgRet = latestMarket.market_avg_return_pct;
      const prevRet = prevMarket.market_avg_return_pct;
      const retDelta = (avgRet - prevRet).toFixed(2);
      
      const volCr = (latestMarket.market_total_volume / 10000000).toFixed(2);
      
      // Calculate avg realized 30d vol
      let sumVol = 0;
      let count = 0;
      for (const sym in D.stocks) {{
        const v = D.stocks[sym].volatility_30d;
        sumVol += v[v.length - 1];
        count++;
      }}
      const avgVol = (sumVol / count).toFixed(1);

      const html = `
        <div class="kpi-card">
          <div class="kpi-label">Latest Settlement Date</div>
          <div class="kpi-value">${{latestMarket.trade_date}}</div>
          <div class="kpi-delta delta-neutral">Official NSE Close</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Market Breadth (A/D)</div>
          <div class="kpi-value">${{adv}} : ${{dec}}</div>
          <div class="kpi-delta ${{adv >= dec ? 'delta-bullish' : 'delta-bearish'}}">
            ${{adv >= dec ? '▲' : '▼'}} ${{adRatio}}x A/D Ratio
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Average Day Return</div>
          <div class="kpi-value" style="color: ${{avgRet >= 0 ? 'var(--bullish)' : 'var(--bearish)'}}">
            ${{avgRet >= 0 ? '+' : ''}}${{avgRet.toFixed(2)}}%
          </div>
          <div class="kpi-delta ${{retDelta >= 0 ? 'delta-bullish' : 'delta-bearish'}}">
            ${{retDelta >= 0 ? '+' : ''}}${{retDelta}}% vs Prev
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Traded Volume</div>
          <div class="kpi-value">${{volCr}} Cr</div>
          <div class="kpi-delta delta-neutral">${{latestMarket.market_total_volume.toLocaleString()}} Shares</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Avg Realized Volatility</div>
          <div class="kpi-value">${{avgVol}}%</div>
          <div class="kpi-delta delta-neutral">Annualized 30-Day σ</div>
        </div>
      `;
      document.getElementById("kpi-strip").innerHTML = html;
    }}

    // =========================================================================
    // 2. OVERVIEW TAB
    // =========================================================================
    function renderOverviewTab() {{
      renderBreadthChart();
      renderSectorBarChart();
      renderConstituentsTable();
    }}

    function renderBreadthChart() {{
      const container = document.getElementById("breadth-chart");
      const w = container.clientWidth || 600;
      const h = container.clientHeight || 380;
      
      // Last 30 sessions
      const data = D.market_summary.slice(-30);
      const dates = data.map(d => d.trade_date);
      const adv = data.map(d => d.advancers_count);
      const dec = data.map(d => d.decliners_count);
      
      // Net breadth cumsum
      let cum = 0;
      const cumLine = data.map(d => {{
        cum += (d.advancers_count - d.decliners_count);
        return cum;
      }});
      
      const padL = 40, padR = 40, padT = 30, padB = 40;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      const n = data.length;
      const slotW = innerW / n;
      const barW = Math.max(slotW * 0.35, 3);
      
      // Y scale for bars (0 to 6)
      const maxCount = 6;
      const yScaleBar = count => padT + innerH * (1 - count / maxCount);
      
      // Y scale for line
      const minCum = Math.min(...cumLine, 0);
      const maxCum = Math.max(...cumLine, 1);
      const yScaleLine = val => padT + innerH * (1 - (val - minCum) / (maxCum - minCum || 1));
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      
      // Grid lines
      for (let i = 0; i <= maxCount; i += 2) {{
        const y = yScaleBar(i);
        svg += `<line x1="${{padL}}" y1="${{y}}" x2="${{w - padR}}" y2="${{y}}" stroke="var(--border-subtle)" stroke-dasharray="3,3" />`;
        svg += `<text x="${{padL - 8}}" y="${{y + 4}}" fill="var(--text-muted)" font-size="10" text-anchor="end">${{i}}</text>`;
      }}

      // Bars
      data.forEach((d, i) => {{
        const cx = padL + i * slotW + slotW / 2;
        
        // Adv bar (green)
        const advH = (d.advancers_count / maxCount) * innerH;
        const advY = padT + innerH - advH;
        svg += `<rect x="${{cx - barW}}" y="${{advY}}" width="${{barW - 1}}" height="${{advH}}" fill="var(--bullish)" opacity="0.8" rx="2" />`;
        
        // Dec bar (red)
        const decH = (d.decliners_count / maxCount) * innerH;
        const decY = padT + innerH - decH;
        svg += `<rect x="${{cx}}" y="${{decY}}" width="${{barW - 1}}" height="${{decH}}" fill="var(--bearish)" opacity="0.8" rx="2" />`;
        
        // Date label every 5 days
        if (i % 5 === 0 || i === n - 1) {{
          svg += `<text x="${{cx}}" y="${{h - padB + 16}}" fill="var(--text-muted)" font-size="9" text-anchor="middle">${{d.trade_date.slice(5)}}</text>`;
        }}
      }});

      // Cumulative line
      let pts = "";
      cumLine.forEach((val, i) => {{
        const cx = padL + i * slotW + slotW / 2;
        const cy = yScaleLine(val);
        pts += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{cy}} `;
      }});
      svg += `<path d="${{pts}}" fill="none" stroke="var(--primary)" stroke-width="2.5" />`;
      
      // Legend
      svg += `
        <rect x="${{w - 220}}" y="10" width="10" height="10" fill="var(--bullish)" rx="2" />
        <text x="${{w - 205}}" y="19" fill="var(--text-muted)" font-size="10">Advances</text>
        <rect x="${{w - 145}}" y="10" width="10" height="10" fill="var(--bearish)" rx="2" />
        <text x="${{w - 130}}" y="19" fill="var(--text-muted)" font-size="10">Declines</text>
        <line x1="${{w - 75}}" y1="15" x2="${{w - 55}}" y2="15" stroke="var(--primary)" stroke-width="2.5" />
        <text x="${{w - 50}}" y="19" fill="var(--text-muted)" font-size="10">A/D Line</text>
      `;

      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderSectorBarChart() {{
      const container = document.getElementById("sector-bar-chart");
      const w = container.clientWidth || 400;
      const h = container.clientHeight || 380;
      
      const latestDate = D.latest_date;
      const secData = D.sector_performance.filter(s => s.trade_date === latestDate);
      secData.sort((a, b) => b.sector_mean_return_pct - a.sector_mean_return_pct);
      
      const padL = 130, padR = 60, padT = 30, padB = 40;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      
      const maxAbs = Math.max(...secData.map(s => Math.abs(s.sector_mean_return_pct)), 1.5);
      const zeroX = padL + innerW / 2;
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      
      // Zero line
      svg += `<line x1="${{zeroX}}" y1="${{padT}}" x2="${{zeroX}}" y2="${{h - padB}}" stroke="var(--border)" stroke-width="1.5" />`;
      
      const rowH = innerH / secData.length;
      const barH = 22;
      
      secData.forEach((s, i) => {{
        const cy = padT + i * rowH + rowH / 2;
        const ret = s.sector_mean_return_pct;
        const barLen = (Math.abs(ret) / maxAbs) * (innerW / 2);
        const bx = ret >= 0 ? zeroX : zeroX - barLen;
        const color = ret >= 0 ? "var(--bullish)" : "var(--bearish)";
        
        // Label
        svg += `<text x="${{padL - 10}}" y="${{cy + 4}}" fill="var(--text)" font-size="11" font-weight="600" text-anchor="end">${{s.sector}}</text>`;
        
        // Bar
        svg += `<rect x="${{bx}}" y="${{cy - barH / 2}}" width="${{barLen}}" height="${{barH}}" fill="${{color}}" rx="4" />`;
        
        // Value text
        const textX = ret >= 0 ? bx + barLen + 8 : bx - 8;
        const anchor = ret >= 0 ? "start" : "end";
        svg += `<text x="${{textX}}" y="${{cy + 4}}" fill="${{color}}" font-size="11" font-weight="700" text-anchor="${{anchor}}">${{ret >= 0 ? '+' : ''}}${{ret.toFixed(2)}}%</text>`;
      }});

      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderConstituentsTable() {{
      const tbody = document.querySelector("#constituents-table tbody");
      let rows = "";
      
      D.companies.forEach(comp => {{
        const sym = comp.symbol;
        const s = D.stocks[sym];
        const lastIdx = s.dates.length - 1;
        const close = s.close[lastIdx];
        const ret = s.daily_return_pct[lastIdx];
        const rsi = s.rsi_14[lastIdx];
        const sma50 = s.sma_50[lastIdx];
        const sma200 = s.sma_200[lastIdx];
        const isGolden = sma50 >= sma200;
        const vol30 = s.volatility_30d[lastIdx];
        const vol = s.volume[lastIdx];
        
        let rsiBadge = '<span class="badge badge-neutral">Neutral</span>';
        if (rsi >= 70) rsiBadge = '<span class="badge badge-warning">Overbought</span>';
        if (rsi <= 30) rsiBadge = '<span class="badge badge-bearish">Oversold</span>';
        
        const trendBadge = isGolden 
          ? '<span class="badge badge-bullish">Golden Cross</span>'
          : '<span class="badge badge-bearish">Death Cross</span>';

        rows += `
          <tr>
            <td style="color: var(--primary); font-weight: 700;">${{sym.replace('.NS', '')}}</td>
            <td class="col-text">${{comp.company_name}}</td>
            <td class="col-text" style="color: var(--text-muted);">${{comp.sector}}</td>
            <td style="font-weight: 700;">₹${{close.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
            <td style="color: ${{ret >= 0 ? 'var(--bullish)' : 'var(--bearish)'}}; font-weight: 700;">
              ${{ret >= 0 ? '+' : ''}}${{ret.toFixed(2)}}%
            </td>
            <td>${{rsi.toFixed(1)}} ${{rsiBadge}}</td>
            <td>₹${{sma50.toFixed(0)}} / ₹${{sma200.toFixed(0)}}</td>
            <td>${{trendBadge}}</td>
            <td>${{vol30.toFixed(1)}}%</td>
            <td>${{vol.toLocaleString()}}</td>
            <td>
              <button class="btn btn-sm" onclick="viewStockInDeepDive('${{sym}}')">Analyze →</button>
            </td>
          </tr>
        `;
      }});
      tbody.innerHTML = rows;
    }}

    // =========================================================================
    // 3. TECHNICAL DEEP DIVE TAB
    // =========================================================================
    function initStockDropdown() {{
      const sel = document.getElementById("stock-select");
      sel.innerHTML = D.companies.map(c => 
        `<option value="${{c.symbol}}" ${{c.symbol === currentStock ? 'selected' : ''}}>
          ${{c.symbol.replace('.NS', '')}} — ${{c.company_name}} (${{c.sector}})
        </option>`
      ).join('');
    }}

    function renderTechnicalTab() {{
      initStockDropdown();
      renderStockKPIs();
      renderTechnicalChart();
    }}

    function renderStockKPIs() {{
      const s = D.stocks[currentStock];
      const comp = D.companies.find(c => c.symbol === currentStock);
      const last = s.dates.length - 1;
      
      const close = s.close[last];
      const ret = s.daily_return_pct[last];
      const rsi = s.rsi_14[last];
      const sma20 = s.sma_20[last];
      const sma50 = s.sma_50[last];
      const sma200 = s.sma_200[last];
      const bbUpper = s.bollinger_upper[last];
      const bbLower = s.bollinger_lower[last];
      const vol30 = s.volatility_30d[last];
      
      const isGC = sma50 >= sma200;
      
      const html = `
        <div class="kpi-card">
          <div class="kpi-label">${{comp.company_name}}</div>
          <div class="kpi-value">₹${{close.toFixed(2)}}</div>
          <div class="kpi-delta ${{ret >= 0 ? 'delta-bullish' : 'delta-bearish'}}">
            ${{ret >= 0 ? '▲' : '▼'}} ${{ret >= 0 ? '+' : ''}}${{ret.toFixed(2)}}% Day Delta
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">RSI 14-Period</div>
          <div class="kpi-value">${{rsi.toFixed(1)}}</div>
          <div class="kpi-delta ${{rsi >= 70 ? 'delta-bearish' : (rsi <= 30 ? 'delta-bullish' : 'delta-neutral')}}">
            ${{rsi >= 70 ? 'Overbought (>=70)' : (rsi <= 30 ? 'Oversold (<=30)' : 'Equilibrium Zone')}}
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">SMA 50 vs 200 Trend</div>
          <div class="kpi-value">₹${{sma50.toFixed(0)}}</div>
          <div class="kpi-delta ${{isGC ? 'delta-bullish' : 'delta-bearish'}}">
            ${{isGC ? '★ Golden Cross (Bull)' : '⚠ Death Cross (Bear)'}}
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Bollinger Band (±2σ)</div>
          <div class="kpi-value">₹${{(bbUpper - bbLower).toFixed(0)}} Spread</div>
          <div class="kpi-delta delta-neutral">Upper ₹${{bbUpper.toFixed(0)}} | Lower ₹${{bbLower.toFixed(0)}}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">30D Realized Volatility</div>
          <div class="kpi-value">${{vol30.toFixed(1)}}%</div>
          <div class="kpi-delta delta-neutral">Annualized Standard Deviation</div>
        </div>
      `;
      document.getElementById("stock-kpis").innerHTML = html;
      document.getElementById("tech-chart-title").innerHTML = `<span>📈</span> ${{currentStock.replace('.NS', '')}} — ${{comp.company_name}} Technical Analysis`;
    }}

    function renderTechnicalChart() {{
      const container = document.getElementById("price-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 420;
      
      const s = D.stocks[currentStock];
      const n = Math.min(currentTimeframe, s.dates.length);
      const startIdx = s.dates.length - n;
      
      const dates = s.dates.slice(startIdx);
      const opens = s.open.slice(startIdx);
      const highs = s.high.slice(startIdx);
      const lows = s.low.slice(startIdx);
      const closes = s.close.slice(startIdx);
      const sma20 = s.sma_20.slice(startIdx);
      const sma50 = s.sma_50.slice(startIdx);
      const sma200 = s.sma_200.slice(startIdx);
      const bbUpper = s.bollinger_upper.slice(startIdx);
      const bbLower = s.bollinger_lower.slice(startIdx);
      const rsi = s.rsi_14.slice(startIdx);
      const volumes = s.volume.slice(startIdx);
      
      const showSMA20 = document.getElementById("show-sma-20").checked;
      const showSMA50 = document.getElementById("show-sma-50").checked;
      const showSMA200 = document.getElementById("show-sma-200").checked;
      const showBB = document.getElementById("show-bollinger").checked;
      const isCandle = document.getElementById("chart-mode-candle").checked;
      
      // Calculate min / max for Y scale
      let minP = Math.min(...lows);
      let maxP = Math.max(...highs);
      if (showBB) {{
        minP = Math.min(minP, ...bbLower);
        maxP = Math.max(maxP, ...bbUpper);
      }}
      const padY = (maxP - minP) * 0.05;
      minP -= padY;
      maxP += padY;
      
      const padL = 50, padR = 60, padT = 20, padB = 30;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      const slotW = innerW / n;
      const candleW = Math.max(slotW * 0.65, 2);
      
      const scaleY = p => padT + innerH * (1 - (p - minP) / (maxP - minP));
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      
      // Grid lines
      for (let i = 0; i <= 5; i++) {{
        const price = minP + (i / 5) * (maxP - minP);
        const y = scaleY(price);
        svg += `<line x1="${{padL}}" y1="${{y}}" x2="${{w - padR}}" y2="${{y}}" stroke="var(--border-subtle)" stroke-dasharray="3,3" />`;
        svg += `<text x="${{w - padR + 8}}" y="${{y + 4}}" fill="var(--text-muted)" font-size="10">₹${{price.toFixed(0)}}</text>`;
      }}
      
      // Bollinger Band shaded fill
      if (showBB) {{
        let bbPath = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          const uy = scaleY(bbUpper[i]);
          bbPath += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{uy}} `;
        }}
        for (let i = n - 1; i >= 0; i--) {{
          const cx = padL + i * slotW + slotW / 2;
          const ly = scaleY(bbLower[i]);
          bbPath += `L ${{cx}} ${{ly}} `;
        }}
        bbPath += "Z";
        svg += `<path d="${{bbPath}}" fill="rgba(148, 163, 184, 0.08)" />`;
        
        // Upper line & lower line
        let upLine = "", lowLine = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          upLine += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(bbUpper[i])}} `;
          lowLine += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(bbLower[i])}} `;
        }}
        svg += `<path d="${{upLine}}" fill="none" stroke="rgba(148, 163, 184, 0.4)" stroke-width="1" stroke-dasharray="2,2" />`;
        svg += `<path d="${{lowLine}}" fill="none" stroke="rgba(148, 163, 184, 0.4)" stroke-width="1" stroke-dasharray="2,2" />`;
      }}

      // Price rendering: Candlestick or Line
      if (isCandle) {{
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
          
          // Wick
          svg += `<line x1="${{cx}}" y1="${{yHi}}" x2="${{cx}}" y2="${{yLo}}" stroke="${{color}}" stroke-width="1" />`;
          // Body
          svg += `<rect x="${{cx - candleW / 2}}" y="${{yTop}}" width="${{candleW}}" height="${{bodyH}}" fill="${{color}}" />`;
        }}
      }} else {{
        let closeLine = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          closeLine += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(closes[i])}} `;
        }}
        svg += `<path d="${{closeLine}}" fill="none" stroke="var(--primary)" stroke-width="2" />`;
      }}

      // Moving Average overlays
      function renderMA(arr, color, width, dash = "") {{
        let path = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          path += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(arr[i])}} `;
        }}
        return `<path d="${{path}}" fill="none" stroke="${{color}}" stroke-width="${{width}}" ${{dash ? `stroke-dasharray="${{dash}}"` : ''}} />`;
      }}

      if (showSMA20) svg += renderMA(sma20, "#f59e0b", 1.5);
      if (showSMA50) svg += renderMA(sma50, "#06b6d4", 1.8);
      if (showSMA200) svg += renderMA(sma200, "#ec4899", 2, "4,3");

      // Date labels on X axis
      const step = Math.ceil(n / 7);
      for (let i = 0; i < n; i += step) {{
        const cx = padL + i * slotW + slotW / 2;
        svg += `<text x="${{cx}}" y="${{h - padB + 18}}" fill="var(--text-muted)" font-size="10" text-anchor="middle">${{dates[i].slice(5)}}</text>`;
      }}

      svg += `</svg>`;
      container.innerHTML = svg;

      // Update Chart Legend
      let leg = "";
      if (showSMA20) leg += `<span style="color: #f59e0b;">● SMA 20</span>`;
      if (showSMA50) leg += `<span style="color: #06b6d4;">● SMA 50</span>`;
      if (showSMA200) leg += `<span style="color: #ec4899;">- - SMA 200</span>`;
      if (showBB) leg += `<span style="color: #94a3b8;">::: Bollinger Bands</span>`;
      document.getElementById("chart-legend").innerHTML = leg;

      // Render Sub-charts
      renderRSIChart(dates, rsi, slotW, padL, padR);
      renderVolumeChart(dates, opens, closes, volumes, slotW, padL, padR);
    }}

    function renderRSIChart(dates, rsi, slotW, padL, padR) {{
      const container = document.getElementById("rsi-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 120;
      const n = rsi.length;
      
      const padT = 15, padB = 20;
      const innerH = h - padT - padB;
      const scaleRSI = val => padT + innerH * (1 - (val - 10) / 80);
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      
      // Overbought 70 and Oversold 30 lines
      const y70 = scaleRSI(70);
      const y30 = scaleRSI(30);
      svg += `<rect x="${{padL}}" y="${{y70}}" width="${{w - padL - padR}}" height="${{y30 - y70}}" fill="rgba(56, 189, 248, 0.05)" />`;
      svg += `<line x1="${{padL}}" y1="${{y70}}" x2="${{w - padR}}" y2="${{y70}}" stroke="rgba(244, 63, 94, 0.5)" stroke-dasharray="3,3" />`;
      svg += `<line x1="${{padL}}" y1="${{y30}}" x2="${{w - padR}}" y2="${{y30}}" stroke="rgba(16, 185, 129, 0.5)" stroke-dasharray="3,3" />`;
      svg += `<text x="${{w - padR + 8}}" y="${{y70 + 4}}" fill="var(--bearish)" font-size="9">70</text>`;
      svg += `<text x="${{w - padR + 8}}" y="${{y30 + 4}}" fill="var(--bullish)" font-size="9">30</text>`;

      // RSI Path
      let pts = "";
      for (let i = 0; i < n; i++) {{
        const cx = padL + i * slotW + slotW / 2;
        pts += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleRSI(rsi[i])}} `;
      }}
      svg += `<path d="${{pts}}" fill="none" stroke="#818cf8" stroke-width="1.8" />`;

      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderVolumeChart(dates, opens, closes, volumes, slotW, padL, padR) {{
      const container = document.getElementById("volume-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 100;
      const n = volumes.length;
      
      const maxVol = Math.max(...volumes);
      const padT = 10, padB = 15;
      const innerH = h - padT - padB;
      const barW = Math.max(slotW * 0.65, 2);
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      
      for (let i = 0; i < n; i++) {{
        const cx = padL + i * slotW + slotW / 2;
        const barH = (volumes[i] / maxVol) * innerH;
        const by = padT + innerH - barH;
        const isBull = closes[i] >= opens[i];
        const color = isBull ? "var(--bullish)" : "var(--bearish)";
        svg += `<rect x="${{cx - barW / 2}}" y="${{by}}" width="${{barW}}" height="${{barH}}" fill="${{color}}" opacity="0.75" />`;
      }}

      svg += `</svg>`;
      container.innerHTML = svg;
      
      document.getElementById("volume-latest-val").innerText = `Latest: ${{volumes[n - 1].toLocaleString()}} Shares`;
    }}

    // =========================================================================
    // 4. SECTOR & RISK-RETURN TAB
    // =========================================================================
    function renderSectorTab() {{
      renderGrowthChart();
      renderRiskReturnChart();
      renderSectorDonutChart();
    }}

    function renderGrowthChart() {{
      const container = document.getElementById("growth-chart");
      const w = container.clientWidth || 900;
      const h = container.clientHeight || 400;
      
      const padL = 50, padR = 120, padT = 20, padB = 40;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      
      const colors = ["#38bdf8", "#818cf8", "#f43f5e", "#10b981", "#f59e0b", "#ec4899"];
      
      // Calculate Base 100 series
      let allNorms = [];
      const series = D.companies.map((comp, idx) => {{
        const s = D.stocks[comp.symbol];
        const base = s.close[0];
        const norm = s.close.map(c => (c / base) * 100);
        allNorms = allNorms.concat(norm);
        return {{ symbol: comp.symbol, name: comp.company_name, norm, color: colors[idx % colors.length] }};
      }});

      const minVal = Math.floor(Math.min(...allNorms) * 0.95);
      const maxVal = Math.ceil(Math.max(...allNorms) * 1.05);
      const n = D.stocks[D.companies[0].symbol].dates.length;
      const slotW = innerW / n;
      
      const scaleY = val => padT + innerH * (1 - (val - minVal) / (maxVal - minVal));
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      
      // 100 Base Line
      const y100 = scaleY(100);
      svg += `<line x1="${{padL}}" y1="${{y100}}" x2="${{w - padR}}" y2="${{y100}}" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="4,4" />`;
      svg += `<text x="${{padL - 8}}" y="${{y100 + 4}}" fill="var(--text-muted)" font-size="10" text-anchor="end">100.0</text>`;

      // Curves
      series.forEach(item => {{
        let pts = "";
        for (let i = 0; i < n; i++) {{
          const cx = padL + i * slotW + slotW / 2;
          pts += `${{i === 0 ? 'M' : 'L'}} ${{cx}} ${{scaleY(item.norm[i])}} `;
        }}
        svg += `<path d="${{pts}}" fill="none" stroke="${{item.color}}" stroke-width="2.2" />`;
        
        // Final label on right
        const lastY = scaleY(item.norm[n - 1]);
        const lastVal = item.norm[n - 1].toFixed(1);
        svg += `<text x="${{w - padR + 8}}" y="${{lastY + 4}}" fill="${{item.color}}" font-size="11" font-weight="700">${{item.symbol.replace('.NS', '')}} (${{lastVal}})</text>`;
      }});

      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderRiskReturnChart() {{
      const container = document.getElementById("risk-return-chart");
      const w = container.clientWidth || 450;
      const h = container.clientHeight || 380;
      
      const padL = 60, padR = 40, padT = 30, padB = 50;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      
      const data = D.companies.map((comp, idx) => {{
        const s = D.stocks[comp.symbol];
        const initP = s.close[0];
        const lastP = s.close[s.close.length - 1];
        const totRet = ((lastP - initP) / initP) * 100;
        const avgVol = s.volatility_30d.reduce((a, b) => a + b, 0) / s.volatility_30d.length;
        return {{ symbol: comp.symbol.replace('.NS', ''), ret: totRet, vol: avgVol, sector: comp.sector }};
      }});

      const minVol = Math.floor(Math.min(...data.map(d => d.vol)) - 3);
      const maxVol = Math.ceil(Math.max(...data.map(d => d.vol)) + 3);
      const minRet = Math.floor(Math.min(...data.map(d => d.ret)) - 5);
      const maxRet = Math.ceil(Math.max(...data.map(d => d.ret)) + 5);

      const scaleX = v => padL + innerW * ((v - minVol) / (maxVol - minVol));
      const scaleY = r => padT + innerH * (1 - (r - minRet) / (maxRet - minRet));

      let svg = `<svg width="${{w}}" height="${{h}}">`;

      // Zero return axis
      if (minRet <= 0 && maxRet >= 0) {{
        const zy = scaleY(0);
        svg += `<line x1="${{padL}}" y1="${{zy}}" x2="${{w - padR}}" y2="${{zy}}" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="3,3" />`;
      }}

      // Scatter Points
      data.forEach(d => {{
        const cx = scaleX(d.vol);
        const cy = scaleY(d.ret);
        const color = d.ret >= 0 ? "var(--bullish)" : "var(--bearish)";
        
        svg += `<circle cx="${{cx}}" cy="${{cy}}" r="9" fill="${{color}}" opacity="0.85" stroke="var(--bg-surface)" stroke-width="2" />`;
        svg += `<text x="${{cx}}" y="${{cy - 12}}" fill="var(--text)" font-size="11" font-weight="700" text-anchor="middle">${{d.symbol}}</text>`;
        svg += `<text x="${{cx}}" y="${{cy + 20}}" fill="var(--text-muted)" font-size="9" text-anchor="middle">${{d.ret.toFixed(1)}}% ret / ${{d.vol.toFixed(1)}}% vol</text>`;
      }});

      // Axis labels
      svg += `<text x="${{w / 2}}" y="${{h - 10}}" fill="var(--text-muted)" font-size="11" text-anchor="middle">Average 30D Annualized Volatility (%)</text>`;
      svg += `<text x="15" y="${{h / 2}}" fill="var(--text-muted)" font-size="11" text-anchor="middle" transform="rotate(-90 15 ${{h / 2}})">Cumulative Return (%)</text>`;

      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    function renderSectorDonutChart() {{
      const container = document.getElementById("sector-donut-chart");
      const w = container.clientWidth || 450;
      const h = container.clientHeight || 380;
      
      // Sum total volume by sector across all records
      const secMap = {{}};
      D.sector_performance.forEach(s => {{
        secMap[s.sector] = (secMap[s.sector] || 0) + s.total_sector_volume;
      }});
      
      const entries = Object.entries(secMap);
      const totalVol = entries.reduce((sum, [, val]) => sum + val, 0);
      
      const cx = w / 2;
      const cy = h / 2 - 15;
      const outerR = 105;
      const innerR = 65;
      
      const colors = ["#0284c7", "#6366f1", "#f59e0b", "#10b981"];
      
      let svg = `<svg width="${{w}}" height="${{h}}">`;
      let currentAngle = -Math.PI / 2;
      
      entries.forEach(([sec, val], i) => {{
        const sliceAngle = (val / totalVol) * 2 * Math.PI;
        const endAngle = currentAngle + sliceAngle;
        
        const x1 = cx + outerR * Math.cos(currentAngle);
        const y1 = cy + outerR * Math.sin(currentAngle);
        const x2 = cx + outerR * Math.cos(endAngle);
        const y2 = cy + outerR * Math.sin(endAngle);
        
        const ix1 = cx + innerR * Math.cos(endAngle);
        const iy1 = cy + innerR * Math.sin(endAngle);
        const ix2 = cx + innerR * Math.cos(currentAngle);
        const iy2 = cy + innerR * Math.sin(currentAngle);
        
        const largeArc = sliceAngle > Math.PI ? 1 : 0;
        const color = colors[i % colors.length];
        
        const pathData = `M ${{x1}} ${{y1}} A ${{outerR}} ${{outerR}} 0 ${{largeArc}} 1 ${{x2}} ${{y2}} L ${{ix1}} ${{iy1}} A ${{innerR}} ${{innerR}} 0 ${{largeArc}} 0 ${{ix2}} ${{iy2}} Z`;
        svg += `<path d="${{pathData}}" fill="${{color}}" opacity="0.88" stroke="var(--bg-surface)" stroke-width="2" />`;
        
        currentAngle = endAngle;
      }});

      // Center summary
      svg += `
        <text x="${{cx}}" y="${{cy - 6}}" fill="var(--text-muted)" font-size="10" text-anchor="middle">TOTAL SHARES</text>
        <text x="${{cx}}" y="${{cy + 15}}" fill="var(--text)" font-size="15" font-weight="700" text-anchor="middle">${{(totalVol / 10000000).toFixed(0)}} Cr</text>
      `;

      // Legend
      let legY = h - 45;
      let legX = 30;
      entries.forEach(([sec, val], i) => {{
        const pct = ((val / totalVol) * 100).toFixed(1);
        const color = colors[i % colors.length];
        svg += `
          <rect x="${{legX}}" y="${{legY}}" width="10" height="10" fill="${{color}}" rx="2" />
          <text x="${{legX + 16}}" y="${{legY + 9}}" fill="var(--text)" font-size="10" font-weight="600">${{sec}} (${{pct}}%)</text>
        `;
        legX += 135;
      }});

      svg += `</svg>`;
      container.innerHTML = svg;
    }}

    // =========================================================================
    // 5. ARCHITECTURE & MARTS TAB
    // =========================================================================
    function renderMartTable() {{
      const sel = document.getElementById("mart-table-select").value;
      const headRow = document.getElementById("mart-headers");
      const body = document.getElementById("mart-rows");
      
      let data = [];
      let cols = [];
      
      if (sel === "Fact_StockAnalytics") {{
        // Flat records for all stocks
        for (const sym in D.stocks) {{
          const st = D.stocks[sym];
          for (let i = Math.max(0, st.dates.length - 20); i < st.dates.length; i++) {{
            data.push({{
              symbol: sym,
              trade_date: st.dates[i],
              close: st.close[i],
              daily_return_pct: st.daily_return_pct[i],
              sma_20: st.sma_20[i],
              sma_50: st.sma_50[i],
              sma_200: st.sma_200[i],
              rsi_14: st.rsi_14[i],
              volatility_30d: st.volatility_30d[i],
              volume: st.volume[i]
            }});
          }}
        }}
        cols = ["symbol", "trade_date", "close", "daily_return_pct", "sma_20", "sma_50", "sma_200", "rsi_14", "volatility_30d", "volume"];
      }} else if (sel === "Fact_SectorPerformance") {{
        data = D.sector_performance.slice(-20);
        cols = ["trade_date", "sector", "constituent_count", "sector_mean_return_pct", "total_sector_volume", "avg_sector_volatility_30d"];
      }} else if (sel === "Fact_MarketSummary") {{
        data = D.market_summary.slice(-20);
        cols = ["trade_date", "total_traded_stocks", "advancers_count", "decliners_count", "market_avg_return_pct", "market_total_volume"];
      }} else {{
        data = D.companies;
        cols = ["symbol", "company_name", "sector", "industry", "market_cap", "market_cap_category"];
      }}

      document.getElementById("mart-stats").innerText = `Showing latest ${{data.length}} records of table: ${{sel}}`;
      
      // Header
      headRow.innerHTML = cols.map(c => `<th>${{c}}</th>`).join('');
      
      // Rows
      body.innerHTML = data.map(row => 
        `<tr>${{cols.map(c => `<td>${{row[c] !== undefined ? row[c] : ''}}</td>`).join('')}}</tr>`
      ).join('');
    }}

    function exportActiveTableCSV() {{
      const sel = document.getElementById("mart-table-select").value;
      alert(`CSV export initiated for ${{sel}}. The raw file is also available in: 03_dashboard_export/exports/${{sel}}.csv`);
    }}

    // =========================================================================
    // INITIALIZATION
    // =========================================================================
    function renderAll() {{
      renderKPIStrip();
      renderOverviewTab();
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      renderAll();
    }});
    window.addEventListener("resize", () => {{
      const activeTab = document.querySelector(".tab-content.active").id;
      if (activeTab === "tab-overview") renderOverviewTab();
      if (activeTab === "tab-technical") renderTechnicalChart();
      if (activeTab === "tab-sector") renderSectorTab();
    }});
  </script>
</body>
</html>
"""

out_path = os.path.join(os.path.dirname(__file__), "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone HTML dashboard at: {out_path} ({len(html_content):,} bytes)")
