#!/usr/bin/env bash
# Vampire Vegan in original manga-tone vs manga-tone + bold symbols: build prompts, generate, rebuild gallery.
# Usage:  bash manga-bold/run.sh            (extra args go to the generator, e.g. --force)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_prompts.py \
  --games-dir manga-bold/games --styles-dir manga-bold/styles \
  --games 35 \
  --styles manga-tone-original manga-tone-bold-symbols \
  --out manga-bold/prompts
python3 scripts/generate_style_tests.py --input manga-bold/prompts --output manga-bold/prompts-generated "$@"
