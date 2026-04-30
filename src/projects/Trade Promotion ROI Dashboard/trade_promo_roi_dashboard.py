"""
Trade Promotion ROI Dashboard
- Portfolio overview: spend, incremental revenue, ROI, baseline vs promoted volume
- Promo calendar heatmap (monthly × SKU)
- Drill-down by mechanic (TPR, Display, Feature, Bundle)
- Waterfall: incremental margin bridge
- ROI optimizer: simulate a spend reallocation
Commercial POV: ProClean FMCG portfolio, 5 SKUs, 4 mechanics, 12 months
"""
import os, json

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

SKUS = [
    {"id":"s1","name":"ProClean 500g",    "segment":"Core",    "base_price":4.20, "cogs_pct":0.42},
    {"id":"s2","name":"ProClean 1kg",     "segment":"Core",    "base_price":7.80, "cogs_pct":0.40},
    {"id":"s3","name":"ProClean Ultra 500g","segment":"Premium","base_price":5.90,"cogs_pct":0.38},
    {"id":"s4","name":"ProClean Ultra 1kg","segment":"Premium","base_price":10.50,"cogs_pct":0.36},
    {"id":"s5","name":"ProClean Eco 750g", "segment":"Eco",    "base_price":6.60, "cogs_pct":0.44},
]

MECHANICS = [
    {"id":"tpr",     "name":"Temporary Price Reduction","short":"TPR",    "color":"#7C3AED"},
    {"id":"display", "name":"Secondary Display",        "short":"Display","color":"#2563EB"},
    {"id":"feature", "name":"Feature / Leaflet",        "short":"Feature","color":"#059669"},
    {"id":"bundle",  "name":"Multi-Buy Bundle",         "short":"Bundle", "color":"#D97706"},
]

# Per-event data: sku, month(0-based), mechanic, spend($), baseline_vol, promo_vol, promo_price
EVENTS = [
    # s1 ProClean 500g
    {"sku":"s1","month":0, "mech":"tpr",    "spend":18000,"base_vol":68000,"promo_vol":98000,"pp":3.78},
    {"sku":"s1","month":2, "mech":"display","spend":12000,"base_vol":65000,"promo_vol":82000,"pp":4.20},
    {"sku":"s1","month":4, "mech":"feature","spend":22000,"base_vol":70000,"promo_vol":108000,"pp":3.99},
    {"sku":"s1","month":6, "mech":"tpr",    "spend":20000,"base_vol":72000,"promo_vol":103000,"pp":3.78},
    {"sku":"s1","month":8, "mech":"bundle", "spend":15000,"base_vol":69000,"promo_vol":91000,"pp":3.99},
    {"sku":"s1","month":10,"mech":"display","spend":13000,"base_vol":71000,"promo_vol":88000,"pp":4.20},
    # s2 ProClean 1kg
    {"sku":"s2","month":1, "mech":"tpr",    "spend":24000,"base_vol":49000,"promo_vol":72000,"pp":7.02},
    {"sku":"s2","month":3, "mech":"feature","spend":28000,"base_vol":51000,"promo_vol":82000,"pp":7.41},
    {"sku":"s2","month":5, "mech":"display","spend":14000,"base_vol":52000,"promo_vol":66000,"pp":7.80},
    {"sku":"s2","month":7, "mech":"tpr",    "spend":26000,"base_vol":53000,"promo_vol":78000,"pp":7.02},
    {"sku":"s2","month":9, "mech":"bundle", "spend":18000,"base_vol":50000,"promo_vol":68000,"pp":7.41},
    {"sku":"s2","month":11,"mech":"feature","spend":30000,"base_vol":54000,"promo_vol":88000,"pp":7.02},
    # s3 ProClean Ultra 500g
    {"sku":"s3","month":0, "mech":"display","spend":10000,"base_vol":24000,"promo_vol":32000,"pp":5.90},
    {"sku":"s3","month":3, "mech":"tpr",    "spend":14000,"base_vol":25000,"promo_vol":36000,"pp":5.31},
    {"sku":"s3","month":6, "mech":"bundle", "spend":12000,"base_vol":26000,"promo_vol":34000,"pp":5.61},
    {"sku":"s3","month":9, "mech":"feature","spend":16000,"base_vol":25000,"promo_vol":38000,"pp":5.60},
    # s4 ProClean Ultra 1kg
    {"sku":"s4","month":2, "mech":"tpr",    "spend":11000,"base_vol":15000,"promo_vol":20000,"pp":9.45},
    {"sku":"s4","month":5, "mech":"display","spend":9000, "base_vol":16000,"promo_vol":21000,"pp":10.50},
    {"sku":"s4","month":8, "mech":"feature","spend":13000,"base_vol":15000,"promo_vol":22000,"pp":9.98},
    {"sku":"s4","month":11,"mech":"bundle", "spend":10000,"base_vol":16000,"promo_vol":22000,"pp":9.98},
    # s5 ProClean Eco 750g
    {"sku":"s5","month":1, "mech":"feature","spend":8000, "base_vol":11000,"promo_vol":16000,"pp":6.27},
    {"sku":"s5","month":4, "mech":"display","spend":7000, "base_vol":11000,"promo_vol":14000,"pp":6.60},
    {"sku":"s5","month":7, "mech":"tpr",    "spend":9000, "base_vol":11000,"promo_vol":16000,"pp":5.94},
    {"sku":"s5","month":10,"mech":"bundle", "spend":8000, "base_vol":12000,"promo_vol":16000,"pp":6.27},
]

# Derive computed fields for each event
for e in EVENTS:
    sku = next(s for s in SKUS if s["id"]==e["sku"])
    e["incr_vol"]   = e["promo_vol"] - e["base_vol"]
    e["base_rev"]   = round(e["base_vol"]  * sku["base_price"], 0)
    e["promo_rev"]  = round(e["promo_vol"] * e["pp"], 0)
    e["incr_rev"]   = round(e["promo_rev"] - e["base_rev"], 0)
    gm              = 1 - sku["cogs_pct"]
    e["base_gp"]    = round(e["base_rev"]  * gm, 0)
    e["promo_gp"]   = round(e["promo_rev"] * gm, 0)
    e["incr_gp"]    = round(e["promo_gp"]  - e["base_gp"], 0)
    e["net_incr_gp"]= round(e["incr_gp"]   - e["spend"], 0)
    e["roi"]        = round((e["incr_gp"] - e["spend"]) / e["spend"] * 100, 1) if e["spend"] else 0
    e["uplift_pct"] = round(e["incr_vol"] / e["base_vol"] * 100, 1)

DATA = {"skus": SKUS, "mechanics": MECHANICS, "months": MONTHS, "events": EVENTS}
DATA_JSON = json.dumps(DATA)

# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trade Promotion ROI Dashboard</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:13.5px}}
:root{{
  --bg:#F0FDF4;--surface:#fff;--surface2:#F7FEF9;--surface3:#ECFDF5;
  --border:#BBF7D0;--border-s:#D1FAE5;
  --g950:#052E16;--g900:#064E3B;--g800:#065F46;--g700:#047857;
  --g600:#059669;--g500:#10B981;--g400:#34D399;--g300:#6EE7B7;
  --g200:#A7F3D0;--g100:#D1FAE5;--g50:#ECFDF5;
  --acc:#059669;--acc-l:#34D399;
  --pos:#059669;--pos-bg:#ECFDF5;
  --neg:#DC2626;--neg-bg:#FFF0F0;
  --warn:#D97706;--warn-bg:#FFFBEB;
  --mech-tpr:#7C3AED;--mech-display:#2563EB;--mech-feature:#059669;--mech-bundle:#D97706;
  --text:#052E16;--tmid:#065F46;--tmuted:#4B7C64;--tfaint:#86A899;
  --sh:0 1px 4px rgba(5,46,22,.07);--sh-lg:0 4px 20px rgba(5,46,22,.10);
  --r:10px;
}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh;}}

/* ── HEADER ── */
.hdr{{
  background:linear-gradient(135deg,var(--g950) 0%,var(--g800) 55%,var(--g600) 100%);
  padding:20px 28px;display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:12px;border-bottom:3px solid var(--g600);
  box-shadow:0 4px 24px rgba(5,46,22,.35);
}}
.hdr-title{{font-size:18px;font-weight:800;letter-spacing:-.3px;
  background:linear-gradient(90deg,#fff 40%,var(--g300));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.hdr-sub{{font-size:11px;color:rgba(255,255,255,.40);margin-top:2px;}}
.hdr-badges{{display:flex;gap:7px;align-items:center;flex-wrap:wrap;}}
.hdr-badge{{font-size:10.5px;font-weight:600;color:rgba(255,255,255,.60);
  background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.14);
  border-radius:20px;padding:3px 12px;}}
.hdr-badge.acc{{color:var(--g200);background:rgba(16,185,129,.28);border-color:rgba(110,231,183,.25);}}

/* ── NAV TABS ── */
.tab-nav{{background:var(--surface);border-bottom:2px solid var(--border-s);
  overflow-x:auto;scrollbar-width:none;box-shadow:0 2px 8px rgba(5,46,22,.05);}}
.tab-nav::-webkit-scrollbar{{display:none;}}
.tab-inner{{display:flex;padding:0 22px;min-width:100%;}}
.tab-btn{{display:flex;align-items:center;gap:6px;padding:0 18px;height:44px;
  font-size:12px;font-weight:600;color:var(--tmuted);background:none;border:none;
  cursor:pointer;white-space:nowrap;border-bottom:3px solid transparent;
  margin-bottom:-2px;transition:color .15s,border-color .15s,background .15s;letter-spacing:.1px;}}
.tab-btn:hover{{color:var(--g600);background:var(--g50);}}
.tab-btn.active{{color:var(--g600);border-bottom-color:var(--g500);background:var(--g50);}}
.tab-btn svg{{width:14px;height:14px;opacity:.5;flex-shrink:0;transition:opacity .15s;}}
.tab-btn:hover svg,.tab-btn.active svg{{opacity:1;}}
.tab-kpi-gap{{height:14px;background:var(--bg);}}

/* ── KPI STRIP ── */
.kpi-strip{{display:grid;grid-template-columns:repeat(6,1fr);
  background:var(--surface);margin:0 16px;border-radius:var(--r);
  overflow:hidden;box-shadow:var(--sh-lg);border:1px solid var(--border-s);
  margin-bottom:16px;}}
.kpi-card{{padding:13px 16px 11px;border-right:1px solid var(--border-s);
  position:relative;overflow:hidden;cursor:default;transition:background .15s;}}
.kpi-card:last-child{{border-right:none;}}
.kpi-card:hover{{background:var(--g50);}}
.kpi-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--kpi-clr,var(--g400));}}
.kpi-lbl{{font-size:9.5px;font-weight:700;color:var(--tfaint);text-transform:uppercase;letter-spacing:.7px;margin-bottom:5px;}}
.kpi-val{{font-size:17px;font-weight:800;color:var(--text);letter-spacing:-.2px;}}
.kpi-sub{{font-size:10px;color:var(--tfaint);margin-top:2px;}}
.kpi-badge{{display:inline-flex;align-items:center;gap:2px;font-size:10px;font-weight:700;
  border-radius:20px;padding:2px 7px;margin-top:5px;}}
