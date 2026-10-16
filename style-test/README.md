# Тест стилей

LUNAR JUNK (игра 1), собранный во всех стилях из `styles/`, по одному готовому промпту на файл: `1_lunar_junk--<стиль>.md` = текст стиля + пустая строка + тема. Для `style1-evolved` тема берётся из `games/1_lunar_junk.md` (с приборами), для остальных — из `games/1_lunar_junk-simplified.md`.

После правок в `styles/` пересоберите командой из корня репозитория:

```sh
for s in styles/*.md; do n=$(basename "$s" .md); [ "$n" = README ] && continue; g=games/1_lunar_junk-simplified.md; [ "$n" = style1-evolved ] && g=games/1_lunar_junk.md; { cat "$s"; echo; tail -n +3 "$g"; } > "style-test/1_lunar_junk--$n.md"; done
```
