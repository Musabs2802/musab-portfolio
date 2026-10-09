import React from "react";
import { process } from "../data/services.data";

const Process: React.FC = () => {
  return (
    <section id="process" className="bg-brand-900 text-white py-24 md:py-28">
      <div className="container-page">
        <div className="max-w-2xl mb-14">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-brand-300 mb-3">
            How I work
          </p>
          <h2 className="text-3xl md:text-4xl font-semibold leading-tight">
            Clear scope, fixed price, weekly progress.
          </h2>
        </div>

        <ol className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {process.map(({ step, title, text }) => (
            <li
              key={step}
              className="rounded-2xl bg-white/[0.06] border border-white/10 p-6"
            >
              <p className="font-heading text-sm font-semibold text-emerald-300 mb-6">
                {step}
              </p>
              <h3 className="text-lg font-semibold mb-2">{title}</h3>
              <p className="text-sm text-brand-100/75 leading-relaxed">{text}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
};

export default Process;
