import React from "react";
import { Link } from "react-router-dom";
import { Github, Linkedin, Mail, MessageCircle } from "lucide-react";
import site from "../data/site.data";

const Footer: React.FC = () => {
  return (
    <footer className="bg-brand-950 text-brand-100/80">
      <div className="container-page py-14 grid gap-10 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <p className="font-heading text-lg font-semibold text-white mb-3">
            Musab Shaikh
          </p>
          <p className="text-sm leading-relaxed max-w-sm">
            Power BI dashboards, Excel trackers, reporting automation and
            Android &amp; iOS apps. Based in {site.location}, working with
            clients across the GCC and worldwide.
          </p>
        </div>

        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-brand-300 mb-4">
            Explore
          </p>
          <ul className="space-y-2 text-sm">
            <li><Link to="/#services" className="hover:text-white">Services</Link></li>
            <li><Link to="/#case-studies" className="hover:text-white">Case studies</Link></li>
            <li><Link to="/works" className="hover:text-white">Sample dashboards</Link></li>
            <li><Link to="/#quote" className="hover:text-white">Get a quote</Link></li>
            <li><Link to="/experience" className="hover:text-white">Experience</Link></li>
          </ul>
        </div>

        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-brand-300 mb-4">
            Get in touch
          </p>
          <ul className="space-y-2 text-sm">
            <li>
              <a href={site.whatsapp} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 hover:text-white">
                <MessageCircle size={15} /> WhatsApp
              </a>
            </li>
            <li>
              <a href={`mailto:${site.email}`} className="inline-flex items-center gap-2 hover:text-white">
                <Mail size={15} /> {site.email}
              </a>
            </li>
            <li>
              <a href={site.linkedin} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 hover:text-white">
                <Linkedin size={15} /> LinkedIn
              </a>
            </li>
            <li>
              <a href={site.github} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 hover:text-white">
                <Github size={15} /> GitHub
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="container-page py-5 text-xs text-brand-100/60 flex flex-col sm:flex-row gap-2 justify-between">
          <p>© {new Date().getFullYear()} Musab Shaikh. All rights reserved.</p>
          <p>{site.responseTime}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
