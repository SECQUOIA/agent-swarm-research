### Root gap closed by R1 over R0, (R1 - R0) / (best - R0), in percent

| group | bounds | n | mean | 25% / median / 75% / max | #>1% | #>10% | R1 < R0 - 1e-6 |
|---|---|---|---|---|---|---|---|
| all | ibp | 80 | 10.2 | 0.4 / 3.6 / 18.4 / 46.2 | 54 | 30 | 1 |
| all | obbt | 80 | 3.7 | 0.3 / 2.2 / 5.4 / 21.0 | 46 | 8 | 1 |
| act=tanh | ibp | 16 | 2.2 | 0.3 / 0.6 / 1.9 / 14.2 | 6 | 1 | 0 |
| act=tanh | obbt | 16 | 1.4 | 0.1 / 0.3 / 0.7 / 11.8 | 3 | 1 | 0 |
| act=sigmoid | ibp | 16 | 5.2 | 0.9 / 4.3 / 8.1 / 14.9 | 12 | 3 | 1 |
| act=sigmoid | obbt | 16 | 2.4 | 0.2 / 0.9 / 4.9 / 9.7 | 7 | 0 | 1 |
| act=silu | ibp | 16 | 19.5 | 11.3 / 20.3 / 26.4 / 41.5 | 14 | 12 | 0 |
| act=silu | obbt | 16 | 5.6 | 2.4 / 5.3 / 9.4 / 10.7 | 13 | 3 | 0 |
| act=gelu | ibp | 16 | 21.0 | 11.1 / 21.6 / 29.1 / 46.2 | 14 | 12 | 0 |
| act=gelu | obbt | 16 | 6.5 | 2.3 / 4.2 / 8.3 / 21.0 | 14 | 3 | 0 |
| act=sin | ibp | 16 | 3.0 | 0.0 / 0.7 / 3.8 / 18.1 | 8 | 2 | 0 |
| act=sin | obbt | 16 | 2.6 | 0.0 / 2.1 / 3.6 / 11.3 | 9 | 1 | 0 |
| d=2 | ibp | 30 | 10.0 | 0.4 / 6.6 / 14.6 / 38.8 | 21 | 11 | 1 |
| d=2 | obbt | 30 | 3.8 | 0.6 / 2.2 / 5.3 / 20.5 | 18 | 3 | 1 |
| d=3 | ibp | 30 | 9.9 | 0.4 / 3.3 / 18.3 / 41.5 | 19 | 11 | 0 |
| d=3 | obbt | 30 | 3.3 | 0.2 / 2.7 / 5.1 / 11.8 | 18 | 1 | 0 |
| d=5 | ibp | 20 | 10.9 | 0.7 / 2.7 / 20.1 / 46.2 | 14 | 8 | 0 |
| d=5 | obbt | 20 | 4.1 | 0.5 / 1.3 / 5.6 / 21.0 | 10 | 4 | 0 |
| hidden layers=1 | ibp | 20 | 1.6 | 0.2 / 0.8 / 1.9 / 8.2 | 9 | 0 | 1 |
| hidden layers=1 | obbt | 20 | 1.6 | 0.2 / 0.8 / 1.9 / 8.2 | 9 | 0 | 1 |
| hidden layers=2 | ibp | 40 | 10.7 | 0.3 / 4.3 / 19.6 / 46.2 | 25 | 18 | 0 |
| hidden layers=2 | obbt | 40 | 3.6 | 0.1 / 1.0 / 5.4 / 21.0 | 19 | 5 | 0 |
| hidden layers=3 | ibp | 20 | 17.8 | 7.6 / 13.5 / 26.4 / 41.5 | 20 | 12 | 0 |
| hidden layers=3 | obbt | 20 | 6.0 | 3.1 / 5.1 / 9.4 / 13.7 | 18 | 3 | 0 |

R1 with IBP bounds beats R0 with OBBT bounds in 24 of 80 (net, sense) pairs.

