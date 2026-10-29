#!/usr/bin/env python3
"""
p5generate.py

Generate TTF/WOFF2 from sfdfinal/**/*.sfd -> xnglofonts/

Structure:
  sfdfinal/xi38sfd/xi38asc/xh38asc.sfd
  -> xnglofonts/ttf/xi38ttf/xi38asc/xh38asc.ttf
  -> xnglofonts/woff2/xi38woff2/xi38asc/xh38asc.woff2

Run:
    fontforge -lang=py -script pysk/xi52py/p5generate.py
"""

import fontforge
import logging
import sys
from pathlib import Path
from datetime import datetime

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "p5generate.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

SFDFINAL_DIR = pff_root / "sfdfinal"
TTF_ROOT = pff_root / "xnglofonts" / "ttf"
WOFF2_ROOT = pff_root / "xnglofonts" / "woff2"


def process_sfd(sfd_path):
    """Generate TTF/WOFF2 from one SFD file."""
    # Relative path from sfdfinal
    rel = sfd_path.relative_to(SFDFINAL_DIR)
    # rel: xi38sfd/xi38asc/xh38asc.sfd
    
    parts = rel.parts
    family = parts[0]  # xi38sfd or xi52sfd
    variant = parts[1]  # xi38asc, xi38utf, xi38mono, ...
    name = sfd_path.stem  # xh38asc
    
    # Output dirs
    ttf_dir = TTF_ROOT / family.replace("sfd", "ttf") / variant
    woff2_dir = WOFF2_ROOT / family.replace("sfd", "woff2") / variant
    ttf_dir.mkdir(parents=True, exist_ok=True)
    woff2_dir.mkdir(parents=True, exist_ok=True)
    
    ttf_path = ttf_dir / f"{name}.ttf"
    woff2_path = woff2_dir / f"{name}.woff2"
    
    try:
        f = fontforge.open(str(sfd_path))
    except Exception as e:
        logging.error(f"Error opening {sfd_path}: {e}")
        return False
    
    try:
        f.generate(str(ttf_path))
        logging.info(f"TTF: {ttf_path.relative_to(pff_root)}")
        f.generate(str(woff2_path))
        logging.info(f"WOFF2: {woff2_path.relative_to(pff_root)}")
        f.close()
        return True
    except Exception as e:
        logging.error(f"Error generating {sfd_path}: {e}")
        try:
            f.close()
        except:
            pass
        return False


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")
    
    if not SFDFINAL_DIR.exists():
        print(f"ERROR: {SFDFINAL_DIR} not found")
        return
    
    # Find all .sfd
    sfd_files = sorted(SFDFINAL_DIR.glob("**/*.sfd"))
    print(f"Found {len(sfd_files)} .sfd files")
    
    success = 0
    fail = 0
    for sfd in sfd_files:
        if process_sfd(sfd):
            success += 1
        else:
            fail += 1
    
    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    logging.info(f"Success: {success}, Fail: {fail}")
    print(f"\nDone! Success: {success}, Fail: {fail}")
    print(f"Logs: {log_file}")


if __name__ == "__main__":
    main()
