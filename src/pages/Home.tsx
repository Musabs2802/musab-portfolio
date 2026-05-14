// src/pages/Home.tsx
import Hero from "../components/Hero";
import Contact from "../components/Contact";
import ClientProjects from "../components/Works";
import Testimonials from "../components/Testimonials";
import About from "../components/About";
import FAQ from "../components/FAQ";
import Skills from "../components/Skills";
import SEO from "../components/SEO";

const Home: React.FC = () => {
  return (
    <main className="min-h-screen bg-white">
      <SEO
        title="Software Engineer and Data Scientist Portfolio"
        description="Musab Shaikh builds AI applications, analytics dashboards, forecasting systems, and automation tools for business growth. Explore live dashboards and consulting work."
        path="/"
      />
      <Hero />
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
