# sfdsrc — master sources for xi52/xi38 pipeline

Master sources for the xi52/xi38 font pipeline.

## Structure

- `xe52/` — English xi52 master source (Sunny Spells + manual designs)
- `xh38/` — Hindi xi38 source (manually designed)
- `scripts/` — Python scripts to improve designs (future)

## Pipeline

Sources here are never overwritten. Pipeline reads from here,
writes to `sfd/xi38sfd/` and `sfd/xi52sfd/`.

## Editing

1. Edit `.sfd` files in FontForge.
2. Save back to this folder.
3. Run pipeline to propagate to targets.

## Noto fallback

Noto TTFs (in `notofonts/`) are used only when a glyph is not
present in this folder.
