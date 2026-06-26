#!/usr/bin/env python3
"""Record HTML page with CSS animations as MP4 via Playwright + ffmpeg."""
import sys
import os
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

def record(html_path: str, output_mp4: str, duration_ms: int = 5000):
    html_path = os.path.abspath(html_path)
    output_dir = Path(output_mp4).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Temp dir for webm
    tmp_dir = output_dir / "_tmp_video"
    tmp_dir.mkdir(exist_ok=True)

    print(f"→ recording {html_path}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=1,
            record_video_dir=str(tmp_dir),
            record_video_size={"width": 1080, "height": 1350},
        )
        page = context.new_page()
        page.goto(f"file://{html_path}")
        # Wait for fonts/images
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(duration_ms)
        context.close()
        browser.close()

    # Find generated webm
    webms = list(tmp_dir.glob("*.webm"))
    if not webms:
        print("✗ no webm produced")
        sys.exit(1)
    webm_path = webms[0]
    print(f"→ webm: {webm_path} ({webm_path.stat().st_size} bytes)")

    # Convert to MP4 with H.264 (Instagram-friendly)
    print(f"→ converting to MP4...")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(webm_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1350:force_original_aspect_ratio=decrease,pad=1080:1350:(ow-iw)/2:(oh-ih)/2:color=#EFEAE0",
        "-movflags", "+faststart",
        "-r", "30",
        output_mp4
    ], check=True)

    # Clean up temp
    webm_path.unlink()
    try:
        tmp_dir.rmdir()
    except OSError:
        pass

    final_size = os.path.getsize(output_mp4)
    print(f"✓ {output_mp4} — {final_size} bytes")

if __name__ == "__main__":
    html = sys.argv[1] if len(sys.argv) > 1 else "тесты/animation_demo.html"
    out = sys.argv[2] if len(sys.argv) > 2 else "тесты/animation_demo.mp4"
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    record(html, out, duration)
