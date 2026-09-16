#!/usr/bin/env python3
"""
Generate TTF and WOFF2 from xi52asc SFD files.
"""

import fontforge
import logging
from pathlib import Path
from datetime import datetime

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "generate_xi52asc.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source: xi52asc SFD
sfd_dir = pff_root / "sfd/xi52font/xi52asc"

# Output: xi52asc TTF
ttf_dir = pff_root / "xnglofonts/ttf/xi52fonts/xi52asc"
ttf_dir.mkdir(parents=True, exist_ok=True)

# Output: xi52asc WOFF2
woff2_dir = pff_root / "xnglofonts/woff2/xi52fonts/xi52asc"
woff2_dir.mkdir(parents=True, exist_ok=True)

FONTS = [
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
    'eNgliSxe52.sfd',
]


def generate_fonts(sfd_path):
    """Generate TTF and WOFF2 from SFD."""
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return False

    logging.info(f"Processing: {sfd_path.name}")

    try:
        font = fontforge.open(str(sfd_path))
        base_name = sfd_path.stem

        # TTF
        ttf_path = ttf_dir / f"{base_name}.ttf"
        font.generate(str(ttf_path))
        logging.info(f"  ✓ TTF: {ttf_path.name}")

        # WOFF2
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
        sfd_path = sfd_dir / font_name
        generate_fonts(sfd_path)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()