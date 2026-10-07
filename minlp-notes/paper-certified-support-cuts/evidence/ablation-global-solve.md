# Part 5U3: a numerical global solve (Gurobi) instead of a certificate

Generated 2026-10-04T00:27:53Z by `verification/ablation_global_solve.py` (campaign-v5-protocol.md, Part 5U3). Offline: no SCIP solve; Gurobi solves only the support subproblems. Machine-readable data: `ablation-global-solve.json`. Part U (`ablation_uncertified.py`) is imported read-only.

## Command

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python /workspace/minlp-notes/paper-certified-support-cuts/verification/ablation_global_solve.py --minlplib /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3/runs/partA-full /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3/runs/partA-root /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3/runs/partB /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3d/runs/partA-root-rowdir /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3d/runs/partB-root-rowdir /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4/runs/partB2 /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4/runs/partD-root /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4/runs/partD-full --path /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3/runs/partC /workspace/minlp-notes/paper-certified-support-cuts/experiments/v3d/runs/partC-rowdir /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4/runs/partC2 /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4/runs/partC3 /workspace/minlp-notes/paper-certified-support-cuts/experiments/v4/runs/partC4 --workers 6
```

Elapsed 81.9 s wall time; 70 worker jobs on at most 6 single-threaded worker processes. Gurobi 13.0.3; parameter values read back from each model: NonConvex 2, Threads 1, Seed 0, TimeLimit 10, MIPGap 0.0001, MIPGapAbs 1e-10, FeasibilityTol 1e-06, OptimalityTol 1e-06, IntFeasTol 1e-05, Presolve -1, Method -1.

## Inputs and selection

| Part | Family | Record file SHA-256 (first 16) | Snapshot integration.py SHA-256 (first 16) | Cuts recorded | Cuts analyzed |
|---|---|---|---|---|---|
| v3/partA-full | minlplib | bfb16c124c1ac6f8 | 128fe10b13d22874 | 188 | 149 |
| v3/partA-root | minlplib | 3a03c854267c279f | 128fe10b13d22874 | 465 | 409 |
| v3/partB | minlplib | d9beda846bcd59b2 | 128fe10b13d22874 | 845 | 845 |
| v3d/partA-root-rowdir | minlplib | d93fac8024f8a8e0 | d8bdeba66604bf62 | 469 | 413 |
| v3d/partB-root-rowdir | minlplib | 49523c64329e1caf | d8bdeba66604bf62 | 529 | 529 |
| v4/partB2 | minlplib | 3e440d610a00cab9 | 35b5a4fd928e123b | 1007 | 1007 |
| v4/partD-root | minlplib | b8f4ded853d355f2 | 35b5a4fd928e123b | 1736 | 1736 |
| v4/partD-full | minlplib | 3370ea7945e18bc1 | 35b5a4fd928e123b | 28 | 28 |
| v3/partC | path | 517fe33e6af76e53 | 128fe10b13d22874 | 6000 | 47 |
| v3d/partC-rowdir | path | d526d2071aeffa5d | d8bdeba66604bf62 | 30000 | 235 |
| v4/partC2 | path | e7eeada9ef51948d | 35b5a4fd928e123b | 24000 | 170 |
| v4/partC3 | path | 194c9c7acc902a81 | 35b5a4fd928e123b | 30000 | 208 |
| v4/partC4 | path | 662adb1918f53da4 | 35b5a4fd928e123b | 48000 | 340 |

MINLPLib parts: every recorded cut with an exact certificate (151 cuts with lower-bound certificates, Arb and Bernstein, are skipped). Path family: `random.Random(0).sample(range(138000), 1000)` over the concatenated cut list of v3/partC, v3d/partC-rowdir, v4/partC2, v4/partC3, v4/partC4 (file order, then cut order within a record), as in Part U.

Cross-check with `ablation-uncertified.json`: same exact-certificate cuts in the same order (part, line, cut, certified value): **True** (6116 here, 6116 there); same sample indices: **True**.

Reconstruction: 6116 of 6116 cuts reproduce the binding stored in the support witness with the snapshot's `_prepare`, round-trip their feature strings and have binary64-exact boxes; domain rows binary64-exact for 6116; the exact expansion equals the certificate's stored problem (coefficients, bounds, rows) for 6116 of 6116 cuts. Cuts whose binary64 objective differs from the exact expansion (one or more coefficients rounded): 1522. Worker errors: 0. Certified value equals `support_stats.exact_support` for 6116 cuts.

## Method as implemented

- Selection, incumbents and case witnesses: `ablation_uncertified.scan` and the two passes of `ablation_uncertified.main`, keeping cuts whose `support_stats.method` is an exact certificate (quadratic_polytope, quadratic_polygon, quadratic_star).
- Block: features, symbols, box, domain rows and the binary64 direction (a, lambda) as recorded; the reconstruction check of Part U (the snapshot's `solver.certified._prepare` reproduces the support witness's model binding) is repeated in each worker.
- Objective: SymPy `Poly(sum_k Rational(fl(c_k)) * g_k, domain=QQ)`; every feature has total degree <= 2. The exact coefficients (constant, x_i, x_i x_j for i <= j) are compared with the certificate's `proof.quadratic.problem` and rounded to the nearest binary64 number (`float(Fraction)`). Box bounds and domain rows are rounded the same way.
- Gurobi model: one continuous variable per block variable with the box as bounds, objective constant + linear terms + quadratic terms (exact zeros omitted) to minimize, one linear row a.u <= rhs per domain row; parameters NonConvex=2, Threads=1, Seed=0, TimeLimit=10, OutputFlag=0, all others at their defaults. One Gurobi environment per worker job.
- Constants: U3 = `ObjBound`, U3p = `ObjVal` (if a solution exists), U3s = U3 - 1e-6*max(1,|U3|) evaluated in binary64. Missing or infinite constants are 'no value'.
- Comparison in exact rational arithmetic between Fraction(constant) and `support_witness.lower_bound`. Invalid: U > value; materially invalid: U - value > 1e-6*max(1,|value|).
- Removal test (materially invalid cuts only, as in Part U): `ablation_uncertified.row_check` and `summarize_rows`: the uncertified row c^T v >= r + (U - beta) is evaluated exactly at every recorded feasible point of the model (pooled by `model_sha256` over all parts given) and the case file's known witness; removal if the violation exceeds 1e-6*max(1,||c||_1). Control: the certified row at the same points. Witnessed: the recorded certified minimizer is exactly feasible and its exact objective lies below the constant by more than the material tolerance.

## Key counts

Counts are per recorded cut; '(d, m)' gives distinct cuts (model, block variables, binary64 direction) and models. inv: constant > certified value; mat: excess > 1e-6*max(1,|value|); rem: materially invalid cuts whose row is violated by more than 1e-6*max(1,||c||_1) at a recorded feasible point; KW: rem cuts that remove the known optimal witness; ctl: row-checked cuts whose certified row is violated at one of the same points.

- **MINLPLib parts** (5116 cuts, 1773 distinct, 47 models).
  U3: invalid 2311, materially invalid 4 (1 distinct, 1 model), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
  U3p: invalid 2683, materially invalid 4 (1 distinct, 1 model), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
  U3s: invalid 4, materially invalid 4 (1 distinct, 1 model), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
- **Path-family sample** (1000 cuts, 995 distinct, 60 models).
  U3: invalid 40, materially invalid 0 (0 distinct, 0 models), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
  U3p: invalid 789, materially invalid 3 (3 distinct, 3 models), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
  U3s: invalid 0, materially invalid 0 (0 distinct, 0 models), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
- **All cuts** (6116 cuts, 2768 distinct, 107 models).
  U3: invalid 2351, materially invalid 4 (1 distinct, 1 model), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
  U3p: invalid 3472, materially invalid 7 (4 distinct, 4 models), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.
  U3s: invalid 4, materially invalid 4 (1 distinct, 1 model), removing 0 (0 distinct, 0 models), known witness removed 0, control 0, no value 0.

## Counts per part

### U3

| Part | Cuts (d, m) | inv | = | < | mat (d, m) | witnessed | rem (d, m) | KW | ctl | no value | max excess | max rel. excess |
|---|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---:|
| v3/partA-full | 149 (38, 9) | 44 | 24 | 81 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 7.63e-17 | 7.63e-17 |
| v3/partA-root | 409 (360, 9) | 171 | 57 | 181 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 2.22e-16 | 2.22e-16 |
| v3/partB | 845 (366, 25) | 409 | 208 | 228 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| v3d/partA-root-rowdir | 413 (360, 9) | 175 | 57 | 181 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 2.22e-16 | 2.22e-16 |
| v3d/partB-root-rowdir | 529 (366, 25) | 271 | 138 | 120 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| v4/partB2 | 1007 (455, 25) | 538 | 303 | 166 | 2 (1, 1) | 2 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| v4/partD-root | 1736 (897, 13) | 697 | 562 | 477 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 3.24e-14 | 1.18e-15 |
| v4/partD-full | 28 (14, 2) | 6 | 14 | 8 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 7.09e-17 | 7.09e-17 |
| v3/partC | 47 (47, 15) | 3 | 3 | 41 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 2.03e-16 | 7.14e-17 |
| v3d/partC-rowdir | 235 (234, 20) | 4 | 7 | 224 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 1.58e-16 | 1.24e-16 |
| v4/partC2 | 170 (169, 19) | 6 | 3 | 161 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 5.52e-08 | 5.52e-08 |
| v4/partC3 | 208 (208, 20) | 10 | 9 | 189 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 3.69e-17 | 3.69e-17 |
| v4/partC4 | 340 (337, 20) | 17 | 8 | 315 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 3.49e-08 | 3.49e-08 |
| **all minlplib** | 5116 (1773, 47) | 2311 | 1363 | 1442 | 4 (1, 1) | 4 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| **all path** | 1000 (995, 60) | 40 | 30 | 930 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 5.52e-08 | 5.52e-08 |
| **all** | 6116 (2768, 107) | 2351 | 1393 | 2372 | 4 (1, 1) | 4 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |

### U3p

| Part | Cuts (d, m) | inv | = | < | mat (d, m) | witnessed | rem (d, m) | KW | ctl | no value | max excess | max rel. excess |
|---|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---:|
| v3/partA-full | 149 (38, 9) | 68 | 30 | 51 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 7.98e-17 | 7.98e-17 |
| v3/partA-root | 409 (360, 9) | 183 | 60 | 166 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 2.22e-16 | 2.22e-16 |
| v3/partB | 845 (366, 25) | 485 | 216 | 144 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| v3d/partA-root-rowdir | 413 (360, 9) | 187 | 60 | 166 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 2.22e-16 | 2.22e-16 |
| v3d/partB-root-rowdir | 529 (366, 25) | 307 | 142 | 80 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| v4/partB2 | 1007 (455, 25) | 576 | 308 | 123 | 2 (1, 1) | 2 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| v4/partD-root | 1736 (897, 13) | 871 | 564 | 301 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 2.51e-07 | 2.51e-07 |
| v4/partD-full | 28 (14, 2) | 6 | 14 | 8 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 7.09e-17 | 7.09e-17 |
| v3/partC | 47 (47, 15) | 35 | 3 | 9 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 2.33e-06 | 2.33e-06 |
| v3d/partC-rowdir | 235 (234, 20) | 185 | 21 | 29 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 8.87e-06 | 7.69e-06 |
| v4/partC2 | 170 (169, 19) | 134 | 7 | 29 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 4.78e-06 | 3.54e-06 |
| v4/partC3 | 208 (208, 20) | 171 | 16 | 21 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 7.18e-07 | 7.18e-07 |
| v4/partC4 | 340 (337, 20) | 264 | 13 | 63 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | 5.85e-07 | 5.85e-07 |
| **all minlplib** | 5116 (1773, 47) | 2683 | 1394 | 1039 | 4 (1, 1) | 4 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |
| **all path** | 1000 (995, 60) | 789 | 60 | 151 | 3 (3, 3) | 3 | 0 (0, 0) | 0 | 0 | 0 | 8.87e-06 | 7.69e-06 |
| **all** | 6116 (2768, 107) | 3472 | 1454 | 1190 | 7 (4, 4) | 7 | 0 (0, 0) | 0 | 0 | 0 | 0.000178 | 0.000178 |

### U3s

| Part | Cuts (d, m) | inv | = | < | mat (d, m) | witnessed | rem (d, m) | KW | ctl | no value | max excess | max rel. excess |
|---|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---:|
| v3/partA-full | 149 (38, 9) | 0 | 0 | 149 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v3/partA-root | 409 (360, 9) | 0 | 0 | 409 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v3/partB | 845 (366, 25) | 1 | 0 | 844 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 0.000177 | 0.000177 |
| v3d/partA-root-rowdir | 413 (360, 9) | 0 | 0 | 413 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v3d/partB-root-rowdir | 529 (366, 25) | 1 | 0 | 528 | 1 (1, 1) | 1 | 0 (0, 0) | 0 | 0 | 0 | 0.000177 | 0.000177 |
| v4/partB2 | 1007 (455, 25) | 2 | 0 | 1005 | 2 (1, 1) | 2 | 0 (0, 0) | 0 | 0 | 0 | 0.000177 | 0.000177 |
| v4/partD-root | 1736 (897, 13) | 0 | 0 | 1736 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v4/partD-full | 28 (14, 2) | 0 | 0 | 28 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v3/partC | 47 (47, 15) | 0 | 0 | 47 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v3d/partC-rowdir | 235 (234, 20) | 0 | 0 | 235 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v4/partC2 | 170 (169, 19) | 0 | 0 | 170 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -9.45e-07 | -9.45e-07 |
| v4/partC3 | 208 (208, 20) | 0 | 0 | 208 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -1e-06 | -1e-06 |
| v4/partC4 | 340 (337, 20) | 0 | 0 | 340 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -9.65e-07 | -9.65e-07 |
| **all minlplib** | 5116 (1773, 47) | 4 | 0 | 5112 | 4 (1, 1) | 4 | 0 (0, 0) | 0 | 0 | 0 | 0.000177 | 0.000177 |
| **all path** | 1000 (995, 60) | 0 | 0 | 1000 | 0 (0, 0) | 0 | 0 (0, 0) | 0 | 0 | 0 | -9.45e-07 | -9.45e-07 |
| **all** | 6116 (2768, 107) | 4 | 0 | 6112 | 4 (1, 1) | 4 | 0 (0, 0) | 0 | 0 | 0 | 0.000177 | 0.000177 |

## Comparison with Part U (same cuts)

U1 and U2 from `ablation-uncertified.json` (`meta.key_counts`); U3, U3p, U3s from this run.

| Family | Constant | inv | mat (d, m) | rem (d, m) | KW |
|---|---|---:|---|---|---:|
| minlplib | U1 (Part U) | 2964 | 1969 (765, 12) | 405 (105, 7) | 0 |
| minlplib | U2 (Part U) | 1621 | 230 (63, 4) | 132 (25, 2) | 0 |
| minlplib | U3 | 2311 | 4 (1, 1) | 0 (0, 0) | 0 |
| minlplib | U3p | 2683 | 4 (1, 1) | 0 (0, 0) | 0 |
| minlplib | U3s | 4 | 4 (1, 1) | 0 (0, 0) | 0 |
| path | U1 (Part U) | 983 | 976 (973, 60) | 506 (505, 58) | 404 |
| path | U2 (Part U) | 793 | 73 (73, 37) | 27 (27, 19) | 13 |
| path | U3 | 40 | 0 (0, 0) | 0 (0, 0) | 0 |
| path | U3p | 789 | 3 (3, 3) | 0 (0, 0) | 0 |
| path | U3s | 0 | 0 (0, 0) | 0 (0, 0) | 0 |

## Errors U - certified value

Exact differences between the binary64 constant and the certified value, as floats; relative = (U - value)/max(1,|value|). Nearest-rank quantiles over the cuts with a value.

| Family | Constant | Kind | n | min | q01 | q05 | q25 | median | q75 | q95 | q99 | max |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minlplib | U3 | excess | 5116 | -0.00533 | -1.23e-05 | -4.63e-11 | -1.14e-18 | 0 | 2.69e-17 | 8.33e-17 | 2.55e-16 | 0.000178 |
| minlplib | U3 | relative excess | 5116 | -6.32e-05 | -1.23e-05 | -4.63e-11 | -1.14e-18 | 0 | 2.43e-17 | 7.81e-17 | 2.12e-16 | 0.000178 |
| minlplib | U3 | abs excess | 5116 | 0 | 0 | 0 | 0 | 1.77e-17 | 6.38e-17 | 4.85e-11 | 1.4e-05 | 0.00533 |
| minlplib | U3p | excess | 5116 | -3.09e-15 | -1.27e-16 | -2.83e-17 | 0 | 1.63e-18 | 4.33e-17 | 1.42e-16 | 1.35e-14 | 0.000178 |
| minlplib | U3p | relative excess | 5116 | -5.48e-16 | -1.21e-16 | -2.83e-17 | 0 | 1.63e-18 | 3.99e-17 | 1.22e-16 | 1.12e-14 | 0.000178 |
| minlplib | U3p | abs excess | 5116 | 0 | 0 | 0 | 0 | 1.47e-17 | 5.55e-17 | 1.7e-16 | 1.35e-14 | 0.000178 |
| minlplib | U3s | excess | 5116 | -0.00541 | -2.03e-05 | -2e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | 0.000177 |
| minlplib | U3s | relative excess | 5116 | -6.42e-05 | -1.33e-05 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | 0.000177 |
| minlplib | U3s | abs excess | 5116 | 1e-06 | 1e-06 | 1e-06 | 1e-06 | 1e-06 | 1e-06 | 2.09e-06 | 2.13e-05 | 0.00541 |
| path | U3 | excess | 1000 | -0.000141 | -9.11e-05 | -1.72e-05 | -1.49e-06 | -3.64e-07 | -1.22e-07 | 0 | 2.03e-16 | 5.52e-08 |
| path | U3 | relative excess | 1000 | -9.93e-05 | -7.66e-05 | -1.72e-05 | -1.49e-06 | -3.59e-07 | -1.21e-07 | 0 | 1.24e-16 | 5.52e-08 |
| path | U3 | abs excess | 1000 | 0 | 0 | 6.07e-18 | 1.21e-07 | 3.64e-07 | 1.49e-06 | 1.72e-05 | 8.81e-05 | 0.000141 |
| path | U3p | excess | 1000 | -3.37e-16 | -2.28e-16 | -3.08e-17 | 5.04e-18 | 1.14e-09 | 7.94e-08 | 2.88e-07 | 5.29e-07 | 8.87e-06 |
| path | U3p | relative excess | 1000 | -2.66e-16 | -1.38e-16 | -2.75e-17 | 5.04e-18 | 1.14e-09 | 7.9e-08 | 2.86e-07 | 5.29e-07 | 7.69e-06 |
| path | U3p | abs excess | 1000 | 0 | 0 | 0 | 1.48e-17 | 1.14e-09 | 7.94e-08 | 2.88e-07 | 5.29e-07 | 8.87e-06 |
| path | U3s | excess | 1000 | -0.000143 | -9.22e-05 | -1.82e-05 | -2.51e-06 | -1.4e-06 | -1.16e-06 | -1e-06 | -1e-06 | -9.45e-07 |
| path | U3s | relative excess | 1000 | -0.0001 | -7.76e-05 | -1.82e-05 | -2.49e-06 | -1.36e-06 | -1.12e-06 | -1e-06 | -1e-06 | -9.45e-07 |
| path | U3s | abs excess | 1000 | 9.45e-07 | 1e-06 | 1e-06 | 1.15e-06 | 1.4e-06 | 2.5e-06 | 1.82e-05 | 8.93e-05 | 0.000143 |
| all | U3 | excess | 6116 | -0.00533 | -2.55e-05 | -1.95e-06 | -4.35e-17 | 0 | 2.27e-17 | 7.81e-17 | 2.47e-16 | 0.000178 |
| all | U3 | relative excess | 6116 | -9.93e-05 | -2.39e-05 | -1.95e-06 | -3.94e-17 | 0 | 2.2e-17 | 7.81e-17 | 2.06e-16 | 0.000178 |
| all | U3 | abs excess | 6116 | 0 | 0 | 0 | 3.22e-19 | 2.27e-17 | 1.49e-16 | 2.14e-06 | 3.21e-05 | 0.00533 |
| all | U3p | excess | 6116 | -3.09e-15 | -1.67e-16 | -2.87e-17 | 0 | 7.43e-18 | 6.42e-17 | 6.01e-08 | 2.74e-07 | 0.000178 |
| all | U3p | relative excess | 6116 | -5.48e-16 | -1.27e-16 | -2.81e-17 | 0 | 7.43e-18 | 6.38e-17 | 5.97e-08 | 2.67e-07 | 0.000178 |
| all | U3p | abs excess | 6116 | 0 | 0 | 0 | 1.08e-19 | 2.08e-17 | 7.63e-17 | 6.01e-08 | 2.74e-07 | 0.000178 |
| all | U3s | excess | 6116 | -0.00541 | -4e-05 | -5e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | 0.000177 |
| all | U3s | relative excess | 6116 | -0.0001 | -2.49e-05 | -2.95e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | -1e-06 | 0.000177 |
| all | U3s | abs excess | 6116 | 9.45e-07 | 1e-06 | 1e-06 | 1e-06 | 1e-06 | 1e-06 | 5e-06 | 4e-05 | 0.00541 |

## Gurobi statuses, times and nodes

| Part | Solved | Statuses | Spatial B&B | No bound | No solution | Runtime total / median / q95 / max (s) | Nodes median / q95 / max | > 1 node |
|---|---:|---|---:|---:|---:|---|---|---:|
| v3/partA-full | 149 | OPTIMAL 149 | 62 | 0 | 0 | 0.09 / 0.00024 / 0.0016 / 0.0019 | 0 / 1 / 1 | 0 |
| v3/partA-root | 409 | OPTIMAL 409 | 121 | 0 | 0 | 0.12 / 0.00021 / 0.0012 / 0.0022 | 0 / 1 / 1 | 0 |
| v3/partB | 845 | OPTIMAL 845 | 737 | 0 | 0 | 0.72 / 0.00047 / 0.0018 / 0.01 | 0 / 1 / 33 | 16 |
| v3d/partA-root-rowdir | 413 | OPTIMAL 413 | 125 | 0 | 0 | 0.13 / 0.00022 / 0.0012 / 0.0023 | 0 / 1 / 1 | 0 |
| v3d/partB-root-rowdir | 529 | OPTIMAL 529 | 463 | 0 | 0 | 0.42 / 0.00042 / 0.0018 / 0.0086 | 0 / 1 / 33 | 8 |
| v4/partB2 | 1007 | OPTIMAL 1007 | 890 | 0 | 0 | 0.71 / 0.00034 / 0.0018 / 0.012 | 0 / 1 / 33 | 14 |
| v4/partD-root | 1736 | OPTIMAL 1736 | 1347 | 0 | 0 | 7.14 / 0.00029 / 0.0017 / 0.39 | 0 / 3 / 5140 | 135 |
| v4/partD-full | 28 | OPTIMAL 28 | 22 | 0 | 0 | 0.02 / 0.00053 / 0.0014 / 0.0014 | 1 / 2 / 2 | 6 |
| v3/partC | 47 | OPTIMAL 47 | 47 | 0 | 0 | 0.16 / 0.0035 / 0.0077 / 0.0086 | 1 / 7 / 11 | 21 |
| v3d/partC-rowdir | 235 | OPTIMAL 235 | 235 | 0 | 0 | 1.11 / 0.0047 / 0.0084 / 0.012 | 3 / 9 / 25 | 173 |
| v4/partC2 | 170 | OPTIMAL 170 | 170 | 0 | 0 | 0.67 / 0.0039 / 0.0072 / 0.011 | 3 / 7 / 12 | 96 |
| v4/partC3 | 208 | OPTIMAL 208 | 208 | 0 | 0 | 0.87 / 0.0043 / 0.0081 / 0.012 | 3 / 9 / 17 | 137 |
| v4/partC4 | 340 | OPTIMAL 340 | 340 | 0 | 0 | 1.38 / 0.0042 / 0.0081 / 0.01 | 3 / 9 / 15 | 202 |
| **all minlplib** | 5116 | OPTIMAL 5116 | 3767 | 0 | 0 | 9.34 / 0.00029 / 0.0018 / 0.39 | 0 / 1 / 5140 | 179 |
| **all path** | 1000 | OPTIMAL 1000 | 1000 | 0 | 0 | 4.19 / 0.0043 / 0.0081 / 0.012 | 3 / 9 / 25 | 629 |
| **all** | 6116 | OPTIMAL 6116 | 4767 | 0 | 0 | 13.53 / 0.00033 / 0.006 / 0.39 | 0 / 7 / 5140 | 808 |

'Spatial B&B': models with Gurobi's `IsMIP` = 1 (nonconvex objective, solved by spatial branch and bound); the others are LPs or convex QPs solved directly (for these, ObjBound is the dual value of the continuous solve). Runtime is Gurobi's `Runtime`; the host is shared, times are descriptive.

## Sanity check: U3 = ObjBound against the certified value

Gurobi's absolute gap tolerance MIPGapAbs = 1e-10. Over 6116 cuts with a bound: U3 <= certified value for 3765; U3 <= certified value + MIPGapAbs for 6109; U3 > certified value for 2351 (by more than MIPGapAbs: 7; materially: 4).

| Family | Cuts | U3 <= value | U3 <= value + MIPGapAbs | U3 > value | U3 > value + MIPGapAbs | material |
|---|---:|---:|---:|---:|---:|---:|
| minlplib | 5116 | 2805 | 5112 | 2311 | 4 | 4 |
| path | 1000 | 960 | 997 | 40 | 3 | 0 |
| all | 6116 | 3765 | 6109 | 2351 | 7 | 4 |

Cuts with U3 > certified value, by model (d: block dimension; rows: domain rows; q: nonzero quadratic terms; nonconvex: min Hessian eigenvalue < 0):

| Model | Cuts | Distinct | d | rows | q | nonconvex | Statuses | max excess | max rel. excess |
|---|---:|---:|---|---|---|---:|---|---:|---:|
| kall_circlespolygons_c1p5b | 254 | 127 | [4] | [0] | [2, 3] | 254 | OPTIMAL 254 | 1.02e-16 | 5.55e-17 |
| cvxnonsep_normcon20r | 205 | 90 | [1] | [0] | [1] | 0 | OPTIMAL 205 | 7.96e-17 | 7.96e-17 |
| hydroenergy2 | 158 | 100 | [3, 4] | [0] | [1, 2, 3] | 158 | OPTIMAL 158 | 1.49e-15 | 1.18e-15 |
| kall_circles_c8a | 156 | 32 | [4] | [1, 3] | [6] | 156 | OPTIMAL 156 | 2.94e-16 | 1.97e-16 |
| kall_circlespolygons_c1p12 | 128 | 62 | [2, 4] | [0] | [1, 2, 3, 4] | 76 | OPTIMAL 128 | 2.55e-16 | 2.55e-16 |
| kall_ellipsoids_tc05a | 96 | 48 | [3] | [0] | [2, 3] | 16 | OPTIMAL 96 | 6.74e-17 | 6.74e-17 |
| nvs02 | 91 | 16 | [3, 4] | [0] | [2, 4, 5] | 91 | OPTIMAL 91 | 0.000178 | 0.000178 |
| pooling_rt2tp | 85 | 19 | [2, 4] | [0, 2] | [1, 2, 3] | 85 | OPTIMAL 85 | 7.63e-17 | 5.55e-17 |
| pooling_bental4pq | 71 | 11 | [2, 4] | [0, 2] | [1, 3] | 71 | OPTIMAL 71 | 4.16e-17 | 4.16e-17 |
| pooling_bental4tp | 71 | 13 | [2, 4] | [0, 2] | [1, 2, 3] | 71 | OPTIMAL 71 | 1.28e-16 | 1.28e-16 |
| kall_congruentcircles_c71 | 70 | 15 | [4] | [1] | [6] | 70 | OPTIMAL 70 | 7.63e-17 | 7.63e-17 |
| kall_congruentcircles_c72 | 68 | 18 | [4] | [1] | [6] | 68 | OPTIMAL 68 | 2.78e-17 | 2.78e-17 |
| pooling_sppa0pq | 66 | 33 | [4] | [0] | [1, 2, 3] | 66 | OPTIMAL 66 | 1.56e-16 | 1.56e-16 |
| pooling_adhya4pq | 64 | 27 | [2, 4] | [0] | [1, 2, 3] | 64 | OPTIMAL 64 | 7.63e-17 | 7.63e-17 |
| kall_congruentcircles_c61 | 59 | 10 | [4] | [1] | [6] | 59 | OPTIMAL 59 | 7.63e-17 | 7.63e-17 |
| kall_congruentcircles_c63 | 53 | 10 | [4] | [1] | [6] | 53 | OPTIMAL 53 | 5.2e-18 | 5.2e-18 |
| ex8_1_7 | 52 | 7 | [1, 2] | [0] | [1] | 9 | OPTIMAL 52 | 2.12e-16 | 2.12e-16 |
| wastewater04m2 | 46 | 19 | [2, 4] | [0, 2] | [1, 2, 3] | 46 | OPTIMAL 46 | 1.45e-16 | 1.45e-16 |
| kall_congruentcircles_c32 | 42 | 4 | [2, 4] | [0, 1, 3] | [1, 6] | 42 | OPTIMAL 42 | 8.33e-17 | 8.33e-17 |
| pooling_haverly3pq | 40 | 7 | [2, 4] | [0, 2] | [1, 2, 3] | 40 | OPTIMAL 40 | 4.16e-17 | 4.16e-17 |
| pointpack04 | 39 | 5 | [4] | [2] | [6] | 39 | OPTIMAL 39 | 8.88e-16 | 1.48e-16 |
| crudeoil_li03 | 38 | 19 | [4] | [0] | [1, 2, 3] | 38 | OPTIMAL 38 | 3.24e-14 | 7.72e-16 |
| kall_congruentcircles_c51 | 38 | 6 | [4] | [1] | [6] | 38 | OPTIMAL 38 | 7.63e-17 | 7.63e-17 |
| p_ball_10b_5p_2d_m | 37 | 16 | [2] | [0] | [2] | 0 | OPTIMAL 37 | 2.06e-16 | 2.06e-16 |
| prob06 | 31 | 3 | [2] | [0] | [2] | 0 | OPTIMAL 31 | 1.06e-17 | 1.06e-17 |
| kall_ellipsoids_tc02b | 30 | 14 | [1, 2, 3] | [0] | [1, 2, 3] | 18 | OPTIMAL 30 | 1.53e-16 | 1.53e-16 |
| pooling_haverly1tp | 29 | 5 | [2, 4] | [0, 2] | [1, 3] | 29 | OPTIMAL 29 | 1.28e-16 | 1.28e-16 |
| kall_circlesrectangles_c6r1 | 28 | 14 | [4] | [0, 2] | [4, 6] | 28 | OPTIMAL 28 | 2.95e-16 | 2.95e-16 |
| pooling_haverly2pq | 26 | 4 | [2, 4] | [0, 2] | [1, 3] | 26 | OPTIMAL 26 | 1.28e-16 | 6.42e-17 |
| multiplants_mtg6 | 24 | 12 | [3, 4] | [0] | [2] | 24 | OPTIMAL 24 | 6.82e-17 | 6.82e-17 |
| ex4_1_8 | 22 | 6 | [1] | [0] | [1] | 0 | OPTIMAL 22 | 4.15e-17 | 4.15e-17 |
| bayes2_50 | 20 | 10 | [3, 4] | [2, 3] | [2, 3, 4] | 20 | OPTIMAL 20 | 1.97e-15 | 1.97e-15 |
| nous1 | 20 | 10 | [2, 4] | [0] | [1, 2] | 20 | OPTIMAL 20 | 2.22e-16 | 2.22e-16 |
| pooling_haverly3tp | 18 | 2 | [2] | [0] | [1] | 18 | OPTIMAL 18 | 6.42e-17 | 6.42e-17 |
| ex3_1_4 | 13 | 1 | [3] | [2] | [6] | 13 | OPTIMAL 13 | 5.55e-17 | 5.55e-17 |
| tanksize | 6 | 2 | [2] | [0] | [1] | 6 | OPTIMAL 6 | 2.08e-17 | 2.08e-17 |
| kriging_peaks-full100 | 5 | 1 | [2] | [0] | [2] | 0 | OPTIMAL 5 | 7.09e-17 | 7.09e-17 |
| ex8_3_4 | 4 | 2 | [1] | [0] | [1] | 0 | OPTIMAL 4 | 5.51e-21 | 5.51e-21 |
| pooling_sppa0stp | 4 | 2 | [4] | [0] | [3] | 4 | OPTIMAL 4 | 7.81e-17 | 7.81e-17 |
| sep1 | 4 | 2 | [4] | [0] | [2, 3] | 4 | OPTIMAL 4 | 4.34e-17 | 4.34e-17 |
| interleaved_path_coupled_n80_s9 | 3 | 3 | [3] | [0] | [5] | 3 | OPTIMAL 3 | 3.24e-16 | 1.31e-16 |
| interleaved_path_n40_s3 | 3 | 3 | [3] | [0] | [5] | 3 | OPTIMAL 3 | 5.52e-08 | 5.52e-08 |
| interleaved_path_coupled_n20_s8 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 2.8e-16 | 2.22e-16 |
| interleaved_path_coupled_n80_s7 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 3.11e-16 | 3.11e-16 |
| interleaved_path_coupled_n80_s8 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 3.85e-17 | 3.2e-17 |
| interleaved_path_n40_s1 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 2.03e-16 | 7.14e-17 |
| interleaved_path_n40_s8 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 6.94e-18 | 6.94e-18 |
| interleaved_path_n80_s1 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 1.18e-08 | 1.18e-08 |
| interleaved_path_n80_s3 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 1.58e-16 | 1.24e-16 |
| interleaved_path_n80_s9 | 2 | 2 | [3] | [0] | [5] | 2 | OPTIMAL 2 | 3.9e-18 | 3.9e-18 |
| interleaved_path_coupled_n20_s9 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 3.49e-08 | 3.49e-08 |
| interleaved_path_coupled_n40_s5 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 1.05e-16 | 8.94e-17 |
| interleaved_path_coupled_n40_s6 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 1.38e-16 | 5.69e-17 |
| interleaved_path_coupled_n40_s7 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 1.52e-16 | 1.25e-16 |
| interleaved_path_coupled_n40_s8 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 5.04e-18 | 5.04e-18 |
| interleaved_path_coupled_n40_s9 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 6.94e-18 | 6.94e-18 |
| interleaved_path_coupled_n80_s5 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 3.47e-18 | 3.47e-18 |
| interleaved_path_coupled_n80_s6 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 2.4e-16 | 9.98e-17 |
| interleaved_path_n10_s2 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 1.45e-12 | 1.45e-12 |
| interleaved_path_n20_s0 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 6.37e-17 | 4.88e-17 |
| interleaved_path_n40_s5 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 6.07e-18 | 6.07e-18 |
| interleaved_path_n40_s6 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 2.47e-17 | 1.95e-17 |
| interleaved_path_n40_s7 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 5.2e-18 | 5.2e-18 |
| interleaved_path_n80_s0 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 3.33e-18 | 3.33e-18 |
| interleaved_path_n80_s2 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 4.09e-16 | 1.56e-16 |
| interleaved_path_n80_s5 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 4.34e-19 | 4.34e-19 |
| interleaved_path_n80_s7 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 1.72e-18 | 1.72e-18 |
| interleaved_path_n80_s8 | 1 | 1 | [3] | [0] | [5] | 1 | OPTIMAL 1 | 3.69e-17 | 3.69e-17 |

Individual cuts (40 of 2351, largest relative excess first; the full list is `sanity.all.above` in the JSON):

| Model | Part | Run | Cut | d | rows | q | min eig. | Status | Nodes | Certified value | U3 | Excess | Rel. excess |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| nvs02 | v3/partB | 065_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | -3.37e-06 | OPTIMAL | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | -3.37e-06 | OPTIMAL | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-noaggr | 20 | 3 | 0 | 2 | -3.37e-06 | OPTIMAL | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-rowdir-noaggr | 20 | 3 | 0 | 2 | -3.37e-06 | OPTIMAL | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 |
| interleaved_path_n40_s3 | v4/partC2 | 008_interleaved_path_n40_s3__full__s0__frozen-wide | 526 | 3 | 0 | 5 | -0.481 | OPTIMAL | 3 | -0.247010947854 | -0.247010892679 | 5.52e-08 | 5.52e-08 |
| interleaved_path_coupled_n20_s9 | v4/partC4 | 034_interleaved_path_coupled_n20_s9__root__s0__rowdir-wide | 134 | 3 | 0 | 5 | -0.503 | OPTIMAL | 3 | -0.0500030942509 | -0.0500030593758 | 3.49e-08 | 3.49e-08 |
| interleaved_path_n80_s1 | v4/partC2 | 001_interleaved_path_n80_s1__full__s0__frozen-wide | 471 | 3 | 0 | 5 | -0.491 | OPTIMAL | 3 | -0.091239048811 | -0.0912390370539 | 1.18e-08 | 1.18e-08 |
| interleaved_path_n10_s2 | v4/partC2 | 017_interleaved_path_n10_s2__full__s0__frozen-wide | 142 | 3 | 0 | 5 | -0.519 | OPTIMAL | 6 | -0.133077774445 | -0.133077774444 | 1.45e-12 | 1.45e-12 |
| bayes2_50 | v3/partB | 076_bayes2_50__root__s0__all-diag | 1 | 4 | 3 | 3 | -0.000695 | OPTIMAL | 0 | -0.928748449027 | -0.928748449027 | 1.97e-15 | 1.97e-15 |
| bayes2_50 | v3d/partB-root-rowdir | 016_bayes2_50__root__s0__all-diag | 1 | 4 | 3 | 3 | -0.000695 | OPTIMAL | 0 | -0.928748449027 | -0.928748449027 | 1.97e-15 | 1.97e-15 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag-rowdir | 14 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -1.26666666667 | -1.26666666667 | 1.49e-15 | 1.18e-15 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 14 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -1.26666666667 | -1.26666666667 | 1.49e-15 | 1.18e-15 |
| crudeoil_li03 | v4/partD-root | 018_crudeoil_li03__root__s0__all-diag-rowdir | 28 | 4 | 0 | 3 | -0.00827 | OPTIMAL | 0 | -42 | -42 | 3.24e-14 | 7.72e-16 |
| crudeoil_li03 | v4/partD-root | 018_crudeoil_li03__root__s0__all-diag | 28 | 4 | 0 | 3 | -0.00827 | OPTIMAL | 0 | -42 | -42 | 3.24e-14 | 7.72e-16 |
| bayes2_50 | v3/partB | 076_bayes2_50__root__s0__all-diag | 0 | 4 | 2 | 4 | -0.000855 | OPTIMAL | 0 | -2 | -2 | 1.33e-15 | 6.65e-16 |
| bayes2_50 | v3d/partB-root-rowdir | 016_bayes2_50__root__s0__all-diag | 0 | 4 | 2 | 4 | -0.000855 | OPTIMAL | 0 | -2 | -2 | 1.33e-15 | 6.65e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag-rowdir | 19 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -1.26666666667 | -1.26666666667 | 7.83e-16 | 6.18e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 19 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -1.26666666667 | -1.26666666667 | 7.83e-16 | 6.18e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag-rowdir | 22 | 4 | 0 | 3 | -0.245 | OPTIMAL | 0 | -1.99972315359 | -1.99972315359 | 8.93e-16 | 4.46e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 22 | 4 | 0 | 3 | -0.245 | OPTIMAL | 0 | -1.99972315359 | -1.99972315359 | 8.93e-16 | 4.46e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag-rowdir | 59 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -0.381248923341 | -0.381248923341 | 3.58e-16 | 3.58e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 59 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -0.381248923341 | -0.381248923341 | 3.58e-16 | 3.58e-16 |
| bayes2_50 | v4/partB2 | 016_bayes2_50__root__s0__all-diag-noaggr | 3 | 4 | 2 | 3 | -0.0013 | OPTIMAL | 1 | -0.990176641808 | -0.990176641808 | 3.41e-16 | 3.41e-16 |
| bayes2_50 | v4/partB2 | 016_bayes2_50__root__s0__all-diag-rowdir-noaggr | 3 | 4 | 2 | 3 | -0.0013 | OPTIMAL | 1 | -0.990176641808 | -0.990176641808 | 3.41e-16 | 3.41e-16 |
| crudeoil_li03 | v4/partD-root | 018_crudeoil_li03__root__s0__all-diag-rowdir | 1 | 4 | 0 | 2 | -0.019 | OPTIMAL | 0 | -2.59090909091 | -2.59090909091 | 8.42e-16 | 3.25e-16 |
| crudeoil_li03 | v4/partD-root | 018_crudeoil_li03__root__s0__all-diag | 1 | 4 | 0 | 2 | -0.019 | OPTIMAL | 0 | -2.59090909091 | -2.59090909091 | 8.42e-16 | 3.25e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 100 | 4 | 0 | 3 | -0.0324 | OPTIMAL | 0 | -0.781248923341 | -0.781248923341 | 3.2e-16 | 3.2e-16 |
| interleaved_path_coupled_n80_s7 | v4/partC4 | 022_interleaved_path_coupled_n80_s7__root__s0__frozen-wide | 552 | 3 | 0 | 5 | -0.498 | OPTIMAL | 7 | -0.0246357172222 | -0.0246357172222 | 3.11e-16 | 3.11e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 75 | 3 | 0 | 2 | -0.0228 | OPTIMAL | 0 | -0.927388358965 | -0.927388358965 | 3e-16 | 3e-16 |
| kall_circlesrectangles_c6r1 | v4/partD-root | 013_kall_circlesrectangles_c6r1__root__s0__all-diag-rowdir | 16 | 4 | 0 | 6 | -0.108 | OPTIMAL | 1 | 0.567567567568 | 0.567567567568 | 2.95e-16 | 2.95e-16 |
| kall_circlesrectangles_c6r1 | v4/partD-root | 013_kall_circlesrectangles_c6r1__root__s0__all-diag | 16 | 4 | 0 | 6 | -0.108 | OPTIMAL | 1 | 0.567567567568 | 0.567567567568 | 2.95e-16 | 2.95e-16 |
| hydroenergy2 | v4/partD-root | 008_hydroenergy2__root__s0__all-diag | 132 | 3 | 0 | 2 | -0.245 | OPTIMAL | 0 | -1.99778951246 | -1.99778951246 | 5.6e-16 | 2.81e-16 |
| kall_circlespolygons_c1p12 | v4/partB2 | 004_kall_circlespolygons_c1p12__root__s0__all-diag-noaggr | 10 | 4 | 0 | 3 | -0.00465 | OPTIMAL | 1 | -0.520833333333 | -0.520833333333 | 2.55e-16 | 2.55e-16 |
| kall_circlespolygons_c1p12 | v4/partB2 | 004_kall_circlespolygons_c1p12__root__s0__all-diag-noaggr | 13 | 4 | 0 | 3 | -0.00465 | OPTIMAL | 1 | -0.520833333333 | -0.520833333333 | 2.55e-16 | 2.55e-16 |
| kall_circlespolygons_c1p12 | v4/partB2 | 004_kall_circlespolygons_c1p12__root__s0__all-diag-rowdir-noaggr | 10 | 4 | 0 | 3 | -0.00465 | OPTIMAL | 1 | -0.520833333333 | -0.520833333333 | 2.55e-16 | 2.55e-16 |
| kall_circlespolygons_c1p12 | v4/partB2 | 004_kall_circlespolygons_c1p12__root__s0__all-diag-rowdir-noaggr | 13 | 4 | 0 | 3 | -0.00465 | OPTIMAL | 1 | -0.520833333333 | -0.520833333333 | 2.55e-16 | 2.55e-16 |
| crudeoil_li03 | v4/partD-root | 018_crudeoil_li03__root__s0__all-diag-rowdir | 7 | 4 | 0 | 2 | -0.0185 | OPTIMAL | 0 | 0.105984244263 | 0.105984244263 | 2.47e-16 | 2.47e-16 |
| crudeoil_li03 | v4/partD-root | 018_crudeoil_li03__root__s0__all-diag | 7 | 4 | 0 | 2 | -0.0185 | OPTIMAL | 0 | 0.105984244263 | 0.105984244263 | 2.47e-16 | 2.47e-16 |
| interleaved_path_coupled_n20_s8 | v4/partC4 | 013_interleaved_path_coupled_n20_s8__full__s0__rowdir-wide | 30 | 3 | 0 | 5 | -0.52 | OPTIMAL | 0 | -1.26048917555 | -1.26048917555 | 2.8e-16 | 2.22e-16 |
| nous1 | v3/partA-root | 004_nous1__root__s0__all-diag | 16 | 2 | 0 | 1 | -0.00333 | OPTIMAL | 0 | -1 | -1 | 2.22e-16 | 2.22e-16 |

## Notable cases

### U3: materially invalid cuts (4)

By model: nvs02 4.

Largest relative excesses (4 of 4):

| Model | Part | Run | Cut | d | rows | q | Status | Nodes | Gap | Certified value | Constant | Excess | Rel. excess | Removes | Part U U1/U2 mat. |
|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| nvs02 | v3/partB | 065_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-noaggr | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-rowdir-noaggr | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |

### U3p: materially invalid cuts (7)

By model: nvs02 4, interleaved_path_n40_s4 1, interleaved_path_n80_s4 1, interleaved_path_n80_s3 1.

Largest relative excesses (7 of 7):

| Model | Part | Run | Cut | d | rows | q | Status | Nodes | Gap | Certified value | Constant | Excess | Rel. excess | Removes | Part U U1/U2 mat. |
|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| nvs02 | v3/partB | 065_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-noaggr | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-rowdir-noaggr | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136362087131 | 0.000178 | 0.000178 | 0/19 | True/True |
| interleaved_path_n80_s4 | v3d/partC-rowdir | 004_interleaved_path_n80_s4__full__s0__all-diag-mech-wide | 1057 | 3 | 0 | 5 | OPTIMAL | 2 | 3.55e-05 | -1.15335193907 | -1.15334306621 | 8.87e-06 | 7.69e-06 | 0/18 | True/False |
| interleaved_path_n80_s3 | v4/partC2 | 023_interleaved_path_n80_s3__root__s0__frozen-wide | 696 | 3 | 0 | 5 | OPTIMAL | 2 | 6.82e-05 | -1.34789072663 | -1.34788595058 | 4.78e-06 | 3.54e-06 | 0/18 | True/False |
| interleaved_path_n40_s4 | v3/partC | 009_interleaved_path_n40_s4__full__s0__all-diag-mech | 10 | 3 | 0 | 5 | OPTIMAL | 1 | 5.41e-05 | -0.102686202686 | -0.102683870327 | 2.33e-06 | 2.33e-06 | 0/18 | True/False |

### U3s: materially invalid cuts (4)

By model: nvs02 4.

Largest relative excesses (4 of 4):

| Model | Part | Run | Cut | d | rows | q | Status | Nodes | Gap | Certified value | Constant | Excess | Rel. excess | Removes | Part U U1/U2 mat. |
|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| nvs02 | v3/partB | 065_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136363087131 | 0.000177 | 0.000177 | 0/19 | True/True |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all-diag | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136363087131 | 0.000177 | 0.000177 | 0/19 | True/True |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-noaggr | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136363087131 | 0.000177 | 0.000177 | 0/19 | True/True |
| nvs02 | v4/partB2 | 005_nvs02__root__s0__all-diag-rowdir-noaggr | 20 | 3 | 0 | 2 | OPTIMAL | 0 | 0 | -0.136540286251 | -0.136363087131 | 0.000177 | 0.000177 | 0/19 | True/True |

### Gurobi status other than OPTIMAL (0)

None.


## Notes added after the run (hand-written)

Everything above this section was generated by the script. This section was
added by hand after the run and is not regenerated.

### Other commands run (targeted; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
P=/workspace/minlp-notes/paper-certified-support-cuts; E=$P/experiments
# Smoke test (output in a mktemp directory, then deleted): exit 0, 58 cuts, 0 errors
T=$(mktemp -d)
$PY -B $P/verification/ablation_global_solve.py --minlplib $E/v4/runs/partD-full --path $E/v4/runs/partC4 \
    --sample-size 30 --workers 6 --out-md $T/smoke.md --out-json $T/smoke.json
# Protocol run: the command at the top of this file (exit 0; 2026-10-04 00:26:31 to 00:27:54 UTC)
# Independent spot check (fresh process; writes evidence/ablation-global-solve-spotcheck.json)
$PY -B $P/verification/ablation_global_solve_spotcheck.py --count 50 --seed 3
```

