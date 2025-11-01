import {
  AppleIcon,
  BarChart,
  CloudLightning,
  Code,
  Globe,
  LayoutTemplate,
} from "lucide-react";
import React from "react";

const Features: React.FC = () => {
  // Features data
  const getFeatures = () => [
    {
      title: "Web Development",
      description:
        "Build fast, responsive, and scalable websites using React, Next.js, and Tailwind CSS.",
      icon: <Globe className="w-6 h-6 text-white" />,
    },
    {
      title: "Mobile App Development",
      description:
        "Develop cross-platform apps with React Native or Flutter that deliver native performance.",
      icon: <AppleIcon className="w-6 h-6 text-white" />,
    },
    {
      title: "Data Science",
      description:
        "Harness the power of data with analytics, forecasting, and machine learning models.",
      icon: <BarChart className="w-6 h-6 text-white" />,
    },
    {
      title: "Automation Solutions",
      description:
        "Streamline workflows and reduce manual effort with custom automation and RPA tools.",
      icon: <CloudLightning className="w-6 h-6 text-white" />,
    },
    {
      title: "Power BI Dashboards",
      description:
        "Turn data into actionable insights with stunning Power BI dashboards tailored for your business.",
      icon: <LayoutTemplate className="w-6 h-6 text-white" />,
    },
    {
      title: "Custom Software",
      description:
        "Create custom software solutions for unique business needs — from CRM systems to ERP tools.",
      icon: <Code className="w-6 h-6 text-white" />,
    },
  ];

  const items = getFeatures();

  return (
    <section
      id="technologies"
      className="py-16 bg-white relative overflow-hidden"
    >
      <div className="max-w-6xl mx-auto px-6 relative z-10">
        {/* Header */}
        <div className="mb-8 md:mx-auto md:mb-12 text-center">
          <p className="text-base text-primary-700 font-bold tracking-wide uppercase mb-2">
            Features
          </p>

          <h2 className="font-bold leading-tighter tracking-tighter text-4xl md:text-5xl text-gray-900">
            What you get with me
          </h2>

          <p className="mt-4 text-gray-500 max-w-2xl mx-auto text-lg">
            Tools and frameworks that power our software engineering and data
            science projects.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid mx-auto gap-8 md:gap-y-12 lg:grid-cols-2 sm:grid-cols-2">
          {items.map(({ title, description, icon }, index) => (
            <div key={index} className="flex items-start gap-4 p-6">
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-primary-700 text-white">
                {icon}
              </div>
              <div>
                <h3 className="text-xl font-bold">{title}</h3>
                <p className="mt-1 text-gray-600 font-extralight">
                  {description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
