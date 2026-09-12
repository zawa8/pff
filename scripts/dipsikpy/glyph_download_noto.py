#!/usr/bin/env python3
"""
Script to download all Noto fonts needed for xi38 fonts.
Uses Google Fonts GitHub repository.
"""

import urllib.request
from pathlib import Path

script_dir = Path(__file__).parent
notofonts_dir = script_dir.parent / "notofonts"
notofonts_dir.mkdir(exist_ok=True)

# Google Fonts URLs (raw)
NOTO_FONTS = {
    'NotoSansBengali-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosansbengali/NotoSansBengali%5Bwdth%2Cwght%5D.ttf',
    'NotoSansGurmukhi-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosansgurmukhi/NotoSansGurmukhi%5Bwdth%2Cwght%5D.ttf',
    'NotoSansGujarati-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosansgujarati/NotoSansGujarati%5Bwdth%2Cwght%5D.ttf',
    'NotoSansOriya-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosansoriya/NotoSansOriya%5Bwdth%2Cwght%5D.ttf',
    'NotoSansTamil-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosanstamil/NotoSansTamil%5Bwdth%2Cwght%5D.ttf',
    'NotoSansTelugu-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosanstelugu/NotoSansTelugu%5Bwdth%2Cwght%5D.ttf',
    'NotoSansKannada-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosanskannada/NotoSansKannada%5Bwdth%2Cwght%5D.ttf',
    'NotoSansMalayalam-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosansmalayalam/NotoSansMalayalam%5Bwdth%2Cwght%5D.ttf',
    'NotoSansSinhala-Regular.ttf':
        'https://github.com/google/fonts/raw/main/ofl/notosanssinhala/NotoSansSinhala%5Bwdth%2Cwght%5D.ttf',
}

def download_font(name, url):
    font_path = notofonts_dir / name
    if font_path.exists():
        print(f"✓ Already exists: {name}")
        return True
    print(f"⬇ Downloading: {name}")
    try:
        urllib.request.urlretrieve(url, str(font_path))
        print(f"✓ Downloaded: {name}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print(f"Downloading to: {notofonts_dir}")
    print("=" * 60)
    success = failed = 0
    for name, url in NOTO_FONTS.items():
        if download_font(name, url):
            success += 1
        else:
            failed += 1
    print("=" * 60)
    print(f"Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()