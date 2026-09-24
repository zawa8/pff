#!/usr/bin/env python3
"""
Update font metadata (family, full, postscript names) to match filename.
Runs in GitHub Actions (needs FontForge).
"""

import fontforge
from pathlib import Path

script_dir = Path(__file__).parent
pff_root = script_dir.parent.parent


def update_metadata(sfd_path):
    """Update font family/full/postscript names to match file name."""
    new_name = sfd_path.stem  # e.g. 'xh52asc'

    font = fontforge.open(str(sfd_path))
    font.familyname = new_name
    font.fullname = new_name
    font.fontname = new_name
    font.save(str(sfd_path))
    font.close()
    print(f"Updated: {sfd_path.name} -> {new_name}")


def main():
    for sfd_dir in [
        pff_root / "sfd/xi52sfd/xi52asc",
        pff_root / "sfd/xi38sfd/xi38asc",
    ]:
        for sfd_path in sorted(sfd_dir.glob("*.sfd")):
            try:
                update_metadata(sfd_path)
            except Exception as e:
                print(f"  Error {sfd_path.name}: {e}")


if __name__ == "__main__":
    main()
