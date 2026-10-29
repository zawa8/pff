#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-
"""
extract_noto_data.py  (part 1 of 2)

Uses FontForge to read each NotoSans*-Regular.ttf and export
glyph details for all 10 Indic script ranges to CSV files.

run with FontForge:
  fontforge -script pysk/notopy/extract_noto_data.py

output: pffsheets/noto_data/xh38.csv, xb38.csv, ... xs38.csv

then run part 2:
  python3 pysk/notopy/gen_noto_sheets.py
"""

import fontforge
import csv
import sys
import json
from pathlib import Path

pff_root  = Path(__file__).resolve().parents[2]
NOTO_DIR  = pff_root / "pysk/notopy"
NAMES_TXT = pff_root / "pysk/notopy/NamesList.txt"
JSON_PATH = pff_root / "sfdsrc/asc-to-utf.json"
OUT_DIR   = pff_root / "pffsheets/noto_data"

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
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    result = {}
    for offset_hex, row in data['rows'].items():
        for col_idx, ch in enumerate(row):
            result[(col_idx, int(offset_hex, 16))] = ch
    return result

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("reading NamesList.txt ...")
    nl_map = parse_nameslist(NAMES_TXT)
    print("reading asc-to-utf.json ...")
    json_map = load_json_map(JSON_PATH)

    for col_idx, (script, prefix, ttf_name, base) in enumerate(SCRIPTS):
        ttf_path = NOTO_DIR / ttf_name
        out_csv  = OUT_DIR / f"{prefix}.csv"

        if not ttf_path.exists():
            print(f"  SKIP {ttf_name} (not found)")
            continue

        print(f"[{col_idx+1}/10] {prefix} {script} -> {out_csv.name}")
        noto = fontforge.open(str(ttf_path))

        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(["hex","nameslist","hskii","width","has_glyph","in_json"])
            for offset in range(0x80):
                cp = base + offset
                try:
                    g         = noto[cp]
                    width     = g.width
                    has_glyph = "Y" if g.isWorthOutputting() else "N"
                except Exception:
                    width     = 0
                    has_glyph = "N"
                nl_raw, nl_hskii = nl_map.get(cp, ("-", "clear"))
                in_json = json_map.get((col_idx, offset), "clear")
                w.writerow([f"{cp:04X}", nl_raw, nl_hskii, width, has_glyph, in_json])

        noto.close()
        print(f"  written {out_csv}")

    print(f"\nDone! CSVs in {OUT_DIR}")
    print("Now run: python3 pysk/notopy/gen_noto_sheets.py")

if __name__ == "__main__":
    main()
