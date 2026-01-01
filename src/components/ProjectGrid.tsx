import React from "react";
import { ExternalLink, Github, Building, Star } from "lucide-react";

interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  category: string;
  client?: string;
  results?: string;
  github?: string;
  demo?: string;
  highlights?: string;
}

interface ProjectGridProps {
  projects: Project[];
  isClient: boolean;
}

const ProjectGrid: React.FC<ProjectGridProps> = ({ projects, isClient }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {projects.map((project) => (
        <div
          key={project.id}
          className="bg-white dark:bg-neutral-900 rounded-xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300"
        >
          <div className="relative overflow-hidden aspect-video">
            <img
              src={project.image}
              alt={project.title}
              className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            />
            <div className="absolute top-4 right-4">
              <span
                className={`px-3 py-1.5 rounded-lg text-xs font-medium shadow-sm ${
                  project.category === "Software"
                    ? "bg-neutral-900 dark:bg-white text-white dark:text-neutral-900"
                    : project.category === "Data Science"
                    ? "bg-neutral-900 dark:bg-white text-white dark:text-neutral-900"
                    : "bg-neutral-900 dark:bg-white text-white dark:text-neutral-900"
                }`}
              >
                {project.category}
              </span>
            </div>
          </div>

          <div className="p-5">
            <h3 className="text-lg font-bold text-neutral-900 dark:text-white mb-2">
              {project.title}
            </h3>

            {isClient && project.client && (
              <div className="flex items-center text-sm text-neutral-600 dark:text-neutral-400 mb-3">
                <Building size={16} className="mr-2" />
                <span>{project.client}</span>
              </div>
            )}

            <p className="text-neutral-600 dark:text-neutral-400 text-sm mb-4 leading-relaxed">
              {project.description}
            </p>

            <div className="flex flex-wrap gap-2 mb-4">
              {project.technologies.slice(0, 4).map((tech, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1.5 bg-gray-100 dark:bg-neutral-800 text-gray-700 dark:text-neutral-300 text-xs rounded-md"
                >
                  {tech}
                </span>
              ))}
              {project.technologies.length > 4 && (
                <span className="px-3 py-1.5 bg-gray-100 dark:bg-neutral-800 text-gray-700 dark:text-neutral-300 text-xs rounded-md">
                  +{project.technologies.length - 4} more
                </span>
              )}
            </div>

            {(project.results || project.highlights) && (
              <div className="mb-4 p-3 bg-orange-50 dark:bg-orange-950/30 rounded-lg">
                <div className="flex items-start">
                  <Star
                    size={16}
                    className="text-orange-600 dark:text-orange-400 mr-2 mt-0.5 flex-shrink-0"
                  />
                  <p className="text-sm text-orange-800 dark:text-orange-300">
                    {project.results || project.highlights}
                  </p>
                </div>
              </div>
            )}

            <div className="flex space-x-3">
              {project.github && (
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-1 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors duration-200"
                >
                  <Github size={16} />
                  <span className="text-sm">Code</span>
                </a>
              )}
              {project.demo && (
                <a
                  href={project.demo}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-1 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors duration-200"
                >
                  <ExternalLink size={16} />
                  <span className="text-sm">Demo</span>
                </a>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProjectGrid;
