interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  period: string;
  responsibilities: string[];
  logo: string;
  logoColor: string;
}

const jobs: Job[] = [
  {
    id: 1,
    title: "Software Engineer",
    company: "Octopusx",
    location: "Chittagong, Bangladesh",
    period: "Apr 2023 - Apr 2025",
    responsibilities: [
      "Built and maintained backend systems and project architecture using a monorepo for multiple apps.",
      "Led front and back-end teams, handled task distribution, code reviews, and made key tech decisions.",
      "Designed ERDs, planned flows, and built scalable database schemas for performance and reliability.",
      "Managed 20+ projects in one codebase, keeping collaboration smooth and development consistent.",
    ],
    logo: "O",
    logoColor: "bg-red-500",
  },
  {
    id: 2,
    title: "Full Stack Developer",
    company: "Monster Studio",
    location: "Chittagong, Bangladesh",
    period: "Jan 2023 - Apr 2023",
    responsibilities: [
      "Handled MongoDB indexing, search, filter, and pagination using Atlas Search; optimized DB structure.",
      "Integrated Cloudflare R2, Meilsearch, Mailgun, Stripe, PayPal, and real-time notifications.",
      "Built bulk file/video upload & download, responsive dashboards, and analytics tracking.",
    ],
    logo: "M",
    logoColor: "bg-green-500",
  },
];

export default function Experience() {
  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-5xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-12 text-[#1a1a1a]">
          Where I've Worked
        </h2>
        <div className="space-y-5">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-5">
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-1">
                    {job.title}
                  </h3>
                  <p className="text-sm text-gray-500">{job.period}</p>
                </div>
                <div
                  className={`w-11 h-11 rounded-lg ${job.logoColor} flex items-center justify-center text-white font-bold flex-shrink-0`}
                >
                  {job.logo}
                </div>
              </div>
              <ul className="space-y-2.5 mb-5">
                {job.responsibilities.map((responsibility, index) => (
                  <li
                    key={index}
                    className="flex gap-3 text-[15px] text-gray-600 leading-relaxed"
                  >
                    <span className="text-gray-400 mt-0.5">•</span>
                    <span>{responsibility}</span>
                  </li>
                ))}
              </ul>
              <div className="flex items-center gap-2.5 pt-4 border-t border-gray-100">
                <div
                  className={`w-6 h-6 rounded ${job.logoColor} flex items-center justify-center text-white text-xs font-bold`}
                >
                  {job.logo}
                </div>
                <div>
                  <div className="font-semibold text-gray-900 text-sm">
                    {job.company}
                  </div>
                  <div className="text-xs text-gray-500">{job.location}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
