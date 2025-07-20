import React from 'react';
import { Mail, Linkedin, Github, MapPin, Phone } from 'lucide-react';

const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-20 bg-gray-50 text-gray-900">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Let's Connect</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            I'm always open to new opportunities, collaborations, or just a friendly chat.
            Feel free to reach out via any of the platforms below.
          </p>
        </div>

        {/* Contact Info & Socials */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
          {/* Contact Info */}
          <div className="space-y-6">
            <div className="flex items-start">
              <Mail className="text-blue-600 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Email</p>
                <a href="mailto:musabs2802@gmail.com" className="text-gray-700">
                  musabs2802@gmail.com
                </a>
              </div>
            </div>

            <div className="flex items-start">
              <Phone className="text-blue-400 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Phone</p>
                <a href="tel:+966507055745" className="text-gray-700">
                  +966 50705-5745
                </a>
              </div>
            </div>

            <div className="flex items-start">
              <MapPin className="text-blue-600 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Location</p>
                <p className="text-gray-700">Jeddah, Saudi Arabia</p>
              </div>
            </div>
          </div>

          {/* Social Links */}
          <div className="space-y-6">
            <p className="text-xl font-semibold mb-4">Find Me Online</p>
            <div className="flex space-x-4">
              <a
                href="https://github.com/Musabs2802"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-600 p-3 rounded-lg text-white hover:bg-blue-700 transition"
              >
                <Linkedin size={24} />
              </a>
              <a
                href="https://www.linkedin.com/in/musab-shaikh-2802/"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-800 p-3 rounded-lg text-white hover:bg-gray-900 transition"
              >
                <Github size={24} />
              </a>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 mt-16 pt-8 text-center">
          <p className="text-gray-500 text-sm">
            © 2025 Musab Shaikh. All rights reserved.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
