import { NextRequest, NextResponse } from 'next/server'
import { getSkill, getSkillFileTree } from '@/lib/skills'
import { SKILL_META } from '@/lib/config'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params
  const skill = getSkill(slug)

  if (!skill) {
    return new NextResponse(`echo "Скилл '${slug}' не найден"`, {
      status: 404,
      headers: { 'Content-Type': 'text/plain' },
    })
  }

  const meta = SKILL_META[slug]
  const displayName = meta?.displayName || slug
  const baseUrl = request.nextUrl.origin
  const files = getSkillFileTree(slug)

  // Команды для скачивания всех файлов с воссозданием структуры папок
  const downloads = files.map(rel => {
    const encoded = rel.split('/').map(encodeURIComponent).join('/')
    const dir = rel.includes('/') ? rel.slice(0, rel.lastIndexOf('/')) : ''
    const mkdir = dir ? `mkdir -p "$SKILL_DIR/${dir}"\n` : ''
    return `${mkdir}curl -fsSL "${baseUrl}/api/skills/${slug}/${encoded}" -o "$SKILL_DIR/${rel}"`
  }).join('\n')

  const script = `#!/bin/bash
set -e

SKILL_DIR="$HOME/.claude/skills/${slug}"
echo "📦 Устанавливаю: ${displayName}..."
mkdir -p "$SKILL_DIR"
${downloads}
echo "✅ Скилл «${displayName}» установлен (${files.length} файлов)"
echo "🔄 Перезапусти Claude Code, затем используй /${slug}"
`

  return new NextResponse(script, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  })
}
