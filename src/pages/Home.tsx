// src/pages/Home.tsx
import React from 'react';
import Hero from '../components/Hero';
import Technologies from '../components/Technologies';
import Experience from '../components/Experience';
import PersonalProjects from '../components/PersonalProjects';
import Contact from '../components/Contact';
import ClientProjects from '../components/ClientProjects';

const Home: React.FC = () => {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <Technologies />
      <Experience />
      <ClientProjects />
      <Contact />
    </main>
  );
};

export default Home;
