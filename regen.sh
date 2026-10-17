#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

FFZ="${FFZ:-/c/Program Files/FontForgeBuilds/bin/fontforge.exe}"
if [ ! -x "$FFZ" ]; then
    echo "ERROR: fontforge not found at $FFZ" >&2
    echo "Set FFZ env var or edit this script" >&2
    exit 1
fi

"$FFZ" -script notofonts/fill_asc-to-utf-csv.py
git diff --stat sfdsrc/asc-to-utf-generated.csv
