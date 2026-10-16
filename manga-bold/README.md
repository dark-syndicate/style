# Manga-tone + bold symbols

Оригинальный `style4-manga-tone` (как в `style-picks`) с символами из `manga-lab` bold-icons. Пока одна игра: **Vampire Vegan**.

| Стиль | Что это |
|---|---|
| `manga-tone-original.md` | точная копия `styles/style4-manga-tone.md`, эталон |
| `manga-tone-bold-symbols.md` | тот же оригинал, к которому добавлены только символы из bold-icons: крупные (~85% ячейки), пухлые, ракурс 3/4, толстый контур со светлым кантом, буквы A K Q J разных цветов, спецсимвол крупнее и со вспышкой. Фон, скринтон, пол и детализация такие же, как в оригинале |

```sh
bash manga-bold/run.sh            # 2 промпта → 2 картинки → галерея manga-bold/prompts-generated/index.html
bash manga-bold/run.sh --force    # перегенерировать
```
