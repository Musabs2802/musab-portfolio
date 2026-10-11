"""Generate the fictional data behind the sample dashboards.

Writes public/dashboards/data/<name>.js, each defining window.DATA. The numbers
are made up but follow real patterns for Saudi businesses: SAR, Ramadan and Eid
peaks, the summer dip, National Day, retailer trade terms and so on.

Run from the repo root:  python3 scripts/dashboards/generate_data.py
"""

import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "public" / "dashboards" / "data"
OUT.mkdir(parents=True, exist_ok=True)

MONTHS = ["Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26",
          "Apr 26", "May 26", "Jun 26", "Jul 26", "Aug 26", "Sep 26"]


def write(name, data):
    body = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    (OUT / f"{name}.js").write_text(f"window.DATA={body};\n", encoding="utf-8")
    print(f"wrote {name}.js ({len(body) // 1024} KB)")


def noise(rng, pct):
    return 1 + rng.uniform(-pct, pct)


FY_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Frozen & chilled food: Ramadan (Feb-Mar 2026) and winter strong, summer softer
FMCG_SEASON = [0.95, 1.12, 1.18, 0.96, 1.0, 0.97, 0.9, 0.92, 1.0, 1.02, 1.0, 1.05]


# --------------------------------------------------------- sales vs target
def sales_performance():
    rng = random.Random(66)
    regions = ["Central", "Western", "Eastern", "Southern"]
    region_base = [15.5e6, 13.0e6, 9.0e6, 4.5e6]
    channels = ["Key accounts", "Supermarkets", "Traditional trade", "HoReCa", "Online & q-commerce"]
    ch_share = [0.34, 0.22, 0.27, 0.12, 0.05]
    cats = ["Poultry", "Ready meals", "Dairy & cheese", "Frozen veg & snacks"]
    cat_share = [0.46, 0.18, 0.21, 0.15]
    # Achievement vs target (the story): West lost a key listing, HoReCa soft,
    # online and ready meals growing, Southern traditional trade under-covered
    def ach(r, c, k):
        a = 0.99
        if r == 1: a -= 0.06
        if c == 3: a -= 0.07
        if c == 4: a += 0.16
        if k == 1: a += 0.07
        if r == 3 and c == 2: a -= 0.13
        if r == 1 and c == 0: a -= 0.05
        return a
    ly_growth = [1.06, 1.17, 1.07, 1.05]  # target vs last year by category

    rows = []  # month, region, channel, category, target, actual, lastYear
    for m in range(9):
        for r in range(4):
            for c in range(5):
                for k in range(4):
                    tgt = region_base[r] * ch_share[c] * cat_share[k] * FMCG_SEASON[m] * (1 + 0.004 * m)
                    act = tgt * ach(r, c, k) * noise(rng, 0.04)
                    ly = tgt / ly_growth[k] * noise(rng, 0.03) / (1.12 if c == 4 else 1)
                    rows.append([m, r, c, k, round(tgt), round(act), round(ly)])

    # October month-to-date by day (31 days, Fridays lighter); actuals to 10 Oct
    oct_target = sum(region_base) * FMCG_SEASON[9] * 1.04
    weights = [0.6 if date(2026, 10, d).weekday() == 4 else 1.0 for d in range(1, 32)]
    wsum = sum(weights)
    daily_target = [oct_target * w / wsum for w in weights]
    daily_actual = [round(t * 0.935 * noise(rng, 0.07)) for t in daily_target[:10]]
    mtd_split = []  # region x channel share of MTD actual vs target
    for r in range(4):
        for c in range(5):
            t = oct_target * region_base[r] / sum(region_base) * ch_share[c]
            mtd_split.append([r, c, round(t), round(t * 10 / 31 * ach(r, c, 0) * 0.95 * noise(rng, 0.05))])

    first = ["Faisal", "Omar", "Yousef", "Imran", "Khalid", "Saeed", "Anwar", "Bilal", "Majed", "Nasser",
             "Tariq", "Hamza", "Ziyad", "Rakan", "Sultan", "Adel", "Fahad", "Waleed", "Salman", "Hassan",
             "Abdullah", "Mazen", "Raed", "Sami"]
    last = ["Al-Harbi", "Khan", "Al-Qahtani", "Siddiqui", "Al-Zahrani", "Mansour", "Al-Ghamdi", "Haddad",
            "Al-Otaibi", "Al-Shehri", "Rahman", "Al-Dosari"]
    salesmen = []
    for i, f in enumerate(first):
        r = [0] * 8 + [1] * 7 + [2] * 6 + [3] * 3
        r = r[i]
        c = rng.choice([1, 2, 2, 3, 0])
        tgt = rng.uniform(0.9, 1.6) * 1e6 * FMCG_SEASON[9]
        a = ach(r, c, 0) * rng.uniform(0.82, 1.12)
        salesmen.append({"name": f"{f} {rng.choice(last)}", "region": r, "channel": c,
                         "target": round(tgt, -3), "mtd": round(tgt * 10 / 31 * a * 0.95, -2),
                         "ytdAch": round(100 * a * rng.uniform(0.97, 1.03), 1)})

    write("sales", {
        "months": FY_MONTHS[:9], "regions": regions, "channels": channels, "categories": cats,
        "rows": rows, "octDailyTarget": [round(t) for t in daily_target], "octDailyActual": daily_actual,
        "mtd": mtd_split, "salesmen": salesmen, "asOf": "10 Oct 2026",
    })


