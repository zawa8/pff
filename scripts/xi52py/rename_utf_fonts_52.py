#!/usr/bin/env python3
"""
Script to update font names in xi52utf SFD files.
Changes: hindixh52 → hindixh52utf
"""

import fontforge
import re
import logging
from pathlib import Path
from datetime import datetime

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "rename_utf_fonts_52.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

utf_dir = pff_root / "sfd/xi52sfd/xi52utf"

FONT_RENAMES = {
    'hindixh52utf.sfd':    ('hindixh52',    'hindixh52utf'),
    'bengalixb52utf.sfd':  ('bengalixb52',  'bengalixb52utf'),
    'pnzabixp52utf.sfd':   ('pnzabixp52',   'pnzabixp52utf'),
    'guzrajixg52utf.sfd':  ('guzrajixg52',  'guzrajixg52utf'),
    'oriyaxo52utf.sfd':    ('oriyaxo52',    'oriyaxo52utf'),
    'tmilxt52utf.sfd':     ('tmilxt52',     'tmilxt52utf'),
    'jeluguxj52utf.sfd':   ('jeluguxj52',   'jeluguxj52utf'),
    'knRaxk52utf.sfd':     ('knRaxk52',     'knRaxk52utf'),
    'mlyalxmxm52utf.sfd':  ('mlyalxmxm52',  'mlyalxmxm52utf'),
    'sinhlaxs52utf.sfd':   ('sinhlaxs52',   'sinhlaxs52utf'),
    'eNgliSxe52utf.sfd':   ('eNgliSxe52',   'eNgliSxe52utf'),
}


def update_font_name(sfd_path, old_name, new_name):
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return False

    logging.info(f"Processing: {sfd_path.name}")

    try:
        font = fontforge.open(str(sfd_path))
        font.fontname = new_name
        font.fullname = new_name
        font.familyname = new_name
        font.weight = "Regular"
        font.save(str(sfd_path))

        # Fix LangName
        text = sfd_path.read_text(encoding='utf-8')
        text = re.sub(rf'\b{re.escape(old_name)}\b', new_name, text)
        sfd_path.write_text(text, encoding='utf-8')

        logging.info(f"  ✓ Updated: {sfd_path.name}")
        return True
    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for sfd_name, (old_name, new_name) in FONT_RENAMES.items():
        sfd_path = utf_dir / sfd_name
        update_font_name(sfd_path, old_name, new_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()