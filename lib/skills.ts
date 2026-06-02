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

export function getAllSkills(): Skill[] {
  if (!fs.existsSync(SKILLS_DIR)) return []

  const slugs = fs.readdirSync(SKILLS_DIR).filter((f) => {
    return fs.statSync(path.join(SKILLS_DIR, f)).isDirectory()
  })

  return slugs.map((slug) => getSkill(slug)).filter(Boolean) as Skill[]
}

export function getSkill(slug: string): Skill | null {
  const skillPath = path.join(SKILLS_DIR, slug, 'SKILL.md')
  if (!fs.existsSync(skillPath)) return null

  const raw = fs.readFileSync(skillPath, 'utf-8')
  const { data } = matter(raw)

  const files = fs
    .readdirSync(path.join(SKILLS_DIR, slug))
    .filter((f) => f.endsWith('.md'))

  return {
    slug,
    name: data.name || slug,
    description: data.description || '',
    files,
  }
}

export function getSkillFileContent(slug: string, filename: string): string {
  const filePath = path.join(SKILLS_DIR, slug, filename)
  if (!fs.existsSync(filePath)) return ''
  return fs.readFileSync(filePath, 'utf-8')
}
