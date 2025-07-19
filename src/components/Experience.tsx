import React from 'react';
import { Calendar, MapPin } from 'lucide-react';
import experienceData from '../data/experience.data';

const Experience: React.FC = () => {
  return (
    <section id="experience" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Professional Experience</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            My journey in technology spans across different domains, from building software solutions to uncovering insights from data.
          </p>
        </div>

        <div className="relative">
          {/* Timeline line */}
          <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 h-full w-0.5 bg-blue-200"></div>

          {experienceData.map((exp, index) => (
            <div key={index} className={`relative flex items-center mb-12 ${
              index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'
            }`}>
              {/* Timeline dot */}
              <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-4 h-4 bg-blue-700 rounded-full border-4 border-white shadow-lg"></div>

              {/* Content */}
              <div className={`ml-12 md:ml-0 md:w-5/12 ${index % 2 === 0 ? 'md:mr-auto md:pr-8' : 'md:ml-auto md:pl-8'}`}>
                <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-100">
                  <div className="flex items-center text-sm text-gray-500 mb-2">
                    <Calendar size={16} className="mr-2" />
                    <span>{exp.period}</span>
                    <MapPin size={16} className="ml-4 mr-2" />
                    <span>{exp.location}</span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{exp.title}</h3>
                  <h4 className="text-lg text-blue-700 font-semibold mb-4">{exp.company}</h4>
                  
                  <ul className="space-y-2 mb-4">
                    {exp.description.map((item, idx) => (
                      <li key={idx} className="text-gray-700 text-sm leading-relaxed">
                        • {item}
                      </li>
                    ))}
                  </ul>
                  
                  <div className="flex flex-wrap gap-2">
                    {exp.technologies.map((tech, idx) => (
                      <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Experience;