#!/usr/bin/env python3
"""
build_utf_fonts.py

Build xi38utf fonts from xi38asc:

1. Copy xi38asc -> xi38utf (128 glyphs).
2. For each of 9 Unicode ranges (Hindi .. Malayalam), reference-copy
   base glyphs at the same offset (UNICODE_HINDI_ARRAY mapping).
3. For Sinhala (U+0D80..U+0DFF), reference-copy using a different
   mapping (SINHALA_OFFSET_MAP).

Result: a single utf file carries the script's own glyphs in *all*
Indic Unicode ranges, so a reader of that script can read any Indic
Unicode text in a script they know.

See scripts/utf_design.md for the full philosophy.

TTF/WOFF2 generation is separate (scripts/xi52py/generatefonts/gen_xi38utf.py).

Run via main.py:
    fontforge -script scripts/xi52py/main.py --phase utf
"""

import fontforge
import logging
from datetime import datetime
from pathlib import Path

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent.parent

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "glyph_kopi_u2utf.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger("").addHandler(console)

# Source (asc)
asc_dir = pff_root / "sfd/xi38sfd/xi38asc"
# Target (utf)
utf_dir = pff_root / "sfd/xi38sfd/xi38utf"
utf_dir.mkdir(parents=True, exist_ok=True)

FONTS = {
    "xh38asc.sfd": "xh38utf.sfd",
    "xb38asc.sfd": "xb38utf.sfd",
    "xp38asc.sfd": "xp38utf.sfd",
    "xg38asc.sfd": "xg38utf.sfd",
    "xo38asc.sfd": "xo38utf.sfd",
    "xt38asc.sfd": "xt38utf.sfd",
    "xj38asc.sfd": "xj38utf.sfd",
    "xk38asc.sfd": "xk38utf.sfd",
    "xm38asc.sfd": "xm38utf.sfd",
    "xs38asc.sfd": "xs38utf.sfd",
}

# 9 Unicode ranges share the same Hindi-based offset mapping.
# Sinhala (0x0D80) uses SINHALA_OFFSET_MAP instead.
RANGES_9 = [
    0x0900,  # Hindi
    0x0980,  # Bengali
    0x0A00,  # Punjabi
    0x0A80,  # Gujarati
    0x0B00,  # Oriya
    0x0B80,  # Tamil
    0x0C00,  # Telugu
    0x0C80,  # Kannada
    0x0D00,  # Malayalam
]

