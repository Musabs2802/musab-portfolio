import React from "react";
import { ChevronDown } from "lucide-react";

const Hero: React.FC = () => {
  const scrollToAbout = () => {
    document.getElementById("about")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section
      className="relative min-h-screen flex items-center justify-center bg-[#FAFAF8] dark:bg-neutral-950 px-6 pt-28"
      style={{
        backgroundImage: `radial-gradient(circle, rgba(0,0,0,0.05) 1px, transparent 1px)`,
        backgroundSize: "24px 24px",
      }}
    >
      <div className="max-w-3xl mx-auto text-center animate-fade-in">
        {/* Avatar / Illustration Placeholder */}
        <div className="mx-auto mb-6 w-24 h-24 rounded-2xl bg-white dark:bg-neutral-900 shadow-sm flex items-center justify-center overflow-hidden">
          <img
            src="https://res.cloudinary.com/de75b0zis/image/upload/v1767276493/musab-img_dbulfo.png"
            alt="Musab Shaikh"
            className="w-full h-full object-cover transition-transform duration-300"
          />
        </div>

        {/* Intro pill */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-6 rounded-full bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 text-sm text-neutral-600 dark:text-neutral-400">
          Hey! I’m{" "}
          <span className="font-medium text-neutral-900 dark:text-white">
            Musab Shaikh
          </span>
        </div>

        {/* Main headline */}
        <h1 className="font-heading text-4xl md:text-6xl font-semibold text-neutral-900 dark:text-white leading-tight mb-6">
          I build data & software systems
          <br />
          <span className="text-neutral-500 dark:text-neutral-400">
            that actually work.
          </span>
        </h1>

        {/* Subtext */}
        <p className="text-base md:text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed max-w-2xl mx-auto mb-10">
          From pricing optimization and demand forecasting to full-stack
          applications, I turn complex business problems into clean,
          production-ready solutions.
        </p>

        {/* CTA */}
        <div className="flex justify-center mb-14">
          <a
            href="https://calendly.com/musabs2802/introductory-meeting"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 text-sm font-medium shadow-sm hover:opacity-90 transition"
          >
            Contact me
          </a>
        </div>

        {/* Scroll indicator */}
        <button
          onClick={scrollToAbout}
          aria-label="Scroll to About Section"
          className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-300 transition animate-bounce"
        >
          <ChevronDown size={28} />
        </button>
      </div>
    </section>
  );
};

export default Hero;
