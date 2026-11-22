# -*- coding: utf-8 -*-
"""
Apply Quantum Horizon & Cyber-Sapphire UI Theme
Across both Microsoft Power BI and Streamlit applications.
"""

import os
import re

# ==============================================================================
# 1. UPDATE POWER BI SCRIPT & COMPILE CANVAS
# ==============================================================================
pbi_script_path = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\build_interactive_powerbi.py"

with open(pbi_script_path, "r", encoding="utf-8") as f:
    pbi_code = f.read()

# Replace Tailwind Config
old_tw_config = '''            pbi: {
              gold: "#f2c811",
              yellow: "#f3c911",
              dark: "#050b0e",
              surface: "#091418",
              card: "#0d1c22",
              hover: "#142c34",
              border: "#16323a",
              ribbon: "#0c181d",
              accent: "#00ff9d",
              mint: "#00f5d4",
              cyan: "#38bdf8",
              rose: "#ff4d6d",
              amber: "#ffd166",
              purple: "#c084fc"
            }'''

new_tw_config = '''            pbi: {
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
            }'''

pbi_code = pbi_code.replace(old_tw_config, new_tw_config)

# Replace Styles in <style>
old_style_block = '''    body {
      background-color: #050b0e;
      color: #e6fffa;
      font-family: 'Segoe UI', sans-serif;
      font-size: 13px;
      overflow-x: hidden;
    }
    
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #050b0e; }
    ::-webkit-scrollbar-thumb { background: #16323a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #00ff9d; }

    .pbi-card {
      background: #091418;
      border: 1px solid #16323a;
      border-radius: 8px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
    }
    .pbi-card:hover {
      border-color: rgba(0, 255, 157, 0.4);
    }

    .pbi-active-row {
      background: rgba(0, 255, 157, 0.12) !important;
      border-left: 3px solid #00ff9d !important;
    }

    #filters-pane {
      transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s ease;
    }

    .data-bar-pos {
      background: linear-gradient(90deg, rgba(0,255,157,0.18), rgba(0,255,157,0.55));
      border-radius: 3px;
    }
    .data-bar-neg {
      background: linear-gradient(90deg, rgba(255,77,109,0.18), rgba(255,77,109,0.55));
      border-radius: 3px;
    }

    @keyframes pulseGlow {
      0%, 100% { opacity: 0.8; }
      50% { opacity: 1; filter: drop-shadow(0 0 8px #00ff9d); }
    }
    .pbi-live-pulse { animation: pulseGlow 2s infinite ease-in-out; }'''

new_style_block = '''    body {
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
    .pbi-live-pulse { animation: pulseGlow 2s infinite ease-in-out; }'''

pbi_code = pbi_code.replace(old_style_block, new_style_block)

# Replace Title
pbi_code = pbi_code.replace(
    "<title>Power BI — Financial Market Intelligence & Executive Analytics</title>",
    "<title>Power BI Quantum — Executive Market Intelligence & Prismatic Analytics</title>"
)

# Replace Power BI Logo & Title Badge in Ribbon
old_header_brand = '''        <div class="w-6 h-6 rounded bg-[#f2c811] flex items-center justify-center shadow-sm">
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
          <span class="text-white font-mono">Financial Market Intelligence</span>
          <span class="text-[10px] text-[#80a5a0] hidden md:inline">/ Databricks Delta Lake DirectQuery</span>
        </div>'''

new_header_brand = '''        <div class="w-6 h-6 rounded bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
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
        </div>'''

pbi_code = pbi_code.replace(old_header_brand, new_header_brand)

# Replace User Avatar
pbi_code = pbi_code.replace(
    'class="w-6 h-6 rounded-full bg-teal-900 border border-pbi-accent/40 flex items-center justify-center text-[10px] font-bold text-pbi-accent"',
    'class="w-6 h-6 rounded-full bg-gradient-to-tr from-indigo-600 to-cyan-500 border border-indigo-400/50 flex items-center justify-center text-[10px] font-bold text-white shadow-sm"'
)

# Replace Slicers Ribbon Border Accent
pbi_code = pbi_code.replace('border-l-pbi-gold', 'border-l-[#818cf8]')
pbi_code = pbi_code.replace('text-pbi-gold uppercase tracking-wider', 'text-[#818cf8] uppercase tracking-wider')

