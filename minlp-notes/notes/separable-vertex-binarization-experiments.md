# Vertex binarization: experiment record

Date: 2026-09-21. Companion to
[the result note](../results/separable-vertex-binarization.md). All numbers
come from the JSON-lines files named below; tables are produced by
`code/vertex_binarization/tables.py`.

## Setup

Gurobi 13.0.3 (4 threads), SCIP 10.0 through PySCIPOpt 6.2.1 (1 thread),
BARON through GAMS 54.3.1 (1 thread). Relative gap `1e-4`. Times are wall
clock and include model construction. Several sweeps shared an 18-core
machine, so differences below a factor of about two are not meaningful.
Every cell is one run with one seed; no repetition or variance estimate
exists. `orig` is the direct model with `w_i == f_i(x_i)` and finite bounds on
`w_i`; `sob` is the reformulation.

## Tables

`code/vertex_binarization/results/jeroslow_w.jsonl` (time limit 120 s; cell = seconds, or `TL gap%` with the gap between the dual bound and the best known value; `!` marks a returned point worse than the best known by more than 1e-4)

| family | n | m | seed | baron orig | baron sob | gurobi orig | gurobi sob | scip orig | scip sob |
|---|---|---|---|---|---|---|---|---|---|
| jeroslow_w | 12 | 1 | 0 | 4.6 | 0.7 | 0.3 | 0.1 | 0.7 | 1.5 |
| jeroslow_w | 18 | 1 | 0 | TL 100.0% | 1.1 | 2.7 | 0.5 | 27.1 | 35.2 |
| jeroslow_w | 24 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.3 | TL 100.0% | 1.8 |
| jeroslow_w | 30 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.2 | TL 100.0% | 0.8 |
| jeroslow_w | 60 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.2 | TL 100.0% | 2.2 |
| jeroslow_w | 120 | 1 | 0 | TL 100.0% | TL 100.0%! | TL 100.0% | 0.3 | TL 100.0% | 1.1 |
| jeroslow_w | 400 | 1 | 0 | TL 100.0% | TL 100.0%! | TL 100.0% | 0.5 | TL 100.0% | TL 100.0% |

`code/vertex_binarization/results/jeroslow.jsonl` (time limit 120 s; cell = seconds, or `TL gap%` with the gap between the dual bound and the best known value; `!` marks a returned point worse than the best known by more than 1e-4)

| family | n | m | seed | baron orig | baron sob | gurobi orig | gurobi sob | scip orig | scip sob |
|---|---|---|---|---|---|---|---|---|---|
| jeroslow | 12 | 1 | 0 | 4.7 | 0.8 | 0.5 | 0.1 | 0.1 | 0.3 |
| jeroslow | 18 | 1 | 0 | TL 100.0% | 0.8 | 3.5 | 0.4 | 0.1 | 0.2 |
| jeroslow | 24 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.5 | 0.1 | 0.5 |
| jeroslow | 30 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.3 | 0.1 | 0.2 |
| jeroslow | 60 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.2 | 0.1 | 0.9 |
| jeroslow | 120 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 0.4 | 0.2 | 0.8 |
| jeroslow | 400 | 1 | 0 | TL 100.0% | TL 100.0% | TL 100.0% | 1.8 | 1.3 | 2.6 |

`code/vertex_binarization/results/pilot.jsonl` (time limit 60 s; cell = seconds, or `TL gap%` with the gap between the dual bound and the best known value; `!` marks a returned point worse than the best known by more than 1e-4)

