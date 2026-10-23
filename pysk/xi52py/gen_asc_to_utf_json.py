#!/usr/bin/env python3
"""
gen_asc_to_utf_json.py
Generate sfdsrc/asc-to-utf.json from notofonts/NamesList.txt.

NamesList.txt format per line:
  XXXX-value
  XXXX-value#comment

value is the hskii glyph string. we take its first char as the src ascii glyph.
absent codepoint or <reserved> -> "clear".

run from repo root:
  python3 pysk/xi52py/gen_asc_to_utf_json.py
"""

import json
from pathlib import Path

pff_root   = Path(__file__).resolve().parents[2]
NAMES_FILE = pff_root / "notofonts/NamesList.txt"
JSON_OUT   = pff_root / "sfdsrc/asc-to-utf.json"

SCRIPT_BASES = [0x0900, 0x0980, 0x0A00, 0x0A80, 0x0B00, 0x0B80, 0x0C00, 0x0C80, 0x0D00, 0x0D80]
SCRIPT_COLS  = ['900',  '980',  'A00',  'A80',  'B00',  'B80',  'C00',  'C80',  'D00',  'D80']


def parse_nameslist(path):
    """Return dict: int_codepoint -> first_char_of_value."""
    mapping = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line:
                continue
            hex_str, rest = line.split('-', 1)
            rest = rest.split('#')[0].strip()       # strip comment
            if not rest or rest == '<reserved>':
                continue
            try:
                cp = int(hex_str, 16)
            except ValueError:
                continue
            mapping[cp] = rest[0]                   # first hskii char
    return mapping


def main():
    if not NAMES_FILE.exists():
        raise FileNotFoundError(f"not found: {NAMES_FILE}")

    mapping = parse_nameslist(NAMES_FILE)
    print(f"parsed {len(mapping)} entries from NamesList.txt")

    rows = {}
    for offset in range(0x80):
        row = []
        for base in SCRIPT_BASES:
            cp  = base + offset
            ch  = mapping.get(cp)
            row.append(ch if ch else 'clear')
        rows[f'{offset:02X}'] = row

    data = {
        "columns"     : ["offset"] + SCRIPT_COLS,
        "indikskripts": SCRIPT_COLS,
        "rows"        : rows,
    }

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"wrote {JSON_OUT}")


if __name__ == "__main__":
    main()
