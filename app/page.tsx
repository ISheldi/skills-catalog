import { getAllSkills, type Skill } from '@/lib/skills'
import Link from 'next/link'

export default function HomePage() {
  const skills = getAllSkills()

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <div className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">🧠 Skills Catalog</h1>
            <p className="text-gray-400 text-sm mt-1">Личный каталог скиллов для Claude Code</p>
          </div>
          <Link
            href="/upload"
            className="bg-indigo-600 hover:bg-indigo-500 transition-colors text-white text-sm font-medium px-4 py-2 rounded-lg"
          >
            + Добавить скилл
          </Link>
        </div>
      </div>

      {/* Stats bar */}
      <div className="max-w-5xl mx-auto px-6 pt-8 pb-2">
        <p className="text-gray-500 text-sm">{skills.length} скиллов в каталоге</p>
      </div>

      {/* Skills grid */}
      <div className="max-w-5xl mx-auto px-6 py-4">
        {skills.length === 0 ? (
          <div className="text-center py-24 text-gray-500">
            <p className="text-4xl mb-4">📭</p>
            <p className="text-lg">Скиллов пока нет</p>
            <p className="text-sm mt-2">Добавь первый скилл через кнопку выше</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {skills.map((skill) => (
              <SkillCard key={skill.slug} skill={skill} />
            ))}
          </div>
        )}
      </div>
    </main>
  )
}

function SkillCard({ skill }: { skill: Skill }) {
  return (
    <Link href={`/skills/${skill.slug}`}>
      <div className="bg-gray-900 border border-gray-800 hover:border-indigo-500 transition-all rounded-xl p-5 cursor-pointer group h-full">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <h2 className="font-semibold text-white group-hover:text-indigo-300 transition-colors">
              {skill.name}
            </h2>
            <p className="text-gray-400 text-sm mt-2 line-clamp-3 leading-relaxed">
              {skill.description.slice(0, 150)}
              {skill.description.length > 150 ? '...' : ''}
            </p>
          </div>
          <span className="text-indigo-400 text-xl mt-0.5 group-hover:translate-x-1 transition-transform shrink-0">→</span>
        </div>
        <div className="mt-4 flex items-center gap-3">
          <span className="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded-md">
            📄 {skill.files.length} файлов
          </span>
          <span className="text-xs text-indigo-400 font-mono bg-indigo-950 px-2 py-1 rounded-md">
            /{skill.slug}
          </span>
        </div>
      </div>
    </Link>
  )
}
