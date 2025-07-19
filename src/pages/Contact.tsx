import React from 'react';
import { Mail, Linkedin, Github } from 'lucide-react';

const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-20 bg-gray-50">
      <div className="max-w-3xl mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">Let's Connect</h2>
        <p className="text-lg text-gray-600 mb-10">
          I'm always open to new opportunities, collaborations, or just a friendly chat. Feel free to reach out via any of the platforms below.
        </p>

        <div className="flex flex-col sm:flex-row justify-center items-center gap-6">
          <a
            href="mailto:musab@example.com"
            className="inline-flex items-center gap-2 px-5 py-3 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition"
          >
            <Mail size={18} />
            musab@example.com
          </a>

          <a
            href="https://linkedin.com/in/musab"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <Linkedin size={18} />
            LinkedIn
          </a>

          <a
            href="https://github.com/musab"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition"
          >
            <Github size={18} />
            GitHub
          </a>
        </div>
      </div>
    </section>
  );
};

export default Contact;
