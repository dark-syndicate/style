#!/usr/bin/env bash
# Build the 16 prompts (4 games x 4 manga-tone variants), generate images, rebuild the gallery.
# Run from anywhere:  bash manga-lab/run.sh            (all 16)
#                     bash manga-lab/run.sh --only 34_  (extra args go to the generator)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_prompts.py \
  --games-dir manga-lab/games --styles-dir manga-lab/styles \
  --games 34 35 36 37 \
  --styles manga-tone-original manga-tone-bold-icons manga-tone-ink-icons manga-tone-premium-icons \
  --out manga-lab/prompts
python3 scripts/generate_style_tests.py --input manga-lab/prompts --output manga-lab/prompts-generated "$@"