# htrlib unicode_hindi_array: offset (0x00-0x7F) -> hskii char
UNICODE_HINDI_ARRAY = [
    '',     # 0x00
    'N',    # 0x01
    'N',    # 0x02
    ':',    # 0x03
    'xe',   # 0x04
    'x',    # 0x05 (अ)
    'a',    # 0x06 (आ)
    'i',    # 0x07 (इ)
    'i',    # 0x08 (ई)
    'u',    # 0x09 (उ)
    'u',    # 0x0A (ऊ)
    'r',    # 0x0B (ऋ)
    'l',    # 0x0C (ऌ)
    'e',    # 0x0D (ऍ)
    'e',    # 0x0E (ऎ)
    'e',    # 0x0F (ए)
    'e',    # 0x10 (ऐ)
    'o',    # 0x11 (ऑ)
    'o',    # 0x12 (ऒ)
    'o',    # 0x13 (ओ)
    'o',    # 0x14 (औ)
    'k',    # 0x15
    'K',    # 0x16
    'g',    # 0x17
    'G',    # 0x18
    'N',    # 0x19
    'c',    # 0x1A
    'C',    # 0x1B
    'z',    # 0x1C
    'Z',    # 0x1D
    'n',    # 0x1E
    't',    # 0x1F
    'J',    # 0x20
    'd',    # 0x21
    'Q',    # 0x22
    'n',    # 0x23
    'T',    # 0x24
    'j',    # 0x25
    'D',    # 0x26
    'q',    # 0x27
    'n',    # 0x28
    'n',    # 0x29
    'p',    # 0x2A
    'f',    # 0x2B
    'b',    # 0x2C
    'B',    # 0x2D
    'm',    # 0x2E
    'y',    # 0x2F
    'r',    # 0x30
    'r',    # 0x31
    'l',    # 0x32
    'l',    # 0x33
    'l',    # 0x34
    'w',    # 0x35
    'S',    # 0x36
    's',    # 0x37
    's',    # 0x38
    'H',    # 0x39
    'oe',   # 0x3A
    'ui',   # 0x3B
    '',     # 0x3C
    '!',    # 0x3D
    'a',    # 0x3E (ा)
    'i',    # 0x3F (ि)
    'i',    # 0x40 (ी)
    'u',    # 0x41 (ु)
    'u',    # 0x42 (ू)
    'r',    # 0x43 (ृ)
    'r',    # 0x44 (ॄ)
    'e',    # 0x45
    'e',    # 0x46
    'e',    # 0x47 (े)
    'e',    # 0x48 (ै)
    'o',    # 0x49 (ॉ)
    'o',    # 0x4A
    'o',    # 0x4B (ो)
    'o',    # 0x4C (ौ)
    '',     # 0x4D (्)
    '',     # 0x4E
    'o',    # 0x4F
    'om',   # 0x50
    '',     # 0x51
    '',     # 0x52
    '`',    # 0x53
    "'",    # 0x54
    'eei',  # 0x55
    'ui',   # 0x56
    'uui',  # 0x57
    'k',    # 0x58
    'K',    # 0x59
    'g',    # 0x5A
    'z',    # 0x5B
    'R',    # 0x5C
    'R',    # 0x5D
    'f',    # 0x5E
    'y',    # 0x5F
    'r',    # 0x60
    'l',    # 0x61
    'l',    # 0x62
    'l',    # 0x63
    '.',    # 0x64
    '.',    # 0x65
    '0',    # 0x66
    '1',    # 0x67
    '2',    # 0x68
    '3',    # 0x69
    '4',    # 0x6A
    '5',    # 0x6B
    '6',    # 0x6C
    '7',    # 0x6D
    '8',    # 0x6E
    '9',    # 0x6F
    '_',    # 0x70
    '__',   # 0x71
    'A',    # 0x72
    'o',    # 0x73
    'o',    # 0x74
    'o',    # 0x75
    'u',    # 0x76
    'u',    # 0x77
    'q',    # 0x78
    'Z',    # 0x79
    'y',    # 0x7A
    'n',    # 0x7B
    'z',    # 0x7C
    '?',    # 0x7D
    'd',    # 0x7E
    'b',    # 0x7F
]

# Sinhala range uses its own mapping (sparse).
SINHALA_BASE = 0x0D80
SINHALA_OFFSET_MAP = {
    0x1A: 'k',  # ක 0D9A
    0x1B: 'K',  # ඛ 0D9B
    0x1C: 'g',  # ග 0D9C
    0x1D: 'G',  # ඝ 0D9D
    0x20: 'c',  # ච 0DA0
    0x21: 'C',  # ඡ 0DA1
    0x22: 'z',  # ජ 0DA2
    0x23: 'Z',  # ඣ 0DA3
    0x27: 't',  # ට 0DA7
    0x28: 'T',  # ඨ 0DA8
    0x29: 'd',  # ඩ 0DA9
    0x2A: 'D',  # ද 0DAF
    0x2D: 'j',  # ත 0DAD
    0x2E: 'J',  # ථ 0DAE
    0x2F: 'q',  # ද 0DAF
    0x30: 'Q',  # ධ 0DB0
    0x31: 'n',  # න 0DB1
    0x34: 'p',  # ප 0DB4
    0x35: 'f',  # ෆ 0DC6
    0x36: 'b',  # බ 0DB6
    0x37: 'B',  # භ 0DB7
    0x38: 'm',  # ම 0DB8
    0x3A: 'y',  # ය 0DBA
    0x3B: 'r',  # ර 0DBB
    0x3D: 'l',  # ල 0DBD
    0x40: 'w',  # ව 0DC0
    0x41: 'S',  # ශ 0DC1
    0x42: 's',  # ස 0DC3
    0x43: 's',  # ස 0DC3
    0x44: 'H',  # හ 0DC4
    0x45: 'l',  # ළ 0DC5
    0x46: 'f',  # ෆ 0DC6
}


