# -*- coding: utf-8 -*-
"""
Upgrade Power BI Canvas with 10-Year Global Multi-Market Intelligence Suite
"""

import os

pbi_file = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\build_interactive_powerbi.py"

with open(pbi_file, "r", encoding="utf-8") as f:
    pbi_code = f.read()

# 1. Update Timeframe Pills to include 5Y and 10Y
old_time_pills = '''            <div class="inline-flex p-0.5 rounded bg-pbi-surface border border-pbi-border" id="timeframe-group">
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('1M', this)">1M</button>
              <button class="px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm" onclick="onTimeframeChange('3M', this)">3M</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('1Y', this)">1Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('YTD', this)">YTD</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('ALL', this)">ALL</button>
            </div>'''

new_time_pills = '''            <div class="inline-flex p-0.5 rounded bg-pbi-surface border border-pbi-border" id="timeframe-group">
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('1M', this)">1M</button>
              <button class="px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm" onclick="onTimeframeChange('3M', this)">3M</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('1Y', this)">1Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('5Y', this)">5Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('10Y', this)">10Y</button>
              <button class="px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white" onclick="onTimeframeChange('ALL', this)">ALL</button>
            </div>'''

pbi_code = pbi_code.replace(old_time_pills, new_time_pills)

# 2. Update onTimeframeChange in JS to support 5Y and 10Y
old_tf_js = '''      let days = 60;
      if (period === '1M') days = 22;
      else if (period === '3M') days = 65;
      else if (period === '1Y') days = 250;
      else if (period === 'ALL') days = 360;'''

new_tf_js = '''      let days = 60;
      if (period === '1M') days = 22;
      else if (period === '3M') days = 65;
      else if (period === '1Y') days = 250;
      else if (period === '5Y') days = 1250;
      else if (period === '10Y') days = 2600;
      else if (period === 'ALL') days = 3650;'''

pbi_code = pbi_code.replace(old_tf_js, new_tf_js)

# 3. Add Tab 4 Button to footer dock
old_footer_tabs = '''      <button class="px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer" id="tab-btn-risk" onclick="switchReportTab('risk')">
        <span class="material-symbols-outlined text-xs">shield</span>
        <span>3. Risk Analytics &amp; DAX Playground</span>
      </button>
    </div>

    <div class="flex items-center gap-3 text-[11px] text-[#94a3b8] font-mono">
      <span>Laptop Viewport Fit</span>
      <span>•</span>
      <span id="page-counter">Page 1 of 3</span>
    </div>'''

new_footer_tabs = '''      <button class="px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer" id="tab-btn-risk" onclick="switchReportTab('risk')">
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
    </div>'''

pbi_code = pbi_code.replace(old_footer_tabs, new_footer_tabs)

# 4. Add Page 4 (10-Year Global Intelligence) HTML
page_decade_html = '''
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
'''

pbi_code = pbi_code.replace('      <!-- =====================================================================\n           PAGE 3: RISK ANALYTICS', page_decade_html + '\n      <!-- =====================================================================\n           PAGE 3: RISK ANALYTICS')

# 5. Update switchReportTab JS function to handle 'decade'
old_tab_switch = '''    function switchReportTab(page) {
      document.getElementById('page-exec').classList.add('hidden');
      document.getElementById('page-tech').classList.add('hidden');
      document.getElementById('page-risk').classList.add('hidden');

      ['exec', 'tech', 'risk'].forEach(p => {
        const btn = document.getElementById(`tab-btn-${p}`);
        btn.className = "px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer";
      });

      const activeBtn = document.getElementById(`tab-btn-${page}`);
      activeBtn.className = "px-3 py-1 rounded-t bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-[#818cf8] font-bold flex items-center gap-1 border-t-2 border-t-[#818cf8] cursor-pointer";

      document.getElementById(`page-${page}`).classList.remove('hidden');

      const pageMap = { 'exec': 'Page 1 of 3', 'tech': 'Page 2 of 3', 'risk': 'Page 3 of 3' };
      document.getElementById('page-counter').innerText = pageMap[page] || 'Page 1 of 3';'''

new_tab_switch = '''    function switchReportTab(page) {
      document.getElementById('page-exec').classList.add('hidden');
      document.getElementById('page-tech').classList.add('hidden');
      document.getElementById('page-risk').classList.add('hidden');
      const pDec = document.getElementById('page-decade');
      if (pDec) pDec.classList.add('hidden');

      ['exec', 'tech', 'risk', 'decade'].forEach(p => {
        const btn = document.getElementById(`tab-btn-${p}`);
        if (btn) btn.className = "px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer";
      });

      const activeBtn = document.getElementById(`tab-btn-${page}`);
      if (activeBtn) activeBtn.className = "px-3 py-1 rounded-t bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-[#818cf8] font-bold flex items-center gap-1 border-t-2 border-t-[#818cf8] cursor-pointer";

      const targetPage = document.getElementById(`page-${page}`);
      if (targetPage) targetPage.classList.remove('hidden');

      const pageMap = { 'exec': 'Page 1 of 4', 'tech': 'Page 2 of 4', 'risk': 'Page 3 of 4', 'decade': 'Page 4 of 4' };
      document.getElementById('page-counter').innerText = pageMap[page] || 'Page 1 of 4';'''

pbi_code = pbi_code.replace(old_tab_switch, new_tab_switch)

with open(pbi_file, "w", encoding="utf-8") as f:
    f.write(pbi_code)

print("Updated build_interactive_powerbi.py with 10-Year Global Intelligence!")

# Also append 10-Year DAX measures to DAX_Measures.dax
dax_file = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\DAX_Measures.dax"
with open(dax_file, "r", encoding="utf-8") as f:
    dax_content = f.read()

new_dax = """
// ==============================================================================
// 10-YEAR GLOBAL DECADE INTELLIGENCE & COMPOUNDING MEASURES
// ==============================================================================

[10Y Total Return %] = 
VAR InceptionPrice = CALCULATE(FIRSTNONBLANK(Fact_StockAnalytics[close], 1), ALL(Dim_Date_10Y))
VAR LatestPrice = [Latest Close Price]
RETURN
    DIVIDE(LatestPrice - InceptionPrice, InceptionPrice, 0) * 100

[10Y CAGR %] = 
VAR InceptionPrice = CALCULATE(FIRSTNONBLANK(Fact_StockAnalytics[close], 1), ALL(Dim_Date_10Y))
VAR LatestPrice = [Latest Close Price]
VAR YearsSpan = 10.0
RETURN
    IF(InceptionPrice > 0, ((LatestPrice / InceptionPrice) ^ (1 / YearsSpan) - 1) * 100, 0)

[10Y Max Drawdown %] = 
MIN(Fact_10Y_PerformanceSummary[max_drawdown])

[10Y Annualized Sharpe] = 
AVERAGE(Fact_10Y_PerformanceSummary[sharpe])
"""

if "[10Y Total Return %]" not in dax_content:
    with open(dax_file, "a", encoding="utf-8") as f:
        f.write("\n" + new_dax)
    print("Appended 10-Year DAX measures to DAX_Measures.dax!")
