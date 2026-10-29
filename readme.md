# pff — font pipeline for xnglo unicase(A-Za-z same heights) fonts

python + fontForge pipeline to generate **xnglo unicase** fonts for ten(8+2) indiAn skripts + english.

three families:

- **xi38** — 38-char alphabet (older)
- **xi52** — 52-char alphabet (current)
- **x4i** — xnglo4inglish based on xskii4 (xnglo(Anglo) symbolik kod for information intercenz)

xskii4 encoding xnd fonts bxsed on xskii4:

- **4 finger mxjhs(mAThs)** — 4 fingers countxbles xnd 1 jhumb kaunter
- **4*4=10=wnti=8+8** — xskii4 encoding default mxjhs is 4fingers 1jhumb(Thumb) based.
- **0123456789LYVWPF** — in xskii4 encoding 0123456789LYVWPF are continuos-dedicated 4-finger-mxjhs dizits
- **LYVWPF** — in xi38/xi52/x4i : 9+7 = L+6 = Y+5 = V+4 = W+3 = P+2 = F+1 = 10 = wnti
- **dedicated 4finger-mAThs-dizits** - in xi38/xi52 LYVWPF are dedicated for 4-fingers-mAThss(m4).
- **dedicated-continuous 4finger-mAThs-dizits** - in x4i 0123456789LYVWPF are dedicated-continuous for 4-fingers-mAThss(m4).
- **:;<=>?** in xskii4 encoding glyphs for  :;<=>? are not after 0123456789.

duxl(duAl) wisuxl(visuAl) glyphs of j,q,v,x in xi52/xi38/x4i:

- **duAl wisuxl (visuAl) glyph for x** — in xi52/xi38/x4i x is for mainly A(अ) sound/woice/voice. for ascii(5) compatibilty its glyph looks like (vertically flipped capital-V-glyph + small x glyph inside so that it looks like A/x for अ/अकस-sound/woice/voice)
- **duAl wisuxl (visuAl) glyph for v** — in xi52/xi38/x4i v is for mainly H(ह) sound/woice/voice. for ascii(5) compatibilty its glyph looks like (capital-V-glyph+h-glyph-at-top so that it looks like V/h for व/ह-sound/woice/voice ).
- **duAl wisuxl (visuAl) glyph for j** — in xi52/xi38/x4i j is for mainly T(त) sound/woice/voice. for ascii(5) compatibilty its glyph looks like (↧-glyph so that it looks like T/J).
- **duAl wisuxl (visuAl) glyph for q** — in xi52/xi38/x4i q is for mainly D(द) sound/woice/voice. for ascii(5) compatibilty its glyph also looks like (D-glyph with small \-glyph inside D-glyph so that new-q-glyph looks D/Q ).

## Roles

### Designer (you)
- Maintain `sfdsrc/*.sfd` in FontForge
- Maintain `glyph_copy_xi38.csv` and `glyph_copy_xi52.csv`
- Verify generated fonts (font viewer / browser)
- Iterate: change sfdsrc + CSV, re-run pipeline

### Python pipelines (mechanical)
- Read `sfdsrc/` + CSVs directly (no intermediate copy)
- Compose `asc`, `utf`, `mono`
- Generate TTF/WOFF2
- **Never decide** — only execute

## Structure

    pff/
    ├── sfdsrc/           ← MASTER SOURCES (designer-maintained)
    │   ├── xi38/         per-script sources (xh38, xb38, ..., xs38)
    │   ├── xi52/         per-script sources (xh52, xb52, ..., xs52)
    │   ├── *.csv         glyph copy maps
    │   └── *.md          documentation
    ├── sfd/              ← TARGETS (rebuilt by pipeline)
    │   ├── xi38sfd/      xi38 targets (asc, utf, mono)
    │   └── xi52sfd/      xi52 targets (asc, utf, mono)
    ├── notofonts/        Noto TTFs (fallback)
    ├── pysk/             pipeline scripts
    └── xnglofonts/       TTF/WOFF2 outputs

## CSV files

| File | Purpose |
|------|---------|
| `glyph_copy_xi38.csv` | xi38 glyph copy rules (legacy) |
| `glyph_copy_xi52.csv` | xi52 glyph copy rules (legacy) |
| `glyphs_copy_map38.csv` | xi38 glyph map (all scripts) |
| `glyphs_copy_map52.csv` | xi52 glyph map (all scripts) |
| `glyphs_copy_map38_noto_tu_sfdsrc.csv` | Noto source mapping (all scripts) |
| `glyphs_copyref_map38_for_utf.csv` | copyref mapping for UTF phase |

Details:
- `glyphs_copy_map38_noto_tu_sfdsrc.md` — Noto mapping doc
- `glyphs_copyref_map38_for_utf.md` — copyref mapping doc

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

Full metadata scheme in `pysk/pipeline_design.md` §8.

## Build

    # Full pipeline (needs FontForge)
    fontforge -script pysk/xi52py/main.py

    # List numbered steps
    fontforge -script pysk/xi52py/main.py --list

    # List phase names
    fontforge -script pysk/xi52py/main.py --list-phases

    # Run one phase (src|asc|utf|mono|meta|gen)

    fontforge -script pysk/xi52py/main.py --phase src
    fontforge -script pysk/xi52py/main.py --phase asc

    # Run a single step
    fontforge -script pysk/xi52py/main.py --only 1

    # Dry run (print without executing)
    fontforge -script pysk/xi52py/main.py --dry-run

6 phases (19 steps):
  src   copy xe fonts as-is (no glyph copy)
  asc   xi38asc + xi52asc build
  utf   xi38utf + xi52utf build
  mono  xi38mono + xi52mono build
  meta  font metadata (Google Fonts format)
  gen   TTF/WOFF2 generation

## Releases

Latest: [v1.6.0](https://github.com/zawa8/pff/releases/tag/v1.6.0)

- **66 TTF + 66 WOFF2** (xi38 + xi52 families)
- Download: [xnglo-fonts-v1.6.0.tar.gz](https://github.com/zawa8/pff/releases/download/v1.6.0/xnglo-fonts-v1.6.0.tar.gz)

## Manual design

1. Open a source in FontForge:
   - `sfdsrc/xe52/xe52asc.sfd` (English master)
   - `sfdsrc/xi38/xh38asc.sfd` (Hindi source, example)
2. Edit glyphs
3. Save `.sfd`
4. Run pipeline (or Ctrl+G in FontForge to generate TTF/WOFF2 directly)

Per-script sources live in `sfdsrc/xi38/` (e.g. `xb38asc.sfd` for
Bengali). Pipeline reads them directly — no intermediate copy.

## Sources (never overwritten)

- `sfdsrc/xe52/xe52asc.sfd` — English master
- `sfdsrc/xi38/*.sfd` — per-script sources (Hindi, Bengali, ..., Sinhala)
- `notofonts/*.ttf` — Noto fallback

Python reads `sfdsrc/` directly (no copy into `sfd/`).

## Outputs

- `xnglofonts/ttf/xi38ttf/{xi38asc,xi38utf,xi38mono}/` — TTF files
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
4. Run phase: `asc`
5. Run phase: `utf`
6. Run phase: `mono`
7. Run phase: `meta` (font metadata)
8. Clean old TTF/WOFF2
9. Generate TTF/WOFF2 (`--only 13` through `--only 18`)
10. Upload SFDs, fonts, logs as artifacts

## See also

- `pysk/pipeline_design.md` — full design doc
- `pysk/groups_and_pipelines.md` — G1-G5 groups
- `pysk/utf_design.md` — utf build philosophy

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
