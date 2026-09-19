#!/usr/bin/env python3
"""
pff\scripts\rename_files.py — rename SFD/TTF/WOFF2 files to new convention.
"""

import subprocess
from pathlib import Path

REPO = Path("C:/progxs/pff")

TARGET_DIRS = [
    "sfd/xi52sfd/xi52asc",
    "sfd/xi52sfd/xi52utf",
    "sfd/xi52sfd/xi52mono",
    "sfd/xi38sfd/xi38asc",
    "sfd/xi38sfd/xi38utf",
    "xnglofonts/ttf/xi52ttf/xi52asc",
    "xnglofonts/ttf/xi52ttf/xi52utf",
    "xnglofonts/ttf/xi52ttf/xi52mono",
    "xnglofonts/ttf/xi38ttf/xi38asc",
    "xnglofonts/ttf/xi38ttf/xi38utf",
    "xnglofonts/ttf/xi38ttf/xi38mono",
    "xnglofonts/woff2/xi52woff2/xi52asc",
    "xnglofonts/woff2/xi52woff2/xi52utf",
    "xnglofonts/woff2/xi52woff2/xi52mono",
    "xnglofonts/woff2/xi38woff2/xi38asc",
    "xnglofonts/woff2/xi38woff2/xi38utf",
    "xnglofonts/woff2/xi38woff2/xi38mono",
]


def new_name(stem: str, suffix: str) -> str:
    s = stem.replace("xv", "xh")
    if suffix == "asc" and not s.endswith("asc"):
        s = s + "asc"
    return s


def process_dir(rel_dir: str):
    d = REPO / rel_dir
    if not d.exists():
        print(f"  SKIP (not found): {rel_dir}")
        return

    folder = d.name
    if folder.endswith("asc"):
        suf = "asc"
    elif folder.endswith("utf"):
        suf = "utf"
    elif folder.endswith("mono"):
        suf = "mono"
    else:
        print(f"  SKIP (unknown suffix): {rel_dir}")
        return

    for f in d.iterdir():
        if not f.is_file():
            continue
        if f.suffix not in (".sfd", ".ttf", ".woff2"):
            continue

        old_stem = f.stem
        new_stem = new_name(old_stem, suf)

        if old_stem == new_stem:
            continue

        old_path = f.relative_to(REPO)
        new_path = old_path.parent / (new_stem + f.suffix)

        print(f"  {old_path} -> {new_path}")

        # Uncomment for actual rename:
        subprocess.run(
            ["git", "mv", str(old_path), str(new_path)],
            cwd=REPO, check=True
        )


def main():
    for rel_dir in TARGET_DIRS:
        print(f"\n[{rel_dir}]")
        process_dir(rel_dir)
    print("\nDone.")


if __name__ == "__main__":
    main()