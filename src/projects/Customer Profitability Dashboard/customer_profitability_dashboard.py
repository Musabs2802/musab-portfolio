"""
Customer Profitability Dashboard
- 30 customers, 4 channels, 5 SKUs
- 6 months (Nov-25 – Apr-26)
- Metrics: Revenue, COGS, Gross Profit, Trade Spend, Logistics, Net Contribution, CM%
- Tabs: Overview, By Customer, By Channel, Pareto Analysis, Margin Waterfall
"""
import os, json, math, random

random.seed(13)

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

MONTHS = ["Nov-25", "Dec-25", "Jan-26", "Feb-26", "Mar-26", "Apr-26"]
N = len(MONTHS)

CHANNELS = [
    {"id": "ch1", "name": "Hypermarkets"},
    {"id": "ch2", "name": "Supermarkets"},
    {"id": "ch3", "name": "Wholesale"},
    {"id": "ch4", "name": "Food Service"},
]

SKUS = [
    {"id": "s1", "name": "ProClean 500g",       "cogs_pct": 0.42, "asp": 18.50},
    {"id": "s2", "name": "ProClean 1kg",         "cogs_pct": 0.40, "asp": 34.00},
    {"id": "s3", "name": "ProClean Ultra 500g",  "cogs_pct": 0.38, "asp": 24.00},
    {"id": "s4", "name": "ProClean Ultra 1kg",   "cogs_pct": 0.36, "asp": 44.00},
    {"id": "s5", "name": "ProClean Eco 750g",    "cogs_pct": 0.44, "asp": 21.00},
]

CUSTOMERS = [
    # Hypermarkets (7)
    {"id":"C01","name":"Al-Noor Hypermarket",      "channel":"ch1","tier_hint":"A"},
    {"id":"C02","name":"Al-Safa Hypermarket",       "channel":"ch1","tier_hint":"A"},
    {"id":"C03","name":"Landmark Superstore",       "channel":"ch1","tier_hint":"B"},
    {"id":"C04","name":"Al-Tamimi Hypermarket",     "channel":"ch1","tier_hint":"A"},
    {"id":"C05","name":"City Mall Hypermarket",     "channel":"ch1","tier_hint":"B"},
    {"id":"C06","name":"Eastern Plaza Hyper",       "channel":"ch1","tier_hint":"C"},
    {"id":"C07","name":"Crown Hypermarket",         "channel":"ch1","tier_hint":"B"},
    # Supermarkets (9)
    {"id":"C08","name":"City Fresh Supermarket",   "channel":"ch2","tier_hint":"A"},
    {"id":"C09","name":"Green Valley Grocery",     "channel":"ch2","tier_hint":"B"},
    {"id":"C10","name":"Al-Rawabi Store",           "channel":"ch2","tier_hint":"B"},
    {"id":"C11","name":"Hilal Food Center",         "channel":"ch2","tier_hint":"C"},
    {"id":"C12","name":"Al-Manar Supermarket",      "channel":"ch2","tier_hint":"A"},
    {"id":"C13","name":"Horizon Superstore",        "channel":"ch2","tier_hint":"B"},
    {"id":"C14","name":"Crescent Grocery",          "channel":"ch2","tier_hint":"C"},
    {"id":"C15","name":"Al-Masah Market",           "channel":"ch2","tier_hint":"C"},
    {"id":"C16","name":"Premier Supermarket",       "channel":"ch2","tier_hint":"B"},
    # Wholesale (7)
    {"id":"C17","name":"Al-Jazeera Wholesale",     "channel":"ch3","tier_hint":"A"},
    {"id":"C18","name":"Western Gate Wholesale",   "channel":"ch3","tier_hint":"B"},
    {"id":"C19","name":"Al-Bahrain Trading",        "channel":"ch3","tier_hint":"A"},
    {"id":"C20","name":"Northern Star Dist.",       "channel":"ch3","tier_hint":"B"},
    {"id":"C21","name":"Pacific Rim Trading",       "channel":"ch3","tier_hint":"C"},
    {"id":"C22","name":"Al-Watan Wholesale",        "channel":"ch3","tier_hint":"B"},
    {"id":"C23","name":"Summit Distributors",       "channel":"ch3","tier_hint":"C"},
    # Food Service (7)
    {"id":"C24","name":"Royal Hotel Catering",     "channel":"ch4","tier_hint":"A"},
    {"id":"C25","name":"Golden Palace Restaurant", "channel":"ch4","tier_hint":"B"},
    {"id":"C26","name":"Four Seasons Catering",    "channel":"ch4","tier_hint":"A"},
    {"id":"C27","name":"Blue Sky Catering",        "channel":"ch4","tier_hint":"B"},
    {"id":"C28","name":"Continental Restaurant",   "channel":"ch4","tier_hint":"C"},
    {"id":"C29","name":"Sea Breeze Restaurant",    "channel":"ch4","tier_hint":"C"},
    {"id":"C30","name":"Desert Spice Kitchen",     "channel":"ch4","tier_hint":"C"},
]

# Revenue scale by tier hint and channel
REV_BASE = {
    ("ch1","A"): 95000, ("ch1","B"): 52000, ("ch1","C"): 24000,
    ("ch2","A"): 68000, ("ch2","B"): 38000, ("ch2","C"): 16000,
    ("ch3","A"): 82000, ("ch3","B"): 45000, ("ch3","C"): 20000,
    ("ch4","A"): 55000, ("ch4","B"): 28000, ("ch4","C"): 12000,
}

# Trade spend % by channel (discount / promotion)
TRADE_PCT = {"ch1": 0.12, "ch2": 0.10, "ch3": 0.08, "ch4": 0.07}
# Logistics cost % of revenue
LOGI_PCT  = {"ch1": 0.04, "ch2": 0.05, "ch3": 0.03, "ch4": 0.06}
# COGS % of revenue (blended across SKU mix)
COGS_PCT  = {"ch1": 0.40, "ch2": 0.41, "ch3": 0.39, "ch4": 0.42}

def build_monthly_revenue(base, seed_offset):
    """6-month revenue series with mild trend and noise."""
    random.seed(seed_offset)
    out = []
    for i in range(N):
        trend = 1 + i * 0.012
        noise = random.uniform(0.92, 1.10)
        out.append(round(base * trend * noise, 0))
    return out

