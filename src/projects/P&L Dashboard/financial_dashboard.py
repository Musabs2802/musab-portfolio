"""
Financial Dashboard v3 — P&L · Cash Flow · Balance Sheet
- Column expansion: Year → Quarter → Month (click year/Q header)
- Row collapse: click section header to collapse sub-items
- Tab spacing: 12px gap between tabs and KPI strip
"""
import os, json
from datetime import datetime as _dt

TODAY = _dt.now().strftime("%d %B %Y")
YEARS = [2022, 2023, 2024]
BF    = 1.05

MW = [0.072,0.068,0.082,0.085,0.088,0.083,0.080,0.082,0.086,0.090,0.092,0.092]
MN = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
QN = ['Q1','Q2','Q3','Q4']

# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA
# ─────────────────────────────────────────────────────────────────────────────
PL_REV  = {
    'Product Sales':           [88_200_000, 105_800_000, 124_600_000],
    'Service Revenue':         [ 7_400_000,   9_300_000,  11_800_000],
    'Other Revenue':           [ 1_600_000,   2_100_000,   2_600_000],
}
PL_COGS = {
    'Direct Materials':        [34_200_000, 40_600_000, 47_100_000],
    'Direct Labour':           [ 9_800_000, 11_200_000, 12_900_000],
    'Manufacturing Overhead':  [ 6_300_000,  7_400_000,  8_500_000],
}
PL_OPEX = {
    'Sales & Distribution':    [11_200_000, 13_400_000, 15_600_000],
    'Marketing':               [ 6_800_000,  8_200_000,  9_700_000],
    'Research & Development':  [ 5_400_000,  6_900_000,  8_100_000],
    'General & Administrative':[ 4_200_000,  5_100_000,  5_900_000],
}
PL_DA  = [2_100_000, 2_500_000, 2_900_000]
PL_INT = [1_200_000, 1_050_000,   900_000]
PL_OTH = [  320_000,   280_000,   240_000]
PL_TAX = [3_490_000, 4_310_000, 5_410_000]

CF_OPS = {
    'Net Income':                 [15_900_000, 19_780_000, 24_950_000],
    'Add: D&A':                   [ 2_100_000,  2_500_000,  2_900_000],
    'Change in Receivables':      [-3_200_000, -3_900_000, -4_600_000],
    'Change in Inventories':      [-2_100_000, -2_400_000, -2_800_000],
    'Change in Payables':         [ 1_800_000,  2_100_000,  2_500_000],
    'Other Working Capital Adj.': [   480_000,    620_000,    780_000],
}
CF_INV = {
    'Purchase of PP&E':          [-8_400_000,-10_200_000,-12_400_000],
    'Acquisitions':              [-2_000_000, -3_500_000, -1_800_000],
    'Proceeds from Asset Sales': [   620_000,    810_000,    940_000],
    'Purchase of Investments':   [-1_500_000, -2_000_000, -2_400_000],
}
CF_FIN = {
    'Proceeds from Borrowings':  [ 5_000_000,  4_000_000,  3_000_000],
    'Repayment of Debt':         [-4_200_000, -4_800_000, -5_400_000],
    'Dividends Paid':            [-2_400_000, -3_100_000, -4_000_000],
    'Share Buybacks':            [-1_000_000, -1_500_000, -2_000_000],
}
BS_CA  = {
    'Cash & Cash Equivalents':     [18_400_000, 21_600_000, 25_300_000],
    'Accounts Receivable':         [14_200_000, 17_100_000, 20_700_000],
    'Inventories':                 [ 9_800_000, 11_400_000, 13_200_000],
    'Prepaid Expenses & Other':    [ 2_400_000,  2_900_000,  3_500_000],
}
BS_NCA = {
    'Property, Plant & Equipment': [28_600_000, 35_400_000, 44_200_000],
    'Intangible Assets':           [ 7_200_000,  8_400_000,  9_800_000],
    'Right-of-Use Assets':         [ 4_100_000,  4_600_000,  5_100_000],
    'Long-term Investments':       [ 5_800_000,  7_200_000,  9_000_000],
}
BS_CL  = {
    'Accounts Payable':    [11_400_000, 13_200_000, 15_600_000],
    'Short-term Debt':     [ 4_800_000,  4_200_000,  3_600_000],
    'Accrued Liabilities': [ 3_200_000,  3_800_000,  4_400_000],
    'Deferred Revenue':    [ 1_200_000,  1_500_000,  1_800_000],
}
BS_NCL = {
    'Long-term Debt':              [18_600_000, 17_800_000, 15_400_000],
    'Deferred Tax Liabilities':    [ 2_100_000,  2_400_000,  2_700_000],
    'Other Long-term Liabilities': [ 1_400_000,  1_600_000,  1_800_000],
}
BS_EQ  = {
    'Share Capital':     [12_000_000, 12_000_000, 12_000_000],
    'Retained Earnings': [22_800_000, 38_580_000, 58_130_000],
    'Other Reserves':    [ 3_100_000,  3_620_000,  4_170_000],
}

# ─────────────────────────────────────────────────────────────────────────────
# DERIVED
# ─────────────────────────────────────────────────────────────────────────────
def cs(d): return [sum(r[i] for r in d.values()) for i in range(3)]

rev    = cs(PL_REV);  cogs   = cs(PL_COGS)
gp     = [rev[i]-cogs[i]     for i in range(3)]
opex   = cs(PL_OPEX)
ebitda = [gp[i]-opex[i]      for i in range(3)]
ebit   = [ebitda[i]-PL_DA[i] for i in range(3)]
ebt    = [ebit[i]-PL_INT[i]-PL_OTH[i] for i in range(3)]
ni     = [ebt[i]-PL_TAX[i]   for i in range(3)]
gm  = [gp[i]/rev[i]*100    for i in range(3)]
ebm = [ebitda[i]/rev[i]*100 for i in range(3)]
eim = [ebit[i]/rev[i]*100   for i in range(3)]
nim = [ni[i]/rev[i]*100     for i in range(3)]

cfo = cs(CF_OPS); cfi = cs(CF_INV); cff = cs(CF_FIN)
ncf = [cfo[i]+cfi[i]+cff[i] for i in range(3)]

cur_ast=cs(BS_CA); nc_ast=cs(BS_NCA); tot_ast=[cur_ast[i]+nc_ast[i] for i in range(3)]
cur_lia=cs(BS_CL); nc_lia=cs(BS_NCL); tot_lia=[cur_lia[i]+nc_lia[i] for i in range(3)]
tot_eq=cs(BS_EQ)
curr_rat=[cur_ast[i]/cur_lia[i]            for i in range(3)]
debt_eq=[(cur_lia[i]+nc_lia[i])/tot_eq[i] for i in range(3)]
roe=[ni[i]/tot_eq[i]*100  for i in range(3)]
roa=[ni[i]/tot_ast[i]*100 for i in range(3)]

bud_rev=round(rev[2]*BF); bud_gp=round(gp[2]*BF)
bud_ebitda=round(ebitda[2]*BF); bud_ni=round(ni[2]*BF)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def yoy(a,b):   return (b-a)/abs(a)*100 if a else 0
def cagr3(a,b): return ((b/a)**0.5-1)*100 if a>0 else 0
def mvals(av):  return [[round(av[yi]*w) for w in MW] for yi in range(3)]
def qvals(av):
    m=mvals(av)
    return [[sum(m[yi][q*3:q*3+3]) for q in range(4)] for yi in range(3)]
def fmt_b(n):
    s=f"{abs(n)/1_000_000:.1f}M" if abs(n)>=1_000_000 else f"{abs(n)/1_000:.0f}K"
    return f"({s})" if n<0 else s

# ─────────────────────────────────────────────────────────────────────────────
# COLUMN EXPANSION CSS (generated)
# ─────────────────────────────────────────────────────────────────────────────
def col_css():
    lines = []
    hidden = []
    for yi in range(3):
        for qi in range(4):
            hidden.append(f'.col-yr{yi}-q{qi}')
            for mi in range(3):
                hidden.append(f'.col-yr{yi}-q{qi}-m{qi*3+mi}')
    lines.append(','.join(hidden)+'{display:none}')
    for yi in range(3):
        s=','.join(f'.tbl.exp-yr{yi} .col-yr{yi}-q{qi}' for qi in range(4))
        lines.append(s+'{display:table-cell}')
    for yi in range(3):
        for qi in range(4):
            s=','.join(f'.tbl.exp-yr{yi}-q{qi} .col-yr{yi}-q{qi}-m{qi*3+mi}' for mi in range(3))
            lines.append(s+'{display:table-cell}')
    return '\n'.join(lines)

