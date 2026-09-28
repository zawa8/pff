# xi52 / xi38 Pipeline Design

Build system for the xi52sfd / xi38sfd font families.

---

## 1. Folder Structure

```

pff/
├── sfdsrc/                    ← MASTER SOURCES (never overwritten)
│   ├── xe52/
│   │   └── xe52asc.sfd        English master source
│   ├── xi38/
│   │   ├── xh38asc.sfd        Hindi source (manually designed)
│   │   ├── xb38asc.sfd        Bengali source (future)
│   │   ├── xk38asc.sfd        Kannada source (future)
│   │   └── ...                baaki scripts ke sources
│   ├── scripts/               ← future design scripts
│   └── README.md
├── sfd/                        ← TARGETS (rebuilt each pipeline run)
│   ├── xi52sfd/
│   │   ├── xi52asc/
│   │   ├── xi52utf/
│   │   └── xi52mono/
│   └── xi38sfd/
│       ├── xi38asc/
│       └── xi38utf/
├── notofonts/                  ← Noto TTFs (fallback)
├── scripts/                    ← pipeline scripts
├── logs/                       ← build logs + build-info.txt
└── xnglofonts/
    ├── ttf/
    │   ├── xi52ttf/
    │   │   ├── xi52asc/
    │   │   ├── xi52utf/
    │   │   └── xi52mono/
    │   └── xi38ttf/
    │       ├── xi38asc/
    │       └── xi38utf/
    └── woff2/
        ├── xi52woff2/
        │   ├── xi52asc/
        │   ├── xi52utf/
        │   └── xi52mono/
        └── xi38woff2/
            ├── xi38asc/
            └── xi38utf/

```

### Sources (never overwritten)
- `sfdsrc/xe52/xe52asc.sfd` — English master
- `sfdsrc/xi38/*.sfd` — per-script sources (Hindi, Bengali, Kannada, ...)

### Targets (rebuilt every pipeline run)
- `sfd/xi52sfd/xi52asc/*.sfd`
- `sfd/xi38sfd/xi38asc/*.sfd`
- `sfd/*/xi*utf/*.sfd`
- `sfd/*/xi*mono/*.sfd`

### Suffixes
- `asc` — first 128 glyph slots (0x00–0xFF). Not "ASCII" — glyph-slot count.
- `utf` — 128 glyphs from `asc`, ref/copy-pasted into Unicode ranges
  0x0900–0xD800 per-language mappings (`xNglo_phoneme_grapheme.csv`).
- `mono` — 128 glyphs from `asc`, equal width + center-aligned.
  Built from `asc`, NOT from `utf`.

### Transformations
- `asc` → `utf`      : copy 128 + ref/copy-paste at Unicode positions
- `asc` → `mono`     : copy 128 + equal-width + center-align
- `xL38asc` → `xL52asc` : copy script-specific glyphs from `xL38asc`
  + Latin/symbol glyphs from `xe52asc`, per `glyph_copy.csv`

### File naming
- `sfd/xi52sfd/xi52asc/xh52asc.sfd`
- `sfd/xi52sfd/xi52utf/xh52utf.sfd`
- `sfd/xi52sfd/xi52mono/xh52mono.sfd`
- `sfd/xi38sfd/xi38asc/xh38asc.sfd`
- `sfd/xi38sfd/xi38utf/xh38utf.sfd`

Rule: **`FontName:` in each `.sfd` equals its filename stem**
(`xh38asc.sfd` → `FontName: xh38asc`).

Note: `xv` → `xh` everywhere (`xh` = xNglohinDi).

---

## 2. Sources vs Targets

### Sources
- `sfdsrc/xe52/xe52asc.sfd` — English master (feeds both xi38 and xi52)
- `sfdsrc/xi38/*.sfd` — per-script sources, manually designed
- `notofonts/*.ttf` — Noto fallback

### Targets
- `sfd/xi52sfd/xi52asc/*.sfd`
- `sfd/xi38sfd/xi38asc/*.sfd`
- `sfd/*/xi*utf/*.sfd`
- `sfd/*/xi*mono/*.sfd`

