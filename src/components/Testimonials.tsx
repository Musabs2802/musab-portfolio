import React from "react";
import { Quote } from "lucide-react";
import testimonialData from "../data/testimonial.data";

const Testimonials: React.FC = () => {
  return (
    <section id="client-projects" className="py-8 bg-primary-50 relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 relative z-10">
        {/* Header */}
        <div className="mb-8 md:mx-auto md:mb-12 text-center">
          <p className="text-base text-secondary dark:text-blue-200 text-primary-700 font-bold tracking-wide uppercase mb-2">
            Testimonials
          </p>

          <h2 className="font-bold leading-tighter tracking-tighter text-4xl md:text-5xl text-gray-900">
            What Clients Say ?
          </h2>

          <p className="mt-4 text-gray-500 max-w-2xl mx-auto text-lg">
            Words from those I’ve collaborated with across startups and
            enterprises.
          </p>
        </div>

        <div className="grid gap-10 sm:grid-cols-2 md:grid-cols-3">
          {testimonialData.map((testimonial, index) => (
            <figure
              key={index}
              className="bg-white p-6 rounded-2xl border text-left"
            >
              <Quote className="text-primary-700 mb-4" size={28} />
              <blockquote className="text-gray-700 italic mb-6">
                “{testimonial.message}”
              </blockquote>
              <figcaption>
                <div className="text-sm font-semibold">{testimonial.name}</div>
                <div className="text-xs text-gray-500">{testimonial.role}</div>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
