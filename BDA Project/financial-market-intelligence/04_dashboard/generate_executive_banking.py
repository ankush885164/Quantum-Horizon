"""
Generate High-Fidelity Desktop Executive Banking & Equities Dashboard
Theme: Dark Obsidian (#080e1b, #0d1320), Emerald (#10b981) accents, Plus Jakarta Sans
"""

import os
import json

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APEX Institutional — Executive Banking & Equities Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-darkest: #050912;
      --bg-obsidian: #080e1b;
      --bg-surface: #0d1320;
      --bg-card: #111827;
      --bg-card-hover: #162032;
      --border: #1a2333;
      --border-subtle: #141c2a;
      --border-highlight: rgba(16, 185, 129, 0.35);
      
      --emerald: #10b981;
      --emerald-glow: rgba(16, 185, 129, 0.22);
      --emerald-subtle: rgba(16, 185, 129, 0.1);
      --emerald-light: #34d399;
      
      --rose: #f43f5e;
      --rose-subtle: rgba(244, 63, 94, 0.12);
      --amber: #f59e0b;
      --amber-subtle: rgba(245, 158, 11, 0.12);
      --sky: #38bdf8;
      --sky-subtle: rgba(56, 189, 248, 0.12);
      
      --text: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      
      --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-obsidian);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      overflow-x: hidden;
      font-size: 13px;
    }

    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-obsidian); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--emerald); }

    /* =========================================================================
       1. LEFT SIDEBAR NAVIGATION
       ========================================================================= */
    .sidebar {
      width: 260px;
      background-color: var(--bg-surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      z-index: 100;
      padding: 1.5rem 1.25rem;
    }

    .brand-box {
      display: flex;
      align-items: center;
      gap: 12px;
      padding-bottom: 1.4rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 1.4rem;
    }

    .brand-logo {
      width: 36px;
      height: 36px;
      border-radius: 9px;
      background: linear-gradient(135deg, #059669, #10b981);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 1.15rem;
      font-weight: 800;
      box-shadow: 0 0 16px var(--emerald-glow);
    }

    .brand-text h2 {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #fff;
    }

    .brand-text p {
      font-size: 0.68rem;
      color: var(--emerald);
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    /* Liquidity Indicator Widget in Sidebar */
    .liquidity-badge {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.9rem 1rem;
      margin-bottom: 1.5rem;
      position: relative;
      overflow: hidden;
    }

    .liquidity-badge::before {
      content: '';
      position: absolute;
      top: 0; left: 0; width: 3px; height: 100%;
      background: var(--emerald);
    }

    .liquidity-label {
      font-size: 0.68rem;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .liquidity-val {
      font-family: var(--font-mono);
      font-size: 1.25rem;
      font-weight: 700;
      color: #fff;
      margin-top: 3px;
    }

    .liquidity-status {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.7rem;
      color: var(--emerald);
      font-weight: 600;
      margin-top: 4px;
    }

    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 8px var(--emerald);
      animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
      0% { transform: scale(0.9); opacity: 0.8; }
      50% { transform: scale(1.3); opacity: 1; }
      100% { transform: scale(0.9); opacity: 0.8; }
    }

    /* Nav Links */
    .nav-menu {
      display: flex;
      flex-direction: column;
      gap: 5px;
      flex: 1;
    }

    .nav-category {
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      font-weight: 700;
      margin: 0.8rem 0 0.35rem 0.5rem;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 0.65rem 0.9rem;
      border-radius: 8px;
      color: var(--text-secondary);
      font-weight: 600;
      font-size: 0.82rem;
      text-decoration: none;
      transition: all 0.15s ease;
      cursor: pointer;
    }

    .nav-link:hover {
      background: var(--bg-card);
      color: #fff;
    }

    .nav-link.active {
      background: var(--emerald-subtle);
      color: var(--emerald);
      border-left: 3px solid var(--emerald);
      border-radius: 0 8px 8px 0;
      font-weight: 700;
    }

    .nav-link svg {
      width: 17px;
      height: 17px;
      stroke-width: 2;
    }

    /* User Profile in Sidebar Footer */
    .user-footer {
      padding-top: 1.2rem;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .user-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, #1e293b, #334155);
      border: 1px solid var(--emerald);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
      color: #fff;
    }

    .user-info h4 {
      font-size: 0.8rem;
      font-weight: 700;
      color: #fff;
    }

    .user-info p {
      font-size: 0.68rem;
      color: var(--text-muted);
    }

    /* =========================================================================
       2. TOP BAR & MAIN VIEW WRAPPER
       ========================================================================= */
    .main-wrapper {
      margin-left: 260px;
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
    }

    .topbar {
      height: 60px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2rem;
      position: sticky;
      top: 0;
      z-index: 90;
      backdrop-filter: blur(8px);
    }

    /* Ticker Tape */
    .ticker-tape {
      display: flex;
      align-items: center;
      gap: 18px;
      font-size: 0.74rem;
      font-family: var(--font-mono);
      overflow-x: auto;
    }

    .ticker-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .ticker-name {
      color: var(--text-muted);
      font-weight: 600;
    }

    .ticker-val {
      color: #fff;
      font-weight: 600;
    }

    .ticker-up {
      color: var(--emerald);
    }

    .ticker-down {
      color: var(--rose);
    }

    .topbar-actions {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    /* Search Bar in Topbar */
    .search-box {
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.4rem 0.85rem;
      width: 250px;
      color: var(--text-secondary);
    }

    .search-box input {
      background: transparent;
      border: none;
      outline: none;
      color: #fff;
      font-size: 0.78rem;
      font-family: var(--font-sans);
      width: 100%;
    }

    .search-box kbd {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      font-size: 0.65rem;
      padding: 2px 5px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    /* Currency Toggle */
    .currency-toggle {
      display: flex;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 2px;
    }

    .currency-btn {
      padding: 4px 10px;
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      border: none;
      background: transparent;
      cursor: pointer;
      border-radius: 5px;
      transition: all 0.15s;
    }

    .currency-btn.active {
      background: var(--emerald);
      color: #fff;
    }

    /* Content Canvas */
    .content-area {
      padding: 1.75rem 2rem 3.5rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    /* =========================================================================
       3. TOP 4 KPI STAT CARDS
       ========================================================================= */
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1.25rem;
    }

    .stat-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem 1.4rem;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 120px;
      transition: border-color 0.2s, transform 0.2s;
    }

    .stat-card:hover {
      border-color: var(--border-highlight);
      transform: translateY(-2px);
    }

    .stat-card::after {
      content: '';
      position: absolute;
      top: 0; right: 0; width: 80px; height: 80px;
      background: radial-gradient(circle, var(--emerald-glow) 0%, transparent 70%);
      pointer-events: none;
    }

    .stat-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .stat-title {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 700;
    }

    .stat-icon {
      width: 28px;
      height: 28px;
      border-radius: 7px;
      background: var(--emerald-subtle);
      color: var(--emerald);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .stat-val {
      font-family: var(--font-mono);
      font-size: 1.8rem;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.03em;
      margin: 0.35rem 0;
    }

    .stat-delta {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 0.74rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
      width: fit-content;
    }

    .delta-green {
      color: var(--emerald);
      background: var(--emerald-subtle);
    }

    .delta-blue {
      color: var(--sky);
      background: var(--sky-subtle);
    }

    .delta-amber {
      color: var(--amber);
      background: var(--amber-subtle);
    }

    /* =========================================================================
       4. MID SECTION: VALUATION AREA CHART & ORDER DESK
       ========================================================================= */
    .mid-row {
      display: grid;
      grid-template-columns: 1.8fr 1.2fr;
      gap: 1.25rem;
    }

    .card-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.4rem 1.6rem;
      display: flex;
      flex-direction: column;
    }

    .panel-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1rem;
    }

    .panel-heading h3 {
      font-size: 1rem;
      font-weight: 700;
      color: #fff;
    }

    .panel-heading p {
      font-size: 0.74rem;
      color: var(--text-muted);
    }

    /* Timeframe Filter Buttons */
    .time-pills {
      display: flex;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 2px;
      gap: 2px;
    }

    .time-btn {
      padding: 4px 10px;
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      border: none;
      background: transparent;
      cursor: pointer;
      border-radius: 6px;
      transition: all 0.15s;
    }

    .time-btn.active {
      background: var(--emerald);
      color: #fff;
    }

    /* Quantitative Metrics Strip under Chart */
    .quant-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
    }

    .quant-box {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
    }

    .quant-name {
      font-size: 0.68rem;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
    }

    .quant-num {
      font-family: var(--font-mono);
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
      margin-top: 2px;
    }

    /* Right Section: Sector Weighting & Order Desk */
    .right-stack {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    /* Sector Breakdown */
    .sector-progress-list {
      display: flex;
      flex-direction: column;
      gap: 9px;
      margin-top: 0.5rem;
    }

    .sector-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .sector-labels {
      display: flex;
      justify-content: space-between;
      font-size: 0.76rem;
    }

    .sector-bar-bg {
      height: 6px;
      background: var(--bg-card);
      border-radius: 3px;
      overflow: hidden;
    }

    .sector-bar-fill {
      height: 100%;
      border-radius: 3px;
    }

    /* Order Desk Widget */
    .order-desk {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem 1.4rem;
    }

    .order-toggle {
      display: grid;
      grid-template-columns: 1fr 1fr;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 3px;
      margin-bottom: 1rem;
    }

    .toggle-side-btn {
      padding: 6px;
      text-align: center;
      font-size: 0.78rem;
      font-weight: 800;
      border-radius: 6px;
      cursor: pointer;
      border: none;
      background: transparent;
      color: var(--text-muted);
      transition: all 0.15s;
    }

    .toggle-side-btn.active-buy {
      background: var(--emerald);
      color: #fff;
    }

    .toggle-side-btn.active-sell {
      background: var(--rose);
      color: #fff;
    }

    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 0.85rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .form-label {
      font-size: 0.68rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-muted);
    }

    .form-input, .form-select {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.5rem 0.75rem;
      color: #fff;
      font-size: 0.8rem;
      font-family: var(--font-mono);
      outline: none;
    }

    .form-input:focus, .form-select:focus {
      border-color: var(--emerald);
    }

    .pct-pills {
      display: flex;
      gap: 6px;
      margin-bottom: 0.85rem;
    }

    .pct-pill {
      flex: 1;
      padding: 3px;
      font-size: 0.68rem;
      font-weight: 700;
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
    }

    .pct-pill:hover {
      border-color: var(--emerald);
      color: #fff;
    }

    .order-summary {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.6rem 0.85rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.85rem;
      font-size: 0.75rem;
    }

    .order-submit-btn {
      width: 100%;
      padding: 0.7rem;
      border-radius: 8px;
      border: none;
      background: var(--emerald);
      color: #fff;
      font-weight: 800;
      font-size: 0.85rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: opacity 0.15s;
    }

    .order-submit-btn:hover {
      opacity: 0.9;
    }

    /* =========================================================================
       5. TABLE: INSTITUTIONAL HOLDINGS & POSITIONS
       ========================================================================= */
    .table-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.4rem 1.6rem;
    }

    .table-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.1rem;
      flex-wrap: wrap;
      gap: 12px;
    }

    .table-filters {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .table-search {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.45rem 0.85rem;
      color: #fff;
      font-size: 0.78rem;
      outline: none;
      width: 220px;
    }

    .table-select {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.45rem 0.85rem;
      color: #fff;
      font-size: 0.78rem;
      outline: none;
    }

    .data-table-wrap {
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--bg-card);
    }

    .exec-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }

    .exec-table th {
      background: var(--bg-surface);
      padding: 0.8rem 1rem;
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
      font-weight: 700;
    }

    .exec-table td {
      padding: 0.85rem 1rem;
      border-bottom: 1px solid var(--border-subtle);
      font-family: var(--font-mono);
      font-size: 0.82rem;
    }

    .exec-table tr:hover td {
      background: var(--bg-card-hover);
    }

    .asset-cell {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .asset-icon {
      width: 28px;
      height: 28px;
      border-radius: 7px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.72rem;
      color: #fff;
    }

    .asset-info {
      display: flex;
      flex-direction: column;
    }

    .asset-ticker {
      font-weight: 800;
      color: #fff;
      font-family: var(--font-mono);
    }

    .asset-name {
      font-size: 0.7rem;
      color: var(--text-muted);
      font-family: var(--font-sans);
    }

    .sector-badge {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 0.68rem;
      font-weight: 700;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      color: var(--text-secondary);
      font-family: var(--font-sans);
    }

    .sparkline-svg {
      width: 90px;
      height: 24px;
    }

    /* Table Pagination */
    .table-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 1rem;
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    .pagination-btns {
      display: flex;
      gap: 6px;
    }

    .page-btn {
      padding: 4px 10px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      cursor: pointer;
      font-size: 0.72rem;
      font-weight: 700;
    }

    .page-btn.active {
      background: var(--emerald);
      border-color: var(--emerald);
      color: #fff;
    }

    /* Notification Toast */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-surface);
      border: 1px solid var(--emerald);
      border-radius: 10px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      z-index: 1000;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s ease;
      pointer-events: none;
    }

    .toast.show {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
  </style>
</head>
<body>

  <!-- =========================================================================
       1. LEFT SIDEBAR NAVIGATION
       ========================================================================= -->
  <aside class="sidebar">
    
    <!-- Branding -->
    <div class="brand-box">
      <div class="brand-logo">▲</div>
      <div class="brand-text">
        <h2>APEX CAPITAL</h2>
        <p>Institutional Banking</p>
      </div>
    </div>

    <!-- Total Liquidity Indicator Widget -->
    <div class="liquidity-badge">
      <div class="liquidity-label">Total Liquidity Pool</div>
      <div class="liquidity-val" id="sidebar-liquidity">$142.85M</div>
      <div class="liquidity-status">
        <span class="pulse-dot"></span> Tier-1 Prime Settlement
      </div>
    </div>

    <!-- Navigation Links -->
    <nav class="nav-menu">
      <div class="nav-category">Core Banking</div>
      <a class="nav-link active" onclick="setNav(this, 'Overview')">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        Overview
      </a>
      <a class="nav-link" onclick="setNav(this, 'Equities & Stocks')">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
        Equities & Stocks
      </a>
      <a class="nav-link" onclick="setNav(this, 'Portfolio Analytics')">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
        Portfolio Analytics
      </a>

      <div class="nav-category">Execution & Treasury</div>
      <a class="nav-link" onclick="setNav(this, 'Trade & Orders')">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
        Trade & Orders
      </a>
      <a class="nav-link" onclick="setNav(this, 'Treasury')">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        Treasury
      </a>
      <a class="nav-link" onclick="setNav(this, 'Risk & Compliance')">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
        Risk & Compliance
      </a>
    </nav>

    <!-- User Profile Footer -->
    <div class="user-footer">
      <div class="user-avatar">AC</div>
      <div class="user-info">
        <h4>Alexander Vance</h4>
        <p>Chief Investment Officer</p>
      </div>
    </div>

  </aside>

  <!-- =========================================================================
       2. TOP BAR & MAIN VIEW WRAPPER
       ========================================================================= -->
  <div class="main-wrapper">
    
    <!-- Top Navigation Bar with Market Ticker -->
    <header class="topbar">
      
      <!-- Real-Time Market Indices Ticker Tape -->
      <div class="ticker-tape">
        <div class="ticker-item">
          <span class="ticker-name">S&P 500</span>
          <span class="ticker-val">5,917.11</span>
          <span class="ticker-up">+0.58%</span>
        </div>
        <span style="color:var(--border);">|</span>
        <div class="ticker-item">
          <span class="ticker-name">NASDAQ</span>
          <span class="ticker-val">19,081.47</span>
          <span class="ticker-up">+0.82%</span>
        </div>
        <span style="color:var(--border);">|</span>
        <div class="ticker-item">
          <span class="ticker-name">FTSE 100</span>
          <span class="ticker-val">8,109.32</span>
          <span class="ticker-down">-0.14%</span>
        </div>
        <span style="color:var(--border);">|</span>
        <div class="ticker-item">
          <span class="ticker-name">NIFTY 50</span>
          <span class="ticker-val">23,518.50</span>
          <span class="ticker-up">+1.04%</span>
        </div>
        <span style="color:var(--border);">|</span>
        <div class="ticker-item">
          <span class="ticker-name">USD/INR</span>
          <span class="ticker-val">84.42</span>
          <span class="ticker-up">+0.05%</span>
        </div>
      </div>

      <!-- Actions: Search, Currency Toggle, User Profile -->
      <div class="topbar-actions">
        
        <!-- Global Search -->
        <div class="search-box">
          <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input type="text" placeholder="Global search positions, orders...">
          <kbd>⌘K</kbd>
        </div>

        <!-- Currency Toggles -->
        <div class="currency-toggle">
          <button class="currency-btn active" onclick="setCurrency('USD')">USD</button>
          <button class="currency-btn" onclick="setCurrency('INR')">INR</button>
          <button class="currency-btn" onclick="setCurrency('EUR')">EUR</button>
          <button class="currency-btn" onclick="setCurrency('GBP')">GBP</button>
        </div>

        <!-- Notification Bell -->
        <button class="btn" style="padding: 6px 10px;" title="System Alerts">
          <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
        </button>

      </div>

    </header>

    <!-- Main Content Canvas -->
    <main class="content-area">
      
      <!-- =====================================================================
           3. TOP 4 KPI CARDS
           ===================================================================== -->
      <section class="kpi-row">
        
        <!-- Card 1: Total Portfolio Value -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Total Portfolio Value</span>
            <div class="stat-icon">
              <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
          </div>
          <div class="stat-val" id="kpi-total-val">$14.84M</div>
          <div class="stat-delta delta-green">
            ▲ +$182.4K (+1.24%) Intraday
          </div>
        </div>

        <!-- Card 2: Unrealized Capital Gains -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Unrealized Capital Gains</span>
            <div class="stat-icon" style="background: var(--emerald-subtle); color: var(--emerald);">
              <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
            </div>
          </div>
          <div class="stat-val" id="kpi-unrealized-val">+$3.22M</div>
          <div class="stat-delta delta-green">
            ▲ +27.6% Inception ROI
          </div>
        </div>

        <!-- Card 3: Day Cash Buffer -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Day Cash Buffer</span>
            <div class="stat-icon" style="background: var(--sky-subtle); color: var(--sky);">
              <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>
            </div>
          </div>
          <div class="stat-val" id="kpi-cash-buffer">$1.89M</div>
          <div class="stat-delta delta-blue">
            12.8% Unencumbered Cash
          </div>
        </div>

        <!-- Card 4: Risk Profiling -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Risk Profiling</span>
            <div class="stat-icon" style="background: var(--amber-subtle); color: var(--amber);">
              <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
            </div>
          </div>
          <div class="stat-val">Beta 0.94</div>
          <div class="stat-delta delta-amber">
            Defensive • VaR (95%): $240K
          </div>
        </div>

      </section>

      <!-- =====================================================================
           4. MID SECTION: VALUATION AREA CHART & ORDER DESK
           ===================================================================== -->
      <section class="mid-row">
        
        <!-- Left: Holdings Valuation Trajectory Area Chart -->
        <div class="card-panel">
          <div class="panel-header">
            <div class="panel-heading">
              <h3>Holdings Valuation Trajectory</h3>
              <p>Historical portfolio NAV, alpha accretion, and benchmarks</p>
            </div>

            <!-- Timeframe Filter Pills -->
            <div class="time-pills">
              <button class="time-btn" onclick="setTimeframe('1D', this)">1D</button>
              <button class="time-btn" onclick="setTimeframe('1W', this)">1W</button>
              <button class="time-btn" onclick="setTimeframe('1M', this)">1M</button>
              <button class="time-btn active" onclick="setTimeframe('3M', this)">3M</button>
              <button class="time-btn" onclick="setTimeframe('1Y', this)">1Y</button>
              <button class="time-btn" onclick="setTimeframe('ALL', this)">ALL</button>
            </div>
          </div>

          <!-- Interactive SVG Area Chart Canvas -->
          <div id="chart-container" style="width: 100%; height: 260px;">
            <svg id="trajectory-chart" width="100%" height="260" preserveAspectRatio="none" style="overflow: visible;"></svg>
          </div>

          <!-- Key Quantitative Metrics Strip -->
          <div class="quant-strip">
            <div class="quant-box">
              <div class="quant-name">Alpha vs SPX</div>
              <div class="quant-num" style="color: var(--emerald);">+4.82%</div>
            </div>
            <div class="quant-box">
              <div class="quant-name">Sharpe Ratio</div>
              <div class="quant-num">2.41</div>
            </div>
            <div class="quant-box">
              <div class="quant-name">Tracking Error</div>
              <div class="quant-num">1.85%</div>
            </div>
            <div class="quant-box">
              <div class="quant-name">Max Drawdown</div>
              <div class="quant-num" style="color: var(--rose);">-6.14%</div>
            </div>
          </div>

        </div>

        <!-- Right Stack: Sector Weighting & Institutional Order Desk -->
        <div class="right-stack">
          
          <!-- Sector Weighting Breakdown -->
          <div class="card-panel" style="padding: 1.25rem 1.4rem;">
            <div class="panel-header" style="margin-bottom: 0.6rem;">
              <div class="panel-heading">
                <h3 style="font-size: 0.92rem;">Sector Allocation Weighting</h3>
                <p>Concentration risk analysis vs mandate limits</p>
              </div>
            </div>

            <div class="sector-progress-list">
              <div class="sector-row">
                <div class="sector-labels">
                  <span style="font-weight: 600;">Technology (IT & Semis)</span>
                  <span style="font-family: var(--font-mono); font-weight: 700; color: #38bdf8;">38.4%</span>
                </div>
                <div class="sector-bar-bg"><div class="sector-bar-fill" style="width: 38.4%; background: #38bdf8;"></div></div>
              </div>

              <div class="sector-row">
                <div class="sector-labels">
                  <span style="font-weight: 600;">Financial Services & Banking</span>
                  <span style="font-family: var(--font-mono); font-weight: 700; color: #10b981;">24.2%</span>
                </div>
                <div class="sector-bar-bg"><div class="sector-bar-fill" style="width: 24.2%; background: #10b981;"></div></div>
              </div>

              <div class="sector-row">
                <div class="sector-labels">
                  <span style="font-weight: 600;">Energy & Conglomerate</span>
                  <span style="font-family: var(--font-mono); font-weight: 700; color: #f59e0b;">16.8%</span>
                </div>
                <div class="sector-bar-bg"><div class="sector-bar-fill" style="width: 16.8%; background: #f59e0b;"></div></div>
              </div>

              <div class="sector-row">
                <div class="sector-labels">
                  <span style="font-weight: 600;">Utilities & Infrastructure</span>
                  <span style="font-family: var(--font-mono); font-weight: 700; color: #a855f7;">11.5%</span>
                </div>
                <div class="sector-bar-bg"><div class="sector-bar-fill" style="width: 11.5%; background: #a855f7;"></div></div>
              </div>

              <div class="sector-row">
                <div class="sector-labels">
                  <span style="font-weight: 600;">Consumer Defensive</span>
                  <span style="font-family: var(--font-mono); font-weight: 700; color: #94a3b8;">9.1%</span>
                </div>
                <div class="sector-bar-bg"><div class="sector-bar-fill" style="width: 9.1%; background: #94a3b8;"></div></div>
              </div>
            </div>

          </div>

          <!-- Institutional Order Desk Widget -->
          <div class="order-desk">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
              <h3 style="font-size: 0.92rem; font-weight: 800; color: #fff;">Institutional Order Desk</h3>
              <span style="font-size: 0.68rem; color: var(--emerald); font-weight: 700; font-family: var(--font-mono);">DMA DIRECT</span>
            </div>

            <!-- Buy / Sell Pill Toggle -->
            <div class="order-toggle">
              <button class="toggle-side-btn active-buy" id="btn-side-buy" onclick="setOrderSide('BUY')">BUY (LONG)</button>
              <button class="toggle-side-btn" id="btn-side-sell" onclick="setOrderSide('SELL')">SELL (SHORT)</button>
            </div>

            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Instrument / Ticker</label>
                <select class="form-select" id="order-ticker" onchange="updateOrderEst()">
                  <option value="RELIANCE">RELIANCE (₹1,360)</option>
                  <option value="TCS">TCS (₹2,349)</option>
                  <option value="HDFCBANK">HDFCBANK (₹1,740)</option>
                  <option value="NVDA">NVDA ($151)</option>
                  <option value="AAPL">AAPL ($352)</option>
                  <option value="BTC-USD">BTC-USD ($63,240)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Order Type</label>
                <select class="form-select" id="order-type">
                  <option value="LIMIT">Limit Order</option>
                  <option value="MARKET">Market Execution</option>
                  <option value="STOP_LIMIT">Stop Limit</option>
                </select>
              </div>
            </div>

            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Shares Quantity</label>
                <input type="number" class="form-input" id="order-qty" value="1500" min="1" oninput="updateOrderEst()">
              </div>

              <div class="form-group">
                <label class="form-label">Limit Price ($ / ₹)</label>
                <input type="number" class="form-input" id="order-price" value="1360.20" step="0.1" oninput="updateOrderEst()">
              </div>
            </div>

            <!-- Quick % Quantity Pills -->
            <div class="pct-pills">
              <div class="pct-pill" onclick="setQtyPct(0.25)">25%</div>
              <div class="pct-pill" onclick="setQtyPct(0.50)">50%</div>
              <div class="pct-pill" onclick="setQtyPct(0.75)">75%</div>
              <div class="pct-pill" onclick="setQtyPct(1.00)">100% (Max)</div>
            </div>

            <div class="order-summary">
              <span style="color: var(--text-muted);">Est. Consideration:</span>
              <span style="font-family: var(--font-mono); font-weight: 800; color: #fff;" id="order-est-val">$24,480.00</span>
            </div>

            <button class="order-submit-btn" id="btn-transmit-order" onclick="transmitOrder()">
              <span>⚡</span> Transmit Institutional Order
            </button>

          </div>

        </div>

      </section>

      <!-- =====================================================================
           5. DATA TABLE: INSTITUTIONAL HOLDINGS & POSITIONS
           ===================================================================== -->
      <section class="table-panel">
        
        <div class="table-toolbar">
          <div class="panel-heading">
            <h3>Institutional Holdings & Equities Positions</h3>
            <p>Live marked-to-market valuations, 7-day volatility sparklines, and cost bases</p>
          </div>

          <div class="table-filters">
            <input type="text" class="table-search" id="holdings-search" placeholder="Filter positions..." onkeyup="filterHoldings()">
            <select class="table-select" id="sector-filter" onchange="filterHoldings()">
              <option value="ALL">All Sectors</option>
              <option value="Technology">Technology</option>
              <option value="Financials">Financial Services</option>
              <option value="Energy">Energy</option>
              <option value="Utilities">Utilities</option>
            </select>
          </div>
        </div>

        <div class="data-table-wrap">
          <table class="exec-table" id="holdings-table">
            <thead>
              <tr>
                <th>Asset / Enterprise</th>
                <th>Sector</th>
                <th>Shares Held</th>
                <th>Avg Purchase</th>
                <th>Live Price</th>
                <th>Total Value</th>
                <th>Daily P&L</th>
                <th>Unrealized Gain</th>
                <th>7-Day Trend</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="holdings-tbody"></tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="table-footer">
          <span id="pagination-info">Showing 1 to 6 of 6 active positions</span>
          <div class="pagination-btns">
            <button class="page-btn">‹ Prev</button>
            <button class="page-btn active">1</button>
            <button class="page-btn">2</button>
            <button class="page-btn">Next ›</button>
          </div>
        </div>

      </section>

    </main>

  </div>

  <!-- Notification Toast -->
  <div class="toast" id="exec-toast">
    <div style="font-size: 1.2rem;">✅</div>
    <div>
      <div style="font-weight: 700; color: #fff; font-size: 0.82rem;" id="toast-title">Order Transmitted</div>
      <div style="color: var(--text-muted); font-size: 0.72rem;" id="toast-msg">Routed to Primary Exchange</div>
    </div>
  </div>

  <!-- =========================================================================
       6. INTERACTIVE DASHBOARD JAVASCRIPT
       ========================================================================= -->
  <script>
    // Holdings Master Data
    const HOLDINGS = [
      {
        ticker: "RELIANCE",
        name: "Reliance Industries Ltd",
        sector: "Energy",
        shares: 125000,
        avgPrice: 1180.50,
        livePrice: 1360.20,
        dayPl: +328000,
        dayPlPct: +2.14,
        color: "#0284c7",
        spark: [1310, 1318, 1324, 1340, 1335, 1352, 1360.2]
      },
      {
        ticker: "TCS",
        name: "Tata Consultancy Services Ltd",
        sector: "Technology",
        shares: 85000,
        avgPrice: 2150.00,
        livePrice: 2349.40,
        dayPl: -185000,
        dayPlPct: -0.92,
        color: "#38bdf8",
        spark: [2410, 2390, 2375, 2380, 2360, 2355, 2349.4]
      },
      {
        ticker: "HDFCBANK",
        name: "HDFC Bank Ltd",
        sector: "Financials",
        shares: 190000,
        avgPrice: 1540.20,
        livePrice: 1742.60,
        dayPl: +420000,
        dayPlPct: +1.45,
        color: "#10b981",
        spark: [1680, 1695, 1710, 1720, 1715, 1735, 1742.6]
      },
      {
        ticker: "INFY",
        name: "Infosys Ltd",
        sector: "Technology",
        shares: 110000,
        avgPrice: 980.00,
        livePrice: 1081.90,
        dayPl: +88000,
        dayPlPct: +0.75,
        color: "#6366f1",
        spark: [1040, 1050, 1065, 1055, 1070, 1078, 1081.9]
      },
      {
        ticker: "ICICIBANK",
        name: "ICICI Bank Ltd",
        sector: "Financials",
        shares: 145000,
        avgPrice: 940.00,
        livePrice: 1092.30,
        dayPl: +194000,
        dayPlPct: +1.28,
        color: "#10b981",
        spark: [1050, 1062, 1075, 1070, 1085, 1088, 1092.3]
      },
      {
        ticker: "NTPC",
        name: "NTPC Ltd (Power & Utilities)",
        sector: "Utilities",
        shares: 320000,
        avgPrice: 185.00,
        livePrice: 228.49,
        dayPl: +112000,
        dayPlPct: +1.65,
        color: "#f59e0b",
        spark: [218, 220, 222, 221, 225, 226, 228.49]
      }
    ];

    // Valuation Trajectory Series (3M default)
    const TRAJECTORY_DATA = {
      '1D': [14.72, 14.75, 14.74, 14.78, 14.79, 14.82, 14.84],
      '1W': [14.50, 14.58, 14.62, 14.60, 14.71, 14.79, 14.84],
      '1M': [14.10, 14.25, 14.20, 14.40, 14.35, 14.60, 14.75, 14.84],
      '3M': [13.20, 13.45, 13.30, 13.80, 13.65, 14.10, 14.35, 14.60, 14.50, 14.84],
      '1Y': [11.60, 12.10, 11.90, 12.80, 13.10, 13.50, 13.20, 14.10, 14.50, 14.84],
      'ALL': [8.50, 9.80, 11.20, 10.90, 12.40, 13.20, 14.84]
    };

    let activeCurrency = "USD";
    let activeSide = "BUY";
    let activeTimeframe = "3M";

    function setNav(el, name) {
      document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
      el.classList.add("active");
    }

    function setCurrency(curr) {
      activeCurrency = curr;
      document.querySelectorAll(".currency-btn").forEach(b => b.classList.remove("active"));
      event.target.classList.add("active");
      
      const rates = { USD: 1, INR: 84.42, EUR: 0.95, GBP: 0.79 };
      const rate = rates[curr];
      const sym = { USD: "$", INR: "₹", EUR: "€", GBP: "£" }[curr];

      document.getElementById("sidebar-liquidity").innerText = `${sym}${(142.85 * rate).toFixed(1)}M`;
      document.getElementById("kpi-total-val").innerText = `${sym}${(14.84 * rate).toFixed(2)}M`;
      document.getElementById("kpi-unrealized-val").innerText = `+${sym}${(3.22 * rate).toFixed(2)}M`;
      document.getElementById("kpi-cash-buffer").innerText = `${sym}${(1.89 * rate).toFixed(2)}M`;
      renderHoldingsTable();
      updateOrderEst();
    }

    // =========================================================================
    // CHART RENDERING: HOLDINGS VALUATION TRAJECTORY
    // =========================================================================
    function setTimeframe(tf, btn) {
      activeTimeframe = tf;
      document.querySelectorAll(".time-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      drawTrajectoryChart();
    }

    function drawTrajectoryChart() {
      const svg = document.getElementById("trajectory-chart");
      const data = TRAJECTORY_DATA[activeTimeframe] || TRAJECTORY_DATA['3M'];
      const rect = svg.getBoundingClientRect();
      const w = rect.width || 650;
      const h = rect.height || 260;

      const padL = 30, padR = 20, padT = 20, padB = 30;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;
      const n = data.length;

      const minVal = Math.min(...data) * 0.98;
      const maxVal = Math.max(...data) * 1.02;

      const scaleX = i => padL + (i / (n - 1)) * innerW;
      const scaleY = v => padT + innerH * (1 - (v - minVal) / (maxVal - minVal));

      // Build path & area
      let linePath = "";
      for (let i = 0; i < n; i++) {
        const x = scaleX(i);
        const y = scaleY(data[i]);
        linePath += `${i === 0 ? 'M' : 'L'} ${x} ${y} `;
      }

      const areaPath = `${linePath} L ${scaleX(n - 1)} ${h - padB} L ${scaleX(0)} ${h - padB} Z`;

      svg.innerHTML = `
        <defs>
          <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.32" />
            <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
          </linearGradient>
        </defs>

        <!-- Horizontal Gridlines -->
        <line x1="${padL}" y1="${padT}" x2="${w - padR}" y2="${padT}" stroke="#1a2333" stroke-dasharray="4,4" />
        <line x1="${padL}" y1="${padT + innerH * 0.5}" x2="${w - padR}" y2="${padT + innerH * 0.5}" stroke="#1a2333" stroke-dasharray="4,4" />
        <line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#1a2333" />

        <!-- Area Fill -->
        <path d="${areaPath}" fill="url(#areaGrad)" />

        <!-- Emerald Trajectory Line -->
        <path d="${linePath}" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" />

        <!-- End Dot Indicator -->
        <circle cx="${scaleX(n - 1)}" cy="${scaleY(data[n - 1])}" r="5" fill="#10b981" stroke="#0d1320" stroke-width="2" />
      `;
    }

    // =========================================================================
    // ORDER DESK LOGIC
    // =========================================================================
    function setOrderSide(side) {
      activeSide = side;
      const buyBtn = document.getElementById("btn-side-buy");
      const sellBtn = document.getElementById("btn-side-sell");
      const transmitBtn = document.getElementById("btn-transmit-order");

      if (side === "BUY") {
        buyBtn.className = "toggle-side-btn active-buy";
        sellBtn.className = "toggle-side-btn";
        transmitBtn.style.background = "var(--emerald)";
        transmitBtn.innerHTML = "<span>⚡</span> Transmit Institutional BUY Order";
      } else {
        buyBtn.className = "toggle-side-btn";
        sellBtn.className = "toggle-side-btn active-sell";
        transmitBtn.style.background = "var(--rose)";
        transmitBtn.innerHTML = "<span>⚡</span> Transmit Institutional SELL Order";
      }
    }

    function setQtyPct(pct) {
      const base = 5000;
      document.getElementById("order-qty").value = Math.round(base * pct);
      updateOrderEst();
    }

    function updateOrderEst() {
      const qty = parseFloat(document.getElementById("order-qty").value) || 0;
      const price = parseFloat(document.getElementById("order-price").value) || 0;
      const total = qty * price;
      
      const sym = { USD: "$", INR: "₹", EUR: "€", GBP: "£" }[activeCurrency] || "$";
      document.getElementById("order-est-val").innerText = `${sym}${total.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    }

    function transmitOrder() {
      const ticker = document.getElementById("order-ticker").value;
      const qty = document.getElementById("order-qty").value;
      const price = document.getElementById("order-price").value;

      showToast("Order Executed & Filled", `${activeSide} ${Number(qty).toLocaleString()} ${ticker} @ ${price}`);
    }

    function showToast(title, msg) {
      const toast = document.getElementById("exec-toast");
      document.getElementById("toast-title").innerText = title;
      document.getElementById("toast-msg").innerText = msg;
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 3500);
    }

    // =========================================================================
    // HOLDINGS DATA TABLE & SPARKLINES
    // =========================================================================
    function renderHoldingsTable() {
      const tbody = document.getElementById("holdings-tbody");
      const search = (document.getElementById("holdings-search").value || "").toUpperCase();
      const sec = document.getElementById("sector-filter").value;

      const filtered = HOLDINGS.filter(h => {
        const m1 = h.ticker.includes(search) || h.name.toUpperCase().includes(search);
        const m2 = (sec === "ALL" || h.sector === sec);
        return m1 && m2;
      });

      const sym = { USD: "$", INR: "₹", EUR: "€", GBP: "£" }[activeCurrency] || "$";

      tbody.innerHTML = filtered.map(h => {
        const totalVal = h.shares * h.livePrice;
        const totalCost = h.shares * h.avgPrice;
        const gain = totalVal - totalCost;
        const gainPct = (gain / totalCost) * 100;

        // Sparkline SVG
        const minS = Math.min(...h.spark);
        const maxS = Math.max(...h.spark);
        const pts = h.spark.map((v, i) => {
          const x = (i / (h.spark.length - 1)) * 88;
          const y = 20 - ((v - minS) / (maxS - minS || 1)) * 16;
          return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`;
        }).join(' ');

        const sparkColor = h.dayPl >= 0 ? "#10b981" : "#f43f5e";

        return `
          <tr>
            <td>
              <div class="asset-cell">
                <div class="asset-icon" style="background:${h.color};">${h.ticker.slice(0, 2)}</div>
                <div class="asset-info">
                  <span class="asset-ticker">${h.ticker}</span>
                  <span class="asset-name">${h.name}</span>
                </div>
              </div>
            </td>
            <td><span class="sector-badge">${h.sector}</span></td>
            <td>${h.shares.toLocaleString()}</td>
            <td>${sym}${h.avgPrice.toFixed(2)}</td>
            <td style="font-weight:700; color:#fff;">${sym}${h.livePrice.toFixed(2)}</td>
            <td style="font-weight:800; color:#fff;">${sym}${(totalVal / 1e6).toFixed(2)}M</td>
            <td style="color:${h.dayPl >= 0 ? 'var(--emerald)' : 'var(--rose)'}; font-weight:700;">
              ${h.dayPl >= 0 ? '+' : ''}${h.dayPlPct.toFixed(2)}%
            </td>
            <td style="color:var(--emerald); font-weight:700;">
              +${sym}${(gain / 1e6).toFixed(2)}M (+${gainPct.toFixed(1)}%)
            </td>
            <td>
              <svg class="sparkline-svg" viewBox="0 0 90 24">
                <path d="${pts}" fill="none" stroke="${sparkColor}" stroke-width="2" stroke-linecap="round" />
              </svg>
            </td>
            <td>
              <button class="btn" style="padding: 4px 8px; font-size: 0.72rem;" onclick="prefillOrder('${h.ticker}', ${h.livePrice})">
                Trade
              </button>
            </td>
          </tr>
        `;
      }).join('');

      document.getElementById("pagination-info").innerText = `Showing 1 to ${filtered.length} of ${filtered.length} active positions`;
    }

    function filterHoldings() {
      renderHoldingsTable();
    }

    function prefillOrder(ticker, price) {
      document.getElementById("order-ticker").value = ticker;
      document.getElementById("order-price").value = price;
      updateOrderEst();
      showToast("Position Loaded into Order Desk", `${ticker} @ ${price}`);
    }

    // Initialize
    window.addEventListener("DOMContentLoaded", () => {
      drawTrajectoryChart();
      renderHoldingsTable();
      updateOrderEst();
    });

    window.addEventListener("resize", () => {
      drawTrajectoryChart();
    });
  </script>
</body>
</html>
"""

dest_path = "financial-market-intelligence/04_dashboard/executive_banking_dashboard.html"
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(html_code)

# Also write directly to brain artifact directory
artifact_dir = r"C:\Users\ankus\.gemini\antigravity\brain\b538a0f7-1b58-48a0-9917-4377b8d7d8bf"
os.makedirs(artifact_dir, exist_ok=True)
artifact_file = os.path.join(artifact_dir, "executive_banking_dashboard.html")
with open(artifact_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Generated Executive Banking Dashboard at: {dest_path}")
print(f"Synced to artifact path: {artifact_file}")
