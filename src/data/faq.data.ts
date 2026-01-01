interface FAQItem {
  id: number;
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    id: 1,
    question: "What kind of projects do you usually work on?",
    answer:
      "I typically work on web and data projects—everything from interactive dashboards analyzing tens of thousands of records to full-stack web apps and e-commerce platforms. I focus on both intuitive interfaces and scalable backend logic.",
  },
  {
    id: 2,
    question: "Do you help with project planning and architecture?",
    answer:
      "Yes! I design system architectures, create ERDs, plan tech stacks, and structure codebases for scalability and maintainability. I’ve architected solutions handling millions of rows of data and multiple user roles efficiently.",
  },
  {
    id: 3,
    question: "Can you handle both front-end and backend?",
    answer:
      "Absolutely. I work across the full stack—from responsive UIs with React to REST APIs, database modeling, and data pipelines. I ensure smooth integration and performance across the entire system.",
  },
  {
    id: 4,
    question: "How soon can you start?",
    answer:
      "I’m usually ready to start within a week, depending on project complexity. I like to align on goals and deliverables before jumping in to ensure a smooth kickoff.",
  },
  {
    id: 5,
    question: "How do you usually work with clients or teams?",
    answer:
      "I prioritize clear, regular communication. I use Slack, email, or video calls to share progress, discuss challenges, and ensure the solution meets business objectives. Collaboration and transparency are key.",
  },
];

export default faqs;
