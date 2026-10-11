// Server entry used only at build time by scripts/prerender.mjs
import React from "react";
import { renderToString } from "react-dom/server";
import { StaticRouter } from "react-router-dom";
import App from "./App";
import { headTags, pages } from "./data/seo.data";

export const routes = Object.keys(pages);

export const render = (url: string) => ({
  head: headTags(url),
  html: renderToString(
    <React.StrictMode>
      <StaticRouter location={url}>
        <App />
      </StaticRouter>
    </React.StrictMode>,
  ),
});
