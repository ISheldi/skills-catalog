import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Гарантируем, что файлы скиллов (включая картинки/видео) попадут в серверные
  // функции на Vercel — иначе API-роуты, читающие их через fs, отдадут 404 в проде.
  outputFileTracingIncludes: {
    '/api/skills/[slug]/[...path]': ['./skills/**/*'],
    '/api/install/[slug]': ['./skills/**/*'],
  },
};

export default nextConfig;
