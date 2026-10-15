# glyphs_copyref_map38_for_utf.csv

Copyref mapping for UTF phase. Maps **Sinhala Unicode offsets**
to **all 10 scripts** (Devanagari, Bengali, ..., Sinhala).

## Format

    ascii, offset, xh38, xb38, xp38, xg38, xo38, xt38, xj38, xk38, xm38, xs38

- **ascii** — Latin character (e.g. `A`, `N`, `k`)
- **offset** — Sinhala Unicode offset (e.g. `5`, `1A`, `4F`)
- **xh38** — Devanagari glyph (e.g. `अ`, `क`, `ा`)
- **xb38** — Bengali glyph (e.g. `অ`, `ক`, `া`)
- ... aise hi 10 scripts ke liye

## Purpose

UTF phase mein **copyref** banane ke liye. Har **Sinhala Unicode**
ke liye, **har script** ka **apna glyph** reference karo.

## Unicode bases

| Script | Base | Range |
|--------|------|-------|
| Hindi (Devanagari) | `900` | 0900–097F |
| Bengali | `980` | 0980–09FF |
| Punjabi (Gurmukhi) | `A00` | 0A00–0A7F |
| Gujarati | `A80` | 0A80–0AFF |
| Oriya | `B00` | 0B00–0B7F |
| Tamil | `B80` | 0B80–0BFF |
| Telugu | `C00` | 0C00–0C7F |
| Kannada | `C80` | 0C80–0CFF |
| Malayalam | `D00` | 0D00–0D7F |
| Sinhala | `D80` | 0D80–0DFF |

## Example

    A,5,अ,অ,ਅ,અ,ଅ,அ,అ,ಅ,അ,අ(D85)
    k,1A,क,ক,ਕ,ક,କ,க,క,ಕ,ക,ක(D9A)
    a,4F,ा,া,ਾ,ા,ା,ா,ా,ಾ,ാ,ා(DCF)

## Notes

- **Sinhala column** mein `(unicode)` bhi hai (e.g. `අ(D85)`)
- **Baaki scripts** mein sirf glyph hai (e.g. `अ`)
- **Offset** Sinhala Unicode ka hai (`0xD80 + offset`)
- **Empty rows** — khaali chhod do (e.g. `17`, `18`, `19`)

## Related

- `glyphs_copy_map38_noto_tu_sfdsrc.csv` — Noto source mapping
- `readme.md` — project overview