# Replace Card 1 Border Accent (Portfolio NAV)
pbi_code = pbi_code.replace('border-t-pbi-accent relative', 'border-t-[#818cf8] relative')
pbi_code = pbi_code.replace('border-t-pbi-mint relative', 'border-t-[#00f0ff] relative')
pbi_code = pbi_code.replace('border-t-pbi-cyan relative', 'border-t-[#c084fc] relative')
pbi_code = pbi_code.replace('border-t-pbi-amber relative', 'border-t-[#fbbf24] relative')

# Replace Color References for Muted Text
pbi_code = pbi_code.replace('#80a5a0', '#94a3b8')

# Replace Chart.js main chart default colors
pbi_code = pbi_code.replace("borderColor: '#00ff9d',", "borderColor: '#00f0ff',")
pbi_code = pbi_code.replace("backgroundColor: 'rgba(0, 255, 157, 0.1)',", "backgroundColor: 'rgba(0, 240, 255, 0.12)',")
pbi_code = pbi_code.replace("borderColor: '#f2c811',", "borderColor: '#fbbf24',")
pbi_code = pbi_code.replace("borderColor: '#38bdf8',", "borderColor: '#ec4899',")
pbi_code = pbi_code.replace("borderColor: 'rgba(0, 245, 212, 0.4)',", "borderColor: 'rgba(192, 132, 252, 0.45)',")
pbi_code = pbi_code.replace("backgroundColor: 'rgba(192, 132, 252, 0.2)',", "backgroundColor: 'rgba(99, 102, 241, 0.35)',")

# Replace Tooltip background and borders
pbi_code = pbi_code.replace("backgroundColor: '#091418',", "backgroundColor: 'rgba(10, 14, 28, 0.95)',")
pbi_code = pbi_code.replace("titleColor: '#00ff9d',", "titleColor: '#00f0ff',")
pbi_code = pbi_code.replace("borderColor: '#16323a',", "borderColor: 'rgba(129, 140, 248, 0.3)',")
pbi_code = pbi_code.replace("grid: { color: 'rgba(22, 50, 58, 0.5)' }", "grid: { color: 'rgba(129, 140, 248, 0.12)' }")

# Replace Donut Chart Colors
pbi_code = pbi_code.replace(
    "backgroundColor: ['#00ff9d', '#38bdf8', '#ffd166', '#c084fc'],",
    "backgroundColor: ['#818cf8', '#00f0ff', '#fbbf24', '#ec4899'],"
)
pbi_code = pbi_code.replace("borderColor: '#091418',", "borderColor: '#0e142c',")

# Replace Donut Legend Dots
pbi_code = pbi_code.replace('bg-pbi-accent"></span>Technology &amp; AI', 'bg-[#818cf8]"></span>Technology &amp; AI')
pbi_code = pbi_code.replace('text-pbi-accent">42.0%', 'text-[#818cf8]">42.0%')
pbi_code = pbi_code.replace('bg-pbi-cyan"></span>Financial Services', 'bg-[#00f0ff]"></span>Financial Services')
pbi_code = pbi_code.replace('text-pbi-cyan">24.0%', 'text-[#00f0ff]">24.0%')
pbi_code = pbi_code.replace('bg-pbi-amber"></span>Energy &amp; Conglomerates', 'bg-[#fbbf24]"></span>Energy &amp; Conglomerates')
pbi_code = pbi_code.replace('text-pbi-amber">18.0%', 'text-[#fbbf24]">18.0%')
pbi_code = pbi_code.replace('bg-purple-400"></span>Semiconductors', 'bg-[#ec4899]"></span>Semiconductors')
pbi_code = pbi_code.replace('text-purple-400">16.0%', 'text-[#ec4899]">16.0%')

# Replace Holdings Data Colors
pbi_code = pbi_code.replace('color: "#00ff9d"', 'color: "#00f0ff"')
pbi_code = pbi_code.replace('color: "#00f5d4"', 'color: "#818cf8"')
pbi_code = pbi_code.replace('color: "#f2c811"', 'color: "#fbbf24"')
pbi_code = pbi_code.replace('color: "#ff4d6d"', 'color: "#f43f5e"')

