#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-
"""
noto_copy.py

Copy glyphs into notosfd/xi38/*asc.sfd and notosfd/xi52/*asc.sfd.

Two CSV files control what gets copied:
  pysk/notopy/noto_map_38.csv -> xi38 series
  pysk/notopy/noto_map_52.csv -> xi52 series

CSV structure:
  row 1 (header)  : ascii, xh38, xb38, ... xs38
  row 2 (src-sfd) : [ignore chars], xe38asc, xe38asc, ...
  row 3+ (data)   : A, 0905, 0985, ...

row 2 "src-sfd" row:
  col 0 : chars in [brackets] that are copied from the src SFD, not NotoSans
  col 1+: source SFD filename (same for all cols, e.g. xe38asc)
  -> copy those chars' glyphs from xe38asc.sfd into each destination font

data rows:
  col 0 : ASCII char (slot in destination xi38asc.sfd)
  col 1+: hex Unicode codepoint in NotoSans TTF for that script
  -> copy glyph from NotoSans TTF to that ASCII slot

run:
  fontforge -script pysk/notopy/noto_copy.py          (both series)
  fontforge -script pysk/notopy/noto_copy.py xi38     (xi38 only)
  fontforge -script pysk/notopy/noto_copy.py xi52     (xi52 only)
  fontforge -script pysk/notopy/noto_copy.py xh38     (one font)
"""

import fontforge
import csv
import sys
import logging
from pathlib import Path
from datetime import datetime

pff_root = Path(__file__).resolve().parents[2]
NOTO_DIR = pff_root / "pysk/notopy"
LOG_DIR  = pff_root / "logs"
LOG_FILE = LOG_DIR  / "noto_copy.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# NotoSans TTF for each script (shared by xi38 and xi52)
NOTO_TTF = {
    "xh": "NotoSansDevanagari-Regular.ttf",
    "xb": "NotoSansBengali-Regular.ttf",
    "xp": "NotoSansGurmukhi-Regular.ttf",
    "xg": "NotoSansGujarati-Regular.ttf",
    "xo": "NotoSansOriya-Regular.ttf",
    "xt": "NotoSansTamil-Regular.ttf",
    "xj": "NotoSansTelugu-Regular.ttf",
    "xk": "NotoSansKannada-Regular.ttf",
    "xm": "NotoSansMalayalam-Regular.ttf",
    "xs": "NotoSansSinhala-Regular.ttf",
}

# series config
SERIES = {
    "xi38": {
        "csv"    : pff_root / "pysk/notopy/noto_map_38.csv",
        "sfd_dir": pff_root / "notosfd/xi38",
    },
    "xi52": {
        "csv"    : pff_root / "pysk/notopy/noto_map_52.csv",
        "sfd_dir": pff_root / "notosfd/xi52",
    },
}


def parse_ignore_chars(cell):
    """Parse '[aieuoh LYVWPF ...]' -> set of single chars."""
    cell = cell.strip().strip("[]")
    chars = set()
    for group in cell.split():
        for ch in group:
            chars.add(ch)
    return chars


def read_csv(path):
    """
    Returns:
      font_cols   : list of font prefixes  e.g. ['xh38','xb38',...]
      src_sfd     : SFD filename for ignore-row chars  e.g. 'xe38asc'
      ignore_chars: set of ASCII chars to copy from src_sfd
      glyph_rows  : list of (ascii_char, {font_prefix: unicode_int})
    """
    font_cols    = []
    src_sfd      = None
    ignore_chars = set()
    glyph_rows   = []

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        # skip # comment lines, find header
        for row in reader:
            if not row or row[0].strip().startswith("#"):
                continue
            font_cols = [c.strip() for c in row[1:]]
            break

        # src-sfd row (previously "ignore" row)
        for row in reader:
            if not row or row[0].strip().startswith("#"):
                continue
            ignore_chars = parse_ignore_chars(row[0])
            # src SFD name from first non-empty value cell
            for cell in row[1:]:
                cell = cell.strip()
                if cell and cell.lower() != "ignore":
                    src_sfd = cell          # e.g. "xe38asc"
                    break
            break

        # data rows
        for row in reader:
            if not row or not row[0].strip() or row[0].strip().startswith("#"):
                continue
            ascii_char = row[0].strip()
            col_map = {}
            for i, font in enumerate(font_cols):
                cell = row[i + 1].strip() if i + 1 < len(row) else ""
                if cell and cell.lower() not in ("", "ignore", "skip"):
                    try:
                        col_map[font] = int(cell, 16)    # unicode codepoint
                    except ValueError:
                        col_map[font] = cell              # SFD source name e.g. 'xe38asc'
                        log.info(f"  sfd-source '{cell}' char '{ascii_char}' col '{font}'")
            glyph_rows.append((ascii_char, col_map))

    return font_cols, src_sfd, ignore_chars, glyph_rows


