import React from "react";
import { Check } from "lucide-react";
import { packages } from "../data/services.data";
import site, { whatsappLink } from "../data/site.data";

const Pricing: React.FC = () => {
  return (
    <section id="pricing" className="bg-sand-100 py-24 md:py-28">
      <div className="container-page">
        <div className="max-w-2xl mb-14">
          <p className="eyebrow mb-3">Pricing</p>
          <h2 className="section-title">Ways to work together</h2>
          <p className="mt-4 text-neutral-600 text-lg leading-relaxed">
            Starting prices in USD. After a free call you get a fixed quote
            based on your data sources, pages or screens.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {packages.map((pkg) => (
            <article
              key={pkg.name}
              className={`relative flex flex-col rounded-3xl p-6 ${
                pkg.featured
                  ? "bg-brand-900 text-white shadow-[0_24px_48px_-24px_rgba(15,61,62,0.6)]"
                  : "bg-white border border-sand-300"
              }`}
            >
              {pkg.featured && (
                <span className="absolute -top-3 left-6 px-2.5 py-1 rounded-full bg-emerald-400 text-brand-950 text-[11px] font-semibold uppercase tracking-wide">
                  Best value
                </span>
              )}
              <h3 className="text-lg font-semibold">{pkg.name}</h3>
              <p
                className={`text-sm mt-1.5 leading-relaxed ${
                  pkg.featured ? "text-brand-100/80" : "text-neutral-600"
                }`}
              >
                {pkg.summary}
              </p>

              <div className="mt-6 mb-6">
                <p
                  className={`text-xs ${
                    pkg.featured ? "text-brand-200" : "text-neutral-500"
                  }`}
                >
                  {pkg.cadence}
                </p>
                <p className="font-heading text-4xl font-semibold tracking-tight">
                  {pkg.price}
                </p>
              </div>

              <ul className="space-y-2 text-sm mb-6">
                {pkg.includes.map((item) => (
                  <li key={item} className="flex gap-2.5">
                    <Check
                      size={16}
                      className={`mt-0.5 shrink-0 ${
                        pkg.featured ? "text-emerald-300" : "text-brand-600"
                      }`}
                    />
                    {item}
                  </li>
                ))}
              </ul>

              <p
                className={`text-xs mt-auto mb-4 ${
                  pkg.featured ? "text-brand-200" : "text-neutral-500"
                }`}
              >
                Timeline: {pkg.timeline}
              </p>
              <a
                href={whatsappLink(
                  `Hi Musab, I'm interested in the ${pkg.name} package.`,
                )}
                target="_blank"
                rel="noopener noreferrer"
                className={
                  pkg.featured
                    ? "inline-flex justify-center px-5 py-2.5 rounded-xl bg-white text-brand-900 text-sm font-medium hover:bg-brand-50 transition-colors"
                    : "btn-secondary !py-2.5"
                }
              >
                Get a quote
              </a>
            </article>
          ))}
        </div>

        <p className="mt-8 text-sm text-neutral-500">
          Need something else, like a one-off analysis or a training session
          for your team?{" "}
          <a
            href={site.calendly}
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand-700 font-medium underline underline-offset-4"
          >
            Book a call
          </a>{" "}
          and we'll scope it together.
        </p>
      </div>
    </section>
  );
};

export default Pricing;
