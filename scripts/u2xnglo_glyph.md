# Unicode to xNglo Glyph Mapping

## Overview

Ye file Devanagari Unicode code points ka xNglo hskii characters me mapping
batati hai. Font `hindixv38.sfd` me in glyphs ko copy kiya jata hai.

## Mapping Table

| Unicode | Codepoint | Devanagari | xNglo | Sound |
|---------|-----------|------------|-------|-------|
| 0x0915 | U+0915 | क | k | ka (velar unaspirated) |
| 0x0916 | U+0916 | ख | K | kha (velar aspirated) |
| 0x0917 | U+0917 | ग | g | ga (velar unaspirated) |
| 0x0918 | U+0918 | घ | G | gha (velar aspirated) |
| 0x091A | U+091A | च | c | cha (palatal unaspirated) |
| 0x091B | U+091B | छ | C | chha (palatal aspirated) |
| 0x091C | U+091C | ज | z | ja (palatal unaspirated) |
| 0x091D | U+091D | झ | Z | jha (palatal aspirated) |
| 0x091F | U+091F | ट | t | ta (retroflex unaspirated) |
| 0x0920 | U+0920 | ठ | J | tha (retroflex aspirated) |
| 0x0921 | U+0921 | ड | d | da (retroflex unaspirated) |
| 0x0922 | U+0922 | ढ | Q | dha (retroflex aspirated) |
| 0x0924 | U+0924 | त | T | ta (dental unaspirated) |
| 0x0925 | U+0925 | थ | j | tha (dental aspirated) |
| 0x0926 | U+0926 | द | D | da (dental unaspirated) |
| 0x0927 | U+0927 | ध | q | dha (dental aspirated) |
| 0x0928 | U+0928 | न | n | na (nasal) |
| 0x092A | U+092A | प | p | pa (labial unaspirated) |
| 0x092B | U+092B | फ | f | pha (labial aspirated) |
| 0x092C | U+092C | ब | b | ba (labial unaspirated) |
| 0x092D | U+092D | भ | B | bha (labial aspirated) |
| 0x092E | U+092E | म | m | ma (nasal) |
| 0x092F | U+092F | य | y | ya (semivowel) |
| 0x0930 | U+0930 | र | r | ra (liquid) |
| 0x0932 | U+0932 | ल | l | la (liquid) |
| 0x0935 | U+0935 | व | w | va (semivowel) |
| 0x0938 | U+0938 | स | s | sa (dental sibilant) |
| 0x0936 | U+0936 | श | S | sha (palatal sibilant) |
| 0x0939 | U+0939 | ह | H | ha (glottal) |
| 0x0939 | U+0939 | ह | v | ha (glottal alt) |

## Total Glyphs

28 unique Devanagari consonants mapped to 30 xNglo positions
(H aur v dono par ह).

## Source Font

- Noto Sans Devanagari: https://github.com/notofonts/devanagari
- Target: hindixv38.sfd

## Script

- Python FontForge script me use hota hai
- Path: scripts/copy_glyphs.py