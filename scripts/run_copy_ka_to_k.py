#!/usr/bin/env python3
"""
Execute the single glyph copy operation: क → k
Copy Devanagari Letter Ka from Noto Sans Devanagari to 'k' position in hindixh38
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
    print("GLYPH COPY OPERATION: क (U+0915) → k (U+006B)")
    print("Devanagari Letter Ka")
    print("="*70 + "\n")
    
    # Paths
    sfd_path = scripts_dir.parent / "sfd/x38ifont/x38iasc/hindixh38asc.sfd"
    
    # Check SFD exists
    if not sfd_path.exists():
        print(f"✗ SFD file not found: {sfd_path}")
        sys.exit(1)
    
    # Download Noto font
    noto_path = download_noto_font()
    if not noto_path:
        sys.exit(1)
    
    # Step 1: Open Noto and copy क
    print("Step 1: Copying क from Noto Sans Devanagari...")
    print("-" * 70)
    try:
        noto = fontforge.open(str(noto_path))
        
        devanagari_ka = 0x0915  # क (Devanagari Letter Ka)
        if devanagari_ka not in noto:
            print(f"✗ Glyph क (U+{devanagari_ka:04X}) not found")
            noto.close()
            sys.exit(1)
        
        glyph_name = noto[devanagari_ka].glyphname
        print(f"✓ Found glyph: {glyph_name}")
        
        noto.selection.select(devanagari_ka)
        noto.editSelectAll()
        noto.copy()
        print(f"✓ Copied क glyph\n")
        noto.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    # Step 2: Open hindixh38 and paste to k
    print("Step 2: Pasting into hindixh38 at 'k' position...")
    print("-" * 70)
    try:
        hindixh38 = fontforge.open(str(sfd_path))
        
        k_unicode = 0x006B  # k (Latin Small Letter K)
        if k_unicode not in hindixh38:
            print(f"✗ Glyph k (U+{k_unicode:04X}) not found")
            hindixh38.close()
            sys.exit(1)
        
        glyph = hindixh38[k_unicode]
        print(f"✓ Found glyph: {glyph.glyphname}")
        
        # Clear and paste
        glyph.clear()
        print(f"✓ Cleared glyph")
        
        hindixh38.selection.select(k_unicode)
        hindixh38.paste()
        print(f"✓ Pasted क into k\n")
        
        # Save SFD
        hindixh38.save(str(sfd_path))
        print(f"✓ Saved: {sfd_path}\n")
        
        hindixh38.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    
    # Step 3: Generate TTF
    print("Step 3: Generating TTF file...")
    print("-" * 70)
    try:
        hindixh38 = fontforge.open(str(sfd_path))
        ttf_path = sfd_path.with_suffix('.ttf')
        hindixh38.generate(str(ttf_path))
        print(f"✓ Generated: {ttf_path}\n")
        hindixh38.close()
    except Exception as e:
        print(f"✗ Error generating TTF: {e}")
        sys.exit(1)
    
    # Summary
    print("="*70)
    print("✓ SUCCESS!")
    print("="*70)
    print(f"Modified SFD: {sfd_path}")
    print(f"Generated TTF: {sfd_path.with_suffix('.ttf')}")
    print("\nThe character 'k' now displays as क from Noto Sans Devanagari")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
