# hskii Encoding System Analysis

## Overview

hskii is a phonetic encoding system that maps human speech sounds to 
single-case ASCII characters, integrates 6 dedicated hex digits, and reserves 
8 uppercase letters for programming symbols. Total usable characters: 128 
(ASCII range).

The key innovation: **hskii text is stored as pure ASCII but displayed via a 
custom font (englosoftw8utf) that renders phonetic glyphs.**

## Phonetic Mapping

### Vowel System

| hskii | Standalone | Matra | Example |
|-------|------------|-------|---------|
| x | अ | - | xm = अम |
| a | आ | ा | kam = काम |
| i | इ | ि | kim = किम |
| u | उ | ु | kum = कुम |
| e | ए | े | kem = केम |
| o | ओ | ो | kom = कोम |

**Key Rule:** The `x` (अ) is explicitly inserted wherever the schwa sound 
occurs in speech. This makes hskii 100% phonetic with no hidden sounds.

#### Example: भारत

| System | Written | Notes |
|--------|---------|-------|
| Devanagari | भारत | schwa after र is hidden |
| hskii | Barxj | भ + ा + र + अ + त = भारअत |
| Standard IAST | bhārata | schwa hidden |
| ITRANS | bhArata | schwa hidden |

### Base Sounds (26 lowercase)

| hskii | Hindi | Glyph in Font |
|-------|-------|---------------|
| a | ा (matra) | a (as-is) |
| b | ब | ब (Devanagari copy) |
| c | च | c (as-is) |
| d | ड | ड (Devanagari copy) |
| e | े (matra) | e (as-is) |
| f | फ | फ (Devanagari copy) |
| g | ग | g (as-is) |
| h | ह | h (as-is) |
| i | ि (matra) | i (as-is) |
| j | त | j/T (dual design) |
| k | क | क (Devanagari copy) |
| l | ल | ल (Devanagari copy) |
| m | म | म (Devanagari copy) |
| n | न | न (Devanagari copy) |
| o | ो (matra) | o (as-is) |
| p | प | प (Devanagari copy) |
| q | द | q/D (dual design) |
| r | र | र (Devanagari copy) |
| s | स | स (Devanagari copy) |
| t | ट | ट (Devanagari copy) |
| u | ु (matra) | u (as-is) |
| v | ह | v/H (dual design) |
| w | व | व (Devanagari copy) |
| x | अ | x (as-is) |
| y | य | य (Devanagari copy) |
| z | ज | ज (Devanagari copy) |

### Aspirated/Modified Sounds (12 capitals)

| hskii | Hindi | Sound | Glyph |
|-------|-------|-------|-------|
| K | ख | aspirated k | क with extra stroke |
| G | घ | aspirated g | ग with extra stroke |
| C | छ | aspirated c | च with extra stroke |
| Z | झ | aspirated z | ज with extra stroke |
| T | ठ | aspirated t | ट with extra stroke |
| D | ढ | aspirated d | ड with extra stroke |
| J | थ | aspirated j | J/Th (dual design) |
| Q | ध | aspirated q | Q/Dh (dual design) |
| B | भ | aspirated b | ब with extra stroke |
| S | श | aspirated s | श (Devanagari) |
| N | ं | nasal | ं (anusvara) |
| R | ड़ | retroflex r | ड़ (retroflex) |

## Font Glyph Design (englosoftw8utf)

### Unchanged Letters (9)

These keep their original Latin glyphs:

| ASCII | Glyph |
|-------|-------|
| a | a |
| i | i |
| u | u |
| e | e |
| o | o |
| h | h |
| c | c |
| g | g |
| x | x |

### Dual Design Letters (5)

These glyphs show both Latin and Hindi shapes:

| ASCII | Hindi | Dual Glyph |
|-------|-------|------------|
| v | ह | v/H |
| q | द | q/D |
| Q | ध | Q/Dh |
| j | त | j/T |
| J | थ | J/Th |

### Devanagari Copy Letters (12)

These use glyphs copied directly from Devanagari:

| ASCII | Devanagari |
|-------|------------|
| b | ब |
| d | ड |
| f | फ |
| k | क |
| l | ल |
| m | म |
| n | न |
| p | प |
| r | र |
| s | स |
| t | ट |
| w | व |
| y | य |
| z | ज |

## Dedicated Hex Digits (6 capitals)

| hskii | Value | Mnemonic |
|-------|-------|----------|
| L | 10 | ten (8+2) |
| Y | 11 | yilewen (8+3) |
| V | 12 | twelw (8+4) |
| W | 13 | dblun (8+5) |
| P | 14 | purxn (8+6) |
| F | 15 | fiwxn (8+7) |

### Key Equation
8+8 = 10 = 4×4 = F+1 = P+2 = W+3 = V+4 = Y+5 = L+6


### Why these letters?