def build_customer_data(c):
    cid = c["id"]
    ch  = c["channel"]
    key = (ch, c["tier_hint"])
    base = REV_BASE[key]
    seed = int(cid[1:]) * 17

    rev_series = build_monthly_revenue(base, seed)
    tc  = TRADE_PCT[ch]
    lc  = LOGI_PCT[ch]
    cg  = COGS_PCT[ch]

    months_data = []
    for m in range(N):
        rev  = rev_series[m]
        cogs = round(rev * cg, 0)
        gp   = rev - cogs
        trade= round(rev * tc, 0)
        logi = round(rev * lc, 0)
        net  = gp - trade - logi
        months_data.append({
            "revenue": rev, "cogs": cogs, "gp": gp,
            "trade": trade, "logi": logi, "net": net,
        })

    # Totals over 6 months
    total_rev   = sum(m["revenue"] for m in months_data)
    total_cogs  = sum(m["cogs"]    for m in months_data)
    total_gp    = sum(m["gp"]      for m in months_data)
    total_trade = sum(m["trade"]   for m in months_data)
    total_logi  = sum(m["logi"]    for m in months_data)
    total_net   = sum(m["net"]     for m in months_data)

    gm_pct  = round(total_gp  / total_rev * 100, 1) if total_rev else 0
    cm_pct  = round(total_net / total_rev * 100, 1) if total_rev else 0

    # SKU mix (% of revenue, 5 SKUs summing to 100)
    raw = [random.uniform(5, 35) for _ in range(5)]
    total_raw = sum(raw)
    sku_mix = [round(r / total_raw * 100, 1) for r in raw]

    # Tier by CM%
    tier = "A" if cm_pct >= 35 else ("B" if cm_pct >= 22 else "C")

    return {
        "id": cid,
        "name": c["name"],
        "channel": ch,
        "tier": tier,
        "total_revenue": round(total_rev, 0),
        "total_cogs":    round(total_cogs, 0),
        "total_gp":      round(total_gp, 0),
        "total_trade":   round(total_trade, 0),
        "total_logi":    round(total_logi, 0),
        "total_net":     round(total_net, 0),
        "gm_pct":        gm_pct,
        "cm_pct":        cm_pct,
        "sku_mix":       sku_mix,
        "rev_series":    [m["revenue"] for m in months_data],
        "gp_series":     [m["gp"]      for m in months_data],
        "net_series":    [m["net"]     for m in months_data],
        "cm_series":     [round(m["net"]/m["revenue"]*100,1) if m["revenue"] else 0 for m in months_data],
    }

CUST_DATA = [build_customer_data(c) for c in CUSTOMERS]

# Channel aggregates
CHANNEL_AGG = []
for ch in CHANNELS:
    custs = [c for c in CUST_DATA if c["channel"] == ch["id"]]
    rev   = sum(c["total_revenue"] for c in custs)
    net   = sum(c["total_net"]     for c in custs)
    gp    = sum(c["total_gp"]      for c in custs)
    trade = sum(c["total_trade"]   for c in custs)
    logi  = sum(c["total_logi"]    for c in custs)
    cogs  = sum(c["total_cogs"]    for c in custs)
    CHANNEL_AGG.append({
        "id":   ch["id"],
        "name": ch["name"],
        "n_customers": len(custs),
        "revenue": rev, "cogs": cogs, "gp": gp,
        "trade": trade, "logi": logi, "net": net,
        "gm_pct": round(gp/rev*100,1) if rev else 0,
        "cm_pct": round(net/rev*100,1) if rev else 0,
    })

# Portfolio totals
PORT_REV   = sum(c["total_revenue"] for c in CUST_DATA)
PORT_COGS  = sum(c["total_cogs"]    for c in CUST_DATA)
PORT_GP    = sum(c["total_gp"]      for c in CUST_DATA)
PORT_TRADE = sum(c["total_trade"]   for c in CUST_DATA)
PORT_LOGI  = sum(c["total_logi"]    for c in CUST_DATA)
PORT_NET   = sum(c["total_net"]     for c in CUST_DATA)
PORT_GM    = round(PORT_GP  / PORT_REV * 100, 1)
PORT_CM    = round(PORT_NET / PORT_REV * 100, 1)

# Pareto — cumulative revenue & net sorted desc by revenue
sorted_by_rev = sorted(CUST_DATA, key=lambda c: c["total_revenue"], reverse=True)
cum_rev = 0; cum_net = 0
PARETO = []
for i, c in enumerate(sorted_by_rev):
    cum_rev += c["total_revenue"]
    cum_net += c["total_net"]
    PARETO.append({
        "rank": i+1,
        "id":   c["id"],
        "name": c["name"],
        "channel": c["channel"],
        "tier": c["tier"],
        "revenue": c["total_revenue"],
        "net": c["total_net"],
        "cm_pct": c["cm_pct"],
        "cum_rev_pct": round(cum_rev / PORT_REV * 100, 1),
        "cum_net_pct": round(cum_net / PORT_NET * 100, 1) if PORT_NET else 0,
    })

SUMMARY = {
    "total_customers": len(CUST_DATA),
    "port_rev":   round(PORT_REV, 0),
    "port_gp":    round(PORT_GP, 0),
    "port_trade": round(PORT_TRADE, 0),
    "port_logi":  round(PORT_LOGI, 0),
    "port_net":   round(PORT_NET, 0),
    "port_gm":    PORT_GM,
    "port_cm":    PORT_CM,
    "tier_a": sum(1 for c in CUST_DATA if c["tier"]=="A"),
    "tier_b": sum(1 for c in CUST_DATA if c["tier"]=="B"),
    "tier_c": sum(1 for c in CUST_DATA if c["tier"]=="C"),
}

