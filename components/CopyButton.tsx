'use client'

import { useState } from 'react'

export default function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <button
      onClick={handleCopy}
      className={`text-sm font-medium px-4 py-1.5 rounded-lg transition-all ${
        copied
          ? 'bg-green-700 text-green-100'
          : 'bg-indigo-600 hover:bg-indigo-500 text-white'
      }`}
    >
      {copied ? '✓ Скопировано!' : '⬇ Копировать команду'}
    </button>
  )
}
