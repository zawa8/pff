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
  hindixv52.sfd      -> hindixh52asc.sfd
  hindixv38.sfd      -> hindixh38asc.sfd
  hindixv52utf.sfd   -> hindixh52utf.sfd
  hindixv38utf.sfd   -> hindixh38utf.sfd
  hindixv52mono.sfd  -> hindixh52mono.sfd
  hindixv38mono.sfd  -> hindixh38mono.sfd
  hindixv52.ttf      -> hindixh52asc.ttf
  hindixv38.ttf      -> hindixh38asc.ttf
  hindixv52.woff2    -> hindixh52asc.woff2
  hindixv38.woff2    -> hindixh38asc.woff2
  bengalixb52.sfd    -> bengalixb52asc.sfd
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
    ("hindixv52.sfd", "hindixh52asc.sfd"),
    ("hindixv38.sfd", "hindixh38asc.sfd"),
    ("bengalixb52.sfd", "bengalixb52asc.sfd"),
    ("bengalixb38.sfd", "bengalixb38asc.sfd"),
    ("guzrajixg52.sfd", "guzrajixg52asc.sfd"),
    ("guzrajixg38.sfd", "guzrajixg38asc.sfd"),
    ("jeluguxj52.sfd", "jeluguxj52asc.sfd"),
    ("jeluguxj38.sfd", "jeluguxj38asc.sfd"),
    ("knRaxk52.sfd", "knRaxk52asc.sfd"),
    ("knRaxk38.sfd", "knRaxk38asc.sfd"),
    ("mlyalxmxm52.sfd", "mlyalxmxm52asc.sfd"),
    ("mlyalxmxm38.sfd", "mlyalxmxm38asc.sfd"),
    ("oriyaxo52.sfd", "oriyaxo52asc.sfd"),
    ("oriyaxo38.sfd", "oriyaxo38asc.sfd"),
    ("pnzabixp52.sfd", "pnzabixp52asc.sfd"),
    ("pnzabixp38.sfd", "pnzabixp38asc.sfd"),
    ("sinhlaxs52.sfd", "sinhlaxs52asc.sfd"),
    ("sinhlaxs38.sfd", "sinhlaxs38asc.sfd"),
    ("tmilxt52.sfd", "tmilxt52asc.sfd"),
    ("tmilxt38.sfd", "tmilxt38asc.sfd"),

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
    ("hindixv52.ttf", "hindixh52asc.ttf"),
    ("hindixv38.ttf", "hindixh38asc.ttf"),
    ("hindixv52.woff2", "hindixh52asc.woff2"),
    ("hindixv38.woff2", "hindixh38asc.woff2"),

    # File renames: xv -> xh (output names without extension)
    ("hindixv52", "hindixh52"),
    ("hindixv38", "hindixh38"),

    # English file renames (asc suffix)
    ("eNgliSxe52.sfd", "eNgliSxe52asc.sfd"),
    ("eNgliSxe38.sfd", "eNgliSxe38asc.sfd"),
    ("eNgliSxe52.ttf", "eNgliSxe52asc.ttf"),
    ("eNgliSxe38.ttf", "eNgliSxe38asc.ttf"),
    ("eNgliSxe52.woff2", "eNgliSxe52asc.woff2"),
    ("eNgliSxe38.woff2", "eNgliSxe38asc.woff2"),

    # Other .sfd asc files
    ("bengalixb52.sfd", "bengalixb52asc.sfd"),
    ("bengalixb38.sfd", "bengalixb38asc.sfd"),
    ("guzrajixg52.sfd", "guzrajixg52asc.sfd"),
    ("guzrajixg38.sfd", "guzrajixg38asc.sfd"),
    # ... (add all scripts)

    # .ttf and .woff2 without xv
    ("bengalixb52.ttf", "bengalixb52asc.ttf"),
    ("bengalixb38.ttf", "bengalixb38asc.ttf"),
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