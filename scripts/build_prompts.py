#!/usr/bin/env python3
"""Assemble ready-to-paste prompts: every game x every style.

Each output file is <out>/<game>--<style>.md = style text + blank line + the game's
theme part (everything after its STYLE: line). Games whose theme mentions "6x5" get
the style's 5x5 composition line rewritten for a 6x5 board; styles/ itself is not changed.

Example (from the repo root):
    python scripts/build_prompts.py --games 24 25 26 27 \
        --styles style4-manga-tone style4-arcade-cabinet --out style-picks
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES_DIR = ROOT / "games"
STYLES_DIR = ROOT / "styles"

GRID_6X5 = [
    ("large nearly square 5x5 symbol board", "large wide 6x5 symbol board (6 reels, 5 rows)"),
    ("All 25 symbol cells", "All 30 symbol cells"),
    ("about 85% of canvas height", "about 78% of canvas height"),
]


def find_game(key):
    """Accept a game number ("24"), a file stem ("24_beam_me_moo") or a path."""
    path = Path(key)
    if path.suffix == ".md" and path.exists():
        return path
    exact = GAMES_DIR / f"{key}.md"
    if exact.exists():
        return exact
    matches = sorted(GAMES_DIR.glob(f"{key}_*.md"))
    matches = [m for m in matches if "-" not in m.stem]  # skip variants like 1_lunar_junk-bold
    if len(matches) != 1:
        sys.exit(f"game '{key}': expected one match in {GAMES_DIR.name}/, found {[m.name for m in matches]}")
    return matches[0]


def find_style(key):
    path = STYLES_DIR / f"{Path(key).stem}.md"
    if not path.exists():
        sys.exit(f"style '{key}' not found in {STYLES_DIR}")
    return path


def theme_part(game_file):
    lines = game_file.read_text(encoding="utf-8").split("\n")
    if not lines[0].startswith("STYLE:"):
        sys.exit(f"{game_file.name}: first line must be 'STYLE: ...'")
    return "\n".join(lines[1:]).strip("\n")


def adapt_grid(style_text, theme, style_name):
    if "6x5" not in theme:
        return style_text
    for old, new in GRID_6X5:
        if old not in style_text:
            sys.exit(f"{style_name}: cannot adapt to 6x5, text '{old}' not found")
        style_text = style_text.replace(old, new)
    return style_text


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--games", nargs="+", required=True)
    p.add_argument("--styles", nargs="+", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--games-dir", default="games", help="folder with game theme files")
    p.add_argument("--styles-dir", default="styles", help="folder with style files")
    args = p.parse_args()

    global GAMES_DIR, STYLES_DIR
    GAMES_DIR, STYLES_DIR = ROOT / args.games_dir, ROOT / args.styles_dir

    games = [find_game(g) for g in args.games]
    styles = [find_style(s) for s in args.styles]
    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for g in games:
        theme = theme_part(g)
        for s in styles:
            style_text = adapt_grid(s.read_text(encoding="utf-8").strip("\n"), theme, s.stem)
            (out_dir / f"{g.stem}--{s.stem}.md").write_text(f"{style_text}\n\n{theme}\n", encoding="utf-8")
            count += 1
    print(f"wrote {count} prompts to {out_dir.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
