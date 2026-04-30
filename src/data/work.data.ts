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
];

export default workData;
