import { getAllSkills, getSkill, getSkillFileContent } from '@/lib/skills'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import CopyButton from '@/components/CopyButton'

export async function generateStaticParams() {
  const skills = getAllSkills()
  return skills.map((s) => ({ slug: s.slug }))
}

export default async function SkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const skill = getSkill(slug)
  if (!skill) notFound()

  const repoUrl = process.env.NEXT_PUBLIC_REPO_URL || 'https://github.com/YOUR_USER/skills-catalog'
  const installCmd = `git clone --depth 1 --filter=blob:none --sparse ${repoUrl}.git /tmp/_sc && git -C /tmp/_sc sparse-checkout set skills/${slug} && cp -r /tmp/_sc/skills/${slug} ~/.claude/skills/ && rm -rf /tmp/_sc`

  const skillMdContent = getSkillFileContent(slug, 'SKILL.md')

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <div className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center gap-3">
          <Link href="/" className="text-gray-500 hover:text-white transition-colors text-sm">
            ← Каталог
          </Link>
          <span className="text-gray-700">/</span>
          <span className="text-gray-300 text-sm font-mono">{skill.name}</span>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-10 space-y-8">
        {/* Title */}
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-white">{skill.name}</h1>
            <span className="text-indigo-400 font-mono text-sm bg-indigo-950 px-2 py-1 rounded-md">/{slug}</span>
          </div>
          <p className="text-gray-400 leading-relaxed max-w-2xl text-sm">
            {skill.description.split('.')[0]}.
          </p>
        </div>

        {/* Install box */}
        <div className="bg-gray-900 border border-indigo-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-indigo-300 uppercase tracking-wide">Установка</h2>
            <CopyButton text={installCmd} />
          </div>
          <code className="text-xs text-green-400 font-mono block bg-gray-950 rounded-lg p-4 overflow-x-auto whitespace-pre-wrap break-all leading-relaxed">
            {installCmd}
          </code>
          <p className="text-gray-500 text-xs mt-3">
            Скопируй команду → вставь в терминал → перезапусти Claude Code
          </p>
        </div>

        {/* Files list */}
        <div>
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
            Файлы ({skill.files.length})
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {skill.files.map((file) => (
              <div key={file} className="bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-sm font-mono text-gray-300 flex items-center gap-2">
                <span className="text-gray-600">📄</span>
                {file}
              </div>
            ))}
          </div>
        </div>

        {/* SKILL.md preview */}
        {skillMdContent && (
          <div>
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Содержимое SKILL.md
            </h2>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <pre className="text-gray-300 text-xs font-mono whitespace-pre-wrap leading-relaxed overflow-x-auto max-h-96 overflow-y-auto">
                {skillMdContent.slice(0, 2000)}
                {skillMdContent.length > 2000 ? '\n\n... (сокращено)' : ''}
              </pre>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
