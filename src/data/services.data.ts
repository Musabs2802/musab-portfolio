export interface Service {
  id: string;
  title: string;
  tagline: string;
  description: string;
  deliverables: string[];
  tools: string[];
  cta: string;
}

const services: Service[] = [
  {
    id: "analytics",
    title: "Analytics & Business Intelligence",
    tagline: "Power BI · Excel · Reporting automation",
    description:
      "Dashboards and trackers your team will actually open every morning, built by someone who runs daily reporting for 250+ users, from the CEO to field sales.",
    deliverables: [
      "Power BI dashboards and semantic models",
      "Excel trackers, templates and data models",
      "Automated daily and weekly reporting (Power Automate, Python)",
      "KPI design, sales targets and incentive tracking",
      "Sales, pricing, distribution and forecasting analysis",
    ],
    tools: ["Power BI", "DAX", "Power Query", "Excel", "SQL", "Python"],
    cta: "Discuss a dashboard",
  },
  {
    id: "apps",
    title: "Mobile App Development",
    tagline: "Android & iOS from one codebase",
    description:
      "Production apps for startups and organisations, from first screens to App Store and Google Play release, with live apps in the UK and Switzerland.",
    deliverables: [
      "Cross-platform Android & iOS apps (Flutter)",
      "UI/UX design and clickable prototypes",
      "Backend, authentication and admin panels",
      "App Store and Google Play publishing",
      "Post-launch maintenance and new features",
    ],
    tools: ["Flutter", "Dart", "Firebase", "REST APIs", "Android", "iOS"],
    cta: "Discuss an app",
  },
];

export interface Package {
  name: string;
  summary: string;
  includes: string[];
  timeline: string;
  featured?: boolean;
}

// Engagement types; quotes depend on scope (data sources, pages, screens)
export const packages: Package[] = [
  {
    name: "Excel Tracker",
    summary:
      "A ready-to-use tracker or template with formulas, validation and a summary dashboard.",
    includes: [
      "Requirements call",
      "Structured data entry sheets",
      "Summary dashboard with charts",
      "1 round of revisions",
      "Short how-to video",
    ],
    timeline: "3–5 days",
  },
  {
    name: "Dashboard Build",
    summary:
      "A Power BI report built on your data, from data model to published dashboard.",
    includes: [
      "Requirements and KPI workshop",
      "Data model and DAX measures",
      "Up to 3 report pages",
      "2 rounds of revisions",
      "Handover session and 2 weeks of support",
    ],
    timeline: "1–2 weeks",
  },
  {
    name: "BI Partner",
    summary:
      "Your part-time BI analyst: keep reports running and keep improving them.",
    includes: [
      "Up to 10 hours a month",
      "Report maintenance and refresh fixes",
      "New visuals, measures and pages",
      "Monthly insights summary",
      "Priority WhatsApp support",
    ],
    timeline: "Month to month",
    featured: true,
  },
  {
    name: "Mobile App",
    summary:
      "An Android and iOS app, designed, built and published to both stores.",
    includes: [
      "Scope and screen design",
      "Flutter app for Android & iOS",
      "Backend and admin panel",
      "Store submission and release",
      "30 days of post-launch support",
    ],
    timeline: "6–10 weeks",
  },
];

export const process = [
  {
    step: "01",
    title: "Free discovery call",
    text: "20 minutes to understand your business, your data and what decision the work needs to support.",
  },
  {
    step: "02",
    title: "Fixed proposal",
    text: "A written scope with deliverables, timeline and a fixed price, so there are no surprises.",
  },
  {
    step: "03",
    title: "Build & weekly check-ins",
    text: "You see progress every week and give feedback early, not just at the end.",
  },
  {
    step: "04",
    title: "Handover & support",
    text: "Documentation, a walkthrough for your team, and support after delivery.",
  },
];

export default services;
