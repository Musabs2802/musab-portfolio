interface FAQItem {
  id: number;
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    id: 1,
    question: "How much does a dashboard or app cost?",
    answer:
      "Excel trackers start at $250, Power BI dashboards at $750, and the monthly BI Partner retainer at $500. Mobile apps start at $4,000. After a free call I send a fixed quote, so the price won't change unless the scope does.",
  },
  {
    id: 2,
    question: "How long does it take?",
    answer:
      "An Excel tracker usually takes 3–5 days and a Power BI dashboard 1–2 weeks. A mobile app takes 6–10 weeks, depending on the number of screens and integrations. You see progress every week.",
  },
  {
    id: 3,
    question: "Will you sign an NDA, and how do you handle our data?",
    answer:
      "Yes, I'm happy to sign an NDA before we start. Where possible I work inside your own environment (your Power BI workspace, OneDrive or SharePoint), never share client data, and never reuse it for other work.",
  },
  {
    id: 4,
    question: "Do we need Power BI licences?",
    answer:
      "To share reports inside your organisation, each viewer usually needs a Power BI Pro licence from Microsoft, unless you have Premium or Fabric capacity. For small teams I'll recommend the cheapest setup that works, which is sometimes Excel.",
  },
  {
    id: 5,
    question: "What do you need from us to start?",
    answer:
      "A sample of your data (an Excel export is fine), the questions the dashboard should answer, and someone who can answer my questions. For apps: your idea, any designs or references, and your App Store / Google Play accounts (I can help you set them up).",
  },
  {
    id: 6,
    question: "How many revisions are included?",
    answer:
      "Dashboard builds include 2 rounds of revisions and trackers include 1. Weekly check-ins mean most feedback is handled while I'm building, so you rarely need more.",
  },
  {
    id: 7,
    question: "Do you publish the app to the App Store and Google Play?",
    answer:
      "Yes. I handle store listings, builds and the review process, and the app is published under your own developer accounts, so you own it fully.",
  },
  {
    id: 8,
    question: "When are you available?",
    answer:
      "I take on a limited number of projects at a time so each one gets proper attention. I'm based in Saudi Arabia (GMT+3), which overlaps well with the GCC, UK and Europe, and I usually reply within 24 hours.",
  },
];

export default faqs;