def copy_from_sfd(src_font, dst_font, chars, label=""):
    """Copy glyphs for each ASCII char from src_font to dst_font.

    No content check — user-edited glyphs are trusted to be valid.
    fontforge.glyph does not support len(), so we skip that check entirely.
    """
    copied = failed = 0
    for ch in sorted(chars):
        cp = ord(ch)
        try:
            src_font.selection.select(cp)
            src_font.copy()
            dst_font.selection.select(cp)
            dst_font.paste()
            dst_font[cp].width = src_font[cp].width
            copied += 1
            log.debug(f"  {label} sfd-copy '{ch}' U+{cp:04X} ok")
        except Exception as e:
            log.warning(f"  {label} sfd-copy '{ch}' U+{cp:04X}: {e}")
            failed += 1
    return copied, failed


def copy_from_ttf(src_font, dst_font, src_cp, dst_ch, label=""):
    """Copy one glyph from NotoSans TTF (src_cp) to ASCII slot (dst_ch)."""
    try:
        src_g = src_font[src_cp]
        if not src_g.isWorthOutputting():
            return False
        src_font.selection.select(src_cp)
        src_font.copy()
        dst_cp = ord(dst_ch)
        dst_font.selection.select(dst_cp)
        dst_font.paste()
        dst_font[dst_cp].width = src_g.width
        return True
    except Exception as e:
        log.warning(f"  {label} ttf-copy '{dst_ch}' U+{src_cp:04X}: {e}")
        return False


