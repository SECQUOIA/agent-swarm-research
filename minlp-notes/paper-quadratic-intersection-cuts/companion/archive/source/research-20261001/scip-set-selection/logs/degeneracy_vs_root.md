instances with degeneracy data and three seeds: 248

| quantity | median over instances | Spearman rho with D(corner, scip) (p) | with D(eff, scip) (p) | with D(scip, off) (p) |
|---|---|---|---|---|
| criterion at zero-cost ray (share of corners) | 0.73 | +0.145 (0.022) | +0.031 (0.62) | -0.509 (8.8e-18) |
| zero-cost share of rays | 0.12 | +0.092 (0.15) | -0.003 (0.96) | -0.421 (4.3e-12) |
| share of corners with dim(lambda) >= 2 | 1.00 | -0.120 (0.059) | -0.032 (0.61) | -0.087 (0.17) |

Root effect of the rules by degeneracy class (seed-averaged RGC difference to SCIP's rule):

| class | n | mean D(corner, scip) | corner better / worse (> 0.01) | Wilcoxon p | mean D(eff, scip) | eff better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|---|
| criterion at a zero-cost ray in < 50% of corners | 97 | -0.0183 | 13 / 26 | 0.00821 | -0.0026 | 16 / 21 | 0.362 |
| criterion at a zero-cost ray in >= 50% of corners | 151 | -0.0023 | 9 / 20 | 0.0862 | +0.0018 | 11 / 12 | 0.456 |
| dim(lambda) >= 2 in >= 50% of corners | 193 | -0.0110 | 22 / 46 | 0.00191 | +0.0001 | 27 / 33 | 0.798 |
| all | 248 | -0.0085 | 22 / 46 | 0.00191 | +0.0001 | 27 / 33 | 0.852 |
