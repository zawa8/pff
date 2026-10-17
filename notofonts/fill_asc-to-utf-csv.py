#!/usr/bin/env python3
"""
fill_asc-to-utf-csv.py

Regenerates sfdsrc/asc-to-utf-generated.csv from local Noto fonts.

Refcopy decision priority (per cell):
  1. manual #NN hint:
       'empty'  -> 'clear'
       <letter> -> that letter
  2. glyph absent -> 'clear'
  3. auto:
       a) explicit exception table:
          pha->f, dha->q, ddha->Q, ja->z, jha->Z, nya->N, ttha->J,
          ta->T, tha->j, da->D, va->w, ha->H
       b) first char of the Unicode short name, uppercased if 'h' appears
          after the first char (ka->k, kha->K, ga->g, gha->G, sha->S)
  4. fallback -> '?'
"""

import csv
import os
import sys
import tempfile
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH   = os.path.join(SCRIPT_DIR, "..", "sfdsrc", "asc-to-utf-generated.csv")
NAMESLIST  = os.path.join(SCRIPT_DIR, "NamesList.txt")

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
    "# auto-hint format:  # <cp>=<short> | <cp>=<short> | ...  (one entry per column)",
    "# auto refcopy: first char of short name, uppercased if 'h' appears after "
    "the first char. Exceptions: pha->f, dha->q, ddha->Q, ja->z, jha->Z, "
    "nya->N, ttha->J, ta->T, tha->j, da->D, va->w, ha->H.",
]

REFCOPY_LETTERS = set("0123456789ADHTKGCZNRBSabcdefghijklmnopqrstuwyz")

# Explicit overrides that win before the generic first-char / -h- rules.
AUTO_REFCOPY_EXCEPTIONS = {
    "pha":  "f",
    "dha":  "q",
    "ddha": "Q",
    "ja":   "z",
    "jha":  "Z",
    "nya":  "N",
    "ttha": "J",
    "ta":   "T",
    "tha":  "j",
    "da":   "D",
    "va":   "w",
    "ha":   "H",
}


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
            if line[0] not in ("\t", "@", ";", "#") and "\t" in line:
                head = line.split("\t", 1)[0]
                try:
                    cur_cp = int(head, 16)
                except ValueError:
                    cur_cp = None
                continue
            if cur_cp is not None and line.startswith("\t= "):
                alias = line[3:].strip()
                if alias and not alias.startswith("<"):
                    short = alias.split()[-1].lower()
                    aliases.setdefault(cur_cp, short)
    print(f"# Loaded {len(aliases)} alias(es) from {os.path.basename(path)}",
          file=sys.stderr)
    return aliases


def short_name(cp, unicode_name, aliases):
    if cp in aliases:
        return aliases[cp]
    if not unicode_name or unicode_name == "<unnamed>":
        return "?"
    return unicode_name.split()[-1].lower()


def scan_fonts(aliases):
    import fontforge
    present = {col: {} for col in FONTS}
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


def auto_refcopy_letter(short):
    """
    Derive refcopy letter from a short name.
      1. explicit exception table wins
         (pha->f, dha->q, ddha->Q, ja->z, jha->Z, nya->N, ttha->J,
          ta->T, tha->j, da->D, va->w, ha->H)
      2. first char must be a valid refcopy letter
      3. uppercase if 'h' appears after the first char
      4. otherwise lowercase
    """
    if not short:
        return None
    short = short.lower()
    if short in AUTO_REFCOPY_EXCEPTIONS:
        return AUTO_REFCOPY_EXCEPTIONS[short]
    first = short[0]
    if first not in REFCOPY_LETTERS:
        return None
    if 'h' in short[1:]:
        upper = first.upper()
        if upper in REFCOPY_LETTERS:
            return upper
    return first


def cell_value(col_idx, present_entry, hint_fields):
    raw = hint_fields[col_idx] if hint_fields is not None else None

    if raw is not None and raw.strip() == "empty":
        return "clear"

    hint = _normalize_hint(raw)
    if hint is not None:
        return hint

    if present_entry is None:
        return "clear"

    _cp, _name, short = present_entry
    auto = auto_refcopy_letter(short)
    if auto is not None:
        return auto

    return "?"


def auto_hint_line(off, present, hint_fields):
    parts = []
    for idx, col in enumerate(FONTS):
        raw = hint_fields[idx] if hint_fields is not None else None
        u = BLOCK_STARTS[col] + off

        if raw is not None and raw.strip() == "empty":
            parts.append(f"{u:04X}=empty")
            continue

        if off in present[col]:
            _cp, _name, short = present[col][off]
            parts.append(f"{u:04X}={short}")

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
            for c in HEADER_COMMENTS:
                f.write(c + "\n")
            f.write(",".join(COLUMNS) + "\n")

            for off in range(0x80):
                manual = hints.get(off)
                auto   = auto_hint_line(off, present, manual)

                if manual is not None:
                    f.write(f"#{off:02X}," + ",".join(manual) + "\n")
                if auto is not None:
                    f.write(auto + "\n")

                row = [f"{off:02X}"]
                for idx, col in enumerate(FONTS):
                    row.append(cell_value(idx, present[col].get(off), manual))
                f.write(",".join(row) + "\n")

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