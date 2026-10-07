# Part U: what certification buys (offline ablation)

Generated 2026-10-03T21:54:55Z by `verification/ablation_uncertified.py` (campaign-v4-protocol.md, Amendment 1, Part U). No solver was run. Machine-readable data: `ablation-uncertified.json`.

## Inputs

| Part | Family | Record file SHA-256 (first 16) | Snapshot integration.py SHA-256 (first 16) | Cuts recorded | Cuts analyzed |
|---|---|---|---|---|---|
| v3/partA-full | minlplib | bfb16c124c1ac6f8 | 128fe10b13d22874 | 188 | 188 |
| v3/partA-root | minlplib | 3a03c854267c279f | 128fe10b13d22874 | 465 | 465 |
| v3/partB | minlplib | d9beda846bcd59b2 | 128fe10b13d22874 | 845 | 845 |
| v3d/partA-root-rowdir | minlplib | d93fac8024f8a8e0 | d8bdeba66604bf62 | 469 | 469 |
| v3d/partB-root-rowdir | minlplib | 49523c64329e1caf | d8bdeba66604bf62 | 529 | 529 |
| v4/partB2 | minlplib | 3e440d610a00cab9 | 35b5a4fd928e123b | 1007 | 1007 |
| v4/partD-root | minlplib | b8f4ded853d355f2 | 35b5a4fd928e123b | 1736 | 1736 |
| v4/partD-full | minlplib | 3370ea7945e18bc1 | 35b5a4fd928e123b | 28 | 28 |
| v3/partC | path | 517fe33e6af76e53 | 128fe10b13d22874 | 6000 | 47 |
| v3d/partC-rowdir | path | d526d2071aeffa5d | d8bdeba66604bf62 | 30000 | 235 |
| v4/partC2 | path | e7eeada9ef51948d | 35b5a4fd928e123b | 24000 | 170 |
| v4/partC3 | path | 194c9c7acc902a81 | 35b5a4fd928e123b | 30000 | 208 |
| v4/partC4 | path | 662adb1918f53da4 | 35b5a4fd928e123b | 48000 | 340 |

Path-family sample: `random.Random(0).sample(range(138000), 1000)` over the concatenated cut list of v3/partC, v3d/partC-rowdir, v4/partC2, v4/partC3, v4/partC4 (file order, then cut order within a record), processed in sorted order.

## Key counts

Counts are per recorded cut: a cut recorded in several runs (seeds, modes, parts) counts each time; 'distinct' identifies a cut by (model, block variables, binary64 direction).

- **MINLPLib parts, exact certificates** (5116 cuts, 1773 distinct, 47 models).
  U1: exceeds the certified minimum for 2964 cuts, materially for 1969 (765 distinct, 12 models). 405 materially invalid cuts (105 distinct) would remove a recorded feasible point, in 7 models: cvxnonsep_normcon20r, ex4_1_8, ex8_3_4, kall_ellipsoids_tc02b, nvs02, p_ball_10b_5p_2d_m, prob06.
  U2: exceeds the certified minimum for 1621 cuts, materially for 230 (63 distinct, 4 models). 132 materially invalid cuts (25 distinct) would remove a recorded feasible point, in 2 models: kall_ellipsoids_tc02b, nvs02.
  Of the 230 U2-materially invalid cuts, 166 had every SLSQP run stop after at most one iteration (all runs reported success).
- **Path-family sample, exact certificates** (1000 cuts, 995 distinct, 60 models).
  U1: exceeds the certified minimum for 983 cuts, materially for 976 (973 distinct, 60 models). 506 materially invalid cuts (505 distinct) would remove a recorded feasible point, in 58 models; 404 of them remove the known optimal witness.
  U2: exceeds the certified minimum for 793 cuts, materially for 73 (73 distinct, 37 models). 27 materially invalid cuts (27 distinct) would remove a recorded feasible point, in 19 models; 13 of them remove the known optimal witness.
  Of the 73 U2-materially invalid cuts, 1 had every SLSQP run stop after at most one iteration (all runs reported success).
- **MINLPLib parts, lower-bound certificates** (Bernstein, Arb; 151 cuts, 3 models): U1 exceeds the certified bound materially for 151, U2 for 151; not counted as invalid. The uncertified row removes a recorded feasible point for 7 cuts with U1 (ex4_1_8) and 0 with U2; such a removal shows directly that the uncertified constant exceeds the true minimum.

