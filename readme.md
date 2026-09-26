# pff — Font Pipeline for xnglo

Python + FontForge pipeline to generate **xnglo** fonts for 11 Indian
scripts + English.

Two families:

- **xi38** — 38-char alphabet (older)
- **xi52** — 52-char alphabet (current)

## Structure

    pff/
    ├── sfdsrc/           ← MASTER SOURCES (never overwritten)
    │   ├── xe52/         English xi52 (xe52asc.sfd)
    │   ├── xh38/         Hindi xi38 (xh38asc.sfd)
    │   └── scripts/      future design scripts
    ├── sfd/              ← TARGETS (rebuilt by pipeline)
    │   ├── xi52sfd/      xi52 targets (asc, utf, mono)
    │   └── xi38sfd/      xi38 targets (asc, utf, mono)
    ├── notofonts/        Noto TTFs (fallback)
    ├── scripts/          pipeline scripts
    └── xnglofonts/       TTF/WOFF2 outputs

## Font naming

| Script    | Prefix | Family                  |
|-----------|--------|-------------------------|
| English   | xe     | xe52asc / xe38asc       |
| Hindi     | xh     | xh52asc / xh38asc       |
| Bengali   | xb     | xb52asc / xb38asc       |
| Punjabi   | xp     | xp52asc / xp38asc       |
| Gujarati  | xg     | xg52asc / xg38asc       |
| Oriya     | xo     | xo52asc / xo38asc       |
| Tamil     | xt     | xt52asc / xt38asc       |
| Telugu    | xj     | xj52asc / xj38asc       |
| Kannada   | xk     | xk52asc / xk38asc       |
| Malayalam | xm     | xm52asc / xm38asc       |
| Sinhala   | xs     | xs52asc / xs38asc       |

## Build

    # Full pipeline (needs FontForge)
    fontforge -script scripts/xi52py/main.py

    # List steps
    fontforge -script scripts/xi52py/main.py --list

    # Run single step
    fontforge -script scripts/xi52py/main.py --only 2

## Manual design

1. Open `sfdsrc/xe52/xe52asc.sfd` or `sfdsrc/xh38/xh38asc.sfd` in FontForge
2. Edit glyphs
3. Save `.sfd`
4. Run pipeline (or Ctrl+G in FontForge to generate TTF/WOFF2 directly)

## Sources (never overwritten)

- `sfdsrc/xe52/xe52asc.sfd` — English master
- `sfdsrc/xh38/xh38asc.sfd` — Hindi xi38 source
- `notofonts/*.ttf` — Noto fallback

## Outputs

- `xnglofonts/ttf/` — TTF files
- `xnglofonts/woff2/` — WOFF2 files

## GitHub Actions

`.github/workflows/build-xi52.yml` runs on push:

1. Sources → targets
2. Build ASC (xi38asc + xi52asc)
3. Update font metadata
4. Clean old fonts
5. Generate TTF/WOFF2
6. Upload artifacts

## See also

- `scripts/pipeline_design.md` — full design doc
- `scripts/groups_and_pipelines.md` — G1-G5 groups
- `hskii-encoding-analysis.md` — encoding scheme

## Related

- [linguist](https://github.com/zawa8/linguist) — Firefox extension
- [font](https://github.com/zawa8/font) — generated fonts repo
- [hscii](https://hscii.vercel.app) / [hfont](https://hfont.vercel.app) — web apps
- [fontsource](https://github.com/fontsource) — font CDN
