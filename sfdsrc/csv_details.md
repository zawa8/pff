# CSV Details — xi52 / xi38 Source Mapping

Designer-facing documentation for where each of the 52 `A–Z`, `a–z`
characters comes from in `xi52asc` and `xi38asc` builds.

## Master sources (designer-maintained)

`sfdsrc/xi52/xe52asc.sfd` and `sfdsrc/xi38/xe38asc.sfd` are **very
important master sources** for every designer. Python scripts must
**not** create or modify them — only the designer edits these.

Similarly, `xh32asc.sfd` / `xh52asc.sfd` (and other `x*38asc.sfd` /
`x*52asc.sfd`) are maintained by hand. The Hindi (`xh`) sources are
easy for the current maintainer because they know Hindi glyphs.

---

## 1. `xi52asc` — sources for 52 chars (`A–Z`, `a–z`)

### 1.1 From `xe52asc.sfd` — 32 chars

| Group | Chars | Count | Status |
|-------|-------|-------|--------|
| 1.1.1 | `a e i o u h`            | 6 | no design change, only copied once |
| 1.1.2 | `c C g G`                | 4 | once designed and fixed |
| 1.1.3 | `j J q Q`                | 4 | once designed and fixed |
| 1.1.4 | `N R`                    | 2 | once designed and fixed |
| 1.1.5 | `x A v H`                | 4 | design changed but not fixed; today also changed in `sfdsrc/` |
| 1.1.6 | `L Y V W P F`            | 6 | no design change, only copied once |
| 1.1.7 | `E I O U M X`            | 6 | no design change, only copied once |

### 1.2 From `sfdsrc/xi52/(xh52asc / xb52asc / ...)` — 20 chars

Source: `sfdsrc/xi52/<script>52asc.sfd`
Target: `sfd/xi52sfd/xi52asc/<script>52asc.sfd`

| Group | Chars | Count | Status |
|-------|-------|-------|--------|
| 1.2.1 | `k K z Z` `t T d D` `n` `p f b B m` `y r l w s S` | 20 | no design change, only copied once |

---

## 2. `xi38asc` — sources for 52 chars (`A–Z`, `a–z`)

### 2.1 From `xe38asc.sfd` — 20 chars

| Group | Chars | Count | Status |
|-------|-------|-------|--------|
| 2.1.1 | `a e i o u h` | 6 | no design change, only copied once |
| 2.1.2 | `N R`         | 2 | once designed and fixed |
| 2.1.3 | `L Y V W P F` | 6 | no design change, only copied once |
| 2.1.4 | `E I O U M X` | 6 | no design change, only copied once |

### 2.2 From `sfdsrc/xi38/(xh38asc / xb38asc / ...)` — 32 chars

Source: `sfdsrc/xi38/<script>38asc.sfd`
Target: `sfd/xi38sfd/xi38asc/<script>38asc.sfd`

| Group | Chars | Count | Status |
|-------|-------|-------|--------|
| 2.2.1 | `k K z Z` `t T d D` `n` `p f b B m` `y r l w s S` | 20 | no design change, only copied once |
| 2.2.2 | `c C g G` | 4 | once designed and fixed |
| 2.2.3 | `j J q Q` | 4 | once designed and fixed |
| 2.2.4 | `x A v H` | 4 | design changed but not fixed; today also changed in `sfdsrc/` |

---

## Summary

| Series | From `xe52` / `xe38` | From `sfdsrc/<script>` | Total |
|--------|----------------------|-------------------------|-------|
| **xi52** | 32 (`xe52asc.sfd`) | 20 (`xi52/<script>52asc.sfd`) | 52 |
| **xi38** | 20 (`xe38asc.sfd`) | 32 (`xi38/<script>38asc.sfd`) | 52 |

### CSV mapping

| CSV | `xe52` / `xe38` rows | `ownsfd` rows | `keep` rows |
|-----|----------------------|---------------|-------------|
| `glyph_copy_xi38.csv` | 20 (`xe38`) | 30 | 1 (`T`) |
| `glyph_copy_xi52.csv` | 32 (`xe52`) | 20 | 1 (`T`) |
