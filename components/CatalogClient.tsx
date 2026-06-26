'use client'

import { useState } from 'react'
import Link from 'next/link'
import { PIPELINE, CATEGORIES, CATEGORY_EMOJI, CATEGORY_COLOR, SKILL_META, SKILL_ORDER, type Category } from '@/lib/config'
import type { Skill } from '@/lib/skills'

interface Props {
  skills: Skill[]
}

export default function CatalogClient({ skills }: Props) {
  const [activeCategory, setActiveCategory] = useState<'Все' | Category>('Все')
  const [showPipeline, setShowPipeline] = useState(false)

  // Группируем по категории + сортируем внутри по логическому порядку
  const grouped: Record<string, Skill[]> = {}
  for (const skill of skills) {
    const meta = SKILL_META[skill.slug]
    const cat = meta?.category || 'Разработка'
    if (!grouped[cat]) grouped[cat] = []
    grouped[cat].push(skill)
  }
  for (const cat of Object.keys(grouped)) {
    grouped[cat].sort((a, b) => (SKILL_ORDER[a.slug] ?? 999) - (SKILL_ORDER[b.slug] ?? 999))
  }

  const filteredCategories = activeCategory === 'Все' ? [...CATEGORIES] : [activeCategory]

  return (
    <main className="min-h-screen bg-[#0a0a0c] text-white font-sans">

      {/* Header */}
      <div className="pt-20 pb-4 text-center px-4">
        <h1 className="text-[5rem] leading-[1.05] font-black text-white tracking-tight">
          Мои виртуальные сотрудники
        </h1>
        <p className="text-gray-400 mt-5 text-lg tracking-wide">
          Личный каталог скиллов для Claude Code
        </p>
      </div>

      {/* Pipeline toggle */}
      <div className="flex justify-center mt-10 mb-8">
        <button
          onClick={() => setShowPipeline(!showPipeline)}
          className="flex items-center gap-2 text-[15px] text-gray-300 bg-[#1a1a1e] hover:bg-[#222226] border border-white/[0.1] px-6 py-3 rounded-full transition-all"
        >
          <span className="text-xs opacity-70">⊙</span>
          {showPipeline ? 'Скрыть Pipeline' : 'Показать Pipeline'}
        </button>
      </div>

      {/* Pipeline */}
      {showPipeline && (
        <div className="max-w-[1200px] mx-auto px-6 mb-12">
          <div className="flex items-start justify-between gap-3">
            {PIPELINE.map((stage, i) => (
              <div key={stage.label} className="flex items-start gap-3 flex-1 min-w-0">
                <div className="bg-[#141416] border border-white/[0.08] rounded-2xl p-5 w-full">
                  <div className="text-[11px] font-bold text-gray-500 uppercase tracking-[0.12em] mb-4 flex items-center gap-1.5">
                    <span>{stage.emoji}</span> {stage.label}
                  </div>
                  <div className="flex flex-col gap-2">
                    {stage.skills.map(slug => {
                      const meta = SKILL_META[slug]
                      return (
                        <Link key={slug} href={`/skills/${slug}`}>
                          <div className={`text-[12px] font-semibold px-3 py-2.5 rounded-xl cursor-pointer transition-all text-center leading-snug ${
                            meta?.featured
                              ? 'bg-amber-500/15 text-amber-300 hover:bg-amber-500/25 border border-amber-500/20'
                              : 'bg-white/[0.04] text-gray-300 hover:bg-white/[0.09] border border-white/[0.06]'
                          }`}>
                            {meta?.featured && '⭐ '}{meta?.displayName || slug}
                          </div>
                        </Link>
                      )
                    })}
                  </div>
                </div>
                {i < PIPELINE.length - 1 && (
                  <div className="text-gray-700 text-lg mt-10 shrink-0">→</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="max-w-[1180px] mx-auto px-6 mb-7">
        <div className="flex gap-2 flex-wrap items-center">
          {(['Все', ...CATEGORIES] as const).map(cat => {
            const count = cat === 'Все' ? skills.length : (grouped[cat]?.length || 0)
            return (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat as 'Все' | Category)}
                className={`text-[15px] px-4 py-2 rounded-full transition-all font-medium flex items-center gap-1.5 ${
                  activeCategory === cat
                    ? 'bg-white text-[#0a0a0c] font-semibold'
                    : 'text-gray-400 border border-white/[0.1] hover:border-white/[0.2] hover:text-gray-200'
                }`}
              >
                {cat}
                <span className={`text-xs ${activeCategory === cat ? 'text-gray-500' : 'text-gray-600'}`}>{count}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Table — translucent container */}
      <div className="max-w-[1180px] mx-auto px-6 pb-28">
        <div className="bg-white/[0.025] border border-white/[0.08] rounded-3xl px-8 py-4 backdrop-blur-sm">
          <table className="w-full table-fixed border-collapse">
            <colgroup>
              <col style={{ width: '280px' }} />
              <col />
              <col style={{ width: '130px' }} />
              <col style={{ width: '70px' }} />
              <col style={{ width: '40px' }} />
            </colgroup>
            <thead>
              <tr className="border-b border-white/[0.08]">
                <th className="py-5 text-left text-[12px] font-semibold text-gray-500 uppercase tracking-[0.1em]">Инструмент</th>
                <th className="py-5 text-left text-[12px] font-semibold text-gray-500 uppercase tracking-[0.1em] pl-4">Описание</th>
                <th className="py-5 text-right text-[12px] font-semibold text-gray-500 uppercase tracking-[0.1em]">Тема</th>
                <th className="py-5 text-right text-[12px] font-semibold text-gray-500 uppercase tracking-[0.1em]">Дата</th>
                <th className="py-5"></th>
              </tr>
            </thead>
            <tbody>
              {filteredCategories.map(cat => {
                const catSkills = grouped[cat]
                if (!catSkills?.length) return null
                return (
                  <>
                    {/* Category header — bold + colored + count */}
                    <tr key={`hdr-${cat}`}>
                      <td colSpan={5} className="pt-9 pb-3">
                        <span className={`text-lg font-extrabold ${CATEGORY_COLOR[cat]}`}>
                          {CATEGORY_EMOJI[cat]} {cat}
                        </span>
                        <span className="text-gray-600 text-sm font-medium ml-2">{catSkills.length}</span>
                      </td>
                    </tr>

                    {catSkills.map(skill => {
                      const meta = SKILL_META[skill.slug]
                      // Описание: meta.desc (русское) приоритетнее, иначе из SKILL.md
                      let desc = meta?.desc || ''
                      if (!desc) {
                        const sentences = skill.description.split(/[.!?\n]/).map(s => s.trim()).filter(s => s.length > 10)
                        desc = sentences.find(s => /[а-яёА-ЯЁ]/.test(s)) || sentences[0] || ''
                      }
                      // запасная обрезка только для аномально длинных (нет meta.desc)
                      if (desc.length > 90) desc = desc.slice(0, 90) + '...'

                      return (
                        <tr
                          key={skill.slug}
                          className="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.03] transition-colors cursor-pointer group"
                          onClick={() => { window.location.href = `/skills/${skill.slug}` }}
                        >
                          {/* Name — white, medium weight */}
                          <td className="py-4 pr-4">
                            <span className={`text-[16px] whitespace-nowrap ${
                              meta?.featured ? 'text-amber-300 font-bold' : 'text-white font-medium'
                            }`}>
                              {meta?.featured && '⭐ '}{meta?.displayName || skill.name}
                            </span>
                          </td>

                          {/* Description */}
                          <td className="py-4 pl-4 pr-4">
                            <span className="text-gray-400 text-[15px] whitespace-nowrap block overflow-hidden text-ellipsis">
                              {desc}
                            </span>
                          </td>

                          {/* Badge */}
                          <td className="py-4 text-right">
                            <CategoryBadge cat={cat} />
                          </td>

                          {/* Date */}
                          <td className="py-4 text-right text-gray-500 text-[15px] tabular-nums">
                            {meta?.date || '—'}
                          </td>

                          {/* Arrow */}
                          <td className="py-4 text-right text-gray-600 group-hover:text-white transition-colors text-lg">
                            →
                          </td>
                        </tr>
                      )
                    })}
                  </>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  )
}

// Solid badges
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
    <span className={`inline-block text-[12px] font-semibold px-3 py-1 rounded-md whitespace-nowrap ${styles[cat]}`}>
      {cat}
    </span>
  )
}
