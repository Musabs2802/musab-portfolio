import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, CalendarDays, TrendingUp, Users } from "lucide-react";
import site from "../data/site.data";

const experienceWith = [
  { name: "Seara (JBS)", note: "World's largest protein company" },
  { name: "Al Kabeer Group", note: "Leading GCC frozen food maker" },
  {
    name: "Tritone Health",
    note: "UK health-tech startup working with the NHS",
  },
  { name: "MBVS", note: "Swiss network of Muslim professionals" },
];

// Rotating end of the headline. All phrases sit in one grid cell, so the
// heading keeps the height of the longest one and nothing below it jumps.
const focusAreas = [
  "dashboards & reporting",
  "sales forecasting",
  "pricing & promo analysis",
  "machine learning models",
  "Android & iOS apps",
];

const RotatingFocus: React.FC = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const id = window.setInterval(
      () => setIndex((i) => (i + 1) % focusAreas.length),
      2600,
    );
    return () => window.clearInterval(id);
  }, []);

  return (
    <span className="grid text-brand-700" aria-hidden="true">
      {focusAreas.map((phrase, i) => (
        <span
          key={phrase}
          className={`[grid-area:1/1] transition-all duration-500 ease-out ${
            i === index
              ? "opacity-100 translate-y-0"
              : "opacity-0 translate-y-3"
          }`}
        >
          {phrase}
        </span>
      ))}
    </span>
  );
};

const Hero: React.FC = () => {
  return (
    <section
      className="relative overflow-hidden bg-sand-100 pt-32 pb-20 md:pt-40 md:pb-28"
      style={{
        backgroundImage:
          "radial-gradient(circle, rgba(15,61,62,0.07) 1px, transparent 1px)",
        backgroundSize: "24px 24px",
      }}
    >
      <div className="container-page grid lg:grid-cols-[1.15fr_0.85fr] gap-14 items-center">
        <div className="animate-fade-in">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 mb-7 rounded-full bg-white border border-sand-300 text-sm text-neutral-600">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
            </span>
            Taking new projects
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-[3.6rem] font-semibold text-ink leading-[1.08] mb-6">
            <span className="sr-only">
              Senior-level analytics and mobile apps for growing businesses:{" "}
              {focusAreas.join(", ")}.
            </span>
            <span aria-hidden="true">Senior-level</span>
            <RotatingFocus />
            <span aria-hidden="true">for growing businesses.</span>
          </h1>

          <p className="text-lg text-neutral-600 leading-relaxed max-w-xl mb-9">
            I'm Musab, a commercial analyst. I run reporting, forecasting and
            targets for a{" "}
            <strong className="font-semibold text-ink">
              $700M+ business across 13 countries
            </strong>
            , used by 250+ people from the CEO to field sales. You get the same
            senior-level work without hiring a full-time analyst.
          </p>

          <div className="flex flex-col sm:flex-row gap-3 mb-12">
            <a
              href={site.calendly}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary !px-7 !py-3.5 !text-[15px]"
            >
              <CalendarDays size={18} />
              Book a free 20-min call
            </a>
            <Link
              to="/works"
              className="btn-secondary !px-7 !py-3.5 !text-[15px]"
            >
              See sample dashboards
              <ArrowRight size={16} />
            </Link>
          </div>

          <div>
            <p className="text-xs uppercase tracking-[0.16em] text-neutral-400 mb-3">
              Experience with
            </p>
            <ul className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm font-medium text-neutral-500">
              {experienceWith.map(({ name, note }) => (
                <li key={name}>
                  <span className="text-ink">{name}</span>
                  <span className="block text-xs font-normal text-neutral-400 mt-0.5">
                    {note}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Illustration with proof chips */}
        <div className="relative mx-auto w-full max-w-sm lg:max-w-none">
          <div className="rounded-[2rem] overflow-hidden bg-white border border-sand-300 shadow-[0_30px_60px_-30px_rgba(15,61,62,0.35)]">
            <img
              src={site.workingImage}
              alt="Illustration of Musab working on a laptop"
              className="w-full h-auto"
            />
          </div>

          <div className="absolute -left-4 sm:-left-10 top-10 flex items-center gap-3 bg-white rounded-2xl border border-sand-200 shadow-lg px-4 py-3">
            <div className="p-2 rounded-xl bg-brand-50 text-brand-700">
              <Users size={18} />
            </div>
            <div>
              <p className="font-heading font-semibold text-ink leading-none">
                250+
              </p>
              <p className="text-xs text-neutral-500 mt-1">
                daily report users
              </p>
            </div>
          </div>

          <div className="absolute -right-3 sm:-right-8 bottom-12 flex items-center gap-3 bg-white rounded-2xl border border-sand-200 shadow-lg px-4 py-3">
            <div className="p-2 rounded-xl bg-emerald-50 text-emerald-700">
              <TrendingUp size={18} />
            </div>
            <div>
              <p className="font-heading font-semibold text-ink leading-none">
                ~$590K / mo
              </p>
              <p className="text-xs text-neutral-500 mt-1">
                growth opportunities found by ML
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