### Independent spot check (50 cuts, seed 3)

`verification/ablation_global_solve_spotcheck.py` does not import
`ablation_global_solve` or `ablation_uncertified`. It picks
`random.Random(3).sample(range(6116), 50)` from the stored `cuts` list. These
are 41 MINLPLib cuts and 9 path-family cuts from 11 parts. For each cut it:

- re-reads the cut from its `records.jsonl` line;
- recomputes the certified value from `support_witness.lower_bound`;
- expands the objective by a different SymPy route (`expand` and
  `as_coefficients_dict`) and checks it against the certificate's stored
  problem;
- rebuilds the Gurobi model in a fresh process and re-solves it with the
  protocol parameters.

Results, out of 50:

- model name and certified value equal the stored ones: 50;
- the expansion equals the certificate's problem: 50;
- ObjBound and ObjVal are identical to the stored values, bit for bit: 50 and 50;
- status and node count are identical: 50 and 50;
- the exact excesses and the invalid and material flags of U3, U3p and U3s
  recomputed from these numbers equal the stored ones: 50.

The sample contains none of the 4 nvs02 cuts. The diagnostic below reproduces
their stored ObjBound and ObjVal exactly, also in a fresh process, with the
terms of the model added in a different order.

### The materially invalid U3: nvs02, cut 20 (diagnostic only)

