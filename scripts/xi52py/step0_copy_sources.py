#!/usr/bin/env python3
"""
step0_copy_sources.py — step 1 of pipeline.

Copies master SFDs from sfdsrc/ into sfd/ targets.
Sources are never modified.

Sources:
  - sfdsrc/xe52/xe52asc.sfd    -> sfd/xi52sfd/xi52asc/xe52asc.sfd
  - sfdsrc/xi38/*.sfd          -> sfd/xi38sfd/xi38asc/*.sfd
"""

import shutil
import logging
from pathlib import Path

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

logging.basicConfig(level=logging.INFO, format='%(message)s')


def copy_dir(src_dir: Path, dst_dir: Path) -> int:
    """Copy all *.sfd from src_dir to dst_dir. Returns count."""
    if not src_dir.exists():
        logging.warning(f"Source dir not found: {src_dir}")
        return 0
    dst_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for src in sorted(src_dir.glob("*.sfd")):
        dst = dst_dir / src.name
        shutil.copy2(src, dst)
        logging.info(f"Copied: {src.name} -> {dst.parent.name}/{dst.name}")
        n += 1
    return n


def main():
    total = 0
    total += copy_dir(pff_root / "sfdsrc/xe52",
                      pff_root / "sfd/xi52sfd/xi52asc")
    total += copy_dir(pff_root / "sfdsrc/xi38",
                      pff_root / "sfd/xi38sfd/xi38asc")
    logging.info(f"Total copied: {total}")


if __name__ == "__main__":
    main()
