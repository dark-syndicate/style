#!/usr/bin/env bash
# Generate every game in manga-dev/games x every style in manga-dev/styles straight to
# manga-dev/generated/ (no prompt files), then rebuild the gallery manga-dev/generated/index.html.
# Usage:  bash manga-dev/run.sh                            missing images only
#         bash manga-dev/run.sh --styles manga-tone-v1     one style
#         bash manga-dev/run.sh --games 35 --force         redo one game
#         bash manga-dev/run.sh --games 35 --print         show the assembled request text
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate_combos.py --dir manga-dev "$@"
