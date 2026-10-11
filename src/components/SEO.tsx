import { useEffect, type FC } from "react";
import { useLocation } from "react-router-dom";
import {
  OG_IMAGE,
  canonicalUrl,
  getPageMeta,
  structuredData,
} from "../data/seo.data";

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

// Keeps the <head> in sync on client-side navigation. The first load already
// has these tags in the HTML, written by scripts/prerender.mjs.
const SEO: FC = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    const { title, description } = getPageMeta(pathname);
    const url = canonicalUrl(pathname);

    document.title = title;
    upsertMeta("description", description);
    upsertMeta("og:title", title, "property");
    upsertMeta("og:description", description, "property");
    upsertMeta("og:url", url, "property");
    upsertMeta("og:image", OG_IMAGE, "property");
    upsertMeta("twitter:title", title);
    upsertMeta("twitter:description", description);

    let canonical = document.querySelector("link[rel='canonical']");
    if (!canonical) {
      canonical = document.createElement("link");
      canonical.setAttribute("rel", "canonical");
      document.head.appendChild(canonical);
    }
    canonical.setAttribute("href", url);

    let ldJson = document.getElementById("ld-json") as HTMLScriptElement | null;
    if (!ldJson) {
      ldJson = document.createElement("script");
      ldJson.id = "ld-json";
      ldJson.type = "application/ld+json";
      document.head.appendChild(ldJson);
    }
    ldJson.text = JSON.stringify(structuredData(pathname));
  }, [pathname]);

  return null;
};

export default SEO;
