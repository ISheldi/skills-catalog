#!/usr/bin/env python3
"""Batch-render all 15 animated HTML slides to MP4 (Instagram-ready, 1080×1350, H.264).

Запускать ПОСЛЕДОВАТЕЛЬНО (не параллельно) — Playwright + ffmpeg по одному файлу за раз.
Это спасает от падения сессии при больших нагрузках.

Длительность видео: 8500ms — захватывает все вступительные анимации (~7s)
плюс ~1.5s на цикл бесконечной анимации (Ken Burns / arrowSlide).

Usage:
    python3 render_animations.py            # all slides 02-16
    python3 render_animations.py 03 07      # only slides 03 and 07
"""
import sys
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("__YOUR_PROJECT_DIR__/Карусель Архетипы")
HTML_DIR = ROOT / "финал" / "html"
MP4_DIR = ROOT / "финал" / "mp4"
MP4_DIR.mkdir(parents=True, exist_ok=True)

DURATION_MS = 8500  # 8.5s — захватывает все вступительные анимации (~4.5s) + 4s на циклы (Ken Burns / arrowSlide)

def list_slides():
    """Return list of (slide_num, html_path, mp4_path) tuples for all 15 slides."""
    slides = []
    for html in sorted(HTML_DIR.glob("*.html")):
        slide_num = html.stem.split("_")[0]
        mp4 = MP4_DIR / f"{html.stem}.mp4"
        slides.append((slide_num, html, mp4))
    return slides

def record_one(html_path: Path, output_mp4: Path, duration_ms: int):
    """Record one HTML file to MP4."""
    tmp_dir = output_mp4.parent / "_tmp_video"
    tmp_dir.mkdir(exist_ok=True)

    print(f"  ▶ {html_path.name}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=1,
            record_video_dir=str(tmp_dir),
            record_video_size={"width": 1080, "height": 1350},
        )
        page = context.new_page()
        page.goto(f"file://{html_path.absolute()}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(duration_ms)
        context.close()
        browser.close()

    # Find generated webm (single per session)
    webms = list(tmp_dir.glob("*.webm"))
    if not webms:
        print(f"  ✗ no webm produced for {html_path.name}")
        return False
    webm_path = webms[0]

    # Convert to MP4 H.264 (Instagram-friendly)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(webm_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1350:force_original_aspect_ratio=decrease,"
               "pad=1080:1350:(ow-iw)/2:(oh-ih)/2:color=#EFEAE0",
        "-movflags", "+faststart",
        "-r", "30",
        str(output_mp4)
    ], check=True)

    webm_path.unlink()
    try:
        tmp_dir.rmdir()
    except OSError:
        pass

    size_kb = output_mp4.stat().st_size / 1024
    print(f"  ✓ {output_mp4.name}  ({size_kb:.0f} KB)")
    return True

def main():
    filter_nums = sys.argv[1:] if len(sys.argv) > 1 else None
    slides = list_slides()
    if filter_nums:
        slides = [s for s in slides if s[0] in filter_nums]
    if not slides:
        print("No slides matched.")
        sys.exit(1)

    total = len(slides)
    print(f"\n🎬 Rendering {total} slide(s) sequentially → {MP4_DIR}\n")
    start = time.time()
    ok = 0
    for i, (num, html, mp4) in enumerate(slides, 1):
        print(f"[{i}/{total}] slide {num}")
        try:
            if record_one(html, mp4, DURATION_MS):
                ok += 1
        except Exception as e:
            print(f"  ✗ ERROR on {html.name}: {e}")
        # Small pause between renders to let system breathe
        time.sleep(0.5)
    elapsed = time.time() - start
    print(f"\n✅ Done: {ok}/{total} in {elapsed:.0f}s → {MP4_DIR}")

if __name__ == "__main__":
    main()