.bdg-pos{{background:var(--pos-bg);color:var(--pos);border:1px solid #6EE7B7;}}
.bdg-neg{{background:var(--neg-bg);color:var(--neg);border:1px solid #FCA5A5;}}
.bdg-warn{{background:var(--warn-bg);color:var(--warn);border:1px solid #FDE68A;}}
.bdg-neutral{{background:var(--g100);color:var(--g700);border:1px solid var(--g200);}}

/* ── MAIN ── */
.main{{padding:0 16px 28px;max-width:1700px;margin:0 auto;}}
.tab-panel{{display:none;}}.tab-panel.active{{display:block;}}

/* ── PAGE TITLE ROW ── */
.page-hdr{{display:flex;justify-content:space-between;align-items:center;
  margin-bottom:14px;padding-top:2px;}}
.page-title{{font-size:11px;font-weight:800;color:var(--g800);text-transform:uppercase;
  letter-spacing:.7px;display:flex;align-items:center;gap:7px;}}
.page-title::before{{content:'';display:inline-block;width:3px;height:14px;
  background:linear-gradient(180deg,var(--g500),var(--g300));border-radius:2px;flex-shrink:0;}}
.page-note{{font-size:11px;color:var(--tfaint);}}

/* ── GRID ── */
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;}}
.g12{{display:grid;grid-template-columns:1fr 2fr;gap:14px;margin-bottom:14px;}}
.g21{{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;}}
.g1{{margin-bottom:14px;}}

/* ── CARD ── */
.card{{background:var(--surface);border:1px solid var(--border-s);border-radius:var(--r);
  padding:16px;box-shadow:var(--sh);min-width:0;}}
.card-title{{font-size:10.5px;font-weight:700;color:var(--tmuted);text-transform:uppercase;
  letter-spacing:.4px;margin-bottom:12px;display:flex;justify-content:space-between;
  align-items:flex-start;gap:8px;flex-wrap:wrap;border-bottom:1px solid var(--border-s);
  padding-bottom:10px;}}
.card-title-txt{{display:flex;align-items:center;gap:6px;}}
.card-title-txt::before{{content:'';width:3px;height:11px;border-radius:2px;
  background:var(--g500);display:inline-block;flex-shrink:0;}}

/* ── CHART AREA ── */
.chart-area{{width:100%;}}
.chart-area svg{{display:block;width:100%;height:auto;}}
.legend{{display:flex;gap:8px;flex-wrap:wrap;}}
.lg-i{{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--tfaint);font-weight:600;}}
.lg-dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0;}}
.lg-sq{{width:10px;height:10px;border-radius:2px;flex-shrink:0;}}
.lg-ln{{width:14px;height:2px;border-radius:2px;flex-shrink:0;}}

/* ── TABLES ── */
.data-tbl{{width:100%;border-collapse:collapse;font-size:12px;}}
.data-tbl th{{background:var(--g800);color:rgba(255,255,255,.82);padding:8px 12px;
  font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;
  text-align:left;white-space:nowrap;border-right:1px solid rgba(255,255,255,.07);}}
.data-tbl th:last-child{{border-right:none;}}
.data-tbl td{{padding:8px 12px;border-bottom:1px solid var(--border-s);white-space:nowrap;vertical-align:middle;}}
.data-tbl tr:last-child td{{border-bottom:none;}}
.data-tbl tr:hover td{{background:var(--g50);}}
.data-tbl th:not(:first-child),.data-tbl td:not(:first-child){{text-align:right;}}
.data-tbl td:first-child{{text-align:left;}}
.seg-tag{{display:inline-block;font-size:9px;font-weight:700;border-radius:20px;padding:1px 7px;}}
.seg-core{{background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;}}
.seg-prem{{background:#F5F3FF;color:#7C3AED;border:1px solid #DDD6FE;}}
.seg-eco{{background:#ECFDF5;color:#059669;border:1px solid #6EE7B7;}}
.mech-tag{{display:inline-block;font-size:9px;font-weight:700;border-radius:20px;padding:1px 8px;white-space:nowrap;}}
.pos-val{{color:var(--pos);font-weight:700;}}
.neg-val{{color:var(--neg);font-weight:700;}}
.warn-val{{color:var(--warn);font-weight:700;}}
.bold-row td{{font-weight:800;background:var(--g50)!important;}}

/* ── ROI BAR CELL ── */
.roi-bar-wrap{{display:flex;align-items:center;gap:6px;min-width:100px;}}
.roi-bg{{flex:1;height:6px;background:var(--border-s);border-radius:3px;overflow:hidden;}}
.roi-fill{{height:100%;border-radius:3px;}}

/* ── INSIGHT PILLS ── */
.insight-row{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;}}
.insight-card{{background:var(--surface);border:1px solid var(--border-s);
  border-radius:var(--r);padding:11px 14px;display:flex;align-items:flex-start;
  gap:10px;flex:1;min-width:220px;box-shadow:var(--sh);}}
.insight-icon{{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;
  justify-content:center;flex-shrink:0;font-size:15px;}}
.insight-txt strong{{font-size:11.5px;font-weight:700;color:var(--text);display:block;margin-bottom:2px;}}
.insight-txt span{{font-size:10.5px;color:var(--tmuted);line-height:1.5;}}

/* ── CALENDAR HEATMAP ── */
.cal-wrap{{overflow-x:auto;}}
.cal-tbl{{border-collapse:collapse;font-size:11px;min-width:100%;}}
.cal-tbl th{{background:var(--g800);color:rgba(255,255,255,.72);
  padding:6px 10px;font-size:9px;font-weight:700;text-transform:uppercase;
  letter-spacing:.3px;text-align:center;border-right:1px solid rgba(255,255,255,.07);
  white-space:nowrap;}}
.cal-tbl th:first-child{{text-align:left;min-width:160px;}}
.cal-tbl .row-hdr{{background:var(--surface2);font-weight:700;color:var(--g700);
  padding:8px 12px;font-size:10.5px;border-right:1px solid var(--border);
  border-bottom:1px solid var(--border-s);text-align:left;white-space:nowrap;}}
.cal-tbl td{{padding:0;border-right:1px solid var(--border-s);border-bottom:1px solid var(--border-s);}}
.cal-tbl tr:last-child td{{border-bottom:none;}}
.cal-cell{{
  width:72px;height:48px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:default;
  transition:filter .15s;font-size:10px;font-weight:700;gap:2px;
}}
.cal-cell:hover{{filter:brightness(.9);}}
.cal-empty{{background:#F8FAFC;}}
.cal-mech-label{{font-size:8.5px;font-weight:700;border-radius:4px;padding:1px 5px;white-space:nowrap;}}

/* ── WATERFALL ── */
.wf-wrap{{overflow-x:auto;}}

/* ── OPTIMIZER ── */
.opt-grid{{display:grid;grid-template-columns:1.2fr 1fr;gap:14px;margin-bottom:14px;}}
.opt-slider-panel{{background:var(--surface);border:1px solid var(--border-s);border-radius:var(--r);padding:16px;box-shadow:var(--sh);}}
.opt-title{{font-size:10.5px;font-weight:700;color:var(--tmuted);text-transform:uppercase;
  letter-spacing:.4px;margin-bottom:14px;border-bottom:1px solid var(--border-s);padding-bottom:10px;
  display:flex;align-items:center;gap:6px;}}
.opt-title::before{{content:'';width:3px;height:11px;border-radius:2px;
  background:var(--g500);display:inline-block;flex-shrink:0;}}
.budget-total{{display:flex;justify-content:space-between;align-items:center;
  background:var(--g50);border:1px solid var(--g100);border-radius:8px;
  padding:10px 14px;margin-bottom:14px;}}
.budget-lbl{{font-size:10px;font-weight:700;color:var(--tmuted);text-transform:uppercase;letter-spacing:.4px;}}
.budget-val{{font-size:15px;font-weight:800;color:var(--g700);}}
.budget-remaining{{font-size:10px;font-weight:700;border-radius:20px;padding:2px 9px;}}
.sku-alloc{{margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid var(--border-s);}}
.sku-alloc:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0;}}
.sku-alloc-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;gap:8px;flex-wrap:wrap;}}
.sku-alloc-name{{font-size:11.5px;font-weight:700;color:var(--text);}}
.sku-alloc-meta{{font-size:10px;color:var(--tfaint);}}
.alloc-slider-row{{display:flex;align-items:center;gap:10px;}}
.alloc-lbl{{font-size:9.5px;color:var(--tfaint);font-weight:600;width:36px;text-align:right;flex-shrink:0;}}
input[type=range]{{
  flex:1;height:4px;border-radius:4px;cursor:pointer;
  accent-color:var(--g600);background:var(--g200);outline:none;
  -webkit-appearance:none;appearance:none;
}}
input[type=range]::-webkit-slider-thumb{{
  -webkit-appearance:none;width:16px;height:16px;border-radius:50%;
  background:var(--g600);border:2px solid #fff;
  box-shadow:0 0 0 2px var(--g300),0 2px 6px rgba(5,150,105,.3);cursor:pointer;
}}
.alloc-val{{font-size:12px;font-weight:700;color:var(--g700);width:58px;text-align:left;flex-shrink:0;}}
.reset-btn{{
  margin-top:14px;width:100%;padding:8px;
  background:var(--g100);border:1px solid var(--g200);border-radius:7px;
  font-size:11.5px;font-weight:700;color:var(--g700);cursor:pointer;
  transition:all .15s;
}}
.reset-btn:hover{{background:var(--g200);color:var(--g800);}}

/* ── TOOLTIP ── */
.tt{{position:fixed;pointer-events:none;background:var(--g900);color:#fff;
  font-size:11px;padding:6px 10px;border-radius:7px;opacity:0;transition:opacity .1s;
  z-index:999;max-width:240px;line-height:1.5;font-weight:600;
  box-shadow:0 4px 16px rgba(5,46,22,.25);}}
.tt.vis{{opacity:1;}}

/* ── FOOTER ── */
.footer{{text-align:center;padding:14px;font-size:11px;color:var(--tfaint);
  border-top:1px solid var(--border-s);background:var(--surface);margin-top:8px;}}

/* ── RESPONSIVE ── */
@media(max-width:1200px){{.kpi-strip{{grid-template-columns:repeat(3,1fr);}}}}
@media(max-width:900px){{
  .g2,.g3,.g12,.g21,.opt-grid{{grid-template-columns:1fr;}}
  .kpi-strip{{grid-template-columns:1fr 1fr;margin:0 8px;}}
}}
</style>
</head>
<body>

<div class="tt" id="tt"></div>

<header class="hdr">
  <div>
    <div class="hdr-title">Trade Promotion ROI Dashboard</div>
    <div class="hdr-sub">ProClean FMCG Portfolio &nbsp;&middot;&nbsp; 5 SKUs &middot; 4 Mechanics &middot; Full Year &nbsp;&middot;&nbsp; Spend &rarr; Incremental Margin</div>
  </div>
  <div class="hdr-badges">
    <span class="hdr-badge acc">&#9650; Commercial Intelligence</span>
    <span class="hdr-badge">24 Promo Events</span>
    <span class="hdr-badge">Demo Data</span>
  </div>
</header>

<nav class="tab-nav">
  <div class="tab-inner">
    <button class="tab-btn active" onclick="switchTab('overview',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M1 11l4-4 3 3 4-5 3 2V14H1v-3z"/></svg>
      Portfolio Overview
    </button>
    <button class="tab-btn" onclick="switchTab('calendar',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><rect x="1" y="3" width="14" height="11" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M5 1v3m6-3v3M1 7h14"/></svg>
      Promo Calendar
    </button>
    <button class="tab-btn" onclick="switchTab('mechanic',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M2 12h3V6H2v6zm4 0h3V4H6v8zm4 0h3V8h-3v4z"/></svg>
      By Mechanic
    </button>
    <button class="tab-btn" onclick="switchTab('waterfall',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M1 14V2l3 4 3-2 3 5 3-3v8H1z"/></svg>
      Margin Waterfall
    </button>
    <button class="tab-btn" onclick="switchTab('optimizer',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 5v3l2 2"/></svg>
      ROI Optimizer
    </button>
  </div>
</nav>
<div class="tab-kpi-gap"></div>

<div class="main">

  <!-- KPI STRIP -->
  <div class="kpi-strip" id="kpi-strip"></div>

  <!-- ═══ OVERVIEW TAB ═══ -->
  <div class="tab-panel active" id="tab-overview">
    <div class="insight-row" id="insight-row"></div>
    <div class="g2">
      <div class="card">
        <div class="card-title">
          <div class="card-title-txt">ROI by SKU (Net Incremental GP / Spend)</div>
          <div class="legend" id="lg-sku-roi"></div>
        </div>
        <div class="chart-area" id="c-sku-roi"></div>
      </div>
      <div class="card">
        <div class="card-title">
          <div class="card-title-txt">Spend vs Incremental GP by Mechanic</div>
          <div class="legend" id="lg-mech-bubble"></div>
        </div>
        <div class="chart-area" id="c-mech-bubble"></div>
      </div>
    </div>
    <div class="g2">
      <div class="card">
        <div class="card-title">
          <div class="card-title-txt">Monthly Spend &amp; Incremental Revenue</div>
          <div class="legend">
            <div class="lg-i"><div class="lg-sq" style="background:#059669;opacity:.8"></div>Incr. Revenue</div>
            <div class="lg-i"><div class="lg-sq" style="background:#DC2626;opacity:.7"></div>Promo Spend</div>
            <div class="lg-i"><div class="lg-ln" style="background:#065F46"></div>Cum. ROI %</div>
          </div>
        </div>
        <div class="chart-area" id="c-monthly"></div>
      </div>
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Volume Uplift % by Promo Event</div></div>
        <div class="chart-area" id="c-uplift"></div>
      </div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">All Promo Events Summary</div>
          <span style="font-size:10px;color:var(--tfaint)">Sorted by ROI descending</span>
        </div>
        <div id="events-table"></div>
      </div>
    </div>
  </div>

  <!-- ═══ CALENDAR TAB ═══ -->
  <div class="tab-panel" id="tab-calendar">
    <div class="page-hdr">
      <div class="page-title">Promo Calendar Heatmap</div>
      <div class="page-note">Colour = mechanic &nbsp;|&nbsp; Value = ROI %</div>
    </div>
    <div class="g1 card">
      <div class="card-title">
        <div class="card-title-txt">SKU × Month Activity Map</div>
        <div class="legend" id="cal-legend"></div>
      </div>
      <div class="cal-wrap" id="cal-heatmap"></div>
    </div>
    <div class="g2">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Events per Month</div></div>
        <div class="chart-area" id="c-events-month"></div>
      </div>
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Spend Distribution by Month</div></div>
        <div class="chart-area" id="c-spend-month"></div>
      </div>
    </div>
  </div>

  <!-- ═══ MECHANIC TAB ═══ -->
  <div class="tab-panel" id="tab-mechanic">
    <div class="page-hdr">
      <div class="page-title">Performance by Promo Mechanic</div>
    </div>
    <div class="g2">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">ROI by Mechanic</div></div>
        <div class="chart-area" id="c-mech-roi"></div>
      </div>
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Avg Volume Uplift % by Mechanic</div></div>
        <div class="chart-area" id="c-mech-uplift"></div>
      </div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Mechanic Detail Table</div></div>
        <div id="mech-table"></div>
      </div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Event-Level Detail by Mechanic</div></div>
        <div id="mech-events-table"></div>
      </div>
    </div>
  </div>

  <!-- ═══ WATERFALL TAB ═══ -->
  <div class="tab-panel" id="tab-waterfall">
    <div class="page-hdr">
      <div class="page-title">Incremental Margin Waterfall</div>
      <div class="page-note">Baseline GP &rarr; Promoted GP &rarr; Less Spend &rarr; Net Incremental GP</div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Portfolio-Level Margin Bridge (Full Year)</div></div>
        <div class="chart-area" id="c-waterfall-portfolio"></div>
      </div>
    </div>
    <div class="g2">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Net Incremental GP by SKU</div></div>
        <div class="chart-area" id="c-net-gp-sku"></div>
      </div>
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Spend Efficiency (Incr. GP per $1 Spent)</div></div>
        <div class="chart-area" id="c-efficiency"></div>
      </div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">SKU-Level Waterfall Summary</div></div>
        <div id="wf-sku-table"></div>
      </div>
    </div>
  </div>

  <!-- ═══ OPTIMIZER TAB ═══ -->
  <div class="tab-panel" id="tab-optimizer">
    <div class="page-hdr">
      <div class="page-title">ROI Optimizer — Reallocate Promo Budget</div>
      <div class="page-note">Adjust spend per SKU; projected impact recalculates using historical ROI rates</div>
    </div>
    <div class="opt-grid">
      <div class="opt-slider-panel">
        <div class="opt-title">Budget Allocation by SKU</div>
        <div class="budget-total">
          <div>
            <div class="budget-lbl">Total Budget</div>
            <div class="budget-val" id="opt-total-budget">$0</div>
          </div>
          <div style="text-align:right">
            <div class="budget-lbl">Remaining</div>
            <div class="budget-remaining bdg-pos" id="opt-remaining">$0</div>
          </div>
        </div>
        <div id="opt-sliders"></div>
        <button class="reset-btn" onclick="resetOptimizer()">&#8635; Reset to Historical Actuals</button>
      </div>
      <div class="card" style="margin-bottom:0">
        <div class="card-title"><div class="card-title-txt">Projected vs Historical Performance</div></div>
        <div class="chart-area" id="c-opt-compare"></div>
      </div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-title"><div class="card-title-txt">Optimizer Output Table</div></div>
        <div id="opt-table"></div>
      </div>
    </div>
  </div>

</div>
<div class="footer">Developed by <strong>Musab Shaikh</strong> &nbsp;&bull;&nbsp; JBS | Seara | Commercial Intelligence &nbsp;&bull;&nbsp; 2026</div>

<script>
// ─────────────────────────────── DATA ────────────────────────────────────────
const D = {DATA_JSON};
const SKUS = D.skus;
const MECHS = D.mechanics;
const MONTHS = D.months;
const EVENTS = D.events;

// ─────────────────────────────── HELPERS ─────────────────────────────────────
const $ = id => document.getElementById(id);
const fmtUSD  = v => '$' + (Math.abs(v)>=1e6 ? (v/1e6).toFixed(2)+'M' : Math.abs(v)>=1e3 ? (v/1e3).toFixed(1)+'K' : v.toFixed(0));
const fmtPct  = v => (v>=0?'+':'')+v.toFixed(1)+'%';
const fmtVol  = v => v>=1e6?(v/1e6).toFixed(2)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':v.toFixed(0);
const clamp   = (v,a,b)=>Math.max(a,Math.min(b,v));

function mechColor(id){{return MECHS.find(m=>m.id===id)?.color||'#94A3B8';}}
function mechShort(id){{return MECHS.find(m=>m.id===id)?.short||id;}}
function skuName(id){{return SKUS.find(s=>s.id===id)?.name||id;}}
function skuSeg(id){{return SKUS.find(s=>s.id===id)?.segment||'';}}
function segClass(s){{return {{Core:'seg-core',Premium:'seg-prem',Eco:'seg-eco'}}[s]||'';}}
function roiClass(r){{return r>=80?'pos-val':r>=30?'warn-val':'neg-val';}}

// Tooltip
const ttEl = $('tt');
let ttTimer;
function showTT(txt,e){{
  ttEl.innerHTML=txt; ttEl.classList.add('vis');
  moveTT(e);
}}
function moveTT(e){{
  const x=e.clientX+14, y=e.clientY-32;
  ttEl.style.left=x+'px'; ttEl.style.top=y+'px';
}}
function hideTT(){{ttEl.classList.remove('vis');}}

// Tab switching
function switchTab(id,btn){{
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  $('tab-'+id).classList.add('active');
  btn.classList.add('active');
}}

// ─────────────────────────────── AGGREGATIONS ────────────────────────────────
function sumEvents(filter){{
  const evs = filter ? EVENTS.filter(filter) : EVENTS;
  return {{
    spend:     evs.reduce((a,e)=>a+e.spend,0),
    incr_rev:  evs.reduce((a,e)=>a+e.incr_rev,0),
    incr_gp:   evs.reduce((a,e)=>a+e.incr_gp,0),
    net_incr_gp: evs.reduce((a,e)=>a+e.net_incr_gp,0),
    base_rev:  evs.reduce((a,e)=>a+e.base_rev,0),
    promo_rev: evs.reduce((a,e)=>a+e.promo_rev,0),
    base_gp:   evs.reduce((a,e)=>a+e.base_gp,0),
    promo_gp:  evs.reduce((a,e)=>a+e.promo_gp,0),
    incr_vol:  evs.reduce((a,e)=>a+e.incr_vol,0),
    count:     evs.length,
    roi: evs.reduce((a,e)=>a+e.spend,0)>0
      ? (evs.reduce((a,e)=>a+e.incr_gp,0)-evs.reduce((a,e)=>a+e.spend,0))
        / evs.reduce((a,e)=>a+e.spend,0)*100
      : 0,
  }};
}}

// ─────────────────────────────── KPI STRIP ───────────────────────────────────
function renderKPIs(){{
  const tot = sumEvents();
  const kpis = [
    {{lbl:'Total Promo Spend', val:fmtUSD(tot.spend), sub:'24 events · FY',
      bdg:'', clr:'var(--g700)'}},
    {{lbl:'Incremental Revenue', val:fmtUSD(tot.incr_rev), sub:'Promoted − baseline',
      bdg:`<span class="kpi-badge bdg-pos">&#9650; ${{fmtPct(tot.incr_rev/tot.base_rev*100)}} of base</span>`,
      clr:'var(--g500)'}},
    {{lbl:'Incremental GP', val:fmtUSD(tot.incr_gp), sub:'Gross margin uplift',
      bdg:'', clr:'var(--g400)'}},
    {{lbl:'Net Incremental GP', val:fmtUSD(tot.net_incr_gp), sub:'After spend deduction',
      bdg: tot.net_incr_gp>=0
        ? `<span class="kpi-badge bdg-pos">&#9650; Positive</span>`
        : `<span class="kpi-badge bdg-neg">&#9660; Below spend</span>`,
      clr:'var(--g300)'}},
    {{lbl:'Portfolio ROI', val:fmtPct(tot.roi), sub:'Net incr. GP / spend',
      bdg: tot.roi>=50
        ? `<span class="kpi-badge bdg-pos">&#9733; Strong</span>`
        : tot.roi>=0
          ? `<span class="kpi-badge bdg-warn">Moderate</span>`
          : `<span class="kpi-badge bdg-neg">Negative</span>`,
      clr:'#D97706'}},
    {{lbl:'Avg Volume Uplift', val:fmtPct(EVENTS.reduce((a,e)=>a+e.uplift_pct,0)/EVENTS.length),
      sub:'Per event average', bdg:'', clr:'#2563EB'}},
  ];
  $('kpi-strip').innerHTML = kpis.map((k,i)=>
    `<div class="kpi-card" style="--kpi-clr:${{k.clr}}">
      <div class="kpi-lbl">${{k.lbl}}</div>
      <div class="kpi-val">${{k.val}}</div>
      <div class="kpi-sub">${{k.sub}}</div>
      ${{k.bdg}}
    </div>`
  ).join('');
}}

// ─────────────────────────────── INSIGHTS ────────────────────────────────────
function renderInsights(){{
  const byMech = MECHS.map(m=>{{const s=sumEvents(e=>e.mech===m.id);return {{...m,...s}};}});
  byMech.sort((a,b)=>b.roi-a.roi);
  const best = byMech[0], worst = byMech[byMech.length-1];
  const bySku = SKUS.map(s=>{{const a=sumEvents(e=>e.sku===s.id);return {{...s,...a}};}});
  bySku.sort((a,b)=>b.roi-a.roi);
  const bestSku = bySku[0];
  const avgUplift = EVENTS.reduce((a,e)=>a+e.uplift_pct,0)/EVENTS.length;
  const highUplift = EVENTS.reduce((p,e)=>e.uplift_pct>p.uplift_pct?e:p);

  const cards = [
    {{icon:'🏆', bg:'#ECFDF5', txt:`<strong>Best mechanic: ${{best.short}} (${{fmtPct(best.roi)}} ROI)</strong>
      <span>${{best.name}} delivers the highest net return across ${{best.count}} events</span>`}},
    {{icon:'📦', bg:'#EFF6FF', txt:`<strong>Top SKU: ${{bestSku.name}} (${{fmtPct(bestSku.roi)}} ROI)</strong>
      <span>Highest net incremental GP after spend deduction across all events</span>`}},
    {{icon:'📈', bg:'#FFFBEB', txt:`<strong>Highest uplift: ${{fmtPct(highUplift.uplift_pct)}} volume lift</strong>
      <span>${{skuName(highUplift.sku)}} – ${{MONTHS[highUplift.month]}} via ${{mechShort(highUplift.mech)}}</span>`}},
    {{icon:'⚠️', bg:'#FFF0F0', txt:`<strong>Weakest mechanic: ${{worst.short}} (${{fmtPct(worst.roi)}} ROI)</strong>
      <span>Review ${{worst.name}} events — lowest net return vs spend</span>`}},
  ];
  $('insight-row').innerHTML = cards.map(c=>
    `<div class="insight-card">
      <div class="insight-icon" style="background:${{c.bg}}">${{c.icon}}</div>
      <div class="insight-txt">${{c.txt}}</div>
    </div>`
  ).join('');
}}

// ─────────────────────────────── SVG HELPERS ─────────────────────────────────
function makeSVG(w,h,body){{
  return `<svg viewBox="0 0 ${{w}} ${{h}}" xmlns="http://www.w3.org/2000/svg"
    style="display:block;width:100%;height:auto">${{body}}</svg>`;
}}

function barChart(items, {{width=600,height=220,barW=32,gap=6,colors,labelFn,valFn,gridLines=4,
    labelRot=0, tooltips, showVal=true, yLabel='', secondLine, positiveOnly=false}}={{}}){{
  const n = items.length;
  const vals = items.map(valFn);
  const maxV = Math.max(...vals.map(Math.abs), 1);
  const minV = positiveOnly ? 0 : Math.min(...vals, 0);
  const pad={{l:44,r:14,t:18,b: labelRot ? 72 : 46}};
  const W=width, H=height;
  const plotW = W-pad.l-pad.r, plotH = H-pad.t-pad.b;
  const slotW = plotW / n;
  const bW = Math.min(barW, slotW*0.55);
  const range = maxV - minV || 1;
  const fy = v => pad.t + plotH * (1-(v-minV)/range);
  const zero = fy(0);
  let svg = '';
  // grid
  for(let i=0;i<=gridLines;i++){{
    const y = pad.t + plotH/gridLines*i;
    const v = maxV - range/gridLines*i;
    svg += `<line x1="${{pad.l}}" y1="${{y}}" x2="${{W-pad.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg += `<text x="${{pad.l-4}}" y="${{y+3.5}}" text-anchor="end" font-size="9" fill="#94A3B8">${{valFn?fmtUSD(v):v.toFixed(0)}}</text>`;
  }}
  // zero line
  if(!positiveOnly && minV<0)
    svg += `<line x1="${{pad.l}}" y1="${{zero}}" x2="${{W-pad.r}}" y2="${{zero}}" stroke="#CBD5E1" stroke-width="1.5"/>`;
  // bars
  items.forEach((item,i)=>{{
    const v = vals[i];
    const cx = pad.l + slotW*(i+0.5);
    const x = cx - bW/2;
    const barH = Math.abs(v-0) / range * plotH;
    const y = v>=0 ? zero-barH : zero;
    const col = Array.isArray(colors) ? colors[i%colors.length] : (colors||'#059669');
    const opacity = v<0?'0.75':'0.88';
    svg += `<rect x="${{x}}" y="${{y}}" width="${{bW}}" height="${{Math.max(barH,1)}}" rx="3"
      fill="${{col}}" opacity="${{opacity}}"
      ${{tooltips?`onmouseenter="showTT('${{tooltips[i]}}',event)" onmouseleave="hideTT()" onmousemove="moveTT(event)"`:''}}/>`;
    if(showVal){{
      const ly = v>=0 ? y-4 : y+barH+11;
      svg += `<text x="${{cx}}" y="${{ly}}" text-anchor="middle" font-size="8.5" font-weight="700"
        fill="${{v<0?'#DC2626':'#065F46'}}">${{fmtUSD(v)}}</text>`;
    }}
    // x label
    const lbl = labelFn(item,i);
    if(labelRot){{
      svg += `<text x="${{cx}}" y="${{H-pad.b+14}}" text-anchor="end" font-size="9" fill="#94A3B8"
        transform="rotate(-35 ${{cx}} ${{H-pad.b+14}})">${{lbl}}</text>`;
    }} else {{
      svg += `<text x="${{cx}}" y="${{H-pad.b+13}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{lbl}}</text>`;
      if(secondLine) svg += `<text x="${{cx}}" y="${{H-pad.b+24}}" text-anchor="middle" font-size="8" fill="#CBD5E1">${{secondLine(item,i)}}</text>`;
    }}
  }});
  return makeSVG(W,H,svg);
}}

