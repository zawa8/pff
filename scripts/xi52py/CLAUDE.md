# CLAUDE.md — scripts/xi52py

Guidance for anyone (human or Claude Code) working in this folder. These
are FontForge automation scripts (`fontforge` Python module) that build
the **xi52** font family by *extending* the already-built xi38 family
(38-codepoint hscii alphabet → 52 codepoints), rather than sourcing
glyphs from Noto directly the way `scripts/xi38py` does.

## Running these scripts

They import `fontforge`, which is only available inside FontForge's own
bundled Python, not a pip package. Run them as:

```
fontforge -script <script>.py
```

not `python3 <script>.py` (the `#!/usr/bin/env python3` shebang is
present but won't actually have `fontforge` importable under a system
Python).

## Pipeline (the "live" xi52 path, intended run order)

1. **`copy_xi38_to_xi52.py`** — creates `sfd/xi52font/xi52asc/*.sfd` by
   copying `sfd/xi38font/xi38asc/*.sfd` and renaming (`…38` → `…52`).
2. **`copy_e52_chars_xi52.py`** — copies specific characters from
   `eNgliSxe52.sfd` into the other 10 xi52asc language fonts.
3. **`copy_xi38utf_to_xi52utf.py`** — creates `sfd/xi52font/xi52utf/*.sfd`
   from `sfd/xi38font/xi38utf/*.sfd` (references are already present in
   xi38utf, so this step doesn't need to re-add them).
4. **`add_unicode_ranges_utf_52.py`** — adds Unicode-range **reference**
   copies to the xi52utf SFDs via `copyReference()`. This is the
   current/clean version — see "Redundant files" below for its
   near-duplicate.
5. **`copy_e52utf_chars_xi52utf.py`** — copies specific chars from
   `eNgliSxe52utf.sfd` into the 10 xi52utf language fonts.
6. **`rename_utf_fonts_52.py`** — renames font internals in the xi52utf
   SFDs (`hindixv52` → `hindixv52utf`, etc.) — the correctly-adapted
   xi52 version of a script that also exists (stale) in this folder;
   see "Redundant files" below.
7. **`copy_utf_to_mono_xi52.py`** — builds `sfd/xi52font/xi52mono/*.sfd`
   from xi52utf, making the first 128 characters monospace.
8. **`center_glyphs_mono_xi52.py`** — centers all glyphs in the xi52mono
   fonts.
9. **`fix_mono_width_xi52.py`** — fixes glyph-width issues in xi52mono
   (scales glyphs that overflow 600 units, like `f`; sets reference
   glyph widths to 600).
10. **`generate_xi52asc_ttf_woff2.py`** — generates `.ttf`/`.woff2` from
    xi52asc.
11. **`generate_xi52_ttf.py`** — generates `.ttf`/`.woff2` from xi52utf.
12. **`generate_mono_ttf.py`** — generates `.ttf`/`.woff2` from xi52mono.

## Removed: redundant files (were byte-identical leftovers from xi38py)

The following were checked with `diff` against their `scripts/xi38py`
counterparts, found **byte-for-byte identical** — still operating on
xi38 paths/fonts despite having lived in the xi52py folder, each with a
properly-adapted xi52 replacement already in this directory — and have
been deleted. See git history if any are needed for reference.

- **`generate_utf_ttf.py`** — docstring literally said *"Generate TTF
  and WOFF2 from xi38utf SFD files"*; read from `sfd/xi38font/xi38utf`
  and wrote to `.../ttf/hscii/xi38utf`. Superseded by
  `generate_xi52_ttf.py` (step 11 above).
- **`glyph_kopi_u2hindi.py`**, **`glyph_kopi_u2utf.py`**,
  **`glyph_kopi_u9scripts.py`**, **`glyph_kopi_usinhala.py`** — all
  identical to their `scripts/xi38py` originals, all still read/wrote
  xi38 paths. xi52 never sources glyphs from Noto directly — it derives
  everything from the already-built xi38 fonts via the `copy_xi38_*`
  scripts (steps 1 & 3 above) — so these four had no real job here.
- **`rename_utf_fonts.py`** — identical to `scripts/xi38py/rename_utf_fonts.py`,
  renamed xi38 (not xi52) font internals. Superseded by
  `rename_utf_fonts_52.py` (step 6 above).

One more near-duplicate, *not* byte-identical but functionally the
same, also removed:

- **`add_unicode_ranges_utf52.py`** vs. **`add_unicode_ranges_utf_52.py`**
  (note the underscore placement was the only filename difference) —
  same `copyReference()` logic against the same xi52utf SFDs. The
  no-underscore version was more verbose (extra comments, an inline
  "← REFERENCE COPY!" note) and logged to a differently-named file; the
  underscored version is the cleaned-up, current one that remains.

`test.html` is byte-identical to `scripts/xi38py/test.html` (a
`@font-face` smoke-test page) — consider making this one shared file
instead of two copies that can drift.

## Other notes

- Same boilerplate/logging pattern as xi38py: resolve `pff_root`, then
  `logging.basicConfig` to `../logs/<script-name>.log` plus a console
  handler at `WARNING` level.
- Output-path handling is inconsistent across the `generate_*` scripts:
  `generate_xi52_ttf.py` and `generate_mono_ttf.py` (plus the redundant
  `generate_utf_ttf.py`) hardcode the Windows path
  `C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font`, while
  `generate_xi52asc_ttf_woff2.py` instead writes relative to the repo
  (`pff_root.parent / "font/..."`). Worth reconciling so all three
  agree on where output actually goes.
