#!/usr/bin/env python3
"""
Script to update font names in xi38utf SFD files using FontForge API.
Changes ALL occurrences: hindixv38 → hindixv38utf
"""

import fontforge
import re
import logging
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "rename_utf_fonts.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# UTF folder
utf_dir = pff_root / "sfd/xi38font/xi38utf"

# Font name mappings (old → new)
FONT_RENAMES = {
    'hindixv38utf.sfd':    ('hindixv38',    'hindixv38utf'),
    'bengalixb38utf.sfd':  ('bengalixb38',  'bengalixb38utf'),
    'pnzabixp38utf.sfd':   ('pnzabixp38',   'pnzabixp38utf'),
    'guzrajixg38utf.sfd':  ('guzrajixg38',  'guzrajixg38utf'),
    'oriyaxo38utf.sfd':    ('oriyaxo38',    'oriyaxo38utf'),
    'tmilxt38utf.sfd':     ('tmilxt38',     'tmilxt38utf'),
    'jeluguxj38utf.sfd':   ('jeluguxj38',   'jeluguxj38utf'),
    'knRaxk38utf.sfd':     ('knRaxk38',     'knRaxk38utf'),
    'mlyalxmxm38utf.sfd':  ('mlyalxmxm38',  'mlyalxmxm38utf'),
    'sinhlaxs38utf.sfd':   ('sinhlaxs38',   'sinhlaxs38utf'),
    'eNgliSxe38utf.sfd':   ('eNgliSxe38',   'eNgliSxe38utf'),
}


def update_font_name(sfd_path, old_name, new_name):
    """Update font name in SFD file - ALL occurrences."""
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return False

    logging.info(f"Processing: {sfd_path.name}")

    try:
        # Open font
        font = fontforge.open(str(sfd_path))

        # Set font names via FontForge API
        font.fontname = new_name
        font.fullname = new_name
        font.familyname = new_name
        font.weight = "Regular"

        # Save (this updates FontName, FullName, FamilyName)
        font.save(str(sfd_path))

        # Now fix LangName line manually (FontForge API doesn't touch it)
        text = sfd_path.read_text(encoding='utf-8')

        # Replace ALL occurrences of old_name with new_name
        # But be careful: old_name might be part of new_name
        # Use word boundary regex
        text = re.sub(
            rf'\b{re.escape(old_name)}\b',
            new_name,
            text
        )

        sfd_path.write_text(text, encoding='utf-8')

        # Count replacements
        count = text.count(new_name)
        logging.info(f"  ✓ Updated: {sfd_path.name} ({count} occurrences)")
        return True

    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")
    logging.info(f"Directory: {utf_dir}")

    for sfd_name, (old_name, new_name) in FONT_RENAMES.items():
        sfd_path = utf_dir / sfd_name
        update_font_name(sfd_path, old_name, new_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()