DATA = {
    "months": MONTHS,
    "skus": SKUS,
    "channels": CHANNELS,
    "customers": CUST_DATA,
    "channel_agg": CHANNEL_AGG,
    "pareto": PARETO,
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
<title>Customer Profitability Dashboard</title>
<style>
:root{{
  --g50:#F8FAFC;--g100:#F1F5F9;--g200:#E2E8F0;--g300:#CBD5E1;
  --g400:#94A3B8;--g600:#475569;--g700:#334155;--g800:#1E293B;--g900:#0F172A;
  --grn:#059669;--red:#DC2626;--amb:#D97706;--blu:#2563EB;--pur:#7C3AED;
  --accent:#7C3AED;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--g50);color:var(--g800);font-size:13px}}
.hdr{{background:linear-gradient(135deg,#2e1065 0%,#4c1d95 60%,#6d28d9 100%);
  color:#fff;padding:18px 28px;display:flex;align-items:center;justify-content:space-between}}
.hdr-title{{font-size:20px;font-weight:700;letter-spacing:.3px}}
.hdr-sub{{font-size:11px;opacity:.75;margin-top:2px}}
.badge{{background:rgba(255,255,255,.15);border-radius:20px;padding:3px 11px;font-size:11px}}
nav{{background:#fff;border-bottom:1px solid var(--g200);display:flex;gap:4px;padding:0 24px;position:sticky;top:0;z-index:50}}
.tab{{padding:12px 18px;font-size:12.5px;font-weight:600;color:var(--g400);cursor:pointer;border-bottom:3px solid transparent;transition:.2s;white-space:nowrap}}
.tab.active{{color:var(--accent);border-color:var(--accent)}}
.tab:hover:not(.active){{color:var(--g700)}}
.page{{display:none;padding:24px 28px;max-width:1400px;margin:0 auto}}
.page.active{{display:block}}
.kpi-strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:14px;margin-bottom:22px}}
.kpi{{background:#fff;border-radius:12px;padding:16px 18px;border:1px solid var(--g200);box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.kpi-label{{font-size:10.5px;font-weight:600;color:var(--g400);text-transform:uppercase;letter-spacing:.5px}}
.kpi-value{{font-size:26px;font-weight:800;color:var(--g800);margin:4px 0 2px;line-height:1}}
.kpi-delta{{font-size:11px;font-weight:600}}
.kpi-delta.up{{color:var(--grn)}} .kpi-delta.dn{{color:var(--red)}} .kpi-delta.neu{{color:var(--g400)}}
.card{{background:#fff;border-radius:12px;border:1px solid var(--g200);box-shadow:0 1px 3px rgba(0,0,0,.06);padding:18px 20px;overflow:hidden;margin-bottom:16px}}
.card-title{{font-size:13px;font-weight:700;color:var(--g700);margin-bottom:14px}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{background:var(--g100);color:var(--g600);font-weight:700;text-align:left;padding:8px 10px;border-bottom:2px solid var(--g200);font-size:11px;text-transform:uppercase;letter-spacing:.4px;white-space:nowrap}}
td{{padding:8px 10px;border-bottom:1px solid var(--g100);vertical-align:middle}}
tr:hover td{{background:#f8fafc}}
.bar-wrap{{background:var(--g100);border-radius:4px;height:7px;width:100%;min-width:60px}}
.bar-fill{{height:7px;border-radius:4px}}
.pill{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10.5px;font-weight:700}}
.pill-A{{background:#EDE9FE;color:#4C1D95}} .pill-B{{background:#DBEAFE;color:#1E40AF}} .pill-C{{background:#FEF3C7;color:#92400E}}
.pill-grn{{background:#D1FAE5;color:#065F46}} .pill-red{{background:#FEE2E2;color:#991B1B}}
.filter-bar{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;align-items:center}}
.filter-bar select,.filter-bar label{{font-size:12px;padding:6px 10px;border:1px solid var(--g200);border-radius:7px;background:#fff;color:var(--g700);cursor:pointer}}
.filter-bar label{{font-weight:600;color:var(--g600);border:none;padding:0}}
#tt{{position:fixed;background:var(--g800);color:#fff;padding:7px 12px;border-radius:8px;font-size:11.5px;pointer-events:none;opacity:0;transition:opacity .15s;z-index:999;max-width:240px;line-height:1.6}}
</style>
</head>
<body>
<div id="tt"></div>

<div class="hdr">
  <div>
    <div class="hdr-title">Customer Profitability Dashboard</div>
    <div class="hdr-sub">FMCG Portfolio · 30 Customers · 4 Channels · Nov 2025 – Apr 2026</div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <span class="badge">Gross Margin</span>
    <span class="badge">Net Contribution</span>
    <span class="badge">Pareto 80/20</span>
  </div>
</div>

<nav>
  <div class="tab active" onclick="showTab('overview',this)">Overview</div>
  <div class="tab" onclick="showTab('by-customer',this)">By Customer</div>
  <div class="tab" onclick="showTab('by-channel',this)">By Channel</div>
  <div class="tab" onclick="showTab('pareto',this)">Pareto Analysis</div>
  <div class="tab" onclick="showTab('waterfall',this)">Margin Waterfall</div>
</nav>

<!-- ══ TAB 1: OVERVIEW ══ -->
<div class="page active" id="tab-overview">
  <div class="kpi-strip" id="kpi-strip"></div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card"><div class="card-title">Revenue vs Net Contribution — All Customers</div>
      <svg id="svg-scatter" width="100%" viewBox="0 0 540 240"></svg></div>
    <div class="card"><div class="card-title">Customer Tier Distribution</div>
      <svg id="svg-tier-donut" width="100%" viewBox="0 0 540 240"></svg></div>
  </div>
  <div class="card"><div class="card-title">Top 10 Customers by Net Contribution</div>
    <table id="tbl-top10"></table></div>
</div>

<!-- ══ TAB 2: BY CUSTOMER ══ -->
<div class="page" id="tab-by-customer">
  <div class="filter-bar">
    <label>Customer:</label>
    <select id="sel-cust" onchange="renderByCustomer()">
      {" ".join(f'<option value="{c["id"]}">{c["name"]}</option>' for c in sorted(CUSTOMERS, key=lambda x: x["name"]))}
    </select>
  </div>
  <div id="cust-kpi-strip" class="kpi-strip" style="grid-template-columns:repeat(5,1fr)"></div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card"><div class="card-title">Monthly Revenue &amp; Net Contribution</div>
      <svg id="svg-cust-trend" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">Contribution Margin % Trend</div>
      <svg id="svg-cust-cm" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card"><div class="card-title">P&amp;L Waterfall — 6-Month Total</div>
      <svg id="svg-cust-wf" width="100%" viewBox="0 0 540 220"></svg></div>
    <div class="card"><div class="card-title">SKU Revenue Mix</div>
      <svg id="svg-cust-sku" width="100%" viewBox="0 0 540 220"></svg></div>
  </div>
</div>

<!-- ══ TAB 3: BY CHANNEL ══ -->
<div class="page" id="tab-by-channel">
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card"><div class="card-title">Revenue by Channel</div>
      <svg id="svg-ch-rev" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">Net Contribution Margin % by Channel</div>
      <svg id="svg-ch-cm" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
  <div class="card"><div class="card-title">Channel P&amp;L Summary</div>
    <table id="tbl-channel"></table></div>
</div>

<!-- ══ TAB 4: PARETO ══ -->
<div class="page" id="tab-pareto">
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card"><div class="card-title">Cumulative Revenue — Customer Pareto</div>
      <svg id="svg-pareto-rev" width="100%" viewBox="0 0 540 220"></svg></div>
    <div class="card"><div class="card-title">Cumulative Net Contribution — Customer Pareto</div>
      <svg id="svg-pareto-net" width="100%" viewBox="0 0 540 220"></svg></div>
  </div>
  <div class="card"><div class="card-title">Full Customer Ranking by Revenue</div>
    <table id="tbl-pareto"></table></div>
</div>

<!-- ══ TAB 5: WATERFALL ══ -->
<div class="page" id="tab-waterfall">
  <div class="card"><div class="card-title">Portfolio P&amp;L Waterfall — 6-Month Total</div>
    <svg id="svg-port-wf" width="100%" viewBox="0 0 700 300"></svg></div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="card"><div class="card-title">Gross Margin % by Channel</div>
      <svg id="svg-gm-ch" width="100%" viewBox="0 0 540 200"></svg></div>
    <div class="card"><div class="card-title">Cost Structure by Channel (% of Revenue)</div>
      <svg id="svg-cost-ch" width="100%" viewBox="0 0 540 200"></svg></div>
  </div>
</div>

<script>
const D = {DATA_JSON};
const MONTHS = D.months;
const SKUS = D.skus;
const CHANNELS = D.channels;
const CD = D.customers;         // customer detail array
const CA = D.channel_agg;       // channel aggregates
const PAR = D.pareto;           // pareto array
const SUM = D.summary;
const CH_COLORS = ['#7C3AED','#2563EB','#059669','#D97706'];
const SKU_COLORS = ['#2563EB','#7C3AED','#059669','#D97706','#DC2626'];

const ttEl = document.getElementById('tt');
function showTT(e,html){{ttEl.innerHTML=html;ttEl.style.opacity=1;moveTT(e);}}
function hideTT(){{ttEl.style.opacity=0;}}
function moveTT(e){{ttEl.style.left=(e.clientX+14)+'px';ttEl.style.top=(e.clientY-32)+'px';}}
document.addEventListener('mousemove',moveTT);

function fM(v){{
  if(v>=1e6) return '$'+(v/1e6).toFixed(2)+'M';
  if(v>=1e3) return '$'+(v/1e3).toFixed(1)+'K';
  return '$'+v.toFixed(0);
}}
function fP(v,d=1){{return v.toFixed(d)+'%';}}
function cmClr(v){{return v>=35?'var(--grn)':v>=22?'var(--amb)':'var(--red)';}}
function chName(id){{return CHANNELS.find(c=>c.id===id)?.name||id;}}

function showTab(id,el){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  el.classList.add('active');
  if(id==='by-customer') renderByCustomer();
  if(id==='by-channel')  renderByChannel();
  if(id==='pareto')      renderPareto();
  if(id==='waterfall')   renderWaterfall();
}}

// ── line chart helper ──────────────────────────────────────────────────
function lineChart(svgId,series,labels,opts){{
  const el=document.getElementById(svgId); if(!el) return;
  const vw=540,vh=opts.h||200;
  el.setAttribute('viewBox','0 0 '+vw+' '+vh);
  const pad=opts.pad||{{l:52,r:16,t:14,b:32}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const allV=series.flatMap(s=>s.data);
  const mn=opts.yMin!==undefined?opts.yMin:Math.max(0,Math.min(...allV)*0.9);
  const mx=opts.yMax!==undefined?opts.yMax:Math.max(...allV)*1.08;
  const fy=v=>pad.t+plotH-(v-mn)/(mx-mn)*plotH;
  const fx=i=>pad.l+i/(labels.length-1)*plotW;
  let svg='';
  for(let i=0;i<=4;i++){{
    const y=pad.t+plotH/4*i; const v=mx-(mx-mn)/4*i;
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-6}}" y="${{y+4}}" text-anchor="end" font-size="9" fill="#94A3B8">${{opts.pct?v.toFixed(0)+'%':fM(v)}}</text>`;
  }}
  labels.forEach((lb,i)=>{{
    svg+=`<text x="${{fx(i)}}" y="${{vh-6}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{lb}}</text>`;
  }});
  series.forEach(s=>{{
    if(s.bar){{
      const bw=plotW/labels.length*0.6;
      s.data.forEach((v,i)=>{{
        const x=fx(i)-bw/2; const h=Math.max(1,(v-mn)/(mx-mn)*plotH);
        const y=pad.t+plotH-h;
        svg+=`<rect x="${{x}}" y="${{y}}" width="${{bw}}" height="${{h}}" rx="2" fill="${{s.color}}" opacity=".7"
          onmouseenter="showTT(event,'<b>${{s.name}}</b><br>${{MONTHS[i]}}: ${{fM(v)}}')" onmouseleave="hideTT()"/>`;
      }});
      return;
    }}
    const pts=s.data.map((v,i)=>fx(i)+','+fy(v)).join(' ');
    svg+=`<polyline points="${{pts}}" fill="none" stroke="${{s.color}}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>`;
    s.data.forEach((v,i)=>{{
      const label=opts.pct?fP(v):fM(v);
      svg+=`<circle cx="${{fx(i)}}" cy="${{fy(v)}}" r="3.5" fill="${{s.color}}" stroke="#fff" stroke-width="1.5"
        onmouseenter="showTT(event,'<b>${{s.name}}</b><br>${{MONTHS[i]}}: ${{label}}')" onmouseleave="hideTT()"/>`;
    }});
  }});
  if(opts.target!==undefined){{
    const ty=fy(opts.target);
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{ty}}" y2="${{ty}}" stroke="#D97706" stroke-width="1.5" stroke-dasharray="5,4"/>`;
  }}
  el.innerHTML=svg;
}}

// ── waterfall helper ───────────────────────────────────────────────────
function waterfallChart(svgId,steps,vw,vh){{
  const el=document.getElementById(svgId); if(!el) return;
  el.setAttribute('viewBox','0 0 '+vw+' '+vh);
  const pad={{l:14,r:14,t:30,b:50}};
  const plotW=vw-pad.l-pad.r, plotH=vh-pad.t-pad.b;
  const n=steps.length;
  // pre-compute all bar extents to derive y-range
  let _r=0;
  const _ext=steps.flatMap(s=>{{
    const s0=s.absolute?0:_r;
    const s1=s.absolute?s.value:_r+s.value;
    if(!s.absolute) _r=s1;
    return [s0,s1];
  }});
  const mn=Math.min(0,..._ext);
  const mx=Math.max(..._ext)*1.08;
  const fy=v=>pad.t+plotH-(v-mn)/(mx-mn)*plotH;
  const bw=plotW/n*0.55;
  const gap=plotW/n;
  let svg='';
  // grid
  [0,.25,.5,.75,1].forEach(f=>{{
    const v=mn+(mx-mn)*f; const y=fy(v);
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-2}}" y="${{y+4}}" text-anchor="end" font-size="9" fill="#94A3B8">${{fM(v)}}</text>`;
  }});
  let running=0;
  steps.forEach((s,i)=>{{
    const x=pad.l+i*gap+(gap-bw)/2;
    const start=s.absolute?0:running;
    const end=s.absolute?s.value:running+s.value;
    const top=fy(Math.max(start,end));
    const bot=fy(Math.min(start,end));
    const h=Math.max(2,bot-top);
    const fc=s.color||(s.value>=0?'var(--grn)':'var(--red)');
    svg+=`<rect x="${{x}}" y="${{top}}" width="${{bw}}" height="${{h}}" rx="3" fill="${{fc}}" opacity=".88"
      onmouseenter="showTT(event,'<b>${{s.label}}</b><br>${{fM(Math.abs(s.value))}}')" onmouseleave="hideTT()"/>`;
    // connector
    if(i<n-1 && !steps[i+1].absolute){{
      svg+=`<line x1="${{x+bw}}" x2="${{x+gap}}" y1="${{fy(end)}}" y2="${{fy(end)}}" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="3,2"/>`;
    }}
    // value label
    const labelY=top-5;
    svg+=`<text x="${{x+bw/2}}" y="${{labelY}}" text-anchor="middle" font-size="9" fill="#334155" font-weight="700">${{fM(Math.abs(s.value))}}</text>`;
    // axis label
    svg+=`<text x="${{x+bw/2}}" y="${{vh-8}}" text-anchor="middle" font-size="9" fill="#475569" font-weight="600"
      transform="rotate(-20,${{x+bw/2}},${{vh-8}})">${{s.label}}</text>`;
    if(!s.absolute) running=end;
  }});
  el.innerHTML=svg;
}}

// ── KPI STRIP ─────────────────────────────────────────────────────────
function renderKPIs(){{
  const kpis=[
    {{label:'Total Revenue',    value:fM(SUM.port_rev),   delta:'30 Customers · 4 Channels', cls:'neu'}},
    {{label:'Gross Profit',     value:fM(SUM.port_gp),    delta:'GM: '+fP(SUM.port_gm),      cls:'up'}},
    {{label:'Trade Spend',      value:fM(SUM.port_trade), delta:'of Revenue',                 cls:'dn'}},
    {{label:'Net Contribution', value:fM(SUM.port_net),   delta:'CM: '+fP(SUM.port_cm),       cls:SUM.port_cm>=25?'up':'dn'}},
    {{label:'Tier A Customers', value:SUM.tier_a,         delta:SUM.tier_b+' Tier B · '+SUM.tier_c+' Tier C', cls:'up'}},
  ];
  document.getElementById('kpi-strip').innerHTML=kpis.map(k=>`
    <div class="kpi">
      <div class="kpi-label">${{k.label}}</div>
      <div class="kpi-value">${{k.value}}</div>
      <div class="kpi-delta ${{k.cls}}">${{k.delta}}</div>
    </div>`).join('');
}}

// ── OVERVIEW ──────────────────────────────────────────────────────────
function renderOverview(){{
  // Scatter: revenue vs CM%
  const el=document.getElementById('svg-scatter');
  const vw=540,vh=240,pad={{l:52,r:20,t:14,b:36}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  const revs=CD.map(c=>c.total_revenue);
  const cms=CD.map(c=>c.cm_pct);
  const maxR=Math.max(...revs)*1.1, minR=0;
  const maxC=Math.max(...cms)*1.1, minC=Math.min(...cms)*0.9;
  let svg='';
  [0,25,50,75,100].forEach(f=>{{
    const y=pad.t+plotH*(1-f/100);
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{pad.l-5}}" y="${{y+4}}" text-anchor="end" font-size="8.5" fill="#94A3B8">${{((maxC-minC)*f/100+minC).toFixed(0)}}%</text>`;
  }});
  // avg CM line
  const avgCM=(SUM.port_cm-minC)/(maxC-minC);
  const avgY=pad.t+plotH*(1-avgCM);
  svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{avgY}}" y2="${{avgY}}" stroke="#D97706" stroke-width="1.2" stroke-dasharray="5,4"/>`;
  svg+=`<text x="${{pad.l+plotW+2}}" y="${{avgY+4}}" font-size="8.5" fill="#D97706" font-weight="700">Avg</text>`;
  CD.forEach(c=>{{
    const x=pad.l+(c.total_revenue-minR)/(maxR-minR)*plotW;
    const y=pad.t+plotH*(1-(c.cm_pct-minC)/(maxC-minC));
    const rc=CH_COLORS[CHANNELS.findIndex(ch=>ch.id===c.channel)]||'#7C3AED';
    svg+=`<circle cx="${{x}}" cy="${{y}}" r="5" fill="${{rc}}" opacity=".8" stroke="#fff" stroke-width="1"
      onmouseenter="showTT(event,'<b>${{c.name}}</b><br>Rev: ${{fM(c.total_revenue)}}<br>CM: ${{fP(c.cm_pct)}}<br>Tier ${{c.tier}}')" onmouseleave="hideTT()"/>`;
  }});
  // x-axis
  svg+=`<text x="${{pad.l+plotW/2}}" y="${{vh-4}}" text-anchor="middle" font-size="9" fill="#94A3B8">Revenue →</text>`;
  svg+=`<text x="${{8}}" y="${{pad.t+plotH/2}}" text-anchor="middle" font-size="9" fill="#94A3B8" transform="rotate(-90,8,${{pad.t+plotH/2}})">CM% →</text>`;
  // legend
  CHANNELS.forEach((ch,i)=>{{
    svg+=`<circle cx="${{pad.l+10+i*110}}" cy="${{14}}" r="4" fill="${{CH_COLORS[i]}}"/>`;
    svg+=`<text x="${{pad.l+18+i*110}}" y="${{18}}" font-size="9" fill="#475569">${{ch.name}}</text>`;
  }});
  el.innerHTML=svg;

  // Tier donut
  const tiers=[
    {{label:'Tier A',value:SUM.tier_a,color:'#7C3AED'}},
    {{label:'Tier B',value:SUM.tier_b,color:'#2563EB'}},
    {{label:'Tier C',value:SUM.tier_c,color:'#D97706'}},
  ];
  const total=tiers.reduce((a,t)=>a+t.value,0);
  const el2=document.getElementById('svg-tier-donut');
  const cx=200,cy=120,R=80,r=50;
  let angle=-Math.PI/2; let svg2='';
  tiers.forEach(t=>{{
    const sweep=t.value/total*Math.PI*2;
    const x1=cx+R*Math.cos(angle),y1=cy+R*Math.sin(angle);
    const x2=cx+R*Math.cos(angle+sweep),y2=cy+R*Math.sin(angle+sweep);
    const xi=cx+r*Math.cos(angle),yi=cy+r*Math.sin(angle);
    const xo=cx+r*Math.cos(angle+sweep),yo=cy+r*Math.sin(angle+sweep);
    const lg=sweep>Math.PI?1:0;
    svg2+=`<path d="M${{xi}},${{yi}} L${{x1}},${{y1}} A${{R}},${{R}} 0 ${{lg}},1 ${{x2}},${{y2}} L${{xo}},${{yo}} A${{r}},${{r}} 0 ${{lg}},0 ${{xi}},${{yi}}Z"
      fill="${{t.color}}" opacity=".88"
      onmouseenter="showTT(event,'<b>${{t.label}}</b><br>${{t.value}} customers')" onmouseleave="hideTT()"/>`;
    const ma=angle+sweep/2;
    const lx=cx+(R+18)*Math.cos(ma),ly=cy+(R+18)*Math.sin(ma);
    svg2+=`<text x="${{lx}}" y="${{ly+4}}" text-anchor="middle" font-size="10" font-weight="700" fill="${{t.color}}">${{t.value}}</text>`;
    angle+=sweep;
  }});
  svg2+=`<text x="${{cx}}" y="${{cy-6}}" text-anchor="middle" font-size="11" fill="#334155" font-weight="700">Customers</text>`;
  svg2+=`<text x="${{cx}}" y="${{cy+10}}" text-anchor="middle" font-size="22" fill="#1E293B" font-weight="800">${{total}}</text>`;
  // legend
  tiers.forEach((t,i)=>{{
    svg2+=`<rect x="310" y="${{90+i*30}}" width="12" height="12" rx="2" fill="${{t.color}}"/>`;
    svg2+=`<text x="328" y="${{101+i*30}}" font-size="11" fill="#334155" font-weight="600">${{t.label}}: ${{t.value}} customers</text>`;
  }});
  el2.innerHTML=svg2;

  // Top 10 table
  const top10=CD.slice().sort((a,b)=>b.total_net-a.total_net).slice(0,10);
  document.getElementById('tbl-top10').innerHTML=`<thead><tr>
    <th>#</th><th>Customer</th><th>Channel</th><th>Tier</th>
    <th>Revenue</th><th>Gross Profit</th><th>Trade Spend</th><th>Net Contribution</th><th>CM%</th>
  </tr></thead><tbody>`+top10.map((c,i)=>`<tr>
    <td style="color:var(--g400);font-weight:700">${{i+1}}</td>
    <td style="font-weight:700">${{c.name}}</td>
    <td style="color:var(--g600)">${{chName(c.channel)}}</td>
    <td><span class="pill pill-${{c.tier}}">${{c.tier}}</span></td>
    <td>${{fM(c.total_revenue)}}</td>
    <td style="color:var(--grn);font-weight:700">${{fM(c.total_gp)}}</td>
    <td style="color:var(--red)">${{fM(c.total_trade)}}</td>
    <td style="font-weight:700;color:${{cmClr(c.cm_pct)}}">${{fM(c.total_net)}}</td>
    <td><span style="font-weight:700;color:${{cmClr(c.cm_pct)}}">${{fP(c.cm_pct)}}</span></td>
  </tr>`).join('')+'</tbody>';
}}

// ── BY CUSTOMER ───────────────────────────────────────────────────────
function renderByCustomer(){{
  const cid=document.getElementById('sel-cust').value;
  const c=CD.find(x=>x.id===cid);
  const skuMeta=D.skus;

  // KPIs
  document.getElementById('cust-kpi-strip').innerHTML=[
    {{l:'Revenue',   v:fM(c.total_revenue), d:'6-month total', cls:'neu'}},
    {{l:'Gross Profit', v:fM(c.total_gp),  d:'GM: '+fP(c.gm_pct), cls:'up'}},
    {{l:'Trade Spend',  v:fM(c.total_trade),d:'of Revenue',    cls:'dn'}},
    {{l:'Net Contribution',v:fM(c.total_net),d:'CM: '+fP(c.cm_pct), cls:c.cm_pct>=25?'up':'dn'}},
    {{l:'Tier',      v:c.tier,             d:chName(c.channel), cls:'neu'}},
  ].map(k=>`<div class="kpi">
    <div class="kpi-label">${{k.l}}</div>
    <div class="kpi-value">${{k.v}}</div>
    <div class="kpi-delta ${{k.cls}}">${{k.d}}</div>
  </div>`).join('');

  // Revenue & Net trend (bar + line)
  lineChart('svg-cust-trend',[
    {{name:'Revenue',      color:'#7C3AED', bar:true, data:c.rev_series}},
    {{name:'Net Contribution',color:'#059669',data:c.net_series}},
  ],MONTHS,{{h:200,pad:{{l:56,r:20,t:14,b:32}}}});

  // CM% trend
  lineChart('svg-cust-cm',[
    {{name:'CM%',color:'#7C3AED',data:c.cm_series}},
  ],MONTHS,{{h:200,pad:{{l:44,r:20,t:14,b:32}},pct:true,yMin:0,yMax:60}});

  // Waterfall
  waterfallChart('svg-cust-wf',[
    {{label:'Revenue',   value:c.total_revenue,  absolute:true, color:'#7C3AED'}},
    {{label:'– COGS',    value:-c.total_cogs,                   color:'#DC2626'}},
    {{label:'Gross Profit',value:c.total_gp,     absolute:true, color:'#059669'}},
    {{label:'– Trade',   value:-c.total_trade,                  color:'#F97316'}},
    {{label:'– Logistics',value:-c.total_logi,                  color:'#F97316'}},
    {{label:'Net Contrib.',value:c.total_net,    absolute:true, color:'#2563EB'}},
  ],540,220);

  // SKU donut
  const el=document.getElementById('svg-cust-sku');
  const cx=160,cy=110,R=80,ri=50;
  let angle=-Math.PI/2; let svg='';
  c.sku_mix.forEach((pct,i)=>{{
    const sweep=pct/100*Math.PI*2;
    const x1=cx+R*Math.cos(angle),y1=cy+R*Math.sin(angle);
    const x2=cx+R*Math.cos(angle+sweep),y2=cy+R*Math.sin(angle+sweep);
    const xi=cx+ri*Math.cos(angle),yi=cy+ri*Math.sin(angle);
    const xo=cx+ri*Math.cos(angle+sweep),yo=cy+ri*Math.sin(angle+sweep);
    const lg=sweep>Math.PI?1:0;
    svg+=`<path d="M${{xi}},${{yi}} L${{x1}},${{y1}} A${{R}},${{R}} 0 ${{lg}},1 ${{x2}},${{y2}} L${{xo}},${{yo}} A${{ri}},${{ri}} 0 ${{lg}},0 ${{xi}},${{yi}}Z"
      fill="${{SKU_COLORS[i]}}" opacity=".88"
      onmouseenter="showTT(event,'<b>${{skuMeta[i].name}}</b><br>${{pct.toFixed(1)}}% of revenue')" onmouseleave="hideTT()"/>`;
    if(sweep>0.3){{
      const ma=angle+sweep/2;
      const lx=cx+(R+16)*Math.cos(ma),ly=cy+(R+16)*Math.sin(ma);
      svg+=`<text x="${{lx}}" y="${{ly+4}}" text-anchor="middle" font-size="9.5" font-weight="700" fill="${{SKU_COLORS[i]}}">${{pct.toFixed(0)}}%</text>`;
    }}
    angle+=sweep;
  }});
  svg+=`<text x="${{cx}}" y="${{cy+5}}" text-anchor="middle" font-size="11" fill="#334155" font-weight="700">SKU Mix</text>`;
  skuMeta.forEach((s,i)=>{{
    svg+=`<rect x="290" y="${{40+i*32}}" width="11" height="11" rx="2" fill="${{SKU_COLORS[i]}}"/>`;
    svg+=`<text x="307" y="${{51+i*32}}" font-size="10" fill="#334155">${{s.name}}: ${{c.sku_mix[i].toFixed(1)}}%</text>`;
  }});
  el.innerHTML=svg;
}}

// ── BY CHANNEL ────────────────────────────────────────────────────────
function renderByChannel(){{
  // Revenue bars
  const maxRev=Math.max(...CA.map(c=>c.revenue));
  const el=document.getElementById('svg-ch-rev');
  const vw=540,vh=200,pad={{l:120,r:20,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  let svg='';
  CA.forEach((ch,i)=>{{
    const bH=28; const y=pad.t+i*(bH+8);
    const w=ch.revenue/maxRev*plotW;
    svg+=`<text x="${{pad.l-8}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10.5" fill="#475569" font-weight="600">${{ch.name}}</text>`;
    svg+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="${{CH_COLORS[i]}}" opacity=".85"
      onmouseenter="showTT(event,'<b>${{ch.name}}</b><br>Rev: ${{fM(ch.revenue)}}<br>Customers: ${{ch.n_customers}}')" onmouseleave="hideTT()"/>`;
    svg+=`<text x="${{pad.l+w+5}}" y="${{y+bH/2+4}}" font-size="10" fill="#334155" font-weight="700">${{fM(ch.revenue)}}</text>`;
  }});
  [0,.25,.5,.75,1].forEach(f=>{{
    const x=pad.l+f*plotW;
    svg+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg+=`<text x="${{x}}" y="${{pad.t+plotH+16}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{fM(maxRev*f)}}</text>`;
  }});
  el.innerHTML=svg;

  // CM% bars
  const el2=document.getElementById('svg-ch-cm');
  let svg2='';
  CA.forEach((ch,i)=>{{
    const bH=28; const y=pad.t+i*(bH+8);
    const w=ch.cm_pct/50*plotW;
    svg2+=`<text x="${{pad.l-8}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10.5" fill="#475569" font-weight="600">${{ch.name}}</text>`;
    svg2+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="${{cmClr(ch.cm_pct)}}" opacity=".85"
      onmouseenter="showTT(event,'<b>${{ch.name}}</b><br>CM: ${{fP(ch.cm_pct)}}<br>Net: ${{fM(ch.net)}}')" onmouseleave="hideTT()"/>`;
    svg2+=`<text x="${{pad.l+w+5}}" y="${{y+bH/2+4}}" font-size="10" fill="#334155" font-weight="700">${{fP(ch.cm_pct)}}</text>`;
  }});
  [0,10,20,30,40,50].forEach(v=>{{
    const x=pad.l+v/50*plotW;
    svg2+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svg2+=`<text x="${{x}}" y="${{pad.t+plotH+16}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}%</text>`;
  }});
  el2.innerHTML=svg2;

  // Channel table
  document.getElementById('tbl-channel').innerHTML=`<thead><tr>
    <th>Channel</th><th>Customers</th><th>Revenue</th><th>COGS</th>
    <th>Gross Profit</th><th>GM%</th><th>Trade Spend</th><th>Logistics</th><th>Net Contribution</th><th>CM%</th>
  </tr></thead><tbody>`+CA.map((ch,i)=>`<tr>
    <td style="font-weight:700;color:${{CH_COLORS[i]}}">${{ch.name}}</td>
    <td>${{ch.n_customers}}</td>
    <td style="font-weight:700">${{fM(ch.revenue)}}</td>
    <td style="color:var(--red)">${{fM(ch.cogs)}}</td>
    <td style="color:var(--grn);font-weight:700">${{fM(ch.gp)}}</td>
    <td style="font-weight:700">${{fP(ch.gm_pct)}}</td>
    <td style="color:#F97316">${{fM(ch.trade)}}</td>
    <td style="color:#F97316">${{fM(ch.logi)}}</td>
    <td style="font-weight:700;color:${{cmClr(ch.cm_pct)}}">${{fM(ch.net)}}</td>
    <td><span style="font-weight:700;color:${{cmClr(ch.cm_pct)}}">${{fP(ch.cm_pct)}}</span></td>
  </tr>`).join('')+'</tbody>';
}}

// ── PARETO ────────────────────────────────────────────────────────────
function renderPareto(){{
  const n=PAR.length;
  const drawPareto=(svgId,yKey,yLabel)=>{{
    const el=document.getElementById(svgId); if(!el) return;
    const vw=540,vh=220,pad={{l:44,r:44,t:14,b:32}};
    const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
    const fx=i=>pad.l+i/(n-1)*plotW;
    const fy=v=>pad.t+plotH*(1-v/100);
    let svg='';
    [0,20,40,60,80,100].forEach(v=>{{
      const y=fy(v);
      svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{y}}" y2="${{y}}" stroke="#E2E8F0" stroke-width="1"/>`;
      svg+=`<text x="${{pad.l-5}}" y="${{y+4}}" text-anchor="end" font-size="9" fill="#94A3B8">${{v}}%</text>`;
    }});
    // 80% reference
    svg+=`<line x1="${{pad.l}}" x2="${{pad.l+plotW}}" y1="${{fy(80)}}" y2="${{fy(80)}}" stroke="#D97706" stroke-width="1.2" stroke-dasharray="5,4"/>`;
    svg+=`<text x="${{pad.l+plotW+2}}" y="${{fy(80)+4}}" font-size="9" fill="#D97706" font-weight="700">80%</text>`;
    const pts=PAR.map((p,i)=>fx(i)+','+fy(p[yKey])).join(' ');
    svg+=`<polyline points="${{pts}}" fill="none" stroke="#7C3AED" stroke-width="2.2" stroke-linejoin="round"/>`;
    // area fill
    svg+=`<polygon points="${{pad.l}},${{fy(0)}} ${{pts}} ${{fx(n-1)}},${{fy(0)}}" fill="#7C3AED" opacity=".08"/>`;
    PAR.forEach((p,i)=>{{
      if(i%5===0||i===n-1)
        svg+=`<circle cx="${{fx(i)}}" cy="${{fy(p[yKey])}}" r="3" fill="#7C3AED" stroke="#fff" stroke-width="1.5"
          onmouseenter="showTT(event,'<b>#${{p.rank}} ${{p.name}}</b><br>${{yLabel}}: ${{p[yKey].toFixed(1)}}%')" onmouseleave="hideTT()"/>`;
    }});
    // x ticks
    [1,6,12,18,24,30].forEach(v=>{{
      if(v<=n){{
        const x=fx(v-1);
        svg+=`<text x="${{x}}" y="${{vh-4}}" text-anchor="middle" font-size="9" fill="#94A3B8">#${{v}}</text>`;
      }}
    }});
    el.innerHTML=svg;
  }};
  drawPareto('svg-pareto-rev','cum_rev_pct','Cum. Revenue');
  drawPareto('svg-pareto-net','cum_net_pct','Cum. Net Contribution');

  // Full table
  document.getElementById('tbl-pareto').innerHTML=`<thead><tr>
    <th>Rank</th><th>Customer</th><th>Channel</th><th>Tier</th>
    <th>Revenue</th><th>Cum Rev%</th><th>Net Contribution</th><th>Cum Net%</th><th>CM%</th>
  </tr></thead><tbody>`+PAR.map(p=>`<tr>
    <td style="color:var(--g400);font-weight:700">${{p.rank}}</td>
    <td style="font-weight:700">${{p.name}}</td>
    <td style="color:var(--g600)">${{chName(p.channel)}}</td>
    <td><span class="pill pill-${{p.tier}}">${{p.tier}}</span></td>
    <td>${{fM(p.revenue)}}</td>
    <td>
      <div style="display:flex;align-items:center;gap:6px">
        <div class="bar-wrap"><div class="bar-fill" style="width:${{p.cum_rev_pct}}%;background:#7C3AED"></div></div>
        <span style="font-weight:700;color:#7C3AED">${{fP(p.cum_rev_pct)}}</span>
      </div>
    </td>
    <td style="font-weight:700;color:${{cmClr(p.cm_pct)}}">${{fM(p.net)}}</td>
    <td>
      <div style="display:flex;align-items:center;gap:6px">
        <div class="bar-wrap"><div class="bar-fill" style="width:${{Math.min(100,p.cum_net_pct)}}%;background:#059669"></div></div>
        <span style="font-weight:700;color:#059669">${{fP(p.cum_net_pct)}}</span>
      </div>
    </td>
    <td><span style="font-weight:700;color:${{cmClr(p.cm_pct)}}">${{fP(p.cm_pct)}}</span></td>
  </tr>`).join('')+'</tbody>';
}}

// ── WATERFALL ─────────────────────────────────────────────────────────
function renderWaterfall(){{
  waterfallChart('svg-port-wf',[
    {{label:'Revenue',    value:SUM.port_rev,   absolute:true, color:'#7C3AED'}},
    {{label:'– COGS',     value:-(SUM.port_rev-SUM.port_gp),  color:'#DC2626'}},
    {{label:'Gross Profit',value:SUM.port_gp,   absolute:true, color:'#059669'}},
    {{label:'– Trade',    value:-SUM.port_trade,              color:'#F97316'}},
    {{label:'– Logistics',value:-SUM.port_logi,              color:'#F97316'}},
    {{label:'Net Contrib.',value:SUM.port_net,  absolute:true, color:'#2563EB'}},
  ],700,300);

  // GM% by channel
  const elG=document.getElementById('svg-gm-ch');
  const vw=540,vh=200,pad={{l:120,r:20,t:14,b:24}};
  const plotW=vw-pad.l-pad.r,plotH=vh-pad.t-pad.b;
  let svgG='';
  CA.forEach((ch,i)=>{{
    const bH=28; const y=pad.t+i*(bH+8);
    const w=ch.gm_pct/80*plotW;
    svgG+=`<text x="${{pad.l-8}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10.5" fill="#475569" font-weight="600">${{ch.name}}</text>`;
    svgG+=`<rect x="${{pad.l}}" y="${{y}}" width="${{w}}" height="${{bH}}" rx="3" fill="${{CH_COLORS[i]}}" opacity=".85"/>`;
    svgG+=`<text x="${{pad.l+w+5}}" y="${{y+bH/2+4}}" font-size="10" fill="#334155" font-weight="700">${{fP(ch.gm_pct)}}</text>`;
  }});
  [0,20,40,60,80].forEach(v=>{{
    const x=pad.l+v/80*plotW;
    svgG+=`<line x1="${{x}}" x2="${{x}}" y1="${{pad.t}}" y2="${{pad.t+plotH}}" stroke="#E2E8F0" stroke-width="1"/>`;
    svgG+=`<text x="${{x}}" y="${{pad.t+plotH+16}}" text-anchor="middle" font-size="9" fill="#94A3B8">${{v}}%</text>`;
  }});
  elG.innerHTML=svgG;

  // Cost structure stacked bar by channel
  const elC=document.getElementById('svg-cost-ch');
  const costKeys=[
    {{key:'cogs', label:'COGS',      color:'#DC2626'}},
    {{key:'trade',label:'Trade',     color:'#F97316'}},
    {{key:'logi', label:'Logistics', color:'#FBBF24'}},
  ];
  let svgC='';
  CA.forEach((ch,i)=>{{
    const bH=28; const y=pad.t+i*(bH+8);
    let xOff=pad.l;
    costKeys.forEach(k=>{{
      const pct=ch[k.key]/ch.revenue*100;
      const w=pct/100*plotW;
      svgC+=`<rect x="${{xOff}}" y="${{y}}" width="${{w}}" height="${{bH}}" fill="${{k.color}}" opacity=".85"
        onmouseenter="showTT(event,'<b>${{ch.name}} — ${{k.label}}</b><br>${{pct.toFixed(1)}}% of Revenue')" onmouseleave="hideTT()"/>`;
      if(w>20) svgC+=`<text x="${{xOff+w/2}}" y="${{y+bH/2+4}}" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">${{pct.toFixed(0)}}%</text>`;
      xOff+=w;
    }});
    svgC+=`<text x="${{pad.l-8}}" y="${{y+bH/2+4}}" text-anchor="end" font-size="10.5" fill="#475569" font-weight="600">${{ch.name}}</text>`;
  }});
  costKeys.forEach((k,i)=>{{
    svgC+=`<rect x="${{pad.l+i*100}}" y="${{pad.t+plotH+14}}" width="10" height="10" rx="2" fill="${{k.color}}"/>`;
    svgC+=`<text x="${{pad.l+i*100+14}}" y="${{pad.t+plotH+23}}" font-size="9.5" fill="#475569">${{k.label}}</text>`;
  }});
  elC.innerHTML=svgC;
}}

// ── INIT ──────────────────────────────────────────────────────────────
renderKPIs();
renderOverview();
</script>
</body>
</html>"""

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Customer_Profitability_Dashboard.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML)
size_kb = round(os.path.getsize(out_path) / 1024, 1)
print(f"Done!  {size_kb} KB  ->  {out_path}")
