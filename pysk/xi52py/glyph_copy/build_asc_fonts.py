#!/usr/bin/env python3
"""
build_asc_fonts.py

Build xi38asc + xi52asc for 9 Indian scripts using per-glyph
source/action from per-family CSVs: glyph_copy_xi38.csv and glyph_copy_xi52.csv
(4 columns: e52, src, action, notes).

Sources:
  - xe52asc.sfd            (English master, from sfdsrc/xe52)
  - xe38asc.sfd            (English xi38)
  - xh38asc.sfd             (Hindi source, from sfdsrc/xi38)
  - NotoSansMath-Regular.ttf     (EIOUMX symbols)
  - NotoSans{Script}-Regular.ttf (Indic consonants)

Actions:
  - replace: copy from source into target
  - keep:    leave target glyph as-is
  - manual:  leave target glyph as-is (same as keep)
  - remove:  (currently treated as keep)
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

# Sources: sfdsrc/ (designer-maintained), notofonts/
ENGLISH_52   = pff_root / "sfdsrc/xi52/xe52asc.sfd"
ENGLISH_38   = pff_root / "sfdsrc/xi38/xe38asc.sfd"
SFDSRC_XI38  = pff_root / "sfdsrc/xi38"
SFDSRC_XI52  = pff_root / "sfdsrc/xi52"
NOTO_MATH    = pff_root / "notofonts/NotoSansMath-Regular.ttf"
SFDSRC_ROOT  = pff_root / "sfdsrc"
CSV_PATH_38  = SFDSRC_ROOT / "glyph_copy_xi38.csv"
CSV_PATH_52  = SFDSRC_ROOT / "glyph_copy_xi52.csv"

# 9 scripts (Sinhala handled separately)
SCRIPTS = {
    'english':   {'notoindik': None, 'base': None,
                  'sfd38': 'xe38asc.sfd', 'sfd52': 'xe52asc.sfd'},
    'hindi':     {'notoindik': 'NotoSansDevanagari-Regular.ttf', 'base': 0x0900,
                  'sfd38': 'xh38asc.sfd',  'sfd52': 'xh52asc.sfd'},
    'bengali':   {'notoindik': 'NotoSansBengali-Regular.ttf',    'base': 0x0980,
                  'sfd38': 'xb38asc.sfd','sfd52': 'xb52asc.sfd'},
    'punjabi':   {'notoindik': 'NotoSansGurmukhi-Regular.ttf',   'base': 0x0A00,
                  'sfd38': 'xp38asc.sfd', 'sfd52': 'xp52asc.sfd'},
    'gujarati':  {'notoindik': 'NotoSansGujarati-Regular.ttf',   'base': 0x0A80,
                  'sfd38': 'xg38asc.sfd','sfd52': 'xg52asc.sfd'},
    'oriya':     {'notoindik': 'NotoSansOriya-Regular.ttf',      'base': 0x0B00,
                  'sfd38': 'xo38asc.sfd',  'sfd52': 'xo52asc.sfd'},
    'tamil':     {'notoindik': 'NotoSansTamil-Regular.ttf',      'base': 0x0B80,
                  'sfd38': 'xt38asc.sfd',   'sfd52': 'xt52asc.sfd'},
    'telugu':    {'notoindik': 'NotoSansTelugu-Regular.ttf',     'base': 0x0C00,
                  'sfd38': 'xj38asc.sfd', 'sfd52': 'xj52asc.sfd'},
    'kannada':   {'notoindik': 'NotoSansKannada-Regular.ttf',    'base': 0x0C80,
                  'sfd38': 'xk38asc.sfd',   'sfd52': 'xk52asc.sfd'},
    'malayalam': {'notoindik': 'NotoSansMalayalam-Regular.ttf',  'base': 0x0D00,
                  'sfd38': 'xm38asc.sfd','sfd52': 'xm52asc.sfd'},
}

# Indic consonants (Latin <- noto_indik offset) for the 8 scripts
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
    0x38: 's',    # स (was 0x37 ष - duplicate, dropped)
    0x39: 'H',
}

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


def read_csv(csv_path=None):
    """Read glyph copy CSV: e52, src, action, notes."""
    rows = []
    if csv_path is None:
        raise ValueError("read_csv: csv_path required")
    path = csv_path
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("e52,"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 3:
                continue
            rows.append({
                "e52":    parts[0],
                "src":    parts[1],
                "action": parts[2] if len(parts) > 2 else "replace",
                "notes":  parts[3] if len(parts) > 3 else "",
            })
    return rows


def copy_glyph(src_font, src_cp, dst_font, dst_cp):
    if src_cp not in src_font:
        return False
    try:
        # source select + copy
        src_font.selection.select(("unicode",), src_cp)
        src_font.copy()
        src_glyph = src_font[src_cp]
        dst_name = src_glyph.glyphname or f"uni{dst_cp:04X}"
        # target me slot nahi hai to -1 (encoding-independent) se banao
        if dst_cp not in dst_font and dst_name not in dst_font:
            dst_font.createChar(-1, dst_name)
            dst_glyph = dst_font[dst_name]
            dst_glyph.unicode = dst_cp
        else:
            dst_glyph = dst_font[dst_cp] if dst_cp in dst_font else dst_font[dst_name]
        dst_glyph.clear()
        dst_font.selection.select(("unicode",), dst_cp)
        dst_font.paste()
        return True
    except Exception as e:
        logging.warning(f"copy U+{dst_cp:04X} failed: {e}")
        return False
    if dst_cp not in dst_font:
        try:
            dst_font.createChar(dst_cp)
        except Exception as e:
            logging.warning(f"createChar U+{dst_cp:04X} failed: {e}")
            return False
    try:
        src_font.selection.select(("unicode",), src_cp)
        src_font.copy()
        glyph = dst_font[dst_cp]
        glyph.clear()
        dst_font.selection.select(("unicode",), dst_cp)
        dst_font.paste()
        return True
    except Exception as e:
        logging.warning(f"copy U+{dst_cp:04X} failed: {e}")
        return False


def offset_for_letter(letter):
    if letter in LETTER_OVERRIDES:
        return LETTER_OVERRIDES[letter]
    for off, ch in CONSONANT_OFFSETS.items():
        if ch == letter:
            return off
    return None


def apply_source(target_font, dst_cp, src_name, action, e52_char, ctx, ownsfd_key="ownsfd38"):
    """Apply one source value to target_font at dst_cp."""
    if action in ("keep", "manual", "remove"):
        return True  # preserve as-is

    if src_name == "xe52":
        return copy_glyph(ctx["xe52"], dst_cp, target_font, dst_cp)
    if src_name == "xe38":
        return copy_glyph(ctx["xe38"], dst_cp, target_font, dst_cp)
    if src_name == "ownsfd":
        if ctx.get(ownsfd_key) is None:
            return False
        return copy_glyph(ctx[ownsfd_key], dst_cp, target_font, dst_cp)
    if src_name == "noto_math":
        math_cp = MATH_SYMBOLS.get(dst_cp)
        if math_cp and copy_glyph(ctx["noto_math"], math_cp, target_font, dst_cp):
            return True
        return False
    if src_name == "notoindik":
        if ctx.get("notoindik") is None or ctx.get("base") is None:
            return False
        off = offset_for_letter(e52_char)
        if off is None:
            if e52_char in ("x", "A"):
                return copy_glyph(ctx["notoindik"], ctx["base"] + SCHWA_OFFSET,
                                  target_font, dst_cp)
            return False
        return copy_glyph(ctx["notoindik"], ctx["base"] + off, target_font, dst_cp)
    return False


def process_script(name, cfg, csv_rows_38, csv_rows_52, sources):
    # Per-script xi38 source from sfdsrc/
    # Hard fail: designer must provide sfdsrc source for each script.
    # No silent skip — if source missing, pipeline stops here.
    script_src_path = SFDSRC_XI38 / cfg["sfd38"]
    if not script_src_path.exists():
        raise FileNotFoundError(
            f"{name}: sfdsrc/xi38/{cfg['sfd38']} not found. "
            f"Designer must prepare it first (copy from sfd/ if needed)."
        )
    # Reuse already-open source font to avoid double-open (FontForge
    # closes the first handle when the same file is opened twice).
    if name == "english" and sources.get("xe38") is not None:
        script_font = sources["xe38"]
        owns_script_font = False
    else:
        script_font = fontforge.open(str(script_src_path))
        owns_script_font = True

    # 52 series source (designer master, always present)
    script_src_path_52 = SFDSRC_XI52 / cfg["sfd52"]
    if not script_src_path_52.exists():
        raise FileNotFoundError(
            f"{name}: sfdsrc/xi52/{cfg['sfd52']} not found. "
            f"Designer must prepare it first."
        )
    if name == "english" and sources.get("xe52") is not None:
        script_font_52 = sources["xe52"]
        owns_script_font_52 = False
    else:
        script_font_52 = fontforge.open(str(script_src_path_52))
        owns_script_font_52 = True

    # notoindik is optional (english/xe38 has no Noto source)
    noto_font = None
    if cfg.get("notoindik"):
        noto_path = pff_root / "notofonts" / cfg["notoindik"]
        if not noto_path.exists():
            logging.error(f"notoindik source not found: {noto_path}")
            script_font.close()
            return
        noto_font = fontforge.open(str(noto_path))

    target_38 = None
    target_52 = None
    try:
        target_38 = fontforge.open(str(pff_root / "sfd/xi38sfd/xi38asc" / cfg["sfd38"]))
        target_52 = fontforge.open(str(pff_root / "sfd/xi52sfd/xi52asc" / cfg["sfd52"]))

        ctx = {
            "xe52":      sources["xe52"],
            "xe38":      sources["xe38"],
            "ownsfd38":  script_font,
            "ownsfd52":  script_font_52,
            "noto_math": sources["noto_math"],
            "notoindik": noto_font,
            "base":      cfg["base"],
        }

        ok38 = ok52 = 0

        # Apply xi38 mapping
        for row in csv_rows_38:
            char = row["e52"]
            dst_cp = ord(char)
            try:
                if apply_source(target_38, dst_cp, row["src"], row["action"], char, ctx, ownsfd_key="ownsfd38"):
                    ok38 += 1
            except Exception as e:
                logging.warning(f"{name}: xi38 {char} failed: {e}")

        # Apply xi52 mapping
        for row in csv_rows_52:
            char = row["e52"]
            dst_cp = ord(char)
            try:
                if apply_source(target_52, dst_cp, row["src"], row["action"], char, ctx, ownsfd_key="ownsfd52"):
                    ok52 += 1
            except Exception as e:
                logging.warning(f"{name}: xi52 {char} failed: {e}")

        target_38.save(str(pff_root / "sfd/xi38sfd/xi38asc" / cfg["sfd38"]))
        target_52.save(str(pff_root / "sfd/xi52sfd/xi52asc" / cfg["sfd52"]))

        logging.info(f"{name}: xi38 ok={ok38}, xi52 ok={ok52}")
        print(f"  {name}: xi38={ok38}, xi52={ok52}")

    except Exception as e:
        logging.error(f"{name} failed: {e}")
        print(f"  {name}: FAILED - {e}")
        raise
    finally:
        for f in (noto_font, target_38, target_52):
            if f is not None:
                try:
                    f.close()
                except Exception as close_err:
                    logging.warning(f"{name}: close failed: {close_err}")
        if owns_script_font and script_font is not None:
            try:
                script_font.close()
            except Exception as close_err:
                logging.warning(f"{name}: close failed: {close_err}")
        if owns_script_font_52 and script_font_52 is not None:
            try:
                script_font_52.close()
            except Exception as close_err:
                logging.warning(f"{name}: close failed: {close_err}")

def main():
    csv_rows_38 = read_csv(CSV_PATH_38)
    csv_rows_52 = read_csv(CSV_PATH_52)
    print(f"Read {len(csv_rows_38)} rows from {CSV_PATH_38.name}")
    print(f"Read {len(csv_rows_52)} rows from {CSV_PATH_52.name}")

    sources = {
        "xe52":      fontforge.open(str(ENGLISH_52)),
        "xe38":      fontforge.open(str(ENGLISH_38)),
        "noto_math": fontforge.open(str(NOTO_MATH)),
    }

    if len(sys.argv) >= 2 and sys.argv[1].lower() != "all":
        name = sys.argv[1].lower()
        if name in SCRIPTS:
            process_script(name, SCRIPTS[name], csv_rows_38, csv_rows_52, sources)
        else:
            print(f"Unknown script: {name}")
    else:
        for name, cfg in SCRIPTS.items():
            process_script(name, cfg, csv_rows_38, csv_rows_52, sources)

    for f in sources.values():
        f.close()

    print("Done.")


if __name__ == "__main__":
    main()
