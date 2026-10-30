# fontforge.md — setup + python api reference

## 1. ffz alias setup

### windows (git bash / mingw64)
add to `~/.bashrc` or `~/.bash_profile`:
```bash
alias ffz='/c/Program\ Files/FontForgeBuilds/bin/fontforge.exe'
```
reload: `source ~/.bashrc`

### linux / ubuntu
```bash
alias ffz='fontforge'
# or full path:
alias ffz='/usr/bin/fontforge'
```

### android termux
```bash
alias ffz='fontforge'
```

### run a python script with fontforge
```bash
ffz pysk/xi52py/myscript.py          # shebang line: #!/usr/bin/env fontforge
ffz -script pysk/xi52py/myscript.py  # explicit
```

> **note**: fontforge bundles its own python. `pip install` must target
> fontforge's python, not system python.
> for scripts that only need `pathlib / shutil / csv / json`, use:
> `py script.py` or `python3 script.py` (no fontforge needed).

---

## 2. fontforge python api — task reference

### 2.1 open / save / close SFD or TTF

```python
import fontforge

# open
f = fontforge.open("path/to/font.sfd")   # SFD, TTF, OTF all work
f = fontforge.open("path/to/font.ttf")

# save as SFD
f.save("path/to/output.sfd")

# generate TTF
f.generate("path/to/output.ttf")

# generate WOFF2
f.generate("path/to/output.woff2")

# generate with flags (recommended for TTF)
f.generate("output.ttf", flags=("opentype",))

# close
f.close()
```

---

### 2.2 copy SFD files / directories (pure python, no fontforge needed)

```python
import shutil
from pathlib import Path

# copy one file
shutil.copy2("sfdsrc/xi38/xh38asc.sfd", "sfd/xi38sfd/xi38asc/xh38asc.sfd")

# copy all *.sfd from one dir to another
src = Path("sfdsrc/xi38")
dst = Path("sfd/xi38sfd/xi38asc")
dst.mkdir(parents=True, exist_ok=True)
for sfd in src.glob("*.sfd"):
    shutil.copy2(sfd, dst / sfd.name)

# copy + rename (asc -> utf)
for sfd in src.glob("*.sfd"):
    new_name = sfd.name.replace("asc", "utf")
    shutil.copy2(sfd, dst / new_name)

# clear a directory
for f in Path("sfd/xi38sfd/xi38utf").glob("*.sfd"):
    f.unlink()
```

---

### 2.3 rename meta names (fontname, familyname, unique-id)

```python
f = fontforge.open("xh38asc.sfd")

# basic name fields
f.fontname   = "XngloHindi-xi38utf"      # PostScript name (no spaces)
f.familyname = "Xnglo Hindi xi38 utf"    # family name
f.fullname   = "Xnglo Hindi xi38 utf Regular"

# sfnt name table (OpenType names shown in OS)
# appendSFNTName(language, nameID, value)
# common nameIDs: 1=family, 2=style, 3=unique-id, 4=full, 5=version, 6=PS-name
f.appendSFNTName("English (US)", 3, "Version 1.000;zawa;xh38utf")
f.appendSFNTName("English (US)", 5, "Version 1.000")

# update all sfnt names that contain 'asc' -> 'utf'
for lang, nid, val in list(f.sfnt_names):
    if "asc" in val or "Asc" in val:
        f.appendSFNTName(lang, nid, val.replace("asc","utf").replace("Asc","Utf"))

# version / revision
f.sfntRevision = 0x00010000    # version 1.0 in fixed-point

f.save("xh38utf.sfd")
f.close()
```

---

### 2.4 glyph copy-paste (outline copy between fonts)

```python
src = fontforge.open("source.sfd")
dst = fontforge.open("destination.sfd")

# copy by unicode codepoint
src.selection.select(0x0915)   # U+0915 = क
src.copy()
dst.selection.select(0x0915)
dst.paste()
dst[0x0915].width = src[0x0915].width   # copy width too

# copy by ASCII char
src.selection.select(ord('k'))    # ASCII 'k' = 107
src.copy()
dst.selection.select(ord('k'))
dst.paste()

# copy multiple glyphs at once
src.selection.select(0x0915, 0x0916, 0x0917)
src.copy()
dst.selection.select(0x0915, 0x0916, 0x0917)
dst.paste()

src.close()
dst.save("destination.sfd")
dst.close()
```

---

### 2.5 glyph copyref-paste (reference, not outline copy)

used in utf fonts: unicode slot references the ascii glyph (shared outlines).

```python
f = fontforge.open("xh38utf.sfd")

src_glyph = f[ord('k')]           # ASCII 'k' glyph
src_name  = src_glyph.glyphname   # e.g. "k"
src_width = src_glyph.width

# create ref at U+0915 pointing to 'k'
dst = f.createChar(0x0915)        # create or get existing
dst.clear()
dst.addReference(src_name, (1, 0, 0, 1, 0, 0))   # identity matrix
dst.width = src_width

# identity matrix = (xx, xy, yx, yy, dx, dy)
# (1,0,0,1,0,0)  = no scale, no offset
# (1,0,0,1,50,0) = shift right by 50 units
# (0.5,0,0,0.5,0,0) = scale to 50%

f.save("xh38utf.sfd")
f.close()
```

---

### 2.6 resize / scale glyphs

```python
f = fontforge.open("font.sfd")
g = f[ord('k')]

# scale glyph (transform matrix)
# transform(xx, xy, yx, yy, dx, dy)
g.transform((0.8, 0, 0, 0.8, 0, 0))    # scale to 80%

# or use fontforge built-in
g.transform(psMat.scale(0.8))           # needs: import psMat

import psMat
g.transform(psMat.scale(0.8, 0.9))     # scale x=80%, y=90%
g.transform(psMat.translate(50, 0))    # move right 50 units
g.transform(psMat.rotate(0.1))         # rotate (radians)

f.save("font.sfd")
f.close()
```

