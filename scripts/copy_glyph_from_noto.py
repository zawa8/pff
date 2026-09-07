#!/usr/bin/env python3
"""
Script to copy ॲ (Devanagari Letter Aw) glyph from Noto Sans Devanagari
and paste it into hindixv38.sfd at code 'A' (Unicode 0x41)
"""

import fontforge
import urllib.request
import os
from pathlib import Path

# Create scripts directory if it doesn't exist
script_dir = Path(__file__).parent
fonts_dir = script_dir.parent / "fonts_temp"
fonts_dir.mkdir(exist_ok=True)

# Download Noto Sans Devanagari if not already present
noto_font_path = fonts_dir / "NotoSansDevanagari-Regular.ttf"

if not noto_font_path.exists():
    print("Downloading Noto Sans Devanagari...")
    url = "https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari-Regular.ttf"
    try:
        urllib.request.urlretrieve(url, str(noto_font_path))
        print(f"✓ Downloaded to {noto_font_path}")
    except Exception as e:
        print(f"✗ Error downloading font: {e}")
        print("Please manually download from: https://github.com/notofonts/devanagari/releases")
        exit(1)
else:
    print(f"✓ Using existing font: {noto_font_path}")

# Open the Noto Sans Devanagari font
print("\nOpening Noto Sans Devanagari...")
noto_font = fontforge.open(str(noto_font_path))

# Unicode for ॲ (Devanagari Letter Aw)
devanagari_aw_unicode = 0x0972

# Check if the glyph exists
if devanagari_aw_unicode in noto_font:
    glyph_name = noto_font[devanagari_aw_unicode].glyphname
    print(f"✓ Found ॲ (U+{devanagari_aw_unicode:04X}) as '{glyph_name}'")
else:
    print(f"✗ Glyph ॲ (U+{devanagari_aw_unicode:04X}) not found in Noto Sans Devanagari")
    noto_font.close()
    exit(1)

# Select and copy the glyph
noto_font.selection.select(devanagari_aw_unicode)
noto_font.editSelectAll()  # Select all points in the glyph
noto_font.copy()
print(f"✓ Copied ॲ glyph")

noto_font.close()

# Open hindixv38.sfd
sfd_path = script_dir.parent / "sfd/x38ifont/x38iasc/hindixv38.sfd"
print(f"\nOpening {sfd_path}...")

if not sfd_path.exists():
    print(f"✗ File not found: {sfd_path}")
    exit(1)

hindixv38 = fontforge.open(str(sfd_path))
print("✓ Opened hindixv38.sfd")

# Unicode for 'A' (Latin Capital Letter A)
a_unicode = 0x41

# Select the 'A' glyph
if a_unicode in hindixv38:
    hindixv38.selection.select(a_unicode)
    glyph = hindixv38[a_unicode]
    print(f"✓ Selected glyph 'A' (U+{a_unicode:04X})")
    
    # Clear the existing glyph
    glyph.clear()
    print("✓ Cleared existing 'A' glyph")
    
    # Paste the ॲ glyph
    hindixv38.paste()
    print("✓ Pasted ॲ glyph into 'A' position")
    
    # Save the modified SFD
    hindixv38.save(str(sfd_path))
    print(f"✓ Saved modified SFD: {sfd_path}")
    
    # Generate TTF
    ttf_path = sfd_path.parent / "hindixv38.ttf"
    hindixv38.generate(str(ttf_path))
    print(f"✓ Generated TTF: {ttf_path}")
    
    print("\n✓ SUCCESS! Glyph ॲ has been copied to 'A' position")
    print(f"  - Modified SFD: {sfd_path}")
    print(f"  - Generated TTF: {ttf_path}")
else:
    print(f"✗ Glyph 'A' (U+{a_unicode:04X}) not found in hindixv38.sfd")
    hindixv38.close()
    exit(1)

hindixv38.close()
print("\nDone!")
