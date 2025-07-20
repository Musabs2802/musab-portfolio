import { SimpleIcon } from "simple-icons";

export interface Experience {
  title: string;
  company: string;
  location: string;
  period: string;
  description: string[];
  technologies: string[];
}

export interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  category: 'Software' | 'Data Science' | 'Analysis';
  github?: string;
  demo?: string;
  highlights: string;
}

export interface Work {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  category: 'Software' | 'Data Science' | 'Analysis';
  client: string;
  results: string;
}

export interface Technology {
  name: string;
  icon: SimpleIcon;
  category: 'Frontend' | 'Language' | 'Backend' | 'Data' | 'Visualization' | 'ML' | 'Tools' | 'Database' | 'Cloud';
}