COL_CSS = col_css()

# ─────────────────────────────────────────────────────────────────────────────
# P&L TABLE BUILDERS
# ─────────────────────────────────────────────────────────────────────────────
def _fv(v, tiny=False):
    neg=v<0; s=f"{abs(v)/1e6:,.2f}"
    pfx="(" if neg else ""; sfx=")" if neg else ""
    neg_cls=" nc_neg" if neg else ""
    t_cls=" nc_t" if tiny else ""
    return neg_cls+t_cls, pfx+s+sfx

def td_val(v, extra="", tiny=False):
    cls_extra, txt = _fv(v, tiny)
    cls=("nc"+cls_extra+(f" {extra}" if extra else "")).strip()
    return f'<td class="{cls}">{txt}</td>'

def pl_all_cols(annual_vals):
    qv=qvals(annual_vals); mv=mvals(annual_vals); out=""
    for yi in range(3):
        for qi in range(4):
            for mi in range(3):
                midx=qi*3+mi
                out+=td_val(mv[yi][midx], f"col-yr{yi}-q{qi}-m{midx}", tiny=True)
            out+=td_val(qv[yi][qi], f"col-yr{yi}-q{qi}", tiny=True)
        out+=td_val(annual_vals[yi])
    p=yoy(annual_vals[1],annual_vals[2])
    out+=f'<td class="{"yoy_up" if p>=0 else "yoy_dn"}">{"▲" if p>=0 else "▼"}{abs(p):.1f}%</td>'
    cg=cagr3(annual_vals[0],annual_vals[2])
    out+=f'<td class="{"cagr_up" if cg>=0 else "cagr_dn"}">{abs(cg):.1f}%{"▲" if cg>=0 else "▼"}</td>'
    return out

def pl_pct_cols(pct_vals):
    out=""
    for yi in range(3):
        for qi in range(4):
            for mi in range(3):
                out+=f'<td class="col-yr{yi}-q{qi}-m{qi*3+mi} nc_dim">&mdash;</td>'
            out+=f'<td class="col-yr{yi}-q{qi} nc_dim">&mdash;</td>'
        out+=f'<td class="pct_val">{pct_vals[yi]:.1f}%</td>'
    pp=pct_vals[2]-pct_vals[1]
    out+=f'<td class="{"yoy_up" if pp>=0 else "yoy_dn"}" style="font-size:10.5px">{"▲" if pp>=0 else "▼"}{abs(pp):.1f}pp</td>'
    out+='<td class="nc_dim">&mdash;</td>'
    return out

def pl_header():
    r1='<tr class="th-r1">'
    r1+='<th class="lbl-th" rowspan="2">Line Item</th>'
    for yi in range(3):
        r1+=(f'<th id="pl-th-yr{yi}" colspan="1" class="th-yr-grp"'
             f' onclick="togglePLYear({yi},event)">'
             f'<span class="col-xbtn" id="pl-cbtn-yr{yi}">+</span>'
             f'FY{YEARS[yi]}</th>')
    r1+='<th rowspan="2" class="th-meta">YoY %</th>'
    r1+='<th rowspan="2" class="th-meta">CAGR</th>'
    r1+='</tr>'
    r2='<tr class="th-r2">'
    for yi in range(3):
        for qi in range(4):
            for mi in range(3):
                midx=qi*3+mi
                r2+=f'<th class="col-yr{yi}-q{qi}-m{midx} th-m">{MN[midx]}</th>'
            r2+=(f'<th class="col-yr{yi}-q{qi} th-q"'
                 f' onclick="togglePLQtr({yi},{qi},event)">'
                 f'<span class="col-xbtn sm" id="pl-cbtn-yr{yi}-q{qi}">+</span>'
                 f'{QN[qi]}</th>')
        r2+=f'<th class="th-ann">FY{str(YEARS[yi])[-2:]}</th>'
    r2+='</tr>'
    return r1+r2

def pl_shdr(label, sec_id):
    return (f'<tr class="t-shdr" onclick="toggleSec(\'{sec_id}\',event)">'
            f'<td colspan="99">'
            f'<span class="sec-arr" id="sarr-{sec_id}">&#9660;</span> {label}'
            f'</td></tr>')

def pl_row(label, vals, cls="t-sub", sec=None, indent=0):
    lbl_cls="lbl"+(f" lbl-il{indent}" if indent else "")
    sec_attr=f' data-sec="{sec}"' if sec else ""
    return (f'<tr class="{cls}"{sec_attr}>'
            f'<td class="{lbl_cls}">{label}</td>'
            f'{pl_all_cols(vals)}</tr>')

def pl_pctrow(label, pct_vals):
    return (f'<tr class="t-pct">'
            f'<td class="lbl lbl-pct">&#x2514; {label}</td>'
            f'{pl_pct_cols(pct_vals)}</tr>')

def build_pl_table():
    r=[]
    r.append(pl_shdr('Revenue','rev'))
    for k,v in PL_REV.items(): r.append(pl_row(k,v,sec='rev',indent=1))
    r.append(pl_row('Total Revenue',rev,cls='t-total row-rev'))
    r.append(pl_pctrow('YoY Growth',[0,yoy(rev[0],rev[1]),yoy(rev[1],rev[2])]))

    r.append(pl_shdr('Cost of Goods Sold','cogs'))
    for k,v in PL_COGS.items(): r.append(pl_row(k,v,sec='cogs',indent=1))
    r.append(pl_row('Total COGS',cogs,cls='t-bold'))
    r.append(pl_row('Gross Profit',gp,cls='t-total row-gp'))
    r.append(pl_pctrow('Gross Margin',gm))

    r.append(pl_shdr('Operating Expenses','opex'))
    for k,v in PL_OPEX.items(): r.append(pl_row(k,v,sec='opex',indent=1))
    r.append(pl_row('Total OpEx',opex,cls='t-bold'))
    r.append(pl_row('EBITDA',ebitda,cls='t-total row-ebitda'))
    r.append(pl_pctrow('EBITDA Margin',ebm))

    r.append(pl_shdr('Below EBITDA','belows'))
    r.append(pl_row('Depreciation & Amortisation',PL_DA,sec='belows',indent=1))
    r.append(pl_row('EBIT',ebit,cls='t-total row-ebit'))
    r.append(pl_pctrow('EBIT Margin',eim))
    r.append(pl_row('Interest Expense',PL_INT,sec='belows',indent=1))
    r.append(pl_row('Other Expense / (Income)',PL_OTH,sec='belows',indent=1))
    r.append(pl_row('Earnings Before Tax',ebt,cls='t-bold'))
    r.append(pl_row('Income Tax (18%)',PL_TAX,sec='belows',indent=1))
    r.append(pl_row('Net Income',ni,cls='t-total row-ni'))
    r.append(pl_pctrow('Net Margin',nim))
    return '\n'.join(r)

# ─────────────────────────────────────────────────────────────────────────────
# CF / BS TABLE BUILDERS  (static 4-col: Label + 3 years + YoY)
# ─────────────────────────────────────────────────────────────────────────────
def _sv(v):
    neg=v<0; s=f"{abs(v)/1e6:,.2f}"
    return f'<td class="{"nc_neg" if neg else "nc"}">{"("+s+")" if neg else s}</td>'

def _yc(a,b):
    p=yoy(a,b)
    return f'<td class="{"yoy_up" if p>=0 else "yoy_dn"}">{"▲" if p>=0 else "▼"}{abs(p):.1f}%</td>'

def _shdr4(label, sec_id):
    return (f'<tr class="t-shdr" onclick="toggleSec(\'{sec_id}\',event)">'
            f'<td colspan="99"><span class="sec-arr" id="sarr-{sec_id}">&#9660;</span> {label}</td></tr>')

def _row4(label, vals, cls='t-sub', sec=None, indent=0):
    il=f' lbl-il{indent}' if indent else ''
    sa=f' data-sec="{sec}"' if sec else ''
    y22,y23,y24=vals
    return (f'<tr class="{cls}"{sa}><td class="lbl{il}">{label}</td>'
            f'{_sv(y22)}{_sv(y23)}{_sv(y24)}{_yc(y23,y24)}</tr>')

def build_cf_table():
    r=[]
    r.append(_shdr4('Operating Activities','cfo'))
    for k,v in CF_OPS.items(): r.append(_row4(k,v,sec='cfo',indent=1))
    r.append(_row4('Net Cash from Operations',cfo,cls='t-total'))
    r.append(_shdr4('Investing Activities','cfi'))
    for k,v in CF_INV.items(): r.append(_row4(k,v,sec='cfi',indent=1))
    r.append(_row4('Net Cash from Investing',cfi,cls='t-total'))
    r.append(_shdr4('Financing Activities','cff'))
    for k,v in CF_FIN.items(): r.append(_row4(k,v,sec='cff',indent=1))
    r.append(_row4('Net Cash from Financing',cff,cls='t-total'))
    r.append(_row4('Net Change in Cash',ncf,cls='t-bold'))
    return '\n'.join(r)

