// Writes a static HTML file per route (dist/<route>/index.html) with the page's
// own <head> tags and rendered content, so search engines and link previews
// (LinkedIn, WhatsApp, X) see real content without running JavaScript.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dist = path.join(root, "dist");
const serverDir = path.join(root, "dist-server");

const { render, routes } = await import(
  pathToFileURL(path.join(serverDir, "entry-server.js")).href
);
const template = fs.readFileSync(path.join(dist, "index.html"), "utf8");

for (const route of routes) {
  const { head, html } = render(route);
  const page = template
    .replace(/<!--seo-->[\s\S]*?<!--\/seo-->/, head)
    .replace("<!--app-->", html);

  const file = path.join(dist, route === "/" ? "" : route, "index.html");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, page);
  console.log(`prerendered ${route}`);
}

fs.rmSync(serverDir, { recursive: true, force: true });
