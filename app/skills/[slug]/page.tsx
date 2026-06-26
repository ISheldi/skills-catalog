import { getAllSkills, getSkill, getSkillFileTree } from '@/lib/skills'
import { SKILL_META, SKILL_ABOUT, CATEGORY_EMOJI, type Category } from '@/lib/config'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import CopyButton from '@/components/CopyButton'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export async function generateStaticParams() {
  const skills = getAllSkills()
  return skills.map((s) => ({ slug: s.slug }))
}

export default async function SkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const skill = getSkill(slug)
  if (!skill) notFound()

  const meta = SKILL_META[slug]
  const displayName = meta?.displayName || skill.name
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://skills-catalog-tau.vercel.app'
  const installCmd = `curl -fsSL ${siteUrl}/api/install/${slug} | bash`
  const about = SKILL_ABOUT[slug] || ''
  const allFiles = getSkillFileTree(slug)

  // Медиа-файлы скилла (картинки/видео) — показываем галереей, чтобы их можно было увидеть
  const IMG_RE = /\.(png|jpe?g|gif|webp|svg|avif)$/i
  const VID_RE = /\.(mp4|webm|mov)$/i
  const encodePath = (p: string) => p.split('/').map(encodeURIComponent).join('/')
  const mediaFiles = allFiles.filter((f) => IMG_RE.test(f) || VID_RE.test(f))
  const images = mediaFiles.filter((f) => IMG_RE.test(f))
  const videos = mediaFiles.filter((f) => VID_RE.test(f))

  // Чистое описание: meta.desc приоритетно, иначе первое русское предложение
  let intro = meta?.desc || ''
  if (!intro) {
    const sentences = skill.description.split(/[.!?\n]/).map(s => s.trim()).filter(s => s.length > 10)
    intro = sentences.find(s => /[а-яёА-ЯЁ]/.test(s)) || sentences[0] || ''
  }

  return (
    <main className="min-h-screen bg-[#0a0a0c] text-white font-sans">

      {/* Top nav */}
      <div className="sticky top-0 z-10 bg-[#0a0a0c]/85 backdrop-blur-md border-b border-white/[0.07]">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm">
            <Link href="/" className="text-gray-500 hover:text-gray-200 transition-colors">Каталог</Link>
            <span className="text-gray-700">/</span>
            <span className="text-gray-200 font-medium">{displayName}</span>
          </div>
          <Link
            href="/"
            className="flex items-center gap-1.5 text-gray-400 hover:text-white hover:bg-white/[0.06] transition-all text-sm px-3 py-1.5 rounded-lg"
          >
            <span className="text-base leading-none">←</span> Назад
          </Link>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 pt-12 pb-24 space-y-8">

        {/* Title */}
        <div>
          <div className="flex items-center gap-3 mb-3 flex-wrap">
            <h1 className="text-[2.75rem] leading-tight font-black tracking-tight text-white">{displayName}</h1>
            {meta?.category && <CategoryBadge cat={meta.category} />}
          </div>
          <div className="flex items-center gap-3">
            <code className="text-indigo-300 font-mono text-sm bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-1 rounded-lg">
              /{slug}
            </code>
            {meta?.date && <span className="text-gray-600 text-sm">{meta.date}</span>}
          </div>
          {intro && <p className="text-gray-400 leading-relaxed mt-5 text-lg">{intro}.</p>}
        </div>

        {/* Install */}
        <div className="bg-white/[0.03] border border-indigo-500/20 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xs font-bold text-indigo-400 uppercase tracking-widest">Установка</h2>
            <CopyButton text={installCmd} />
          </div>
          <code className="text-sm text-emerald-400 font-mono block bg-black/40 rounded-xl px-5 py-4 overflow-x-auto whitespace-pre-wrap break-all leading-relaxed">
            {installCmd}
          </code>
          <p className="text-gray-600 text-xs mt-3">
            Скопируй команду → вставь в терминал → перезапусти Claude Code
          </p>
        </div>

        {/* Files */}
        <div>
          <h2 className="text-xs font-bold text-gray-600 uppercase tracking-widest mb-3">
            Файлы ({allFiles.length})
          </h2>
          <div className="flex flex-wrap gap-2">
            {allFiles.slice(0, 24).map((file) => (
              <span
                key={file}
                className="bg-white/[0.04] border border-white/[0.07] rounded-lg px-3 py-1.5 text-sm font-mono text-gray-400"
              >
                {file}
              </span>
            ))}
            {allFiles.length > 24 && (
              <span className="text-gray-600 text-sm px-2 py-1.5">+{allFiles.length - 24}</span>
            )}
          </div>
        </div>

        {/* Галерея медиа — картинки и видео скилла */}
        {mediaFiles.length > 0 && (
          <div>
            <h2 className="text-xs font-bold text-gray-600 uppercase tracking-widest mb-4">
              Примеры — картинки и видео ({mediaFiles.length})
            </h2>

            {videos.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                {videos.map((file) => (
                  <figure key={file} className="bg-white/[0.02] border border-white/[0.07] rounded-xl overflow-hidden">
                    <video
                      controls
                      preload="none"
                      className="w-full h-auto bg-black"
                      src={`/api/skills/${slug}/${encodePath(file)}`}
                    />
                    <figcaption className="text-gray-500 text-xs font-mono px-3 py-2 truncate">
                      {file.split('/').pop()}
                    </figcaption>
                  </figure>
                ))}
              </div>
            )}

            {images.length > 0 && (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {images.map((file) => (
                  <a
                    key={file}
                    href={`/api/skills/${slug}/${encodePath(file)}`}
                    target="_blank"
                    rel="noreferrer"
                    className="group block bg-white/[0.02] border border-white/[0.07] rounded-xl overflow-hidden hover:border-white/[0.2] transition-colors"
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      loading="lazy"
                      alt={file.split('/').pop() || file}
                      className="w-full h-40 object-cover bg-black/40"
                      src={`/api/skills/${slug}/${encodePath(file)}`}
                    />
                    <div className="text-gray-500 text-[11px] font-mono px-2.5 py-1.5 truncate group-hover:text-gray-300">
                      {file.split('/').pop()}
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Что делает скилл — на русском */}
        {about && (
          <div>
            <h2 className="text-xs font-bold text-gray-600 uppercase tracking-widest mb-4">Что делает</h2>
            <div className="bg-white/[0.02] border border-white/[0.06] rounded-2xl px-7 py-6">
              <article className="skill-md">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{about}</ReactMarkdown>
              </article>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}

function CategoryBadge({ cat }: { cat: Category }) {
  const styles: Record<Category, string> = {
    'Аудитория': 'bg-amber-500 text-white',
    'Продукт':   'bg-red-500 text-white',
    'Контент':   'bg-teal-500 text-white',
    'Воронки':   'bg-violet-600 text-white',
    'Продажи':   'bg-yellow-500 text-black',
    'SEO':       'bg-cyan-600 text-white',
    'CRO':       'bg-orange-500 text-white',
    'Разработка':'bg-zinc-600 text-white',
    'Дизайн':    'bg-pink-500 text-white',
    'Изображения':'bg-fuchsia-500 text-white',
    'Видео':     'bg-rose-500 text-white',
  }
  return (
    <span className={`inline-block text-[13px] font-semibold px-3 py-1 rounded-md ${styles[cat]}`}>
      {CATEGORY_EMOJI[cat]} {cat}
    </span>
  )
}
