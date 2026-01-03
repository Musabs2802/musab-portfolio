import React from "react";
import { Code2, BarChart3 } from "lucide-react";

const About: React.FC = () => {
  return (
    <section id="about" className="bg-[#f8f6f3] dark:bg-neutral-950 px-6 py-28">
      <div className="max-w-6xl mx-auto">
        {/* Top Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-14 items-center mb-20">
          {/* Illustration / Image */}
          <div className="flex justify-center">
            <div className="w-full max-w-sm rounded-3xl bg-white dark:bg-neutral-900 shadow-sm overflow-hidden">
              <img
                src="https://res.cloudinary.com/de75b0zis/image/upload/v1767276292/musab-working-img_pb9nkt.png" // replace with your image
                alt="Working illustration"
                className="w-full h-auto"
              />
            </div>
          </div>

          {/* Text */}
          <div>
            <h2 className="font-heading text-3xl md:text-4xl font-semibold text-neutral-900 dark:text-white mb-4">
              A bit about me
              <span className="text-neutral-400"> (and my work)</span>
            </h2>

            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              I’m a software engineer and data scientist passionate about
              building systems that don’t just run — they scale, deliver
              insights, and solve real business challenges.
            </p>

            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-8">
              From full-stack applications to AI-driven analytics, pricing
              optimization, and demand forecasting, I transform messy data and
              abstract ideas into clean, production-ready solutions that create
              measurable impact.
            </p>

            <a
              href="https://calendly.com/musabs2802/introductory-meeting"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 text-sm font-medium shadow-sm hover:opacity-90 transition"
            >
              Contact me
            </a>
          </div>
        </div>

        {/* Bottom Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Software Engineer Card */}
          <div className="rounded-2xl bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-xl bg-neutral-100 dark:bg-neutral-800">
                <Code2 className="w-5 h-5 text-neutral-700 dark:text-neutral-300" />
              </div>
              <h3 className="font-medium text-lg text-neutral-900 dark:text-white">
                Software Engineer
              </h3>
            </div>

            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              I design and build scalable, maintainable applications using
              modern front-end and back-end technologies, with a strong focus on
              clean architecture and long-term reliability.
            </p>
          </div>

          {/* Data Analyst / Scientist Card */}
          <div className="rounded-2xl bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-xl bg-neutral-100 dark:bg-neutral-800">
                <BarChart3 className="w-5 h-5 text-neutral-700 dark:text-neutral-300" />
              </div>
              <h3 className="font-medium text-lg text-neutral-900 dark:text-white">
                Data Analyst
              </h3>
            </div>

            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              I’m a Power BI & Excel expert who turns complex datasets into
              actionable insights, building forecasting, pricing, and predictive
              models while creating dashboards that help businesses improve
              revenue, optimize operations, and make confident data-driven
              decisions.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
