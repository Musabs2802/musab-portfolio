import React from 'react';
import { ChevronDown, Github, Linkedin, Mail } from 'lucide-react';

const Hero: React.FC = () => {
  const scrollToAbout = () => {
    document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section id="about" className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-teal-50 pt-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="animate-fade-in">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
            Hi, I'm <span className="text-blue-700">Musab</span>
          </h1>
          <h2 className="text-2xl md:text-3xl text-gray-600 mb-8">
            Software Engineer & Data Scientist
          </h2>
          <p className="text-lg md:text-xl text-gray-700 max-w-3xl mx-auto mb-12 leading-relaxed">
            I specialize in building innovative software solutions and extracting actionable insights from complex data. 
            With expertise spanning full-stack development, machine learning, and data analysis, I help businesses 
            transform their ideas into reality and make data-driven decisions.
          </p>
          
          <div className="flex justify-center space-x-6 mb-16">
            <a
              href="mailto:musab@example.com"
              className="flex items-center space-x-2 bg-blue-700 text-white px-6 py-3 rounded-lg hover:bg-blue-800 transition-colors duration-200"
            >
              <Mail size={20} />
              <span>Get In Touch</span>
            </a>
            <a
              href="#"
              className="flex items-center space-x-2 border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:border-gray-400 transition-colors duration-200"
            >
              <Github size={20} />
              <span>GitHub</span>
            </a>
            <a
              href="#"
              className="flex items-center space-x-2 border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:border-gray-400 transition-colors duration-200"
            >
              <Linkedin size={20} />
              <span>LinkedIn</span>
            </a>
          </div>

          <button
            onClick={scrollToAbout}
            className="animate-bounce"
          >
            <ChevronDown size={32} className="text-gray-500" />
          </button>
        </div>
      </div>
    </section>
  );
};

export default Hero;