def build_bs_table():
    r=[]
    r.append(_shdr4('Current Assets','bsca'))
    for k,v in BS_CA.items():  r.append(_row4(k,v,sec='bsca',indent=1))
    r.append(_row4('Total Current Assets',cur_ast,cls='t-total'))
    r.append(_shdr4('Non-Current Assets','bsnca'))
    for k,v in BS_NCA.items(): r.append(_row4(k,v,sec='bsnca',indent=1))
    r.append(_row4('Total Non-Current Assets',nc_ast,cls='t-total'))
    r.append(_row4('TOTAL ASSETS',tot_ast,cls='t-bold'))
    r.append(_shdr4('Current Liabilities','bscl'))
    for k,v in BS_CL.items():  r.append(_row4(k,v,sec='bscl',indent=1))
    r.append(_row4('Total Current Liabilities',cur_lia,cls='t-total'))
    r.append(_shdr4('Non-Current Liabilities','bsncl'))
    for k,v in BS_NCL.items(): r.append(_row4(k,v,sec='bsncl',indent=1))
    r.append(_row4('Total Non-Current Liabilities',nc_lia,cls='t-total'))
    r.append(_row4('TOTAL LIABILITIES',tot_lia,cls='t-bold'))
    r.append(_shdr4("Shareholders' Equity",'bseq'))
    for k,v in BS_EQ.items():  r.append(_row4(k,v,sec='bseq',indent=1))
    r.append(_row4('TOTAL EQUITY',tot_eq,cls='t-bold'))
    r.append(_row4('TOTAL LIABILITIES & EQUITY',[tot_lia[i]+tot_eq[i] for i in range(3)],cls='t-total'))
    return '\n'.join(r)

# ─────────────────────────────────────────────────────────────────────────────
# PRE-RENDER
# ─────────────────────────────────────────────────────────────────────────────
PL_HEADER = pl_header()
PL_ROWS   = build_pl_table()
CF_ROWS   = build_cf_table()
BS_ROWS   = build_bs_table()

CHART_DATA = json.dumps({
    "years":YEARS,"rev":rev,"gp":gp,"ebitda":ebitda,"ebit":ebit,"ni":ni,
    "gm":[round(x,2) for x in gm],"ebm":[round(x,2) for x in ebm],
    "eim":[round(x,2) for x in eim],"nim":[round(x,2) for x in nim],
    "cfo":cfo,"cfi":cfi,"cff":cff,"ncf":ncf,
    "cur_ast":cur_ast,"nc_ast":nc_ast,"tot_ast":tot_ast,
    "cur_lia":cur_lia,"nc_lia":nc_lia,"tot_lia":tot_lia,"tot_eq":tot_eq,
    "curr_rat":[round(x,2) for x in curr_rat],
    "debt_eq":[round(x,2) for x in debt_eq],
    "roe":[round(x,2) for x in roe],"roa":[round(x,2) for x in roa],
    "opex_items":{k:v for k,v in PL_OPEX.items()},
    "bud":{"rev":bud_rev,"gp":bud_gp,"ebitda":bud_ebitda,"ni":bud_ni},
})

def kpi_badge(val):
    cls="bdg-up" if val>=0 else "bdg-dn"
    return f'<span class="kpi-badge {cls}">{"▲" if val>=0 else "▼"} {abs(val):.1f}%</span>'

def bud_badge(act,bud):
    p=(act-bud)/abs(bud)*100
    cls="bdg-up" if p>=0 else "bdg-dn"
    return f'<span class="kpi-badge {cls}">{"▲" if p>=0 else "▼"} {abs(p):.1f}% vs Bud</span>'

# ─────────────────────────────────────────────────────────────────────────────
# JAVASCRIPT  (plain strings — no f-string braces to escape)
# ─────────────────────────────────────────────────────────────────────────────
JS_TABS = """
function switchTab(id, btn) {
  document.querySelectorAll('.tab-panel').forEach(function(p){ p.classList.remove('active'); });
  document.querySelectorAll('.tab-btn').forEach(function(b){ b.classList.remove('active'); });
  document.getElementById('tab-' + id).classList.add('active');
  btn.classList.add('active');
  setTimeout(drawAllCharts, 80);
}
"""

JS_TABLES = """
// ── P&L Column Expansion ─────────────────────────────────────────────────
var plSt = {};

function getYrSpan(yi) {
  if (!plSt['yr' + yi]) return 1;
  var s = 5;
  for (var qi = 0; qi < 4; qi++) {
    if (plSt['yr' + yi + '-q' + qi]) s += 3;
  }
  return s;
}

function refreshSpans() {
  for (var yi = 0; yi < 3; yi++) {
    var th = document.getElementById('pl-th-yr' + yi);
    if (th) th.colSpan = getYrSpan(yi);
  }
}

function togglePLYear(yi, e) {
  e.stopPropagation();
  var tbl = document.getElementById('pl-tbl');
  if (!tbl) return;
  var k = 'yr' + yi;
  plSt[k] = !plSt[k];
  var btn = document.getElementById('pl-cbtn-yr' + yi);
  if (plSt[k]) {
    tbl.classList.add('exp-yr' + yi);
    if (btn) { btn.textContent = '\u2212'; btn.classList.add('open'); }
  } else {
    for (var qi = 0; qi < 4; qi++) {
      plSt['yr' + yi + '-q' + qi] = false;
      tbl.classList.remove('exp-yr' + yi + '-q' + qi);
      var qb = document.getElementById('pl-cbtn-yr' + yi + '-q' + qi);
      if (qb) { qb.textContent = '+'; qb.classList.remove('open'); }
    }
    tbl.classList.remove('exp-yr' + yi);
    if (btn) { btn.textContent = '+'; btn.classList.remove('open'); }
  }
  refreshSpans();
}

function togglePLQtr(yi, qi, e) {
  e.stopPropagation();
  var tbl = document.getElementById('pl-tbl');
  if (!tbl || !plSt['yr' + yi]) return;
  var k = 'yr' + yi + '-q' + qi;
  plSt[k] = !plSt[k];
  var btn = document.getElementById('pl-cbtn-yr' + yi + '-q' + qi);
  if (plSt[k]) {
    tbl.classList.add('exp-' + k);
    if (btn) { btn.textContent = '\u2212'; btn.classList.add('open'); }
  } else {
    tbl.classList.remove('exp-' + k);
    if (btn) { btn.textContent = '+'; btn.classList.remove('open'); }
  }
  refreshSpans();
}

// ── Row Section Collapse ─────────────────────────────────────────────────
var secSt = {};

function toggleSec(secId, e) {
  e.stopPropagation();
  secSt[secId] = !secSt[secId];
  var arr = document.getElementById('sarr-' + secId);
  var collapsed = secSt[secId];
  document.querySelectorAll('[data-sec="' + secId + '"]').forEach(function(r) {
    r.style.display = collapsed ? 'none' : '';
  });
  if (arr) arr.style.transform = collapsed ? 'rotate(-90deg)' : '';
}
"""

# ─────────────────────────────────────────────────────────────────────────────
# RATIO ROWS helper
# ─────────────────────────────────────────────────────────────────────────────
def ratio_vals_html(vals, fmt):
    return ''.join(f'<div class="rv-yr"><div class="rv">{fmt(v)}</div><div class="rl">FY{y}</div></div>'
                   for v,y in zip(vals,YEARS))

# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Financial Dashboard — FY{YEARS[0]}–{YEARS[-1]}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:13.5px}}
:root{{
  --bg:#EEF2F7;--surface:#fff;--surface2:#F8FAFC;
  --border:#CBD5E1;--border-s:#E2E8F0;
  --b900:#0F2A5E;--b800:#1E3A8A;--b700:#1D4ED8;
  --b600:#2563EB;--b500:#3B82F6;--b400:#60A5FA;--b300:#93C5FD;
  --b200:#BFDBFE;--b100:#DBEAFE;--b50:#EFF6FF;
  --text:#0F172A;--tmid:#334155;--tmuted:#64748B;--tfaint:#94A3B8;
  --pos:#059669;--pos-bg:#ECFDF5;--neg:#DC2626;--neg-bg:#FEF2F2;
  --warn:#D97706;
  --sh:0 1px 3px rgba(15,42,94,.05),0 1px 2px rgba(15,42,94,.04);
  --sh-lg:0 4px 16px rgba(15,42,94,.08);--r:8px;
}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh;}}