function hBarChart(items,{{width=500,height=220,labelFn,valFn,colorFn,tooltips,maxVal,trailingFn}}={{}}){{
  const n=items.length;
  const vals=items.map(valFn);
  const maxV=maxVal||Math.max(...vals.map(Math.abs),1);
  const pad={{l:130,r:60,t:10,b:20}};
  const W=width,H=height;
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const rowH=plotH/n;
  const bH=Math.min(rowH*0.55,22);
  let svg='';
  for(let i=0;i<=4;i++){{
    const x=pad.l+plotW/4*i;
    svg+=`<line x1="${{x}}" y1="${{pad.t}}" x2="${{x}}" y2="${{H-pad.b}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{H-pad.b+11}}" text-anchor="middle" font-size="8" fill="#94A3B8">${{fmtUSD(maxV/4*i)}}</text>`;
  }}
  items.forEach((item,i)=>{{
    const v=vals[i];
    const cy=pad.t+rowH*(i+0.5);
    const bY=cy-bH/2;
    const bW=Math.abs(v)/maxV*plotW;
    const col=colorFn?colorFn(item,i):'#059669';
    svg+=`<text x="${{pad.l-6}}" y="${{cy+4}}" text-anchor="end" font-size="9.5" font-weight="600" fill="#334155">${{labelFn(item,i)}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{bY}}" width="${{bW}}" height="${{bH}}" rx="3" fill="${{col}}" opacity=".85"
      ${{tooltips?`onmouseenter="showTT('${{tooltips[i]}}',event)" onmouseleave="hideTT()" onmousemove="moveTT(event)"`:''}}/>`;
    svg+=`<text x="${{pad.l+bW+5}}" y="${{cy+4}}" font-size="9.5" font-weight="700" fill="${{col}}">${{trailingFn?trailingFn(item,i):fmtUSD(v)}}</text>`;
  }});
  return makeSVG(W,H,svg);
}}

