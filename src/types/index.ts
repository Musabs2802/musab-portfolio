export interface Experience {
  title: string;
  company: string;
  companyNote?: string;
  location: string;
  period: string;
  description: string[];
  technologies: string[];
}

export interface Work {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  category: "Software" | "Data Science" | "Analysis" | "Dashboard";
  client: string;
  results: string;
  demo?: string;
}
