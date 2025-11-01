import React, { useState } from "react";
import ProjectGrid from "./ProjectGrid";
import workData from "../data/work.data";
import { useNavigate } from "react-router-dom";

const ClientProjects: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<
    "All" | "Software" | "Data Science" | "Analysis"
  >("All");

  const filteredProjects =
    activeTab === "All"
      ? workData
      : workData.filter((work) => work.category === activeTab);

  const visibleProjects = filteredProjects.slice(0, 3);

  const tabs = [
    { id: "All", label: "All Projects" },
    { id: "Software", label: "Software" },
    { id: "Data Science", label: "Data Science" },
    { id: "Analysis", label: "Analysis" },
  ];

  return (
    <section id="client-projects" className="py-24 bg-white relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 relative z-10">
        {/* Header */}
        <div className="mb-8 md:mx-auto md:mb-12 text-center">
          <p className="text-base text-secondary dark:text-blue-200 text-primary-700 font-bold tracking-wide uppercase mb-2">
            Projects
          </p>

          <h2 className="font-bold leading-tighter tracking-tighter text-4xl md:text-5xl text-gray-900">
            What I have done ?
          </h2>

          <p className="mt-4 text-gray-500 max-w-2xl mx-auto text-lg">
            High-impact solutions crafted for clients across software, data
            science, and analytics domains.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex bg-white/80 backdrop-blur-md border border-gray-200 rounded-2xl shadow-sm p-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-5 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 ${
                  activeTab === tab.id
                    ? "bg-primary-700 text-white shadow-md"
                    : "text-gray-700 hover:bg-blue-50 hover:text-blue-700"
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
          <div className="mt-12 flex justify-center">
            <button
              onClick={() => navigate("/works")}
              className="flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-xl hover:bg-primary-700 transition duration-200 shadow-md"
            >
              <span>View More Projects</span>
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default ClientProjects;
