#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-
"""
prep_utf.py  —  Pipeline 2: UTF preparation

Steps:
  3.1.1  sfdsrc/xi38/*.sfd  ->  sfd/xi38sfd/xi38asc/   (copy, overwrite)
  3.1.2  sfdsrc/xi52/*.sfd  ->  sfd/xi52sfd/xi52asc/   (copy, overwrite)
  3.1.3  clear sfd/xi38sfd/xi38utf/
  3.1.4  clear sfd/xi52sfd/xi52utf/
  3.1.5  sfdsrc/xi38/*asc.sfd -> sfd/xi38sfd/xi38utf/*utf.sfd (copy+rename)
  3.1.6  sfdsrc/xi52/*asc.sfd -> sfd/xi52sfd/xi52utf/*utf.sfd (copy+rename)
  3.1.7  update font metadata (fontname/familyname: asc->utf) in all utf SFDs
  3.1.8  add unicode glyph refs to xh38utf.sfd only
         (run copy_utf_unicode_blocks.py afterwards for rest)

run:
  fontforge -script pysk/xi52py/prep_utf.py

then:
  python3  pysk/xi52py/copy_utf_unicode_blocks.py
  fontforge -script pysk/xi52py/verify_utf.py
"""

import fontforge
import shutil
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

pff_root = Path(__file__).resolve().parents[2]

SFDSRC_38 = pff_root / "sfdsrc/xi38"
SFDSRC_52 = pff_root / "sfdsrc/xi52"
SFD_38ASC = pff_root / "sfd/xi38sfd/xi38asc"
SFD_52ASC = pff_root / "sfd/xi52sfd/xi52asc"
SFD_38UTF = pff_root / "sfd/xi38sfd/xi38utf"
SFD_52UTF = pff_root / "sfd/xi52sfd/xi52utf"
JSON_PATH = pff_root / "sfdsrc/asc-to-utf.json"
LOG_DIR   = pff_root / "logs"
LOG_FILE  = LOG_DIR  / "prep_utf.log"

SCRIPT_BASES = [0x0900, 0x0980, 0x0A00, 0x0A80, 0x0B00, 0x0B80, 0x0C00, 0x0C80, 0x0D00, 0x0D80]
SCRIPT_COLS  = ['900',  '980',  'A00',  'A80',  'B00',  'B80',  'C00',  'C80',  'D00',  'D80']

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


# ── helpers ──────────────────────────────────────────────────────────────────

