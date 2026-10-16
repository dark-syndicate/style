# manga-dev

Рабочая папка для доводки оригинального manga-tone на трёх играх 6x5.

- `styles/style4-manga-tone.md` — копия оригинала `styles/style4-manga-tone.md`. Правки стиля для этих игр вносятся здесь, общий файл не трогаем.
- `games/` — игры `31_zombie_zumba`, `35_vampire_vegan`, `37_coupon_queen`.
- `prompts/` — 3 готовых промпта.
- `prompts-generated/` — картинки и галерея `index.html`. Картинка Vampire Vegan уже есть: её прежний промпт полностью совпадает с нынешним.

```sh
bash manga-dev/run.sh                 # собрать промпты → сгенерировать недостающие → обновить галерею
bash manga-dev/run.sh --only 35_      # одна игра
bash manga-dev/run.sh --force         # перегенерировать после правки стиля
```
