import React from "react";

const stats = [
  { value: "$700M+", label: "yearly revenue covered by my Power BI reports" },
  { value: "250+", label: "people use my dashboards every day, CEO to field sales" },
  { value: "~$590K", label: "a month in growth opportunities found by my ML model" },
  { value: "83%", label: "less time spent on daily reporting after automation" },
];

const Stats: React.FC = () => {
  return (
    <section className="bg-brand-900 text-white">
      <div className="container-page py-14 md:py-16">
        <dl className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-10">
          {stats.map(({ value, label }) => (
            <div key={value} className="border-l border-white/15 pl-5">
              <dt className="sr-only">{label}</dt>
              <dd className="font-heading text-3xl md:text-4xl font-semibold tracking-tight">
                {value}
              </dd>
              <dd className="mt-2 text-sm text-brand-100/80 leading-snug">
                {label}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
};

export default Stats;
