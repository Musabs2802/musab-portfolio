// src/pages/Home.tsx
import React from 'react';
import Hero from '../components/Hero';
import Technologies from '../components/Technologies';
import Contact from '../components/Contact';
import ClientProjects from '../components/Works';
import Testimonials from '../components/Testimonials';

const Home: React.FC = () => {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <Technologies />
      <ClientProjects />
      <Testimonials />
      <Contact />
    </main>
  );
};

export default Home;
