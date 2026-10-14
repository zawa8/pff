# Glyph Copy Logic — `build_asc_fonts.py`

Technical documentation for how the asc-build pipeline copies glyphs from master sources into `sfd/` targets, driven by per-family CSVs.

## Overview

`build_asc_fonts.py` reads two CSVs:

- `sfdsrc/glyph_copy_xi38.csv` — decisions for 38 series
- `sfdsrc/glyph_copy_xi52.csv` — decisions for 52 series

For each script (english, hindi, bengali, ...), it opens:

- the per-series master sources (`xe38` / `xe52`, and per-script `<script>38asc.sfd` / `<script>52asc.sfd`)
- the `sfd/` targets (`sfd/xi38sfd/xi38asc/<script>38asc.sfd`, `sfd/xi52sfd/xi52asc/<script>52asc.sfd`)

Then, for each CSV row, it applies the decision and writes back the target.

## CSV Format

```
e52, src, action, notes
```

| Column | Meaning |
|--------|---------|
| `e52`  | Letter (ASCII slot 0x00–0xFF) |
| `src`  | Where to take the glyph from |
| `action` | What to do |
| `notes` | Free-form documentation |

Lines starting with `#` are comments. The header line (`e52,...`) is skipped.

## Actions

| Action | Behavior |
|--------|----------|
| `replace` | Copy glyph from `src` into target |
| `keep`    | Leave target glyph as-is (skip copy) |
| `manual`  | Same as `keep` (reserved for hand-drawn glyphs) |
| `remove`  | Currently treated as `keep` |

**Note:** `keep` means "don't touch this glyph in `sfd/`". The target's existing glyph remains unchanged.

## Source Types

| `src` | Meaning |
|-------|---------|
| `xe52` | Copy from `sfdsrc/xi52/xe52asc.sfd` (52 Latin master) |
| `xe38` | Copy from `sfdsrc/xi38/xe38asc.sfd` (38 Latin master) |
| `ownsfd` | Copy from current script's `sfdsrc/<series>/<script><series>asc.sfd` |
| `notoindik` | Copy from Noto Indic (per-script, e.g. `NotoSansDevanagari`) |
| `noto_math` | Copy from `notofonts/NotoSansMath-Regular.ttf` |

**Currently used:** `xe52`, `xe38`, `ownsfd`. `notoindik` and `noto_math` are legacy (bootstrap done — see `csv_details.md`).

## `ownsfd` — Per-Script Logic

`ownsfd` is **per-script**. When processing the Hindi script:

- `ownsfd` for xi38 → `sfdsrc/xi38/xh38asc.sfd`
- `ownsfd` for xi52 → `sfdsrc/xi52/xh52asc.sfd`

When processing Bengali:

- `ownsfd` for xi38 → `sfdsrc/xi38/xb38asc.sfd`
- `ownsfd` for xi52 → `sfdsrc/xi52/xb52asc.sfd`

And so on for all 11 scripts.

**Example** (`ownsfd` for `k` glyph in Hindi):

```
sfdsrc/xi38/xh38asc.sfd  --copy-paste k-->  sfd/xi38sfd/xi38asc/xh38asc.sfd
```

## Per-Series CSV

Each series has its own CSV. The `ownsfd` key is different per series:

| CSV | `ownsfd` key in ctx | Source |
|-----|---------------------|--------|
| `glyph_copy_xi38.csv` | `ownsfd38` | `sfdsrc/xi38/<script>38asc.sfd` |
| `glyph_copy_xi52.csv` | `ownsfd52` | `sfdsrc/xi52/<script>52asc.sfd` |

`apply_source()` receives an `ownsfd_key` parameter so the same function handles both series without conflating them.

## Code Flow

```
main()
  ├─ read_csv(CSV_PATH_38) -> csv_rows_38
  ├─ read_csv(CSV_PATH_52) -> csv_rows_52
  ├─ open sources (xe52, xe38, noto_math)
  └─ for each script in SCRIPTS:
       process_script(name, cfg, csv_rows_38, csv_rows_52, sources)
```

```
process_script(name, cfg, ...)
  ├─ open script_font     = sfdsrc/xi38/<script>38asc.sfd   (or xe38 for english)
  ├─ open script_font_52  = sfdsrc/xi52/<script>52asc.sfd   (or xe52 for english)
  ├─ open noto_font       (optional, for notoindik sources)
  ├─ open target_38       = sfd/xi38sfd/xi38asc/<script>38asc.sfd
  ├─ open target_52       = sfd/xi52sfd/xi52asc/<script>52asc.sfd
  ├─ build ctx dict:
  │    xe52, xe38, ownsfd38, ownsfd52, noto_math, notoindik, base
  ├─ for row in csv_rows_38:
  │    apply_source(target_38, cp, src, action, char, ctx, ownsfd_key="ownsfd38")
  ├─ for row in csv_rows_52:
  │    apply_source(target_52, cp, src, action, char, ctx, ownsfd_key="ownsfd52")
  └─ save target_38, target_52
```

```
apply_source(target_font, dst_cp, src_name, action, e52_char, ctx, ownsfd_key)
  ├─ if action in (keep, manual, remove): return True  (skip)
  ├─ if src_name == "xe52":  copy_glyph(ctx["xe52"], ...)
  ├─ if src_name == "xe38":  copy_glyph(ctx["xe38"], ...)
  ├─ if src_name == "ownsfd": copy_glyph(ctx[ownsfd_key], ...)
  ├─ if src_name == "noto_math": ...
  ├─ if src_name == "notoindik": ...
  └─ return False  (unknown src)
```

```
copy_glyph(src_font, src_cp, dst_font, dst_cp)
  ├─ if src_cp not in src_font: return False
  ├─ select + copy src glyph
  ├─ if dst_cp not in dst_font: createChar(-1, glyphname)
  ├─ select + paste into dst glyph
  └─ return True
```

## `createChar` for Missing Slots

If the target font doesn't have `dst_cp`, `copy_glyph()` creates it with:

```
dst_font.createChar(-1, glyphname)
```

`-1` means "encoding-independent" (works even if the target's encoding doesn't include the slot).

The new glyph's `unicode` is set to `dst_cp` afterwards.

## `keep` Behavior

When `action` is `keep` (or `manual` / `remove`), `apply_source()` returns `True` **without copying**. The target's existing glyph stays as-is.

`T` and `D` both use `ownsfd,replace` (same treatment), per `csv_details.md`.

## Related Docs

- `sfdsrc/csv_details.md` — canonical per-glyph source mapping (designer-facing)
- `xnglo-fonts-glyphs.md` — glyph types and sources (high level)
- `scripts/pipeline_design.md` — 18-step pipeline overview
- `scripts/designer_workflow.md` — designer workflow

## Pipeline

Run via `main.py`:

```
fontforge -script scripts/xi52py/main.py --phase asc
```

See `main.py` for the full 18-step pipeline.
