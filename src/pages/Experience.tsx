import React from "react";
import { Calendar, MapPin } from "lucide-react";
import experienceData from "../data/experience.data";

const Experience: React.FC = () => {
  return (
    <section
      id="experience"
      className="min-h-screen bg-[#FAFAF8] dark:bg-neutral-950 px-6 pt-28 pb-16"
    >
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-neutral-900 dark:text-white mb-4">
            Experience
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto leading-relaxed">
            My journey in tech spans from building scalable software to
            uncovering insights from data — across multiple industries and
            roles.
          </p>
        </div>

        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 h-full w-0.5 bg-neutral-300 dark:bg-neutral-700"></div>

          {/* Timeline items */}
          {experienceData.map((exp, index) => (
            <div
              key={index}
              className={`relative flex items-center mb-12 ${
                index % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"
              }`}
            >
              {/* Dot */}
              <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-4 h-4 bg-neutral-900 dark:bg-white rounded-full border-4 border-[#FAFAF8] dark:border-neutral-950 shadow-sm z-10"></div>

              {/* Content */}
              <div
                className={`ml-12 md:ml-0 md:w-5/12 ${
                  index % 2 === 0 ? "md:mr-auto md:pr-8" : "md:ml-auto md:pl-8"
                }`}
              >
                <div className="bg-white dark:bg-neutral-900 p-6 rounded-xl shadow-sm">
                  <div className="flex items-center text-sm text-neutral-500 dark:text-neutral-400 mb-2">
                    <Calendar size={16} className="mr-2" />
                    <span>{exp.period}</span>
                    <MapPin size={16} className="ml-4 mr-2" />
                    <span>{exp.location}</span>
                  </div>

                  <h3 className="text-xl font-bold text-neutral-900 dark:text-white mb-1">
                    {exp.title}
                  </h3>
                  <h4 className="text-lg text-neutral-600 dark:text-neutral-400 font-semibold mb-4">
                    {exp.company}
                  </h4>

                  <ul className="space-y-2 mb-4 list-disc list-inside text-neutral-600 dark:text-neutral-400 text-sm leading-relaxed">
                    {exp.description.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>

                  <div className="flex flex-wrap gap-2">
                    {exp.technologies.map((tech, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1.5 bg-gray-100 dark:bg-neutral-800 text-gray-700 dark:text-neutral-300 text-xs rounded-md"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Experience;