// ─────────────────────────────── OVERVIEW TAB ────────────────────────────────
function renderSkuROI(){{
  const bySku = SKUS.map(s=>{{
    const agg=sumEvents(e=>e.sku===s.id);
    return {{...s,...agg}};
  }});
  const colors = bySku.map(s=>s.roi>=80?'#059669':s.roi>=30?'#D97706':'#DC2626');
  const tips = bySku.map(s=>`${{s.name}}<br>ROI: ${{fmtPct(s.roi)}}<br>Spend: ${{fmtUSD(s.spend)}}<br>Net Incr GP: ${{fmtUSD(s.net_incr_gp)}}`);
  $('c-sku-roi').innerHTML = barChart(bySku,{{
    width:600,height:240,barW:44,colors,
    labelFn:s=>s.name.replace('ProClean ',''),
    valFn:s=>s.roi,
    gridLines:4, tooltips:tips, showVal:true,
  }});
  // Replace fmtUSD with fmtPct in y-axis labels
  $('c-sku-roi').innerHTML = $('c-sku-roi').innerHTML.replace(
    /text-anchor="end" font-size="9" fill="#94A3B8">\$[^<]+</g,
    m=>m  // we'll just accept USD for now; grid is approximate
  );
  // Actually redraw properly:
  const n=bySku.length;
  const vals=bySku.map(s=>s.roi);
  const maxV=Math.max(...vals,0)+10;
  const minV=Math.min(...vals,0);
  const pad={{l:40,r:14,t:18,b:46}};
  const W=600,H=240;
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const slotW=plotW/n, bW=40;
  const range=maxV-minV||1;
  const fy=v=>pad.t+plotH*(1-(v-minV)/range);
  const zero=fy(0);
  let svg='';
  for(let i=0;i<=5;i++){{
    const y=pad.t+plotH/5*i;
    const v=maxV-range/5*i;
    svg+=`<line x1="${{pad.l}}" y1="${{y}}" x2="${{W-pad.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-4}}" y="${{y+3.5}}" text-anchor="end" font-size="9" fill="#94A3B8">${{v.toFixed(0)}}%</text>`;
  }}
  if(minV<0) svg+=`<line x1="${{pad.l}}" y1="${{zero}}" x2="${{W-pad.r}}" y2="${{zero}}" stroke="#CBD5E1" stroke-width="1.5"/>`;
  bySku.forEach((s,i)=>{{
    const v=vals[i];
    const cx=pad.l+slotW*(i+0.5);
    const x=cx-bW/2;
    const barH=Math.abs(v)/range*plotH;
    const y=v>=0?zero-barH:zero;
    const col=colors[i];
    svg+=`<rect x="${{x}}" y="${{y}}" width="${{bW}}" height="${{Math.max(barH,2)}}" rx="3" fill="${{col}}" opacity=".88"
      onmouseenter="showTT('${{tips[i]}}',event)" onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg+=`<text x="${{cx}}" y="${{y+(v>=0?-4:barH+11)}}" text-anchor="middle" font-size="9" font-weight="700" fill="${{col}}">${{v.toFixed(0)}}%</text>`;
    svg+=`<text x="${{cx}}" y="${{H-pad.b+13}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{s.name.replace('ProClean ','')}}</text>`;
  }});
  $('c-sku-roi').innerHTML=makeSVG(W,H,svg);
}}

