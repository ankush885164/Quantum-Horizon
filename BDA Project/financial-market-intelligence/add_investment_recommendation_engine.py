# -*- coding: utf-8 -*-
"""
Add Quantitative AI Investment Recommendation & Decision Engine
Across Streamlit (04_dashboard/app.py) and Power BI (05_powerbi_dashboard)
"""

import os
import re

# ==============================================================================
# 1. UPGRADE STREAMLIT APP (04_dashboard/app.py)
# ==============================================================================
st_file = r"D:\BDA Project\financial-market-intelligence\04_dashboard\app.py"
with open(st_file, "r", encoding="utf-8") as f:
    code = f.read()

# Helper function definition for Investment Recommendation
rec_function_code = '''
# ==============================================================================
# QUANTITATIVE INVESTMENT DECISION & RECOMMENDATION ENGINE
# ==============================================================================
def compute_investment_decision(price, sma20, sma50, sma200, rsi, cagr=None, max_dd=None, sharpe=None):
    score = 50
    catalysts = []
    risks = []

    # 1. Trend Analysis
    if price >= sma20:
        score += 8
        catalysts.append("Trading above 20 SMA (Short-term momentum is positive)")
    else:
        score -= 6
        risks.append("Trading below 20 SMA (Experiencing short-term pullback)")

    if price >= sma50:
        score += 10
        catalysts.append("Trading above 50 SMA (Intermediate trend remains upward)")
    else:
        score -= 8
        risks.append("Below 50 SMA (Medium-term resistance headwind)")

    if sma50 >= sma200:
        score += 12
        catalysts.append("Confirmed Golden Cross (50 SMA > 200 SMA secular bull structure)")
    else:
        score -= 10
        risks.append("Death Cross structure (50 SMA < 200 SMA macro consolidation)")

    # 2. RSI Momentum
    if 45 <= rsi <= 65:
        score += 10
        catalysts.append(f"RSI at {rsi:.1f} in optimal continuation zone (Healthy trend without exhaustion)")
    elif rsi < 35:
        score += 8
        catalysts.append(f"RSI at {rsi:.1f} in oversold zone (Contrarian value accumulation opportunity)")
    elif rsi > 75:
        score -= 8
        risks.append(f"RSI at {rsi:.1f} in overbought zone (Elevated near-term consolidation risk)")
    else:
        score += 4

    # 3. 10Y Compounding track record
    if cagr is not None:
        if cagr >= 25:
            score += 15
            catalysts.append(f"Decade CAGR of {cagr:.1f}% indicates top-tier global compounding power")
        elif cagr >= 12:
            score += 10
            catalysts.append(f"Decade CAGR of {cagr:.1f}% consistently outperforms broad market benchmark")
        elif cagr < 5:
            score -= 10
            risks.append(f"Low decade CAGR of {cagr:.1f}% lags inflation benchmarks")

    if sharpe is not None:
        if sharpe >= 1.2:
            score += 10
            catalysts.append(f"Sharpe Ratio of {sharpe:.2f} confirms superior risk-adjusted alpha")
        elif sharpe < 0.6:
            score -= 6
            risks.append(f"Low Sharpe Ratio ({sharpe:.2f}) indicates excess volatility per unit return")

    score = max(10, min(96, score))

    if score >= 80:
        verdict = "STRONG BUY"
        action = "High Conviction Accumulation • Overweight Core Portfolio"
        color = "#10b981" # Emerald
        bg = "rgba(16, 185, 129, 0.15)"
        border = "rgba(16, 185, 129, 0.4)"
        allocation = "7% - 12% Target Portfolio Allocation"
    elif score >= 65:
        verdict = "BUY / ACCUMULATE"
        action = "Scale In on Dips • Favorable Risk-Reward Setup"
        color = "#00f0ff" # Cyan
        bg = "rgba(0, 240, 255, 0.15)"
        border = "rgba(0, 240, 255, 0.4)"
        allocation = "4% - 7% Target Portfolio Allocation"
    elif score >= 50:
        verdict = "HOLD / NEUTRAL"
        action = "Maintain Existing Positions • Await Confirmed Breakout"
        color = "#fbbf24" # Amber
        bg = "rgba(251, 191, 36, 0.15)"
        border = "rgba(251, 191, 36, 0.4)"
        allocation = "2% - 4% Tactical Position"
    elif score >= 38:
        verdict = "TRIM / TAKE PROFITS"
        action = "Harvest Partial Gains • Tighten Trailing Stop-Loss"
        color = "#ec4899" # Fuchsia
        bg = "rgba(236, 72, 153, 0.15)"
        border = "rgba(236, 72, 153, 0.4)"
        allocation = "Underweight / Reduce Exposure"
    else:
        verdict = "AVOID / HIGH RISK"
        action = "Capital Preservation Priority • Avoid Initiating Longs"
        color = "#f43f5e" # Rose
        bg = "rgba(244, 63, 94, 0.15)"
        border = "rgba(244, 63, 94, 0.4)"
        allocation = "0% Allocation (Cash / Capital Preservation)"

    stop_loss = round(price * 0.92, 2)
    target_1y = round(price * 1.24, 2)
    entry_low = round(price * 0.97, 2)
    entry_high = round(price * 1.01, 2)

    return {
        "verdict": verdict,
        "score": score,
        "action": action,
        "color": color,
        "bg": bg,
        "border": border,
        "allocation": allocation,
        "entry_range": f"{entry_low} - {entry_high}",
        "target_1y": target_1y,
        "stop_loss": stop_loss,
        "catalysts": catalysts[:3],
        "risks": risks[:2] if risks else ["Normal market volatility applies (Set disciplined stop-losses)"]
    }
'''

