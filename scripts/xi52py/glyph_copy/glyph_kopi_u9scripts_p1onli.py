#!/usr/bin/env python3
"""
glyph_kopi_u9scripts_p1onli.py

Build xi38asc and xi52asc SFDs for 9 Indian scripts using the G1–G5
copy rules from glyph_copy.csv.

For each script (e.g. hindi):
  - xh38asc.sfd (hindixh38asc.sfd)  ← xh38_src
  - xh52asc.sfd (hindixh52asc.sfd)  ← xh52_src

Sources:
  - eNgliSxe52asc.sfd            (Latin, master)
  - eNgliSxe38asc.sfd            (Latin, xi38 English)
  - NotoSansMath-Regular.ttf     (EIOUMX symbols)
  - NotoSans{Script}-Regular.ttf (Indic consonants, per script)

Does NOT generate TTF/WOFF2. Does NOT build eNgliSxe38asc.sfd
(that's a separate manual/script task).

Run with FontForge's Python:
    fontforge -script glyph_kopi_u9scripts_p1onli.py
    fontforge -script glyph_kopi_u9scripts_p1onli.py hindi
"""

import sys
import csv
import fontforge
import logging
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent.parent

log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "glyph_kopi_u9scripts.log"

logging.basicConfig(
    filename=str(log_file), level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s', filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)

ENGLISH_52 = pff_root / "sfd/xi52sfd/xi52asc/eNgliSxe52asc.sfd"
ENGLISH_38 = pff_root / "sfd/xi38sfd/xi38asc/eNgliSxe38asc.sfd"
NOTO_MATH  = pff_root / "notofonts/NotoSansMath-Regular.ttf"
CSV_PATH   = script_dir / "glyph_copy.csv"

# 9 scripts (Sinhala has its own script)
SCRIPTS = {
    'hindi':     {'noto': 'NotoSansDevanagari-Regular.ttf', 'base': 0x0900,
                  'sfd38': 'hindixh38asc.sfd',  'sfd52': 'hindixh52asc.sfd'},
    'bengali':   {'noto': 'NotoSansBengali-Regular.ttf',    'base': 0x0980,
                  'sfd38': 'bengalixb38asc.sfd','sfd52': 'bengalixb52asc.sfd'},
    'punjabi':   {'noto': 'NotoSansGurmukhi-Regular.ttf',   'base': 0x0A00,
                  'sfd38': 'pnzabixp38asc.sfd', 'sfd52': 'pnzabixp52asc.sfd'},
    'gujarati':  {'noto': 'NotoSansGujarati-Regular.ttf',   'base': 0x0A80,
                  'sfd38': 'guzrajixg38asc.sfd','sfd52': 'guzrajixg52asc.sfd'},
    'oriya':     {'noto': 'NotoSansOriya-Regular.ttf',      'base': 0x0B00,
                  'sfd38': 'oriyaxo38asc.sfd',  'sfd52': 'oriyaxo52asc.sfd'},
    'tamil':     {'noto': 'NotoSansTamil-Regular.ttf',      'base': 0x0B80,
                  'sfd38': 'tmilxt38asc.sfd',   'sfd52': 'tmilxt52asc.sfd'},
    'telugu':    {'noto': 'NotoSansTelugu-Regular.ttf',     'base': 0x0C00,
                  'sfd38': 'jeluguxj38asc.sfd', 'sfd52': 'jeluguxj52asc.sfd'},
    'kannada':   {'noto': 'NotoSansKannada-Regular.ttf',    'base': 0x0C80,
                  'sfd38': 'knRaxk38asc.sfd',   'sfd52': 'knRaxk52asc.sfd'},
    'malayalam': {'noto': 'NotoSansMalayalam-Regular.ttf',  'base': 0x0D00,
                  'sfd38': 'mlyalxmxm38asc.sfd','sfd52': 'mlyalxmxm52asc.sfd'},
}

# Indic consonants (Latin <- Noto offset) for the 8 scripts with same layout
# Priority for duplicate letters (n appears 3 times) is set explicitly in
# offset_for_letter().
CONSONANT_OFFSETS = {
    0x15: 'k',  0x16: 'K',
    0x17: 'g',  0x18: 'G',
    0x1A: 'c',  0x1B: 'C',
    0x1C: 'z',  0x1D: 'Z',
    0x1F: 't',  0x20: 'J',
    0x21: 'd',  0x22: 'Q',
    0x24: 'T',  0x25: 'j',
    0x26: 'D',  0x27: 'q',
    0x2A: 'p',  0x2B: 'f',
    0x2C: 'b',  0x2D: 'B',
    0x2E: 'm',  0x2F: 'y',
    0x30: 'r',  0x32: 'l',
    0x35: 'w',  0x36: 'S',
    0x37: 's',  0x38: 's',
    0x39: 'H',
}

# For duplicate Latin targets, pick the correct Noto codepoint.
# (n → न, not ञ or ण)
LETTER_OVERRIDES = {
    'n': 0x28,   # न
}

MATH_SYMBOLS = {
    ord('E'): 0x2261,  # ≡
    ord('I'): 0x2260,  # ≠
    ord('O'): 0x2192,  # →
    ord('U'): 0x2193,  # ↓
    ord('M'): 0x2265,  # ≥
    ord('X'): 0x2264,  # ≤
}

SCHWA_OFFSET = 0x05


def read_csv():
    rows = []
    with open(CSV_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("e52,"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 4:
                continue
            rows.append({
                "e52":      parts[0],
                "xe38_src": parts[1],
                "xh52_src": parts[2],
                "xh38_src": parts[3],
            })
    return rows


def copy_glyph(src_font, src_cp, dst_font, dst_cp):
    if src_cp not in src_font or dst_cp not in dst_font:
        return False
    src_font.selection.select(("unicode",), src_cp)
    src_font.copy()
    glyph = dst_font[dst_cp]
    glyph.clear()
    dst_font.selection.select(("unicode",), dst_cp)
    dst_font.paste()
    return True


def offset_for_letter(letter):
    """Return Noto offset for a Latin target letter."""
    if letter in LETTER_OVERRIDES:
        return LETTER_OVERRIDES[letter]
    for off, ch in CONSONANT_OFFSETS.items():
        if ch == letter:
            return off
    return None


def apply_source(target_font, dst_cp, src_name, e52_char, ctx):
    """Apply one source value to target_font at dst_cp."""
    if src_name == "xe52":
        return copy_glyph(ctx["xe52"], dst_cp, target_font, dst_cp)
    if src_name == "xe38":
        return copy_glyph(ctx["xe38"], dst_cp, target_font, dst_cp)
    if src_name == "noto_math":
        math_cp = MATH_SYMBOLS.get(dst_cp)
        if math_cp and copy_glyph(ctx["noto_math"], math_cp, target_font, dst_cp):
            return True
        return False
    if src_name == "noto":
        off = offset_for_letter(e52_char)
        if off is None:
            # Not a consonant; try schwa (x, A)
            if e52_char in ("x", "A"):
                return copy_glyph(ctx["noto"], ctx["base"] + SCHWA_OFFSET,
                                  target_font, dst_cp)
            return False
        return copy_glyph(ctx["noto"], ctx["base"] + off, target_font, dst_cp)
    # 'manual' / unknown -> skip
    return False


def process_script(name, cfg, csv_rows, sources):
    noto_path = pff_root / "notofonts" / cfg["noto"]
    if not noto_path.exists():
        logging.error(f"Noto not found: {noto_path}")
        return

    noto_font = fontforge.open(str(noto_path))
    target_38 = fontforge.open(str(pff_root / "sfd/xi38sfd/xi38asc" / cfg["sfd38"]))
    target_52 = fontforge.open(str(pff_root / "sfd/xi52sfd/xi52asc" / cfg["sfd52"]))

    ctx = {
        "xe52":      sources["xe52"],
        "xe38":      sources["xe38"],
        "noto_math": sources["noto_math"],
        "noto":      noto_font,
        "base":      cfg["base"],
    }

    ok38 = ok52 = 0

    for row in csv_rows:
        char = row["e52"]
        dst_cp = ord(char)

        # xi38 (hindixh38asc.sfd)
        if apply_source(target_38, dst_cp, row["xh38_src"], char, ctx):
            ok38 += 1

        # xi52 (hindixh52asc.sfd)
        if apply_source(target_52, dst_cp, row["xh52_src"], char, ctx):
            ok52 += 1

    target_38.save(str(pff_root / "sfd/xi38sfd/xi38asc" / cfg["sfd38"]))
    target_52.save(str(pff_root / "sfd/xi52sfd/xi52asc" / cfg["sfd52"]))

    logging.info(f"{name}: xi38 ok={ok38}, xi52 ok={ok52}")
    print(f"  {name}: xi38={ok38}, xi52={ok52}")

    noto_font.close()
    target_38.close()
    target_52.close()

def build_sources():
    return {
        "xe52":      fontforge.open(str(ENGLISH_52)),
        "xe38":      fontforge.open(str(ENGLISH_38)),
        "noto_math": fontforge.open(str(NOTO_MATH)),
    }

def main():
    csv_rows = read_csv()
    print(f"Read {len(csv_rows)} rows from {CSV_PATH.name}")

    sources = {
        "xe52":      fontforge.open(str(ENGLISH_52)),
        "xe38":      fontforge.open(str(ENGLISH_38)),
        "noto_math": fontforge.open(str(NOTO_MATH)),
    }

    if len(sys.argv) >= 2 and sys.argv[1].lower() != "all":
        name = sys.argv[1].lower()
        if name in SCRIPTS:
            process_script(name, SCRIPTS[name], csv_rows, sources)
        else:
            print(f"Unknown script: {name}")
    else:
        for name, cfg in SCRIPTS.items():
            process_script(name, cfg, csv_rows, sources)

    for f in sources.values():
        f.close()

    print("Done.")


if __name__ == "__main__":
    main()