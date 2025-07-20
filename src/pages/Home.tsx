// src/pages/Home.tsx
import React from 'react';
import Hero from '../components/Hero';
import Technologies from '../components/Technologies';
import Experience from '../components/Experience';
import PersonalProjects from '../components/Projects';
import Contact from '../components/Contact';
import ClientProjects from '../components/Works';

const Home: React.FC = () => {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <Technologies />
      <ClientProjects />
      <Contact />
    </main>
  );
};

export default Home;
