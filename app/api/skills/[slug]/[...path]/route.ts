import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

const SKILLS_DIR = path.join(process.cwd(), 'skills')

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ slug: string; path: string[] }> }
) {
  const { slug, path: parts } = await params

  // Защита от path traversal
  if (parts.some(p => p === '..' || p.includes('\0'))) {
    return new NextResponse('Bad request', { status: 400 })
  }

  const filePath = path.join(SKILLS_DIR, slug, ...parts)
  const resolved = path.resolve(filePath)
  if (!resolved.startsWith(path.resolve(SKILLS_DIR))) {
    return new NextResponse('Forbidden', { status: 403 })
  }

  if (!fs.existsSync(resolved) || fs.statSync(resolved).isDirectory()) {
    return new NextResponse('Not found', { status: 404 })
  }

  const data = fs.readFileSync(resolved)
  const ext = path.extname(resolved).toLowerCase()
  const MIME: Record<string, string> = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.avif': 'image/avif',
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.mov': 'video/quicktime',
    '.pdf': 'application/pdf',
    '.md': 'text/markdown; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
  }
  return new NextResponse(data, {
    headers: {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Cache-Control': 'public, max-age=3600',
    },
  })
}
