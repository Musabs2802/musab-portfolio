import React from 'react';
import { ExternalLink, Github, Building, Star } from 'lucide-react';

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
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {projects.map((project) => (
        <div
          key={project.id}
          className="bg-white rounded-lg shadow-lg overflow-hidden border border-gray-100 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <div className="relative overflow-hidden">
            <img
              src={project.image}
              alt={project.title}
              className="w-full h-48 object-cover transition-transform duration-300 hover:scale-105"
            />
            <div className="absolute top-4 right-4">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                project.category === 'software' 
                  ? 'bg-blue-100 text-blue-800'
                  : project.category === 'data-science'
                  ? 'bg-purple-100 text-purple-800'
                  : 'bg-green-100 text-green-800'
              }`}>
                {project.category.replace('-', ' ')}
              </span>
            </div>
          </div>

          <div className="p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-2">{project.title}</h3>
            
            {isClient && project.client && (
              <div className="flex items-center text-sm text-gray-600 mb-3">
                <Building size={16} className="mr-2" />
                <span>{project.client}</span>
              </div>
            )}

            <p className="text-gray-700 text-sm mb-4 leading-relaxed">{project.description}</p>

            <div className="flex flex-wrap gap-2 mb-4">
              {project.technologies.slice(0, 4).map((tech, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                >
                  {tech}
                </span>
              ))}
              {project.technologies.length > 4 && (
                <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                  +{project.technologies.length - 4} more
                </span>
              )}
            </div>

            {(project.results || project.highlights) && (
              <div className="mb-4 p-3 bg-orange-50 rounded-lg border border-orange-100">
                <div className="flex items-start">
                  <Star size={16} className="text-orange-600 mr-2 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-orange-800">
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
                  className="flex items-center space-x-1 text-gray-600 hover:text-gray-900 transition-colors duration-200"
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
                  className="flex items-center space-x-1 text-blue-600 hover:text-blue-800 transition-colors duration-200"
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