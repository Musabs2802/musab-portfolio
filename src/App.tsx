import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Experience from './components/Experience';
import ClientProjects from './components/ClientProjects';
import PersonalProjects from './components/PersonalProjects';
import Contact from './components/Contact';
import Technologies from './components/Technologies';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <Hero />
      <Technologies />
      <Experience />
      <ClientProjects />
      <PersonalProjects />
      <Contact />
    </div>
  );
}

export default App;