#!/usr/bin/env python3
"""Generate images straight from a work folder: every game x every style, no prompt files.

The folder must contain games/ (theme files, first line STYLE: ...) and styles/ (style blocks).
Each request is assembled on the fly (style + blank line + theme, 6x5 adaptation as in
build_prompts.py) and sent to the OpenAI Images API. Images land in <dir>/generated/ as
<game>--<style>.png, and <dir>/generated/index.html (comparison gallery) is rebuilt.

Examples (from the repo root):
    python3 scripts/generate_combos.py --dir manga-dev                         # everything missing
    python3 scripts/generate_combos.py --dir manga-dev --styles manga-tone-v1  # one style
    python3 scripts/generate_combos.py --dir manga-dev --games 35 --force      # redo one game
    python3 scripts/generate_combos.py --dir manga-dev --games 35 --styles manga-tone-v1 --print
"""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_gallery  # noqa: E402
import build_prompts  # noqa: E402
from generate_style_tests import generate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dir", required=True, help="work folder with games/ and styles/")
    p.add_argument("--games", nargs="+", help="game numbers or file stems (default: all in <dir>/games)")
    p.add_argument("--styles", nargs="+", help="style file stems (default: all in <dir>/styles)")
    p.add_argument("--only", action="append", default=[], help="substring filter on <game>--<style>, repeatable")
    p.add_argument("--print", action="store_true", help="print the assembled prompts and exit")
    p.add_argument("--dry-run", action="store_true", help="list what would be generated")
    p.add_argument("--force", action="store_true", help="regenerate even if the image exists")
    p.add_argument("--model", default="gpt-image-2.5-sunburst")
    p.add_argument("--size", default="2048x1152")
    p.add_argument("--quality", default="high")
    p.add_argument("--format", default="png", choices=["png", "jpeg", "webp"])
    p.add_argument("--workers", type=int, default=5)
    p.add_argument("--retries", type=int, default=3)
    return p.parse_args()


def main():
    args = parse_args()
    work = ROOT / args.dir
    build_prompts.GAMES_DIR, build_prompts.STYLES_DIR = work / "games", work / "styles"
    games = ([build_prompts.find_game(g) for g in args.games] if args.games
             else sorted(f for f in build_prompts.GAMES_DIR.glob("*.md") if f.name != "README.md"))
    styles = ([build_prompts.find_style(s) for s in args.styles] if args.styles
              else sorted(f for f in build_prompts.STYLES_DIR.glob("*.md") if f.name != "README.md"))
    if not games or not styles:
        sys.exit(f"need at least one game and one style in {args.dir}/games and {args.dir}/styles")

    out_dir = work / "generated"
    combos = []
    for g in games:
        theme = build_prompts.theme_part(g)
        for s in styles:
            name = f"{g.stem}--{s.stem}"
            if args.only and not any(o in name for o in args.only):
                continue
            style_text = build_prompts.adapt_grid(s.read_text(encoding="utf-8").strip("\n"), theme, s.stem)
            combos.append((name, f"{style_text}\n\n{theme}", out_dir / f"{name}.{args.format}"))

    if args.print:
        for name, prompt, _ in combos:
            print(f"===== {name}\n{prompt}\n")
        return 0
    jobs = [c for c in combos if args.force or not c[2].exists()]
    print(f"{len(combos)} combinations, {len(combos) - len(jobs)} already generated, {len(jobs)} to go")
    if args.dry_run:
        for name, _, out in jobs:
            print(f"  {name} -> {out.relative_to(ROOT)}")
        return 0

    failed = []
    if jobs:
        from openai import OpenAI
        out_dir.mkdir(parents=True, exist_ok=True)
        client = OpenAI()  # reads OPENAI_API_KEY from the environment
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(generate, client, args, None, out, prompt): name for name, prompt, out in jobs}
            for i, fut in enumerate(as_completed(futures), 1):
                name = futures[fut]
                try:
                    fut.result()
                    print(f"[{i}/{len(jobs)}] ok    {name}", flush=True)
                except Exception as e:
                    failed.append(name)
                    print(f"[{i}/{len(jobs)}] FAIL  {name}: {e}", flush=True)

    all_slots = [f"{g.stem}--{s.stem}" for g in games for s in styles]
    build_gallery.build(out_dir, args.only, all_slots)
    if failed:
        print(f"\n{len(failed)} failed, rerun to retry them: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
