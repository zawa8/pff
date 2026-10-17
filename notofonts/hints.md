# Refcopy hint format — `sfdsrc/asc-to-utf-generated.csv`

`sfdsrc/asc-to-utf-generated.csv` is **auto-generated** by
`notofonts/fill_asc-to-utf-csv.py` from local Noto fonts. The generated
data rows contain only `?` (glyph present, refcopy undecided) or
`clear` (no glyph). The final refcopy decisions live in **manual hint
lines** written by the designer, which the script re-applies on every
regeneration.

---

## 1. Columns

    offset,900,980,A00,A80,B00,B80,C00,C80,D00,D80

| Column | Script     | Noto font                         | Block start |
|--------|------------|-----------------------------------|-------------|
| `900`  | Devanagari | NotoSansDevanagari-Regular.ttf    | U+0900      |
| `980`  | Bengali    | NotoSansBengali-Regular.ttf       | U+0980      |
| `A00`  | Gurmukhi   | NotoSansGurmukhi-Regular.ttf      | U+0A00      |
| `A80`  | Gujarati   | NotoSansGujarati-Regular.ttf      | U+0A80      |
| `B00`  | Oriya      | NotoSansOriya-Regular.ttf         | U+0B00      |
| `B80`  | Tamil      | NotoSansTamil-Regular.ttf         | U+0B80      |
| `C00`  | Telugu     | NotoSansTelugu-Regular.ttf        | U+0C00      |
| `C80`  | Kannada    | NotoSansKannada-Regular.ttf       | U+0C80      |
| `D00`  | Malayalam  | NotoSansMalayalam-Regular.ttf     | U+0D00      |
| `D80`  | Sinhala    | NotoSansSinhala-Regular.ttf       | U+0D80      |

Each row's `offset` is a hex byte. The Unicode codepoint for column S
at row NN is `block_start(S) + 0xNN`. Example: row `15`, column `D80`
= `U+0D80 + 0x15 = U+0D95` = `ඕ SINHALA LETTER OOYANNA`.

---

## 2. Hint line format

    #NN,<field-900>,<field-980>,<field-A00>,...,<field-D80>

- `NN` = 2-hex-digit offset (`00`–`7F`), **must** match a data row.
- Exactly **10 fields** after the offset (one per script column).
- Fields are comma-separated, no spaces around commas.

### Field values

| Field                    | Meaning in the data row                |
|--------------------------|----------------------------------------|
| `<Latin><native>` (e.g. `kक`) | refcopy letter = first char (`k`)  |
| `<Latin>` (e.g. `k`)     | refcopy letter = that char (`k`)       |
| `empty`                  | force `clear` (no refcopy, no glyph)   |
| `?` or blank             | `?` if glyph present, `clear` if not   |

The reference set of refcopy letters is:

    0123456789 ADHT KGCZNRBS abcdefghijklmnopqrstuwyz

The Latin letter is the refcopy target — a corresponding glyph from
a reference font. The optional trailing native character is decorative
for humans; the script only reads the first Latin character.

---

## 3. Example — Sinhala / Devanagari vowels

    #04,eऄ,empty,?,?,?,?,?,?,?,?
    04,e,clear,clear,clear,clear,clear,?,?,?,clear

    #05,Aअ,Aঅ,?,?,?,?,?,?,?,Aඅ
    05,A,A,A,A,A,A,A,A,A,A

    #06,aआ,aআ,?,?,?,?,?,?,?,aආ
    06,a,a,a,a,a,a,a,a,a,a

    #15,kक,kক,?,?,?,?,?,?,?,oඕ
    15,k,k,k,k,k,k,k,k,k,o

The data row immediately below each hint is filled by the script on the
next run. **Do not hand-edit the data rows** — they will be overwritten.
Only `#NN,...` hint lines and `# auto-hint ...` comment lines are safe
to touch.

---

## 4. Auto-hint lines

For every offset with **no** manual hint, the script emits a worksheet
line listing every glyph present at that offset:

    # 0914=au | 0994=au | 0A14=au | ... | 0D96=au

Format: `<codepoint>=<short>`, one entry per column where a glyph
exists. `<short>` comes from the Unicode `NamesList.txt` alias when
available (`0D9A=ka`), otherwise the last word of the Unicode name.

Auto-hint lines are **read-only** — edit them into a manual hint if you
want to commit a refcopy decision.

---

## 5. Workflow

1. Run the generator:

       cd /c/xpzs/pff
       ./regen.sh

2. Open `sfdsrc/asc-to-utf-generated.csv`.

3. For each offset you want to decide, **add** (or edit) a `#NN,...` line
   above its data row, following the format in §2.

4. Re-run `./regen.sh` — the data row fills automatically.

5. Commit both the hint lines and the regenerated data rows:

       git add sfdsrc/asc-to-utf-generated.csv
       git commit -m "apply refcopy hints for offsets XX–YY"
       git push

---

## 6. Regeneration is idempotent

Running `./regen.sh` twice produces the same CSV. Manual hints survive
regeneration because the script reads them back from the existing CSV
before rewriting. Backups of the previous CSV are safe to delete
(`sfdsrc/*.bak*` is git-ignored).

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `TypeError: open() takes no keyword arguments` | use `ffz -script fill_asc-to-utf-csv.py`, not `ffz -c` |
| `0D9A=KAYANNA` in auto-hint | `notofonts/NamesList.txt` missing — download from `https://www.unicode.org/Public/18.0.0/ucd/NamesList.txt` |
| Manual hint not applied | check `#NN,` prefix, 10 comma-separated fields, valid Latin first char |
| `empty` cell still shows `?` | make sure the field text is exactly `empty` (lowercase) |
