#!/usr/bin/env python3
"""
copy_utf_unicode_blocks.py

After build_utf_fonts.py has processed xh38utf.sfd (only),
extract all StartChar blocks for U+0900-U+0DFF from it
and copy them verbatim into every other *utf.sfd file.

This avoids running FontForge 10 more times for identical output.
Works because all xi38asc fonts share the same glyph names and
encoding slots, so Refer lines are identical across fonts.

run AFTER:
  fontforge -script pysk/xi52py/main.py --phase utf
  (with build_utf_fonts.py modified to process only xh38utf.sfd)

run:
  python3 pysk/xi52py/copy_utf_unicode_blocks.py
"""

import re
from pathlib import Path

pff_root = Path(__file__).resolve().parents[2]

# source: xh38utf.sfd (has unicode refs added by prep_utf.py)
SOURCE_DIR  = pff_root / "sfd/xi38sfd/xi38utf"
SOURCE_FONT = "xh38utf.sfd"

# destination fonts — xi38 series (same dir as source)
XI38_FONTS = [
    "xb38utf.sfd",
    "xg38utf.sfd",
    "xj38utf.sfd",
    "xk38utf.sfd",
    "xm38utf.sfd",
    "xo38utf.sfd",
    "xp38utf.sfd",
    "xs38utf.sfd",
    "xt38utf.sfd",
]

# destination fonts — xi52 series (different dir)
XI52_DIR   = pff_root / "sfd/xi52sfd/xi52utf"
XI52_FONTS = [
    "xh52utf.sfd",
    "xb52utf.sfd",
    "xg52utf.sfd",
    "xj52utf.sfd",
    "xk52utf.sfd",
    "xm52utf.sfd",
    "xo52utf.sfd",
    "xp52utf.sfd",
    "xs52utf.sfd",
    "xt52utf.sfd",
]

# Indic unicode range to copy (inclusive)
UNICODE_START = 0x0900
UNICODE_END   = 0x0DFF

# regex: one glyph block  StartChar...EndChar
_BLOCK_RE = re.compile(
    r'(StartChar: [^\n]+\n'
    r'Encoding: (\d+) \d+ \d+.*?'
    r'EndChar)',
    re.DOTALL,
)


def extract_unicode_blocks(text):
    """Return list of (codepoint, block_string) for Indic range."""
    blocks = []
    for m in _BLOCK_RE.finditer(text):
        enc = int(m.group(2))
        if UNICODE_START <= enc <= UNICODE_END:
            blocks.append((enc, m.group(1)))
    blocks.sort(key=lambda x: x[0])
    return blocks


def remove_unicode_blocks(text):
    """Remove existing Indic unicode blocks from SFD text."""
    def keep(m):
        enc = int(m.group(1))   # only 1 group in this pattern
        if UNICODE_START <= enc <= UNICODE_END:
            return ''
        return m.group(0)
    # pattern needs to match the full block including trailing newline
    pat = re.compile(
        r'StartChar: [^\n]+\n'
        r'Encoding: (\d+) \d+ \d+.*?'
        r'EndChar\n?',
        re.DOTALL,
    )
    return pat.sub(keep, text)


def update_beginchars(text, delta):
    """Increment/decrement the glyph count in BeginChars header line."""
    def replace(m):
        enc_size = m.group(1)
        count    = int(m.group(2)) + delta
        return f'BeginChars: {enc_size} {count}'
    return re.sub(r'BeginChars: (\d+) (\d+)', replace, text)


def patch_fonts(src_blocks, insert_text, font_list, font_dir):
    """Copy unicode blocks into each font in font_list inside font_dir."""
    for fname in font_list:
        fpath = font_dir / fname
        if not fpath.exists():
            print(f"  skip (not found): {fname}")
            continue
        text      = fpath.read_text(encoding='latin-1')
        old_blocks= extract_unicode_blocks(text)
        text2     = remove_unicode_blocks(text)
        delta     = len(src_blocks) - len(old_blocks)
        if 'EndChars' in text2:
            text2 = text2.replace('EndChars', insert_text + 'EndChars', 1)
        else:
            text2 = text2.rstrip('\n') + '\n' + insert_text + 'EndChars\n'
        text2 = update_beginchars(text2, delta)
        fpath.write_text(text2, encoding='latin-1')
        print(f"  {fname}: {len(old_blocks)} old -> {len(src_blocks)} new blocks  (BeginChars {delta:+d})")


def main():
    src_path = SOURCE_DIR / SOURCE_FONT
    if not src_path.exists():
        raise FileNotFoundError(f"source not found: {src_path}")

    src_text   = src_path.read_text(encoding='latin-1')
    src_blocks = extract_unicode_blocks(src_text)

    if not src_blocks:
        print(f"ERROR: no Indic unicode blocks found in {SOURCE_FONT}")
        print("  -> run prep_utf.py first")
        return

    print(f"{SOURCE_FONT}: {len(src_blocks)} unicode blocks "
          f"(U+{src_blocks[0][0]:04X} .. U+{src_blocks[-1][0]:04X})")
    insert_text = '\n'.join(b[1] for b in src_blocks) + '\n'

    print("\n--- xi38utf ---")
    patch_fonts(src_blocks, insert_text, XI38_FONTS, SOURCE_DIR)

    print("\n--- xi52utf ---")
    XI52_DIR.mkdir(parents=True, exist_ok=True)
    patch_fonts(src_blocks, insert_text, XI52_FONTS, XI52_DIR)

    print("\ndone.")


if __name__ == "__main__":
    main()
