#!/usr/bin/env python3
"""Fail the build if utf fonts have no (or collapsed) references in Indic ranges."""
import sys
from pathlib import Path
import fontforge

root = Path(__file__).resolve().parents[2]
utf_dir = root / "sfd/xi38sfd/xi38utf"
# xe38utf.sfd is a base font with no unicode refs — skip it
SKIP = {"xe38utf.sfd", "xe52utf.sfd"}
fonts = [p for p in sorted(utf_dir.glob("*.sfd")) if p.name not in SKIP]
if not fonts:
    sys.exit(f"no utf sfd found in {utf_dir}")

failed = False
for p in fonts:
    f = fontforge.open(str(p))
    refs = collapsed = 0
    for g in f.glyphs():
        if 0x0900 <= g.unicode < 0x0E00 and g.references:
            refs += 1
            for ref in g.references:
                m = ref[1]
                if m[0] == 0 and m[3] == 0:
                    collapsed += 1
    print(f"{p.name}: {refs} ref glyphs, {collapsed} collapsed")
    f.close()
    if refs == 0 or collapsed:
        failed = True
sys.exit(1 if failed else 0)