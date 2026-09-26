# xi52 / xi38 Pipeline Design

Build system for the xi52sfd / xi38sfd font families.

---

## 1. Folder Structure

```

pff/
├── sfdsrc/                    ← MASTER SOURCES (never overwritten)
│   ├── xe52/
│   │   └── xe52asc.sfd
│   ├── xh38/
│   │   └── xh38asc.sfd
│   ├── scripts/               ← future design scripts
│   └── README.md
├── sfd/                        ← TARGETS (built each pipeline run)
│   ├── xi52sfd/
│   │   ├── xi52asc/
│   │   ├── xi52utf/
│   │   └── xi52mono/
│   └── xi38sfd/
│       ├── xi38asc/
│       ├── xi38utf/
│       └── xi38mono/
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
    │       ├── xi38utf/
    │       └── xi38mono/
    └── woff2/
        ├── xi52woff2/
        │   ├── xi52asc/
        │   ├── xi52utf/
        │   └── xi52mono/
        └── xi38woff2/
            ├── xi38asc/
            ├── xi38utf/
            └── xi38mono/

```

### Suffixes
- `asc` — ASCII-only
- `utf` — Unicode
- `mono` — monospace (built from `utf`)

### File naming examples (Hindi)
- `sfd/xi52sfd/xi52asc/hindixh52asc.sfd`
- `sfd/xi52sfd/xi52utf/hindixh52utf.sfd`
- `sfd/xi52sfd/xi52mono/hindixh52mono.sfd`
- `sfd/xi38sfd/xi38asc/hindixh38asc.sfd`

Note: `xv` → `xh` everywhere (`xh` = xNglohinDi).

---

## 2. Sources vs Targets

### Sources (never overwritten by pipeline)
- `sfdsrc/xe52/xe52asc.sfd` — English master
- `sfdsrc/xh38/xh38asc.sfd` — Hindi xi38 source (manually designed)
- `notofonts/*.ttf` — Noto fallback

### Targets (rebuilt every pipeline run)
- `sfd/xi52sfd/xi52asc/*.sfd`
- `sfd/xi38sfd/xi38asc/*.sfd`
- `sfd/*/xi*utf/*.sfd`
- `sfd/*/xi*mono/*.sfd`

Step 1 (`step0_copy_sources.py`) copies sources into targets
before the build steps run. Sources themselves are never modified.

---

## 3. CSV Format

`glyph_copy.csv` (for xh52) and `glyph_copy_xe38.csv` (for xe38) have
4 columns:

```

e52, src, action, notes

```

- `e52`    — letter (ASCII)
- `src`    — source for that letter: `xe52` / `xe38` / `xh38` /
             `noto` / `noto_math` / `keep`
- `action` — `replace` / `keep` / `manual` / `remove`
- `notes`  — free-form documentation

### Actions
- `replace` — copy from source into target
- `keep`    — leave target glyph as-is
- `manual`  — same as keep
- `remove`  — currently treated as keep

### Example rows

```

k,noto,replace,Indic consonant
x,xh38,replace,Hindi schwa design (अ + small x)
N,xe52,replace,Latin shape
E,noto_math,replace,math ≡
T,keep,keep,Sunny Spells design pending

```

---

## 4. Groups

| Group | Letters | Sources |
|-------|---------|---------|
| G1 | `a i u e o h N R L Y V W P F` (14) | noto (except N, R from xe52) |
| G2 | `x j J q Q v c C g G` (10) | xh38 (Hindi designs) |
| G3 | `N R a i u e o h L Y V W P F` (14) | xe52 (Latin shapes) |
| G4 | `E I O U M X` (6) | noto_math |
| G5 | `A H` (2) | xh38 (Hindi designs) |

Total: 14 + 10 + 14 + 6 + 2 = 46 letters

Note: Actual letter counts depend on each script. Tamil has fewer
consonants, Bengali has no `w`, etc. Scripts gracefully skip letters
that don't exist in their Noto source.

---

## 5. Pipeline (16 steps, 6 phases)

### Phase `src` — sources → targets
1. `[src] copy sources -> targets`

### Phase `asc` — xi38asc + xi52asc
2. `[asc] build xi38asc + xi52asc, 9 scripts (G1-G5)`
3. `[asc] build xi38asc + xi52asc, Sinhala`

### Phase `utf` — xi38utf + xi52utf
4. `[utf] xi38asc -> xi38utf (copy 128 + unicode refs)`
5. `[utf] xi52asc -> xi52utf (copy + refs)`
6. `[utf] add unicode-range refs to xi52utf`
7. `[utf] rename xi52utf internals`

### Phase `mono` — xi52mono  *(WIP, not run in CI)*
8. `[mono] xi52utf -> xi52mono`
9. `[mono] center glyphs in xi52mono`
10. `[mono] fix widths in xi52mono`

### Phase `meta` — font metadata
11. `[meta] update font metadata (Google Fonts format)`

### Phase `gen` — TTF/WOFF2 generation
12. `[gen] TTF/WOFF2 from xi38asc`
13. `[gen] TTF/WOFF2 from xi38utf`
14. `[gen] TTF/WOFF2 from xi52asc`
15. `[gen] TTF/WOFF2 from xi52utf`
16. `[gen] TTF/WOFF2 from xi52mono`

Metadata is stamped on every SFD **before** the `gen` phase, so TTF/WOFF2
carry correct Google Fonts metadata (UniqueID, Copyright, License, Version,
family/full/postscript names).

---

## 6. Commands

Run the whole pipeline:

    fontforge -script scripts/xi52py/main.py

List numbered steps:

    fontforge -script scripts/xi52py/main.py --list

List phase names:

    fontforge -script scripts/xi52py/main.py --list-phases

Run one phase only:

    fontforge -script scripts/xi52py/main.py --phase asc

Resume from a step:

    fontforge -script scripts/xi52py/main.py --from N

Run one step:

    fontforge -script scripts/xi52py/main.py --only N

Skip specific steps:

    fontforge -script scripts/xi52py/main.py --skip 8,9,10

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
8. `--only 12` through `--only 15` (gen)
9. Upload SFDs, TTF/WOFF2, logs as artifacts

Mono steps are not run in CI yet (see Pending).

---

## 8. Pending

- Non-Hindi scripts — G5 designs pending (per-script designers)
- `xi38mono` pipeline — not yet implemented
- Mono phase (steps 8–10, 16) — implemented but not run in CI
- `glyph_sources.csv` — may not be needed (`.csv` already documents)