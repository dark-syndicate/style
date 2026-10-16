#!/usr/bin/env bash
# Build the 3 prompts (Zombie Zumba, Vampire Vegan, Coupon Queen x original manga-tone),
# generate images, rebuild the gallery.
# Usage:  bash manga-dev/run.sh            (extra args go to the generator, e.g. --force, --only 35_)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_prompts.py \
  --games-dir manga-dev/games --styles-dir manga-dev/styles \
  --games 31 35 37 --styles style4-manga-tone \
  --out manga-dev/prompts
python3 scripts/generate_style_tests.py --input manga-dev/prompts --output manga-dev/prompts-generated "$@"
