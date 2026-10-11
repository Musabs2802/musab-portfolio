// Page titles, descriptions and structured data. Used by the SEO component in
// the browser and by scripts/prerender.mjs to write each page's static <head>.
import site from "./site.data";
import faqs from "./faq.data";

export const SITE_URL = "https://musab-shaikh.vercel.app";
export const OG_IMAGE = `${SITE_URL}/og-image.png`;

export interface PageMeta {
  // Full text for the browser tab and search result headline
  title: string;
  description: string;
}

export const pages: Record<string, PageMeta> = {
  "/": {
    title: "Musab Shaikh | Data & AI Consultant",
    description:
      "Freelance data analyst in Jeddah. Power BI dashboards, sales forecasting, pricing analysis, reporting automation and Android & iOS apps for growing businesses in the GCC and worldwide.",
  },
  "/works": {
    title: "Case Studies & Sample Power BI Dashboards | Musab Shaikh",
    description:
      "Client case studies and interactive sample dashboards for commercial, finance and demand planning teams: sales vs target, detailed P&L, pricing and promotion simulator, demand and supply planning, key account profitability, sales targeting and cash flow.",
  },
  "/experience": {
    title: "Experience | Musab Shaikh, Commercial Data Analyst",
    description:
      "Commercial analytics experience: Power BI reporting for a $700M+ FMCG business across 13 countries, ML propensity modelling, sales target setting and reporting automation in the GCC.",
  },
  "/contact": {
    title: "Contact & Get a Quote | Musab Shaikh",
    description:
      "Book a free 20-minute call or message Musab Shaikh about a Power BI dashboard, Excel tracker, forecasting, reporting automation or mobile app project. Replies within 24 hours.",
  },
};

export const getPageMeta = (path: string): PageMeta =>
  pages[path] ?? pages["/"];

export const canonicalUrl = (path: string) =>
  `${SITE_URL}${path === "/" ? "/" : path}`;

export const structuredData = (path: string) => {
  const meta = getPageMeta(path);
  const graph: Record<string, unknown>[] = [
    {
      "@type": "Person",
      "@id": `${SITE_URL}/#person`,
      name: site.name,
      jobTitle: "Power BI Consultant & Data Analyst",
      url: `${SITE_URL}/`,
      image: site.avatar,
      email: site.email,
      address: {
        "@type": "PostalAddress",
        addressLocality: "Jeddah",
        addressCountry: "SA",
      },
      knowsAbout: [
        "Power BI",
        "DAX",
        "Excel",
        "SQL",
        "Python",
        "Sales forecasting",
        "Price elasticity",
        "Machine learning",
        "Flutter",
      ],
      sameAs: [site.linkedin, site.github],
    },
    {
      "@type": "ProfessionalService",
      "@id": `${SITE_URL}/#service`,
      name: "Musab Shaikh – Analytics & App Development",
      url: `${SITE_URL}/`,
      image: OG_IMAGE,
      email: site.email,
      telephone: site.phone,
      founder: { "@id": `${SITE_URL}/#person` },
      address: {
        "@type": "PostalAddress",
        addressLocality: "Jeddah",
        addressCountry: "SA",
      },
      areaServed: ["SA", "AE", "KW", "QA", "BH", "OM", "GB", "CH", "Worldwide"],
      hasOfferCatalog: {
        "@type": "OfferCatalog",
        name: "Services",
        itemListElement: [
          "Power BI dashboard development",
          "Excel trackers and data models",
          "Sales forecasting and pricing analysis",
          "Reporting automation",
          "Machine learning models",
          "Android and iOS app development",
        ].map((name) => ({
          "@type": "Offer",
          itemOffered: { "@type": "Service", name },
        })),
      },
    },
    {
      "@type": "WebSite",
      "@id": `${SITE_URL}/#website`,
      name: site.name,
      url: `${SITE_URL}/`,
    },
    {
      "@type": "WebPage",
      name: meta.title,
      url: canonicalUrl(path),
      description: meta.description,
      isPartOf: { "@id": `${SITE_URL}/#website` },
      about: { "@id": `${SITE_URL}/#person` },
    },
  ];

  if (path === "/") {
    graph.push({
      "@type": "FAQPage",
      mainEntity: faqs.map((f) => ({
        "@type": "Question",
        name: f.question,
        acceptedAnswer: { "@type": "Answer", text: f.answer },
      })),
    });
  }

  return { "@context": "https://schema.org", "@graph": graph };
};

const escapeAttr = (value: string) =>
  value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

// The SEO tags for a page, as HTML, for the prerendered <head>
export const headTags = (path: string) => {
  const { title, description } = getPageMeta(path);
  const url = canonicalUrl(path);
  const t = escapeAttr(title);
  const d = escapeAttr(description);
  const json = JSON.stringify(structuredData(path)).replace(/</g, "\\u003c");

  return [
    `<title>${t}</title>`,
    `<meta name="description" content="${d}" />`,
    `<link rel="canonical" href="${url}" />`,
    `<meta property="og:type" content="website" />`,
    `<meta property="og:site_name" content="Musab Shaikh" />`,
    `<meta property="og:locale" content="en_US" />`,
    `<meta property="og:title" content="${t}" />`,
    `<meta property="og:description" content="${d}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:image" content="${OG_IMAGE}" />`,
    `<meta property="og:image:width" content="1200" />`,
    `<meta property="og:image:height" content="630" />`,
    `<meta property="og:image:alt" content="Musab Shaikh, Power BI consultant and data analyst" />`,
    `<meta name="twitter:card" content="summary_large_image" />`,
    `<meta name="twitter:title" content="${t}" />`,
    `<meta name="twitter:description" content="${d}" />`,
    `<meta name="twitter:image" content="${OG_IMAGE}" />`,
    `<script type="application/ld+json" id="ld-json">${json}</script>`,
  ].join("\n    ");
};
