# -*- coding: utf-8 -*-
"""
Generate High-Fidelity Desktop Executive Banking & Equities Terminal
Theme: Aurora Green (#00ff9d, #00f5d4, #10f2a5) on Deep Obsidian Teal (#040a0c, #081417, #0b1c20)
Features:
- Full Sidebar Drawer with 3-Way Expand/Collapse Toggle:
  1. Topbar Hamburger Menu Button (always visible)
  2. Inside-Sidebar Collapse Button (arrow/menu_open)
  3. Floating Quick-Access Drawer Pill
  4. Keyboard shortcut: Alt+S or Ctrl+B
- Aurora Green Aesthetic:
  - Luminous glowing neon accents, soft neon gradients, glassmorphism cards
  - Real-time animated pulse nodes & sparklines
- Multi-Market Equities & Assets:
  - US Tech (NVDA, MSFT, AAPL, AMZN, GOOGL)
  - Indian Blue Chips (RELIANCE.NS, TCS.NS, HDFCBANK.NS)
  - Crypto & FX (BTC-USD, ETH-USD, USD/INR)
- Dynamic Controls:
  - Holdings Valuation Trajectory Area Chart with 6 timeframes (1D, 1W, 1M, 1Y, YTD, ALL)
  - Institutional DMA Order Desk with live estimation, Buy/Sell side switch, and execution toasts
  - Holdings Data Table with instant search, sector & market filtering, 7-day sparklines, and CSV export
  - Multi-Currency converter (USD, INR, EUR, GBP)
"""

import os

