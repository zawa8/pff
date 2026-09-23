# Groups and Pipelines — xi52/xi38

## Naming
- `xv` → `xh` (xNglohinDi)
- Suffixes: `asc`, `utf`, `mono`
- Sources in `sfdsrc/`, targets in `sfd/`

## Groups (sources for xh52)

| Group | Letters | xh52 source |
|-------|---------|-------------|
| G1 | `k K z Z t T d D n p f b B m y r l w s S` (20) | noto (Indic consonants) |
| G2 | `x j J q Q v c C g G` (10) | xh38 (Hindi designs) |
| G3 | `N R a i u e o h L Y V W P F` (14) | xe52 (Latin shapes) |
| G4 | `E I O U M X` (6) | noto_math (symbols) |
| G5 | `A H` (2) | xh38 (Hindi designs) |

Total: 52 letters

## Actions in .csv
- `replace` — copy from source
- `keep` — leave as-is
- `manual` — leave as-is
- `remove` — (treated as keep)

## Pipelines (15 steps)

### Phase 0 — sources → targets
1. Copy sfdsrc/ into sfd/

### Phase 1 — asc
2. Build xi38asc + xi52asc, 9 scripts (G1-G5)
3. Build xi38asc + xi52asc, Sinhala

### Phase 2 — utf
4. xi38asc → xi38utf (copy 128 + unicode refs)
5. xi52asc → xi52utf (copy + refs)
6. Add unicode-range refs to xi52utf
7. Rename xi52utf internals

### Phase 3 — mono
8. xi52utf → xi52mono
9. Center glyphs
10. Fix widths

### Phase 4 — generate TTF/WOFF2
11-15. Generate all TTF/WOFF2 (xi38asc/utf/mono, xi52asc/utf/mono)

## Design workflow
1. Edit sources in `sfdsrc/xe52/` or `sfdsrc/xh38/` (FontForge)
2. Run pipeline
3. Targets rebuilt
4. Sources never overwritten
