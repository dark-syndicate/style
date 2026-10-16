# manga-dev

Рабочая папка для доводки manga-tone на трёх играх 6x5. Файлов-промптов нет: скрипт сам склеивает каждую игру с каждым стилем и отправляет готовый запрос в OpenAI.

- `styles/manga-tone-original.md` — оригинальный `style4-manga-tone`. **Не меняем.** Новые версии кладём рядом: `manga-tone-v1.md`, `manga-tone-v2.md`, …
- `styles/manga-tone-v2.md` — оригинал + чуть более плоский задний фон (плоская заливка, одна тень, меньше бликов и мелочей) + матовый пол без отражений.
- `games/` — `31_zombie_zumba`, `35_vampire_vegan`, `37_coupon_queen`. Только тема, без строки `STYLE:`.
- `generated/` — картинки `<игра>--<стиль>.png` и галерея `index.html` для сравнения версий.

```sh
bash manga-dev/run.sh                              # все недостающие картинки (игры × стили)
bash manga-dev/run.sh --styles manga-tone-v1       # только одна версия стиля
bash manga-dev/run.sh --games 35                   # только Vampire Vegan
bash manga-dev/run.sh --games 35 --force           # перегенерировать
bash manga-dev/run.sh --games 35 --print           # показать собранный текст запроса
bash manga-dev/run.sh --dry-run                    # что будет сгенерировано
```
