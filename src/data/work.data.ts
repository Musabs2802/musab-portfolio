import { Work } from "../types";

const workData: Work[] = [
    {
      id: 1,
      title: "MBVS Networking App",
      description: "Built for professionals in Switzerland to network, find services, attend events, and apply for jobs — all in one intuitive app.",
      image: "https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Flutter", "iOS", "Android"],
      category: "Software",
      client: "MBVS | Switzerland",
      results: "Featured amongst Swiss community; praised for its user-friendly design and all-in-one utility"
    },
    {
      id: 2,
      title: "Bubble Care Health Tech App",
      description: "A healthcare app connecting patients and caregivers for daily activity tracking, built for a UK startup in collaboration with the NHS.",
      image: "https://images.pexels.com/photos/590022/pexels-photo-590022.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Android", "iOS", "Kotlin", "Swift"],
      category: "Software",
      client: "Tritone Health | UK",
      results: "Received positive feedback from both patients and caregivers for intuitive design and reliability"
    },
    {
      id: 3,
      title: "Automation System at Al Kabeer Group",
      description: "Automated sales & finance workflows for Al Kabeer using Python, reducing manual effort and enabling faster, data-driven decision-making.",
      image: "https://images.pexels.com/photos/586103/pexels-photo-586103.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "Excel", "Cloud"],
      category: "Software",
      client: "Al Kabeer Group | UAE",
      results: "Saved 200+ man-hours monthly by automating reporting, improving accuracy and enabling real-time sales insights for faster executive decisions"
    },
    {
      id: 4,
      title: "Customer Propensity Model",
      description: "Build a Machine Learning model based on historical sales to predict what customers would by which skus in the next month",
      image: "https://images.pexels.com/photos/4164418/pexels-photo-4164418.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["Python", "Machine Learning", "AWS"],
      category: "Data Science",
      client: "Seara | KSA",
      results: "Achieved 65% prediction accuracy, enabling targeted sales campaigns and increasing monthly SKU lift by 20%"
    },
    {
      id: 5,
      title: "Sales Analytics Dashboard",
      description: "Designed and developed an advanced sales analytics dashboard using Power BI and complex DAX, replicating Coca-Cola’s sales intelligence model to deliver deep insights for stakeholders, sales managers, and supervisors.",
      image: "https://images.pexels.com/photos/590020/pexels-photo-590020.jpeg?auto=compress&cs=tinysrgb&w=600",
      technologies: ["PowerBi", "SQL", "Excel"],
      category: "Analysis",
      client: "Seara | KSA",
      results: "Enabled data-driven decision-making across all sales tiers; improved visibility into KPIs and sales trends, reducing reporting turnaround time by 80%"
    }
  ];

export default workData;