#!/usr/bin/env python3
"""
Generate TTF and WOFF2 from xi38utf SFD files.
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
log_file = log_dir / "generate_utf_ttf.log"

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
utf_dir = pff_root / "sfd/xi38sfd/xi38utf"

# Output
font_repo = Path("C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font")
ttf_dir = font_repo / "ttf/hscii/xi38utf"
woff2_dir = font_repo / "woff2/hscii/xi38utf"
ttf_dir.mkdir(parents=True, exist_ok=True)
woff2_dir.mkdir(parents=True, exist_ok=True)

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


def generate_fonts(sfd_path):
    """Generate TTF and WOFF2 from SFD."""
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return False

    logging.info(f"Processing: {sfd_path.name}")

    try:
        font = fontforge.open(str(sfd_path))

        base_name = sfd_path.stem  # e.g. hindixh38utf

        # Generate TTF
        ttf_path = ttf_dir / f"{base_name}.ttf"
        font.generate(str(ttf_path))
        logging.info(f"  ✓ TTF: {ttf_path.name}")

        # Generate WOFF2
        woff2_path = woff2_dir / f"{base_name}.woff2"
        font.generate(str(woff2_path))
        logging.info(f"  ✓ WOFF2: {woff2_path.name}")

        font.close()
        return True

    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for font_name in FONTS:
        sfd_path = utf_dir / font_name
        generate_fonts(sfd_path)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()