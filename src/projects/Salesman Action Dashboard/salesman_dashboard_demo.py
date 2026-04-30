"""
Salesman Action Dashboard — Demo
Generates a fully standalone HTML dashboard with dummy data for client showcasing.
No real data is used. Same UI as the production dashboard.
"""

import os, json, random
from datetime import datetime as _dt

random.seed(42)
TODAY_DATE = _dt.now().strftime("%d %B %Y")

# ── CONFIG ──────────────────────────────────────────────────
LOYALTY_THRESHOLD = 4

# ── DUMMY META ─────────────────────────────────────────────
MONTHS_LIST = [
    "November 2025", "December 2025", "January 2026",
    "February 2026", "March 2026", "April 2026",
]
REGIONS_LIST    = ["Central Region", "Western Region", "Eastern Region"]
CHANNELS_LIST   = ["Modern Trade", "Traditional Trade", "Food Service"]
SUB_CHANNELS_LIST = ["Hypermarkets", "Supermarkets", "Convenience", "Restaurants", "Catering"]
KEY_CATS = [
    "Bottled Water", "Carbonated Drinks", "Juices & Nectars", "Dairy Drinks", "Energy Drinks",
    "Biscuits & Cookies", "Snack Bars", "Instant Noodles", "Condiments & Sauces", "Breakfast Cereals", "Confectionery",
]

# ── DUMMY SALESMEN ─────────────────────────────────────────
DUMMY_SALESMEN = [
    {"name": "Khalid Al-Mansoor",   "no": "SM-101", "region": "Central Region"},
    {"name": "Omar Al-Farsi",        "no": "SM-102", "region": "Western Region"},
    {"name": "Ahmed Al-Rashid",      "no": "SM-103", "region": "Eastern Region"},
    {"name": "Faisal Al-Otaibi",     "no": "SM-104", "region": "Central Region"},
    {"name": "Mohammed Al-Zahrani",  "no": "SM-105", "region": "Western Region"},
    {"name": "Tariq Al-Harbi",       "no": "SM-106", "region": "Eastern Region"},
]

# ── DUMMY CUSTOMERS ────────────────────────────────────────
_CUST_NAMES = [
    "Al-Noor Hypermarket", "Golden Star Restaurant", "City Fresh Supermarket",
    "Royal Hotel Catering", "Al-Jazeera Convenience", "Sunrise Cafeteria",
    "Al-Faisaliah Market", "Green Valley Grocery", "Al-Riyadh Restaurant",
    "Crown Bakery", "Al-Safa Hypermarket", "Desert Spice Kitchen",
    "Landmark Superstore", "Al-Hamra Cafeteria", "Sea Breeze Restaurant",
    "Western Gate Market", "Al-Khaleej Store", "Hilal Food Center",
    "Crescent Grocery", "Blue Sky Catering", "Al-Watan Market",
    "Silver Spoon Restaurant", "Al-Manar Supermarket", "Horizon Food Service",
    "Al-Rawabi Store", "Al-Masah Market", "Golden Palace Restaurant",
    "First Class Grocers", "Al-Tamimi Hypermarket", "Oasis Restaurant",
    "Eastern Star Market", "Capital City Catering", "Bright Light Store",
    "Al-Murjan Market", "Four Seasons Catering", "Al-Salam Grocery",
    "Continental Restaurant", "Fresh & Clean Store", "Al-Andalus Catering",
    "Summit Restaurant", "Al-Jawhara Grocery", "Coral Reef Catering",
    "Northern Star Market", "Al-Qassim Supermarket", "Al-Riyad Mart",
    "Eastern Breeze Market", "Pacific Rim Catering", "Al-Bahrain Store",
    "Horizon Superstore", "Premier Food Service",
]

# ── DUMMY SKUS ─────────────────────────────────────────────
_SKU_BY_CAT = {
    "Bottled Water":      [("P1001", "Still Water 500ml 12-Pack"),        ("P1002", "Sparkling Water 330ml 24-Pack")],
    "Carbonated Drinks":  [("P1003", "Cola Classic 355ml 24-Pack"),        ("P1004", "Orange Fizz 355ml 24-Pack"),     ("P1005", "Lemon Soda 250ml 24-Pack")],
    "Juices & Nectars":   [("P1006", "Orange Juice 1L 12-Pack"),           ("P1007", "Mixed Fruit Nectar 250ml 24-Pack")],
    "Dairy Drinks":       [("P1008", "Full Cream Milk 1L 12-Pack"),        ("P1009", "Strawberry Flavoured Milk 200ml 24-Pack")],
    "Energy Drinks":      [("P1010", "Energy Boost Original 250ml 24-Pack"),("P1011", "Sugar-Free Energy 250ml 24-Pack")],
    "Biscuits & Cookies": [("P1012", "Butter Cookies 200g"),               ("P1013", "Chocolate Digestive 300g"),       ("P1014", "Cream-Filled Wafers 150g")],
    "Snack Bars":         [("P1015", "Oat & Honey Bar 6-Pack"),            ("P1016", "Chocolate Nut Bar 6-Pack")],
    "Instant Noodles":    [("P1017", "Chicken Flavour Noodles 80g 24-Pack"),("P1018", "Beef Flavour Noodles 80g 24-Pack")],
    "Condiments & Sauces":[("P1019", "Tomato Ketchup 500ml"),              ("P1020", "Chilli Sauce 250ml"),            ("P1021", "Mayonnaise 400g")],
    "Breakfast Cereals":  [("P1022", "Corn Flakes 500g"),                  ("P1023", "Honey Loops 375g")],
    "Confectionery":      [("P1024", "Milk Chocolate Bar 100g"),           ("P1025", "Assorted Toffees 250g")],
}
SKU_CATALOG = [
    {"code": code, "name": name, "category": cat}
    for cat, items in _SKU_BY_CAT.items()
    for code, name in items
]
sku_map = {s["code"]: s["name"] for s in SKU_CATALOG}
sku_family2_map = {s["code"]: s["category"] for s in SKU_CATALOG}

# ── ASSIGN CUSTOMERS TO SALESMEN ───────────────────────────
_cust_pool = list(enumerate(_CUST_NAMES, start=1))
random.shuffle(_cust_pool)
_pool_idx = 0

SM_CUSTS = {}
for sm in DUMMY_SALESMEN:
    n = random.randint(7, 11)
    custs = []
    for _ in range(n):
        i, cname = _cust_pool[_pool_idx % len(_cust_pool)]
        _pool_idx += 1
        n_skus = random.randint(3, 7)
        assigned_skus = random.sample(SKU_CATALOG, min(n_skus, len(SKU_CATALOG)))
        custs.append({
            "id":             f"C{1000 + i}",
            "name":           cname,
            "channel":        random.choice(CHANNELS_LIST),
            "sub_channel":    random.choice(SUB_CHANNELS_LIST),
            "months_active":  random.randint(1, 8),
            "skus":           assigned_skus,
        })
    SM_CUSTS[sm["name"]] = custs

# ── BUILD DATA & KEY_DATA RECORDS ─────────────────────────
records      = []
key_records  = []
actuals_hist = {}

for sm in DUMMY_SALESMEN:
    sm_name = sm["name"]
    sm_no   = sm["no"]
    region  = sm["region"]

    for cust in SM_CUSTS[sm_name]:
        cid           = cust["id"]
        cname         = cust["name"]
        channel       = cust["channel"]
        sub_channel   = cust["sub_channel"]
        months_active = cust["months_active"]
        category      = "hold" if months_active >= LOYALTY_THRESHOLD else "battle"
        cust_skus     = cust["skus"]
        sku_codes     = [s["code"] for s in cust_skus]

        actuals_hist[cid] = {}

        for month in MONTHS_LIST:
            if random.random() < 0.12:   # ~12% chance customer skips a month
                continue

            exp_rev   = round(random.uniform(8_000, 130_000))
            comp_pct  = random.uniform(0.18, 1.08)
            act_rev   = round(exp_rev * comp_pct)
            pred_qty  = round(random.uniform(50, 900), 1)
            act_qty   = round(pred_qty * comp_pct, 1)
            pred_ton  = round(pred_qty * 0.02, 2)
            act_ton   = round(act_qty  * 0.02, 2)
            avg_conf  = round(random.uniform(0.55, 0.93), 3)

            records.append({
                "Month":         month,
                "Salesman":      sm_name,
                "Salesman_No":   sm_no,
                "Region":        region,
                "Customer":      cid,
                "Customer_Name": cname,
                "n_skus":        len(sku_codes),
                "exp_rev":       exp_rev,
                "act_rev":       act_rev,
                "pred_qty":      pred_qty,
                "act_qty":       act_qty,
                "pred_ton":      pred_ton,
                "act_ton":       act_ton,
                "avg_conf":      avg_conf,
                "months_active": months_active,
                "category":      category,
                "channel":       channel,
                "sub_channel":   sub_channel,
                "sku_codes":     sku_codes,
            })
            actuals_hist[cid][month] = [act_qty, act_rev, act_ton]

            # KEY_DATA: one record per (Customer, SKU_Category, Month)
            cat_groups: dict = {}
            for sku in cust_skus:
                cat_groups.setdefault(sku["category"], []).append(sku["code"])

            for cat, codes in cat_groups.items():
                w = len(codes) / len(sku_codes)
                cat_exp  = round(exp_rev  * w * random.uniform(0.85, 1.15))
                cat_act  = round(cat_exp  * comp_pct)
                cat_pqty = round(pred_qty * w * random.uniform(0.85, 1.15), 1)
                cat_aqty = round(cat_pqty * comp_pct, 1)
                key_records.append({
                    "Month":         month,
                    "Salesman":      sm_name,
                    "Salesman_No":   sm_no,
                    "Region":        region,
                    "Customer":      cid,
                    "Customer_Name": cname,
                    "SKU_Category":  cat,
                    "n_skus":        len(codes),
                    "exp_rev":       cat_exp,
                    "act_rev":       cat_act,
                    "pred_qty":      cat_pqty,
                    "act_qty":       cat_aqty,
                    "pred_ton":      round(cat_pqty * 0.02, 2),
                    "act_ton":       round(cat_aqty  * 0.02, 2),
                    "avg_conf":      avg_conf,
                    "months_active": months_active,
                    "category":      category,
                    "channel":       channel,
                    "sub_channel":   sub_channel,
                    "sku_codes":     codes,
                })

