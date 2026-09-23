#!/usr/bin/env python3
"""
Generate TTF and WOFF2 from xi38asc SFD files.
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
log_file = log_dir / "generate_xi38asc.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source: xi38asc SFD
sfd_dir = pff_root / "sfd/xi38sfd/xi38asc"

# Output: xi38asc TTF
ttf_dir = pff_root / "xnglofonts/ttf/xi38ttf/xi38asc"
ttf_dir.mkdir(parents=True, exist_ok=True)

# Output: xi38asc WOFF2
woff2_dir = pff_root / "xnglofonts/woff2/xi38woff2/xi38asc"
woff2_dir.mkdir(parents=True, exist_ok=True)

FONTS = [
    'hindixh38asc.sfd',
    'bengalixb38asc.sfd',
    'pnzabixp38asc.sfd',
    'guzrajixg38asc.sfd',
    'oriyaxo38asc.sfd',
    'tmilxt38asc.sfd',
    'jeluguxj38asc.sfd',
    'knRaxk38asc.sfd',
    'mlyalxmxm38asc.sfd',
    'sinhlaxs38asc.sfd',
    'eNgliSxe38asc.sfd',
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
