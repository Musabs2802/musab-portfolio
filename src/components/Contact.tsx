import React from "react";
import { Link } from "react-router-dom";

const Contact: React.FC = () => {
  return (
    <section className="bg-[#f8f6f3] px-6 py-28">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-3xl shadow-sm p-10 md:p-14 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-5">
            Ready to Build Something Great?
          </h2>
          <p className="text-lg text-neutral-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            Let's discuss your project and create a solution that meets your
            needs. I'm always excited to take on new challenges.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/contact"
              className="inline-flex items-center justify-center gap-2 px-7 py-3 rounded-xl bg-neutral-900 text-white font-medium shadow-sm hover:opacity-90 transition"
            >
              Get In Touch
            </Link>
            <Link
              to="/works"
              className="inline-flex items-center justify-center gap-2 px-7 py-3 rounded-xl border border-neutral-300 text-neutral-900 font-medium hover:bg-neutral-100 transition"
            >
              View My Work
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
