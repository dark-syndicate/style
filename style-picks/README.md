# Выбранные стили × 4 игры (6x5)

4 игры из `ideas/slot-ideas-6x5.md` (`games/24`–`27`), каждая в 6 выбранных стилях: 24 готовых промпта `<игра>--<стиль>.md`. Поле 6x5 подставляется при сборке, `styles/` не меняется.

| Игра | Маскот |
|---|---|
| `24_beam_me_moo` | пришелец-студент проваливает экзамен по похищению коров |
| `25_safecracker_sal` | женщина-медвежатница со стетоскопом и жвачкой |
| `26_goblin_garage` | гоблин-механик с гаечным ключом больше себя |
| `27_bowling_bears` | медведь-боулер, последняя кегля не падает |

Стили: `style4-manga-tone`, `style4-arcade-cabinet`, `style4-chrome-shine`, `style4-faceted-geo`, `style4-rubberhose-mix`, `style4-spooky-glow`.

Пересобрать промпты (из корня репозитория):

```sh
python3 scripts/build_prompts.py --games 24 25 26 27 --styles style4-manga-tone style4-arcade-cabinet style4-chrome-shine style4-faceted-geo style4-rubberhose-mix style4-spooky-glow --out style-picks
```

Сгенерировать картинки в `style-picks-generated/`:

```sh
python3 scripts/generate_style_tests.py --input style-picks --output style-picks-generated
```
