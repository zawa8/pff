#!/usr/bin/env python3
"""
Script to copy glyphs from Noto font to xi38asc SFD for 9 Indian scripts.

Consonants: from Noto (script-specific)
English chars (E,F,L,M,N,O,P,U,V,W,X,Y,a,i,u,e,o): from eNgliSxe38.sfd
x and A: अ from Noto (respective Indian language)
R (ड़): from Noto Devanagari (Hindi only)
"""

import sys
import fontforge
import logging
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "glyph_kopi_u9scripts.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source: English font
english_sfd = pff_root / "sfd/x38ifont/x38iasc/eNgliSxe38.sfd"

# Source: Noto Devanagari (for ड़)
noto_devanagari = pff_root / "notofonts/NotoSansDevanagari-Regular.ttf"

# 9 scripts configuration
SCRIPTS = {
    'hindi': {
        'noto': 'NotoSansDevanagari-Regular.ttf',
        'sfd': 'hindixv38.sfd',
        'output': 'hindixv38',
        'base_unicode': 0x0900,
    },
    'bengali': {
        'noto': 'NotoSansBengali-Regular.ttf',
        'sfd': 'bengalixb38.sfd',
        'output': 'bengalixb38',
        'base_unicode': 0x0980,
    },
    'punjabi': {
        'noto': 'NotoSansGurmukhi-Regular.ttf',
        'sfd': 'pnzabixp38.sfd',
        'output': 'pnzabixp38',
        'base_unicode': 0x0A00,
    },
    'gujarati': {
        'noto': 'NotoSansGujarati-Regular.ttf',
        'sfd': 'guzrajixg38.sfd',
        'output': 'guzrajixg38',
        'base_unicode': 0x0A80,
    },
    'oriya': {
        'noto': 'NotoSansOriya-Regular.ttf',
        'sfd': 'oriyaxo38.sfd',
        'output': 'oriyaxo38',
        'base_unicode': 0x0B00,
    },
    'tamil': {
        'noto': 'NotoSansTamil-Regular.ttf',
        'sfd': 'tmilxt38.sfd',
        'output': 'tmilxt38',
        'base_unicode': 0x0B80,
    },
    'telugu': {
        'noto': 'NotoSansTelugu-Regular.ttf',
        'sfd': 'jeluguxj38.sfd',
        'output': 'jeluguxj38',
        'base_unicode': 0x0C00,
    },
    'kannada': {
        'noto': 'NotoSansKannada-Regular.ttf',
        'sfd': 'knRaxk38.sfd',
        'output': 'knRaxk38',
        'base_unicode': 0x0C80,
    },
    'malayalam': {
        'noto': 'NotoSansMalayalam-Regular.ttf',
        'sfd': 'mlyalxmxm38.sfd',
        'output': 'mlyalxmxm38',
        'base_unicode': 0x0D00,
    },
}

# CONSONANTS: from Noto (script-specific) # 0915 क
CONSONANT_MAP = {
    ### below are hewing issues for 52 series and p1only branch
    ### so comment in case of 52 series and p1only branch
    0x1A: 'c',
    0x1B: 'C',
    0x17: 'g', 0x18: 'G',
    0x20: 'J', 0x25: 'j',
    0x27: 'q', 0x22: 'Q',
    0x39: 'v', 0x5: 'x',
    
    ### below no issues for 52/p1only
    0x39: 'H', 0x5: 'A',
    0x15: 'k', 0x16: 'K',
    0x1C: 'z', 0x1D: 'Z',
    0x1F: 't',  0x21: 'd',  
    0x24: 'T',  0x26: 'D', 
    0x2A: 'p', 0x2B: 'f', 0x2C: 'b', 0x2D: 'B', 0x2E: 'm',
    0x2F: 'y', 0x30: 'r', 0x32: 'l', 0x35: 'w', 0x36: 'S', 0x37: 's', 0x38: 's', 
    0x1E: 'n',
    0x23: 'n',
    0x28: 'n',
    
}

# ENGLISH CHARS: from eNgliSxe38.sfd
ENGLISH_KEEP = [
    ord('c'),
    ord('C'),
    ord('g'), ord('G'),
    ord('j'), ord('J'),
    ord('q'), ord('Q'),
    ord('v'), ord('A'), ord('x'),
    
    ### 0123456789LYVWPF 10=F+1=wnti=8+8=4*4=ten + 6=L+6
    ord('L'),ord('Y'),ord('V'),ord('W'),ord('P'),ord('F'),
    
    ord('E'), ord('I'), ord('O'), ord('U'),ord('M'), ord('X'),
    ord('a'), ord('i'), ord('u'), ord('e'), ord('o'), ord('h'),
]

# अ (schwa): from Noto (respective Indian language)
# x = अ (0x0905 for Hindi, 0x0985 for Bengali, etc.)
SCHWA_OFFSET = 0x05  # अ is at offset 0x05 in all 9 scripts

# R (ड़): from Noto Devanagari (Hindi only)
R_FIX = [
    (ord('R'), 0x095C),  # R = ड़
]


