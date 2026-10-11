import React from "react";
import { Check } from "lucide-react";
import { packages } from "../data/services.data";
import site, { whatsappLink } from "../data/site.data";

const Quote: React.FC = () => {
  return (
    <section id="quote" className="bg-sand-100 py-24 md:py-28">
      <div className="container-page">
        <div className="max-w-2xl mb-14">
          <p className="eyebrow mb-3">Get a quote</p>
          <h2 className="section-title">Ways to work together</h2>
          <p className="mt-4 text-neutral-600 text-lg leading-relaxed">
            Every project is scoped to your data, pages or screens. Pick what
            fits, tell me a little about it, and you get a fixed quote within
            24 hours.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-5">
          {packages.map((pkg) => (
            <article
              key={pkg.name}
              className={`relative flex flex-col rounded-3xl p-6 ${
                pkg.featured
                  ? "bg-brand-900 text-white shadow-[0_24px_48px_-24px_rgba(15,61,62,0.6)]"
                  : "bg-white border border-sand-300"
              }`}
            >
              <h3 className="text-lg font-semibold">{pkg.name}</h3>
              <p
                className={`text-sm mt-1.5 leading-relaxed ${
                  pkg.featured ? "text-brand-100/80" : "text-neutral-600"
                }`}
              >
                {pkg.summary}
              </p>


              <ul className="space-y-2 text-sm mt-6 mb-6">
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
          Not sure which fits, or need something else, like a one-off analysis
          or a training session for your team?{" "}
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

export default Quote;
