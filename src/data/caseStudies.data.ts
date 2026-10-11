import tritoneImage from "../assets/case-tritone.webp";
import mbvsImage from "../assets/case-mbvs.webp";

export interface CaseStudy {
  id: string;
  service: "Analytics" | "Mobile App";
  title: string;
  client: string;
  problem: string;
  built: string[];
  results: { value: string; label: string }[];
  tools: string[];
  visual:
    | { type: "image"; src: string; alt: string; caption?: string }
    | { type: "before-after"; before: string; after: string; unit: string };
  quote?: { text: string; author: string };
  link?: { label: string; href: string };
}

const caseStudies: CaseStudy[] = [
  {
    id: "propensity",
    service: "Analytics",
    title: "Customer-SKU propensity model",
    client: "JBS, the world's largest protein company · KSA, UAE & Kuwait",
    problem:
      "Distribution was thin and field sales were not reaching the right customers with the right products. Salesmen planned visits from habit, so growth opportunities went unnoticed.",
    built: [
      "An ensemble machine learning model (LightGBM, XGBoost, Random Forest) that predicts next-month purchase likelihood, volume and revenue for every customer-SKU pair",
      "~35,000 predictions a month in KSA alone, refreshed monthly since October 2025",
      "Customers split into loyal accounts to protect and growth accounts to win",
      "A Power BI action dashboard that gives 250+ salesmen their monthly target list",
    ],
    results: [
      { value: "~$590K", label: "a month in growth opportunities surfaced" },
      {
        value: "65%",
        label: "of flagged KSA customers bought in the predicted month",
      },
      { value: "6,000+", label: "customers scored, a 15% sales opportunity" },
    ],
    tools: ["Python", "LightGBM", "XGBoost", "Power BI"],
    visual: {
      type: "image",
      src: "/thumbnails/sales-distributor.webp",
      alt: "Sales dashboard listing which customers each salesman should visit and what to offer",
      caption: "Recreated with sample data. Client data stays confidential.",
    },
    link: {
      label: "Open the sample dashboard",
      href: "/dashboards/sales-distributor.html",
    },
  },
  {
    id: "reporting-automation",
    service: "Analytics",
    title: "Daily sales reporting automation",
    client: "Al Kabeer Group, a leading GCC frozen food maker · 6 countries",
    problem:
      "Daily sales reports were assembled by hand every morning. It took 3 hours, so senior management saw the numbers late, and each country's report looked different.",
    built: [
      "Python pipelines that pull, clean and consolidate daily sales data automatically",
      "Scalable Excel data models that replaced manual country reports",
      "One consistent reporting format for 10+ area managers across KSA, UAE, Kuwait, Qatar, Bahrain and Oman",
    ],
    results: [
      { value: "83%", label: "less time: 3 hours down to 30 minutes" },
      { value: "6", label: "GCC countries on one reporting standard" },
      {
        value: "10+",
        label: "area managers receiving reports at the start of each day",
      },
    ],
    tools: ["Python", "Pandas", "Excel", "Data Modeling"],
    visual: {
      type: "before-after",
      before: "3 hrs",
      after: "30 min",
      unit: "daily reporting time",
    },
    quote: {
      text: "In just four months, Musab streamlined and automated our accounting process, resulting in significant efficiency improvements.",
      author: "Al Kabeer Group, Dubai",
    },
  },
  {
    id: "tritone",
    service: "Mobile App",
    title: "Medii: health app for neurodivergent people",
    client:
      "Tritone Health, a UK health-tech startup working with the NHS · London",
    problem:
      "Tritone Health needed a simple, accessible app that helps neurodivergent and developmentally diverse people, and their carers, track their health and stay connected with their care team.",
    built: [
      "Cross-platform Android & iOS app",
      "Health tracking for mood, medicine and goals, plus a personal diary",
      "Gamified goals with rewards to keep users engaged",
      "A digital health passport and secure chat with care staff",
    ],
    results: [
      {
        value: "iOS + Android",
        label: "live on the App Store and Google Play",
      },
      { value: "1 codebase", label: "for both platforms" },
    ],
    tools: ["Flutter", "Dart", "Firebase", "REST APIs"],
    visual: {
      type: "image",
      src: tritoneImage,
      alt: "Medii app home screen showing goals, diary, medicine and mood",
    },
    quote: {
      text: "Musab was the best app developer we ever had.",
      author: "Naveed Iqbal, CEO, Tritone Health",
    },
    link: { label: "tritonehealth.com", href: "https://www.tritonehealth.com" },
  },
  {
    id: "mbvs",
    service: "Mobile App",
    title: "MBVS Hub: professional networking app",
    client: "MBVS, Switzerland's network of Muslim professionals · Zürich",
    problem:
      "Switzerland's association of Muslim professionals needed one place where members could find each other, discover events and share job and business opportunities.",
    built: [
      "Member directory searchable by company and role, with rich profiles",
      "Events in Zürich, Bern and Geneva with language tags and details",
      "Business listings and notification preferences",
      "Android & iOS apps published under the association's own accounts",
    ],
    results: [
      {
        value: "iOS + Android",
        label: "live on the App Store and Google Play",
      },
      { value: "3 cities", label: "of events in one app" },
    ],
    tools: ["Flutter", "Dart", "Firebase"],
    visual: {
      type: "image",
      src: mbvsImage,
      alt: "MBVS Hub app screens: member profile, member directory and events",
    },
    quote: {
      text: "Musab handled the requirements of our app very well, with timely delivery, top-quality work and great availability.",
      author: "MBVS, Zürich",
    },
    link: { label: "mbvs.ch", href: "https://mbvs.ch" },
  },
];

export default caseStudies;