data_json        = json.dumps(records)
key_data_json    = json.dumps(key_records)
actuals_hist_json = json.dumps(actuals_hist)

# ── SKU CONTRIB + LAST ORDER MAPS ──────────────────────────
sku_contrib_map     = {}
last_order_month_map = {}

for sm in DUMMY_SALESMEN:
    for cust in SM_CUSTS[sm["name"]]:
        cid       = cust["id"]
        cust_skus = cust["skus"]
        weights   = [random.uniform(0.5, 3.0) for _ in cust_skus]
        total_w   = sum(weights)
        for i, sku in enumerate(cust_skus):
            key = f"{cid}||{sku['code']}"
            sku_contrib_map[key]      = round(weights[i] / total_w * 100, 2)
            last_order_month_map[key] = random.choice(MONTHS_LIST[-3:])

sku_map_json            = json.dumps(sku_map)
sku_family2_map_json    = json.dumps(sku_family2_map)
sku_contrib_map_json    = json.dumps(sku_contrib_map)
last_order_month_map_json = json.dumps(last_order_month_map)

# ── FILTER LISTS ───────────────────────────────────────────
sorted_months = MONTHS_LIST
regions       = REGIONS_LIST
salesmen      = sorted(sm["name"] for sm in DUMMY_SALESMEN)
channels      = CHANNELS_LIST
sub_channels  = SUB_CHANNELS_LIST

# ── HTML ────────────────────────────────────────────────────
print("Generating Salesman Action Dashboard (Demo) …")

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Salesman Action Dashboard</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#FAFAFA;--surface:#FFF;--border:#F0E0E0;
  --red-900:#7F1D1D;--red-700:#B91C1C;--red-600:#DC2626;
  --red-500:#EF4444;--red-400:#F87171;--red-100:#FEE2E2;--red-50:#FEF2F2;
  --slate-900:#0F172A;--slate-700:#334155;--slate-500:#64748B;--slate-400:#94A3B8;
  --slate-300:#CBD5E1;--slate-200:#E2E8F0;--slate-100:#F1F5F9;
  --green-600:#16A34A;--green-100:#DCFCE7;
  --amber-600:#D97706;--amber-100:#FEF3C7;
  --radius:10px;--shadow:0 1px 3px rgba(0,0,0,.06);
}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--slate-700);line-height:1.5;}}

