#!/usr/bin/env python3
"""
Fix xi52mono fonts:
1. Scale glyphs that overflow 600 (like 'f')
2. Set reference glyphs width to 600
"""

import fontforge
import logging
from pathlib import Path
from datetime import datetime

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "fix_mono_width_xi52.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

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
MARGIN = 20


def get_bbox_width(glyph):
    """Get glyph bbox width."""
    try:
        bbox = glyph.boundingBox()
        return int(bbox[2] - bbox[0]), bbox
    except:
        return 0, None


def scale_glyph(glyph, target_width):
    """Scale glyph to fit target."""
    actual_width, bbox = get_bbox_width(glyph)
    if actual_width <= target_width:
        return False
    
    scale = target_width / actual_width
    
    # Scale around center
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2
    
    glyph.transform((
        scale, 0,
        0, scale,
        -center_x * scale + center_x,
        -center_y * scale + center_y
    ))
    return True


def center_glyph(glyph, mono_width):
    """Center glyph."""
    try:
        actual_width, bbox = get_bbox_width(glyph)
        if actual_width <= 0:
            glyph.width = mono_width
            return False
        
        new_lsb = int((mono_width - actual_width) / 2)
        glyph.left_side_bearing = new_lsb
        glyph.width = mono_width
        return True
    except:
        return False


def process_font(sfd_name):
    sfd_path = mono_dir / sfd_name
    if not sfd_path.exists():
        logging.error(f"Not found: {sfd_path}")
        return

    logging.info(f"\nProcessing: {sfd_name}")

    try:
        font = fontforge.open(str(sfd_path))
        available = MONO_WIDTH - 2 * MARGIN

        # Step 1: Scale overflow glyphs
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
                
                # Center around center
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2
                
                glyph.transform((
                    scale, 0,
                    0, scale,
                    -center_x * scale + center_x,
                    -center_y * scale + center_y
                ))
                scaled += 1
                logging.info(f"  Scaled '{chr(ascii_code)}' (was {actual_width})")

        # Step 2: RE-CALCULATE bbox after scaling, then center
        centered = 0
        for ascii_code in range(128):
            if ascii_code not in font:
                continue
            glyph = font[ascii_code]
            if not glyph:
                continue
            
            # RECALCULATE
            actual_width, bbox = get_bbox_width(glyph)
            if actual_width <= 0:
                glyph.width = MONO_WIDTH
                continue
            
            # Force bbox to fit (if still overflow)
            if actual_width > MONO_WIDTH:
                scale = MONO_WIDTH / actual_width
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2
                glyph.transform((
                    scale, 0,
                    0, scale,
                    -center_x * scale + center_x,
                    -center_y * scale + center_y
                ))
                actual_width, bbox = get_bbox_width(glyph)
            
            # Center
            new_lsb = int((MONO_WIDTH - actual_width) / 2)
            glyph.left_side_bearing = new_lsb
            glyph.width = MONO_WIDTH
            centered += 1

        # Step 3: Fix reference glyphs
        fixed = 0
        for glyph in font.glyphs():
            try:
                if glyph.unicode < 128:
                    continue
                if not glyph.references:
                    continue
                glyph.width = MONO_WIDTH
                fixed += 1
            except:
                pass

        logging.info(f"  ✓ {sfd_name}: {scaled} scaled, {centered} centered, {fixed} refs fixed")

        font.save(str(sfd_path))
        font.close()

    except Exception as e:
        logging.error(f"  ✗ Error: {e}")

def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for sfd_name in FONTS:
        process_font(sfd_name)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()