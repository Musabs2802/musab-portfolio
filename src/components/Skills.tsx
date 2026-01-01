import skillCategories from "../data/skills.data";

export default function Skills() {
  return (
    <section className="bg-[#FAFAF8] dark:bg-neutral-950 px-6 py-28">
      <div className="max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-12 text-[#1a1a1a] dark:text-white">
          My Skills & Stack
        </h2>

        <div className="bg-white dark:bg-neutral-900 rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-neutral-800">
                  <th className="text-left py-4 px-6 font-semibold text-gray-600 dark:text-gray-300 text-sm">
                    Category
                  </th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-600 dark:text-gray-300 text-sm">
                    Skills
                  </th>
                </tr>
              </thead>

              <tbody>
                {skillCategories.map((category, index) => (
                  <tr
                    key={index}
                    className="border-b border-gray-100 dark:border-neutral-800 last:border-0"
                  >
                    <td className="py-5 px-6 text-gray-400 font-medium align-top whitespace-nowrap">
                      {category.category}
                    </td>

                    <td className="py-5 px-6">
                      <div className="flex flex-wrap gap-2">
                        {category.skills.map((skill, skillIndex) => (
                          <span
                            key={skillIndex}
                            className="px-3 py-1.5 bg-gray-100 dark:bg-neutral-800 text-gray-700 dark:text-gray-200 rounded-md text-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
