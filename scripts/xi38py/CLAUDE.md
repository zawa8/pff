# CLAUDE.md — scripts/xi38py

Guidance for anyone (human or Claude Code) working in this folder. These
are FontForge automation scripts (`fontforge` Python module) that build
the **xi38** font family — 9 Indian scripts + English "hscii" — from
Noto source glyphs down to shippable `.ttf`/`.woff2`.

## Running these scripts

They import `fontforge`, which is only available inside FontForge's own
bundled Python, not a pip package. Run them as:

```
fontforge -script <script>.py
```

not `python3 <script>.py` (the `#!/usr/bin/env python3` shebang is
present but won't actually have `fontforge` importable under a system
Python).

## Pipeline (intended run order)

1. **`glyph_download_noto.py`** — downloads the Noto Sans regular TTFs
   for Bengali/Gurmukhi/Gujarati/Oriya/Tamil/Telugu/Kannada/Malayalam/
   Sinhala into `../notofonts/`. (Devanagari isn't in this script's
   list — `NotoSansDevanagari-Regular.ttf` is expected to already be
   present in `notofonts/`.)
2. **`glyph_kopi_u9scripts.py`** — copies consonant glyphs (script-
   specific, from Noto), the schwa/`x`, and the retroflex-flap `R` fix
   from Noto, plus a shared set of English-derived vowel/letter glyphs
   from `eNgliSxe38.sfd`, into each of the 9 xi38asc SFDs.
   - ⚠ **Hardcoded path looks stale**: `sfd_path = pff_root /
     "sfd/x38ifont/x38iasc" / ...` — the folder that actually exists in
     this repo is `sfd/xi38font/xi38asc` (letters transposed:
     `x38i` vs `xi38`). As committed, this script won't find its SFDs.
   - Also writes generated `.ttf`/`.woff2` to a hardcoded Windows path
     (`C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font`) —
     update per machine before running.
3. **`glyph_kopi_usinhala.py`** — same idea as #2 but for Sinhala alone
   (it isn't in `glyph_kopi_u9scripts.py`'s script table, so it needs
   its own consonant mapping). Also copies ASCII 0x00–0x40 plus a batch
   of vowels/English letters from `eNgliSxe38.sfd`.
4. **`glyph_kopi_u2utf.py`** — builds the xi38utf SFDs from xi38asc: copies
   the 128 ASCII glyphs across, then adds Unicode-range references
   (mapping from htrlib's `unicode_hindi_array`) so each script's real
   Unicode codepoints reference the matching ASCII glyph.
5. **`add_unicode_ranges_utf.py`** — adds further Unicode-range
   **reference** copies to the xi38utf SFDs via FontForge's
   `copyReference()` API. Conceptually overlaps with step 4's
   reference-adding — worth checking whether both passes are actually
   needed or whether this is a leftover from before step 4 existed.
6. **`rename_utf_fonts.py`** — renames font internals in each xi38utf
   SFD (e.g. `hindixv38` → `hindixv38utf`) via the FontForge naming API,
   plus a regex pass over the raw SFD text to fix the `LangName` line
   (which FontForge's API doesn't touch).
7. **`generate_utf_ttf.py`** — generates `.ttf` + `.woff2` from the
   finished xi38utf SFDs, written to the same hardcoded Windows
   `font_repo` path as step 2.

`test.html` is a static `@font-face` smoke-test page for
`hindixv38utf.woff2`, not part of the build pipeline. **An identical
copy of this file also lives in `scripts/xi52py/test.html`** — worth
deciding whether that should be one shared file instead of two copies
that can silently drift apart.

## Known issue: stale/redundant script

**`glyph_kopi_u2hindi.py`** looks like an older, Hindi-only draft of
step 2's job (copies just Devanagari glyphs into `hindixv38.sfd`,
using the same stale `sfd/x38ifont/x38iasc` path as
`glyph_kopi_u9scripts.py`). Since `glyph_kopi_u9scripts.py` already
covers Hindi as one of its 9 configured scripts, this script's separate
existence looks like dead code left over from before the 9-script
version was written — confirm with the repo owner before deleting.

## Other notes

- All scripts share the same boilerplate: resolve `pff_root`, then set
  up `logging.basicConfig` writing to `../logs/<script-name>.log` with
  a console handler at `WARNING` level.
- The `x`/consonant/vowel → Unicode mappings mirror this project's own
  hskii/xi38 romanization scheme — see `/reAdme.md` and
  `/hskii-encoding-analysis.md` at the repo root for the scheme itself.
- Several scripts hardcode the same Windows-only output path
  (`C:/Users/ravi_/OneDrive/Desktop/Vimal/wimxlprogs/gitt/font`).
  There's no cross-platform/relative fallback — this needs manual
  editing on any other machine or OS.
