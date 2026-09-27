#!/usr/bin/env python3
"""
update_font_metadata.py

Stamp every built .sfd with Google Fonts / Microsoft submission metadata:
  - FontName, FullName, FamilyName (hybrid: technical PS name,
    human-readable family/full name)
  - Version, Copyright, License, License URL, UniqueID (sfnt)
  - PS UniqueID (numeric) = 0 (safe for modern workflows)

Naming:
    filename stem -> (Family, Fullname, PS name)
    xh38asc       -> (Xnglo Hindi xi38 asc, ... Regular, XngloHindi-xi38asc)
    xh52utf       -> (Xnglo Hindi xi52 utf, ... Regular, XngloHindi-xi52utf)
    xh52mono      -> (Xnglo Hindi xi52 mono, ... Regular, XngloHindi-xi52mono)
    xbinaryheks   -> (Xnglo Binary Hex, ... Regular, XngloBinary-Hex)
    xnglosoftw8utf-> (skipped, special case)

Version comes from the latest git tag (v1.2.0 -> "Version 1.2.0");
falls back to "Version 1.000" if git is unavailable.

Run via main.py (step 10, phase `meta`):
    fontforge -script scripts/xi52py/main.py --phase meta

Or standalone:
    fontforge -script scripts/xi52py/update_font_metadata.py
"""

import logging
import re
import subprocess
import sys
from pathlib import Path

import fontforge

# --------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------

script_dir = Path(__file__).resolve().parent
pff_root = script_dir.parent.parent
log_dir = pff_root / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "update_font_metadata.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

# --------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------

VENDOR = "zawa8"
COPYRIGHT = (
    "Copyright 2025 The Xnglo Project Authors "
    "(https://github.com/zawa8/pff)"
)
LICENSE_STR = (
    "This Font Software is licensed under the SIL Open Font License, "
    "Version 1.1."
)
LICENSE_URL = "https://openfontlicense.org"

# Script code -> human-readable name (used in Family / Fullname)
SCRIPT_NAMES = {
    "xh": "Hindi",
    "xb": "Bengali",
    "xp": "Punjabi",
    "xg": "Gujarati",
    "xo": "Oriya",
    "xt": "Tamil",
    "xj": "Telugu",
    "xk": "Kannada",
    "xm": "Malayalam",
    "xs": "Sinhala",
    "xe": "English",
}

# Directories whose .sfd files get metadata stamped.
# xi38mono does not exist yet (skip).
SFD_DIRS = [
    pff_root / "sfd/xi52sfd/xi52asc",
    pff_root / "sfd/xi38sfd/xi38asc",
    pff_root / "sfd/xi52sfd/xi52utf",
    pff_root / "sfd/xi38sfd/xi38utf",
    pff_root / "sfd/xi52sfd/xi52mono",
]

# Files to leave alone (special cases, pending rename, or not in our scheme).
SKIP = {
    "koreanonlyw8asc.sfd",
    "russianonlyw8asc.sfd",
    "xnglosoftw8utf.sfd",
    "xnglosoftw8mono.sfd",
}

# --------------------------------------------------------------------------
# version
# --------------------------------------------------------------------------

def get_version() -> str:
    """Read latest git tag and format it as 'Version X.Y.Z'."""
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=str(pff_root),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception as e:
        logging.warning("git describe failed (%s); using fallback version", e)
        return "Version 1.000"

    if not tag:
        return "Version 1.000"

    # v1.2.0 -> 1.2.0
    tag = tag.lstrip("v")
    return f"Version {tag}"


# --------------------------------------------------------------------------
# naming
# --------------------------------------------------------------------------

def parse_stem(stem: str) -> tuple[str, str, str]:
    """
    Map a filename stem to (Family, Fullname, PostScriptName).

    Special cases:
        xbinaryheks  -> (Xnglo Binary Hex, ... Regular, XngloBinary-Hex)

    Regular pattern:
        <xx><38|52><asc|utf|mono>
        where <xx> is a two-letter script code (xh, xb, ...).

    Returns:
        family, fullname, ps_name
    """
    if stem == "xbinaryheks":
        return (
            "Xnglo Binary Hex",
            "Xnglo Binary Hex Regular",
            "XngloBinary-Hex",
        )

    m = re.match(r"^(x[a-z]+)(38|52)(asc|utf|mono)$", stem)
    if not m:
        # unknown pattern: fall back to technical name for everything
        logging.warning("unknown filename pattern: %s (using stem as name)", stem)
        return (stem, stem, stem)

    code, size, variant = m.group(1), m.group(2), m.group(3)
    script = SCRIPT_NAMES.get(code)
    if script is None:
        logging.warning("unknown script code '%s' in %s", code, stem)
        return (stem, stem, stem)

    family = f"Xnglo {script} xi{size} {variant}"
    fullname = f"{family} Regular"
    # PostScript names must not contain spaces.
    ps_name = f"Xnglo{script}-xi{size}{variant}"
    return family, fullname, ps_name


# --------------------------------------------------------------------------
# sfnt name helper
# --------------------------------------------------------------------------

def set_sfnt_name(font, name_id: str, value: str) -> None:
    """Replace or add an English (US) sfnt name entry."""
    names = [
        n for n in font.sfnt_names
        if not (n[0] == "English (US)" and n[1] == name_id)
    ]
    names.append(("English (US)", name_id, value))
    font.sfnt_names = names


# --------------------------------------------------------------------------
# per-file update
# --------------------------------------------------------------------------

def update_metadata(sfd_path: Path, version: str) -> None:
    stem = sfd_path.stem
    family, fullname, ps_name = parse_stem(stem)

    logging.info("%s -> family='%s' ps='%s'", sfd_path.name, family, ps_name)

    font = fontforge.open(str(sfd_path))

    # PS-level / font-level fields
    font.familyname = family
    font.fullname = fullname
    font.fontname = ps_name
    font.version = version
    # PS numeric UniqueID: 0 is safe for modern workflows (Google/Microsoft).
    font.uniqueid = 0

    # SFNT (TTF names) fields
    set_sfnt_name(font, "Family", family)
    set_sfnt_name(font, "Fullname", fullname)
    set_sfnt_name(font, "PostScriptName", ps_name)
    set_sfnt_name(font, "UniqueID", f"{version}; {VENDOR}; {ps_name}")
    set_sfnt_name(font, "Version", version)
    set_sfnt_name(font, "Copyright", COPYRIGHT)
    set_sfnt_name(font, "License", LICENSE_STR)
    set_sfnt_name(font, "License URL", LICENSE_URL)

    font.save(str(sfd_path))
    font.close()


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> None:
    version = get_version()
    logging.info("using %s", version)

    failed = 0
    processed = 0

    for sfd_dir in SFD_DIRS:
        if not sfd_dir.exists():
            logging.warning("skip (missing dir): %s", sfd_dir)
            continue

        for sfd_path in sorted(sfd_dir.glob("*.sfd")):
            if sfd_path.name in SKIP:
                logging.info("skip (SKIP set): %s", sfd_path.name)
                continue

            try:
                update_metadata(sfd_path, version)
                processed += 1
            except Exception as e:
                failed += 1
                logging.error("failed: %s: %s", sfd_path.name, e)

    logging.info("done: %d processed, %d failed", processed, failed)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()