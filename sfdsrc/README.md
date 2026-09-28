# sfdsrc — master sources for xi52/xi38 pipeline

Master sources for the xi52/xi38 font pipeline.

## Structure

- `xe52/` — English xi52 master source (Sunny Spells + manual designs)
- `xi38/` — per-script xi38 sources (Hindi: `xh38asc.sfd`, future: `xb38asc.sfd`, ...)
- `scripts/` — Python scripts to improve designs (future)

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
3. Run pipeline to propagate to targets.

## Noto fallback

Noto TTFs (in `notofonts/`) are used only when a glyph is not
present in this folder.
