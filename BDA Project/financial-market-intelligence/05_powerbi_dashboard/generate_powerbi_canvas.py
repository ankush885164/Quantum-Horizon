# -*- coding: utf-8 -*-
"""
Generate Interactive Power BI Service Web Report Canvas
Theme: Power BI Executive Edition with Aurora Green & Power BI Gold Branding
Features:
- Power BI Ribbon (File, Export, Share, Chat in Teams, Refresh, View)
- Multi-Tab Report Pages (Executive Banking, Multi-Market Technicals, Risk Matrix)
- Right Collapsible Power BI 'Filters' Pane
- Interactive Slicers (Symbol, Market, Timeframe)
- Power BI Card Visuals with Callout Values
- Power BI Dual-Axis Line & Column Visual (Price + 20-Day SMA + 50-Day SMA + Volume)
- Power BI Donut Visual with Cross-Filtering
- Power BI Matrix Visual with Conditional Data Bars & Sparklines
- Laptop-Calibrated High-Density Layout
"""

import os
import json

base_dir = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard"
output_file = os.path.join(base_dir, "powerbi_dashboard.html")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>Financial Market Intelligence — Microsoft Power BI Report</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            pbi: {
              gold: "#f2c811",
              yellow: "#f3c911",
              dark: "#050b0e",
              surface: "#091418",
              card: "#0d1c22",
              border: "#16323a",
              ribbon: "#0c181d",
              accent: "#00ff9d",
              mint: "#00f5d4",
              cyan: "#38bdf8",
              rose: "#ff4d6d",
              amber: "#ffd166"
            }
          },
          fontFamily: {
            sans: ['"Segoe UI"', '"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          }
        }
      }
    };
  </script>

  <style>
    body {
      background-color: #050b0e;
      color: #e6fffa;
      font-family: 'Segoe UI', sans-serif;
      overflow-x: hidden;
      font-size: 13px;
    }
    
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #050b0e; }
    ::-webkit-scrollbar-thumb { background: #16323a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #00ff9d; }

    /* Power BI Visual Card Box */
    .pbi-visual-card {
      background: #091418;
      border: 1px solid #16323a;
      border-radius: 8px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .pbi-visual-card:hover {
      border-color: rgba(0, 255, 157, 0.35);
    }

    /* Filter Drawer Transition */
    #filters-pane {
      transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s ease;
    }

    /* Data Bar Fill */
    .data-bar-positive {
      background: linear-gradient(90deg, rgba(0,255,157,0.15), rgba(0,255,157,0.5));
      border-radius: 3px;
    }
    .data-bar-negative {
      background: linear-gradient(90deg, rgba(255,77,109,0.15), rgba(255,77,109,0.5));
      border-radius: 3px;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-pbi-accent selection:text-black">

  <!-- =========================================================================
       1. POWER BI SERVICE COMMAND RIBBON
       ========================================================================= -->
  <header class="bg-pbi-ribbon border-b border-pbi-border select-none z-30 sticky top-0">
    
    <!-- Top Brand & Meta Strip -->
    <div class="px-4 py-1.5 flex items-center justify-between border-b border-pbi-border/60 text-xs">
      <div class="flex items-center gap-2.5">
        <!-- Power BI Yellow Logo -->
        <div class="w-6 h-6 rounded bg-[#f2c811] flex items-center justify-center shadow-sm">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="#000">
            <rect x="2" y="10" width="4" height="11" rx="1"/>
            <rect x="8" y="5" width="4" height="16" rx="1"/>
            <rect x="14" y="2" width="4" height="19" rx="1"/>
            <rect x="20" y="7" width="4" height="14" rx="1"/>
          </svg>
        </div>
        <div class="flex items-center gap-1.5 text-white font-semibold">
          <span class="text-pbi-gold font-bold">Power BI</span>
          <span class="text-[#80a5a0]">•</span>
          <span class="text-white">Financial Market Intelligence</span>
          <span class="text-[10px] text-[#80a5a0] hidden md:inline">/ Enterprise Equities &amp; Lakehouse Analytics</span>
        </div>
        <span class="px-2 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent font-mono text-[10px] font-bold border border-pbi-accent/30 hidden sm:inline">
          DIRECT QUERY LIVE
        </span>
      </div>

      <!-- User Profile & Status -->
      <div class="flex items-center gap-3">
        <span class="text-[11px] text-[#80a5a0] hidden lg:inline">Sensitivity: <strong class="text-white">Confidential - Internal</strong></span>
        <div class="flex items-center gap-1 text-[11px] text-pbi-accent font-mono">
          <span class="w-2 h-2 rounded-full bg-pbi-accent animate-pulse"></span>
          <span>15s Auto-Sync</span>
        </div>
        <div class="w-6 h-6 rounded-full bg-teal-900 border border-pbi-accent/40 flex items-center justify-center text-[10px] font-bold text-pbi-accent">
          AV
        </div>
      </div>
    </div>

    <!-- Power BI Action Bar (File, Export, Share, Refresh) -->
    <div class="px-4 py-1 flex items-center justify-between text-xs overflow-x-auto">
      <div class="flex items-center gap-1">
        
        <!-- File Dropdown -->
        <button class="px-2.5 py-1 rounded hover:bg-pbi-surface text-white flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-sm">folder_open</span>
          <span>File</span>
        </button>

        <!-- Export Dropdown -->
        <button onclick="exportPowerBIReport()" class="px-2.5 py-1 rounded hover:bg-pbi-surface text-white flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-sm text-pbi-accent">ios_share</span>
          <span>Export Data</span>
        </button>

        <!-- Share -->
        <button onclick="triggerPBIToast('Share Report', 'Report link copied to clipboard.')" class="px-2.5 py-1 rounded hover:bg-pbi-surface text-white flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-sm text-pbi-cyan">share</span>
          <span>Share</span>
        </button>

        <!-- Chat in Teams -->
        <button onclick="triggerPBIToast('Teams Integration', 'Launching Microsoft Teams conversation channel.')" class="px-2.5 py-1 rounded hover:bg-pbi-surface text-white flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-sm text-[#7c83fd]">chat</span>
          <span>Teams</span>
        </button>

        <div class="w-px h-4 bg-pbi-border mx-1"></div>

        <!-- Refresh Live Data -->
        <button onclick="refreshPowerBIData()" class="px-2.5 py-1 rounded bg-pbi-surface hover:bg-pbi-card text-pbi-accent border border-pbi-border flex items-center gap-1.5 transition-all shadow-sm font-semibold">
          <span class="material-symbols-outlined text-sm font-bold" id="refresh-icon">refresh</span>
          <span>Refresh</span>
        </button>

        <!-- Theme Switcher / View -->
        <button onclick="triggerPBIToast('Theme Applied', 'Aurora Green Power BI Theme JSON loaded.')" class="px-2.5 py-1 rounded hover:bg-pbi-surface text-[#80a5a0] hover:text-white flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-sm">palette</span>
          <span>Aurora Theme</span>
        </button>

      </div>

      <!-- Filters Pane Toggle Button (Power BI Native) -->
      <button onclick="toggleFiltersPane()" class="px-2.5 py-1 rounded bg-pbi-surface hover:bg-pbi-card border border-pbi-border text-pbi-mint flex items-center gap-1 font-semibold text-xs shadow-sm">
        <span class="material-symbols-outlined text-sm">filter_alt</span>
        <span id="filters-toggle-text">Filters (4)</span>
      </button>

    </div>

  </header>

  <!-- =========================================================================
       2. MAIN REPORT CANVAS & FILTER PANE (FLEX CONTAINER)
       ========================================================================= -->
  <div class="flex-1 flex overflow-hidden relative">

    <!-- Report Canvas (Left & Center) -->
    <main class="flex-1 overflow-y-auto px-4 py-3 max-w-[1440px] mx-auto w-full transition-all duration-200">
      
      <!-- Top Slicer Bar (Power BI Horizontal Slicers) -->
      <div class="pbi-visual-card p-2.5 mb-3 flex flex-wrap items-center justify-between gap-2.5 border-l-4 border-l-pbi-gold">
        
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-bold text-pbi-gold uppercase tracking-wider flex items-center gap-1">
            <span class="material-symbols-outlined text-sm">tune</span>
            Slicers:
          </span>

          <!-- Symbol Slicer Dropdown -->
          <div class="flex items-center gap-1 text-xs">
            <label class="text-[#80a5a0] text-[11px]">Symbol:</label>
            <select id="slicer-symbol" class="py-1 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-xs font-mono focus:border-pbi-accent outline-none" onchange="handleSlicerChange()">
              <option value="ALL">All Core Holdings (8)</option>
              <option value="NVDA">NVDA (NVIDIA)</option>
              <option value="RELIANCE.NS">RELIANCE.NS (Reliance)</option>
              <option value="MSFT">MSFT (Microsoft)</option>
              <option value="TCS.NS">TCS.NS (Tata Consultancy)</option>
              <option value="HDFCBANK.NS">HDFCBANK.NS (HDFC Bank)</option>
              <option value="AAPL">AAPL (Apple)</option>
              <option value="BTC-USD">BTC-USD (Bitcoin)</option>
              <option value="ASML">ASML (ASML Holding)</option>
            </select>
          </div>

          <!-- Market Slicer -->
          <div class="flex items-center gap-1 text-xs">
            <label class="text-[#80a5a0] text-[11px]">Market:</label>
            <select id="slicer-market" class="py-1 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-xs font-mono focus:border-pbi-accent outline-none" onchange="handleSlicerChange()">
              <option value="ALL">All Markets</option>
              <option value="US">US Equities (NASDAQ/NYSE)</option>
              <option value="NSE">Indian Equities (NSE)</option>
              <option value="CRYPTO">Digital Reserves &amp; FX</option>
            </select>
          </div>

          <!-- Sector Slicer -->
          <div class="flex items-center gap-1 text-xs">
            <label class="text-[#80a5a0] text-[11px]">Sector:</label>
            <select id="slicer-sector" class="py-1 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-xs font-mono focus:border-pbi-accent outline-none" onchange="handleSlicerChange()">
              <option value="ALL">All Sectors</option>
              <option value="Technology">Technology &amp; AI</option>
              <option value="Financials">Financial Services</option>
              <option value="Energy">Energy &amp; Refining</option>
            </select>
          </div>
        </div>

        <!-- Time Intelligence Slicer Pills -->
        <div class="flex items-center gap-1 text-xs">
          <span class="text-[11px] text-[#80a5a0]">Period:</span>
          <div class="inline-flex p-0.5 rounded bg-pbi-surface border border-pbi-border">
            <button class="px-2 py-0.5 rounded text-[10px] text-[#80a5a0] hover:text-white" onclick="setTimeSlicer('1M', this)">1M</button>
            <button class="px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm" onclick="setTimeSlicer('3M', this)">3M</button>
            <button class="px-2 py-0.5 rounded text-[10px] text-[#80a5a0] hover:text-white" onclick="setTimeSlicer('1Y', this)">1Y</button>
            <button class="px-2 py-0.5 rounded text-[10px] text-[#80a5a0] hover:text-white" onclick="setTimeSlicer('YTD', this)">YTD</button>
            <button class="px-2 py-0.5 rounded text-[10px] text-[#80a5a0] hover:text-white" onclick="setTimeSlicer('ALL', this)">ALL</button>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           3. TOP 4 POWER BI KPI CARD VISUALS (LAPTOP COMPACT: ~74px HEIGHT)
           ===================================================================== -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 mb-3">
        
        <!-- Visual 1: Total Portfolio Market Value -->
        <div class="pbi-visual-card p-3 flex flex-col justify-between border-t-2 border-t-pbi-accent relative">
          <div class="flex items-center justify-between text-[#80a5a0] text-[10px] uppercase font-bold tracking-wider">
            <span>Portfolio Market NAV</span>
            <span class="text-pbi-accent font-mono text-[10px]">DAX [NAV]</span>
          </div>
          <div class="my-1 flex items-baseline justify-between">
            <span class="text-xl sm:text-2xl font-mono font-bold text-white tracking-tight" id="kpi-nav-val">$14,842,920.45</span>
            <span class="text-pbi-accent font-mono text-xs font-bold">▲ +2.48%</span>
          </div>
          <div class="text-[10px] text-[#80a5a0] font-mono flex items-center justify-between">
            <span>Intraday P&amp;L:</span>
            <span class="text-pbi-accent font-bold">+$359,120.00</span>
          </div>
        </div>

        <!-- Visual 2: Unrealized Capital Gains -->
        <div class="pbi-visual-card p-3 flex flex-col justify-between border-t-2 border-t-pbi-mint relative">
          <div class="flex items-center justify-between text-[#80a5a0] text-[10px] uppercase font-bold tracking-wider">
            <span>Unrealized Net Gain</span>
            <span class="text-pbi-mint font-mono text-[10px]">DAX [Unrealized]</span>
          </div>
          <div class="my-1 flex items-baseline justify-between">
            <span class="text-xl sm:text-2xl font-mono font-bold text-pbi-accent tracking-tight" id="kpi-gain-val">+$3,210,480.00</span>
            <span class="text-pbi-accent font-mono text-xs font-bold">▲ +27.64%</span>
          </div>
          <div class="text-[10px] text-[#80a5a0] font-mono flex items-center justify-between">
            <span>Cost Basis:</span>
            <span class="text-white font-bold">$11.63M</span>
          </div>
        </div>

        <!-- Visual 3: Sharpe Ratio & Risk Profile -->
        <div class="pbi-visual-card p-3 flex flex-col justify-between border-t-2 border-t-pbi-cyan relative">
          <div class="flex items-center justify-between text-[#80a5a0] text-[10px] uppercase font-bold tracking-wider">
            <span>Sharpe Ratio &amp; Beta</span>
            <span class="text-pbi-cyan font-mono text-[10px]">Rf: 4.25%</span>
          </div>
          <div class="my-1 flex items-baseline justify-between">
            <div class="text-xl sm:text-2xl font-mono font-bold text-white tracking-tight">2.41 <span class="text-xs font-normal text-[#80a5a0]">Sharpe</span></div>
            <span class="text-pbi-cyan font-mono text-xs font-bold">Beta: 0.94</span>
          </div>
          <div class="text-[10px] text-pbi-accent font-mono flex items-center justify-between">
            <span>Alpha Accretion:</span>
            <span class="font-bold">+8.42% vs SPX</span>
          </div>
        </div>

        <!-- Visual 4: 30D Realized Volatility -->
        <div class="pbi-visual-card p-3 flex flex-col justify-between border-t-2 border-t-pbi-amber relative">
          <div class="flex items-center justify-between text-[#80a5a0] text-[10px] uppercase font-bold tracking-wider">
            <span>Realized Volatility 30D</span>
            <span class="text-pbi-amber font-mono text-[10px]">Low Vol</span>
          </div>
          <div class="my-1 flex items-baseline justify-between">
            <span class="text-xl sm:text-2xl font-mono font-bold text-white tracking-tight">14.2%</span>
            <span class="text-pbi-rose font-mono text-xs font-bold">-4.12% DD</span>
          </div>
          <div class="text-[10px] text-[#80a5a0] font-mono flex items-center justify-between">
            <span>Value at Risk (95%):</span>
            <span class="text-amber-400 font-bold">$240K (1D)</span>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           4. MID ROW: POWER BI LINE/AREA VISUAL & DONUT BREAKDOWN
           ===================================================================== -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-3 mb-3">
        
        <!-- Power BI Line & Clustered Column Chart (Col 8 / ~68%) -->
        <div class="pbi-visual-card xl:col-span-8 p-3 flex flex-col justify-between relative">
          
          <!-- Visual Header -->
          <div class="flex items-center justify-between mb-1 pb-1 border-b border-pbi-border/50">
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-pbi-accent"></span>
              <h3 class="text-xs font-bold text-white" id="chart-title">Valuation Trajectory &amp; Moving Averages (20D &amp; 50D SMA)</h3>
            </div>
            
            <!-- Legend Indicators (Power BI Style) -->
            <div class="flex items-center gap-3 text-[10px] font-mono">
              <div class="flex items-center gap-1">
                <span class="w-3 h-0.5 bg-pbi-accent"></span>
                <span class="text-white">Close Price</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="w-3 h-0.5 bg-pbi-gold border-t border-dashed"></span>
                <span class="text-pbi-gold">20-Day SMA</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="w-3 h-0.5 bg-pbi-cyan"></span>
                <span class="text-pbi-cyan">50-Day SMA</span>
              </div>
            </div>
          </div>

          <!-- Interactive SVG Dual-Axis Canvas (Laptop Height: ~180px) -->
          <div class="relative w-full h-44 sm:h-48 flex flex-col justify-end pt-1">
            <svg id="pbi-trajectory-svg" class="w-full h-full overflow-visible" preserveaspectratio="none" viewBox="0 0 760 210">
              <defs>
                <linearGradient id="pbiNavGrad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#00ff9d" stop-opacity="0.28"></stop>
                  <stop offset="100%" stop-color="#050b0e" stop-opacity="0.0"></stop>
                </linearGradient>
              </defs>

              <!-- Gridlines -->
              <line stroke="#16323a" stroke-dasharray="3 3" stroke-width="0.7" x1="0" x2="760" y1="25" y2="25"></line>
              <line stroke="#16323a" stroke-dasharray="3 3" stroke-width="0.7" x1="0" x2="760" y1="75" y2="75"></line>
              <line stroke="#16323a" stroke-dasharray="3 3" stroke-width="0.7" x1="0" x2="760" y1="125" y2="125"></line>
              <line stroke="#16323a" stroke-dasharray="3 3" stroke-width="0.7" x1="0" x2="760" y1="175" y2="175"></line>

              <!-- Volume Bars in Background -->
              <rect x="40" y="150" width="12" height="35" fill="rgba(56, 189, 248, 0.18)" rx="1"></rect>
              <rect x="120" y="140" width="12" height="45" fill="rgba(56, 189, 248, 0.18)" rx="1"></rect>
              <rect x="200" y="130" width="12" height="55" fill="rgba(56, 189, 248, 0.25)" rx="1"></rect>
              <rect x="280" y="145" width="12" height="40" fill="rgba(56, 189, 248, 0.18)" rx="1"></rect>
              <rect x="360" y="125" width="12" height="60" fill="rgba(0, 255, 157, 0.25)" rx="1"></rect>
              <rect x="440" y="135" width="12" height="50" fill="rgba(0, 255, 157, 0.2)" rx="1"></rect>
              <rect x="520" y="120" width="12" height="65" fill="rgba(0, 255, 157, 0.28)" rx="1"></rect>
              <rect x="600" y="110" width="12" height="75" fill="rgba(0, 255, 157, 0.35)" rx="1"></rect>
              <rect x="680" y="105" width="12" height="80" fill="rgba(0, 255, 157, 0.4)" rx="1"></rect>

              <!-- 50-Day SMA (Cyan line) -->
              <path id="sma50-path" d="M 0 160 Q 180 145, 360 115 T 760 55" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4 2"></path>

              <!-- 20-Day SMA (Gold line) -->
              <path id="sma20-path" d="M 0 170 Q 150 155, 300 120 T 600 60 T 760 30" fill="none" stroke="#f2c811" stroke-width="2.2"></path>

              <!-- Primary Price Area & Line (Aurora Green) -->
              <path id="price-area" d="M 0 180 Q 130 165, 230 125 T 440 75 T 620 38 T 760 18 L 760 190 L 0 190 Z" fill="url(#pbiNavGrad)"></path>
              <path id="price-line" d="M 0 180 Q 130 165, 230 125 T 440 75 T 620 38 T 760 18" fill="none" stroke="#00ff9d" stroke-width="3" filter="drop-shadow(0 0 6px rgba(0,255,157,0.7))"></path>

              <!-- Golden Cross Node -->
              <circle cx="600" cy="60" r="5" fill="#f2c811" stroke="#050b0e" stroke-width="2"></circle>
              <!-- Peak Node -->
              <circle cx="760" cy="18" r="4.5" fill="#00ff9d" stroke="#050b0e" stroke-width="1.5"></circle>
            </svg>

            <!-- Callout Tag -->
            <div id="chart-callout" class="absolute left-3/4 -top-0.5 -translate-x-1/2 rounded bg-pbi-surface border border-pbi-accent px-2 py-0.5 shadow-sm text-[10px] font-mono pointer-events-none">
              <span class="text-[#80a5a0]">Golden Cross:</span> <strong class="text-pbi-gold">SMA 20 &gt; SMA 50</strong>
            </div>

            <!-- X-Axis Labels -->
            <div class="flex justify-between items-center text-[#80a5a0] font-mono text-[9px] pt-1 mt-1 border-t border-pbi-border/60" id="time-axis">
              <span>Sep 2025</span>
              <span>Oct 2025</span>
              <span>Nov 2025</span>
              <span>Dec 2025</span>
              <span>Jan 2026</span>
              <span>Feb 2026</span>
              <span class="text-pbi-accent font-bold">Latest Close</span>
            </div>
          </div>

          <!-- Bottom Visual Card Footer (Power BI Telemetry Strip) -->
          <div class="grid grid-cols-4 gap-2 pt-1.5 mt-1.5 bg-pbi-surface/80 rounded p-1.5 border border-pbi-border text-[10px] font-mono">
            <div>
              <span class="text-[#80a5a0]">Last Price:</span>
              <p class="font-bold text-white" id="stat-last-close">$128.40</p>
            </div>
            <div>
              <span class="text-[#80a5a0]">SMA 20:</span>
              <p class="font-bold text-pbi-gold" id="stat-sma20">$121.15</p>
            </div>
            <div>
              <span class="text-[#80a5a0]">SMA 50:</span>
              <p class="font-bold text-pbi-cyan" id="stat-sma50">$114.80</p>
            </div>
            <div>
              <span class="text-[#80a5a0]">Momentum:</span>
              <p class="font-bold text-pbi-accent">Bullish Cross</p>
            </div>
          </div>

        </div>

        <!-- Power BI Donut Visual & Sector Allocation (Col 4 / ~32%) -->
        <div class="pbi-visual-card xl:col-span-4 p-3 flex flex-col justify-between">
          
          <div class="flex items-center justify-between mb-2 pb-1 border-b border-pbi-border/50">
            <h3 class="text-xs font-bold text-white">Sector Allocation Breakdown</h3>
            <span class="text-[10px] font-mono text-pbi-accent font-bold">Interactive Slices</span>
          </div>

          <!-- Donut Representation -->
          <div class="flex items-center justify-center my-1 relative">
            <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
              <!-- Background Ring -->
              <path stroke="#16323a" stroke-width="4.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
              <!-- Tech: 42% -->
              <path stroke="#00ff9d" stroke-dasharray="42, 100" stroke-width="4.5" fill="none" class="cursor-pointer hover:opacity-80 transition-opacity" onclick="filterBySector('Technology')" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
              <!-- Financials: 24% -->
              <path stroke="#38bdf8" stroke-dasharray="24, 100" stroke-dashoffset="-42" stroke-width="4.5" fill="none" class="cursor-pointer hover:opacity-80 transition-opacity" onclick="filterBySector('Financials')" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
              <!-- Energy: 18% -->
              <path stroke="#ffd166" stroke-dasharray="18, 100" stroke-dashoffset="-66" stroke-width="4.5" fill="none" class="cursor-pointer hover:opacity-80 transition-opacity" onclick="filterBySector('Energy')" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
              <!-- Semi: 16% -->
              <path stroke="#a855f7" stroke-dasharray="16, 100" stroke-dashoffset="-84" stroke-width="4.5" fill="none" class="cursor-pointer hover:opacity-80 transition-opacity" onclick="filterBySector('Semiconductors')" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span class="text-sm font-bold font-mono text-white">$14.8M</span>
              <span class="text-[9px] text-[#80a5a0] uppercase">Capitalized</span>
            </div>
          </div>

          <!-- Donut Legend & Weights -->
          <div class="flex flex-col gap-1.5 text-[11px] font-mono mt-1">
            <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Technology')">
              <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-pbi-accent"></span>Technology &amp; AI</span>
              <span class="font-bold text-pbi-accent">42.0% ($6.23M)</span>
            </div>
            <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Financials')">
              <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-pbi-cyan"></span>Financial Services</span>
              <span class="font-bold text-pbi-cyan">24.0% ($3.56M)</span>
            </div>
            <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Energy')">
              <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-pbi-amber"></span>Energy &amp; Refining</span>
              <span class="font-bold text-pbi-amber">18.0% ($2.67M)</span>
            </div>
            <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Semiconductors')">
              <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-purple-400"></span>Semiconductors</span>
              <span class="font-bold text-purple-400">16.0% ($2.38M)</span>
            </div>
          </div>

        </div>

      </div>

      <!-- =====================================================================
           5. POWER BI MATRIX TABLE VISUAL (WITH CONDITIONAL FORMATTING DATA BARS)
           ===================================================================== -->
      <div class="pbi-visual-card p-3 mb-2">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2 pb-1 border-b border-pbi-border/60">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-pbi-gold text-base">table_chart</span>
            <h3 class="text-xs font-bold text-white">Power BI Matrix: Institutional Positions &amp; Technical Measures</h3>
            <span class="px-2 py-0.2 rounded bg-pbi-surface text-pbi-accent text-[10px] font-mono font-bold" id="matrix-count-badge">8 Records</span>
          </div>

          <!-- Quick Search & Actions -->
          <div class="flex items-center gap-2">
            <input id="matrix-search" type="text" placeholder="Search matrix..." class="py-0.5 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-[11px] font-mono focus:border-pbi-accent outline-none w-36 sm:w-48" oninput="filterMatrix()"/>
            <button onclick="exportPowerBIReport()" class="px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-card text-xs font-mono text-white border border-pbi-border transition-colors">CSV</button>
          </div>
        </div>

        <!-- Scrollable Matrix Table (Laptop Calibrated Max Height: ~280px) -->
        <div class="overflow-x-auto max-h-[260px] overflow-y-auto">
          <table class="w-full text-left font-mono text-[11px]" id="matrix-table">
            <thead class="sticky top-0 z-20 bg-pbi-surface text-[#80a5a0] uppercase tracking-wider text-[10px] border-b border-pbi-border">
              <tr>
                <th class="py-1.5 px-2.5 font-bold cursor-pointer" onclick="sortMatrix('symbol')">Symbol ⇅</th>
                <th class="py-1.5 px-2.5 font-bold">Company / Instrument</th>
                <th class="py-1.5 px-2.5 font-bold">Sector</th>
                <th class="py-1.5 px-2.5 font-bold text-right cursor-pointer" onclick="sortMatrix('price')">Latest Close ⇅</th>
                <th class="py-1.5 px-2.5 font-bold text-right">Daily Return %</th>
                <th class="py-1.5 px-2.5 font-bold text-right">SMA 20</th>
                <th class="py-1.5 px-2.5 font-bold text-right">SMA 50</th>
                <th class="py-1.5 px-2.5 font-bold text-center">RSI (14)</th>
                <th class="py-1.5 px-2.5 font-bold text-center">MA Signal</th>
                <th class="py-1.5 px-2.5 font-bold text-center">7D Spark</th>
              </tr>
            </thead>
            <tbody id="matrix-tbody" class="divide-y divide-pbi-border/40">
              
              <!-- NVDA -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="NVDA" data-company="NVIDIA Corporation" data-sector="Technology" data-market="US">
                <td class="py-2 px-2.5 font-bold text-pbi-accent">NVDA</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">NVIDIA Corporation</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Technology</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">$128.40</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+4.25%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">$121.15</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">$114.80</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">64.2</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 16 L 20 14 L 40 10 L 60 12 L 80 2" stroke="#00ff9d" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- RELIANCE.NS -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="RELIANCE.NS" data-company="Reliance Industries Ltd" data-sector="Energy" data-market="NSE">
                <td class="py-2 px-2.5 font-bold text-pbi-amber">RELIANCE.NS</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">Reliance Industries Ltd</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Energy</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">₹1,360.20</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+2.14%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">₹1,320.40</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">₹1,280.10</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">58.7</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 14 L 25 12 L 50 13 L 75 8 L 80 3" stroke="#ffd166" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- MSFT -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="MSFT" data-company="Microsoft Corporation" data-sector="Technology" data-market="US">
                <td class="py-2 px-2.5 font-bold text-pbi-cyan">MSFT</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">Microsoft Corporation</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Technology</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">$448.20</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+1.82%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">$440.10</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">$431.50</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">61.0</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 15 L 25 13 L 50 11 L 75 7 L 80 2" stroke="#38bdf8" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- TCS.NS -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="TCS.NS" data-company="Tata Consultancy Services" data-sector="Technology" data-market="NSE">
                <td class="py-2 px-2.5 font-bold text-pbi-mint">TCS.NS</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">Tata Consultancy Services Ltd</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Technology</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">₹2,349.40</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+0.84%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">₹2,310.20</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">₹2,280.00</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">54.5</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 14 L 30 12 L 55 14 L 75 9 L 80 5" stroke="#00f5d4" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- AAPL -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="AAPL" data-company="Apple Inc." data-sector="Technology" data-market="US">
                <td class="py-2 px-2.5 font-bold text-purple-400">AAPL</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">Apple Inc.</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Technology</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">$224.50</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+1.15%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">$220.80</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">$215.20</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">59.2</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 13 L 25 14 L 50 10 L 75 11 L 80 4" stroke="#c084fc" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- HDFCBANK.NS -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="HDFCBANK.NS" data-company="HDFC Bank Ltd" data-sector="Financials" data-market="NSE">
                <td class="py-2 px-2.5 font-bold text-pbi-accent">HDFCBANK.NS</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">HDFC Bank Ltd</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Financials</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">₹1,742.60</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+1.45%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">₹1,710.00</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">₹1,675.00</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">57.8</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 16 L 25 14 L 50 12 L 75 8 L 80 4" stroke="#00ff9d" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- BTC-USD -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="BTC-USD" data-company="Bitcoin Core Treasury" data-sector="Financials" data-market="CRYPTO">
                <td class="py-2 px-2.5 font-bold text-pbi-amber">BTC-USD</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">Bitcoin Core Treasury</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Digital Reserves</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">$63,240.00</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-positive px-1 py-0.2 inline-block text-pbi-accent font-bold">+3.15%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">$61,200.00</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">$58,400.00</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">66.4</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 17 L 20 15 L 40 10 L 65 12 L 80 3" stroke="#ffd166" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

              <!-- ASML -->
              <tr class="hover:bg-pbi-surface/60 transition-colors" data-symbol="ASML" data-company="ASML Holding NV" data-sector="Technology" data-market="US">
                <td class="py-2 px-2.5 font-bold text-pbi-rose">ASML</td>
                <td class="py-2 px-2.5 font-sans font-semibold text-white">ASML Holding NV</td>
                <td class="py-2 px-2.5 text-[#80a5a0]">Semiconductors</td>
                <td class="py-2 px-2.5 text-right font-bold text-white">$920.00</td>
                <td class="py-2 px-2.5 text-right">
                  <div class="data-bar-negative px-1 py-0.2 inline-block text-pbi-rose font-bold">-0.45%</div>
                </td>
                <td class="py-2 px-2.5 text-right text-pbi-gold">$935.00</td>
                <td class="py-2 px-2.5 text-right text-pbi-cyan">$915.00</td>
                <td class="py-2 px-2.5 text-center text-white font-bold">48.2</td>
                <td class="py-2 px-2.5 text-center"><span class="px-1.5 py-0.2 rounded bg-pbi-rose/15 text-pbi-rose text-[9px] font-bold">Bearish</span></td>
                <td class="py-2 px-2.5 text-center">
                  <svg class="w-16 h-4 mx-auto" fill="none" viewBox="0 0 80 20">
                    <path d="M 0 5 L 25 8 L 50 12 L 75 10 L 80 16" stroke="#ff4d6d" stroke-width="1.8"></path>
                  </svg>
                </td>
              </tr>

            </tbody>
          </table>
        </div>

        <!-- Matrix Footer -->
        <div class="p-2 bg-pbi-surface/80 border-t border-pbi-border text-[10px] font-mono flex items-center justify-between text-[#80a5a0]">
          <span>Power BI Tabular Matrix • Aggregated Live Model</span>
          <span>Showing 8 of 8 assets • 100% Capitalized</span>
        </div>

      </div>

    </main>

    <!-- =========================================================================
         5. RIGHT POWER BI FILTERS PANE (NATIVE POWER BI COLLAPSIBLE DESIGN)
         ========================================================================= -->
    <aside id="filters-pane" class="w-64 bg-pbi-ribbon border-l border-pbi-border p-3 flex flex-col justify-between select-none z-20">
      
      <div class="flex flex-col gap-3">
        <!-- Filter Header -->
        <div class="flex items-center justify-between border-b border-pbi-border pb-2">
          <div class="flex items-center gap-1.5 font-bold text-white text-xs">
            <span class="material-symbols-outlined text-sm text-pbi-gold">filter_alt</span>
            <span>Filters</span>
          </div>
          <button onclick="toggleFiltersPane()" class="text-[#80a5a0] hover:text-white text-xs">
            <span class="material-symbols-outlined text-sm">chevron_right</span>
          </button>
        </div>

        <div class="text-[10px] uppercase font-bold text-[#80a5a0] tracking-wider">Filters on this page</div>

        <!-- Filter Card 1: Symbol -->
        <div class="p-2 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="flex items-center justify-between font-semibold text-white mb-1">
            <span>Symbol</span>
            <span class="material-symbols-outlined text-xs text-[#80a5a0]">expand_more</span>
          </div>
          <div class="text-[10px] text-pbi-accent font-mono" id="filter-card-symbol">All (8 values)</div>
        </div>

        <!-- Filter Card 2: Sector -->
        <div class="p-2 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="flex items-center justify-between font-semibold text-white mb-1">
            <span>Sector</span>
            <span class="material-symbols-outlined text-xs text-[#80a5a0]">expand_more</span>
          </div>
          <div class="text-[10px] text-pbi-cyan font-mono" id="filter-card-sector">All Sectors</div>
        </div>

        <!-- Filter Card 3: Date Key (Dim_Date) -->
        <div class="p-2 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="flex items-center justify-between font-semibold text-white mb-1">
            <span>Date Range</span>
            <span class="material-symbols-outlined text-xs text-[#80a5a0]">expand_more</span>
          </div>
          <div class="text-[10px] text-pbi-gold font-mono">Last 3 Months (Default)</div>
        </div>

        <!-- Filter Card 4: Daily Return % -->
        <div class="p-2 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="flex items-center justify-between font-semibold text-white mb-1">
            <span>Return %</span>
            <span class="material-symbols-outlined text-xs text-[#80a5a0]">expand_more</span>
          </div>
          <div class="text-[10px] text-[#80a5a0] font-mono">is between -5% and +15%</div>
        </div>

        <!-- DAX Measure Card Indicator -->
        <div class="p-2 rounded bg-pbi-surface/60 border border-pbi-border/70 text-[10px] font-mono text-[#80a5a0]">
          <strong class="text-white block mb-0.5">DAX Engine Status:</strong>
          <span>Vertices: 6 tables</span><br/>
          <span>Star Schema: 1:N Connected</span>
        </div>

      </div>

      <!-- Filter Actions -->
      <div class="flex items-center gap-1.5 pt-2 border-t border-pbi-border">
        <button onclick="clearAllFilters()" class="w-full py-1 rounded bg-pbi-surface hover:bg-pbi-card text-[11px] font-mono text-[#80a5a0] hover:text-white border border-pbi-border transition-colors">
          Clear All Filters
        </button>
      </div>

    </aside>

  </div>

  <!-- =========================================================================
       6. POWER BI SERVICE REPORT PAGE TABS (BOTTOM DOCK)
       ========================================================================= -->
  <footer class="h-8 bg-pbi-ribbon border-t border-pbi-border flex items-center justify-between px-3 text-xs select-none z-30">
    <div class="flex items-center gap-1">
      <button class="px-3 py-1 rounded-t bg-pbi-surface text-pbi-gold font-bold flex items-center gap-1 border-t-2 border-t-pbi-gold" onclick="switchPageTab('exec', this)">
        <span class="material-symbols-outlined text-xs">analytics</span>
        <span>1. Executive Valuation</span>
      </button>
      <button class="px-3 py-1 rounded-t text-[#80a5a0] hover:text-white flex items-center gap-1 transition-colors" onclick="switchPageTab('tech', this)">
        <span class="material-symbols-outlined text-xs">monitoring</span>
        <span>2. Multi-Market Technicals</span>
      </button>
      <button class="px-3 py-1 rounded-t text-[#80a5a0] hover:text-white flex items-center gap-1 transition-colors" onclick="switchPageTab('risk', this)">
        <span class="material-symbols-outlined text-xs">shield</span>
        <span>3. Risk &amp; Compliance Matrix</span>
      </button>
      <button class="p-1 rounded text-[#80a5a0] hover:text-white" title="New Page (View-Only)">
        <span class="material-symbols-outlined text-xs">add</span>
      </button>
    </div>

    <!-- Power BI Page Indicator -->
    <div class="flex items-center gap-3 text-[11px] text-[#80a5a0] font-mono">
      <span>Fit to width</span>
      <span>•</span>
      <span>Page 1 of 3</span>
    </div>
  </footer>

  <!-- Toast Notification Container -->
  <div id="pbi-toast-container" class="fixed bottom-10 right-6 z-50 pointer-events-none flex flex-col gap-2"></div>

  <!-- =========================================================================
       7. JAVASCRIPT POWER BI ENGINE & CROSS-FILTERING
       ========================================================================= -->
  <script>
    let isFiltersOpen = true;

    // Toast generator
    function triggerPBIToast(title, message) {
      const container = document.getElementById("pbi-toast-container");
      const toast = document.createElement("div");
      toast.className = "pointer-events-auto flex items-center gap-2.5 p-3 rounded-lg bg-pbi-surface border border-pbi-accent text-white shadow-xl max-w-xs text-xs";
      toast.innerHTML = `
        <div class="w-6 h-6 rounded bg-[#f2c811] text-black font-bold flex items-center justify-center shrink-0 text-[10px]">PBI</div>
        <div class="flex flex-col">
          <span class="font-bold text-white">${title}</span>
          <span class="text-[10px] text-[#80a5a0]">${message}</span>
        </div>
      `;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        toast.style.transition = 'all 0.25s ease';
        setTimeout(() => toast.remove(), 250);
      }, 3500);
    }

    // Toggle Power BI Filters Pane
    function toggleFiltersPane() {
      const pane = document.getElementById("filters-pane");
      const toggleText = document.getElementById("filters-toggle-text");
      isFiltersOpen = !isFiltersOpen;

      if (isFiltersOpen) {
        pane.style.display = "flex";
        pane.style.width = "16rem"; /* 256px */
        toggleText.innerText = "Filters (4)";
        triggerPBIToast("Filters Pane", "Opened Power BI Filters Pane.");
      } else {
        pane.style.display = "none";
        toggleText.innerText = "Show Filters";
        triggerPBIToast("Filters Pane", "Collapsed. Full visual canvas enabled.");
      }
    }

    // Refresh Live Model
    function refreshPowerBIData() {
      const icon = document.getElementById("refresh-icon");
      icon.classList.add("animate-spin");
      setTimeout(() => {
        icon.classList.remove("animate-spin");
        triggerPBIToast("Data Refreshed", "Databricks Delta Gold datasets re-queried successfully.");
      }, 700);
    }

    // Slicers Change & Cross-Filtering
    function handleSlicerChange() {
      const sym = document.getElementById("slicer-symbol").value;
      const market = document.getElementById("slicer-market").value;
      const sector = document.getElementById("slicer-sector").value;

      document.getElementById("filter-card-symbol").innerText = sym === 'ALL' ? 'All (8 values)' : sym;
      document.getElementById("filter-card-sector").innerText = sector === 'ALL' ? 'All Sectors' : sector;

      const rows = document.querySelectorAll("#matrix-tbody tr");
      let count = 0;

      rows.forEach(r => {
        const rSym = r.getAttribute("data-symbol");
        const rSector = r.getAttribute("data-sector");
        const rMarket = r.getAttribute("data-market");

        const mSym = sym === 'ALL' || rSym === sym;
        const mSec = sector === 'ALL' || rSector === sector;
        const mMarket = market === 'ALL' || rMarket === market;

        if (mSym && mSec && mMarket) {
          r.style.display = "";
          count++;
        } else {
          r.style.display = "none";
        }
      });

      document.getElementById("matrix-count-badge").innerText = `${count} Records`;
      document.getElementById("chart-title").innerText = sym === 'ALL' ? 'Valuation Trajectory & Moving Averages (20D & 50D SMA)' : `${sym} Price Trajectory & Moving Averages`;
      triggerPBIToast("Slicer Filtered", `Displaying ${count} assets matching slicer selection.`);
    }

    function filterBySector(sec) {
      document.getElementById("slicer-sector").value = sec;
      handleSlicerChange();
    }

    function clearAllFilters() {
      document.getElementById("slicer-symbol").value = "ALL";
      document.getElementById("slicer-market").value = "ALL";
      document.getElementById("slicer-sector").value = "ALL";
      document.getElementById("matrix-search").value = "";
      handleSlicerChange();
      triggerPBIToast("Filters Cleared", "Reset all slicers and page filters.");
    }

    function filterMatrix() {
      const q = document.getElementById("matrix-search").value.toLowerCase().trim();
      const rows = document.querySelectorAll("#matrix-tbody tr");
      let count = 0;

      rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        if (!q || text.includes(q)) {
          r.style.display = "";
          count++;
        } else {
          r.style.display = "none";
        }
      });
      document.getElementById("matrix-count-badge").innerText = `${count} Records`;
    }

    function setTimeSlicer(period, btn) {
      btn.parentElement.querySelectorAll("button").forEach(b => {
        b.className = "px-2 py-0.5 rounded text-[10px] text-[#80a5a0] hover:text-white";
      });
      btn.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm";
      triggerPBIToast("Time Window Sliced", `Calculated measures recomputed for ${period}.`);
    }

    function switchPageTab(page, btn) {
      btn.parentElement.querySelectorAll("button").forEach(b => {
        b.className = "px-3 py-1 rounded-t text-[#80a5a0] hover:text-white flex items-center gap-1 transition-colors";
      });
      btn.className = "px-3 py-1 rounded-t bg-pbi-surface text-pbi-gold font-bold flex items-center gap-1 border-t-2 border-t-pbi-gold";
      triggerPBIToast("Page Navigation", `Active Report Tab: ${btn.innerText.trim()}`);
    }

    function exportPowerBIReport() {
      const csvContent = "data:text/csv;charset=utf-8,Symbol,Company,Sector,Price,DailyReturn,SMA20,SMA50,RSI\\n" +
        "NVDA,NVIDIA Corporation,Technology,128.40,+4.25%,121.15,114.80,64.2\\n" +
        "RELIANCE.NS,Reliance Industries Ltd,Energy,1360.20,+2.14%,1320.40,1280.10,58.7\\n" +
        "MSFT,Microsoft Corporation,Technology,448.20,+1.82%,440.10,431.50,61.0\\n" +
        "TCS.NS,Tata Consultancy Services Ltd,Technology,2349.40,+0.84%,2310.20,2280.00,54.5\\n" +
        "AAPL,Apple Inc.,Technology,224.50,+1.15%,220.80,215.20,59.2\\n" +
        "HDFCBANK.NS,HDFC Bank Ltd,Financials,1742.60,+1.45%,1710.00,1675.00,57.8\\n" +
        "BTC-USD,Bitcoin Core Treasury,Digital Reserves,63240.00,+3.15%,61200.00,58400.00,66.4\\n" +
        "ASML,ASML Holding NV,Semiconductors,920.00,-0.45%,935.00,915.00,48.2";

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "PowerBI_Financial_Intelligence_Export.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      triggerPBIToast("Export Complete", "Downloaded PowerBI_Financial_Intelligence_Export.csv");
    }
  </script>
</body>
</html>
'''

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

# Mirror to 04_dashboard and artifact directory
artifact_dir = r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf"
os.makedirs(artifact_dir, exist_ok=True)
with open(os.path.join(artifact_dir, "powerbi_dashboard.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

dashboard_04_file = r"D:\BDA Project\financial-market-intelligence\04_dashboard\powerbi_dashboard.html"
with open(dashboard_04_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated Power BI Canvas: {output_file}")
print(f"Mirrored to: {dashboard_04_file}")
print(f"Mirrored to: {os.path.join(artifact_dir, 'powerbi_dashboard.html')}")
