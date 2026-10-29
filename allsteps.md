# pff — allsteps: all pipelines + manual steps

## full flow overview

```
[PIPELINE 1]  NotoSans*.ttf + xe*asc.sfd + noto_map*.csv
              ──────────────────────────────────────────
              noto_copy.py
              ──────────────────────────────────────────
              notosfd/xi38/x*38asc.sfd
              notosfd/xi52/x*52asc.sfd

[MANUAL A]    notosfd/**/*.sfd  ──copy+design──>  sfdsrc/**/*.sfd

[MANUAL B]    update NamesList.txt / asc-to-utf.json / noto_map*.csv

[PIPELINE 2]  sfdsrc/xi38/x*38asc.sfd
              sfdsrc/xi52/x*52asc.sfd
              sfdsrc/asc-to-utf.json
              ──────────────────────────────────────────
              prep_utf.py
              copy_utf_unicode_blocks.py
              verify_utf.py
              main.py --phase mono
              main.py --phase meta
              ──────────────────────────────────────────
              sfd/xi38sfd/xi38asc/   xi38utf/   xi38mono/
              sfd/xi52sfd/xi52asc/   xi52utf/   xi52mono/

[MANUAL C]    check sfd/**/*utf.sfd in FontForge

[MANUAL D]    sfd/**/*.sfd  ──copy+final-design──>  sfdfinal/**/*.sfd

[MANUAL E]    check sfdfinal/**/*.sfd in FontForge

[PIPELINE 3]  sfdfinal/**/*.sfd
              ──────────────────────────────────────────
              p5generate.py
              ──────────────────────────────────────────
              xnglofonts/ttf/**/*.ttf
              xnglofonts/woff2/**/*.woff2

[MANUAL F]    publish to GitHub release + jsDelivr CDN
```

---

## pipeline 1 — noto → notosfd

**purpose**: copy glyphs from NotoSans TTF fonts into source SFD files.

**inputs**:
- `pysk/notopy/NotoSans*-Regular.ttf` (10 Indic script Noto fonts)
- `notosfd/xi38/xe38asc.sfd` — shared base glyphs for xi38 (vowels, marks, etc.)
- `notosfd/xi52/xe52asc.sfd` — shared base glyphs for xi52
- `pysk/notopy/noto_map_38.csv` — glyph map: NotoSans codepoint → xi38asc ASCII slot
- `pysk/notopy/noto_map_52.csv` — glyph map: NotoSans codepoint → xi52asc ASCII slot

**csv cell values**:
- `0915` (hex) = copy that NotoSans glyph to this ASCII slot
- `xe38asc` = copy from xe38asc.sfd instead of NotoSans
- `skip` = do not copy anything to this slot

**run**:
```bash
ffz pysk/notopy/noto_copy.py           # both xi38 + xi52
ffz pysk/notopy/noto_copy.py xi38      # xi38 only
ffz pysk/notopy/noto_copy.py xi52      # xi52 only
ffz pysk/notopy/noto_copy.py xh38      # one font only
```

**log**: `logs/noto_copy.log`

**outputs**: `notosfd/xi38/x*38asc.sfd` and `notosfd/xi52/x*52asc.sfd`

---

## [MANUAL A] — notosfd → sfdsrc (copy + glyph design)

**who**: each script designer for their language.

| font prefix | script | language |
|-------------|--------|----------|
| xh* | Devanagari | Hindi |
| xb* | Bengali | Bengali |
| xp* | Gurmukhi | Punjabi |
| xg* | Gujarati | Gujarati |
| xo* | Odia | Odia |
| xt* | Tamil | Tamil |
| xj* | Telugu | Telugu |
| xk* | Kannada | Kannada |
| xm* | Malayalam | Malayalam |
| xs* | Sinhala | Sinhala |

**steps**:
1. copy `notosfd/xi38/*.sfd` → `sfdsrc/xi38/`
2. copy `notosfd/xi52/*.sfd` → `sfdsrc/xi52/`
3. open each `sfdsrc/xi38/x*38asc.sfd` in FontForge
4. review + modify glyphs as needed for that script
5. save

> **important**: `sfdsrc/` is **read-only for all python scripts** — only human designers edit here.

---

## [MANUAL B] — update mapping files

update these when glyph assignments change:

