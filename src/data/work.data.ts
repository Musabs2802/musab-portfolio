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
    client: "Data Consulting Demo",
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
    client: "Data Consulting Demo",
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
    client: "Data Consulting Demo",
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
    client: "Data Consulting Demo",
    results:
      "24 promo events · 5 SKUs · Waterfall margin bridge · ROI optimizer with live spend reallocation sliders · Promo calendar heatmap · Mechanic benchmarking",
    demo: "/trade-promo-roi-dashboard.html",
  },
];

export default workData;