There is 1 distinct cut, recorded 4 times: v3/partB, v3d/partB-root-rowdir
and v4/partB2 (twice), in all-diag modes, run 065 or 005, cut 20.

- **Block.** Variables (x0, x2, x4), box [0, 200]^3, no domain rows. After
  expansion the objective is
  -6.7554e-4 x0 - 3.2947e-4 x2 - 6.7554e-4 x4 + 3.3732e-6 x0 x4 + 2.1627e-5 x2^2.
  It is nonconvex (minimum Hessian eigenvalue -3.37e-6). Gurobi solves it by
  spatial B&B (`IsMIP` = 1).
- **Certified minimum.** -0.136540286251, at (200, 7.617..., 200). The
  certificate's minimizer is exactly feasible. Its value in the rounded
  binary64 model is also -0.136540286251.
- **Gurobi with the protocol parameters.** It reports OPTIMAL after 0 nodes,
  with gap 0, ObjBound = ObjVal = -0.136362087131 at u = (200, 7.6171875, 0).
  This is 1.78e-4 above the certified minimum, so U3, U3p and U3s are all
  materially invalid.
- **Cause: the optimality tolerance.** At x0 = 200 the derivative of the
  objective in x4 is -6.7554e-4 + 3.3732e-6 * 200 = -8.9e-7. This is smaller in
  magnitude than OptimalityTol = 1e-6, so x4 = 0 is accepted as optimal. Over
  a box width of 200 the loss is 8.9e-7 * 200 = 1.78e-4, which is the excess.
