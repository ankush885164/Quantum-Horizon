# -*- coding: utf-8 -*-
"""
Build Sovereign Executive Banking & Equities Dashboard
Preserves 100% of the User's HTML, Tailwind config, and typography.
Injects rich interactive client-side logic:
- Order Desk calculations & DMA order execution with animated toast
- Table search & sector filtering
- Interactive timeframe switcher updating the SVG Trajectory Chart
- Currency switcher (USD, EUR, GBP)
- Nav item active states & breadcrumb updates
- Live CSV export of core holdings
"""

import os

html_template = '''<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <meta content="web_dashboard" name="shell-type"/>
  <title>SOVEREIGN — Executive Wealth & Equities Terminal</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
  <style>
    @layer base {
      html, body { margin:0; padding:0; }
      body { overscroll-behavior:none; }
      main > :first-child { margin-top:0 !important; }
      main > :last-child { margin-bottom:0 !important; }
    }
    ::-webkit-scrollbar { display:none; }
    /* Toast animation */
    .toast-anim {
      animation: slideUpFade 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes slideUpFade {
      from { transform: translateY(24px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    .chart-transition {
      transition: d 0.4s ease-in-out;
    }
  </style>
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
  tailwind.config = {
    darkMode: "class",
    theme: {
      extend: {
        "colors": {
          "tertiary-fixed": "#ffdadb",
          "background": "#0d1320",
          "on-tertiary-fixed-variant": "#92002a",
          "primary-container": "#10b981",
          "tertiary-container": "#ff7886",
          "on-tertiary-fixed": "#40000d",
          "on-error-container": "#ffdad6",
          "secondary-fixed-dim": "#4cd7f6",
          "primary": "#4edea3",
          "on-primary": "#003824",
          "on-primary-fixed-variant": "#005236",
          "on-surface-variant": "#bbcabf",
          "secondary-fixed": "#acedff",
          "on-secondary-container": "#00424e",
          "on-primary-container": "#00422b",
          "surface-container": "#1a1f2d",
          "inverse-on-surface": "#2a303f",
          "primary-fixed-dim": "#4edea3",
          "on-secondary": "#003640",
          "surface": "#0d1320",
          "error-container": "#93000a",
          "surface-container-low": "#161b29",
          "outline": "#86948a",
          "on-secondary-fixed-variant": "#004e5c",
          "primary-fixed": "#6ffbbe",
          "error": "#ffb4ab",
          "on-primary-fixed": "#002113",
          "on-surface": "#dde2f5",
          "secondary": "#4cd7f6",
          "surface-tint": "#4edea3",
          "outline-variant": "#3c4a42",
          "tertiary-fixed-dim": "#ffb2b7",
          "surface-container-highest": "#2f3543",
          "inverse-primary": "#006c49",
          "on-error": "#690005",
          "surface-container-high": "#242a38",
          "on-background": "#dde2f5",
          "on-tertiary": "#67001b",
          "surface-bright": "#333948",
          "tertiary": "#ffb2b7",
          "inverse-surface": "#dde2f5",
          "secondary-container": "#03b5d3",
          "surface-container-lowest": "#080e1b",
          "surface-dim": "#0d1320",
          "on-tertiary-container": "#780021",
          "on-secondary-fixed": "#001f26",
          "surface-variant": "#2f3543"
        },
        "borderRadius": {
          "DEFAULT": "0.25rem",
          "lg": "0.5rem",
          "xl": "0.75rem",
          "full": "9999px"
        },
        "spacing": {
          "space-md": "1rem",
          "gutter-sm": "1rem",
          "space-xl": "2.5rem",
          "gutter-lg": "2rem",
          "space-xs": "0.25rem",
          "gutter": "1.5rem",
          "margin-sm": "1rem",
          "margin-lg": "3rem",
          "margin": "2rem",
          "space-lg": "1.5rem",
          "space-sm": "0.5rem"
        },
        "fontFamily": {
          "headline-md": ["Plus Jakarta Sans"],
          "display-lg-mobile": ["Plus Jakarta Sans"],
          "headline-lg": ["Plus Jakarta Sans"],
          "display-md-mobile": ["Plus Jakarta Sans"],
          "label-lg": ["Inter"],
          "label-md": ["Inter"],
          "body-lg": ["Inter"],
          "body-md": ["Inter"],
          "metric-num-md": ["Plus Jakarta Sans"],
          "label-sm": ["Inter"],
          "body-sm": ["Inter"],
          "metric-num-lg": ["Plus Jakarta Sans"],
          "headline-sm": ["Plus Jakarta Sans"],
          "display-lg": ["Plus Jakarta Sans"],
          "display-md": ["Plus Jakarta Sans"]
        },
        "fontSize": {
          "headline-md": ["22px", { "lineHeight": "30px", "letterSpacing": "-0.015em", "fontWeight": "600" }],
          "display-lg-mobile": ["32px", { "lineHeight": "40px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
          "headline-lg": ["28px", { "lineHeight": "36px", "letterSpacing": "-0.02em", "fontWeight": "600" }],
          "display-md-mobile": ["26px", { "lineHeight": "34px", "letterSpacing": "-0.02em", "fontWeight": "600" }],
          "label-lg": ["14px", { "lineHeight": "20px", "letterSpacing": "0.01em", "fontWeight": "500" }],
          "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.02em", "fontWeight": "500" }],
          "body-lg": ["16px", { "lineHeight": "24px", "letterSpacing": "-0.005em", "fontWeight": "400" }],
          "body-md": ["14px", { "lineHeight": "22px", "letterSpacing": "0em", "fontWeight": "400" }],
          "metric-num-md": ["20px", { "lineHeight": "26px", "letterSpacing": "-0.01em", "fontWeight": "600" }],
          "label-sm": ["10px", { "lineHeight": "14px", "letterSpacing": "0.06em", "fontWeight": "600" }],
          "body-sm": ["12px", { "lineHeight": "18px", "letterSpacing": "0.005em", "fontWeight": "400" }],
          "metric-num-lg": ["32px", { "lineHeight": "38px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
          "headline-sm": ["18px", { "lineHeight": "26px", "letterSpacing": "-0.01em", "fontWeight": "600" }],
          "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.03em", "fontWeight": "700" }],
          "display-md": ["36px", { "lineHeight": "44px", "letterSpacing": "-0.025em", "fontWeight": "600" }]
        }
      }
    }
  };
  </script>
</head>
<body class="bg-surface font-body-md text-body-md text-on-surface">

  <!-- =========================================================================
       1. LEFT SIDEBAR NAVIGATION
       ========================================================================= -->
  <aside class="fixed left-0 top-0 h-full w-72 bg-surface-container-lowest z-50 flex flex-col justify-between py-space-lg shadow-[0_1px_8px_rgba(0,0,0,0.04)] border-r border-surface-container">
    <div class="flex flex-col gap-space-lg">
      
      <!-- Brand Logo Header -->
      <div class="px-space-lg flex items-center gap-space-sm cursor-pointer" onclick="switchNav('overview', 'Overview')">
        <img alt="Sovereign Finance Emblem" class="h-8 w-auto object-contain" src="https://lh3.googleusercontent.com/aida/ALJJyrAVZRyCSAbgmf3RxDhkzI-_h-cyizdysCHHHyZ0Ndy-bNYHmQwkbdw6xisp7x3im65su-LBqk7_zfBzEikH_65CPTgmmfHbB_1p8mOwr4iGZXAMqiDeQ90pA_dfA9n5vNEvo21OMzfG8JDqSaFqRkXS0JpFc0IZzqOUOLOmn8Aa-cdKQNZc9czGtf1M3qY7a92GeH-Gp1-uJ4uaqOdDA5SpZiErobnKalUMGirB5Q1A"/>
        <div class="flex flex-col">
          <span class="font-headline-sm text-headline-sm text-on-surface tracking-tight leading-none">SOVEREIGN</span>
          <span class="font-label-sm text-label-sm text-primary tracking-widest uppercase mt-space-xs font-semibold">Executive Wealth</span>
        </div>
      </div>

      <!-- Vault Liquidity Indicator -->
      <div class="px-space-md">
        <div class="p-space-sm rounded-lg bg-surface-container-low flex items-center justify-between border border-surface-container-high/40">
          <div class="flex flex-col">
            <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Vault Liquidity</span>
            <span class="font-metric-num-md text-metric-num-md text-on-surface" id="vault-liquidity-display">$142,850,200</span>
          </div>
          <span class="material-symbols-outlined text-primary text-lg">lock_open</span>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="flex flex-col gap-space-xs px-space-md" id="sidebar-nav">
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer" data-path="overview" onclick="switchNav('overview', 'Overview')">
          <span class="material-symbols-outlined text-xl">dashboard</span>
          <span>Overview</span>
        </a>
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg bg-primary-container text-on-primary-container font-semibold font-label-lg text-label-lg transition-all cursor-pointer" data-path="equities-and-stocks" onclick="switchNav('equities-and-stocks', 'Equities &amp; Stocks')">
          <span class="material-symbols-outlined text-xl">monitoring</span>
          <span>Equities &amp; Stocks</span>
        </a>
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer" data-path="portfolio-analytics" onclick="switchNav('portfolio-analytics', 'Portfolio Analytics')">
          <span class="material-symbols-outlined text-xl">analytics</span>
          <span>Portfolio Analytics</span>
        </a>
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer" data-path="trade-and-orders" onclick="switchNav('trade-and-orders', 'Trade &amp; Orders')">
          <span class="material-symbols-outlined text-xl">sync_alt</span>
          <span>Trade &amp; Orders</span>
        </a>
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer" data-path="treasury" onclick="switchNav('treasury', 'Treasury')">
          <span class="material-symbols-outlined text-xl">account_balance</span>
          <span>Treasury</span>
        </a>
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer" data-path="risk-and-compliance" onclick="switchNav('risk-and-compliance', 'Risk &amp; Compliance')">
          <span class="material-symbols-outlined text-xl">verified_user</span>
          <span>Risk &amp; Compliance</span>
        </a>
        <a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer" data-path="settings" onclick="switchNav('settings', 'Settings')">
          <span class="material-symbols-outlined text-xl">settings</span>
          <span>Settings</span>
        </a>
      </nav>
    </div>

    <!-- Terminal Status Footer -->
    <div class="px-space-md flex flex-col gap-space-sm">
      <div class="p-space-sm rounded-lg bg-surface-container-low flex items-center gap-space-sm border border-surface-container-high/40">
        <div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
        <div class="flex flex-col">
          <span class="font-label-sm text-label-sm text-on-surface font-semibold">Terminal Connected</span>
          <span class="font-label-sm text-label-sm text-on-surface-variant">NY-EQX Node 04 • Fast DMA</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- =========================================================================
       2. TOP BAR & MAIN CONTENT WRAPPER
       ========================================================================= -->
  <div class="pl-72">
    
    <!-- Topbar -->
    <header class="fixed top-0 left-72 right-0 h-16 bg-surface-container-lowest/80 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] border-b border-surface-container z-40 flex items-center justify-between px-space-lg">
      <div class="flex items-center gap-space-lg flex-1 mr-space-lg">
        
        <!-- Market Indices Live Strip -->
        <div class="hidden xl:flex items-center gap-space-md py-space-xs px-space-sm rounded-lg bg-surface-container-low border border-surface-container-high/30">
          <div class="flex items-center gap-space-xs">
            <span class="font-label-sm text-label-sm text-on-surface-variant">S&amp;P 500</span>
            <span class="font-metric-num-md text-label-sm text-on-surface" id="idx-spx">5,234.18</span>
            <span class="font-label-sm text-label-sm text-primary flex items-center">
              <span class="material-symbols-outlined text-xs">arrow_drop_up</span>+0.64%
            </span>
          </div>
          <div class="w-px h-3 bg-surface-container-highest"></div>
          <div class="flex items-center gap-space-xs">
            <span class="font-label-sm text-label-sm text-on-surface-variant">NASDAQ</span>
            <span class="font-metric-num-md text-label-sm text-on-surface" id="idx-ndx">16,428.82</span>
            <span class="font-label-sm text-label-sm text-primary flex items-center">
              <span class="material-symbols-outlined text-xs">arrow_drop_up</span>+0.82%
            </span>
          </div>
          <div class="w-px h-3 bg-surface-container-highest"></div>
          <div class="flex items-center gap-space-xs">
            <span class="font-label-sm text-label-sm text-on-surface-variant">FTSE 100</span>
            <span class="font-metric-num-md text-label-sm text-on-surface" id="idx-ftse">7,930.92</span>
            <span class="font-label-sm text-label-sm text-tertiary flex items-center">
              <span class="material-symbols-outlined text-xs">arrow_drop_down</span>-0.14%
            </span>
          </div>
          <div class="w-px h-3 bg-surface-container-highest"></div>
          <div class="flex items-center gap-space-xs">
            <span class="font-label-sm text-label-sm text-on-surface-variant">US 10Y</span>
            <span class="font-metric-num-md text-label-sm text-on-surface">4.22%</span>
            <span class="font-label-sm text-label-sm text-primary flex items-center">
              <span class="material-symbols-outlined text-xs">arrow_drop_up</span>+0.03
            </span>
          </div>
        </div>

        <!-- Global Search -->
        <div class="relative w-full max-w-xs">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-lg">search</span>
          <input id="global-search" class="w-full pl-9 pr-space-sm py-1.5 rounded-lg bg-surface-container-low text-on-surface placeholder:text-on-surface-variant font-body-sm text-body-sm focus:outline-none focus:bg-surface-container border border-surface-container-high/40" placeholder="Search ticker, ISIN, asset..." type="text" oninput="handleGlobalSearch(this.value)"/>
        </div>
      </div>

      <!-- Currency Toggles & User Profile -->
      <div class="flex items-center gap-space-md">
        
        <!-- Currency Buttons -->
        <div class="flex items-center p-0.5 rounded-lg bg-surface-container-low border border-surface-container-high/30">
          <button id="curr-USD" class="px-space-sm py-1 rounded bg-surface-container text-primary font-label-sm text-label-sm font-semibold transition-all" type="button" onclick="setCurrency('USD')">USD</button>
          <button id="curr-EUR" class="px-space-sm py-1 rounded text-on-surface-variant hover:text-on-surface font-label-sm text-label-sm transition-all" type="button" onclick="setCurrency('EUR')">EUR</button>
          <button id="curr-GBP" class="px-space-sm py-1 rounded text-on-surface-variant hover:text-on-surface font-label-sm text-label-sm transition-all" type="button" onclick="setCurrency('GBP')">GBP</button>
        </div>

        <!-- Notification Bell -->
        <button class="relative p-space-xs rounded-lg text-on-surface-variant hover:text-on-surface hover:bg-surface-container-low transition-colors" type="button" onclick="triggerToast('System Alerts', 'All institutional nodes operating within nominal risk boundaries.')">
          <span class="material-symbols-outlined text-xl">notifications</span>
          <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary animate-ping"></span>
        </button>

        <!-- User Profile -->
        <div class="flex items-center gap-space-sm pl-space-sm">
          <img alt="Profile" class="w-8 h-8 rounded-full object-cover border border-primary/40 shadow-sm" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAMkfFKAZUEDYgJe11J7HueIwZ2YhLOCPGeU_vsQiYJwCzs3IuOFgtOWt1QLCLQbthHNy4gPuiq_sCueOKCGYqt85U_MsTOLTIBe8lSaulH-r-Mg6psxR_Zis2_N8plTVdp5tYwBejpBL4PjHkixReg7vCOQ-rATtxRZZj7HwjHaLI2vTnImghz9erh-d2u7583oGinnYQdPSqdHMvLdq3XV1pAjJ-WCp5B4YE-W8k"/>
          <div class="hidden md:flex flex-col text-left">
            <span class="font-label-md text-label-md text-on-surface font-semibold leading-tight">Lord Alexander Vance</span>
            <span class="font-label-sm text-label-sm text-on-surface-variant leading-tight">Managing Principal</span>
          </div>
        </div>

      </div>
    </header>

    <!-- Main Content Area -->
    <main class="relative pt-16 bg-surface w-full px-space-lg">
      <div class="flex flex-col w-full pb-space-xl">
        
        <!-- TOP BANNER & STATS STRIP -->
        <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-space-lg mb-space-lg pt-6">
          <div class="flex flex-col gap-space-xs">
            <div class="flex items-center gap-space-sm text-on-surface-variant font-label-sm text-label-sm uppercase tracking-widest">
              <span>Portfolio</span>
              <span class="material-symbols-outlined text-xs">chevron_right</span>
              <span class="text-primary font-semibold" id="breadcrumb-current">Equities &amp; Stocks</span>
            </div>
            <div class="flex flex-wrap items-center gap-space-md">
              <h1 class="font-headline-lg text-headline-lg text-on-surface tracking-tight" id="main-view-title">Equities &amp; Market Valuation</h1>
              <div class="flex items-center gap-space-xs px-space-sm py-0.5 rounded-full bg-surface-container-high">
                <span class="w-1.5 h-1.5 rounded-full bg-primary animate-ping"></span>
                <span class="font-label-sm text-label-sm text-primary font-medium">Live Feeds • 15s latency</span>
              </div>
            </div>
          </div>

          <!-- TIMEFRAME SELECTOR & ACTIONS -->
          <div class="flex flex-wrap items-center gap-space-sm">
            <div class="inline-flex p-1 rounded-lg bg-surface-container-low shadow-sm border border-surface-container-high/30" id="timeframe-group">
              <button class="px-space-sm py-1 rounded text-on-surface-variant font-label-sm text-label-sm hover:text-on-surface transition-colors" type="button" onclick="setTimeframe('1D', this)">1D</button>
              <button class="px-space-sm py-1 rounded text-on-surface-variant font-label-sm text-label-sm hover:text-on-surface transition-colors" type="button" onclick="setTimeframe('1W', this)">1W</button>
              <button class="px-space-sm py-1 rounded bg-surface-container text-primary font-label-sm text-label-sm shadow-sm font-semibold" type="button" onclick="setTimeframe('1M', this)">1M</button>
              <button class="px-space-sm py-1 rounded text-on-surface-variant font-label-sm text-label-sm hover:text-on-surface transition-colors" type="button" onclick="setTimeframe('1Y', this)">1Y</button>
              <button class="px-space-sm py-1 rounded text-on-surface-variant font-label-sm text-label-sm hover:text-on-surface transition-colors" type="button" onclick="setTimeframe('YTD', this)">YTD</button>
              <button class="px-space-sm py-1 rounded text-on-surface-variant font-label-sm text-label-sm hover:text-on-surface transition-colors" type="button" onclick="setTimeframe('ALL', this)">ALL</button>
            </div>
            <button class="flex items-center gap-space-xs px-space-md py-2 rounded-lg bg-surface-container-high text-on-surface hover:bg-surface-bright transition-all shadow-sm font-label-md text-label-md" type="button" onclick="exportHoldingsCSV()">
              <span class="material-symbols-outlined text-lg">file_download</span>
              <span>Export</span>
            </button>
            <button class="flex items-center gap-space-xs px-space-md py-2 rounded-lg bg-primary-container text-on-primary-container hover:bg-primary font-label-md text-label-md shadow-md transition-all font-semibold" type="button" onclick="scrollToOrderDesk()">
              <span class="material-symbols-outlined text-lg">add_circle</span>
              <span>Place Order</span>
            </button>
          </div>
        </div>

        <!-- =====================================================================
             3. KPI SUMMARY ROW (4 CARDS)
             ===================================================================== -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-space-md mb-space-lg">
          
          <!-- Card 1: Total Equity Valuation -->
          <div class="relative overflow-hidden rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between border border-surface-container-high/40">
            <div class="absolute -right-4 -top-4 w-24 h-24 bg-primary/10 rounded-full blur-2xl pointer-events-none"></div>
            <div class="flex items-start justify-between">
              <span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Total Portfolio Market Value</span>
              <span class="p-1.5 rounded-lg bg-surface-container-high text-primary material-symbols-outlined text-lg">account_balance_wallet</span>
            </div>
            <div class="mt-space-md">
              <div class="font-metric-num-lg text-metric-num-lg text-on-surface tracking-tight" id="kpi-total-val">$14,842,920.45</div>
              <div class="flex items-center gap-space-xs mt-space-xs">
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-primary bg-primary/10 font-label-sm text-label-sm font-semibold">
                  <span class="material-symbols-outlined text-xs">arrow_drop_up</span>+2.48%
                </span>
                <span class="font-body-sm text-body-sm text-on-surface-variant">+$359,120.00 intraday</span>
              </div>
            </div>
          </div>

          <!-- Card 2: Unrealized Gains/Losses -->
          <div class="relative overflow-hidden rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between border border-surface-container-high/40">
            <div class="absolute -right-4 -top-4 w-24 h-24 bg-primary/10 rounded-full blur-2xl pointer-events-none"></div>
            <div class="flex items-start justify-between">
              <span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Unrealized Capital Gains</span>
              <span class="p-1.5 rounded-lg bg-surface-container-high text-primary material-symbols-outlined text-lg">trending_up</span>
            </div>
            <div class="mt-space-md">
              <div class="font-metric-num-lg text-metric-num-lg text-primary tracking-tight" id="kpi-unrealized-val">+$3,210,480.00</div>
              <div class="flex items-center gap-space-xs mt-space-xs">
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-primary bg-primary/10 font-label-sm text-label-sm font-semibold">
                  <span class="material-symbols-outlined text-xs">north_east</span>+27.64%
                </span>
                <span class="font-body-sm text-body-sm text-on-surface-variant">Cost Basis: $11.63M</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Trading Volume & Liquidity -->
          <div class="relative overflow-hidden rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between border border-surface-container-high/40">
            <div class="flex items-start justify-between">
              <span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Day Executions &amp; Cash Buffer</span>
              <span class="p-1.5 rounded-lg bg-surface-container-high text-secondary material-symbols-outlined text-lg">swap_horiz</span>
            </div>
            <div class="mt-space-md">
              <div class="font-metric-num-lg text-metric-num-lg text-on-surface tracking-tight" id="kpi-cash-val">$1,894,200.00</div>
              <div class="flex items-center justify-between gap-space-xs mt-space-xs">
                <span class="font-body-sm text-body-sm text-on-surface-variant">Liquid Vault Cash:</span>
                <span class="font-label-md text-label-md text-secondary font-semibold">$2,450,000.00</span>
              </div>
            </div>
          </div>

          <!-- Card 4: Beta & Risk Profile -->
          <div class="relative overflow-hidden rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between border border-surface-container-high/40">
            <div class="flex items-start justify-between">
              <span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Risk Profiling &amp; Volatility</span>
              <span class="p-1.5 rounded-lg bg-surface-container-high text-primary material-symbols-outlined text-lg">security</span>
            </div>
            <div class="mt-space-md">
              <div class="flex items-baseline gap-space-xs">
                <span class="font-metric-num-lg text-metric-num-lg text-on-surface tracking-tight">0.94</span>
                <span class="font-label-sm text-label-sm text-on-surface-variant">Beta vs SPX</span>
              </div>
              <div class="flex items-center gap-space-md mt-space-xs">
                <div class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                  <span class="font-label-sm text-label-sm text-on-surface">Low Volatility</span>
                </div>
                <span class="px-2 py-0.5 rounded bg-surface-container font-label-sm text-label-sm text-primary font-bold">ESG: AA</span>
              </div>
            </div>
          </div>

        </div>

        <!-- =====================================================================
             4. MARKET MOVERS TICKER STRIP
             ===================================================================== -->
        <div class="rounded-xl bg-surface-container-low p-space-sm mb-space-lg flex items-center gap-space-md overflow-x-auto shadow-sm border border-surface-container-high/30">
          <div class="flex items-center gap-space-xs px-space-sm py-1 rounded bg-surface-container-high shrink-0">
            <span class="material-symbols-outlined text-primary text-base">bolt</span>
            <span class="font-label-sm text-label-sm text-on-surface font-semibold uppercase tracking-wider">Fast Movers</span>
          </div>
          <div class="flex items-center gap-space-lg shrink-0">
            <div class="flex items-center gap-space-xs cursor-pointer hover:opacity-80 transition-opacity" onclick="prefillOrder('NVDA', 128.40)">
              <span class="font-label-md text-label-md text-on-surface font-semibold">NVDA</span>
              <span class="font-label-sm text-label-sm text-on-surface-variant">$128.40</span>
              <span class="font-label-sm text-label-sm text-primary flex items-center font-medium"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+4.25%</span>
            </div>
            <div class="w-px h-3 bg-surface-container-highest"></div>
            <div class="flex items-center gap-space-xs cursor-pointer hover:opacity-80 transition-opacity" onclick="prefillOrder('MSFT', 448.20)">
              <span class="font-label-md text-label-md text-on-surface font-semibold">MSFT</span>
              <span class="font-label-sm text-label-sm text-on-surface-variant">$448.20</span>
              <span class="font-label-sm text-label-sm text-primary flex items-center font-medium"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+1.82%</span>
            </div>
            <div class="w-px h-3 bg-surface-container-highest"></div>
            <div class="flex items-center gap-space-xs cursor-pointer hover:opacity-80 transition-opacity" onclick="prefillOrder('AMZN', 186.75)">
              <span class="font-label-md text-label-md text-on-surface font-semibold">AMZN</span>
              <span class="font-label-sm text-label-sm text-on-surface-variant">$186.75</span>
              <span class="font-label-sm text-label-sm text-primary flex items-center font-medium"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+2.30%</span>
            </div>
            <div class="w-px h-3 bg-surface-container-highest"></div>
            <div class="flex items-center gap-space-xs cursor-pointer hover:opacity-80 transition-opacity" onclick="prefillOrder('AAPL', 224.50)">
              <span class="font-label-md text-label-md text-on-surface font-semibold">AAPL</span>
              <span class="font-label-sm text-label-sm text-on-surface-variant">$224.50</span>
              <span class="font-label-sm text-label-sm text-primary flex items-center font-medium"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+1.15%</span>
            </div>
            <div class="w-px h-3 bg-surface-container-highest"></div>
            <div class="flex items-center gap-space-xs cursor-pointer hover:opacity-80 transition-opacity" onclick="prefillOrder('ASML', 920.00)">
              <span class="font-label-md text-label-md text-on-surface font-semibold">ASML</span>
              <span class="font-label-sm text-label-sm text-on-surface-variant">$920.00</span>
              <span class="font-label-sm text-label-sm text-tertiary flex items-center font-medium"><span class="material-symbols-outlined text-xs">arrow_drop_down</span>-0.45%</span>
            </div>
            <div class="w-px h-3 bg-surface-container-highest"></div>
            <div class="flex items-center gap-space-xs cursor-pointer hover:opacity-80 transition-opacity" onclick="prefillOrder('JPM', 212.30)">
              <span class="font-label-md text-label-md text-on-surface font-semibold">JPM</span>
              <span class="font-label-sm text-label-sm text-on-surface-variant">$212.30</span>
              <span class="font-label-sm text-label-sm text-primary flex items-center font-medium"><span class="material-symbols-outlined text-xs">arrow_drop_up</span>+0.65%</span>
            </div>
          </div>
        </div>

        <!-- =====================================================================
             5. MID SECTION: VALUATION CHART (70%) & TRADE/ALLOCATION (30%)
             ===================================================================== -->
        <div class="grid grid-cols-1 xl:grid-cols-12 gap-space-lg mb-space-lg">
          
          <!-- Main Interactive Valuation Chart (Col 8 / ~70%) -->
          <div class="xl:col-span-8 rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between border border-surface-container-high/40">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-space-md mb-space-md">
              <div>
                <div class="flex items-center gap-space-xs">
                  <h2 class="font-headline-sm text-headline-sm text-on-surface font-semibold">Holdings Valuation Trajectory</h2>
                  <span class="material-symbols-outlined text-on-surface-variant text-base cursor-pointer hover:text-on-surface" title="Multi-asset marked-to-market performance against benchmark">info</span>
                </div>
                <span class="font-body-sm text-body-sm text-on-surface-variant">Aggregated equity market performance vs benchmark index</span>
              </div>
              <div class="flex items-center gap-space-md">
                <div class="flex items-center gap-space-xs">
                  <span class="w-3 h-3 rounded-full bg-primary"></span>
                  <span class="font-label-sm text-label-sm text-on-surface">Portfolio NAV</span>
                </div>
                <div class="flex items-center gap-space-xs">
                  <span class="w-3 h-3 rounded-full bg-secondary"></span>
                  <span class="font-label-sm text-label-sm text-on-surface-variant">S&amp;P 500 Index</span>
                </div>
                <div class="flex items-center gap-space-xs">
                  <span class="w-3 h-1 bg-surface-variant rounded"></span>
                  <span class="font-label-sm text-label-sm text-on-surface-variant">Cost Basis</span>
                </div>
              </div>
            </div>

            <!-- Area Chart SVG Visual -->
            <div class="relative w-full h-72 sm:h-80 flex flex-col justify-end pt-4">
              <svg id="trajectory-svg" class="w-full h-full overflow-visible" preserveaspectratio="none" viewbox="0 0 760 260">
                <defs>
                  <lineargradient id="primaryNavGrad" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#4edea3" stop-opacity="0.32"></stop>
                    <stop offset="100%" stop-color="#4edea3" stop-opacity="0.0"></stop>
                  </lineargradient>
                  <lineargradient id="spxGrad" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#4cd7f6" stop-opacity="0.18"></stop>
                    <stop offset="100%" stop-color="#4cd7f6" stop-opacity="0.0"></stop>
                  </lineargradient>
                </defs>
                <!-- Faint Gridlines -->
                <line stroke="#242a38" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="20" y2="20"></line>
                <line stroke="#242a38" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="80" y2="80"></line>
                <line stroke="#242a38" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="140" y2="140"></line>
                <line stroke="#242a38" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="760" y1="200" y2="200"></line>
                
                <!-- Benchmark S&P Line (Secondary) -->
                <path id="spx-area" d="M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65 L 760 240 L 0 240 Z" fill="url(#spxGrad)"></path>
                <path id="spx-line" d="M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65" fill="none" stroke="#4cd7f6" stroke-linecap="round" stroke-width="2"></path>
                
                <!-- NAV Primary Area Graph -->
                <path id="nav-area" d="M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22 L 760 240 L 0 240 Z" fill="url(#primaryNavGrad)"></path>
                <path id="nav-line" d="M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22" fill="none" stroke="#4edea3" stroke-linecap="round" stroke-width="3"></path>
                
                <!-- Cost Basis Horizontal Guideline -->
                <line stroke="#3c4a42" stroke-dasharray="6 4" stroke-width="1.5" x1="0" x2="760" y1="170" y2="170"></line>
                
                <!-- Highlight Key Performance Node -->
                <circle id="peak-node-core" class="filter drop-shadow-[0_0_8px_rgba(78,222,163,0.8)]" cx="620" cy="50" fill="#4edea3" r="5"></circle>
                <circle id="peak-node-ring" cx="620" cy="50" fill="#4edea3" fill-opacity="0.25" r="10"></circle>
              </svg>

              <!-- Dynamic Floating Value Tag Over Chart -->
              <div id="floating-tag" class="absolute left-3/4 -top-1 -translate-x-1/2 rounded-lg bg-surface-container-high px-space-sm py-1 shadow-lg pointer-events-none hidden sm:flex flex-col border border-primary/30">
                <span class="font-label-sm text-label-sm text-on-surface-variant" id="tag-label">May 14 Peak</span>
                <span class="font-metric-num-md text-label-md text-primary font-bold" id="tag-val">$14,842,920</span>
              </div>

              <!-- Axis Labels -->
              <div class="flex justify-between items-center text-on-surface-variant font-label-sm text-label-sm pt-space-xs mt-space-xs" id="axis-labels">
                <span>May 01</span>
                <span>May 05</span>
                <span>May 10</span>
                <span>May 15</span>
                <span>May 20</span>
                <span>May 25</span>
                <span>Today (May 29)</span>
              </div>
            </div>

            <!-- Quick Metrics Footer inside chart container -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-space-sm pt-space-md mt-space-md bg-surface-container/50 rounded-lg p-space-sm border border-surface-container-high/30">
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Annualized Alpha</span>
                <p class="font-headline-sm text-headline-sm text-primary">+8.42%</p>
              </div>
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Sharpe Ratio</span>
                <p class="font-headline-sm text-headline-sm text-on-surface">2.41</p>
              </div>
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Tracking Error</span>
                <p class="font-headline-sm text-headline-sm text-on-surface">1.18%</p>
              </div>
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Max Drawdown (1Y)</span>
                <p class="font-headline-sm text-headline-sm text-tertiary">-4.12%</p>
              </div>
            </div>
          </div>

          <!-- Right Column: Sector Allocation & Fast Order Ticket (Col 4 / ~30%) -->
          <div class="xl:col-span-4 flex flex-col gap-space-md">
            
            <!-- Sector Allocation Card -->
            <div class="rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between border border-surface-container-high/40">
              <div class="flex items-center justify-between mb-space-sm">
                <h2 class="font-headline-sm text-headline-sm text-on-surface">Sector Weighting</h2>
                <span class="font-label-sm text-label-sm text-primary font-semibold">100% Capitalized</span>
              </div>
              <div class="flex flex-col gap-space-sm my-space-xs">
                <!-- Technology -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between items-center font-label-md text-label-md">
                    <span class="text-on-surface flex items-center gap-space-xs">
                      <span class="w-2.5 h-2.5 rounded-sm bg-primary"></span>Technology
                    </span>
                    <span class="text-on-surface font-semibold">42.0% <span class="text-on-surface-variant font-normal">($6.23M)</span></span>
                  </div>
                  <div class="w-full bg-surface-container-high rounded-full h-1.5 overflow-hidden">
                    <div class="bg-primary h-full rounded-full" style="width: 42%;"></div>
                  </div>
                </div>
                <!-- Healthcare -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between items-center font-label-md text-label-md">
                    <span class="text-on-surface flex items-center gap-space-xs">
                      <span class="w-2.5 h-2.5 rounded-sm bg-secondary"></span>Healthcare
                    </span>
                    <span class="text-on-surface font-semibold">18.0% <span class="text-on-surface-variant font-normal">($2.67M)</span></span>
                  </div>
                  <div class="w-full bg-surface-container-high rounded-full h-1.5 overflow-hidden">
                    <div class="bg-secondary h-full rounded-full" style="width: 18%;"></div>
                  </div>
                </div>
                <!-- Financials -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between items-center font-label-md text-label-md">
                    <span class="text-on-surface flex items-center gap-space-xs">
                      <span class="w-2.5 h-2.5 rounded-sm bg-primary-fixed"></span>Financials
                    </span>
                    <span class="text-on-surface font-semibold">15.0% <span class="text-on-surface-variant font-normal">($2.22M)</span></span>
                  </div>
                  <div class="w-full bg-surface-container-high rounded-full h-1.5 overflow-hidden">
                    <div class="bg-primary-fixed h-full rounded-full" style="width: 15%;"></div>
                  </div>
                </div>
                <!-- Industrials -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between items-center font-label-md text-label-md">
                    <span class="text-on-surface flex items-center gap-space-xs">
                      <span class="w-2.5 h-2.5 rounded-sm bg-secondary-fixed-dim"></span>Industrials &amp; Semi
                    </span>
                    <span class="text-on-surface font-semibold">13.0% <span class="text-on-surface-variant font-normal">($1.92M)</span></span>
                  </div>
                  <div class="w-full bg-surface-container-high rounded-full h-1.5 overflow-hidden">
                    <div class="bg-secondary-fixed-dim h-full rounded-full" style="width: 13%;"></div>
                  </div>
                </div>
                <!-- Energy & Commodities -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between items-center font-label-md text-label-md">
                    <span class="text-on-surface flex items-center gap-space-xs">
                      <span class="w-2.5 h-2.5 rounded-sm bg-surface-bright"></span>Energy &amp; Infrastructure
                    </span>
                    <span class="text-on-surface font-semibold">12.0% <span class="text-on-surface-variant font-normal">($1.78M)</span></span>
                  </div>
                  <div class="w-full bg-surface-container-high rounded-full h-1.5 overflow-hidden">
                    <div class="bg-surface-bright h-full rounded-full" style="width: 12%;"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Trade Execution Ticket Widget -->
            <div id="order-desk-card" class="rounded-xl bg-surface-container-low p-space-lg shadow-md flex flex-col justify-between flex-1 border border-surface-container-high/40">
              <div class="flex items-center justify-between mb-space-sm">
                <div class="flex items-center gap-space-xs">
                  <span class="material-symbols-outlined text-primary text-xl">bolt</span>
                  <h2 class="font-headline-sm text-headline-sm text-on-surface">Institutional Order Desk</h2>
                </div>
                <span class="px-2 py-0.5 rounded text-primary bg-primary/10 font-label-sm text-label-sm font-semibold">DMA Direct</span>
              </div>
              <div class="flex flex-col gap-space-sm">
                
                <!-- Buy/Sell Toggle -->
                <div class="grid grid-cols-2 p-1 rounded-lg bg-surface-container-high">
                  <button id="side-buy-btn" class="py-1 rounded bg-primary-container text-on-primary-container font-label-md text-label-md font-semibold text-center transition-all cursor-pointer" type="button" onclick="setOrderSide('BUY')">BUY (LONG)</button>
                  <button id="side-sell-btn" class="py-1 rounded text-on-surface-variant hover:text-on-surface font-label-md text-label-md font-medium text-center transition-all cursor-pointer" type="button" onclick="setOrderSide('SELL')">SELL (SHORT)</button>
                </div>

                <!-- Ticker & Order Type Inputs -->
                <div class="grid grid-cols-2 gap-space-sm">
                  <div>
                    <label class="block font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant mb-1">Ticker / ISIN</label>
                    <div class="relative">
                      <input id="order-ticker" class="w-full py-1.5 px-space-sm rounded-lg bg-surface-container text-on-surface font-label-md text-label-md uppercase font-semibold focus:outline-none focus:bg-surface-container-highest border border-surface-container-high/40" type="text" value="NVDA" onchange="autoFillPrice(this.value)"/>
                    </div>
                  </div>
                  <div>
                    <label class="block font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant mb-1">Execution</label>
                    <select id="order-exec-type" class="w-full py-1.5 px-space-sm rounded-lg bg-surface-container text-on-surface font-label-md text-label-md focus:outline-none focus:bg-surface-container-highest border border-surface-container-high/40">
                      <option value="Limit">Limit Order</option>
                      <option value="Market">Market</option>
                      <option value="Stop-Loss">Stop-Loss</option>
                    </select>
                  </div>
                </div>

                <!-- Quantity & Limit Price -->
                <div class="grid grid-cols-2 gap-space-sm">
                  <div>
                    <label class="block font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant mb-1">Shares Count</label>
                    <input id="order-shares" class="w-full py-1.5 px-space-sm rounded-lg bg-surface-container text-on-surface font-label-md text-label-md focus:outline-none focus:bg-surface-container-highest border border-surface-container-high/40" type="number" value="500" min="1" oninput="recalcOrderTotal()"/>
                  </div>
                  <div>
                    <label class="block font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant mb-1">Limit (USD)</label>
                    <input id="order-limit" class="w-full py-1.5 px-space-sm rounded-lg bg-surface-container text-on-surface font-label-md text-label-md focus:outline-none focus:bg-surface-container-highest border border-surface-container-high/40" type="number" step="0.05" value="128.00" oninput="recalcOrderTotal()"/>
                  </div>
                </div>

                <!-- Quick Quantity Pills -->
                <div class="grid grid-cols-4 gap-1">
                  <button class="py-0.5 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm text-center transition-colors" type="button" onclick="setSharesPct(250)">250</button>
                  <button class="py-0.5 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm text-center transition-colors" type="button" onclick="setSharesPct(500)">500</button>
                  <button class="py-0.5 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm text-center transition-colors" type="button" onclick="setSharesPct(1000)">1,000</button>
                  <button class="py-0.5 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm text-center transition-colors" type="button" onclick="setSharesPct(2500)">2,500</button>
                </div>

                <!-- Estimated Total Settlement -->
                <div class="p-space-sm rounded-lg bg-surface-container flex items-center justify-between border border-surface-container-high/30">
                  <span class="font-label-sm text-label-sm text-on-surface-variant">Est. Principal Settlement:</span>
                  <span class="font-label-md text-label-md text-primary font-bold" id="order-est-total">$64,000.00</span>
                </div>

                <!-- Execute Button -->
                <button class="w-full py-2.5 rounded-lg bg-primary-container text-on-primary-container hover:bg-primary font-label-md text-label-md font-bold tracking-wide shadow-md transition-all flex items-center justify-center gap-space-xs mt-space-xs cursor-pointer" type="button" onclick="transmitOrder()">
                  <span class="material-symbols-outlined text-base">send</span>
                  <span id="order-submit-text">TRANSMIT ORDER TICKET</span>
                </button>
              </div>
            </div>

          </div>

        </div>

        <!-- =====================================================================
             6. COMPREHENSIVE EQUITIES & HOLDINGS DATA GRID
             ===================================================================== -->
        <div class="rounded-xl bg-surface-container-low shadow-md overflow-hidden flex flex-col border border-surface-container-high/40">
          
          <!-- Grid Control Bar -->
          <div class="p-space-lg flex flex-col md:flex-row md:items-center justify-between gap-space-md border-b border-surface-container">
            <div class="flex items-center gap-space-md">
              <h2 class="font-headline-sm text-headline-sm text-on-surface font-semibold">Institutional Holdings &amp; Positions</h2>
              <span class="px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm" id="holdings-count-badge">7 Active Core Holdings</span>
            </div>
            <div class="flex flex-wrap items-center gap-space-sm">
              <!-- Search Ticker -->
              <div class="relative">
                <span class="material-symbols-outlined absolute left-2.5 top-1/2 -translate-y-1/2 text-on-surface-variant text-base">search</span>
                <input id="holdings-search-input" class="pl-8 pr-space-sm py-1.5 rounded-lg bg-surface-container text-on-surface placeholder:text-on-surface-variant font-body-sm text-body-sm focus:outline-none focus:bg-surface-container-high w-48 sm:w-64 border border-surface-container-high/30" placeholder="Filter company, ticker..." type="text" oninput="filterTable()"/>
              </div>
              <!-- Filter Sector -->
              <select id="sector-select" class="px-space-sm py-1.5 rounded-lg bg-surface-container text-on-surface font-label-sm text-label-sm focus:outline-none border border-surface-container-high/30" onchange="filterTable()">
                <option value="ALL">All Sectors</option>
                <option value="Technology">Technology</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Financials">Financials</option>
                <option value="Semiconductors">Semiconductors</option>
              </select>
              <!-- Column Settings -->
              <button class="p-1.5 rounded-lg bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high transition-colors" type="button" title="Table Columns Preferences" onclick="triggerToast('Table Preferences', 'Displaying all 9 institutional audit columns.')">
                <span class="material-symbols-outlined text-lg">tune</span>
              </button>
            </div>
          </div>

          <!-- Data Table Container -->
          <div class="overflow-x-auto w-full">
            <table class="w-full text-left" id="holdings-table">
              <thead>
                <tr class="bg-surface-container-high/60 text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">
                  <th class="py-space-sm px-space-md font-semibold">Asset &amp; Ticker</th>
                  <th class="py-space-sm px-space-md font-semibold text-right">Shares Held</th>
                  <th class="py-space-sm px-space-md font-semibold text-right">Avg Purchase</th>
                  <th class="py-space-sm px-space-md font-semibold text-right">Market Price</th>
                  <th class="py-space-sm px-space-md font-semibold text-right">Total Market Value</th>
                  <th class="py-space-sm px-space-md font-semibold text-right">Day PnL ($ / %)</th>
                  <th class="py-space-sm px-space-md font-semibold text-right">Unrealized Gain</th>
                  <th class="py-space-sm px-space-md font-semibold text-center">7D Performance</th>
                  <th class="py-space-sm px-space-md font-semibold text-center">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y-0" id="holdings-tbody">
                
                <!-- NVDA -->
                <tr class="hover:bg-surface-container-high/40 transition-colors" data-ticker="NVDA" data-company="NVIDIA Corporation" data-sector="Technology">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-primary font-bold font-headline-sm text-headline-sm border border-primary/20">
                        NV
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">NVIDIA Corporation</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">NVDA</span>
                          <span class="text-on-surface-variant text-xs">• Mega-Cap Tech</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">8,500</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$88.20</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$128.40</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$1,091,400.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$44,450.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+4.25%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$341,700.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+45.58%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 25 L 20 22 L 40 18 L 60 20 L 80 10 L 100 4" stroke="#4edea3" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade NVDA" type="button" onclick="prefillOrder('NVDA', 128.40)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'NVDA alert threshold set at $130.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- MSFT -->
                <tr class="hover:bg-surface-container-high/40 transition-colors bg-surface-container/20" data-ticker="MSFT" data-company="Microsoft Corporation" data-sector="Technology">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-secondary font-bold font-headline-sm text-headline-sm border border-secondary/20">
                        MS
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">Microsoft Corporation</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">MSFT</span>
                          <span class="text-on-surface-variant text-xs">• Enterprise Software</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">7,200</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$382.50</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$448.20</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$3,227,040.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$57,600.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+1.82%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$473,040.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+17.18%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 20 L 25 18 L 45 15 L 70 12 L 100 5" stroke="#4edea3" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade MSFT" type="button" onclick="prefillOrder('MSFT', 448.20)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'MSFT alert threshold set at $450.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- AAPL -->
                <tr class="hover:bg-surface-container-high/40 transition-colors" data-ticker="AAPL" data-company="Apple Inc." data-sector="Technology">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-on-surface font-bold font-headline-sm text-headline-sm border border-surface-container-highest">
                        AP
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">Apple Inc.</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">AAPL</span>
                          <span class="text-on-surface-variant text-xs">• Consumer Hardware</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">12,000</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$175.40</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$224.50</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$2,694,000.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$30,600.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+1.15%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$589,200.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+27.99%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 15 L 20 18 L 40 12 L 65 14 L 100 8" stroke="#4edea3" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade AAPL" type="button" onclick="prefillOrder('AAPL', 224.50)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'AAPL alert threshold set at $230.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- JPM -->
                <tr class="hover:bg-surface-container-high/40 transition-colors bg-surface-container/20" data-ticker="JPM" data-company="JPMorgan Chase & Co" data-sector="Financials">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-primary-fixed font-bold font-headline-sm text-headline-sm border border-primary-fixed/20">
                        JP
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">JPMorgan Chase &amp; Co</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">JPM</span>
                          <span class="text-on-surface-variant text-xs">• Investment Banking</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">9,100</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$164.80</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$212.30</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$1,931,930.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$12,450.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+0.65%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$432,250.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+28.82%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 22 L 30 18 L 60 19 L 80 14 L 100 10" stroke="#4edea3" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade JPM" type="button" onclick="prefillOrder('JPM', 212.30)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'JPM alert threshold set at $215.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- GOOGL -->
                <tr class="hover:bg-surface-container-high/40 transition-colors" data-ticker="GOOGL" data-company="Alphabet Inc. Class A" data-sector="Technology">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-secondary-fixed font-bold font-headline-sm text-headline-sm border border-secondary-fixed/20">
                        GO
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">Alphabet Inc. Class A</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">GOOGL</span>
                          <span class="text-on-surface-variant text-xs">• Search &amp; AI Infra</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">8,000</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$142.10</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$179.80</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$1,438,400.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$13,100.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+0.92%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$301,600.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+26.53%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 18 L 30 16 L 50 20 L 75 12 L 100 7" stroke="#4edea3" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade GOOGL" type="button" onclick="prefillOrder('GOOGL', 179.80)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'GOOGL alert threshold set at $185.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- AMZN -->
                <tr class="hover:bg-surface-container-high/40 transition-colors bg-surface-container/20" data-ticker="AMZN" data-company="Amazon.com Inc." data-sector="Technology">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-primary font-bold font-headline-sm text-headline-sm border border-primary/20">
                        AZ
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">Amazon.com Inc.</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">AMZN</span>
                          <span class="text-on-surface-variant text-xs">• Cloud &amp; Retail</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">6,400</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$135.00</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$186.75</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$1,195,200.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$26,880.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+2.30%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$331,200.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+38.33%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 25 L 30 20 L 50 15 L 75 14 L 100 6" stroke="#4edea3" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade AMZN" type="button" onclick="prefillOrder('AMZN', 186.75)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'AMZN alert threshold set at $190.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- ASML -->
                <tr class="hover:bg-surface-container-high/40 transition-colors" data-ticker="ASML" data-company="ASML Holding NV" data-sector="Semiconductors">
                  <td class="py-space-md px-space-md">
                    <div class="flex items-center gap-space-sm">
                      <div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-tertiary font-bold font-headline-sm text-headline-sm border border-tertiary/20">
                        AS
                      </div>
                      <div class="flex flex-col">
                        <span class="font-label-md text-label-md text-on-surface font-semibold">ASML Holding NV</span>
                        <div class="flex items-center gap-space-xs">
                          <span class="font-label-sm text-label-sm text-primary font-bold">ASML</span>
                          <span class="text-on-surface-variant text-xs">• Lithography Systems</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface">1,500</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface-variant">$690.00</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-semibold">$920.00</td>
                  <td class="py-space-md px-space-md text-right font-metric-num-md text-label-md text-on-surface font-bold">$1,380,000.00</td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-tertiary font-semibold">-$6,250.00</span>
                      <span class="font-label-sm text-label-sm text-tertiary">-0.45%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-right">
                    <div class="flex flex-col items-end">
                      <span class="font-label-md text-label-md text-primary font-semibold">+$345,000.00</span>
                      <span class="font-label-sm text-label-sm text-primary">+33.33%</span>
                    </div>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <svg class="w-24 h-7 mx-auto" fill="none" viewbox="0 0 100 30">
                      <path d="M 0 8 L 25 10 L 50 15 L 75 14 L 100 22" stroke="#ffb2b7" stroke-linecap="round" stroke-width="2"></path>
                    </svg>
                  </td>
                  <td class="py-space-md px-space-md text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Trade ASML" type="button" onclick="prefillOrder('ASML', 920.00)">
                        <span class="material-symbols-outlined text-base">swap_horiz</span>
                      </button>
                      <button class="p-1 rounded bg-surface-container hover:bg-surface-bright text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Alert" type="button" onclick="triggerToast('Price Alert Set', 'ASML alert threshold set at $900.00')">
                        <span class="material-symbols-outlined text-base">notifications_active</span>
                      </button>
                    </div>
                  </td>
                </tr>

              </tbody>
            </table>
          </div>

          <!-- Table Pagination & Aggregate Summary Footer -->
          <div class="p-space-md bg-surface-container flex flex-col sm:flex-row sm:items-center justify-between gap-space-md border-t border-surface-container-high/40">
            <div class="flex items-center gap-space-xs font-body-sm text-body-sm text-on-surface-variant">
              <span id="footer-count-text">Showing 1 to 7 of 7 holdings</span>
              <span>•</span>
              <span>Aggregated Val: <span class="text-on-surface font-semibold" id="table-agg-val">$12,957,970.00</span> in direct equities</span>
            </div>
            <div class="flex items-center gap-space-xs">
              <button class="px-3 py-1 rounded bg-surface-container-high text-on-surface-variant hover:text-on-surface font-label-sm text-label-sm disabled:opacity-50 cursor-pointer" type="button" onclick="triggerToast('Pagination', 'Displaying page 1 of institutional equities register.')">Previous</button>
              <button class="px-2.5 py-1 rounded bg-primary-container text-on-primary-container font-label-sm text-label-sm font-bold cursor-pointer" type="button">1</button>
              <button class="px-3 py-1 rounded bg-surface-container-high text-on-surface-variant hover:text-on-surface font-label-sm text-label-sm cursor-pointer" type="button" onclick="triggerToast('Pagination', 'No additional pages in active portfolio mandate.')">Next</button>
            </div>
          </div>

        </div>

      </div>
    </main>
  </div>

  <!-- =========================================================================
       7. INSTITUTIONAL NOTIFICATION TOAST
       ========================================================================= -->
  <div id="toast-container" class="fixed bottom-6 right-6 z-50 pointer-events-none flex flex-col gap-2"></div>

  <!-- =========================================================================
       8. JAVASCRIPT: DYNAMIC CONTROLS & REAL-TIME INTERACTION
       ========================================================================= -->
  <script>
    // Asset reference prices
    const ASSET_PRICES = {
      "NVDA": 128.40,
      "MSFT": 448.20,
      "AAPL": 224.50,
      "JPM": 212.30,
      "GOOGL": 179.80,
      "AMZN": 186.75,
      "ASML": 920.00,
      "RELIANCE": 1360.20,
      "TCS": 2349.40,
      "HDFCBANK": 1742.60
    };

    let currentSide = "BUY";
    let currentCurrency = "USD";
    const FX_RATES = { "USD": 1.0, "EUR": 0.92, "GBP": 0.79 };
    const FX_SYMS = { "USD": "$", "EUR": "€", "GBP": "£" };

    // Toast Generator
    function triggerToast(title, message) {
      const container = document.getElementById("toast-container");
      const toast = document.createElement("div");
      toast.className = "toast-anim pointer-events-auto flex items-center gap-3 p-4 rounded-xl bg-surface-container-high border border-primary/30 shadow-2xl text-on-surface max-w-sm";
      toast.innerHTML = `
        <div class="w-8 h-8 rounded-lg bg-primary-container/20 text-primary flex items-center justify-center shrink-0">
          <span class="material-symbols-outlined text-lg">verified</span>
        </div>
        <div class="flex flex-col">
          <span class="font-label-md text-label-md font-semibold text-on-surface">${title}</span>
          <span class="font-body-sm text-body-sm text-on-surface-variant">${message}</span>
        </div>
      `;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }

    // Navigation Switcher
    function switchNav(path, label) {
      const nav = document.getElementById("sidebar-nav");
      nav.querySelectorAll("a").forEach(a => {
        if (a.getAttribute("data-path") === path) {
          a.className = "flex items-center gap-space-sm px-space-md py-space-sm rounded-lg bg-primary-container text-on-primary-container font-semibold font-label-lg text-label-lg transition-all cursor-pointer";
        } else {
          a.className = "flex items-center gap-space-sm px-space-md py-space-sm rounded-lg text-on-surface-variant font-label-lg text-label-lg hover:bg-surface-container-high hover:text-on-surface transition-all cursor-pointer";
        }
      });
      document.getElementById("breadcrumb-current").innerHTML = label;
      document.getElementById("main-view-title").innerHTML = label === 'Overview' ? 'Executive Wealth Overview' : label + ' &amp; Market Valuation';
      triggerToast('Module Activated', `Switched to ${label} module.`);
    }

    // Currency Switcher
    function setCurrency(curr) {
      currentCurrency = curr;
      ['USD', 'EUR', 'GBP'].forEach(c => {
        const btn = document.getElementById(`curr-${c}`);
        if (c === curr) {
          btn.className = "px-space-sm py-1 rounded bg-surface-container text-primary font-label-sm text-label-sm font-semibold transition-all";
        } else {
          btn.className = "px-space-sm py-1 rounded text-on-surface-variant hover:text-on-surface font-label-sm text-label-sm transition-all";
        }
      });
      const sym = FX_SYMS[curr];
      const rate = FX_RATES[curr];
      
      const totalVal = 14842920.45 * rate;
      const unrealVal = 3210480.00 * rate;
      const cashVal = 1894200.00 * rate;
      const vaultVal = 142850200.00 * rate;

      document.getElementById("kpi-total-val").innerText = `${sym}${totalVal.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById("kpi-unrealized-val").innerText = `+${sym}${unrealVal.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById("kpi-cash-val").innerText = `${sym}${cashVal.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById("vault-liquidity-display").innerText = `${sym}${vaultVal.toLocaleString('en-US', {maximumFractionDigits: 0})}`;
      recalcOrderTotal();
      triggerToast('FX Currency Switched', `Active valuation denomination: ${curr} (${sym})`);
    }

    // Timeframe chart dataset simulation
    const TIMEFRAME_PATHS = {
      '1D': {
        nav: "M 0 160 Q 150 140, 300 130 T 550 90 T 760 40",
        navArea: "M 0 160 Q 150 140, 300 130 T 550 90 T 760 40 L 760 240 L 0 240 Z",
        spx: "M 0 180 Q 180 160, 360 140 T 760 100",
        spxArea: "M 0 180 Q 180 160, 360 140 T 760 100 L 760 240 L 0 240 Z",
        tag: { label: "1D High", val: "$14,842,920", cx: 760, cy: 40 },
        axis: ["09:30 AM", "11:00 AM", "01:00 PM", "02:30 PM", "04:00 PM"]
      },
      '1W': {
        nav: "M 0 190 Q 130 180, 260 140 T 520 80 T 760 30",
        navArea: "M 0 190 Q 130 180, 260 140 T 520 80 T 760 30 L 760 240 L 0 240 Z",
        spx: "M 0 200 Q 150 170, 350 130 T 760 70",
        spxArea: "M 0 200 Q 150 170, 350 130 T 760 70 L 760 240 L 0 240 Z",
        tag: { label: "Weekly Peak", val: "$14,842,920", cx: 620, cy: 50 },
        axis: ["Mon", "Tue", "Wed", "Thu", "Fri"]
      },
      '1M': {
        nav: "M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22",
        navArea: "M 0 210 Q 130 195, 230 145 T 440 90 T 620 50 T 760 22 L 760 240 L 0 240 Z",
        spx: "M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65",
        spxArea: "M 0 190 Q 120 180, 220 150 T 420 110 T 600 95 T 760 65 L 760 240 L 0 240 Z",
        tag: { label: "May 14 Peak", val: "$14,842,920", cx: 620, cy: 50 },
        axis: ["May 01", "May 05", "May 10", "May 15", "May 20", "May 25", "Today (May 29)"]
      },
      '1Y': {
        nav: "M 0 220 Q 180 200, 360 120 T 560 60 T 760 18",
        navArea: "M 0 220 Q 180 200, 360 120 T 560 60 T 760 18 L 760 240 L 0 240 Z",
        spx: "M 0 210 Q 180 170, 360 130 T 760 55",
        spxArea: "M 0 210 Q 180 170, 360 130 T 760 55 L 760 240 L 0 240 Z",
        tag: { label: "52-Week High", val: "$14,842,920", cx: 700, cy: 30 },
        axis: ["Q1", "Q2", "Q3", "Q4", "Current"]
      },
      'YTD': {
        nav: "M 0 200 Q 150 185, 320 130 T 540 70 T 760 22",
        navArea: "M 0 200 Q 150 185, 320 130 T 540 70 T 760 22 L 760 240 L 0 240 Z",
        spx: "M 0 190 Q 160 160, 340 120 T 760 60",
        spxArea: "M 0 190 Q 160 160, 340 120 T 760 60 L 760 240 L 0 240 Z",
        tag: { label: "YTD Performance +27.6%", val: "$14,842,920", cx: 620, cy: 50 },
        axis: ["Jan", "Feb", "Mar", "Apr", "May"]
      },
      'ALL': {
        nav: "M 0 230 Q 160 210, 320 150 T 520 80 T 760 15",
        navArea: "M 0 230 Q 160 210, 320 150 T 520 80 T 760 15 L 760 240 L 0 240 Z",
        spx: "M 0 220 Q 180 180, 360 130 T 760 50",
        spxArea: "M 0 220 Q 180 180, 360 130 T 760 50 L 760 240 L 0 240 Z",
        tag: { label: "All-Time High", val: "$14,842,920", cx: 720, cy: 22 },
        axis: ["2022", "2023", "2024", "2025", "2026"]
      }
    };

    function setTimeframe(tf, btn) {
      const group = document.getElementById("timeframe-group");
      group.querySelectorAll("button").forEach(b => {
        b.className = "px-space-sm py-1 rounded text-on-surface-variant font-label-sm text-label-sm hover:text-on-surface transition-colors cursor-pointer";
      });
      btn.className = "px-space-sm py-1 rounded bg-surface-container text-primary font-label-sm text-label-sm shadow-sm font-semibold cursor-pointer";

      const data = TIMEFRAME_PATHS[tf] || TIMEFRAME_PATHS['1M'];
      document.getElementById("nav-line").setAttribute("d", data.nav);
      document.getElementById("nav-area").setAttribute("d", data.navArea);
      document.getElementById("spx-line").setAttribute("d", data.spx);
      document.getElementById("spx-area").setAttribute("d", data.spxArea);

      document.getElementById("peak-node-core").setAttribute("cx", data.tag.cx);
      document.getElementById("peak-node-core").setAttribute("cy", data.tag.cy);
      document.getElementById("peak-node-ring").setAttribute("cx", data.tag.cx);
      document.getElementById("peak-node-ring").setAttribute("cy", data.tag.cy);

      document.getElementById("tag-label").innerText = data.tag.label;
      document.getElementById("tag-val").innerText = data.tag.val;

      const axisDiv = document.getElementById("axis-labels");
      axisDiv.innerHTML = data.axis.map(lbl => `<span>${lbl}</span>`).join('');
      triggerToast('Timeframe Updated', `Chart window switched to ${tf}.`);
    }

    // Order Desk Interactions
    function setOrderSide(side) {
      currentSide = side;
      const buyBtn = document.getElementById("side-buy-btn");
      const sellBtn = document.getElementById("side-sell-btn");
      if (side === 'BUY') {
        buyBtn.className = "py-1 rounded bg-primary-container text-on-primary-container font-label-md text-label-md font-semibold text-center transition-all cursor-pointer";
        sellBtn.className = "py-1 rounded text-on-surface-variant hover:text-on-surface font-label-md text-label-md font-medium text-center transition-all cursor-pointer";
        document.getElementById("order-submit-text").innerText = "TRANSMIT ORDER TICKET (BUY)";
      } else {
        sellBtn.className = "py-1 rounded bg-rose-600 text-white font-label-md text-label-md font-semibold text-center transition-all cursor-pointer";
        buyBtn.className = "py-1 rounded text-on-surface-variant hover:text-on-surface font-label-md text-label-md font-medium text-center transition-all cursor-pointer";
        document.getElementById("order-submit-text").innerText = "TRANSMIT ORDER TICKET (SELL)";
      }
    }

    function autoFillPrice(ticker) {
      const sym = ticker.toUpperCase().trim();
      if (ASSET_PRICES[sym]) {
        document.getElementById("order-limit").value = ASSET_PRICES[sym].toFixed(2);
      }
      recalcOrderTotal();
    }

    function setSharesPct(qty) {
      document.getElementById("order-shares").value = qty;
      recalcOrderTotal();
    }

    function recalcOrderTotal() {
      const shares = parseFloat(document.getElementById("order-shares").value) || 0;
      const limit = parseFloat(document.getElementById("order-limit").value) || 0;
      const total = shares * limit;
      const sym = FX_SYMS[currentCurrency];
      document.getElementById("order-est-total").innerText = `${sym}${total.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    }

    function prefillOrder(ticker, price) {
      document.getElementById("order-ticker").value = ticker;
      document.getElementById("order-limit").value = price.toFixed(2);
      recalcOrderTotal();
      scrollToOrderDesk();
      triggerToast("Asset Selected", `${ticker} pre-loaded into Order Desk @ $${price.toFixed(2)}.`);
    }

    function scrollToOrderDesk() {
      const card = document.getElementById("order-desk-card");
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      card.classList.add("ring-2", "ring-primary");
      setTimeout(() => card.classList.remove("ring-2", "ring-primary"), 1500);
    }

    function transmitOrder() {
      const ticker = document.getElementById("order-ticker").value.toUpperCase();
      const shares = document.getElementById("order-shares").value;
      const limit = document.getElementById("order-limit").value;
      const orderType = document.getElementById("order-exec-type").value;
      const sym = FX_SYMS[currentCurrency];
      
      triggerToast("DMA Order Routed", `Executing ${currentSide} ${shares} shares of ${ticker} @ ${sym}${limit} (${orderType}) via Node 04.`);
    }

    // Table Filter & Search
    function filterTable() {
      const query = (document.getElementById("holdings-search-input").value || "").toLowerCase().trim();
      const sector = document.getElementById("sector-select").value;
      const rows = document.querySelectorAll("#holdings-tbody tr");
      let visibleCount = 0;

      rows.forEach(row => {
        const ticker = (row.getAttribute("data-ticker") || "").toLowerCase();
        const company = (row.getAttribute("data-company") || "").toLowerCase();
        const rowSector = row.getAttribute("data-sector") || "";

        const matchesQuery = !query || ticker.includes(query) || company.includes(query);
        const matchesSector = sector === 'ALL' || rowSector.toLowerCase() === sector.toLowerCase();

        if (matchesQuery && matchesSector) {
          row.style.display = "";
          visibleCount++;
        } else {
          row.style.display = "none";
        }
      });

      document.getElementById("holdings-count-badge").innerText = `${visibleCount} Holdings Visible`;
      document.getElementById("footer-count-text").innerText = `Showing 1 to ${visibleCount} of 7 holdings`;
    }

    function handleGlobalSearch(val) {
      document.getElementById("holdings-search-input").value = val;
      filterTable();
    }

    // Export Table CSV
    function exportHoldingsCSV() {
      const rows = [
        ["Asset", "Ticker", "Sector", "Shares Held", "Avg Purchase Price", "Market Price", "Total Market Value", "Day PnL", "Unrealized Gain"],
        ["NVIDIA Corporation", "NVDA", "Technology", "8500", "88.20", "128.40", "1091400.00", "+44450.00 (+4.25%)", "+341700.00 (+45.58%)"],
        ["Microsoft Corporation", "MSFT", "Technology", "7200", "382.50", "448.20", "3227040.00", "+57600.00 (+1.82%)", "+473040.00 (+17.18%)"],
        ["Apple Inc.", "AAPL", "Technology", "12000", "175.40", "224.50", "2694000.00", "+30600.00 (+1.15%)", "+589200.00 (+27.99%)"],
        ["JPMorgan Chase & Co", "JPM", "Financials", "9100", "164.80", "212.30", "1931930.00", "+12450.00 (+0.65%)", "+432250.00 (+28.82%)"],
        ["Alphabet Inc. Class A", "GOOGL", "Technology", "8000", "142.10", "179.80", "1438400.00", "+13100.00 (+0.92%)", "+301600.00 (+26.53%)"],
        ["Amazon.com Inc.", "AMZN", "Technology", "6400", "135.00", "186.75", "1195200.00", "+26880.00 (+2.30%)", "+331200.00 (+38.33%)"],
        ["ASML Holding NV", "ASML", "Semiconductors", "1500", "690.00", "920.00", "1380000.00", "-6250.00 (-0.45%)", "+345000.00 (+33.33%)"]
      ];

      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "Sovereign_Institutional_Equities_Holdings.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      triggerToast("Holdings Exported", "Downloaded Sovereign_Institutional_Equities_Holdings.csv.");
    }

    // Live Tick Pulse Simulation
    setInterval(() => {
      const spxEl = document.getElementById("idx-spx");
      if (spxEl) {
        const cur = parseFloat(spxEl.innerText.replace(/,/g, ''));
        const delta = (Math.random() * 0.8 - 0.38);
        const next = cur + delta;
        spxEl.innerText = next.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
      }
    }, 8000);

    // Initial setup on load
    window.addEventListener("DOMContentLoaded", () => {
      recalcOrderTotal();
    });
  </script>
</body>
</html>
'''

target_paths = [
    r"D:\BDA Project\financial-market-intelligence\04_dashboard\executive_banking_dashboard.html",
    r"D:\BDA Project\financial-market-intelligence\04_dashboard\index.html",
    r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf\executive_banking_dashboard.html",
    r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf\dashboard.html"
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Successfully written to: {p}")
