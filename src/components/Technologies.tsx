import React from "react";
import { Technology } from "../types";
import technologiesData from "../data/technologies.data";

const Technologies: React.FC = () => {
  const getCategoryStyles = (category: Technology["category"]): string => {
    const categoryStyles: Record<Technology["category"], string> = {
      Frontend: "bg-blue-50 text-blue-600",
      Backend: "bg-emerald-50 text-emerald-600",
      Language: "bg-green-50 text-green-600",
      Data: "bg-purple-50 text-purple-600",
      ML: "bg-rose-50 text-rose-600",
      Visualization: "bg-amber-50 text-amber-600",
      Database: "bg-indigo-50 text-indigo-600",
      Tools: "bg-gray-50 text-gray-600",
      Cloud: "bg-cyan-50 text-cyan-600",
    };
    return categoryStyles[category];
  };

  return (
    <section
      id="technologies"
      className="py-8 bg-primary-50 relative overflow-hidden"
    >
      <div className="max-w-6xl mx-auto px-6 relative z-10">
        {/* Header */}
        <div className="mb-8 md:mx-auto md:mb-12 text-center">
          <p className="text-base text-secondary dark:text-blue-200 text-primary-700 font-bold tracking-wide uppercase mb-2">
            Technologies
          </p>

          <h2 className="font-bold leading-tighter tracking-tighter text-4xl md:text-5xl text-gray-900">
            What do I use ?
          </h2>

          <p className="mt-4 text-gray-500 max-w-2xl mx-auto text-lg">
            Tools and frameworks that power my software engineering and data
            science projects
          </p>
        </div>

        {/* Tech Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {technologiesData.map((tech, index) => (
            <div
              key={`${tech.name}-${index}`}
              className="group bg-white/90 backdrop-blur-lg border border-gray-100 rounded-2xl shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 p-5 text-center"
            >
              <div className="flex flex-col items-center justify-center">
                <svg
                  className="mb-3 group-hover:scale-110 transition-transform duration-300"
                  role="img"
                  viewBox="0 0 24 24"
                  width="42"
                  height="42"
                  fill={`#${tech.icon.hex}`}
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <title>{tech.icon.title}</title>
                  <path d={tech.icon.path} />
                </svg>

                <h3 className="font-semibold text-gray-800 text-sm mb-1">
                  {tech.name}
                </h3>

                <span
                  className={`inline-block mt-1 px-2.5 py-1 rounded-full text-xs font-medium ${getCategoryStyles(
                    tech.category
                  )}`}
                >
                  {tech.category}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Technologies;
