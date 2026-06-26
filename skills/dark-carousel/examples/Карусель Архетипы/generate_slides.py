#!/usr/bin/env python3
"""Generate all 15 ANIMATED slide HTML files (02-16) for the 12 Archetypes carousel.

Финальная анимация — комбинация из утверждённых эффектов:
  • Header maskReveal (по диагонали) — из v4_editorial
  • Number roll (slot-machine, останавливается на финальной цифре) — из v3_typewriter
  • Logos Ken Burns (фото "дышит") — из v2_parallax
  • Card fadeUp + per-row typewriter (Желание/Страх/Бренды) — из v3_typewriter
  • Footer drawLine underline — из v4_editorial
  • Nick charStagger (буквы сходятся) — из v2_parallax
  • Counter "NN/16": JetBrains Mono для стабильной ширины (фикс бага обрезания)
  • Никакого transform на .frame (cameraShake удалён — он обрезал meta-tl)
"""
from pathlib import Path

ROOT = Path("__YOUR_PROJECT_DIR__/Карусель Архетипы")
HTML_DIR = ROOT / "финал" / "html"
HTML_DIR.mkdir(parents=True, exist_ok=True)

COMMON_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1080px; height: 1350px; overflow: hidden; background: #EFEAE0; }
  .frame {
    position: relative; width: 1080px; height: 1350px;
    background: #EFEAE0;
    font-family: 'Inter', sans-serif;
    color: #1A1A1A; overflow: hidden;
  }
  /* Background grid drift */
  .grid-overlay {
    position: absolute; inset: 0;
    background:
      linear-gradient(#CFC4A8 1px, transparent 1px) 0 0/40px 40px,
      linear-gradient(90deg, #CFC4A8 1px, transparent 1px) 0 0/40px 40px;
    opacity: 0.32; pointer-events: none;
    animation: gridShift 10s linear infinite;
  }
  @keyframes gridShift {
    from { background-position: 0 0, 0 0; }
    to   { background-position: 40px 40px, 40px 40px; }
  }
  /* Bookmark stamp-in */
  .bookmark {
    position: absolute; top: 36px; left: 56px;
    width: 38px; height: 60px; background: #E85A2C;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 78%, 0 100%);
    z-index: 5;
    transform: scale(0);
    animation: stampIn 0.4s 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  }
  @keyframes stampIn {
    from { transform: scale(0) rotate(-30deg); }
    to   { transform: scale(1) rotate(0); }
  }
  /* Counter: JetBrains Mono fixes width crop bug */
  .meta-tl {
    position: absolute; top: 56px; left: 116px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700; font-size: 22px; letter-spacing: 0.5px;
    color: #1A1A1A; z-index: 6;
    padding-right: 8px;
    opacity: 0;
    animation: fadeIn 0.3s 0.2s forwards;
  }
  /* Nick charStagger (буквы сходятся) */
  .nick {
    position: absolute; bottom: 36px; left: 56px;
    font-weight: 800; font-size: 22px; color: #1A1A1A; letter-spacing: 8px; z-index: 5;
    opacity: 0;
    animation: charStagger 0.8s 1.0s forwards;
  }
  @keyframes charStagger {
    from { opacity: 0; letter-spacing: 30px; }
    to   { opacity: 1; letter-spacing: 1px; }
  }
  @keyframes fadeIn { to { opacity: 1; } }
"""

# ---- TEMPLATE: ARCHETYPE slide (#1 ... #12) ----
ARCHETYPE_TEMPLATE = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
{common}
  /* HEADER: быстрый maskReveal (название появляется сразу) */
  .header {{
    position: absolute; top: 110px; left: 56px; right: 56px; z-index: 4;
    -webkit-mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
            mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
    -webkit-mask-size: 250% 250%;
            mask-size: 250% 250%;
    -webkit-mask-position: 100% 100%;
            mask-position: 100% 100%;
    animation: maskReveal 0.5s 0.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes maskReveal {{
    to {{ -webkit-mask-position: 0% 0%; mask-position: 0% 0%; }}
  }}

  /* NUMBER ROLL: ширина 280px (двузначные #10/#11/#12 влезают),
     высота 160px (ascenders шрифта не обрезаются) */
  .num-wrap {{
    display: inline-block;
    width: 280px; height: 160px;
    overflow: hidden;
    vertical-align: top;
    padding-top: 10px;
    box-sizing: border-box;
  }}
  .num-roll {{
    display: flex; flex-direction: column;
    line-height: 150px; height: 150px;
    transform: translateY(0);
    animation: rollNum 1.0s 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes rollNum {{
    from {{ transform: translateY(0); }}
    to   {{ transform: translateY(-1650px); }}  /* 11 × 150px */
  }}
  .num-roll span {{
    font-weight: 900; font-size: 130px; line-height: 150px;
    color: #E85A2C; letter-spacing: -5px; height: 150px;
  }}
  .num-roll .final {{
    animation: numPulse 2.5s 1.4s ease-in-out infinite;
  }}
  @keyframes numPulse {{
    0%, 100% {{ text-shadow: 0 0 0 transparent; }}
    50%      {{ text-shadow: 0 0 30px rgba(232, 90, 44, 0.5); }}
  }}

  .arch-name {{
    font-weight: 900; font-size: 92px; line-height: 0.98;
    color: #1A1A1A; letter-spacing: -3px; margin-top: 14px;
  }}
  .tagline {{
    font-weight: 800; font-size: 30px; line-height: 1.18;
    color: #E85A2C; margin-top: 22px;
    letter-spacing: -0.2px; max-width: 940px;
  }}

  /* LOGOS: Ken Burns — появляются раньше */
  .logos {{
    position: absolute; top: 470px; left: 0; right: 0;
    width: 1080px; height: 460px;
    z-index: 3; overflow: hidden;
    opacity: 0;
    animation: fadeIn 0.5s 0.7s forwards;
  }}
  .logos img {{
    width: 100%; height: 100%;
    object-fit: cover; display: block;
    transform-origin: center;
    animation: kenBurns 8s 0.7s ease-in-out infinite alternate;
  }}
  @keyframes kenBurns {{
    from {{ transform: scale(1) translate(0, 0); }}
    to   {{ transform: scale(1.12) translate(-15px, -10px); }}
  }}

  /* CARD: fadeUp + быстрые per-row typewriter */
  .card {{
    position: absolute; bottom: 200px; left: 56px; right: 56px;
    background: #0A0A0A; border-radius: 24px;
    padding: 30px 44px; z-index: 3;
    box-shadow: 0 20px 60px rgba(232, 90, 44, 0.18), 0 4px 12px rgba(0,0,0,0.35);
    color: #FFFFFF;
    opacity: 0;
    animation: cardFadeUp 0.5s 1.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes cardFadeUp {{
    from {{ opacity: 0; transform: translateY(40px) scale(0.96); filter: blur(6px); }}
    to   {{ opacity: 1; transform: translateY(0)   scale(1);    filter: blur(0); }}
  }}
  .row {{
    display: flex; align-items: baseline;
    padding: 9px 0; border-bottom: 1px solid #2A2A2A;
  }}
  .row:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .row:first-child {{ padding-top: 0; }}
  .label {{
    width: 180px; flex-shrink: 0;
    font-weight: 900; font-size: 16px;
    color: #E85A2C; letter-spacing: 1.5px;
    text-transform: uppercase;
  }}
  .value {{
    flex: 1; font-weight: 700; font-size: 22px;
    color: #FFFFFF; line-height: 1.25; letter-spacing: -0.2px;
    overflow: hidden; white-space: nowrap;
    width: 0;
  }}
  .row:nth-child(1) .value {{ animation: typeRow 0.6s 1.7s steps(40) forwards; }}
  .row:nth-child(2) .value {{ animation: typeRow 0.5s 2.4s steps(28) forwards; }}
  .row:nth-child(3) .value {{ animation: typeRow 0.6s 3.0s steps(32) forwards; }}
  @keyframes typeRow {{ to {{ width: 100%; }} }}

  /* FOOTER: drawLine underline (из v4) */
  .footer {{
    position: absolute; bottom: 110px; left: 56px; right: 56px;
    font-weight: 800; font-size: 26px; color: #1A1A1A;
    line-height: 1.3; letter-spacing: -0.3px; z-index: 4;
    opacity: 0;
    padding-bottom: 8px;
    animation: fadeIn 0.4s 3.7s forwards;
  }}
  .footer .accent {{ color: #E85A2C; font-weight: 900; }}
  .footer::after {{
    content: '';
    position: absolute; left: 0; bottom: 0;
    height: 3px; background: #E85A2C;
    width: 0;
    animation: drawLine 0.8s 4.0s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes drawLine {{ to {{ width: 540px; }} }}
  .arrow {{
    color: #E85A2C; font-weight: 900;
    display: inline-block;
    animation: arrowSlide 1.4s 4.5s ease-in-out infinite;
  }}
  @keyframes arrowSlide {{
    0%, 100% {{ transform: translateX(0); opacity: 0.7; }}
    50%      {{ transform: translateX(14px); opacity: 1; }}
  }}
</style></head><body>
<div class="frame">
  <div class="grid-overlay"></div>
  <div class="bookmark"></div>
  <div class="meta-tl">{counter}</div>
  <div class="header">
    <div class="num-wrap">
      <div class="num-roll">
        <span>#7</span><span>#3</span><span>#9</span><span>#2</span>
        <span>#5</span><span>#8</span><span>#4</span><span>#6</span>
        <span>#0</span><span>#3</span><span>#2</span><span class="final">#{num}</span>
      </div>
    </div>
    <div class="arch-name">{name}</div>
    <div class="tagline">{tagline}</div>
  </div>
  <div class="logos"><img src="../../assets/3d_logos/{logo_file}" alt=""></div>
  <div class="card">
    <div class="row"><div class="label">Желание</div><div class="value">{want}</div></div>
    <div class="row"><div class="label">Страх</div><div class="value">{fear}</div></div>
    <div class="row"><div class="label">Бренды</div><div class="value">{brands}</div></div>
  </div>
  <div class="footer">{money} <span class="arrow">→</span></div>
  <div class="nick">@vladyasko</div>
</div></body></html>
"""

# ---- TEMPLATE: CONTEXT (slide 02) ----
CONTEXT_TEMPLATE = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
{common}
  .header {{
    position: absolute; top: 130px; left: 56px; right: 56px; z-index: 4;
    -webkit-mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
            mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
    -webkit-mask-size: 250% 250%;
            mask-size: 250% 250%;
    -webkit-mask-position: 100% 100%;
            mask-position: 100% 100%;
    animation: maskReveal 0.5s 0.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes maskReveal {{
    to {{ -webkit-mask-position: 0% 0%; mask-position: 0% 0%; }}
  }}
  .h1 {{
    font-weight: 900; font-size: 96px; line-height: 0.96;
    color: #1A1A1A; letter-spacing: -3px;
  }}
  .h1 .accent {{ color: #E85A2C; }}
  .h2 {{
    font-weight: 800; font-size: 32px; line-height: 1.2;
    color: #1A1A1A; margin-top: 32px; letter-spacing: -0.3px; max-width: 920px;
  }}
  .card {{
    position: absolute; bottom: 230px; left: 56px; right: 56px;
    background: #0A0A0A; border-radius: 24px;
    padding: 36px 44px; z-index: 3;
    box-shadow: 0 20px 60px rgba(232, 90, 44, 0.18), 0 4px 12px rgba(0,0,0,0.35);
    opacity: 0;
    animation: cardFadeUp 0.5s 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes cardFadeUp {{
    from {{ opacity: 0; transform: translateY(40px) scale(0.96); filter: blur(6px); }}
    to   {{ opacity: 1; transform: translateY(0)   scale(1);    filter: blur(0); }}
  }}
  .equation {{
    font-weight: 900; font-size: 38px; color: #FFFFFF;
    line-height: 1.4; letter-spacing: -0.5px;
  }}
  .equation .brand {{ color: #FFFFFF; }}
  .equation .eq {{ color: #E85A2C; padding: 0 12px; }}
  .equation .arch {{ color: #E85A2C; font-weight: 900; }}
  .equation .row-eq {{
    display: flex; align-items: center; padding: 6px 0;
    opacity: 0;
  }}
  .equation .row-eq:nth-child(1) {{ animation: rowFadeIn 0.4s 1.4s forwards; }}
  .equation .row-eq:nth-child(2) {{ animation: rowFadeIn 0.4s 1.7s forwards; }}
  .equation .row-eq:nth-child(3) {{ animation: rowFadeIn 0.4s 2.0s forwards; }}
  .equation .row-eq:nth-child(4) {{ animation: rowFadeIn 0.4s 2.3s forwards; }}
  @keyframes rowFadeIn {{
    from {{ opacity: 0; transform: translateX(-20px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
  }}
  .footer {{
    position: absolute; bottom: 90px; left: 56px; right: 56px;
    font-weight: 800; font-size: 28px; color: #1A1A1A;
    line-height: 1.3; letter-spacing: -0.3px; z-index: 4;
    opacity: 0;
    animation: fadeIn 0.4s 2.9s forwards;
  }}
  .footer .accent {{ color: #E85A2C; }}
</style></head><body>
<div class="frame">
  <div class="grid-overlay"></div>
  <div class="bookmark"></div>
  <div class="meta-tl">02/16</div>
  <div class="header">
    <div class="h1">АРХЕТИП =<br><span class="accent">ТВОЯ СТРАТЕГИЯ.</span></div>
    <div class="h2">12 типажей по Юнгу. У каждого своё желание, страх и стиль поведения.<br>В бизнесе архетип = почему люди покупают именно у тебя.</div>
  </div>
  <div class="card">
    <div class="equation">
      <div class="row-eq"><span class="brand">APPLE</span><span class="eq">=</span><span class="arch">МАГ</span></div>
      <div class="row-eq"><span class="brand">NIKE</span><span class="eq">=</span><span class="arch">ГЕРОЙ</span></div>
      <div class="row-eq"><span class="brand">HARLEY</span><span class="eq">=</span><span class="arch">БУНТАРЬ</span></div>
      <div class="row-eq"><span class="brand">ROLEX</span><span class="eq">=</span><span class="arch">ПРАВИТЕЛЬ</span></div>
    </div>
  </div>
  <div class="footer">Это не маркетинг. <span class="accent">Это код мышления.</span> 12 кодов ↓</div>
  <div class="nick">@vladyasko</div>
</div></body></html>
"""

# ---- TEMPLATE: DARK SIDE (slide 15) ----
DARK_TEMPLATE = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
{common}
  .header {{
    position: absolute; top: 110px; left: 56px; right: 56px; z-index: 4;
    -webkit-mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
            mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
    -webkit-mask-size: 250% 250%;
            mask-size: 250% 250%;
    -webkit-mask-position: 100% 100%;
            mask-position: 100% 100%;
    animation: maskReveal 0.5s 0.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes maskReveal {{
    to {{ -webkit-mask-position: 0% 0%; mask-position: 0% 0%; }}
  }}
  .h1 {{
    font-weight: 900; font-size: 110px; line-height: 0.96;
    color: #1A1A1A; letter-spacing: -4px;
  }}
  .h1 .accent {{ color: #E85A2C; }}
  .h2 {{
    font-weight: 800; font-size: 26px; color: #E85A2C;
    margin-top: 14px; letter-spacing: 0.5px; text-transform: uppercase;
  }}
  .card {{
    position: absolute; top: 380px; left: 56px; right: 56px; bottom: 110px;
    background: #0A0A0A; border-radius: 24px;
    padding: 28px 36px; z-index: 3;
    box-shadow: 0 20px 60px rgba(232, 90, 44, 0.18), 0 4px 12px rgba(0,0,0,0.35);
    color: #FFFFFF;
    opacity: 0;
    animation: cardFadeUp 0.5s 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes cardFadeUp {{
    from {{ opacity: 0; transform: translateY(40px) scale(0.96); filter: blur(6px); }}
    to   {{ opacity: 1; transform: translateY(0)   scale(1);    filter: blur(0); }}
  }}
  .row {{
    display: flex; align-items: baseline;
    padding: 9px 0; border-bottom: 1px solid #2A2A2A;
    font-size: 21px;
    opacity: 0;
  }}
  .row:last-child {{ border-bottom: none; }}
  .row:nth-child(1)  {{ animation: rowSlideIn 0.35s 1.2s forwards; }}
  .row:nth-child(2)  {{ animation: rowSlideIn 0.35s 1.3s forwards; }}
  .row:nth-child(3)  {{ animation: rowSlideIn 0.35s 1.4s forwards; }}
  .row:nth-child(4)  {{ animation: rowSlideIn 0.35s 1.5s forwards; }}
  .row:nth-child(5)  {{ animation: rowSlideIn 0.35s 1.6s forwards; }}
  .row:nth-child(6)  {{ animation: rowSlideIn 0.35s 1.7s forwards; }}
  .row:nth-child(7)  {{ animation: rowSlideIn 0.35s 1.8s forwards; }}
  .row:nth-child(8)  {{ animation: rowSlideIn 0.35s 1.9s forwards; }}
  .row:nth-child(9)  {{ animation: rowSlideIn 0.35s 2.0s forwards; }}
  .row:nth-child(10) {{ animation: rowSlideIn 0.35s 2.1s forwards; }}
  .row:nth-child(11) {{ animation: rowSlideIn 0.35s 2.2s forwards; }}
  .row:nth-child(12) {{ animation: rowSlideIn 0.35s 2.3s forwards; }}
  @keyframes rowSlideIn {{
    from {{ opacity: 0; transform: translateX(-20px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
  }}
  .light {{
    width: 280px; flex-shrink: 0;
    font-weight: 900; color: #FFFFFF; letter-spacing: -0.2px;
  }}
  .arrow {{
    width: 30px; flex-shrink: 0;
    color: #E85A2C; font-weight: 900;
  }}
  .dark {{
    flex: 1; font-weight: 700; color: #B5B5B5;
    line-height: 1.2;
  }}
</style></head><body>
<div class="frame">
  <div class="grid-overlay"></div>
  <div class="bookmark"></div>
  <div class="meta-tl">15/16</div>
  <div class="header">
    <div class="h1">ТЁМНАЯ <span class="accent">СТОРОНА.</span></div>
    <div class="h2">У каждого архетипа есть инверсия ↓</div>
  </div>
  <div class="card">
    <div class="row"><div class="light">Простодушный</div><div class="arrow">→</div><div class="dark">отрицание реальности</div></div>
    <div class="row"><div class="light">Искатель</div><div class="arrow">→</div><div class="dark">хаотичный перфекционист</div></div>
    <div class="row"><div class="light">Мудрец</div><div class="arrow">→</div><div class="dark">бесчувственный судья</div></div>
    <div class="row"><div class="light">Бунтарь</div><div class="arrow">→</div><div class="dark">саморазрушение</div></div>
    <div class="row"><div class="light">Маг</div><div class="arrow">→</div><div class="dark">манипулятор, тёмный маг</div></div>
    <div class="row"><div class="light">Герой</div><div class="arrow">→</div><div class="dark">преступник в боевой готовности</div></div>
    <div class="row"><div class="light">Любовник</div><div class="arrow">→</div><div class="dark">одержимый соблазнитель</div></div>
    <div class="row"><div class="light">Шут</div><div class="arrow">→</div><div class="dark">обжора, мошенник</div></div>
    <div class="row"><div class="light">Славный Малый</div><div class="arrow">→</div><div class="dark">жертва, требующая льгот</div></div>
    <div class="row"><div class="light">Заботливый</div><div class="arrow">→</div><div class="dark">мученик-манипулятор</div></div>
    <div class="row"><div class="light">Правитель</div><div class="arrow">→</div><div class="dark">тиран «голову с плеч»</div></div>
    <div class="row"><div class="light">Творец</div><div class="arrow">→</div><div class="dark">одержим, ничего не доводит до конца</div></div>
  </div>
  <div class="nick">@vladyasko</div>
</div></body></html>
"""

# ---- TEMPLATE: CTA (slide 16) ----
CTA_TEMPLATE = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
{common}
  .center-block {{
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    justify-content: center; align-items: flex-start;
    padding: 0 56px; z-index: 4;
    -webkit-mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
            mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
    -webkit-mask-size: 250% 250%;
            mask-size: 250% 250%;
    -webkit-mask-position: 100% 100%;
            mask-position: 100% 100%;
    animation: maskReveal 0.6s 0.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes maskReveal {{
    to {{ -webkit-mask-position: 0% 0%; mask-position: 0% 0%; }}
  }}
  .save-icon {{
    width: 110px; height: 170px; background: #E85A2C;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 78%, 0 100%);
    margin-bottom: 36px;
    transform-origin: top center;
    animation: savePulse 2.5s 1.0s ease-in-out infinite;
  }}
  @keyframes savePulse {{
    0%, 100% {{ filter: drop-shadow(0 0 0 rgba(232, 90, 44, 0)); transform: scale(1); }}
    50%      {{ filter: drop-shadow(0 0 24px rgba(232, 90, 44, 0.7)); transform: scale(1.04); }}
  }}
  .quote {{
    font-weight: 900; font-size: 88px; line-height: 0.96;
    color: #1A1A1A; letter-spacing: -3px;
  }}
  .quote .accent {{ color: #E85A2C; }}
  .author {{
    font-weight: 800; font-size: 26px; color: #E85A2C;
    margin-top: 24px; letter-spacing: 1px; text-transform: uppercase;
  }}
  .sub {{
    font-weight: 800; font-size: 30px; color: #1A1A1A;
    margin-top: 60px; line-height: 1.3; max-width: 760px;
    letter-spacing: -0.3px;
  }}
  .sub .accent {{ color: #E85A2C; }}
  .nick-big {{
    position: absolute; bottom: 90px; left: 56px;
    font-weight: 900; font-size: 56px; color: #1A1A1A;
    letter-spacing: -1px; z-index: 5;
    opacity: 0;
    animation: nickBig 0.7s 1.0s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  @keyframes nickBig {{
    from {{ opacity: 0; transform: translateY(20px); letter-spacing: 4px; }}
    to   {{ opacity: 1; transform: translateY(0);    letter-spacing: -1px; }}
  }}
  .nick-big .at {{ color: #E85A2C; }}
</style></head><body>
<div class="frame">
  <div class="grid-overlay"></div>
  <div class="bookmark"></div>
  <div class="meta-tl">16/16</div>
  <div class="center-block">
    <div class="save-icon"></div>
    <div class="quote">ЕСЛИ НЕ <span class="accent">РАСТЁШЬ —</span><br>ТЫ НЕ В СВОЕЙ<br>СТРАТЕГИИ.</div>
    <div class="author">— НИКА ЗЕБРА</div>
    <div class="sub">Сохрани карусель — и <span class="accent">найди свой архетип.</span> Это твоя точка роста.</div>
  </div>
  <div class="nick-big"><span class="at">@</span>your_handle</div>
</div></body></html>
"""

# ---- DATA: 12 Archetypes ----
ARCHETYPES = [
    {
        "num": 1, "name": "ПРОСТОДУШНЫЙ",
        "tagline": "Ищет рай. Боится ошибиться.",
        "want": "Идеальная жизнь. Счастливый финал.",
        "fear": "Сделать что-то не так.",
        "brands": "Disney · Coca-Cola · McDonald's",
        "money": "Зарабатывает на простоте и оптимизме.",
        "logo": "03_pro.png",
    },
    {
        "num": 2, "name": "ИСКАТЕЛЬ",
        "tagline": "Жаждет свободы. Боится застрять.",
        "want": "Приключения. Открытие нового.",
        "fear": "Ловушка. Внутренняя пустота.",
        "brands": "Nike · GoPro · Patagonia",
        "money": "Продаёт «не такой как все» путь.",
        "logo": "04_iska.png",
    },
    {
        "num": 3, "name": "МУДРЕЦ",
        "tagline": "Ищет истину. Боится невежества.",
        "want": "Понять, как устроен мир.",
        "fear": "Быть обманутым. Поверхностность.",
        "brands": "Google · BBC · Harvard",
        "money": "Зарабатывает на экспертности и данных.",
        "logo": "05_mudr.png",
    },
    {
        "num": 4, "name": "БУНТАРЬ",
        "tagline": "Хочет революции. Боится заурядности.",
        "want": "Сломать систему. Месть статус-кво.",
        "fear": "Быть бессильным. Слиться с толпой.",
        "brands": "Harley-Davidson · Uber · Vice",
        "money": "Продаёт оппозицию и провокацию.",
        "logo": "06_bunt.png",
    },
    {
        "num": 5, "name": "МАГ",
        "tagline": "Превращает мечты в явь. Боится последствий.",
        "want": "Знать законы мира. Менять реальность.",
        "fear": "Непредвиденные негативные эффекты.",
        "brands": "Apple · Tesla · Disney+",
        "money": "Продаёт магию трансформации и «wow».",
        "logo": "07_mag.png",
    },
    {
        "num": 6, "name": "ГЕРОЙ",
        "tagline": "Доказывает силу. Боится слабости.",
        "want": "Победить. Стать сильнее всех.",
        "fear": "Слабость. Стать жертвой.",
        "brands": "Adidas · BMW M · US Army",
        "money": "Зарабатывает на вызове и преодолении.",
        "logo": "08_geroy.png",
    },
    {
        "num": 7, "name": "ЛЮБОВНИК",
        "tagline": "Ищет близость. Боится одиночества.",
        "want": "Чувственность. Глубокая интимность.",
        "fear": "Остаться нелюбимым. Быть отвергнутым.",
        "brands": "Chanel · Dior · Häagen-Dazs",
        "money": "Продаёт красоту и желание.",
        "logo": "09_lover.png",
    },
    {
        "num": 8, "name": "ШУТ",
        "tagline": "Живёт здесь и сейчас. Боится скуки.",
        "want": "Веселье. Максимум удовольствия.",
        "fear": "Скучать или быть скучным.",
        "brands": "Old Spice · Ben &amp; Jerry's · Skittles",
        "money": "Продаёт лёгкость, юмор, развлечение.",
        "logo": "10_shut.png",
    },
    {
        "num": 9, "name": "СЛАВНЫЙ МАЛЫЙ",
        "tagline": "Хочет быть как все. Боится выделиться.",
        "want": "Связь с окружающими. Принадлежность.",
        "fear": "Быть отвергнутым. Высовываться.",
        "brands": "IKEA · Levi's · Gap",
        "money": "Продаёт доступность и «для каждого».",
        "logo": "11_slavny.png",
    },
    {
        "num": 10, "name": "ЗАБОТЛИВЫЙ",
        "tagline": "Хочет защитить. Боится эгоизма.",
        "want": "Помочь. Уберечь близких от вреда.",
        "fear": "Неблагодарность. Пренебречь любимыми.",
        "brands": "Volvo · UNICEF · Johnson &amp; Johnson",
        "money": "Зарабатывает на безопасности и доверии.",
        "logo": "12_zabot.png",
    },
    {
        "num": 11, "name": "ПРАВИТЕЛЬ",
        "tagline": "Управляет миром. Боится хаоса.",
        "want": "Контроль. Создать успешное сообщество.",
        "fear": "Хаос. Быть свергнутым.",
        "brands": "Rolex · Mercedes · AmEx Black",
        "money": "Продаёт статус, эксклюзив, премиум.",
        "logo": "13_pravit.png",
    },
    {
        "num": 12, "name": "ТВОРЕЦ",
        "tagline": "Воплощает видение. Боится посредственности.",
        "want": "Создать что-то вечное и уникальное.",
        "fear": "Посредственное воплощение.",
        "brands": "Lego · Adobe · A24",
        "money": "Продаёт уникальность и инструменты создания.",
        "logo": "14_tvor.png",
    },
]

def write_slide(filename, content):
    path = HTML_DIR / filename
    path.write_text(content, encoding="utf-8")
    print(f"  → {filename}")

# Slide 02 — Context
write_slide("02_context.html", CONTEXT_TEMPLATE.format(common=COMMON_CSS))

# Slides 03-14 — 12 archetypes
for i, arch in enumerate(ARCHETYPES):
    slide_num = i + 3
    counter = f"{slide_num:02d}/16"
    safe_name = arch["name"].lower().replace(" ", "_")
    html = ARCHETYPE_TEMPLATE.format(
        common=COMMON_CSS,
        counter=counter,
        num=arch["num"],
        name=arch["name"],
        tagline=arch["tagline"],
        want=arch["want"],
        fear=arch["fear"],
        brands=arch["brands"],
        money=arch["money"],
        logo_file=arch["logo"],
    )
    write_slide(f"{slide_num:02d}_{safe_name}.html", html)

# Slide 15 — Dark side
write_slide("15_dark.html", DARK_TEMPLATE.format(common=COMMON_CSS))

# Slide 16 — CTA
write_slide("16_cta.html", CTA_TEMPLATE.format(common=COMMON_CSS))

print(f"\n✅ Generated 15 ANIMATED HTML files in {HTML_DIR}")
