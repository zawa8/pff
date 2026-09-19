# xi52 / xi38 Pipeline Design

This document describes the naming, groups, pipelines, and migration
plan for the xi52sfd / xi38sfd font build system.

---

## 1. Naming Convention

### 1.1 Folder renames (old → new)

| Old | New |
|---|---|
| `sfd/xi52font/` | `sfd/xi52sfd/` |
| `sfd/xi38font/` | `sfd/xi38sfd/` |
| `xnglofonts/ttf/xi52fonts/` | `xnglofonts/ttf/xi52ttf/` |
| `xnglofonts/ttf/xi38fonts/` | `xnglofonts/ttf/xi38ttf/` |
| `xnglofonts/woff2/xi52fonts/` | `xnglofonts/woff2/xi52woff2/` |
| `xnglofonts/woff2/xi38fonts/` | `xnglofonts/woff2/xi38woff2/` |

Folders that stay the same:
- `pff/notofonts/`
- `pff/scripts/`
- `pff/xnglofonts/`
- `pff/logs/`

### 1.2 Subfolder structure
pff/
├── sfd/
│ ├── xi52sfd/
│ │ ├── xi52asc/
│ │ ├── xi52utf/
│ │ └── xi52mono/
│ └── xi38sfd/
│ ├── xi38asc/
│ ├── xi38utf/
│ └── xi38mono/
├── notofonts/ (unchanged)
├── scripts/ (unchanged)
└── xnglofonts/
├── ttf/
│ ├── xi52ttf/
│ │ ├── xi52asc/
│ │ ├── xi52utf/
│ │ └── xi52mono/
│ └── xi38ttf/
│ ├── xi38asc/
│ ├── xi38utf/
│ └── xi38mono/
└── woff2/
├── xi52woff2/
│ ├── xi52asc/
│ ├── xi52utf/
│ └── xi52mono/
└── xi38woff2/
├── xi38asc/
├── xi38utf/
└── xi38mono/

### 1.3 File naming

Suffixes:
- `asc` — ASCII-only
- `utf` — Unicode
- `mono` — monospace (built from `asc`)

Examples (Hindi):

| Pipeline | Path |
|---|---|
| asc | `sfd/xi52sfd/xi52asc/hindixh52asc.sfd` |
| utf | `sfd/xi52sfd/xi52utf/hindixh52utf.sfd` |
| mono | `sfd/xi52sfd/xi52mono/hindixh52mono.sfd` |
| asc (xi38) | `sfd/xi38sfd/xi38asc/hindixh38asc.sfd` |
| utf (xi38) | `sfd/xi38sfd/xi38utf/hindixh38utf.sfd` |
| mono (xi38) | `sfd/xi38sfd/xi38mono/hindixh38mono.sfd` |

English files:
- `sfd/xi52sfd/xi52asc/eNgliSxe52asc.sfd`
- `sfd/xi38sfd/xi38asc/eNgliSxe38asc.sfd`

### 1.4 File renames (old → new)

| Old | New |
|---|---|
| `eNgliSxe52.sfd` | `eNgliSxe52asc.sfd` |
| `eNgliSxe38.sfd` | `eNgliSxe38asc.sfd` |
| `hindixv52.sfd` | `hindixh52asc.sfd` |
| `hindixv38.sfd` | `hindixh38asc.sfd` |
| `bengalixb52.sfd` | `bengalixb52asc.sfd` |
| `bengalixb38.sfd` | `bengalixb38asc.sfd` |
| `pnzabixp52.sfd` | `pnzabixp52asc.sfd` |
| `guzrajixg52.sfd` | `guzrajixg52asc.sfd` |
| `oriyaxo52.sfd` | `oriyaxo52asc.sfd` |
| `tmilxt52.sfd` | `tmilxt52asc.sfd` |
| `jeluguxj52.sfd` | `jeluguxj52asc.sfd` |
| `knRaxk52.sfd` | `knRaxk52asc.sfd` |
| `mlyalxmxm52.sfd` | `mlyalxmxm52asc.sfd` |
| `sinhlaxs52.sfd` | `sinhlaxs52asc.sfd` |
| ... (xi38 files likewise) | ... |

Note: `xv` → `xh` everywhere (`xh` = xNglohinDi).

---

## 2. Groups (G1–G5)

52 Latin letters grouped by copy pipeline. Sources:
- `xe52` = `eNgliSxe52asc.sfd`
- `xe38` = `eNgliSxe38asc.sfd`
- `notomath` = `NotoSansMath-Regular.ttf`
- `notolang` = `NotoSans{Script}-Regular.ttf` (script-specific)

### G1 — 14 letters

Letters: `a i u e o h N R L Y V W P F`

Flow (sequential chain, all English shapes): xe52 → xe38 → xh52 → xh38


### G2 — 6 letters

Letters: `E I O U M X`

Two parallel chains:
1. xe52 → xh52
2. notomath → xe38 → xh38


