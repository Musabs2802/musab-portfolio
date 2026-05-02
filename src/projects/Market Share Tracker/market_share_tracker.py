"""
Market Share & Competitive Tracker Dashboard
- ProClean brand vs 4 competitors
- 5 sub-categories, 4 channels, 6 months (Nov-25 – Apr-26)
- Metrics: Volume Share %, Value Share %, Numeric Distribution %, Share of Shelf %
- Tabs: Overview, By Category, By Channel, Head-to-Head, Share Movement
"""
import os, json, math, random

random.seed(99)

MONTHS = ["Nov-25", "Dec-25", "Jan-26", "Feb-26", "Mar-26", "Apr-26"]
N = len(MONTHS)

BRANDS = [
    {"id": "b0", "name": "ProClean",    "ours": True,  "color": "#7C3AED"},
    {"id": "b1", "name": "BrightClean", "ours": False, "color": "#2563EB"},
    {"id": "b2", "name": "EcoWash",     "ours": False, "color": "#059669"},
    {"id": "b3", "name": "CleanPro",    "ours": False, "color": "#D97706"},
    {"id": "b4", "name": "ZipClean",    "ours": False, "color": "#DC2626"},
]

CATEGORIES = [
    {"id": "c1", "name": "Surface Cleaners"},
    {"id": "c2", "name": "Laundry Detergent"},
    {"id": "c3", "name": "Dishwashing"},
    {"id": "c4", "name": "Bathroom Care"},
    {"id": "c5", "name": "Air & Fabric Care"},
]

CHANNELS = [
    {"id": "ch1", "name": "Hypermarkets"},
    {"id": "ch2", "name": "Supermarkets"},
    {"id": "ch3", "name": "Convenience"},
    {"id": "ch4", "name": "Wholesale"},
]

# Base volume share % per brand per category (latest month, must sum to ~100)
# ProClean strongest in Surface Cleaners, moderate in others
BASE_VOL = {
    "c1": {"b0": 32.5, "b1": 24.0, "b2": 18.0, "b3": 15.0, "b4": 10.5},
    "c2": {"b0": 22.0, "b1": 30.0, "b2": 20.0, "b3": 18.0, "b4": 10.0},
    "c3": {"b0": 28.0, "b1": 22.0, "b2": 15.0, "b3": 20.0, "b4": 15.0},
    "c4": {"b0": 25.0, "b1": 28.0, "b2": 22.0, "b3": 14.0, "b4": 11.0},
    "c5": {"b0": 18.0, "b1": 26.0, "b2": 28.0, "b3": 16.0, "b4": 12.0},
}

# Value share premium/discount vs volume share (premium brands have higher value share)
VAL_PREMIUM = {"b0": +2.5, "b1": +1.5, "b2": -1.5, "b3": -2.0, "b4": -0.5}

# Distribution share base per brand per channel
BASE_DIST = {
    "ch1": {"b0": 88, "b1": 92, "b2": 78, "b3": 72, "b4": 65},
    "ch2": {"b0": 82, "b1": 85, "b2": 72, "b3": 68, "b4": 58},
    "ch3": {"b0": 68, "b1": 72, "b2": 60, "b3": 55, "b4": 48},
    "ch4": {"b0": 75, "b1": 70, "b2": 62, "b3": 65, "b4": 52},
}

# Shelf share base per brand per channel
BASE_SHELF = {
    "ch1": {"b0": 24, "b1": 28, "b2": 18, "b3": 16, "b4": 14},
    "ch2": {"b0": 22, "b1": 26, "b2": 20, "b3": 18, "b4": 14},
    "ch3": {"b0": 20, "b1": 24, "b2": 22, "b3": 18, "b4": 16},
    "ch4": {"b0": 26, "b1": 22, "b2": 20, "b3": 20, "b4": 12},
}

def make_share_series(base_shares, trend_brand0=+0.5, noise=0.8):
    """
    Build 6-month series for each brand.
    ProClean (b0) gains trend_brand0 pp/month; competitors lose proportionally.
    Shares always sum to 100.
    """
    brands = list(base_shares.keys())
    # Work backwards from latest month
    result = {b: [] for b in brands}
    for m in range(N):
        delta_from_end = N - 1 - m
        shares = {}
        for b in brands:
            drift = -delta_from_end * trend_brand0 if b == "b0" else delta_from_end * trend_brand0 / (len(brands) - 1)
            noise_v = random.uniform(-noise, noise)
            shares[b] = max(1, base_shares[b] + drift + noise_v)
        # Normalize to 100
        total = sum(shares.values())
        for b in brands:
            result[b].append(round(shares[b] / total * 100, 2))
    return result

def make_pct_series(base, trend=0.4, noise=1.0):
    """Simple series ending at base, trending upward for ProClean."""
    out = []
    for m in range(N):
        delta_from_end = N - 1 - m
        val = base - delta_from_end * trend + random.uniform(-noise, noise)
        out.append(round(min(100, max(0, val)), 1))
    return out

# ── Build all data ─────────────────────────────────────────────────────
# Volume share per category per brand (series)
CAT_VOL = {}
for cat in CATEGORIES:
    CAT_VOL[cat["id"]] = make_share_series(BASE_VOL[cat["id"]])

# Value share = volume share + premium
CAT_VAL = {}
for cat in CATEGORIES:
    vol = CAT_VOL[cat["id"]]
    val_raw = {b: [v + VAL_PREMIUM[b] for v in vol[b]] for b in vol}
    # re-normalize
    val_norm = {b: [] for b in val_raw}
    for m in range(N):
        tot = sum(val_raw[b][m] for b in val_raw)
        for b in val_raw:
            val_norm[b].append(round(val_raw[b][m] / tot * 100, 2))
    CAT_VAL[cat["id"]] = val_norm

