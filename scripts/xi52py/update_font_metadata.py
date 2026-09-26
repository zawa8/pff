#!/usr/bin/env python3
"""
update_font_metadata.py

Update font metadata for Google Fonts / Microsoft submission.
"""

import fontforge
import sys
from pathlib import Path

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent

# Constants
VERSION = "Version 1.000"
VENDOR = "zawa"
COPYRIGHT = "Copyright 2025 The Xnglo Project Authors (https://github.com/zawa8/pff)"
LICENSE_STR = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
LICENSE_URL = "https://openfontlicense.org"

SFD_DIRS = [
    pff_root / "sfd/xi52sfd/xi52asc",
    pff_root / "sfd/xi38sfd/xi38asc",
]

SKIP = {
    'binarywonlyw8asc.sfd',
    'frenchonlyw8asc.sfd',
    'germanonlyw8asc.sfd',
    'koreanonlyw8asc.sfd',
    'russianonlyw8asc.sfd',
    'spanishonlyw8asc.sfd',
}


def set_sfnt_name(font, name_id: str, value: str):
    """Replace or add an English (US) sfnt name entry."""
    names = list(font.sfnt_names)
    names = [
        n for n in names
        if not (n[0] == 'English (US)' and n[1] == name_id)
    ]
    names.append(('English (US)', name_id, value))
    font.sfnt_names = names


def update_metadata(sfd_path: Path):
    new_name = sfd_path.stem

    font = fontforge.open(str(sfd_path))

    font.familyname = new_name
    font.fullname = new_name
    font.fontname = new_name
    font.uniqueid = 0

    set_sfnt_name(font, 'Family', new_name)
    set_sfnt_name(font, 'Fullname', new_name)
    set_sfnt_name(font, 'PostScriptName', new_name)
    set_sfnt_name(font, 'UniqueID', f"{VERSION}; {VENDOR}; {new_name}")
    set_sfnt_name(font, 'Version', VERSION)
    set_sfnt_name(font, 'Copyright', COPYRIGHT)
    set_sfnt_name(font, 'License', LICENSE_STR)
    set_sfnt_name(font, 'License URL', LICENSE_URL)

    font.save(str(sfd_path))
    font.close()
    print(f"Updated: {sfd_path.name} -> {new_name}")


def main():
    for sfd_dir in SFD_DIRS:
        if not sfd_dir.exists():
            print(f"  SKIP (not found): {sfd_dir}")
            continue
        for sfd_path in sorted(sfd_dir.glob("*.sfd")):
            if sfd_path.name in SKIP:
                print(f"  SKIP: {sfd_path.name}")
                continue
            try:
                update_metadata(sfd_path)
            except Exception as e:
                print(f"  Error {sfd_path.name}: {e}")
                sys.exit(1)


if __name__ == "__main__":
    main()