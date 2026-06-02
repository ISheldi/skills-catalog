import Link from 'next/link'

export default function UploadPage() {
  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <div className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center gap-3">
          <Link href="/" className="text-gray-500 hover:text-white transition-colors text-sm">
            ← Каталог
          </Link>
          <span className="text-gray-700">/</span>
          <span className="text-gray-300 text-sm">Добавить скилл</span>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-10 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Добавить скилл</h1>
          <p className="text-gray-400 text-sm mt-2">Скиллы хранятся в папке <code className="text-indigo-400">/skills</code> в репозитории</p>
        </div>

        <div className="space-y-4">
          {/* Step 1 */}
          <Step
            number="1"
            title="Подготовь папку скилла"
            description={`Структура:\nskills/\n  мой-скилл/\n    SKILL.md   ← обязательно\n    role.md\n    part1.md\n    ...`}
            code
          />

          {/* Step 2 */}
          <Step
            number="2"
            title="SKILL.md должен содержать frontmatter"
            description={`---\nname: "Название скилла"\ndescription: "Описание что делает скилл. Используй когда..."\n---\n\n# Остальной контент скилла...`}
            code
          />

          {/* Step 3 */}
          <Step
            number="3"
            title="Добавь в репозиторий"
            description={`git clone <repo-url>\ncp -r ~/мой-скилл skills/\ngit add skills/мой-скилл\ngit commit -m "add: мой-скилл"\ngit push`}
            code
          />

          {/* Step 4 */}
          <Step
            number="4"
            title="Vercel задеплоит автоматически"
            description="После push в main — Vercel пересоберёт сайт и скилл появится в каталоге через ~1 минуту."
          />
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-indigo-300 mb-2">💡 Быстрый способ</h3>
          <p className="text-gray-400 text-sm">
            Если скилл уже установлен локально в <code className="text-indigo-400">~/.claude/skills/</code> — просто скопируй папку в репозиторий:
          </p>
          <code className="text-xs text-green-400 font-mono block bg-gray-950 rounded-lg p-3 mt-3 overflow-x-auto">
            cp -r ~/.claude/skills/мой-скилл ~/skills-catalog/skills/
          </code>
        </div>
      </div>
    </main>
  )
}

function Step({ number, title, description, code = false }: {
  number: string
  title: string
  description: string
  code?: boolean
}) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 flex gap-4">
      <div className="shrink-0 w-7 h-7 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold text-white">
        {number}
      </div>
      <div className="flex-1 min-w-0">
        <h3 className="font-semibold text-white text-sm">{title}</h3>
        {code ? (
          <pre className="text-xs text-gray-300 font-mono mt-2 bg-gray-950 rounded-lg p-3 overflow-x-auto whitespace-pre-wrap">
            {description}
          </pre>
        ) : (
          <p className="text-gray-400 text-sm mt-1">{description}</p>
        )}
      </div>
    </div>
  )
}