def process_series(series_name, cfg, wanted_fonts):
    csv_path = cfg["csv"]
    sfd_dir  = cfg["sfd_dir"]

    if not csv_path.exists():
        log.error(f"[{series_name}] CSV not found: {csv_path}")
        return

    log.info(f"[{series_name}] reading {csv_path.name}")
    font_cols, src_sfd_name, ignore_chars, glyph_rows = read_csv(csv_path)
    log.info(f"  fonts: {font_cols}")
    log.info(f"  src_sfd: {src_sfd_name}  ignore chars({len(ignore_chars)}): {''.join(sorted(ignore_chars))}")
    log.info(f"  glyph rows: {len(glyph_rows)}")

    # open source SFD for ignore chars (merged into sfd_cache to avoid double-open)
    src_sfd_font = None
    if src_sfd_name:
        src_sfd_path = sfd_dir / f"{src_sfd_name}.sfd"
        if src_sfd_path.exists():
            if src_sfd_name not in sfd_cache:
                log.info(f"  opening src SFD: {src_sfd_path.name}")
                sfd_cache[src_sfd_name] = fontforge.open(str(src_sfd_path))
            src_sfd_font = sfd_cache[src_sfd_name]
        else:
            log.warning(f"  src SFD not found: {src_sfd_path}")

    # open NotoSans TTFs (lazy, cache by prefix)
    noto_cache = {}     # ttf filename -> fontforge.font
    sfd_cache   = {}     # sfd stem -> fontforge.font (ignore-row + data-row sfd sources)

    total_copied = total_failed = 0

    for font_col in font_cols:
        if wanted_fonts and font_col not in wanted_fonts:
            continue

        sfd_path = sfd_dir / f"{font_col}asc.sfd"
        if not sfd_path.exists():
            log.warning(f"  [{font_col}] SFD not found: {sfd_path}, skipping")
            continue

        log.info(f"\n  [{font_col}] -> {sfd_path.name}")
        dst = fontforge.open(str(sfd_path))

        copied = skipped = failed = 0

        # step 1: copy ignore chars from src SFD
        if src_sfd_font and ignore_chars:
            c, f = copy_from_sfd(src_sfd_font, dst, ignore_chars, label=font_col)
            copied += c; failed += f
            log.info(f"    sfd-copy: {c} copied, {f} failed")

        # step 2: copy noto glyphs from TTF
        prefix = font_col[:2]   # "xh", "xb", etc.
        ttf_name = NOTO_TTF.get(prefix)
        if not ttf_name:
            log.warning(f"    no TTF mapping for prefix '{prefix}'")
        else:
            ttf_path = NOTO_DIR / ttf_name
            if not ttf_path.exists():
                log.warning(f"    TTF not found: {ttf_path}")
            else:
                if ttf_name not in noto_cache:
                    log.info(f"    opening {ttf_name}")
                    noto_cache[ttf_name] = fontforge.open(str(ttf_path))
                noto = noto_cache[ttf_name]

                for ascii_char, col_map in glyph_rows:
                    if font_col not in col_map:
                        skipped += 1
                        continue
                    val = col_map[font_col]
                    if isinstance(val, str):
                        # SFD source name in data row (e.g. 'xe38asc')
                        sfd_src_path = sfd_dir / f"{val}.sfd"
                        if not sfd_src_path.exists():
                            log.warning(f"  [{font_col}] sfd-source '{val}' not found for '{ascii_char}'")
                            failed += 1
                        else:
                            if val not in sfd_cache:
                                log.info(f"  opening sfd-source: {val}.sfd")
                                sfd_cache[val] = fontforge.open(str(sfd_src_path))
                            src_sfd = sfd_cache[val]
                            cp = ord(ascii_char)
                            try:
                                src_sfd.selection.select(cp)
                                src_sfd.copy()
                                dst.selection.select(cp)
                                dst.paste()
                                dst[cp].width = src_sfd[cp].width
                                copied += 1
                                log.debug(f"  [{font_col}] sfd-copy '{ascii_char}' from {val}")
                            except Exception as e:
                                log.warning(f"  [{font_col}] sfd-copy '{ascii_char}' from {val}: {e}")
                                failed += 1
                    else:
                        ok = copy_from_ttf(noto, dst, val, ascii_char, label=font_col)
                        if ok: copied += 1
                        else:  failed  += 1

        dst.save(str(sfd_path))
        dst.close()
        log.info(f"    saved  copied={copied} skipped={skipped} failed={failed}")
        total_copied += copied
        total_failed += failed

    # close cached fonts
    for f in noto_cache.values():
        f.close()
    for f in sfd_cache.values():
        f.close()
    # src_sfd_font is in sfd_cache, closed above

    return total_copied, total_failed


def main():
    log.info("=" * 60)
    log.info(f"noto_copy  started {datetime.now()}")

    # CLI args: series names (xi38/xi52) or font prefixes (xh38/xh52/...)
    args = set(sys.argv[1:])
    wanted_series = set()
    wanted_fonts  = set()
    for a in args:
        if a in SERIES:
            wanted_series.add(a)
        else:
            wanted_fonts.add(a)
            # infer series from font name
            if "38" in a:
                wanted_series.add("xi38")
            elif "52" in a:
                wanted_series.add("xi52")
    if not wanted_series:
        wanted_series = set(SERIES.keys())   # default: both

    log.info(f"series: {sorted(wanted_series)}  font filter: {sorted(wanted_fonts) or 'all'}")

    grand_copied = grand_failed = 0
    for sname in sorted(wanted_series):
        c, f = process_series(sname, SERIES[sname], wanted_fonts or None)
        grand_copied += c
        grand_failed += f

    log.info("=" * 60)
    log.info(f"done  total copied={grand_copied}  failed={grand_failed}")
    print(f"\nDone! Logs: {LOG_FILE}")
    if grand_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
