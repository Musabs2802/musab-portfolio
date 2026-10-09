import React from "react";
import { Link } from "react-router-dom";
import { CalendarDays, MessageCircle } from "lucide-react";
import site from "../data/site.data";

const Contact: React.FC = () => {
  return (
    <section className="bg-white py-24 md:py-28">
      <div className="container-page">
        <div className="relative overflow-hidden rounded-[2rem] bg-brand-900 text-white px-7 py-14 md:p-16 text-center">
          <div
            aria-hidden
            className="absolute inset-0 opacity-30"
            style={{
              backgroundImage:
                "radial-gradient(circle, rgba(255,255,255,0.12) 1px, transparent 1px)",
              backgroundSize: "22px 22px",
            }}
          />
          <div className="relative">
            <h2 className="text-3xl md:text-[2.75rem] font-semibold leading-tight max-w-2xl mx-auto mb-5">
              Have a report that takes too long, or an app idea?
            </h2>
            <p className="text-brand-100/80 text-lg max-w-xl mx-auto mb-10 leading-relaxed">
              Tell me about it on a free 20-minute call. You'll leave with a
              clear plan, whether or not we work together.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <a
                href={site.calendly}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-white text-brand-900 font-medium hover:bg-brand-50 transition-colors"
              >
                <CalendarDays size={18} /> Book a free call
              </a>
              <Link
                to="/contact"
                className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl border border-white/25 text-white font-medium hover:bg-white/10 transition-colors"
              >
                <MessageCircle size={18} /> Send project details
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
