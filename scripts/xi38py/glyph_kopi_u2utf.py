#!/usr/bin/env python3
"""
Script to create xi38utf fonts by:
1. Copying 128 glyphs from xi38asc
2. Adding 10 Unicode ranges with references to ASCII base glyphs

Reference mapping based on htrlib unicode_hindi_array.
"""

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
log_file = log_dir / "glyph_kopi_u2utf.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Source (asc)
asc_dir = pff_root / "sfd/x38ifont/x38iasc"
# Target (utf)
utf_dir = pff_root / "sfd/x38ifont/x38iutf"
utf_dir.mkdir(parents=True, exist_ok=True)

# Output (font repo)
font_repo = Path("C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font")
ttf_dir = font_repo / "ttf/hscii/xi38utf"
woff2_dir = font_repo / "woff2/hscii/xi38utf"
ttf_dir.mkdir(parents=True, exist_ok=True)
woff2_dir.mkdir(parents=True, exist_ok=True)

FONTS = {
    'hindixh38asc.sfd': 'hindixh38utf.sfd',
    'bengalixb38asc.sfd': 'bengalixb38utf.sfd',
    'pnzabixp38asc.sfd': 'pnzabixp38utf.sfd',
    'guzrajixg38asc.sfd': 'guzrajixg38utf.sfd',
    'oriyaxo38asc.sfd': 'oriyaxo38utf.sfd',
    'tmilxt38asc.sfd': 'tmilxt38utf.sfd',
    'jeluguxj38asc.sfd': 'jeluguxj38utf.sfd',
    'knRaxk38asc.sfd': 'knRaxk38utf.sfd',
    'mlyalxmxm38asc.sfd': 'mlyalxmxm38utf.sfd',
    'sinhlaxs38asc.sfd': 'sinhlaxs38utf.sfd',
}

# 10 Unicode ranges
UNICODE_RANGES = [
    0x0900, 0x0980, 0x0A00, 0x0A80, 0x0B00,
    0x0B80, 0x0C00, 0x0C80, 0x0D00, 0x0D80,
]

# htrlib unicode_hindi_array mapping
# Each offset (0x00-0x7F) maps to hskii chars
# We need to find the ASCII position for each hskii char
UNICODE_HINDI_ARRAY = [
    '',     # 0x00
    'N',    # 0x01
    'N',    # 0x02
    ':',    # 0x03
    'xe',   # 0x04
    'x',    # 0x05 (अ) → x (0x78)
    'a',    # 0x06 (आ) → a (0x61)
    'i',    # 0x07 (इ) → i (0x69)
    'i',    # 0x08 (ई) → i (0x69)
    'u',    # 0x09 (उ) → u (0x75)
    'u',    # 0x0A (ऊ) → u (0x75)
    'r',    # 0x0B (ऋ) → r (0x72)
    'l',    # 0x0C (ऌ) → l (0x6C)
    'e',    # 0x0D (ऍ) → e (0x65)
    'e',    # 0x0E (ऎ) → e (0x65)
    'e',    # 0x0F (ए) → e (0x65)
    'e',    # 0x10 (ऐ) → e (0x65)
    'o',    # 0x11 (ऑ) → o (0x6F)
    'o',    # 0x12 (ऒ) → o (0x6F)
    'o',    # 0x13 (ओ) → o (0x6F)
    'o',    # 0x14 (औ) → o (0x6F)
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


def build_char_to_ascii_map():
    """Build a map from hskii char to ASCII position."""
    char_to_ascii = {}
    for offset, hskii_chars in enumerate(UNICODE_HINDI_ARRAY):
        if not hskii_chars:
            continue
        # Take the first character
        first_char = hskii_chars[0]
        if first_char not in char_to_ascii:
            char_to_ascii[first_char] = offset
    return char_to_ascii


def create_utf_font(asc_name, utf_name):
    """Step 1: Copy asc → utf."""
    asc_path = asc_dir / asc_name
    utf_path = utf_dir / utf_name

    if not asc_path.exists():
        logging.error(f"Not found: {asc_path}")
        return None

    logging.info(f"Processing: {asc_name} → {utf_name}")

    try:
        asc_font = fontforge.open(str(asc_path))
        asc_font.save(str(utf_path))
        asc_font.close()
        logging.info(f"Copied to {utf_path.name}")
        return utf_path
    except Exception as e:
        logging.error(f"Error copying: {e}")
        return None


def add_unicode_ranges(utf_path):
    """Step 2: Add Unicode ranges with references."""
    logging.info(f"Adding Unicode ranges to {utf_path.name}")

    try:
        utf_font = fontforge.open(str(utf_path))
    except Exception as e:
        logging.error(f"Error opening: {e}")
        return 0

    total_refs = 0

    for base_unicode in UNICODE_RANGES:
        range_count = 0

        for offset in range(128):
            dst_unicode = base_unicode + offset

            hskii_chars = UNICODE_HINDI_ARRAY[offset] if offset < len(UNICODE_HINDI_ARRAY) else ''
            if not hskii_chars:
                continue

            hskii_char = hskii_chars[0]
            src_ascii = ord(hskii_char)

            try:
                src_glyph = utf_font[src_ascii]
                if src_glyph is None:
                    continue
                src_name = src_glyph.glyphname
                if not src_name:
                    continue
            except Exception:
                continue

            try:
                # Create destination if not exists
                if dst_unicode not in utf_font:
                    utf_font.createChar(dst_unicode)

                dst_glyph = utf_font[dst_unicode]
                dst_glyph.clear()
                # Use addReference instead of references
                dst_glyph.addReference(src_name, (0, 0, 0, 0, 0, 0))

                range_count += 1
                total_refs += 1

            except Exception as e:
                logging.warning(
                    f"Error ref 0x{offset:02X} → U+{dst_unicode:04X}: {e}"
                )

        logging.info(f"  U+{base_unicode:04X}: {range_count} refs")

    try:
        utf_font.save(str(utf_path))
        logging.info(f"  Saved: {utf_path.name}")

        base_name = utf_path.stem
        ttf_path = ttf_dir / f"{base_name}.ttf"
        utf_font.generate(str(ttf_path))

        woff2_path = woff2_dir / f"{base_name}.woff2"
        utf_font.generate(str(woff2_path))

        logging.info(f"  TTF: {ttf_path.name}, WOFF2: {woff2_path.name}")
    except Exception as e:
        logging.error(f"Error saving: {e}")

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
    print(f"\n✓ Done! Logs: {log_file}")


if __name__ == "__main__":
    main()