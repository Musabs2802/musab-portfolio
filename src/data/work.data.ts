import { Work } from "../types";

const workData: Work[] = [
  {
    id: 1,
    title: "P&L Dashboard",
    description:
      "5-year expandable Profit & Loss dashboard for FMCG. Drill from annual summary to quarterly and monthly detail. Includes full income statement waterfall, margin trend charts, YoY variance analysis, and dynamic filters by Business Unit, Region, and Channel.",
    image:
      "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "Covers Revenue → Gross Profit → EBITDA → EBIT → Net Income with live filter slicing, SVG charts, CSV export, and USD/thousands or millions toggle",
    demo: "/pl-dashboard.html",
  },
  {
    id: 2,
    title: "Salesman Action Dashboard",
    description:
      "Customer-level sales action dashboard for FMCG field teams. Categorises customers into Battles (acquire) and Hold Position (retain) using a propensity-style scoring model. Includes SKU portfolio drill-down, 6-month completion trend charts, and regional performance summaries.",
    image:
      "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "Covers 6 salesmen × 50 customers × 6 months with Revenue / Qty / Tonnage metrics, searchable salesman filter, completion flags, and CSV export",
    demo: "/salesman-action-dashboard.html",
  },
  {
    id: 3,
    title: "Price Elasticity Dashboard",
    description:
      "Commercial price elasticity analysis for a 5-SKU FMCG portfolio vs 6 competitor SKUs. Own-price elasticity, cross-price substitution matrix, competitive positioning map, and an interactive price simulator that computes revenue/volume/GP impact with cross-elasticity effects auto-applied.",
    image:
      "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "Covers elasticity analysis, 5×5 cross-elasticity matrix, cannibalisation heatmap, price-response curves, revenue optimisation curves, and a live price simulator with waterfall impact chart",
    demo: "/price-elasticity-dashboard.html",
  },
  {
    id: 4,
    title: "Trade Promotion ROI Dashboard",
    description:
      "Full-year trade promotion ROI analysis for a 5-SKU FMCG portfolio across 4 promo mechanics (TPR, Display, Feature, Bundle). Tracks spend vs incremental revenue, gross profit uplift, net ROI per event, and volume uplift %. Includes a promo calendar heatmap, mechanic benchmarking, margin waterfall bridge, and an interactive budget optimizer.",
    image:
      "https://images.unsplash.com/photo-1543286386-713bdd548da4?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "24 promo events · 5 SKUs · Waterfall margin bridge · ROI optimizer with live spend reallocation sliders · Promo calendar heatmap · Mechanic benchmarking",
    demo: "/trade-promo-roi-dashboard.html",
  },
  {
    id: 5,
    title: "Demand Forecasting Dashboard",
    description:
      "24-month demand history (Jan 2024 – Dec 2025) for a 5-SKU FMCG portfolio with 3-month forward forecasts using a Trend × Seasonality model. Compares Naïve, Moving Average, and Trend methods. Includes accuracy metrics (MAPE, MAE, RMSE, Bias), residual diagnostics, and an interactive Scenario Planner with per-SKU growth multiplier sliders.",
    image:
      "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "5 SKUs · 24-month actuals · 3-month forecast · MAPE / MAE / RMSE accuracy panel · Residual scatter · Method comparison · Scenario planner with live volume reforecast",
    demo: "/demand-forecasting-dashboard.html",
  },
  {
    id: 6,
    title: "Distribution & SKU Availability Dashboard",
    description:
      "End-to-end distribution intelligence for a 5-SKU FMCG portfolio across 6 channels and 120 outlets. Tracks Numeric Distribution (ND%), Weighted Distribution (WD%), Out-of-Stock rates, and SKU range compliance over 6 rolling months. Includes per-channel and per-SKU drill-downs, an OOS heatmap, and a Gap Analyser showing uncovered outlets vs target.",
    image:
      "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "5 SKUs · 6 channels · 120 outlets · ND% / WD% / OOS% metrics · SKU × Channel heatmaps · Coverage score vs target · Gap analyser with outlet-level breakdown",
    demo: "/distribution-dashboard.html",
  },
  {
    id: 7,
    title: "Customer Profitability Dashboard",
    description:
      "Full customer-level P&L for a 30-customer FMCG portfolio across 4 channels. Tracks Revenue, COGS, Gross Profit, Trade Spend, Logistics, and Net Contribution Margin per customer over 6 rolling months. Includes a revenue vs CM% scatter plot, customer tier classification (A/B/C), per-customer P&L waterfall with SKU mix donut, channel benchmarking, and a Pareto 80/20 analysis.",
    image:
      "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "30 customers · 4 channels · Revenue / GP / Trade / Logistics / Net CM waterfall · Tier A/B/C classification · Pareto cumulative curves · Channel cost structure breakdown",
    demo: "/customer-profitability-dashboard.html",
  },
  {
    id: 8,
    title: "Market Share & Competitive Tracker",
    description:
      "Competitive intelligence dashboard tracking ProClean vs 4 rivals (BrightClean, EcoWash, CleanPro, ZipClean) across 5 FMCG categories and 4 channels over 6 rolling months. Covers Volume Share %, Value Share %, Numeric Distribution %, and Share of Shelf %. Includes category drill-downs, channel benchmarking, head-to-head brand comparisons, and a share movement heatmap showing gains/losses vs prior period.",
    image:
      "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
    technologies: ["Python", "HTML", "CSS", "JavaScript", "Data Viz"],
    category: "Dashboard",
    client: "Data Consulting",
    results:
      "5 brands · 5 categories · 4 channels · Volume & Value share trends · Distribution & shelf share · Head-to-head comparison · Share movement heatmap · Category rank tracker",
    demo: "/market-share-tracker.html",
  },
];

export default workData;
