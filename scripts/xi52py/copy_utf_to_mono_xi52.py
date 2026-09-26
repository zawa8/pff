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
src_dir = pff_root / "sfd/xi52sfd/xi52utf"

# Target (xi52mono)
target_dir = pff_root / "sfd/xi52sfd/xi52mono"
target_dir.mkdir(parents=True, exist_ok=True)

# Font mappings: (src_file, old_name, new_name)
FONTS = [
    ('xh52utf.sfd',    'xh52utf',    'xh52mono'),
    ('xb52utf.sfd',  'xb52utf',  'xb52mono'),
    ('xp52utf.sfd',   'xp52utf',   'xp52mono'),
    ('xg52utf.sfd',  'xg52utf',  'xg52mono'),
    ('xo52utf.sfd',    'xo52utf',    'xo52mono'),
    ('xt52utf.sfd',     'xt52utf',     'xt52mono'),
    ('xj52utf.sfd',   'xj52utf',   'xj52mono'),
    ('xk52utf.sfd',     'xk52utf',     'xk52mono'),
    ('xm52utf.sfd',  'xm52utf',  'xm52mono'),
    ('xs52utf.sfd',   'xs52utf',   'xs52mono'),
    ('xe52utf.sfd',   'xe52utf',   'xe52mono'),
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