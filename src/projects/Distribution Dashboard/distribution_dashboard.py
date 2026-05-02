"""
Distribution & SKU Availability Dashboard
- 5 SKUs across 6 channels, 120 outlets, 6 months (Nov-25 → Apr-26)
- Metrics: Numeric Distribution (ND%), Weighted Distribution (WD%),
           Out-of-Stock rate (OOS%), SKU Range Compliance, Coverage Gap
- Tabs: Overview, By Channel, By SKU, OOS Tracker, Gap Analyser
"""
import os, json, math, random

random.seed(7)

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

MONTHS = ["Nov-25", "Dec-25", "Jan-26", "Feb-26", "Mar-26", "Apr-26"]
N_MONTHS = len(MONTHS)

SKUS = [
    {"id": "s1", "name": "ProClean 500g",       "segment": "Core",    "color": "#2563EB", "target_nd": 90},
    {"id": "s2", "name": "ProClean 1kg",         "segment": "Core",    "color": "#7C3AED", "target_nd": 85},
    {"id": "s3", "name": "ProClean Ultra 500g",  "segment": "Premium", "color": "#059669", "target_nd": 75},
    {"id": "s4", "name": "ProClean Ultra 1kg",   "segment": "Premium", "color": "#D97706", "target_nd": 70},
    {"id": "s5", "name": "ProClean Eco 750g",    "segment": "Eco",     "color": "#DC2626", "target_nd": 65},
]

CHANNELS = [
    {"id": "ch1", "name": "Hypermarkets",    "n_outlets": 12, "avg_vol_weight": 4.2},
    {"id": "ch2", "name": "Supermarkets",    "n_outlets": 28, "avg_vol_weight": 2.1},
    {"id": "ch3", "name": "Convenience",     "n_outlets": 35, "avg_vol_weight": 0.8},
    {"id": "ch4", "name": "Wholesale",       "n_outlets": 15, "avg_vol_weight": 3.5},
    {"id": "ch5", "name": "Food Service",    "n_outlets": 18, "avg_vol_weight": 1.6},
    {"id": "ch6", "name": "Pharmacy & Health","n_outlets": 12,"avg_vol_weight": 1.1},
]

TOTAL_OUTLETS = sum(c["n_outlets"] for c in CHANNELS)  # 120

# Base ND% per SKU per channel (latest month); trend upward over months
BASE_ND = {
    "s1": {"ch1": 92, "ch2": 88, "ch3": 76, "ch4": 85, "ch5": 70, "ch6": 60},
    "s2": {"ch1": 88, "ch2": 82, "ch3": 68, "ch4": 80, "ch5": 62, "ch6": 50},
    "s3": {"ch1": 83, "ch2": 74, "ch3": 55, "ch4": 72, "ch5": 58, "ch6": 45},
    "s4": {"ch1": 78, "ch2": 66, "ch3": 45, "ch4": 65, "ch5": 50, "ch6": 38},
    "s5": {"ch1": 72, "ch2": 60, "ch3": 42, "ch4": 58, "ch5": 44, "ch6": 32},
}

# OOS rate % (when stocked, % of visits where product was OOS)
BASE_OOS = {
    "s1": {"ch1": 3, "ch2": 5, "ch3": 10, "ch4": 4, "ch5": 8,  "ch6": 12},
    "s2": {"ch1": 4, "ch2": 6, "ch3": 12, "ch4": 5, "ch5": 9,  "ch6": 14},
    "s3": {"ch1": 5, "ch2": 8, "ch3": 15, "ch4": 7, "ch5": 11, "ch6": 18},
    "s4": {"ch1": 6, "ch2": 9, "ch3": 17, "ch4": 8, "ch5": 13, "ch6": 20},
    "s5": {"ch1": 7, "ch2": 10,"ch3": 19, "ch4": 9, "ch5": 14, "ch6": 22},
}

def build_series(base, trend=0.8, noise=1.5):
    """Build 6-month series ending at base, trending from base - 5*trend."""
    series = []
    for i in range(N_MONTHS):
        delta_from_end = N_MONTHS - 1 - i
        val = base - delta_from_end * trend + random.uniform(-noise, noise)
        series.append(round(min(100, max(0, val)), 1))
    return series

def build_oos_series(base, trend=-0.3, noise=0.8):
    series = []
    for i in range(N_MONTHS):
        delta_from_end = N_MONTHS - 1 - i
        val = base - delta_from_end * trend + random.uniform(-noise, noise)
        series.append(round(min(50, max(0, val)), 1))
    return series

# Build monthly ND% and OOS% series per SKU per channel
ND_DATA  = {}
OOS_DATA = {}

for s in SKUS:
    sid = s["id"]
    ND_DATA[sid]  = {}
    OOS_DATA[sid] = {}
    for c in CHANNELS:
        cid = c["id"]
        ND_DATA[sid][cid]  = build_series(BASE_ND[sid][cid])
        OOS_DATA[sid][cid] = build_oos_series(BASE_OOS[sid][cid])