Step 1 (`step0_copy_sources.py`) copies `xe52asc.sfd` and the
selected `xL38asc.sfd` into `sfd/` targets before the build steps.
Sources themselves are never modified.

---

## 3. CSV Format — `glyph_copy.csv`

Per-glyph decision table for the 128 e52 slots. `build_asc_fonts.py`
reads this CSV and builds each script's `xL52asc.sfd` by copying
glyphs from the listed sources.

### Files
- `glyph_copy.csv`        — main pipeline (all scripts)
- `glyph_copy_xe38.csv`   — xe38-specific overrides
- `glyph_sources.csv`     — IPA + Hindi documentation (reference only)

### Columns (4)

```

e52, src, action, notes

```

- `e52`    — letter (ASCII slot 0x00–0xFF)
- `src`    — source for that letter:
             `xe52` | `xe38` | `xh38` | `notoindik` | `noto_math` | `keep`
             (`notoindik` = per-script Indic Noto, e.g. `NotoSansDevanagari`,
             `NotoSansBengali`, ...)
- `action` — `replace` | `keep` | `manual` | `remove`
- `notes`  — free-form documentation

### Actions
- `replace` — copy from `src` into target
- `keep`    — leave target glyph as-is
- `manual`  — same as keep (reserved for hand-drawn glyphs)
- `remove`  — currently treated as keep

### Example rows

```

k,notoindik,replace,Indic consonant
x,xh38,replace,Hindi schwa design (अ + small x)
N,xe52,replace,Latin shape
E,noto_math,replace,math ≡
T,keep,keep,Sunny Spells T

```

---

## 4. Groups

| Group | Letters | Sources |
|-------|---------|---------|
| G1 | `a i u e o h N R L Y V W P F` (14) | notoindik (except N, R from xe52) |
| G2 | `x j J q Q v c C g G` (10) | xh38 (Hindi designs) |
| G3 | `N R a i u e o h L Y V W P F` (14) | xe52 (Latin shapes) |
| G4 | `E I O U M X` (6) | noto_math |
| G5 | `A H` (2) | xh38 (Hindi designs) |

Total: 14 + 10 + 14 + 6 + 2 = 46 letters

Note: Actual letter counts depend on each script. Tamil has fewer
consonants, Bengali has no `w`, etc. Scripts gracefully skip letters
that don't exist in their Noto source.

---

## 5. Pipeline (15 steps, 6 phases)

### Phase `src` — sources → targets
1. `[src] copy sources -> targets`

### Phase `asc` — xi38asc + xi52asc
2. `[asc] build xi38asc + xi52asc, 9 scripts (G1-G5)`
3. `[asc] build xi38asc + xi52asc, Sinhala`

### Phase `utf` — xi38utf + xi52utf
4. `[utf] xi38asc -> xi38utf (copy 128 + unicode refs)`
5. `[utf] xi52asc -> xi52utf (copy + refs)`
6. `[utf] add unicode-range refs to xi52utf`

### Phase `mono` — xi52mono  *(WIP, not run in CI)*
7. `[mono] xi52asc -> xi52mono`
8. `[mono] center glyphs in xi52mono`
9. `[mono] fix widths in xi52mono`

### Phase `meta` — font metadata
10. `[meta] update font metadata (Google Fonts format)`

### Phase `gen` — TTF/WOFF2 generation
11. `[gen] TTF/WOFF2 from xi38asc`
12. `[gen] TTF/WOFF2 from xi38utf`
13. `[gen] TTF/WOFF2 from xi52asc`
14. `[gen] TTF/WOFF2 from xi52utf`
15. `[gen] TTF/WOFF2 from xi52mono`

Metadata is stamped on every SFD **before** the `gen` phase, so TTF/WOFF2
carry correct Google Fonts metadata (Version, Copyright, License,
UniqueID, family/full/postscript names).

---

## 6. Commands

Run the whole pipeline:

    fontforge -script scripts/xi52py/main.py

List numbered steps:

    fontforge -script scripts/xi52py/main.py --list

