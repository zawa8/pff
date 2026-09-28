# pff — Font Pipeline for xnglo

Python + FontForge pipeline to generate **xnglo** fonts for 11 Indian
scripts + English.

Two families:

- **xi38** — 38-char alphabet (older)
- **xi52** — 52-char alphabet (current)

## Structure

    pff/
    ├── sfdsrc/           ← MASTER SOURCES (never overwritten)
    │   ├── xe52/         English master (xe52asc.sfd)
    │   ├── xh38/         Hindi xi38 source (xh38asc.sfd)
    │   ├── xi38/         future per-script sources (xi38/xh38asc.sfd, ...)
    │   └── scripts/      future design scripts
    ├── sfd/              ← TARGETS (rebuilt by pipeline)
    │   ├── xi52sfd/      xi52 targets (asc, utf, mono)
    │   └── xi38sfd/      xi38 targets (asc, utf)
    ├── notofonts/        Noto TTFs (fallback)
    ├── scripts/          pipeline scripts
    └── xnglofonts/       TTF/WOFF2 outputs

## Font naming

Prefix table (technical names in filenames):

| Script    | Prefix | Family (sfnt)                        |
|-----------|--------|--------------------------------------|
| English   | xe     | Xnglo English xi38/xi52 asc/utf/mono |
| Hindi     | xh     | Xnglo Hindi xi38/xi52 asc/utf/mono   |
| Bengali   | xb     | Xnglo Bengali xi38/xi52 asc/utf/mono |
| Punjabi   | xp     | Xnglo Punjabi xi38/xi52 asc/utf/mono |
| Gujarati  | xg     | Xnglo Gujarati xi38/xi52 asc/utf/mono|
| Oriya     | xo     | Xnglo Oriya xi38/xi52 asc/utf/mono   |
| Tamil     | xt     | Xnglo Tamil xi38/xi52 asc/utf/mono   |
| Telugu    | xj     | Xnglo Telugu xi38/xi52 asc/utf/mono  |
| Kannada   | xk     | Xnglo Kannada xi38/xi52 asc/utf/mono |
| Malayalam | xm     | Xnglo Malayalam xi38/xi52 asc/utf/mono|
| Sinhala   | xs     | Xnglo Sinhala xi38/xi52 asc/utf/mono |

PostScript names follow the pattern
`Xnglo<Script>-xi<38|52><variant>` (e.g. `XngloHindi-xi38asc`).

Full metadata scheme in `scripts/pipeline_design.md` §8.

## Build

    # Full pipeline (needs FontForge)
    fontforge -script scripts/xi52py/main.py

    # List numbered steps
    fontforge -script scripts/xi52py/main.py --list

    # List phase names
    fontforge -script scripts/xi52py/main.py --list-phases

    # Run one phase (src|asc|utf|mono|meta|gen)
    fontforge -script scripts/xi52py/main.py --phase asc

    # Run a single step
    fontforge -script scripts/xi52py/main.py --only 2

    # Dry run (print without executing)
    fontforge -script scripts/xi52py/main.py --dry-run

6 phases:
  src   sources -> targets
  asc   xi38asc + xi52asc build
  utf   xi38utf + xi52utf build
  mono  xi52mono build (WIP, not in CI)
  meta  font metadata (Google Fonts format)
  gen   TTF/WOFF2 generation

## Manual design

1. Open a source in FontForge:
   - `sfdsrc/xe52/xe52asc.sfd` (English master)
   - `sfdsrc/xi38/xh38asc.sfd` (Hindi source, example)
2. Edit glyphs
3. Save `.sfd`
4. Run pipeline (or Ctrl+G in FontForge to generate TTF/WOFF2 directly)

New per-script sources will live in `sfdsrc/xi38/`, e.g.
`sfdsrc/xi38/xb38asc.sfd` for Bengali.

## Sources (never overwritten)

- `sfdsrc/xe52/xe52asc.sfd` — English master
- `sfdsrc/xi38/xh38asc.sfd` — Hindi xi38 source
- `notofonts/*.ttf` — Noto fallback

Future per-script sources will live in `sfdsrc/xi38/`.

## Outputs

- `xnglofonts/ttf/xi38ttf/{xi38asc,xi38utf}/`          — TTF files
- `xnglofonts/ttf/xi52ttf/{xi52asc,xi52utf,xi52mono}/` — TTF files
- `xnglofonts/woff2/.../`                              — WOFF2 (same layout)

Fonts are tracked in-repo so users can download directly from
`https://raw.githubusercontent.com/zawa8/pff/main/xnglofonts/...`
and versioned with git tags.

## Versioning

Each release is tagged (`v1.3.1`, etc.). The version string embedded
in the fonts is taken from the latest git tag by
`update_font_metadata.py` (e.g. `Version 1.3.1`).

## GitHub Actions

`.github/workflows/build-xi52.yml` runs on push to `main` and on PRs:

1. Install FontForge
2. Verify Python syntax (`py_compile`)
3. Sanity check (`main.py --list`)
4. Run phases: `src`, `asc`
5. Run phase: `utf`
6. Run phase: `meta` (font metadata)
7. Clean old TTF/WOFF2
8. Generate ASC + UTF TTF/WOFF2
9. Upload SFDs, fonts, logs as artifacts

## See also

- `scripts/pipeline_design.md` — full design doc
- `scripts/groups_and_pipelines.md` — G1-G5 groups
- `hskii-encoding-analysis.md` — encoding scheme

## Related

- [linguist](https://github.com/zawa8/linguist) — Firefox extension
- [fontsource](https://github.com/fontsource) — font CDN

## Deprecated

- [zawa8/font](https://github.com/zawa8/font) — superseded by `xnglofonts/` in this repo

## Download

Fonts live in this repo:

- TTF: `xnglofonts/ttf/`
- WOFF2: `xnglofonts/woff2/`

### jsDelivr CDN (recommended)

Versioned URLs (immutable, fast, global):

    https://cdn.jsdelivr.net/gh/zawa8/pff@v1.3.1/xnglofonts/woff2/xi38woff2/xi38asc/xh38asc.woff2

Always-latest (main branch):

    https://cdn.jsdelivr.net/gh/zawa8/pff@main/xnglofonts/woff2/xi38woff2/xi38asc/xh38asc.woff2

### Direct from GitHub

    https://raw.githubusercontent.com/zawa8/pff/main/xnglofonts/ttf/xi38ttf/xi38asc/xh38asc.ttf

Versioned with git tags (`v1.3.1`, etc.).

### CSS example

    @font-face {
      font-family: 'Xnglo Hindi xi38 asc';
      src: url('https://cdn.jsdelivr.net/gh/zawa8/pff@v1.3.1/xnglofonts/woff2/xi38woff2/xi38asc/xh38asc.woff2') format('woff2'),
           url('https://cdn.jsdelivr.net/gh/zawa8/pff@v1.3.1/xnglofonts/ttf/xi38ttf/xi38asc/xh38asc.ttf') format('truetype');
      font-display: swap;
    }