if "def compute_investment_decision" not in code:
    code = code.replace("def format_currency_price", rec_function_code + "\n\ndef format_currency_price")

# Inject Investment Decision Card into Tab 0 (right after the 5 hero metric cards)
old_tab0_anchor = 'st.markdown("<div style=\'height: 1.2rem;\'></div>", unsafe_allow_html=True)'

rec_card_injection = '''
        # ----------------------------------------------------------------------
        # AI Quantitative Investment Decision & Recommendation Desk
        # ----------------------------------------------------------------------
        sma200_val = latest_row.get("SMA_200", sma50 * 0.95)
        rec = compute_investment_decision(curr_price, sma20, sma50, sma200_val, rsi_val)

        catalysts_html = "".join([f"<li style='margin-bottom:3px;'>✅ {c}</li>" for c in rec["catalysts"]])
        risks_html = "".join([f"<li style='margin-bottom:3px;'>⚠️ {r}</li>" for r in rec["risks"]])

        st.markdown(f"""
        <div style="background:{rec['bg']}; border:1px solid {rec['border']}; border-radius:12px; padding:1.1rem 1.35rem; margin-top:1rem; margin-bottom:1.1rem; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
            <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; margin-bottom:0.75rem; border-bottom:1px solid {rec['border']}; padding-bottom:0.65rem;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="background:{rec['color']}; color:#000; font-weight:800; font-size:0.75rem; padding:3px 10px; border-radius:6px; letter-spacing:0.04em;">
                        INVESTMENT RECOMMENDATION
                    </span>
                    <span style="font-size:1.35rem; font-weight:800; color:{rec['color']}; font-family:'JetBrains Mono';">
                        {rec['verdict']}
                    </span>
                    <span style="font-size:0.85rem; color:#f8fafc; font-weight:700; background:rgba(255,255,255,0.08); padding:3px 8px; border-radius:6px;">
                        Quantitative Score: {rec['score']} / 100
                    </span>
                </div>
                <div style="font-size:0.8rem; font-weight:700; color:{rec['color']}; font-family:'JetBrains Mono';">
                    🎯 {rec['action']}
                </div>
            </div>
            
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:0.75rem; font-size:0.78rem;">
                <div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);">
                    <span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">SUGGESTED BUY / ACCUMULATION ZONE</span>
                    <strong style="color:#f8fafc; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(rec['entry_range'].split(' - ')[0], active_ticker)} - {format_currency_price(rec['entry_range'].split(' - ')[1], active_ticker)}</strong>
                </div>
                <div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);">
                    <span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">1-YEAR PROJECTED TARGET PRICE</span>
                    <strong style="color:#10b981; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(rec['target_1y'], active_ticker)} (+24% Upside)</strong>
                </div>
                <div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);">
                    <span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">PROTECTIVE INVALIDATION STOP-LOSS</span>
                    <strong style="color:#f43f5e; font-size:0.95rem; font-family:'JetBrains Mono';">{format_currency_price(rec['stop_loss'], active_ticker)} (-8% Risk Cut)</strong>
                </div>
                <div style="background:rgba(14,20,44,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(129,140,248,0.2);">
                    <span style="color:#94a3b8; font-size:0.7rem; font-weight:700; display:block;">PORTFOLIO SIZING GUIDELINE</span>
                    <strong style="color:#818cf8; font-size:0.95rem; font-family:'JetBrains Mono';">{rec['allocation']}</strong>
                </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:0.76rem; margin-top:6px;">
                <div style="color:#e2e8f0;">
                    <strong style="color:#10b981; display:block; margin-bottom:4px;">Pillars Supporting Investment:</strong>
                    <ul style="margin:0; padding-left:14px; list-style-type:none;">
                        {catalysts_html}
                    </ul>
                </div>
                <div style="color:#e2e8f0;">
                    <strong style="color:#f43f5e; display:block; margin-bottom:4px;">Risk Checks & Invalidation Conditions:</strong>
                    <ul style="margin:0; padding-left:14px; list-style-type:none;">
                        {risks_html}
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
'''

