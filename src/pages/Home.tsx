// src/pages/Home.tsx
import Hero from "../components/Hero";
import Stats from "../components/Stats";
import Services from "../components/Services";
import Contact from "../components/Contact";
import ClientProjects from "../components/Works";
import Testimonials from "../components/Testimonials";
import About from "../components/About";
import FAQ from "../components/FAQ";
import Skills from "../components/Skills";
import SEO from "../components/SEO";

const Home: React.FC = () => {
  return (
    <main className="min-h-screen">
      <SEO
        title="Power BI Consultant & Mobile App Developer"
        description="Power BI dashboards, Excel trackers, reporting automation and Android & iOS apps for growing businesses in Saudi Arabia, the GCC and worldwide."
        path="/"
      />
      <Hero />
      <Stats />
      <Services />
      <About />
      <Skills />
      <ClientProjects />
      <Testimonials />
      <FAQ />
      <Contact />
    </main>
  );
};

export default Home;