# --------------------------------------------------------- key accounts
def key_accounts():
    rng = random.Random(77)
    accounts = [
        # name, channel, gross sales YTD, on-invoice %, rebate %, promo %, listing & display %, cost-to-serve %, returns %
        ("Nakheel Hypermarkets", 0, 41.0e6, 0.06, 0.05, 0.06, 0.035, 0.055, 0.025),
        ("Danat Markets", 0, 27.5e6, 0.05, 0.04, 0.045, 0.025, 0.05, 0.015),
        ("Al Fanar Hyper", 0, 19.0e6, 0.05, 0.045, 0.05, 0.03, 0.05, 0.02),
        ("Sahra Hyper", 0, 12.4e6, 0.045, 0.035, 0.04, 0.02, 0.06, 0.018),
        ("Qimma Supermarkets", 1, 15.8e6, 0.04, 0.03, 0.035, 0.015, 0.065, 0.012),
        ("Rawabi Mart", 1, 9.6e6, 0.035, 0.025, 0.03, 0.012, 0.07, 0.014),
        ("Wahat Markets", 1, 8.1e6, 0.04, 0.03, 0.03, 0.01, 0.075, 0.02),
        ("Bayt Al Taza", 1, 6.3e6, 0.03, 0.02, 0.025, 0.01, 0.08, 0.016),
        ("Tamr Express", 2, 7.4e6, 0.03, 0.02, 0.03, 0.0, 0.035, 0.006),
        ("Basket Now", 2, 4.9e6, 0.03, 0.02, 0.025, 0.0, 0.035, 0.005),
        ("Sufra Foodservice", 3, 11.2e6, 0.02, 0.03, 0.0, 0.0, 0.06, 0.01),
        ("Diyafa Catering", 3, 5.8e6, 0.025, 0.025, 0.0, 0.0, 0.065, 0.008),
    ]
    channels = ["Hypermarkets", "Supermarkets", "Online & q-commerce", "Foodservice"]
    cogs = [0.6, 0.6, 0.6, 0.6]
    out = []
    for name, ch, gross, inv, reb, promo, lst, cts, ret in accounts:
        mix = rng.uniform(-0.015, 0.015)  # richer or poorer product mix
        out.append({"name": name, "channel": ch, "gross": round(gross),
                    "invoice": round(gross * inv), "rebate": round(gross * reb), "promo": round(gross * promo),
                    "listing": round(gross * lst), "cogs": round(gross * (cogs[ch] + mix - (0.02 if ch == 2 else 0))),
                    "serve": round(gross * cts), "returns": round(gross * ret),
                    "lyMargin": None})
    for a in out:
        net = a["gross"] - a["invoice"] - a["rebate"] - a["promo"] - a["listing"]
        contrib = net - a["cogs"] - a["serve"] - a["returns"]
        a["lyMargin"] = round((contrib / net) * 100 + rng.uniform(-2.5, 3.5) + (3 if a["name"] == "Nakheel Hypermarkets" else 0), 1)

    total_net = sum(a["gross"] - a["invoice"] - a["rebate"] - a["promo"] - a["listing"] for a in out)
    total_contrib = sum(a["gross"] - a["invoice"] - a["rebate"] - a["promo"] - a["listing"] - a["cogs"] - a["serve"] - a["returns"] for a in out)
    # Year-on-year contribution bridge (SAR), sums to this year's contribution
    bridge = [("Last year", None), ("Price increase", 2.9e6), ("Volume", 1.7e6), ("Product mix", -1.1e6),
              ("Trade spend", -2.4e6), ("Cost to serve", -0.6e6)]
    ly = total_contrib - sum(v for _, v in bridge[1:])
    bridge[0] = ("Last year", ly)

    promos = [
        ("Nakheel Hypermarkets", "Ramadan gondola end + 20% off", 1_150_000, 820_000),
        ("Danat Markets", "Buy 2 get 1 nuggets", 640_000, 910_000),
        ("Al Fanar Hyper", "Leaflet + 15% off poultry", 520_000, 470_000),
        ("Qimma Supermarkets", "Ready meals sampling", 180_000, 365_000),
        ("Tamr Express", "App banner + free delivery", 150_000, 330_000),
        ("Nakheel Hypermarkets", "National Day 25% off", 690_000, 390_000),
        ("Sahra Hyper", "Cheese bundle", 210_000, 260_000),
        ("Rawabi Mart", "Summer ice cream chiller", 120_000, 95_000),
    ]
    write("accounts", {
        "channels": channels, "accounts": out,
        "bridge": [{"label": l, "value": round(v)} for l, v in bridge],
        "promos": [{"account": a, "name": n, "spend": s, "incGP": g, "roi": round((g - s) / s * 100)} for a, n, s, g in promos],
        "period": "Jan–Sep 2026", "totalNet": round(total_net),
    })