- **Diagnostic re-solves** (run from a temporary script, not part of the
  protocol):

  | Settings | ObjBound | ObjVal | Nodes | x4 |
  |---|---|---|---|---|
  | protocol (default tolerances) | -0.136362087131 | -0.136362087131 | 0 | 0 |
  | MIPGap = MIPGapAbs = 0 | -0.136362087131 | -0.136362087131 | 0 | 0 |
  | NumericFocus = 3 | -0.136362087131 | -0.136362087131 | 0 | 0 |
  | Presolve = 0 | -0.136540286273 | -0.136540286129 | 1 | 200 |
  | FeasibilityTol = OptimalityTol = 1e-9 | -0.136540286251 | -0.136540286251 | 0 | 200 |

- **Removal test.** None of these rows removes a recorded feasible point
  (0 of 19 points for nvs02).
- **Part U on the same cut.** U1 and U2 are also materially invalid.

### Reading the sanity check

- **U3 above the certified value.** U3 > value for 2,351 of 6,116 cuts. For
  2,344 of them the excess is at most 1e-10 (MIPGapAbs). Their largest
  relative excess is 1.45e-12, and every other one is at most 2e-15, which is
  binary64 rounding size.
- **Rounding of the model.** Only 353 of the 2,351 have a rounded binary64
  objective. In the others the model is exact, and the excess comes from
  Gurobi's floating-point arithmetic.
