import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, CalendarDays, TrendingUp, Users } from "lucide-react";
import site from "../data/site.data";

const experienceWith = [
  "Seara (JBS)",
  "Al Kabeer Group",
  "Tritone Health · UK",
  "MBVS · Switzerland",
];

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
            Taking new projects · Jeddah &amp; remote
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-[3.6rem] font-semibold text-ink leading-[1.08] mb-6">
            Power BI dashboards, Excel trackers{" "}
            <span className="text-brand-700">&amp; mobile apps</span> for
            growing businesses.
          </h1>

          <p className="text-lg text-neutral-600 leading-relaxed max-w-xl mb-9">
            I'm Musab, a commercial BI analyst. I run daily reporting for a{" "}
            <strong className="font-semibold text-ink">
              $700M+ business across 13 countries
            </strong>
            , used by 250+ people from the CEO to field sales. I bring that
            same standard to your business, along with Android &amp; iOS apps.
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
            <Link to="/works" className="btn-secondary !px-7 !py-3.5 !text-[15px]">
              See sample dashboards
              <ArrowRight size={16} />
            </Link>
          </div>

          <div>
            <p className="text-xs uppercase tracking-[0.16em] text-neutral-400 mb-3">
              Experience with
            </p>
            <ul className="flex flex-wrap gap-x-6 gap-y-2 text-sm font-medium text-neutral-500">
              {experienceWith.map((name) => (
                <li key={name}>{name}</li>
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
              <p className="text-xs text-neutral-500 mt-1">daily report users</p>
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