### G3 — 10 letters

Letters: `c C g G D q Q T j J`

Two parallel chains:

1. xe52 → xe38 → xh52 
2. notolang → xh38


### G4 — 18 letters

Letters: `b d f k l m n p r s t w y z K S Z B`

Two parallel chains:
1. xe52 → xe38
2. notolang → xh38 → xh52


### G5 — 4 letters

Letters: `v H x A`

Two parallel chains:
1. xe52 → xe38
2. notolang → xh38 → manual (FontForge) → xh52


For G5, the manual step means:
1. Open `x{lang}38asc.sfd` in FontForge.
2. Wait for the designer to save and close all FontForge windows.
3. Copy final designed glyphs from `x{lang}38asc.sfd` into `x{lang}52asc.sfd`.

Total letters: 14 + 6 + 10 + 18 + 4 = 52 ✔

---

## 3. Pipelines

### Pipeline 1 — asc

Build `*asc.sfd` for both 52 and 38 series using groups G1–G5.

Steps:
1. For each script in {hindi, bengali, punjabi, gujarati, oriya,
   tamil, telugu, kannada, malayalam, sinhala}:
   - Apply G1–G5 rules to produce `x{lang}52asc.sfd` and
     `x{lang}38asc.sfd`.
2. Save all `*asc.sfd` files.
3. Generate `*asc.ttf` and `*asc.woff2` for every script and both
   series, writing into the `*asc/` output folders.

### Pipeline 2 — utf

Build `*utf.sfd` from `*asc.sfd`.

Steps:
1. Copy 128 basic glyphs from `*asc.sfd` into `*utf.sfd`.
2. Copy references for those 128 glyphs into 10 Unicode ranges
   (per a mapping dictionary) inside `*utf.sfd`.
3. Save all `*utf.sfd` files.
4. Generate `*utf.ttf` and `*utf.woff2`.

### Pipeline 3 — mono

Build `*mono.sfd` from `*asc.sfd`.

Steps:
1. Create `*mono.sfd` from `*asc.sfd` (rename files and metadata).
2. Make all glyph widths equal: use the maximum width found in
   glyphs 65–128 (0x41–0x80).
3. Center-align every glyph in the mono font.
4. Generate `*mono.ttf` and `*mono.woff2`.
5. Ask the operator: `git commit && push` or `git restore *.sfd`.

---

## 4. CSV Format

The file `glyph_copy.csv` drives Pipeline 1. Its columns are:

e52,group,xe38_src,xh52_src,xh38_src


- `e52`     — letter (ASCII)
- `group`   — G1..G5
- `xe38_src` — direct source for xe38: `xe52`, `notomath`, `notolang`
- `xh52_src` — direct source for xh52: `xe38`, `xe52`, `notolang`
- `xh38_src` — direct source for xh38: `xh52`, `xe38`, `notolang`

Example rows:
1. a,G1,xe52,xe38,xh52
2. E,G2,xe52,xe52,notomath
3. c,G3,xe52,xe38,notolang
4. b,G4,xe52,notolang,notolang
5. v,G5,xe52,notolang,notolang


Note: for chains (e.g. G1), the script must execute the steps in
order — first build xe38, then xh52, then xh38 — because each step
depends on the previous one.

---

## 5. Migration Plan

Phase 1 — folders and file names
1. Rename folders (see §1.1).
2. Rename files (see §1.4). Use `git mv` to preserve history.
3. Delete any stale/duplicate folders no longer referenced.

Phase 2 — scripts
4. Update every script path in `scripts/xi52py/`:
   - `sfd/xi52font/`     → `sfd/xi52sfd/`
   - `sfd/xi38font/`     → `sfd/xi38sfd/`
   - `xnglofonts/ttf/xi52fonts/`     → `xnglofonts/ttf/xi52ttf/`
   - `xnglofonts/woff2/xi52fonts/`   → `xnglofonts/woff2/xi52woff2/`
   - ... (all the pairs from §1.1)
5. Replace `xv` with `xh` in all script filenames and string
   literals.

Phase 3 — CSV and `.md`
6. Update `glyph_copy.csv` to the new format from §4.
7. Commit and push.

---

## 6. Commands

Run the whole pipeline:

    fontforge -script scripts/xi52py/main.py

List numbered steps:

    fontforge -script scripts/xi52py/main.py --list

Resume from a step:

    fontforge -script scripts/xi52py/main.py --from 4

Run a single step:

    fontforge -script scripts/xi52py/main.py --only 7

---

## 7. Pending decisions

- `T` glyph: to be copied from Sunny Spells. Locate and copy.
- `E` glyph: to be designed manually (3 horizontal lines, ≡).
- Remaining `ipa38` / `hinDi` values for `glyph_sources.csv`.
- Whether `glyph_sources.csv` is needed at all, given that
  `glyph_copy.csv` already drives the copy.