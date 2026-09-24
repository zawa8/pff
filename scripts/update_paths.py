#!/usr/bin/env python3
"""
update_paths.py — bulk update old paths to new naming convention.

Rules:
  sfd/xi52font       -> sfd/xi52sfd
  sfd/xi38font       -> sfd/xi38sfd
  ttf/xi52fonts      -> ttf/xi52ttf
  ttf/xi38fonts      -> ttf/xi38ttf
  woff2/xi52fonts    -> woff2/xi52woff2
  woff2/xi38fonts    -> woff2/xi38woff2
  hindixv52.sfd      -> xh52asc.sfd
  hindixv38.sfd      -> xh38asc.sfd
  hindixv52utf.sfd   -> hindixh52utf.sfd
  hindixv38utf.sfd   -> hindixh38utf.sfd
  hindixv52mono.sfd  -> hindixh52mono.sfd
  hindixv38mono.sfd  -> hindixh38mono.sfd
  hindixv52.ttf      -> xh52asc.ttf
  hindixv38.ttf      -> xh38asc.ttf
  hindixv52.woff2    -> xh52asc.woff2
  hindixv38.woff2    -> xh38asc.woff2
  bengalixb52.sfd    -> xb52asc.sfd
  ... (same for all scripts)

Run from repo root:
    python scripts/update_paths.py
"""

from pathlib import Path
import re

REPO = Path("C:/progxs/pff")
SCRIPTS_DIR = REPO / "scripts"

# Ordered replacements (longest patterns first to avoid partial matches)
REPLACEMENTS = [
    # Folder renames
    ("sfd/xi52font", "sfd/xi52sfd"),
    ("sfd/xi38font", "sfd/xi38sfd"),
    ("sfd\\xi52font", "sfd\\xi52sfd"),
    ("sfd\\xi38font", "sfd\\xi38sfd"),

    # TTF folder renames
    ("ttf/xi52fonts", "ttf/xi52ttf"),
    ("ttf/xi38fonts", "ttf/xi38ttf"),
    ("ttf\\xi52fonts", "ttf\\xi52ttf"),
    ("ttf\\xi38fonts", "ttf\\xi38ttf"),

    # WOFF2 folder renames
    ("woff2/xi52fonts", "woff2/xi52woff2"),
    ("woff2/xi38fonts", "woff2/xi38woff2"),
    ("woff2\\xi52fonts", "woff2\\xi52woff2"),
    ("woff2\\xi38fonts", "woff2\\xi38woff2"),

    # File renames: xv -> xh with asc suffix (asc files)
    ("hindixv52.sfd", "xh52asc.sfd"),
    ("hindixv38.sfd", "xh38asc.sfd"),
    ("bengalixb52.sfd", "xb52asc.sfd"),
    ("bengalixb38.sfd", "xb38asc.sfd"),
    ("guzrajixg52.sfd", "xg52asc.sfd"),
    ("guzrajixg38.sfd", "xg38asc.sfd"),
    ("jeluguxj52.sfd", "xj52asc.sfd"),
    ("jeluguxj38.sfd", "xj38asc.sfd"),
    ("knRaxk52.sfd", "xk52asc.sfd"),
    ("knRaxk38.sfd", "xk38asc.sfd"),
    ("mlyalxmxm52.sfd", "xm52asc.sfd"),
    ("mlyalxmxm38.sfd", "xm38asc.sfd"),
    ("oriyaxo52.sfd", "xo52asc.sfd"),
    ("oriyaxo38.sfd", "xo38asc.sfd"),
    ("pnzabixp52.sfd", "xp52asc.sfd"),
    ("pnzabixp38.sfd", "xp38asc.sfd"),
    ("sinhlaxs52.sfd", "xs52asc.sfd"),
    ("sinhlaxs38.sfd", "xs38asc.sfd"),
    ("tmilxt52.sfd", "xt52asc.sfd"),
    ("tmilxt38.sfd", "xt38asc.sfd"),

    # File renames: xv -> xh (utf files)
    ("hindixv52utf.sfd", "hindixh52utf.sfd"),
    ("hindixv38utf.sfd", "hindixh38utf.sfd"),
    ("hindixv52utf", "hindixh52utf"),
    ("hindixv38utf", "hindixh38utf"),

    # File renames: xv -> xh (mono files)
    ("hindixv52mono.sfd", "hindixh52mono.sfd"),
    ("hindixv38mono.sfd", "hindixh38mono.sfd"),
    ("hindixv52mono", "hindixh52mono"),
    ("hindixv38mono", "hindixh38mono"),

    # File renames: xv -> xh (ttf/woff2 asc)
    ("hindixv52.ttf", "xh52asc.ttf"),
    ("hindixv38.ttf", "xh38asc.ttf"),
    ("hindixv52.woff2", "xh52asc.woff2"),
    ("hindixv38.woff2", "xh38asc.woff2"),

    # File renames: xv -> xh (output names without extension)
    ("hindixv52", "hindixh52"),
    ("hindixv38", "hindixh38"),

    # English file renames (asc suffix)
    ("eNgliSxe52.sfd", "xe52asc.sfd"),
    ("eNgliSxe38.sfd", "xe38asc.sfd"),
    ("eNgliSxe52.ttf", "xe52asc.ttf"),
    ("eNgliSxe38.ttf", "xe38asc.ttf"),
    ("eNgliSxe52.woff2", "xe52asc.woff2"),
    ("eNgliSxe38.woff2", "xe38asc.woff2"),

    # Other .sfd asc files
    ("bengalixb52.sfd", "xb52asc.sfd"),
    ("bengalixb38.sfd", "xb38asc.sfd"),
    ("guzrajixg52.sfd", "xg52asc.sfd"),
    ("guzrajixg38.sfd", "xg38asc.sfd"),
    # ... (add all scripts)

    # .ttf and .woff2 without xv
    ("bengalixb52.ttf", "xb52asc.ttf"),
    ("bengalixb38.ttf", "xb38asc.ttf"),
    # ... (add all scripts)
]


def update_file(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for py in SCRIPTS_DIR.rglob("*.py"):
        if py.name == "update_paths.py":
            continue
        if update_file(py):
            changed.append(py.relative_to(REPO))

    print(f"Updated {len(changed)} files:")
    for p in changed:
        print(f"  {p}")


if __name__ == "__main__":
    main()