function renderMechBubble(){{
  const byMech = MECHS.map(m=>{{const a=sumEvents(e=>e.mech===m.id);return{{...m,...a}};}});
  // Scatter: x=spend, y=roi, size=incr_rev
  const maxSpend=Math.max(...byMech.map(m=>m.spend));
  const maxRoi  =Math.max(...byMech.map(m=>m.roi))+20;
  const maxR    =Math.max(...byMech.map(m=>m.incr_rev));
  const W=580,H=260;
  const pad={{l:54,r:24,t:20,b:48}};
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  let svg='';
  for(let i=0;i<=4;i++){{
    const x=pad.l+plotW/4*i;
    const y=pad.t+plotH/4*i;
    svg+=`<line x1="${{x}}" y1="${{pad.t}}" x2="${{x}}" y2="${{H-pad.b}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<line x1="${{pad.l}}" y1="${{y}}" x2="${{W-pad.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{H-pad.b+11}}" text-anchor="middle" font-size="8" fill="#94A3B8">${{fmtUSD(maxSpend/4*i)}}</text>`;
    const rv=maxRoi-maxRoi/4*i;
    svg+=`<text x="${{pad.l-4}}" y="${{y+3}}" text-anchor="end" font-size="8" fill="#94A3B8">${{rv.toFixed(0)}}%</text>`;
  }}
  svg+=`<text x="${{pad.l+plotW/2}}" y="${{H-2}}" text-anchor="middle" font-size="9" fill="#94A3B8">Promo Spend →</text>`;
  svg+=`<text x="10" y="${{pad.t+plotH/2}}" text-anchor="middle" font-size="9" fill="#94A3B8" transform="rotate(-90 10 ${{pad.t+plotH/2}})">ROI % →</text>`;
  byMech.forEach(m=>{{
    const x=pad.l+(m.spend/maxSpend)*plotW;
    const y=pad.t+(1-m.roi/maxRoi)*plotH;
    const r=10+20*(m.incr_rev/maxR);
    svg+=`<circle cx="${{x}}" cy="${{y}}" r="${{r}}" fill="${{m.color}}" opacity=".20"/>`;
    svg+=`<circle cx="${{x}}" cy="${{y}}" r="8" fill="${{m.color}}" opacity=".85"
      onmouseenter="showTT('${{m.name}}<br>Spend: ${{fmtUSD(m.spend)}}<br>ROI: ${{fmtPct(m.roi)}}<br>Incr Rev: ${{fmtUSD(m.incr_rev)}}',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg+=`<text x="${{x+r+4}}" y="${{y+4}}" font-size="9.5" font-weight="700" fill="${{m.color}}">${{m.short}}</text>`;
  }});
  $('c-mech-bubble').innerHTML=makeSVG(W,H,svg);
  $('lg-mech-bubble').innerHTML=byMech.map(m=>
    `<div class="lg-i"><div class="lg-dot" style="background:${{m.color}}"></div>${{m.short}}</div>`
  ).join('');
}}

function renderMonthlyChart(){{
  const byMonth=MONTHS.map((_,mi)=>sumEvents(e=>e.month===mi));
  const maxRev=Math.max(...byMonth.map(m=>m.incr_rev),1);
  const maxSpend=Math.max(...byMonth.map(m=>m.spend),1);
  const maxBar=Math.max(maxRev,maxSpend)*1.15;
  const W=620,H=240,pad={{l:50,r:50,t:20,b:36}};
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const slotW=plotW/12;
  const bW=slotW*0.35;
  let svg='', cumRoi=0, cumSpend=0, cumGp=0;
  for(let i=0;i<=4;i++){{
    const y=pad.t+plotH/4*i;
    const v=maxBar-maxBar/4*i;
    svg+=`<line x1="${{pad.l}}" y1="${{y}}" x2="${{W-pad.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-4}}" y="${{y+3}}" text-anchor="end" font-size="8" fill="#94A3B8">${{fmtUSD(v)}}</text>`;
  }}
  let linePoints='';
  byMonth.forEach((m,mi)=>{{
    const cx=pad.l+slotW*(mi+0.5);
    const revH=m.incr_rev/maxBar*plotH;
    const spH=m.spend/maxBar*plotH;
    const y0=pad.t+plotH;
    if(m.count>0){{
      svg+=`<rect x="${{cx-bW-1}}" y="${{y0-revH}}" width="${{bW}}" height="${{revH}}" rx="2" fill="#059669" opacity=".80"
        onmouseenter="showTT('${{MONTHS[mi]}}<br>Incr Rev: ${{fmtUSD(m.incr_rev)}}<br>Spend: ${{fmtUSD(m.spend)}}<br>Events: ${{m.count}}',event)"
        onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
      svg+=`<rect x="${{cx+1}}" y="${{y0-spH}}" width="${{bW}}" height="${{spH}}" rx="2" fill="#DC2626" opacity=".65"
        onmouseenter="showTT('${{MONTHS[mi]}}<br>Spend: ${{fmtUSD(m.spend)}}<br>Incr Rev: ${{fmtUSD(m.incr_rev)}}',event)"
        onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    }}
    cumSpend+=m.spend; cumGp+=m.incr_gp;
    const roi=cumSpend>0?(cumGp-cumSpend)/cumSpend*100:0;
    const ry=pad.t+plotH*(1-clamp(roi,0,200)/200);
    linePoints+=`${{cx}},${{ry}} `;
    svg+=`<text x="${{cx}}" y="${{H-pad.b+12}}" text-anchor="middle" font-size="8.5" fill="#94A3B8">${{MONTHS[mi]}}</text>`;
  }});
  const pts=linePoints.trim().split(' ');
  svg+=`<polyline points="${{pts.join(' ')}}" fill="none" stroke="#065F46" stroke-width="2" stroke-linecap="round"/>`;
  pts.forEach((p,i)=>{{
    if(!byMonth[i]||!byMonth[i].count) return;
    const [x,y]=p.split(',');
    svg+=`<circle cx="${{x}}" cy="${{y}}" r="3.5" fill="#065F46" stroke="#fff" stroke-width="1.5"/>`;
  }});
  // right axis label
  svg+=`<text x="${{W-pad.r+4}}" y="${{pad.t+plotH/2}}" font-size="8" fill="#065F46" transform="rotate(90 ${{W-pad.r+14}} ${{pad.t+plotH/2}})">Cum. ROI</text>`;
  $('c-monthly').innerHTML=makeSVG(W,H,svg);
}}

function renderUpliftChart(){{
  const sorted=[...EVENTS].sort((a,b)=>b.uplift_pct-a.uplift_pct);
  const W=620,H=260,pad={{l:150,r:60,t:10,b:20}};
  const n=sorted.length;
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const rowH=plotH/n;
  const bH=Math.min(rowH*0.6,14);
  const maxU=Math.max(...sorted.map(e=>e.uplift_pct));
  let svg='';
  for(let i=0;i<=4;i++){{
    const x=pad.l+plotW/4*i;
    svg+=`<line x1="${{x}}" y1="${{pad.t}}" x2="${{x}}" y2="${{H-pad.b}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{H-pad.b+11}}" text-anchor="middle" font-size="7.5" fill="#94A3B8">${{(maxU/4*i).toFixed(0)}}%</text>`;
  }}
  sorted.forEach((e,i)=>{{
    const cy=pad.t+rowH*(i+0.5);
    const bW=e.uplift_pct/maxU*plotW;
    const col=mechColor(e.mech);
    const lbl=skuName(e.sku).replace('ProClean ','PC ')+' · '+MONTHS[e.month];
    svg+=`<text x="${{pad.l-5}}" y="${{cy+3.5}}" text-anchor="end" font-size="9" fill="#334155">${{lbl}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{cy-bH/2}}" width="${{bW}}" height="${{bH}}" rx="2" fill="${{col}}" opacity=".82"
      onmouseenter="showTT('${{skuName(e.sku)}}<br>${{MONTHS[e.month]}} · ${{mechShort(e.mech)}}<br>Uplift: +${{e.uplift_pct.toFixed(1)}}%<br>ROI: ${{e.roi.toFixed(1)}}%',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg+=`<text x="${{pad.l+bW+4}}" y="${{cy+3.5}}" font-size="9" font-weight="700" fill="${{col}}">+${{e.uplift_pct.toFixed(0)}}%</text>`;
  }});
  $('c-uplift').innerHTML=makeSVG(W,H,svg);
}}