# --------------------------------------------------------- demand planning
def demand_planning():
    rng = random.Random(88)
    skus = [
        # name, category, base monthly units, unit price SAR, shelf life days, variability, promo months
        ("Chicken breast 1kg", "Poultry", 92_000, 24, 365, 0.08, [2, 8]),
        ("Whole chicken 1.1kg", "Poultry", 118_000, 17, 365, 0.07, [2]),
        ("Chicken nuggets 750g", "Poultry", 64_000, 21, 365, 0.14, [1, 2, 8]),
        ("Chicken franks 400g", "Poultry", 51_000, 9, 365, 0.12, [8]),
        ("Chicken shawarma 1kg", "Poultry", 18_000, 32, 365, 0.25, []),
        ("Beef burger 20pc", "Ready meals", 22_000, 38, 365, 0.18, [5]),
        ("Samosa pastry 40pc", "Ready meals", 26_000, 15, 365, 0.35, [1, 2]),
        ("Spring rolls 20pc", "Ready meals", 14_000, 18, 365, 0.3, [2]),
        ("Chicken biryani meal 400g", "Ready meals", 21_000, 14, 365, 0.2, []),
        ("Puff pastry 1kg", "Ready meals", 9_500, 19, 365, 0.4, [2]),
        ("Mozzarella 1kg", "Dairy & cheese", 30_000, 34, 120, 0.1, [4]),
        ("Cheddar slices 200g", "Dairy & cheese", 47_000, 11, 90, 0.11, []),
        ("Labneh 500g", "Dairy & cheese", 38_000, 12, 30, 0.13, [2]),
        ("Fresh yoghurt 1kg", "Dairy & cheese", 55_000, 8, 21, 0.09, []),
        ("Halloumi 225g", "Dairy & cheese", 12_000, 16, 60, 0.28, [2]),
        ("French fries 2.5kg", "Frozen veg & snacks", 41_000, 22, 365, 0.1, [6]),
        ("Mixed vegetables 900g", "Frozen veg & snacks", 33_000, 9, 365, 0.12, []),
        ("Okra 400g", "Frozen veg & snacks", 16_000, 7, 365, 0.22, [2]),
        ("Molokhia 400g", "Frozen veg & snacks", 11_000, 7, 365, 0.33, [2]),
        ("Ice cream tub 2L", "Frozen veg & snacks", 19_000, 21, 365, 0.45, [5, 6]),
    ]
    out = []
    for name, cat, base, price, life, var, promos in skus:
        actual, stat, cons = [], [], []
        level = base
        for m in range(12):
            season = FMCG_SEASON[m] * (1.4 if "Ice cream" in name and 4 <= m <= 7 else 1)
            promo = m in promos
            true = level * season * (1.22 if promo else 1) * rng.gauss(1, var)
            # Statistical forecast: unbiased, misses part of promo uplift
            s = level * season * (1.1 if promo else 1) * rng.gauss(1, var * 0.4)
            # Consensus: sales team adds optimism, much more in promo months
            c = s * (1.32 if promo else 1.04 + rng.uniform(0, 0.05))
            if m < 9:
                actual.append(round(max(0, true)))
            stat.append(round(s))
            cons.append(round(c))
            level *= 1.004
        daily = actual[-1] / 30
        cover_target = 14 if life <= 30 else 21 if life <= 120 else 35
        cover = cover_target * rng.choice([0.4, 0.7, 0.9, 1.0, 1.1, 1.3, 1.8, 2.6])
        if name in ("Labneh 500g", "Fresh yoghurt 1kg", "Halloumi 225g"):
            cover = life * rng.uniform(0.85, 1.3)  # chilled stock building past shelf life
        if name in ("Chicken breast 1kg", "Chicken nuggets 750g"):
            cover = rng.uniform(6, 9)  # A-class items running low before National Day
        out.append({"name": name, "category": cat, "price": price, "shelfLife": life,
                    "actual": actual, "stat": stat, "consensus": cons,
                    "stock": round(daily * cover), "coverTarget": cover_target})

    # Supply side: stock by DC, safety stock, lead times and planned receipts
    srng = random.Random(89)
    dcs = ["Riyadh DC", "Jeddah DC", "Dammam DC"]
    for o in out:
        split = [0.45, 0.35, 0.2]
        if o["name"] == "Chicken breast 1kg":
            split = [0.62, 0.18, 0.2]  # stock sits in Riyadh while Jeddah runs short
        o["dcStock"] = [round(o["stock"] * x * noise(srng, 0.1)) for x in split]
        o["safetyDays"] = 7 if o["shelfLife"] <= 30 else 10 if o["shelfLife"] <= 120 else 14
        o["leadWeeks"] = 1 if o["shelfLife"] <= 30 else 2 if o["category"] != "Poultry" else 3
        weekly = o["consensus"][9] / 4.33
        batch = round(weekly * srng.choice([2, 3, 4]), -2)
        receipts = [0] * 12
        if o["name"] in ("Chicken breast 1kg", "Chicken nuggets 750g"):
            for w, f in zip((3, 5, 7, 9, 11), (2.6, 2.1, 2.1, 2.1, 2.1)):
                receipts[w] = round(weekly * f, -2)  # next production slot is week 4
        elif o["shelfLife"] <= 60:
            for w in range(2, 12, 2):
                receipts[w] = round(weekly * 1.6, -2)
        else:
            stock_w = o["stock"]
            for w in range(12):
                stock_w -= weekly
                if stock_w < weekly * (o["safetyDays"] / 7 + o["leadWeeks"]):
                    receipts[w] = batch; stock_w += batch
        o["receipts"] = receipts
        o["batch"] = batch

    weeks = [(date(2026, 4, 5) + timedelta(weeks=i)).strftime("%d %b") for i in range(26)]
    otif = []
    for i in range(26):
        v = 95.5 + srng.uniform(-1.4, 1.2) - (2.8 if 9 <= i <= 12 else 0) - (3.5 if i >= 23 else 0)
        otif.append(round(v, 1))
    misses = [("Out of stock at DC", 41), ("Late truck dispatch", 23), ("Short-picked", 14),
              ("Order after cut-off", 12), ("Temperature hold", 6), ("Damaged in transit", 4)]
    suppliers = [
        ("Qassim Poultry Farms", "Live birds", 3, 96.5, 98.1),
        ("Al Kharj Dairy Inputs", "Milk & cream", 1, 97.8, 99.0),
        ("Gulf Pack", "Trays & film", 4, 81.4, 93.2),
        ("Euro Dairy Powder (import)", "Milk powder", 8, 74.6, 96.4),
        ("Spice Masters", "Seasonings", 3, 94.2, 97.5),
        ("Coldline Logistics", "Primary freight", 1, 88.3, 99.2),
        ("Saudi Flour Mills", "Flour & crumb", 2, 97.1, 98.6),
        ("PackPro Cartons", "Shipper cartons", 3, 90.5, 95.8),
    ]
    lines = ["Poultry line 1", "Poultry line 2", "Ready meals", "Dairy & cheese"]
    prod = []
    for li, ln in enumerate(lines):
        for w in range(13):
            plan = [62_000, 58_000, 21_000, 34_000][li] * noise(srng, 0.05)
            adh = 0.97 + srng.uniform(-0.04, 0.02) - (0.14 if li == 1 and 6 <= w <= 8 else 0) - (0.08 if li == 2 and w >= 10 else 0)
            prod.append([w, li, round(plan), round(plan * adh)])
    wh = [
        {"dc": "Riyadh DC", "zone": "Frozen", "capacity": 9_000, "used": 8_350},
        {"dc": "Riyadh DC", "zone": "Chilled", "capacity": 2_400, "used": 1_780},
        {"dc": "Jeddah DC", "zone": "Frozen", "capacity": 6_500, "used": 5_050},
        {"dc": "Jeddah DC", "zone": "Chilled", "capacity": 1_800, "used": 1_710},
        {"dc": "Dammam DC", "zone": "Frozen", "capacity": 4_000, "used": 2_640},
        {"dc": "Dammam DC", "zone": "Chilled", "capacity": 1_000, "used": 690},
    ]

    write("demand", {
        "months": FY_MONTHS, "actualMonths": 9, "skus": out,
        "categories": ["Poultry", "Ready meals", "Dairy & cheese", "Frozen veg & snacks"],
        "fillRate": [96.8, 95.1, 92.4, 96.2, 97.0, 96.5, 97.3, 96.9, 94.6],
        "dcs": dcs, "projWeeks": [(date(2026, 10, 4) + timedelta(weeks=i)).strftime("%d %b") for i in range(12)],
        "otifWeeks": weeks, "otif": otif,
        "misses": [{"reason": r, "orders": n} for r, n in misses],
        "suppliers": [{"name": n, "item": it, "leadWeeks": lt, "onTime": ot, "inFull": inf} for n, it, lt, ot, inf in suppliers],
        "lines": lines, "production": prod, "prodWeeks": [(date(2026, 7, 5) + timedelta(weeks=i)).strftime("%d %b") for i in range(13)],
        "warehouses": wh,
    })