| family | n | m | seed | baron orig | baron sob | gurobi orig | gurobi sob | scip orig | scip sob |
|---|---|---|---|---|---|---|---|---|---|
| cknap | 25 | 1 | 1 | 0.4 | 0.5 | 0.6 | 0.5 | 0.0 | 0.0 |
| cknap | 25 | 2 | 1 | 1.0 | 4.5 | 0.6 | 0.3 | 0.1 | 1.4 |
| cknap | 25 | 5 | 1 | 1.2 | TL 4.2%! | 0.1 | 3.0 | 0.3 | 56.9 |
| cknap | 50 | 1 | 1 | 0.5 | 1.7 | 0.1 | 0.1 | 0.1 | 0.2 |
| cknap | 50 | 2 | 1 | 0.8 | 10.6 | 0.1 | 0.4 | 0.1 | 3.5 |
| cknap | 50 | 5 | 1 | 3.0 | TL 1.4%! | 0.2 | 39.3 | 0.6 | TL 1.1%! |
| cknap | 100 | 1 | 1 | 1.6 | 4.0 | 0.3 | 0.4 | 0.3 | 2.1 |
| cknap | 100 | 2 | 1 | 1.3 | 14.9 | 0.3 | 1.0 | 0.3 | 9.6 |
| cknap | 100 | 5 | 1 | 28.2 | TL 0.6%! | 0.5 | TL 0.2% | 2.2 | TL 0.6%! |
| power | 25 | 1 | 1 | 0.3! | 3.0 | 0.1 | 0.0 | 0.1 | 0.1 |
| power | 25 | 2 | 1 | 0.3! | 1.8 | 0.0 | 0.1 | 0.1 | 2.9 |
| power | 25 | 5 | 1 | 0.3! | 5.8 | 0.1 | 0.1 | 0.1 | 1.0 |
| power | 50 | 1 | 1 | 0.4 | 1.3 | 0.1 | 0.0 | 0.1 | 0.1 |
| power | 50 | 2 | 1 | 0.6 | 4.7 | 0.1 | 0.2 | 0.2 | 15.0 |
| power | 50 | 5 | 1 | 0.9 | TL 3.7% | 0.1 | 1.8 | 0.3 | 21.7 |
| power | 100 | 1 | 1 | 1.0 | 3.2 | 0.1 | 0.3 | 0.3 | 0.6 |
| power | 100 | 2 | 1 | 2.3 | 25.1 | 0.2 | 2.4 | 0.6 | 26.4 |
| power | 100 | 5 | 1 | 2.4 | TL 1.2%! | 0.3 | TL 0.1% | 2.6 | TL 1.1% |
| sigmoid | 25 | 1 | 1 | TL 11.2% | TL 3.5% | 0.1 | 0.2 | TL 41.9% | TL 3.6% |
| sigmoid | 25 | 2 | 1 | TL 15.1% | TL 3.3% | 0.1 | 0.2 | TL 46.1%! | TL 7.1% |
| sigmoid | 25 | 5 | 1 | TL 14.6% | TL 3.3% | 0.1 | 0.1 | TL 44.6%! | TL 11.4% |
| sigmoid | 50 | 1 | 1 | TL 18.2% | TL 3.6% | 0.5 | 0.5 | TL 75.2%! | TL 7.1%! |
| sigmoid | 50 | 2 | 1 | TL 18.2% | TL 3.5% | 0.4 | 0.6 | TL 70.3%! | TL 7.8% |
| sigmoid | 50 | 5 | 1 | TL 18.9%! | TL 3.6% | 0.7 | 0.4 | TL 70.9%! | TL 11.1%! |
| sigmoid | 100 | 1 | 1 | TL 20.2%! | TL 3.8% | 0.1 | 0.2 | TL 71.5%! | TL 7.6%! |
| sigmoid | 100 | 2 | 1 | TL 19.9%! | TL 3.5% | 0.2 | 0.3 | TL 71.2%! | TL 8.0%! |
| sigmoid | 100 | 5 | 1 | TL 20.4%! | TL 3.7% | 1.2 | 1.0 | TL 69.5%! | TL 9.3%! |

`code/vertex_binarization/results/pilot_quartic.jsonl` (time limit 60 s; cell = seconds, or `TL gap%` with the gap between the dual bound and the best known value; `!` marks a returned point worse than the best known by more than 1e-4)

| family | n | m | seed | baron orig | baron sob | gurobi orig | gurobi sob | scip orig | scip sob |
|---|---|---|---|---|---|---|---|---|---|
| quartic | 10 | 1 | 1 | 51.6 | TL 117.7% | TL 30.3%! | TL 3.1% | 44.2 | TL 25.9% |
| quartic | 10 | 3 | 1 | 25.2 | TL 179.9% | 53.8 | 43.5! | 17.5 | TL 49.6% |
| quartic | 20 | 1 | 1 | TL 69.4%! | TL 138.1%! | TL 75.4%! | TL 15.8% | TL 60.9%! | TL 63.6%! |
| quartic | 20 | 3 | 1 | TL 65.9% | TL 140.7%! | TL 74.9%! | TL 6.5%! | TL 68.1%! | TL 63.7%! |
| quartic | 40 | 1 | 1 | TL 98.3%! | TL 134.9%! | TL 94.8%! | TL 19.1% | TL 93.3%! | TL 61.4%! |
| quartic | 40 | 3 | 1 | TL 101.1% | TL 142.9%! | TL 104.0%! | TL 7.3%! | TL 99.2%! | TL 65.9%! |


## What the data show

1. **Asymmetric lower-bound family (`jeroslow_w`).** On the original model
   Gurobi and SCIP reach the limit from `n = 24` and BARON from `n = 18`, all
   with dual bound `0`. On the reformulation Gurobi solves every size up to
   `n = 400` in at most 0.5 s. SCIP solves `n = 24..120` in 0.8–2.2 s and
   times out at `n = 400`. BARON solves `n <= 18` and times out from
   `n = 24`; at `n = 120` and `n = 400` it also returns a worse point.