function renderEventsTable(){{
  const sorted=[...EVENTS].sort((a,b)=>b.roi-a.roi);
  const maxRoi=Math.max(...sorted.map(e=>e.roi),1);
  const rows=sorted.map(e=>{{
    const rClass=roiClass(e.roi);
    const mCol=mechColor(e.mech);
    return `<tr>
      <td><span class="sku-nm">${{skuName(e.sku)}}</span>
          <span class="seg-tag ${{segClass(skuSeg(e.sku))}}" style="margin-left:6px">${{skuSeg(e.sku)}}</span></td>
      <td>${{MONTHS[e.month]}}</td>
      <td><span class="mech-tag" style="background:${{mCol}}22;color:${{mCol}};border:1px solid ${{mCol}}44">${{mechShort(e.mech)}}</span></td>
      <td>${{fmtUSD(e.spend)}}</td>
      <td>+${{e.uplift_pct.toFixed(1)}}%</td>
      <td>${{fmtUSD(e.incr_rev)}}</td>
      <td>${{fmtUSD(e.incr_gp)}}</td>
      <td>${{fmtUSD(e.net_incr_gp)}}</td>
      <td class="${{rClass}}">
        <div class="roi-bar-wrap">
          <div class="roi-bg"><div class="roi-fill" style="width:${{clamp(e.roi/maxRoi*100,0,100)}}%;background:${{rClass==='pos-val'?'#059669':rClass==='warn-val'?'#D97706':'#DC2626'}}"></div></div>
          ${{e.roi.toFixed(1)}}%
        </div>
      </td>
    </tr>`;
  }}).join('');
  $('events-table').innerHTML=`
    <table class="data-tbl"><thead><tr>
      <th>SKU</th><th>Month</th><th>Mechanic</th><th>Spend</th>
      <th>Vol Uplift</th><th>Incr Revenue</th><th>Incr GP</th>
      <th>Net Incr GP</th><th>ROI %</th>
    </tr></thead><tbody>${{rows}}</tbody></table>`;
}}

