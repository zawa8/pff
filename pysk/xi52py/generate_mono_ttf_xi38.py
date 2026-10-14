#!/usr/bin/env python3
"""
generate_mono_ttf_xi38.py

Generate TTF and WOFF2 from xi38mono SFD files.

Mirrors generate_mono_ttf.py (for xi52mono).
"""

import fontforge
import logging
from datetime import datetime
from pathlib import Path

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "generate_mono_ttf_xi38.log"

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

ttf_dir = pff_root / "xnglofonts/ttf/xi38ttf/xi38mono"
woff2_dir = pff_root / "xnglofonts/woff2/xi38woff2/xi38mono"
ttf_dir.mkdir(parents=True, exist_ok=True)
woff2_dir.mkdir(parents=True, exist_ok=True)

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


def generate_fonts(sfd_path):
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return False

    logging.info(f"Processing: {sfd_path.name}")

    try:
        font = fontforge.open(str(sfd_path))
        base_name = sfd_path.stem

        ttf_path = ttf_dir / f"{base_name}.ttf"
        font.generate(str(ttf_path))
        logging.info(f"  TTF: {ttf_path.name}")

        woff2_path = woff2_dir / f"{base_name}.woff2"
        font.generate(str(woff2_path))
        logging.info(f"  WOFF2: {woff2_path.name}")

        font.close()
        return True
    except Exception as e:
        logging.error(f"  Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for font_name in FONTS:
        sfd_path = mono_dir / font_name
        generate_fonts(sfd_path)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\nDone! Logs: {log_file}")


if __name__ == "__main__":
    main()
