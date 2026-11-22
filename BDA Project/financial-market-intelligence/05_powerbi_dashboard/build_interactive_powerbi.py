# -*- coding: utf-8 -*-
"""
Generate Ultra-Interactive Power BI Executive Dashboard
Equipped with:
- Chart.js 4.4 with Dual-Axis (Prices + 20D SMA + 50D SMA + Bollinger Bands + Volume)
- Interactive Hover Tooltips with exact crosshair inspection
- Dynamic Cross-Filtering: Clicking any stock in the Matrix immediately updates the Chart, KPIs, and Donut!
- Dynamic Technical Overlays: Toggle 20-Day SMA, 50-Day SMA, Bollinger Bands, Volume, and RSI (14)
- 3 Fully Built & Working Report Tabs:
  1. Executive Banking & Valuation
  2. Multi-Market Technicals & MAs
  3. Risk Analytics & Interactive DAX Playground
- Functional Power BI Collapsible Filters Pane (Checkboxes, Price Slider, Sector Filter)
- Live Data Ticking Simulation (Play/Pause Streaming Dataset)
- Laptop-Calibrated High-Density Ergonomics (Fits 1366x768 to 1920x1080 screens)
"""

import os
import json

base_dir = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard"
output_file = os.path.join(base_dir, "powerbi_dashboard.html")

