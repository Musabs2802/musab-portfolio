import React from 'react';
import { ChevronDown } from 'lucide-react';

const Hero: React.FC = () => {
  const scrollToAbout = () => {
    document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-teal-50 pt-24 px-6">
      <div className="max-w-4xl mx-auto text-center animate-fade-in">
        <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-4">
          Hi, I'm <span className="text-blue-700">Musab</span>
        </h1>
        <h2 className="text-2xl md:text-3xl text-gray-600 mb-6">
          Software Engineer & Data Scientist
        </h2>
        <p className="text-lg md:text-xl text-gray-700 max-w-3xl mx-auto mb-10 leading-relaxed">
          I build scalable software and extract insights from data. Combining full-stack development with machine learning, I help turn ideas into data-driven solutions.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {/* Calendly */}
          <a
            href="https://calendly.com/musabs2802/introductory-meeting"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition duration-200 shadow-md"
          >
            <span>📅 Book a Free Call Now</span>
          </a>
        </div>

        {/* Chevron Scroll */}
        <button
          onClick={scrollToAbout}
          aria-label="Scroll to About Section"
          className="animate-bounce text-gray-400 hover:text-gray-600 transition"
        >
          <ChevronDown size={32} />
        </button>
      </div>
    </section>
  );
};

export default Hero;