# ------------------------------------------------------------- detailed P&L
def pnl():
    rng = random.Random(99)
    cats = ["Poultry", "Ready meals", "Dairy & cheese", "Frozen veg & snacks"]
    share = [0.46, 0.18, 0.21, 0.15]
    # Cost of goods as % of net sales (budget): materials, packaging, conversion, freight to DC
    cogs_pct = [[0.55, 0.05, 0.13, 0.05], [0.34, 0.08, 0.14, 0.04], [0.45, 0.07, 0.10, 0.04], [0.40, 0.06, 0.11, 0.05]]
    ach = [0.965, 1.06, 0.975, 0.985]
    growth = [1.03, 1.17, 1.05, 1.04]
    trade_pct = [0.14, 0.12, 0.13, 0.12]
    inflation = [1.08, 1.03, 1.09, 1.02]  # feed and milk powder costs up this year
    budget_net = [42_000_000 * FMCG_SEASON[m] * (1 + 0.004 * m) for m in range(12)]

    cat_rows = []  # [month, cat, scenario(0 actual,1 budget,2 LY), gross, trade, materials, packaging, conversion, freight]
    for m in range(12):
        for k in range(4):
            b_net = budget_net[m] * share[k]
            scen = {1: b_net}
            if m < 9:
                scen[0] = b_net * ach[k] * noise(rng, 0.025)
            scen[2] = (scen.get(0) or b_net * ach[k]) / growth[k] * noise(rng, 0.02)
            for sc, net in scen.items():
                tp = trade_pct[k] * (1.06 if sc == 0 else 0.97 if sc == 2 else 1)
                gross = net / (1 - tp)
                mat = cogs_pct[k][0] * (inflation[k] * (0.97 if m >= 2 else 1.0) if sc == 0 else 0.97 if sc == 2 else 1)
                conv = cogs_pct[k][2] * (0.97 if sc == 0 else 1.02 if sc == 2 else 1)
                frt = cogs_pct[k][3] * (1.08 if sc == 0 else 1)
                pack = cogs_pct[k][1] * (1.02 if sc == 0 else 1)
                cat_rows.append([m, k, sc, round(gross), round(gross - net),
                                 round(net * mat * noise(rng, 0.01)), round(net * pack), round(net * conv * noise(rng, 0.01)), round(net * frt)])

    opex = ["Distribution & warehousing", "Sales force", "Advertising & promotion", "General & admin", "Depreciation & amortisation", "Finance costs", "Zakat"]
    pct = {0: [0.070, 0.041, 0.026, 0.031, 0.022, 0.006, 0.007], 1: [0.065, 0.042, 0.035, 0.030, 0.022, 0.006, 0.008], 2: [0.064, 0.043, 0.032, 0.031, 0.023, 0.007, 0.008]}
    opex_rows = []  # [month, scenario, values...]
    for m in range(12):
        for sc in (0, 1, 2):
            if sc == 0 and m >= 9:
                continue
            net = sum((r[3] - r[4]) for r in cat_rows if r[0] == m and r[2] == sc)
            opex_rows.append([m, sc] + [round(net * p * noise(rng, 0.03)) for p in pct[sc]])

    # Gross profit bridge, LY Jan-Sep to TY Jan-Sep (sums exactly)
    def gp(sc):
        rows = [r for r in cat_rows if r[2] == sc and r[0] < 9]
        return sum((r[3] - r[4]) - r[5] - r[6] - r[7] - r[8] for r in rows)
    ly, ty = gp(2), gp(0)
    parts = [("Price increase", 0.62), ("Volume", 0.48), ("Mix", 0.12), ("Raw materials", -1.0), ("Factory efficiency", 0.10), ("Freight", -0.16)]
    total_change = ty - ly
    unit = 9_000_000
    vals = [v * unit for _, v in parts]
    vals[3] = total_change - (sum(vals) - vals[3])  # raw materials absorbs the remainder
    bridge = [{"label": "Last year", "value": round(ly), "total": True}] + \
             [{"label": n, "value": round(v)} for (n, _), v in zip(parts, vals)] + \
             [{"label": "This year", "value": round(ty), "total": True}]

    write("pnl", {"months": FY_MONTHS, "actualMonths": 9, "categories": cats, "catRows": cat_rows,
                  "opex": opex, "opexRows": opex_rows, "gpBridge": bridge})