# Distribution share per channel per brand
CH_DIST = {}
for ch in CHANNELS:
    CH_DIST[ch["id"]] = {b["id"]: make_pct_series(BASE_DIST[ch["id"]][b["id"]]) for b in BRANDS}

# Shelf share per channel per brand
CH_SHELF = {}
for ch in CHANNELS:
    raw = {b["id"]: make_pct_series(BASE_SHELF[ch["id"]][b["id"]], trend=0.2, noise=0.6) for b in BRANDS}
    # normalize shelf share to 100
    norm = {b: [] for b in raw}
    for m in range(N):
        tot = sum(raw[b][m] for b in raw)
        for b in raw:
            norm[b].append(round(raw[b][m] / tot * 100, 2))
    CH_SHELF[ch["id"]] = norm

# Portfolio volume share (avg across categories, weighted equally)
PORT_VOL = {b["id"]: [] for b in BRANDS}
for m in range(N):
    for b in BRANDS:
        avg = sum(CAT_VOL[c["id"]][b["id"]][m] for c in CATEGORIES) / len(CATEGORIES)
        PORT_VOL[b["id"]].append(round(avg, 2))

PORT_VAL = {b["id"]: [] for b in BRANDS}
for m in range(N):
    for b in BRANDS:
        avg = sum(CAT_VAL[c["id"]][b["id"]][m] for c in CATEGORIES) / len(CATEGORIES)
        PORT_VAL[b["id"]].append(round(avg, 2))

# Share movement: latest vs 3 months ago per brand per category
def share_move(series, brand, latest_idx=5, prior_idx=2):
    return round(series[brand][latest_idx] - series[brand][prior_idx], 2)

MOVEMENT = []
for cat in CATEGORIES:
    row = {"category": cat["name"]}
    for b in BRANDS:
        row[b["id"]] = share_move(CAT_VOL[cat["id"]], b["id"])
    MOVEMENT.append(row)

# Summary
OUR = "b0"
latest = N - 1
prev   = N - 2

SUMMARY = {
    "port_vol_latest": PORT_VOL[OUR][latest],
    "port_vol_prev":   PORT_VOL[OUR][prev],
    "port_val_latest": PORT_VAL[OUR][latest],
    "port_val_prev":   PORT_VAL[OUR][prev],
    "top_cat": max(CATEGORIES, key=lambda c: CAT_VOL[c["id"]][OUR][latest])["name"],
    "weakest_cat": min(CATEGORIES, key=lambda c: CAT_VOL[c["id"]][OUR][latest])["name"],
    "strongest_rival": max((b for b in BRANDS if not b["ours"]),
                           key=lambda b: PORT_VOL[b["id"]][latest])["name"],
}

DATA = {
    "months": MONTHS,
    "brands": BRANDS,
    "categories": CATEGORIES,
    "channels": CHANNELS,
    "port_vol": PORT_VOL,
    "port_val": PORT_VAL,
    "cat_vol": CAT_VOL,
    "cat_val": CAT_VAL,
    "ch_dist": CH_DIST,
    "ch_shelf": CH_SHELF,
    "movement": MOVEMENT,
    "summary": SUMMARY,
}
DATA_JSON = json.dumps(DATA)

# Pre-build HTML fragments that contain quotes (can't use backslashes inside f-string expressions)
CAT_TH_HTML = "".join(
    f'<th>{c["name"]}<br><span style="font-weight:400">Vol %</span></th>'
    for c in DATA["categories"]
)
CAT_OPT_HTML = "".join(
    f'<option value="{c["id"]}">{c["name"]}</option>'
    for c in DATA["categories"]
)
METRIC_OPT_HTML = '<option value="vol">Volume Share %</option><option value="val">Value Share %</option>'
CH_OPT_HTML = "".join(
    f'<option value="{c["id"]}">{c["name"]}</option>'
    for c in DATA["channels"]
)
RIVAL_OPT_HTML = "".join(
    f'<option value="{b["id"]}">{b["name"]}</option>'
    for b in DATA["brands"] if not b["ours"]
)

# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Market Share &amp; Competitive Tracker</title>
<style>
:root{{
  --g50:#F8FAFC;--g100:#F1F5F9;--g200:#E2E8F0;--g300:#CBD5E1;
  --g400:#94A3B8;--g600:#475569;--g700:#334155;--g800:#1E293B;
  --grn:#059669;--red:#DC2626;--amb:#D97706;--pur:#7C3AED;
  --accent:#7C3AED;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--g50);color:var(--g800);font-size:13px}}
.hdr{{background:linear-gradient(135deg,#1e1b4b 0%,#312e81 60%,#4338ca 100%);
  color:#fff;padding:18px 28px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}}
.hdr-title{{font-size:20px;font-weight:700;letter-spacing:.3px}}
.hdr-sub{{font-size:11px;opacity:.75;margin-top:2px}}
.badge{{background:rgba(255,255,255,.15);border-radius:20px;padding:3px 11px;font-size:11px}}
nav{{background:#fff;border-bottom:1px solid var(--g200);display:flex;gap:4px;padding:0 24px;position:sticky;top:0;z-index:50;overflow-x:auto}}
.tab{{padding:12px 18px;font-size:12.5px;font-weight:600;color:var(--g400);cursor:pointer;border-bottom:3px solid transparent;transition:.2s;white-space:nowrap}}
.tab.active{{color:var(--accent);border-color:var(--accent)}}
.tab:hover:not(.active){{color:var(--g700)}}
.page{{display:none;padding:24px 28px;max-width:1400px;margin:0 auto}}
.page.active{{display:block}}
.kpi-strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:22px}}
.kpi{{background:#fff;border-radius:12px;padding:16px 18px;border:1px solid var(--g200);box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.kpi-label{{font-size:10.5px;font-weight:600;color:var(--g400);text-transform:uppercase;letter-spacing:.5px}}
.kpi-value{{font-size:26px;font-weight:800;color:var(--g800);margin:4px 0 2px;line-height:1}}
.kpi-delta{{font-size:11px;font-weight:600}}
.kpi-delta.up{{color:var(--grn)}} .kpi-delta.dn{{color:var(--red)}} .kpi-delta.neu{{color:var(--g400)}}
.card{{background:#fff;border-radius:12px;border:1px solid var(--g200);box-shadow:0 1px 3px rgba(0,0,0,.06);padding:18px 20px;overflow:hidden;margin-bottom:16px}}
.card-title{{font-size:13px;font-weight:700;color:var(--g700);margin-bottom:14px}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{background:var(--g100);color:var(--g600);font-weight:700;text-align:left;padding:8px 10px;border-bottom:2px solid var(--g200);font-size:11px;text-transform:uppercase;letter-spacing:.4px;white-space:nowrap}}
td{{padding:8px 10px;border-bottom:1px solid var(--g100);vertical-align:middle}}
tr:hover td{{background:#f8fafc}}
.bar-wrap{{background:var(--g100);border-radius:4px;height:7px;width:100%;min-width:60px}}
.bar-fill{{height:7px;border-radius:4px}}
.pill{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10.5px;font-weight:700}}
.pill-grn{{background:#D1FAE5;color:#065F46}} .pill-red{{background:#FEE2E2;color:#991B1B}} .pill-pur{{background:#EDE9FE;color:#4C1D95}}
.filter-bar{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;align-items:center}}
.filter-bar select,.filter-bar label{{font-size:12px;padding:6px 10px;border:1px solid var(--g200);border-radius:7px;background:#fff;color:var(--g700);cursor:pointer}}
.filter-bar label{{font-weight:600;color:var(--g600);border:none;padding:0}}
#tt{{position:fixed;background:var(--g800);color:#fff;padding:7px 12px;border-radius:8px;font-size:11.5px;pointer-events:none;opacity:0;transition:opacity .15s;z-index:999;max-width:220px;line-height:1.6}}
.legend{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px}}
.leg-item{{display:flex;align-items:center;gap:5px;font-size:11.5px;color:var(--g600);font-weight:600}}
.leg-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0}}
.our-ring{{box-shadow:0 0 0 2px #fff,0 0 0 4px #7C3AED}}
</style>
</head>
<body>
<div id="tt"></div>

<div class="hdr">
  <div>
    <div class="hdr-title">Market Share &amp; Competitive Tracker</div>
    <div class="hdr-sub">ProClean vs 4 Competitors · 5 Categories · 4 Channels · Nov 2025 – Apr 2026</div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <span class="badge">Volume Share</span>
    <span class="badge">Value Share</span>
    <span class="badge">Share of Shelf</span>
  </div>
</div>

<nav>
  <div class="tab active" onclick="showTab('overview',this)">Overview</div>
  <div class="tab" onclick="showTab('by-category',this)">By Category</div>
  <div class="tab" onclick="showTab('by-channel',this)">By Channel</div>
  <div class="tab" onclick="showTab('head2head',this)">Head-to-Head</div>
  <div class="tab" onclick="showTab('movement',this)">Share Movement</div>
</nav>

<!-- ══ TAB 1: OVERVIEW ══ -->
<div class="page active" id="tab-overview">
  <div class="kpi-strip" id="kpi-strip"></div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-title">Portfolio Volume Share Trend — All Categories</div>
      <div class="legend" id="leg-overview"></div>
      <svg id="svg-port-vol" width="100%" viewBox="0 0 540 190"></svg>
    </div>
    <div class="card">
      <div class="card-title">Volume Share by Category — Apr-26 (Stacked)</div>
      <svg id="svg-cat-stack" width="100%" viewBox="0 0 540 220"></svg>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Brand Scorecard — Apr-26</div>
    <table id="tbl-scorecard"></table>
  </div>
</div>

<!-- ══ TAB 2: BY CATEGORY ══ -->
<div class="page" id="tab-by-category">
  <div class="filter-bar">
    <label>Category:</label>
    <select id="sel-cat" onchange="renderByCategory()">
      {CAT_OPT_HTML}
    </select>
    <label style="margin-left:12px">Metric:</label>
    <select id="sel-cat-metric" onchange="renderByCategory()">
      {METRIC_OPT_HTML}
    </select>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-title" id="cat-trend-title">Volume Share Trend</div>
      <svg id="svg-cat-trend" width="100%" viewBox="0 0 540 200"></svg>
    </div>
    <div class="card">
      <div class="card-title">Share — Apr-26</div>
      <svg id="svg-cat-bar" width="100%" viewBox="0 0 540 200"></svg>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Volume vs Value Share Gap — Apr-26</div>
    <svg id="svg-vol-val" width="100%" viewBox="0 0 540 200"></svg>
  </div>
</div>

<!-- ══ TAB 3: BY CHANNEL ══ -->
<div class="page" id="tab-by-channel">
  <div class="filter-bar">
    <label>Channel:</label>
    <select id="sel-ch" onchange="renderByChannel()">
      {CH_OPT_HTML}
    </select>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-title">Numeric Distribution % — Trend</div>
      <svg id="svg-ch-dist" width="100%" viewBox="0 0 540 200"></svg>
    </div>
    <div class="card">
      <div class="card-title">Share of Shelf % — Apr-26</div>
      <svg id="svg-ch-shelf" width="100%" viewBox="0 0 540 200"></svg>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Channel Competitive Summary — Apr-26</div>
    <table id="tbl-channel"></table>
  </div>
</div>

<!-- ══ TAB 4: HEAD-TO-HEAD ══ -->
<div class="page" id="tab-head2head">
  <div class="filter-bar">
    <label>Competitor:</label>
    <select id="sel-rival" onchange="renderH2H()">
      {RIVAL_OPT_HTML}
    </select>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-title">Volume Share — ProClean vs <span id="rival-name-1">BrightClean</span></div>
      <svg id="svg-h2h-vol" width="100%" viewBox="0 0 540 200"></svg>
    </div>
    <div class="card">
      <div class="card-title">Value Share — ProClean vs <span id="rival-name-2">BrightClean</span></div>
      <svg id="svg-h2h-val" width="100%" viewBox="0 0 540 200"></svg>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Category-by-Category Comparison — Apr-26</div>
    <svg id="svg-h2h-cat" width="100%" viewBox="0 0 700 240"></svg>
  </div>
</div>

<!-- ══ TAB 5: SHARE MOVEMENT ══ -->
<div class="page" id="tab-movement">
  <div class="card">
    <div class="card-title">Share Movement Heatmap — Volume Share Δ (Apr-26 vs Jan-26)</div>
    <div id="move-heatmap" style="overflow-x:auto"></div>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-title">ProClean Share Gain/Loss by Category</div>
      <svg id="svg-move-bar" width="100%" viewBox="0 0 540 200"></svg>
    </div>
    <div class="card">
      <div class="card-title">Competitive Pressure Index — Volume Share Rank by Category</div>
      <svg id="svg-rank" width="100%" viewBox="0 0 540 200"></svg>
    </div>
  </div>
</div>

<script>
const D = {DATA_JSON};
const MONTHS = D.months;
const BRANDS = D.brands;
const CATS = D.categories;
const CHS = D.channels;
const SUM = D.summary;

const ttEl=document.getElementById('tt');
function showTT(e,html){{ttEl.innerHTML=html;ttEl.style.opacity=1;moveTT(e);}}
function hideTT(){{ttEl.style.opacity=0;}}
function moveTT(e){{ttEl.style.left=(e.clientX+14)+'px';ttEl.style.top=(e.clientY-32)+'px';}}
document.addEventListener('mousemove',moveTT);

function fP(v,d=1){{return v.toFixed(d)+'%';}}
function fPp(v){{return (v>=0?'+':'')+v.toFixed(2)+'pp';}}
function bClr(bid){{return BRANDS.find(b=>b.id===bid).color;}}
function bName(bid){{return BRANDS.find(b=>b.id===bid).name;}}

function showTab(id,el){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  el.classList.add('active');
  if(id==='by-category') renderByCategory();
  if(id==='by-channel')  renderByChannel();
  if(id==='head2head')   renderH2H();
  if(id==='movement')    renderMovement();
}}

// ── chart helpers ──────────────────────────────────────────────────────
function lineChart(svgId,series,labels,opts){{
  const el=document.getElementById(svgId); if(!el) return;
  const vw=540,vh=opts.h||200;
  el.setAttribute('viewBox','0 0 '+vw+' '+vh);
  const pad=opts.pad||{{l:40,r:16,t:14,b:32}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const allV=series.flatMap(s=>s.data);
  const mn=opts.yMin!==undefined?opts.yMin:Math.max(0,Math.min(...allV)-3);
  const mx=opts.yMax!==undefined?opts.yMax:Math.min(100,Math.max(...allV)+3);
  const fy=v=>pad.t+plotH-(v-mn)/(mx-mn)*plotH;
  const fx=i=>pad.l+i/(labels.length-1)*plotW;
  let svg='';
  for(let i=0;i<=4;i++){{
    const y=pad.t+plotH/4*i; const v=mx-(mx-mn)/4*i;
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-5}}" y="${{y+4}}" text-anchor="end" font-size="9" fill="#94A3B8">${{v.toFixed(0)}}%</text>`;
  }}
  labels.forEach((lb,i)=>{{
    svg+=`<text x="${{fx(i)}}" y="${{vh-4}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{lb}}</text>`;
  }});
  series.forEach(s=>{{
    const pts=s.data.map((v,i)=>fx(i)+','+fy(v)).join(' ');
    const sw=s.ours?2.8:1.8;
    svg+=`<polyline points="${{pts}}" fill="none" stroke="${{s.color}}" stroke-width="${{sw}}" stroke-linejoin="round" stroke-linecap="round" ${{s.ours?'':'stroke-dasharray="6,3"'}}/>`;
    s.data.forEach((v,i)=>{{
      const r=s.ours?4:3;
      svg+=`<circle cx="${{fx(i)}}" cy="${{fy(v)}}" r="${{r}}" fill="${{s.color}}" stroke="#fff" stroke-width="1.5"
        onmouseenter="showTT(event,'<b>${{s.name}}</b><br>${{MONTHS[i]}}: ${{fP(v)}}')" onmouseleave="hideTT()"/>`;
    }});
  }});
  el.innerHTML=svg;
}}

function barChart(svgId,bars,opts){{
  const el=document.getElementById(svgId); if(!el) return;
  const vw=540,vh=opts.h||200;
  el.setAttribute('viewBox','0 0 '+vw+' '+vh);
  const pad=opts.pad||{{l:100,r:20,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const maxV=opts.maxV||Math.max(...bars.map(b=>Math.abs(b.value)))*1.2;
  const bH=Math.min(26,plotH/bars.length-6);
  let svg='';
  [0,25,50,75,100].filter(v=>v<=maxV+5).forEach(v=>{{
    const x=pad.l+v/maxV*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+14}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}%</text>`;
  }});
  bars.forEach((b,i)=>{{
    const y=pad.t+i*(bH+6);
    const w=Math.max(2,Math.abs(b.value)/maxV*plotW);
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10" fill="${{b.ours?b.color:'#475569'}}" font-weight="${{b.ours?'800':'600'}}">${{b.label}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="${{b.color}}" opacity="${{b.ours?'.95':'.7'}}"
      onmouseenter="showTT(event,'<b>${{b.label}}</b><br>${{fP(b.value)}}')" onmouseleave="hideTT()"/>`;
    if(b.ours) svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="none" stroke="#7C3AED" stroke-width="2"/>`;
    svg+=`<text x="${{pad.l+w+4}}" y="${{y+bH/2+4}}" font-size="10" fill="#334155" font-weight="700">${{fP(b.value)}}</text>`;
  }});
  el.innerHTML=svg;
}}

// ── KPI strip ──────────────────────────────────────────────────────────
function renderKPIs(){{
  const volD=SUM.port_vol_latest-SUM.port_vol_prev;
  const valD=SUM.port_val_latest-SUM.port_val_prev;
  const kpis=[
    {{l:'Portfolio Vol. Share',v:fP(SUM.port_vol_latest),d:(volD>=0?'+':'')+volD.toFixed(2)+'pp MoM',cls:volD>=0?'up':'dn'}},
    {{l:'Portfolio Val. Share',v:fP(SUM.port_val_latest),d:(valD>=0?'+':'')+valD.toFixed(2)+'pp MoM',cls:valD>=0?'up':'dn'}},
    {{l:'#1 Category',v:SUM.top_cat,d:'Highest volume share',cls:'up'}},
    {{l:'Weakest Category',v:SUM.weakest_cat,d:'Lowest volume share',cls:'dn'}},
    {{l:'Strongest Rival',v:SUM.strongest_rival,d:'By portfolio share',cls:'neu'}},
  ];
  document.getElementById('kpi-strip').innerHTML=kpis.map(k=>`
    <div class="kpi">
      <div class="kpi-label">${{k.l}}</div>
      <div class="kpi-value" style="font-size:${{k.v.length>8?'18px':'26px'}}">${{k.v}}</div>
      <div class="kpi-delta ${{k.cls}}">${{k.d}}</div>
    </div>`).join('');
}}

// ── OVERVIEW ───────────────────────────────────────────────────────────
function renderOverview(){{
  // legend
  document.getElementById('leg-overview').innerHTML=BRANDS.map(b=>`
    <div class="leg-item">
      <div class="leg-dot" style="background:${{b.color}};${{b.ours?'box-shadow:0 0 0 2px #fff,0 0 0 4px '+b.color:''}}"></div>
      ${{b.ours?'<b>'+b.name+'</b>':b.name}}
    </div>`).join('');

  // Portfolio volume share trend
  lineChart('svg-port-vol',BRANDS.map(b=>{{
    return{{name:b.name,color:b.color,ours:b.ours,data:D.port_vol[b.id]}};
  }}),MONTHS,{{h:190,pad:{{l:40,r:16,t:14,b:32}}}});

  // Stacked bar by category (latest month)
  const el=document.getElementById('svg-cat-stack');
  const vw=540,vh=220,pad={{l:120,r:20,t:14,b:32}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const bH=26, gap=6;
  let svg='';
  CATS.forEach((cat,ci)=>{{
    const y=pad.t+ci*(bH+gap);
    let xOff=pad.l;
    BRANDS.forEach(b=>{{
      const v=D.cat_vol[cat.id][b.id][5];
      const w=v/100*plotW;
      svg+=`<rect x="${{xOff}}" y="${{y}}" width="${{w}}" height="${{bH}}" fill="${{b.color}}" opacity="${{b.ours?'.95':'.72'}}"
        onmouseenter="showTT(event,'<b>${{cat.name}}</b><br>${{b.name}}: ${{fP(v)}}')" onmouseleave="hideTT()"/>`;
      if(w>18) svg+=`<text x="${{xOff+w/2}}" y="${{y+bH/2+4}}" text-anchor="middle" font-size="8.5" fill="#fff" font-weight="${{b.ours?'800':'500'}}">${{v.toFixed(0)}}%</text>`;
      xOff+=w;
    }});
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10" fill="#334155" font-weight="600">${{cat.name}}</text>`;
  }});
  // legend x-axis label
  svg+=`<text x="${{pad.l+plotW/2}}" y="${{vh-4}}" text-anchor="middle" font-size="9" fill="#94A3B8">100% = Total Market</text>`;
  el.setAttribute('viewBox','0 0 540 220');
  el.innerHTML=svg;

  // Scorecard table
  document.getElementById('tbl-scorecard').innerHTML=`<thead><tr>
    <th>Brand</th>
    {CAT_TH_HTML}
    <th>Portfolio Vol%</th><th>Portfolio Val%</th><th>MoM Δ</th>
  </tr></thead><tbody>`+BRANDS.map(b=>`<tr>
    <td style="font-weight:${{b.ours?'800':'600'}};color:${{b.color}}">${{b.ours?'★ ':''}}${{b.name}}</td>
    ${{CATS.map(c=>`<td style="font-weight:${{b.ours?'700':'400'}}">${{fP(D.cat_vol[c.id][b.id][5])}}</td>`).join('')}}
    <td style="font-weight:700;color:${{b.ours?'var(--pur)':'#334155'}}">${{fP(D.port_vol[b.id][5])}}</td>
    <td style="font-weight:700;color:${{b.ours?'var(--pur)':'#334155'}}">${{fP(D.port_val[b.id][5])}}</td>
    <td style="font-weight:700;color:${{(D.port_vol[b.id][5]-D.port_vol[b.id][4])>=0?'var(--grn)':'var(--red)'}}">
      ${{fPp(D.port_vol[b.id][5]-D.port_vol[b.id][4])}}
    </td>
  </tr>`).join('')+'</tbody>';
}}

// ── BY CATEGORY ────────────────────────────────────────────────────────
function renderByCategory(){{
  const cid=document.getElementById('sel-cat').value;
  const metric=document.getElementById('sel-cat-metric').value;
  const src=metric==='vol'?D.cat_vol:D.cat_val;
  const mLabel=metric==='vol'?'Volume Share':'Value Share';
  document.getElementById('cat-trend-title').textContent=mLabel+' Trend';

  lineChart('svg-cat-trend',BRANDS.map(b=>{{
    return{{name:b.name,color:b.color,ours:b.ours,data:src[cid][b.id]}};
  }}),MONTHS,{{h:200,pad:{{l:40,r:16,t:14,b:32}}}});

  barChart('svg-cat-bar',BRANDS.map(b=>{{
    return{{label:b.name,value:src[cid][b.id][5],color:b.color,ours:b.ours}};
  }}),{{h:200,pad:{{l:100,r:20,t:14,b:24}},maxV:50}});

  // Vol vs Val gap
  const el=document.getElementById('svg-vol-val');
  const vw=540,vh=200,pad={{l:100,r:20,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const bH=22,gap2=8;
  let svg='';
  const maxV=40;
  [0,10,20,30,40].forEach(v=>{{
    const x=pad.l+v/maxV*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+14}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}%</text>`;
  }});
  BRANDS.forEach((b,i)=>{{
    const vol=D.cat_vol[cid][b.id][5];
    const val=D.cat_val[cid][b.id][5];
    const y=pad.t+i*(bH*2+gap2);
    const wVol=vol/maxV*plotW;
    const wVal=val/maxV*plotW;
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH+4}}" text-anchor="end" font-size="10" fill="${{b.color}}" font-weight="${{b.ours?'800':'600'}}">${{b.name}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{wVol}}" height="${{bH-1}}" rx="2" fill="${{b.color}}" opacity=".85"/>`;
    svg+=`<text x="${{pad.l+wVol+3}}" y="${{y+bH/2+3}}" font-size="9" fill="#334155">${{fP(vol)}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y+bH}}" width="${{wVal}}" height="${{bH-1}}" rx="2" fill="${{b.color}}" opacity=".4"/>`;
    svg+=`<text x="${{pad.l+wVal+3}}" y="${{y+bH+bH/2+3}}" font-size="9" fill="#334155">${{fP(val)}}</text>`;
  }});
  // legend
  svg+=`<rect x="${{pad.l}}" y="${{pad.t+plotH+20}}" width="10" height="8" rx="1" fill="#7C3AED" opacity=".85"/>`;
  svg+=`<text x="${{pad.l+14}}" y="${{pad.t+plotH+28}}" font-size="9" fill="#475569">Volume Share</text>`;
  svg+=`<rect x="${{pad.l+100}}" y="${{pad.t+plotH+20}}" width="10" height="8" rx="1" fill="#7C3AED" opacity=".4"/>`;
  svg+=`<text x="${{pad.l+114}}" y="${{pad.t+plotH+28}}" font-size="9" fill="#475569">Value Share</text>`;
  el.setAttribute('viewBox','0 0 540 200');
  el.innerHTML=svg;
}}

// ── BY CHANNEL ─────────────────────────────────────────────────────────
function renderByChannel(){{
  const chid=document.getElementById('sel-ch').value;

  lineChart('svg-ch-dist',BRANDS.map(b=>{{
    return{{name:b.name,color:b.color,ours:b.ours,data:D.ch_dist[chid][b.id]}};
  }}),MONTHS,{{h:200,pad:{{l:40,r:16,t:14,b:32}},yMin:30,yMax:100}});

  // Shelf share donut-ish: use bar
  const shelf=BRANDS.map(b=>{{return{{label:b.name,value:D.ch_shelf[chid][b.id][5],color:b.color,ours:b.ours}}}});
  barChart('svg-ch-shelf',shelf,{{h:200,pad:{{l:100,r:20,t:14,b:24}},maxV:40}});

  // Table
  document.getElementById('tbl-channel').innerHTML=`<thead><tr>
    <th>Brand</th><th>Distribution % (Apr)</th><th>Dist MoM Δ</th><th>Shelf Share % (Apr)</th><th>Shelf MoM Δ</th>
  </tr></thead><tbody>`+BRANDS.map(b=>{{
    const dist=D.ch_dist[chid][b.id];
    const shelf2=D.ch_shelf[chid][b.id];
    const dD=dist[5]-dist[4], sD=shelf2[5]-shelf2[4];
    const dClr=dD>=0?'#059669':'#DC2626', sClr=sD>=0?'#059669':'#DC2626';
    return `<tr>
      <td style="font-weight:${{b.ours?'800':'600'}};color:${{b.color}}">${{b.ours?'★ ':''}}${{b.name}}</td>
      <td><div style="display:flex;align-items:center;gap:8px">
        <div style="background:#F1F5F9;border-radius:4px;height:7px;width:80px">
          <div style="background:${{b.color}};height:7px;border-radius:4px;width:${{dist[5]}}%"></div></div>
        <span style="font-weight:700">${{fP(dist[5])}}</span></div></td>
      <td style="font-weight:700;color:${{dClr}}">${{fPp(dD)}}</td>
      <td style="font-weight:700;color:${{b.ours?'#7C3AED':'#334155'}}">${{fP(shelf2[5])}}</td>
      <td style="font-weight:700;color:${{sClr}}">${{fPp(sD)}}</td>
    </tr>`;
  }}).join('')+'</tbody>';
}}

// ── HEAD-TO-HEAD ───────────────────────────────────────────────────────
function renderH2H(){{
  const rid=document.getElementById('sel-rival').value;
  const rName=bName(rid);
  document.getElementById('rival-name-1').textContent=rName;
  document.getElementById('rival-name-2').textContent=rName;

  const our=BRANDS.find(b=>b.ours);
  lineChart('svg-h2h-vol',[
    {{name:'ProClean',color:our.color,ours:true, data:D.port_vol['b0']}},
    {{name:rName,    color:bClr(rid), ours:false,data:D.port_vol[rid]}},
  ],MONTHS,{{h:200,pad:{{l:40,r:16,t:14,b:32}}}});

  lineChart('svg-h2h-val',[
    {{name:'ProClean',color:our.color,ours:true, data:D.port_val['b0']}},
    {{name:rName,    color:bClr(rid), ours:false,data:D.port_val[rid]}},
  ],MONTHS,{{h:200,pad:{{l:40,r:16,t:14,b:32}}}});

  // Cat-by-cat grouped bar
  const el=document.getElementById('svg-h2h-cat');
  const vw=700,vh=240,pad={{l:130,r:20,t:14,b:32}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const groupH=(plotH-6*(CATS.length-1))/CATS.length;
  const bW=(groupH-4)/2;
  const maxV=50;
  let svg='';
  [0,10,20,30,40,50].forEach(v=>{{
    const x=pad.l+v/maxV*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+14}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}%</text>`;
  }});
  CATS.forEach((cat,ci)=>{{
    const y=pad.t+ci*(groupH+6);
    const vOur=D.cat_vol[cat.id]['b0'][5];
    const vRiv=D.cat_vol[cat.id][rid][5];
    const wOur=vOur/maxV*plotW;
    const wRiv=vRiv/maxV*plotW;
    svg+=`<text x="${{pad.l-6}}" y="${{y+groupH/2+4}}" text-anchor="end" font-size="10.5" fill="#334155" font-weight="600">${{cat.name}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{wOur}}" height="${{bW}}" rx="2" fill="${{our.color}}" opacity=".9"
      onmouseenter="showTT(event,'<b>${{cat.name}}</b><br>ProClean: ${{fP(vOur)}}')" onmouseleave="hideTT()"/>`;
    svg+=`<text x="${{pad.l+wOur+4}}" y="${{y+bW/2+3}}" font-size="9" fill="#334155" font-weight="700">${{fP(vOur)}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y+bW+4}}" width="${{wRiv}}" height="${{bW}}" rx="2" fill="${{bClr(rid)}}" opacity=".75"
      onmouseenter="showTT(event,'<b>${{cat.name}}</b><br>${{rName}}: ${{fP(vRiv)}}')" onmouseleave="hideTT()"/>`;
    svg+=`<text x="${{pad.l+wRiv+4}}" y="${{y+bW+4+bW/2+3}}" font-size="9" fill="#334155">${{fP(vRiv)}}</text>`;
    // gap indicator
    const gap=vOur-vRiv;
    const gapX=pad.l+Math.max(wOur,wRiv)+36;
    svg+=`<text x="${{gapX}}" y="${{y+groupH/2+4}}" font-size="10" fill="${{gap>=0?'var(--grn)':'var(--red)'}}" font-weight="700">${{gap>=0?'▲':'▼'}} ${{Math.abs(gap).toFixed(1)}}pp</text>`;
  }});
  // legend
  svg+=`<rect x="${{pad.l}}" y="${{pad.t+plotH+20}}" width="10" height="10" rx="2" fill="${{our.color}}"/>`;
  svg+=`<text x="${{pad.l+14}}" y="${{pad.t+plotH+29}}" font-size="10" fill="#475569" font-weight="700">ProClean</text>`;
  svg+=`<rect x="${{pad.l+90}}" y="${{pad.t+plotH+20}}" width="10" height="10" rx="2" fill="${{bClr(rid)}}" opacity=".75"/>`;
  svg+=`<text x="${{pad.l+104}}" y="${{pad.t+plotH+29}}" font-size="10" fill="#475569">${{rName}}</text>`;
  el.setAttribute('viewBox','0 0 700 240');
  el.innerHTML=svg;
}}

// ── SHARE MOVEMENT ─────────────────────────────────────────────────────
function renderMovement(){{
  // Heatmap: rows=brands, cols=categories, value=share Δ Apr vs Jan
  let html='<table style="border-collapse:separate;border-spacing:4px;width:100%"><thead><tr>';
  html+=`<th style="font-size:10px;padding:4px 8px">Brand</th>`;
  CATS.forEach(c=>{{html+=`<th style="font-size:10px;padding:4px 8px;white-space:nowrap">${{c.name}}</th>`;}});
  html+=`<th style="font-size:10px;padding:4px 8px">Portfolio Avg</th>`;
  html+='</tr></thead><tbody>';
  BRANDS.forEach(b=>{{
    html+=`<tr><td style="font-weight:${{b.ours?'800':'600'}};font-size:11px;white-space:nowrap;color:${{b.color}};padding:4px 8px">${{b.ours?'★ ':''}}${{b.name}}</td>`;
    let portSum=0;
    CATS.forEach(c=>{{
      const delta=D.cat_vol[c.id][b.id][5]-D.cat_vol[c.id][b.id][2]; // Apr vs Jan
      portSum+=delta;
      const bg=delta>0.5?'#D1FAE5':delta<-0.5?'#FEE2E2':'#F1F5F9';
      const tc=delta>0.5?'#065F46':delta<-0.5?'#991B1B':'#475569';
      html+=`<td><div style="background:${{bg}};color:${{tc}};font-weight:700;font-size:11px;padding:6px 10px;border-radius:6px;text-align:center">
        ${{delta>=0?'+':''}}${{delta.toFixed(2)}}pp</div></td>`;
    }});
    const portAvg=portSum/CATS.length;
    const bg2=portAvg>0.2?'#D1FAE5':portAvg<-0.2?'#FEE2E2':'#F1F5F9';
    const tc2=portAvg>0.2?'#065F46':portAvg<-0.2?'#991B1B':'#475569';
    html+=`<td><div style="background:${{bg2}};color:${{tc2}};font-weight:800;font-size:11px;padding:6px 10px;border-radius:6px;text-align:center">
      ${{portAvg>=0?'+':''}}${{portAvg.toFixed(2)}}pp</div></td>`;
    html+='</tr>';
  }});
  html+='</tbody></table>';
  document.getElementById('move-heatmap').innerHTML=html;

  // ProClean gain/loss bar
  const el=document.getElementById('svg-move-bar');
  const vw=540,vh=200,pad={{l:130,r:30,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const deltas=CATS.map(c=>{{
    return{{label:c.name,value:D.cat_vol[c.id]['b0'][5]-D.cat_vol[c.id]['b0'][2]}};
  }});
  const maxAbs=Math.max(...deltas.map(d=>Math.abs(d.value)))*1.4||1;
  const midX=pad.l+plotW/2;
  const bH=22;
  let svg='';
  svg+=`<line x1="${{midX}}" x2="${{midX}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#CBD5E1" stroke-width="1.5"/>`;
  deltas.forEach((d,i)=>{{
    const y=pad.t+i*(bH+8);
    const w=Math.abs(d.value)/maxAbs*(plotW/2);
    const fc=d.value>=0?'var(--grn)':'var(--red)';
    const x=d.value>=0?midX:midX-w;
    svg+=`<text x="${{pad.l-6}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10" fill="#475569" font-weight="600">${{d.label}}</text>`;
    svg+=`<rect x="${{x}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="2" fill="${{fc}}" opacity=".85"
      onmouseenter="showTT(event,'<b>ProClean — ${{d.label}}</b><br>Δ Apr vs Jan: ${{fPp(d.value)}}')" onmouseleave="hideTT()"/>`;
    svg+=`<text x="${{d.value>=0?x+w+4:x-4}}" y="${{y+bH/2+4}}" text-anchor="${{d.value>=0?'start':'end'}}" font-size="9.5" fill="#334155" font-weight="700">${{fPp(d.value)}}</text>`;
  }});
  el.setAttribute('viewBox','0 0 540 200');
  el.innerHTML=svg;

  // Rank chart: ProClean rank by category
  const el2=document.getElementById('svg-rank');
  const vw2=540,vh2=200,pad2={{l:130,r:20,t:14,b:32}};
  const plotW2=vw2-pad2.l-pad2.r,plotH2=vh2-pad2.t-pad2.b;
  const nBrands=BRANDS.length;
  let svg2='';
  for(let r=1;r<=nBrands;r++){{
    const y=pad2.t+(r-1)/(nBrands-1)*plotH2;
    svg2+=`<line x1="${{pad2.l}}" x2="${{pad2.l+plotW2}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg2+=`<text x="${{pad2.l-5}}" y="${{y+4}}" text-anchor="end" font-size="9" fill="#94A3B8">#${{r}}</text>`;
  }}
  CATS.forEach((cat,ci)=>{{
    const fx=pad2.l+ci/(CATS.length-1)*plotW2;
    // sort brands by share in this cat
    const sorted=[...BRANDS].sort((a,b)=>D.cat_vol[cat.id][b.id][5]-D.cat_vol[cat.id][a.id][5]);
    sorted.forEach((b,ri)=>{{
      const ry=pad2.t+ri/(nBrands-1)*plotH2;
      const r2=b.ours?5:3.5;
      svg2+=`<circle cx="${{fx}}" cy="${{ry}}" r="${{r2}}" fill="${{b.color}}" stroke="#fff" stroke-width="1.5" opacity="${{b.ours?'1':'.7'}}"
        onmouseenter="showTT(event,'${{cat.name}}<br>${{b.name}}: #${{ri+1}} (${{fP(D.cat_vol[cat.id][b.id][5])}})')" onmouseleave="hideTT()"/>`;
    }});
    svg2+=`<text x="${{fx}}" y="${{pad2.t+plotH2+14}}" text-anchor="middle" font-size="9" fill="#475569">${{cat.name.split(' ')[0]}}</text>`;
  }});
  // connect ProClean dots
  const pts=CATS.map((cat,ci)=>{{
    const sorted=[...BRANDS].sort((a,b)=>D.cat_vol[cat.id][b.id][5]-D.cat_vol[cat.id][a.id][5]);
    const ri=sorted.findIndex(b=>b.ours);
    const fx=pad2.l+ci/(CATS.length-1)*plotW2;
    const ry=pad2.t+ri/(nBrands-1)*plotH2;
    return fx+','+ry;
  }}).join(' ');
  svg2=`<polyline points="${{pts}}" fill="none" stroke="#7C3AED" stroke-width="1.5" stroke-dasharray="5,3"/>`+svg2;
  el2.setAttribute('viewBox','0 0 540 200');
  el2.innerHTML=svg2;
}}

// ── INIT ──────────────────────────────────────────────────────────────
renderKPIs();
renderOverview();
</script>
</body>
</html>"""

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Market_Share_Tracker.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML)
size_kb = round(os.path.getsize(out_path) / 1024, 1)
print(f"Done!  {size_kb} KB  ->  {out_path}")
