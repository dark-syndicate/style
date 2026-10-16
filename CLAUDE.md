# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

There is no code here: no build, lint or test steps. The repo holds English-language text prompts for an image generator. Each prompt produces one finished 16:9 slot-game concept screen: a 5x5 symbol board in a themed frame, a logo in the upper left, a full-body cartoon mascot with a prop in the lower right, and an illustrated background. The user iterates on a shared art style across many game themes. The user usually writes in Russian.

## Structure

- `styles/`: shared prompt blocks. Each block is 4 lines covering composition, style, rendering and color. `styles/README.md` maps each style to the games that use it.
- `games/N_gamename.md`: one game per file. Line 1 is `STYLE: styles/<file>.md`, line 2 is blank, and the rest is the theme part starting with `TITLE exactly "..."`.
- `concepts/`: generated reference images (`v1.png`–`v3.png` correspond to games 1–3 in style 1).

To get a full prompt ready to paste, take the style file's text, then a blank line, then everything in the game file after the `STYLE:` line. When the user asks for prompts "with the style", give them fully assembled like this.

## Styles

Only five styles are kept in `styles/` (the rest were deleted on request; their text survives in git history and in the assembled prompts in `style-test/` and `style-picks/`):

1. `style1-evolved`: the original. Full detail, five gauges on the frame.
2. `style2-simplified`: slightly simpler shapes. No rust, wear or grime. Background is 3–4 big masses with no gradients. No gauges or indicators anywhere on the frame.
3. `style3-bold`: simpler still, with noticeably thicker outlines and the board EXACTLY IN THE CENTER. Used for animal and human mascots alike (the old `-human`/`-nocenter` variants were removed).
4. `style4-faceted-geo` and `style4-manga-tone`: MEDIUM detail (richer than style2, never as realistic as style1). `manga-tone` is the user's favourite; both work for animal and human mascots.

When changing a style, edit the file in `styles/`. Never paste style text back into the game files.

## Scripts and assembled prompt folders

- `scripts/build_prompts.py --games ... --styles ... --out <dir>` writes every game × style as a ready-to-paste prompt `<dir>/<game>--<style>.md`. If a game's theme says `6x5`, it rewrites the style's 5x5 composition line for a 6x5 board at assembly time. Styles stay 5x5 in `styles/`.
- `scripts/generate_style_tests.py [--input dir] [--output dir]` sends each prompt to the OpenAI Images API (`gpt-image-2.5-sunburst`, 2048x1152) and saves images. It needs `OPENAI_API_KEY` and skips images that already exist.
- `scripts/build_gallery.py [folder]` writes `<folder>/index.html`, a local page for comparing `<game>--<style>` images. It has duels with a swipe slider, stacked lists of all games and all styles (no selects, chips jump to a section), and a win-rate ranking (votes are kept in the browser's localStorage). `generate_style_tests.py` rebuilds it automatically after every run. For `<x>-generated` folders it also adds slots for prompts in `<x>/` that have no image yet.
- `scripts/serve_gallery.py <images folder>` serves the folder on http://localhost:8765/ with a `/__list` JSON endpoint; the gallery page then discovers every `<game>--<style>` image by itself and re-checks every 10 s, so it never needs rebuilding (opened via file:// it falls back to the embedded list). `manga-dev/view.sh` wraps it.
- `style-test/`: Lunar Junk in all styles. `style-picks/`: games 24–33 (6x5) in the 6 styles the user picked. `manga-dev/`: the current work folder. `styles/` holds only the active versions: `manga-tone-v1.md` is the current base (formerly v15); new iterations go next to it as `manga-tone-v2.md`, … Everything older (the original manga-tone, old v1, v12–v14) and old images live in `manga-dev/archive/` and are not used by the script. `games/` holds theme-only files (no STYLE line) for games 29, 35, 37 and 39–43 (flamboyant fictional 1980s tycoon mascots; never a real person's name or likeness, no drugs or weapons). There are no prompt files: `bash manga-dev/run.sh` (= `scripts/generate_combos.py --dir manga-dev`) assembles every game × style on the fly, sends the requests and writes `manga-dev/generated/<game>--<style>.png` plus the gallery. `build_prompts.py` accepts `--games-dir` and `--styles-dir` for such folders. Each folder's README has the rebuild command.

## Theme-part conventions (follow them in new games)

Each theme part needs:
- the exact title;
- a dark board color;
- a frame description with no gauges, dials or meters and a clean top edge;
- 5 themed symbols plus A K Q J glyphs built from theme materials;
- ONE special symbol with a tiny high-chroma accent;
- an original mascot (never a copied franchise character) with one clear cartoon gag;
- a compact vehicle or prop to lean on, with "Show whole mascot and ...";
- a background of 3–4 big masses;
- a palette line;
- a logo description.

Human mascots are described as adults. Women add "Capable, confident and stylish, not sexualized."

New games take the next number. A variant of an existing game keeps its number and adds a suffix, e.g. `1_lunar_junk-bold.md`.

## Git workflow

- Work only on `main`. Do not create feature branches.
- Commit and push to `main` as soon as a requested change is done; no need to wait for approval.
- The user also pushes generated images from their machine, so fetch first. If the push is rejected, rebase onto `origin/main` and push again.
- The session proxy rejects deleting remote branches (HTTP 403); the user has to do that themselves.