def _copy_dir(src_dir, dst_dir, label):
    """Copy all *.sfd from src_dir to dst_dir (overwrite)."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sfd in sorted(src_dir.glob("*.sfd")):
        shutil.copy2(sfd, dst_dir / sfd.name)
        count += 1
    log.info(f"[{label}] {count} SFDs copied from {src_dir.name}/")
    return count


def _clear_dir(dst_dir, label):
    """Remove all *.sfd files from dst_dir."""
    removed = 0
    if dst_dir.exists():
        for f in dst_dir.glob("*.sfd"):
            f.unlink()
            removed += 1
    log.info(f"[{label}] cleared {removed} SFDs")


def _copy_rename_asc_to_utf(src_dir, dst_dir, label):
    """
    Copy sfdsrc/*.sfd to dst_dir, renaming *asc.sfd -> *utf.sfd.
    e.g.  xh38asc.sfd  ->  xh38utf.sfd
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sfd in sorted(src_dir.glob("*.sfd")):
        new_name = sfd.name.replace("asc", "utf")
        shutil.copy2(sfd, dst_dir / new_name)
        count += 1
    log.info(f"[{label}] {count} SFDs copied+renamed from sfdsrc")
    return count


# ── pipeline steps ────────────────────────────────────────────────────────────

def step_copy_to_asc():
    """3.1.1 + 3.1.2 — sfdsrc -> xi38asc / xi52asc"""
    _copy_dir(SFDSRC_38, SFD_38ASC, "xi38asc")
    _copy_dir(SFDSRC_52, SFD_52ASC, "xi52asc")


def step_build_utf_dirs():
    """3.1.3 to 3.1.6 — clear utf dirs, copy+rename from sfdsrc"""
    _clear_dir(SFD_38UTF, "xi38utf")
    _clear_dir(SFD_52UTF, "xi52utf")
    _copy_rename_asc_to_utf(SFDSRC_38, SFD_38UTF, "xi38utf")
    _copy_rename_asc_to_utf(SFDSRC_52, SFD_52UTF, "xi52utf")


def step_update_metadata():
    """3.1.7 — update fontname/familyname: 'asc' -> 'utf' in all utf SFDs"""
    for utf_dir, label in [(SFD_38UTF, "xi38utf"), (SFD_52UTF, "xi52utf")]:
        count = 0
        for sfd_path in sorted(utf_dir.glob("*utf.sfd")):
            try:
                f = fontforge.open(str(sfd_path))
                for attr in ("fontname", "familyname", "fullname"):
                    val = getattr(f, attr, "") or ""
                    new_val = val.replace("asc", "utf").replace("Asc", "Utf")
                    if new_val != val:
                        setattr(f, attr, new_val)
                f.save(str(sfd_path))
                f.close()
                count += 1
            except Exception as e:
                log.warning(f"  [{label}] {sfd_path.name} meta: {e}")
        log.info(f"[{label}] metadata updated in {count} SFDs")


def step_add_unicode_refs():
    """3.1.8 — add unicode glyph refs to xh38utf.sfd (all 10 script ranges)"""
    if not JSON_PATH.exists():
        log.error(f"asc-to-utf.json not found: {JSON_PATH}")
        return 0

    with open(JSON_PATH, encoding="utf-8") as jf:
        data = json.load(jf)
    rows = data["rows"]     # {"00":[char,...], "01":[...], ...}

    xh38utf = SFD_38UTF / "xh38utf.sfd"
    if not xh38utf.exists():
        log.error(f"xh38utf.sfd not found: {xh38utf}")
        return 0

    f = fontforge.open(str(xh38utf))
    total = 0

    for col_idx, (col, base) in enumerate(zip(SCRIPT_COLS, SCRIPT_BASES)):
        added = 0
        for offset_hex, row in rows.items():
            if col_idx >= len(row):
                continue
            ascii_char = row[col_idx]
            if not ascii_char or ascii_char == "clear":
                continue

            dst_cp  = base + int(offset_hex, 16)
            src_cp  = ord(ascii_char)

            try:
                src_g = f[src_cp]
                dst_g = f.createChar(dst_cp)
                dst_g.clear()
                dst_g.addReference(src_g.glyphname, (1, 0, 0, 1, 0, 0))
                dst_g.width = src_g.width
                added += 1
            except Exception as e:
                log.warning(f"  U+{dst_cp:04X} <- '{ascii_char}': {e}")

        log.info(f"  U+{base:04X} ({col}): {added} refs added")
        total += added

    f.save(str(xh38utf))
    f.close()
    log.info(f"[xh38utf] total {total} unicode refs — saved")
    return total


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 60)
    log.info(f"prep_utf  started {datetime.now()}")

    log.info("\n--- 3.1.1+3.1.2  copy sfdsrc -> xi38asc / xi52asc ---")
    step_copy_to_asc()

    log.info("\n--- 3.1.3-3.1.6  clear utf dirs + copy+rename from sfdsrc ---")
    step_build_utf_dirs()

    log.info("\n--- 3.1.7  update utf font metadata ---")
    step_update_metadata()

    log.info("\n--- 3.1.8  add unicode refs -> xh38utf.sfd ---")
    step_add_unicode_refs()

    log.info("\n" + "=" * 60)
    log.info("done. next steps:")
    log.info("  1. check xh38utf.sfd in FontForge (U+0915 etc.)")
    log.info("  2. python3 pysk/xi52py/copy_utf_unicode_blocks.py")
    log.info("  3. fontforge -script pysk/xi52py/verify_utf.py")
    print(f"\nDone! Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
