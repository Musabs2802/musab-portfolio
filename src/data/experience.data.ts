import { Experience } from "../types";

const experienceData: Experience[] = [
  {
    title: "Sales Analyst III",
    company: "Seara (JBS)",
    location: "Jeddah, KSA",
    period: "Apr 2025 - Present",
    description: [
      "Own commercial BI for a $700M+ yearly revenue business across 13+ MENA countries, with 5+ automated Power BI reports used daily by 250+ users, including the CEO and CCO",
      "Built a customer-SKU propensity model (LightGBM, XGBoost, Random Forest) for KSA, the UAE and Kuwait that surfaces ~$590K a month in growth opportunities across 6,000+ customers; in KSA, 65% of flagged customers bought in the predicted month",
      "Guide area and channel managers with incentive and rebate programs that delivered 35% YoY sales growth and a 23% uplift against forecast for targeted product families",
      "Set sales targets for 250+ salesmen across 7 channels, cascaded to salesman, customer and SKU level, and oversee the customer distribution KPI that guides market coverage",
    ],
    technologies: ["Power BI", "DAX", "Power Automate", "Python", "SQL", "Excel"],
  },
  {
    title: "Data Analyst",
    company: "Al Kabeer Group of Companies",
    location: "Dubai, UAE",
    period: "Feb 2023 - Sep 2024",
    description: [
      "Cut daily sales reporting from 3 hours to 30 minutes (83%) by automating reporting pipelines in Python, giving senior management sales visibility at the start of each day",
      "Led the shift to automated reporting for 10+ area managers across 6 GCC countries by replacing manual country reports with scalable Excel data models",
    ],
    technologies: ["Python", "Excel", "Data Modeling"],
  },
];

export default experienceData;
