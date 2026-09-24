#!/usr/bin/env python3
"""
Script to copy Sinhala glyphs from Noto to xs38asc.sfd.
Also copies 0x00-0x40, a,e,i,u,o,N, and E,I,M,L,O,P,U,V,W,X,Y from xe38asc.sfd.

Mapping (ASCII | Sinhala | Hindi):
    B | භ 0DB7 | भ 092D
    C | ඡ 0DA1 | छ 091B
    D | ද 0DAF | द 0926
    G | ඝ 0D9D | घ 0918
    H | හ 0DC4 | ह 0939
    J | ථ 0DAE | थ 0925
    K | ඛ 0D9B | ख 0916
    N | (English) | N
    Q | ධ 0DB0 | ध 0927
    R | ර 0DBB | र 0930
    S | ශ 0DC1 | श 0936
    T | ඨ 0DA8 | ठ 0920
    Z | ඣ 0DA3 | झ 091D
    b | බ 0DB6 | ब 092C
    c | ච 0DA0 | च 091A
    d | ඩ 0DA9 | ड 0921
    f | ෆ 0DC6 | फ 092B
    g | ග 0D9C | ग 0917
    j | ත 0DAD | त 0924
    k | ක 0D9A | क 0915
    l | ල 0DBD | ल 0932
    m | ම 0DB8 | म 092E
    n | න 0DB1 | न 0928
    p | ප 0DB4 | प 092A
    q | ද 0DAF | द 0926
    r | ර 0DBB | र 0930
    s | ස 0DC3 | स 0938
    t | ට 0DA7 | ट 091F
    v | හ 0DC4 | ह 0939
    w | ව 0DC0 | व 0935
    x | අ 0D85 | अ 0905
    y | ය 0DBA | य 092F
    z | ජ 0DA2 | ज 091C
"""

import fontforge
import logging
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent.parent  # glyph_copy/ is 2 levels deeper than xi52py/'s other scripts

# Log
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "glyph_kopi_usinhala.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

# Sources
noto_font_path = pff_root / "notofonts" / "NotoSansSinhala-Regular.ttf"
english_sfd = pff_root / "sfd/xi38sfd/xi38asc/xe38asc.sfd"
sfd_path = pff_root / "sfd/xi38sfd/xi38asc/xs38asc.sfd"

# Output
# font_repo removed (use pff_root)
ttf_dir = pff_root / "xnglofonts/ttf/xi38ttf/xi38asc"
woff2_dir = pff_root / "xnglofonts/woff2/xi38woff2/xi38asc"

# Sinhala consonants from Noto
# Format: {offset: hskii_char}
# Mapping: ASCII | Sinhala | Hindi
SINHALA_OFFSET_MAP = {
    # Consonants
    0x1A: 'k',    # k | ක 0D9A | क 0915
    0x1B: 'K',    # K | ඛ 0D9B | ख 0916
    0x1C: 'g',    # g | ග 0D9C | ग 0917
    0x1D: 'G',    # G | ඝ 0D9D | घ 0918
    # 0x1E: 'N',  # N | (English) - skip
    0x20: 'c',    # c | ච 0DA0 | च 091A
    0x21: 'C',    # C | ඡ 0DA1 | छ 091B
    0x22: 'z',    # z | ජ 0DA2 | ज 091C
    0x23: 'Z',    # Z | ඣ 0DA3 | झ 091D
    0x27: 't',    # t | ට 0DA7 | ट 091F
    0x28: 'T',    # T | ඨ 0DA8 | ठ 0920
    0x29: 'd',    # d | ඩ 0DA9 | ड 0921
    0x2A: 'D',    # D | ද 0DAF | द 0926
    0x2D: 'j',    # j | ත 0DAD | त 0924
    0x2E: 'J',    # J | ථ 0DAE | थ 0925
    0x2F: 'q',    # q | ද 0DAF | द 0926
    0x30: 'Q',    # Q | ධ 0DB0 | ध 0927
    0x31: 'n',    # n | න 0DB1 | न 0928
    0x34: 'p',    # p | ප 0DB4 | प 092A
    0x35: 'f',    # f | ෆ 0DC6 | फ 092B
    0x36: 'b',    # b | බ 0DB6 | ब 092C
    0x37: 'B',    # B | භ 0DB7 | भ 092D
    0x38: 'm',    # m | ම 0DB8 | म 092E
    0x3A: 'y',    # y | ය 0DBA | य 092F
    0x3B: 'r',    # r | ර 0DBB | र 0930
    0x3D: 'l',    # l | ල 0DBD | ल 0932
    0x40: 'w',    # w | ව 0DC0 | व 0935
    0x41: 'S',    # S | ශ 0DC1 | श 0936
    0x42: 's',    # s | ස 0DC3 | स 0938
    0x43: 's',    # s | ස 0DC3 | स 0938
    0x44: 'H',    # H | හ 0DC4 | ह 0939
    0x45: 'l',    # l | ළ 0DC5 | ळ 0933
    0x46: 'f',    # f | ෆ 0DC6 | फ़ 095E
}

SINHALA_BASE = 0x0D80

# Extra English chars from xe38asc.sfd
EXTRA_ENGLISH = [
    ord('N'),  # N | (English)
    ord('a'),  # a | (English)
    ord('e'),  # e | (English)
    ord('i'),  # i | (English)
    ord('u'),  # u | (English)
    ord('o'),  # o | (English)
    ord('E'),  # E | (English)
    ord('I'),  # I | (English)
    ord('M'),  # M | (English)
    ord('L'),  # L | (English)
    ord('O'),  # O | (English)
    ord('P'),  # P | (English)
    ord('U'),  # U | (English)
    ord('V'),  # V | (English)
    ord('W'),  # W | (English)
    ord('X'),  # X | (English)
    ord('Y'),  # Y | (English)
]


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
    eng_font = fontforge.open(str(english_sfd))
    target_font = fontforge.open(str(sfd_path))

    success = 0

    # STEP 1: Sinhala consonants from Noto
    print("\n[1] Copying Sinhala glyphs from Noto...")
    for offset, hskii_char in SINHALA_OFFSET_MAP.items():
        src_unicode = SINHALA_BASE + offset
        if src_unicode not in noto_font or not hskii_char:
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
                logging.debug(f"  ✓ {hskii_char} ← U+{src_unicode:04X}")
        except Exception as e:
            logging.warning(f"  ✗ Error 0x{offset:02X}: {e}")

    # STEP 2: 0x00-0x40 from English
    print("\n[2] Copying 0x00-0x40 from English...")
    for ascii_code in range(0x00, 0x41):
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
            logging.warning(f"  ✗ Error {ascii_code}: {e}")

    # STEP 3: Extra English chars
    print("\n[3] Copying extra English chars...")
    for ascii_code in EXTRA_ENGLISH:
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
            logging.info(f"  ✓ Copied '{chr(ascii_code)}'")
        except Exception as e:
            logging.warning(f"  ✗ Error {ascii_code}: {e}")

    print(f"\nSuccess: {success}")

    target_font.save(str(sfd_path))
    print(f"✓ Saved SFD: {sfd_path.name}")

    target_font.generate(str(ttf_dir / "xs38asc.ttf"))
    print(f"✓ TTF: xs38asc.ttf")

    target_font.generate(str(woff2_dir / "xs38asc.woff2"))
    print(f"✓ WOFF2: xs38asc.woff2")

    noto_font.close()
    eng_font.close()
    target_font.close()
    print("\nDone!")


if __name__ == "__main__":
    main()