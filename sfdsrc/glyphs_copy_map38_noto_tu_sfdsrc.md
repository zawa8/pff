# glyphs_copy_map38_noto_tu_sfdsrc.csv

Noto source mapping for all scripts. Maps Latin ASCII characters
to their Indic glyphs (Devanagari, Bengali, ..., Sinhala).

## Format

    char(ascii_hex), xh38(unicode_hex), xb38(unicode_hex), ...

- **char** — Latin ASCII character (e.g. `A(41)`)
- **xh38** — Devanagari glyph (e.g. `अ(905)`)
- **xb38** — Bengali glyph (e.g. `অ(985)`)
- ... aise hi 10 scripts ke liye

## Purpose

Yeh CSV batati hai ki **kaunse Latin character** ko **kaunse Indic glyph**
se replace karna hai, **har script** ke liye.

## Example

    A(41),अ(905),অ(985),ਅ(A05),અ(A85),ଅ(B05),அ(B85),అ(C05),ಅ(C85),അ(D05),අ(D85)
    H(48),ह(939),হ(9B9),ਹ(A39),હ(AB9),ହ(B39),ஹ(BB9),హ(C39),ಹ(CB9),ഹ(D39),හ(DC4)

## Sections

1. **Indik copied_from_notosans_ownsfd** — `A`, `H`, `c`, `C`, ...
2. **Latin vowels** — `a`, `e`, `i`, `o`, `u`, `h`
3. **Latin glyphs designed** — `N`, `R`
4. **Latin glyphs not designed** — `L`, `Y`, `V`, `W`, `P`, `F`
5. **Maths symbols** — `E`, `I`, `O`, `U`, `M`, `X`

## Related

- `glyphs_copyref_map38_for_utf.csv` — copyref mapping for UTF phase
- `readme.md` — project overview