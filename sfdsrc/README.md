# sfdsrc — master sources for xi52/xi38 pipeline

Master sources for the xi52/xi38 font pipeline.

## Structure

- `xe52/xe52asc.sfd` — English master source (Sunny Spells + manual designs)
- `xi38/` — per-script xi38 sources
  - `xh38asc.sfd` — Hindi
  - `xb38asc.sfd` — Bengali
  - `xp38asc.sfd` — Punjabi
  - `xg38asc.sfd` — Gujarati
  - `xo38asc.sfd` — Oriya
  - `xt38asc.sfd` — Tamil
  - `xj38asc.sfd` — Telugu
  - `xk38asc.sfd` — Kannada
  - `xm38asc.sfd` — Malayalam
  - `xs38asc.sfd` — Sinhala
- `glyph_copy_xh38.csv` — xi38 per-glyph decisions (src, action, notes)
- `glyph_copy_xh52.csv` — xi52 per-glyph decisions
- `phoneme_map.csv` — IPA + Hindi reference (documentation)

## Pipeline

Sources here are never overwritten. Pipeline reads from here,
writes to `sfd/xi38sfd/` and `sfd/xi52sfd/`.

## Naming

Each per-script source follows `<script>38asc.sfd` (e.g. `xh38asc.sfd`
= Hindi xi38 asc). New sources welcome — a Bengali contributor adds
`xi38/xb38asc.sfd`.

## Editing

1. Edit `.sfd` files in FontForge.
2. Save back to this folder.
3. Edit `.csv` files to set per-glyph decisions.
4. Run pipeline to propagate to targets.

See `scripts/designer_workflow.md` for the full 4-step workflow.

## Noto fallback

Noto TTFs (in `notofonts/`) are used only when a glyph is not
present in this folder.
