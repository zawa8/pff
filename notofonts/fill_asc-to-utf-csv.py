#!/usr/bin/env python3
"""
fill_asc-to-utf-csv.py

Auto-hint format:  # 0914=AU | 0994=AU | ... | 0D9A=ka | ...
Short name priority:
  1. Unicode NamesList.txt alias  ("= sinhala letter ka" -> "ka")
  2. fallback: last word of Unicode name, lowercased
"""

import csv
import os
import sys
import tempfile
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH   = os.path.join(SCRIPT_DIR, "..", "sfdsrc", "asc-to-utf-generated.csv")
NAMESLIST  = os.path.join(SCRIPT_DIR, "NamesList.txt")   # download separately

FONTS = {
    "900": "NotoSansDevanagari-Regular.ttf",
    "980": "NotoSansBengali-Regular.ttf",
    "A00": "NotoSansGurmukhi-Regular.ttf",
    "A80": "NotoSansGujarati-Regular.ttf",
    "B00": "NotoSansOriya-Regular.ttf",
    "B80": "NotoSansTamil-Regular.ttf",
    "C00": "NotoSansTelugu-Regular.ttf",
    "C80": "NotoSansKannada-Regular.ttf",
    "D00": "NotoSansMalayalam-Regular.ttf",
    "D80": "NotoSansSinhala-Regular.ttf",
}
COLUMNS      = ["offset"] + list(FONTS.keys())
BLOCK_STARTS = {k: int(k, 16) for k in FONTS}

HEADER_COMMENTS = [
    "# asc-to-utf-generated.csv",
    "# Auto-generated from local Noto fonts via FontForge",
    "# glyphs of these chars can will be refcopied : "
    "0123456789 ADHT KGCZNRBS abcdefghijklmnopqrstuwyz",
    "# 'clear' = no glyph present, '?' = glyph present, refcopy not yet decided",
    "# 'empty' hint in a #NN line forces 'clear' regardless of glyph presence",
    "# auto-hint format:  # <cp>=<short> | <cp>=<short> | ...",
]

REFCOPY_LETTERS = set("0123456789ADHTKGCZNRBSabcdefghijklmnopqrstuwyz")


# --------------------------------------------------------------------------- #
# NamesList.txt parser -> {codepoint_int: short_alias_lowercase}
# --------------------------------------------------------------------------- #
def load_nameslist(path):
    aliases = {}
    if not os.path.exists(path):
        print(f"# WARNING: {path} not found; auto-hint falls back to last word",
              file=sys.stderr)
        return aliases
    cur_cp = None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            # Codepoint line: starts at col 0, hex digits, then tab
            if line[0] not in ("\t", "@", ";", "#") and "\t" in line:
                head = line.split("\t", 1)[0]
                try:
                    cur_cp = int(head, 16)
                except ValueError:
                    cur_cp = None
                continue
            # Alias line: starts with "= "
            if cur_cp is not None and line.startswith("\t= "):
                alias = line[3:].strip()
                if alias and not alias.startswith("<"):
                    # "sinhala letter ka" -> "ka"
                    short = alias.split()[-1].lower()
                    aliases.setdefault(cur_cp, short)
            # Skip cross-refs / refs, but keep scanning
    print(f"# Loaded {len(aliases)} alias(es) from {os.path.basename(path)}",
          file=sys.stderr)
    return aliases


# --------------------------------------------------------------------------- #
def short_name(cp, unicode_name, aliases):
    if cp in aliases:
        return aliases[cp]
    if not unicode_name or unicode_name == "<unnamed>":
        return "?"
    return unicode_name.split()[-1].lower()


def scan_fonts(aliases):
    import fontforge
    present = {col: {} for col in FONTS}     # col -> {offset: (cp, name, short)}
    for col, fname in FONTS.items():
        path = os.path.join(SCRIPT_DIR, fname)
        if not os.path.exists(path):
            print(f"# WARNING: missing {path} (column {col} -> all 'clear')",
                  file=sys.stderr)
            continue
        font = fontforge.open(path)
        base = BLOCK_STARTS[col]
        for glyph in font.glyphs():
            u = glyph.unicode
            if u != -1 and base <= u <= base + 0x7F:
                off = u - base
                name = unicodedata.name(chr(u), "<unnamed>")
                present[col][off] = (u, name, short_name(u, name, aliases))
        font.close()
        print(f"# {col}: {len(present[col])} glyphs found", file=sys.stderr)
    return present


def read_hints(path):
    hints = {}
    if not os.path.exists(path):
        return hints
    with open(path, "r", encoding="utf-8", newline="") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.startswith("#"):
                continue
            body = line.lstrip("#").lstrip()
            if body.startswith("auto-hint") or "," not in body:
                continue
            first, rest = body.split(",", 1)
            try:
                off = int(first, 16)
            except ValueError:
                continue
            if not (0 <= off <= 0x7F):
                continue
            fields = [x.strip() for x in rest.split(",")]
            fields = (fields + [""] * len(FONTS))[: len(FONTS)]
            hints[off] = fields
    return hints


def _normalize_hint(h):
    if h is None:
        return None
    h = h.strip()
    if h in ("", "?"):
        return None
    c = h[0]
    return c if c in REFCOPY_LETTERS else None


def cell_value(col_idx, present_col, hint_fields):
    raw = hint_fields[col_idx] if hint_fields is not None else None
    if raw is not None and raw.strip() == "empty":
        return "clear"
    hint = _normalize_hint(raw)
    if not present_col:
        return "clear"
    if hint is not None:
        return hint
    return "?"


def auto_hint_line(off, present):
    parts = []
    for col in FONTS:
        if off in present[col]:
            cp, _name, short = present[col][off]
            parts.append(f"{cp:04X}={short}")
    if not parts:
        return None
    return "# " + " | ".join(parts)


def write_csv(present, hints, out_path):
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".asc-to-utf-", suffix=".csv.tmp",
                                    dir=out_dir)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            for c in HEADER_COMMENTS:
                w.writerow([c])
            w.writerow(COLUMNS)
            for off in range(0x80):
                manual = hints.get(off)
                auto   = auto_hint_line(off, present)
                if manual is not None:
                    w.writerow([f"#{off:02X}," + ",".join(manual)])
                elif auto is not None:
                    w.writerow([auto])
                row = [f"{off:02X}"]
                for idx, col in enumerate(FONTS):
                    row.append(cell_value(idx, off in present[col], manual))
                w.writerow(row)
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    print(f"# Wrote {out_path}", file=sys.stderr)


def main():
    aliases = load_nameslist(NAMESLIST)
    present = scan_fonts(aliases)
    hints   = read_hints(OUT_PATH)
    if hints:
        print(f"# Read {len(hints)} manual hint line(s) from existing CSV",
              file=sys.stderr)
    write_csv(present, hints, OUT_PATH)


if __name__ == "__main__" or "fontforge" in sys.modules:
    main()