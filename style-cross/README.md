# Гибриды faceted-geo × manga-tone

10 игр 6x5 (`games/24`–`33`) в трёх гибридных стилях: 30 готовых промптов `<игра>--<стиль>.md`.

| Стиль | Баланс |
|---|---|
| `style5-geo-manga-balanced` | 50/50: гранёные рама и фон, грани фона чередуют чистый тон и скринтон, маскот с манга-линией |
| `style5-geo-manga-ink` | ближе к манге: кистевая обводка, фон в одном чернильном цвете со скринтоном, грани только как акцент, линии скорости |
| `style5-geo-manga-prism` | ближе к faceted-geo: полноцветный гранёный мир в закатном свете, цветной скринтон только в теневых гранях и небе |

Во всех трёх запрещён читаемый текст в сцене, кроме логотипа.

```sh
# пересобрать промпты
python3 scripts/build_prompts.py --games 24 25 26 27 28 29 30 31 32 33 --styles style5-geo-manga-balanced style5-geo-manga-ink style5-geo-manga-prism --out style-cross
# сгенерировать картинки
python3 scripts/generate_style_tests.py --input style-cross --output style-cross-generated
# только 3 игры (генерация и галерея)
python3 scripts/generate_style_tests.py --input style-cross --output style-cross-generated --only bowling_bears --only safecracker_sal --only magnificent_mime
# галерея вручную, с тем же фильтром
python3 scripts/build_gallery.py style-cross-generated --only bowling_bears --only safecracker_sal --only magnificent_mime
```
