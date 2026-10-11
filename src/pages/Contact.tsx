import React, { useState } from "react";
import {
  CalendarDays,
  Clock,
  Github,
  Linkedin,
  Mail,
  MapPin,
  MessageCircle,
  Phone,
} from "lucide-react";
import SEO from "../components/SEO";
import site, { whatsappLink } from "../data/site.data";

const serviceOptions = [
  "Power BI dashboard",
  "Excel tracker / template",
  "Reporting automation",
  "Monthly BI support",
  "Mobile app (Android & iOS)",
  "Something else",
];

const budgetOptions = [
  "Under $500",
  "$500 – $1,500",
  "$1,500 – $5,000",
  "$5,000+",
  "Not sure yet",
];

const timelineOptions = ["As soon as possible", "Within a month", "1–3 months", "Just exploring"];

const inputClass =
  "w-full rounded-xl border border-sand-300 bg-white px-4 py-3 text-[15px] text-ink placeholder:text-neutral-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-100";

const Contact: React.FC = () => {
  const [form, setForm] = useState({
    name: "",
    company: "",
    service: serviceOptions[0],
    budget: budgetOptions[4],
    timeline: timelineOptions[1],
    message: "",
  });

  const update =
    (field: keyof typeof form) =>
    (
      e: React.ChangeEvent<
        HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
      >,
    ) =>
      setForm({ ...form, [field]: e.target.value });

  const summary = [
    `Hi Musab, I'm ${form.name || "[name]"}${form.company ? ` from ${form.company}` : ""}.`,
    "",
    `Service: ${form.service}`,
    `Budget: ${form.budget}`,
    `Timeline: ${form.timeline}`,
    "",
    form.message,
  ].join("\n");

  const sendWhatsApp = (e: React.FormEvent) => {
    e.preventDefault();
    window.open(whatsappLink(summary), "_blank", "noopener,noreferrer");
  };

  const mailto = `mailto:${site.email}?subject=${encodeURIComponent(
    `Project enquiry: ${form.service}`,
  )}&body=${encodeURIComponent(summary)}`;

  return (
    <main className="min-h-screen bg-sand-100 pt-32 pb-24">
      <SEO />
      <div className="container-page">
        <header className="max-w-2xl mb-12">
          <p className="eyebrow mb-3">Contact</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-ink leading-tight">
            Tell me about your project
          </h1>
          <p className="mt-4 text-neutral-600 text-lg leading-relaxed">
            Share a few details and I'll reply within 24 hours with next steps.
            Prefer to talk?{" "}
            <a
              href={site.calendly}
              target="_blank"
              rel="noopener noreferrer"
              className="text-brand-700 font-medium underline underline-offset-4"
            >
              Book a free 20-minute call
            </a>
            .
          </p>
        </header>

        <div className="grid lg:grid-cols-[1.4fr_1fr] gap-8">
          {/* Enquiry form */}
          <form
            onSubmit={sendWhatsApp}
            className="rounded-3xl bg-white border border-sand-300 p-6 md:p-8 space-y-5"
          >
            <div className="grid sm:grid-cols-2 gap-5">
              <label className="block">
                <span className="block text-sm font-medium text-ink mb-1.5">
                  Your name
                </span>
                <input
                  required
                  value={form.name}
                  onChange={update("name")}
                  className={inputClass}
                  placeholder="Jane Smith"
                />
              </label>
              <label className="block">
                <span className="block text-sm font-medium text-ink mb-1.5">
                  Company <span className="text-neutral-400 font-normal">(optional)</span>
                </span>
                <input
                  value={form.company}
                  onChange={update("company")}
                  className={inputClass}
                  placeholder="Acme Trading"
                />
              </label>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <label className="block sm:col-span-2">
                <span className="block text-sm font-medium text-ink mb-1.5">
                  What do you need?
                </span>
                <select value={form.service} onChange={update("service")} className={inputClass}>
                  {serviceOptions.map((o) => (
                    <option key={o}>{o}</option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="block text-sm font-medium text-ink mb-1.5">
                  Budget
                </span>
                <select value={form.budget} onChange={update("budget")} className={inputClass}>
                  {budgetOptions.map((o) => (
                    <option key={o}>{o}</option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="block text-sm font-medium text-ink mb-1.5">
                  Timeline
                </span>
                <select value={form.timeline} onChange={update("timeline")} className={inputClass}>
                  {timelineOptions.map((o) => (
                    <option key={o}>{o}</option>
                  ))}
                </select>
              </label>
            </div>

            <label className="block">
              <span className="block text-sm font-medium text-ink mb-1.5">
                Project details
              </span>
              <textarea
                required
                rows={5}
                value={form.message}
                onChange={update("message")}
                className={inputClass}
                placeholder="What should the dashboard or app do? Where does your data live today (Excel, ERP, SQL)?"
              />
            </label>

            <div className="flex flex-col sm:flex-row gap-3 pt-1">
              <button type="submit" className="btn-primary">
                <MessageCircle size={17} /> Send via WhatsApp
              </button>
              <a href={mailto} className="btn-secondary">
                <Mail size={17} /> Send via email
              </a>
            </div>
            <p className="text-xs text-neutral-500">
              Opens WhatsApp or your email app with your details filled in.
              Nothing is stored on this site.
            </p>
          </form>

          {/* Direct contact */}
          <aside className="space-y-5">
            <div className="rounded-3xl bg-brand-900 text-white p-7">
              <h2 className="text-xl font-semibold mb-2">Rather just talk?</h2>
              <p className="text-brand-100/80 text-sm leading-relaxed mb-6">
                A free 20-minute call to understand what you need. No
                obligation, no sales pitch.
              </p>
              <a
                href={site.calendly}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex w-full items-center justify-center gap-2 px-5 py-3 rounded-xl bg-white text-brand-900 text-sm font-medium hover:bg-brand-50 transition-colors"
              >
                <CalendarDays size={17} /> Book a free call
              </a>
            </div>

            <div className="rounded-3xl bg-white border border-sand-300 p-7 space-y-4 text-sm">
              <a href={site.whatsapp} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 text-ink hover:text-brand-700">
                <MessageCircle size={18} className="text-brand-600" /> WhatsApp {site.phoneDisplay}
              </a>
              <a href={`mailto:${site.email}`} className="flex items-center gap-3 text-ink hover:text-brand-700">
                <Mail size={18} className="text-brand-600" /> {site.email}
              </a>
              <a href={`tel:${site.phone}`} className="flex items-center gap-3 text-ink hover:text-brand-700">
                <Phone size={18} className="text-brand-600" /> {site.phoneDisplay}
              </a>
              <p className="flex items-center gap-3 text-ink">
                <MapPin size={18} className="text-brand-600" /> {site.location}
              </p>
              <p className="flex items-center gap-3 text-ink">
                <Clock size={18} className="text-brand-600" /> {site.responseTime}
              </p>
              <div className="flex gap-3 pt-2">
                <a href={site.linkedin} target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" className="p-2.5 rounded-xl bg-sand-100 text-ink hover:bg-brand-50 hover:text-brand-700">
                  <Linkedin size={18} />
                </a>
                <a href={site.github} target="_blank" rel="noopener noreferrer" aria-label="GitHub" className="p-2.5 rounded-xl bg-sand-100 text-ink hover:bg-brand-50 hover:text-brand-700">
                  <Github size={18} />
                </a>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
};

export default Contact;
