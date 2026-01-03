import React from "react";
import { Mail, Linkedin, Github, MapPin, Phone } from "lucide-react";

const Contact: React.FC = () => {
  return (
    <section
      id="contact"
      className="min-h-screen flex items-center justify-center bg-[#f8f6f3] dark:bg-neutral-950 px-6 pt-28 pb-16"
    >
      <div className="max-w-4xl mx-auto w-full">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-neutral-900 dark:text-white">
            Let's Connect
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto leading-relaxed">
            I'm always open to new opportunities, collaborations, or just a
            friendly chat. Feel free to reach out via any of the platforms
            below.
          </p>
        </div>

        {/* Calendly CTA */}
        <div className="text-center mb-14">
          <a
            href="https://calendly.com/musabs2802/introductory-meeting"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-4 bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 font-medium text-lg rounded-xl shadow-sm hover:opacity-90 transition"
          >
            📅 Book a Free Call with Me
          </a>
        </div>

        {/* Contact Info & Socials */}
        <div className="bg-white dark:bg-neutral-900 rounded-3xl shadow-sm p-8 md:p-10">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            {/* Contact Info */}
            <div className="space-y-6">
              <h3 className="text-xl font-semibold mb-6 text-neutral-900 dark:text-white">
                Contact Info
              </h3>
              <div className="flex items-start gap-4">
                <Mail
                  className="text-neutral-600 dark:text-neutral-400 mt-1 flex-shrink-0"
                  size={20}
                />
                <div>
                  <p className="font-semibold text-neutral-900 dark:text-white text-sm mb-1">
                    Email
                  </p>
                  <a
                    href="mailto:musabs2802@gmail.com"
                    className="text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition"
                  >
                    musabs2802@gmail.com
                  </a>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <Phone
                  className="text-neutral-600 dark:text-neutral-400 mt-1 flex-shrink-0"
                  size={20}
                />
                <div>
                  <p className="font-semibold text-neutral-900 dark:text-white text-sm mb-1">
                    Phone
                  </p>
                  <a
                    href="tel:+966507055745"
                    className="text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition"
                  >
                    +966 50705-5745
                  </a>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <MapPin
                  className="text-neutral-600 dark:text-neutral-400 mt-1 flex-shrink-0"
                  size={20}
                />
                <div>
                  <p className="font-semibold text-neutral-900 dark:text-white text-sm mb-1">
                    Location
                  </p>
                  <p className="text-neutral-600 dark:text-neutral-400">
                    Jeddah, Saudi Arabia
                  </p>
                </div>
              </div>
            </div>

            {/* Social Links */}
            <div>
              <h3 className="text-xl font-semibold mb-6 text-neutral-900 dark:text-white">
                Find Me Online
              </h3>
              <div className="flex gap-4">
                <a
                  href="https://www.linkedin.com/in/musab-shaikh-2802/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center w-12 h-12 bg-neutral-900 dark:bg-white rounded-xl text-white dark:text-neutral-900 hover:opacity-90 transition shadow-sm"
                  aria-label="LinkedIn"
                >
                  <Linkedin size={20} />
                </a>
                <a
                  href="https://github.com/Musabs2802"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center w-12 h-12 bg-neutral-900 dark:bg-white rounded-xl text-white dark:text-neutral-900 hover:opacity-90 transition shadow-sm"
                  aria-label="GitHub"
                >
                  <Github size={20} />
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <p className="text-neutral-500 dark:text-neutral-400 text-sm">
            © 2025 Musab Shaikh. All rights reserved.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