| file | purpose |
|------|---------|
| `pysk/notopy/NamesList.txt` | unicode codepoint → hskii char (source of truth) |
| `sfdsrc/asc-to-utf.json` | ascii char → unicode offset per script (for pipeline 2) |
| `pysk/notopy/noto_map_38.csv` | NotoSans codepoint → xi38asc ASCII slot (for pipeline 1) |
| `pysk/notopy/noto_map_52.csv` | NotoSans codepoint → xi52asc ASCII slot (for pipeline 1) |

**regenerate json/csv from NamesList.txt**:
```bash
python3 pysk/xi52py/gen_asc_to_utf_json.py   # regenerates sfdsrc/asc-to-utf.json
python3 pysk/notopy/gen_notottf_csv.py        # regenerates noto_map_38.csv
```

**analysis tool** (Excel workbook — glyph details from NotoSans for review):
```bash
ffz pysk/notopy/extract_noto_data.py       # exports pffsheets/noto_data/*.csv
python3 pysk/notopy/gen_noto_sheets.py     # builds pffsheets/noto_glyph_sheets.xlsx
```
- 🟢 green row = glyph exists in NotoSans
- 🟠 orange = empty/clear glyph
- 🟡 yellow = mismatch between NamesList.txt and asc-to-utf.json (needs fix)

---

## pipeline 2 — sfdsrc → sfd (utf + mono font generation)

### step 2.1 — prep_utf

```bash
ffz pysk/xi52py/prep_utf.py
```

does all of:
- `sfdsrc/xi38/*.sfd` → `sfd/xi38sfd/xi38asc/` (copy)
- `sfdsrc/xi52/*.sfd` → `sfd/xi52sfd/xi52asc/` (copy)
- clears `sfd/xi38sfd/xi38utf/` and `sfd/xi52sfd/xi52utf/`
- `sfdsrc/xi38/*asc.sfd` → `sfd/xi38sfd/xi38utf/*utf.sfd` (copy + rename)
- `sfdsrc/xi52/*asc.sfd` → `sfd/xi52sfd/xi52utf/*utf.sfd` (copy + rename)
- updates font metadata (`fontname`/`familyname`: `asc` → `utf`)
- updates sfnt name table (unique-id, version string)
- adds unicode glyph refs to `xh38utf.sfd` only (reads `sfdsrc/asc-to-utf.json`)

log: `logs/prep_utf.log`

### step 2.2 — copy unicode blocks

```bash
py pysk/xi52py/copy_utf_unicode_blocks.py
```

copies `StartChar: uni0904` ... to end-of-file  
from `xh38utf.sfd` → all other `*utf.sfd` files (xb38, xg38, ... xs38).

### step 2.3 — verify

```bash
ffz pysk/xi52py/verify_utf.py
echo $?    # must be 0
```

expected: `824 ref glyphs, 0 collapsed` for all 10 fonts.

### step 2.4 — mono phase

```bash
ffz pysk/xi52py/main.py --phase mono
```

generates xi38mono and xi52mono (fixed-width, centered glyphs) from utf fonts.

### step 2.5 — meta phase

```bash
ffz pysk/xi52py/main.py --phase meta
```

updates font family names and PostScript names (Google Fonts format) in all SFDs.

---

## [MANUAL C] — check sfd/**/*utf.sfd in FontForge

open `sfd/xi38sfd/xi38utf/xh38utf.sfd` and verify:
- U+0915 (क Devanagari ka) → shows क glyph ✓
- U+0985 (অ Bengali a) → shows correct glyph ✓
- U+0900–U+0903 (combining marks) → empty/clear ✓
- glyph width and alignment correct

---

## [MANUAL D] — sfd → sfdfinal (copy + designer final review)

1. copy `sfd/xi38sfd/` → `sfdfinal/xi38sfd/`
2. copy `sfd/xi52sfd/` → `sfdfinal/xi52sfd/`
3. each designer opens their `sfdfinal/**/x*utf.sfd` in FontForge
4. makes final glyph adjustments in unicode ranges if needed
5. saves to `sfdfinal/`

**who does what**:
- Hindi speaker → `sfdfinal/**/xh*utf.sfd` (Devanagari glyphs)
- Bengali designer → `sfdfinal/**/xb*utf.sfd`
- Tamil designer → `sfdfinal/**/xt*utf.sfd`
- etc.

---

## [MANUAL E] — final check of sfdfinal/**/*.sfd

review all fonts in FontForge before generating TTF/WOFF2.  
check unicode ranges + asc glyphs look correct for each script.

