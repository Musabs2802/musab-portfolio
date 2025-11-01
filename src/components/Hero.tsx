import React from "react";
import { ChevronDown } from "lucide-react";

const Hero: React.FC = () => {
  const scrollToAbout = () => {
    document.getElementById("about")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="min-h-screen flex items-center justify-center bg-white dark:bg-neutral-900 pt-24 px-6">
      <div className="max-w-4xl mx-auto text-center animate-fade-in">
        {/* Heading */}
        <h1 className="font-heading text-5xl md:text-7xl font-bold text-neutral-900 dark:text-white mb-4">
          Hi, I’m{" "}
          <span className="text-primary-600 dark:text-primary-400">Musab</span>
        </h1>

        {/* Subtitle */}
        <h2 className="text-xl md:text-2xl font-sans text-neutral-600 dark:text-neutral-300 mb-6">
          Software Engineer & Data Scientist
        </h2>

        {/* Description */}
        <p className="text-base md:text-lg font-sans text-neutral-700 dark:text-neutral-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          I build scalable software and extract insights from data. Combining
          full-stack development with machine learning, I help turn ideas into
          data-driven solutions.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <a
            href="https://calendly.com/musabs2802/introductory-meeting"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-xl shadow-md transition duration-200"
          >
            📅 Book a Free Call Now
          </a>
        </div>

        {/* Scroll Chevron */}
        <button
          onClick={scrollToAbout}
          aria-label="Scroll to About Section"
          className="animate-bounce text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 transition"
        >
          <ChevronDown size={32} />
        </button>
      </div>
    </section>
  );
};

export default Hero;