# Replace Tab Navigation Active Style
old_tab_active = '''      <button class="px-3 py-1 rounded-t bg-pbi-surface text-pbi-gold font-bold flex items-center gap-1 border-t-2 border-t-pbi-gold cursor-pointer" id="tab-btn-exec" onclick="switchReportTab('exec')">'''
new_tab_active = '''      <button class="px-3 py-1 rounded-t bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-[#818cf8] font-bold flex items-center gap-1 border-t-2 border-t-[#818cf8] cursor-pointer" id="tab-btn-exec" onclick="switchReportTab('exec')">'''
pbi_code = pbi_code.replace(old_tab_active, new_tab_active)

# Replace Tab Switch JS function
old_tab_switch_js = '''        btn.className = "px-3 py-1 rounded-t bg-pbi-surface text-pbi-gold font-bold flex items-center gap-1 border-t-2 border-t-pbi-gold cursor-pointer";'''
new_tab_switch_js = '''        btn.className = "px-3 py-1 rounded-t bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-[#818cf8] font-bold flex items-center gap-1 border-t-2 border-t-[#818cf8] cursor-pointer";'''
pbi_code = pbi_code.replace(old_tab_switch_js, new_tab_switch_js)

# Write updated build_interactive_powerbi.py
with open(pbi_script_path, "w", encoding="utf-8") as f:
    f.write(pbi_code)

print("Updated build_interactive_powerbi.py successfully!")


# ==============================================================================
# 2. UPDATE STREAMLIT APP (04_dashboard/app.py)
# ==============================================================================
st_app_path = r"D:\BDA Project\financial-market-intelligence\04_dashboard\app.py"

with open(st_app_path, "r", encoding="utf-8") as f:
    st_code = f.read()

# Replace Theme Colors
old_theme_colors = '''# Theme Colors
BG_COLOR = "#09090b" if IS_DARK else "#ffffff"
BG_SUBTLE = "#0c0c0f" if IS_DARK else "#f8fafc"
CARD_BG = "#111115" if IS_DARK else "#ffffff"
BORDER_COLOR = "#27272a" if IS_DARK else "#e2e8f0"
BORDER_SUBTLE = "#1e1e24" if IS_DARK else "#f1f5f9"
TEXT_COLOR = "#f4f4f5" if IS_DARK else "#09090b"
TEXT_MUTED = "#a1a1aa" if IS_DARK else "#64748b"
ACCENT = "#38bdf8"
ACCENT_GREEN = "#22c55e" if IS_DARK else "#16a34a"
ACCENT_RED = "#ef4444" if IS_DARK else "#dc2626"
ACCENT_AMBER = "#f59e0b" if IS_DARK else "#d97706"'''

new_theme_colors = '''# Theme Colors - Quantum Horizon & Holographic Amethyst
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
ACCENT_FUCHSIA = "#ec4899"'''

st_code = st_code.replace(old_theme_colors, new_theme_colors)

# Replace Global CSS
old_css_part = '''    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {
        background-color: '''

new_css_part = '''    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {
        background: radial-gradient(circle at 12% 10%, rgba(99, 102, 241, 0.16) 0%, transparent 45%),
                    radial-gradient(circle at 88% 85%, rgba(244, 63, 94, 0.12) 0%, transparent 45%),
                    radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 55%),
                    #070913 !important;
        background-color: '''

st_code = st_code.replace(old_css_part, new_css_part)

# Replace metric-card CSS
old_metric_card = '''.metric-card {
        background: '''

new_metric_card_css = '''.metric-card {
        background: rgba(14, 20, 44, 0.82) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.65), inset 0 1px 0 0 rgba(255, 255, 255, 0.08) !important;
        background: '''

st_code = st_code.replace(old_metric_card, new_metric_card_css)

# Replace Header Logo and Title
old_st_header = '''    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.2rem;">
        <div style="background: linear-gradient(135deg, #0284c7, #38bdf8); width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: #fff; font-weight: 700;">
            ₹
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 700; margin: 0; padding: 0; letter-spacing: -0.02em; color: {TEXT_COLOR};">
                Financial Market Intelligence
            </h1>
            <p style="font-size: 0.8rem; color: {TEXT_MUTED}; margin: 2px 0 0 0;">
                <span class="live-dot"></span><strong>Live Multi-Asset Terminal</strong> • Indian Equities • Forex • Cryptocurrencies • Lakehouse Gold Analytics
            </p>
        </div>
    </div>'''

