### leaf table (eps = 1e-4)

| relaxation, rule, instance | n=2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | growth |
|---|---|---|---|---|---|---|---|---|---|---|
| `mc` bisect, `kappa=0`, `c=0` | 24 | 100 | 320 | 962 | 2780 | 7976 | 23552 | 69632 | 206612 | 2.94 |
| `mc` bisect, seed 0 | 20 | 80 | 249 | 738 | 2254 | 7121 | 21001 | 64518 | 198363 | 3.06 |
| `mc` oracle, seed 0 | 31 | 111 | 335 | 954 | 2594 | 7174 | 20296 | 57637 | 164804 | 2.82 |
| `mc` viol, seed 0 | 16 | 67 | 206 | 700 | 1941 | 8350 | 15717 | 50493 | 130035 | 2.86 |
| `mc` vw, seed 0 | 19 | 66 | 189 | 587 | 1766 | 5791 | 15756 | 47043 |  | 2.99 |
| `mcx` bisect, seed 0 | 17 | 77 | 241 | 648 | 1988 | 6229 | 18032 | 54788 |  | 3.03 |
| `mcx` oracle, seed 0 | 24 | 101 | 316 | 904 | 2405 | 6483 | 18012 | 49771 |  | 2.72 |
| `mcx` vw, seed 0 | 16 | 61 | 182 | 499 | 1474 | 4503 | 11976 | 35908 |  | 2.91 |
| `mcx` vw, seed 1 | 16 | 58 | 173 | 560 | 1711 | 4822 | 14954 | 40860 |  | 2.92 |
| `mcx` vw, `c=0` | 20 | 65 | 228 | 664 | 1780 | 5064 | 13994 | 39297 |  | 2.77 |
| `abb` bisect, `kappa=0`, `c=0` | 32 | 114 | 316 | 804 | 1992 | 4828 | 11532 | 27314 | 64740 | 2.39 |
| `abb` viol, `kappa=0`, `c=0` | 16 | 46 | 142 | 456 | 1338 | 3930 | 11406 | 32254 | 95198 | 2.90 |
| `abbU` bisect, `c=0` (PROGRAM factorization) | 34 | 114 | 318 | 824 | 2094 | 5284 | 13352 |  |  | 2.55 |
| `abbS` bisect, `c=0` (balanced split) | 1 | 24 | 64 | 162 | 404 | 1000 | 2476 |  |  | 2.49 |
| Theorem 1 lower bound | 1.6 | 2.7 | 4.4 | 7.4 | 12.3 | 20.5 | 34.2 | 56.9 | 94.9 | 1.67 |

### eps table

| relaxation, rule, instance | n | `1e-02` | `1e-03` | `1e-04` | `1e-05` | `1e-06` |
|---|---|---|---|---|---|---|
| `mcx` bisect, seed 0 | 4 | 113 | 159 | 241 | 313 | 359 |
|  | 6 | 875 | 1443 | 1988 | 2564 | 3130 |
|  | 8 | 8290 | 13337 | 18032 | 23418 | 28024 |
| `mcx` vw, seed 0 | 4 | 86 | 136 | 182 | 231 | 270 |
|  | 6 | 704 | 1121 | 1474 | 1850 | 2251 |
|  | 8 | 5707 | 8966 | 11976 | 15200 | 18715 |
| `mc` bisect, `kappa=0`, `c=0` | 4 | 132 | 232 | 320 | 422 | 522 |
|  | 6 | 1122 | 1954 | 2780 | 3636 | 4474 |
|  | 8 | 9508 | 16534 | 23552 | 30474 | 37500 |
| `mc` viol, seed 0 | 8 | 6820 | 10626 | 15717 | 26771 | 36220 |

### certified-bound statistics (nodes refined by dual ascent / undecided / solver value too high)

totals over all 176 runs: refined=375834, undecided=0, solver-too-high=150353
runs with undecided nodes: none

### grid DP

    grid DP n=2 K=4 grid points=11 eps=1e-02 kappa=0.0 rel=mc: min grid-guillotine leaves = 4 (2804 relaxations, 2.2s; refined 139)
    grid DP n=2 K=7 grid points=17 eps=1e-04 kappa=0.0 rel=mc: min grid-guillotine leaves = 8 (18327 relaxations, 17.7s; refined 612)
    grid DP n=2 K=10 grid points=23 eps=1e-06 kappa=0.0 rel=mc: min grid-guillotine leaves = 12 (63791 relaxations, 114.0s; refined 2012)
    grid DP n=3 K=4 grid points=11 eps=1e-02 kappa=0.0 rel=mc: min grid-guillotine leaves = 10 (162410 relaxations, 150.5s; refined 7883)
    grid DP n=3 K=5 grid points=13 eps=1e-03 kappa=0.0 rel=mc: min grid-guillotine leaves = 16 (470092 relaxations, 407.8s; refined 20221)
    grid DP n=4 K=3 grid points=9 eps=1e-02 kappa=0.0 rel=mc: min grid-guillotine leaves = 32 (1638378 relaxations, 1392.0s; refined 56184)
