import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, GraduationCap, MapPin, Clock } from "lucide-react";
import site from "../data/site.data";

const facts = [
  {
    icon: <MapPin size={16} />,
    text: "Jeddah, Saudi Arabia · works remotely worldwide",
  },
  {
    icon: <GraduationCap size={16} />,
    text: "MSc Data Science (Distinction), Middlesex University Dubai",
  },
  {
    icon: <Clock size={16} />,
    text: "Overlaps with GCC, UK and European working hours",
  },
];

const About: React.FC = () => {
  return (
    <section id="about" className="bg-white py-24 md:py-28">
      <div className="container-page grid md:grid-cols-[0.8fr_1.2fr] gap-12 lg:gap-20 items-center">
        <div className="mx-auto w-full max-w-xs md:max-w-none">
          <div className="rounded-[2rem] overflow-hidden bg-sand-100 border border-sand-300">
            <img
              src={site.avatar}
              alt="Illustrated portrait of Musab Shaikh"
              loading="lazy"
              className="w-full h-auto"
            />
          </div>
        </div>

        <div>
          <p className="eyebrow mb-3">About me</p>
          <h2 className="section-title mb-6">
            An analyst who knows how sales teams actually work.
          </h2>
          <div className="space-y-4 text-neutral-600 text-[17px] leading-relaxed">
            <p>
              I've spent 3+ years in FMCG commercial teams across the GCC. Today
              I'm a Sales Analyst III at JBS, where I own the Power BI reporting
              that everyone from the CEO to field sales opens each morning. I
              also set sales targets for 250+ salesmen and track the incentive
              programs behind 35% year-on-year growth.
            </p>
            <p>
              That's what I bring to freelance work: dashboards built around the
              decisions your team needs to make, not just charts. And because I
              also build mobile apps, I can take an idea from a spreadsheet to
              an app in your customers' hands.
            </p>
          </div>

          <ul className="mt-8 space-y-3">
            {facts.map(({ icon, text }) => (
              <li
                key={text}
                className="flex items-center gap-3 text-sm text-ink"
              >
                <span className="p-2 rounded-lg bg-brand-50 text-brand-700">
                  {icon}
                </span>
                {text}
              </li>
            ))}
          </ul>

          <Link
            to="/experience"
            className="inline-flex items-center gap-1.5 mt-8 text-sm font-medium text-brand-700 hover:text-brand-900"
          >
            See my full experience <ArrowRight size={15} />
          </Link>
        </div>
      </div>
    </section>
  );
};

export default About;
