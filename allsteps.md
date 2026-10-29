# pff — all steps / pipelines

## overview

```
NotoSans*.ttf
xe38asc.sfd / xe52asc.sfd      ← pipeline 1 (noto_copy.py)
noto_map_38.csv / noto_map_52.csv
        │
        ▼
notosfd/xi38/x*38asc.sfd
notosfd/xi52/x*52asc.sfd        ← [MANUAL A] copy + glyph design
        │
        ▼
sfdsrc/xi38/x*38asc.sfd
sfdsrc/xi52/x*52asc.sfd         ← [MANUAL B] update csv/json maps
        │
        ▼  pipeline 2 (prep_utf.py)
sfd/xi38sfd/xi38asc/            (readonly reference copy)
sfd/xi52sfd/xi52asc/
sfd/xi38sfd/xi38utf/xh38utf.sfd ← unicode refs added (xh38 only)
sfd/xi52sfd/xi52utf/
        │
        ▼  copy_utf_unicode_blocks.py
all *utf.sfd files              ← unicode blocks copied from xh38utf
        │
        ▼  main.py --phase mono/meta
sfd/xi38sfd/xi38mono/
sfd/xi52sfd/xi52mono/
        │
        ▼  [MANUAL C] check in FontForge
        │
        ▼  [MANUAL D] copy + designer review
sfdfinal/xi38sfd/xi38asc/
sfdfinal/xi38sfd/xi38utf/
sfdfinal/xi38sfd/xi38mono/
sfdfinal/xi52sfd/...
        │
        ▼  [MANUAL E] final check in FontForge
        │
        ▼  pipeline 3 (p5generate.py)
xnglofonts/ttf/.../*.ttf
xnglofonts/woff2/.../*.woff2
```

---

## pipeline 1 — noto → notosfd

**purpose**: copy glyphs from NotoSans fonts into source SFD files.

**inputs**:
- `pysk/notopy/NotoSans*-Regular.ttf` (10 Indic script fonts)
- `notosfd/xi38/xe38asc.sfd` — shared base glyphs (vowels, marks) for xi38
- `notosfd/xi52/xe52asc.sfd` — shared base glyphs for xi52
- `pysk/notopy/noto_map_38.csv` — glyph map for xi38 (which NotoSans codepoint → which ASCII slot)
- `pysk/notopy/noto_map_52.csv` — glyph map for xi52

**run**:
```bash
ffz pysk/notopy/noto_copy.py           # both xi38 + xi52
ffz pysk/notopy/noto_copy.py xi38      # xi38 only
ffz pysk/notopy/noto_copy.py xh38      # one font only
```

**outputs**: `notosfd/xi38/x*38asc.sfd` and `notosfd/xi52/x*52asc.sfd`

**log**: `logs/noto_copy.log`

---

## [MANUAL A] — notosfd → sfdsrc (copy + glyph design)

**who**: each script designer for their language.

| font prefix | script | designer |
|-------------|--------|----------|
| xh* | Hindi/Devanagari | Hindi speaker |
| xb* | Bengali | Bengali designer |
| xp* | Punjabi/Gurmukhi | Punjabi designer |
| xg* | Gujarati | Gujarati designer |
| xo* | Odia | Odia designer |
| xt* | Tamil | Tamil designer |
| xj* | Telugu | Telugu designer |
| xk* | Kannada | Kannada designer |
| xm* | Malayalam | Malayalam designer |
| xs* | Sinhala | Sinhala designer |

**steps**:
1. copy `notosfd/xi38/*.sfd` → `sfdsrc/xi38/`
2. copy `notosfd/xi52/*.sfd` → `sfdsrc/xi52/`
3. open each `sfdsrc/xi38/x*38asc.sfd` in FontForge
4. review and modify glyphs as needed for that script
5. save

**note**: `sfdsrc/` is **read-only** for all python scripts — only humans edit here.

---

## [MANUAL B] — update mapping files

update these files when glyph assignments change:

| file | purpose | how to regenerate |
|------|---------|------------------|
| `pysk/notopy/NamesList.txt` | unicode codepoint → hskii char | edit manually |
| `sfdsrc/asc-to-utf.json` | ascii char → unicode offset per script | `python3 pysk/xi52py/gen_asc_to_utf_json.py` |
| `pysk/notopy/noto_map_38.csv` | noto TTF codepoint → xi38asc ASCII slot | `python3 pysk/notopy/gen_notottf_csv.py` |
| `pysk/notopy/noto_map_52.csv` | noto TTF codepoint → xi52asc ASCII slot | edit manually |