/* ── HEADER ── */
.app-hdr{{
  background:linear-gradient(135deg,var(--b900) 0%,var(--b800) 55%,var(--b700) 100%);
  padding:18px 28px;display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:12px;border-bottom:3px solid var(--b600);
  box-shadow:0 4px 20px rgba(15,42,94,.28);position:relative;overflow:hidden;
}}
.app-hdr::after{{
  content:'';position:absolute;top:-60px;right:-60px;width:200px;height:200px;
  border-radius:50%;background:radial-gradient(circle,rgba(96,165,250,.12) 0%,transparent 70%);
  pointer-events:none;
}}
.hdr-title{{
  font-size:18px;font-weight:800;letter-spacing:-.3px;
  background:linear-gradient(90deg,#fff 40%,var(--b300));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.hdr-sub{{font-size:11px;color:rgba(255,255,255,.42);margin-top:2px;}}
.hdr-right{{display:flex;align-items:center;gap:8px;position:relative;z-index:1;}}
.hdr-badge{{font-size:11px;font-weight:600;color:rgba(255,255,255,.65);
  background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);
  border-radius:20px;padding:3px 12px;}}
.hdr-guide{{font-size:11px;font-weight:700;color:#93C5FD;
  background:rgba(37,99,235,.28);border:1px solid rgba(147,197,253,.25);
  border-radius:20px;padding:3px 12px;cursor:pointer;transition:all .15s;}}
.hdr-guide:hover{{background:rgba(37,99,235,.55);color:#fff;}}

/* ── TAB NAV ── */
.tab-nav{{
  background:var(--surface);
  border-bottom:2px solid var(--border-s);
  overflow-x:auto;scrollbar-width:none;
  box-shadow:0 2px 8px rgba(15,42,94,.05);
}}
.tab-nav::-webkit-scrollbar{{display:none;}}
.tab-nav-inner{{display:flex;padding:0 22px;gap:0;flex-shrink:0;min-width:100%;}}
.tab-btn{{
  display:flex;align-items:center;gap:6px;
  padding:0 20px;height:44px;
  font-size:12px;font-weight:600;color:var(--tmuted);
  background:none;border:none;cursor:pointer;white-space:nowrap;
  border-bottom:3px solid transparent;margin-bottom:-2px;
  transition:color .15s,border-color .15s,background .15s;letter-spacing:.1px;
}}
.tab-btn:hover{{color:var(--b700);background:var(--b50);}}
.tab-btn.active{{color:var(--b700);border-bottom-color:var(--b600);background:var(--b50);}}
.tab-btn svg{{width:14px;height:14px;opacity:.5;flex-shrink:0;transition:opacity .15s;}}
.tab-btn:hover svg,.tab-btn.active svg{{opacity:1;}}

/* ── TAB→KPI SPACER ── */
.tab-kpi-gap{{height:14px;background:var(--bg);}}

/* ── KPI STRIP ── */
.kpi-strip{{
  display:grid;grid-template-columns:repeat(6,1fr);
  background:var(--surface);
  border-bottom:1px solid var(--border-s);
  border-radius:0;
  box-shadow:var(--sh);
  margin:0 16px;border-radius:var(--r);
  overflow:hidden;
}}
.kpi-card{{
  padding:13px 16px 11px;border-right:1px solid var(--border-s);
  position:relative;overflow:hidden;transition:background .15s;cursor:default;
}}
.kpi-card:last-child{{border-right:none;}}
.kpi-card:hover{{background:var(--b50);}}
.kpi-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--kpi-clr,var(--b400));}}
.kpi-lbl{{font-size:9.5px;font-weight:700;color:var(--tfaint);text-transform:uppercase;letter-spacing:.7px;margin-bottom:5px;}}
.kpi-val{{font-size:17px;font-weight:800;color:var(--text);letter-spacing:-.2px;line-height:1.2;}}
.kpi-sub{{font-size:10px;color:var(--tfaint);margin-top:2px;}}
.kpi-badge{{display:inline-flex;align-items:center;gap:2px;font-size:10px;font-weight:700;
  border-radius:20px;padding:2px 7px;margin-top:5px;}}
.bdg-up{{background:var(--pos-bg);color:var(--pos);border:1px solid #6EE7B7;}}
.bdg-dn{{background:var(--neg-bg);color:var(--neg);border:1px solid #FCA5A5;}}

/* ── MAIN ── */
.main{{padding:14px 16px 28px;max-width:1700px;margin:0 auto;}}
.kpi-row{{margin-bottom:14px;}}
.tab-panel{{display:none;}}.tab-panel.active{{display:block;}}

/* ── SECTION HEADER ── */
.sec-hdr{{display:flex;justify-content:space-between;align-items:center;margin:0 0 10px;}}
.sec-title{{font-size:11px;font-weight:800;color:var(--b900);text-transform:uppercase;
  letter-spacing:.7px;display:flex;align-items:center;gap:7px;}}
.sec-title::before{{content:'';display:inline-block;width:3px;height:14px;
  background:linear-gradient(180deg,var(--b600),var(--b400));border-radius:2px;flex-shrink:0;}}
.sec-note{{font-size:11px;color:var(--tfaint);}}

/* ── CHART GRID ── */
.cg-2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;}}
.cg-3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;}}
.cg-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;}}
.chart-card{{background:#fff;border:1px solid var(--border-s);border-radius:var(--r);
  padding:13px 14px 10px;box-shadow:var(--sh);min-width:0;}}
.chart-title{{font-size:10.5px;font-weight:700;color:var(--tmid);text-transform:uppercase;
  letter-spacing:.4px;margin-bottom:10px;display:flex;justify-content:space-between;
  align-items:flex-start;gap:8px;flex-wrap:wrap;}}
.chart-area{{width:100%;}}
.chart-area svg{{display:block;width:100%;height:auto;}}
.legend{{display:flex;gap:8px;flex-wrap:wrap;}}
.lg-i{{display:flex;align-items:center;gap:3px;font-size:10px;color:var(--tfaint);font-weight:600;}}
.lg-dot{{width:7px;height:7px;border-radius:50%;flex-shrink:0;}}
.lg-ln{{width:12px;height:2px;border-radius:2px;flex-shrink:0;}}

/* ── RATIO CARDS ── */
.ratio-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;}}
.ratio-card{{background:#fff;border:1px solid var(--border-s);border-radius:var(--r);
  padding:12px 14px;box-shadow:var(--sh);border-top:3px solid var(--rc-clr,var(--b400));}}
.ratio-lbl{{font-size:9.5px;font-weight:700;color:var(--tfaint);text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px;}}
.ratio-vals{{display:flex;gap:10px;}}
.rv-yr{{text-align:center;flex:1;}}
.rv-yr .rv{{font-size:14px;font-weight:700;color:var(--text);}}
.rv-yr .rl{{font-size:9px;color:var(--tfaint);margin-top:1px;}}

/* ── TABLE WRAPPER ── */
.tbl-wrap{{background:#fff;border:1px solid var(--border-s);border-radius:var(--r);
  overflow:hidden;box-shadow:var(--sh-lg);margin-bottom:16px;}}
.tbl-scroll{{overflow-x:auto;}}

/* ── TABLE BASE ── */
.tbl{{width:100%;border-collapse:collapse;font-size:12.5px;}}

/* Two-row thead */
.tbl thead{{position:sticky;top:0;z-index:20;}}
.tbl .th-r1 th{{
  background:var(--b900);color:rgba(255,255,255,.82);
  padding:9px 12px;font-size:10px;font-weight:700;text-transform:uppercase;
  letter-spacing:.4px;white-space:nowrap;text-align:right;
  border-right:1px solid rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.08);
}}
.tbl .th-r1 th:first-child{{text-align:left;min-width:220px;position:sticky;left:0;z-index:25;background:var(--b900);}}
.tbl .th-r2 th{{
  background:var(--b800);color:rgba(255,255,255,.55);
  padding:5px 10px;font-size:9px;font-weight:700;text-align:right;white-space:nowrap;
  border-right:1px solid rgba(255,255,255,.05);border-bottom:2px solid var(--b600);
}}

