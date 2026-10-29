#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-
"""
gen_noto_sheets.py

Read each NotoSans*-Regular.ttf using fontforge.
For each of 10 Indic script ranges, extract glyph details and
write to one sheet in pffsheets/noto_glyph_sheets.xlsx.

Sheet columns:
  hex       : unicode codepoint (e.g. 0915)
  unicode   : codepoint as U+XXXX
  noto_name : glyph name in NotoSans font
  nameslist : hskii value from NamesList.txt
  hskii     : resolved single hskii char (or 'clear')
  width     : advance width in NotoSans
  has_glyph : Y/N (isWorthOutputting)
  in_json   : hskii char in asc-to-utf.json for this slot

run:
  fontforge -script pysk/notopy/gen_noto_sheets.py

requires openpyxl:
  pip install openpyxl
"""

import fontforge
import sys
import json
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
except ImportError:
    print("ERROR: openpyxl not installed. run: pip install openpyxl")
    sys.exit(1)

pff_root  = Path(__file__).resolve().parents[2]
NOTO_DIR  = pff_root / "pysk/notopy"
NAMES_TXT = pff_root / "pysk/notopy/NamesList.txt"
JSON_PATH = pff_root / "sfdsrc/asc-to-utf.json"
OUT_XLSX  = pff_root / "pffsheets/noto_glyph_sheets.xlsx"

# 10 scripts: (script_name, font_prefix, noto_ttf, unicode_base)
SCRIPTS = [
    ("Devanagari", "xh38", "NotoSansDevanagari-Regular.ttf", 0x0900),
    ("Bengali",    "xb38", "NotoSansBengali-Regular.ttf",    0x0980),
    ("Gurmukhi",   "xp38", "NotoSansGurmukhi-Regular.ttf",   0x0A00),
    ("Gujarati",   "xg38", "NotoSansGujarati-Regular.ttf",   0x0A80),
    ("Odia",       "xo38", "NotoSansOriya-Regular.ttf",      0x0B00),
    ("Tamil",      "xt38", "NotoSansTamil-Regular.ttf",      0x0B80),
    ("Telugu",     "xj38", "NotoSansTelugu-Regular.ttf",     0x0C00),
    ("Kannada",    "xk38", "NotoSansKannada-Regular.ttf",    0x0C80),
    ("Malayalam",  "xm38", "NotoSansMalayalam-Regular.ttf",  0x0D00),
    ("Sinhala",    "xs38", "NotoSansSinhala-Regular.ttf",    0x0D80),
]

# column widths for the sheet
COL_WIDTHS = [8, 10, 22, 16, 8, 8, 10, 10]
HEADERS    = ["hex", "unicode", "noto_name", "nameslist", "hskii", "width", "has_glyph", "in_json"]

HEADER_FILL  = PatternFill("solid", fgColor="1F497D")
HEADER_FONT  = Font(bold=True, color="FFFFFF", name="Consolas", size=10)
CLEAR_FILL   = PatternFill("solid", fgColor="F2DCDB")   # light red = clear
GLYPH_FILL   = PatternFill("solid", fgColor="EBF1DE")   # light green = has glyph
NORMAL_FONT  = Font(name="Consolas", size=9)
CENTER_ALIGN = Alignment(horizontal="center")


# ── parse NamesList.txt ──────────────────────────────────────────────────────

VALUE_TO_HSKII = {
    'ga':'g','gha':'G','ca':'c','chha':'C',
    'nga':None,'nha':None,'wa':'w','maa':'m','fa':'f',
    'aa':'a','ee':'e','ai':'e','au':'o','aira':'A',
    'khha':'K','ghha':'G','za':'z','yya':'y','zha':'z',
    'ttta':None,'nnga':None,'nndda':None,'mba':None,
    'nyja':None,'jnya':None,'nda':None,
    'OE':None,'OOE':None,'AA':'a','AI':'e','AU':'o',
    'oe':None,'ui':None,'eei':None,'uui':None,
    'candrabindu':None,'anunasika':None,'bindu':None,'visarga':None,
    'anusvara':None,'nukta':None,'avagraha':None,'virama':None,
    'viram':None,'halant':None,'sign':None,'mark':None,
    'tippi':None,'addak':None,'bindi':None,'aytham':None,
    'pulli':None,'iri':None,'ura':None,'onkar':None,'yakash':None,
    'knna':None,'sihari':None,'bihari':None,'aunkar':None,
    'dulainkar':None,'lanvan':None,'dulanvan':None,'hora':None,
    'knaura':None,'udaat':None,'svarita':None,'anudatta':None,
    'accent':None,'isshar':None,'siddhirastu':None,'kunddaliya':None,
    'pra':None,'reph':None,'praslesham':None,'om':None,
    'arasunna':None,'sunna':None,
    'SHORT':None,'ADAK':None,'LENGTH':None,'COMBINING':None,
    'CANDRA':None,'VOCALIC':None,'PRISHTHAMATRA':None,'AW':None,
    'ANUSVARA':None,'HIGH':None,
}