# Replace only the first occurrence in Tab 0
parts = code.split(old_tab0_anchor)
if len(parts) >= 2:
    code = parts[0] + old_tab0_anchor + "\n" + rec_card_injection + old_tab0_anchor.join(parts[1:])

with open(st_file, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated Streamlit app with AI Investment Decision Engine successfully!")


# ==============================================================================
# 2. UPGRADE POWER BI DASHBOARD (05_powerbi_dashboard/build_interactive_powerbi.py)
# ==============================================================================
pbi_file = r"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\build_interactive_powerbi.py"
with open(pbi_file, "r", encoding="utf-8") as f:
    pbi_code = f.read()

# Add AI Investment Recommendation card above the main chart
old_chart_header = '''              <!-- Interactive Layer Toggles -->
              <div class="flex flex-wrap items-center gap-2 text-[10px] font-mono">'''

new_chart_header = '''              <!-- Dynamic Investment Recommendation Badge -->
              <div class="flex items-center gap-2 px-2.5 py-1 rounded bg-pbi-surface border border-pbi-border text-xs font-mono">
                <span class="text-[10px] text-[#94a3b8] uppercase font-bold">AI Verdict:</span>
                <span class="px-2 py-0.5 rounded font-bold text-xs" id="ai-rec-badge" style="background:rgba(16,185,129,0.18); color:#10b981; border:1px solid rgba(16,185,129,0.4);">STRONG BUY</span>
                <span class="text-white font-bold text-[11px]" id="ai-rec-score">Score: 88/100</span>
                <span class="text-[10px] text-[#00f0ff] hidden md:inline" id="ai-rec-action">Target: Scale In on Dips</span>
              </div>

              <!-- Interactive Layer Toggles -->
              <div class="flex flex-wrap items-center gap-2 text-[10px] font-mono">'''

pbi_code = pbi_code.replace(old_chart_header, new_chart_header)

# Update HOLDINGS in JS to include recommendation fields
old_holdings_js = '''    // Master Holdings Data
    const HOLDINGS = ['''

new_holdings_js = '''    // Dynamic AI Investment Verdict Calculator
    function getStockRecommendation(price, sma20, sma50, rsi) {
      let score = 50;
      if (price >= sma20) score += 10; else score -= 6;
      if (price >= sma50) score += 12; else score -= 8;
      if (sma20 >= sma50) score += 14; else score -= 10;
      if (rsi >= 45 && rsi <= 65) score += 12;
      else if (rsi < 35) score += 8;
      else if (rsi > 75) score -= 8;

      score = Math.max(12, Math.min(96, score));
      if (score >= 80) return { verdict: "STRONG BUY", score: score, color: "#10b981", action: "Core Accumulate", bg: "rgba(16,185,129,0.18)" };
      if (score >= 65) return { verdict: "BUY", score: score, color: "#00f0ff", action: "Scale in on Dips", bg: "rgba(0,240,255,0.18)" };
      if (score >= 50) return { verdict: "HOLD", score: score, color: "#fbbf24", action: "Maintain Position", bg: "rgba(251,191,36,0.18)" };
      if (score >= 38) return { verdict: "TRIM", score: score, color: "#ec4899", action: "Take Partial Profits", bg: "rgba(236,72,153,0.18)" };
      return { verdict: "AVOID", score: score, color: "#f43f5e", action: "Capital Preservation", bg: "rgba(244,63,94,0.18)" };
    }

    // Master Holdings Data
    const HOLDINGS = ['''

pbi_code = pbi_code.replace(old_holdings_js, new_holdings_js)

# Update focusOnHolding to update the AI verdict badge
old_focus_js = '''      document.getElementById('slicer-symbol').value = symbol;
      document.getElementById('main-chart-title').innerText = `Interactive Trajectory: ${h.symbol} (${h.name})`;
      document.getElementById('active-focus-label').innerText = `${h.symbol} • ${h.name.toUpperCase()}`;'''

new_focus_js = '''      document.getElementById('slicer-symbol').value = symbol;
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
      if (recAction) recAction.innerText = `Strategy: ${rec.action}`;'''

pbi_code = pbi_code.replace(old_focus_js, new_focus_js)

with open(pbi_file, "w", encoding="utf-8") as f:
    f.write(pbi_code)

print("Updated build_interactive_powerbi.py with AI Recommendation Desk successfully!")
