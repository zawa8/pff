#!/usr/bin/env python3
"""
Script to add Unicode ranges with REFERENCE copies to xi38utf SFD files.

Uses copyReference() API from FontForge.
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
log_file = log_dir / "add_unicode_ranges_utf.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

utf_dir = pff_root / "sfd/xi38sfd/xi38utf"

FONTS = [
    'hindixh38utf.sfd',
    'bengalixb38utf.sfd',
    'pnzabixp38utf.sfd',
    'guzrajixg38utf.sfd',
    'oriyaxo38utf.sfd',
    'tmilxt38utf.sfd',
    'jeluguxj38utf.sfd',
    'knRaxk38utf.sfd',
    'mlyalxmxm38utf.sfd',
    'sinhlaxs38utf.sfd',
    'eNgliSxe38utf.sfd',
]

UNICODE_RANGES = [
    0x0900, 0x0980, 0x0A00, 0x0A80, 0x0B00,
    0x0B80, 0x0C00, 0x0C80, 0x0D00, 0x0D80,
]

UNICODE_HINDI_ARRAY = [
    '', 'N', 'N', ':', 'xe', 'x', 'a', 'i', 'i', 'u', 'u', 'r', 'l',
    'e', 'e', 'e', 'e', 'o', 'o', 'o', 'o',
    'k', 'K', 'g', 'G', 'N', 'c', 'C', 'z', 'Z', 'n',
    't', 'J', 'd', 'Q', 'n', 'T', 'j', 'D', 'q', 'n', 'n',
    'p', 'f', 'b', 'B', 'm', 'y', 'r', 'r', 'l', 'l', 'l', 'w', 'S', 's', 's', 'H',
    'oe', 'ui', '', '!',
    'a', 'i', 'i', 'u', 'u', 'r', 'r', 'e', 'e', 'e', 'e', 'o', 'o', 'o', 'o',
    '', '', 'o', 'om', '', '', '`', "'", 'eei', 'ui', 'uui',
    'k', 'K', 'g', 'z', 'R', 'R', 'f', 'y', 'r', 'l', 'l', 'l',
    '.', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '_', '__', 'A', 'o', 'o', 'o', 'u', 'u', 'q', 'Z', 'y', 'n', 'z', '?', 'd', 'b',
]


def add_unicode_ranges(utf_path):
    """Add Unicode ranges with REFERENCE copies."""
    if not utf_path.exists():
        logging.error(f"Not found: {utf_path}")
        return 0

    logging.info(f"Processing: {utf_path.name}")

    try:
        font = fontforge.open(str(utf_path))
    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return 0

    total_added = 0

    for base_unicode in UNICODE_RANGES:
        range_added = 0

        for offset in range(128):
            dst_unicode = base_unicode + offset

            if offset >= len(UNICODE_HINDI_ARRAY):
                continue

            hskii_chars = UNICODE_HINDI_ARRAY[offset]
            if not hskii_chars:
                continue

            hskii_char = hskii_chars[0]
            src_ascii = ord(hskii_char)

            if src_ascii not in font:
                continue

            try:
                # Select source
                font.selection.select(src_ascii)
                font.copyReference()      # ← REFERENCE COPY!

                # Create destination if not exists
                if dst_unicode not in font:
                    font.createChar(dst_unicode)

                # Select and paste
                font.selection.select(dst_unicode)
                font.clear()
                font.paste()

                range_added += 1
                total_added += 1

            except Exception as e:
                logging.warning(f"  Error U+{dst_unicode:04X}: {e}")

        if range_added > 0:
            logging.info(f"  U+{base_unicode:04X}: {range_added}")

    try:
        font.save(str(utf_path))
        logging.info(f"  ✓ Saved: {utf_path.name} ({total_added} total)")
    except Exception as e:
        logging.error(f"  ✗ Save error: {e}")

    font.close()
    return total_added


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for font_name in FONTS:
        utf_path = utf_dir / font_name
        add_unicode_ranges(utf_path)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()