import React, { useEffect, useState } from "react";
import workData from "../data/work.data";
import SEO from "../components/SEO";

type Category = "All" | "Dashboard" | "Data Science" | "Analysis" | "Software";

const categoryStyle: Record<string, string> = {
  Dashboard: "bg-blue-50 text-blue-700",
  "Data Science":
    "bg-violet-50 text-violet-700",
  Analysis:
    "bg-amber-50 text-amber-700",
  Software:
    "bg-emerald-50 text-emerald-700",
};

const getDemoUrl = (demo: string) => {
  if (/^(https?:)?\/\//.test(demo)) {
    return demo;
  }

  const normalizedPath = demo.replace(/^\/+/, "");
  return `${import.meta.env.BASE_URL}${normalizedPath}`;
};

const Work: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState<Category>("All");

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const categories = [
    "All",
    ...Array.from(new Set(workData.map((w) => w.category))),
  ] as Category[];

  const filtered =
    activeCategory === "All"
      ? workData
      : workData.filter((w) => w.category === activeCategory);

  const CardContent = ({ project }: { project: (typeof workData)[0] }) => (
    <>
      <div className="relative aspect-[16/9] overflow-hidden bg-neutral-100">
        <img
          src={project.image}
          alt={project.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
        />
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/35 transition-all duration-300 flex items-center justify-center">
          <span className="opacity-0 group-hover:opacity-100 translate-y-1 group-hover:translate-y-0 transition-all duration-300 text-white text-sm font-semibold bg-black/55 backdrop-blur-sm px-5 py-2.5 rounded-full flex items-center gap-2">
            Open Dashboard
            <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
              <path
                d="M2 11L11 2M11 2H5M11 2V8"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>
        </div>
      </div>
      <div className="p-5">
        <div className="flex items-start justify-between gap-3 mb-2">
          <h2 className="text-lg font-bold text-neutral-900 leading-snug">
            {project.title}
          </h2>
          <span
            className={`shrink-0 mt-0.5 px-2 py-0.5 rounded text-xs font-semibold ${
              categoryStyle[project.category] ??
              "bg-neutral-100 text-neutral-600"
            }`}
          >
            {project.category}
          </span>
        </div>
        <p className="text-neutral-500 text-sm leading-relaxed mb-4 line-clamp-2">
          {project.description}
        </p>
        <div className="flex flex-wrap gap-1.5 mb-4">
          {project.technologies.map((tech, i) => (
            <span
              key={i}
              className="px-2.5 py-1 bg-neutral-100 text-neutral-600 text-xs rounded font-medium"
            >
              {tech}
            </span>
          ))}
        </div>
        <div className="flex items-center justify-between border-t border-neutral-100 pt-3.5">
          <span className="text-xs text-neutral-400">{project.client}</span>
          <span className="text-sm font-semibold text-neutral-800 flex items-center gap-1">
            View{" "}
            <span className="group-hover:translate-x-0.5 transition-transform inline-block">
              →
            </span>
          </span>
        </div>
      </div>
    </>
  );

  return (
    <section className="min-h-screen bg-[#f8f6f3] px-6 pt-28 pb-20">
      <SEO
        title="Work & Sample Dashboards"
        description="Client case studies and interactive sample dashboards by Musab Shaikh: P&L, sales, price elasticity, trade promotion ROI, forecasting, distribution and more."
        path="/works"
      />
      <div className="max-w-7xl mx-auto">
        <div className="mb-10">
          <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-neutral-400 mb-3">
            Portfolio
          </p>
          <div className="flex items-end justify-between gap-4 flex-wrap">
            <div>
              <h1 className="text-5xl font-bold text-neutral-900 leading-none">
                Work
              </h1>
              <p className="mt-3 text-neutral-500 text-base max-w-md">
                Live, interactive data consulting deliverables — built to
                production standard.
              </p>
            </div>
            <p className="text-sm text-neutral-400 pb-1">
              {filtered.length} project{filtered.length !== 1 ? "s" : ""}
            </p>
          </div>
          <div className="flex flex-wrap gap-2 mt-7">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all duration-200 ${
                  activeCategory === cat
                    ? "bg-neutral-900 text-white border-neutral-900"
                    : "bg-transparent text-neutral-500 border-neutral-200 hover:border-neutral-400"
                }`}
              >
                {cat === "All" ? "All Projects" : cat}
              </button>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((project) =>
            project.demo ? (
              <a
                key={project.id}
                href={getDemoUrl(project.demo)}
                target="_blank"
                rel="noopener noreferrer"
                className="group block bg-white rounded-2xl overflow-hidden border border-neutral-200 hover:border-neutral-300 hover:shadow-[0_8px_32px_rgba(0,0,0,0.09)] transition-all duration-300 cursor-pointer"
              >
                <CardContent project={project} />
              </a>
            ) : (
              <div
                key={project.id}
                className="group bg-white rounded-2xl overflow-hidden border border-neutral-200"
              >
                <CardContent project={project} />
              </div>
            ),
          )}
        </div>
      </div>
    </section>
  );
};

export default Work;