## Method as implemented

- Sample set: `solver.integration._sample(block, Config(**record['config']))` of the run's own snapshot (the routine behind the direction LP `propose_direction`): `np.linspace` grids with `grid_1d` = 33 points in 1D, `grid_2d` = 7 per axis in 2D and 3 per axis for d = 3, 4, filtered by the domain rows (tolerance 1e-12*max(1,|rhs|)), plus the exact vertices of box and domain rows (`theory.quadratic_polytope.polytope_vertices`) and their centroid for quadratic blocks within the face budget. Sample values come from `solver.integration._evaluate` (SymPy lambdify, NumPy binary64). Exchange samples (certified minimizers added later by the separator) are excluded.
- Block: features, symbols, box, domain rows and the binary64 direction (a, lambda) as recorded; the reconstruction is accepted only if the snapshot's `solver.certified._prepare` reproduces the model binding stored in the support witness. `quadratic` is recomputed as in `discover` (every side polynomial of total degree <= 2).
- U1 = min over the sample of `sample @ (a, lambda)` in binary64.
- U2 = min(U1, SLSQP values): `scipy.optimize.minimize(method='SLSQP')` from the 3 best samples (stable sort), bounds = block box, inequality constraints = domain rows (with their exact Jacobian), analytic objective gradient (SymPy), default tolerances, maxiter 200; the final point is clipped to the box and accepted if every domain row holds within 1e-09*max(1,|rhs|); its value is re-evaluated with `_evaluate` in binary64.
- Comparison in exact rational arithmetic with `support_witness.lower_bound`. Invalid: U > value; materially invalid: U - value > 1e-6*max(1,|value|). Exact certificates: quadratic_polytope, quadratic_polygon, quadratic_star; Bernstein and Arb are lower bounds and reported separately.
- Uncertified row: c^T v >= r + (U - beta), with c = `row_certificate.exact.coefficients`, r = `exact.eliminated_rhs` and beta = the recorded binary64 support constant (`binding.support.rhs`), i.e. exactly U - sum_r lambda_r b_r. Columns `x<i>` map to `original_values[i]` (the record's `column_names` are checked to be `v<i>` in the same order); the column `objective_epigraph` takes the incumbent's objective value (`primal_check.objective`, else `primal`; for a case witness `known_optimum_exact`).
- Incumbents: every record (any part, mode, seed) of the same model (same `model_sha256`) with `original_values` whose `primal_check.passed` is true, plus the case file's `known_witness_exact` when present. Removal: violation > 1e-6*max(1,||c||_1), exact.

Reconstruction: for 6267 of 6267 analyzed cuts the reconstructed block (features, symbols, box, domain rows, direction) gives exactly the model binding stored in the support witness (`_prepare` of the snapshot), the feature strings round-trip, and the recorded box is binary64-exact. Worker errors: 0; binding mismatches: 0.
For 6116 of 6116 exact-certificate cuts, the certified value (`support_witness.lower_bound`) equals the recorded exact minimum (`support_stats.exact_support`).

## Exact certificates: invalid uncertified constants

Counts of cuts whose uncertified constant exceeds the certified exact minimum (invalid) and exceeds it by more than 1e-6*max(1,|value|) (materially invalid). `=`: the constant equals the exact minimum; `<`: it lies below it (binary64 evaluation rounding at or near the minimizer, or an SLSQP point within the row tolerance); the last column gives the largest such deficit relative to max(1,|value|).

| Part | Method | Cuts | U1 invalid | U1 material | U1 = | U1 < | U1 max excess | U2 invalid | U2 material | U2 = | U2 < | U2 max excess | max rel. deficit U1 / U2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v3/partA-full | quadratic_polytope | 149 | 81 | 72 | 30 | 38 | 0.00347 | 18 | 0 | 30 | 101 | 2.08e-17 | 1.39e-17 / 6.34e-17 |
| v3/partA-root | quadratic_polytope | 409 | 313 | 280 | 66 | 30 | 0.00758 | 88 | 0 | 66 | 255 | 3.19e-09 | 1.11e-16 / 1.67e-16 |
| v3/partB | quadratic_polytope | 845 | 366 | 191 | 203 | 276 | 0.0167 | 239 | 65 | 210 | 396 | 0.0107 | 2.08e-16 / 1.05e-12 |
| v3d/partA-root-rowdir | quadratic_polytope | 413 | 313 | 280 | 66 | 34 | 0.00758 | 88 | 0 | 66 | 259 | 3.19e-09 | 1.11e-16 / 1.67e-16 |
| v3d/partB-root-rowdir | quadratic_polytope | 529 | 207 | 108 | 139 | 183 | 0.0167 | 140 | 36 | 142 | 247 | 0.0107 | 2.08e-16 / 1.05e-12 |
| v4/partB2 | quadratic_polytope | 1007 | 427 | 238 | 304 | 276 | 0.125 | 302 | 76 | 307 | 398 | 0.0938 | 1.39e-16 / 1.05e-12 |
| v4/partD-root | quadratic_polytope | 1736 | 1229 | 772 | 333 | 174 | 0.25 | 734 | 51 | 541 | 461 | 0.25 | 3.26e-16 / 3.26e-16 |
| v4/partD-full | quadratic_polytope | 28 | 28 | 28 | 0 | 0 | 0.25 | 12 | 2 | 12 | 4 | 0.25 | - / 9.57e-17 |
| v3/partC | quadratic_polytope | 47 | 47 | 47 | 0 | 0 | 0.033 | 37 | 6 | 1 | 9 | 0.03 | - / 8.52e-17 |
| v3d/partC-rowdir | quadratic_polytope | 235 | 234 | 234 | 1 | 0 | 0.0461 | 195 | 17 | 9 | 31 | 0.0178 | - / 2.22e-16 |
| v4/partC2 | quadratic_polytope | 170 | 167 | 166 | 2 | 1 | 0.0334 | 134 | 15 | 3 | 33 | 0.0253 | 1.99e-17 / 1.38e-16 |
| v4/partC3 | quadratic_polytope | 208 | 202 | 199 | 2 | 4 | 0.0646 | 161 | 15 | 12 | 35 | 0.0131 | 3.39e-17 / 4.55e-17 |
| v4/partC4 | quadratic_polytope | 340 | 333 | 330 | 4 | 3 | 0.033 | 266 | 20 | 12 | 62 | 0.0123 | 4.96e-17 / 1.2e-16 |
| **all minlplib** | exact | 5116 | 2964 | 1969 | | | | 1621 | 230 | | | | |
| **all path** | exact | 1000 | 983 | 976 | | | | 793 | 73 | | | | |

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
| v4/partB2 | U1 | 238 | 238 | 238 | 75 | 2 / 4 | 0 | 0 |
| v4/partB2 | U2 | 76 | 76 | 76 | 48 | 1 / 2 | 0 | 0 |
| v4/partD-root | U1 | 772 | 772 | 772 | 48 | 1 / 4 | 0 | 0 |
| v4/partD-root | U2 | 51 | 51 | 51 | 1 | 1 / 2 | 0 | 0 |
| v4/partD-full | U1 | 28 | 28 | 28 | 4 | 1 / 2 | 0 | 0 |
| v4/partD-full | U2 | 2 | 2 | 2 | 2 | 1 / 1 | 0 | 0 |
| v3/partC | U1 | 47 | 47 | 47 | 25 | 13 / 15 | 16 | 0 |
| v3/partC | U2 | 6 | 6 | 6 | 2 | 2 / 5 | 1 | 0 |
| v3d/partC-rowdir | U1 | 234 | 234 | 234 | 118 | 18 / 20 | 94 | 0 |
| v3d/partC-rowdir | U2 | 17 | 17 | 17 | 9 | 7 / 10 | 5 | 0 |
| v4/partC2 | U1 | 166 | 166 | 166 | 89 | 15 / 19 | 67 | 0 |
| v4/partC2 | U2 | 15 | 15 | 15 | 6 | 6 / 8 | 2 | 0 |
| v4/partC3 | U1 | 199 | 199 | 199 | 111 | 19 / 20 | 82 | 0 |
| v4/partC3 | U2 | 15 | 15 | 15 | 7 | 6 / 10 | 2 | 0 |
| v4/partC4 | U1 | 330 | 330 | 330 | 163 | 20 / 20 | 145 | 0 |
| v4/partC4 | U2 | 20 | 20 | 20 | 3 | 2 / 14 | 3 | 0 |

- minlplib, U1: 405 cuts would remove a recorded feasible point, in 7 models: cvxnonsep_normcon20r, ex4_1_8, ex8_3_4, kall_ellipsoids_tc02b, nvs02, p_ball_10b_5p_2d_m, prob06.
- minlplib, U2: 132 cuts would remove a recorded feasible point, in 2 models: kall_ellipsoids_tc02b, nvs02.
- path, U1: 506 cuts would remove a recorded feasible point, in 58 models.
- path, U2: 27 cuts would remove a recorded feasible point, in 19 models.

Incumbents available per model with a materially invalid cut:

- minlplib: 12 models; points per model min 0, median 17.0, max 19.
- path: 60 models; points per model min 10, median 10.0, max 18.

## Largest excesses (exact certificates)

**minlplib, U1** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 3 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 6/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 4 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 7/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 5 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 3/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 6 | 3 | 0 | 6 | -0.375 | -0.125 | 0.25 | 3/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 9 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 5/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 10 | 3 | 0 | 6 | -0.375 | -0.125 | 0.25 | 0/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 50 | 3 | 0 | 6 | -0.375 | -0.125 | 0.25 | 0/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 59 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 1/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 61 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 3/9 |
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all-diag | 100 | 3 | 0 | 6 | -0.375 | -0.125 | 0.25 | 0/9 |

**minlplib, U2** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| kall_ellipsoids_tc02b | v4/partD-root | 002_kall_ellipsoids_tc02b__root__s0__all | 7 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 3/9 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag | 158 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 0/0 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag-rowdir | 158 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 0/0 |
| kall_ellipsoids_tc02b | v4/partD-full | 002_kall_ellipsoids_tc02b__full__s0__auto | 7 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 3/9 |
| kall_ellipsoids_tc02b | v4/partD-full | 002_kall_ellipsoids_tc02b__full__s0__all | 7 | 3 | 0 | 6 | -0.25 | 0 | 0.25 | 3/9 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag | 67 | 3 | 0 | 6 | -0.25 | -0.0625 | 0.188 | 0/0 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag-rowdir | 67 | 3 | 0 | 6 | -0.25 | -0.0625 | 0.188 | 0/0 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag | 102 | 3 | 0 | 6 | -0.2569444444 | -0.09027777778 | 0.167 | 0/0 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag | 159 | 3 | 0 | 6 | -0.2569444444 | -0.09027777778 | 0.167 | 0/0 |
| kall_ellipsoids_tc05a | v4/partD-root | 001_kall_ellipsoids_tc05a__root__s0__all-diag-rowdir | 102 | 3 | 0 | 6 | -0.2569444444 | -0.09027777778 | 0.167 | 0/0 |

**path, U1** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| interleaved_path_n80_s8 | v4/partC3 | 023_interleaved_path_n80_s8__root__s0__rowdir-wide | 31 | 3 | 0 | 1 | -0.07629394531 | -0.01171875 | 0.0646 | 10/10 |
| interleaved_path_n80_s7 | v4/partC3 | 002_interleaved_path_n80_s7__full__s0__rowdir-wide | 202 | 3 | 0 | 1 | -0.5626220703 | -0.5087890625 | 0.0538 | 10/10 |
| interleaved_path_n80_s9 | v4/partC3 | 004_interleaved_path_n80_s9__full__s0__rowdir-wide | 180 | 3 | 0 | 1 | -0.1055908203 | -0.05786132812 | 0.0477 | 10/10 |
| interleaved_path_n80_s4 | v3d/partC-rowdir | 024_interleaved_path_n80_s4__root__s0__all-diag-mech | 47 | 3 | 0 | 1 | -0.125 | -0.07885742188 | 0.0461 | 18/18 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 000_interleaved_path_n80_s0__full__s0__all-diag-mech-wide | 0 | 3 | 0 | 1 | -0.03796386719 | 0 | 0.038 | 18/18 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 000_interleaved_path_n80_s0__full__s0__all-diag-mech | 149 | 3 | 0 | 1 | -0.03384452671 | 0 | 0.0338 | 0/18 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 020_interleaved_path_n80_s0__root__s0__all-diag-mech | 148 | 3 | 0 | 1 | -0.07615018509 | -0.04230565838 | 0.0338 | 0/18 |
| interleaved_path_n40_s3 | v4/partC2 | 008_interleaved_path_n40_s3__full__s0__frozen-wide | 547 | 3 | 0 | 1 | -1.317576391 | -1.284147297 | 0.0334 | 0/18 |
| interleaved_path_n80_s8 | v4/partC3 | 003_interleaved_path_n80_s8__full__s0__rowdir-wide | 34 | 3 | 0 | 1 | -0.0957398374 | -0.06243902439 | 0.0333 | 1/10 |
| interleaved_path_n80_s7 | v4/partC3 | 022_interleaved_path_n80_s7__root__s0__rowdir-wide | 274 | 3 | 0 | 1 | -0.0330471826 | 0 | 0.033 | 0/10 |

**path, U2** (top 10)

| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |
|---|---|---|---|---|---|---|---|---|---|---|
| interleaved_path_n40_s2 | v3/partC | 007_interleaved_path_n40_s2__full__s0__all-diag-mech | 118 | 3 | 0 | 1 | -0.1372654155 | -0.1072383339 | 0.03 | 0/18 |
| interleaved_path_n80_s1 | v4/partC2 | 001_interleaved_path_n80_s1__full__s0__frozen-wide | 3 | 3 | 0 | 1 | -0.1013283514 | -0.07602792863 | 0.0253 | 3/18 |
| interleaved_path_n40_s2 | v4/partC2 | 007_interleaved_path_n40_s2__full__s0__frozen-wide | 17 | 3 | 0 | 1 | -0.08347826087 | -0.06288819876 | 0.0206 | 0/18 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 020_interleaved_path_n80_s0__root__s0__all-diag-mech | 148 | 3 | 0 | 1 | -0.07615018509 | -0.05830248546 | 0.0178 | 0/18 |
| interleaved_path_n80_s2 | v3d/partC-rowdir | 022_interleaved_path_n80_s2__root__s0__all-diag-mech-wide | 222 | 3 | 0 | 1 | -0.1683901364 | -0.150553669 | 0.0178 | 1/18 |
| interleaved_path_n10_s8 | v4/partC3 | 038_interleaved_path_n10_s8__root__s0__all-diag-mech | 34 | 3 | 0 | 1 | -0.01624276001 | -0.003147821707 | 0.0131 | 1/10 |
| interleaved_path_coupled_n80_s9 | v4/partC4 | 024_interleaved_path_coupled_n80_s9__root__s0__frozen-wide | 169 | 3 | 0 | 1 | -0.1067259589 | -0.09440429868 | 0.0123 | 9/10 |
| interleaved_path_coupled_n80_s9 | v4/partC4 | 024_interleaved_path_coupled_n80_s9__root__s0__frozen-wide | 657 | 3 | 0 | 1 | -0.01236298751 | -0.001147081315 | 0.0112 | 0/10 |
| interleaved_path_n80_s0 | v3d/partC-rowdir | 020_interleaved_path_n80_s0__root__s0__all-diag-mech | 135 | 3 | 0 | 1 | -0.095703125 | -0.08532714844 | 0.0104 | 18/18 |
| interleaved_path_n40_s3 | v3d/partC-rowdir | 028_interleaved_path_n40_s3__root__s0__all-diag-mech-wide | 281 | 3 | 0 | 1 | -0.1014755371 | -0.0911208905 | 0.0104 | 4/18 |

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
| v4/partB2 | 1007 | 121 | 79 | 1007 | 6.94e-17 | 1.12e-18 | 6.94e-17 | 1.12e-18 | 1.49e-16 |
| v4/partD-root | 1736 | 209 | 131 | 1736 | 8.48e-16 | 2.12e-17 | 8.48e-16 | 2.12e-17 | 1.11e-16 |
| v4/partD-full | 28 | 6 | 6 | 28 | 3.21e-17 | 2e-17 | 3.21e-17 | 2e-17 | 2.51e-17 |
| v3/partC | 6000 | 5820 | 4632 | 6000 | 1.69e-16 | 2.49e-18 | 1.29e-16 | 2.44e-18 | 2.09e-16 |
| v3d/partC-rowdir | 30000 | 26714 | 20970 | 30000 | 1.69e-16 | 1.76e-18 | 1.29e-16 | 1.73e-18 | 2.09e-16 |
| v4/partC2 | 24000 | 23020 | 18294 | 24000 | 2.12e-16 | 1.92e-18 | 1.31e-16 | 1.9e-18 | 2.09e-16 |
| v4/partC3 | 30000 | 27312 | 20966 | 30000 | 2.08e-16 | 1.73e-18 | 1.52e-16 | 1.73e-18 | 2.08e-16 |
| v4/partC4 | 48000 | 44812 | 35000 | 48000 | 2.08e-16 | 1.97e-18 | 1.52e-16 | 1.95e-18 | 2.09e-16 |

## Spot checks

### kall_ellipsoids_tc02b (v4/partD-root, run 002_kall_ellipsoids_tc02b__root__s0__all, cut 7, quadratic_polytope)

- Block variables ['x40', 'x43', 'x46'], box [['-1', '1'], ['-1', '1'], ['-1', '1']].
- Features g: ['-x40**2', 'x40**2', '-x40*x43', 'x40*x43', '-x40*x46', 'x40*x46'].
- Signed sides: ['row71:upper', 'row71:lower', 'row74:upper', 'row74:lower', 'row77:upper', 'row77:lower'].
- Domain rows (a, rhs; a.u <= rhs): none.
- Direction a = [-0.5, -0.0, -0.0], lambda = [0.0, 1.0, 0.5, 0.0, 0.0, -0.0].
- U1 (sample minimum over 36 samples) = 0.0 at u = [0.0, -1.0, -1.0].
- U2 (best of U1 and 3 SLSQP runs) = 0.0 at u = [0.0, -1.0, -1.0]; SLSQP statuses [0, 0, 0], accepted [True, True, True].
- Certified minimum = -1/4 = -0.25, minimizer ['1/2', '1', '-1'] = [0.5, 1.0, -1.0].
- Exact objective at the certified minimizer = -1/4; minimizer exactly feasible: True.
- Excess U1 = 0.25, U2 = 0.25 (material tolerance 1e-06).
- U1 row: violated beyond 2e-06 at 3 of 9 points (max violation 0.203); certified row violated at 0.
- U2 row: violated beyond 2e-06 at 3 of 9 points (max violation 0.203); certified row violated at 0.

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
- U1 row: violated beyond 1e-06 at 19 of 19 points (max violation 0.00555); certified row violated at 0.
- U2 row: violated beyond 1e-06 at 19 of 19 points (max violation 0.00555); certified row violated at 0.

### interleaved_path_n40_s2 (v3/partC, run 007_interleaved_path_n40_s2__full__s0__all-diag-mech, cut 118, quadratic_polytope)

- Block variables ['x56', 'x57', 'x58'], box [['0', '1'], ['0', '1'], ['0', '1']].
- Features g: ['-207*x56**2/256 + 7*x56*x57/8 + 2*x57**2 + 15*x57*x58/16 - 799*x58**2/1024'].
- Signed sides: ['row15:upper'].
- Domain rows (a, rhs; a.u <= rhs): none.
- Direction a = [0.09055704498063748, -0.45755138516532623, 0.1904081024724456], lambda = [0.2440274054215073].
- U1 (sample minimum over 36 samples) = -0.10676198987190949 at u = [1.0, 0.0, 1.0].
- U2 (best of U1 and 3 SLSQP runs) = -0.10723833386944251 at u = [0.0, 0.4694965743223116, 0.0]; SLSQP statuses [0, 0, 0], accepted [True, True, True].
- Certified minimum = -5565564551635788411767249108925527/40546007378127908451210891421024256 = -0.13726541554959787, minimizer ['1', '35168055427983661/140672221711934624', '0'] = [1.0, 0.25000000000000006, 0.0].
- Exact objective at the certified minimizer = -5565564551635788411767249108925527/40546007378127908451210891421024256; minimizer exactly feasible: True.
- Excess U1 = 0.0305034, U2 = 0.0300271 (material tolerance 1e-06).
- U1 row: violated beyond 1e-06 at 10 of 18 points (max violation 0.00022); certified row violated at 0.
- U2 row: violated beyond 1e-06 at 0 of 18 points (max violation -0.000256); certified row violated at 0.

