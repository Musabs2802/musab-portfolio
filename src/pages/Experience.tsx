import React from "react";
import { Calendar, GraduationCap, MapPin } from "lucide-react";
import experienceData from "../data/experience.data";
import Skills from "../components/Skills";
import SEO from "../components/SEO";

const Experience: React.FC = () => {
  return (
    <main className="min-h-screen bg-sand-100 pt-32 pb-24">
      <SEO
        title="Experience"
        description="Commercial BI experience of Musab Shaikh: Power BI reporting for a $700M+ FMCG business, propensity modelling, target setting and reporting automation across the GCC."
        path="/experience"
      />
      <div className="container-page max-w-4xl">
        <header className="mb-14">
          <p className="eyebrow mb-3">Experience</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-ink leading-tight">
            3+ years in FMCG commercial analytics
          </h1>
          <p className="mt-4 text-neutral-600 text-lg leading-relaxed max-w-2xl">
            Building the reporting, targets and models that sales teams across
            the GCC use to make decisions every day.
          </p>
        </header>

        <ol className="relative border-l-2 border-sand-300 ml-2 space-y-10">
          {experienceData.map((exp) => (
            <li key={exp.company} className="pl-8 relative">
              <span className="absolute -left-[9px] top-7 h-4 w-4 rounded-full bg-brand-700 ring-4 ring-sand-100" />
              <article className="rounded-2xl bg-white border border-sand-300 p-6 md:p-8">
                <div className="flex flex-wrap items-center gap-x-5 gap-y-1 text-sm text-neutral-500 mb-3">
                  <span className="inline-flex items-center gap-1.5">
                    <Calendar size={15} /> {exp.period}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <MapPin size={15} /> {exp.location}
                  </span>
                </div>
                <h2 className="text-xl md:text-2xl font-semibold text-ink">
                  {exp.title}
                </h2>
                <p className="text-brand-700 font-medium mb-5">{exp.company}</p>

                <ul className="space-y-2.5 mb-6 text-neutral-700 text-[15px] leading-relaxed">
                  {exp.description.map((item) => (
                    <li key={item} className="flex gap-3">
                      <span className="mt-[0.6rem] h-1.5 w-1.5 shrink-0 rounded-full bg-brand-500" />
                      {item}
                    </li>
                  ))}
                </ul>

                <div className="flex flex-wrap gap-2">
                  {exp.technologies.map((tech) => (
                    <span key={tech} className="chip">
                      {tech}
                    </span>
                  ))}
                </div>
              </article>
            </li>
          ))}

          <li className="pl-8 relative">
            <span className="absolute -left-[9px] top-7 h-4 w-4 rounded-full bg-sand-300 ring-4 ring-sand-100" />
            <article className="rounded-2xl bg-white border border-sand-300 p-6 md:p-8">
              <div className="flex items-center gap-1.5 text-sm text-neutral-500 mb-3">
                <GraduationCap size={16} /> Sep 2023 - Feb 2025
              </div>
              <h2 className="text-xl font-semibold text-ink">
                MSc Data Science, Distinction
              </h2>
              <p className="text-brand-700 font-medium mb-3">
                Middlesex University Dubai
              </p>
              <p className="text-neutral-700 text-[15px]">
                Dissertation: Price Elasticity in FMCG.
              </p>
            </article>
          </li>
        </ol>

        <Skills />
      </div>
    </main>
  );
};

export default Experience;
