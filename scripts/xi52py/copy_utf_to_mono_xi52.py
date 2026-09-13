#!/usr/bin/env python3
"""
Script to create xi52mono fonts by copying xi52utf fonts,
changing names, and making first 128 chars monospace.
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
log_file = log_dir / "copy_utf_to_mono_xi52.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source (xi52utf)
src_dir = pff_root / "sfd/xi52font/xi52utf"

# Target (xi52mono)
target_dir = pff_root / "sfd/xi52font/xi52mono"
target_dir.mkdir(parents=True, exist_ok=True)

# Font mappings: (src_file, old_name, new_name)
FONTS = [
    ('hindixv52utf.sfd',    'hindixv52utf',    'hindixv52mono'),
    ('bengalixb52utf.sfd',  'bengalixb52utf',  'bengalixb52mono'),
    ('pnzabixp52utf.sfd',   'pnzabixp52utf',   'pnzabixp52mono'),
    ('guzrajixg52utf.sfd',  'guzrajixg52utf',  'guzrajixg52mono'),
    ('oriyaxo52utf.sfd',    'oriyaxo52utf',    'oriyaxo52mono'),
    ('tmilxt52utf.sfd',     'tmilxt52utf',     'tmilxt52mono'),
    ('jeluguxj52utf.sfd',   'jeluguxj52utf',   'jeluguxj52mono'),
    ('knRaxk52utf.sfd',     'knRaxk52utf',     'knRaxk52mono'),
    ('mlyalxmxm52utf.sfd',  'mlyalxmxm52utf',  'mlyalxmxm52mono'),
    ('sinhlaxs52utf.sfd',   'sinhlaxs52utf',   'sinhlaxs52mono'),
    ('eNgliSxe52utf.sfd',   'eNgliSxe52utf',   'eNgliSxe52mono'),
]

# Monospace width
MONO_WIDTH = 600  # Adjust as needed


def make_monospace(font):
    """Make first 128 characters same width."""
    for ascii_code in range(128):
        if ascii_code not in font:
            continue
        try:
            glyph = font[ascii_code]
            if glyph:
                glyph.width = MONO_WIDTH
                logging.debug(f"    Set width {MONO_WIDTH} for ASCII {ascii_code}")
        except Exception as e:
            logging.warning(f"    Error setting width {ascii_code}: {e}")


def copy_font(src_name, old_name, new_name):
    """Copy xi52utf font to xi52mono with new name and monospace."""
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

        # Make monospace
        logging.info(f"  Making first 128 chars monospace (width={MONO_WIDTH})")
        make_monospace(font)

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
    logging.info(f"Mono width: {MONO_WIDTH}")

    for src_name, old_name, new_name in FONTS:
        copy_font(src_name, old_name, new_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()