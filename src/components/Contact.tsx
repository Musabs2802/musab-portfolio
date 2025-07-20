import React from 'react';
import { Mail, Phone, MapPin, Github, Linkedin, Twitter } from 'lucide-react';

const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-20 bg-gray-900 text-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Let's Work Together</h2>
          <p className="text-lg text-gray-300 max-w-2xl mx-auto">
            I'm always open to new opportunities and exciting collaborations. Reach out to discuss your project or just say hello!
          </p>
        </div>

        {/* Contact Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-start">
          {/* Contact Details */}
          <div className="space-y-6">
            <div className="flex items-start">
              <Mail className="text-blue-400 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Email</p>
                <a href="mailto:musab@example.com" className="text-gray-300 hover:text-white transition">
                  musab@example.com
                </a>
              </div>
            </div>

            <div className="flex items-start">
              <Phone className="text-blue-400 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Phone</p>
                <a href="tel:+1234567890" className="text-gray-300 hover:text-white transition">
                  +1 (234) 567-8900
                </a>
              </div>
            </div>

            <div className="flex items-start">
              <MapPin className="text-blue-400 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Location</p>
                <p className="text-gray-300">Jeddah, Saudi Arabia</p>
              </div>
            </div>
          </div>

          {/* Social Links */}
          <div className="space-y-6">
            <p className="text-xl font-semibold mb-4">Connect with me</p>
            <div className="flex space-x-4">
              <a
                href="https://github.com/musab"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-800 p-3 rounded-lg hover:bg-gray-700 transition"
              >
                <Github size={24} />
              </a>
              <a
                href="https://linkedin.com/in/musab"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-800 p-3 rounded-lg hover:bg-gray-700 transition"
              >
                <Linkedin size={24} />
              </a>
              <a
                href="https://twitter.com/musab"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-800 p-3 rounded-lg hover:bg-gray-700 transition"
              >
                <Twitter size={24} />
              </a>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-800 mt-16 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2025 Musab Shaikh. All rights reserved.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
