import React, { useState } from 'react';
import ProjectGrid from '../components/ProjectGrid';

interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  category: 'software' | 'data-science' | 'analysis';
  github?: string;
  demo?: string;
  highlights: string;
}

const Projects: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'all' | 'software' | 'data-science' | 'analysis'>('all');

  const projects: Project[] = [
    {
      id: 1,
      title: "Task Management PWA",
      description: "A progressive web application for task management with offline support, real-time collaboration, and advanced analytics.",
      image: "https://images.pexels.com/photos/7078666/pexels-photo-7078666.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["React", "TypeScript", "PWA", "IndexedDB", "WebSockets"],
      category: "software",
      github: "https://github.com/musab/task-manager",
      demo: "https://task-manager-demo.com",
      highlights: "Featured on Product Hunt, 500+ GitHub stars"
    },
    {
      id: 2,
      title: "Stock Price Prediction ML",
      description: "Machine learning model for stock price prediction using LSTM networks and technical indicators with 85% accuracy.",
      image: "https://images.pexels.com/photos/186461/pexels-photo-186461.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "TensorFlow", "Pandas", "NumPy", "Matplotlib"],
      category: "data-science",
      github: "https://github.com/musab/stock-prediction",
      highlights: "85% prediction accuracy, published research paper"
    },
    {
      id: 3,
      title: "Personal Finance Dashboard",
      description: "Interactive dashboard for personal finance tracking with automated categorization and spending insights.",
      image: "https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["D3.js", "Python", "Flask", "SQLite", "Chart.js"],
      category: "analysis",
      github: "https://github.com/musab/finance-dashboard",
      demo: "https://finance-dashboard-demo.com",
      highlights: "Used by 1000+ users, featured in tech blog"
    },
    {
      id: 4,
      title: "Real-time Chat Application",
      description: "Scalable real-time chat application with group messaging, file sharing, and video calls built with modern web technologies.",
      image: "https://images.pexels.com/photos/4050302/pexels-photo-4050302.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Next.js", "Socket.io", "MongoDB", "WebRTC", "Tailwind CSS"],
      category: "software",
      github: "https://github.com/musab/chat-app",
      demo: "https://chat-app-demo.com",
      highlights: "Supports 10,000+ concurrent users"
    },
    {
      id: 5,
      title: "Image Classification CNN",
      description: "Deep learning model for image classification using convolutional neural networks with data augmentation techniques.",
      image: "https://images.pexels.com/photos/8386434/pexels-photo-8386434.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "PyTorch", "OpenCV", "Albumentations", "Jupyter"],
      category: "data-science",
      github: "https://github.com/musab/image-classifier",
      highlights: "92% accuracy on CIFAR-10 dataset"
    },
    {
      id: 6,
      title: "Social Media Analytics",
      description: "Comprehensive analysis of social media trends and engagement patterns using APIs and advanced statistical methods.",
      image: "https://images.pexels.com/photos/267350/pexels-photo-267350.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "Twitter API", "Plotly", "Pandas", "Streamlit"],
      category: "analysis",
      github: "https://github.com/musab/social-analytics",
      demo: "https://social-analytics-demo.com",
      highlights: "Analyzed 1M+ tweets, viral on LinkedIn"
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