List phase names:

    fontforge -script scripts/xi52py/main.py --list-phases

Run one phase only (src|asc|utf|mono|meta|gen):

    fontforge -script scripts/xi52py/main.py --phase asc

Resume from a step:

    fontforge -script scripts/xi52py/main.py --from N

Run one step:

    fontforge -script scripts/xi52py/main.py --only N

Skip specific steps:

    fontforge -script scripts/xi52py/main.py --skip 7,8,9

Dry run (print without executing):

    fontforge -script scripts/xi52py/main.py --dry-run

Keep going after a failure:

    fontforge -script scripts/xi52py/main.py --continue

Each run writes `logs/build-info.txt` (git SHA, FontForge version,
Python version, selected steps, timestamp).

---

## 7. CI

`.github/workflows/build-xi52.yml` runs on push to `main` and on
pull requests against `main`.

Steps:
1. Install FontForge
2. Verify Python syntax (`py_compile` on all entry scripts)
3. Sanity check (`main.py --list`)
4. `--phase src`, `--phase asc`
5. `--phase utf`
6. `--phase meta`
7. Clean old TTF/WOFF2
8. `--only 11` through `--only 14` (gen)
9. Upload SFDs, TTF/WOFF2, logs as artifacts

Mono steps (7–9, 15) are not run in CI yet (see Pending).

---

## 8. Font naming scheme (Google Fonts / web)

Hybrid naming — internal PostScript name stays technical, family/full
names are human-readable.

| Field | Example (`xh38asc.sfd`) |
|-------|-------------------------|
| **FontName** (SFD) | `xh38asc` (filename stem) |
| **Family** (sfnt) | `Xnglo Hindi xi38 asc` |
| **Fullname** (sfnt) | `Xnglo Hindi xi38 asc Regular` |
| **PostScriptName** (sfnt) | `XngloHindi-xi38asc` |
| **Version** | `Version X.Y.Z` from latest git tag |
| **Copyright** | `Copyright 2025 The Xnglo Project Authors (https://github.com/zawa8/pff)` |
| **License** | `This Font Software is licensed under the SIL Open Font License, Version 1.1.` |
| **License URL** | `https://openfontlicense.org` |
| **UniqueID (sfnt)** | `Version X.Y.Z; zawa8; XngloHindi-xi38asc` |
| **UniqueID (PS numeric)** | `0` (modern-workflow safe) |

Script code → human name map (in `update_font_metadata.py`):

    xh→Hindi  xb→Bengali  xp→Punjabi  xg→Gujarati  xo→Oriya
    xt→Tamil  xj→Telugu   xk→Kannada  xm→Malayalam xs→Sinhala
    xe→English

Special case:

    xbinaryheks → Family "Xnglo Binary Hex",
                  Fullname "Xnglo Binary Hex Regular",
                  PostScriptName "XngloBinary-Hex"

---

## 9. Metadata special cases (`SKIP` set)

Files in `update_font_metadata.py`'s `SKIP` set are left alone:

- `koreanonlyw8asc.sfd` — pending rename to `xko*` + xi52 pipeline add
- `russianonlyw8asc.sfd` — pending rename to `xr*` + xi52 pipeline add
- `xnglosoftw8utf.sfd` — special font, not part of x* scheme

Removed in v1.3.0:

- `frenchonlyw8asc.sfd` (removed)
- `germanonlyw8asc.sfd` (removed)
- `spanishonlyw8asc.sfd` (removed)

`binarywonlyw8asc.sfd` → `xbinaryheks.sfd` in v1.3.0.

---

## 10. Pending

- Non-Hindi scripts — G5 designs pending (per-script designers)
- `xi38mono` pipeline — not yet implemented
- Mono phase (steps 7–9, 15) — implemented but not run in CI
- `koreanonlyw8asc.sfd`, `russianonlyw8asc.sfd` — rename + xi52 add
- `xnglosoftw8utf.sfd` — decide scheme or remove
- `glyph_sources.csv` — may not be needed (`.csv` already documents)