new_st_header = '''    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.2rem;">
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
    </div>'''

st_code = st_code.replace(old_st_header, new_st_header)

# Replace Candlestick increasing/decreasing colors in app.py
st_code = st_code.replace('increasing_line_color="#22c55e"', 'increasing_line_color="#10b981"')
st_code = st_code.replace('decreasing_line_color="#ef4444"', 'decreasing_line_color="#f43f5e"')
st_code = st_code.replace('line=dict(color="#38bdf8", width=2)', 'line=dict(color="#00f0ff", width=2.5)')

# Replace badges
st_code = st_code.replace('.badge-bullish { color: #22c55e; background: rgba(34,197,94,0.15); }', '.badge-bullish { color: #10b981; background: rgba(16,185,129,0.18); border: 1px solid rgba(16,185,129,0.3); }')
st_code = st_code.replace('.badge-bearish { color: #ef4444; background: rgba(239,68,68,0.15); }', '.badge-bearish { color: #f43f5e; background: rgba(244,63,94,0.18); border: 1px solid rgba(244,63,94,0.3); }')
st_code = st_code.replace('.badge-neutral { color: #38bdf8; background: rgba(56,189,248,0.15); }', '.badge-neutral { color: #00f0ff; background: rgba(0,240,255,0.18); border: 1px solid rgba(0,240,255,0.3); }')
st_code = st_code.replace('.badge-warn    { color: #f59e0b; background: rgba(245,158,11,0.15); }', '.badge-warn    { color: #fbbf24; background: rgba(251,191,36,0.18); border: 1px solid rgba(251,191,36,0.3); }')

# Replace Tab styles in CSS for Streamlit
tab_css_snippet = '''
    /* Custom Tabs with glowing indicator */
    button[data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(129, 140, 248, 0.1) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(6, 182, 212, 0.2)) !important;
        border: 1px solid rgba(129, 140, 248, 0.5) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25) !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #818cf8 !important;
    }
'''

if '/* Custom Tabs with glowing indicator */' not in st_code:
    st_code = st_code.replace('</style>', tab_css_snippet + '\n</style>')

with open(st_app_path, "w", encoding="utf-8") as f:
    f.write(st_code)

print("Updated 04_dashboard/app.py successfully!")


# ==============================================================================
# 3. UPDATE POWER BI DESKTOP THEME JSON
# ==============================================================================
theme_json_path = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\PowerBI_Aurora_Theme.json"
quantum_theme_json = """{
  "name": "Quantum Horizon & Holographic Amethyst Theme",
  "dataColors": [
    "#818cf8",
    "#00f0ff",
    "#fbbf24",
    "#ec4899",
    "#10b981",
    "#f43f5e",
    "#c084fc",
    "#38bdf8"
  ],
  "background": "#070913",
  "foreground": "#0e142c",
  "tableAccent": "#818cf8",
  "visualStyles": {
    "*": {
      "*": {
        "background": [
          {
            "color": { "solid": { "color": "#0e142c" } },
            "transparency": 10
          }
        ],
        "border": [
          {
            "color": { "solid": { "color": "#1e294b" } },
            "width": 1,
            "radius": 10
          }
        ],
        "dropShadow": [
          {
            "show": true,
            "color": { "solid": { "color": "#000000" } },
            "position": "Outer",
            "preset": "BottomRight"
          }
        ],
        "title": [
          {
            "fontColor": { "solid": { "color": "#f8fafc" } },
            "fontFamily": "Segoe UI Semibold",
            "fontSize": 12
          }
        ]
      }
    },
    "card": {
      "*": {
        "labels": [
          {
            "color": { "solid": { "color": "#00f0ff" } },
            "fontFamily": "JetBrains Mono",
            "fontSize": 24
          }
        ],
        "categoryLabels": [
          {
            "color": { "solid": { "color": "#94a3b8" } },
            "fontFamily": "Segoe UI",
            "fontSize": 10
          }
        ]
      }
    }
  }
}"""

with open(theme_json_path, "w", encoding="utf-8") as f:
    f.write(quantum_theme_json)

# Also write to PowerBI_Quantum_Theme.json
with open(r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\PowerBI_Quantum_Theme.json", "w", encoding="utf-8") as f:
    f.write(quantum_theme_json)

print("Updated Power BI Theme JSON successfully!")
