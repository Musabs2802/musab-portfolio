import React, { useEffect, useState } from 'react';
import ProjectGrid from '../components/ProjectGrid';
import workData from '../data/work.data';


const Work: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'All' | 'Software' | 'Data Science' | 'Analysis'>('All');
  const [showAll, setShowAll] = useState(false);
  
  useEffect(() => {
    window.scrollTo(0, 0); // Scroll to top on mount
  }, []);

  const filteredProjects = activeTab === 'All'
    ? workData
    : workData.filter(work => work.category === activeTab);

  const visibleProjects = showAll ? filteredProjects : filteredProjects.slice(0, 3);

  const tabs = [
    { id: 'All', label: 'All Projects' },
    { id: 'Software', label: 'Software' },
    { id: 'Data Science', label: 'Data Science' },
    { id: 'Analysis', label: 'Analysis' }
  ];

  return (
    <section id="work" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-extrabold text-gray-900 mb-4">Work</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            High-impact solutions delivered for clients across software, data science, and analytics domains.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center mb-10">
          <div className="inline-flex bg-white rounded-xl p-1 shadow-sm border border-gray-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as any);
                  setShowAll(false); // reset view more
                }}
                className={`px-5 py-2 text-sm font-semibold rounded-xl transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-700 text-white'
                    : 'text-gray-700 hover:text-blue-700'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Projects Grid */}
        <ProjectGrid projects={visibleProjects} isClient={true} />

        {/* View More Button */}
        {filteredProjects.length > 3 && (
          <div className="mt-10 flex justify-center">
            {showAll ? <></> : 
            <button
              onClick={() => setShowAll(!showAll)}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-all"
            >
              {showAll ? <></> : 'View More'}
            </button>}
          </div>
        )}
      </div>
    </section>
  );
};

export default Work;
