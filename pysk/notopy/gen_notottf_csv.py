#!/usr/bin/env python3
"""
gen_notottf_csv.py
Generate notofonts/notottf-x38ascsfd.csv from notofonts/NamesList.txt.

The CSV maps each hskii ASCII glyph char to its Unicode codepoint
in each of 10 Indic script Noto fonts.

Purpose: build pipeline copies the right Noto TTF glyph into each
ASCII slot of each xi38asc.sfd font.

run:
  python3 pysk/xi52py/gen_notottf_csv.py
"""

import csv
from pathlib import Path
from collections import defaultdict

pff_root   = Path(__file__).resolve().parents[2]
NAMES_FILE = pff_root / "pysk/notopy/NamesList.txt"
CSV_OUT    = pff_root / "pysk/notopy/notottf-x38ascsfd.csv"

# Script ranges → font prefix (CSV column order)
SCRIPTS = [
    (0x0900, 0x097F, 'xh38'),  # Devanagari (Hindi)
    (0x0980, 0x09FF, 'xb38'),  # Bengali
    (0x0A00, 0x0A7F, 'xp38'),  # Gurmukhi (Punjabi)
    (0x0A80, 0x0AFF, 'xg38'),  # Gujarati
    (0x0B00, 0x0B7F, 'xo38'),  # Odia
    (0x0B80, 0x0BFF, 'xt38'),  # Tamil
    (0x0C00, 0x0C7F, 'xj38'),  # Telugu
    (0x0C80, 0x0CFF, 'xk38'),  # Kannada
    (0x0D00, 0x0D7F, 'xm38'),  # Malayalam
    (0x0D80, 0x0DFF, 'xs38'),  # Sinhala
]
FONT_COLS = [s[2] for s in SCRIPTS]

# NamesList phonetic value → hskii ASCII char
# None = skip (combining mark / not used as standalone glyph)
VALUE_TO_HSKII = {
    # multi-char phonetic forms
    'ga':'g', 'gha':'G', 'ca':'c', 'chha':'C',
    'nga':None, 'nha':None,
    'wa':'w', 'maa':'m', 'fa':'f',
    'aa':'a', 'ee':'e', 'ai':'e', 'au':'o',
    'aira':'A',                        # Punjabi short A
    'khha':'K', 'ghha':'G',
    'za':'z', 'yya':'y', 'zha':'z',
    'ttta':None, 'nnga':None, 'nndda':None, 'mba':None,
    'nyja':None, 'jnya':None, 'nda':None,
    'OE':None, 'OOE':None, 'AA':'a', 'AI':'e', 'AU':'o',
    'oe':None, 'ui':None, 'eei':None, 'uui':None,
    # combining/diacritic marks → skip
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
    'sukun':None,'shadda':None,'maddah':None,
    'dddha':None,'rha':None,
    # uppercase descriptive words → skip
    'SHORT':None,'ADAK':None,'LENGTH':None,'COMBINING':None,
    'CANDRA':None,'VOCALIC':None,'PRISHTHAMATRA':None,'AW':None,
    'ANUSVARA':None,'HIGH':None,
}

# Explicit CSV row order (hskii ASCII chars in xi38asc fonts)
CSV_CHARS = [
    # group: ignored matras / vowel-marks (document only, no Noto copy row)
    # 'a','i','e','u','o','h', 'L','Y','V','W','P','F','E','I','O','U','M','X','N','R'
    # group: standalone vowel
    'A',
    # group: velar stops
    'k','K','g','G',
    # group: palatal stops
    'c','C','z','Z',
    # group: retroflex stops
    't','J','d','Q',
    # group: dental stops
    'T','j','D','q',
    # group: nasal (merged)
    'n',
    # group: labial stops
    'p','f','b','B','m',
    # group: approximants
    'y','r','l','w',
    # group: sibilants + h
    's','S','H',
]

IGNORE_CHARS = 'aieuoh LYVWPF EIOUMX NR'


def parse_nameslist(path):
    """Return dict: hskii_char -> {font_prefix -> first_cp_hex}"""
    result = defaultdict(dict)
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line:
                continue
            hex_str, rest = line.split('-', 1)
            value = rest.split('#')[0].strip()
            if not value or value == '<reserved>':
                continue
            try:
                cp = int(hex_str, 16)
            except ValueError:
                continue

            # get hskii char
            if value in VALUE_TO_HSKII:
                hskii_char = VALUE_TO_HSKII[value]
            else:
                hskii_char = value[0]          # first char as fallback

            if not hskii_char:
                continue                        # None = skip

            # find script range
            for base, end, font in SCRIPTS:
                if base <= cp <= end:
                    if font not in result[hskii_char]:
                        result[hskii_char][font] = hex_str.upper()
                    break

    return result


def main():
    if not NAMES_FILE.exists():
        raise FileNotFoundError(f"not found: {NAMES_FILE}")

    mapping = parse_nameslist(NAMES_FILE)

    with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['ascii'] + FONT_COLS)
        w.writerow([f'[{IGNORE_CHARS}]'] + ['ignore'] * len(FONT_COLS))
        for char in CSV_CHARS:
            row = [char]
            for _, _, font in SCRIPTS:
                cp = mapping.get(char, {}).get(font, '')
                row.append(cp)
            w.writerow(row)

    print(f"wrote {CSV_OUT}")

    # preview
    with open(CSV_OUT, newline='', encoding='utf-8') as f:
        for i, r in enumerate(f):
            print(r.rstrip())
            if i >= 10:
                print('...')
                break


if __name__ == '__main__':
    main()