# ------------------------------------------------------ pricing & promotion
def pricing():
    rng = random.Random(111)
    skus = [
        # name, category, base list price, unit cost, elasticity, competitor price ratio
        ("Chicken breast 1kg", 0, 24.0, 17.9, -1.9, 0.97),
        ("Whole chicken 1.1kg", 0, 17.0, 13.0, -2.3, 0.95),
        ("Chicken nuggets 750g", 0, 21.0, 13.4, -1.6, 1.02),
        ("Chicken franks 400g", 0, 9.0, 5.9, -1.4, 0.98),
        ("Samosa pastry 40pc", 1, 15.0, 8.6, -1.2, 1.05),
        ("Mozzarella 1kg", 2, 34.0, 22.8, -1.7, 0.96),
        ("Labneh 500g", 2, 12.0, 7.5, -1.1, 1.01),
        ("French fries 2.5kg", 3, 22.0, 13.9, -1.5, 0.99),
    ]
    channels = ["Key accounts", "Supermarkets", "Traditional trade"]
    ch_base = [5200, 3100, 4300]  # weekly units at list price, per SKU scale 1
    ch_elastic = [1.25, 1.0, 0.6]
    competitors = ["Golden Farms", "Al Reef Foods", "Nova Foods"]
    start = date(2024, 10, 5)
    weeks = [start + timedelta(weeks=i) for i in range(104)]

    def season(d):
        f = 1.0
        if date(2025, 2, 22) <= d <= date(2025, 3, 31) or date(2026, 2, 12) <= d <= date(2026, 3, 21):
            f = 1.22  # Ramadan
        elif d.month in (7, 8):
            f = 0.88
        elif d.month in (12, 1):
            f = 1.06
        return round(f * noise(rng, 0.02), 3)
    seas = [season(d) for d in weeks]

    rows = []  # week, sku, channel, list price, shelf price, competitor price, promo depth %, display, units
    scale = [1.0, 1.3, 0.8, 1.1, 0.6, 0.45, 0.7, 0.75]
    promo_log = []
    for si, (name, cat, price, cost, e, comp_ratio) in enumerate(skus):
        for ci in range(3):
            el = e * ch_elastic[ci]
            promo_weeks = set(rng.sample(range(4, 104), 9))
            for wi, d in enumerate(weeks):
                list_p = price * (1.06 if d >= date(2026, 3, 1) and cat in (0, 2) else 1.0) * (1.03 if d >= date(2025, 6, 1) else 1)
                comp = price * comp_ratio * (1.03 if d >= date(2025, 6, 1) else 1) * (1.02 if d >= date(2026, 5, 1) and cat in (0, 2) else 1) * noise(rng, 0.015)
                depth = rng.choice([10, 15, 20, 25, 30]) if wi in promo_weeks else 0
                display = 1 if depth and rng.random() < 0.4 else 0
                shelf = list_p * (1 - depth / 100)
                uplift = 1 + 2.1 * depth / 100 + 0.14 * display
                post = 0.9 if (wi - 1) in promo_weeks else 1.0  # pantry loading dip
                units = ch_base[ci] * scale[si] * seas[wi] * (shelf / price) ** el * (comp / (price * comp_ratio)) ** 0.7 * uplift * post * noise(rng, 0.07)
                rows.append([wi, si, ci, round(list_p, 2), round(shelf, 2), round(comp, 2), depth, display, round(units)])

    # Market share by category, monthly (us + 3 competitors; rest is "Others")
    months = [(date(2024, 10, 1) + timedelta(days=31 * i)).strftime("%b %y") for i in range(24)]
    share = []
    base = [[31, 27, 14, 9], [22, 11, 19, 15], [18, 14, 9, 21], [24, 16, 18, 12]]
    for k in range(4):
        series = []
        for i in range(24):
            dip = -2.6 if k in (0, 2) and 17 <= i <= 19 else -1.2 if k in (0, 2) and i >= 20 else 0
            us = base[k][0] + dip + (0.08 * i if k == 1 else 0) + rng.uniform(-0.5, 0.5)
            c1 = base[k][1] - dip * 0.8 + rng.uniform(-0.5, 0.5)
            c2 = base[k][2] + rng.uniform(-0.5, 0.5) - (0.05 * i if k == 1 else 0)
            c3 = base[k][3] + rng.uniform(-0.4, 0.4)
            series.append([round(us, 1), round(c1, 1), round(c2, 1), round(c3, 1)])
        share.append(series)

    # Next quarter seasonality (Oct-Dec 2026)
    next_q = [round(1.0 if i < 9 else 1.06, 2) for i in range(13)]

    write("pricing", {
        "skus": [{"name": n, "category": c, "price": p, "cost": co} for n, c, p, co, _, _ in skus],
        "categories": ["Poultry", "Ready meals", "Dairy & cheese", "Frozen veg & snacks"],
        "channels": channels, "competitors": competitors,
        "weeks": [d.strftime("%d %b %y") for d in weeks], "season": seas, "nextQuarterSeason": next_q,
        "rows": rows, "shareMonths": months, "share": share,
    })


