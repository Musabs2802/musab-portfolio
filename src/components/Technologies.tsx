import React from 'react';
import { siCss, siDocker, siGit, siHtml5, siJavascript, siJupyter, siMongodb, SimpleIcon, siNodedotjs, siNumpy, siPandas, siPlotly, siPostgresql, siPython, siPytorch, siReact, siScikitlearn, siTailwindcss, siTensorflow, siTypescript, siVuedotjs } from 'simple-icons';

interface Technology {
  name: string;
  icon: SimpleIcon;
  category: 'frontend' | 'language' | 'web' | 'styling' | 'backend' | 'data' | 'visualization' | 'ml' | 'tools' | 'database' | 'cloud';
}

const Technologies: React.FC = () => {
  const technologies: Technology[] = [
  { name: 'React', icon: siReact, category: 'frontend' },
  { name: 'JavaScript', icon: siJavascript, category: 'language' },
  { name: 'TypeScript', icon: siTypescript, category: 'language' },
  { name: 'Vue.js', icon: siVuedotjs, category: 'frontend' },
  { name: 'HTML5', icon: siHtml5, category: 'web' },
  { name: 'CSS3', icon: siCss, category: 'web' },
  { name: 'Tailwind', icon: siTailwindcss, category: 'styling' },
  { name: 'Node.js', icon: siNodedotjs, category: 'backend' },
  { name: 'Python', icon: siPython, category: 'language' },
  { name: 'Pandas', icon: siPandas, category: 'data' },
  { name: 'NumPy', icon: siNumpy, category: 'data' },
  // These don't exist in Simple Icons:
  { name: 'Matplotlib', icon: siPython, category: 'visualization' },
  { name: 'Plotly', icon: siPlotly, category: 'visualization' },
  { name: 'Seaborn', icon: siPython, category: 'visualization' },
  { name: 'Scikit-learn', icon: siScikitlearn, category: 'ml' },
  { name: 'TensorFlow', icon: siTensorflow, category: 'ml' },
  { name: 'PyTorch', icon: siPytorch, category: 'ml' },
  { name: 'Jupyter', icon: siJupyter, category: 'tools' },
  // SQL as a language doesn't exist, use PostgreSQL or MySQL as proxy
  { name: 'SQL', icon: siPostgresql, category: 'database' },
  { name: 'PostgreSQL', icon: siPostgresql, category: 'database' },
  { name: 'MongoDB', icon: siMongodb, category: 'database' },
  { name: 'Git', icon: siGit, category: 'tools' },
  { name: 'Docker', icon: siDocker, category: 'tools' },
];


  const getCategoryStyles = (category: Technology['category']): string => {
    const categoryStyles: Record<Technology['category'], string> = {
      frontend: 'bg-blue-100 text-blue-700',
      language: 'bg-green-100 text-green-700',
      data: 'bg-purple-100 text-purple-700',
      ml: 'bg-red-100 text-red-700',
      visualization: 'bg-orange-100 text-orange-700',
      database: 'bg-indigo-100 text-indigo-700',
      tools: 'bg-gray-100 text-gray-700',
      cloud: 'bg-cyan-100 text-cyan-700',
      web: 'bg-yellow-100 text-yellow-700',
      styling: 'bg-pink-100 text-pink-700',
      backend: 'bg-emerald-100 text-emerald-700',
    };
    return categoryStyles[category];
  };

  const duplicatedTechnologies: Technology[] = [...technologies, ...technologies];

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
              transform: translateX(-50%);
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
