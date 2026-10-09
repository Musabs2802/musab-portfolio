import React from "react";
import { ArrowUpRight, Quote } from "lucide-react";
import caseStudies, { CaseStudy } from "../data/caseStudies.data";

const Visual: React.FC<{ visual: CaseStudy["visual"] }> = ({ visual }) => {
  if (visual.type === "before-after") {
    return (
      <div className="h-full min-h-[280px] rounded-3xl bg-brand-900 text-white p-8 flex flex-col justify-center">
        <p className="text-xs uppercase tracking-[0.16em] text-brand-300 mb-8">
          {visual.unit}
        </p>
        <div className="space-y-6">
          <div>
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-sm text-brand-100/70">Before</span>
              <span className="font-heading text-2xl font-semibold text-brand-100/70">
                {visual.before}
              </span>
            </div>
            <div className="h-3 rounded-full bg-white/25 w-full" />
          </div>
          <div>
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-sm text-white">After</span>
              <span className="font-heading text-4xl font-semibold">
                {visual.after}
              </span>
            </div>
            <div className="h-3 rounded-full bg-emerald-400 w-[17%]" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <figure className="h-full">
      <div className="rounded-3xl overflow-hidden border border-sand-300 bg-white shadow-[0_24px_48px_-28px_rgba(15,61,62,0.35)]">
        <img
          src={visual.src}
          alt={visual.alt}
          loading="lazy"
          className="w-full h-auto"
        />
      </div>
      {visual.caption && (
        <figcaption className="mt-3 text-xs text-neutral-500">
          {visual.caption}
        </figcaption>
      )}
    </figure>
  );
};

const CaseStudyCard: React.FC<{ study: CaseStudy; flip: boolean }> = ({
  study,
  flip,
}) => (
  <article className="grid lg:grid-cols-2 gap-10 lg:gap-14 items-center">
    <div className={flip ? "lg:order-2" : ""}>
      <Visual visual={study.visual} />
    </div>

    <div>
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <span
          className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
            study.service === "Analytics"
              ? "bg-brand-50 text-brand-700"
              : "bg-amber-50 text-amber-700"
          }`}
        >
          {study.service}
        </span>
        <span className="text-sm text-neutral-500">{study.client}</span>
      </div>

      <h3 className="text-2xl md:text-[1.75rem] font-semibold text-ink mb-5">
        {study.title}
      </h3>

      <dl className="space-y-5 text-[15px] leading-relaxed">
        <div>
          <dt className="text-xs uppercase tracking-[0.14em] font-semibold text-neutral-400 mb-1.5">
            Problem
          </dt>
          <dd className="text-neutral-700">{study.problem}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-[0.14em] font-semibold text-neutral-400 mb-1.5">
            What I built
          </dt>
          <dd>
            <ul className="space-y-1.5 text-neutral-700">
              {study.built.map((item) => (
                <li key={item} className="flex gap-2.5">
                  <span className="mt-[0.6rem] h-1.5 w-1.5 shrink-0 rounded-full bg-brand-500" />
                  {item}
                </li>
              ))}
            </ul>
          </dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-[0.14em] font-semibold text-neutral-400 mb-2.5">
            Result
          </dt>
          <dd className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {study.results.map((r) => (
              <div
                key={r.label}
                className="rounded-2xl bg-white border border-sand-300 p-4"
              >
                <p className="font-heading text-xl font-semibold text-brand-800 leading-tight">
                  {r.value}
                </p>
                <p className="text-xs text-neutral-500 mt-1 leading-snug">
                  {r.label}
                </p>
              </div>
            ))}
          </dd>
        </div>
      </dl>

      {study.quote && (
        <blockquote className="mt-6 flex gap-3 rounded-2xl bg-sand-200/60 p-4">
          <Quote size={18} className="shrink-0 text-brand-600 mt-0.5" />
          <div>
            <p className="text-[15px] text-ink italic">“{study.quote.text}”</p>
            <footer className="text-xs text-neutral-500 mt-1.5">
              {study.quote.author}
            </footer>
          </div>
        </blockquote>
      )}

      <div className="mt-6 flex flex-wrap items-center gap-x-5 gap-y-3">
        <div className="flex flex-wrap gap-1.5">
          {study.tools.map((tool) => (
            <span key={tool} className="chip bg-white border border-sand-200">
              {tool}
            </span>
          ))}
        </div>
        {study.link && (
          <a
            href={study.link.href}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-sm font-medium text-brand-700 hover:text-brand-900"
          >
            {study.link.label}
            <ArrowUpRight size={15} />
          </a>
        )}
      </div>
    </div>
  </article>
);

const CaseStudies: React.FC = () => {
  return (
    <section id="case-studies" className="bg-sand-100 py-24 md:py-28">
      <div className="container-page">
        <div className="max-w-2xl mb-16">
          <p className="eyebrow mb-3">Case studies</p>
          <h2 className="section-title">
            Real problems, what I built, and what changed.
          </h2>
        </div>

        <div className="space-y-24">
          {caseStudies.map((study, i) => (
            <CaseStudyCard key={study.id} study={study} flip={i % 2 === 1} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default CaseStudies;
