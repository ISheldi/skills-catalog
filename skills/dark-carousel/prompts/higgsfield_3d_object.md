# Higgsfield — Преамбула для 3D-объектов (БЕЗ текста внутри)

Используется для cover'ов формата B и для иконок-элементов внутри слайдов.

```
Editorial 3D render. Photorealistic 3D object on cream-beige background #EFEAE0. Negative space, minimal composition. Soft natural lighting from top-left. Subtle shadow. Studio product photography aesthetic.
NO TEXT inside image. NO logos. NO captions. NO labels.
NO cartoon. NO illustration. NO flat 2D. NO physical mockups with text.
Center the object, leave breathing room around it.
```

## Когда использовать
- Cover-слайды формата B (статуя / 3D-объект / символ)
- Иконки-элементы для вставки в HTML-слайды
- Slide 02 «приземление» — визуальный объект, обозначающий тему

## Параметры
```
generate_image(
  model="nano_banana_2",
  prompt="<эта преамбула> + <описание объекта>",
  aspect_ratio="4:5",
  resolution="1k"
)
```

## Принцип
- Текст НЕ внутри картинки. Текст накладываем HTML/CSS поверх через `workflows/build_cover.md`.
- Это решает баг 2 (Cyrillic плывёт) и даёт полный контроль над типографикой.

## Связано
- `workflows/build_cover.md` — как накладывать HTML-overlay поверх Higgsfield-генерации
- `knowledge/visual_dna_format_B.md` — цвета и сетка
