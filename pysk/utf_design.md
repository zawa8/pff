# xnglo UTF design

How `xi38utf` / `xi52utf` files are built from `asc`.

## Core idea

Every script's `utf` file carries **its own glyphs** in *all* Unicode
ranges, so a reader of that script can read *any* Indic Unicode text
in a script they know.

Example: a Bengali reader opens `xb38utf.sfd`. Hindi, Punjabi, Tamil,
Malayalam, Sinhala Unicode text — all render as **Bengali glyphs**
(plus ASCII/Latin), not as the original scripts.

## Base

`asc` file's `0x30–0x7F` slots hold the script's Latin/Indic glyphs.

- `xh38asc.sfd` — Hindi glyphs
- `xb38asc.sfd` — Bengali glyphs
- `xp38asc.sfd` — Punjabi glyphs
- ... etc.

## Build: `asc` → `utf`

1. Copy `asc` → `utf` (128 glyph slots, unchanged).
2. For each Unicode range, **reference-copy** base glyphs into the
   range's codepoints, using a per-range mapping.

### Ranges (9 scripts + Sinhala)

| Script    | Unicode range   | Base offset    |
|-----------|-----------------|----------------|
| Hindi     | `U+0900–U+097F` | 0x00–0x7F      |
| Bengali   | `U+0980–U+09FF` | 0x00–0x7F      |
| Punjabi   | `U+0A00–U+0A7F` | 0x00–0x7F      |
| Gujarati  | `U+0A80–U+0AFF` | 0x00–0x7F      |
| Oriya     | `U+0B00–U+0B7F` | 0x00–0x7F      |
| Tamil     | `U+0B80–U+0BFF` | 0x00–0x7F      |
| Telugu    | `U+0C00–U+0C7F` | 0x00–0x7F      |
| Kannada   | `U+0C80–U+0CFF` | 0x00–0x7F      |
| Malayalam | `U+0D00–U+0D7F` | 0x00–0x7F      |
| Sinhala   | `U+0D80–U+0DFF` | 0x00–0x7F (*)  |

(*) **Sinhala uses a different mapping** — `SINHALA_OFFSET_MAP`.
All other 9 ranges share the same offset mapping
(`UNICODE_HINDI_ARRAY`).

### Why the same mapping for 9 ranges?

Indic scripts place vowel signs, consonants, and matras at
**consistent offsets** within their Unicode block. So a single
mapping (`UNICODE_HINDI_ARRAY`, borrowed from htrlib) works for all
9. Sinhala's block is arranged differently, so it needs its own map.

### Example (Bengali reader, `xb38utf`)

| Unicode text        | Codepoint  | `xb38utf` render       |
|---------------------|------------|------------------------|
| Hindi `ा`           | `U+093E`   | Bengali `া` (from `a`) |
| Bengali `া`         | `U+09BE`   | Bengali `া` (from `a`) |
| Malayalam `ാ`       | `U+0D3E`   | Bengali `া` (from `a`) |
| Sinhala `ක`         | `U+0D9A`   | Bengali `k`            |
| Sinhala `ද`         | `U+0DAF`   | Bengali `D`            |

Sinhala rows use `SINHALA_OFFSET_MAP` (`0x1A → k`, `0x2A → D`),
but the **source glyph** is still the Bengali base.

## Sinhala range

Sinhala's own `utf` file (`xs38utf.sfd`) uses `SINHALA_OFFSET_MAP`
with **Sinhala base glyphs** (from `xs38asc.sfd`).

All other scripts use `SINHALA_OFFSET_MAP` too, but their own base
glyphs. So:

- `xb38utf` Sinhala range → Bengali glyphs
- `xh38utf` Sinhala range → Hindi glyphs
- `xs38utf` Sinhala range → Sinhala glyphs

## Files involved

- `scripts/xi52py/glyph_copy/build_utf_fonts.py` — main builder
- `scripts/xi52py/glyph_copy/build_sinhala_asc.py` — builds
  `xs38asc.sfd` from Noto Sinhala + English
- `UNICODE_HINDI_ARRAY` — 128-entry offset → ASCII char map
  (Hindi-based, shared by 9 ranges)
- `SINHALA_OFFSET_MAP` — sparse offset → ASCII char map
  (Sinhala-specific)

## Invariants

- `asc` files are never modified by the UTF build.
- `utf` files start as a copy of `asc`, then get extra refs.
- Each Unicode range has exactly 128 slots (0x00–0x7F offsets).
- Empty mapping entries are skipped (no glyph created).
- Refs point to base glyphs (no outline duplication).

## Purpose

A single `utf` file lets a reader of one script read Unicode text
from **all 11 scripts**, rendered in the script they know. No
translation, no glyph substitution by the renderer — everything is
baked into the font's character map.
