import React, { useEffect, useState } from "react";
import ProjectGrid from "../components/ProjectGrid";
import workData from "../data/work.data";

const Work: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    "All" | "Software" | "Data Science" | "Analysis"
  >("All");

  useEffect(() => {
    window.scrollTo(0, 0); // Scroll to top on mount
  }, []);

  const filteredProjects =
    activeTab === "All"
      ? workData
      : workData.filter((work) => work.category === activeTab);

  const tabs = [
    { id: "All", label: "All Projects" },
    { id: "Software", label: "Software" },
    { id: "Data Science", label: "Data Science" },
    { id: "Analysis", label: "Analysis" },
  ];

  return (
    <section
      id="work"
      className="min-h-screen bg-[#FAFAF8] dark:bg-neutral-950 px-6 pt-28 pb-16"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-neutral-900 dark:text-white mb-4">
            Work
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto leading-relaxed">
            High-impact solutions delivered for clients across software, data
            science, and analytics domains.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center mb-10">
          <div className="inline-flex bg-white dark:bg-neutral-900 rounded-xl p-1 shadow-sm">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as any);
                }}
                className={`px-5 py-2 text-sm font-medium rounded-lg transition-all ${
                  activeTab === tab.id
                    ? "bg-neutral-900 dark:bg-white text-white dark:text-neutral-900"
                    : "text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Projects Grid */}
        <ProjectGrid projects={filteredProjects} isClient={true} />
      </div>
    </section>
  );
};

export default Work;
