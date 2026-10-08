# Designer Workflow

How to modify xnglo fonts as a designer.

## Your workspace: `sfdsrc/`

All designer files live in `sfdsrc/` — one folder for everything.

    sfdsrc/
    ├── xe52/xe52asc.sfd          English master
    ├── xi38/
    │   ├── xh38asc.sfd           Hindi source
    │   ├── xb38asc.sfd           Bengali source
    │   ├── xp38asc.sfd           Punjabi source
    │   ├── xg38asc.sfd           Gujarati source
    │   ├── xo38asc.sfd           Oriya source
    │   ├── xt38asc.sfd           Tamil source
    │   ├── xj38asc.sfd           Telugu source
    │   ├── xk38asc.sfd           Kannada source
    │   ├── xm38asc.sfd           Malayalam source
    │   └── xs38asc.sfd           Sinhala source
    ├── glyph_copy_xh38.csv       xi38 per-glyph decisions
    ├── glyph_copy_xh52.csv       xi52 per-glyph decisions
    └── phoneme_map.csv           IPA + Hindi reference

## 4-step workflow

### Step 1 — Edit `sfdsrc/*.sfd` (FontForge)

Open a source in FontForge:
- `sfdsrc/xe52/xe52asc.sfd` (English master)
- `sfdsrc/xi38/xh38asc.sfd` (Hindi, example)

Edit glyphs. Save `.sfd`.

**Note:** Sources are 128 ASCII slots. No Unicode here.

### Step 2 — Edit `sfdsrc/glyph_copy_*.csv` (decisions)

Per-glyph decisions. Format:

    e52, src, action, notes

- `e52`    — letter (ASCII slot)
- `src`    — where to take the glyph from:
             - `xe52`       English master
             - `script`     current script's sfdsrc source
             - `notoindik`  Noto Indic fallback
             - `noto_math`  Noto Math symbols
             - `keep`       leave target as-is (FontForge work)
- `action` — `replace` / `keep` / `manual` / `remove`
- `notes`  — free-form documentation

Example:

    k,notoindik,replace,Indic consonant
    x,script,replace,current script's schwa
    v,xe52,replace,Latin dual glyph
    T,keep,keep,Sunny Spells T

### Step 3 — Run the pipeline

**If FontForge installed (local):**

    cd pff
    fontforge -script scripts/xi52py/main.py

**If no FontForge (CI):**

    git switch -c my-design
    git add sfdsrc/
    git commit -m "design: update X glyph"
    git push -u origin my-design

    gh pr create --title "design: ..." --body "..."

    # Wait for CI green. Then download artifacts:
    gh run download <RUN_ID> --name fonts --dir ~/ci-fonts

### Step 4 — Review `xnglofonts/`

Open generated TTF in font viewer / browser:
- `xnglofonts/ttf/xi38ttf/xi38asc/xh38asc.ttf`
- `xnglofonts/ttf/xi52ttf/xi52asc/xh52asc.ttf`
- etc.

Test strings:
- `Dhanyavaad` → `दhaनयa∀aaड`
- `jug queen cat game` → Latin
- `bus sun star` → स (not ष)
- `E I O U M X` → ≡ ≠ → ↓ ≥ ≤

See `fontimz/` for example rendering screenshots.

**If OK** → commit/merge.
**If not** → back to Step 1 (iterate).

## Iteration limit

If after 2-3 iterations it's still not right, ask for help — maybe
a structural issue (not just a glyph tweak).

## Files you never touch

These are maintained by the pipeline, not designers:

- `sfd/`        — targets (regenerated each run)
- `xnglofonts/` — generated TTF/WOFF2 (regenerated)
- `scripts/`    — pipeline code (ask before editing)
- `notofonts/`  — Noto fallback (external)

## Roles

- **Designer (you):** `sfdsrc/*.sfd` + `sfdsrc/*.csv`
- **Python:** reads `sfdsrc/` + CSV → writes `sfd/` → `xnglofonts/`
- **Never decide** in python — only execute
