import React from 'react';
import { Quote } from 'lucide-react';
import testimonialData from '../data/testimonial.data';

const Testimonials: React.FC = () => {
  return (
    <section className="py-24 bg-white text-gray-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-4xl font-extrabold tracking-tight mb-4">What People Say</h2>
        <p className="text-lg text-gray-600 mb-14 max-w-2xl mx-auto">
          Words from those I’ve collaborated with across startups and enterprises.
        </p>

        <div className="grid gap-10 sm:grid-cols-2 md:grid-cols-3">
          {testimonialData.map((testimonial, index) => (
            <figure
              key={index}
              className="bg-gray-50 p-6 rounded-2xl border shadow-sm hover:shadow-lg transition duration-300 text-left"
            >
              <Quote className="text-blue-500 mb-4" size={28} />
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