/* Year group header — clickable */
.th-yr-grp{{
  cursor:pointer;text-align:center!important;
  transition:background .15s;letter-spacing:.2px;
}}
.th-yr-grp:hover{{background:var(--b700)!important;}}
/* Quarter sub-header — clickable */
.th-q{{cursor:pointer;text-align:center!important;}}
.th-q:hover{{background:var(--b700)!important;}}
/* Month sub-header */
.th-m{{text-align:center!important;color:rgba(255,255,255,.38)!important;font-size:8.5px!important;}}
/* Annual sub-header */
.th-ann{{text-align:center!important;}}
/* Meta (YoY/CAGR) */
.th-meta,.tbl .th-r1 .th-meta{{background:var(--b800)!important;color:rgba(255,255,255,.5)!important;
  font-size:9px!important;text-align:center!important;}}

/* Expand button in header */
.col-xbtn{{
  display:inline-flex;align-items:center;justify-content:center;
  width:14px;height:14px;border-radius:3px;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
  font-size:10px;font-weight:700;cursor:pointer;color:rgba(255,255,255,.85);
  margin-right:4px;vertical-align:middle;transition:all .15s;
  line-height:1;user-select:none;flex-shrink:0;
}}
.col-xbtn.open{{background:var(--b500);border-color:var(--b400);color:#fff;}}
.th-yr-grp:hover .col-xbtn{{background:rgba(255,255,255,.22);}}
.col-xbtn.sm{{width:12px;height:12px;font-size:9px;margin-right:3px;}}

/* ── DATA ROWS ── */
.tbl td{{
  padding:7px 12px;border-bottom:1px solid var(--border-s);
  text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;
}}
.tbl td:first-child{{
  text-align:left;position:sticky;left:0;z-index:5;
  background:inherit;border-right:1px solid var(--border-s);
}}
.tbl tr.t-shdr td{{
  background:var(--b50);color:var(--b700);font-size:10px;font-weight:800;
  text-transform:uppercase;letter-spacing:.8px;padding:7px 14px;
  border-top:1px solid var(--b100);cursor:pointer;
}}
.tbl tr.t-shdr:hover td{{background:var(--b100);}}
.tbl tr.t-sub td{{background:#fff;}}
.tbl tr.t-sub:hover td{{background:var(--b50);}}
.tbl tr.t-bold td{{background:var(--surface2);font-weight:700;}}
.tbl tr.t-bold:hover td{{background:#EEF2F7;}}
.tbl tr.t-pct td{{background:#FAFBFF;font-style:italic;}}
.tbl tr.t-total td{{
  font-weight:800;font-size:13px;
  border-top:2px solid var(--border)!important;
  border-bottom:2px solid var(--border)!important;
}}
/* Row accent colours */
.tbl tr.row-rev td{{background:#FFFBEB;}}
.tbl tr.row-rev td:first-child{{border-left:4px solid #F59E0B;padding-left:10px;}}
.tbl tr.row-gp td{{background:var(--pos-bg);}}
.tbl tr.row-gp td:first-child{{border-left:4px solid #10B981;padding-left:10px;}}
.tbl tr.row-ebitda td{{background:var(--b50);}}
.tbl tr.row-ebitda td:first-child{{border-left:4px solid var(--b600);padding-left:10px;}}
.tbl tr.row-ebit td{{background:#F5F3FF;}}
.tbl tr.row-ebit td:first-child{{border-left:4px solid #7C3AED;padding-left:10px;}}
.tbl tr.row-ni td{{background:var(--pos-bg);font-size:14px;}}
.tbl tr.row-ni td:first-child{{border-left:4px solid #059669;padding-left:10px;}}

/* Label cell styles */
.lbl-il1{{padding-left:24px!important;color:var(--tmid);}}
.lbl-pct{{padding-left:22px!important;color:var(--b500)!important;font-size:11px;}}

/* Value cell styles */
.nc{{color:var(--text);}}
.nc_neg{{color:var(--neg);}}
.nc_t{{color:var(--tmid);font-size:12px;}}
.nc_dim{{color:var(--tfaint);font-style:italic;text-align:center;}}
.pct_val{{color:var(--b600);}}
.yoy_up{{color:var(--pos);font-size:11px;font-weight:700;}}
.yoy_dn{{color:var(--neg);font-size:11px;font-weight:700;}}
.cagr_up{{color:var(--b600);font-size:11px;font-weight:600;}}
.cagr_dn{{color:var(--warn);font-size:11px;font-weight:600;}}

/* Section collapse arrow */
.sec-arr{{
  display:inline-block;font-size:9px;color:var(--b500);
  margin-right:6px;transition:transform .2s;transform-origin:center;
}}

/* ── GENERATED: column show/hide ── */
{COL_CSS}

/* ── MODAL ── */
.modal-bg{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.38);z-index:500;
  align-items:center;justify-content:center;backdrop-filter:blur(3px);}}
.modal-bg.open{{display:flex;}}
.modal{{background:#fff;border-radius:12px;padding:24px 26px;max-width:500px;width:92%;
  box-shadow:0 24px 64px rgba(0,0,0,.14);max-height:88vh;overflow-y:auto;}}
.modal h2{{font-size:14px;font-weight:800;color:var(--b900);margin-bottom:12px;}}
.modal-x{{float:right;background:var(--surface2);border:1px solid var(--border);
  border-radius:5px;padding:2px 9px;cursor:pointer;font-size:12px;color:var(--tmuted);}}
.modal-x:hover{{background:var(--border);}}
.modal p{{font-size:12px;color:var(--tmuted);line-height:1.75;margin-bottom:9px;}}

/* ── FOOTER ── */
.footer{{text-align:center;padding:14px;font-size:11px;color:var(--tfaint);
  border-top:1px solid var(--border-s);background:var(--surface);margin-top:8px;}}

/* ── RESPONSIVE ── */
@media(max-width:1100px){{.kpi-strip{{grid-template-columns:repeat(3,1fr);}}}}
@media(max-width:900px){{
  .cg-2,.cg-3,.cg-4{{grid-template-columns:1fr;}}
  .ratio-grid{{grid-template-columns:1fr 1fr;}}
  .kpi-strip{{grid-template-columns:1fr 1fr;margin:0 8px;}}
}}
@media(max-width:560px){{.main{{padding:10px;}}}}
</style>
</head>
<body>

<header class="app-hdr">
  <div>
    <div class="hdr-title">Financial Dashboard &mdash; FMCG Corp</div>
    <div class="hdr-sub">FY{YEARS[0]}&ndash;FY{YEARS[-1]} &nbsp;&middot;&nbsp; USD millions &nbsp;&middot;&nbsp; Demo Data</div>
  </div>
  <div class="hdr-right">
    <span class="hdr-badge">&#x1F4C5; {TODAY}</span>
    <button class="hdr-guide" onclick="document.getElementById('modal').classList.add('open')">&#9432; Guide</button>
  </div>
</header>

<nav class="tab-nav">
  <div class="tab-nav-inner">
    <button class="tab-btn active" onclick="switchTab('pl',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M2 2h12a1 1 0 011 1v10a1 1 0 01-1 1H2a1 1 0 01-1-1V3a1 1 0 011-1zm1 2v8h10V4H3zm2 2h6v1H5V6zm0 2h4v1H5V8z"/></svg>
      P&amp;L Statement
    </button>
    <button class="tab-btn" onclick="switchTab('cf',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm-.75 9.75v.75h1.5v-.75H10v-1.5H8.75V7.5h1V6h-1V5.25h-1.5V6H6v1.5h1.25v2H6v1.5h1.25z"/></svg>
      Cash Flow
    </button>
    <button class="tab-btn" onclick="switchTab('bs',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M1 3h14v2H1V3zm0 4h6v2H1V7zm8 0h6v2H9V7zm-8 4h6v2H1v-2zm8 0h6v2H9v-2z"/></svg>
      Balance Sheet
    </button>
    <button class="tab-btn" onclick="switchTab('ov',this)">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M1 11l4-4 3 3 4-5 3 2V14H1v-3zm14-9a1 1 0 00-1-1H2a1 1 0 00-1 1v1h14V2z"/></svg>
      Overview &amp; Ratios
    </button>
  </div>
</nav>

<div class="tab-kpi-gap"></div>

<div class="main">
  <div class="kpi-row">
    <div class="kpi-strip">
      <div class="kpi-card" style="--kpi-clr:#F59E0B">
        <div class="kpi-lbl">FY{YEARS[-1]} Revenue</div>
        <div class="kpi-val">{fmt_b(rev[2])}</div>
        <div class="kpi-sub">Prior year: {fmt_b(rev[1])}</div>
        {kpi_badge(yoy(rev[1],rev[2]))}
      </div>
      <div class="kpi-card" style="--kpi-clr:#10B981">
        <div class="kpi-lbl">Gross Profit</div>
        <div class="kpi-val">{fmt_b(gp[2])}</div>
        <div class="kpi-sub">Margin: {gm[2]:.1f}%</div>
        {kpi_badge(yoy(gp[1],gp[2]))}
      </div>
      <div class="kpi-card" style="--kpi-clr:#2563EB">
        <div class="kpi-lbl">EBITDA</div>
        <div class="kpi-val">{fmt_b(ebitda[2])}</div>
        <div class="kpi-sub">Margin: {ebm[2]:.1f}%</div>
        {kpi_badge(yoy(ebitda[1],ebitda[2]))}
      </div>
      <div class="kpi-card" style="--kpi-clr:#7C3AED">
        <div class="kpi-lbl">EBIT</div>
        <div class="kpi-val">{fmt_b(ebit[2])}</div>
        <div class="kpi-sub">Margin: {eim[2]:.1f}%</div>
        {kpi_badge(yoy(ebit[1],ebit[2]))}
      </div>
      <div class="kpi-card" style="--kpi-clr:#059669">
        <div class="kpi-lbl">Net Income</div>
        <div class="kpi-val">{fmt_b(ni[2])}</div>
        <div class="kpi-sub">Net margin: {nim[2]:.1f}%</div>
        {kpi_badge(yoy(ni[1],ni[2]))}
      </div>
      <div class="kpi-card" style="--kpi-clr:#0EA5E9">
        <div class="kpi-lbl">Operating Cash Flow</div>
        <div class="kpi-val">{fmt_b(cfo[2])}</div>
        <div class="kpi-sub">FCF: {fmt_b(cfo[2] + CF_INV["Purchase of PP&E"][2])}</div>
        {kpi_badge(yoy(cfo[1],cfo[2]))}
      </div>
    </div>
  </div>

  <!-- ════════ P&L TAB ════════ -->
  <div class="tab-panel active" id="tab-pl">
    <div class="cg-2">
      <div class="chart-card">
        <div class="chart-title">Revenue vs Net Income (USD M)
          <div class="legend">
            <div class="lg-i"><div class="lg-dot" style="background:#F59E0B"></div>Revenue</div>
            <div class="lg-i"><div class="lg-dot" style="background:#059669"></div>Net Income</div>
          </div>
        </div>
        <div class="chart-area" id="c-rev-ni"></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Margin Trends (%)
          <div class="legend">
            <div class="lg-i"><div class="lg-ln" style="background:#10B981"></div>Gross</div>
            <div class="lg-i"><div class="lg-ln" style="background:#2563EB"></div>EBITDA</div>
            <div class="lg-i"><div class="lg-ln" style="background:#7C3AED"></div>EBIT</div>
            <div class="lg-i"><div class="lg-ln" style="background:#059669"></div>Net</div>
          </div>
        </div>
        <div class="chart-area" id="c-margins"></div>
      </div>
    </div>
    <div class="cg-2">
      <div class="chart-card">
        <div class="chart-title">Gross Profit &amp; EBITDA (USD M)
          <div class="legend">
            <div class="lg-i"><div class="lg-dot" style="background:#10B981"></div>GP</div>
            <div class="lg-i"><div class="lg-dot" style="background:#2563EB"></div>EBITDA</div>
          </div>
        </div>
        <div class="chart-area" id="c-gp-eb"></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">OpEx Breakdown (USD M)
          <div class="legend">
            <div class="lg-i"><div class="lg-dot" style="background:#60A5FA"></div>Sales</div>
            <div class="lg-i"><div class="lg-dot" style="background:#F59E0B"></div>Mktg</div>
            <div class="lg-i"><div class="lg-dot" style="background:#10B981"></div>R&amp;D</div>
            <div class="lg-i"><div class="lg-dot" style="background:#A78BFA"></div>G&amp;A</div>
          </div>
        </div>
        <div class="chart-area" id="c-opex"></div>
      </div>
    </div>

    <div class="sec-hdr">
      <div class="sec-title">Income Statement</div>
      <div class="sec-note">
        USD millions &nbsp;&middot;&nbsp;
        Click <b style="color:var(--b600)">+</b> on a year header to expand quarters &amp; months &nbsp;&middot;&nbsp;
        Click a section header to collapse sub-items
      </div>
    </div>
    <div class="tbl-wrap">
      <div class="tbl-scroll">
        <table class="tbl" id="pl-tbl">
          <thead>{PL_HEADER}</thead>
          <tbody>{PL_ROWS}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ════════ CASH FLOW TAB ════════ -->
  <div class="tab-panel" id="tab-cf">
    <div class="cg-3">
      <div class="chart-card">
        <div class="chart-title">Operating Cash Flow (USD M)</div>
        <div class="chart-area" id="c-cfo"></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">CF Components (USD M)
          <div class="legend">
            <div class="lg-i"><div class="lg-dot" style="background:#2563EB"></div>CFO</div>
            <div class="lg-i"><div class="lg-dot" style="background:#DC2626"></div>CFI</div>
            <div class="lg-i"><div class="lg-dot" style="background:#F59E0B"></div>CFF</div>
          </div>
        </div>
        <div class="chart-area" id="c-cf-sum"></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Net Change in Cash (USD M)</div>
        <div class="chart-area" id="c-ncf"></div>
      </div>
    </div>
    <div class="sec-hdr">
      <div class="sec-title">Cash Flow Statement</div>
      <div class="sec-note">USD millions &nbsp;&middot;&nbsp; Indirect method &nbsp;&middot;&nbsp; Click section header to collapse</div>
    </div>
    <div class="tbl-wrap">
      <div class="tbl-scroll">
        <table class="tbl">
          <thead><tr class="th-r1">
            <th style="text-align:left;min-width:240px">Line Item</th>
            <th>FY{YEARS[0]}</th><th>FY{YEARS[1]}</th><th>FY{YEARS[2]}</th>
            <th class="th-meta">YoY %</th>
          </tr></thead>
          <tbody>{CF_ROWS}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ════════ BALANCE SHEET TAB ════════ -->
  <div class="tab-panel" id="tab-bs">
    <div class="cg-2">
      <div class="chart-card">
        <div class="chart-title">Assets vs Liabilities &amp; Equity (USD M)
          <div class="legend">
            <div class="lg-i"><div class="lg-dot" style="background:#2563EB"></div>Assets</div>
            <div class="lg-i"><div class="lg-dot" style="background:#DC2626"></div>Liabilities</div>
            <div class="lg-i"><div class="lg-dot" style="background:#10B981"></div>Equity</div>
          </div>
        </div>
        <div class="chart-area" id="c-bs-bar"></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Asset Composition (USD M)
          <div class="legend">
            <div class="lg-i"><div class="lg-dot" style="background:#60A5FA"></div>Current</div>
            <div class="lg-i"><div class="lg-dot" style="background:#1D4ED8"></div>Non-Current</div>
          </div>
        </div>
        <div class="chart-area" id="c-bs-assets"></div>
      </div>
    </div>
    <div class="sec-hdr">
      <div class="sec-title">Balance Sheet</div>
      <div class="sec-note">USD millions &nbsp;&middot;&nbsp; Click section header to collapse</div>
    </div>
    <div class="tbl-wrap">
      <div class="tbl-scroll">
        <table class="tbl">
          <thead><tr class="th-r1">
            <th style="text-align:left;min-width:260px">Line Item</th>
            <th>FY{YEARS[0]}</th><th>FY{YEARS[1]}</th><th>FY{YEARS[2]}</th>
            <th class="th-meta">YoY %</th>
          </tr></thead>
          <tbody>{BS_ROWS}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ════════ OVERVIEW TAB ════════ -->
  <div class="tab-panel" id="tab-ov">
    <div class="sec-hdr" style="margin-bottom:10px">
      <div class="sec-title">Key Financial Ratios</div>
      <div class="sec-note">FY{YEARS[0]} &rarr; FY{YEARS[-1]}</div>
    </div>
    <div class="ratio-grid">
      <div class="ratio-card" style="--rc-clr:#10B981">
        <div class="ratio-lbl">Gross Margin</div>
        <div class="ratio-vals">{ratio_vals_html(gm, lambda v: f"{v:.1f}%")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#2563EB">
        <div class="ratio-lbl">EBITDA Margin</div>
        <div class="ratio-vals">{ratio_vals_html(ebm, lambda v: f"{v:.1f}%")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#7C3AED">
        <div class="ratio-lbl">EBIT Margin</div>
        <div class="ratio-vals">{ratio_vals_html(eim, lambda v: f"{v:.1f}%")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#059669">
        <div class="ratio-lbl">Net Margin</div>
        <div class="ratio-vals">{ratio_vals_html(nim, lambda v: f"{v:.1f}%")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#0EA5E9">
        <div class="ratio-lbl">Current Ratio</div>
        <div class="ratio-vals">{ratio_vals_html(curr_rat, lambda v: f"{v:.2f}x")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#F59E0B">
        <div class="ratio-lbl">Debt / Equity</div>
        <div class="ratio-vals">{ratio_vals_html(debt_eq, lambda v: f"{v:.2f}x")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#8B5CF6">
        <div class="ratio-lbl">Return on Equity (ROE)</div>
        <div class="ratio-vals">{ratio_vals_html(roe, lambda v: f"{v:.1f}%")}</div>
      </div>
      <div class="ratio-card" style="--rc-clr:#DC2626">
        <div class="ratio-lbl">Return on Assets (ROA)</div>
        <div class="ratio-vals">{ratio_vals_html(roa, lambda v: f"{v:.1f}%")}</div>
      </div>
    </div>
    <div class="cg-2">
      <div class="chart-card">
        <div class="chart-title">Revenue Bridge FY{YEARS[0]} → FY{YEARS[-1]} (USD M)</div>
        <div class="chart-area" id="c-waterfall"></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Profitability Margins (%)
          <div class="legend">
            <div class="lg-i"><div class="lg-ln" style="background:#2563EB"></div>EBITDA</div>
            <div class="lg-i"><div class="lg-ln" style="background:#10B981"></div>Gross</div>
            <div class="lg-i"><div class="lg-ln" style="background:#059669"></div>Net</div>
          </div>
        </div>
        <div class="chart-area" id="c-ov-margins"></div>
      </div>
    </div>
    <div class="sec-hdr" style="margin-top:4px">
      <div class="sec-title">FY{YEARS[-1]} Budget vs Actual</div>
    </div>
    <div class="cg-4">
      <div class="ratio-card" style="--rc-clr:#F59E0B">
        <div class="ratio-lbl">Revenue</div>
        <div style="font-size:16px;font-weight:800;margin-top:6px">{fmt_b(rev[2])}</div>
        <div style="font-size:10.5px;color:var(--tfaint);margin-top:3px">Budget: {fmt_b(bud_rev)}</div>
        {bud_badge(rev[2],bud_rev)}
      </div>
      <div class="ratio-card" style="--rc-clr:#10B981">
        <div class="ratio-lbl">Gross Profit</div>
        <div style="font-size:16px;font-weight:800;margin-top:6px">{fmt_b(gp[2])}</div>
        <div style="font-size:10.5px;color:var(--tfaint);margin-top:3px">Budget: {fmt_b(bud_gp)}</div>
        {bud_badge(gp[2],bud_gp)}
      </div>
      <div class="ratio-card" style="--rc-clr:#2563EB">
        <div class="ratio-lbl">EBITDA</div>
        <div style="font-size:16px;font-weight:800;margin-top:6px">{fmt_b(ebitda[2])}</div>
        <div style="font-size:10.5px;color:var(--tfaint);margin-top:3px">Budget: {fmt_b(bud_ebitda)}</div>
        {bud_badge(ebitda[2],bud_ebitda)}
      </div>
      <div class="ratio-card" style="--rc-clr:#059669">
        <div class="ratio-lbl">Net Income</div>
        <div style="font-size:16px;font-weight:800;margin-top:6px">{fmt_b(ni[2])}</div>
        <div style="font-size:10.5px;color:var(--tfaint);margin-top:3px">Budget: {fmt_b(bud_ni)}</div>
        {bud_badge(ni[2],bud_ni)}
      </div>
    </div>
  </div>
</div>

<footer class="footer">
  Developed by <strong>Musab Shaikh</strong> &nbsp;&middot;&nbsp; FMCG | Commercial Intelligence &nbsp;&middot;&nbsp; {_dt.now().year}
</footer>

<div class="modal-bg" id="modal" onclick="if(event.target===this)this.classList.remove('open')">
  <div class="modal">
    <button class="modal-x" onclick="document.getElementById('modal').classList.remove('open')">&#10005;</button>
    <h2>&#9432; Dashboard Guide</h2>
    <p><strong>P&amp;L Column Expansion:</strong> Click the <b style="color:#2563EB">+</b> button inside any year header (FY2022 / FY2023 / FY2024) to expand that year into Q1–Q4 quarterly columns. Click the <b style="color:#2563EB">+</b> on a quarter header to further expand into monthly columns (Jan–Dec). Click again (−) to collapse.</p>
    <p><strong>P&amp;L Row Collapse:</strong> Click any blue section header (e.g. <em>Revenue</em>, <em>Cost of Goods Sold</em>) to collapse its sub-items. Click again to expand. This works on all three statements.</p>
    <p><strong>Cash Flow:</strong> Indirect method — Operating, Investing, Financing. Parentheses = cash outflows.</p>
    <p><strong>Balance Sheet:</strong> Assets = Liabilities + Equity across all three years with YoY movement.</p>
    <p style="color:#94A3B8;font-size:11px">All figures are simulated demo data. Monthly seasonality uses FMCG weights that sum exactly to annual totals.</p>
  </div>
</div>

<script>
const D = {CHART_DATA};
const M = 1000000;

{JS_TABS}
{JS_TABLES}

// ── SVG CHART ENGINE ─────────────────────────────────────────────────────
var HC = 155, PAD = {{l:44,r:12,t:28,b:26}};

function niceMax(arr) {{
  var mx = Math.max.apply(null, arr.map(Math.abs));
  if (!mx) return 1;
  var mag = Math.pow(10, Math.floor(Math.log10(mx)));
  return Math.ceil(mx/mag)*mag*1.12;
}}
function gridLines(pL,pT,iW,iH,mn,mx,fmt) {{
  var out='', steps=[0,.25,.5,.75,1];
  steps.forEach(function(f) {{
    var v=mn+f*(mx-mn), y=(pT+iH*(1-f)).toFixed(1);
    out+='<line x1="'+pL+'" y1="'+y+'" x2="'+(pL+iW)+'" y2="'+y+'" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="'+(f?'4,3':'0')+'"/>';
    out+='<text x="'+(pL-4)+'" y="'+y+'" text-anchor="end" dominant-baseline="middle" fill="#94A3B8" font-size="9" font-family="system-ui">'+fmt(v)+'</text>';
  }});
  return out;
}}
function xLbls(pL,pT,iW,iH,n) {{
  return D.years.map(function(y,i) {{
    var cx=(pL+iW/n*(i+.5)).toFixed(1);
    return '<text x="'+cx+'" y="'+(pT+iH+16)+'" text-anchor="middle" fill="#64748B" font-size="9.5" font-family="system-ui">'+y+'</text>';
  }}).join('');
}}
function barChart(id,series) {{
  var el=document.getElementById(id); if(!el) return;
  var W=el.offsetWidth||360, pL=PAD.l,pR=PAD.r,pT=PAD.t,pB=PAD.b;
  var iW=W-pL-pR, iH=HC-pT-pB, n=D.years.length;
  var all=series.reduce(function(a,s){{return a.concat(s.vals);}},[]); 
  var mx=niceMax(all);
  var mn=Math.min.apply(null,all.map(function(v){{return Math.min(v,0);}}));
  var rng=mx-mn; var baseY=pT+iH*(1-(0-mn)/rng);
  var fmt=function(v){{return (v/M).toFixed(1);}};
  var gap=iW/n, tbw=Math.floor(gap*.68), bw=Math.max(4,Math.floor(tbw/series.length)-2);
  var out=gridLines(pL,pT,iW,iH,mn,mx,fmt)+xLbls(pL,pT,iW,iH,n);
  series.forEach(function(s,si) {{
    s.vals.forEach(function(v,i) {{
      var bh=Math.max(Math.abs(v)/rng*iH,2);
      var bx=(pL+gap*i+(gap-tbw)/2+si*(bw+2)).toFixed(1);
      var by=(v>=0?baseY-bh:baseY).toFixed(1);
      out+='<rect x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh.toFixed(1)+'" fill="'+s.col+'" rx="2.5" opacity=".88"><title>'+s.label+' '+D.years[i]+': '+fmt(v)+'</title></rect>';
      if(series.length<=2) {{
        var lY=(v>=0?parseFloat(by)-5:parseFloat(by)+bh+11).toFixed(1);
        out+='<text x="'+(parseFloat(bx)+bw/2).toFixed(1)+'" y="'+lY+'" text-anchor="middle" fill="'+s.col+'" font-size="8.5" font-weight="600" font-family="system-ui" opacity=".88">'+fmt(v)+'</text>';
      }}
    }});
  }});
  el.innerHTML='<svg viewBox="0 0 '+W+' '+HC+'" width="'+W+'" height="'+HC+'">'+out+'</svg>';
}}
function lineChart(id,series,pct) {{
  var el=document.getElementById(id); if(!el) return;
  var W=el.offsetWidth||360, pL=38,pR=12,pT=28,pB=26;
  var iW=W-pL-pR, iH=HC-pT-pB, n=D.years.length;
  var all=series.reduce(function(a,s){{return a.concat(s.vals);}},[]); 
  var mn=Math.min.apply(null,all)*.88, mx=Math.max.apply(null,all)*1.1||1;
  var fmt=pct?function(v){{return v.toFixed(1)+'%';}}:function(v){{return (v/M).toFixed(1);}};
  var xp=function(i){{return pL+(n>1?iW/(n-1)*i:iW/2);}};
  var yp=function(v){{return pT+iH-(v-mn)/(mx-mn)*iH;}};
  var out=gridLines(pL,pT,iW,iH,mn,mx,fmt)+xLbls(pL,pT,iW,iH,n);
  series.forEach(function(s) {{
    var pts=s.vals.map(function(v,i){{return {{x:xp(i),y:yp(v)}};}}); 
    var d=pts.map(function(p,i){{return (i?'L':'M')+p.x.toFixed(1)+','+p.y.toFixed(1);}}).join(' ');
    out+='<path d="'+d+'" fill="none" stroke="'+s.col+'" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>';
    pts.forEach(function(p,i) {{
      out+='<circle cx="'+p.x.toFixed(1)+'" cy="'+p.y.toFixed(1)+'" r="4" fill="'+s.col+'" stroke="#fff" stroke-width="2"><title>'+s.label+' '+D.years[i]+': '+fmt(s.vals[i])+'</title></circle>';
      out+='<text x="'+p.x.toFixed(1)+'" y="'+(p.y-9).toFixed(1)+'" text-anchor="middle" fill="'+s.col+'" font-size="8.5" font-weight="600" font-family="system-ui" opacity=".9">'+fmt(s.vals[i])+'</text>';
    }});
  }});
  el.innerHTML='<svg viewBox="0 0 '+W+' '+HC+'" width="'+W+'" height="'+HC+'">'+out+'</svg>';
}}
function stackedBar(id,series) {{
  var el=document.getElementById(id); if(!el) return;
  var W=el.offsetWidth||360, pL=PAD.l,pR=PAD.r,pT=PAD.t,pB=PAD.b;
  var iW=W-pL-pR, iH=HC-pT-pB, n=D.years.length;
  var tots=D.years.map(function(_,i){{return series.reduce(function(s,r){{return s+Math.abs(r.vals[i]);}},0);}});
  var mx=Math.max.apply(null,tots)*1.1||1, bw=Math.floor(iW/n*.52);
  var fmt=function(v){{return (v/M).toFixed(1);}};
  var out=gridLines(pL,pT,iW,iH,0,mx,fmt)+xLbls(pL,pT,iW,iH,n);
  D.years.forEach(function(y,i) {{
    var cx=pL+iW/n*(i+.5), base=pT+iH;
    series.forEach(function(s) {{
      var bh=Math.max(Math.abs(s.vals[i])/mx*iH,1); base-=bh;
      out+='<rect x="'+(cx-bw/2).toFixed(1)+'" y="'+base.toFixed(1)+'" width="'+bw+'" height="'+bh.toFixed(1)+'" fill="'+s.col+'" rx="1.5" opacity=".88"><title>'+s.label+' '+y+': '+fmt(s.vals[i])+'</title></rect>';
    }});
  }});
  el.innerHTML='<svg viewBox="0 0 '+W+' '+HC+'" width="'+W+'" height="'+HC+'">'+out+'</svg>';
}}
function waterfallChart(id) {{
  var el=document.getElementById(id); if(!el) return;
  var W=el.offsetWidth||360, pH=HC+20, pL=44,pR=12,pT=28,pB=40;
  var iW=W-pL-pR, iH=pH-pT-pB;
  var items=[
    {{l:'FY22',v:D.rev[0],t:'abs'}},
    {{l:'\u039423',v:D.rev[1]-D.rev[0],t:'d'}},
    {{l:'\u039424',v:D.rev[2]-D.rev[1],t:'d'}},
    {{l:'FY24',v:D.rev[2],t:'abs'}}
  ];
  var mx=Math.max.apply(null,items.map(function(it){{return Math.abs(it.v);}}))*1.15||1;
  var fmt=function(v){{return (v/M).toFixed(1);}};
  var gap=iW/items.length, bw=Math.floor(gap*.56);
  var out=gridLines(pL,pT,iW,iH,0,mx,fmt);
  var run=0;
  items.forEach(function(it,i) {{
    var cx=pL+gap*i+gap/2;
    var col=it.t==='abs'?'#2563EB':(it.v>=0?'#059669':'#DC2626');
    var bh,by;
    if(it.t==='abs'){{bh=it.v/mx*iH; by=pT+iH-bh; run=it.v;}}
    else{{bh=Math.abs(it.v)/mx*iH; by=it.v>=0?pT+iH-run/mx*iH-bh:pT+iH-run/mx*iH; run+=it.v;}}
    out+='<rect x="'+(cx-bw/2).toFixed(1)+'" y="'+by.toFixed(1)+'" width="'+bw+'" height="'+Math.max(bh,2).toFixed(1)+'" fill="'+col+'" rx="2.5" opacity=".88"><title>'+it.l+': '+fmt(it.v)+'</title></rect>';
    out+='<text x="'+cx.toFixed(1)+'" y="'+(by-5).toFixed(1)+'" text-anchor="middle" fill="'+col+'" font-size="9" font-weight="700" font-family="system-ui">'+fmt(it.v)+'</text>';
    out+='<text x="'+cx.toFixed(1)+'" y="'+(pT+iH+20)+'" text-anchor="middle" fill="#64748B" font-size="9.5" font-family="system-ui">'+it.l+'</text>';
  }});
  el.innerHTML='<svg viewBox="0 0 '+W+' '+pH+'" width="'+W+'" height="'+pH+'">'+out+'</svg>';
}}

function drawAllCharts() {{
  barChart('c-rev-ni',[{{vals:D.rev,col:'#F59E0B',label:'Revenue'}},{{vals:D.ni,col:'#059669',label:'Net Income'}}]);
  lineChart('c-margins',[{{vals:D.gm,col:'#10B981',label:'Gross%'}},{{vals:D.ebm,col:'#2563EB',label:'EBITDA%'}},{{vals:D.eim,col:'#7C3AED',label:'EBIT%'}},{{vals:D.nim,col:'#059669',label:'Net%'}}],true);
  barChart('c-gp-eb',[{{vals:D.gp,col:'#10B981',label:'GP'}},{{vals:D.ebitda,col:'#2563EB',label:'EBITDA'}}]);
  stackedBar('c-opex',[
    {{vals:D.opex_items['Sales & Distribution'],col:'#60A5FA',label:'Sales'}},
    {{vals:D.opex_items['Marketing'],col:'#F59E0B',label:'Marketing'}},
    {{vals:D.opex_items['Research & Development'],col:'#10B981',label:'R&D'}},
    {{vals:D.opex_items['General & Administrative'],col:'#A78BFA',label:'G&A'}}
  ]);
  barChart('c-cfo',[{{vals:D.cfo,col:'#2563EB',label:'CFO'}}]);
  barChart('c-cf-sum',[{{vals:D.cfo,col:'#2563EB',label:'CFO'}},{{vals:D.cfi,col:'#DC2626',label:'CFI'}},{{vals:D.cff,col:'#F59E0B',label:'CFF'}}]);
  barChart('c-ncf',[{{vals:D.ncf,col:'#059669',label:'Net Cash'}}]);
  barChart('c-bs-bar',[{{vals:D.tot_ast,col:'#2563EB',label:'Assets'}},{{vals:D.tot_lia,col:'#DC2626',label:'Liabilities'}},{{vals:D.tot_eq,col:'#10B981',label:'Equity'}}]);
  stackedBar('c-bs-assets',[{{vals:D.cur_ast,col:'#60A5FA',label:'Current'}},{{vals:D.nc_ast,col:'#1D4ED8',label:'Non-Current'}}]);
  waterfallChart('c-waterfall');
  lineChart('c-ov-margins',[{{vals:D.ebm,col:'#2563EB',label:'EBITDA%'}},{{vals:D.gm,col:'#10B981',label:'Gross%'}},{{vals:D.nim,col:'#059669',label:'Net%'}}],true);
}}

window.addEventListener('resize', drawAllCharts);
drawAllCharts();
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Financial_Dashboard.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Done!  {os.path.getsize(out)//1024} KB  \u2192  {out}")
