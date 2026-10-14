# xnglo Fonts — Glyph Sources & Types

Documentation for the xnglo font family: 2 series × 3 categories × 11 fonts = 66 fonts.

## Structure

**2 series:** `x38` (38 series), `x52` (52 series)

**3 categories per series:**
- `asc` — master source
- `utf` — derived from `asc` (`asc → utf`: copy 52 + Indic Unicode refs)
- `mono` — derived from `asc` (`asc → mono`: copy 52 + equal width + center-align)

**11 fonts per (series × category):**

| Code | Script | Region |
|------|--------|--------|
| `xe` | English | Latin/English master |
| `xh` | Hindi | India |
| `xb` | Bengali | India |
| `xg` | Gujarati | India |
| `xp` | Punjabi (Gurmukhi) | India |
| `xo` | Oriya | India |
| `xt` | Tamil | India |
| `xj` | Telugu | India |
| `xk` | Kannada | India |
| `xm` | Malayalam | India |
| `xs` | Sinhala | Sri Lanka |

**9 India:** `xh xb xg xp xo xt xj xk xm`
**1 Sri Lanka:** `xs`
**1 English:** `xe`

**Total:** 2 × 3 × 11 = **66 `.sfd` files** → **66 TTF + 66 WOFF2 = 132 fonts** in `xnglofonts/`.

---

## Glyph Types (5)

### 1. Copied Latin glyphs (from Sunny Spells unicase)

| Glyphs | Series | Count |
|--------|--------|-------|
| `a i u e o h k z t d n p f b m y r l w s Y V W P F` | 38 + 52 | 26 |
| `E I O U M X` | 52 only | 6 |

### 2. Designed Latin glyphs (custom)

| Glyphs | Series | Count | Status |
|--------|--------|-------|--------|
| `N R L` | 38 + 52 | 3 | designed and fixed |
| `x A v H` | 52 | 4 | design changed but not fixed |
| `c C g G` | 52 | 4 | designed and fixed |
| `j J q Q` | 52 | 4 | designed and fixed |
| `E I O U M X` | 38 | 6 | designed (38 series specific) |

### 3. Copied Unicode Indic glyphs (from Noto Indic)

| Glyphs | Series | Scripts |
|--------|--------|---------|
| `k z t d T D n p f b m y r l w s` | 38 + 52 | all 10 Indic (9 India + 1 Sri Lanka) |

Source: `notofonts/NotoSans<Script>-Regular.ttf` per script.

### 4. Designed Indic glyphs (custom, per script)

| Glyphs | Series | Scripts |
|--------|--------|---------|
| `c C g G j J q Q x A v H` | **38 only** | all 10 Indic (9 India + 1 Sri Lanka) |

**52 series has no designed Indic glyphs** — all Indic chars are copied from Noto.

Source: `sfdsrc/xi38/<script>38asc.sfd` (per-script designed glyphs).

### 5. `xe` fonts (English only)

`xe38` / `xe52` have **no Indic glyphs** — all Latin (copied + designed).

---

## Per-Series Summary

### 52 series (`x*52`)

| Source | Glyphs | Count |
|--------|--------|-------|
| `xe52` — copied Latin | `a i u e o h k z t d n p f b m y r l w s Y V W P F E I O U M X` | 32 |
| `xe52` — designed Latin | `N R L x A v H c C g G j J q Q` | 14 |
| `ownsfd` — copied Indic (Noto) | `k z t d T D n p f b m y r l w s` | 16 |
| `ownsfd` — designed Indic | — | **0** |

Total: 32 + 14 + 16 + 0 = 62 (52 expected; 10 overlap across groups)

See `sfdsrc/csv_details.md` for canonical mapping.

### 38 series (`x*38`)

| Source | Glyphs | Count |
|--------|--------|-------|
| `xe38` — copied Latin | `a i u e o h k z t d n p f b m y r l w s Y V W P F` | 26 |
| `xe38` — designed Latin | `N R L E I O U M X` | 9 |
| `ownsfd` — copied Indic (Noto) | `k z t d T D n p f b m y r l w s` | 16 |
| `ownsfd` — designed Indic | `c C g G j J q Q x A v H` | 12 |

See `sfdsrc/csv_details.md` for canonical mapping.

---

## Sources

- **Latin master:** `sfdsrc/xi38/xe38asc.sfd`, `sfdsrc/xi52/xe52asc.sfd`
- **Indic masters:** `sfdsrc/xi38/<script>38asc.sfd`, `sfdsrc/xi52/<script>52asc.sfd`
- **Noto fallback:** `notofonts/`
- **CSV decisions:** `sfdsrc/glyph_copy_xi38.csv`, `sfdsrc/glyph_copy_xi52.csv`
- **Canonical mapping:** `sfdsrc/csv_details.md`

## Generated Outputs

- `sfd/xi38sfd/{xi38asc,xi38utf,xi38mono}/*.sfd`
- `sfd/xi52sfd/{xi52asc,xi52utf,xi52mono}/*.sfd`
- `xnglofonts/ttf/{xi38ttf,xi52ttf}/{xi38asc,xi38utf,xi38mono}/*.ttf`
- `xnglofonts/woff2/{xi38woff2,xi52woff2}/{xi38asc,xi38utf,xi38mono}/*.woff2`

## Pipeline

See `pysk/pipeline_design.md` for the 18-step pipeline.
