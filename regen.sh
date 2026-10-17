#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ffz -script notofonts/fill_asc-to-utf-csv.py
git diff --stat sfdsrc/asc-to-utf-generated.csv
