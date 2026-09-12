#!/usr/bin/env python3
"""
Script to copy specific characters from eNgliSxe52.sfd
to all 10 xi52 language fonts.
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
log_file = log_dir / "copy_e52_chars_xi52.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source
src_sfd = pff_root / "sfd/xi52font/xi52asc/eNgliSxe52.sfd"

# Target folder
target_dir = pff_root / "sfd/xi52font/xi52asc"

# Target fonts (10 languages)
TARGET_FONTS = [
    'hindixv52.sfd',
    'bengalixb52.sfd',
    'pnzabixp52.sfd',
    'guzrajixg52.sfd',
    'oriyaxo52.sfd',
    'tmilxt52.sfd',
    'jeluguxj52.sfd',
    'knRaxk52.sfd',
    'mlyalxmxm52.sfd',
    'sinhlaxs52.sfd',
]

# Characters to copy (ASCII codes)
CHARS_TO_COPY = [
    ord('c'),  # 99
    ord('C'),  # 67
    ord('g'),  # 103
    ord('G'),  # 71
    ord('q'),  # 113
    ord('Q'),  # 81
    ord('j'),  # 106
    ord('J'),  # 74
    ord('x'),  # 120
    ord('X'),  # 88
    ord('v'),  # 118
]


def copy_chars_to_target(target_name, eng_font):
    """Copy specific chars from English to target."""
    target_path = target_dir / target_name

    if not target_path.exists():
        logging.error(f"Target not found: {target_path}")
        return 0

    logging.info(f"Processing: {target_name}")

    try:
        target_font = fontforge.open(str(target_path))

        copied = 0

        for ascii_code in CHARS_TO_COPY:
            if ascii_code not in eng_font:
                logging.warning(f"  ASCII {ascii_code} not in English")
                continue

            if ascii_code not in target_font:
                logging.warning(f"  ASCII {ascii_code} not in {target_name}")
                continue

            try:
                # Copy from English
                eng_font.selection.select(ascii_code)
                eng_font.copy()

                # Paste to target
                target_font.selection.select(ascii_code)
                glyph = target_font[ascii_code]
                glyph.clear()
                target_font.paste()

                char = chr(ascii_code)
                logging.debug(f"  ✓ Copied '{char}'")
                copied += 1

            except Exception as e:
                logging.warning(f"  ✗ Error {ascii_code}: {e}")

        # Save
        target_font.save(str(target_path))
        logging.info(f"  ✓ Saved: {target_name} ({copied} chars)")
        target_font.close()
        return copied

    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return 0


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")
    logging.info(f"Source: {src_sfd.name}")
    logging.info(f"Chars: {[chr(c) for c in CHARS_TO_COPY]}")

    if not src_sfd.exists():
        print(f"✗ Source not found: {src_sfd}")
        return

    # Open English source
    eng_font = fontforge.open(str(src_sfd))

    total = 0
    for target_name in TARGET_FONTS:
        copied = copy_chars_to_target(target_name, eng_font)
        total += copied

    eng_font.close()

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    logging.info(f"Total copied: {total}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()