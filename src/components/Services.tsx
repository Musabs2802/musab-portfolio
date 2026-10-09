import React from "react";
import { BarChart3, Check, Smartphone } from "lucide-react";
import services from "../data/services.data";
import { whatsappLink } from "../data/site.data";

const icons: Record<string, React.ReactNode> = {
  analytics: <BarChart3 size={22} />,
  apps: <Smartphone size={22} />,
};

const Services: React.FC = () => {
  return (
    <section id="services" className="bg-white py-24 md:py-28">
      <div className="container-page">
        <div className="max-w-2xl mb-14">
          <p className="eyebrow mb-3">Services</p>
          <h2 className="section-title">
            Two things I do, and do properly.
          </h2>
          <p className="mt-4 text-neutral-600 text-lg leading-relaxed">
            Reporting that helps your team decide faster, and apps that put
            your product in your customers' pockets.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {services.map((service) => (
            <article
              key={service.id}
              className="flex flex-col rounded-3xl border border-sand-300 bg-sand-50 p-7 md:p-9"
            >
              <div className="flex items-center gap-3 mb-5">
                <div className="p-3 rounded-2xl bg-brand-900 text-white">
                  {icons[service.id]}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-ink">
                    {service.title}
                  </h3>
                  <p className="text-sm text-brand-700 font-medium">
                    {service.tagline}
                  </p>
                </div>
              </div>

              <p className="text-neutral-600 leading-relaxed mb-6">
                {service.description}
              </p>

              <ul className="space-y-2.5 mb-7">
                {service.deliverables.map((item) => (
                  <li key={item} className="flex gap-3 text-[15px] text-ink">
                    <Check
                      size={18}
                      className="mt-0.5 shrink-0 text-brand-600"
                    />
                    {item}
                  </li>
                ))}
              </ul>

              <div className="flex flex-wrap gap-1.5 mb-8">
                {service.tools.map((tool) => (
                  <span key={tool} className="chip bg-white border border-sand-200">
                    {tool}
                  </span>
                ))}
              </div>

              <a
                href={whatsappLink(
                  `Hi Musab, I'd like to discuss a project: ${service.title}.`,
                )}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary mt-auto self-start"
              >
                {service.cta} on WhatsApp
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;
