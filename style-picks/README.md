# Выбранные стили × 6 игр (6x5)

6 игр из `ideas/slot-ideas-6x5.md` (`games/24`–`29`), каждая в 6 выбранных стилях: 36 готовых промптов `<игра>--<стиль>.md`. Поле 6x5 подставляется при сборке, `styles/` не меняется.

| Игра | Маскот |
|---|---|
| `24_beam_me_moo` | пришелец-студент проваливает экзамен по похищению коров |
| `25_safecracker_sal` | женщина-медвежатница со стетоскопом и жвачкой |
| `26_goblin_garage` | гоблин-механик с гаечным ключом больше себя |
| `27_bowling_bears` | медведь-боулер, последняя кегля не падает |
| `28_quantum_cat` | кот-физик гордо показывает коробку, а из неё выглядывает его копия |
| `29_magnificent_mime` | мим упирается в невидимую стену, а на невидимой коробке сидит голубь |

Стили: `style4-manga-tone`, `style4-arcade-cabinet`, `style4-chrome-shine`, `style4-faceted-geo`, `style4-rubberhose-mix`, `style4-spooky-glow`.

Пересобрать промпты (из корня репозитория):

```sh
python3 scripts/build_prompts.py --games 24 25 26 27 28 29 --styles style4-manga-tone style4-arcade-cabinet style4-chrome-shine style4-faceted-geo style4-rubberhose-mix style4-spooky-glow --out style-picks
```

Сгенерировать картинки в `style-picks-generated/`:

```sh
python3 scripts/generate_style_tests.py --input style-picks --output style-picks-generated
```
