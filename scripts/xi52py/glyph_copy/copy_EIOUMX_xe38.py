#!/usr/bin/env python3
"""
copy_EIOUMX_xe38.py
"""
import fontforge
import sys
from pathlib import Path

PFF_ROOT   = Path("C:/progxs/pff")
NOTO_MATH  = PFF_ROOT / "notofonts" / "NotoSansMath-Regular.ttf"
TARGET_SFD = PFF_ROOT / "sfd" / "xi38font" / "xi38asc" / "eNgliSxe38.sfd"

SYMBOL_MAP = {
    0x45: 0x2261,  # E -> ≡
    0x49: 0x2260,  # I -> ≠
    0x4F: 0x2192,  # O -> →
    0x55: 0x2193,  # U -> ↓
    0x4D: 0x2265,  # M -> ≥
    0x58: 0x2264,  # X -> ≤
}


def main():
    print(f"Source: {NOTO_MATH}")
    print(f"Target: {TARGET_SFD}")

    if not NOTO_MATH.exists():
        print(f"Error: source not found")
        sys.exit(1)
    if not TARGET_SFD.exists():
        print(f"Error: target not found")
        sys.exit(1)

    src    = fontforge.open(str(NOTO_MATH))
    target = fontforge.open(str(TARGET_SFD))

    ok = 0
    skip = 0
    for dst_cp, src_cp in SYMBOL_MAP.items():
        letter = chr(dst_cp)
        print(f"  {letter} (U+{dst_cp:04X}) <- U+{src_cp:04X}", end=" ... ")

        if src_cp not in src:
            print("NOT IN SOURCE, skipped")
            skip += 1
            continue
        if dst_cp not in target:
            print("NOT IN TARGET, skipped")
            skip += 1
            continue

        try:
            # Select source glyph by unicode codepoint
            src.selection.select(("unicode",), src_cp)
            src.copy()

            # Clear target glyph and paste
            glyph = target[dst_cp]
            glyph.clear()
            target.selection.select(("unicode",), dst_cp)
            target.paste()

            print("OK")
            ok += 1
        except Exception as e:
            print(f"ERROR: {e}")
            skip += 1

    print(f"\nCopied {ok}, skipped {skip}")

    if ok > 0:
        print(f"Saving {TARGET_SFD}")
        target.save(str(TARGET_SFD))
    else:
        print("Nothing copied, not saving")

    src.close()
    target.close()
    print("Done.")


if __name__ == "__main__":
    main()