#!/usr/bin/env python3
"""
Script to copy Sinhala glyphs from Noto to sinhlaxs38.sfd.
Sinhala uses different offset mapping (0x0D80 block).
"""

import fontforge
from pathlib import Path

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent
noto_font_path = pff_root / "notofonts" / "NotoSansSinhala-Regular.ttf"
sfd_path = pff_root / "sfd/x38ifont/x38iasc/sinhlaxs38.sfd"

font_repo = Path("C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font")
ttf_dir = font_repo / "ttf/hscii/xi38font"
woff2_dir = font_repo / "woff2/hscii/xi38font"

# Sinhala offset mapping (from htrlib)
# Format: {offset: hskii_char}
SINHALA_OFFSET_MAP = {
    # Vowels
    0x05: 'x',    # අ
    0x06: 'a',    # ආ
    0x07: 'e',    # ඇ (AE)
    0x08: 'e',    # ඈ (ae)
    0x09: 'i',    # ඉ (AI)
    0x0A: 'i',    # ඊ (AI)
    0x0B: 'u',    # උ (AU)
    0x0C: 'u',    # ඌ (AU)
    0x0D: 'r',    # ඍ
    0x0E: 'r',    # ඎ (ri)
    0x0F: 'l',    # ඏ
    0x10: 'l',    # ඐ (li)
    0x11: 'e',    # එ (AE)
    0x12: 'e',    # ඒ (AE)
    0x13: 'e',    # ඓ (AE)
    0x14: 'o',    # ඔ (AO)
    0x15: 'o',    # ඕ (AO)
    0x16: 'o',    # ඖ (AO)

    # Consonants
    0x1A: 'k',    # ක
    0x1B: 'K',    # ඛ
    0x1C: 'g',    # ග
    0x1D: 'G',    # ඝ (gh → G)
    0x1E: 'N',    # ඞ
    0x1F: 'N',    # ඟ
    0x20: 'c',    # ච (ch → c)
    0x21: 'C',    # ඡ (Ch → C)
    0x22: 'z',    # ජ
    0x23: 'Z',    # ඣ
    0x24: 'n',    # ඤ
    0x25: 'n',    # ඥ
    0x26: 'n',    # ඦ
    0x27: 't',    # ට
    0x28: 'T',    # ඨ
    0x29: 'd',    # ඩ
    0x2A: 'D',    # ඪ
    0x2B: 'n',    # ණ
    0x2C: 'n',    # ඬ
    0x2D: 'j',    # ත
    0x2E: 'J',    # ථ
    0x2F: 'q',    # ද
    0x30: 'Q',    # ධ
    0x31: 'n',    # න
    0x33: 'n',    # ඳ (nq)
    0x34: 'p',    # ප
    0x35: 'f',    # ඵ
    0x36: 'b',    # බ
    0x37: 'B',    # භ
    0x38: 'm',    # ම
    0x39: 'm',    # ඹ (mb)
    0x3A: 'y',    # ය
    0x3B: 'r',    # ර
    0x3D: 'l',    # ල
    0x40: 'w',    # ව
    0x41: 'S',    # ශ
    0x42: 's',    # ෂ
    0x43: 's',    # ස
    0x44: 'H',    # හ
    0x45: 'l',    # ළ
    0x46: 'f',    # ෆ

    # Matras
    0x4F: 'a',    # ා
    0x50: 'e',    # ැ
    0x51: 'e',    # ෑ (ae)
    0x52: 'i',    # ි
    0x53: 'i',    # ී
    0x54: 'u',    # ු
    0x56: 'u',    # ූ
    0x58: 'r',    # ෘ (ri)
    0x59: 'e',    # ෙ
    0x5A: 'e',    # ේ
    0x5B: 'e',    # ෛ (ye)
    0x5C: 'o',    # ො
    0x5D: 'o',    # ෝ
    0x5E: 'o',    # ෞ
    0x5F: 'l',    # ෟ

    # Digits
    0x66: '0', 0x67: '1', 0x68: '2', 0x69: '3', 0x6A: '4',
    0x6B: '5', 0x6C: '6', 0x6D: '7', 0x6E: '8', 0x6F: '9',

    # Punctuation
    0x74: '.',    # ෴
}

SINHALA_BASE = 0x0D80


def main():
    if not noto_font_path.exists():
        print(f"✗ Noto not found: {noto_font_path}")
        return

    if not sfd_path.exists():
        print(f"✗ SFD not found: {sfd_path}")
        return

    print(f"Processing Sinhala...")
    print(f"  Noto: {noto_font_path.name}")
    print(f"  SFD: {sfd_path.name}")

    noto_font = fontforge.open(str(noto_font_path))
    target_font = fontforge.open(str(sfd_path))

    success = errors = 0

    for offset, hskii_char in SINHALA_OFFSET_MAP.items():
        src_unicode = SINHALA_BASE + offset

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

    print(f"\nSuccess: {success}, Errors: {errors}")

    if success > 0:
        target_font.save(str(sfd_path))
        print(f"✓ Saved SFD")

        ttf_path = ttf_dir / "sinhlaxs38.ttf"
        target_font.generate(str(ttf_path))
        print(f"✓ TTF: {ttf_path.name}")

        woff2_path = woff2_dir / "sinhlaxs38.woff2"
        target_font.generate(str(woff2_path))
        print(f"✓ WOFF2: {woff2_path.name}")

    noto_font.close()
    target_font.close()
    print("\nDone!")


if __name__ == "__main__":
    main()