- **The 7 cuts above MIPGapAbs.** Every one reports OPTIMAL. Four are the
  nvs02 cut above (1.78e-4). Three are path-family cuts, all with relative
  excess below the material tolerance and 3 nodes each:
  - interleaved_path_n40_s3, C2 cut 526: 5.5e-8;
  - interleaved_path_coupled_n20_s9, C4 cut 134: 3.5e-8;
  - interleaved_path_n80_s1, C2 cut 471: 1.2e-8.
- **U3 well below the value.** The other tail is wide: the largest relative
  deficit is 9.9e-5 (interleaved_path_coupled_n80_s7). This is consistent
  with stopping once the relative gap is at most MIPGap = 1e-4.
- **U3p.** U3p = ObjVal is the value of a feasible point, so it is normally at
  or above the minimum: 3,472 cuts are invalid. Seven are materially invalid.
  - Four are the nvs02 cut.
  - Three are path-family cuts that stopped with a final relative MIP gap of
    3.6e-5 to 6.8e-5, below MIPGap = 1e-4. Their excesses are 2.3e-6 to
    7.7e-6 relative, and their U3 values lie below the certified value.
  - None of these rows removes a recorded feasible point or a known witness.
- **U3s.** The shift of 1e-6*max(1,|U3|) removes every invalid U3 except the
  nvs02 cut, whose excess (1.78e-4) is far larger than the shift.
