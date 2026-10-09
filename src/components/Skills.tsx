import skillCategories from "../data/skills.data";

export default function Skills() {
  return (
    <section className="mt-20">
      <p className="eyebrow mb-3">Toolkit</p>
      <h2 className="section-title mb-8">Skills &amp; tools</h2>

      <div className="rounded-2xl bg-white border border-sand-300 divide-y divide-sand-200">
        {skillCategories.map(({ category, skills }) => (
          <div
            key={category}
            className="grid sm:grid-cols-[200px_1fr] gap-3 sm:gap-6 px-6 py-5"
          >
            <p className="text-sm font-semibold text-ink pt-1">{category}</p>
            <div className="flex flex-wrap gap-2">
              {skills.map((skill) => (
                <span key={skill} className="chip">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
