#!/usr/bin/env python3
"""
Script to create xi52 fonts by copying xi38asc fonts
and changing font names (38 → 52).
"""

import fontforge
import logging
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "copy_xi38_to_xi52.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source (xi38asc)
src_dir = pff_root / "sfd/xi38sfd/xi38asc"

# Target (xi52asc)
target_dir = pff_root / "sfd/xi52sfd/xi52asc"
target_dir.mkdir(parents=True, exist_ok=True)

# Font mappings: (src_file, old_name, new_name)
FONTS = [
    ('xe38asc.sfd',   'eNgliSxe38',   'eNgliSxe52'),
    ('xh38asc.sfd',    'hindixh38',    'hindixh52'),
    ('xb38asc.sfd',  'bengalixb38',  'bengalixb52'),
    ('xp38asc.sfd',   'pnzabixp38',   'pnzabixp52'),
    ('xg38asc.sfd',  'guzrajixg38',  'guzrajixg52'),
    ('xo38asc.sfd',    'oriyaxo38',    'oriyaxo52'),
    ('xt38asc.sfd',     'tmilxt38',     'tmilxt52'),
    ('xj38asc.sfd',   'jeluguxj38',   'jeluguxj52'),
    ('xk38asc.sfd',     'knRaxk38',     'knRaxk52'),
    ('xm38asc.sfd',  'mlyalxmxm38',  'mlyalxmxm52'),
    ('xs38asc.sfd',   'sinhlaxs38',   'sinhlaxs52'),
]


def copy_font(src_name, old_name, new_name):
    """Copy xi38 font to xi52 with new name."""
    src_path = src_dir / src_name
    target_path = target_dir / f"{new_name}.sfd"

    if not src_path.exists():
        logging.error(f"Source not found: {src_path}")
        return False

    logging.info(f"Processing: {src_name} → {new_name}.sfd")

    try:
        # Open source
        font = fontforge.open(str(src_path))

        # Change names
        font.fontname = new_name
        font.fullname = new_name
        font.familyname = new_name
        font.weight = "Regular"

        # Save to target
        font.save(str(target_path))
        logging.info(f"  ✓ Saved: {target_path.name}")

        font.close()

        # Fix LangName
        text = target_path.read_text(encoding='utf-8')
        text = text.replace(old_name, new_name)
        target_path.write_text(text, encoding='utf-8')
        logging.info(f"  ✓ Fixed LangName")

        return True

    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")
    logging.info(f"Source: {src_dir}")
    logging.info(f"Target: {target_dir}")

    for src_name, old_name, new_name in FONTS:
        copy_font(src_name, old_name, new_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()