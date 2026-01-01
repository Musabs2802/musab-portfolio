// src/pages/Home.tsx
import Hero from "../components/Hero";
import Contact from "../components/Contact";
import ClientProjects from "../components/Works";
import Testimonials from "../components/Testimonials";
import About from "../components/About";
import FAQ from "../components/FAQ";
import Skills from "../components/Skills";

const Home: React.FC = () => {
  return (
    <main className="min-h-screen bg-white">
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
