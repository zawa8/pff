"""
gen_asc_to_utf.py

Generate asc-to-utf.csv from Noto fonts.
Maps Latin ASCII to Indic unicode ranges (per script).
"""

import fontforge
from pathlib import Path

pff_root = Path.home() / "pff"
noto_dir = pff_root / "notofonts"
output_csv = pff_root / "sfdsrc" / "asc-to-utf.csv"

SCRIPTS = [
    ('900', 0x0900, 'NotoSansDevanagari-Regular.ttf'),
    ('980', 0x0980, 'NotoSansBengali-Regular.ttf'),
    ('A00', 0x0A00, 'NotoSansGurmukhi-Regular.ttf'),
    ('A80', 0x0A80, 'NotoSansGujarati-Regular.ttf'),
    ('B00', 0x0B00, 'NotoSansOriya-Regular.ttf'),
    ('B80', 0x0B80, 'NotoSansTamil-Regular.ttf'),
    ('C00', 0x0C00, 'NotoSansTelugu-Regular.ttf'),
    ('C80', 0x0C80, 'NotoSansKannada-Regular.ttf'),
    ('D00', 0x0D00, 'NotoSansMalayalam-Regular.ttf'),
    ('D80', 0x0D80, 'NotoSansSinhala-Regular.ttf'),
]

fonts = {}
for col, base, noto_file in SCRIPTS:
    path = noto_dir / noto_file
    if path.exists():
        try:
            fonts[col] = fontforge.open(str(path))
        except Exception as e:
            print(f"ERROR opening {noto_file}: {e}")
    else:
        print(f"NOT FOUND: {path}")

lines = []
lines.append("# asc-to-utf.csv")
lines.append("# Maps Latin ASCII to Indic unicode ranges (per script)")
lines.append("# Format: offset, 900, 980, A00, A80, B00, B80, C00, C80, D00, D80")
lines.append("# Value: clear = clear, <latin><indic> = refcopy")
lines.append("offset,900,980,A00,A80,B00,B80,C00,C80,D00,D80")

for offset in range(128):
    row = [f"{offset:02X}"]
    for col, base, noto_file in SCRIPTS:
        if col not in fonts:
            row.append("clear")
            continue
        f = fonts[col]
        cp = base + offset
        if cp in f:
            row.append("clear")  # Will refine later
        else:
            row.append("clear")
    lines.append(",".join(row))

with open(output_csv, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines) + "\n")

for f in fonts.values():
    f.close()

print(f"Generated: {output_csv}")
print(f"Rows: {len(lines) - 5}")
