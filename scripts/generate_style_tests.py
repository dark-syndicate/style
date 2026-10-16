#!/usr/bin/env python3
"""Generate an image for every prompt in a folder (default style-test/) via the OpenAI Images API.

Usage (from the repo root):
    pip install openai
    export OPENAI_API_KEY=sk-...
    python scripts/generate_style_tests.py                    # all prompts
    python scripts/generate_style_tests.py --only neon-rim    # names containing "neon-rim"
    python scripts/generate_style_tests.py --dry-run          # list what would be generated
    python scripts/generate_style_tests.py --input style-picks --output style-picks-generated

Images are saved to <output>/<prompt name>.<format>. Existing images are
skipped unless --force is given, so an interrupted run can simply be restarted.
"""

import argparse
import base64
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "style-test"
OUT_DIR = ROOT / "style-generated"


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="style-test", help="folder with prompt .md files")
    p.add_argument("--output", default="style-generated", help="folder for generated images")
    p.add_argument("--model", default="gpt-image-2.5-sunburst")
    p.add_argument("--size", default="2048x1152", help="WIDTHxHEIGHT, default is 16:9 2K")
    p.add_argument("--quality", default="high", help="auto, low, medium, high, ...")
    p.add_argument("--format", default="png", choices=["png", "jpeg", "webp"])
    p.add_argument("--only", action="append", default=[], help="substring filter on file name, repeatable")
    p.add_argument("--workers", type=int, default=5, help="parallel requests")
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--force", action="store_true", help="regenerate even if the image exists")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def collect_jobs(args):
    prompts = sorted(f for f in PROMPTS_DIR.glob("*.md") if f.name != "README.md")
    if args.only:
        prompts = [f for f in prompts if any(s in f.stem for s in args.only)]
    jobs = []
    for f in prompts:
        out = OUT_DIR / f"{f.stem}.{args.format}"
        if out.exists() and not args.force:
            continue
        jobs.append((f, out))
    return prompts, jobs


def generate(client, args, prompt_file, out_file):
    prompt = prompt_file.read_text(encoding="utf-8").strip()
    for attempt in range(1, args.retries + 1):
        try:
            res = client.images.generate(
                model=args.model,
                prompt=prompt,
                size=args.size,
                quality=args.quality,
                output_format=args.format,
                n=1,
            )
            item = res.data[0]
            if item.b64_json:
                data = base64.b64decode(item.b64_json)
            else:
                with urllib.request.urlopen(item.url) as r:
                    data = r.read()
            tmp = out_file.with_suffix(out_file.suffix + ".part")
            tmp.write_bytes(data)
            tmp.replace(out_file)
            return
        except Exception as e:
            if attempt == args.retries:
                raise
            wait = 5 * 2 ** (attempt - 1)
            print(f"  retry {attempt}/{args.retries - 1} for {prompt_file.stem} in {wait}s: {e}", flush=True)
            time.sleep(wait)


def main():
    global PROMPTS_DIR, OUT_DIR
    args = parse_args()
    PROMPTS_DIR, OUT_DIR = ROOT / args.input, ROOT / args.output
    if not PROMPTS_DIR.is_dir():
        sys.exit(f"input folder {args.input} not found")
    prompts, jobs = collect_jobs(args)
    print(f"{len(prompts)} prompts, {len(prompts) - len(jobs)} already generated, {len(jobs)} to go")
    if args.dry_run or not jobs:
        for f, out in jobs:
            print(f"  {f.relative_to(ROOT)} -> {out.relative_to(ROOT)}")
        return 0

    OUT_DIR.mkdir(exist_ok=True)
    client = OpenAI()  # reads OPENAI_API_KEY from the environment
    failed = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(generate, client, args, f, out): f for f, out in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            name = futures[fut].stem
            try:
                fut.result()
                print(f"[{i}/{len(jobs)}] ok    {name}", flush=True)
            except Exception as e:
                failed.append(name)
                print(f"[{i}/{len(jobs)}] FAIL  {name}: {e}", flush=True)

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_gallery
    build_gallery.build(OUT_DIR, args.only)
    if failed:
        print(f"\n{len(failed)} failed, rerun to retry them: {', '.join(failed)}")
        return 1
    print(f"\nDone, images are in {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
