# manga-dev

Рабочая папка для доводки manga-tone на трёх играх 6x5. Файлов-промптов нет: скрипт сам склеивает каждую игру с каждым стилем и отправляет готовый запрос в OpenAI.

- `styles/manga-tone-original.md` — оригинальный `style4-manga-tone`. **Не меняем.** Новые версии кладём рядом: `manga-tone-v1.md`, `manga-tone-v2.md`, …
- `styles/manga-tone-v1.md` — ваш вариант: оригинал (уже под 6x5) + чуть больше скринтона в фоне + матовый пол без отражений.
- `styles/manga-tone-v12.md` — v1 + bold-символы, чёткое разделение планов, лаконичный фон из силуэтов, точки скринтона среднего размера и только в выбранных местах (маскот и символы без точек), упрощённый реквизит, матовый пол.
- `games/` — `29_magnificent_mime`, `35_vampire_vegan`, `37_coupon_queen`. Только тема, без строки `STYLE:`.
- `generated/` — картинки `<игра>--<стиль>.png` и галерея `index.html` для сравнения версий.

```sh
bash manga-dev/run.sh                              # все недостающие картинки (игры × стили)
bash manga-dev/run.sh --styles manga-tone-v1       # только одна версия стиля
bash manga-dev/run.sh --games 35                   # только Vampire Vegan
bash manga-dev/run.sh --games 35 --force           # перегенерировать
bash manga-dev/run.sh --games 35 --print           # показать собранный текст запроса
bash manga-dev/run.sh --dry-run                    # что будет сгенерировано
```
