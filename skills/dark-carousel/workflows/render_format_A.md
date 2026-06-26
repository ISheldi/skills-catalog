# Workflow — Рендер формата A (Бренд-личность)

См. также: `knowledge/visual_dna_format_A.md`, `templates/slide_format_A.html`.

---

## Предусловия

- Пройден `workflows/onboarding.md` + `workflows/plan_and_approve.md`
- Апрув от пользователя получен
- Знаешь имена фото для слайдов 1, 5, 9 (varied `outfit_set`)

---

## Шаг 1: Подготовка фото

1. Прочитай `Фото для каруселей/photos_index.json` (НЕ сканируй JPG/PNG).
2. Выбери фото с учётом `outfit_set`, `mood`, `recommended_for`. **Варьируй outfit между слайдами.**
3. Кропы `IMG_5224*` — один кадр в 4 версиях, не брать два подряд.
4. Если нужен визуальный ре-скан — открой превью из `.thumbs/` (700px JPEG, ~50KB).
5. Перед `Read` любого PNG/JPG > 2000px → `sips -Z 2000 file.jpg`.

## Шаг 2: Загрузка фото в Higgsfield (если новое)

```
media_upload(filename, content_type="image/jpeg")
→ curl -X PUT "{upload_url}" --data-binary @"/path/to/photo.jpg"
→ media_confirm(media_id)
```

## Шаг 3: Генерация фото-слайдов (1, 5, 9)

```
generate_image(
  model="nano_banana_2",
  prompt="<преамбула из prompts/higgsfield_photo.md> + <контент слайда>",
  aspect_ratio="4:5",
  resolution="1k",
  medias=[{"value": "<media_id>", "role": "image"}]
)
→ job_display(job_id)
→ curl -o "готовые/<название>/0N_*.png" "{image_url}"
```

См. лимиты итераций → `workflows/safe_higgsfield_iteration.md`.

## Шаг 4: Рендер типографских слайдов через Playwright

Каждая карусель создаёт свой `generate_slides.py` в папке `готовые/<название>/черновики/`.
Эталон-генератор: `examples/Карусель Архетипы/generate_slides.py` — берёшь его за основу.

```bash
cd "готовые/<название>/черновики"
python3 generate_slides.py    # читает slides_data.json → рендерит PNG → кладёт в родительскую папку
```

HTML-шаблон: `templates/slide_format_A.html` (этой папки скилла).
Дизайн-параметры: `config/settings.yml` + `knowledge/visual_dna_format_A.md`.

## Шаг 5: Self-check

Прочитать 1-2 ключевых PNG (1080×1350, в пределах лимита 2000px → безопасно). Не более 5 за раз.

## Шаг 6: Сдача

- Файлы в `готовые/<название>/` с именами `01_*.png` … `NN_*.png`
- `подпись_под_пост.md` рядом
- Показать сетку (1-2 ключевых через preview, остальное путём)