| bounds | mean rounds R0 / R1 | mean cuts R0 | mean cuts R1 (1-D + Thm 1) | mean sep. time R0 / R1 (s) | mean total time R0 / R1 (s) |
|---|---|---|---|---|---|
| ibp | 9.8 / 11.5 | 75 | 49 + 140 | 0.41 / 1.11 | 0.64 / 1.33 |
| obbt | 9.8 / 10.2 | 78 | 65 + 100 | 0.40 / 0.96 | 0.61 / 1.18 |

Cut-loop termination (R0 status, R1 status): {('converged', 'converged'): 146, ('stalled', 'converged'): 2, ('converged', 'stalled'): 2, ('stalled', 'stalled'): 10}

### Python B&B, R0 vs R1 (600 s CPU limit)

| group | runs | closed R0 | closed R1 | both closed | SGM time R0 / R1 (s, shift 1) | SGM nodes R0 / R1 (shift 10) | median node ratio R1/R0 | median time ratio R1/R0 | R1 faster / slower (>10%) | open both: median rel. gap R0 / R1 |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 80 | 59 | 53 | 53 | 18.2 / 28.4 | 328 / 210 | 0.68 | 1.55 | 1 / 47 | 1.05e+00 / 1.34e+00 |
| act=tanh | 16 | 12 | 12 | 12 | 28.3 / 43.8 | 472 / 305 | 0.65 | 1.61 | 0 / 10 | 6.05e-01 / 7.76e-01 |
| act=sigmoid | 16 | 13 | 13 | 13 | 8.9 / 13.0 | 184 / 103 | 0.57 | 1.52 | 1 / 12 | 3.70e-01 / 5.03e-01 |
| act=silu | 16 | 11 | 10 | 10 | 19.0 / 30.0 | 364 / 225 | 0.66 | 1.72 | 0 / 9 | 3.25e+00 / 5.28e+00 |
| act=gelu | 16 | 11 | 9 | 9 | 16.4 / 27.4 | 287 / 203 | 0.73 | 1.67 | 0 / 8 | 1.05e+00 / 1.89e+00 |
| act=sin | 16 | 12 | 9 | 9 | 29.2 / 47.2 | 468 / 329 | 0.72 | 1.71 | 0 / 8 | 1.10e+00 / 1.28e+00 |
| d=2 | 30 | 30 | 30 | 30 | 11.0 / 18.7 | 201 / 143 | 0.73 | 1.67 | 0 / 30 | - |
| d=3 | 30 | 27 | 22 | 22 | 32.0 / 46.1 | 568 / 325 | 0.58 | 1.33 | 0 / 17 | 1.05e+00 / 1.89e+00 |
| d=5 | 20 | 2 | 1 | 1 | 199.3 / 166.2 | 3673 / 1011 | 0.28 | 0.83 | 1 / 0 | 9.40e-01 / 1.13e+00 |
| hidden layers=1 | 20 | 20 | 20 | 20 | 8.5 / 10.3 | 164 / 101 | 0.63 | 1.25 | 0 / 15 | - |
| hidden layers=2 | 40 | 22 | 18 | 18 | 32.0 / 61.7 | 493 / 312 | 0.68 | 2.05 | 1 / 17 | 9.40e-01 / 1.13e+00 |
| hidden layers=3 | 20 | 17 | 15 | 15 | 24.6 / 41.5 | 499 / 337 | 0.69 | 1.68 | 0 / 15 | 1.05e+00 / 1.89e+00 |

Runs open in both modes at the limit: 21; final gap smaller with R1 in 0, larger in 21.

### SCIP 10 and Gurobi 13 (context; GELU skipped)

| solver | runs | closed (gap <= max(1e-6, 1e-4 abs(UB))) | SGM time on closed (s) | Python B&B R0 / R1 closed on the same runs |
|---|---|---|---|---|
| scip | 64 | 35 | 24.2 | 48 / 44 |
| gurobi | 64 | 53 | 5.5 | 48 / 44 |
