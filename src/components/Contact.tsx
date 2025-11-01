import React from "react";
import { Mail, Phone, MapPin, Github, Linkedin } from "lucide-react";

const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-20 bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-10">
          <h2 className="font-bold leading-tighter tracking-tighter text-4xl md:text-5xl text-gray-900 mb-4">
            Let's Work Together
          </h2>
          <p className="text-lg text-gray-500 max-w-2xl mx-auto">
            I'm always open to new opportunities and exciting collaborations.
            Reach out to discuss your project or just say hello!
          </p>
        </div>

        {/* Calendly CTA */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <a
            href="https://calendly.com/musabs2802/introductory-meeting"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-xl shadow-md transition duration-200"
          >
            📅 Book a Free Call Now
          </a>
        </div>

        {/* Contact Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-start">
          {/* Contact Details */}
          <div className="space-y-6">
            <div className="flex items-start">
              <Mail className="text-primary-600 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Email</p>
                <a
                  href="mailto:musabs2802@gmail.com"
                  className="text-gray-500 hover:text-gray-800 transition"
                >
                  musabs2802@gmail.com
                </a>
              </div>
            </div>

            <div className="flex items-start">
              <Phone className="text-primary-600 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Phone</p>
                <a
                  href="tel:+966507055745"
                  className="text-gray-500 hover:text-gray-800 transition"
                >
                  +966 50705-5745
                </a>
              </div>
            </div>

            <div className="flex items-start">
              <MapPin className="text-primary-600 mt-1 mr-4" size={24} />
              <div>
                <p className="font-semibold">Location</p>
                <p className="text-gray-500">Jeddah, Saudi Arabia</p>
              </div>
            </div>
          </div>

          {/* Social Links */}
          <div className="space-y-6">
            <p className="text-xl font-semibold mb-4">Connect with me</p>
            <div className="flex space-x-4">
              <a
                href="https://github.com/Musabs2802"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-200 p-3 rounded-lg hover:bg-gray-300 transition"
              >
                <Github size={24} />
              </a>
              <a
                href="https://www.linkedin.com/in/musab-shaikh-2802/"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-200 p-3 rounded-lg hover:bg-gray-300 transition"
              >
                <Linkedin size={24} />
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
