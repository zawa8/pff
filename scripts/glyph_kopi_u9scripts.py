#!/usr/bin/env python3
"""
Script to copy glyphs from Noto font to xi38asc SFD for 9 Indian scripts.
Usage: python glyph_kopi_u9scripts.py <script_name>
"""

import sys
import fontforge
from pathlib import Path

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

# 9-scripts offset mapping (same for all 9)
# {offset: hskii_char}
OFFSET_MAP = {
    # Vowels
    0x05: 'x',   # अ (schwa)
    0x06: 'a',   # आ (aa)
    0x07: 'i',   # इ (i)
    0x08: 'i',   # ई (ii)
    0x09: 'u',   # उ (u)
    0x0A: 'u',   # ऊ (uu)
    0x0B: 'r',   # ऋ (vocalic r)
    0x0C: 'l',   # ऌ (vocalic l)
    0x0F: 'e',   # ए (e)
    0x10: 'e',   # ऐ (ai)
    0x13: 'o',   # ओ (o)
    0x14: 'o',   # औ (au)

    # Consonants
    0x15: 'k',   # क
    0x16: 'K',   # ख
    0x17: 'g',   # ग
    0x18: 'G',   # घ
    0x19: 'N',   # ङ
    0x1A: 'c',   # च
    0x1B: 'C',   # छ
    0x1C: 'z',   # ज
    0x1D: 'Z',   # झ
    0x1E: 'n',   # ञ
    0x1F: 't',   # ट
    0x20: 'J',   # ठ
    0x21: 'd',   # ड
    0x22: 'Q',   # ढ
    0x23: 'n',   # ण
    0x24: 'T',   # त
    0x25: 'j',   # थ
    0x26: 'D',   # द
    0x27: 'q',   # ध
    0x28: 'n',   # न
    0x2A: 'p',   # प
    0x2B: 'f',   # फ
    0x2C: 'b',   # ब
    0x2D: 'B',   # भ
    0x2E: 'm',   # म
    0x2F: 'y',   # य
    0x30: 'r',   # र
    0x32: 'l',   # ल
    0x33: 'l',   # ळ
    0x35: 'w',   # व
    0x36: 'S',   # श
    0x37: 's',   # ष
    0x38: 's',   # स
    0x39: 'H',   # ह

    # Matras
    0x3E: 'a',   # ा
    0x3F: 'i',   # ि
    0x40: 'i',   # ी
    0x41: 'u',   # ु
    0x42: 'u',   # ू
    0x43: 'r',   # ृ
    0x44: 'r',   # ॄ
    0x47: 'e',   # े
    0x48: 'e',   # ै
    0x49: 'o',   # ॉ
    0x4B: 'o',   # ो
    0x4C: 'o',   # ौ
    0x4D: '',    # ् (virama)
}


def process_script(script_name):
    if script_name not in SCRIPTS:
        print(f"✗ Unknown script: {script_name}")
        print(f"Available: {list(SCRIPTS.keys())}")
        return False

    config = SCRIPTS[script_name]

    # Paths
    script_dir = Path(__file__).parent
    pff_root = script_dir.parent
    noto_font_path = pff_root / "notofonts" / config['noto']
    sfd_path = pff_root / "sfd/x38ifont/x38iasc" / config['sfd']

    font_repo = Path("C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font")
    ttf_dir = font_repo / "ttf/hscii/xi38font"
    woff2_dir = font_repo / "woff2/hscii/xi38font"

    if not noto_font_path.exists():
        print(f"✗ Noto not found: {noto_font_path}")
        return False

    if not sfd_path.exists():
        print(f"✗ SFD not found: {sfd_path}")
        return False

    print(f"\n{'='*60}")
    print(f"Processing: {script_name}")
    print(f"  Noto: {noto_font_path.name}")
    print(f"  SFD: {sfd_path.name}")

    noto_font = fontforge.open(str(noto_font_path))
    target_font = fontforge.open(str(sfd_path))

    success = errors = 0
    base = config['base_unicode']

    for offset, hskii_char in OFFSET_MAP.items():
        src_unicode = base + offset

        if src_unicode not in noto_font:
            continue

        if not hskii_char:
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
                print(f"  ✓ {hskii_char} (ASCII {dst_ascii}) ← U+{src_unicode:04X}")
                success += 1
        except Exception as e:
            print(f"  ✗ Error 0x{offset:02X}: {e}")
            errors += 1

    print(f"  Success: {success}, Errors: {errors}")

    if success > 0:
        target_font.save(str(sfd_path))
        print(f"  ✓ Saved SFD")

        ttf_path = ttf_dir / f"{config['output']}.ttf"
        target_font.generate(str(ttf_path))
        print(f"  ✓ TTF: {ttf_path.name}")

        woff2_path = woff2_dir / f"{config['output']}.woff2"
        target_font.generate(str(woff2_path))
        print(f"  ✓ WOFF2: {woff2_path.name}")

    noto_font.close()
    target_font.close()
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python glyph_kopi_u9scripts.py <script_name>")
        print(f"Scripts: {list(SCRIPTS.keys())}")
        print("Or: python glyph_kopi_u9scripts.py all")
        sys.exit(1)

    script_name = sys.argv[1].lower()

    if script_name == 'all':
        for name in SCRIPTS.keys():
            process_script(name)
    else:
        process_script(script_name)

    print("\nDone!")


if __name__ == "__main__":
    main()