// ─────────────────────────────── CALENDAR TAB ────────────────────────────────
function renderCalendar(){{
  // Legend
  $('cal-legend').innerHTML=MECHS.map(m=>
    `<div class="lg-i"><div class="lg-sq" style="background:${{m.color}}"></div>${{m.short}}</div>`
  ).join('');
  // Heatmap
  const header=`<tr><th>SKU</th>${{MONTHS.map(m=>`<th>${{m}}</th>`).join('')}}</tr>`;
  const rows=SKUS.map(s=>{{
    const cells=MONTHS.map((_,mi)=>{{
      const ev=EVENTS.find(e=>e.sku===s.id&&e.month===mi);
      if(!ev) return `<td><div class="cal-cell cal-empty"></div></td>`;
      const col=mechColor(ev.mech);
      const roi=ev.roi;
      const bg=col+'22', textCol=col;
      return `<td><div class="cal-cell" style="background:${{bg}}"
        onmouseenter="showTT('${{s.name}}<br>${{MONTHS[mi]}} · ${{mechShort(ev.mech)}}<br>ROI: ${{roi.toFixed(1)}}%<br>Spend: ${{fmtUSD(ev.spend)}}<br>Uplift: +${{ev.uplift_pct.toFixed(1)}}%',event)"
        onmouseleave="hideTT()" onmousemove="moveTT(event)">
          <span style="font-size:10.5px;font-weight:700;color:${{textCol}}">${{roi.toFixed(0)}}%</span>
          <span class="cal-mech-label" style="background:${{col}}33;color:${{col}}">${{mechShort(ev.mech)}}</span>
        </div></td>`;
    }}).join('');
    return `<tr><td class="row-hdr">${{s.name.replace('ProClean ','')}}</td>${{cells}}</tr>`;
  }}).join('');
  $('cal-heatmap').innerHTML=`<table class="cal-tbl"><thead>${{header}}</thead><tbody>${{rows}}</tbody></table>`;

  // Events per month bar
  const evCounts=MONTHS.map((_,i)=>EVENTS.filter(e=>e.month===i).length);
  const maxC=Math.max(...evCounts);
  const W=560,H=160,pad={{l:30,r:14,t:14,b:30}};
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const slotW=plotW/12, bW=slotW*0.5;
  let svg='';
  evCounts.forEach((c,i)=>{{
    const cx=pad.l+slotW*(i+0.5);
    const bH=c/maxC*plotH;
    const y=pad.t+plotH-bH;
    svg+=`<rect x="${{cx-bW/2}}" y="${{y}}" width="${{bW}}" height="${{bH}}" rx="2" fill="#059669" opacity=".75"/>`;
    if(c>0) svg+=`<text x="${{cx}}" y="${{y-3}}" text-anchor="middle" font-size="9" fill="#065F46" font-weight="700">${{c}}</text>`;
    svg+=`<text x="${{cx}}" y="${{H-pad.b+12}}" text-anchor="middle" font-size="8.5" fill="#94A3B8">${{MONTHS[i]}}</text>`;
  }});
  $('c-events-month').innerHTML=makeSVG(W,H,svg);

  // Spend by month
  const spends=MONTHS.map((_,i)=>EVENTS.filter(e=>e.month===i).reduce((a,e)=>a+e.spend,0));
  const maxSp=Math.max(...spends);
  let svg2='';
  for(let gi=0;gi<=3;gi++){{
    const y=pad.t+plotH/3*gi;
    svg2+=`<line x1="${{pad.l}}" y1="${{y}}" x2="${{W-pad.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg2+=`<text x="${{pad.l-4}}" y="${{y+3}}" text-anchor="end" font-size="8" fill="#94A3B8">${{fmtUSD(maxSp-maxSp/3*gi)}}</text>`;
  }}
  spends.forEach((sp,i)=>{{
    const cx=pad.l+slotW*(i+0.5);
    const bH=sp/maxSp*plotH;
    const y=pad.t+plotH-bH;
    svg2+=`<rect x="${{cx-bW/2}}" y="${{y}}" width="${{bW}}" height="${{bH}}" rx="2" fill="#7C3AED" opacity=".70"/>`;
    if(sp>0) svg2+=`<text x="${{cx}}" y="${{y-3}}" text-anchor="middle" font-size="8" fill="#7C3AED" font-weight="700">${{fmtUSD(sp)}}</text>`;
    svg2+=`<text x="${{cx}}" y="${{H-pad.b+12}}" text-anchor="middle" font-size="8.5" fill="#94A3B8">${{MONTHS[i]}}</text>`;
  }});
  $('c-spend-month').innerHTML=makeSVG(W,H,svg2);
}}

// ─────────────────────────────── MECHANIC TAB ────────────────────────────────
function renderMechanic(){{
  const byMech=MECHS.map(m=>{{const a=sumEvents(e=>e.mech===m.id);return{{...m,...a}};}});

  // ROI bar
  const maxROI=Math.max(...byMech.map(m=>m.roi));
  const W=500,H=180,pad={{l:70,r:60,t:14,b:24}};
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const rowH=plotH/4, bH=rowH*0.55;
  let svg='';
  byMech.forEach((m,i)=>{{
    const cy=pad.t+rowH*(i+0.5);
    const bW=m.roi/maxROI*plotW;
    svg+=`<text x="${{pad.l-6}}" y="${{cy+4}}" text-anchor="end" font-size="10" font-weight="600" fill="#334155">${{m.short}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{cy-bH/2}}" width="${{bW}}" height="${{bH}}" rx="3" fill="${{m.color}}" opacity=".85"
      onmouseenter="showTT('${{m.name}}<br>ROI: ${{fmtPct(m.roi)}}<br>Spend: ${{fmtUSD(m.spend)}}<br>Events: ${{m.count}}',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg+=`<text x="${{pad.l+bW+5}}" y="${{cy+4}}" font-size="10" font-weight="700" fill="${{m.color}}">${{m.roi.toFixed(1)}}%</text>`;
  }});
  $('c-mech-roi').innerHTML=makeSVG(W,H,svg);

  // Uplift bar
  const byMechUplift=MECHS.map(m=>{{
    const evs=EVENTS.filter(e=>e.mech===m.id);
    const avg=evs.length?evs.reduce((a,e)=>a+e.uplift_pct,0)/evs.length:0;
    return{{...m,avg_uplift:avg,count:evs.length}};
  }});
  const maxU=Math.max(...byMechUplift.map(m=>m.avg_uplift));
  let svg3='';
  byMechUplift.forEach((m,i)=>{{
    const cy=pad.t+rowH*(i+0.5);
    const bW=m.avg_uplift/maxU*plotW;
    svg3+=`<text x="${{pad.l-6}}" y="${{cy+4}}" text-anchor="end" font-size="10" font-weight="600" fill="#334155">${{m.short}}</text>`;
    svg3+=`<rect x="${{pad.l}}" y="${{cy-bH/2}}" width="${{bW}}" height="${{bH}}" rx="3" fill="${{m.color}}" opacity=".80"
      onmouseenter="showTT('${{m.name}}<br>Avg Uplift: +${{m.avg_uplift.toFixed(1)}}%<br>Events: ${{m.count}}',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg3+=`<text x="${{pad.l+bW+5}}" y="${{cy+4}}" font-size="10" font-weight="700" fill="${{m.color}}">+${{m.avg_uplift.toFixed(1)}}%</text>`;
  }});
  $('c-mech-uplift').innerHTML=makeSVG(W,H,svg3);

  // Mechanic summary table
  const rows=byMech.map(m=>{{
    const rC=roiClass(m.roi);
    return `<tr>
      <td><span style="display:inline-flex;align-items:center;gap:6px">
        <span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${{m.color}}"></span>
        ${{m.name}}</span></td>
      <td>${{m.count}}</td>
      <td>${{fmtUSD(m.spend)}}</td>
      <td>${{fmtUSD(m.incr_rev)}}</td>
      <td>${{fmtUSD(m.incr_gp)}}</td>
      <td>${{fmtUSD(m.net_incr_gp)}}</td>
      <td class="${{rC}}">${{m.roi.toFixed(1)}}%</td>
    </tr>`;
  }}).join('');
  const tot=sumEvents();
  const totRow=`<tr class="bold-row">
    <td>Total</td><td>${{tot.count}}</td>
    <td>${{fmtUSD(tot.spend)}}</td><td>${{fmtUSD(tot.incr_rev)}}</td>
    <td>${{fmtUSD(tot.incr_gp)}}</td><td>${{fmtUSD(tot.net_incr_gp)}}</td>
    <td class="${{roiClass(tot.roi)}}">${{tot.roi.toFixed(1)}}%</td>
  </tr>`;
  $('mech-table').innerHTML=`<table class="data-tbl"><thead><tr>
    <th>Mechanic</th><th>Events</th><th>Spend</th><th>Incr Revenue</th>
    <th>Incr GP</th><th>Net Incr GP</th><th>ROI %</th>
  </tr></thead><tbody>${{rows}}${{totRow}}</tbody></table>`;

  // Event-level by mechanic
  const evRows=EVENTS.map(e=>{{
    const col=mechColor(e.mech);
    const rC=roiClass(e.roi);
    return `<tr>
      <td><span class="mech-tag" style="background:${{col}}22;color:${{col}};border:1px solid ${{col}}44">${{mechShort(e.mech)}}</span></td>
      <td>${{skuName(e.sku).replace('ProClean ','')}}</td>
      <td>${{MONTHS[e.month]}}</td>
      <td>${{fmtUSD(e.spend)}}</td>
      <td>+${{e.uplift_pct.toFixed(1)}}%</td>
      <td>${{fmtUSD(e.incr_rev)}}</td>
      <td class="${{rC}}">${{e.roi.toFixed(1)}}%</td>
    </tr>`;
  }}).join('');
  $('mech-events-table').innerHTML=`<table class="data-tbl"><thead><tr>
    <th>Mechanic</th><th>SKU</th><th>Month</th><th>Spend</th>
    <th>Vol Uplift</th><th>Incr Revenue</th><th>ROI %</th>
  </tr></thead><tbody>${{evRows}}</tbody></table>`;
}}

// ─────────────────────────────── WATERFALL TAB ────────────────────────────────
function renderWaterfall(){{
  const tot=sumEvents();
  // Portfolio-level waterfall bars
  const steps=[
    {{lbl:'Baseline GP',    val:tot.base_gp,   abs:true,  col:'#3B82F6'}},
    {{lbl:'Price Discount', val:-(tot.base_gp*0.06), abs:false, col:'#DC2626'}},
    {{lbl:'Volume Uplift',  val:tot.incr_gp+(tot.base_gp*0.06), abs:false, col:'#059669'}},
    {{lbl:'= Promoted GP',  val:tot.promo_gp,  abs:true,  col:'#059669'}},
    {{lbl:'Promo Spend',    val:-tot.spend,    abs:false, col:'#DC2626'}},
    {{lbl:'Net Incr GP',    val:tot.net_incr_gp, abs:true, col:tot.net_incr_gp>=0?'#059669':'#DC2626'}},
  ];
  const W=680,H=280,pad={{l:110,r:20,t:20,b:50}};
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const n=steps.length, slotW=plotW/n, bW=slotW*0.48;
  const allAbs=steps.map(s=>Math.abs(s.val));
  const maxV=Math.max(...allAbs)*1.15;
  let running=0, svg='';
  // Grid
  for(let i=0;i<=4;i++){{
    const y=pad.t+plotH/4*i;
    svg+=`<line x1="${{pad.l}}" y1="${{y}}" x2="${{W-pad.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-4}}" y="${{y+3}}" text-anchor="end" font-size="8.5" fill="#94A3B8">${{fmtUSD(maxV-maxV/4*i)}}</text>`;
  }}
  steps.forEach((s,i)=>{{
    const cx=pad.l+slotW*(i+0.5);
    const x=cx-bW/2;
    if(s.abs){{
      const bH=s.val/maxV*plotH;
      const y=pad.t+plotH-bH;
      svg+=`<rect x="${{x}}" y="${{y}}" width="${{bW}}" height="${{bH}}" rx="3" fill="${{s.col}}" opacity=".82"
        onmouseenter="showTT('${{s.lbl}}: ${{fmtUSD(s.val)}}',event)" onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
      svg+=`<text x="${{cx}}" y="${{y-4}}" text-anchor="middle" font-size="9" font-weight="700" fill="${{s.col}}">${{fmtUSD(s.val)}}</text>`;
      running=s.val;
    }} else {{
      const base=running/maxV*plotH;
      const bH=Math.abs(s.val)/maxV*plotH;
      const baseY=pad.t+plotH-base;
      const y=s.val>=0?baseY-bH:baseY;
      svg+=`<rect x="${{x}}" y="${{y}}" width="${{bW}}" height="${{bH}}" rx="3" fill="${{s.col}}" opacity=".75"
        onmouseenter="showTT('${{s.lbl}}: ${{fmtUSD(s.val)}}',event)" onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
      const lv=s.val>=0?'+'+fmtUSD(s.val):fmtUSD(s.val);
      svg+=`<text x="${{cx}}" y="${{s.val>=0?y-4:y+bH+11}}" text-anchor="middle" font-size="9" font-weight="700" fill="${{s.col}}">${{lv}}</text>`;
      // connector
      if(i>0){{
        const prevX=pad.l+slotW*(i-0.5)+bW/2;
        svg+=`<line x1="${{prevX}}" y1="${{baseY}}" x2="${{x}}" y2="${{baseY}}" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="3,2"/>`;
      }}
      running+=s.val;
    }}
    svg+=`<text x="${{cx}}" y="${{H-pad.b+13}}" text-anchor="middle" font-size="9.5" fill="#64748B">${{s.lbl}}</text>`;
    if(i>0&&i<n-1){{
      svg+=`<text x="${{cx}}" y="${{H-pad.b+25}}" text-anchor="middle" font-size="8" fill="#94A3B8">${{fmtUSD(running)}}</text>`;
    }}
  }});
  $('c-waterfall-portfolio').innerHTML=makeSVG(W,H,svg);

  // Net GP by SKU
  const bySku=SKUS.map(s=>{{const a=sumEvents(e=>e.sku===s.id);return{{...s,...a}};}});
  const netVals=bySku.map(s=>s.net_incr_gp);
  const maxNet=Math.max(...netVals.map(Math.abs))*1.2;
  const W2=540,H2=220,pad2={{l:40,r:14,t:18,b:50}};
  const plotW2=W2-pad2.l-pad2.r, plotH2=H2-pad2.t-pad2.b;
  const slotW2=plotW2/5, bW2=36;
  let svg2='';
  for(let gi=0;gi<=4;gi++){{
    const y=pad2.t+plotH2/4*gi;
    const v=maxNet-maxNet/4*gi;
    svg2+=`<line x1="${{pad2.l}}" y1="${{y}}" x2="${{W2-pad2.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg2+=`<text x="${{pad2.l-4}}" y="${{y+3}}" text-anchor="end" font-size="8" fill="#94A3B8">${{fmtUSD(v)}}</text>`;
  }}
  bySku.forEach((s,i)=>{{
    const v=s.net_incr_gp;
    const cx=pad2.l+slotW2*(i+0.5);
    const zero2=pad2.t+plotH2;
    const bH=Math.abs(v)/maxNet*plotH2;
    const y=v>=0?zero2-bH:zero2;
    const col=v>=0?'#059669':'#DC2626';
    svg2+=`<rect x="${{cx-bW2/2}}" y="${{y}}" width="${{bW2}}" height="${{bH}}" rx="3" fill="${{col}}" opacity=".82"
      onmouseenter="showTT('${{s.name}}<br>Net Incr GP: ${{fmtUSD(v)}}<br>Spend: ${{fmtUSD(s.spend)}}<br>ROI: ${{s.roi.toFixed(1)}}%',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg2+=`<text x="${{cx}}" y="${{v>=0?y-4:y+bH+11}}" text-anchor="middle" font-size="9" font-weight="700" fill="${{col}}">${{fmtUSD(v)}}</text>`;
    svg2+=`<text x="${{cx}}" y="${{H2-pad2.b+13}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{s.name.replace('ProClean ','')}}</text>`;
    svg2+=`<text x="${{cx}}" y="${{H2-pad2.b+25}}" text-anchor="middle" font-size="8" fill="#CBD5E1">${{s.roi.toFixed(0)}}% ROI</text>`;
  }});
  $('c-net-gp-sku').innerHTML=makeSVG(W2,H2,svg2);

  // Efficiency: incr GP per $1 spent
  const eff=bySku.map(s=>s.spend>0?s.incr_gp/s.spend:0);
  const maxEff=Math.max(...eff)*1.1;
  const W3=540,H3=200;
  const pad3={{l:40,r:14,t:16,b:50}};
  const plotW3=W3-pad3.l-pad3.r, plotH3=H3-pad3.t-pad3.b;
  const slotW3=plotW3/5, bW3=36;
  let svg3='';
  for(let gi=0;gi<=3;gi++){{
    const y=pad3.t+plotH3/3*gi;
    const v=maxEff-maxEff/3*gi;
    svg3+=`<line x1="${{pad3.l}}" y1="${{y}}" x2="${{W3-pad3.r}}" y2="${{y}}" stroke="#F1F5F9" stroke-width="1"/>`;
    svg3+=`<text x="${{pad3.l-4}}" y="${{y+3}}" text-anchor="end" font-size="8" fill="#94A3B8">${{v.toFixed(2)}}x</text>`;
  }}
  bySku.forEach((s,i)=>{{
    const v=eff[i];
    const cx=pad3.l+slotW3*(i+0.5);
    const zero3=pad3.t+plotH3;
    const bH=v/maxEff*plotH3;
    const y=zero3-bH;
    const col=v>=1.5?'#059669':v>=1?'#D97706':'#DC2626';
    svg3+=`<rect x="${{cx-bW3/2}}" y="${{y}}" width="${{bW3}}" height="${{bH}}" rx="3" fill="${{col}}" opacity=".80"
      onmouseenter="showTT('${{s.name}}<br>Incr GP per $1 Spend: ${{v.toFixed(2)}}x',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg3+=`<text x="${{cx}}" y="${{y-4}}" text-anchor="middle" font-size="9" font-weight="700" fill="${{col}}">${{v.toFixed(2)}}x</text>`;
    svg3+=`<text x="${{cx}}" y="${{H3-pad3.b+13}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{s.name.replace('ProClean ','')}}</text>`;
  }});
  $('c-efficiency').innerHTML=makeSVG(W3,H3,svg3);

  // SKU table
  const tableRows=bySku.map(s=>{{
    const rC=roiClass(s.roi);
    return `<tr>
      <td><span class="sku-nm">${{s.name}}</span>
          <span class="seg-tag ${{segClass(s.segment)}}" style="margin-left:6px">${{s.segment}}</span></td>
      <td>${{fmtUSD(s.base_gp)}}</td>
      <td>${{fmtUSD(s.promo_gp)}}</td>
      <td>${{fmtUSD(s.incr_gp)}}</td>
      <td>${{fmtUSD(s.spend)}}</td>
      <td>${{fmtUSD(s.net_incr_gp)}}</td>
      <td class="${{rC}}">${{s.roi.toFixed(1)}}%</td>
    </tr>`;
  }}).join('');
  $('wf-sku-table').innerHTML=`<table class="data-tbl"><thead><tr>
    <th>SKU</th><th>Baseline GP</th><th>Promoted GP</th><th>Incr GP</th>
    <th>Promo Spend</th><th>Net Incr GP</th><th>ROI %</th>
  </tr></thead><tbody>${{tableRows}}</tbody></table>`;
}}

