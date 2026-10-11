# Musab Shaikh — Portfolio

Freelance portfolio for Power BI dashboards, Excel trackers, reporting automation and Android & iOS apps. Live at [musab-shaikh.vercel.app](https://musab-shaikh.vercel.app).

## Stack

React 18, TypeScript, Vite, Tailwind CSS, React Router. Hosted on Vercel.

## Development

```bash
npm install
npm run dev      # local dev server
npm run build    # production build into dist/
npm run lint
```

## Where things live

- `src/data/` — all site copy that changes often: services, case studies, sample dashboards (`work.data.ts`), experience, testimonials, FAQ.
- `src/components/` — page sections; `src/pages/` — routed pages.
- `public/dashboards/` — the standalone sample dashboards. They share `dash.css` and `dash.js` (a small SVG chart kit with light and dark mode). Their fictional data comes from `scripts/dashboards/generate_data.py`; run `python3 scripts/dashboards/generate_data.py` after changing it.
- `public/thumbnails/` — card screenshots of those dashboards.