html_content = '''<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>AURORA // Executive Equities & Sovereign Wealth Terminal</title>
  
  <!-- Google Fonts: Plus Jakarta Sans, Inter, JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            aurora: {
              DEFAULT: "#00ff9d",
              glow: "#00ff9d",
              bright: "#10f2a5",
              mint: "#00f5d4",
              cyan: "#38bdf8",
              emerald: "#059669",
              dark: "#040a0c",
              surface: "#081417",
              container: "#0b1c20",
              card: "#10262c",
              hover: "#15333b",
              border: "#1a3d46",
              borderGlow: "rgba(0, 255, 157, 0.28)",
              rose: "#ff4d6d",
              amber: "#ffd166"
            }
          },
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          },
          boxShadow: {
            'aurora-sm': '0 0 12px rgba(0, 255, 157, 0.2)',
            'aurora-md': '0 0 24px rgba(0, 255, 157, 0.28)',
            'aurora-lg': '0 0 40px rgba(0, 255, 157, 0.35)',
            'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.45)'
          }
        }
      }
    };
  </script>

  <style>
    @layer base {
      html, body {
        margin: 0;
        padding: 0;
        background-color: #040a0c;
        color: #e6fffa;
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
      }
    }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #040a0c; }
    ::-webkit-scrollbar-thumb { background: #1a3d46; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #00ff9d; }

    /* Aurora Glow Shimmer Animations */
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.85; filter: drop-shadow(0 0 8px rgba(0, 255, 157, 0.6)); }
      50% { opacity: 1; filter: drop-shadow(0 0 16px rgba(0, 255, 157, 0.9)); }
    }
    .aurora-pulse { animation: pulseGlow 2.5s infinite ease-in-out; }

    @keyframes auroraBreathe {
      0%, 100% { transform: scale(1); opacity: 0.25; }
      50% { transform: scale(1.08); opacity: 0.4; }
    }
    .aurora-ambient-glow {
      position: absolute;
      width: 480px;
      height: 480px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0, 255, 157, 0.18) 0%, rgba(0, 245, 212, 0.08) 45%, rgba(4, 10, 12, 0) 70%);
      pointer-events: none;
      animation: auroraBreathe 7s infinite ease-in-out;
      filter: blur(40px);
    }

    /* Smooth Drawer Slide transitions */
    #sidebar {
      transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), width 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #main-content-wrapper {
      transition: margin-left 0.32s cubic-bezier(0.16, 1, 0.3, 1), padding-left 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #topbar {
      transition: left 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Toast animation */
    @keyframes slideInUp {
      from { transform: translateY(30px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    .toast-entry { animation: slideInUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
  </style>
</head>
<body class="bg-aurora-dark min-h-screen text-[#e6fffa] selection:bg-aurora selection:text-black">

  <!-- Ambient Aurora Backdrops -->
  <div class="aurora-ambient-glow -top-32 -left-32 z-0"></div>
  <div class="aurora-ambient-glow top-1/3 -right-32 z-0"></div>

  <!-- =========================================================================
       1. COLLAPSIBLE AURORA SIDEBAR
       ========================================================================= -->
  <aside id="sidebar" class="fixed left-0 top-0 h-full w-72 bg-aurora-surface/95 backdrop-blur-2xl z-50 flex flex-col justify-between py-5 border-r border-aurora-border shadow-2xl">
    
    <div class="flex flex-col gap-5">
      
      <!-- Brand & Sidebar Collapse Action -->
      <div class="px-5 flex items-center justify-between border-b border-aurora-border/60 pb-4">
        <div class="flex items-center gap-3 cursor-pointer" onclick="switchNav('overview', 'Overview')">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-aurora via-aurora-mint to-teal-800 p-0.5 shadow-aurora-sm flex items-center justify-center">
            <div class="w-full h-full bg-aurora-dark rounded-[10px] flex items-center justify-center">
              <span class="material-symbols-outlined text-aurora text-2xl font-bold">cyclone</span>
            </div>
          </div>
          <div class="flex flex-col">
            <span class="text-lg font-extrabold tracking-tight text-white leading-none flex items-center gap-1.5">
              AURORA
              <span class="w-1.5 h-1.5 rounded-full bg-aurora animate-ping"></span>
            </span>
            <span class="text-[10px] text-aurora font-bold tracking-widest uppercase mt-1">Prime Equities</span>
          </div>
        </div>

        <!-- Dedicated Inside-Sidebar Collapse Button -->
        <button id="sidebar-inside-collapse" onclick="toggleSidebar()" class="p-1.5 rounded-lg bg-aurora-container hover:bg-aurora-hover border border-aurora-border text-aurora-mint hover:text-aurora hover:border-aurora/50 transition-all flex items-center justify-center group" title="Collapse Sidebar (Alt+S)">
          <span class="material-symbols-outlined text-xl group-hover:-translate-x-0.5 transition-transform">menu_open</span>
        </button>
      </div>

      <!-- Total Vault Liquidity Pill Widget -->
      <div class="px-4">
        <div class="p-3.5 rounded-xl bg-gradient-to-b from-aurora-container to-aurora-surface border border-aurora-border hover:border-aurora/40 transition-all shadow-inner relative overflow-hidden group">
          <div class="absolute -right-6 -bottom-6 w-20 h-20 bg-aurora/10 rounded-full blur-xl group-hover:bg-aurora/20 transition-all"></div>
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-bold uppercase tracking-wider text-[#80a5a0]">Total Vault Liquidity</span>
            <span class="material-symbols-outlined text-aurora text-base">lock_open</span>
          </div>
          <div class="text-xl font-mono font-bold text-white mt-1.5 flex items-baseline gap-1" id="vault-liquidity-display">
            $142,850,200
          </div>
          <div class="flex items-center gap-1.5 mt-1 text-[11px] text-aurora font-semibold">
            <span class="w-2 h-2 rounded-full bg-aurora animate-pulse"></span>
            Tier-1 Prime Settlement
          </div>
        </div>
      </div>

      <!-- Navigation Menu Links -->
      <nav class="flex flex-col gap-1 px-3" id="sidebar-nav">
        <div class="px-3 pt-2 pb-1 text-[10px] font-extrabold uppercase tracking-widest text-[#5b7b77]">Prime Navigation</div>
        
        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group" data-path="overview" onclick="switchNav('overview', 'Executive Overview')">
          <span class="material-symbols-outlined text-lg text-aurora-mint group-hover:text-aurora transition-colors">dashboard</span>
          <span>Overview</span>
        </a>

        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-aurora/15 border border-aurora/30 text-aurora font-bold text-sm shadow-aurora-sm transition-all cursor-pointer group" data-path="equities-and-stocks" onclick="switchNav('equities-and-stocks', 'Equities &amp; Stocks')">
          <span class="material-symbols-outlined text-lg text-aurora">monitoring</span>
          <span>Equities &amp; Stocks</span>
        </a>

        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group" data-path="portfolio-analytics" onclick="switchNav('portfolio-analytics', 'Portfolio Analytics')">
          <span class="material-symbols-outlined text-lg text-aurora-mint group-hover:text-aurora transition-colors">analytics</span>
          <span>Portfolio Analytics</span>
        </a>

        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group" data-path="trade-and-orders" onclick="switchNav('trade-and-orders', 'Trade &amp; Orders')">
          <span class="material-symbols-outlined text-lg text-aurora-mint group-hover:text-aurora transition-colors">sync_alt</span>
          <span>Trade &amp; Orders</span>
        </a>

        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group" data-path="treasury" onclick="switchNav('treasury', 'Treasury')">
          <span class="material-symbols-outlined text-lg text-aurora-mint group-hover:text-aurora transition-colors">account_balance</span>
          <span>Treasury</span>
        </a>

        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group" data-path="risk-and-compliance" onclick="switchNav('risk-and-compliance', 'Risk &amp; Compliance')">
          <span class="material-symbols-outlined text-lg text-aurora-mint group-hover:text-aurora transition-colors">verified_user</span>
          <span>Risk &amp; Compliance</span>
        </a>

        <a class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group" data-path="settings" onclick="switchNav('settings', 'Terminal Settings')">
          <span class="material-symbols-outlined text-lg text-aurora-mint group-hover:text-aurora transition-colors">settings</span>
          <span>Settings</span>
        </a>
      </nav>

    </div>

    <!-- Terminal Node Connectivity Footer -->
    <div class="px-4 flex flex-col gap-2">
      <div class="p-3 rounded-xl bg-aurora-container/90 border border-aurora-border flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-2.5 h-2.5 rounded-full bg-aurora animate-pulse shadow-aurora-sm"></div>
          <div class="flex flex-col">
            <span class="text-xs font-bold text-white leading-tight">Node Alpha-04</span>
            <span class="text-[10px] text-aurora font-mono">12ms • NY-EQX Live</span>
          </div>
        </div>
        <span class="text-[10px] px-2 py-0.5 rounded bg-aurora/10 text-aurora font-bold border border-aurora/30">FAST DMA</span>
      </div>
      
      <!-- Quick collapse hint -->
      <div class="text-[10px] text-[#5b7b77] text-center font-mono">Press [Alt + S] to collapse</div>
    </div>

  </aside>

  <!-- Mobile Backdrop Overlay when sidebar is open -->
  <div id="sidebar-backdrop" onclick="toggleSidebar()" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 hidden md:hidden"></div>

  <!-- =========================================================================
       2. TOPBAR HEADER WITH SIDEBAR TOGGLE BUTTON
       ========================================================================= -->
  <header id="topbar" class="fixed top-0 left-72 right-0 h-16 bg-aurora-surface/90 backdrop-blur-xl border-b border-aurora-border z-40 flex items-center justify-between px-6 shadow-md">
    
    <div class="flex items-center gap-4 flex-1 mr-6">
      
      <!-- PRIMARY SIDEBAR TOGGLE BUTTON (EXPAND / COLLAPSE) -->
      <button id="topbar-sidebar-toggle" onclick="toggleSidebar()" class="p-2 rounded-xl bg-aurora-container hover:bg-aurora-hover border border-aurora-border hover:border-aurora text-aurora-mint hover:text-aurora transition-all flex items-center justify-center shadow-sm cursor-pointer group" title="Toggle Sidebar Navigation (Alt+S)">
        <span class="material-symbols-outlined text-2xl transition-transform group-hover:scale-110" id="topbar-toggle-icon">menu</span>
      </button>

      <!-- Live Indices Ticker Tape with Aurora Nodes -->
      <div class="hidden xl:flex items-center gap-4 py-1 px-3 rounded-xl bg-aurora-container/80 border border-aurora-border font-mono text-xs">
        <div class="flex items-center gap-1.5">
          <span class="text-[#80a5a0] font-sans font-semibold">S&amp;P 500</span>
          <span class="font-bold text-white" id="idx-spx">5,917.40</span>
          <span class="text-aurora flex items-center font-semibold"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+0.64%</span>
        </div>
        <div class="w-px h-3 bg-aurora-border"></div>
        <div class="flex items-center gap-1.5">
          <span class="text-[#80a5a0] font-sans font-semibold">NASDAQ</span>
          <span class="font-bold text-white" id="idx-ndx">19,081.47</span>
          <span class="text-aurora flex items-center font-semibold"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+0.82%</span>
        </div>
        <div class="w-px h-3 bg-aurora-border"></div>
        <div class="flex items-center gap-1.5">
          <span class="text-[#80a5a0] font-sans font-semibold">NIFTY 50</span>
          <span class="font-bold text-white">23,518.50</span>
          <span class="text-aurora flex items-center font-semibold"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+1.04%</span>
        </div>
        <div class="w-px h-3 bg-aurora-border"></div>
        <div class="flex items-center gap-1.5">
          <span class="text-[#80a5a0] font-sans font-semibold">BTC/USD</span>
          <span class="font-bold text-white">$63,240</span>
          <span class="text-aurora flex items-center font-semibold"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+3.15%</span>
        </div>
      </div>

      <!-- Global Asset & Ticker Search -->
      <div class="relative w-full max-w-xs">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-aurora text-lg">search</span>
        <input id="global-search-input" class="w-full pl-9 pr-8 py-1.5 rounded-xl bg-aurora-container text-white placeholder-[#80a5a0] text-xs font-mono focus:outline-none focus:border-aurora border border-aurora-border transition-all" placeholder="Search NVDA, RELIANCE, BTC..." type="text" oninput="handleGlobalSearch(this.value)"/>
        <kbd class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[9px] px-1.5 py-0.5 rounded bg-aurora-surface text-[#80a5a0] border border-aurora-border font-mono">⌘K</kbd>
      </div>

    </div>

    <!-- Actions: Currency Selector, System Alerts, Executive Profile -->
    <div class="flex items-center gap-4">
      
      <!-- Currency Switcher -->
      <div class="flex items-center p-0.5 rounded-xl bg-aurora-container border border-aurora-border text-xs font-bold font-mono">
        <button id="curr-USD" class="px-2.5 py-1 rounded-lg bg-aurora text-black shadow-aurora-sm transition-all" onclick="setCurrency('USD')">USD</button>
        <button id="curr-INR" class="px-2.5 py-1 rounded-lg text-[#80a5a0] hover:text-white transition-all" onclick="setCurrency('INR')">INR</button>
        <button id="curr-EUR" class="px-2.5 py-1 rounded-lg text-[#80a5a0] hover:text-white transition-all" onclick="setCurrency('EUR')">EUR</button>
        <button id="curr-GBP" class="px-2.5 py-1 rounded-lg text-[#80a5a0] hover:text-white transition-all" onclick="setCurrency('GBP')">GBP</button>
      </div>

      <!-- Quick Action: Export & Alert -->
      <button onclick="triggerToast('System Alerts', 'Aurora Node NY-EQX: Latency 12ms. All risk gates green.')" class="relative p-2 rounded-xl bg-aurora-container hover:bg-aurora-hover border border-aurora-border text-[#80a5a0] hover:text-aurora transition-colors" title="System Status">
        <span class="material-symbols-outlined text-xl">notifications</span>
        <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-aurora animate-ping"></span>
      </button>

      <!-- Executive Profile Avatar -->
      <div class="flex items-center gap-3 pl-2 border-l border-aurora-border">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-aurora-container via-teal-900 to-aurora p-0.5 shadow-sm">
          <div class="w-full h-full bg-aurora-dark rounded-[10px] flex items-center justify-center text-aurora font-bold text-xs">
            AV
          </div>
        </div>
        <div class="hidden md:flex flex-col text-left">
          <span class="text-xs font-extrabold text-white leading-tight">Alexander Vance</span>
          <span class="text-[10px] text-aurora font-semibold leading-tight">Chief Investment Officer</span>
        </div>
      </div>

    </div>

  </header>

  <!-- =========================================================================
       3. FLOATING QUICK-ACCESS SIDEBAR BUTTON (VISIBLE WHEN COLLAPSED)
       ========================================================================= -->
  <button id="floating-sidebar-toggle" onclick="toggleSidebar()" class="fixed bottom-6 left-6 z-50 p-3 rounded-2xl bg-aurora-container/95 border-2 border-aurora text-aurora shadow-aurora-md hover:scale-110 hover:bg-aurora hover:text-black transition-all flex items-center gap-2 font-bold text-xs cursor-pointer group" title="Expand Aurora Sidebar (Alt+S)">
    <span class="material-symbols-outlined text-2xl group-hover:rotate-180 transition-transform">dock_to_right</span>
    <span class="hidden sm:inline font-mono">SIDEBAR</span>
  </button>

  <!-- =========================================================================
       4. MAIN CONTENT VIEW WRAPPER
       ========================================================================= -->
  <div id="main-content-wrapper" class="pl-72 pt-16 min-h-screen relative z-10 transition-all duration-300">
    <main class="w-full px-6 py-6 max-w-[1720px] mx-auto">
      
      <!-- Top Banner Header & Timeframe Pills -->
      <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-5 mb-6">
        <div class="flex flex-col gap-1">
          <div class="flex items-center gap-2 text-xs uppercase tracking-widest text-[#80a5a0] font-bold">
            <span>Portfolio Mandate</span>
            <span class="material-symbols-outlined text-xs text-aurora">chevron_right</span>
            <span class="text-aurora font-extrabold" id="breadcrumb-current">Equities &amp; Stocks</span>
          </div>
          <div class="flex flex-wrap items-center gap-3">
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight" id="main-title">
              Equities &amp; Valuation Terminal
            </h1>
            <div class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-aurora/10 border border-aurora/30 shadow-aurora-sm">
              <span class="w-2 h-2 rounded-full bg-aurora animate-pulse"></span>
              <span class="text-xs text-aurora font-bold font-mono">AURORA LIVE FEED • 0.05s</span>
            </div>
          </div>
        </div>

        <!-- Controls: Timeframe Pills & Action Buttons -->
        <div class="flex flex-wrap items-center gap-2.5">
          
          <!-- Timeframe Selector -->
          <div class="inline-flex p-1 rounded-xl bg-aurora-container border border-aurora-border shadow-inner" id="timeframe-buttons">
            <button class="px-3 py-1 rounded-lg text-xs font-bold text-[#80a5a0] hover:text-white transition-colors cursor-pointer" onclick="setTimeframe('1D', this)">1D</button>
            <button class="px-3 py-1 rounded-lg text-xs font-bold text-[#80a5a0] hover:text-white transition-colors cursor-pointer" onclick="setTimeframe('1W', this)">1W</button>
            <button class="px-3 py-1 rounded-lg text-xs font-bold text-[#80a5a0] hover:text-white transition-colors cursor-pointer" onclick="setTimeframe('1M', this)">1M</button>
            <button class="px-3 py-1 rounded-lg text-xs font-bold bg-aurora text-black shadow-aurora-sm font-extrabold cursor-pointer" onclick="setTimeframe('3M', this)">3M</button>
            <button class="px-3 py-1 rounded-lg text-xs font-bold text-[#80a5a0] hover:text-white transition-colors cursor-pointer" onclick="setTimeframe('1Y', this)">1Y</button>
            <button class="px-3 py-1 rounded-lg text-xs font-bold text-[#80a5a0] hover:text-white transition-colors cursor-pointer" onclick="setTimeframe('ALL', this)">ALL</button>
          </div>

          <!-- Export CSV -->
          <button onclick="exportHoldingsCSV()" class="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-aurora-container hover:bg-aurora-hover border border-aurora-border text-white text-xs font-bold transition-all shadow-sm cursor-pointer">
            <span class="material-symbols-outlined text-base text-aurora">file_download</span>
            <span>Export CSV</span>
          </button>

          <!-- Place Order Shortcut -->
          <button onclick="scrollToOrderDesk()" class="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-aurora via-aurora-bright to-aurora-mint text-black font-extrabold text-xs shadow-aurora-md hover:scale-105 transition-all cursor-pointer">
            <span class="material-symbols-outlined text-base font-bold">bolt</span>
            <span>DMA Order Desk</span>
          </button>

        </div>
      </div>

      <!-- =====================================================================
           5. TOP 4 EXECUTIVE KPI CARDS (AURORA GREEN THEMED)
           ===================================================================== -->
      <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        
        <!-- Card 1: Total Portfolio Value -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-b from-aurora-container to-aurora-surface p-5 border border-aurora-border hover:border-aurora/50 transition-all shadow-glass group">
          <div class="absolute -right-6 -top-6 w-28 h-28 bg-aurora/10 rounded-full blur-2xl group-hover:bg-aurora/25 transition-all"></div>
          <div class="flex items-start justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-[#80a5a0]">Total Portfolio Value</span>
            <div class="w-8 h-8 rounded-xl bg-aurora/15 border border-aurora/30 flex items-center justify-center text-aurora shadow-aurora-sm">
              <span class="material-symbols-outlined text-base">account_balance_wallet</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="text-2xl sm:text-3xl font-mono font-extrabold text-white tracking-tight" id="kpi-total-val">$14,842,920.45</div>
            <div class="flex items-center gap-2 mt-2">
              <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold bg-aurora/15 text-aurora border border-aurora/30">
                ▲ +2.48%
              </span>
              <span class="text-xs text-[#80a5a0] font-mono">+$359,120.00 intraday</span>
            </div>
          </div>
        </div>

        <!-- Card 2: Unrealized Capital Gains -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-b from-aurora-container to-aurora-surface p-5 border border-aurora-border hover:border-aurora/50 transition-all shadow-glass group">
          <div class="absolute -right-6 -top-6 w-28 h-28 bg-aurora-mint/10 rounded-full blur-2xl group-hover:bg-aurora-mint/25 transition-all"></div>
          <div class="flex items-start justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-[#80a5a0]">Unrealized Net Gain</span>
            <div class="w-8 h-8 rounded-xl bg-aurora-mint/15 border border-aurora-mint/30 flex items-center justify-center text-aurora-mint shadow-aurora-sm">
              <span class="material-symbols-outlined text-base">trending_up</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="text-2xl sm:text-3xl font-mono font-extrabold text-aurora tracking-tight" id="kpi-unrealized-val">+$3,210,480.00</div>
            <div class="flex items-center gap-2 mt-2">
              <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold bg-aurora/20 text-aurora border border-aurora/40">
                ▲ +27.64%
              </span>
              <span class="text-xs text-[#80a5a0] font-mono">Cost Basis: $11.63M</span>
            </div>
          </div>
        </div>

        <!-- Card 3: Cash & Execution Buffer -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-b from-aurora-container to-aurora-surface p-5 border border-aurora-border hover:border-aurora/50 transition-all shadow-glass group">
          <div class="flex items-start justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-[#80a5a0]">Day Buffer &amp; Execution</span>
            <div class="w-8 h-8 rounded-xl bg-sky-500/15 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <span class="material-symbols-outlined text-base">swap_horiz</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="text-2xl sm:text-3xl font-mono font-extrabold text-white tracking-tight" id="kpi-cash-val">$1,894,200.00</div>
            <div class="flex items-center justify-between gap-2 mt-2">
              <span class="text-xs text-[#80a5a0]">Liquid Reserves:</span>
              <span class="text-xs text-sky-400 font-bold font-mono">$2,450,000.00</span>
            </div>
          </div>
        </div>

        <!-- Card 4: Quantitative Risk Profiling -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-b from-aurora-container to-aurora-surface p-5 border border-aurora-border hover:border-aurora/50 transition-all shadow-glass group">
          <div class="flex items-start justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-[#80a5a0]">Risk Profiling (SPX)</span>
            <div class="w-8 h-8 rounded-xl bg-amber-400/15 border border-amber-400/30 flex items-center justify-center text-amber-400">
              <span class="material-symbols-outlined text-base">security</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="flex items-baseline gap-2">
              <div class="text-2xl sm:text-3xl font-mono font-extrabold text-white tracking-tight">0.94</div>
              <span class="text-xs text-[#80a5a0] font-bold">Beta vs SPX</span>
            </div>
            <div class="flex items-center gap-3 mt-2">
              <div class="flex items-center gap-1.5 text-xs text-aurora font-semibold">
                <span class="w-2 h-2 rounded-full bg-aurora"></span>
                Defensive Low Vol
              </div>
              <span class="px-2 py-0.5 rounded bg-aurora/10 text-aurora text-[10px] font-bold border border-aurora/30">ESG: AA</span>
            </div>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           6. MID SECTION: VALUATION AREA CANVAS & ORDER DESK (12-COL GRID)
           ===================================================================== -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-5 mb-6">
        
        <!-- Left: Holdings Valuation Trajectory (Col 8 / ~68%) -->
        <div class="xl:col-span-8 rounded-2xl bg-aurora-surface/90 border border-aurora-border p-6 shadow-glass flex flex-col justify-between relative overflow-hidden">
          
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
            <div>
              <div class="flex items-center gap-2">
                <h2 class="text-base sm:text-lg font-extrabold text-white">Holdings Valuation Trajectory</h2>
                <span class="material-symbols-outlined text-aurora-mint text-base cursor-pointer hover:text-aurora" title="Historical Multi-Asset NAV with Alpha Benchmark Accretion">info</span>
              </div>
              <p class="text-xs text-[#80a5a0]">Live marked-to-market performance vs S&amp;P 500 Index</p>
            </div>
            
            <!-- Legend Indicators -->
            <div class="flex items-center gap-4 text-xs font-mono">
              <div class="flex items-center gap-1.5">
                <span class="w-3 h-3 rounded-full bg-aurora shadow-aurora-sm"></span>
                <span class="text-white font-bold">Portfolio NAV</span>
              </div>
              <div class="flex items-center gap-1.5">
                <span class="w-3 h-3 rounded-full bg-aurora-cyan"></span>
                <span class="text-[#80a5a0]">S&amp;P 500</span>
              </div>
              <div class="flex items-center gap-1.5">
                <span class="w-4 h-0.5 bg-[#5b7b77]"></span>
                <span class="text-[#80a5a0]">Cost Basis</span>
              </div>
            </div>
          </div>

          <!-- Dynamic SVG Area Performance Graph -->
          <div class="relative w-full h-72 sm:h-80 flex flex-col justify-end pt-2">
            <svg id="trajectory-svg" class="w-full h-full overflow-visible" preserveaspectratio="none" viewbox="0 0 760 260">
              <defs>
                <!-- Neon Aurora Green Gradient -->
                <lineargradient id="auroraNavGrad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#00ff9d" stop-opacity="0.35"></stop>
                  <stop offset="70%" stop-color="#00f5d4" stop-opacity="0.08"></stop>
                  <stop offset="100%" stop-color="#040a0c" stop-opacity="0.0"></stop>
                </lineargradient>
                <!-- Benchmark Cyan Gradient -->
                <lineargradient id="benchmarkGrad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.18"></stop>
                  <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.0"></stop>
                </lineargradient>
              </defs>

              <!-- Subtle Gridlines -->
              <line stroke="#1a3d46" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="30" y2="30"></line>
              <line stroke="#1a3d46" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="90" y2="90"></line>
              <line stroke="#1a3d46" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="150" y2="150"></line>
              <line stroke="#1a3d46" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="210" y2="210"></line>
              
              <!-- Cost Basis Baseline -->
              <line stroke="#5b7b77" stroke-dasharray="6 4" stroke-width="1.5" x1="0" x2="760" y1="180" y2="180"></line>

              <!-- S&P 500 Benchmark Curve -->
              <path id="spx-area" d="M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65 L 760 240 L 0 240 Z" fill="url(#benchmarkGrad)"></path>
              <path id="spx-line" d="M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65" fill="none" stroke="#38bdf8" stroke-linecap="round" stroke-width="2"></path>

              <!-- Aurora NAV Area Curve -->
              <path id="nav-area" d="M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22 L 760 240 L 0 240 Z" fill="url(#auroraNavGrad)"></path>
              <path id="nav-line" d="M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22" fill="none" stroke="#00ff9d" stroke-linecap="round" stroke-width="3.5" filter="drop-shadow(0 0 8px rgba(0,255,157,0.7))"></path>

              <!-- Peak Performance Glow Nodes -->
              <circle id="peak-core" cx="620" cy="50" fill="#00ff9d" r="5.5" class="aurora-pulse"></circle>
              <circle id="peak-ring" cx="620" cy="50" fill="#00ff9d" fill-opacity="0.3" r="12"></circle>
            </svg>

            <!-- Floating Peak Metric Tooltip -->
            <div id="chart-tag" class="absolute left-3/4 -top-1 -translate-x-1/2 rounded-xl bg-aurora-card px-3 py-1.5 shadow-aurora-md border border-aurora flex flex-col pointer-events-none">
              <span class="text-[10px] text-[#80a5a0] uppercase font-bold" id="tag-label">All-Time Peak</span>
              <span class="text-xs font-mono font-extrabold text-aurora" id="tag-val">$14,842,920</span>
            </div>

            <!-- Horizontal Time Axis -->
            <div class="flex justify-between items-center text-[#80a5a0] font-mono text-[11px] pt-3 mt-2 border-t border-aurora-border/60" id="axis-labels">
              <span>Nov 01</span>
              <span>Nov 05</span>
              <span>Nov 10</span>
              <span>Nov 15</span>
              <span>Nov 20</span>
              <span>Nov 25</span>
              <span class="text-aurora font-bold">Today</span>
            </div>
          </div>

          <!-- Quantitative Metrics Strip under Chart -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 mt-4 bg-aurora-container/60 rounded-xl p-3 border border-aurora-border">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#80a5a0]">Alpha vs Benchmark</span>
              <p class="text-lg font-mono font-extrabold text-aurora">+8.42%</p>
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#80a5a0]">Sharpe Ratio</span>
              <p class="text-lg font-mono font-extrabold text-white">2.41</p>
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#80a5a0]">Tracking Error</span>
              <p class="text-lg font-mono font-extrabold text-white">1.18%</p>
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#80a5a0]">Max Drawdown (1Y)</span>
              <p class="text-lg font-mono font-extrabold text-aurora-rose">-4.12%</p>
            </div>
          </div>

        </div>

        <!-- Right Stack: Sector Weighting & DMA Order Desk (Col 4 / ~32%) -->
        <div class="xl:col-span-4 flex flex-col gap-5">
          
          <!-- Sector Weighting Breakdown -->
          <div class="rounded-2xl bg-aurora-surface/90 border border-aurora-border p-5 shadow-glass">
            <div class="flex items-center justify-between mb-3">
              <h2 class="text-sm font-extrabold text-white">Sector Allocation</h2>
              <span class="text-[11px] font-mono text-aurora font-bold">100% Capitalized</span>
            </div>
            <div class="flex flex-col gap-2.5">
              <!-- Technology -->
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-white font-semibold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-aurora"></span>Technology &amp; AI</span>
                  <span class="font-mono font-bold text-white">42.0% <span class="text-[#80a5a0] font-normal">($6.23M)</span></span>
                </div>
                <div class="w-full bg-aurora-container rounded-full h-1.5 overflow-hidden">
                  <div class="bg-gradient-to-r from-aurora to-aurora-mint h-full rounded-full shadow-aurora-sm" style="width: 42%;"></div>
                </div>
              </div>
              <!-- Financials -->
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-white font-semibold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-sky-400"></span>Banking &amp; Financials</span>
                  <span class="font-mono font-bold text-white">24.0% <span class="text-[#80a5a0] font-normal">($3.56M)</span></span>
                </div>
                <div class="w-full bg-aurora-container rounded-full h-1.5 overflow-hidden">
                  <div class="bg-sky-400 h-full rounded-full" style="width: 24%;"></div>
                </div>
              </div>
              <!-- Energy & Infra -->
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-white font-semibold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-400"></span>Energy &amp; Conglomerates</span>
                  <span class="font-mono font-bold text-white">18.0% <span class="text-[#80a5a0] font-normal">($2.67M)</span></span>
                </div>
                <div class="w-full bg-aurora-container rounded-full h-1.5 overflow-hidden">
                  <div class="bg-amber-400 h-full rounded-full" style="width: 18%;"></div>
                </div>
              </div>
              <!-- Semiconductors -->
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-white font-semibold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-purple-400"></span>Semiconductors &amp; Systems</span>
                  <span class="font-mono font-bold text-white">16.0% <span class="text-[#80a5a0] font-normal">($2.38M)</span></span>
                </div>
                <div class="w-full bg-aurora-container rounded-full h-1.5 overflow-hidden">
                  <div class="bg-purple-400 h-full rounded-full" style="width: 16%;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Institutional Order Desk Card -->
          <div id="order-desk-card" class="rounded-2xl bg-aurora-surface/90 border border-aurora-border p-5 shadow-glass flex flex-col justify-between flex-1">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-aurora text-lg">bolt</span>
                <h2 class="text-sm font-extrabold text-white">DMA Institutional Order Desk</h2>
              </div>
              <span class="px-2 py-0.5 rounded bg-aurora/10 text-aurora text-[10px] font-bold font-mono border border-aurora/30">NODE 04 ACTIVE</span>
            </div>

            <!-- Buy / Sell Side Selector -->
            <div class="grid grid-cols-2 p-1 rounded-xl bg-aurora-container border border-aurora-border mb-3 font-mono">
              <button id="side-buy-btn" onclick="setOrderSide('BUY')" class="py-1.5 rounded-lg bg-aurora text-black font-extrabold text-xs shadow-aurora-sm transition-all cursor-pointer">
                BUY (LONG)
              </button>
              <button id="side-sell-btn" onclick="setOrderSide('SELL')" class="py-1.5 rounded-lg text-[#80a5a0] hover:text-white font-extrabold text-xs transition-all cursor-pointer">
                SELL (SHORT)
              </button>
            </div>

            <!-- Ticker & Order Type -->
            <div class="grid grid-cols-2 gap-2.5 mb-2.5">
              <div>
                <label class="block text-[10px] font-bold uppercase tracking-wider text-[#80a5a0] mb-1">Asset Ticker</label>
                <select id="order-ticker-select" class="w-full py-1.5 px-2.5 rounded-xl bg-aurora-container text-white font-mono font-bold text-xs border border-aurora-border focus:border-aurora outline-none" onchange="handleTickerSelect(this.value)">
                  <option value="NVDA">NVDA ($128.40)</option>
                  <option value="RELIANCE.NS">RELIANCE (₹1,360)</option>
                  <option value="MSFT">MSFT ($448.20)</option>
                  <option value="TCS.NS">TCS (₹2,349)</option>
                  <option value="AAPL">AAPL ($224.50)</option>
                  <option value="HDFCBANK.NS">HDFCBANK (₹1,742)</option>
                  <option value="BTC-USD">BTC-USD ($63,240)</option>
                </select>
              </div>
              <div>
                <label class="block text-[10px] font-bold uppercase tracking-wider text-[#80a5a0] mb-1">Execution Mode</label>
                <select id="order-type-select" class="w-full py-1.5 px-2.5 rounded-xl bg-aurora-container text-white font-mono font-bold text-xs border border-aurora-border focus:border-aurora outline-none">
                  <option value="LIMIT">Limit Order</option>
                  <option value="MARKET">Market Direct</option>
                  <option value="STOP_LOSS">Stop-Loss DMA</option>
                </select>
              </div>
            </div>

            <!-- Shares Count & Limit Price -->
            <div class="grid grid-cols-2 gap-2.5 mb-3">
              <div>
                <label class="block text-[10px] font-bold uppercase tracking-wider text-[#80a5a0] mb-1">Quantity (Shares)</label>
                <input id="order-shares" type="number" value="500" min="1" class="w-full py-1.5 px-2.5 rounded-xl bg-aurora-container text-white font-mono font-bold text-xs border border-aurora-border focus:border-aurora outline-none" oninput="recalcOrderTotal()"/>
              </div>
              <div>
                <label class="block text-[10px] font-bold uppercase tracking-wider text-[#80a5a0] mb-1">Price Limit</label>
                <input id="order-limit" type="number" step="0.1" value="128.40" class="w-full py-1.5 px-2.5 rounded-xl bg-aurora-container text-white font-mono font-bold text-xs border border-aurora-border focus:border-aurora outline-none" oninput="recalcOrderTotal()"/>
              </div>
            </div>

            <!-- Quick Pill Multipliers -->
            <div class="grid grid-cols-4 gap-1.5 mb-3 font-mono">
              <button onclick="setSharesQty(250)" class="py-1 rounded-lg bg-aurora-container hover:bg-aurora-hover text-[#80a5a0] hover:text-white text-[11px] font-bold border border-aurora-border transition-colors">250</button>
              <button onclick="setSharesQty(500)" class="py-1 rounded-lg bg-aurora-container hover:bg-aurora-hover text-[#80a5a0] hover:text-white text-[11px] font-bold border border-aurora-border transition-colors">500</button>
              <button onclick="setSharesQty(1000)" class="py-1 rounded-lg bg-aurora-container hover:bg-aurora-hover text-[#80a5a0] hover:text-white text-[11px] font-bold border border-aurora-border transition-colors">1,000</button>
              <button onclick="setSharesQty(2500)" class="py-1 rounded-lg bg-aurora-container hover:bg-aurora-hover text-[#80a5a0] hover:text-white text-[11px] font-bold border border-aurora-border transition-colors">2,500</button>
            </div>

            <!-- Settlement Consideration -->
            <div class="p-3 rounded-xl bg-aurora-container border border-aurora-border flex items-center justify-between mb-3 font-mono">
              <span class="text-xs text-[#80a5a0]">Est. Gross Consideration:</span>
              <span class="text-sm font-extrabold text-aurora" id="order-est-total">$64,200.00</span>
            </div>

            <!-- Transmit Order Button -->
            <button onclick="transmitOrder()" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-aurora via-aurora-bright to-aurora-mint text-black font-extrabold text-xs tracking-wider shadow-aurora-md hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer" id="order-submit-btn">
              <span class="material-symbols-outlined text-base">send</span>
              <span id="order-submit-text">TRANSMIT DMA ORDER TICKET</span>
            </button>

          </div>

        </div>

      </div>

      <!-- =====================================================================
           7. MULTI-MARKET HOLDINGS DATA GRID (WITH SEARCH, SPARKLINE, CSV)
           ===================================================================== -->
      <div class="rounded-2xl bg-aurora-surface/90 border border-aurora-border shadow-glass overflow-hidden">
        
        <!-- Table Control Toolbar -->
        <div class="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-aurora-border">
          <div class="flex items-center gap-3">
            <h2 class="text-base font-extrabold text-white">Institutional Holdings &amp; Positions</h2>
            <span class="px-2.5 py-0.5 rounded-full bg-aurora/10 text-aurora font-mono text-xs font-bold border border-aurora/30" id="holdings-count-badge">8 Core Assets Active</span>
          </div>

          <div class="flex flex-wrap items-center gap-2.5">
            <!-- Filter Ticker Search -->
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-aurora text-base">search</span>
              <input id="table-search-input" type="text" placeholder="Filter ticker, name..." class="pl-9 pr-3 py-1.5 rounded-xl bg-aurora-container text-white placeholder-[#80a5a0] text-xs font-mono border border-aurora-border focus:border-aurora outline-none w-48 sm:w-60" oninput="filterTable()"/>
            </div>

            <!-- Market Filter Dropdown -->
            <select id="market-filter-select" class="px-3 py-1.5 rounded-xl bg-aurora-container text-white font-mono text-xs border border-aurora-border focus:border-aurora outline-none" onchange="filterTable()">
              <option value="ALL">All Markets</option>
              <option value="US">US Equities</option>
              <option value="IN">Indian NSE (.NS)</option>
              <option value="CRYPTO">Crypto &amp; FX</option>
            </select>

            <!-- Sector Filter Dropdown -->
            <select id="sector-filter-select" class="px-3 py-1.5 rounded-xl bg-aurora-container text-white font-mono text-xs border border-aurora-border focus:border-aurora outline-none" onchange="filterTable()">
              <option value="ALL">All Sectors</option>
              <option value="Technology">Technology</option>
              <option value="Financials">Financials</option>
              <option value="Energy">Energy</option>
              <option value="Semiconductors">Semiconductors</option>
            </select>
          </div>
        </div>

        <!-- Table Container -->
        <div class="overflow-x-auto w-full">
          <table class="w-full text-left" id="holdings-table">
            <thead>
              <tr class="bg-aurora-container/70 text-[#80a5a0] font-mono text-[11px] uppercase tracking-wider border-b border-aurora-border">
                <th class="py-3 px-4 font-bold">Asset &amp; Ticker</th>
                <th class="py-3 px-4 font-bold text-right">Shares Held</th>
                <th class="py-3 px-4 font-bold text-right">Avg Cost</th>
                <th class="py-3 px-4 font-bold text-right">Market Price</th>
                <th class="py-3 px-4 font-bold text-right">Total Market Value</th>
                <th class="py-3 px-4 font-bold text-right">Day P&amp;L</th>
                <th class="py-3 px-4 font-bold text-right">Unrealized Gain</th>
                <th class="py-3 px-4 font-bold text-center">7D Aurora Sparkline</th>
                <th class="py-3 px-4 font-bold text-center">Action</th>
              </tr>
            </thead>
            <tbody id="holdings-tbody" class="divide-y divide-aurora-border/50 text-xs font-mono">
              
              <!-- NVDA -->
              <tr class="hover:bg-aurora-container/60 transition-colors" data-ticker="NVDA" data-company="NVIDIA Corporation" data-market="US" data-sector="Technology">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-aurora/15 border border-aurora/30 flex items-center justify-center text-aurora font-extrabold text-xs shadow-aurora-sm">NV</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">NVIDIA Corporation</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-aurora font-bold">NVDA</span>
                        <span class="text-[#80a5a0]">• US MegaCap Tech</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">8,500</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">$88.20</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$128.40</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$1,091,400.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$44,450 (+4.25%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$341,700 (+45.58%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 20 L 20 18 L 40 14 L 60 16 L 80 8 L 100 3" stroke="#00ff9d" stroke-linecap="round" stroke-width="2" filter="drop-shadow(0 0 4px rgba(0,255,157,0.5))"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('NVDA', 128.40)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- RELIANCE.NS -->
              <tr class="hover:bg-aurora-container/60 transition-colors bg-aurora-container/20" data-ticker="RELIANCE.NS" data-company="Reliance Industries Ltd" data-market="IN" data-sector="Energy">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-amber-400/15 border border-amber-400/30 flex items-center justify-center text-amber-400 font-extrabold text-xs">RI</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">Reliance Industries Ltd</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-amber-400 font-bold">RELIANCE.NS</span>
                        <span class="text-[#80a5a0]">• NSE Energy &amp; Telecom</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">125,000</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">₹1,180.50</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">₹1,360.20</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">₹170,025,000.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+₹328,000 (+2.14%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+₹22.4M (+15.2%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 18 L 25 15 L 45 16 L 70 10 L 100 4" stroke="#ffd166" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('RELIANCE.NS', 1360.20)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- MSFT -->
              <tr class="hover:bg-aurora-container/60 transition-colors" data-ticker="MSFT" data-company="Microsoft Corporation" data-market="US" data-sector="Technology">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-sky-400/15 border border-sky-400/30 flex items-center justify-center text-sky-400 font-extrabold text-xs">MS</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">Microsoft Corporation</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-sky-400 font-bold">MSFT</span>
                        <span class="text-[#80a5a0]">• US Cloud &amp; AI</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">7,200</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">$382.50</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$448.20</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$3,227,040.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$57,600 (+1.82%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$473,040 (+17.18%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 18 L 25 16 L 50 14 L 75 10 L 100 4" stroke="#00ff9d" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('MSFT', 448.20)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- TCS.NS -->
              <tr class="hover:bg-aurora-container/60 transition-colors bg-aurora-container/20" data-ticker="TCS.NS" data-company="Tata Consultancy Services" data-market="IN" data-sector="Technology">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-aurora-mint/15 border border-aurora-mint/30 flex items-center justify-center text-aurora-mint font-extrabold text-xs">TC</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">Tata Consultancy Services Ltd</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-aurora-mint font-bold">TCS.NS</span>
                        <span class="text-[#80a5a0]">• NSE Enterprise IT</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">85,000</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">₹2,150.00</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">₹2,349.40</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">₹199,699,000.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+₹142,000 (+0.84%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+₹16.9M (+9.27%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 17 L 30 15 L 50 18 L 75 11 L 100 6" stroke="#00f5d4" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('TCS.NS', 2349.40)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- AAPL -->
              <tr class="hover:bg-aurora-container/60 transition-colors" data-ticker="AAPL" data-company="Apple Inc." data-market="US" data-sector="Technology">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-purple-400/15 border border-purple-400/30 flex items-center justify-center text-purple-400 font-extrabold text-xs">AP</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">Apple Inc.</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-purple-400 font-bold">AAPL</span>
                        <span class="text-[#80a5a0]">• US Consumer Tech</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">12,000</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">$175.40</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$224.50</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$2,694,000.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$30,600 (+1.15%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$589,200 (+27.99%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 16 L 25 17 L 50 12 L 75 14 L 100 5" stroke="#00ff9d" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('AAPL', 224.50)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- HDFCBANK.NS -->
              <tr class="hover:bg-aurora-container/60 transition-colors bg-aurora-container/20" data-ticker="HDFCBANK.NS" data-company="HDFC Bank Ltd" data-market="IN" data-sector="Financials">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-aurora/15 border border-aurora/30 flex items-center justify-center text-aurora font-extrabold text-xs">HD</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">HDFC Bank Ltd</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-aurora font-bold">HDFCBANK.NS</span>
                        <span class="text-[#80a5a0]">• NSE Premier Banking</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">190,000</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">₹1,540.20</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">₹1,742.60</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">₹331,094,000.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+₹420,000 (+1.45%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+₹38.4M (+13.1%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 19 L 25 16 L 50 14 L 75 10 L 100 5" stroke="#00ff9d" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('HDFCBANK.NS', 1742.60)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- BTC-USD -->
              <tr class="hover:bg-aurora-container/60 transition-colors" data-ticker="BTC-USD" data-company="Bitcoin Core Treasury" data-market="CRYPTO" data-sector="Financials">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-amber-400/15 border border-amber-400/30 flex items-center justify-center text-amber-400 font-extrabold text-xs">₿</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">Bitcoin Core Treasury</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-amber-400 font-bold">BTC-USD</span>
                        <span class="text-[#80a5a0]">• Global Crypto Treasury</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">45.0</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">$51,200.00</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$63,240.00</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$2,845,800.00</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$88,200 (+3.15%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$541,800 (+23.51%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 21 L 20 18 L 40 12 L 65 15 L 85 8 L 100 3" stroke="#ffd166" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('BTC-USD', 63240.00)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

              <!-- ASML -->
              <tr class="hover:bg-aurora-container/60 transition-colors bg-aurora-container/20" data-ticker="ASML" data-company="ASML Holding NV" data-market="US" data-sector="Semiconductors">
                <td class="py-3.5 px-4 font-sans">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-aurora-rose/15 border border-aurora-rose/30 flex items-center justify-center text-aurora-rose font-extrabold text-xs">AS</div>
                    <div class="flex flex-col">
                      <span class="font-extrabold text-white text-xs">ASML Holding NV</span>
                      <div class="flex items-center gap-1.5 text-[11px] font-mono">
                        <span class="text-aurora-rose font-bold">ASML</span>
                        <span class="text-[#80a5a0]">• Lithography Systems</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3.5 px-4 text-right text-white font-bold">1,500</td>
                <td class="py-3.5 px-4 text-right text-[#80a5a0]">$690.00</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$920.00</td>
                <td class="py-3.5 px-4 text-right text-white font-extrabold">$1,380,000.00</td>
                <td class="py-3.5 px-4 text-right text-aurora-rose font-bold">-$6,250 (-0.45%)</td>
                <td class="py-3.5 px-4 text-right text-aurora font-bold">+$345,000 (+33.33%)</td>
                <td class="py-3.5 px-4 text-center">
                  <svg class="w-24 h-6 mx-auto" fill="none" viewBox="0 0 100 24">
                    <path d="M 0 6 L 25 9 L 50 14 L 75 12 L 100 19" stroke="#ff4d6d" stroke-linecap="round" stroke-width="2"></path>
                  </svg>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <button onclick="prefillOrder('ASML', 920.00)" class="px-2.5 py-1 rounded-lg bg-aurora/15 hover:bg-aurora text-aurora hover:text-black font-extrabold text-[11px] border border-aurora/40 transition-all cursor-pointer">
                    Trade
                  </button>
                </td>
              </tr>

            </tbody>
          </table>
        </div>

        <!-- Table Summary Footer -->
        <div class="p-4 bg-aurora-container/90 border-t border-aurora-border flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs font-mono">
          <div class="text-[#80a5a0] flex items-center gap-2">
            <span id="footer-count-text">Showing 8 of 8 active core assets</span>
            <span>•</span>
            <span>Total Direct Equities: <span class="text-aurora font-bold">$14,842,920.45</span></span>
          </div>
          <div class="flex items-center gap-1.5">
            <button onclick="triggerToast('Pagination', 'Displaying Page 1 of Institutional Register.')" class="px-3 py-1 rounded-lg bg-aurora-surface hover:bg-aurora-hover text-[#80a5a0] hover:text-white border border-aurora-border transition-colors">Prev</button>
            <button class="px-3 py-1 rounded-lg bg-aurora text-black font-extrabold shadow-aurora-sm">1</button>
            <button onclick="triggerToast('Pagination', 'No additional pages in active mandate.')" class="px-3 py-1 rounded-lg bg-aurora-surface hover:bg-aurora-hover text-[#80a5a0] hover:text-white border border-aurora-border transition-colors">Next</button>
          </div>
        </div>

      </div>

    </main>
  </div>

  <!-- Notification Toast Container -->
  <div id="toast-container" class="fixed bottom-6 right-6 z-50 pointer-events-none flex flex-col gap-2.5"></div>

  <!-- =========================================================================
       8. INTERACTIVE JAVASCRIPT LOGIC
       ========================================================================= -->
  <script>
    // Asset reference prices
    const ASSET_PRICES = {
      "NVDA": 128.40,
      "RELIANCE.NS": 1360.20,
      "MSFT": 448.20,
      "TCS.NS": 2349.40,
      "AAPL": 224.50,
      "HDFCBANK.NS": 1742.60,
      "BTC-USD": 63240.00,
      "ASML": 920.00
    };

    let isSidebarOpen = true;
    let currentSide = "BUY";
    let currentCurrency = "USD";
    const FX_RATES = { "USD": 1.0, "INR": 84.42, "EUR": 0.92, "GBP": 0.79 };
    const FX_SYMBOLS = { "USD": "$", "INR": "₹", "EUR": "€", "GBP": "£" };

    // =======================================================================
    // 1. SIDEBAR TOGGLE & DRAWER CONTROLS
    // =======================================================================
    function toggleSidebar() {
      const sidebar = document.getElementById("sidebar");
      const wrapper = document.getElementById("main-content-wrapper");
      const topbar = document.getElementById("topbar");
      const topbarIcon = document.getElementById("topbar-toggle-icon");
      const floatingBtn = document.getElementById("floating-sidebar-toggle");
      const backdrop = document.getElementById("sidebar-backdrop");

      isSidebarOpen = !isSidebarOpen;

      if (isSidebarOpen) {
        // Expand Sidebar
        sidebar.style.transform = "translateX(0)";
        wrapper.style.paddingLeft = window.innerWidth >= 768 ? "18rem" : "0";
        topbar.style.left = window.innerWidth >= 768 ? "18rem" : "0";
        topbarIcon.innerText = "menu";
        floatingBtn.style.display = "none";
        backdrop.classList.add("hidden");
        triggerToast("Sidebar Expanded", "Navigation panel restored.");
      } else {
        // Collapse Sidebar
        sidebar.style.transform = "translateX(-100%)";
        wrapper.style.paddingLeft = "0";
        topbar.style.left = "0";
        topbarIcon.innerText = "menu_open";
        floatingBtn.style.display = "flex";
        backdrop.classList.add("hidden");
        triggerToast("Sidebar Collapsed", "Expanded canvas view active. Click Menu or press Alt+S to restore.");
      }
    }

    // Keyboard shortcut for sidebar: Alt+S or Ctrl+B
    window.addEventListener("keydown", (e) => {
      if ((e.altKey && e.key.toLowerCase() === 's') || (e.ctrlKey && e.key.toLowerCase() === 'b')) {
        e.preventDefault();
        toggleSidebar();
      }
    });

    // Handle responsive resize
    window.addEventListener("resize", () => {
      const wrapper = document.getElementById("main-content-wrapper");
      const topbar = document.getElementById("topbar");
      if (isSidebarOpen) {
        if (window.innerWidth < 768) {
          wrapper.style.paddingLeft = "0";
          topbar.style.left = "0";
        } else {
          wrapper.style.paddingLeft = "18rem";
          topbar.style.left = "18rem";
        }
      }
    });

    // =======================================================================
    // 2. TOAST SYSTEM
    // =======================================================================
    function triggerToast(title, message) {
      const container = document.getElementById("toast-container");
      const toast = document.createElement("div");
      toast.className = "toast-entry pointer-events-auto flex items-center gap-3 p-4 rounded-2xl bg-aurora-card/95 border border-aurora text-white shadow-aurora-md max-w-sm backdrop-blur-xl";
      toast.innerHTML = `
        <div class="w-8 h-8 rounded-xl bg-aurora/20 text-aurora flex items-center justify-center shrink-0 border border-aurora/30">
          <span class="material-symbols-outlined text-lg">verified</span>
        </div>
        <div class="flex flex-col">
          <span class="text-xs font-extrabold text-white">${title}</span>
          <span class="text-[11px] text-[#80a5a0] font-sans">${message}</span>
        </div>
      `;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(12px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }

    // =======================================================================
    // 3. NAVIGATION SWITCHER
    // =======================================================================
    function switchNav(path, label) {
      const nav = document.getElementById("sidebar-nav");
      nav.querySelectorAll("a").forEach(a => {
        if (a.getAttribute("data-path") === path) {
          a.className = "flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-aurora/15 border border-aurora/30 text-aurora font-bold text-sm shadow-aurora-sm transition-all cursor-pointer group";
        } else {
          a.className = "flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[#94a3b8] font-semibold text-sm hover:bg-aurora-container hover:text-white transition-all cursor-pointer group";
        }
      });
      document.getElementById("breadcrumb-current").innerText = label;
      document.getElementById("main-title").innerText = label.includes("Overview") ? "Executive Wealth Overview" : label + " & Valuation Terminal";
      triggerToast("Module Loaded", `Switched view to ${label}.`);
    }

    // =======================================================================
    // 4. CURRENCY CONVERTER
    // =======================================================================
    function setCurrency(curr) {
      currentCurrency = curr;
      ['USD', 'INR', 'EUR', 'GBP'].forEach(c => {
        const btn = document.getElementById(`curr-${c}`);
        if (c === curr) {
          btn.className = "px-2.5 py-1 rounded-lg bg-aurora text-black shadow-aurora-sm transition-all";
        } else {
          btn.className = "px-2.5 py-1 rounded-lg text-[#80a5a0] hover:text-white transition-all";
        }
      });

      const sym = FX_SYMBOLS[curr];
      const rate = FX_RATES[curr];
      
      const totalVal = 14842920.45 * (curr === 'USD' ? 1.0 : rate);
      const unrealVal = 3210480.00 * (curr === 'USD' ? 1.0 : rate);
      const cashVal = 1894200.00 * (curr === 'USD' ? 1.0 : rate);
      const vaultVal = 142850200.00 * (curr === 'USD' ? 1.0 : rate);

      document.getElementById("kpi-total-val").innerText = `${sym}${totalVal.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById("kpi-unrealized-val").innerText = `+${sym}${unrealVal.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById("kpi-cash-val").innerText = `${sym}${cashVal.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById("vault-liquidity-display").innerText = `${sym}${vaultVal.toLocaleString('en-US', {maximumFractionDigits: 0})}`;
      recalcOrderTotal();
      triggerToast("FX Rate Switched", `Portfolio currency redenominated to ${curr} (${sym}).`);
    }

    // =======================================================================
    // 5. TIMEFRAME TRAJECTORY SVG CONTROLLER
    // =======================================================================
    const TIMEFRAME_DATA = {
      '1D': {
        nav: "M 0 170 Q 150 150, 300 130 T 550 90 T 760 35",
        navArea: "M 0 170 Q 150 150, 300 130 T 550 90 T 760 35 L 760 240 L 0 240 Z",
        spx: "M 0 180 Q 180 160, 360 140 T 760 95",
        spxArea: "M 0 180 Q 180 160, 360 140 T 760 95 L 760 240 L 0 240 Z",
        peak: { cx: 760, cy: 35, val: "$14,842,920", label: "Intraday High" },
        axis: ["09:30 AM", "11:00 AM", "01:00 PM", "02:30 PM", "04:00 PM"]
      },
      '1W': {
        nav: "M 0 190 Q 130 170, 260 140 T 520 80 T 760 30",
        navArea: "M 0 190 Q 130 170, 260 140 T 520 80 T 760 30 L 760 240 L 0 240 Z",
        spx: "M 0 200 Q 150 170, 350 130 T 760 70",
        spxArea: "M 0 200 Q 150 170, 350 130 T 760 70 L 760 240 L 0 240 Z",
        peak: { cx: 620, cy: 50, val: "$14,842,920", label: "Weekly Peak" },
        axis: ["Mon", "Tue", "Wed", "Thu", "Fri"]
      },
      '1M': {
        nav: "M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22",
        navArea: "M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22 L 760 240 L 0 240 Z",
        spx: "M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65",
        spxArea: "M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65 L 760 240 L 0 240 Z",
        peak: { cx: 620, cy: 50, val: "$14,842,920", label: "Month Peak" },
        axis: ["Week 1", "Week 2", "Week 3", "Week 4", "Current"]
      },
      '3M': {
        nav: "M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22",
        navArea: "M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22 L 760 240 L 0 240 Z",
        spx: "M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65",
        spxArea: "M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65 L 760 240 L 0 240 Z",
        peak: { cx: 620, cy: 50, val: "$14,842,920", label: "All-Time Peak" },
        axis: ["Nov 01", "Nov 05", "Nov 10", "Nov 15", "Nov 20", "Nov 25", "Today"]
      },
      '1Y': {
        nav: "M 0 220 Q 180 200, 360 120 T 560 60 T 760 18",
        navArea: "M 0 220 Q 180 200, 360 120 T 560 60 T 760 18 L 760 240 L 0 240 Z",
        spx: "M 0 210 Q 180 170, 360 130 T 760 55",
        spxArea: "M 0 210 Q 180 170, 360 130 T 760 55 L 760 240 L 0 240 Z",
        peak: { cx: 700, cy: 30, val: "$14,842,920", label: "52-Week High" },
        axis: ["Q1", "Q2", "Q3", "Q4", "Current"]
      },
      'ALL': {
        nav: "M 0 230 Q 160 210, 320 150 T 520 80 T 760 15",
        navArea: "M 0 230 Q 160 210, 320 150 T 520 80 T 760 15 L 760 240 L 0 240 Z",
        spx: "M 0 220 Q 180 180, 360 130 T 760 50",
        spxArea: "M 0 220 Q 180 180, 360 130 T 760 50 L 760 240 L 0 240 Z",
        peak: { cx: 720, cy: 22, val: "$14,842,920", label: "Inception Peak" },
        axis: ["2022", "2023", "2024", "2025", "2026"]
      }
    };

    function setTimeframe(tf, btn) {
      const container = document.getElementById("timeframe-buttons");
      container.querySelectorAll("button").forEach(b => {
        b.className = "px-3 py-1 rounded-lg text-xs font-bold text-[#80a5a0] hover:text-white transition-colors cursor-pointer";
      });
      btn.className = "px-3 py-1 rounded-lg text-xs font-bold bg-aurora text-black shadow-aurora-sm font-extrabold cursor-pointer";

      const data = TIMEFRAME_DATA[tf] || TIMEFRAME_DATA['3M'];
      document.getElementById("nav-line").setAttribute("d", data.nav);
      document.getElementById("nav-area").setAttribute("d", data.navArea);
      document.getElementById("spx-line").setAttribute("d", data.spx);
      document.getElementById("spx-area").setAttribute("d", data.spxArea);

      document.getElementById("peak-core").setAttribute("cx", data.peak.cx);
      document.getElementById("peak-core").setAttribute("cy", data.peak.cy);
      document.getElementById("peak-ring").setAttribute("cx", data.peak.cx);
      document.getElementById("peak-ring").setAttribute("cy", data.peak.cy);

      document.getElementById("tag-label").innerText = data.peak.label;
      document.getElementById("tag-val").innerText = data.peak.val;

      const axisDiv = document.getElementById("axis-labels");
      axisDiv.innerHTML = data.axis.map(lbl => `<span>${lbl}</span>`).join('');
      triggerToast("Timeframe Shifted", `Valuation window updated to ${tf}.`);
    }

    // =======================================================================
    // 6. DMA ORDER DESK INTERACTIONS
    // =======================================================================
    function setOrderSide(side) {
      currentSide = side;
      const buyBtn = document.getElementById("side-buy-btn");
      const sellBtn = document.getElementById("side-sell-btn");
      const submitText = document.getElementById("order-submit-text");
      const submitBtn = document.getElementById("order-submit-btn");

      if (side === 'BUY') {
        buyBtn.className = "py-1.5 rounded-lg bg-aurora text-black font-extrabold text-xs shadow-aurora-sm transition-all cursor-pointer";
        sellBtn.className = "py-1.5 rounded-lg text-[#80a5a0] hover:text-white font-extrabold text-xs transition-all cursor-pointer";
        submitBtn.className = "w-full py-2.5 rounded-xl bg-gradient-to-r from-aurora via-aurora-bright to-aurora-mint text-black font-extrabold text-xs tracking-wider shadow-aurora-md hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer";
        submitText.innerText = "TRANSMIT DMA ORDER TICKET (BUY)";
      } else {
        sellBtn.className = "py-1.5 rounded-lg bg-aurora-rose text-white font-extrabold text-xs shadow-lg transition-all cursor-pointer";
        buyBtn.className = "py-1.5 rounded-lg text-[#80a5a0] hover:text-white font-extrabold text-xs transition-all cursor-pointer";
        submitBtn.className = "w-full py-2.5 rounded-xl bg-gradient-to-r from-rose-600 to-red-500 text-white font-extrabold text-xs tracking-wider shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer";
        submitText.innerText = "TRANSMIT DMA ORDER TICKET (SELL)";
      }
    }

    function handleTickerSelect(ticker) {
      if (ASSET_PRICES[ticker]) {
        document.getElementById("order-limit").value = ASSET_PRICES[ticker].toFixed(2);
      }
      recalcOrderTotal();
    }

    function setSharesQty(qty) {
      document.getElementById("order-shares").value = qty;
      recalcOrderTotal();
    }

    function recalcOrderTotal() {
      const shares = parseFloat(document.getElementById("order-shares").value) || 0;
      const limit = parseFloat(document.getElementById("order-limit").value) || 0;
      const total = shares * limit;
      const sym = FX_SYMBOLS[currentCurrency];
      document.getElementById("order-est-total").innerText = `${sym}${total.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    }

    function prefillOrder(ticker, price) {
      const select = document.getElementById("order-ticker-select");
      let found = false;
      for (let opt of select.options) {
        if (opt.value === ticker) {
          select.value = ticker;
          found = true;
          break;
        }
      }
      if (!found) {
        const opt = new Option(`${ticker} (${price})`, ticker);
        select.add(opt);
        select.value = ticker;
      }
      document.getElementById("order-limit").value = price.toFixed(2);
      recalcOrderTotal();
      scrollToOrderDesk();
      triggerToast("Asset Queued into Order Desk", `${ticker} prefilled @ ${price.toFixed(2)}.`);
    }

    function scrollToOrderDesk() {
      const card = document.getElementById("order-desk-card");
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      card.classList.add("ring-2", "ring-aurora");
      setTimeout(() => card.classList.remove("ring-2", "ring-aurora"), 1600);
    }

    function transmitOrder() {
      const ticker = document.getElementById("order-ticker-select").value;
      const shares = document.getElementById("order-shares").value;
      const limit = document.getElementById("order-limit").value;
      const orderType = document.getElementById("order-type-select").value;
      const sym = FX_SYMBOLS[currentCurrency];

      triggerToast("DMA Order Executed", `Routed ${currentSide} ${shares} shares of ${ticker} @ ${sym}${limit} (${orderType}) through Node 04.`);
    }

    // =======================================================================
    // 7. TABLE SEARCH & FILTERING
    // =======================================================================
    function filterTable() {
      const query = (document.getElementById("table-search-input").value || "").toLowerCase().trim();
      const market = document.getElementById("market-filter-select").value;
      const sector = document.getElementById("sector-filter-select").value;
      const rows = document.querySelectorAll("#holdings-tbody tr");
      let visibleCount = 0;

      rows.forEach(row => {
        const ticker = (row.getAttribute("data-ticker") || "").toLowerCase();
        const company = (row.getAttribute("data-company") || "").toLowerCase();
        const rowMarket = row.getAttribute("data-market") || "";
        const rowSector = row.getAttribute("data-sector") || "";

        const matchesQuery = !query || ticker.includes(query) || company.includes(query);
        const matchesMarket = market === 'ALL' || rowMarket === market;
        const matchesSector = sector === 'ALL' || rowSector.toLowerCase() === sector.toLowerCase();

        if (matchesQuery && matchesMarket && matchesSector) {
          row.style.display = "";
          visibleCount++;
        } else {
          row.style.display = "none";
        }
      });

      document.getElementById("holdings-count-badge").innerText = `${visibleCount} Core Assets Visible`;
      document.getElementById("footer-count-text").innerText = `Showing ${visibleCount} of 8 active core assets`;
    }

    function handleGlobalSearch(val) {
      document.getElementById("table-search-input").value = val;
      filterTable();
    }

    // =======================================================================
    // 8. CSV EXPORT FUNCTION
    // =======================================================================
    function exportHoldingsCSV() {
      const rows = [
        ["Asset", "Ticker", "Market", "Sector", "Shares Held", "Avg Cost", "Market Price", "Total Market Value", "Day PnL", "Unrealized Gain"],
        ["NVIDIA Corporation", "NVDA", "US Equities", "Technology", "8500", "88.20", "128.40", "1091400.00", "+44450.00 (+4.25%)", "+341700.00 (+45.58%)"],
        ["Reliance Industries Ltd", "RELIANCE.NS", "Indian NSE", "Energy", "125000", "1180.50", "1360.20", "170025000.00", "+328000.00 (+2.14%)", "+22462500.00 (+15.22%)"],
        ["Microsoft Corporation", "MSFT", "US Equities", "Technology", "7200", "382.50", "448.20", "3227040.00", "+57600.00 (+1.82%)", "+473040.00 (+17.18%)"],
        ["Tata Consultancy Services", "TCS.NS", "Indian NSE", "Technology", "85000", "2150.00", "2349.40", "199699000.00", "+142000.00 (+0.84%)", "+16949000.00 (+9.27%)"],
        ["Apple Inc.", "AAPL", "US Equities", "Technology", "12000", "175.40", "224.50", "2694000.00", "+30600.00 (+1.15%)", "+589200.00 (+27.99%)"],
        ["HDFC Bank Ltd", "HDFCBANK.NS", "Indian NSE", "Financials", "190000", "1540.20", "1742.60", "331094000.00", "+420000.00 (+1.45%)", "+38456000.00 (+13.14%)"],
        ["Bitcoin Core Treasury", "BTC-USD", "Crypto", "Financials", "45.0", "51200.00", "63240.00", "2845800.00", "+88200.00 (+3.15%)", "+541800.00 (+23.51%)"],
        ["ASML Holding NV", "ASML", "US Equities", "Semiconductors", "1500", "690.00", "920.00", "1380000.00", "-6250.00 (-0.45%)", "+345000.00 (+33.33%)"]
      ];

      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "Aurora_Prime_Equities_Holdings.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      triggerToast("Holdings Exported", "Downloaded Aurora_Prime_Equities_Holdings.csv.");
    }

    // =======================================================================
    // 9. REAL-TIME TICK SIMULATION
    // =======================================================================
    setInterval(() => {
      const spx = document.getElementById("idx-spx");
      if (spx) {
        const cur = parseFloat(spx.innerText.replace(/,/g, ''));
        const delta = (Math.random() * 0.9 - 0.42);
        spx.innerText = (cur + delta).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
      }
    }, 6000);

    // Initial boot
    window.addEventListener("DOMContentLoaded", () => {
      recalcOrderTotal();
    });
  </script>
</body>
</html>
'''

target_files = [
    r"D:\BDA Project\financial-market-intelligence\04_dashboard\executive_banking_dashboard.html",
    r"D:\BDA Project\financial-market-intelligence\04_dashboard\index.html",
    r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf\executive_banking_dashboard.html",
    r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf\dashboard.html"
]

for tf in target_files:
    os.makedirs(os.path.dirname(tf), exist_ok=True)
    with open(tf, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated Aurora Dashboard at: {tf}")
