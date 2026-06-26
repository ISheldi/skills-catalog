#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Прозрачный оверлей для слайда 07 (текст+карточка поверх видео-фона)."""
import pathlib
from playwright.sync_api import sync_playwright

DRAFT = pathlib.Path(__file__).parent
OUT = DRAFT / "07_overlay.png"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">')

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1350px; overflow:hidden; background:transparent; font-family:'Inter',-apple-system,sans-serif; }
.frame { position:relative; width:1080px; height:1350px; }
.scrim { position:absolute; inset:0; background:linear-gradient(to bottom,
  rgba(10,10,10,.6) 0%, rgba(10,10,10,.42) 30%, rgba(10,10,10,.3) 50%, rgba(10,10,10,.55) 100%); }
.bookmark { position:absolute; top:0; left:80px; width:72px; height:118px; background:#E85A2C;
  clip-path:polygon(0 0,100% 0,100% 100%,50% 80%,0 100%); }
.counter { position:absolute; top:46px; left:180px; font-family:'JetBrains Mono',monospace; font-weight:700;
  font-size:30px; color:#FFFFFF; text-shadow:0 2px 14px rgba(0,0,0,.6); }
.nick { position:absolute; bottom:70px; left:80px; font-weight:800; font-size:30px; color:#FFFFFF; letter-spacing:1px; text-shadow:0 2px 14px rgba(0,0,0,.6); }
.swipe { position:absolute; bottom:74px; left:50%; transform:translateX(-50%); font-weight:900; font-size:40px; color:#FF7A45; text-shadow:0 2px 14px rgba(0,0,0,.6); }
.wrap { position:absolute; left:80px; right:80px; top:210px; }
.kicker { font-family:'JetBrains Mono',monospace; font-weight:700; font-size:30px; letter-spacing:3px;
  color:#FF7A45; text-transform:uppercase; margin-bottom:30px; text-shadow:0 2px 16px rgba(0,0,0,.5); }
.headline { font-weight:900; font-size:84px; line-height:1.04; color:#FFFFFF; letter-spacing:-2px; text-shadow:0 4px 30px rgba(0,0,0,.55); }
.headline.sm { font-size:68px; }
.card { position:absolute; left:80px; right:80px; bottom:200px; background:#0A0A0A; border-radius:28px;
  padding:54px 60px; box-shadow:0 24px 70px rgba(0,0,0,.5); color:#EFEAE0; }
.crow { display:flex; gap:28px; align-items:baseline; margin-bottom:30px; }
.crow:last-child { margin-bottom:0; }
.clabel { font-weight:900; font-size:54px; color:#E85A2C; min-width:120px; line-height:1; font-family:'JetBrains Mono',monospace; }
.clabel.txt { font-family:'Inter'; font-size:30px; letter-spacing:1px; text-transform:uppercase; min-width:230px; }
.cval { font-weight:600; font-size:34px; color:#EFEAE0; line-height:1.3; }
.note { position:absolute; left:80px; right:80px; bottom:150px; font-weight:600; font-size:28px; color:#EFEAE0; opacity:.85; text-shadow:0 2px 14px rgba(0,0,0,.6); }
"""

INNER = ("<div class='frame'><div class='scrim'></div><div class='bookmark'></div>"
         "<div class='counter'>07/10</div>"
         "<div class='wrap'><div class='kicker'>что такое модель</div>"
         "<div class='headline sm'>МОДЕЛЬ = ОТВЕТ<br>НА 3 ВОПРОСА</div></div>"
         "<div class='card'>"
         "<div class='crow'><div class='clabel txt'>ЧТО</div><div class='cval'>что именно ты продаёшь</div></div>"
         "<div class='crow'><div class='clabel txt'>КОМУ</div><div class='cval'>кому это нужно и за что платит</div></div>"
         "<div class='crow'><div class='clabel txt'>ЗА СЧЁТ ЧЕГО</div><div class='cval'>как это масштабируется</div></div>"
         "</div>"
         "<div class='note'>(а не «какие кнопки жать в нейросети»)</div>"
         "<div class='nick'>@vladyasko</div><div class='swipe'>→</div></div>")

HTML = f"<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>{FONTS}<style>{CSS}</style></head><body>{INNER}</body></html>"

with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=1)
    path_html = DRAFT / "07_overlay.html"
    path_html.write_text(HTML, encoding="utf-8")
    pg.goto(f"file://{path_html}")
    try:
        pg.evaluate("document.fonts.ready")
    except Exception:
        pass
    pg.wait_for_timeout(700)
    pg.screenshot(path=str(OUT), omit_background=True)
    browser.close()
print("overlay ->", OUT)
