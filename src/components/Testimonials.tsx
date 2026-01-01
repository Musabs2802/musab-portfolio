import React from "react";
import testimonials from "../data/testimonial.data";
import { LucideQuote } from "lucide-react";

const Testimonials: React.FC = () => {
  return (
    <section className="bg-[#FAFAF8] dark:bg-neutral-950 px-6 py-28">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-12 text-[#1a1a1a]">
          What They Said About Me
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {testimonials.map((testimonial) => (
            <div
              key={testimonial.id}
              className="bg-white rounded-xl p-6 shadow-sm"
            >
              <div className="text-5xl text-gray-300 leading-none mb-3">
                <LucideQuote />
              </div>

              <p className="text-gray-600 mb-6 text-[15px] leading-relaxed">
                {testimonial.message}
              </p>

              <div>
                <div className="font-semibold text-gray-900 text-sm">
                  {testimonial.name}
                </div>
                <div className="text-xs text-gray-500">{testimonial.role}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
