#!/usr/bin/env python3
"""
Script to center all glyphs in xi52mono fonts using FontForge API.
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
log_file = log_dir / "center_glyphs_mono_xi52.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Mono folder
mono_dir = pff_root / "sfd/xi52sfd/xi52mono"

FONTS = [
    'hindixh52mono.sfd',
    'bengalixb52mono.sfd',
    'pnzabixp52mono.sfd',
    'guzrajixg52mono.sfd',
    'oriyaxo52mono.sfd',
    'tmilxt52mono.sfd',
    'jeluguxj52mono.sfd',
    'knRaxk52mono.sfd',
    'mlyalxmxm52mono.sfd',
    'sinhlaxs52mono.sfd',
    'eNgliSxe52mono.sfd',
]

MONO_WIDTH = 600


def center_glyph(glyph, mono_width):
    """Center a single glyph horizontally."""
    try:
        # Get bounding box (floats)
        bbox = glyph.boundingBox()
        left, bottom, right, top = bbox

        # Actual glyph width (float → int)
        actual_width = int(right - left)

        # Skip empty glyphs
        if actual_width <= 0:
            glyph.width = mono_width
            return False

        # Calculate centered position (int)
        new_lsb = int((mono_width - actual_width) / 2)

        # Apply
        glyph.left_side_bearing = new_lsb
        glyph.width = mono_width

        return True

    except Exception as e:
        logging.warning(f"    Error: {e}")
        return False


def process_font(sfd_name):
    """Center all glyphs in font."""
    sfd_path = mono_dir / sfd_name

    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return 0

    logging.info(f"Processing: {sfd_name}")

    try:
        font = fontforge.open(str(sfd_path))

        centered = 0
        total = 0

        for ascii_code in range(128):
            if ascii_code not in font:
                continue

            glyph = font[ascii_code]
            if not glyph:
                continue

            total += 1
            if center_glyph(glyph, MONO_WIDTH):
                centered += 1

        logging.info(f"  ✓ {sfd_name}: {centered}/{total} centered")

        font.save(str(sfd_path))
        font.close()
        return centered

    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return 0


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")
    logging.info(f"Folder: {mono_dir}")
    logging.info(f"Mono width: {MONO_WIDTH}")

    total = 0
    for sfd_name in FONTS:
        total += process_font(sfd_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    logging.info(f"Total centered: {total}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()