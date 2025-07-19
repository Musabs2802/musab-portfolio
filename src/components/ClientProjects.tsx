import React, { useState } from 'react';
import ProjectGrid from './ProjectGrid';

interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  category: 'software' | 'data-science' | 'analysis';
  client: string;
  results: string;
}

const ClientProjects: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'all' | 'software' | 'data-science' | 'analysis'>('all');

  const projects: Project[] = [
    {
      id: 1,
      title: "E-commerce Platform Optimization",
      description: "Built a comprehensive e-commerce platform with advanced analytics and personalization features for a retail client.",
      image: "https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["React", "Node.js", "PostgreSQL", "Redis", "AWS"],
      category: "software",
      client: "RetailCorp",
      results: "Increased conversion rate by 35% and reduced page load time by 60%"
    },
    {
      id: 2,
      title: "Customer Behavior Prediction Model",
      description: "Developed machine learning models to predict customer behavior and optimize marketing campaigns for a fintech company.",
      image: "https://images.pexels.com/photos/590022/pexels-photo-590022.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "TensorFlow", "Scikit-learn", "Apache Spark", "AWS SageMaker"],
      category: "data-science",
      client: "FinTech Solutions",
      results: "Improved prediction accuracy to 89% and increased ROI by 25%"
    },
    {
      id: 3,
      title: "Supply Chain Analytics Dashboard",
      description: "Created real-time analytics dashboard for supply chain optimization with predictive insights and automated reporting.",
      image: "https://images.pexels.com/photos/586103/pexels-photo-586103.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Tableau", "SQL", "Python", "Power BI", "Azure"],
      category: "analysis",
      client: "LogisticsPro",
      results: "Reduced operational costs by 20% and improved delivery times by 30%"
    },
    {
      id: 4,
      title: "Healthcare Management System",
      description: "Developed a comprehensive healthcare management system with patient tracking, appointment scheduling, and analytics.",
      image: "https://images.pexels.com/photos/4386467/pexels-photo-4386467.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Vue.js", "Django", "MySQL", "Docker", "Kubernetes"],
      category: "software",
      client: "MedCare Systems",
      results: "Streamlined operations for 50+ clinics and improved patient satisfaction by 40%"
    },
    {
      id: 5,
      title: "Fraud Detection AI System",
      description: "Built an advanced fraud detection system using deep learning to identify suspicious transactions in real-time.",
      image: "https://images.pexels.com/photos/4164418/pexels-photo-4164418.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "PyTorch", "Apache Kafka", "Elasticsearch", "Docker"],
      category: "data-science",
      client: "SecureBank",
      results: "Reduced fraud incidents by 78% and saved $2M+ annually"
    },
    {
      id: 6,
      title: "Market Research Analytics",
      description: "Conducted comprehensive market research and competitive analysis using advanced statistical methods and visualization.",
      image: "https://images.pexels.com/photos/590020/pexels-photo-590020.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["R", "SPSS", "Tableau", "SQL", "Excel"],
      category: "analysis",
      client: "MarketInsights Co.",
      results: "Identified 3 new market opportunities worth $10M+ potential revenue"
    }
  ];

  const filteredProjects = activeTab === 'all' 
    ? projects 
    : projects.filter(project => project.category === activeTab);

  const tabs = [
    { id: 'all', label: 'All Projects' },
    { id: 'software', label: 'Software' },
    { id: 'data-science', label: 'Data Science' },
    { id: 'analysis', label: 'Analysis' }
  ];

  return (
    <section id="client-projects" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Client Projects</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Successful projects delivered for clients across various industries, from startups to enterprise companies.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex bg-white rounded-lg p-1 shadow-sm border border-gray-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-6 py-3 rounded-md text-sm font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-blue-700 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <ProjectGrid projects={filteredProjects} isClient={true} />
      </div>
    </section>
  );
};

export default ClientProjects;