---

### 2.7 fit / center glyph for mono fonts

```python
import psMat
f = fontforge.open("xh38mono.sfd")

MONO_WIDTH = 1024   # target fixed width for all glyphs

for g in f.glyphs():
    if not g.isWorthOutputting():
        continue

    bb = g.boundingBox()             # (xmin, ymin, xmax, ymax)
    glyph_w = bb[2] - bb[0]
    glyph_h = bb[3] - bb[1]

    if glyph_w <= 0:
        g.width = MONO_WIDTH
        continue

    # center horizontally in MONO_WIDTH
    current_center = (bb[0] + bb[2]) / 2
    target_center  = MONO_WIDTH / 2
    dx = target_center - current_center
    g.transform(psMat.translate(dx, 0))
    g.width = MONO_WIDTH

f.save("xh38mono.sfd")
f.close()
```

---

### 2.8 iterate glyphs / check glyph properties

```python
f = fontforge.open("font.sfd")

# iterate all glyphs
for g in f.glyphs():
    print(g.glyphname, g.unicode, g.width)

# check if glyph has content
if g.isWorthOutputting():
    print("has outlines")

# bounding box
bb = g.boundingBox()    # (xmin, ymin, xmax, ymax)
width  = bb[2] - bb[0]
height = bb[3] - bb[1]

# check references
for ref in g.references:
    ref_name   = ref[0]    # referenced glyph name
    ref_matrix = ref[1]    # transform matrix tuple
    print(f"  ref: {ref_name}  matrix: {ref_matrix}")

# glyph by unicode
g = f[0x0915]         # by codepoint
g = f[ord('k')]       # by ASCII
g = f["k"]            # by glyph name

# create new glyph
g = f.createChar(0x0915, "uni0915")   # codepoint, optional name
g = f.createChar(0x0915)              # auto-name
f.close()
```

---

### 2.9 font-level properties

```python
f = fontforge.open("font.sfd")

# metrics
print(f.ascent)           # ascender height
print(f.descent)          # descender depth (positive value)
print(f.em)               # em size (ascent + descent)
print(f.upos)             # underline position
print(f.uwidth)           # underline width

# encoding
f.encoding = "UnicodeFull"
f.encoding = "latin1"

# count glyphs
print(len(list(f.glyphs())))

# glyph names list
names = [g.glyphname for g in f.glyphs()]

f.close()
```

---

### 2.10 generate TTF + WOFF2 from SFD

```python
import fontforge
from pathlib import Path

sfd_path  = Path("sfdfinal/xi38sfd/xi38utf/xh38utf.sfd")
ttf_out   = Path("xnglofonts/ttf/xi38ttf/xi38utf/xh38utf.ttf")
woff2_out = Path("xnglofonts/woff2/xi38woff2/xi38utf/xh38utf.woff2")

ttf_out.parent.mkdir(parents=True, exist_ok=True)
woff2_out.parent.mkdir(parents=True, exist_ok=True)

f = fontforge.open(str(sfd_path))
f.generate(str(ttf_out),   flags=("opentype",))
f.generate(str(woff2_out), flags=("opentype",))
f.close()
print(f"generated {ttf_out.name} + {woff2_out.name}")
```

---

## 3. psMat — transformation matrix helpers

```python
import psMat

psMat.identity()                # (1,0,0,1,0,0)  no change
psMat.scale(sx, sy)             # scale x by sx, y by sy
psMat.scale(s)                  # uniform scale
psMat.translate(dx, dy)         # shift
psMat.rotate(angle_radians)     # rotate
psMat.skew(angle_radians)       # shear/skew
psMat.compose(m1, m2)           # combine two matrices
```

---

## 4. common matrix values

| transform | matrix |
|-----------|--------|
| identity (no change) | `(1, 0, 0, 1, 0, 0)` |
| scale 50% | `(0.5, 0, 0, 0.5, 0, 0)` |
| shift right 100 units | `(1, 0, 0, 1, 100, 0)` |
| shift up 50 units | `(1, 0, 0, 1, 0, 50)` |
| zero/collapsed (bug!) | `(0, 0, 0, 0, 0, 0)` |

> **warning**: `(0,0,0,0,0,0)` = zero scale = glyph collapses to a point.
> always use `(1,0,0,1,0,0)` for identity refs.

---

## 5. pff project — key script locations

| script | run with | purpose |
|--------|----------|---------|
| `pysk/notopy/noto_copy.py` | `ffz` | pipeline 1: noto TTF → notosfd |
| `pysk/xi52py/prep_utf.py` | `ffz` | pipeline 2: sfdsrc → sfd (utf) |
| `pysk/xi52py/copy_utf_unicode_blocks.py` | `py` | copy unicode blocks to all *utf.sfd |
| `pysk/xi52py/verify_utf.py` | `ffz` | verify 0 collapsed refs |
| `pysk/xi52py/main.py --phase mono` | `ffz` | generate mono fonts |
| `pysk/xi52py/main.py --phase meta` | `ffz` | update font metadata |
| `pysk/xi52py/p5generate.py` | `ffz` | pipeline 3: sfdfinal → TTF/WOFF2 |
| `pysk/xi52py/gen_asc_to_utf_json.py` | `py` | regen asc-to-utf.json |
| `pysk/notopy/extract_noto_data.py` | `ffz` | export noto glyph data to CSV |
| `pysk/notopy/gen_noto_sheets.py` | `py` | CSV → Excel workbook |
