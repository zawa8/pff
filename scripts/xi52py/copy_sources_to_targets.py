#!/usr/bin/env python3
"""
copy_sources_to_targets.py — step 0 of pipeline.
"""

import shutil
import logging
from pathlib import Path

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

logging.basicConfig(level=logging.INFO, format='%(message)s')

COPIES = [
    (
        pff_root / "sfdsrc/xe52/xe52asc.sfd",
        pff_root / "sfd/xi52sfd/xi52asc/xe52asc.sfd",
    ),
    (
        pff_root / "sfdsrc/xh38/xh38asc.sfd",
        pff_root / "sfd/xi38sfd/xi38asc/xh38asc.sfd",
    ),
]


def main():
    for src, dst in COPIES:
        if not src.exists():
            logging.error(f"Source not found: {src}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        logging.info(f"Copied: {src.name} -> {dst.parent.name}/{dst.name}")


if __name__ == "__main__":
    main()