# ---------------------------------------------------------------- distributor
def distributor():
    rng = random.Random(33)
    salesmen = ["Faisal", "Omar", "Yousef", "Imran", "Khalid", "Saeed", "Anwar", "Bilal"]
    channels = ["Baqala", "Mini-market", "Supermarket", "HoReCa"]
    areas = ["Jeddah North", "Jeddah South", "Makkah", "Taif"]
    skus = [
        "Chicken breast 1kg", "Whole chicken 1.1kg", "Chicken nuggets 750g",
        "Beef burger 20pc", "Chicken franks 400g", "French fries 2.5kg",
        "Mixed vegetables 900g", "Mozzarella 1kg", "Cheddar slices 200g",
        "Labneh 500g", "Basmati rice 5kg", "Sunflower oil 1.5L",
        "Tomato paste 400g", "Samosa pastry 40pc", "Spring rolls 20pc",
        "Chicken shawarma 1kg", "Fish fillet 800g", "Shrimp 500g",
        "Puff pastry 1kg", "Ice cream tub 2L",
    ]
    sku_dist = [0.81, 0.74, 0.58, 0.49, 0.66, 0.62, 0.44, 0.39, 0.33, 0.36,
                0.71, 0.69, 0.57, 0.41, 0.31, 0.27, 0.22, 0.14, 0.19, 0.24]
    prefixes = {
        "Baqala": ["Baqala", "Baqala", "Tamween"],
        "Mini-market": ["Mini Market", "Mart", "Corner Market"],
        "Supermarket": ["Supermarket", "Hyper", "Markets"],
        "HoReCa": ["Restaurant", "Café", "Kitchen", "Catering"],
    }
    words = ["Al Noor", "Al Salam", "Al Rayan", "Al Madina", "Al Sharq", "Al Faisal",
             "Al Hamra", "Al Safa", "Al Marwa", "Al Nakheel", "Al Andalus", "Al Bustan",
             "Al Yasmin", "Al Khaleej", "Al Fayha", "Al Zahra", "Al Riyadh", "Al Shifa",
             "Al Rabie", "Al Jawhara", "Al Hayat", "Al Masa", "Al Diyafa", "Al Barakah",
             "Al Qamar", "Al Wurud", "Al Murjan", "Al Thuraya", "Al Ward", "Al Aseel"]
    ch_w = [0.45, 0.25, 0.12, 0.18]
    ch_size = [9_000, 22_000, 85_000, 30_000]

    customers = []
    used = set()
    for i in range(320):
        ch = rng.choices(range(4), ch_w)[0]
        while True:
            name = f"{rng.choice(prefixes[channels[ch]])} {rng.choice(words)}"
            if rng.random() < 0.3:
                name += f" {rng.randint(2, 9)}"
            if name not in used:
                used.add(name)
                break
        sales6m = ch_size[ch] * 6 * rng.lognormvariate(0, 0.55)
        n_skus = max(2, min(19, round(rng.gauss(7 + 3 * ch, 3))))
        bought = set(rng.sample(range(len(skus)), n_skus))
        # Segment: loyal accounts to protect, or growth accounts to win
        loyal = sales6m > ch_size[ch] * 6 * 1.1 and rng.random() < 0.75
        score = min(0.97, max(0.05, rng.betavariate(5, 2) if loyal else rng.betavariate(2, 3.2)))
        missing = [s for s in range(len(skus)) if s not in bought]
        missing.sort(key=lambda s: -sku_dist[s] * rng.uniform(0.6, 1.4))
        recs = missing[:3]
        monthly = sales6m / 6
        opp = monthly * (0.18 if loyal else 0.32) * score * rng.uniform(0.7, 1.3)
        customers.append({
            "id": f"C{1000 + i}",
            "name": name,
            "salesman": rng.randrange(len(salesmen)),
            "channel": ch,
            "area": rng.randrange(len(areas)),
            "sales6m": round(sales6m),
            "skus": n_skus,
            "score": round(score, 2),
            "action": "Protect" if loyal else "Win",
            "opportunity": round(opp, -1),
            "recs": recs,
            "lastVisit": rng.randint(2, 45) if not loyal else rng.randint(1, 14),
        })

    # Model check from last month: predicted vs actual buy rate by score band
    calibration = []
    for d in range(10):
        pred = 0.05 + d * 0.093
        actual = min(0.98, max(0.01, pred + rng.uniform(-0.05, 0.05)))
        calibration.append({"band": f"{d * 10}–{d * 10 + 10}", "predicted": round(pred * 100, 1),
                            "actual": round(actual * 100, 1)})

    promos = [
        ("Buy 10 nuggets, get 1 free", "Jan 26", 38_000, 61_000),
        ("Ramadan family bundle", "Feb–Mar 26", 92_000, 214_000),
        ("Fries 2+1 HoReCa", "Apr 26", 21_000, 17_500),
        ("Mozzarella shelf rental", "May 26", 45_000, 31_000),
        ("Summer ice cream display", "Jul 26", 30_000, 52_000),
        ("National Day 15% off franks", "Sep 26", 26_000, 34_000),
    ]
    promo_rows = [{"name": n, "period": p, "spend": s, "incGP": g,
                   "roi": round((g - s) / s * 100)} for n, p, s, g in promos]

    write("distributor", {
        "salesmen": salesmen,
        "channels": channels,
        "areas": areas,
        "skus": skus,
        "skuDistribution": sku_dist,
        "customers": customers,
        "calibration": calibration,
        "hitRate": {"flagged": 65, "notFlagged": 21},
        "promos": promo_rows,
    })