**analysis tool** (Excel workbook with 10 sheets — glyph details from NotoSans):
```bash
ffz pysk/notopy/extract_noto_data.py      # extract data to pffsheets/noto_data/*.csv
python3 pysk/notopy/gen_noto_sheets.py    # build pffsheets/noto_glyph_sheets.xlsx
```

---

## pipeline 2 — sfdsrc → sfd (utf/mono font generation)

### step 2.1 — prep_utf (sfdsrc → sfd, unicode refs)

```bash
ffz pysk/xi52py/prep_utf.py
```

does:
- `sfdsrc/xi38/*.sfd` → `sfd/xi38sfd/xi38asc/` (copy)
- `sfdsrc/xi52/*.sfd` → `sfd/xi52sfd/xi52asc/` (copy)
- clears `sfd/xi38sfd/xi38utf/` and `sfd/xi52sfd/xi52utf/`
- `sfdsrc/xi38/*asc.sfd` → `sfd/xi38sfd/xi38utf/*utf.sfd` (copy + rename)
- `sfdsrc/xi52/*asc.sfd` → `sfd/xi52sfd/xi52utf/*utf.sfd` (copy + rename)
- updates font metadata (familyname/fontname: asc → utf)
- adds unicode glyph refs to `xh38utf.sfd` only (reads `sfdsrc/asc-to-utf.json`)

log: `logs/prep_utf.log`

### step 2.2 — copy unicode blocks to all utf fonts

```bash
python3 pysk/xi52py/copy_utf_unicode_blocks.py
```

copies `StartChar: uni0900` ... to end-of-file from `xh38utf.sfd` → all other `*utf.sfd` files.

### step 2.3 — verify utf refs

```bash
ffz pysk/xi52py/verify_utf.py
echo $?    # must be 0
```

### step 2.4 — mono phase

```bash
ffz pysk/xi52py/main.py --phase mono
```

generates xi38mono and xi52mono from utf fonts (fixed-width, centered glyphs).

### step 2.5 — meta phase

```bash
ffz pysk/xi52py/main.py --phase meta
```

updates Google Fonts format metadata in all SFDs.

---

## [MANUAL C] — check sfd/**/*utf.sfd in FontForge

open sample fonts and verify:
- U+0915 (क Devanagari ka) has correct shape
- U+0985 (অ Bengali a) has correct shape
- combining marks (U+0900-U+0903) are empty/clear
- glyph width and alignment look correct

---

## [MANUAL D] — sfd → sfdfinal (copy + designer final review)

1. copy `sfd/xi38sfd/` → `sfdfinal/xi38sfd/`
2. copy `sfd/xi52sfd/` → `sfdfinal/xi52sfd/`
3. each designer opens their `sfdfinal/**/x*utf.sfd` in FontForge
4. makes final glyph adjustments if needed
5. saves to `sfdfinal/`

---

## [MANUAL E] — final check of sfdfinal/**/*.sfd

review all fonts in FontForge before generating TTF/WOFF2.

---

## pipeline 3 — sfdfinal → TTF/WOFF2

```bash
ffz pysk/xi52py/p5generate.py
```

reads `sfdfinal/**/*.sfd` → generates:
- `xnglofonts/ttf/**/*.ttf`
- `xnglofonts/woff2/**/*.woff2`

log: `logs/p5generate.log`

---

## ci/cd (github actions)

`.github/workflows/build-xi52.yml` runs **pipeline 2 only** on every push to main:
- phases: utf → verify → copy_utf_unicode_blocks → mono → meta → gen
- uploads artifacts: `sfd/`, `xnglofonts/`, `logs/`

---

## quick reference — common commands

```bash
# pipeline 1
ffz pysk/notopy/noto_copy.py

# pipeline 2 (full utf regeneration)
ffz pysk/xi52py/prep_utf.py
python3 pysk/xi52py/copy_utf_unicode_blocks.py
ffz pysk/xi52py/verify_utf.py
ffz pysk/xi52py/main.py --phase mono
ffz pysk/xi52py/main.py --phase meta

# pipeline 3
ffz pysk/xi52py/p5generate.py

# regenerate json/csv maps
python3 pysk/xi52py/gen_asc_to_utf_json.py
python3 pysk/notopy/gen_notottf_csv.py

# noto analysis sheets
ffz pysk/notopy/extract_noto_data.py
python3 pysk/notopy/gen_noto_sheets.py

# check pipeline 2 step list
ffz pysk/xi52py/main.py --list
```
