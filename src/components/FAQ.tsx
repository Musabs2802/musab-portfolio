"use client";

import { useState } from "react";
import faqs from "../data/faq.data";

export default function FAQ() {
  const [openId, setOpenId] = useState<number | null>(1);

  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-12 text-[#1a1a1a]">
          Let's Clear Things Up
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Contact Card */}
          <div className="flex flex-col items-center justify-center bg-[#f8f6f3] rounded-xl p-8">
            <div className="w-20 h-20 rounded-full bg-white mb-5 flex items-center justify-center overflow-hidden">
              <img
                src="https://res.cloudinary.com/de75b0zis/image/upload/v1767276493/musab-img_dbulfo.png"
                alt="Profile"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-lg font-bold mb-2 text-gray-900">
              Got a question? Let's chat.
            </h3>
            <p className="text-gray-600 text-center mb-6 text-sm">
              I'm just a message away. Whether it's a bug, a collab, or just to
              say hi.
            </p>
            <a
              href="mailto:musabs2802@gmail.com"
              className="w-full mb-3 px-5 py-2.5 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium flex items-center justify-center gap-2"
            >
              ✉️ Send me an email
            </a>
            <a
              href="https://wa.me/966507055745"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full px-5 py-2.5 border border-gray-300 bg-white rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium flex items-center justify-center gap-2"
            >
              <span className="text-green-500 text-xs">●</span> Text me on
              Whatsapp
            </a>
          </div>

          {/* FAQ List */}
          <div className="space-y-3">
            {faqs.map((faq) => (
              <div
                key={faq.id}
                className="border border-gray-200 rounded-lg overflow-hidden bg-white"
              >
                <button
                  onClick={() => setOpenId(openId === faq.id ? null : faq.id)}
                  className="w-full px-5 py-4 text-left font-medium text-gray-900 hover:bg-gray-50 transition-colors flex items-start justify-between gap-4 text-sm"
                >
                  <span>
                    <span className="text-gray-400">{faq.id}.</span>{" "}
                    {faq.question}
                  </span>
                  <span className="text-xl text-gray-400 flex-shrink-0 leading-none">
                    {openId === faq.id ? "−" : "+"}
                  </span>
                </button>
                {openId === faq.id && (
                  <div className="px-5 py-4 bg-gray-50 text-gray-600 border-t border-gray-100 text-[15px] leading-relaxed">
                    {faq.answer}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
