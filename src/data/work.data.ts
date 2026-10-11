import { Work } from "../types";

// Sample dashboards in public/dashboards/, aimed at commercial, finance and
// demand planning teams. Data comes from scripts/dashboards/generate_data.py
// and is fictional.
const workData: Work[] = [
  {
    id: 1,
    title: "Sales vs target",
    description:
      "The daily commercial report: sales against target by region, channel, category and salesman, growth vs last year, and whether this month will land at the current run rate.",
    image: "/thumbnails/sales-performance.webp",
    technologies: ["Target tracking", "Run-rate projection", "Salesman tracker"],
    category: "Dashboard",
    client: "Commercial · sample with fictional data",
    results: "Shows where the year's gap comes from and what each salesman needs per day",
    demo: "/dashboards/sales-performance.html",
  },
  {
    id: 6,
    title: "Detailed P&L",
    description:
      "The month-end income statement from gross sales to net profit, expandable to raw materials, freight and advertising, against budget and last year, with a gross margin bridge and cost structure by category.",
    image: "/thumbnails/pnl.webp",
    technologies: ["Income statement", "Budget vs actual", "Margin bridge"],
    category: "Dashboard",
    client: "Finance · sample with fictional data",
    results: "Shows that raw material inflation, not sales, is why profit missed budget",
    demo: "/dashboards/pnl.html",
  },
  {
    id: 7,
    title: "Pricing & promotion simulator",
    description:
      "A what-if simulator for price changes and promotions built on price elasticity estimated from two years of weekly sales, plus competitor price index, market share and history by product and channel.",
    image: "/thumbnails/pricing-promotion.webp",
    technologies: ["Price elasticity", "Promo simulator", "Competitor index"],
    category: "Dashboard",
    client: "Commercial · sample with fictional data",
    results: "Tests a price or promo plan's profit impact before the budget is committed",
    demo: "/dashboards/pricing-promotion.html",
  },
  {
    id: 3,
    title: "Demand, stock and supply",
    description:
      "For the S&OP meeting: forecast accuracy and bias, projected stock by product and DC, expiry and stock-out risk, customer OTIF, production adherence, warehouse space and supplier performance.",
    image: "/thumbnails/demand-planning.webp",
    technologies: ["Forecast accuracy", "Stock projection", "OTIF & suppliers"],
    category: "Dashboard",
    client: "Demand & supply planning · sample with fictional data",
    results: "Shows that sales overrides reduce accuracy, and the stock at risk of expiry",
    demo: "/dashboards/demand-planning.html",
  },
  {
    id: 2,
    title: "Key account profitability",
    description:
      "What each retail account really earns: a price waterfall from gross sales to contribution, trade spend by term, a year-on-year profit bridge and promotion ROI.",
    image: "/thumbnails/key-account-profitability.webp",
    technologies: ["Price waterfall", "Trade spend", "Promo ROI"],
    category: "Dashboard",
    client: "Commercial finance · sample with fictional data",
    results: "Finds the biggest account earning the lowest margin before negotiations",
    demo: "/dashboards/key-account-profitability.html",
  },
  {
    id: 4,
    title: "Who to visit, and what to sell",
    description:
      "A machine learning model ranks which customers each salesman should visit this month and what to offer them, with a check of last month's accuracy, distribution gaps and promo ROI.",
    image: "/thumbnails/sales-distributor.webp",
    technologies: ["Propensity model", "Distribution gaps", "Promo ROI"],
    category: "Dashboard",
    client: "Commercial · sample with fictional data",
    results: "Ranks 320 customers by opportunity for the field team",
    demo: "/dashboards/sales-distributor.html",
  },
  {
    id: 5,
    title: "Budget and cash",
    description:
      "A food distributor's P&L against budget, cost variances, a 13-week cash forecast and receivables aging. Shows why the bank balance falls while sales beat the plan.",
    image: "/thumbnails/finance-cash.webp",
    technologies: ["P&L vs budget", "Cash forecast", "Receivables aging"],
    category: "Dashboard",
    client: "Finance · sample with fictional data",
    results: "Spots a cash shortfall eight weeks ahead and the customers causing it",
    demo: "/dashboards/finance-cash.html",
  },
];

export default workData;
