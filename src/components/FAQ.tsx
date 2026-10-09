import { useState } from "react";
import { Mail, MessageCircle, Minus, Plus } from "lucide-react";
import faqs from "../data/faq.data";
import site from "../data/site.data";

export default function FAQ() {
  const [openId, setOpenId] = useState<number | null>(1);

  return (
    <section id="faq" className="bg-sand-100 py-24 md:py-28">
      <div className="container-page grid lg:grid-cols-[0.8fr_1.2fr] gap-10 lg:gap-16">
        <div>
          <p className="eyebrow mb-3">FAQ</p>
          <h2 className="section-title mb-4">Questions clients usually ask</h2>
          <p className="text-neutral-600 leading-relaxed mb-8">
            Don't see yours? Send me a message. I usually reply within 24 hours.
          </p>
          <div className="flex flex-col sm:flex-row lg:flex-col gap-3 max-w-xs">
            <a
              href={site.whatsapp}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary"
            >
              <MessageCircle size={17} /> Message on WhatsApp
            </a>
            <a href={`mailto:${site.email}`} className="btn-secondary">
              <Mail size={17} /> Send an email
            </a>
          </div>
        </div>

        <div className="space-y-3">
          {faqs.map((faq) => {
            const isOpen = openId === faq.id;
            return (
              <div
                key={faq.id}
                className="rounded-2xl border border-sand-300 bg-white overflow-hidden"
              >
                <button
                  onClick={() => setOpenId(isOpen ? null : faq.id)}
                  aria-expanded={isOpen}
                  className="w-full px-5 py-4 text-left font-medium text-ink hover:bg-sand-50 transition-colors flex items-center justify-between gap-4"
                >
                  {faq.question}
                  <span className="shrink-0 text-brand-600">
                    {isOpen ? <Minus size={18} /> : <Plus size={18} />}
                  </span>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 text-neutral-600 text-[15px] leading-relaxed">
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
