import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, ArrowUpRight, Info } from "lucide-react";
import workData from "../data/work.data";
import caseStudies from "../data/caseStudies.data";
import SEO from "../components/SEO";
import { getDemoUrl } from "../utils/demoUrl";

const Work: React.FC = () => {
  return (
    <main className="min-h-screen bg-sand-100 pt-32 pb-24">
      <SEO
        title="Work & Sample Dashboards"
        description="Client case studies and interactive sample dashboards by Musab Shaikh: P&L, sales, price elasticity, trade promotion ROI, forecasting, distribution and more."
        path="/works"
      />
      <div className="container-page">
        <header className="max-w-2xl mb-14">
          <p className="eyebrow mb-3">Work</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-ink leading-tight">
            Sample dashboards
          </h1>
          <p className="mt-4 text-neutral-600 text-lg leading-relaxed">
            Interactive dashboards covering the questions commercial teams ask
            most. Open any of them and click around: filters, drill-downs and
            simulators all work.
          </p>
          <p className="mt-5 flex gap-2.5 rounded-xl bg-white border border-sand-300 px-4 py-3 text-sm text-neutral-600">
            <Info size={18} className="shrink-0 text-brand-600 mt-0.5" />
            All data here is fictional. For clients I build the same views in
            Power BI or Excel, on your own data.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {workData.map((project) => (
            <a
              key={project.id}
              href={project.demo ? getDemoUrl(project.demo) : undefined}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex flex-col rounded-2xl overflow-hidden border border-sand-300 bg-white hover:border-brand-300 hover:shadow-[0_16px_40px_-20px_rgba(15,61,62,0.35)] transition-all"
            >
              <div className="relative aspect-[16/10] overflow-hidden bg-sand-200 border-b border-sand-200">
                <img
                  src={project.image}
                  alt={`${project.title} screenshot`}
                  loading="lazy"
                  className="w-full h-full object-cover object-top group-hover:scale-[1.03] transition-transform duration-500"
                />
                <span className="absolute top-3 left-3 px-2 py-0.5 rounded-md bg-white/90 backdrop-blur text-[11px] font-semibold text-neutral-600">
                  Sample
                </span>
              </div>
              <div className="flex flex-col flex-1 p-5">
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h2 className="text-lg font-semibold text-ink leading-snug">
                    {project.title}
                  </h2>
                  <ArrowUpRight
                    size={18}
                    className="shrink-0 mt-1 text-neutral-400 group-hover:text-brand-700 transition-colors"
                  />
                </div>
                <p className="text-neutral-600 text-sm leading-relaxed mb-4 line-clamp-3">
                  {project.description}
                </p>
                <p className="mt-auto pt-4 border-t border-sand-200 text-sm font-medium text-brand-700">
                  Open interactive dashboard
                </p>
              </div>
            </a>
          ))}
        </div>

        {/* Client work */}
        <section className="mt-24">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
            <div>
              <p className="eyebrow mb-3">Client work</p>
              <h2 className="section-title">Case studies</h2>
            </div>
            <Link to="/#case-studies" className="btn-secondary self-start md:self-auto">
              Read all case studies <ArrowRight size={16} />
            </Link>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {caseStudies.map((study) => (
              <Link
                key={study.id}
                to="/#case-studies"
                className="rounded-2xl bg-white border border-sand-300 p-5 hover:border-brand-300 transition-colors"
              >
                <p className="text-xs font-semibold text-brand-700 mb-2">
                  {study.service}
                </p>
                <h3 className="font-semibold text-ink leading-snug mb-3">
                  {study.title}
                </h3>
                <p className="font-heading text-2xl font-semibold text-brand-800">
                  {study.results[0].value}
                </p>
                <p className="text-xs text-neutral-500 mt-1">
                  {study.results[0].label}
                </p>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
};

export default Work;
