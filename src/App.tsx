// src/App.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Work from './pages/Works';
import Projects from './pages/Projects';
import Experience from './pages/Experience';
import Contact from './pages/Contact';
// import Projects, Experience, Contact pages if you create them separately

function App() {
  return (
    <>
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/works" element={<Work />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/experience" element={<Experience />} />
        <Route path="/contact" element={<Contact />} />
        {/* Add other routes here like Projects, Experience, Contact */}
      </Routes>
    </>
  );
}

export default App;
