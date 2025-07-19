import React from 'react';
import { Mail, Phone, MapPin, Github, Linkedin, Twitter } from 'lucide-react';

const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-20 bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Let's Work Together</h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            I'm always interested in new opportunities and exciting projects. Let's discuss how we can bring your ideas to life.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <div>
            <h3 className="text-2xl font-bold mb-8">Get In Touch</h3>
            
            <div className="space-y-6">
              <div className="flex items-center">
                <Mail className="text-blue-400 mr-4" size={24} />
                <div>
                  <p className="font-semibold">Email</p>
                  <a href="mailto:musab@example.com" className="text-gray-300 hover:text-white transition-colors">
                    musab@example.com
                  </a>
                </div>
              </div>

              <div className="flex items-center">
                <Phone className="text-blue-400 mr-4" size={24} />
                <div>
                  <p className="font-semibold">Phone</p>
                  <a href="tel:+1234567890" className="text-gray-300 hover:text-white transition-colors">
                    +1 (234) 567-8900
                  </a>
                </div>
              </div>

              <div className="flex items-center">
                <MapPin className="text-blue-400 mr-4" size={24} />
                <div>
                  <p className="font-semibold">Location</p>
                  <p className="text-gray-300">San Francisco, CA</p>
                </div>
              </div>
            </div>

            <div className="mt-12">
              <h4 className="text-lg font-semibold mb-4">Follow Me</h4>
              <div className="flex space-x-4">
                <a
                  href="#"
                  className="bg-gray-800 p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200"
                >
                  <Github size={24} />
                </a>
                <a
                  href="#"
                  className="bg-gray-800 p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200"
                >
                  <Linkedin size={24} />
                </a>
                <a
                  href="#"
                  className="bg-gray-800 p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200"
                >
                  <Twitter size={24} />
                </a>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h3 className="text-2xl font-bold mb-8">Send a Message</h3>
            
            <form className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="firstName" className="block text-sm font-medium mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="John"
                  />
                </div>
                <div>
                  <label htmlFor="lastName" className="block text-sm font-medium mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    id="lastName"
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="john@example.com"
                />
              </div>

              <div>
                <label htmlFor="subject" className="block text-sm font-medium mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Project Discussion"
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  rows={6}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Tell me about your project..."
                ></textarea>
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-semibold"
              >
                Send Message
              </button>
            </form>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-16 pt-8 text-center">
          <p className="text-gray-400">
            © 2025 Musab Shaikh. All rights reserved.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;