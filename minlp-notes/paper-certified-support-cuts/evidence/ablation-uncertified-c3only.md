# Part U: what certification buys (offline ablation)

Generated 2026-10-03T17:24:36Z by `verification/ablation_uncertified.py` (campaign-v4-protocol.md, Amendment 1, Part U). No solver was run. Machine-readable data: `ablation-uncertified.json`.

## Inputs

| Part | Family | Record file SHA-256 (first 16) | Snapshot integration.py SHA-256 (first 16) | Cuts recorded | Cuts analyzed |
|---|---|---|---|---|---|
| v3/partA-full | minlplib | bfb16c124c1ac6f8 | 128fe10b13d22874 | 188 | 188 |
| v3/partA-root | minlplib | 3a03c854267c279f | 128fe10b13d22874 | 465 | 465 |
| v3/partB | minlplib | d9beda846bcd59b2 | 128fe10b13d22874 | 845 | 845 |
| v3d/partA-root-rowdir | minlplib | d93fac8024f8a8e0 | d8bdeba66604bf62 | 469 | 469 |
| v3d/partB-root-rowdir | minlplib | 49523c64329e1caf | d8bdeba66604bf62 | 529 | 529 |
| v3/partC | path | 517fe33e6af76e53 | 128fe10b13d22874 | 6000 | 180 |
| v3d/partC-rowdir | path | d526d2071aeffa5d | d8bdeba66604bf62 | 30000 | 820 |

Path-family sample: `random.Random(0).sample(range(36000), 1000)` over the concatenated cut list of v3/partC, v3d/partC-rowdir (file order, then cut order within a record), processed in sorted order.

## Key counts

Counts are per recorded cut: a cut recorded in several runs (seeds, modes, parts) counts each time; 'distinct' identifies a cut by (model, block variables, binary64 direction).

- **MINLPLib parts, exact certificates** (2345 cuts, 727 distinct, 34 models).
  U1: exceeds the certified minimum for 1280 cuts, materially for 931 (327 distinct, 8 models). 278 materially invalid cuts (81 distinct) would remove a recorded feasible point, in 6 models: cvxnonsep_normcon20r, ex4_1_8, ex8_3_4, nvs02, p_ball_10b_5p_2d_m, prob06.
  U2: exceeds the certified minimum for 573 cuts, materially for 101 (26 distinct, 1 model). 81 materially invalid cuts (24 distinct) would remove a recorded feasible point, in 1 model: nvs02.
  Of the 101 U2-materially invalid cuts, 101 had every SLSQP run stop after at most one iteration (all runs reported success).
- **Path-family sample, exact certificates** (1000 cuts, 977 distinct, 20 models).
  U1: exceeds the certified minimum for 990 cuts, materially for 987 (964 distinct, 20 models). 464 materially invalid cuts (453 distinct) would remove a recorded feasible point, in 20 models; 359 of them remove the known optimal witness.
  U2: exceeds the certified minimum for 757 cuts, materially for 74 (72 distinct, 17 models). 21 materially invalid cuts (20 distinct) would remove a recorded feasible point, in 14 models; 15 of them remove the known optimal witness.
  Of the 74 U2-materially invalid cuts, 1 had every SLSQP run stop after at most one iteration (all runs reported success).
- **MINLPLib parts, lower-bound certificates** (Bernstein, Arb; 151 cuts, 3 models): U1 exceeds the certified bound materially for 151, U2 for 151; not counted as invalid. The uncertified row removes a recorded feasible point for 7 cuts with U1 (ex4_1_8) and 0 with U2; such a removal shows directly that the uncertified constant exceeds the true minimum.

## Method as implemented

