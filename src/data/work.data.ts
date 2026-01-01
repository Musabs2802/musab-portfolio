import { Work } from "../types";

const workData: Work[] = [
  {
    id: 1,
    title: "Sales Analytics Dashboard",
    description:
      "Designed and developed an advanced sales analytics dashboard using Power BI and complex DAX, delivering Coca-Cola–style sales intelligence for managers, supervisors, and leadership.",
    image:
      "https://res.cloudinary.com/de75b0zis/image/upload/v1753605143/sales-dashboard-work-scr_n5uiqc.jpg",
    technologies: ["PowerBi", "SQL", "Excel"],
    category: "Analysis",
    client: "Seara | KSA",
    results:
      "Enabled data-driven decision-making across all sales tiers; improved visibility into KPIs and sales trends, reducing reporting turnaround time by 80%",
  },
  {
    id: 2,
    title: "Customer Propensity Model",
    description:
      "Built a machine learning customer propensity model using historical sales data to predict SKU-level purchase likelihood for the following month.",
    image:
      "https://res.cloudinary.com/de75b0zis/image/upload/v1753605143/customer-propensity-work-scr_oy1opg.jpg",
    technologies: ["Python", "Machine Learning", "AWS"],
    category: "Data Science",
    client: "Seara | KSA",
    results:
      "Achieved ~65% prediction accuracy, enabling targeted sales campaigns and contributing to a 20% lift in monthly SKU-level sales",
  },
  {
    id: 3,
    title: "MBVS Networking App",
    description:
      "Designed and developed a cross-platform mobile application enabling professionals in Switzerland to network, discover services, attend events, and apply for jobs from a single platform.",
    image:
      "https://res.cloudinary.com/de75b0zis/image/upload/v1753605143/mbvs-networking-work-src_fdn4hj.png",
    technologies: ["Flutter", "iOS", "Android"],
    category: "Software",
    client: "MBVS | Switzerland",
    results:
      "Adopted by Swiss professional communities; recognized for consolidating networking, services, and job discovery into a single mobile platform",
  },
  {
    id: 4,
    title: "Automation System at Al Kabeer Group",
    description:
      "Designed and implemented Python-based automation for sales and finance workflows at Al Kabeer Group, replacing manual reporting and enabling faster, data-driven decision-making.",
    image:
      "https://res.cloudinary.com/de75b0zis/image/upload/v1753605143/al-kabeer-work-scr_k0fvva.png",
    technologies: ["Python", "Excel", "Cloud"],
    category: "Software",
    client: "Al Kabeer Group | UAE",
    results:
      "Saved 200+ man-hours monthly by automating reporting, improving accuracy and enabling real-time sales insights for faster executive decisions",
  },
  {
    id: 5,
    title: "Bubble Care Health Tech App",
    description:
      "Built a healthcare mobile application connecting patients and caregivers for daily activity tracking and care coordination, developed for a UK health-tech startup working alongside NHS stakeholders.",
    image:
      "https://res.cloudinary.com/de75b0zis/image/upload/v1753605143/tritone-health-work-scr_hwauzt.png",
    technologies: ["Android", "iOS", "Kotlin", "Swift"],
    category: "Software",
    client: "Tritone Health | UK",
    results:
      "Improved daily activity tracking and communication between patients and caregivers; validated through pilot usage with healthcare stakeholders",
  },
];

export default workData;
