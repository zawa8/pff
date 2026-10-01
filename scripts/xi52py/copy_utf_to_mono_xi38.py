#!/usr/bin/env python3
"""
copy_utf_to_mono_xi38.py

Create xi38mono fonts by copying xi38utf fonts, renaming, and making
the first 128 characters monospace (same width).

Mirrors copy_utf_to_mono_xi52.py.
"""

import fontforge
import logging
from datetime import datetime
from pathlib import Path

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "copy_utf_to_mono_xi38.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger("").addHandler(console)

# Source (xi38utf)
src_dir = pff_root / "sfd/xi38sfd/xi38utf"
# Target (xi38mono)
target_dir = pff_root / "sfd/xi38sfd/xi38mono"
target_dir.mkdir(parents=True, exist_ok=True)

# Font mappings: (src_file, old_name, new_name)
FONTS = [
    ("xh38utf.sfd", "xh38utf", "xh38mono"),
    ("xb38utf.sfd", "xb38utf", "xb38mono"),
    ("xp38utf.sfd", "xp38utf", "xp38mono"),
    ("xg38utf.sfd", "xg38utf", "xg38mono"),
    ("xo38utf.sfd", "xo38utf", "xo38mono"),
    ("xt38utf.sfd", "xt38utf", "xt38mono"),
    ("xj38utf.sfd", "xj38utf", "xj38mono"),
    ("xk38utf.sfd", "xk38utf", "xk38mono"),
    ("xm38utf.sfd", "xm38utf", "xm38mono"),
    ("xs38utf.sfd", "xs38utf", "xs38mono"),
    ("xe38utf.sfd", "xe38utf", "xe38mono"),
]

MONO_WIDTH = 600


def make_monospace(font):
    """Set first 128 characters to the same width."""
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
    """Copy xi38utf font to xi38mono with new name and monospace width."""
    src_path = src_dir / src_name
    target_path = target_dir / f"{new_name}.sfd"

    if not src_path.exists():
        logging.error(f"Source not found: {src_path}")
        return False

    logging.info(f"Processing: {src_name} -> {new_name}.sfd")

    try:
        font = fontforge.open(str(src_path))

        font.fontname = new_name
        font.fullname = new_name
        font.familyname = new_name
        font.weight = "Regular"

        logging.info(f"  Making first 128 chars monospace (width={MONO_WIDTH})")
        make_monospace(font)

        font.save(str(target_path))
        logging.info(f"  Saved: {target_path.name}")
        font.close()

        # Fix LangName in the saved SFD
        text = target_path.read_text(encoding="utf-8")
        text = text.replace(old_name, new_name)
        target_path.write_text(text, encoding="utf-8")
        logging.info(f"  Fixed LangName")

        return True
    except Exception as e:
        logging.error(f"  Error: {e}")
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
    print(f"\nDone! Logs: {log_file}")


if __name__ == "__main__":
    main()
