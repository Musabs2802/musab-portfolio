// src/pages/Home.tsx
import Hero from "../components/Hero";
import Technologies from "../components/Technologies";
import Contact from "../components/Contact";
import ClientProjects from "../components/Works";
import Testimonials from "../components/Testimonials";
import { InfoIcon } from "lucide-react";
import Services from "../components/Features";

const Home: React.FC = () => {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <section className="bg-primary-50 dark:bg-slate-800 not-prose mb-5">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 text-md text-center font-medium">
          <InfoIcon className="w-5 h-5 inline-block align-text-bottom font-bold mx-2" />
          <span className="font-bold">Philosophy: </span>
          <span className="font-thin">
            Simplicity, Best Practices and High Performance
          </span>
        </div>
      </section>
      <Services />
      <Technologies />
      <ClientProjects />
      <Testimonials />
      <Contact />
    </main>
  );
};

export default Home;