def process_script(script_name):
    if script_name not in SCRIPTS:
        logging.error(f"Unknown script: {script_name}")
        return False

    config = SCRIPTS[script_name]

    noto_font_path = pff_root / "notofonts" / config['noto']
    sfd_path = pff_root / "sfd/x38ifont/x38iasc" / config['sfd']

    # font_repo = Path("C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font")
    # ttf_dir = font_repo / "ttf/hscii/xi38font"
    # woff2_dir = font_repo / "woff2/hscii/xi38font"
    
    # "C:\Users\ravi_\OneDrive\Desktop\Vimal\wimxlprogs\gitt\pff\xnglofonts"
    # C:\Users\ravi_\OneDrive\Desktop\Vimal\wimxlprogs\gitt\pff\xnglofonts\ttf\xi38fonts\xi38asc
    ttf_dir = pff_root / "xnglofonts/ttf/xi38fonts/xi38asc"
    woff2_dir = pff_root / "xnglofonts/woff2/xi38fonts/xi38asc"

    if not noto_font_path.exists():
        logging.error(f"Noto not found: {noto_font_path}")
        return False

    if not sfd_path.exists():
        logging.error(f"SFD not found: {sfd_path}")
        return False

    logging.info(f"\n{'='*60}")
    logging.info(f"Processing: {script_name}")

    try:
        noto_font = fontforge.open(str(noto_font_path))
    except Exception as e:
        logging.error(f"Error opening Noto: {e}")
        return False

    try:
        eng_font = fontforge.open(str(english_sfd))
    except Exception as e:
        logging.error(f"Error opening English: {e}")
        return False

    try:
        target_font = fontforge.open(str(sfd_path))
    except Exception as e:
        logging.error(f"Error opening target: {e}")
        return False

    success = 0
    base = config['base_unicode']

    # STEP 1: Copy consonants from Noto
    for offset, hskii_char in CONSONANT_MAP.items():
        src_unicode = base + offset
        if src_unicode not in noto_font:
            continue
        dst_ascii = ord(hskii_char)
        try:
            noto_font.selection.select(src_unicode)
            noto_font.copy()
            if dst_ascii in target_font:
                target_font.selection.select(dst_ascii)
                glyph = target_font[dst_ascii]
                glyph.clear()
                target_font.paste()
                success += 1
        except Exception as e:
            logging.warning(f"  Error consonant 0x{offset:02X}: {e}")

    # STEP 2: Copy English chars from eNgliSxe38.sfd
    for ascii_code in ENGLISH_KEEP:
        if ascii_code not in eng_font or ascii_code not in target_font:
            continue
        try:
            eng_font.selection.select(ascii_code)
            eng_font.copy()
            target_font.selection.select(ascii_code)
            glyph = target_font[ascii_code]
            glyph.clear()
            target_font.paste()
            success += 1
        except Exception as e:
            logging.warning(f"  Error English {ascii_code}: {e}")

    # STEP 3: Copy अ (schwa) to both 'x' and 'A'
    schwa_unicode = base + SCHWA_OFFSET
    if schwa_unicode in noto_font:
        for ascii_char in ['x', 'A']:
            ascii_code = ord(ascii_char)
            if ascii_code not in target_font:
                continue
            try:
                noto_font.selection.select(schwa_unicode)
                noto_font.copy()
                target_font.selection.select(ascii_code)
                glyph = target_font[ascii_code]
                glyph.clear()
                target_font.paste()
                success += 1
                logging.info(f"  ✓ '{ascii_char}' ← अ (U+{schwa_unicode:04X})")
            except Exception as e:
                logging.warning(f"  Error schwa for {ascii_char}: {e}")

    # STEP 4: Fix R (ड़) from Noto Devanagari (Hindi only)
    if script_name == 'hindi' and noto_devanagari.exists():
        try:
            noto_dev = fontforge.open(str(noto_devanagari))
            for ascii_code, noto_unicode in R_FIX:
                if noto_unicode not in noto_dev or ascii_code not in target_font:
                    continue
                try:
                    noto_dev.selection.select(noto_unicode)
                    noto_dev.copy()
                    target_font.selection.select(ascii_code)
                    glyph = target_font[ascii_code]
                    glyph.clear()
                    target_font.paste()
                    success += 1
                except Exception as e:
                    logging.warning(f"  Error R fix: {e}")
            noto_dev.close()
        except Exception as e:
            logging.warning(f"  Error opening Noto Dev: {e}")

    logging.info(f"  Success: {success}")

    try:
        target_font.save(str(sfd_path))
        base_name = config['output']
        target_font.generate(str(ttf_dir / f"{base_name}.ttf"))
        target_font.generate(str(woff2_dir / f"{base_name}.woff2"))
        logging.info(f"  ✓ Saved and regenerated: {base_name}")
    except Exception as e:
        logging.error(f"  Error saving: {e}")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python glyph_kopi_u9scripts.py <script_name|all>")
        sys.exit(1)

    script_name = sys.argv[1].lower()

    logging.info(f"Started: {datetime.now()}")

    if script_name == 'all':
        for name in SCRIPTS.keys():
            process_script(name)
    else:
        process_script(script_name)

    logging.info(f"Finished: {datetime.now()}")
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()