#!/usr/bin/env python3
"""
Script to create xi52utf fonts by copying xi38utf fonts
and changing font names (38utf → 52utf).

References are already in xi38utf, no need to add again.
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
log_file = log_dir / "copy_xi38utf_to_xi52utf.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source (xi38utf)
src_dir = pff_root / "sfd/xi38font/xi38utf"

# Target (xi52utf)
target_dir = pff_root / "sfd/xi52font/xi52utf"
target_dir.mkdir(parents=True, exist_ok=True)

# Font mappings: (src_file, old_name, new_name)
FONTS = [
    ('hindixv38utf.sfd',    'hindixv38utf',    'hindixv52utf'),
    ('bengalixb38utf.sfd',  'bengalixb38utf',  'bengalixb52utf'),
    ('pnzabixp38utf.sfd',   'pnzabixp38utf',   'pnzabixp52utf'),
    ('guzrajixg38utf.sfd',  'guzrajixg38utf',  'guzrajixg52utf'),
    ('oriyaxo38utf.sfd',    'oriyaxo38utf',    'oriyaxo52utf'),
    ('tmilxt38utf.sfd',     'tmilxt38utf',     'tmilxt52utf'),
    ('jeluguxj38utf.sfd',   'jeluguxj38utf',   'jeluguxj52utf'),
    ('knRaxk38utf.sfd',     'knRaxk38utf',     'knRaxk52utf'),
    ('mlyalxmxm38utf.sfd',  'mlyalxmxm38utf',  'mlyalxmxm52utf'),
    ('sinhlaxs38utf.sfd',   'sinhlaxs38utf',   'sinhlaxs52utf'),
    ('eNgliSxe38utf.sfd',   'eNgliSxe38utf',   'eNgliSxe52utf'),
]


def copy_font(src_name, old_name, new_name):
    """Copy xi38utf font to xi52utf with new name."""
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