2. **Symmetric family (`jeroslow`).** SCIP solves the *original* model at
   every size in at most 1.3 s. This is symmetry handling: with
   `misc/usesymmetry = 0` SCIP on `n = 30` reaches a 30 s limit with dual
   bound `0` after 117,721 nodes, against 11 nodes with the default. Gurobi
   and BARON behave as on the asymmetric family. SCIP's success on the
   symmetric reformulation at `n = 400` probably also relies on symmetry,
   since it fails on the asymmetric one.
3. **Random instances (`pilot.jsonl`).** The reformulation is slower in
   almost every `cknap` and `power` cell. With `m = 5` it reaches the 60 s
   limit for BARON from `n = 25` (`cknap`) or `n = 50` (`power`), for SCIP
   from `n = 50` or `n = 100`, and for Gurobi at `n = 100`. `power 50/5` is solved by SCIP in 21.7 s and by Gurobi in
   1.8 s, against 0.3 s and 0.1 s on the original.
4. **Sigmoid (`pilot.jsonl`).** Gurobi solves both forms in at most 1.2 s.
   Over all tested sizes (`n = 25, 50, 100`, `m = 1, 2, 5`), SCIP stops at
   42–75% gap on the original and 3.6–11.4% on the reformulation; BARON
   stops at 11–20% on the original and 3.3–3.8% on the reformulation. At
   `n = 25` alone the original gaps are 42–46% (SCIP) and 11–15% (BARON).
5. **Quartic (`pilot_quartic.jsonl`).** The reformulation lowers Gurobi's gap
   from 30–104% to 3–19% but no solver finishes `n >= 20` in either form, and
   SCIP and BARON get worse. The
   [univariate envelope handler](../results/composite-univariate-envelopes.md)
   is the right tool for this family.

## Solver errors observed

- **Gurobi 13.0.3.** Cell `quartic/10/3/1/sob/gurobi` reports `optimal` with
  value -8.336; the optimum is -9.250 (other solvers, and Gurobi itself when
  given that point as a start). The reviewer reproduced it with 2 and 4
  threads. The model is valid; this is a solver error.
- **BARON through GAMS.** On the original `power` models with `n = 25` BARON
  reports `optimal` at 0 nodes with values 11–38% above the optimum. The
  reviewer found that the value depends on the start point and that raising
  the lower bound of `x` from `0` to `1e-7` gives the correct value, with
  either `**` or `rpower`. Whether the fault is in BARON or in the GAMS link
  was not determined. These cells are marked `!` and are not counted as
  solved.

## Side checks

- `code/vertex_binarization/results/explicit_x.txt`
  (`side_checks/explicit_x_check.py`, symmetric family, `n = 60`, Gurobi,
  20 s): with the `x_i` substituted into the linking row Gurobi proves
  optimality in 0.1 s; with explicit `x_i` and defining equalities it stops
  at dual bound `0` after 614,397 nodes. Defining the objective terms through
  auxiliary variables does not matter.
- `code/vertex_binarization/results/boxqp.jsonl`
  (`side_checks/boxqp_binarize.py`, six `spar` box-QP instances from
  github.com/sburer/BoxQP_instances, Gurobi, 4 threads): declaring the
  variables with `Q_ii >= 0` binary changes the time of five instances by
  -16% to +27% in `bin` and -4% to +33% in `bin2` (the largest increase is
  `spar080-025-1`: 0.557 s originally, 0.708 s in `bin` and 0.742 s in
  `bin2`) and makes `spar060-020-1` about 28 times slower in `bin`, 2.11 s
  and 70,663 nodes against 0.076 s and 1 node. Pairwise second-order cuts
  (`bin2`) change nothing material. There is no evidence of a benefit.

## Review findings and their resolution

The [independent review](review-separable-vertex-binarization.md) is kept as
written. Resolutions:

1. SCIP and symmetry: the asymmetric family is now the main experiment; the
   symmetric one is reported with the symmetry explanation.
2. `jeroslow_w` added to the note, the README and the results.
3. Gurobi and BARON errors: reported above and in the result note.
4. Unsupported sentences: the box-QP and explicit-`x` checks now have code
   and data; the box-QP sentence was wrong for one instance and is corrected.
5. Numbers in the computational section were recomputed from the files.
6. Theorem 3 now states the bound tightening and the incumbent; the
   comparison with the lower bounds carries three qualifications.
7. Curvature tags: `sob/functions.py` no longer samples. It tags a piece
   concave only when ball arithmetic encloses the second derivative in the
   nonpositive reals. The reviewer's narrow-dip example is now split
   correctly. Constant and linear terms no longer break the Gurobi backend.
8. Remarks (b) and (c) of Theorem 1 were made precise.
9. Not done: tests with side variables `y`; a rank computation that is robust
   to nearly dependent columns (`numpy.linalg.matrix_rank` is used; an
   underestimate would make the budget too small and the model invalid).