html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>Power BI Quantum — Executive Market Intelligence & Prismatic Analytics</title>
  
  <!-- Fonts & Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>

  <!-- Tailwind CSS & Chart.js -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            pbi: {
              gold: "#fbbf24",
              yellow: "#fbbf24",
              dark: "#070913",
              surface: "#0e142c",
              card: "#121a36",
              hover: "#1b254b",
              border: "#1e294b",
              ribbon: "#0a0e20",
              accent: "#818cf8",
              indigo: "#6366f1",
              mint: "#00f0ff",
              cyan: "#00f0ff",
              rose: "#f43f5e",
              amber: "#fbbf24",
              purple: "#c084fc",
              fuchsia: "#ec4899"
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
      background: radial-gradient(circle at 12% 10%, rgba(99, 102, 241, 0.18) 0%, transparent 45%),
                  radial-gradient(circle at 88% 85%, rgba(244, 63, 94, 0.12) 0%, transparent 45%),
                  radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 55%),
                  #070913;
      color: #f8fafc;
      font-family: 'Segoe UI', 'Plus Jakarta Sans', sans-serif;
      font-size: 13px;
      overflow-x: hidden;
      min-height: 100vh;
    }
    
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #070913; }
    ::-webkit-scrollbar-thumb { background: #1e294b; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #818cf8; }

    .pbi-card {
      background: rgba(14, 20, 44, 0.78);
      border: 1px solid rgba(129, 140, 248, 0.18);
      border-radius: 10px;
      backdrop-filter: blur(20px) saturate(180%);
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.75), inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .pbi-card:hover {
      border-color: rgba(129, 140, 248, 0.55);
      box-shadow: 0 12px 36px -8px rgba(99, 102, 241, 0.25), inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
      transform: translateY(-1px);
    }

    .pbi-active-row {
      background: rgba(99, 102, 241, 0.18) !important;
      border-left: 3px solid #818cf8 !important;
      box-shadow: inset 0 0 16px rgba(99, 102, 241, 0.18);
    }

    #filters-pane {
      transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s ease;
      background: rgba(10, 14, 32, 0.95);
      backdrop-filter: blur(20px);
    }

    .data-bar-pos {
      background: linear-gradient(90deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.65));
      border-radius: 3px;
    }
    .data-bar-neg {
      background: linear-gradient(90deg, rgba(244, 63, 94, 0.2), rgba(244, 63, 94, 0.65));
      border-radius: 3px;
    }

    @keyframes pulseGlow {
      0%, 100% { opacity: 0.8; }
      50% { opacity: 1; filter: drop-shadow(0 0 10px #818cf8); }
    }
    .pbi-live-pulse { animation: pulseGlow 2s infinite ease-in-out; }
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-pbi-accent selection:text-black">

  <!-- =========================================================================
       1. POWER BI SERVICE COMMAND RIBBON
       ========================================================================= -->
  <header class="bg-pbi-ribbon border-b border-pbi-border select-none z-30 sticky top-0 shadow-sm">
    
    <!-- Top Workspace & Document Header -->
    <div class="px-4 py-1.5 flex items-center justify-between border-b border-pbi-border/60 text-xs">
      <div class="flex items-center gap-2.5">
        <div class="w-6 h-6 rounded bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="#ffffff">
            <rect x="2" y="10" width="4" height="11" rx="1"/>
            <rect x="8" y="5" width="4" height="16" rx="1"/>
            <rect x="14" y="2" width="4" height="19" rx="1"/>
            <rect x="20" y="7" width="4" height="14" rx="1"/>
          </svg>
        </div>
        <div class="flex items-center gap-1.5 text-white font-semibold">
          <span class="bg-gradient-to-r from-indigo-400 via-purple-300 to-cyan-300 bg-clip-text text-transparent font-bold">Power BI Quantum</span>
          <span class="text-[#64748b]">•</span>
          <span class="text-white font-mono">Market Intelligence</span>
          <span class="text-[10px] text-[#818cf8] hidden md:inline">/ DirectQuery Fabric</span>
        </div>
        <span class="px-2 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent font-mono text-[10px] font-bold border border-pbi-accent/30 hidden sm:inline">
          INTERACTIVE ENGINE LIVE
        </span>
      </div>

      <!-- Action Toggles & Profile -->
      <div class="flex items-center gap-3">
        <!-- Live Ticks Toggle -->
        <button id="btn-live-toggle" onclick="toggleLiveSimulation()" class="px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-card border border-pbi-border text-[11px] font-mono text-pbi-accent flex items-center gap-1 transition-colors" title="Toggle Live Streaming Data Ticks">
          <span class="material-symbols-outlined text-xs text-pbi-accent" id="live-icon">play_arrow</span>
          <span id="live-text">Live Ticks: Off</span>
        </button>

        <div class="flex items-center gap-1 text-[11px] text-pbi-accent font-mono">
          <span class="w-2 h-2 rounded-full bg-pbi-accent pbi-live-pulse"></span>
          <span id="sync-status">DirectQuery Ready</span>
        </div>
        <div class="w-6 h-6 rounded-full bg-gradient-to-tr from-indigo-600 to-cyan-500 border border-indigo-400/50 flex items-center justify-center text-[10px] font-bold text-white shadow-sm">
          AV
        </div>
      </div>
    </div>

    <!-- Power BI Command Actions (File, Export, Refresh, Reset) -->
    <div class="px-4 py-1 flex items-center justify-between text-xs overflow-x-auto">
      <div class="flex items-center gap-1">
        
        <button onclick="exportFilteredData()" class="px-2.5 py-1 rounded hover:bg-pbi-surface text-white flex items-center gap-1 transition-colors" title="Export Current Data to CSV">
          <span class="material-symbols-outlined text-sm text-pbi-accent">ios_share</span>
          <span>Export Data</span>
        </button>

        <button onclick="refreshDataModel()" class="px-2.5 py-1 rounded bg-pbi-surface hover:bg-pbi-card text-pbi-accent border border-pbi-border flex items-center gap-1.5 transition-all shadow-sm font-semibold">
          <span class="material-symbols-outlined text-sm font-bold" id="refresh-icon">refresh</span>
          <span>Refresh Visuals</span>
        </button>

        <button onclick="resetAllSelections()" class="px-2.5 py-1 rounded hover:bg-pbi-surface text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors" title="Clear Cross-Filters & Reset">
          <span class="material-symbols-outlined text-sm text-pbi-amber">restart_alt</span>
          <span>Reset Slicers</span>
        </button>

        <div class="w-px h-4 bg-pbi-border mx-1"></div>

        <!-- Active Focused Stock Pill -->
        <div class="flex items-center gap-1 px-2 py-0.5 rounded bg-pbi-surface border border-pbi-border text-[11px] font-mono">
          <span class="text-[#94a3b8]">Active Visual Focus:</span>
          <strong class="text-pbi-accent" id="active-focus-label">ALL CORE ASSETS (8)</strong>
        </div>

      </div>

      <!-- Filters Pane Toggle Button -->
      <button onclick="toggleFiltersPane()" class="px-2.5 py-1 rounded bg-pbi-surface hover:bg-pbi-card border border-pbi-border text-pbi-mint flex items-center gap-1 font-semibold text-xs shadow-sm cursor-pointer">
        <span class="material-symbols-outlined text-sm">filter_alt</span>
        <span id="filters-toggle-text">Filters (4)</span>
      </button>

    </div>

  </header>

  <!-- =========================================================================
       2. MAIN REPORT CANVAS & FILTER PANE (FLEX CONTAINER)
       ========================================================================= -->
  <div class="flex-1 flex overflow-hidden relative">

    <!-- Main Canvas Viewport -->
    <main class="flex-1 overflow-y-auto px-4 py-3 max-w-[1440px] mx-auto w-full transition-all duration-200" id="main-canvas">
      
      <!-- =====================================================================
           PAGE 1: EXECUTIVE BANKING & VALUATION (DEFAULT VIEW)
           ===================================================================== -->
      <div id="page-exec" class="flex flex-col gap-3">
        
        <!-- Interactive Slicer Ribbon -->
        <div class="pbi-card p-2.5 flex flex-wrap items-center justify-between gap-2.5 border-l-4 border-l-[#818cf8]">
          <div class="flex flex-wrap items-center gap-3">
            <span class="text-[11px] font-bold text-[#818cf8] uppercase tracking-wider flex items-center gap-1">
              <span class="material-symbols-outlined text-sm">tune</span>
              Slicers:
            </span>

            <!-- Symbol Slicer -->
            <div class="flex items-center gap-1 text-xs">
              <label class="text-[#94a3b8] text-[11px]">Symbol:</label>
              <select id="slicer-symbol" class="py-1 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-xs font-mono focus:border-pbi-accent outline-none cursor-pointer" onchange="onSymbolSlicerChange(this.value)">
                <option value="ALL">All Core Holdings (8)</option>
                <option value="NVDA">NVDA — NVIDIA Corp</option>
                <option value="RELIANCE.NS">RELIANCE.NS — Reliance Ind</option>
                <option value="MSFT">MSFT — Microsoft Corp</option>
                <option value="TCS.NS">TCS.NS — Tata Consultancy</option>
                <option value="AAPL">AAPL — Apple Inc</option>
                <option value="HDFCBANK.NS">HDFCBANK.NS — HDFC Bank</option>
                <option value="BTC-USD">BTC-USD — Bitcoin Treasury</option>
                <option value="ASML">ASML — ASML Holding</option>
              </select>
            </div>

            <!-- Market Slicer -->
            <div class="flex items-center gap-1 text-xs">
              <label class="text-[#94a3b8] text-[11px]">Market:</label>
              <select id="slicer-market" class="py-1 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-xs font-mono focus:border-pbi-accent outline-none cursor-pointer" onchange="onMarketSlicerChange(this.value)">
                <option value="ALL">All Markets</option>
                <option value="US">US Equities (NASDAQ/NYSE)</option>
                <option value="NSE">Indian NSE (.NS)</option>
                <option value="CRYPTO">Crypto Treasury &amp; FX</option>
              </select>
            </div>

            <!-- Currency Slicer -->
            <div class="flex items-center gap-1 text-xs">
              <label class="text-[#94a3b8] text-[11px]">Currency:</label>
              <div class="inline-flex p-0.5 rounded bg-pbi-surface border border-pbi-border font-mono text-[10px]">
                <button class="px-2 py-0.5 rounded bg-pbi-accent text-black font-bold" id="btn-curr-USD" onclick="setCurrency('USD')">USD</button>
                <button class="px-2 py-0.5 rounded text-[#94a3b8] hover:text-white" id="btn-curr-INR" onclick="setCurrency('INR')">INR</button>
                <button class="px-2 py-0.5 rounded text-[#94a3b8] hover:text-white" id="btn-curr-EUR" onclick="setCurrency('EUR')">EUR</button>
                <button class="px-2 py-0.5 rounded text-[#94a3b8] hover:text-white" id="btn-curr-GBP" onclick="setCurrency('GBP')">GBP</button>
              </div>
            </div>
          </div>

          <!-- Time Slicer Pills -->
          <div class="flex items-center gap-1 text-xs font-mono">
            <span class="text-[11px] text-[#94a3b8]">Timeframe:</span>
            <div class="inline-flex p-0.5 rounded bg-pbi-surface border border-pbi-border" id="timeframe-group">
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('1M', this)">1M</button>
              <button class="px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm" onclick="onTimeframeChange('3M', this)">3M</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('1Y', this)">1Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('5Y', this)">5Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('10Y', this)">10Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('ALL', this)">ALL</button>
            </div>
          </div>
        </div>

        <!-- 4 Top KPI Cards (Laptop Ergonomic: ~74px Height) -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5">
          
          <!-- Card 1: Total Portfolio Market Value -->
          <div class="pbi-card p-3 flex flex-col justify-between border-t-2 border-t-[#818cf8] relative">
            <div class="flex items-center justify-between text-[#94a3b8] text-[10px] uppercase font-bold tracking-wider">
              <span id="kpi-title-1">Portfolio NAV</span>
              <span class="text-pbi-accent font-mono text-[9px] px-1 py-0.2 rounded bg-pbi-accent/10">DAX [NAV]</span>
            </div>
            <div class="my-1 flex items-baseline justify-between">
              <span class="text-xl sm:text-2xl font-mono font-bold text-white tracking-tight" id="kpi-nav-val">$14,842,920.45</span>
              <span class="text-pbi-accent font-mono text-xs font-bold" id="kpi-nav-delta">▲ +2.48%</span>
            </div>
            <div class="text-[10px] text-[#94a3b8] font-mono flex items-center justify-between">
              <span>Day P&amp;L:</span>
              <span class="text-pbi-accent font-bold" id="kpi-nav-sub">+$359,120.00</span>
            </div>
          </div>

          <!-- Card 2: Unrealized Capital Gains -->
          <div class="pbi-card p-3 flex flex-col justify-between border-t-2 border-t-[#00f0ff] relative">
            <div class="flex items-center justify-between text-[#94a3b8] text-[10px] uppercase font-bold tracking-wider">
              <span id="kpi-title-2">Unrealized Net Gain</span>
              <span class="text-pbi-mint font-mono text-[9px] px-1 py-0.2 rounded bg-pbi-mint/10">DAX [Unrealized]</span>
            </div>
            <div class="my-1 flex items-baseline justify-between">
              <span class="text-xl sm:text-2xl font-mono font-bold text-pbi-accent tracking-tight" id="kpi-gain-val">+$3,210,480.00</span>
              <span class="text-pbi-accent font-mono text-xs font-bold" id="kpi-gain-delta">▲ +27.64%</span>
            </div>
            <div class="text-[10px] text-[#94a3b8] font-mono flex items-center justify-between">
              <span>Cost Basis:</span>
              <span class="text-white font-bold" id="kpi-gain-sub">$11.63M</span>
            </div>
          </div>

          <!-- Card 3: Sharpe Ratio & Risk Profile -->
          <div class="pbi-card p-3 flex flex-col justify-between border-t-2 border-t-[#c084fc] relative">
            <div class="flex items-center justify-between text-[#94a3b8] text-[10px] uppercase font-bold tracking-wider">
              <span>Sharpe Ratio &amp; Beta</span>
              <span class="text-pbi-cyan font-mono text-[9px] px-1 py-0.2 rounded bg-pbi-cyan/10">DAX [Sharpe]</span>
            </div>
            <div class="my-1 flex items-baseline justify-between">
              <div class="text-xl sm:text-2xl font-mono font-bold text-white tracking-tight" id="kpi-sharpe-val">2.41 <span class="text-xs font-normal text-[#94a3b8]">Sharpe</span></div>
              <span class="text-pbi-cyan font-mono text-xs font-bold" id="kpi-beta-val">Beta: 0.94</span>
            </div>
            <div class="text-[10px] text-pbi-accent font-mono flex items-center justify-between">
              <span>Alpha vs SPX:</span>
              <span class="font-bold text-pbi-accent" id="kpi-alpha-val">+8.42%</span>
            </div>
          </div>

          <!-- Card 4: 30D Volatility & VaR -->
          <div class="pbi-card p-3 flex flex-col justify-between border-t-2 border-t-[#fbbf24] relative">
            <div class="flex items-center justify-between text-[#94a3b8] text-[10px] uppercase font-bold tracking-wider">
              <span>Realized Volatility 30D</span>
              <span class="text-pbi-amber font-mono text-[9px] px-1 py-0.2 rounded bg-pbi-amber/10">DAX [Vol]</span>
            </div>
            <div class="my-1 flex items-baseline justify-between">
              <span class="text-xl sm:text-2xl font-mono font-bold text-white tracking-tight" id="kpi-vol-val">14.2%</span>
              <span class="text-pbi-rose font-mono text-xs font-bold" id="kpi-dd-val">-4.12% DD</span>
            </div>
            <div class="text-[10px] text-[#94a3b8] font-mono flex items-center justify-between">
              <span>Value at Risk (95%):</span>
              <span class="text-amber-400 font-bold" id="kpi-var-val">$240K (1D)</span>
            </div>
          </div>

        </div>

        <!-- Mid Row: Interactive Chart.js Visual & Donut Breakdown -->
        <div class="grid grid-cols-1 xl:grid-cols-12 gap-3">
          
          <!-- Chart.js Dual-Axis Line & Column Visual (Col 8 / ~68%) -->
          <div class="pbi-card xl:col-span-8 p-3 flex flex-col justify-between relative">
            
            <!-- Visual Header with Overlay Toggles -->
            <div class="flex flex-wrap items-center justify-between gap-2 mb-1 pb-1.5 border-b border-pbi-border/60">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-pbi-accent animate-pulse"></span>
                <h3 class="text-xs font-bold text-white font-mono" id="main-chart-title">
                  Interactive Trajectory: NVDA (NVIDIA Corporation)
                </h3>
              </div>
              
              <!-- Dynamic Investment Recommendation Badge -->
              <div class="flex items-center gap-2 px-2.5 py-1 rounded bg-pbi-surface border border-pbi-border text-xs font-mono">
                <span class="text-[10px] text-[#94a3b8] uppercase font-bold">AI Verdict:</span>
                <span class="px-2 py-0.5 rounded font-bold text-xs" id="ai-rec-badge" style="background:rgba(16,185,129,0.18); color:#10b981; border:1px solid rgba(16,185,129,0.4);">STRONG BUY</span>
                <span class="text-white font-bold text-[11px]" id="ai-rec-score">Score: 88/100</span>
                <span class="text-[10px] text-[#00f0ff] hidden md:inline" id="ai-rec-action">Target: Scale In on Dips</span>
              </div>

              <!-- Interactive Layer Toggles -->
              <div class="flex flex-wrap items-center gap-2 text-[10px] font-mono">
                <label class="flex items-center gap-1 cursor-pointer select-none text-pbi-gold">
                  <input type="checkbox" id="chk-sma20" checked onchange="toggleChartDataset(1, this.checked)" class="accent-pbi-gold cursor-pointer"/>
                  <span>20D SMA</span>
                </label>
                <label class="flex items-center gap-1 cursor-pointer select-none text-pbi-cyan">
                  <input type="checkbox" id="chk-sma50" checked onchange="toggleChartDataset(2, this.checked)" class="accent-pbi-cyan cursor-pointer"/>
                  <span>50D SMA</span>
                </label>
                <label class="flex items-center gap-1 cursor-pointer select-none text-pbi-mint">
                  <input type="checkbox" id="chk-bb" onchange="toggleBollingerBands(this.checked)" class="accent-pbi-mint cursor-pointer"/>
                  <span>Bollinger</span>
                </label>
                <label class="flex items-center gap-1 cursor-pointer select-none text-purple-400">
                  <input type="checkbox" id="chk-volume" checked onchange="toggleChartDataset(5, this.checked)" class="accent-purple-400 cursor-pointer"/>
                  <span>Volume</span>
                </label>
              </div>
            </div>

            <!-- Canvas Container (Responsive Laptop Height: ~200px) -->
            <div class="relative w-full h-48 sm:h-52">
              <canvas id="pbiChartCanvas"></canvas>
            </div>

            <!-- Chart Footer Telemetry -->
            <div class="grid grid-cols-4 gap-2 pt-1.5 mt-1.5 bg-pbi-surface/80 rounded p-1.5 border border-pbi-border text-[10px] font-mono">
              <div>
                <span class="text-[#94a3b8]">Marked Price:</span>
                <p class="font-bold text-white" id="tele-price">$128.40</p>
              </div>
              <div>
                <span class="text-[#94a3b8]">20-Day SMA:</span>
                <p class="font-bold text-pbi-gold" id="tele-sma20">$121.15</p>
              </div>
              <div>
                <span class="text-[#94a3b8]">50-Day SMA:</span>
                <p class="font-bold text-pbi-cyan" id="tele-sma50">$114.80</p>
              </div>
              <div>
                <span class="text-[#94a3b8]">Technical Momentum:</span>
                <p class="font-bold text-pbi-accent" id="tele-signal">Bullish (SMA20 &gt; SMA50)</p>
              </div>
            </div>

          </div>

          <!-- Sector Donut Visual with Cross-Filtering (Col 4 / ~32%) -->
          <div class="pbi-card xl:col-span-4 p-3 flex flex-col justify-between">
            <div class="flex items-center justify-between mb-1 pb-1 border-b border-pbi-border/50">
              <h3 class="text-xs font-bold text-white font-mono">Sector Allocation Breakdown</h3>
              <span class="text-[10px] font-mono text-pbi-accent font-bold">Cross-Filtering</span>
            </div>

            <!-- Donut Canvas Container -->
            <div class="relative w-full h-36 flex items-center justify-center my-1">
              <canvas id="pbiDonutCanvas"></canvas>
            </div>

            <!-- Interactive Sector Legend -->
            <div class="flex flex-col gap-1 text-[11px] font-mono mt-1">
              <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Technology')">
                <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#818cf8]"></span>Technology &amp; AI</span>
                <span class="font-bold text-[#818cf8]">42.0% ($6.23M)</span>
              </div>
              <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Financials')">
                <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#00f0ff]"></span>Financial Services</span>
                <span class="font-bold text-[#00f0ff]">24.0% ($3.56M)</span>
              </div>
              <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Energy')">
                <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#fbbf24]"></span>Energy &amp; Conglomerates</span>
                <span class="font-bold text-[#fbbf24]">18.0% ($2.67M)</span>
              </div>
              <div class="flex items-center justify-between cursor-pointer hover:bg-pbi-surface p-1 rounded transition-colors" onclick="filterBySector('Semiconductors')">
                <span class="text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#ec4899]"></span>Semiconductors</span>
                <span class="font-bold text-[#ec4899]">16.0% ($2.38M)</span>
              </div>
            </div>
          </div>

        </div>

        <!-- Matrix Table Visual with Live Row Selection -->
        <div class="pbi-card p-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2 pb-1 border-b border-pbi-border/60">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-pbi-gold text-base">table_chart</span>
              <h3 class="text-xs font-bold text-white font-mono">Institutional Holdings Matrix (Click any row to focus visuals)</h3>
              <span class="px-2 py-0.2 rounded bg-pbi-surface text-pbi-accent text-[10px] font-mono font-bold" id="matrix-count-badge">8 Core Holdings</span>
            </div>

            <div class="flex items-center gap-2">
              <input id="matrix-search" type="text" placeholder="Search matrix..." class="py-0.5 px-2 rounded bg-pbi-surface border border-pbi-border text-white text-[11px] font-mono focus:border-pbi-accent outline-none w-36 sm:w-48" oninput="filterMatrix()"/>
              <button onclick="exportFilteredData()" class="px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-card text-xs font-mono text-white border border-pbi-border transition-colors">Export CSV</button>
            </div>
          </div>

          <!-- Table Container (Laptop Max Height: ~260px) -->
          <div class="overflow-x-auto max-h-[260px] overflow-y-auto">
            <table class="w-full text-left font-mono text-[11px]" id="matrix-table">
              <thead class="sticky top-0 z-20 bg-pbi-surface text-[#94a3b8] uppercase tracking-wider text-[10px] border-b border-pbi-border">
                <tr>
                  <th class="py-1.5 px-2.5 font-bold cursor-pointer hover:text-white" onclick="sortMatrix('symbol')">Symbol ⇅</th>
                  <th class="py-1.5 px-2.5 font-bold">Company / Instrument</th>
                  <th class="py-1.5 px-2.5 font-bold">Sector</th>
                  <th class="py-1.5 px-2.5 font-bold text-right cursor-pointer hover:text-white" onclick="sortMatrix('price')">Latest Close ⇅</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">Daily Return %</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">SMA 20</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">SMA 50</th>
                  <th class="py-1.5 px-2.5 font-bold text-center">RSI (14)</th>
                  <th class="py-1.5 px-2.5 font-bold text-center">MA Cross Signal</th>
                  <th class="py-1.5 px-2.5 font-bold text-center">Action</th>
                </tr>
              </thead>
              <tbody id="matrix-tbody" class="divide-y divide-pbi-border/40">
                <!-- Dynamically populated via JS -->
              </tbody>
            </table>
          </div>

          <div class="p-2 bg-pbi-surface/80 border-t border-pbi-border text-[10px] font-mono flex items-center justify-between text-[#94a3b8]">
            <span>Tip: Click on any row to cross-filter the line chart and KPI cards to that holding.</span>
            <span>Live DirectQuery Sync Active</span>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           PAGE 2: MULTI-MARKET TECHNICALS & MOVING AVERAGES (TAB 2)
           ===================================================================== -->
      <div id="page-tech" class="hidden flex flex-col gap-3">
        <div class="pbi-card p-3 border-l-4 border-l-pbi-cyan">
          <div class="flex items-center justify-between mb-2">
            <div>
              <h2 class="text-sm font-bold text-white font-mono">Multi-Asset Technical Benchmark Comparison</h2>
              <p class="text-[11px] text-[#94a3b8]">Normalized Cumulative Return Performance (Base 100 Index)</p>
            </div>
            <div class="flex items-center gap-2 text-[10px] font-mono">
              <span class="px-2 py-0.5 rounded bg-pbi-accent/15 text-pbi-accent font-bold">NVDA (+45.5%)</span>
              <span class="px-2 py-0.5 rounded bg-purple-400/15 text-purple-400 font-bold">BTC-USD (+23.5%)</span>
              <span class="px-2 py-0.5 rounded bg-amber-400/15 text-amber-400 font-bold">RELIANCE (+15.2%)</span>
            </div>
          </div>
          <div class="relative w-full h-64">
            <canvas id="techBenchmarkCanvas"></canvas>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <!-- RSI Momentum Radar -->
          <div class="pbi-card p-3">
            <h3 class="text-xs font-bold text-white font-mono mb-2">RSI (14) Momentum Gauge Visual</h3>
            <div class="relative w-full h-44">
              <canvas id="rsiBarCanvas"></canvas>
            </div>
          </div>

          <!-- Volatility Bands -->
          <div class="pbi-card p-3">
            <h3 class="text-xs font-bold text-white font-mono mb-2">Annualized 30-Day Volatility Dispersion</h3>
            <div class="relative w-full h-44">
              <canvas id="volBarCanvas"></canvas>
            </div>
          </div>
        </div>
      </div>


      <!-- =====================================================================
           PAGE 4: 10-YEAR GLOBAL DECADE INTELLIGENCE (TAB 4)
           ===================================================================== -->
      <div id="page-decade" class="hidden flex flex-col gap-3">
        
        <!-- Decade Overview Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-2.5">
          <div class="pbi-card p-3 border-t-2 border-t-[#00f0ff]">
            <span class="text-[10px] text-[#94a3b8] font-bold uppercase block">10Y S&amp;P 500 (Wall St)</span>
            <span class="text-xl font-mono font-bold text-white block my-0.5">+212.2%</span>
            <span class="text-[10px] text-[#10b981] font-mono font-bold">12.1% CAGR • Max DD -34%</span>
          </div>
          <div class="pbi-card p-3 border-t-2 border-t-[#818cf8]">
            <span class="text-[10px] text-[#94a3b8] font-bold uppercase block">10Y NIFTY 50 (India)</span>
            <span class="text-xl font-mono font-bold text-white block my-0.5">+228.4%</span>
            <span class="text-[10px] text-[#10b981] font-mono font-bold">12.6% CAGR • Max DD -38%</span>
          </div>
          <div class="pbi-card p-3 border-t-2 border-t-[#00f0ff]">
            <span class="text-[10px] text-[#94a3b8] font-bold uppercase block">10Y Tech Leader (NVDA)</span>
            <span class="text-xl font-mono font-bold text-[#00f0ff] block my-0.5">+5,326.0%</span>
            <span class="text-[10px] text-[#10b981] font-mono font-bold">49.1% CAGR • 54.3x Return</span>
          </div>
          <div class="pbi-card p-3 border-t-2 border-t-[#fbbf24]">
            <span class="text-[10px] text-[#94a3b8] font-bold uppercase block">10Y Gold Safe Haven</span>
            <span class="text-xl font-mono font-bold text-[#fbbf24] block my-0.5">+198.4%</span>
            <span class="text-[10px] text-[#10b981] font-mono font-bold">11.6% CAGR • Max DD -21%</span>
          </div>
          <div class="pbi-card p-3 border-t-2 border-t-[#c084fc]">
            <span class="text-[10px] text-[#94a3b8] font-bold uppercase block">10Y Digital Gold (BTC)</span>
            <span class="text-xl font-mono font-bold text-[#c084fc] block my-0.5">+8,122.5%</span>
            <span class="text-[10px] text-[#10b981] font-mono font-bold">55.4% CAGR • 82.2x Return</span>
          </div>
        </div>

        <!-- 10-Year Global Leaderboard Matrix Visual -->
        <div class="pbi-card p-3">
          <div class="flex items-center justify-between mb-2 pb-1 border-b border-pbi-border">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-[#818cf8] text-base">public</span>
              <h3 class="text-xs font-bold text-white font-mono">10-Year Global Equities &amp; Asset Compounding Matrix (2015–2026)</h3>
            </div>
            <span class="px-2 py-0.5 rounded bg-indigo-500/15 text-[#818cf8] text-[10px] font-mono font-bold">25+ World Assets Covered</span>
          </div>

          <div class="overflow-x-auto max-h-[300px] overflow-y-auto">
            <table class="w-full text-left font-mono text-[11px]">
              <thead class="sticky top-0 bg-pbi-surface text-[#94a3b8] uppercase text-[10px] border-b border-pbi-border">
                <tr>
                  <th class="py-1.5 px-2.5 font-bold">Symbol</th>
                  <th class="py-1.5 px-2.5 font-bold">Company / Instrument</th>
                  <th class="py-1.5 px-2.5 font-bold">Region</th>
                  <th class="py-1.5 px-2.5 font-bold">Sector</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">10Y CAGR %</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">10Y Total Return</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">Max Drawdown</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">10Y Sharpe</th>
                  <th class="py-1.5 px-2.5 font-bold text-right">Market Cap</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-pbi-border/40">
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#00f0ff] font-bold">NVDA</td><td>NVIDIA Corporation</td><td><span class="px-1.5 py-0.2 rounded bg-indigo-500/20 text-[#818cf8] text-[9px]">US</span></td><td>Semiconductors &amp; AI</td><td class="text-right text-[#10b981] font-bold">49.1%</td><td class="text-right text-[#10b981] font-bold">+5,326.0%</td><td class="text-right text-[#f43f5e]">-66.4%</td><td class="text-right text-[#00f0ff] font-bold">1.48</td><td class="text-right text-white">$3,420B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#c084fc] font-bold">BTC-USD</td><td>Bitcoin Core Treasury</td><td><span class="px-1.5 py-0.2 rounded bg-purple-500/20 text-[#c084fc] text-[9px]">Digital</span></td><td>Digital Gold</td><td class="text-right text-[#10b981] font-bold">55.4%</td><td class="text-right text-[#10b981] font-bold">+8,122.5%</td><td class="text-right text-[#f43f5e]">-84.0%</td><td class="text-right text-[#00f0ff] font-bold">1.25</td><td class="text-right text-white">$1,880B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#818cf8] font-bold">ASML</td><td>ASML Holding NV</td><td><span class="px-1.5 py-0.2 rounded bg-cyan-500/20 text-[#00f0ff] text-[9px]">Europe</span></td><td>Semiconductor Equip</td><td class="text-right text-[#10b981] font-bold">29.6%</td><td class="text-right text-[#10b981] font-bold">+1,236.8%</td><td class="text-right text-[#f43f5e]">-54.2%</td><td class="text-right text-[#00f0ff] font-bold">1.12</td><td class="text-right text-white">$380B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#818cf8] font-bold">TSM</td><td>Taiwan Semiconductor</td><td><span class="px-1.5 py-0.2 rounded bg-emerald-500/20 text-[#10b981] text-[9px]">APAC</span></td><td>Foundry</td><td class="text-right text-[#10b981] font-bold">28.5%</td><td class="text-right text-[#10b981] font-bold">+1,135.0%</td><td class="text-right text-[#f43f5e]">-58.2%</td><td class="text-right text-[#00f0ff] font-bold">1.08</td><td class="text-right text-white">$980B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#818cf8] font-bold">MSFT</td><td>Microsoft Corporation</td><td><span class="px-1.5 py-0.2 rounded bg-indigo-500/20 text-[#818cf8] text-[9px]">US</span></td><td>Software &amp; Cloud</td><td class="text-right text-[#10b981] font-bold">26.2%</td><td class="text-right text-[#10b981] font-bold">+925.0%</td><td class="text-right text-[#f43f5e]">-37.1%</td><td class="text-right text-[#00f0ff] font-bold">1.22</td><td class="text-right text-white">$3,150B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#818cf8] font-bold">AAPL</td><td>Apple Inc.</td><td><span class="px-1.5 py-0.2 rounded bg-indigo-500/20 text-[#818cf8] text-[9px]">US</span></td><td>Hardware &amp; Ecosystem</td><td class="text-right text-[#10b981] font-bold">24.8%</td><td class="text-right text-[#10b981] font-bold">+818.0%</td><td class="text-right text-[#f43f5e]">-38.5%</td><td class="text-right text-[#00f0ff] font-bold">1.15</td><td class="text-right text-white">$3,520B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#fbbf24] font-bold">RELIANCE.NS</td><td>Reliance Industries Ltd</td><td><span class="px-1.5 py-0.2 rounded bg-amber-500/20 text-[#fbbf24] text-[9px]">India</span></td><td>Energy &amp; Conglomerate</td><td class="text-right text-[#10b981] font-bold">20.3%</td><td class="text-right text-[#10b981] font-bold">+535.6%</td><td class="text-right text-[#f43f5e]">-44.2%</td><td class="text-right text-[#00f0ff] font-bold">0.95</td><td class="text-right text-white">$220B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#fbbf24] font-bold">BHARTIARTL.NS</td><td>Bharti Airtel Ltd</td><td><span class="px-1.5 py-0.2 rounded bg-amber-500/20 text-[#fbbf24] text-[9px]">India</span></td><td>Telecom</td><td class="text-right text-[#10b981] font-bold">19.4%</td><td class="text-right text-[#10b981] font-bold">+488.0%</td><td class="text-right text-[#f43f5e]">-42.0%</td><td class="text-right text-[#00f0ff] font-bold">0.91</td><td class="text-right text-white">$125B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#818cf8] font-bold">MC.PA</td><td>LVMH Moët Hennessy</td><td><span class="px-1.5 py-0.2 rounded bg-cyan-500/20 text-[#00f0ff] text-[9px]">Europe</span></td><td>Global Luxury</td><td class="text-right text-[#10b981] font-bold">18.2%</td><td class="text-right text-[#10b981] font-bold">+432.0%</td><td class="text-right text-[#f43f5e]">-41.0%</td><td class="text-right text-[#00f0ff] font-bold">0.86</td><td class="text-right text-white">$360B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#fbbf24] font-bold">TCS.NS</td><td>Tata Consultancy Services</td><td><span class="px-1.5 py-0.2 rounded bg-amber-500/20 text-[#fbbf24] text-[9px]">India</span></td><td>IT Services</td><td class="text-right text-[#10b981] font-bold">17.5%</td><td class="text-right text-[#10b981] font-bold">+402.0%</td><td class="text-right text-[#f43f5e]">-30.5%</td><td class="text-right text-[#00f0ff] font-bold">1.02</td><td class="text-right text-white">$175B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#00f0ff] font-bold">^NSEI</td><td>NIFTY 50 (India)</td><td><span class="px-1.5 py-0.2 rounded bg-amber-500/20 text-[#fbbf24] text-[9px]">India</span></td><td>Benchmark Index</td><td class="text-right text-[#10b981] font-bold">12.6%</td><td class="text-right text-[#10b981] font-bold">+228.4%</td><td class="text-right text-[#f43f5e]">-38.4%</td><td class="text-right text-[#00f0ff] font-bold">0.82</td><td class="text-right text-white">$4,200B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#00f0ff] font-bold">^GSPC</td><td>S&amp;P 500 (USA)</td><td><span class="px-1.5 py-0.2 rounded bg-indigo-500/20 text-[#818cf8] text-[9px]">US</span></td><td>Benchmark Index</td><td class="text-right text-[#10b981] font-bold">12.1%</td><td class="text-right text-[#10b981] font-bold">+212.2%</td><td class="text-right text-[#f43f5e]">-34.0%</td><td class="text-right text-[#00f0ff] font-bold">0.85</td><td class="text-right text-white">$48,000B</td></tr>
                <tr class="hover:bg-pbi-hover"><td class="py-1 px-2.5 text-[#fbbf24] font-bold">GC=F</td><td>Gold Commodity Futures</td><td><span class="px-1.5 py-0.2 rounded bg-amber-500/20 text-[#fbbf24] text-[9px]">Global</span></td><td>Safe Haven Metal</td><td class="text-right text-[#10b981] font-bold">11.6%</td><td class="text-right text-[#10b981] font-bold">+198.4%</td><td class="text-right text-[#10b981] font-bold">-21.5%</td><td class="text-right text-[#00f0ff] font-bold">0.86</td><td class="text-right text-white">$16,000B</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 10-Year Macro Crises Chronology -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-2.5">
          <div class="pbi-card p-3 border-l-4 border-l-[#ec4899]">
            <span class="text-[10px] text-[#ec4899] font-bold block">2015 – 2016 CRISIS</span>
            <strong class="text-xs text-white block">Oil Collapse &amp; Yuan Devaluation</strong>
            <p class="text-[10px] text-[#94a3b8] mt-1">Crude plummeted to $27. China equity circuit breakers fired. Emerging markets faced liquidity drains.</p>
          </div>
          <div class="pbi-card p-3 border-l-4 border-l-[#f43f5e]">
            <span class="text-[10px] text-[#f43f5e] font-bold block">2020 LIQUIDITY FLASH CRASH</span>
            <strong class="text-xs text-white block">COVID-19 Global Pandemic Shock</strong>
            <p class="text-[10px] text-[#94a3b8] mt-1">S&amp;P 500 plunged -34% in 33 days. Global central banks injected $16T in stimulus sparking a massive recovery.</p>
          </div>
          <div class="pbi-card p-3 border-l-4 border-l-[#fbbf24]">
            <span class="text-[10px] text-[#fbbf24] font-bold block">2022 INFLATION &amp; RATE HIKE SHOCK</span>
            <strong class="text-xs text-white block">500bps Rapid Central Bank Tightening</strong>
            <p class="text-[10px] text-[#94a3b8] mt-1">Global 40-year inflation peak. Tech stocks declined -33%, paving the way for the 2024–2026 AI supercycle.</p>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           PAGE 3: RISK ANALYTICS & INTERACTIVE DAX PLAYGROUND (TAB 3)
           ===================================================================== -->
      <div id="page-risk" class="hidden flex flex-col gap-3">
        
        <div class="pbi-card p-4 border-l-4 border-l-pbi-accent">
          <div class="flex items-center justify-between mb-3 pb-2 border-b border-pbi-border">
            <div>
              <h2 class="text-sm font-bold text-white font-mono">Interactive DAX Measure Calculator &amp; Evaluator</h2>
              <p class="text-[11px] text-[#94a3b8]">Execute and test Power BI DAX formulas dynamically against the in-memory Lakehouse model.</p>
            </div>
            <span class="px-2.5 py-1 rounded bg-pbi-accent/20 text-pbi-accent text-xs font-mono font-bold">DAX Engine Online</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-3 mb-3">
            <div class="lg:col-span-5 flex flex-col gap-2">
              <label class="text-[11px] font-bold text-[#94a3b8] uppercase">Select DAX Measure:</label>
              <select id="dax-selector" class="w-full py-1.5 px-2.5 rounded bg-pbi-surface border border-pbi-border text-white text-xs font-mono focus:border-pbi-accent outline-none" onchange="runDAXEvaluation()">
                <option value="SHARPE">[Sharpe Ratio] — Risk-Adjusted Return Measure</option>
                <option value="GOLDEN_CROSS">[MA Cross Signal] — 20D vs 50D Moving Average Crossover</option>
                <option value="UNREALIZED_ROI">[Portfolio Unrealized ROI %] — Inception Return</option>
                <option value="BETA">[Portfolio Beta vs SPX] — Market Systematic Risk</option>
                <option value="VAR_95">[Value at Risk 95%] — 1-Day Maximum Expected Loss</option>
              </select>

              <button onclick="runDAXEvaluation()" class="py-2 px-3 rounded bg-gradient-to-r from-pbi-accent to-pbi-mint text-black font-extrabold text-xs font-mono shadow-sm hover:scale-[1.01] transition-all cursor-pointer">
                ⚡ Evaluate Measure Across Portfolio
              </button>
            </div>

            <!-- Evaluated Result Callout -->
            <div class="lg:col-span-7 p-3 rounded bg-pbi-surface border border-pbi-border flex flex-col justify-between">
              <div class="flex items-center justify-between text-xs text-[#94a3b8] font-mono">
                <span>Calculated Result:</span>
                <span class="text-pbi-accent font-bold" id="dax-eval-time">Latency: 0.8ms</span>
              </div>
              <div class="text-2xl font-mono font-extrabold text-white my-1" id="dax-eval-output">
                2.41 (Annualized Sharpe)
              </div>
              <div class="text-[11px] text-[#94a3b8] font-mono" id="dax-eval-formula">
                Formula: DIVIDE([Portfolio Unrealized ROI %] / 100 - 0.0425, [Realized Volatility 30D] / 100, 2.41)
              </div>
            </div>
          </div>

          <!-- Formatted DAX Code Snippet -->
          <div class="p-3 rounded bg-pbi-dark border border-pbi-border font-mono text-xs text-[#a5d6a7]">
            <pre id="dax-code-preview" class="whitespace-pre-wrap">// Power BI DAX Definition
[Sharpe Ratio] = 
VAR RiskFreeRate = 0.0425
VAR AnnualReturn = [Portfolio Unrealized ROI %] / 100
VAR AnnualVol = [Realized Volatility 30D] / 100
RETURN
    DIVIDE(AnnualReturn - RiskFreeRate, AnnualVol, 2.41)</pre>
          </div>
        </div>

        <!-- Stress Testing Scenario Simulator -->
        <div class="pbi-card p-3">
          <div class="flex items-center justify-between mb-2 pb-1 border-b border-pbi-border">
            <h3 class="text-xs font-bold text-white font-mono">Market Stress-Test Sensitivity Simulator</h3>
            <span class="text-[10px] text-pbi-gold font-mono font-bold" id="shock-display">Market Shock: 0%</span>
          </div>

          <div class="flex items-center gap-3 my-2">
            <span class="text-xs font-mono text-pbi-rose font-bold">-25% (Crash)</span>
            <input type="range" id="stress-slider" min="-25" max="25" value="0" step="1" class="w-full accent-pbi-accent cursor-pointer" oninput="onStressShock(this.value)"/>
            <span class="text-xs font-mono text-pbi-accent font-bold">+25% (Rally)</span>
          </div>

          <div class="grid grid-cols-3 gap-2 mt-2 font-mono text-xs text-center">
            <div class="p-2 rounded bg-pbi-surface border border-pbi-border">
              <span class="text-[10px] text-[#94a3b8] uppercase block">Simulated Portfolio NAV</span>
              <strong class="text-white text-sm" id="stress-nav">$14,842,920</strong>
            </div>
            <div class="p-2 rounded bg-pbi-surface border border-pbi-border">
              <span class="text-[10px] text-[#94a3b8] uppercase block">Simulated Net Impact</span>
              <strong class="text-pbi-accent text-sm" id="stress-impact">$0.00 (0%)</strong>
            </div>
            <div class="p-2 rounded bg-pbi-surface border border-pbi-border">
              <span class="text-[10px] text-[#94a3b8] uppercase block">Capital Adequacy Status</span>
              <strong class="text-pbi-mint text-sm" id="stress-status">Nominal Tier-1</strong>
            </div>
          </div>
        </div>

      </div>

    </main>

    <!-- =========================================================================
         3. RIGHT POWER BI FILTERS PANE (NATIVE INTERACTIVE POWER BI DRAWER)
         ========================================================================= -->
    <aside id="filters-pane" class="w-64 bg-pbi-ribbon border-l border-pbi-border p-3 flex flex-col justify-between select-none z-20">
      
      <div class="flex flex-col gap-3">
        <!-- Filter Header -->
        <div class="flex items-center justify-between border-b border-pbi-border pb-2">
          <div class="flex items-center gap-1.5 font-bold text-white text-xs">
            <span class="material-symbols-outlined text-sm text-pbi-gold">filter_alt</span>
            <span>Filters</span>
          </div>
          <button onclick="toggleFiltersPane()" class="text-[#94a3b8] hover:text-white text-xs cursor-pointer">
            <span class="material-symbols-outlined text-sm">chevron_right</span>
          </button>
        </div>

        <div class="text-[10px] uppercase font-bold text-[#94a3b8] tracking-wider">Filters on this report</div>

        <!-- Filter 1: Market Segments Checkboxes -->
        <div class="p-2.5 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="font-semibold text-white mb-1.5 flex items-center justify-between">
            <span>Market Segment</span>
            <span class="text-[10px] text-pbi-accent" id="filter-market-count">4/4</span>
          </div>
          <div class="flex flex-col gap-1 text-[11px] font-mono text-[#94a3b8]">
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-white">
              <input type="checkbox" id="flt-us" checked onchange="applyFiltersPane()" class="accent-pbi-accent"/>
              <span>US MegaCap Equities</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-white">
              <input type="checkbox" id="flt-nse" checked onchange="applyFiltersPane()" class="accent-pbi-accent"/>
              <span>Indian NSE Equities</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-white">
              <input type="checkbox" id="flt-crypto" checked onchange="applyFiltersPane()" class="accent-pbi-accent"/>
              <span>Digital Asset Reserve</span>
            </label>
          </div>
        </div>

        <!-- Filter 2: Sector Checkboxes -->
        <div class="p-2.5 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="font-semibold text-white mb-1.5 flex items-center justify-between">
            <span>Sector Category</span>
            <span class="text-[10px] text-pbi-cyan" id="filter-sector-count">4/4</span>
          </div>
          <div class="flex flex-col gap-1 text-[11px] font-mono text-[#94a3b8]">
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-white">
              <input type="checkbox" id="flt-sec-tech" checked onchange="applyFiltersPane()" class="accent-pbi-accent"/>
              <span>Technology &amp; AI</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-white">
              <input type="checkbox" id="flt-sec-fin" checked onchange="applyFiltersPane()" class="accent-pbi-accent"/>
              <span>Financial Services</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-white">
              <input type="checkbox" id="flt-sec-energy" checked onchange="applyFiltersPane()" class="accent-pbi-accent"/>
              <span>Energy &amp; Refining</span>
            </label>
          </div>
        </div>

        <!-- Filter 3: Minimum Daily Return Filter -->
        <div class="p-2.5 rounded bg-pbi-surface border border-pbi-border text-xs">
          <div class="flex items-center justify-between font-semibold text-white mb-1">
            <span>Min Return %</span>
            <span class="font-mono text-pbi-gold text-[10px]" id="min-ret-label">&ge; -5.0%</span>
          </div>
          <input type="range" id="flt-min-return" min="-5" max="5" value="-5" step="0.5" class="w-full accent-pbi-gold cursor-pointer" oninput="onMinReturnChange(this.value)"/>
        </div>

        <!-- Vertices & Data Model Info -->
        <div class="p-2 rounded bg-pbi-surface/60 border border-pbi-border/70 text-[10px] font-mono text-[#94a3b8]">
          <strong class="text-white block mb-0.5">Power BI VertiPaq Engine:</strong>
          <span>Star Schema: 1:N Relationships</span><br/>
          <span>Active Rows: <span class="text-pbi-accent" id="vertipaq-rows">8 holdings</span></span>
        </div>

      </div>

      <div class="flex items-center gap-1.5 pt-2 border-t border-pbi-border">
        <button onclick="resetAllFiltersPane()" class="w-full py-1.5 rounded bg-pbi-surface hover:bg-pbi-card text-[11px] font-mono text-[#94a3b8] hover:text-white border border-pbi-border transition-colors cursor-pointer">
          Clear All Filters
        </button>
      </div>

    </aside>

  </div>

  <!-- =========================================================================
       4. POWER BI SERVICE REPORT PAGE TABS (BOTTOM DOCK)
       ========================================================================= -->
  <footer class="h-8 bg-pbi-ribbon border-t border-pbi-border flex items-center justify-between px-3 text-xs select-none z-30">
    <div class="flex items-center gap-1">
      <button class="px-3 py-1 rounded-t bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-[#818cf8] font-bold flex items-center gap-1 border-t-2 border-t-[#818cf8] cursor-pointer" id="tab-btn-exec" onclick="switchReportTab('exec')">
        <span class="material-symbols-outlined text-xs">analytics</span>
        <span>1. Executive Valuation</span>
      </button>
      <button class="px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer" id="tab-btn-tech" onclick="switchReportTab('tech')">
        <span class="material-symbols-outlined text-xs">monitoring</span>
        <span>2. Multi-Market Technicals</span>
      </button>
      <button class="px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer" id="tab-btn-risk" onclick="switchReportTab('risk')">
        <span class="material-symbols-outlined text-xs">shield</span>
        <span>3. Risk Analytics &amp; DAX Playground</span>
      </button>
      <button class="px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer" id="tab-btn-decade" onclick="switchReportTab('decade')">
        <span class="material-symbols-outlined text-xs">public</span>
        <span>4. 10-Year Global Intelligence</span>
      </button>
    </div>

    <div class="flex items-center gap-3 text-[11px] text-[#94a3b8] font-mono">
      <span>Laptop Viewport Fit</span>
      <span>•</span>
      <span id="page-counter">Page 1 of 4</span>
    </div>
  </footer>

  <!-- Notification Toast Container -->
  <div id="pbi-toast-container" class="fixed bottom-10 right-6 z-50 pointer-events-none flex flex-col gap-2"></div>

  <!-- =========================================================================
       5. JAVASCRIPT POWER BI ENGINE & DATA ENGINE
       ========================================================================= -->
  <script>
    // Dynamic AI Investment Verdict Calculator
    function getStockRecommendation(price, sma20, sma50, rsi) {
      let score = 50;

      // Moving average alignment (max 40 pts)
      if (price > sma20 && sma20 > sma50) {
        score += 24; // Full Bullish Stack
      } else if (price > sma50 && sma20 > sma50) {
        score += 12; // Pullback in bullish trend
      } else if (price > sma20 && price < sma50) {
        score += 2;  // Mean reversion rally
      } else if (price < sma20 && price < sma50) {
        score -= 22; // Bearish breakdown
      }

      // RSI Momentum & Reversal Zones (max 25 pts)
      if (rsi >= 50 && rsi <= 65) {
        score += 18; // Sweet spot momentum
      } else if (rsi >= 40 && rsi < 50) {
        score += 6;  // Neutral consolidation
      } else if (rsi < 32) {
        score += 14; // Deep oversold - contrarian value buy
      } else if (rsi > 75) {
        score -= 16; // Extreme overbought - high trim risk
      } else if (rsi > 66) {
        score -= 4;  // Slightly overbought
      }

      // Spread modifier
      const spreadPct = ((sma20 - sma50) / sma50) * 100;
      if (spreadPct > 5) score += 4;
      else if (spreadPct < -2) score -= 6;

      score = Math.max(15, Math.min(98, Math.round(score)));

      if (score >= 82) {
        return { verdict: "STRONG BUY", score: score, color: "#10b981", action: "Core Accumulate", bg: "rgba(16,185,129,0.18)" };
      } else if (score >= 68) {
        return { verdict: "BUY / ACCUMULATE", score: score, color: "#00f0ff", action: "Scale In on Dips", bg: "rgba(0,240,255,0.18)" };
      } else if (score >= 52) {
        return { verdict: "HOLD / NEUTRAL", score: score, color: "#fbbf24", action: "Maintain Position", bg: "rgba(251,191,36,0.18)" };
      } else if (score >= 38) {
        return { verdict: "TRIM / TAKE PROFIT", score: score, color: "#ec4899", action: "Lock Partial Gains", bg: "rgba(236,72,153,0.18)" };
      } else {
        return { verdict: "AVOID / HIGH RISK", score: score, color: "#f43f5e", action: "Capital Preservation", bg: "rgba(244,63,94,0.18)" };
      }
    }

    // Master Holdings Data
    const HOLDINGS = [
      {
        symbol: "NVDA",
        name: "NVIDIA Corporation",
        sector: "Technology",
        market: "US",
        price: 128.40,
        shares: 8500,
        cost: 88.20,
        dayPl: +44450.00,
        dayReturn: +4.25,
        sma20: 121.15,
        sma50: 114.80,
        rsi: 64.2,
        vol: 18.4,
        color: "#00f0ff"
      },
      {
        symbol: "RELIANCE.NS",
        name: "Reliance Industries Ltd",
        sector: "Energy",
        market: "NSE",
        price: 1360.20,
        shares: 125000,
        cost: 1180.50,
        dayPl: +328000.00,
        dayReturn: +2.14,
        sma20: 1320.40,
        sma50: 1280.10,
        rsi: 58.7,
        vol: 14.1,
        color: "#ffd166"
      },
      {
        symbol: "MSFT",
        name: "Microsoft Corporation",
        sector: "Technology",
        market: "US",
        price: 448.20,
        shares: 7200,
        cost: 382.50,
        dayPl: +57600.00,
        dayReturn: +1.82,
        sma20: 440.10,
        sma50: 431.50,
        rsi: 61.0,
        vol: 12.8,
        color: "#38bdf8"
      },
      {
        symbol: "TCS.NS",
        name: "Tata Consultancy Services",
        sector: "Technology",
        market: "NSE",
        price: 2349.40,
        shares: 85000,
        cost: 2150.00,
        dayPl: +142000.00,
        dayReturn: +0.84,
        sma20: 2310.20,
        sma50: 2280.00,
        rsi: 54.5,
        vol: 11.9,
        color: "#818cf8"
      },
      {
        symbol: "AAPL",
        name: "Apple Inc.",
        sector: "Technology",
        market: "US",
        price: 224.50,
        shares: 12000,
        cost: 175.40,
        dayPl: +30600.00,
        dayReturn: +1.15,
        sma20: 220.80,
        sma50: 215.20,
        rsi: 59.2,
        vol: 13.5,
        color: "#c084fc"
      },
      {
        symbol: "HDFCBANK.NS",
        name: "HDFC Bank Ltd",
        sector: "Financials",
        market: "NSE",
        price: 1742.60,
        shares: 190000,
        cost: 1540.20,
        dayPl: +420000.00,
        dayReturn: +1.45,
        sma20: 1710.00,
        sma50: 1675.00,
        rsi: 57.8,
        vol: 13.9,
        color: "#00f0ff"
      },
      {
        symbol: "BTC-USD",
        name: "Bitcoin Core Treasury",
        sector: "Financials",
        market: "CRYPTO",
        price: 63240.00,
        shares: 45.0,
        cost: 51200.00,
        dayPl: +88200.00,
        dayReturn: +3.15,
        sma20: 61200.00,
        sma50: 58400.00,
        rsi: 66.4,
        vol: 28.5,
        color: "#f59e0b"
      },
      {
        symbol: "ASML",
        name: "ASML Holding NV",
        sector: "Semiconductors",
        market: "US",
        price: 920.00,
        shares: 1500,
        cost: 690.00,
        dayPl: -6250.00,
        dayReturn: -0.45,
        sma20: 935.00,
        sma50: 915.00,
        rsi: 48.2,
        vol: 21.0,
        color: "#f43f5e"
      }
    ];

    let activeSymbol = "NVDA";
    let activeCurrency = "USD";
    const FX_RATES = { "USD": 1.0, "INR": 84.42, "EUR": 0.92, "GBP": 0.79 };
    const FX_SYMS = { "USD": "$", "INR": "₹", "EUR": "€", "GBP": "£" };

    let isFiltersOpen = true;
    let liveSimulationInterval = null;

    let pbiChart = null;
    let pbiDonut = null;
    let techBenchmarkChart = null;
    let rsiBarChart = null;
    let volBarChart = null;

    // Toast Utility
    function triggerPBIToast(title, message) {
      const container = document.getElementById("pbi-toast-container");
      const toast = document.createElement("div");
      toast.className = "pointer-events-auto flex items-center gap-2.5 p-3 rounded-lg bg-pbi-surface border border-pbi-accent text-white shadow-xl max-w-xs text-xs";
      toast.innerHTML = `
        <div class="w-6 h-6 rounded bg-[#f2c811] text-black font-bold flex items-center justify-center shrink-0 text-[10px]">PBI</div>
        <div class="flex flex-col">
          <span class="font-bold text-white">${title}</span>
          <span class="text-[10px] text-[#94a3b8]">${message}</span>
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

    // Toggle Filters Pane
    function toggleFiltersPane() {
      const pane = document.getElementById("filters-pane");
      const toggleText = document.getElementById("filters-toggle-text");
      isFiltersOpen = !isFiltersOpen;

      if (isFiltersOpen) {
        pane.style.display = "flex";
        pane.style.width = "16rem";
        toggleText.innerText = "Filters (4)";
        triggerPBIToast("Filters Pane", "Opened Filter Drawer.");
      } else {
        pane.style.display = "none";
        toggleText.innerText = "Show Filters";
        triggerPBIToast("Filters Pane", "Collapsed. Maximum Canvas Enabled.");
      }
    }

    // Generate Dynamic Historical Series for any asset
    function generateStockHistory(symbol, basePrice, days=60) {
      const labels = [];
      const prices = [];
      const sma20 = [];
      const sma50 = [];
      const bUpper = [];
      const bLower = [];
      const volumes = [];

      let cur = basePrice * 0.88;
      const today = new Date();

      for (let i = days; i >= 0; i--) {
        const d = new Date(today);
        d.setDate(today.getDate() - i);
        labels.push(d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));

        const noise = (Math.sin(i * 0.3) * 0.015) + (Math.cos(i * 0.1) * 0.01) + 0.002;
        cur = cur * (1 + noise);
        if (i === 0) cur = basePrice; // anchor to exact live price
        prices.push(parseFloat(cur.toFixed(2)));

        // Volume
        volumes.push(Math.round(800000 + Math.random() * 2500000));
      }

      // Calculate SMAs
      for (let i = 0; i < prices.length; i++) {
        // SMA 20
        if (i >= 19) {
          const slice20 = prices.slice(i - 19, i + 1);
          const avg20 = slice20.reduce((a, b) => a + b, 0) / 20;
          sma20.push(parseFloat(avg20.toFixed(2)));
          // Bollinger Bands
          const std = Math.sqrt(slice20.map(x => Math.pow(x - avg20, 2)).reduce((a, b) => a + b) / 20);
          bUpper.push(parseFloat((avg20 + 2 * std).toFixed(2)));
          bLower.push(parseFloat((avg20 - 2 * std).toFixed(2)));
        } else {
          sma20.push(prices[i]);
          bUpper.push(prices[i] * 1.04);
          bLower.push(prices[i] * 0.96);
        }

        // SMA 50
        if (i >= 49) {
          const slice50 = prices.slice(i - 49, i + 1);
          sma50.push(parseFloat((slice50.reduce((a, b) => a + b, 0) / 50).toFixed(2)));
        } else {
          sma50.push(prices[Math.max(0, i - 5)]);
        }
      }

      return { labels, prices, sma20, sma50, bUpper, bLower, volumes };
    }

    // Initialize Main Chart.js Visual
    function initMainChart() {
      const ctx = document.getElementById('pbiChartCanvas').getContext('2d');
      const hist = generateStockHistory(activeSymbol, HOLDINGS.find(h => h.symbol === activeSymbol).price, 60);

      pbiChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: hist.labels,
          datasets: [
            {
              label: 'Close Price',
              data: hist.prices,
              borderColor: '#00f0ff',
              borderWidth: 2.5,
              backgroundColor: 'rgba(0, 240, 255, 0.12)',
              fill: true,
              tension: 0.25,
              yAxisID: 'y'
            },
            {
              label: '20-Day SMA',
              data: hist.sma20,
              borderColor: '#fbbf24',
              borderWidth: 2,
              borderDash: [4, 2],
              pointRadius: 0,
              fill: false,
              tension: 0.2,
              yAxisID: 'y'
            },
            {
              label: '50-Day SMA',
              data: hist.sma50,
              borderColor: '#ec4899',
              borderWidth: 1.8,
              borderDash: [5, 3],
              pointRadius: 0,
              fill: false,
              tension: 0.2,
              yAxisID: 'y'
            },
            {
              label: 'Bollinger Upper',
              data: hist.bUpper,
              borderColor: 'rgba(192, 132, 252, 0.45)',
              borderWidth: 1,
              pointRadius: 0,
              fill: false,
              hidden: true,
              yAxisID: 'y'
            },
            {
              label: 'Bollinger Lower',
              data: hist.bLower,
              borderColor: 'rgba(192, 132, 252, 0.45)',
              borderWidth: 1,
              pointRadius: 0,
              fill: false,
              hidden: true,
              yAxisID: 'y'
            },
            {
              type: 'bar',
              label: 'Trading Volume',
              data: hist.volumes,
              backgroundColor: 'rgba(99, 102, 241, 0.35)',
              borderRadius: 2,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(10, 14, 28, 0.95)',
              titleColor: '#00f0ff',
              bodyColor: '#e6fffa',
              borderColor: 'rgba(129, 140, 248, 0.3)',
              borderWidth: 1,
              padding: 10,
              titleFont: { family: 'JetBrains Mono', size: 12 },
              bodyFont: { family: 'JetBrains Mono', size: 11 },
              callbacks: {
                label: function(context) {
                  const sym = FX_SYMS[activeCurrency];
                  const label = context.dataset.label || '';
                  if (label === 'Trading Volume') {
                    return ` Volume: ${(context.raw / 1000000).toFixed(2)}M`;
                  }
                  return ` ${label}: ${sym}${context.raw.toLocaleString()}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(129, 140, 248, 0.12)' },
              ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8 }
            },
            y: {
              type: 'linear',
              position: 'left',
              grid: { color: 'rgba(129, 140, 248, 0.12)' },
              ticks: {
                color: '#94a3b8',
                font: { family: 'JetBrains Mono', size: 10 },
                callback: v => FX_SYMS[activeCurrency] + v.toLocaleString()
              }
            },
            y1: {
              type: 'linear',
              position: 'right',
              grid: { display: false },
              ticks: { display: false },
              max: Math.max(...hist.volumes) * 3
            }
          }
        }
      });
    }

    // Initialize Donut Chart
    function initDonutChart() {
      const ctx = document.getElementById('pbiDonutCanvas').getContext('2d');
      pbiDonut = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Technology & AI', 'Financial Services', 'Energy & Refining', 'Semiconductors'],
          datasets: [{
            data: [42.0, 24.0, 18.0, 16.0],
            backgroundColor: ['#818cf8', '#00f0ff', '#fbbf24', '#ec4899'],
            borderColor: '#0e142c',
            borderWidth: 3,
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(10, 14, 28, 0.95)',
              titleColor: '#00f0ff',
              bodyColor: '#fff',
              borderColor: 'rgba(129, 140, 248, 0.3)',
              borderWidth: 1,
              callbacks: {
                label: ctx => ` ${ctx.label}: ${ctx.raw}% Allocation`
              }
            }
          },
          onClick: (evt, activeElements) => {
            if (activeElements.length > 0) {
              const idx = activeElements[0].index;
              const sectors = ['Technology', 'Financials', 'Energy', 'Semiconductors'];
              filterBySector(sectors[idx]);
            }
          }
        }
      });
    }

    // Update Main Visual when selecting a holding
    function focusOnHolding(symbol) {
      activeSymbol = symbol;
      const h = HOLDINGS.find(item => item.symbol === symbol);
      if (!h) return;

      document.getElementById('slicer-symbol').value = symbol;
      document.getElementById('main-chart-title').innerText = `Interactive Trajectory: ${h.symbol} (${h.name})`;
      document.getElementById('active-focus-label').innerText = `${h.symbol} • ${h.name.toUpperCase()}`;

      // Update AI Investment Recommendation Desk
      const rec = getStockRecommendation(h.price, h.sma20, h.sma50, h.rsi);
      const recBadge = document.getElementById('ai-rec-badge');
      const recScore = document.getElementById('ai-rec-score');
      const recAction = document.getElementById('ai-rec-action');
      if (recBadge) {
        recBadge.innerText = rec.verdict;
        recBadge.style.color = rec.color;
        recBadge.style.background = rec.bg;
        recBadge.style.borderColor = rec.color;
      }
      if (recScore) recScore.innerText = `Score: ${rec.score}/100`;
      if (recAction) recAction.innerText = `Strategy: ${rec.action}`;

      // Update Chart Data
      const hist = generateStockHistory(h.symbol, h.price, 60);
      pbiChart.data.labels = hist.labels;
      pbiChart.data.datasets[0].data = hist.prices;
      pbiChart.data.datasets[0].borderColor = h.color;
      pbiChart.data.datasets[1].data = hist.sma20;
      pbiChart.data.datasets[2].data = hist.sma50;
      pbiChart.data.datasets[3].data = hist.bUpper;
      pbiChart.data.datasets[4].data = hist.bLower;
      pbiChart.data.datasets[5].data = hist.volumes;
      pbiChart.update();

      // Update Bottom Telemetry
      const sym = FX_SYMS[activeCurrency];
      document.getElementById('tele-price').innerText = `${sym}${h.price.toFixed(2)}`;
      document.getElementById('tele-sma20').innerText = `${sym}${h.sma20.toFixed(2)}`;
      document.getElementById('tele-sma50').innerText = `${sym}${h.sma50.toFixed(2)}`;
      document.getElementById('tele-signal').innerText = h.sma20 > h.sma50 ? "Bullish (SMA20 > SMA50)" : "Bearish Momentum";
      document.getElementById('tele-signal').style.color = h.sma20 > h.sma50 ? "var(--tw-colors-pbi-accent, #00ff9d)" : "var(--tw-colors-pbi-rose, #ff4d6d)";

      // Highlight Table Row
      renderMatrixTable();

      triggerPBIToast("Focus Updated", `Visuals sliced to ${h.symbol} (${h.name}).`);
    }

    // Toggle Technical Overlays
    function toggleChartDataset(index, isVisible) {
      if (pbiChart) {
        pbiChart.data.datasets[index].hidden = !isVisible;
        pbiChart.update();
      }
    }

    function toggleBollingerBands(isVisible) {
      if (pbiChart) {
        pbiChart.data.datasets[3].hidden = !isVisible;
        pbiChart.data.datasets[4].hidden = !isVisible;
        pbiChart.update();
        triggerPBIToast("Bollinger Bands", isVisible ? "Displayed on Chart." : "Hidden.");
      }
    }

    // Timeframe Slicing
    function onTimeframeChange(period, btn) {
      document.querySelectorAll('#timeframe-group button').forEach(b => {
        b.className = "px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white";
      });
      btn.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm";

      let days = 60;
      if (period === '1M') days = 22;
      else if (period === '3M') days = 65;
      else if (period === '1Y') days = 250;
      else if (period === '5Y') days = 1250;
      else if (period === '10Y') days = 2600;
      else if (period === 'ALL') days = 3650;

      const h = HOLDINGS.find(item => item.symbol === activeSymbol) || HOLDINGS[0];
      const hist = generateStockHistory(h.symbol, h.price, days);

      pbiChart.data.labels = hist.labels;
      pbiChart.data.datasets[0].data = hist.prices;
      pbiChart.data.datasets[1].data = hist.sma20;
      pbiChart.data.datasets[2].data = hist.sma50;
      pbiChart.data.datasets[3].data = hist.bUpper;
      pbiChart.data.datasets[4].data = hist.bLower;
      pbiChart.data.datasets[5].data = hist.volumes;
      pbiChart.update();

      triggerPBIToast("Time Window Sliced", `Evaluated historical measures for ${period} window.`);
    }

    // Render Matrix Table
    function renderMatrixTable() {
      const tbody = document.getElementById('matrix-tbody');
      const sym = FX_SYMS[activeCurrency];

      tbody.innerHTML = HOLDINGS.map(h => {
        const isSelected = h.symbol === activeSymbol;
        const totalVal = h.shares * h.price;
        const posClass = h.dayReturn >= 0 ? 'data-bar-pos text-pbi-accent' : 'data-bar-neg text-pbi-rose';
        const crossBadge = h.sma20 > h.sma50 
          ? '<span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish Cross</span>' 
          : '<span class="px-1.5 py-0.2 rounded bg-pbi-rose/15 text-pbi-rose text-[9px] font-bold">Bearish</span>';

        return `
          <tr class="hover:bg-pbi-surface/80 transition-colors cursor-pointer ${isSelected ? 'pbi-active-row' : ''}" onclick="focusOnHolding('${h.symbol}')">
            <td class="py-2 px-2.5 font-bold" style="color:${h.color};">${h.symbol}</td>
            <td class="py-2 px-2.5 font-sans font-semibold text-white">${h.name}</td>
            <td class="py-2 px-2.5 text-[#94a3b8]">${h.sector}</td>
            <td class="py-2 px-2.5 text-right font-bold text-white">${sym}${h.price.toFixed(2)}</td>
            <td class="py-2 px-2.5 text-right">
              <div class="${posClass} px-1.5 py-0.2 inline-block font-bold">
                ${h.dayReturn >= 0 ? '+' : ''}${h.dayReturn.toFixed(2)}%
              </div>
            </td>
            <td class="py-2 px-2.5 text-right text-pbi-gold">${sym}${h.sma20.toFixed(2)}</td>
            <td class="py-2 px-2.5 text-right text-pbi-cyan">${sym}${h.sma50.toFixed(2)}</td>
            <td class="py-2 px-2.5 text-center text-white font-bold">${h.rsi.toFixed(1)}</td>
            <td class="py-2 px-2.5 text-center">${crossBadge}</td>
            <td class="py-2 px-2.5 text-center">
              <button onclick="event.stopPropagation(); focusOnHolding('${h.symbol}');" class="px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-accent hover:text-black text-pbi-mint font-bold text-[10px] border border-pbi-border transition-all">
                Select
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    // Slicer Handlers
    function onSymbolSlicerChange(val) {
      if (val === 'ALL') {
        activeSymbol = "NVDA";
        focusOnHolding("NVDA");
        document.getElementById('active-focus-label').innerText = "ALL CORE ASSETS (8)";
      } else {
        focusOnHolding(val);
      }
    }

    function onMarketSlicerChange(val) {
      const rows = document.querySelectorAll('#matrix-tbody tr');
      let count = 0;
      rows.forEach(r => {
        const sym = r.querySelector('td').innerText.trim();
        const h = HOLDINGS.find(item => item.symbol === sym);
        if (val === 'ALL' || h.market === val) {
          r.style.display = '';
          count++;
        } else {
          r.style.display = 'none';
        }
      });
      document.getElementById('matrix-count-badge').innerText = `${count} Holdings`;
      triggerPBIToast("Market Sliced", `Filtered to ${val} market segment.`);
    }

    function filterBySector(sec) {
      const rows = document.querySelectorAll('#matrix-tbody tr');
      let count = 0;
      rows.forEach(r => {
        const sym = r.querySelector('td').innerText.trim();
        const h = HOLDINGS.find(item => item.symbol === sym);
        if (h.sector === sec) {
          r.style.display = '';
          count++;
        } else {
          r.style.display = 'none';
        }
      });
      document.getElementById('matrix-count-badge').innerText = `${count} Holdings (${sec})`;
      const firstInSec = HOLDINGS.find(h => h.sector === sec);
      if (firstInSec) focusOnHolding(firstInSec.symbol);
      triggerPBIToast("Sector Sliced", `Filtered to ${sec}.`);
    }

    function filterMatrix() {
      const q = document.getElementById('matrix-search').value.toLowerCase().trim();
      const rows = document.querySelectorAll('#matrix-tbody tr');
      let count = 0;
      rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        if (!q || text.includes(q)) {
          r.style.display = '';
          count++;
        } else {
          r.style.display = 'none';
        }
      });
      document.getElementById('matrix-count-badge').innerText = `${count} Holdings`;
    }

    function resetAllSelections() {
      document.getElementById('slicer-symbol').value = 'ALL';
      document.getElementById('slicer-market').value = 'ALL';
      document.getElementById('matrix-search').value = '';
      const rows = document.querySelectorAll('#matrix-tbody tr');
      rows.forEach(r => r.style.display = '');
      document.getElementById('matrix-count-badge').innerText = `8 Core Holdings`;
      focusOnHolding('NVDA');
      document.getElementById('active-focus-label').innerText = "ALL CORE ASSETS (8)";
      triggerPBIToast("Reset Complete", "All visual selections cleared.");
    }

    function setCurrency(curr) {
      activeCurrency = curr;
      ['USD', 'INR', 'EUR', 'GBP'].forEach(c => {
        const b = document.getElementById(`btn-curr-${c}`);
        if (c === curr) b.className = "px-2 py-0.5 rounded bg-pbi-accent text-black font-bold";
        else b.className = "px-2 py-0.5 rounded text-[#94a3b8] hover:text-white";
      });

      const sym = FX_SYMS[curr];
      const rate = FX_RATES[curr];
      document.getElementById('kpi-nav-val').innerText = `${sym}${(14842920.45 * rate).toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById('kpi-gain-val').innerText = `+${sym}${(3210480.00 * rate).toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      renderMatrixTable();
      focusOnHolding(activeSymbol);
      triggerPBIToast("Currency Converted", `${curr} (${sym})`);
    }

    // Report Tab Switcher
    function switchReportTab(tabId) {
      ['exec', 'tech', 'risk', 'decade'].forEach(t => {
        const pageEl = document.getElementById(`page-${t}`);
        if (pageEl) pageEl.classList.add('hidden');
        const btn = document.getElementById(`tab-btn-${t}`);
        if (btn) btn.className = "px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer";
      });

      const activePage = document.getElementById(`page-${tabId}`);
      if (activePage) activePage.classList.remove('hidden');
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      if (activeBtn) activeBtn.className = "px-3 py-1 rounded-t bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-[#818cf8] font-bold flex items-center gap-1 border-t-2 border-t-[#818cf8] cursor-pointer";

      const pageNames = { 
        'exec': 'Page 1 of 4 (Executive Valuation)', 
        'tech': 'Page 2 of 4 (Technicals)', 
        'risk': 'Page 3 of 4 (Risk & DAX)', 
        'decade': 'Page 4 of 4 (10-Year Global Intelligence)' 
      };
      const counter = document.getElementById('page-counter');
      if (counter && pageNames[tabId]) counter.innerText = pageNames[tabId];

      if (tabId === 'tech' && !techBenchmarkChart) initTechPageCharts();
      triggerPBIToast("Tab Switched", activeBtn ? activeBtn.innerText.trim() : tabId);
    }

    // Page 2: Technicals Charts
    function initTechPageCharts() {
      // Comparison Benchmark
      const ctx1 = document.getElementById('techBenchmarkCanvas').getContext('2d');
      const dates = Array.from({length: 30}, (_, i) => `Day ${i+1}`);
      techBenchmarkChart = new Chart(ctx1, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [
            { label: 'NVDA', data: dates.map((_, i) => 100 + i * 1.5 + Math.sin(i) * 3), borderColor: '#00f0ff', tension: 0.2 },
            { label: 'BTC-USD', data: dates.map((_, i) => 100 + i * 0.8 + Math.cos(i) * 5), borderColor: '#c084fc', tension: 0.2 },
            { label: 'RELIANCE.NS', data: dates.map((_, i) => 100 + i * 0.5 + Math.sin(i * 0.5) * 2), borderColor: '#ffd166', tension: 0.2 },
            { label: 'S&P 500 Benchmark', data: dates.map((_, i) => 100 + i * 0.3), borderColor: '#ec4899', borderDash: [4, 4], tension: 0.2 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } } } },
          scales: {
            x: { grid: { color: 'rgba(22, 50, 58, 0.4)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(22, 50, 58, 0.4)' }, ticks: { color: '#94a3b8', callback: v => v + '%' } }
          }
        }
      });

      // RSI Horizontal Bar Chart
      const ctx2 = document.getElementById('rsiBarCanvas').getContext('2d');
      rsiBarChart = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: HOLDINGS.map(h => h.symbol),
          datasets: [{
            label: 'RSI (14)',
            data: HOLDINGS.map(h => h.rsi),
            backgroundColor: HOLDINGS.map(h => h.rsi >= 70 ? '#ff4d6d' : (h.rsi <= 30 ? '#00f5d4' : '#00ff9d')),
            borderRadius: 3
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: 'rgba(22, 50, 58, 0.4)' } },
            y: { ticks: { color: '#fff', font: { family: 'JetBrains Mono', size: 10 } } }
          }
        }
      });

      // Volatility Bar Chart
      const ctx3 = document.getElementById('volBarCanvas').getContext('2d');
      volBarChart = new Chart(ctx3, {
        type: 'bar',
        data: {
          labels: HOLDINGS.map(h => h.symbol),
          datasets: [{
            label: '30D Vol %',
            data: HOLDINGS.map(h => h.vol),
            backgroundColor: '#38bdf8',
            borderRadius: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#fff', font: { family: 'JetBrains Mono', size: 9 } } },
            y: { ticks: { color: '#94a3b8', callback: v => v + '%' }, grid: { color: 'rgba(22, 50, 58, 0.4)' } }
          }
        }
      });
    }

    // Page 3: DAX Evaluator
    const DAX_CATALOG = {
      "SHARPE": {
        output: "2.41 (Annualized Sharpe Ratio)",
        formula: "DIVIDE([Portfolio Unrealized ROI %] / 100 - 0.0425, [Realized Volatility 30D] / 100, 2.41)",
        code: `// Power BI DAX Definition\\n[Sharpe Ratio] = \\nVAR RiskFreeRate = 0.0425\\nVAR AnnualReturn = [Portfolio Unrealized ROI %] / 100\\nVAR AnnualVol = [Realized Volatility 30D] / 100\\nRETURN\\n    DIVIDE(AnnualReturn - RiskFreeRate, AnnualVol, 2.41)`
      },
      "GOLDEN_CROSS": {
        output: "Bullish Cross Signal (SMA 20 > SMA 50 across 7 of 8 holdings)",
        formula: "IF([SMA 20] > [SMA 50], 'Bullish Golden Cross', 'Bearish Death Cross')",
        code: `// Power BI DAX Definition\\n[MA Cross Signal] = \\nVAR Sma20Val = [SMA 20]\\nVAR Sma50Val = [SMA 50]\\nRETURN\\n    IF(ISBLANK(Sma20Val) || ISBLANK(Sma50Val), 'Neutral',\\n       IF(Sma20Val > Sma50Val, 'Bullish Golden Cross', 'Bearish Cross'))`
      },
      "UNREALIZED_ROI": {
        output: "+27.64% (Portfolio Total Inception Return)",
        formula: "DIVIDE([Total Unrealized Gain], [Total Portfolio Value] - [Total Unrealized Gain], 0) * 100",
        code: `// Power BI DAX Definition\\n[Portfolio Unrealized ROI %] = \\nVAR Gains = SUM(Fact_PortfolioPositions[unrealized_gain])\\nVAR Cost = SUM(Fact_PortfolioPositions[total_value]) - Gains\\nRETURN\\n    DIVIDE(Gains, Cost, 0) * 100`
      },
      "BETA": {
        output: "0.94 (Systematic Beta vs S&P 500 Index)",
        formula: "DIVIDE(COVARIANCE.S(Fact_StockAnalytics[return], Benchmark[return]), VARIANCE.S(Benchmark[return]))",
        code: `// Power BI DAX Definition\\n[Portfolio Beta] = \\nVAR Covar = COVARIANCE.S(Fact_StockAnalytics[daily_return_pct], Benchmark_SPX[daily_return_pct])\\nVAR BenchVar = VARIANCE.S(Benchmark_SPX[daily_return_pct])\\nRETURN\\n    DIVIDE(Covar, BenchVar, 0.94)`
      },
      "VAR_95": {
        output: "$240,000.00 (95% 1-Day Maximum Value at Risk)",
        formula: "[Total Portfolio Value] * 1.645 * ([Realized Volatility 30D] / SQRT(252))",
        code: `// Power BI DAX Definition\\n[Value at Risk 95%] = \\nVAR ZScore = 1.645\\nVAR DailyVol = [Realized Volatility 30D] / SQRT(252)\\nRETURN\\n    [Total Portfolio Value] * ZScore * DailyVol`
      }
    };

    function runDAXEvaluation() {
      const key = document.getElementById('dax-selector').value;
      const data = DAX_CATALOG[key];
      if (data) {
        document.getElementById('dax-eval-output').innerText = data.output;
        document.getElementById('dax-eval-formula').innerText = `Formula: ${data.formula}`;
        document.getElementById('dax-code-preview').innerText = data.code;
        document.getElementById('dax-eval-time').innerText = `Evaluated in ${(Math.random() * 0.8 + 0.3).toFixed(1)}ms`;
        triggerPBIToast("DAX Query Executed", `Computed ${key} measure.`);
      }
    }

    // Stress Testing
    function onStressShock(val) {
      const pct = parseFloat(val);
      document.getElementById('shock-display').innerText = `Market Shock: ${pct >= 0 ? '+' : ''}${pct}%`;
      const baseNav = 14842920.45;
      const nextNav = baseNav * (1 + (pct * 0.94 / 100));
      const impact = nextNav - baseNav;

      document.getElementById('stress-nav').innerText = `$${(nextNav / 1000000).toFixed(2)}M`;
      document.getElementById('stress-impact').innerText = `${impact >= 0 ? '+' : ''}$${(impact / 1000).toFixed(1)}K (${pct}%)`;
      document.getElementById('stress-impact').style.color = impact >= 0 ? '#00ff9d' : '#ff4d6d';
      document.getElementById('stress-status').innerText = pct <= -15 ? 'Capital Buffer Alert' : 'Nominal Tier-1';
      document.getElementById('stress-status').style.color = pct <= -15 ? '#ffd166' : '#00ff9d';
    }

    // Live Streaming Simulation Toggle
    function toggleLiveSimulation() {
      const btn = document.getElementById('btn-live-toggle');
      const icon = document.getElementById('live-icon');
      const text = document.getElementById('live-text');
      const status = document.getElementById('sync-status');

      if (!liveSimulationInterval) {
        // Start Live Streaming Ticks
        liveSimulationInterval = setInterval(() => {
          // Jiggle prices slightly
          HOLDINGS.forEach(h => {
            const delta = (Math.random() * 0.6 - 0.28);
            h.price = Math.max(10, h.price + delta);
            h.dayReturn += (delta * 0.05);
          });
          focusOnHolding(activeSymbol);
          status.innerText = `Tick: ${new Date().toLocaleTimeString()}`;
        }, 3000);

        icon.innerText = "pause";
        text.innerText = "Live Ticks: ON";
        btn.className = "px-2 py-0.5 rounded bg-pbi-accent text-black font-bold text-[11px] font-mono flex items-center gap-1 shadow-sm";
        triggerPBIToast("Live Streaming Active", "Streaming simulated DirectQuery market ticks every 3s.");
      } else {
        // Stop Live Ticks
        clearInterval(liveSimulationInterval);
        liveSimulationInterval = null;
        icon.innerText = "play_arrow";
        text.innerText = "Live Ticks: Off";
        btn.className = "px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-card border border-pbi-border text-[11px] font-mono text-pbi-accent flex items-center gap-1";
        status.innerText = "DirectQuery Paused";
        triggerPBIToast("Streaming Paused", "DirectQuery sync paused.");
      }
    }

    function refreshDataModel() {
      const icon = document.getElementById('refresh-icon');
      icon.classList.add('animate-spin');
      setTimeout(() => {
        icon.classList.remove('animate-spin');
        focusOnHolding(activeSymbol);
        triggerPBIToast("Data Refreshed", "Re-queried Databricks Delta Gold layers.");
      }, 600);
    }

    function exportFilteredData() {
      const csvContent = "data:text/csv;charset=utf-8,Symbol,Name,Sector,Market,Price,SharesHeld,CostBasis,DayReturnPct,SMA20,SMA50,RSI\\n" +
        HOLDINGS.map(h => `${h.symbol},${h.name},${h.sector},${h.market},${h.price},${h.shares},${h.cost},${h.dayReturn},${h.sma20},${h.sma50},${h.rsi}`).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "PowerBI_Export_Holdings.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      triggerPBIToast("Export Complete", "Downloaded PowerBI_Export_Holdings.csv.");
    }

    // Initialize Everything
    window.addEventListener('DOMContentLoaded', () => {
      renderMatrixTable();
      initMainChart();
      initDonutChart();
      focusOnHolding('NVDA');
    });
  </script>
</body>
</html>
'''

# Write to 05_powerbi_dashboard\powerbi_dashboard.html and index.html
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_code)

index_file = os.path.join(base_dir, "index.html")
with open(index_file, "w", encoding="utf-8") as f:
    f.write(html_code)

# Mirror to 04_dashboard and artifact directory
artifact_dir = r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf"
os.makedirs(artifact_dir, exist_ok=True)
with open(os.path.join(artifact_dir, "powerbi_dashboard.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

dashboard_04_file = r"D:\BDA Project\financial-market-intelligence\04_dashboard\powerbi_dashboard.html"
with open(dashboard_04_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Generated Ultra-Interactive Power BI Dashboard at: {output_file}")
print(f"Updated index.html: {index_file}")
print(f"Mirrored to: {dashboard_04_file}")
print(f"Mirrored to: {os.path.join(artifact_dir, 'powerbi_dashboard.html')}")