def parse_nameslist(path):
    """Return {codepoint_int: (raw_value, hskii_char_or_clear)}"""
    result = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line: continue
            hex_str, rest = line.split('-', 1)
            raw = rest.split('#')[0].strip()
            if not raw or raw == '<reserved>': continue
            try: cp = int(hex_str, 16)
            except: continue
            # space in value = Unicode descriptive name = clear
            if ' ' in raw:
                result[cp] = (raw, 'clear')
                continue
            if raw in VALUE_TO_HSKII:
                ch = VALUE_TO_HSKII[raw]
                result[cp] = (raw, ch if ch else 'clear')
            else:
                result[cp] = (raw, raw[0])
    return result


def load_json_map(path):
    """Return {(col_idx, offset): hskii_char} from asc-to-utf.json"""
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    result = {}
    cols = data['columns'][1:]   # skip 'offset'
    for offset_hex, row in data['rows'].items():
        for col_idx, ch in enumerate(row):
            result[(col_idx, int(offset_hex, 16))] = ch
    return result, cols


# ── build one sheet ──────────────────────────────────────────────────────────

def build_sheet(ws, script_name, font_prefix, ttf_path, base_cp,
                col_idx, nameslist_map, json_map):
    """Fill one worksheet with glyph data for this script range."""
    ws.title = f"{font_prefix} {script_name}"

    # header
    for c, (h, w) in enumerate(zip(HEADERS, COL_WIDTHS), 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font  = HEADER_FONT
        cell.fill  = HEADER_FILL
        cell.alignment = CENTER_ALIGN
        ws.column_dimensions[cell.column_letter].width = w

    ws.freeze_panes = "A2"

    # open NotoSans font
    if not ttf_path.exists():
        ws.cell(row=2, column=1, value=f"TTF not found: {ttf_path.name}")
        return 0

    print(f"  opening {ttf_path.name} ...")
    noto = fontforge.open(str(ttf_path))

    count = 0
    for offset in range(0x80):
        cp = base_cp + offset
        hex_str   = f"{cp:04X}"
        uni_str   = f"U+{cp:04X}"

        # NotoSans glyph info
        try:
            g          = noto[cp]
            noto_name  = g.glyphname
            width      = g.width
            has_glyph  = "Y" if g.isWorthOutputting() else "N"
        except Exception:
            noto_name  = "-"
            width      = 0
            has_glyph  = "N"

        # NamesList info
        nl_raw, nl_hskii = nameslist_map.get(cp, ("-", "clear"))

        # asc-to-utf.json info
        in_json = json_map.get((col_idx, offset), "clear")

        row = offset + 2
        vals = [hex_str, uni_str, noto_name, nl_raw, nl_hskii, width, has_glyph, in_json]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = NORMAL_FONT
            if c in (1, 2, 5, 7, 8):
                cell.alignment = CENTER_ALIGN

        # highlight rows
        fill = GLYPH_FILL if has_glyph == "Y" else CLEAR_FILL
        for c in range(1, len(HEADERS)+1):
            ws.cell(row=row, column=c).fill = fill

        count += 1

    noto.close()
    return count


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    print("gen_noto_sheets — reading NamesList.txt ...")
    nameslist_map = parse_nameslist(NAMES_TXT)
    print(f"  {len(nameslist_map)} entries")

    print("reading asc-to-utf.json ...")
    json_map, json_cols = load_json_map(JSON_PATH)

    wb = openpyxl.Workbook()
    # remove default sheet
    wb.remove(wb.active)

    for idx, (script, prefix, ttf_name, base) in enumerate(SCRIPTS):
        print(f"\n[{idx+1}/10] {script} ({prefix})")
        ws = wb.create_sheet()
        ttf_path = NOTO_DIR / ttf_name
        count = build_sheet(ws, script, prefix, ttf_path, base,
                            idx, nameslist_map, json_map)
        print(f"  {count} rows written")

    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(OUT_XLSX))
    print(f"\nSaved: {OUT_XLSX}")


if __name__ == "__main__":
    main()