/* ── HEADER ─────────────────────────────────── */
.header{{background:linear-gradient(135deg,var(--red-900),var(--red-700));color:#fff;padding:24px 32px;}}
.header h1{{font-size:22px;font-weight:700;letter-spacing:-.3px;}}
.header p{{font-size:13px;opacity:.8;margin-top:4px;}}

/* ── FILTER BAR ─────────────────────────────── */
.filters{{display:flex;flex-wrap:wrap;align-items:stretch;background:var(--surface);border-bottom:2px solid var(--border)}}
.f-section{{display:flex;gap:10px;padding:12px 16px;align-items:flex-end;flex-wrap:wrap}}
.f-section-actions{{display:flex;gap:8px;padding:12px 16px;align-items:flex-end;margin-left:auto}}
.f-divider{{width:1px;background:var(--border);align-self:stretch;margin:8px 0;flex-shrink:0}}
.f-group{{display:flex;flex-direction:column;gap:4px}}
.f-group label{{font-size:10px;font-weight:700;color:var(--slate-400);text-transform:uppercase;letter-spacing:.7px}}
.f-group select{{height:34px;padding:0 26px 0 10px;border:1px solid var(--slate-300);border-radius:6px;font-size:13px;color:var(--slate-700);background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2394A3B8'/%3E%3C/svg%3E") no-repeat right 9px center;-webkit-appearance:none;appearance:none;cursor:pointer;min-width:130px}}
.f-group select:focus{{outline:none;box-shadow:0 0 0 3px rgba(185,28,28,.15);border-color:var(--red-500)}}
/* action buttons */
.f-btn{{height:34px;padding:0 14px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid;white-space:nowrap;display:inline-flex;align-items:center;gap:5px}}
.f-btn-reset{{background:var(--slate-100);color:var(--slate-600);border-color:var(--slate-300)}}
.f-btn-reset:hover{{background:var(--slate-200)}}
.f-btn-export{{background:var(--red-700);color:#fff;border-color:var(--red-700)}}
.f-btn-export:hover{{background:var(--red-900)}}
/* salesman search-select */
.ss-wrap{{position:relative;min-width:190px}}
.ss-input{{height:34px;width:100%;padding:0 28px 0 10px;border:1px solid var(--slate-300);border-radius:6px;font-size:13px;color:var(--slate-700);background:#fff;outline:none;box-sizing:border-box}}
.ss-input:focus{{border-color:var(--red-500);box-shadow:0 0 0 3px rgba(185,28,28,.15)}}
.ss-arrow{{position:absolute;right:9px;top:50%;transform:translateY(-50%);color:var(--slate-400);pointer-events:none;font-size:10px;transition:transform .18s}}
.ss-wrap.open .ss-arrow{{transform:translateY(-50%) rotate(180deg)}}
.ss-list{{display:none;position:absolute;top:calc(100% + 3px);left:0;right:0;background:#fff;border:1px solid var(--slate-300);border-radius:6px;box-shadow:0 6px 18px rgba(0,0,0,.11);list-style:none;max-height:230px;overflow-y:auto;z-index:999}}
.ss-list.open{{display:block}}
.ss-list li{{padding:8px 12px;font-size:13px;color:var(--slate-700);cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.ss-list li:hover,.ss-list li.hi{{background:var(--red-50);color:var(--red-700)}}
.ss-list li.sel{{font-weight:700;color:var(--red-700);background:var(--red-50)}}

/* ── SEGMENTED FOCUS CONTROL ────────────────── */
.view-toggle{{display:flex;border:1px solid var(--slate-300);border-radius:7px;overflow:hidden;align-self:flex-end;background:#fff}}
.vt-btn{{padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer;border:none;border-right:1px solid var(--slate-300);background:transparent;color:var(--slate-600);transition:background .15s,color .15s;white-space:nowrap;display:flex;align-items:center;gap:6px;line-height:1}}
.vt-btn:last-child{{border-right:none}}
.vt-btn:hover{{background:var(--slate-100)}}
.vt-btn.active{{font-weight:700}}
.vt-btn.risks.active{{background:var(--red-600);color:#fff}}
.vt-btn.wins.active{{background:var(--green-600);color:#fff}}
.vt-dot{{width:7px;height:7px;border-radius:50%;flex-shrink:0;transition:background .15s}}
.vt-btn.risks .vt-dot{{background:var(--red-400)}}
.vt-btn.risks.active .vt-dot{{background:rgba(255,255,255,.6)}}
.vt-btn.wins .vt-dot{{background:#4ade80}}
.vt-btn.on-track.active{{background:#16A34A;color:#fff}}
.vt-btn.on-track.active .vt-dot{{background:rgba(255,255,255,.6)}}
.vt-btn.on-track .vt-dot{{background:#4ade80}}
.vt-btn.building{{border-right:1px solid var(--slate-300)}}
.vt-btn.building.active{{background:var(--amber-600);color:#fff}}
.vt-btn.building.active .vt-dot{{background:rgba(255,255,255,.6)}}
.vt-btn.building .vt-dot{{background:#fbbf24}}
.vt-btn.critical.active{{background:var(--red-600);color:#fff}}
.vt-btn.critical.active .vt-dot{{background:rgba(255,255,255,.6)}}
.vt-btn.critical .vt-dot{{background:var(--red-400)}}

/* ── LAYOUT ─────────────────────────────────── */
.main{{padding:24px 32px;max-width:1440px;margin:0 auto}}

/* ── SALESMAN CARD ──────────────────────────── */
.sm-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:20px;overflow:hidden;box-shadow:var(--shadow)}}
.sm-header{{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;background:var(--red-50);border-bottom:1px solid var(--border);cursor:pointer;user-select:none}}
.sm-header:hover{{background:var(--red-100)}}
.sm-name{{font-size:16px;font-weight:700;color:var(--red-900)}}
.sm-meta{{display:flex;gap:20px;font-size:12px;color:var(--slate-500)}}
.sm-meta b{{color:var(--slate-700)}}
.sm-body{{display:none;padding:0}}
.sm-card.open .sm-body{{display:block}}
.sm-arrow{{font-size:14px;color:var(--red-400);transition:transform .2s}}
.sm-card.open .sm-arrow{{transform:rotate(180deg)}}

/* ── CATEGORY SECTIONS ──────────────────────── */
.cat-tabs{{display:flex;border-bottom:1px solid var(--border)}}
.cat-tab{{flex:1;padding:12px;text-align:center;font-size:13px;font-weight:700;cursor:pointer;transition:all .15s;border-bottom:3px solid transparent;color:var(--slate-400)}}
.cat-tab:hover{{color:var(--slate-700)}}
.cat-tab.active{{color:var(--red-700);border-bottom-color:var(--red-600);background:var(--red-50)}}
.cat-tab .cat-count{{display:inline-block;background:var(--slate-200);color:var(--slate-700);border-radius:10px;padding:1px 8px;font-size:11px;margin-left:6px}}
.cat-tab.active .cat-count{{background:var(--red-600);color:#fff}}
.cat-grid{{padding:16px 20px}}

/* ── SUMMARY STRIP ──────────────────────────── */
.summary-strip{{display:flex;gap:16px;padding:0 20px 12px;flex-wrap:wrap}}
.summary-chip{{background:var(--slate-100);border-radius:8px;padding:10px 16px;flex:1;min-width:140px;text-align:center}}
.summary-chip .sv{{font-size:18px;font-weight:700;color:var(--red-700)}}
.summary-chip .sl{{font-size:11px;color:var(--slate-500);margin-top:2px}}

/* ── CUSTOMER ROW ───────────────────────────── */
.cust-wrapper{{border-bottom:1px solid var(--slate-100)}}
.cust-wrapper:last-child{{border-bottom:none}}
.cust-row{{display:grid;grid-template-columns:1fr 120px 120px 120px 1fr;gap:12px;align-items:center;padding:12px 0;cursor:pointer}}
.cust-row:hover{{background:var(--slate-100);border-radius:6px}}
.cust-info{{}}
.cust-name{{font-size:14px;font-weight:600;color:var(--slate-900)}}
.expand-arrow{{display:inline-block;font-size:10px;color:var(--slate-400);margin-right:6px;transition:transform .2s}}
.cust-wrapper.expanded .expand-arrow{{transform:rotate(90deg);color:var(--red-600)}}
.cust-id{{font-size:11px;color:var(--slate-400)}}
.cust-metric{{text-align:right}}
.cust-metric .cm-val{{font-size:14px;font-weight:700;color:var(--slate-900)}}
.cust-metric .cm-sub{{font-size:11px;color:var(--slate-400)}}
.cust-progress{{}}
.progress-row{{display:flex;align-items:center;gap:8px;margin-bottom:4px}}
.progress-row:last-child{{margin-bottom:0}}
.progress-label{{font-size:10px;color:var(--slate-500);width:30px;text-align:right;flex-shrink:0}}
.progress-bar{{flex:1;height:8px;background:var(--slate-100);border-radius:4px;overflow:hidden;position:relative}}
.progress-fill{{height:100%;border-radius:4px;transition:width .4s ease}}
.progress-pct{{font-size:10px;color:var(--slate-500);width:36px;flex-shrink:0}}

/* ── COLORS FOR PROGRESS ────────────────────── */
.fill-green{{background:var(--green-600)}}
.fill-amber{{background:var(--amber-600)}}
.fill-red{{background:var(--red-500)}}

/* ── EXPANDABLE CUSTOMER DETAIL ─────────────── */
.cust-expand{{display:none;padding:0 12px 16px;background:var(--red-50);border-top:1px dashed var(--border)}}
.cust-wrapper.expanded .cust-expand{{display:block}}
.xp-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:12px}}
.xp-section{{}}
.xp-title{{font-size:12px;font-weight:700;color:var(--red-700);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}}
.trend-badge{{display:inline-flex;align-items:center;gap:5px;border-radius:999px;padding:4px 9px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.35px}}
.trend-badge.up{{background:var(--green-100);color:var(--green-600)}}
.trend-badge.flat{{background:var(--slate-100);color:var(--slate-700)}}
.trend-badge.down{{background:var(--red-100);color:var(--red-600)}}
.chart-section{{border-top:1px solid var(--border);margin-top:12px}}
.chart-toggle{{display:flex;justify-content:space-between;align-items:center;padding:7px 12px;cursor:pointer;user-select:none;background:var(--slate-100)}}
.chart-toggle:hover{{background:var(--slate-200)}}
.chart-toggle-label{{font-size:11px;font-weight:700;color:var(--slate-700)}}
.chart-toggle-arrow{{font-size:10px;color:var(--slate-400);transition:transform .2s}}
.chart-section.open .chart-toggle-arrow{{transform:rotate(180deg)}}
.chart-body{{display:none;padding:8px 12px 10px;background:#fff}}
.chart-section.open .chart-body{{display:block}}
.xp-table{{width:100%;border-collapse:collapse;font-size:12px}}
.xp-table th{{text-align:left;padding:6px 10px;background:var(--red-100);color:var(--red-900);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.3px}}
.xp-table td{{padding:5px 10px;border-bottom:1px solid var(--border);color:var(--slate-700)}}
.xp-table tbody tr:hover{{background:rgba(255,255,255,.6)}}
.xp-table.hist td:first-child{{font-weight:500}}
.xp-table .code-col{{color:var(--slate-500);font-family:monospace;font-size:11px}}

/* ── RESPONSIVE ─────────────────────────────── */
@media(max-width:900px){{
  .cust-row{{grid-template-columns:1fr 1fr;gap:8px}}
  .xp-grid{{grid-template-columns:1fr}}
  .filters,.main{{padding-left:16px;padding-right:16px}}
  .header{{padding:16px}}
}}

/* ── EMPTY STATE ────────────────────────────── */
.empty{{text-align:center;padding:40px 20px;color:var(--slate-400);font-size:14px}}

/* ── STATS BAR ──────────────────────────────── */
.stats-bar{{background:var(--surface);border-bottom:1px solid var(--border);}}
.stats-bar-hdr{{display:flex;align-items:center;justify-content:space-between;padding:10px 32px;cursor:pointer;user-select:none;font-size:12px;font-weight:700;color:var(--slate-700);letter-spacing:.2px;border-bottom:1px solid transparent}}
.stats-bar-hdr:hover{{background:var(--slate-100)}}
.stats-bar.open .stats-bar-hdr{{border-bottom-color:var(--border)}}
.stats-bar-arrow{{font-size:10px;color:var(--slate-400);transition:transform .2s;margin-left:6px}}
.stats-bar.open .stats-bar-arrow{{transform:rotate(180deg)}}
.stats-bar-body{{display:none;padding:16px 32px;gap:16px}}
.stats-bar.open .stats-bar-body{{display:grid;grid-template-columns:1fr 1fr}}
.stats-panel{{border-radius:10px;padding:16px 20px;display:flex;flex-direction:column;gap:10px}}
.stats-panel.battle{{background:var(--red-50);border:1px solid var(--red-100)}}
.stats-panel.hold{{background:var(--green-100);border:1px solid #bbf7d0}}
.stats-panel-title{{font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px}}
.stats-panel.battle .stats-panel-title{{color:var(--red-700)}}
.stats-panel.hold .stats-panel-title{{color:var(--green-600)}}
.stats-rows{{display:flex;gap:10px;flex-wrap:wrap}}
.stats-kv{{flex:1;min-width:110px;background:#fff;border-radius:8px;padding:10px 14px;box-shadow:var(--shadow)}}
.stats-kv .sk-label{{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.4px;color:var(--slate-500);margin-bottom:3px}}
.stats-kv .sk-exp{{font-size:15px;font-weight:700;color:var(--slate-900);white-space:nowrap}}
.stats-kv .sk-act{{font-size:11px;color:var(--slate-500);margin-top:1px;white-space:nowrap}}
.stats-kv .sk-pct{{display:inline-block;font-size:10px;font-weight:700;border-radius:10px;padding:1px 7px;margin-top:4px}}
.sk-pct.g{{background:var(--green-100);color:var(--green-600)}}
.sk-pct.a{{background:var(--amber-100);color:var(--amber-600)}}
.sk-pct.r{{background:var(--red-100);color:var(--red-600)}}

/* ── INFO BUTTON & MODAL ─────────────────────── */
.info-btn{{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;border-radius:20px;padding:5px 14px;font-size:12px;cursor:pointer;white-space:nowrap}}
.info-btn:hover{{background:rgba(255,255,255,.25)}}
.modal-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:1000;align-items:center;justify-content:center}}
.modal-overlay.open{{display:flex}}
.modal{{background:#fff;border-radius:12px;padding:28px 32px;max-width:580px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.2);max-height:85vh;overflow-y:auto}}
.modal h2{{font-size:17px;font-weight:700;color:var(--red-900);margin-bottom:16px}}
.modal-section{{border:1px solid var(--border);border-radius:8px;padding:14px 16px;margin-bottom:12px}}
.modal-section h3{{font-size:13px;font-weight:700;color:var(--slate-900);margin:0 0 6px;display:flex;align-items:center;gap:6px}}
.modal-section p{{font-size:13px;color:var(--slate-500);line-height:1.7;margin:0}}
.modal-close{{float:right;background:var(--slate-100);border:none;border-radius:6px;padding:4px 12px;cursor:pointer;font-size:13px;color:var(--slate-500);cursor:pointer}}
.modal-close:hover{{background:var(--slate-200)}}
.badge-battle{{background:var(--red-100);color:var(--red-700);border-radius:4px;padding:1px 8px;font-size:11px;font-weight:700}}
.badge-hold{{background:var(--green-100);color:var(--green-600);border-radius:4px;padding:1px 8px;font-size:11px;font-weight:700}}

/* ── FOOTER ──────────────────────────────────── */
.footer{{text-align:center;padding:16px 32px;font-size:11px;color:var(--slate-400);border-top:1px solid var(--border);margin-top:8px;letter-spacing:.2px}}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
  <div>
    <h1>Salesman Action Dashboard</h1>
    <p>Customer categorisation &mdash; Battles &amp; Hold Position</p>
  </div>
  <div style="display:flex;align-items:center;gap:16px">
    <span style="font-size:12px;font-weight:600;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.3);border-radius:20px;padding:5px 14px;letter-spacing:.3px;">&#128197;&nbsp; {TODAY_DATE}</span>
    <button class="info-btn" onclick="openInfo()">&#9432; Info</button>
  </div>
</div>

<!-- FILTERS -->
<div class="filters">
  <!-- Period + Territory -->
  <div class="f-section">
    <div class="f-group"><label>Month</label><select id="fMonth"></select></div>
    <div class="f-group"><label>Area</label><select id="fRegion"></select></div>
  </div>
  <div class="f-divider"></div>
  <!-- Channel -->
  <div class="f-section">
    <div class="f-group"><label>Channel</label><select id="fChannel"></select></div>
    <div class="f-group"><label>Sub-Channel</label><select id="fSubChannel"></select></div>
  </div>
  <div class="f-divider"></div>
  <!-- Key Family -->
  <div class="f-section">
    <div class="f-group"><label>Key Family</label><select id="fKeyFamily"></select></div>
  </div>
  <div class="f-divider"></div>
  <!-- Salesman (searchable combobox) -->
  <div class="f-section">
    <div class="f-group">
      <label>Salesman</label>
      <div class="ss-wrap" id="ssWrap">
        <input type="text" class="ss-input" id="fSalesmanInput" placeholder="All Salesmen" autocomplete="off" spellcheck="false" />
        <span class="ss-arrow">&#9660;</span>
        <ul class="ss-list" id="ssList"></ul>
      </div>
      <select id="fSalesman" hidden></select>
    </div>
  </div>
  <div class="f-divider"></div>
  <!-- Display options -->
  <div class="f-section">
    <div class="f-group">
      <label>Metric</label>
      <select id="fMetric">
        <option value="rev" selected>Revenue</option>
        <option value="ctn">Quantity (CTN)</option>
        <option value="ton">Quantity (TON)</option>
      </select>
    </div>
    <div class="f-group">
      <label>Currency</label>
      <select id="fCurrency">
        <option value="SAR" selected>SAR</option>
        <option value="USD">USD</option>
      </select>
    </div>
  </div>
  <div class="f-divider"></div>
  <!-- Focus toggles -->
  <div class="f-section">
    <div class="f-group">
      <label>Completion</label>
      <div class="view-toggle">
        <button class="vt-btn on-track" id="btnOnTrack" onclick="toggleCompletion('on-track')" title="Salesmen &ge;80% completion"><span class="vt-dot"></span> On Track</button>
        <button class="vt-btn building" id="btnBuilding" onclick="toggleCompletion('building')" title="Salesmen 40&ndash;79% completion"><span class="vt-dot"></span> Building</button>
        <button class="vt-btn critical" id="btnCritical" onclick="toggleCompletion('critical')" title="Salesmen &lt;40% completion"><span class="vt-dot"></span> Critical</button>
      </div>
    </div>
    <div class="f-group">
      <label>Quick Focus</label>
      <div class="view-toggle">
        <button class="vt-btn risks" id="btnRisks" onclick="toggleView('risks')" title="High-value customers with &lt;40% revenue completion"><span class="vt-dot"></span> Top Risks</button>
        <button class="vt-btn wins" id="btnWins" onclick="toggleView('wins')" title="High-value customers with &ge;80% revenue completion"><span class="vt-dot"></span> Top Wins</button>
      </div>
    </div>
  </div>
  <!-- Actions -->
  <div class="f-section-actions">
    <button class="f-btn f-btn-reset" onclick="resetFilters()">&#8635; Reset</button>
    <button class="f-btn f-btn-export" onclick="exportCSV()">&#8681; Export CSV</button>
  </div>
</div>

<!-- STATS BAR -->
<div class="stats-bar" id="statsBar"></div>

<!-- MAIN -->
<div class="main" id="main"></div>

<!-- FOOTER -->
<div class="footer">Developed by <strong>Musab Shaikh</strong> &nbsp;&bull;&nbsp; JBS | Seara | Commercial Intelligence &nbsp;&bull;&nbsp; {_dt.now().year}</div>

<!-- INFO MODAL -->
<div class="modal-overlay" id="infoModal" onclick="if(event.target===this)closeInfo()">
  <div class="modal">
    <button class="modal-close" onclick="closeInfo()">&#10005; Close</button>
    <h2>&#9432; Info</h2>
    <div class="modal-section">
      <h3><span class="badge-battle">&#9876; Battles</span></h3>
      <p>Customers where the model predicts purchases (Confidence &gt; 0) but who are <b>not yet loyal</b> &mdash; they have lower historical engagement. These are opportunities the salesman must <b>&ldquo;fight&rdquo; for</b>: visit regularly, push orders, introduce new SKUs, and grow wallet share.</p>
    </div>
    <div class="modal-section">
      <h3><span class="badge-hold">&#9879; Hold Position</span></h3>
      <p>Customers who are <b>already loyal</b> (high historical activity, frequent purchases). The salesman&apos;s job is to <b>maintain the relationship</b>, protect existing orders, fulfil expectations, and prevent churn.</p>
    </div>
  </div>
</div>

<script>
// ===== DATA =====
const DATA = {data_json};
const ACTUALS_HIST = {actuals_hist_json};
const MONTHS = {json.dumps(sorted_months)};
const REGIONS = {json.dumps(regions)};
const CHANNELS = {json.dumps(channels)};
const SUB_CHANNELS = {json.dumps(sub_channels)};
const KEY_CATS    = {json.dumps(KEY_CATS)};
const KEY_DATA    = {key_data_json};
const SALESMEN = {json.dumps(salesmen)};
const SKU_MAP = {sku_map_json};
const SKU_FAMILY2_MAP = {sku_family2_map_json};
const SKU_CONTRIB_MAP = {sku_contrib_map_json};
const LAST_ORDER_MONTH_MAP = {last_order_month_map_json};
const USD_RATE = 3.75;
let RENDERED_SM = [];
let CURRENT_VIEW = 'all'; // 'all' | 'risks' | 'wins'

// ===== INIT FILTERS =====
function populateSelect(id, items, allLabel) {{
  const sel = document.getElementById(id);
  const opt0 = document.createElement('option'); opt0.value='All'; opt0.textContent=allLabel||'All'; sel.appendChild(opt0);
  items.forEach(v => {{ const o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }});
}}
populateSelect('fMonth',      MONTHS,         'All');
populateSelect('fRegion',     REGIONS,        'All');
populateSelect('fChannel',    CHANNELS,       'All');
populateSelect('fSubChannel', SUB_CHANNELS,   'All');
populateSelect('fKeyFamily',  KEY_CATS,       'All');
populateSelect('fSalesman',   SALESMEN,       'All Salesmen'); // hidden; used as value store

// Default to latest month
document.getElementById('fMonth').value = MONTHS[MONTHS.length - 1];

// ===== SALESMAN SEARCH-SELECT =====
let _smList = ['All', ...SALESMEN];

function buildSSList(names, q) {{
  const ul = document.getElementById('ssList');
  const cur = document.getElementById('fSalesman').value;
  const sq  = (q || '').toLowerCase().trim();
  const filtered = sq ? names.filter(n => n === 'All' || n.toLowerCase().includes(sq)) : names;
  ul.innerHTML = '';
  filtered.forEach(v => {{
    const li = document.createElement('li');
    li.textContent = v === 'All' ? 'All Salesmen' : v;
    li.dataset.value = v;
    if (v === cur) li.classList.add('sel');
    li.addEventListener('mousedown', e => {{
      e.preventDefault();
      setSmValue(v);
      closeSSList();
      render();
    }});
    ul.appendChild(li);
  }});
}}
function openSSList()  {{ document.getElementById('ssList').classList.add('open');  document.getElementById('ssWrap').classList.add('open'); }}
function closeSSList() {{
  document.getElementById('ssList').classList.remove('open');
  document.getElementById('ssWrap').classList.remove('open');
  // Restore display to match current selection
  const cur = document.getElementById('fSalesman').value;
  document.getElementById('fSalesmanInput').value = cur === 'All' ? '' : cur;
}}
function setSmValue(v) {{
  document.getElementById('fSalesman').value = v;
  document.getElementById('fSalesmanInput').value = v === 'All' ? '' : v;
}}
(function initSS() {{
  const inp = document.getElementById('fSalesmanInput');
  inp.addEventListener('focus', () => {{ buildSSList(_smList); openSSList(); }});
  inp.addEventListener('blur',  () => {{ setTimeout(closeSSList, 150); }});
  inp.addEventListener('input', () => {{ buildSSList(_smList, inp.value); openSSList(); }});
}})();

// ===== EVENT LISTENERS =====
document.getElementById('fMonth').addEventListener('change', render);
document.getElementById('fRegion').addEventListener('change',     () => {{ updateSalesmanFilter(); render(); }});
document.getElementById('fChannel').addEventListener('change',    () => {{ updateSalesmanFilter(); render(); }});
document.getElementById('fSubChannel').addEventListener('change', () => {{ updateSalesmanFilter(); render(); }});
document.getElementById('fKeyFamily').addEventListener('change',  () => {{ updateSalesmanFilter(); render(); }});
document.getElementById('fSalesman').addEventListener('change', render);
document.getElementById('fMetric').addEventListener('change', render);
document.getElementById('fCurrency').addEventListener('change', render);
let COMPLETION_FILTER = 'all';

function toggleCompletion(v) {{
  COMPLETION_FILTER = (COMPLETION_FILTER === v) ? 'all' : v;
  document.getElementById('btnOnTrack').className = 'vt-btn on-track' + (COMPLETION_FILTER === 'on-track' ? ' active' : '');
  document.getElementById('btnBuilding').className = 'vt-btn building' + (COMPLETION_FILTER === 'building' ? ' active' : '');
  document.getElementById('btnCritical').className = 'vt-btn critical' + (COMPLETION_FILTER === 'critical' ? ' active' : '');
  render();
}}

function resetFilters() {{
  document.getElementById('fMonth').value      = MONTHS[MONTHS.length - 1];
  document.getElementById('fRegion').value     = 'All';
  document.getElementById('fChannel').value    = 'All';
  document.getElementById('fSubChannel').value = 'All';
  document.getElementById('fKeyFamily').value  = 'All';
  updateSalesmanFilter();
  setSmValue('All');
  document.getElementById('fMetric').value   = 'rev';
  document.getElementById('fCurrency').value = 'SAR';
  COMPLETION_FILTER = 'all';
  document.getElementById('btnOnTrack').className = 'vt-btn on-track';
  document.getElementById('btnBuilding').className = 'vt-btn building';
  document.getElementById('btnCritical').className = 'vt-btn critical';
  CURRENT_VIEW = 'all';
  document.getElementById('btnRisks').className = 'vt-btn risks';
  document.getElementById('btnWins').className  = 'vt-btn wins';
  render();
}}

function toggleView(v) {{
  CURRENT_VIEW = (CURRENT_VIEW === v) ? 'all' : v;
  document.getElementById('btnRisks').className = 'vt-btn risks' + (CURRENT_VIEW === 'risks' ? ' active' : '');
  document.getElementById('btnWins').className = 'vt-btn wins' + (CURRENT_VIEW === 'wins' ? ' active' : '');
  render();
}}

function updateSalesmanFilter() {{
  const region     = document.getElementById('fRegion').value;
  const channel    = document.getElementById('fChannel').value;
  const subChannel = document.getElementById('fSubChannel').value;
  const keyFamily  = document.getElementById('fKeyFamily').value;
  const prevVal    = document.getElementById('fSalesman').value;
  const isAll = region === 'All' && channel === 'All' && subChannel === 'All' && keyFamily === 'All';
  let names;
  if (isAll) {{
    names = SALESMEN;
  }} else {{
    const src = keyFamily !== 'All' ? KEY_DATA.filter(r => r.SKU_Category === keyFamily) : DATA;
    const sub = src.filter(r => {{
      if (region     !== 'All' && r.Region      !== region)     return false;
      if (channel    !== 'All' && r.channel     !== channel)    return false;
      if (subChannel !== 'All' && r.sub_channel !== subChannel) return false;
      return true;
    }});
    names = [...new Set(sub.map(r => r.Salesman))].sort();
  }}
  _smList = ['All', ...names];
  // Rebuild hidden select (source of truth for render())
  const sel = document.getElementById('fSalesman');
  sel.innerHTML = '';
  const opt0 = document.createElement('option'); opt0.value='All'; opt0.textContent='All Salesmen'; sel.appendChild(opt0);
  names.forEach(v => {{ const o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }});
  const newVal = names.includes(prevVal) ? prevVal : 'All';
  setSmValue(newVal);
  buildSSList(_smList);
}}

// ===== HELPERS =====
function fmt(n) {{ return Math.round(n).toLocaleString(); }}
function fmtRev(n) {{
  const cur = document.getElementById('fCurrency').value;
  if (cur === 'USD') return 'USD ' + Math.round(n / USD_RATE).toLocaleString();
  return 'SAR ' + fmt(n);
}}

function progressColor(pct) {{
  if (pct >= 80) return 'fill-green';
  if (pct >= 40) return 'fill-amber';
  return 'fill-red';
}}

// ===== RENDER =====
function render() {{
  const month = document.getElementById('fMonth').value;
  const region = document.getElementById('fRegion').value;
  const salesman = document.getElementById('fSalesman').value;
  const metric = document.getElementById('fMetric').value;
  const pK = metric === 'rev' ? 'exp_rev' : metric === 'ctn' ? 'pred_qty' : 'pred_ton';
  const aK = metric === 'rev' ? 'act_rev' : metric === 'ctn' ? 'act_qty' : 'act_ton';
  const fmtV = metric === 'rev' ? v => fmtRev(v) : v => fmt(v);
  const expLabel = metric === 'rev' ? 'Expected Revenue' : 'Expected Qty';
  const actLabel = metric === 'rev' ? 'Actual Revenue'   : 'Actual Qty';
  const unitSfx  = metric === 'ctn' ? ' CTN' : metric === 'ton' ? ' TON' : '';

  const channel    = document.getElementById('fChannel').value;
  const subChannel = document.getElementById('fSubChannel').value;
  const keyFamily  = document.getElementById('fKeyFamily').value;
  const activeData = keyFamily !== 'All' ? KEY_DATA.filter(r => r.SKU_Category === keyFamily) : DATA;

  // Filter data
  let rows = activeData.filter(r => {{
    if (month      !== 'All' && r.Month      !== month)      return false;
    if (region     !== 'All' && r.Region     !== region)     return false;
    if (channel    !== 'All' && r.channel    !== channel)    return false;
    if (subChannel !== 'All' && r.sub_channel !== subChannel) return false;
    if (salesman   !== 'All' && r.Salesman   !== salesman)   return false;
    return true;
  }});

  // Group by salesman → customer list
  const smMap = {{}};
  rows.forEach(r => {{
    const sm = r.Salesman || 'Unassigned';
    if (!smMap[sm]) smMap[sm] = {{name: sm, no: r.Salesman_No || '', region: r.Region || '', _custMap: {{}}}};
    const cid = r.Customer;
    const cm = smMap[sm]._custMap;
    if (!cm[cid]) {{
      cm[cid] = {{
        id: cid, name: r.Customer_Name || cid,
        _skuCodeSet: new Set(),
        category: r.category || 'battle',
        channel: r.channel || '',
        sub_channel: r.sub_channel || '',
        exp_rev: 0, act_rev: 0, pred_qty: 0, act_qty: 0,
        pred_ton: 0, act_ton: 0,
        _confSum: 0, _confN: 0, months_active: r.months_active || 0,
        _monthData: {{}},
      }};
    }}
    const c = cm[cid];
    (r.sku_codes || []).forEach(s => c._skuCodeSet.add(s));
    c.exp_rev += r.exp_rev || 0;
    c.act_rev += r.act_rev || 0;
    c.pred_qty += r.pred_qty || 0;
    c.act_qty += r.act_qty || 0;
    c.pred_ton += r.pred_ton || 0;
    c.act_ton += r.act_ton || 0;
    c._confSum += (r.avg_conf || 0) * (r.n_skus || 1);
    c._confN += r.n_skus || 1;
    if (r.months_active > c.months_active) c.months_active = r.months_active;
    if (r.category === 'hold') c.category = 'hold';
  }});

  // Populate monthly history
  activeData.forEach(r => {{
    const sm = r.Salesman || 'Unassigned';
    if (!smMap[sm]) return;
    const cm = smMap[sm]._custMap;
    const cid = r.Customer;
    if (!cm[cid]) return;
    if (region     !== 'All' && r.Region      !== region)     return;
    if (channel    !== 'All' && r.channel     !== channel)    return;
    if (subChannel !== 'All' && r.sub_channel !== subChannel) return;
    if (!r.Month) return;
    const c = cm[cid];
    if (!c._monthData[r.Month]) c._monthData[r.Month] = {{exp_rev:0,act_rev:0,pred_qty:0,act_qty:0,pred_ton:0,act_ton:0}};
    const md = c._monthData[r.Month];
    md.exp_rev += r.exp_rev||0; md.act_rev += r.act_rev||0;
    md.pred_qty += r.pred_qty||0; md.act_qty += r.act_qty||0;
    md.pred_ton += r.pred_ton||0; md.act_ton += r.act_ton||0;
  }});

  // Supplement _monthData from ACTUALS_HIST (all months, all-SKU totals)
  if (keyFamily === 'All') {{
    Object.values(smMap).forEach(sm => {{
      Object.entries(sm._custMap).forEach(([cid, c]) => {{
        const ah = ACTUALS_HIST[String(cid)];
        if (!ah) return;
        Object.entries(ah).forEach(([m, vals]) => {{
          if (!c._monthData[m]) c._monthData[m] = {{exp_rev:0,act_rev:0,pred_qty:0,act_qty:0,pred_ton:0,act_ton:0}};
          c._monthData[m].act_qty = vals[0];
          c._monthData[m].act_rev = vals[1];
          c._monthData[m].act_ton = vals[2];
        }});
      }});
    }});
  }}

  // Flatten _custMap → customers array
  Object.values(smMap).forEach(sm => {{
    sm.customers = Object.values(sm._custMap).map(c => {{
      c.sku_codes = Array.from(c._skuCodeSet); c.n_skus = c.sku_codes.length;
      c.avg_conf = c._confN > 0 ? c._confSum / c._confN : 0;
      c.monthData = c._monthData;
      delete c._skuCodeSet; delete c._confSum; delete c._confN; delete c._monthData;
      return c;
    }});
    delete sm._custMap;
  }});

  // Sort salesmen by total expected metric value
  let salesmenArr = Object.values(smMap).sort((a, b) => {{
    const aVal = a.customers.reduce((s, c) => s + (c[pK] || 0), 0);
    const bVal = b.customers.reduce((s, c) => s + (c[pK] || 0), 0);
    return bVal - aVal;
  }});

  // Apply Completion filter at salesman level
  if (COMPLETION_FILTER !== 'all') {{
    salesmenArr = salesmenArr.filter(sm => {{
      const smExp = sm.customers.reduce((s, c) => s + (c[pK] || 0), 0);
      const smAct = sm.customers.reduce((s, c) => s + (c[aK] || 0), 0);
      const pct = smExp > 0 ? smAct / smExp * 100 : 0;
      if (COMPLETION_FILTER === 'on-track')  return pct >= 80;
      if (COMPLETION_FILTER === 'building')  return pct >= 40 && pct < 80;
      if (COMPLETION_FILTER === 'critical')  return pct < 40;
      return true;
    }});
  }}

  // Apply Top Risks / Top Wins view filter
  let visibleSalesmen = salesmenArr;
  if (CURRENT_VIEW !== 'all') {{
    const allCusts = salesmenArr.flatMap(sm => sm.customers);
    const expVals = allCusts.map(c => c[pK] || 0).filter(v => v > 0).sort((a, b) => a - b);
    const medianExpVal = expVals.length > 0 ? expVals[Math.floor(expVals.length / 2)] : 0;
    visibleSalesmen = salesmenArr.map(sm => ({{
      ...sm,
      customers: sm.customers.filter(c => {{
        if ((c[pK] || 0) < medianExpVal) return false;
        const revPct = (c[pK] || 0) > 0 ? (c[aK] || 0) / (c[pK] || 0) * 100 : 0;
        return CURRENT_VIEW === 'risks' ? revPct < 40 : revPct >= 80;
      }})
    }})).filter(sm => sm.customers.length > 0);
  }}

  RENDERED_SM = visibleSalesmen;
  updateStats(visibleSalesmen);

  const main = document.getElementById('main');
  if (visibleSalesmen.length === 0) {{
    const viewMsg = CURRENT_VIEW === 'risks'
      ? 'No high-value customers with low completion (&lt;40%) found for these filters.'
      : CURRENT_VIEW === 'wins'
      ? 'No high-value customers with high completion (&ge;80%) found for these filters.'
      : 'No leads found for the selected filters.';
    main.innerHTML = `<div class="empty">${{viewMsg}}</div>`;
    return;
  }}

  main.innerHTML = visibleSalesmen.map((sm, si) => {{
    const custs = sm.customers;
    const battles = custs.filter(c => c.category === 'battle').sort((a, b) => (b[pK]||0) - (a[pK]||0));
    const holds   = custs.filter(c => c.category === 'hold').sort((a, b) => (b[pK]||0) - (a[pK]||0));
    const totalExp = custs.reduce((s, c) => s + (c[pK] || 0), 0);
    const totalAct = custs.reduce((s, c) => s + (c[aK] || 0), 0);

    const isOpen = salesman !== 'All' || si === 0 ? 'open' : '';

    return `<div class="sm-card ${{isOpen}}" data-idx="${{si}}">
      <div class="sm-header" onclick="toggleSM(${{si}})">
        <div>
          <div class="sm-name">${{esc(sm.name)}} <span style="font-weight:400;font-size:12px;color:var(--slate-500)">#${{sm.no}}</span></div>
          <div class="sm-meta">
            <span>${{sm.region}}</span>
            <span><b>${{custs.length}}</b> customers</span>
            <span><b>${{battles.length}}</b> battles</span>
            <span><b>${{holds.length}}</b> hold</span>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:20px;">
          <div style="text-align:right">
            <div style="font-size:15px;font-weight:700;color:var(--red-700)">${{fmtV(totalExp)}}${{unitSfx}}</div>
            <div style="font-size:11px;color:var(--slate-500)">${{expLabel}}</div>
          </div>
          ${{totalExp > 0 ? (() => {{
            const compPct = Math.min(Math.round(totalAct / totalExp * 100), 100);
            const compColor = compPct >= 80 ? 'var(--green-600)' : compPct >= 40 ? 'var(--amber-600)' : 'var(--red-500)';
            return `<div style="text-align:center;min-width:80px">
              <div style="font-size:15px;font-weight:700;color:${{compColor}}">${{compPct}}%</div>
              <div style="height:5px;background:var(--slate-200);border-radius:3px;margin-top:4px;overflow:hidden">
                <div style="height:100%;width:${{compPct}}%;background:${{compColor}};border-radius:3px;transition:width .4s ease"></div>
              </div>
            </div>`;
          }})() : ''}}
          <span class="sm-arrow">&#9660;</span>
        </div>
      </div>
      <div class="sm-body">
        <!-- Summary -->
        <div class="summary-strip" style="padding-top:12px">
          <div class="summary-chip"><div class="sv">${{fmtRev(custs.reduce((s,c)=>s+c.exp_rev,0))}}</div><div class="sl">Expected Revenue</div></div>
          <div class="summary-chip"><div class="sv">${{fmtRev(custs.reduce((s,c)=>s+c.act_rev,0))}}</div><div class="sl">Actual Revenue</div></div>
          <div class="summary-chip"><div class="sv">${{fmt(custs.reduce((s,c)=>s+c.pred_qty,0))}} CTN</div><div class="sl">Predicted Qty</div></div>
          <div class="summary-chip"><div class="sv">${{fmt(custs.reduce((s,c)=>s+c.act_qty,0))}} CTN</div><div class="sl">Actual Qty</div></div>
          <div class="summary-chip"><div class="sv">${{(() => {{ const e=custs.reduce((s,c)=>s+c.exp_rev,0); return e>0?Math.round(custs.reduce((s,c)=>s+c.act_rev,0)/e*100):0; }})()}}%</div><div class="sl">Revenue Completion</div></div>
        </div>
        <!-- Category Tabs -->
        <div class="cat-tabs">
          <div class="cat-tab active" onclick="switchCat(${{si}},'battle')">&#9876; Battles <span class="cat-count">${{battles.length}}</span></div>
          <div class="cat-tab" onclick="switchCat(${{si}},'hold')">&#9879; Hold Position <span class="cat-count">${{holds.length}}</span></div>
        </div>
        <div class="cat-grid" id="cat_${{si}}_battle">${{renderCustomers(battles, metric, si)}}</div>
        <div class="cat-grid" id="cat_${{si}}_hold" style="display:none">${{renderCustomers(holds, metric, si)}}</div>
      </div>
    </div>`;
  }}).join('');
}}

function renderCustomers(custs, metric, si) {{
  if (custs.length === 0) return '<div class="empty">No customers in this category.</div>';

  const metricLabel = metric === 'rev' ? 'Revenue' : metric === 'ctn' ? 'Qty (CTN)' : 'Qty (TON)';
  const predKey = metric === 'rev' ? 'exp_rev' : metric === 'ctn' ? 'pred_qty' : 'pred_ton';
  const actKey = metric === 'rev' ? 'act_rev' : metric === 'ctn' ? 'act_qty' : 'act_ton';
  const fmtVal = metric === 'rev' ? v => fmtRev(v) : v => fmt(v);

  return custs.map(c => {{
    const pred = c[predKey] || 0;
    const act = c[actKey] || 0;
    const pct = pred > 0 ? Math.min(Math.round(act / pred * 100), 999) : 0;

    return `<div class="cust-wrapper">
      <div class="cust-row" onclick="toggleExpand(this)">
        <div class="cust-info">
          <div class="cust-name"><span class="expand-arrow">&#9654;</span> ${{esc(c.name)}}</div>
          <div class="cust-id">#${{c.id}} &middot; ${{c.n_skus}} SKUs &middot; ${{c.channel}}</div>
        </div>
        <div class="cust-metric">
          <div class="cm-val">${{fmtVal(pred)}}</div>
          <div class="cm-sub">Expected</div>
        </div>
        <div class="cust-metric">
          <div class="cm-val">${{fmtVal(act)}}</div>
          <div class="cm-sub">Actual</div>
        </div>
        <div class="cust-metric">
          <div class="cm-val" style="color:${{pct >= 80 ? 'var(--green-600)' : pct >= 40 ? 'var(--amber-600)' : 'var(--red-500)'}}">${{pct}}%</div>
          <div class="cm-sub">Completion</div>
        </div>
        <div class="cust-progress">
          <div class="progress-row">
            <div class="progress-bar"><div class="progress-fill ${{progressColor(pct)}}" style="width:${{Math.min(pct, 100)}}%"></div></div>
          </div>
        </div>
      </div>
      <div class="cust-expand" data-si="${{si}}" data-cid="${{c.id}}"></div>
    </div>`;
  }}).join('');
}}

function esc(s) {{
  const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML;
}}

function normKey(v) {{
  const s = String(v ?? '');
  return s.endsWith('.0') ? s.slice(0, -2) : s;
}}

function shortMonthLabel(month) {{
  if (!month) return '';
  const parts = String(month).split(' ');
  return parts.length >= 2 ? parts[0].slice(0, 3) + ' ' + parts[1].slice(-2) : String(month);
}}

function calcCompletion(act, exp) {{
  return exp > 0 ? Math.min((act / exp) * 100, 999) : 0;
}}

function detectTrend(values) {{
  if (!values || values.length < 2) return {{ key: 'flat', label: 'Flat', icon: '&#8594;' }};
  const recent = values.slice(-3);
  const first = recent[0] ?? 0;
  const last = recent[recent.length - 1] ?? 0;
  const delta = last - first;
  if (delta >= 8) return {{ key: 'up', label: 'Improving', icon: '&#8599;' }};
  if (delta <= -8) return {{ key: 'down', label: 'Declining', icon: '&#8600;' }};
  return {{ key: 'flat', label: 'Flat', icon: '&#8594;' }};
}}

function toggleChart(el) {{
  const section = el.closest('.chart-section');
  section.classList.toggle('open');
  if (section.classList.contains('open')) {{
    const wrap = section.querySelector('.chart-canvas-wrap');
    if (!wrap.dataset.rendered) {{
      wrap.dataset.rendered = '1';
      const months = JSON.parse(section.dataset.months);
      const values = JSON.parse(section.dataset.values);
      const tone = section.dataset.tone;
      wrap.innerHTML = buildChartSVG(months, values, tone, wrap.offsetWidth || 500);
    }}
  }}
}}

function buildChartSVG(months, values, tone, W) {{
  const H = 110;
  const padL = 36, padR = 10, padT = 10, padB = 26;
  const innerW = W - padL - padR;
  const innerH = H - padT - padB;
  const n = values.length;
  if (!n) return '';
  const maxVal = Math.max(100, ...values);
  function xPos(i) {{ return padL + (n > 1 ? (innerW / (n - 1)) * i : innerW / 2); }}
  function yPos(v) {{ return padT + innerH - (Math.max(v, 0) / maxVal) * innerH; }}
  const pts = values.map((v, i) => ({{x: xPos(i), y: yPos(v)}}));
  const linePath = pts.map((p, i) => (i === 0 ? 'M' : 'L') + p.x.toFixed(1) + ',' + p.y.toFixed(1)).join(' ');
  const areaPath = 'M' + xPos(0).toFixed(1) + ',' + (padT + innerH).toFixed(1) + ' ' +
    pts.map(p => 'L' + p.x.toFixed(1) + ',' + p.y.toFixed(1)).join(' ') +
    ' L' + xPos(n - 1).toFixed(1) + ',' + (padT + innerH).toFixed(1) + ' Z';
  const strokeColor = tone === 'rev' ? '#DC2626' : '#D97706';
  const areaFill   = tone === 'rev' ? 'rgba(220,38,38,.09)' : 'rgba(217,119,6,.11)';
  const yTicks = maxVal > 120 ? [0, 50, 100, Math.ceil(maxVal / 10) * 10] : [0, 50, 100];
  const grids = yTicks.map(t => {{
    const y = yPos(t).toFixed(1);
    if (t === 100) {{
      return '<line x1="' + padL + '" y1="' + y + '" x2="' + (W - padR) + '" y2="' + y + '" stroke="#16A34A" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.7"/>' +
        '<text x="' + (padL - 5) + '" y="' + y + '" text-anchor="end" dominant-baseline="middle" fill="#16A34A" font-size="9" font-weight="700" font-family="-apple-system,sans-serif">100%</text>' +
        '<text x="' + (W - padR) + '" y="' + (parseFloat(y) - 5) + '" text-anchor="end" fill="#16A34A" font-size="8" font-weight="600" font-family="-apple-system,sans-serif">&#9654; Target</text>';
    }}
    const dash = (t > 0) ? ' stroke-dasharray="3,3"' : '';
    return '<line x1="' + padL + '" y1="' + y + '" x2="' + (W - padR) + '" y2="' + y + '" stroke="#E2E8F0" stroke-width="1"' + dash + '/>' +
      '<text x="' + (padL - 5) + '" y="' + y + '" text-anchor="end" dominant-baseline="middle" fill="#94A3B8" font-size="9" font-family="-apple-system,sans-serif">' + t + '%</text>';
  }}).join('');
  const xLabels = months.map((m, i) => {{
    const x = xPos(i).toFixed(1);
    return '<text x="' + x + '" y="' + (padT + innerH + 16) + '" text-anchor="middle" fill="#64748B" font-size="9" font-family="-apple-system,sans-serif">' + shortMonthLabel(m) + '</text>';
  }}).join('');
  const dots = pts.map((p, i) =>
    '<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="3" fill="' + strokeColor + '" stroke="#fff" stroke-width="1.5"><title>' + months[i] + ': ' + values[i].toFixed(0) + '%</title></circle>'
  ).join('');
  return '<svg width="' + W + '" height="' + H + '" style="display:block;overflow:visible">' +
    grids + xLabels +
    '<path d="' + areaPath + '" fill="' + areaFill + '"/>' +
    '<path d="' + linePath + '" fill="none" stroke="' + strokeColor + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    dots +
  '</svg>';
}}

function renderCompletionChart(months, values, tone, label) {{
  if (!months.length) return '';
  const latest = values[values.length - 1];
  const best = Math.max(...values);
  const trend = detectTrend(values);
  const mData = JSON.stringify(months).replace(/"/g, '&quot;');
  const vData = JSON.stringify(values).replace(/"/g, '&quot;');
  return '<div class="chart-section" data-months="' + mData + '" data-values="' + vData + '" data-tone="' + tone + '">' +
    '<div class="chart-toggle" onclick="toggleChart(this)">' +
      '<span class="chart-toggle-label">&#128200; 6-Month Completion &mdash; ' + esc(label) + '</span>' +
      '<div style="display:flex;align-items:center;gap:10px">' +
        '<span class="trend-badge ' + trend.key + '">' + trend.icon + ' ' + trend.label + '</span>' +
        '<span class="chart-toggle-arrow">&#9660;</span>' +
      '</div>' +
    '</div>' +
    '<div class="chart-body">' +
      '<div class="chart-canvas-wrap"></div>' +
      '<div style="font-size:10px;color:#64748B;text-align:right;padding:2px 6px 0">Latest <b>' + latest.toFixed(0) + '%</b> &nbsp;&middot;&nbsp; Peak <b>' + best.toFixed(0) + '%</b></div>' +
    '</div>' +
  '</div>';
}}

function toggleSM(idx) {{
  const card = document.querySelector(`.sm-card[data-idx="${{idx}}"]`);
  if (card) card.classList.toggle('open');
}}

function toggleExpand(rowEl) {{
  const wrapper = rowEl.closest('.cust-wrapper');
  const expandDiv = wrapper.querySelector('.cust-expand');
  const isOpen = wrapper.classList.toggle('expanded');
  if (isOpen && !expandDiv.dataset.loaded) {{
    const si = parseInt(expandDiv.dataset.si);
    const cid = expandDiv.dataset.cid;
    const metric = document.getElementById('fMetric').value;
    const sm = RENDERED_SM[si];
    if (!sm) return;
    const c = sm.customers.find(x => String(x.id) === String(cid));
    if (!c) return;
    const mLabel = metric === 'rev' ? 'Revenue' : metric === 'ctn' ? 'Quantity (CTN)' : 'Quantity (TON)';
    const pK = metric === 'rev' ? 'exp_rev' : metric === 'ctn' ? 'pred_qty' : 'pred_ton';
    const aK = metric === 'rev' ? 'act_rev' : metric === 'ctn' ? 'act_qty' : 'act_ton';
    const fV = metric === 'rev' ? v => fmtRev(v) : v => fmt(v);
    const chartMonths = MONTHS.slice(-6).filter(m => c.monthData && c.monthData[m]);
    const chartTone = metric === 'rev' ? 'rev' : 'vol';
    const chartValues = chartMonths.map(m => {{
      const md = c.monthData[m] || {{}};
      return calcCompletion(md[aK] || 0, md[pK] || 0);
    }});
    const chartSection = chartMonths.length ? renderCompletionChart(chartMonths, chartValues, chartTone, mLabel) : '';
    const skuItems = (c.sku_codes || []).map(code => {{
      const name = SKU_MAP[code] || 'Unknown';
      const familyII = SKU_FAMILY2_MAP[code] || '';
      const contribKey = normKey(c.id) + '||' + normKey(code);
      const contribPct = Number(SKU_CONTRIB_MAP[contribKey] || 0);
      const lastOrderMonth = LAST_ORDER_MONTH_MAP[contribKey] || '-';
      return {{ code, name, familyII, contribPct, lastOrderMonth }};
    }}).sort((a, b) => b.contribPct - a.contribPct);

    const skuRows = skuItems.map(item =>
      `<tr><td class="code-col">${{item.code}}</td><td>${{esc(item.name)}}</td><td>${{esc(item.familyII)}}</td><td>${{item.lastOrderMonth}}</td><td style="text-align:right">${{item.contribPct.toFixed(1)}}%</td></tr>`
    ).join('');
    const allHistMonths = c.monthData ? Object.keys(c.monthData).sort((a, b) => {{
      try {{ return new Date('1 ' + a) - new Date('1 ' + b); }} catch(e) {{ return a < b ? -1 : 1; }}
    }}) : [];
    const histRows = allHistMonths.map(m => {{
      const md = c.monthData[m];
      const a = md[aK] || 0;
      return `<tr><td>${{m}}</td><td style="text-align:right">${{fV(a)}}</td></tr>`;
    }}).join('');
    expandDiv.innerHTML = `<div class="xp-grid">
      <div class="xp-section">
        <div class="xp-title">SKU Portfolio (${{(c.sku_codes||[]).length}} items)</div>
        <div style="max-height:300px;overflow-y:auto">
        <table class="xp-table"><thead><tr><th>Item Code</th><th>SKU Name</th><th>Family II</th><th>Last Order</th><th style="text-align:right">Contri. %</th></tr></thead>
        <tbody>${{skuRows || '<tr><td colspan="5">No SKU data</td></tr>'}}</tbody></table>
        </div>
      </div>
      <div class="xp-section">
        <div class="xp-title">Monthly History &mdash; ${{mLabel}}</div>
        <table class="xp-table hist"><thead><tr><th>Month</th><th style="text-align:right">Actual</th></tr></thead>
        <tbody>${{histRows || '<tr><td colspan="2">No history</td></tr>'}}</tbody></table>
      </div>
    </div>${{chartSection}}`;
    expandDiv.dataset.loaded = 'true';
  }}
}}

function switchCat(smIdx, cat) {{
  const card = document.querySelector(`.sm-card[data-idx="${{smIdx}}"]`);
  card.querySelectorAll('.cat-tab').forEach((t, i) => {{
    t.classList.toggle('active', (i === 0 && cat === 'battle') || (i === 1 && cat === 'hold'));
  }});
  const bg = document.getElementById('cat_' + smIdx + '_battle');
  const hg = document.getElementById('cat_' + smIdx + '_hold');
  bg.style.display = cat === 'battle' ? '' : 'none';
  hg.style.display = cat === 'hold' ? '' : 'none';
}}

// ===== STATS BAR =====
function updateStats(arr) {{
  const sb = document.getElementById('statsBar');
  if (!arr || arr.length === 0) {{ sb.innerHTML = ''; return; }}
  const metric = document.getElementById('fMetric').value;
  const pK = metric === 'rev' ? 'exp_rev' : metric === 'ctn' ? 'pred_qty' : 'pred_ton';
  const aK = metric === 'rev' ? 'act_rev' : metric === 'ctn' ? 'act_qty' : 'act_ton';
  const mLabel = metric === 'rev' ? 'Revenue' : metric === 'ctn' ? 'Quantity (CTN)' : 'Quantity (TON)';
  const isSAR = document.getElementById('fCurrency').value !== 'USD';
  function fmtM(v) {{
    if (metric === 'rev') return (isSAR ? 'SAR ' : 'USD ') + Math.round(isSAR ? v : v / USD_RATE).toLocaleString();
    return Math.round(v).toLocaleString();
  }}
  function pctChip(p) {{
    const cls = p >= 80 ? 'g' : p >= 40 ? 'a' : 'r';
    return `<span class="sk-pct ${{cls}}">${{p}}%</span>`;
  }}
  let totalCust = 0, battles = 0, holds = 0;
  let bExp = 0, bAct = 0, hExp = 0, hAct = 0;
  arr.forEach(sm => {{
    sm.customers.forEach(c => {{
      totalCust++;
      if (c.category === 'battle') {{
        battles++; bExp += c[pK] || 0; bAct += c[aK] || 0;
      }} else {{
        holds++;  hExp += c[pK] || 0; hAct += c[aK] || 0;
      }}
    }});
  }});
  const bPct = bExp > 0 ? Math.round(bAct / bExp * 100) : 0;
  const hPct = hExp > 0 ? Math.round(hAct / hExp * 100) : 0;
  const wasOpen = sb.classList.contains('open');
  sb.innerHTML = `
    <div class="stats-bar-hdr" onclick="toggleStats()">
      <span>&#128202; Summary &mdash; <b>${{arr.length}}</b> Salesmen &middot; <b>${{totalCust.toLocaleString()}}</b> Customers &middot; <span style="color:var(--red-600)"><b>${{battles}}</b> Battles</span> &middot; <span style="color:var(--green-600)"><b>${{holds}}</b> Hold Position</span></span>
      <span style="font-size:10px;color:var(--slate-400)">Click to expand <span class="stats-bar-arrow">&#9660;</span></span>
    </div>
    <div class="stats-bar-body">
      <div class="stats-panel battle">
        <div class="stats-panel-title">&#9876; Battles &mdash; ${{battles.toLocaleString()}} customers</div>
        <div class="stats-rows">
          <div class="stats-kv">
            <div class="sk-label">Expected ${{mLabel}}</div>
            <div class="sk-exp">${{fmtM(bExp)}}</div>
          </div>
          <div class="stats-kv">
            <div class="sk-label">Actual ${{mLabel}}</div>
            <div class="sk-exp">${{fmtM(bAct)}}</div>
            <div class="sk-act">Completion ${{pctChip(bPct)}}</div>
          </div>
        </div>
      </div>
      <div class="stats-panel hold">
        <div class="stats-panel-title">&#9879; Hold Position &mdash; ${{holds.toLocaleString()}} customers</div>
        <div class="stats-rows">
          <div class="stats-kv">
            <div class="sk-label">Expected ${{mLabel}}</div>
            <div class="sk-exp">${{fmtM(hExp)}}</div>
          </div>
          <div class="stats-kv">
            <div class="sk-label">Actual ${{mLabel}}</div>
            <div class="sk-exp">${{fmtM(hAct)}}</div>
            <div class="sk-act">Completion ${{pctChip(hPct)}}</div>
          </div>
        </div>
      </div>
    </div>
  `;
  if (wasOpen) sb.classList.add('open');
}}

function toggleStats() {{
  document.getElementById('statsBar').classList.toggle('open');
}}

// ===== INFO MODAL =====
function openInfo() {{
  document.getElementById('infoModal').style.display = 'flex';
}}
function closeInfo() {{
  document.getElementById('infoModal').style.display = 'none';
}}

// ===== EXPORT CSV =====
function exportCSV() {{
  if (!RENDERED_SM || RENDERED_SM.length === 0) return;
  const metric = document.getElementById('fMetric').value;
  const pK = metric === 'rev' ? 'exp_rev' : metric === 'ctn' ? 'pred_qty' : 'pred_ton';
  const aK = metric === 'rev' ? 'act_rev' : metric === 'ctn' ? 'act_qty' : 'act_ton';
  const mLabel = metric === 'rev' ? 'Expected_Revenue' : metric === 'ctn' ? 'Expected_CTN' : 'Expected_TON';
  const aLabel = metric === 'rev' ? 'Actual_Revenue' : metric === 'ctn' ? 'Actual_CTN' : 'Actual_TON';
  const monthFilter = document.getElementById('fMonth').value;
  const csvRows = ['Salesman,Salesman_No,Region,Category,Customer_No,Customer_Name,SKUs,' + mLabel + ',' + aLabel + ',Completion_%,Avg_Confidence'];
  RENDERED_SM.forEach(sm => {{
    sm.customers.forEach(c => {{
      const p = c[pK] || 0, a = c[aK] || 0;
      const pct = p > 0 ? Math.round(a / p * 100) : 0;
      const conf = (c.avg_conf * 100).toFixed(0);
      const q = v => String.fromCharCode(34) + String(v).replace(/"/g, '""') + String.fromCharCode(34);
      csvRows.push([q(sm.name), q(sm.no), q(sm.region), c.category, q(c.id), q(c.name), c.n_skus, Math.round(p), Math.round(a), pct, conf].join(','));
    }});
  }});
  const NL = String.fromCharCode(10);
  const blob = new Blob([csvRows.join(NL)], {{type: 'text/csv;charset=utf-8;'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'salesman_leads_demo_' + (monthFilter === 'All' ? 'all' : monthFilter.replace(/ /g,'_')) + '.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
}}

// ===== INITIAL RENDER =====
render();
</script>
</body>
</html>"""

# ── EXPORT ──────────────────────────────────────────────────
output_file = os.path.join(os.path.dirname(__file__), "Salesman_Action_Dashboard_Demo.html")
print(f"Writing demo dashboard to: {output_file}")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(HTML)
size_kb = os.path.getsize(output_file) / 1024
print(f"Done! File: {output_file} ({size_kb:.0f} KB)")
