# xi52/xi38 build pipeline (p1onli)

## Manual setup (one-time)

1. Sunny Spells → eNgliSxe52.sfd
2. Modify in eNgliSxe52.sfd:
   x, X, A, j, J, q, Q, v, H, L, Y, V, W, P, F,
   c, C, g, G, N, R, B, K, S, Z
3. eNgliSxe52.sfd → eNgliSxe38.sfd (full copy)
4. Modify in eNgliSxe38.sfd:
   E, I, O, U, M, X (6 programming symbols, from Noto Math)

## Phase 1: asc fonts (xi52asc and xi38asc, in parallel)

- xi52asc = Noto (Indic) + eNgliSxe52.sfd (Latin, per groups G1-G5)
- xi38asc = Noto (Indic) + eNgliSxe38.sfd (Latin, per groups G1-G5)

## Phase 2: utf fonts

- xi52utf = xi52asc + unicode references
- xi38utf = xi38asc + unicode references

## Phase 3: mono fonts

- xi52mono = xi52utf + rename + widths + center
- xi38mono = xi38utf + rename + widths + center

## Phase 4: generate TTF/WOFF2 (last)

- All 6 folders: xi38asc/utf/mono, xi52asc/utf/mono