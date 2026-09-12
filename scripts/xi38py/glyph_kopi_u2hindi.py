#!/usr/bin/env python3
"""
Script to copy Devanagari glyphs from Noto Sans Devanagari
and paste them into hindixv38.sfd at hskii positions.
Generates .ttf and .woff2 in font repo.
"""

import fontforge
from pathlib import Path

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent

# Source
noto_fonts_dir = pff_root / "notofonts"
noto_font_path = noto_fonts_dir / "NotoSansDevanagari-Regular.ttf"

# SFD (edit)
sfd_path = pff_root / "sfd/x38ifont/x38iasc/hindixv38.sfd"

# Output (font repo)
font_repo = Path("C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font")
ttf_output_dir = font_repo / "ttf/hscii/xi38font"
woff2_output_dir = font_repo / "woff2/hscii/xi38font"

# Create output dirs if not exist
ttf_output_dir.mkdir(parents=True, exist_ok=True)
woff2_output_dir.mkdir(parents=True, exist_ok=True)

# Check if Noto font exists
if not noto_font_path.exists():
    print(f"✗ Font not found: {noto_font_path}")
    print("Please download NotoSansDevanagari-Regular.ttf to notofonts folder")
    exit(1)

# hskii mapping: {hskii_char: devanagari_unicode}
hskii_mapping = {
    # Vowels
    'x': 0x0905,  # अ (schwa)
    'A': 0x0972,  # ॲ (candra a)

    # Velar consonants
    'k': 0x0915,  # क
    'K': 0x0916,  # ख
    'g': 0x0917,  # ग
    'G': 0x0918,  # घ

    # Palatal consonants
    'c': 0x091A,  # च
    'C': 0x091B,  # छ
    'z': 0x091C,  # ज
    'Z': 0x091D,  # झ

    # Retroflex consonants
    't': 0x091F,  # ट
    'J': 0x0920,  # ठ
    'd': 0x0921,  # ड
    'Q': 0x0922,  # ढ

    # Dental consonants
    'T': 0x0924,  # त
    'j': 0x0925,  # थ
    'D': 0x0926,  # द
    'q': 0x0927,  # ध

    # Nasal
    'n': 0x0928,  # न
    'N': 0x0928,  # न

    # Labial consonants
    'p': 0x092A,  # प
    'f': 0x092B,  # फ
    'b': 0x092C,  # ब
    'B': 0x092D,  # भ
    'm': 0x092E,  # म

    # Semivowels
    'y': 0x092F,  # य
    'r': 0x0930,  # र
    'R': 0x095C,  # ड़
    'l': 0x0932,  # ल
    'w': 0x0935,  # व

    # Sibilants
    's': 0x0938,  # स
    'S': 0x0936,  # श

    # Glottal
    'H': 0x0939,  # ह
    'v': 0x0939,  # ह
}

# Open Noto font
print("Opening Noto Sans Devanagari...")
noto_font = fontforge.open(str(noto_font_path))

# Open hindixv38.sfd
print(f"Opening {sfd_path}...")
if not sfd_path.exists():
    print(f"✗ File not found: {sfd_path}")
    noto_font.close()
    exit(1)

hindixv38 = fontforge.open(str(sfd_path))

success_count = 0
error_count = 0

for hskii_char, dev_unicode in hskii_mapping.items():
    try:
        if dev_unicode not in noto_font:
            print(f"✗ U+{dev_unicode:04X} not found in Noto")
            error_count += 1
            continue

        # Copy from Noto
        noto_font.selection.select(dev_unicode)
        noto_font.copy()

        ascii_code = ord(hskii_char)

        if ascii_code in hindixv38:
            hindixv38.selection.select(ascii_code)
            glyph = hindixv38[ascii_code]
            glyph.clear()
            hindixv38.paste()

            print(f"✓ {hskii_char} (ASCII {ascii_code}) ← U+{dev_unicode:04X}")
            success_count += 1
        else:
            print(f"✗ ASCII {ascii_code} not found")
            error_count += 1

    except Exception as e:
        print(f"✗ Error for {hskii_char}: {e}")
        error_count += 1

print(f"\nSuccess: {success_count}, Errors: {error_count}")

if success_count > 0:
    # Save SFD
    hindixv38.save(str(sfd_path))
    print(f"✓ Saved SFD: {sfd_path}")

    # Generate TTF in font repo
    ttf_path = ttf_output_dir / "hindixv38.ttf"
    hindixv38.generate(str(ttf_path))
    print(f"✓ Generated TTF: {ttf_path}")

    # Generate WOFF2 in font repo
    woff2_path = woff2_output_dir / "hindixv38.woff2"
    hindixv38.generate(str(woff2_path))
    print(f"✓ Generated WOFF2: {woff2_path}")

noto_font.close()
hindixv38.close()
print("\nDone!")