def create_utf_font(asc_name, utf_name):
    """Step 1: Copy asc -> utf."""
    asc_path = asc_dir / asc_name
    utf_path = utf_dir / utf_name

    if not asc_path.exists():
        logging.error(f"Not found: {asc_path}")
        return None

    logging.info(f"Processing: {asc_name} -> {utf_name}")
    try:
        asc_font = fontforge.open(str(asc_path))
        asc_font.save(str(utf_path))
        asc_font.close()
        logging.info(f"Copied to {utf_path.name}")
        return utf_path
    except Exception as e:
        logging.error(f"Error copying: {e}")
        return None


def _add_ref(utf_font, dst_unicode, src_ascii):
    """Add a reference at dst_unicode pointing to base glyph at src_ascii.

    Returns True on success, False on skip/error.
    """
    try:
        src_glyph = utf_font[src_ascii]
        if src_glyph is None:
            return False
        src_name = src_glyph.glyphname
        if not src_name:
            return False
    except Exception:
        return False

    try:
        if dst_unicode not in utf_font:
            utf_font.createChar(dst_unicode)
        dst_glyph = utf_font[dst_unicode]
        dst_glyph.clear()
        dst_glyph.addReference(src_name, (0, 0, 0, 0, 0, 0))
        return True
    except Exception as e:
        logging.warning(f"Error ref U+{dst_unicode:04X}: {e}")
        return False


def add_unicode_ranges(utf_path):
    """Step 2: Add Unicode ranges with references."""
    logging.info(f"Adding Unicode ranges to {utf_path.name}")

    try:
        utf_font = fontforge.open(str(utf_path))
    except Exception as e:
        logging.error(f"Error opening: {e}")
        return 0

    total_refs = 0

    # 9 ranges: same Hindi-based mapping
    for base_unicode in RANGES_9:
        range_count = 0
        for offset in range(128):
            hskii_chars = UNICODE_HINDI_ARRAY[offset] if offset < len(UNICODE_HINDI_ARRAY) else ""
            if not hskii_chars:
                continue
            src_ascii = ord(hskii_chars[0])
            if _add_ref(utf_font, base_unicode + offset, src_ascii):
                range_count += 1
                total_refs += 1
        logging.info(f"  U+{base_unicode:04X}: {range_count} refs")

    # Sinhala range: sparse mapping
    sinhala_count = 0
    for offset, hskii_char in SINHALA_OFFSET_MAP.items():
        if not hskii_char:
            continue
        src_ascii = ord(hskii_char)
        if _add_ref(utf_font, SINHALA_BASE + offset, src_ascii):
            sinhala_count += 1
            total_refs += 1
    logging.info(f"  U+{SINHALA_BASE:04X} (Sinhala): {sinhala_count} refs")

    try:
        utf_font.save(str(utf_path))
        logging.info(f"  Saved: {utf_path.name}")
    except Exception as e:
        logging.error(f"Error saving: {e}")

    utf_font.close()
    return total_refs


def main():
    logging.info("=" * 60)
    logging.info(f"Started: {datetime.now()}")

    for asc_name, utf_name in FONTS.items():
        utf_path = create_utf_font(asc_name, utf_name)
        if utf_path:
            add_unicode_ranges(utf_path)

    logging.info("=" * 60)
    logging.info(f"Finished: {datetime.now()}")
    print(f"\nDone! Logs: {log_file}")


if __name__ == "__main__":
    main()