- Sample set: `solver.integration._sample(block, Config(**record['config']))` of the run's own snapshot (the routine behind the direction LP `propose_direction`): `np.linspace` grids with `grid_1d` = 33 points in 1D, `grid_2d` = 7 per axis in 2D and 3 per axis for d = 3, 4, filtered by the domain rows (tolerance 1e-12*max(1,|rhs|)), plus the exact vertices of box and domain rows (`theory.quadratic_polytope.polytope_vertices`) and their centroid for quadratic blocks within the face budget. Sample values come from `solver.integration._evaluate` (SymPy lambdify, NumPy binary64). Exchange samples (certified minimizers added later by the separator) are excluded.
- Block: features, symbols, box, domain rows and the binary64 direction (a, lambda) as recorded; the reconstruction is accepted only if the snapshot's `solver.certified._prepare` reproduces the model binding stored in the support witness. `quadratic` is recomputed as in `discover` (every side polynomial of total degree <= 2).
- U1 = min over the sample of `sample @ (a, lambda)` in binary64.
- U2 = min(U1, SLSQP values): `scipy.optimize.minimize(method='SLSQP')` from the 3 best samples (stable sort), bounds = block box, inequality constraints = domain rows (with their exact Jacobian), analytic objective gradient (SymPy), default tolerances, maxiter 200; the final point is clipped to the box and accepted if every domain row holds within 1e-09*max(1,|rhs|); its value is re-evaluated with `_evaluate` in binary64.
- Comparison in exact rational arithmetic with `support_witness.lower_bound`. Invalid: U > value; materially invalid: U - value > 1e-6*max(1,|value|). Exact certificates: quadratic_polytope, quadratic_polygon, quadratic_star; Bernstein and Arb are lower bounds and reported separately.
- Uncertified row: c^T v >= r + (U - beta), with c = `row_certificate.exact.coefficients`, r = `exact.eliminated_rhs` and beta = the recorded binary64 support constant (`binding.support.rhs`), i.e. exactly U - sum_r lambda_r b_r. Columns `x<i>` map to `original_values[i]` (the record's `column_names` are checked to be `v<i>` in the same order); the column `objective_epigraph` takes the incumbent's objective value (`primal_check.objective`, else `primal`; for a case witness `known_optimum_exact`).
- Incumbents: every record (any part, mode, seed) of the same model (same `model_sha256`) with `original_values` whose `primal_check.passed` is true, plus the case file's `known_witness_exact` when present. Removal: violation > 1e-6*max(1,||c||_1), exact.

Reconstruction: for 3496 of 3496 analyzed cuts the reconstructed block (features, symbols, box, domain rows, direction) gives exactly the model binding stored in the support witness (`_prepare` of the snapshot), the feature strings round-trip, and the recorded box is binary64-exact. Worker errors: 0; binding mismatches: 0.
For 3345 of 3345 exact-certificate cuts, the certified value (`support_witness.lower_bound`) equals the recorded exact minimum (`support_stats.exact_support`).

## Exact certificates: invalid uncertified constants

Counts of cuts whose uncertified constant exceeds the certified exact minimum (invalid) and exceeds it by more than 1e-6*max(1,|value|) (materially invalid). `=`: the constant equals the exact minimum; `<`: it lies below it (binary64 evaluation rounding at or near the minimizer, or an SLSQP point within the row tolerance); the last column gives the largest such deficit relative to max(1,|value|).

| Part | Method | Cuts | U1 invalid | U1 material | U1 = | U1 < | U1 max excess | U2 invalid | U2 material | U2 = | U2 < | U2 max excess | max rel. deficit U1 / U2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v3/partA-full | quadratic_polytope | 149 | 81 | 72 | 30 | 38 | 0.00347 | 18 | 0 | 30 | 101 | 2.08e-17 | 1.39e-17 / 6.34e-17 |
| v3/partA-root | quadratic_polytope | 409 | 313 | 280 | 66 | 30 | 0.00758 | 88 | 0 | 66 | 255 | 3.19e-09 | 1.11e-16 / 1.67e-16 |
| v3/partB | quadratic_polytope | 845 | 366 | 191 | 203 | 276 | 0.0167 | 239 | 65 | 210 | 396 | 0.0107 | 2.08e-16 / 1.05e-12 |
| v3d/partA-root-rowdir | quadratic_polytope | 413 | 313 | 280 | 66 | 34 | 0.00758 | 88 | 0 | 66 | 259 | 3.19e-09 | 1.11e-16 / 1.67e-16 |
| v3d/partB-root-rowdir | quadratic_polytope | 529 | 207 | 108 | 139 | 183 | 0.0167 | 140 | 36 | 142 | 247 | 0.0107 | 2.08e-16 / 1.05e-12 |
| v3/partC | quadratic_polytope | 180 | 175 | 175 | 3 | 2 | 0.0343 | 140 | 15 | 7 | 33 | 0.0206 | 1.97e-17 / 1.21e-16 |
| v3d/partC-rowdir | quadratic_polytope | 820 | 815 | 812 | 5 | 0 | 0.089 | 617 | 59 | 53 | 150 | 0.0275 | - / 2.22e-16 |
| **all minlplib** | exact | 2345 | 1280 | 931 | | | | 573 | 101 | | | | |
| **all path** | exact | 1000 | 990 | 987 | | | | 757 | 74 | | | | |

## Exact certificates: would the uncertified cut remove a recorded feasible point?

For each materially invalid cut, the eliminated row with the uncertified constant is evaluated exactly at every recorded incumbent of the same model (and at the known optimal witness of the case file, where one exists). `Removing` counts cuts violated by more than 1e-6*max(1,||c||_1) at one or more of these points. `Witnessed` counts materially invalid cuts for which the recorded certified minimizer is exactly feasible and its exact objective value lies below the uncertified constant by more than the material tolerance (an explicit feasible counterexample to the uncertified support inequality, independent of the oracle's proof). `Control` counts cuts whose certified row is violated by more than the tolerance at one of the points.

| Part | Variant | Material | Witnessed | Rows checked | Removing | Models removing / material | Known witness removed | Control |
|---|---|---|---|---|---|---|---|---|
| v3/partA-full | U1 | 72 | 72 | 72 | 21 | 2 / 4 | 0 | 0 |
| v3/partA-full | U2 | 0 | 0 | 0 | 0 | 0 / 0 | 0 | 0 |
| v3/partA-root | U1 | 280 | 280 | 280 | 55 | 4 / 4 | 0 | 0 |
| v3/partA-root | U2 | 0 | 0 | 0 | 0 | 0 / 0 | 0 | 0 |
| v3/partB | U1 | 191 | 191 | 191 | 96 | 2 / 4 | 0 | 0 |
| v3/partB | U2 | 65 | 65 | 65 | 51 | 1 / 1 | 0 | 0 |
| v3d/partA-root-rowdir | U1 | 280 | 280 | 280 | 55 | 4 / 4 | 0 | 0 |
| v3d/partA-root-rowdir | U2 | 0 | 0 | 0 | 0 | 0 / 0 | 0 | 0 |
| v3d/partB-root-rowdir | U1 | 108 | 108 | 108 | 51 | 2 / 4 | 0 | 0 |
| v3d/partB-root-rowdir | U2 | 36 | 36 | 36 | 30 | 1 / 1 | 0 | 0 |
| v3/partC | U1 | 175 | 175 | 175 | 60 | 16 / 19 | 41 | 0 |
| v3/partC | U2 | 15 | 15 | 15 | 0 | 0 / 9 | 0 | 0 |
| v3d/partC-rowdir | U1 | 812 | 812 | 812 | 404 | 20 / 20 | 318 | 0 |
| v3d/partC-rowdir | U2 | 59 | 59 | 59 | 21 | 14 / 17 | 15 | 0 |

- minlplib, U1: 278 cuts would remove a recorded feasible point, in 6 models: cvxnonsep_normcon20r, ex4_1_8, ex8_3_4, nvs02, p_ball_10b_5p_2d_m, prob06.
- minlplib, U2: 81 cuts would remove a recorded feasible point, in 1 model: nvs02.
- path, U1: 464 cuts would remove a recorded feasible point, in 20 models.
- path, U2: 21 cuts would remove a recorded feasible point, in 14 models.

Incumbents available per model with a materially invalid cut:

- minlplib: 8 models; points per model min 14, median 15.5, max 17.
- path: 20 models; points per model min 11, median 11.0, max 11.

## Largest excesses (exact certificates)

**minlplib, U1** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| kall_circlespolygons_c1p12 | v3/partB | 064_kall_circlespolygons_c1p12__root__s0__all-diag | 0 | 2 | 0 | 2 | -0.2833333333 | -0.2666666667 | 0.0167 | 0/14 |
| kall_circlespolygons_c1p12 | v3d/partB-root-rowdir | 004_kall_circlespolygons_c1p12__root__s0__all-diag | 0 | 2 | 0 | 2 | -0.2833333333 | -0.2666666667 | 0.0167 | 0/14 |
| nvs02 | v3/partB | 005_nvs02__full__s0__auto | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3/partB | 005_nvs02__full__s0__all | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3/partB | 035_nvs02__full__s1__all | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3/partB | 035_nvs02__full__s1__auto | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3/partB | 065_nvs02__root__s0__all | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3/partB | 065_nvs02__root__s0__auto | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3/partB | 065_nvs02__root__s0__all-diag | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all | 2 | 4 | 0 | 3 | -0.01351673329 | 0 | 0.0135 | 0/14 |

**minlplib, U2** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| nvs02 | v3/partB | 005_nvs02__full__s0__auto | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3/partB | 005_nvs02__full__s0__all | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3/partB | 035_nvs02__full__s1__all | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3/partB | 035_nvs02__full__s1__auto | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3/partB | 065_nvs02__root__s0__all | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3/partB | 065_nvs02__root__s0__auto | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3/partB | 065_nvs02__root__s0__all-diag | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__auto | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |
| nvs02 | v3d/partB-root-rowdir | 005_nvs02__root__s0__all-diag | 0 | 4 | 0 | 3 | -0.0107476865 | 0 | 0.0107 | 0/14 |

**path, U1** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| interleaved_path_n80_s3 | v3d/partC-rowdir | 003_interleaved_path_n80_s3__full__s0__all-diag-mech-wide | 226 | 3 | 0 | 1 | -0.5687255859 | -0.4797363281 | 0.089 | 11/11 |
| interleaved_path_n40_s0 | v3d/partC-rowdir | 005_interleaved_path_n40_s0__full__s0__all-diag-mech-wide | 61 | 3 | 0 | 1 | -1.010864258 | -0.921875 | 0.089 | 9/11 |
| interleaved_path_n80_s3 | v3d/partC-rowdir | 023_interleaved_path_n80_s3__root__s0__all-diag-mech-wide | 257 | 3 | 0 | 1 | -0.5516357422 | -0.46875 | 0.0829 | 11/11 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 020_interleaved_path_n80_s0__root__s0__all-diag-mech-wide | 147 | 3 | 0 | 1 | -0.4652099609 | -0.390625 | 0.0746 | 11/11 |
| interleaved_path_n80_s1 | v3d/partC-rowdir | 001_interleaved_path_n80_s1__full__s0__all-diag-mech | 70 | 3 | 0 | 1 | -0.2371826172 | -0.1875 | 0.0497 | 11/11 |
| interleaved_path_n40_s1 | v3d/partC-rowdir | 006_interleaved_path_n40_s1__full__s0__all-diag-mech-wide | 11 | 3 | 0 | 1 | -0.4034423828 | -0.359375 | 0.0441 | 11/11 |
| interleaved_path_n10_s2 | v3d/partC-rowdir | 017_interleaved_path_n10_s2__full__s0__all-diag-mech-wide | 4 | 3 | 0 | 1 | -0.5870361328 | -0.54296875 | 0.0441 | 11/11 |
| interleaved_path_n40_s2 | v3d/partC-rowdir | 007_interleaved_path_n40_s2__full__s0__all-diag-mech-wide | 109 | 3 | 0 | 1 | -1.010864258 | -0.9675292969 | 0.0433 | 11/11 |
| interleaved_path_n20_s3 | v3d/partC-rowdir | 013_interleaved_path_n20_s3__full__s0__all-diag-mech | 12 | 3 | 0 | 1 | -0.9669189453 | -0.9260253906 | 0.0409 | 11/11 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 000_interleaved_path_n80_s0__full__s0__all-diag-mech-wide | 27 | 3 | 0 | 1 | -0.1468706537 | -0.1112656467 | 0.0356 | 11/11 |

**path, U2** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| interleaved_path_n40_s2 | v3d/partC-rowdir | 027_interleaved_path_n40_s2__root__s0__all-diag-mech-wide | 13 | 3 | 0 | 1 | -0.1132104244 | -0.0856702793 | 0.0275 | 1/11 |
| interleaved_path_n80_s3 | v3d/partC-rowdir | 023_interleaved_path_n80_s3__root__s0__all-diag-mech | 318 | 3 | 0 | 1 | -0.1035783068 | -0.07771609833 | 0.0259 | 5/11 |
| interleaved_path_n80_s1 | v3d/partC-rowdir | 001_interleaved_path_n80_s1__full__s0__all-diag-mech-wide | 5 | 3 | 0 | 1 | -0.1013283514 | -0.07602792863 | 0.0253 | 2/11 |
| interleaved_path_n40_s3 | v3d/partC-rowdir | 028_interleaved_path_n40_s3__root__s0__all-diag-mech-wide | 20 | 3 | 0 | 1 | -0.09047098888 | -0.06798175159 | 0.0225 | 2/11 |
| interleaved_path_n10_s2 | v3d/partC-rowdir | 037_interleaved_path_n10_s2__root__s0__all-diag-mech-wide | 25 | 3 | 0 | 1 | -0.09399453339 | -0.07197188598 | 0.022 | 0/11 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 000_interleaved_path_n80_s0__full__s0__all-diag-mech | 138 | 3 | 0 | 1 | -0.5335693359 | -0.5120849609 | 0.0215 | 11/11 |
| interleaved_path_n40_s2 | v3/partC | 027_interleaved_path_n40_s2__root__s0__all-diag-mech | 17 | 3 | 0 | 1 | -0.08347826087 | -0.06288819876 | 0.0206 | 0/11 |
| interleaved_path_n40_s3 | v3/partC | 028_interleaved_path_n40_s3__root__s0__all-diag-mech | 26 | 3 | 0 | 1 | -0.3481012658 | -0.3375527426 | 0.0105 | 0/11 |
| interleaved_path_n10_s2 | v3d/partC-rowdir | 037_interleaved_path_n10_s2__root__s0__all-diag-mech | 32 | 3 | 0 | 1 | -0.1608979528 | -0.1527815995 | 0.00812 | 0/11 |
| interleaved_path_n80_s1 | v3/partC | 021_interleaved_path_n80_s1__root__s0__all-diag-mech | 173 | 3 | 0 | 1 | -0.007818703806 | 0 | 0.00782 | 0/11 |

## Lower-bound certificates (Bernstein, Arb)

These values are certified lower bounds, not minima: the separator only asks them to reach the separation target. An excess is therefore not evidence of invalidity, and these cuts are not counted as invalid above. The incumbent test is still applied to cuts with a material excess.

| Part | Method | Cuts | U1 > bound | U1 material | U1 max excess | U1 removing incumbent | U2 > bound | U2 material | U2 max excess | U2 removing incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| v3/partA-full | arb | 36 | 36 | 36 | 0.0384 | 0 | 36 | 36 | 0.038 | 0 |
| v3/partA-full | bernstein | 3 | 3 | 3 | 0.00415 | 3 | 3 | 3 | 0.00396 | 0 |
| v3/partA-root | arb | 53 | 53 | 53 | 0.0384 | 0 | 53 | 53 | 0.038 | 0 |
| v3/partA-root | bernstein | 3 | 3 | 3 | 0.00415 | 2 | 3 | 3 | 0.00396 | 0 |
| v3d/partA-root-rowdir | arb | 53 | 53 | 53 | 0.0384 | 0 | 53 | 53 | 0.038 | 0 |
| v3d/partA-root-rowdir | bernstein | 3 | 3 | 3 | 0.00415 | 2 | 3 | 3 | 0.00396 | 0 |

## Exported rows and the bound correction E

Over every recorded cut (not only the sample). `Rounded` counts rows whose binary64 coefficients differ from the exact eliminated rational row. E is the correction `box_compensation` of Proposition 'Safe export' (E <= 0); `|E|/max(1,|r|)` is relative to the exact eliminated right-hand side. `Safe` counts rows with exported rhs <= r + E in exact arithmetic. The last column is the further downward rounding of the exported right-hand side, relative.

| Part | Rows | Rounded | Nonzero E | Safe | max abs(E) | median abs(E) (rounded rows) | max rel. abs(E) | median rel. abs(E) | max rel. rhs rounding |
|---|---|---|---|---|---|---|---|---|---|
| v3/partA-full | 188 | 15 | 12 | 188 | 9.99e-17 | 9.99e-17 | 9.99e-17 | 9.99e-17 | 8.7e-17 |
| v3/partA-root | 465 | 56 | 36 | 465 | 2.22e-16 | 1.25e-17 | 2.22e-16 | 1.25e-17 | 2.17e-16 |
| v3/partB | 845 | 162 | 84 | 845 | 6.94e-17 | 1.12e-18 | 6.94e-17 | 1.12e-18 | 2.13e-16 |
| v3d/partA-root-rowdir | 469 | 56 | 36 | 469 | 2.22e-16 | 1.25e-17 | 2.22e-16 | 1.25e-17 | 2.17e-16 |
| v3d/partB-root-rowdir | 529 | 85 | 48 | 529 | 6.94e-17 | 1.12e-18 | 6.94e-17 | 1.12e-18 | 2.13e-16 |
| v3/partC | 6000 | 5820 | 4632 | 6000 | 1.69e-16 | 2.49e-18 | 1.29e-16 | 2.44e-18 | 2.09e-16 |
| v3d/partC-rowdir | 30000 | 26714 | 20970 | 30000 | 1.69e-16 | 1.76e-18 | 1.29e-16 | 1.73e-18 | 2.09e-16 |

## Spot checks

### nvs02 (v3/partB, run 005_nvs02__full__s0__all, cut 8, quadratic_polytope)

- Block variables ['x0', 'x1', 'x2', 'x4'], box [['0', '200'], ['0', '200'], ['0', '200'], ['0', '200']].
- Features g: ['6166297181155461*x0*x4/73786976294838206464 + 308859295109443*x2**2/576460752303423488', '-1726788183524905*x0*x1/576460752303423488 - 8222290294404651*x1*x4/1152921504606846976 - 5029735355997831*x2**2/2305843009213693952', '1726788183524905*x0*x1/576460752303423488 + 8222290294404651*x1*x4/1152921504606846976 + 5029735355997831*x2**2/2305843009213693952'].
- Signed sides: ['row0:objective', 'row2:upper', 'row2:lower'].
- Domain rows (a, rhs; a.u <= rhs): none.
- Direction a = [0.005, 4.222717865765131e-06, -0.0008107618302269047, -5.278397332206403e-06], lambda = [0.04036461322837505, 2.9605268489736884e-06, 0.0].
- U1 (sample minimum over 98 samples) = -0.0010556794664412805 at u = [0.0, 0.0, 0.0, 200.0].
- U2 (best of U1 and 3 SLSQP runs) = -0.0010556794664412805 at u = [0.0, 0.0, 0.0, 200.0]; SLSQP statuses [0, 0, 0], accepted [True, True, True].
- Certified minimum = -150375502135258265778276012508508114762282730521490227/17371253730995485306977901572027525779127032232573665280 = -0.008656571624818515, minimizer ['0', '0', '2207103636790105635413197717495611392/117712193962138935016789646786452635', '200'] = [0.0, 0.0, 18.750000000000004, 200.0].
- Exact objective at the certified minimizer = -150375502135258265778276012508508114762282730521490227/17371253730995485306977901572027525779127032232573665280; minimizer exactly feasible: True.
- Excess U1 = 0.00760089, U2 = 0.00760089 (material tolerance 1e-06).
- U1 row: violated beyond 1e-06 at 14 of 14 points (max violation 0.00555); certified row violated at 0.
- U2 row: violated beyond 1e-06 at 14 of 14 points (max violation 0.00555); certified row violated at 0.

### prob06 (v3/partB, run 011_prob06__full__s0__auto, cut 0, quadratic_polytope)

- Block variables ['x0', 'x1'], box [['1', '11/2'], ['1', '11/2']].
- Features g: ['-x0**2/16 - x1**2/16', '321685687669321*x0**2/4503599627370496 + 321685687669321*x1**2/4503599627370496'].
- Signed sides: ['row1:upper', 'row2:upper'].
- Domain rows (a, rhs; a.u <= rhs): none.
- Direction a = [-0.04700854700854702, -0.07264957264957264], lambda = [0.0, 0.2393162393162394].
- U1 (sample minimum over 54 samples) = -0.10470085470085473 at u = [1.75, 1.75].
- U2 (best of U1 and 3 SLSQP runs) = -0.10950854700854701 at u = [1.3750000000000004, 2.125]; SLSQP statuses [0, 0, 0], accepted [True, True, True].
- Certified minimum = -2286981939125961316056379994909/20884049707530728408623678966016 = -0.10950854700854702, minimizer ['1906893210599730241681747869696/1386831425890712433385166181337', '2947016780017763741885525917696/1386831425890712433385166181337'] = [1.3750000000000004, 2.125].
- Exact objective at the certified minimizer = -2286981939125961316056379994909/20884049707530728408623678966016; minimizer exactly feasible: True.
- Excess U1 = 0.00480769, U2 = 7.12211e-18 (material tolerance 1e-06).
- U1 row: violated beyond 1e-06 at 14 of 14 points (max violation 0.00409); certified row violated at 0.

### interleaved_path_n40_s2 (v3d/partC-rowdir, run 027_interleaved_path_n40_s2__root__s0__all-diag-mech-wide, cut 13, quadratic_polytope)

- Block variables ['x12', 'x13', 'x14'], box [['0', '1'], ['0', '1'], ['0', '1']].
- Features g: ['-3655*x12**2/4096 + 21*x12*x13/32 + 2*x13**2 + 11*x13*x14/16 - 903*x14**2/1024'].
- Signed sides: ['row4:upper'].
- Domain rows (a, rhs; a.u <= rhs): none.
- Direction a = [0.14096405752016714, -0.4138036201717066, 0.22032114918340268], lambda = [0.2498436951980115].
- U1 (sample minimum over 36 samples) = -0.08197996248684758 at u = [1.0, 0.0, 1.0].
- U2 (best of U1 and 3 SLSQP runs) = -0.08567027929613168 at u = [0.0, 0.4141162297756836, 1.1102230246251565e-16]; SLSQP statuses [0, 0, 0], accepted [True, True, True].
- Certified minimum = -300776761962923963955444874025221887/2656793873820401896424496190669717504 = -0.11321042438659897, minimizer ['1', '288050168984225921/1152200675936903552', '0'] = [1.0, 0.25000000000000006, 0.0].
- Exact objective at the certified minimizer = -300776761962923963955444874025221887/2656793873820401896424496190669717504; minimizer exactly feasible: True.
- Excess U1 = 0.0312305, U2 = 0.0275401 (material tolerance 1e-06).
- U1 row: violated beyond 1e-06 at 1 of 11 points (max violation 0.00887); certified row violated at 0.
- U2 row: violated beyond 1e-06 at 1 of 11 points (max violation 0.00518); certified row violated at 0.

## Hand verification of the spot checks (added by hand after the run of 2026-10-03)

This section was written by hand. Rerunning the script regenerates everything above and drops it.
The checks use plain `fractions.Fraction` arithmetic on coefficients copied from the feature
strings, plus closed forms. They do not use SymPy, the snapshot code or the oracle's proof.

- **nvs02** (v3/partB, run 005_nvs02__full__s0__all, cut 8). At x0 = x1 = 0 and x4 = 200 the
  support objective reduces to a_x2*x2 + a_x4*200 + q*x2^2, where
  q = lambda_1*308859295109443/2^59 - lambda_2*5029735355997831/2^61 + lambda_3*5029735355997831/2^61 > 0.
  Its minimizer is x2* = -a_x2/(2q) = 18.750000000000004. The minimum value equals the certified
  value -0.008656571624818515 exactly. The sample minimum is at the vertex (0,0,0,200), with value
  a_x4*200 = -0.0010556794664412805 = U1. At the baseline incumbent (block point (0,7,9,200)) the
  exact support objective is -0.0066013. This lies below U1 by 0.0055456, which equals the
  reported row violation. The uncertified cut therefore removes this feasible point.
  SLSQP from (0,0,0,200) with the default `ftol` = 1e-6 stops after one iteration and reports
  success. With `ftol` = 1e-12 it reaches (0,0,18.75,200) in 9 iterations. So U2 fails here
  because SLSQP's stopping test is absolute while the support objective is of order 1e-2. All
  101 U2-materially invalid MINLPLib cuts (all in nvs02) show this one-iteration stop. In the
  path family, the U2 failures have another cause: only 1 of 74 stops after one iteration.
  In the path-family spot check below, SLSQP converges to a non-global local minimum.
- **prob06** (v3/partB, run 011_prob06__full__s0__auto, cut 0). The objective is
  a.u + k*(u0^2 + u1^2) with k = lambda_2*321685687669321/2^52 - lambda_1/16 > 0. Its minimizer
  -a/(2k) = (1.375, 2.125) lies inside the box [1, 5.5]^2, and its value equals the certified value
  exactly. The exact minimum over the 7x7 grid is -0.10470085470085472. The binary64 U1 is
  -0.10470085470085473, one unit in the last place lower.
- **interleaved_path_n40_s2** (v3d/partC-rowdir, run 027_..._all-diag-mech-wide, cut 13; copy
  i = 4 with A = (45/64, 3/8), C = (35/64, 13/64)). The recorded feature equals the quadratic part
  of D_4 from `mechanism.expand`: (p^2-1, 2, q^2-1, -2p, -2q) = (-3655/4096, 2, -903/1024, 21/32,
  11/16). The objective is concave in x and in z, so its minimum over [0,1]^3 has x, z in {0,1}.
  Enumerating these four cases with the exact minimizer in y gives -0.11321042438659897 at
  (1, 0.25, 0), equal to the certified value. The values at the U1 and U2 points reproduce U1
  and U2. SLSQP stopped at the local minimum (0, 0.414, 0).
