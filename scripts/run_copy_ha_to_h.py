#!/usr/bin/env python3
"""
Execute the single glyph copy operation: ह → H
Copy Devanagari Letter Ha from Noto Sans Devanagari to 'H' position in hindixv38
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from font_modifier import FontModifier, FontValidator
import fontforge
import urllib.request

def download_noto_font():
    """Download Noto Sans Devanagari"""
    fonts_temp_dir = scripts_dir.parent / "fonts_temp"
    fonts_temp_dir.mkdir(exist_ok=True)
    
    noto_path = fonts_temp_dir / "NotoSansDevanagari-Regular.ttf"
    
    if not noto_path.exists():
        print("📥 Downloading Noto Sans Devanagari...")
        url = "https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari-Regular.ttf"
        try:
            urllib.request.urlretrieve(url, str(noto_path))
            print(f"✓ Downloaded: {noto_path}\n")
        except Exception as e:
            print(f"✗ Download failed: {e}")
            return None
    else:
        print(f"✓ Using cached Noto font\n")
    
    return noto_path

def main():
    print("="*70)
    print("GLYPH COPY OPERATION: ह (U+0939) → H (U+0048)")
    print("Devanagari Letter Ha")
    print("="*70 + "\n")
    
    # Paths
    sfd_path = scripts_dir.parent / "sfd/x38ifont/x38iasc/hindixv38.sfd"
    
    # Check SFD exists
    if not sfd_path.exists():
        print(f"✗ SFD file not found: {sfd_path}")
        sys.exit(1)
    
    # Download Noto font
    noto_path = download_noto_font()
    if not noto_path:
        sys.exit(1)
    
    # Step 1: Open Noto and copy ह
    print("Step 1: Copying ह from Noto Sans Devanagari...")
    print("-" * 70)
    try:
        noto = fontforge.open(str(noto_path))
        
        devanagari_ha = 0x0939  # ह (Devanagari Letter Ha)
        if devanagari_ha not in noto:
            print(f"✗ Glyph ह (U+{devanagari_ha:04X}) not found")
            noto.close()
            sys.exit(1)
        
        glyph_name = noto[devanagari_ha].glyphname
        print(f"✓ Found glyph: {glyph_name}")
        
        noto.selection.select(devanagari_ha)
        noto.editSelectAll()
        noto.copy()
        print(f"✓ Copied ह glyph\n")
        noto.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    # Step 2: Open hindixv38 and paste to H
    print("Step 2: Pasting into hindixv38 at 'H' position...")
    print("-" * 70)
    try:
        hindixv38 = fontforge.open(str(sfd_path))
        
        h_unicode = 0x0048  # H
        if h_unicode not in hindixv38:
            print(f"✗ Glyph H (U+{h_unicode:04X}) not found")
            hindixv38.close()
            sys.exit(1)
        
        glyph = hindixv38[h_unicode]
        print(f"✓ Found glyph: {glyph.glyphname}")
        
        # Clear and paste
        glyph.clear()
        print(f"✓ Cleared glyph")
        
        hindixv38.selection.select(h_unicode)
        hindixv38.paste()
        print(f"✓ Pasted ह into H\n")
        
        # Save SFD
        hindixv38.save(str(sfd_path))
        print(f"✓ Saved: {sfd_path}\n")
        
        hindixv38.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    # Step 3: Generate TTF
    print("Step 3: Generating TTF file...")
    print("-" * 70)
    try:
        hindixv38 = fontforge.open(str(sfd_path))
        ttf_path = sfd_path.with_suffix('.ttf')
        hindixv38.generate(str(ttf_path))
        print(f"✓ Generated: {ttf_path}\n")
        hindixv38.close()
    except Exception as e:
        print(f"✗ Error generating TTF: {e}")
        sys.exit(1)
    
    # Summary
    print("="*70)
    print("✓ SUCCESS!")
    print("="*70)
    print(f"Modified SFD: {sfd_path}")
    print(f"Generated TTF: {sfd_path.with_suffix('.ttf')}")
    print("\nThe character 'H' now displays as ह from Noto Sans Devanagari")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
