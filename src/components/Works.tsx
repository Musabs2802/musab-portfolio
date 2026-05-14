import React from "react";
import workData from "../data/work.data";
import { Link } from "react-router-dom";

const getDemoUrl = (demo: string) => {
  if (/^(https?:)?\/\//.test(demo)) {
    return demo;
  }

  const normalizedPath = demo.replace(/^\/+/, "");
  return `${import.meta.env.BASE_URL}${normalizedPath}`;
};

const Works: React.FC = () => {
  return (
    <section
      id="projects"
      className="bg-[#f8f6f3] dark:bg-neutral-950 px-6 py-28"
    >
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-10">
          <h2 className="text-4xl md:text-5xl font-bold text-[#1a1a1a]">
            My Works
          </h2>
          <Link
            to="/works"
            className="px-5 py-2.5 bg-neutral-900 text-white rounded-xl hover:opacity-90 transition font-medium text-sm flex items-center gap-2 shadow-sm"
          >
            View All
            <span>→</span>
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {workData.slice(0, 6).map((project) => {
            const card = (
              <>
                <div className="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 overflow-hidden">
                  <img
                    src={project.image}
                    alt={project.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">
                    {project.title}
                  </h3>
                  <p className="text-gray-600 mb-4 text-sm leading-relaxed line-clamp-2">
                    {project.description}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {project.technologies.map((tech, index) => (
                      <span
                        key={index}
                        className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md text-xs"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </>
            );

            return project.demo ? (
              <a
                key={project.id}
                href={getDemoUrl(project.demo)}
                target="_blank"
                rel="noopener noreferrer"
                className="group bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow block"
              >
                {card}
              </a>
            ) : (
              <div
                key={project.id}
                className="group bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow"
              >
                {card}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Works;
