#!/usr/bin/env python3
"""
Generate TTF and WOFF2 from xi38utf SFD files (p1onli branch).

Adapted from scripts/xi38py/generate_utf_ttf.py: same FONTS list and
generate_fonts() logic, but pointed at this branch's canonical output
location (xnglofonts/ttf|woff2/xi38fonts/xi38utf, matching the
xnglofonts/ttf/xi38fonts/readme.md placeholder already in the repo,
and the same convention glyph_kopi_u9scripts_p1onli.py already uses
for xi38asc) instead of the original's hardcoded Windows path.

This is the step that was missing from main.py's pipeline: step 3
(glyph_kopi_u2utf_p1onli.py) builds the p1onli-restricted
sfd/xi38font/xi38utf/*.sfd files, but nothing turned those into usable
.ttf/.woff2 -- this script is that step.
"""

import fontforge
import logging
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent.parent  # generatefonts/ is 2 levels deeper than xi52py/'s other scripts

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "generate_xi38utf_ttf_p1onli.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# UTF folder (source)
utf_dir = pff_root / "sfd/xi38font/xi38utf"

# Output
ttf_dir = pff_root / "xnglofonts/ttf/xi38fonts/xi38utf"
woff2_dir = pff_root / "xnglofonts/woff2/xi38fonts/xi38utf"
ttf_dir.mkdir(parents=True, exist_ok=True)
woff2_dir.mkdir(parents=True, exist_ok=True)

FONTS = [
    'hindixv38utf.sfd',
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

        base_name = sfd_path.stem  # e.g. hindixv38utf

        # Generate TTF
        ttf_path = ttf_dir / f"{base_name}.ttf"
        font.generate(str(ttf_path))
        logging.info(f"  \u2713 TTF: {ttf_path.name}")

        # Generate WOFF2
        woff2_path = woff2_dir / f"{base_name}.woff2"
        font.generate(str(woff2_path))
        logging.info(f"  \u2713 WOFF2: {woff2_path.name}")

        font.close()
        return True

    except Exception as e:
        logging.error(f"  \u2717 Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for font_name in FONTS:
        sfd_path = utf_dir / font_name
        generate_fonts(sfd_path)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n\u2713 Done! Logs: {log_file}")


if __name__ == "__main__":
    main()
