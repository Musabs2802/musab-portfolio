import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import workData from "../data/work.data";
import { getDemoUrl } from "../utils/demoUrl";

const Works: React.FC = () => {
  return (
    <section id="samples" className="bg-white py-24 md:py-28">
      <div className="container-page">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div className="max-w-2xl">
            <p className="eyebrow mb-3">Sample dashboards</p>
            <h2 className="section-title">Click around before you hire me.</h2>
            <p className="mt-4 text-neutral-600 text-lg leading-relaxed">
              Interactive dashboards I built on fictional FMCG data to show
              what's possible. Yours is built in Power BI or Excel, on your own
              data.
            </p>
          </div>
          <Link to="/works" className="btn-secondary shrink-0 self-start md:self-auto">
            View all {workData.length}
            <ArrowRight size={16} />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {workData.slice(0, 6).map((project) => (
            <a
              key={project.id}
              href={project.demo ? getDemoUrl(project.demo) : undefined}
              target="_blank"
              rel="noopener noreferrer"
              className="group block rounded-2xl overflow-hidden border border-sand-300 bg-sand-50 hover:border-brand-300 hover:shadow-[0_16px_40px_-20px_rgba(15,61,62,0.35)] transition-all"
            >
              <div className="aspect-[16/10] overflow-hidden bg-sand-200 border-b border-sand-200">
                <img
                  src={project.image}
                  alt={`${project.title} screenshot`}
                  loading="lazy"
                  className="w-full h-full object-cover object-top group-hover:scale-[1.03] transition-transform duration-500"
                />
              </div>
              <div className="p-5">
                <div className="flex items-start justify-between gap-3">
                  <h3 className="font-semibold text-ink leading-snug">
                    {project.title}
                  </h3>
                  <ArrowUpRight
                    size={18}
                    className="shrink-0 text-neutral-400 group-hover:text-brand-700 transition-colors"
                  />
                </div>
                <p className="text-neutral-600 mt-2 text-sm leading-relaxed line-clamp-2">
                  {project.description}
                </p>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Works;