// ─────────────────────────────── OPTIMIZER TAB ────────────────────────────────
// Historical spends and ROI rates per SKU
const histSpend = SKUS.map(s=>EVENTS.filter(e=>e.sku===s.id).reduce((a,e)=>a+e.spend,0));
const histROI   = SKUS.map(s=>{{const a=sumEvents(e=>e.sku===s.id);return a.roi;}});

let optSpends = [...histSpend];
const TOTAL_BUDGET = histSpend.reduce((a,b)=>a+b,0);

function projectedMetrics(spends){{
  return SKUS.map((s,i)=>{{
    const roi=histROI[i];
    const spend=spends[i];
    const incr_gp = spend * (roi/100+1);
    const net_incr_gp = incr_gp - spend;
    return {{sku:s.id, name:s.name, spend, incr_gp, net_incr_gp, roi}};
  }});
}}

function renderOptimizer(){{
  $('opt-total-budget').textContent = fmtUSD(TOTAL_BUDGET);
  updateOptimizer();
}}

function updateOptimizer(){{
  const used = optSpends.reduce((a,b)=>a+b,0);
  const rem = TOTAL_BUDGET - used;
  const remEl=$('opt-remaining');
  remEl.textContent = (rem>=0?'+':'')+fmtUSD(rem);
  remEl.className='budget-remaining '+(rem>=0?'bdg-pos':'bdg-neg');

  const proj=projectedMetrics(optSpends);
  const hist=projectedMetrics(histSpend);

  // Update slider display values
  SKUS.forEach((s,i)=>{{
    const el=$('opt-val-'+s.id);
    if(el) el.textContent=fmtUSD(optSpends[i]);
    const pill=$('opt-pill-'+s.id);
    if(pill){{
      const dNet=proj[i].net_incr_gp-hist[i].net_incr_gp;
      pill.textContent=(dNet>=0?'+':'')+fmtUSD(dNet);
      pill.className='kpi-badge '+(dNet>=0?'bdg-pos':'bdg-neg');
    }}
  }});

  // Compare chart
  const W=560,H=240,pad={{l:130,r:14,t:14,b:36}};
  const plotW=W-pad.l-pad.r, plotH=H-pad.t-pad.b;
  const n=SKUS.length;
  const rowH=plotH/n;
  const bH=Math.min(rowH*0.35,14);
  const allVals=[...proj.map(p=>p.net_incr_gp),...hist.map(p=>p.net_incr_gp)];
  const maxV=Math.max(...allVals.map(Math.abs))*1.15||1;
  const zeroX=pad.l+plotW*0.5;
  let svg='';
  for(let gi=0;gi<=4;gi++){{
    const x=pad.l+plotW/4*gi;
    svg+=`<line x1="${{x}}" y1="${{pad.t}}" x2="${{x}}" y2="${{H-pad.b}}" stroke="#F1F5F9" stroke-width="1"/>`;
  }}
  svg+=`<line x1="${{zeroX}}" y1="${{pad.t}}" x2="${{zeroX}}" y2="${{H-pad.b}}" stroke="#CBD5E1" stroke-width="1.5"/>`;
  SKUS.forEach((s,i)=>{{
    const cy=pad.t+rowH*(i+0.5);
    const pv=proj[i].net_incr_gp;
    const hv=hist[i].net_incr_gp;
    const pw=Math.abs(pv)/maxV*plotW*0.5;
    const hw=Math.abs(hv)/maxV*plotW*0.5;
    const pCol=pv>=0?'#059669':'#DC2626';
    const hCol='#94A3B8';
    // hist bar (thinner, behind)
    const hx=hv>=0?zeroX:zeroX-hw;
    svg+=`<rect x="${{hx}}" y="${{cy-bH*0.8}}" width="${{hw}}" height="${{bH*0.8}}" rx="2" fill="${{hCol}}" opacity=".50"/>`;
    // proj bar
    const px=pv>=0?zeroX:zeroX-pw;
    svg+=`<rect x="${{px}}" y="${{cy}}" width="${{pw}}" height="${{bH}}" rx="2" fill="${{pCol}}" opacity=".82"
      onmouseenter="showTT('${{s.name}}<br>Projected Net GP: ${{fmtUSD(pv)}}<br>Historical: ${{fmtUSD(hv)}}',event)"
      onmouseleave="hideTT()" onmousemove="moveTT(event)"/>`;
    svg+=`<text x="${{pad.l-6}}" y="${{cy+bH/2+3}}" text-anchor="end" font-size="9.5" font-weight="600" fill="#334155">${{s.name.replace('ProClean ','')}}</text>`;
    svg+=`<text x="${{pv>=0?px+pw+4:px-4}}" y="${{cy+bH/2+3}}" ${{pv<0?'text-anchor="end"':''}} font-size="9" font-weight="700" fill="${{pCol}}">${{fmtUSD(pv)}}</text>`;
  }});
  svg+=`<text x="${{pad.l}}" y="${{H-pad.b+13}}" font-size="8.5" fill="#94A3B8">← Negative</text>`;
  svg+=`<text x="${{W-pad.r}}" y="${{H-pad.b+13}}" text-anchor="end" font-size="8.5" fill="#94A3B8">Positive →</text>`;
  svg+=`<rect x="${{pad.l}}" y="${{H-pad.b+20}}" width="8" height="6" rx="1" fill="#94A3B8" opacity=".50"/>`;
  svg+=`<text x="${{pad.l+11}}" y="${{H-pad.b+26}}" font-size="8.5" fill="#94A3B8">Historical</text>`;
  svg+=`<rect x="${{pad.l+80}}" y="${{H-pad.b+20}}" width="8" height="6" rx="1" fill="#059669"/>`;
  svg+=`<text x="${{pad.l+91}}" y="${{H-pad.b+26}}" font-size="8.5" fill="#94A3B8">Projected</text>`;
  $('c-opt-compare').innerHTML=makeSVG(W,H,svg);

  // Output table
  const totHist=hist.reduce((a,p)=>a+p.net_incr_gp,0);
  const totProj=proj.reduce((a,p)=>a+p.net_incr_gp,0);
  const rows=SKUS.map((s,i)=>{{
    const p=proj[i],h=hist[i];
    const dNet=p.net_incr_gp-h.net_incr_gp;
    const dSpend=optSpends[i]-histSpend[i];
    const rC=roiClass(p.roi);
    return `<tr>
      <td><span class="sku-nm">${{s.name}}</span></td>
      <td>${{fmtUSD(histSpend[i])}}</td>
      <td>${{fmtUSD(optSpends[i])}}</td>
      <td class="${{dSpend>=0?'pos-val':'neg-val'}}">${{(dSpend>=0?'+':'')+fmtUSD(dSpend)}}</td>
      <td>${{fmtUSD(h.net_incr_gp)}}</td>
      <td>${{fmtUSD(p.net_incr_gp)}}</td>
      <td class="${{dNet>=0?'pos-val':'neg-val'}}">${{(dNet>=0?'+':'')+fmtUSD(dNet)}}</td>
      <td class="${{rC}}">${{p.roi.toFixed(1)}}%</td>
    </tr>`;
  }}).join('');
  const dTot=totProj-totHist;
  const totRow=`<tr class="bold-row">
    <td>Total</td>
    <td>${{fmtUSD(histSpend.reduce((a,b)=>a+b,0))}}</td>
    <td>${{fmtUSD(optSpends.reduce((a,b)=>a+b,0))}}</td>
    <td class="${{(optSpends.reduce((a,b)=>a+b,0)-histSpend.reduce((a,b)=>a+b,0))>=0?'pos-val':'neg-val'}}">
      ${{(optSpends.reduce((a,b)=>a+b,0)-histSpend.reduce((a,b)=>a+b,0))>=0?'+':''}}${{fmtUSD(optSpends.reduce((a,b)=>a+b,0)-histSpend.reduce((a,b)=>a+b,0))}}
    </td>
    <td>${{fmtUSD(totHist)}}</td>
    <td>${{fmtUSD(totProj)}}</td>
    <td class="${{dTot>=0?'pos-val':'neg-val'}}">${{(dTot>=0?'+':'')+fmtUSD(dTot)}}</td>
    <td>&mdash;</td>
  </tr>`;
  $('opt-table').innerHTML=`<table class="data-tbl"><thead><tr>
    <th>SKU</th><th>Hist Spend</th><th>New Spend</th><th>&Delta; Spend</th>
    <th>Hist Net GP</th><th>Proj Net GP</th><th>&Delta; Net GP</th><th>ROI %</th>
  </tr></thead><tbody>${{rows}}${{totRow}}</tbody></table>`;
}}

function buildOptSliders(){{
  const html=SKUS.map((s,i)=>{{
    const hist=histSpend[i];
    const min=0, max=Math.round(hist*2/1000)*1000;
    return `<div class="sku-alloc">
      <div class="sku-alloc-top">
        <span class="sku-alloc-name">${{s.name}}</span>
        <span class="kpi-badge bdg-neutral" id="opt-pill-${{s.id}}">–</span>
      </div>
      <div class="alloc-slider-row">
        <span class="alloc-lbl">$0</span>
        <input type="range" min="${{min}}" max="${{max}}" step="1000" value="${{hist}}"
          id="opt-slider-${{s.id}}"
          oninput="optSpends[${{i}}]=+this.value; document.getElementById('opt-val-${{s.id}}').textContent=fmtUSD(+this.value); updateOptimizer()"/>
        <span class="alloc-val" id="opt-val-${{s.id}}">${{fmtUSD(hist)}}</span>
      </div>
    </div>`;
  }}).join('');
  $('opt-sliders').innerHTML=html;
}}

function resetOptimizer(){{
  optSpends=[...histSpend];
  SKUS.forEach((s,i)=>{{
    const el=$('opt-slider-'+s.id);
    if(el) el.value=histSpend[i];
  }});
  updateOptimizer();
}}

// ─────────────────────────────── INIT ────────────────────────────────────────
renderKPIs();
renderInsights();
renderSkuROI();
renderMechBubble();
renderMonthlyChart();
renderUpliftChart();
renderEventsTable();
renderCalendar();
renderMechanic();
renderWaterfall();
buildOptSliders();
renderOptimizer();

window.addEventListener('resize', ()=>{{
  renderSkuROI(); renderMechBubble(); renderMonthlyChart(); renderUpliftChart();
  renderWaterfall(); updateOptimizer();
}});
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Trade_Promo_ROI_Dashboard.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Done!  {os.path.getsize(out)//1024} KB  ->  {out}")