| Letter | Phonetic Status | Reason |
|--------|-----------------|--------|
| L | same as l | No different sound, free to use |
| Y | same as y | No different sound |
| V | same as v | No different sound |
| W | same as w | No different sound |
| P | same as p | No different sound |
| F | same as f | No different sound |

## Programming Symbols (8 capitals)

| hskii | Symbol | Meaning |
|-------|--------|---------|
| E | `==` | is-equal-to |
| U | `!=` | not-equal-to |
| I | `>=` | greater-than-or-equal-to |
| O | `<=` | less-than-or-equal-to |
| M | `&&` | logical AND |
| X | `\|\|` | logical OR |
| A | `=>` | arrow/lambda |
| H | `++` | increment |

## Complete Character Set

### Total: 44 defined characters

| Category | Count | Characters |
|----------|-------|------------|
| Digits | 10 | 0-9 |
| Base sounds | 26 | a-z |
| Aspirated | 12 | K,G,C,Z,T,D,J,Q,B,S,N,R |
| Hex digits | 6 | L,Y,V,W,P,F |
| Programming | 8 | A,E,I,O,U,M,X,H |

### Remaining: 84 slots (of 128) available

## hskii vs ASCII vs Unicode

### Comparison Table

| Feature | ASCII | Unicode | hskii |
|---------|-------|---------|-------|
| Char size | 1 byte | 1-4 bytes | 1 byte |
| Universal sounds | ❌ | ❌ | ✅ |
| Phonetic typing | ❌ | ❌ | ✅ |
| Simple rendering | ✅ | ❌ | ✅ |
| Native hex | ❌ | ❌ | ✅ |
| Standard keyboard | ✅ | ❌ | ✅ |
| Cross-language | ❌ | Partial | ✅ |
| Case sensitivity | 2 cases | varies | 1 case |
| Programming symbols | ✅ | ✅ | ✅ (8 reserved) |
| Single font for all | ❌ | ❌ | ✅ |

### Storage Efficiency

| Text | ASCII/UTF-8 | hskii | Savings |
|------|-------------|-------|---------|
| भारत | 12 bytes (UTF-8) | 5 bytes | 2.4× |
| विद्या | 12 bytes (UTF-8) | 5 bytes | 2.4× |
| निकेतन | 18 bytes (UTF-8) | 7 bytes | 2.6× |

## The x (अ) Insertion Advantage

### Problem with Unicode Hindi

Devanagari hides the schwa (अ) sound. Example:
भारत = भ + ा + र + त


Here `र` is written without halant but pronounced as र् (half र), 
suppressing the inherent schwa.

### hskii Solution

hskii makes schwa explicit:
Barxj = भ + ा + र + अ + त


### Advantages

1. **True Phonetic Accuracy** - every sound is written
2. **No Halant Needed** - no complex conjunct formation
3. **Simplifies Parsing** - one character = one sound
4. **Consistent Word Structure** - syllable boundaries obvious
5. **Better for Speech Recognition** - direct sound-to-character mapping
6. **Cross-Language Consistency** - schwa explicit everywhere

### Cost

Text becomes 20-30% longer, but clarity is absolute.

## Number System: plong

### Format
-2P,5V,67,5V.67.78.89


- Comma separates integer digits
- Period separates fractional digits
- Each digit = one u8 (0-255, displayed as hex pair)
- Base-256 storage

### Example
cplong x("-2P,5V,67,5V.67.78.89");
// wlyu = [46, 92, 103, 92, 103, 120, 137]
// start_prisizxn_leyr = 3
// is_negetiw = true


## Advantages of hskii

1. **Universal phonetic representation** - one sound = one symbol
2. **Compact storage** - 1 byte per sound
3. **Simple rendering** - no complex text layout
4. **Native hex support** - L,Y,V,W,P,F
5. **QWERTY-compatible** - no special keyboard
6. **Cross-script** - works for Hindi, Urdu, Bengali, etc.
7. **Easy to parse** - fixed width, no ambiguity
8. **Programming-ready** - 8 symbols for operators
9. **Single font** - englosoftw8utf renders everything
10. **No font switching** - one font for all text

## Disadvantages

1. **Limited to 44 defined characters**
2. **Learning curve** - phonetic mapping
3. **Not standard** - no existing infrastructure
4. **Glyph ambiguity** - v may look like H
5. **Single case** - no upper/lower distinction
6. **Text length** - 20-30% longer due to x insertion

## Verdict

hskii is superior for:
- Phonetic keyboard input
- Cross-language text storage
- Arbitrary-precision numbers
- Compact text representation
- Single-font rendering
- Speech recognition integration

Not suitable for:
- Standard text documents (compatibility)
- Mathematical notation (beyond 8 operators)
- Emojis/symbols

## References

- Font: https://github.com/zawa8/font/tree/main/ttf/hscii
- FontForge: https://github.com/zawa8/pff/tree/main/sfd/englosoftw8
- Keyboard: https://github.com/zawa8/xNglobord
- Number system: https://github.com/zawa8/plong
- Rust: https://github.com/zawa8/vskii_rust4
- 
