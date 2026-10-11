// src/pages/Home.tsx
import Hero from "../components/Hero";
import Stats from "../components/Stats";
import Services from "../components/Services";
import CaseStudies from "../components/CaseStudies";
import Works from "../components/Works";
import Process from "../components/Process";
import Quote from "../components/Quote";
import About from "../components/About";
import FAQ from "../components/FAQ";
import Contact from "../components/Contact";
import SEO from "../components/SEO";

const Home: React.FC = () => {
  return (
    <main className="min-h-screen">
      <SEO />
      <Hero />
      <Stats />
      <Services />
      <CaseStudies />
      <Works />
      <Process />
      <Quote />
      <About />
      <FAQ />
      <Contact />
    </main>
  );
};

export default Home;
