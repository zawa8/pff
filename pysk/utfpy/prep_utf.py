#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-
"""
prep_utf.py  —  pipeline 2: utf preparation

Steps:
  3.1.1  sfdsrc/38asc/*.sfd  ->  sfd/38/asc/   (copy, overwrite)
  3.1.2  sfdsrc/52asc/*.sfd  ->  sfd/52/asc/   (copy, overwrite)
  3.1.3  clear sfd/38/utf/
  3.1.4  clear sfd/52/utf/
  3.1.5  sfdsrc/38asc/*asc.sfd -> sfd/38/utf/*utf.sfd (copy+rename)
  3.1.6  sfdsrc/52asc/*asc.sfd -> sfd/52/utf/*utf.sfd (copy+rename)
  3.1.7  update font metadata (fontname/familyname: asc->utf) in all utf SFDs
  3.1.8  add unicode glyph refs to xh38utf.sfd only
         (run copy_utf_unicode_blocks.py afterwards for rest)

run:
  fontforge -script pysk/utfpy/prep_utf.py

then:
  python3  pysk/utfpy/copy_utf_unicode_blocks.py
  fontforge -script pysk/utfpy/verify_utf.py
"""

import fontforge
import shutil
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

pff_root = Path(__file__).resolve().parents[2]

sfdsrc_38 = pff_root / "sfdsrc/38asc"
sfdsrc_52 = pff_root / "sfdsrc/52asc"
sfd_38asc = pff_root / "sfd/38/asc"
sfd_52asc = pff_root / "sfd/52/asc"
sfd_38utf = pff_root / "sfd/38/utf"
sfd_52utf = pff_root / "sfd/52/utf"
json_path = pff_root / "sfdsrc/asc-to-utf.json"
log_dir   = pff_root / "logs"
log_file  = log_dir  / "prep_utf.log"

skript_bases = [0x0900, 0x0980, 0x0A00, 0x0A80, 0x0B00, 0x0B80, 0x0C00, 0x0C80, 0x0D00, 0x0D80]
script_cols  = ['900',  '980',  'A00',  'A80',  'B00',  'B80',  'C00',  'C80',  'D00',  'D80']

log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ── helpers ──────────────────────────────────────────────────────────────────

def _copy_dir(src_dir, dst_dir, label):
    """kopy all *.sfd from src_dir to dst_dir (owerwrite)."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sfd in sorted(src_dir.glob("*.sfd")):
        shutil.copy2(sfd, dst_dir / sfd.name)
        count += 1
    log.info(f"[{label}] {count} sfds copied from {src_dir.name}/")
    return count


def _clear_dir(dst_dir, label):
    """rimuw aal *.sfd files from dst_dir."""
    rimuwd = 0
    if dst_dir.exists():
        for f in dst_dir.glob("*.sfd"):
            f.unlink()
            rimuwd += 1
    log.info(f"[{label}] kleared {rimuwd} sfds")


def _copy_rename_asc_to_utf(src_dir, dst_dir, label):
    """
    kopi sfdsrc/*.sfd to dst_dir, renaming *asc.sfd -> *utf.sfd.
    e.g.  xh38asc.sfd  ->  xh38utf.sfd
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sfd in sorted(src_dir.glob("*.sfd")):
        new_name = sfd.name.replace("asc", "utf")
        shutil.copy2(sfd, dst_dir / new_name)
        count += 1
    log.info(f"[{label}] {count} sfds copied+renamed from sfdsrc")
    return count


# ── pipeline steps ────────────────────────────────────────────────────────────

def step_copy_to_asc():
    """3.1.1 + 3.1.2 — sfdsrc -> 38asc / 52asc"""
    _copy_dir(sfdsrc_38, sfd_38asc, "38asc")
    _copy_dir(sfdsrc_52, sfd_52asc, "52asc")


def step_build_utf_dirs():
    """3.1.3 to 3.1.6 — clear utf dirs, copy+rename from sfdsrc"""
    _clear_dir(sfd_38utf, "38utf")
    _clear_dir(sfd_52utf, "52utf")
    _copy_rename_asc_to_utf(sfdsrc_38, sfd_38utf, "38utf")
    _copy_rename_asc_to_utf(sfdsrc_52, sfd_52utf, "52utf")


def step_update_metadata():
    """3.1.7 — update fontname/familyname: 'asc' -> 'utf' in all utf SFDs"""
    for utf_dir, label in [(sfd_38utf, "xi38utf"), (sfd_52utf, "xi52utf")]:
        count = 0
        for sfd_path in sorted(utf_dir.glob("*utf.sfd")):
            try:
                f = fontforge.open(str(sfd_path))
                # update fontname / familyname / fullname
                for attr in ("fontname", "familyname", "fullname"):
                    val = getattr(f, attr, "") or ""
                    new_val = val.replace("asc", "utf").replace("Asc", "Utf")
                    if new_val != val:
                        setattr(f, attr, new_val)
                # update sfnt name table (unique-id, version string, etc.)
                for lang, nid, val in list(f.sfnt_names):
                    if "asc" in val or "Asc" in val:
                        new_val = val.replace("asc", "utf").replace("Asc", "Utf")
                        f.appendSFNTName(lang, nid, new_val)
                f.save(str(sfd_path))
                f.close()
                count += 1
            except Exception as e:
                log.warning(f"  [{label}] {sfd_path.name} meta: {e}")
        log.info(f"[{label}] metadata updated in {count} SFDs")


def step_add_unicode_refs():
    """3.1.8 — add unicode glyph refs to xh38utf.sfd (all 10 script ranges)"""
    if not json_path.exists():
        log.error(f"asc-to-utf.json not found: {json_path}")
        return 0

    with open(json_path, encoding="utf-8") as jf:
        data = json.load(jf)
    rows = data["rows"]     # {"00":[char,...], "01":[...], ...}

    xh38utf = sfd_38utf / "xh38utf.sfd"
    if not xh38utf.exists():
        log.error(f"xh38utf.sfd not found: {xh38utf}")
        return 0

    f = fontforge.open(str(xh38utf))
    total = 0

    for col_idx, (col, base) in enumerate(zip(script_cols, skript_bases)):
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
    print(f"\nDone! Log: {log_file}")


if __name__ == "__main__":
    main()
