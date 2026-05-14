import { useEffect, type FC } from "react";
import { useLocation } from "react-router-dom";

interface SEOProps {
  title: string;
  description: string;
  path?: string;
  image?: string;
}

const DEFAULT_SITE_URL = "https://musab-portfolio.vercel.app";
const DEFAULT_IMAGE =
  "https://res.cloudinary.com/de75b0zis/image/upload/v1767276493/musab-img_dbulfo.png";

const getSiteUrl = () => {
  const envUrl = import.meta.env.VITE_SITE_URL;
  return (envUrl || DEFAULT_SITE_URL).replace(/\/$/, "");
};

const upsertMeta = (
  key: string,
  value: string,
  attr: "name" | "property" = "name",
) => {
  let tag = document.querySelector(`meta[${attr}='${key}']`);
  if (!tag) {
    tag = document.createElement("meta");
    tag.setAttribute(attr, key);
    document.head.appendChild(tag);
  }
  tag.setAttribute("content", value);
};

const SEO: FC<SEOProps> = ({ title, description, path, image }) => {
  const location = useLocation();

  useEffect(() => {
    const siteUrl = getSiteUrl();
    const finalPath = path ?? location.pathname;
    const canonicalUrl = `${siteUrl}${finalPath === "/" ? "" : finalPath}`;
    const finalImage = image || DEFAULT_IMAGE;

    document.title = `${title} | Musab Shaikh`;

    upsertMeta("description", description);
    upsertMeta("robots", "index, follow, max-image-preview:large");

    upsertMeta("og:type", "website", "property");
    upsertMeta("og:title", `${title} | Musab Shaikh`, "property");
    upsertMeta("og:description", description, "property");
    upsertMeta("og:url", canonicalUrl, "property");
    upsertMeta("og:image", finalImage, "property");

    upsertMeta("twitter:card", "summary_large_image");
    upsertMeta("twitter:title", `${title} | Musab Shaikh`);
    upsertMeta("twitter:description", description);
    upsertMeta("twitter:image", finalImage);

    let canonicalTag = document.querySelector("link[rel='canonical']");
    if (!canonicalTag) {
      canonicalTag = document.createElement("link");
      canonicalTag.setAttribute("rel", "canonical");
      document.head.appendChild(canonicalTag);
    }
    canonicalTag.setAttribute("href", canonicalUrl);

    const ldJsonId = "website-ld-json";
    let scriptTag = document.getElementById(
      ldJsonId,
    ) as HTMLScriptElement | null;
    if (!scriptTag) {
      scriptTag = document.createElement("script");
      scriptTag.id = ldJsonId;
      scriptTag.type = "application/ld+json";
      document.head.appendChild(scriptTag);
    }

    scriptTag.text = JSON.stringify({
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Person",
          name: "Musab Shaikh",
          jobTitle: "Software Engineer & Data Scientist",
          url: siteUrl,
          image: DEFAULT_IMAGE,
          sameAs: [
            "https://www.linkedin.com/in/musab-shaikh-2802/",
            "https://github.com/Musabs2802",
          ],
        },
        {
          "@type": "WebSite",
          name: "Musab Shaikh Portfolio",
          url: siteUrl,
        },
        {
          "@type": "WebPage",
          name: title,
          url: canonicalUrl,
          description,
        },
      ],
    });
  }, [title, description, path, image, location.pathname]);

  return null;
};

export default SEO;
