#!/usr/bin/env bash
# Vampire Vegan in the ORIGINAL style4-manga-tone (styles/style4-manga-tone.md, untouched):
# build the prompt, generate the image, rebuild the gallery.
# Usage:  bash vampire-manga/run.sh            (extra args go to the generator, e.g. --force)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_prompts.py \
  --games-dir vampire-manga/games \
  --games 35 --styles style4-manga-tone \
  --out vampire-manga/prompts
python3 scripts/generate_style_tests.py --input vampire-manga/prompts --output vampire-manga/prompts-generated "$@"
