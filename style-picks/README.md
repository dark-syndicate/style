# Выбранные стили × 10 игр (6x5)

10 игр из `ideas/slot-ideas-6x5.md` (`games/24`–`33`), каждая в 6 выбранных стилях: 60 готовых промптов `<игра>--<стиль>.md`. Поле 6x5 подставляется при сборке, `styles/` не меняется.

| Игра | Маскот |
|---|---|
| `24_beam_me_moo` | пришелец-студент проваливает экзамен по похищению коров |
| `25_safecracker_sal` | женщина-медвежатница со стетоскопом и жвачкой |
| `26_goblin_garage` | гоблин-механик с гаечным ключом больше себя |
| `27_bowling_bears` | медведь-боулер, последняя кегля не падает |
| `28_quantum_cat` | кот-физик гордо показывает коробку, а из неё выглядывает его копия |
| `29_magnificent_mime` | мим упирается в невидимую стену, а на невидимой коробке сидит голубь |
| `30_dragon_dentist` | стоматолог рвёт зуб маленькому дракону, а его чих опалил ей хвост волос |
| `31_zombie_zumba` | зомби-тренер танцует, а отвалившаяся рука танцует сама рядом |
| `32_beaver_builders` | бобр-прораб закрыл лицо огромным чертежом, хвост держит шаткую стопку брёвен |
| `33_claw_crab` | краб держит приз, а клешня автомата поднимает его самого за кепку |

Стили: `style4-manga-tone`, `style4-arcade-cabinet`, `style4-chrome-shine`, `style4-faceted-geo`, `style4-rubberhose-mix`, `style4-spooky-glow`.

Пересобрать промпты (из корня репозитория). Внимание: из этих 6 стилей в `styles/` остались только `style4-manga-tone` и `style4-faceted-geo`, поэтому команду ниже нужно сократить до них; уже собранные промпты в папке сохраняют полный текст всех 6 стилей.

```sh
python3 scripts/build_prompts.py --games 24 25 26 27 28 29 30 31 32 33 --styles style4-manga-tone style4-arcade-cabinet style4-chrome-shine style4-faceted-geo style4-rubberhose-mix style4-spooky-glow --out style-picks
```

Сгенерировать картинки в `style-picks-generated/`:

```sh
python3 scripts/generate_style_tests.py --input style-picks --output style-picks-generated
```

Сравнить стили: откройте `style-picks-generated/index.html` (дуэли, сетки, рейтинг). После генерации новых картинок обновите страницу:

```sh
python3 scripts/build_gallery.py style-picks-generated
```
