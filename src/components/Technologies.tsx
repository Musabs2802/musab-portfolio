import React from 'react';
import { Technology } from '../types';
import technologiesData from '../data/technologies.data';

const Technologies: React.FC = () => {
  const getCategoryStyles = (category: Technology['category']): string => {
    const categoryStyles: Record<Technology['category'], string> = {
      Frontend: 'bg-blue-100 text-blue-700',
      Language: 'bg-green-100 text-green-700',
      Data: 'bg-purple-100 text-purple-700',
      ML: 'bg-red-100 text-red-700',
      Visualization: 'bg-orange-100 text-orange-700',
      Database: 'bg-indigo-100 text-indigo-700',
      Tools: 'bg-gray-100 text-gray-700',
      Cloud: 'bg-cyan-100 text-cyan-700',
      Backend: 'bg-emerald-100 text-emerald-700',
    };
    return categoryStyles[category];
  };

  const duplicatedTechnologies: Technology[] = [...technologiesData, ...technologiesData];

  return (
    <section className="py-16 bg-gradient-to-br from-slate-50 to-blue-50 overflow-hidden">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Technologies I Use
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            A comprehensive toolkit spanning software development, data science, and analytics
          </p>
        </div>

        <div className="relative">
          <div className="flex scroll-track">
            {duplicatedTechnologies.map((tech, index) => (
            <div key={`${tech.name}-${index}`} className="flex-shrink-0 mx-4 group">
                <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-6 min-w-[140px] text-center border border-gray-100 hover:border-blue-200 hover:scale-105">
                <svg
                    className="mx-auto mb-3 group-hover:scale-110 transition-transform duration-300"
                    role="img"
                    viewBox="0 0 24 24"
                    width="40"
                    height="40"
                    fill={`#${tech.icon.hex}`}
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <title>{tech.icon.title}</title>
                    <path d={tech.icon.path} />
                </svg>
                <h3 className="font-semibold text-gray-800 text-sm mb-1">{tech.name}</h3>
                <span
                    className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getCategoryStyles(
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
      </div>

      {/* ✅ Standard <style> for animation */}
      <style>
        {`
          @keyframes scroll {
            0% {
              transform: translateX(0);
            }
            100% {
              transform: translateX(-100%);
            }
          }

          .scroll-track {
            animation: scroll 6s linear infinite;
          }

          .scroll-track:hover {
            animation-play-state: paused;
          }
        `}
      </style>
    </section>
  );
};

export default Technologies;
