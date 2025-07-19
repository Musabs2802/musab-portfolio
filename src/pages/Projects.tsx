import React, { useState } from 'react';
import ProjectGrid from '../components/ProjectGrid';
import projectData from '../data/project.data';

const Projects: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'All' | 'Software' | 'Data Science' | 'Analysis'>('All');

  const filteredProjects = activeTab === 'All'
    ? projectData
    : projectData.filter(project => project.category === activeTab);

  const tabs = [
    { id: 'all', label: 'All Projects' },
    { id: 'software', label: 'Software' },
    { id: 'data-science', label: 'Data Science' },
    { id: 'analysis', label: 'Analysis' }
  ];

  return (
    <section id="projects" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Projects</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Side projects and experiments where I explore new technologies and push the boundaries of what's possible.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex bg-gray-100 rounded-lg p-1 shadow-sm border border-gray-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-6 py-3 rounded-md text-sm font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-teal-700 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <ProjectGrid projects={filteredProjects} isClient={false} />
      </div>
    </section>
  );
};

export default Projects;
