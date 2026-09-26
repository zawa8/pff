#!/usr/bin/env python3
"""
fix_script_refs.py — one-off utility.

Replaces legacy .sfd basenames with new ones in all pipeline scripts.

Usage:
    python scripts/xi52py/tools/fix_script_refs.py --dry
    python scripts/xi52py/tools/fix_script_refs.py
"""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
PFF_ROOT = HERE.parent.parent.parent

# old -> new (filename stems and possibly full names)
REPLACEMENTS = [
    # English
    ("eNgliSxe38utf",  "xe38utf"),
    ("eNgliSxe52utf",  "xe52utf"),
    ("eNgliSxe52mono", "xe52mono"),
    # Hindi
    ("hindixh38utf",   "xh38utf"),
    ("hindixh52utf",   "xh52utf"),
    ("hindixh52mono",  "xh52mono"),
    ("hindixv38",      "xh38"),
    ("hindixv52",      "xh52"),
    # Bengali
    ("bengalixb38utf",  "xb38utf"),
    ("bengalixb52utf",  "xb52utf"),
    ("bengalixb52mono", "xb52mono"),
    # Punjabi
    ("pnzabixp38utf",   "xp38utf"),
    ("pnzabixp52utf",   "xp52utf"),
    ("pnzabixp52mono",  "xp52mono"),
    # Gujarati
    ("guzrajixg38utf",  "xg38utf"),
    ("guzrajixg52utf",  "xg52utf"),
    ("guzrajixg52mono", "xg52mono"),
    # Oriya
    ("oriyaxo38utf",    "xo38utf"),
    ("oriyaxo52utf",    "xo52utf"),
    ("oriyaxo52mono",   "xo52mono"),
    # Tamil
    ("tmilxt38utf",     "xt38utf"),
    ("tmilxt52utf",     "xt52utf"),
    ("tmilxt52mono",    "xt52mono"),
    # Telugu
    ("jeluguxj38utf",   "xj38utf"),
    ("jeluguxj52utf",   "xj52utf"),
    ("jeluguxj52mono",  "xj52mono"),
    # Kannada
    ("knRaxk38utf",     "xk38utf"),
    ("knRaxk52utf",     "xk52utf"),
    ("knRaxk52mono",    "xk52mono"),
    # Malayalam
    ("mlyalxmxm38utf",  "xm38utf"),
    ("mlyalxmxm52utf",  "xm52utf"),
    ("mlyalxmxm52mono", "xm52mono"),
    # Sinhala
    ("sinhlaxs38utf",   "xs38utf"),
    ("sinhlaxs52utf",   "xs52utf"),
    ("sinhlaxs52mono",  "xs52mono"),
]

TARGETS = [
    PFF_ROOT / "scripts/xi52py/add_unicode_ranges_utf_52.py",
    PFF_ROOT / "scripts/xi52py/center_glyphs_mono_xi52.py",
    PFF_ROOT / "scripts/xi52py/copy_e52utf_chars_xi52utf.py",
    PFF_ROOT / "scripts/xi52py/copy_utf_to_mono_xi52.py",
    PFF_ROOT / "scripts/xi52py/copy_xi38utf_to_xi52utf.py",
    PFF_ROOT / "scripts/xi52py/copy_xi38_to_xi52.py",
    PFF_ROOT / "scripts/xi52py/fix_mono_width_xi52.py",
    PFF_ROOT / "scripts/xi52py/generatefonts/gen_xi38utf.py",
    PFF_ROOT / "scripts/xi52py/generatefonts/gen_xi52utf.py",
    PFF_ROOT / "scripts/xi52py/generate_mono_ttf.py",
    PFF_ROOT / "scripts/xi52py/glyph_copy/build_utf_fonts.py",
    PFF_ROOT / "scripts/xi52py/rename_utf_fonts_52.py",
]


def process(path: Path, dry: bool) -> int:
    if not path.exists():
        print(f"  missing: {path}")
        return 0
    text = path.read_text(encoding="utf-8")
    orig = text
    hits = 0
    for old, new in REPLACEMENTS:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            hits += n
    if text == orig:
        print(f"  no change: {path.name}")
        return 0
    print(f"  {hits} repl: {path.name}")
    if not dry:
        path.write_text(text, encoding="utf-8")
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    total = 0
    for p in TARGETS:
        total += process(p, args.dry)
    verb = "would be " if args.dry else ""
    print(f"\n{total} replacement(s) {verb}made.")


if __name__ == "__main__":
    main()