# --------------------------------------------------------------------- clinic
def finance():
    rng = random.Random(55)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    actual_months = 9
    season = [0.94, 0.97, 0.9, 1.0, 1.04, 0.98, 0.93, 0.96, 1.06, 1.1, 1.08, 1.04]
    budget_rev = [2_050_000 * s * (1 + 0.004 * i) for i, s in enumerate(season)]

    lines = {
        # name, kind, budget as % of revenue (or fixed SAR per month), actual drift
        "Revenue": ("revenue", None, None),
        "Cost of goods sold": ("cogs", 0.755, 0.004),
        "Salaries": ("opex", 180_000, 0.0),
        "Rent & utilities": ("opex", 62_000, 0.01),
        "Logistics & fuel": ("opex", 0.034, 0.19),
        "Marketing": ("opex", 0.012, -0.12),
        "General & admin": ("opex", 48_000, 0.04),
    }
    data = {k: {"budget": [], "actual": []} for k in lines}
    for i in range(12):
        b_rev = budget_rev[i]
        a_rev = b_rev * (1.04 + rng.uniform(-0.035, 0.035)) if i < actual_months else None
        data["Revenue"]["budget"].append(round(b_rev))
        data["Revenue"]["actual"].append(round(a_rev) if a_rev else None)
        for name, (kind, basis, drift) in lines.items():
            if kind == "revenue":
                continue
            budget = b_rev * basis if basis < 1 else basis
            data[name]["budget"].append(round(budget))
            if a_rev is None:
                data[name]["actual"].append(None)
                continue
            if basis < 1:
                actual = a_rev * basis * (1 + drift) * noise(rng, 0.02)
            else:
                actual = budget * (1 + drift) * noise(rng, 0.02)
            data[name]["actual"].append(round(actual))

    # 13-week cash forecast from 1 Oct
    start = date(2026, 10, 4)
    weeks = [(start + timedelta(weeks=i)).strftime("%d %b") for i in range(13)]
    cash = 1_480_000
    cash_rows = []
    for i in range(13):
        inflow = 530_000 * noise(rng, 0.06)
        if i in (6, 7, 8):
            inflow *= 0.5  # three large customers paying late
        if i == 10:
            inflow *= 1.6  # catch-up after collections push
        outflow = 455_000 * noise(rng, 0.05)
        if i in (4, 8, 12):
            outflow += 310_000  # supplier payment runs
        if i == 7:
            outflow += 120_000  # quarterly VAT
        cash = cash + inflow - outflow
        cash_rows.append({"week": weeks[i], "inflow": round(inflow), "outflow": round(outflow),
                          "closing": round(cash)})

    customers = [
        ("Marjan Hypermarkets", [180, 210, 160, 340]),
        ("Red Sea Restaurants Group", [220, 140, 90, 0]),
        ("Masar Supermarkets", [95, 160, 175, 210]),
        ("Al Jazeera Markets", [260, 80, 20, 0]),
        ("Najd Catering Co.", [140, 110, 60, 95]),
        ("Tihama Mini Marts", [120, 70, 40, 0]),
        ("Gulf Hotels Group", [80, 65, 55, 120]),
        ("Al Safwa Trading", [110, 40, 0, 0]),
    ]
    aging = [{"customer": c, "buckets": [v * 1000 for v in b]} for c, b in customers]

    write("finance", {
        "months": months,
        "actualMonths": actual_months,
        "lines": data,
        "cashWeeks": cash_rows,
        "minCash": 750_000,
        "aging": aging,
        "agingBuckets": ["0–30 days", "31–60 days", "61–90 days", "90+ days"],
        "dso": {"actual": 74, "target": 60},
    })


if __name__ == "__main__":
    sales_performance()
    key_accounts()
    demand_planning()
    pnl()
    pricing()
    distributor()
    finance()
