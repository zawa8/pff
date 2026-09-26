#!/usr/bin/env python3
"""
fix_fontnames.py — one-off utility.

Sets `FontName:` in each .sfd file to match its filename stem,
so internal font name and file name stay consistent.

Usage:
    python scripts/xi52py/tools/fix_fontnames.py          # apply
    python scripts/xi52py/tools/fix_fontnames.py --dry    # show only
"""
import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PFF_ROOT = HERE.parent.parent.parent

TARGET_DIRS = [
    PFF_ROOT / "sfd/xi38sfd/xi38utf",
    PFF_ROOT / "sfd/xi52sfd/xi52utf",
    PFF_ROOT / "sfd/xi52sfd/xi52mono",
]

SKIP_PREFIXES = ("xnglosoft",)


def process(sfd: Path, dry: bool) -> bool:
    stem = sfd.stem
    text = sfd.read_text(encoding="utf-8", errors="replace")
    new_text, n = re.subn(
        r"^FontName:\s*.*$",
        f"FontName: {stem}",
        text, count=1, flags=re.MULTILINE,
    )
    if n == 0:
        print(f"  no FontName line: {sfd.name}")
        return False
    if new_text == text:
        print(f"  already ok: {sfd.name}")
        return False
    # show old -> new
    m = re.search(r"^FontName:\s*(\S+)", text, flags=re.MULTILINE)
    old = m.group(1) if m else "(?)"
    print(f"  fix: {sfd.name}  {old} -> {stem}")
    if not dry:
        sfd.write_text(new_text, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true",
                    help="show changes without writing")
    args = ap.parse_args()

    changed = 0
    total = 0
    for d in TARGET_DIRS:
        if not d.exists():
            print(f"skip (missing): {d}")
            continue
        print(f"{d.relative_to(PFF_ROOT)}/")
        for sfd in sorted(d.glob("*.sfd")):
            if sfd.name.startswith(SKIP_PREFIXES):
                print(f"  skip: {sfd.name}")
                continue
            total += 1
            if process(sfd, args.dry):
                changed += 1
    verb = "would be " if args.dry else ""
    print(f"\n{changed} of {total} file(s) {verb}changed.")


if __name__ == "__main__":
    main()