---

## pipeline 3 — sfdfinal → TTF/WOFF2

```bash
ffz pysk/xi52py/p5generate.py
```

reads `sfdfinal/**/*.sfd` → generates:
- `xnglofonts/ttf/xi38ttf/xi38asc/*.ttf`
- `xnglofonts/ttf/xi38ttf/xi38utf/*.ttf`
- `xnglofonts/ttf/xi38ttf/xi38mono/*.ttf`
- `xnglofonts/ttf/xi52ttf/**/*.ttf`
- `xnglofonts/woff2/**/*.woff2`

log: `logs/p5generate.log`

---

## [MANUAL F] — publish fonts

### github release
```bash
# tag a version
git tag v1.x.x
git push origin v1.x.x
# github actions release.yml runs automatically → creates GitHub Release with zip
```

### jsdelivr CDN
after GitHub release is created, fonts are auto-available at:
```
https://cdn.jsdelivr.net/gh/zawa8/pff@v1.x.x/xnglofonts/ttf/xi38ttf/xi38utf/xh38utf.ttf
https://cdn.jsdelivr.net/gh/zawa8/pff@v1.x.x/xnglofonts/woff2/xi38woff2/xi38utf/xh38utf.woff2
```

CSS usage:
```css
@font-face {
  font-family: 'XngloHindi';
  src: url('https://cdn.jsdelivr.net/gh/zawa8/pff@v1.x.x/xnglofonts/woff2/xi38woff2/xi38utf/xh38utf.woff2') format('woff2'),
       url('https://cdn.jsdelivr.net/gh/zawa8/pff@v1.x.x/xnglofonts/ttf/xi38ttf/xi38utf/xh38utf.ttf') format('truetype');
}
```

---

## quick reference — all commands

```bash
# ── pipeline 1 ──────────────────────────────────────────
ffz pysk/notopy/noto_copy.py

# ── pipeline 2 ──────────────────────────────────────────
ffz pysk/xi52py/prep_utf.py
py  pysk/xi52py/copy_utf_unicode_blocks.py
ffz pysk/xi52py/verify_utf.py && echo "utf ok"
ffz pysk/xi52py/main.py --phase mono
ffz pysk/xi52py/main.py --phase meta

# ── pipeline 3 ──────────────────────────────────────────
ffz pysk/xi52py/p5generate.py

# ── helper scripts ───────────────────────────────────────
python3 pysk/xi52py/gen_asc_to_utf_json.py   # regen asc-to-utf.json
python3 pysk/notopy/gen_notottf_csv.py        # regen noto_map_38.csv
ffz     pysk/notopy/extract_noto_data.py      # noto glyph → csv
python3 pysk/notopy/gen_noto_sheets.py        # csv → excel workbook

# ── check pipeline 2 step list ──────────────────────────
ffz pysk/xi52py/main.py --list

# ── publish ─────────────────────────────────────────────
git tag v1.x.x && git push origin v1.x.x
```

---

## ci/cd — github actions

`.github/workflows/build-xi52.yml`  
runs on every push to `main`:
```
Verify syntax → asc phase → utf phase → copy_utf_unicode_blocks
→ verify_utf → mono → meta → gen → upload artifacts
```

`.github/workflows/release.yml`  
runs on git tag `v*`:
```
checkout → collect xnglofonts → zip → create GitHub Release
```

---

## folder structure

```
pff/
├── pysk/
│   ├── notopy/            pipeline 1 scripts + NotoSans TTFs + NamesList
│   └── xi52py/            pipeline 2+3 scripts
├── notosfd/               pipeline 1 output (DO NOT EDIT MANUALLY)
│   ├── xi38/
│   └── xi52/
├── sfdsrc/                designer source (READ-ONLY for python scripts)
│   ├── xi38/
│   ├── xi52/
│   └── asc-to-utf.json
├── sfd/                   pipeline 2 output
│   ├── xi38sfd/xi38asc/
│   ├── xi38sfd/xi38utf/
│   ├── xi38sfd/xi38mono/
│   └── xi52sfd/...
├── sfdfinal/              designer final review copy → input for pipeline 3
│   ├── xi38sfd/
│   └── xi52sfd/
├── xnglofonts/            pipeline 3 output (TTF + WOFF2)
├── pffsheets/             analysis worksheets (Excel)
└── allsteps.md            this file
```