def weighted_dist(nd_by_channel, month_idx):
    """Volume-weighted distribution across channels for a given month."""
    total_weight = sum(c["avg_vol_weight"] * c["n_outlets"] for c in CHANNELS)
    wd = 0.0
    for c in CHANNELS:
        nd = nd_by_channel[c["id"]][month_idx] / 100
        wd += nd * c["avg_vol_weight"] * c["n_outlets"]
    return round(wd / total_weight * 100, 1) if total_weight else 0

def portfolio_nd(month_idx):
    """Simple average ND across all SKUs and channels for the month."""
    vals = []
    for s in SKUS:
        for c in CHANNELS:
            vals.append(ND_DATA[s["id"]][c["id"]][month_idx])
    return round(sum(vals) / len(vals), 1)

def sku_nd(sid, month_idx):
    """Volume-weighted ND for a single SKU across channels."""
    total_outlets = TOTAL_OUTLETS
    outlets_with = sum(
        round(ND_DATA[sid][c["id"]][month_idx] / 100 * c["n_outlets"])
        for c in CHANNELS
    )
    return round(outlets_with / total_outlets * 100, 1)

def sku_wd(sid, month_idx):
    return weighted_dist(ND_DATA[sid], month_idx)

def sku_oos(sid, month_idx):
    """Weighted OOS rate for a single SKU across channels."""
    total_weight = sum(c["avg_vol_weight"] * c["n_outlets"] for c in CHANNELS)
    oos = 0.0
    for c in CHANNELS:
        oos += OOS_DATA[sid][c["id"]][month_idx] * c["avg_vol_weight"] * c["n_outlets"]
    return round(oos / total_weight, 1) if total_weight else 0

def channel_nd(cid, month_idx):
    """Average ND across all SKUs for a channel."""
    vals = [ND_DATA[s["id"]][cid][month_idx] for s in SKUS]
    return round(sum(vals) / len(vals), 1)

# Pre-compute summaries
latest = N_MONTHS - 1
prev   = N_MONTHS - 2

SUMMARY = {
    "total_outlets": TOTAL_OUTLETS,
    "portfolio_nd_latest":  portfolio_nd(latest),
    "portfolio_nd_prev":    portfolio_nd(prev),
    "portfolio_wd_latest":  round(sum(sku_wd(s["id"], latest) for s in SKUS) / len(SKUS), 1),
    "portfolio_wd_prev":    round(sum(sku_wd(s["id"], prev)   for s in SKUS) / len(SKUS), 1),
    "avg_oos_latest":       round(sum(sku_oos(s["id"], latest) for s in SKUS) / len(SKUS), 1),
    "avg_oos_prev":         round(sum(sku_oos(s["id"], prev)   for s in SKUS) / len(SKUS), 1),
}

SKU_SUMMARY = []
for s in SKUS:
    sid = s["id"]
    nd_l = sku_nd(sid, latest)
    nd_p = sku_nd(sid, prev)
    wd_l = sku_wd(sid, latest)
    oos_l = sku_oos(sid, latest)
    gap_outlets = round((100 - nd_l) / 100 * TOTAL_OUTLETS)
    SKU_SUMMARY.append({
        "id": sid,
        "name": s["name"],
        "color": s["color"],
        "segment": s["segment"],
        "target_nd": s["target_nd"],
        "nd_latest": nd_l,
        "nd_prev": nd_p,
        "nd_vs_target": round(nd_l - s["target_nd"], 1),
        "wd_latest": wd_l,
        "oos_latest": oos_l,
        "gap_outlets": gap_outlets,
        "nd_series": [sku_nd(sid, m) for m in range(N_MONTHS)],
        "wd_series": [sku_wd(sid, m) for m in range(N_MONTHS)],
        "oos_series": [sku_oos(sid, m) for m in range(N_MONTHS)],
    })

CHANNEL_SUMMARY = []
for c in CHANNELS:
    cid = c["id"]
    nd_l = channel_nd(cid, latest)
    nd_p = channel_nd(cid, prev)
    CHANNEL_SUMMARY.append({
        "id": cid,
        "name": c["name"],
        "n_outlets": c["n_outlets"],
        "nd_latest": nd_l,
        "nd_prev": nd_p,
        "nd_series": [channel_nd(cid, m) for m in range(N_MONTHS)],
        "sku_nd": {
            s["id"]: {
                "nd_series": ND_DATA[s["id"]][cid],
                "oos_series": OOS_DATA[s["id"]][cid],
            }
            for s in SKUS
        },
    })

# Gap analysis: per SKU per channel — gap outlets and OOS severity
GAP_MATRIX = []
for s in SKUS:
    row = []
    for c in CHANNELS:
        nd = ND_DATA[s["id"]][c["id"]][latest]
        oos = OOS_DATA[s["id"]][c["id"]][latest]
        gap = round((100 - nd) / 100 * c["n_outlets"])
        row.append({"nd": nd, "oos": oos, "gap_outlets": gap})
    GAP_MATRIX.append(row)

DATA = {
    "months": MONTHS,
    "skus": SKUS,
    "channels": CHANNELS,
    "sku_summary": SKU_SUMMARY,
    "channel_summary": CHANNEL_SUMMARY,
    "gap_matrix": GAP_MATRIX,
    "summary": SUMMARY,
}
DATA_JSON = json.dumps(DATA)

# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Distribution &amp; SKU Availability Dashboard</title>
<style>
:root{{
  --g50:#F8FAFC;--g100:#F1F5F9;--g200:#E2E8F0;--g300:#CBD5E1;
  --g400:#94A3B8;--g600:#475569;--g700:#334155;--g800:#1E293B;--g900:#0F172A;
  --grn:#059669;--red:#DC2626;--amb:#D97706;--blu:#2563EB;
  --accent:#059669;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--g50);color:var(--g800);font-size:13px}}
/* ── header ── */
.hdr{{background:linear-gradient(135deg,#064e3b 0%,#065f46 60%,#047857 100%);
  color:#fff;padding:18px 28px;display:flex;align-items:center;justify-content:space-between}}
.hdr-title{{font-size:20px;font-weight:700;letter-spacing:.3px}}
.hdr-sub{{font-size:11px;opacity:.75;margin-top:2px}}
.badge{{background:rgba(255,255,255,.15);border-radius:20px;padding:3px 11px;font-size:11px}}
/* ── nav ── */
nav{{background:#fff;border-bottom:1px solid var(--g200);display:flex;gap:4px;padding:0 24px;position:sticky;top:0;z-index:50}}
.tab{{padding:12px 18px;font-size:12.5px;font-weight:600;color:var(--g400);cursor:pointer;border-bottom:3px solid transparent;transition:.2s;white-space:nowrap}}
.tab.active{{color:var(--accent);border-color:var(--accent)}}
.tab:hover:not(.active){{color:var(--g700)}}
/* ── main layout ── */
.page{{display:none;padding:24px 28px;max-width:1400px;margin:0 auto}}
.page.active{{display:block}}
/* ── KPI strip ── */
.kpi-strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:22px}}
.kpi{{background:#fff;border-radius:12px;padding:16px 18px;border:1px solid var(--g200);box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.kpi-label{{font-size:10.5px;font-weight:600;color:var(--g400);text-transform:uppercase;letter-spacing:.5px}}
.kpi-value{{font-size:26px;font-weight:800;color:var(--g800);margin:4px 0 2px;line-height:1}}
.kpi-delta{{font-size:11px;font-weight:600}}
.kpi-delta.up{{color:var(--grn)}} .kpi-delta.dn{{color:var(--red)}} .kpi-delta.neu{{color:var(--g400)}}
/* ── cards ── */
.card{{background:#fff;border-radius:12px;border:1px solid var(--g200);box-shadow:0 1px 3px rgba(0,0,0,.06);padding:18px 20px;overflow:hidden}}
.card-title{{font-size:13px;font-weight:700;color:var(--g700);margin-bottom:14px}}
/* ── grid helpers ── */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px}}
.grid-1{{display:grid;grid-template-columns:1fr;gap:16px;margin-bottom:16px}}
/* ── table ── */
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{background:var(--g100);color:var(--g600);font-weight:700;text-align:left;padding:8px 10px;border-bottom:2px solid var(--g200);font-size:11px;text-transform:uppercase;letter-spacing:.4px;white-space:nowrap}}
td{{padding:8px 10px;border-bottom:1px solid var(--g100);vertical-align:middle}}
tr:hover td{{background:#f8fafc}}
/* ── progress bar ── */
.bar-wrap{{background:var(--g100);border-radius:4px;height:7px;width:100%;min-width:80px}}
.bar-fill{{height:7px;border-radius:4px;transition:.3s}}
/* ── badge pills ── */
.pill{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10.5px;font-weight:700}}
.pill-grn{{background:#D1FAE5;color:#065F46}} .pill-red{{background:#FEE2E2;color:#991B1B}}
.pill-amb{{background:#FEF3C7;color:#92400E}} .pill-blu{{background:#DBEAFE;color:#1E40AF}}
/* ── heatmap ── */
.hm-cell{{display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border-radius:4px;height:38px}}
/* ── legend ── */
.legend{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px}}
.leg-item{{display:flex;align-items:center;gap:5px;font-size:11.5px;color:var(--g600);font-weight:600}}
.leg-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0}}
/* ── filter bar ── */
.filter-bar{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;align-items:center}}
.filter-bar select,.filter-bar label{{font-size:12px;padding:6px 10px;border:1px solid var(--g200);border-radius:7px;background:#fff;color:var(--g700);cursor:pointer}}
.filter-bar label{{font-weight:600;color:var(--g600);border:none;padding:0}}
/* ── tooltip ── */
#tt{{position:fixed;background:var(--g800);color:#fff;padding:7px 12px;border-radius:8px;font-size:11.5px;pointer-events:none;opacity:0;transition:opacity .15s;z-index:999;max-width:220px;line-height:1.5}}
/* ── section label ── */
.sec-label{{font-size:10.5px;font-weight:700;color:var(--g400);text-transform:uppercase;letter-spacing:.6px;margin:18px 0 8px}}
/* ── target line indicator ── */
.target-ind{{font-size:10px;font-weight:700;color:var(--amb)}}
</style>
</head>
<body>
<div id="tt"></div>

<div class="hdr">
  <div>
    <div class="hdr-title">Distribution &amp; SKU Availability Dashboard</div>
    <div class="hdr-sub">FMCG Portfolio · 5 SKUs · 6 Channels · 120 Outlets · Nov 2025 – Apr 2026</div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <span class="badge">Numeric Distribution</span>
    <span class="badge">Weighted Distribution</span>
    <span class="badge">OOS Tracker</span>
  </div>
</div>

<nav>
  <div class="tab active" onclick="showTab('overview')">Overview</div>
  <div class="tab" onclick="showTab('by-channel')">By Channel</div>
  <div class="tab" onclick="showTab('by-sku')">By SKU</div>
  <div class="tab" onclick="showTab('oos')">OOS Tracker</div>
  <div class="tab" onclick="showTab('gap')">Gap Analyser</div>
</nav>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 1 — OVERVIEW                                                       -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div class="page active" id="tab-overview">
  <div class="kpi-strip" id="kpi-strip"></div>
  <div class="grid-2">
    <div class="card"><div class="card-title">Portfolio Numeric Distribution Trend (%)</div>
      <svg id="svg-port-nd" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">ND% by Channel — Latest Month</div>
      <svg id="svg-ch-bar" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
  <div class="grid-2">
    <div class="card"><div class="card-title">SKU Distribution vs Target (Apr-26)</div>
      <svg id="svg-sku-vs-target" width="100%" viewBox="0 0 540 220"></svg></div>
    <div class="card"><div class="card-title">SKU Range Compliance — Outlets Reached</div>
      <svg id="svg-range" width="100%" viewBox="0 0 540 220"></svg></div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 2 — BY CHANNEL                                                     -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div class="page" id="tab-by-channel">
  <div class="filter-bar">
    <label>Channel:</label>
    <select id="sel-channel" onchange="renderByChannel()">
      {" ".join(f'<option value="{c["id"]}">{c["name"]} ({c["n_outlets"]} outlets)</option>' for c in DATA["channels"])}
    </select>
  </div>
  <div class="grid-2">
    <div class="card"><div class="card-title">ND% by SKU — Trend</div>
      <svg id="svg-ch-sku-nd" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">OOS% by SKU — Trend</div>
      <svg id="svg-ch-sku-oos" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
  <div class="card" style="margin-bottom:16px">
    <div class="card-title">Channel SKU Scorecard — Apr-26</div>
    <table id="tbl-channel-sku"></table>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 3 — BY SKU                                                         -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div class="page" id="tab-by-sku">
  <div class="filter-bar">
    <label>SKU:</label>
    <select id="sel-sku" onchange="renderBySku()">
      {" ".join(f'<option value="{s["id"]}">{s["name"]}</option>' for s in DATA["skus"])}
    </select>
  </div>
  <div class="grid-2">
    <div class="card"><div class="card-title">ND% Trend by Channel</div>
      <svg id="svg-sku-nd-ch" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">WD% vs ND% Trend</div>
      <svg id="svg-sku-wd-nd" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
  <div class="card" style="margin-bottom:16px">
    <div class="card-title">Channel Breakdown — Apr-26</div>
    <table id="tbl-sku-ch"></table>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 4 — OOS TRACKER                                                    -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div class="page" id="tab-oos">
  <div class="grid-2">
    <div class="card"><div class="card-title">OOS% Trend by SKU (Portfolio Average)</div>
      <svg id="svg-oos-sku" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">OOS% by Channel — Latest Month (Avg SKU)</div>
      <svg id="svg-oos-ch" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
  <div class="card" style="margin-bottom:16px">
    <div class="card-title">OOS% Heatmap — SKU × Channel (Apr-26)</div>
    <div id="oos-heatmap" style="overflow-x:auto"></div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 5 — GAP ANALYSER                                                   -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div class="page" id="tab-gap">
  <div class="card" style="margin-bottom:16px">
    <div class="card-title">Distribution Gap Matrix — Outlets Not Reached (Apr-26)</div>
    <div id="gap-matrix" style="overflow-x:auto"></div>
  </div>
  <div class="grid-2">
    <div class="card"><div class="card-title">Top Gap Opportunities by SKU</div>
      <svg id="svg-gap-sku" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">Coverage Score — ND% vs Target</div>
      <svg id="svg-coverage" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- SCRIPT                                                                  -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<script>
const D = {DATA_JSON};
const MONTHS = D.months;
const SKUS = D.skus;
const CHANNELS = D.channels;
const SS = D.sku_summary;     // array of sku summary objects
const CS = D.channel_summary; // array of channel summary objects
const GM = D.gap_matrix;      // [sku_idx][ch_idx]
const SUM = D.summary;

// ── utils ──────────────────────────────────────────────────────────────
const ttEl = document.getElementById('tt');
function showTT(e, html){{ttEl.innerHTML=html;ttEl.style.opacity=1;moveTT(e);}}
function hideTT(){{ttEl.style.opacity=0;}}
function moveTT(e){{ttEl.style.left=(e.clientX+14)+'px';ttEl.style.top=(e.clientY-32)+'px';}}
document.addEventListener('mousemove',moveTT);

function fP(v,d=1){{return v.toFixed(d)+'%';}}
function fN(v){{return Math.round(v).toLocaleString();}}
function clr(v, thr1=75, thr2=60){{return v>=thr1?'var(--grn)':v>=thr2?'var(--amb)':'var(--red)';}}
function oosCl(v){{return v<=5?'var(--grn)':v<=12?'var(--amb)':'var(--red)';}}

// ── tabs ──────────────────────────────────────────────────────────────
function showTab(id){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  event.currentTarget.classList.add('active');
  if(id==='by-channel') renderByChannel();
  if(id==='by-sku')     renderBySku();
  if(id==='oos')        renderOOS();
  if(id==='gap')        renderGap();
}}

// ── SVG helpers ────────────────────────────────────────────────────────
function lineChart(svgId, series, labels, opts){{
  const el=document.getElementById(svgId);
  if(!el) return;
  const vw=540,vh=opts.h||200;
  el.setAttribute('viewBox','0 0 '+vw+' '+vh);
  const pad=opts.pad||{{l:44,r:16,t:14,b:32}};
  const plotW=vw-pad.l-pad.r, plotH=vh-pad.t-pad.b;
  const allV=series.flatMap(s=>s.data);
  const mn=opts.yMin!==undefined?opts.yMin:Math.max(0,Math.min(...allV)-5);
  const mx=opts.yMax!==undefined?opts.yMax:Math.min(100,Math.max(...allV)+5);
  const fy=v=>pad.t+plotH-(v-mn)/(mx-mn)*plotH;
  const fx=i=>pad.l+i/(labels.length-1)*plotW;
  let svg='';
  // grid
  const ticks=5;
  for(let i=0;i<=ticks;i++){{
    const y=pad.t+plotH/ticks*i;
    const v=mx-(mx-mn)/ticks*i;
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-6}}" y="${{y+4}}" text-anchor="end" font-size="9" fill="#94A3B8">${{v.toFixed(0)}}</text>`;
  }}
  // x labels
  labels.forEach((lb,i)=>{{
    if(i%(Math.ceil(labels.length/6))===0||i===labels.length-1)
      svg+=`<text x="${{fx(i)}}" y="${{vh-6}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{lb}}</text>`;
  }});
  // lines
  series.forEach(s=>{{
    const pts=s.data.map((v,i)=>fx(i)+','+fy(v)).join(' ');
    svg+=`<polyline points="${{pts}}" fill="none" stroke="${{s.color}}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
    // dots
    s.data.forEach((v,i)=>{{
      svg+=`<circle cx="${{fx(i)}}" cy="${{fy(v)}}" r="3.5" fill="${{s.color}}" stroke="#fff" stroke-width="1.5"
        onmouseenter="showTT(event,'<b>${{s.name}}</b><br>${{MONTHS[i]}}: ${{v.toFixed(1)}}%')" onmouseleave="hideTT()"/>`;
    }});
  }});
  // target line
  if(opts.target!==undefined){{
    const ty=fy(opts.target);
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{ty}}" y2="${{ty}}" stroke="#D97706" stroke-width="1.5" stroke-dasharray="5,4"/>`;
    svg+=`<text x="${{pad.l+plotW+2}}" y="${{ty+4}}" font-size="9" fill="#D97706" font-weight="700">TGT</text>`;
  }}
  el.innerHTML=svg;
}}

function barChart(svgId, bars, opts){{
  const el=document.getElementById(svgId);
  if(!el) return;
  const vw=540,vh=opts.h||200;
  el.setAttribute('viewBox','0 0 '+vw+' '+vh);
  const pad=opts.pad||{{l:110,r:16,t:14,b:20}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const maxV=Math.min(100,Math.max(...bars.map(b=>b.value))+10);
  const bH=Math.min(24, plotH/bars.length-6);
  let svg='';
  // gridlines
  [0,25,50,75,100].forEach(v=>{{
    const x=pad.l+v/maxV*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+14}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}</text>`;
  }});
  bars.forEach((b,i)=>{{
    const y=pad.t+i*(bH+6);
    const w=Math.max(2,b.value/maxV*plotW);
    const fc=opts.colorFn?opts.colorFn(b.value):b.color||'var(--blu)';
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10" fill="#475569" font-weight="600">${{b.label}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="${{fc}}" opacity=".85"
      onmouseenter="showTT(event,'<b>${{b.label}}</b><br>${{opts.metric||'ND%'}}: ${{b.value.toFixed(1)}}%')" onmouseleave="hideTT()"/>`;
    svg+=`<text x="${{pad.l+w+4}}" y="${{y+bH/2+4}}" font-size="9.5" fill="#334155" font-weight="700">${{b.value.toFixed(1)}}%</text>`;
    // target marker
    if(b.target!==undefined){{
      const tx=pad.l+b.target/maxV*plotW;
      svg+=`<line x1="${{tx}}" x2="${{tx}}" y1="${{y-2}}" y2="${{y+bH+2}}" stroke="#D97706" stroke-width="2" stroke-dasharray="3,2"/>`;
    }}
  }});
  el.innerHTML=svg;
}}

// ── KPI STRIP ─────────────────────────────────────────────────────────
function renderKPIs(){{
  const kpis=[
    {{label:'Total Outlets',value:SUM.total_outlets,fmt:v=>v,delta:'6 Channels',cls:'neu'}},
    {{label:'Portfolio ND%',value:SUM.portfolio_nd_latest,fmt:v=>fP(v),delta:(SUM.portfolio_nd_latest-SUM.portfolio_nd_prev).toFixed(1)+'pp MoM',cls:SUM.portfolio_nd_latest>=SUM.portfolio_nd_prev?'up':'dn'}},
    {{label:'Portfolio WD%',value:SUM.portfolio_wd_latest,fmt:v=>fP(v),delta:(SUM.portfolio_wd_latest-SUM.portfolio_wd_prev).toFixed(1)+'pp MoM',cls:SUM.portfolio_wd_latest>=SUM.portfolio_wd_prev?'up':'dn'}},
    {{label:'Avg OOS%',value:SUM.avg_oos_latest,fmt:v=>fP(v),delta:(SUM.avg_oos_latest-SUM.avg_oos_prev).toFixed(1)+'pp MoM',cls:SUM.avg_oos_latest<=SUM.avg_oos_prev?'up':'dn'}},
    {{label:'SKUs On Target',value:SS.filter(s=>s.nd_vs_target>=0).length,fmt:v=>v+' / '+SS.length,delta:'vs ND% targets',cls:'neu'}},
    {{label:'Total Gap Outlets',value:SS.reduce((a,s)=>a+s.gap_outlets,0),fmt:v=>v+' outlets',delta:'below ND% target',cls:'dn'}},
  ];
  document.getElementById('kpi-strip').innerHTML=kpis.map(k=>`
    <div class="kpi">
      <div class="kpi-label">${{k.label}}</div>
      <div class="kpi-value">${{k.fmt(k.value)}}</div>
      <div class="kpi-delta ${{k.cls}}">${{k.delta}}</div>
    </div>`).join('');
}}

// ── OVERVIEW CHARTS ───────────────────────────────────────────────────
function renderOverview(){{
  // Portfolio ND trend
  lineChart('svg-port-nd',[{{name:'Portfolio ND%',color:'var(--accent)',data:MONTHS.map((_,i)=>{{
    const vals=SS.flatMap(s=>[s.nd_series[i]]);
    return vals.reduce((a,b)=>a+b,0)/vals.length;
  }})}}],MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},yMin:50,yMax:100}});

  // Channel bar
  barChart('svg-ch-bar',CS.map(c=>{{return{{label:c.name,value:c.nd_latest,color:'var(--accent)'}}}}),
    {{h:200,pad:{{l:120,r:20,t:14,b:24}},colorFn:v=>clr(v)}});

  // SKU vs target
  barChart('svg-sku-vs-target',SS.map(s=>{{return{{label:s.name.replace('ProClean ',''),value:s.nd_latest,color:s.color,target:s.target_nd}}}}),
    {{h:220,pad:{{l:100,r:20,t:14,b:24}},colorFn:(v,i)=>{{return 'var(--accent)';}}}});

  // Range compliance — outlets reached
  const vw=540,vh=220,pad={{l:110,r:20,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const maxO=120;
  let svg='';
  SS.forEach((s,i)=>{{
    const reached=Math.round(s.nd_latest/100*120);
    const gap=120-reached;
    const bH=24;
    const y=pad.t+i*(bH+8);
    const wR=reached/maxO*plotW;
    const wG=gap/maxO*plotW;
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10" fill="#475569" font-weight="600">${{s.name.replace('ProClean ','')}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{wR}}" height="${{bH}}" rx="3" fill="${{s.color}}" opacity=".85"/>`;
    svg+=`<rect x="${{pad.l+wR}}" y="${{y}}" width="${{wG}}" height="${{bH}}" rx="3" fill="#E2E8F0"/>`;
    svg+=`<text x="${{pad.l+wR+4}}" y="${{y+bH/2+4}}" font-size="9.5" fill="#94A3B8">${{gap}} gap</text>`;
    svg+=`<text x="${{pad.l-6+(-5)}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="9.5" fill="#334155" font-weight="700" x="${{pad.l+wR-4}}" text-anchor="end">${{reached}}</text>`;
  }});
  // x labels
  [0,30,60,90,120].forEach(v=>{{
    const x=pad.l+v/maxO*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+14}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}</text>`;
  }});
  document.getElementById('svg-range').setAttribute('viewBox','0 0 540 220');
  document.getElementById('svg-range').innerHTML=svg;
}}

// ── BY CHANNEL ────────────────────────────────────────────────────────
function renderByChannel(){{
  const cid=document.getElementById('sel-channel').value;
  const ch=CS.find(c=>c.id===cid);

  // ND trend per SKU
  lineChart('svg-ch-sku-nd',SKUS.map(s=>{{return{{name:s.name,color:s.color,
    data:ch.sku_nd[s.id].nd_series}}}}),MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},yMin:20,yMax:100}});

  // OOS trend per SKU
  lineChart('svg-ch-sku-oos',SKUS.map(s=>{{return{{name:s.name,color:s.color,
    data:ch.sku_nd[s.id].oos_series}}}}),MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},yMin:0,yMax:30}});

  // Table
  const tbl=document.getElementById('tbl-channel-sku');
  tbl.innerHTML=`<thead><tr>
    <th>SKU</th><th>Segment</th><th>ND% (Apr-26)</th><th>MoM Δ</th><th>OOS% (Apr-26)</th><th>Status</th>
  </tr></thead><tbody>`+SKUS.map((s,si)=>{{
    const nd=ch.sku_nd[s.id].nd_series[5];
    const ndp=ch.sku_nd[s.id].nd_series[4];
    const oos=ch.sku_nd[s.id].oos_series[5];
    const delta=nd-ndp;
    const tgt=D.skus[si].target_nd;
    const ok=nd>=tgt;
    return `<tr>
      <td style="font-weight:700;color:${{s.color}}">${{s.name}}</td>
      <td><span class="pill pill-blu">${{s.segment}}</span></td>
      <td><div style="display:flex;align-items:center;gap:8px">
        <div class="bar-wrap"><div class="bar-fill" style="width:${{nd}}%;background:${{s.color}}"></div></div>
        <span style="font-weight:700;color:${{clr(nd)}}">${{fP(nd)}}</span></div></td>
      <td style="color:${{delta>=0?'var(--grn)':'var(--red)'}};font-weight:700">${{delta>=0?'+':''}}${{delta.toFixed(1)}}pp</td>
      <td style="font-weight:700;color:${{oosCl(oos)}}">${{fP(oos)}}</td>
      <td><span class="pill ${{ok?'pill-grn':'pill-red'}}">${{ok?'On Target':'Below Target'}}</span></td>
    </tr>`;
  }}).join('')+'</tbody>';
}}

// ── BY SKU ────────────────────────────────────────────────────────────
function renderBySku(){{
  const sid=document.getElementById('sel-sku').value;
  const s=SS.find(x=>x.id===sid);
  const skuMeta=SKUS.find(x=>x.id===sid);

  // ND by channel trend
  lineChart('svg-sku-nd-ch',CHANNELS.map(c=>{{return{{name:c.name,
    color:['#2563EB','#7C3AED','#059669','#D97706','#DC2626','#0891B2'][CHANNELS.indexOf(c)],
    data:CS.find(x=>x.id===c.id).sku_nd[sid].nd_series}}}}),
    MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},yMin:10,yMax:100}});

  // WD vs ND
  lineChart('svg-sku-wd-nd',[
    {{name:'ND%',color:skuMeta.color,data:s.nd_series}},
    {{name:'WD%',color:'#0891B2',data:s.wd_series}},
  ],MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},yMin:30,yMax:100,target:skuMeta.target_nd}});

  // Table
  const tbl=document.getElementById('tbl-sku-ch');
  tbl.innerHTML=`<thead><tr>
    <th>Channel</th><th>Outlets</th><th>ND% (Apr-26)</th><th>MoM Δ</th><th>WD%</th><th>OOS%</th><th>Gap Outlets</th>
  </tr></thead><tbody>`+CHANNELS.map((c,ci)=>{{
    const nd=CS.find(x=>x.id===c.id).sku_nd[sid].nd_series[5];
    const ndp=CS.find(x=>x.id===c.id).sku_nd[sid].nd_series[4];
    const oos=CS.find(x=>x.id===c.id).sku_nd[sid].oos_series[5];
    const delta=nd-ndp;
    const gap=Math.round((100-nd)/100*c.n_outlets);
    // weighted dist for this channel
    const wd=nd; // simplified: same as nd within channel (1 channel = uniform weight)
    return `<tr>
      <td style="font-weight:700">${{c.name}}</td>
      <td>${{c.n_outlets}}</td>
      <td><div style="display:flex;align-items:center;gap:8px">
        <div class="bar-wrap"><div class="bar-fill" style="width:${{nd}}%;background:${{skuMeta.color}}"></div></div>
        <span style="font-weight:700;color:${{clr(nd)}}">${{fP(nd)}}</span></div></td>
      <td style="color:${{delta>=0?'var(--grn)':'var(--red)'}};font-weight:700">${{delta>=0?'+':''}}${{delta.toFixed(1)}}pp</td>
      <td style="font-weight:700;color:#0891B2">${{fP(wd)}}</td>
      <td style="font-weight:700;color:${{oosCl(oos)}}">${{fP(oos)}}</td>
      <td style="font-weight:700;color:${{gap>2?'var(--red)':'var(--grn)'}}">${{gap}}</td>
    </tr>`;
  }}).join('')+'</tbody>';
}}

// ── OOS ───────────────────────────────────────────────────────────────
function renderOOS(){{
  // OOS trend by SKU
  lineChart('svg-oos-sku',SKUS.map(s=>{{
    return{{name:s.name,color:s.color,
      data:MONTHS.map((_,mi)=>SS.find(x=>x.id===s.id).oos_series[mi])}}}},
  ),MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},yMin:0,yMax:30}});

  // OOS by channel latest
  barChart('svg-oos-ch',CS.map(c=>{{
    const avg=SKUS.reduce((a,s)=>a+CS.find(x=>x.id===c.id).sku_nd[s.id].oos_series[5],0)/SKUS.length;
    return{{label:c.name,value:parseFloat(avg.toFixed(1)),color:'var(--red)'}}
  }}),{{h:200,pad:{{l:120,r:20,t:14,b:24}},colorFn:oosCl,metric:'OOS%'}});

  // Heatmap
  const cells=GM;
  let html='<table style="border-collapse:separate;border-spacing:4px;width:100%"><thead><tr><th style="font-size:10px;padding:4px 8px">SKU \\ Channel</th>';
  CHANNELS.forEach(c=>{{html+=`<th style="font-size:10px;padding:4px 8px;white-space:nowrap">${{c.name}}</th>`;}});
  html+='</tr></thead><tbody>';
  SKUS.forEach((s,si)=>{{
    html+=`<tr><td style="font-weight:700;font-size:11px;white-space:nowrap;padding:4px 8px">${{s.name.replace('ProClean ','')}}</td>`;
    CHANNELS.forEach((c,ci)=>{{
      const v=cells[si][ci].oos;
      const bg=v<=5?'#D1FAE5':v<=12?'#FEF3C7':'#FEE2E2';
      const tc=v<=5?'#065F46':v<=12?'#92400E':'#991B1B';
      html+=`<td><div class="hm-cell" style="background:${{bg}};color:${{tc}}">${{v.toFixed(1)}}%</div></td>`;
    }});
    html+='</tr>';
  }});
  html+='</tbody></table>';
  document.getElementById('oos-heatmap').innerHTML=html;
}}

// ── GAP ───────────────────────────────────────────────────────────────
function renderGap(){{
  // Gap matrix
  let html='<table style="border-collapse:separate;border-spacing:4px;width:100%"><thead><tr><th style="font-size:10px;padding:4px 8px">SKU \\ Channel</th>';
  CHANNELS.forEach(c=>{{html+=`<th style="font-size:10px;padding:4px 8px;white-space:nowrap">${{c.name}}<br><span style="font-weight:400;color:#94A3B8">${{c.n_outlets}} outlets</span></th>`;}});
  html+='</tr></thead><tbody>';
  SKUS.forEach((s,si)=>{{
    html+=`<tr><td style="font-weight:700;font-size:11px;white-space:nowrap;padding:4px 8px;color:${{s.color}}">${{s.name.replace('ProClean ','')}}</td>`;
    CHANNELS.forEach((c,ci)=>{{
      const gap=GM[si][ci].gap_outlets;
      const nd=GM[si][ci].nd;
      const bg=gap===0?'#D1FAE5':gap<=2?'#FEF3C7':gap<=5?'#FEF9C3':'#FEE2E2';
      const tc=gap===0?'#065F46':gap<=2?'#92400E':gap<=5?'#854D0E':'#991B1B';
      html+=`<td><div class="hm-cell" style="background:${{bg}};color:${{tc}}" title="${{nd.toFixed(1)}}% ND">${{gap===0?'✓':gap+' gap'}}</div></td>`;
    }});
    html+='</tr>';
  }});
  html+='</tbody></table>';
  document.getElementById('gap-matrix').innerHTML=html;

  // Gap by SKU bar
  barChart('svg-gap-sku',SS.map(s=>{{return{{label:s.name.replace('ProClean ',''),value:s.gap_outlets,color:'var(--red)'}}}}),
    {{h:200,pad:{{l:100,r:20,t:14,b:24}},metric:'Gap Outlets'}});

  // Coverage score — ND vs target
  const vw=540,vh=200,pad={{l:110,r:20,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  let svg='';
  SS.forEach((s,i)=>{{
    const score=Math.min(100,s.nd_latest/s.target_nd*100);
    const bH=24;
    const y=pad.t+i*(bH+8);
    const w=score/100*plotW;
    const fc=score>=100?'var(--grn)':score>=85?'var(--amb)':'var(--red)';
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10" fill="#475569" font-weight="600">${{s.name.replace('ProClean ','')}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{plotW}}" height="${{bH}}" rx="3" fill="#F1F5F9"/>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="${{fc}}" opacity=".85"
      onmouseenter="showTT(event,'<b>${{s.name}}</b><br>ND: ${{s.nd_latest}}% vs Target ${{s.target_nd}}%<br>Coverage: ${{score.toFixed(0)}}%')" onmouseleave="hideTT()"/>`;
    svg+=`<text x="${{pad.l+w+4}}" y="${{y+bH/2+4}}" font-size="9.5" fill="#334155" font-weight="700">${{score.toFixed(0)}}%</text>`;
    // target line at 100%
    svg+=`<line x1="${{pad.l+plotW}}" x2="${{pad.l+plotW}}" y1="${{y-2}}" y2="${{y+bH+2}}" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4,3"/>`;
  }});
  [0,25,50,75,100].forEach(v=>{{
    const x=pad.l+v/100*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+14}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}%</text>`;
  }});
  document.getElementById('svg-coverage').setAttribute('viewBox','0 0 540 200');
  document.getElementById('svg-coverage').innerHTML=svg;
}}

// ── INIT ──────────────────────────────────────────────────────────────
renderKPIs();
renderOverview();
</script>
</body>
</html>"""

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Distribution_Dashboard.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML)
size_kb = round(os.path.getsize(out_path) / 1024, 1)
print(f"Done!  {size_kb} KB  ->  {out_path}")
