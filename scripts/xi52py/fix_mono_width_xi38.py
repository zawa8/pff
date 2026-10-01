#!/usr/bin/env python3
"""
fix_mono_width_xi38.py

Fix xi38mono fonts:
1. Scale glyphs that overflow 600 (like 'f')
2. Set reference glyphs width to 600

Mirrors fix_mono_width_xi52.py.
"""

import fontforge
import logging
from datetime import datetime
from pathlib import Path

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "fix_mono_width_xi38.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger("").addHandler(console)

mono_dir = pff_root / "sfd/xi38sfd/xi38mono"

FONTS = [
    "xh38mono.sfd",
    "xb38mono.sfd",
    "xp38mono.sfd",
    "xg38mono.sfd",
    "xo38mono.sfd",
    "xt38mono.sfd",
    "xj38mono.sfd",
    "xk38mono.sfd",
    "xm38mono.sfd",
    "xs38mono.sfd",
    "xe38mono.sfd",
]

MONO_WIDTH = 600
MARGIN = 20


def get_bbox_width(glyph):
    try:
        bbox = glyph.boundingBox()
        return int(bbox[2] - bbox[0]), bbox
    except Exception:
        return 0, None


def process_font(sfd_name):
    sfd_path = mono_dir / sfd_name
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return

    logging.info(f"\nProcessing: {sfd_name}")

    try:
        font = fontforge.open(str(sfd_path))
        available = MONO_WIDTH - 2 * MARGIN

        scaled = 0
        for ascii_code in range(128):
            if ascii_code not in font:
                continue
            glyph = font[ascii_code]
            if not glyph:
                continue

            actual_width, bbox = get_bbox_width(glyph)
            if actual_width > available:
                scale = available / actual_width
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2
                glyph.transform((
                    scale, 0,
                    0, scale,
                    -center_x * scale + center_x,
                    -center_y * scale + center_y,
                ))
                scaled += 1
                logging.info(f"  Scaled '{chr(ascii_code)}' (was {actual_width})")

        centered = 0
        for ascii_code in range(128):
            if ascii_code not in font:
                continue
            glyph = font[ascii_code]
            if not glyph:
                continue
            actual_width, bbox = get_bbox_width(glyph)
            if actual_width <= 0:
                glyph.width = MONO_WIDTH
                continue
            if actual_width > MONO_WIDTH:
                scale = MONO_WIDTH / actual_width
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2
                glyph.transform((
                    scale, 0,
                    0, scale,
                    -center_x * scale + center_x,
                    -center_y * scale + center_y,
                ))
                actual_width, bbox = get_bbox_width(glyph)
            new_lsb = int((MONO_WIDTH - actual_width) / 2)
            glyph.left_side_bearing = new_lsb
            glyph.width = MONO_WIDTH
            centered += 1

        fixed = 0
        for glyph in font.glyphs():
            try:
                if glyph.unicode < 128:
                    continue
                if not glyph.references:
                    continue
                glyph.width = MONO_WIDTH
                fixed += 1
            except Exception:
                pass

        logging.info(f"  {sfd_name}: {scaled} scaled, {centered} centered, {fixed} refs fixed")
        font.save(str(sfd_path))
        font.close()
    except Exception as e:
        logging.error(f"  Error: {e}")


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for sfd_name in FONTS:
        process_font(sfd_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\nDone! Logs: {log_file}")


if __name__ == "__main__":
    main()
