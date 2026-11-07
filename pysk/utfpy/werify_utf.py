#!/usr/bin/env python3
"""Fail the build if utf utf38sfd_list have no (or collapsed) references in Indic ranges."""
import sys
from pathlib import Path
import fontforge

root = Path(__file__).resolve().parents[2]
utf38dir = root / "sfd/38/utf"
utf52dir = root / "sfd/52/utf"

# xe38utf.sfd is a base font with no unicode refs — skip it
SKIP = {"xe38utf.sfd"}

utf38sfd_list = [p for p in sorted(utf38dir.glob("*.sfd")) if p.name not in SKIP]
utf52sfd_list = [p for p in sorted(utf52dir.glob("*.sfd"))]

if not utf38sfd_list:
    sys.exit(f"no utf sfd found in {utf38dir}")
if not utf52sfd_list:
    sys.exit(f"no utf sfd found in {utf52dir}")

failed = False

# Combine into a single list of tuples to avoid code duplication
all_sfd_files = [(p, "38") for p in utf38sfd_list] + [(p, "52") for p in utf52sfd_list]

for p, version in all_sfd_files:
    f = fontforge.open(str(p))
    refs = collapsed = 0
    
    for g in f.glyphs():
        # Check Indic unicode range and if references exist
        if 0x0900 <= g.unicode < 0x0E00 and g.references:
            refs += 1
            for ref in g.references:
                m = ref[1]  # Transformation matrix
                if m[0] == 0 and m[3] == 0:
                    collapsed += 1
                    
    print(f"[{version}] {p.name}: {refs} ref glyphs, {collapsed} collapsed")
    f.close()
    
    # If any single font fails, the entire build status becomes failed
    if refs == 0 or collapsed > 0:
        failed = True

sys.exit(1 if failed else 0)
