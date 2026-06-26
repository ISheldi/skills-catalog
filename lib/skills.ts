import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

export interface Skill {
  slug: string
  name: string
  description: string
  files: string[]
}

const SKILLS_DIR = path.join(process.cwd(), 'skills')

// Безопасный разбор frontmatter: некоторые SKILL.md (напр. seedance-*) содержат
// двоеточия в незакавыченном description, на чём строгий YAML-парсер падает.
// В таких случаях не роняем сборку — отдаём пустой data и тело без frontmatter,
// а отображаемые название/описание всё равно берутся из config.ts (SKILL_META).
function safeMatter(raw: string): { data: Record<string, string>; content: string } {
  try {
    const { data, content } = matter(raw)
    return { data: data as Record<string, string>, content }
  } catch {
    // Ручная очистка frontmatter-блока между первой парой '---'
    const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
    const content = m ? raw.slice(m[0].length) : raw
    return { data: {}, content }
  }
}

export function getAllSkills(): Skill[] {
  if (!fs.existsSync(SKILLS_DIR)) return []

  const slugs = fs.readdirSync(SKILLS_DIR).filter((f) => {
    return fs.statSync(path.join(SKILLS_DIR, f)).isDirectory()
  })

  return slugs.map((slug) => getSkill(slug)).filter(Boolean) as Skill[]
}

function extractFallback(raw: string): { name: string; description: string } {
  const lines = raw.split('\n').map(l => l.trim()).filter(Boolean)
  // Try to find a heading
  const heading = lines.find(l => l.startsWith('#'))
  const name = heading ? heading.replace(/^#+\s*/, '') : ''
  // First non-heading, non-special line as description
  const descLine = lines.find(l => !l.startsWith('#') && !l.startsWith('---') && l.length > 20)
  return { name, description: descLine || '' }
}

export function getSkill(slug: string): Skill | null {
  const skillPath = path.join(SKILLS_DIR, slug, 'SKILL.md')
  if (!fs.existsSync(skillPath)) return null

  const raw = fs.readFileSync(skillPath, 'utf-8')
  const { data, content } = safeMatter(raw)

  const fallback = extractFallback(content || raw)

  const files = fs
    .readdirSync(path.join(SKILLS_DIR, slug))
    .filter((f) => f.endsWith('.md') || f.endsWith('.txt'))

  return {
    slug,
    name: data.name || fallback.name || slug,
    description: data.description || fallback.description || '',
    files,
  }
}

export function getSkillFileContent(slug: string, filename: string): string {
  const filePath = path.join(SKILLS_DIR, slug, filename)
  if (!fs.existsSync(filePath)) return ''
  return fs.readFileSync(filePath, 'utf-8')
}

// Тело SKILL.md без YAML-фронтматтера (для красивого рендера)
export function getSkillBody(slug: string): string {
  const skillPath = path.join(SKILLS_DIR, slug, 'SKILL.md')
  if (!fs.existsSync(skillPath)) return ''
  const raw = fs.readFileSync(skillPath, 'utf-8')
  const { content } = safeMatter(raw)
  return content.trim()
}

// Рекурсивный список ВСЕХ файлов скилла (относительные пути) — для полной установки
export function getSkillFileTree(slug: string): string[] {
  const root = path.join(SKILLS_DIR, slug)
  if (!fs.existsSync(root)) return []
  const out: string[] = []
  const walk = (dir: string, prefix: string) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name === '.git' || entry.name === 'node_modules') continue
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name
      if (entry.isDirectory()) walk(path.join(dir, entry.name), rel)
      else out.push(rel)
    }
  }
  walk(root, '')
  return out
}
