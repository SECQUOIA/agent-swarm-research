# Review of the row-hull code and experiments

**Historical review, superseded where indicated.** The failures and original
counts below describe the code before the pricing correction. The correction,
regression test, and affected reruns are recorded in
[the experiment record](row-hull-experiments.md#review-findings-and-their-resolution).
Current Gurobi solved counts are 96 to 124 overall and 72 to 77 on unequal-width
instances. The later ten-agent audit is recorded in
[the corrective audit](review-minlp-developments-20260922.md). The original
findings are retained to explain the defect and its detection.

Date: 2026-09-21. Independent review of `code/row_hull/`, of
[row-hull-experiments.md](row-hull-experiments.md), and of the Summary and
Computational results of
[results/row-hull-separable-concave.md](../results/row-hull-separable-concave.md).
The theory was reviewed separately. No existing file was changed. Review
scripts and their outputs are in `code/row_hull/review_code/`.

All commands below were run from `code/row_hull` with
`RUN="nice uv run --project ../minlp_solver_lab python"`, at most 4 threads,
no run longer than 10 minutes. These are targeted checks, not CI.

## Verdict

| Item | Verdict |
| --- | --- |
| 1. Soundness of cuts | **Fails.** `pricing._compress` can discard the most profitable of several subsets with (numerically) the same sum. The "valid lower bound" is then not a lower bound and the cut is invalid. This happens on the experiment instances with two-decimal capacities, and in two checked cells the cuts given to Gurobi cut off the optimal solution. A small fix (eight lines) removes every failure found. Everything else I tested is sound. |
| 2. Experiment integrity | Tables and almost all quoted numbers reproduce exactly from the JSONL files. Five small discrepancies (below). Time accounting and model forms are fair. Code hashes match. The consistency check is too coarse to detect the bug of item 1. |
| 3. Fairness and overclaims | The headline solved counts are driven by the `uniform` families, which are built so that Theorem 2 applies exactly. On the 80 unequal-width Gurobi instances the cuts give no mean time gain (10.8 s against 10.9 s) and 72 against 76 solved. "Valid cuts always" is not true of the code as run. |
| 4. Reproducibility | The pytest command and `run_one.py` cells of all three forms run. The README omits the commands for several results quoted in the record, and one README statement about timing is wrong. |

## 1. Soundness of cuts

### 1.1 Bug: duplicate-sum elimination keeps the wrong state (invalid cuts)

File `code/row_hull/rowhull/pricing.py`, `_compress`, lines 35–41 of the file
(the `np.lexsort((-P, lo))` and the `keep[1:] = ...` lines).

The states are sorted by exact `lo`, then by decreasing profit. Then a state is
dropped when its `lo` and `hi` differ from the previous state by at most
`1e-11 * scale`. The intent is "identical sums: keep the most profitable". That
holds only when the sums are bit-identical. Two different subsets whose widths
have the same sum in exact arithmetic (`2.37 + 5.12` and `3.49 + 4.00`)
usually differ by one unit in the last place as floats. The sort then orders
them by that rounding error, not by profit, and the state with the smaller
float survives whatever its profit. If the discarded subset is the minimizer of
`omega_j gamma_j(r) - pi.v`, then

- `lower` returned by `price` is larger than the true minimum, so the constant
  `pi0 = lower - 1e-9...` in `separate.py` line 93 is too large and the cut
  cuts off a row vertex;
- the column of that vertex is never generated, so column generation also
  stops early.

The same comparison is chained (`i` against `i-1` even when `i-1` was
dropped), which has the same effect. Interval merging itself (`len(lo) > kmax`)
is correct: it takes the maximum profit and the outer interval. With `kmax=30`
the failures disappear, because merging repairs the choice.

Data with few decimals trigger the bug: `cap='random'` capacities are rounded
to two decimals, in `transport`, `netflow` and `transport_fc`. Integer widths
and generic real widths do not trigger it, which is why `test_rowhull.py`
(136 passed) does not see it: its rows use `rng.uniform` widths or integers.

Evidence (all reproducible):

- `review_code/check_pricing.py`: `price` against brute force over all row
  vertices, 10 items, random duals. `lower` exceeds the true minimum on 6 of
  300 rows with two-decimal widths (worst excess 0.66) and on 49 of 300 with
  one-decimal widths (worst 1.63); 0 of 300 for integer and for continuous
  widths.
- `review_code/check_row_cuts.py`: `RowSeparator` + `cut_to_model` +
  `clean_cut`, each cut evaluated in model variables at every vertex of the row
  polytope with the true functions (mixed signs, shifted bounds, `==`, `<=`,
  `>=`, fixed charge in both orientations). One-decimal widths: 34 of 382 cuts
  invalid, worst scaled violation 0.26. Two-decimal widths, up to 11 items: 70
  of 734 invalid, worst 0.34.
- `review_code/check_experiment_cuts.py`, on the instances of the final study
  (output in `review_code/experiment_cuts.jsonl`). For every separated cut the
  true minimum over the row vertices is recomputed with the corrected pricing.
  For a violated row vertex, a point feasible for the whole problem that
  extends it is found by a linear program, `w = f(x)` is set exactly, and the
  cut is evaluated there. Over 38 instances: 91 of 9,955 generated cuts are
  invalid on 21 instances; 72 are confirmed at a feasible point of the whole
  problem; on 12 instances such a cut survives the "binding" filter and was
  therefore handed to the solver. Examples:
  `transport-random-quad-8x12-s0` 4 invalid cuts, scaled violation 0.32, 3 kept;
  `transport-random-quad-10x15-s3` 14 invalid, 6 kept;
  `netflow-random-log-40n3d-s2` 4 invalid (0.58), 4 kept;
  `transportfc-random-quad-8x12-s0` 4 invalid, none kept.
  `transport-uncap-quad-8x12` (5 seeds): none.
- `review_code/check_optimum_cut_off.py`: the optimal solution of the original
  model (Gurobi, gap `1e-6`) is inserted into the kept cuts of `cut_loop`.
  **`transport-random-quad-10x15-s3`: 5 of 207 cuts are violated by the
  optimum, scaled violation `2.7e-3`. `netflow-random-quad-40n3d-s3`: 1 of 114,
  `1.1e-4`.** Four other cells: none. This agrees with the recorded runs: the
  `cuts` form reports 113.06245 and 173.65010, the `orig` form 113.06125 and
  173.64956. The differences are `1e-5` relative, inside the `1e-4` gap
  tolerance, so the consistency check of `summarize.py` (tolerance `2e-4`)
  cannot see them. The statement "Consistency of all final runs: 0 violations
  attributable to cuts" is true as computed but does not establish validity.

Fix (checked: `review_code/patched_pricing.py`, installed by `--patch` in the
scripts). Group states whose `(lo, hi)` agree within the tolerance and keep,
per group, the maximum profit, the mask of that maximum, the smallest `lo` and
the largest `hi`:

```python
order = np.lexsort((hi, lo))
lo, hi, P, mask = lo[order], hi[order], P[order], mask[order]
new = np.ones(len(lo), bool)
new[1:] = (lo[1:] - lo[:-1] > 1e-11 * scale) | (np.abs(hi[1:] - hi[:-1]) > 1e-11 * scale)
starts = np.flatnonzero(new); grp = np.cumsum(new) - 1
best = np.maximum.reduceat(P, starts)
idx = np.flatnonzero(P >= best[grp]); first = np.unique(grp[idx], return_index=True)[1]
lo, hi, P, mask = np.minimum.reduceat(lo, starts), np.maximum.reduceat(hi, starts), best, mask[idx[first]]
```

With this change: `check_pricing_patched.py` 0 failures in 1,500 rows
(including forced merging with `kmax=30`); `check_row_cuts.py --patch` 0
invalid of 1,212 cuts. A regression test should use widths with one or two
decimals and compare `price` with brute force.

Effect on the reported results. The root bounds with and without the fix agree
to `5e-5` relative or better (largest change: 111.2665 to 111.2618 on
`transport-random-quad-10x15-s3`). Five `cuts` cells rerun with the fix
(`review_code/patched_reruns.jsonl`, Gurobi, 4 threads) all solve, with the
optimum of `orig` to seven digits and node counts equal or lower than recorded
(for example 2,471 against 3,158; 18,644 against 29,428). I therefore expect
the tables to survive qualitatively, but the `random` and `netflow-random` and
`transportfc-random` cells of all three solvers, the `L` mode of `bb.py` on the
`random` instances, and the `scip_sepa.py` numbers on
`transport-random-quad-8x12-s0` were produced with cuts that are not all valid
and should be rerun after the fix. The `uniform` cells use only the closed
form and are not affected. `residual_bounds` uses the same routine with zero
profits; there the defect only shifts an endpoint by at most `1e-11 * scale`,
which is harmless.

A cheap additional safeguard in `RowSeparator.separate`: at convergence the
true minimum reduced cost is about zero, so `lower` should not exceed the
shifted `pi0` by more than the LP tolerance. Returning `None` when
`lower > pi0 + 1e-6 * max(1, |pi0|)` would have caught this bug.

### 1.2 Items checked and found sound

Reading and tests (`check_row_cuts.py --patch`, and
`review_code/check_problem_cuts.py` on 108 small instances: transport 3x4 and
4x5 with every capacity and cost type including `pow`, `netflow` g8n2d,
`transport_fc` f3x4, and my own problems with coefficients `-1, 1, 2, -0.5`,
shifted bounds and `==`, `<=`, `>=` rows). The problem-level script samples
150 vertices of the feasible polytope and 150 convex combinations, sets
`w_i = f_i(x_i)` exactly and `y_i = 1[x_i > 0]` (and also `y = 1` with `x = 0`),
checks every cut of `cut_loop` with and without the closed form (3,340 cuts),
checks that the extended rows of `cut_loop` and of `closed_form_ir` are
satisfiable by a linear program in the `zeta` variables, and compares the root
bound with the best sampled vertex value and with the Gurobi optimum of the
original model. Result: 0 invalid cuts, 0 unsatisfiable extended systems, 0
bounds above the optimum. (Rows of 4–5 items are too short to trigger 1.1.)

- Pruning `lo + w <= B + tol`: correct; the true sum is at least `lo`.
- Bucket merging and the endpoint argument: correct for `omega >= 0`, which
  `separate.py` line 82 enforces. Clipping the `r`-interval to `[0, width]`
  only enlarges the set over which the minimum is taken.
- Leave-one-out divide and conquer: correct.
- `uint64` masks: `assert n <= 63` in `price`; `cut_loop` skips longer unequal
  rows silently (stated in Limitations). `residual_bounds` does not assert, but
  it never reads the masks, so long rows are safe there.
- Dual shift in `separate.py` lines 78–79: consistent (`pi0 + shift*B`); the
  final constant does not depend on it.
- Big-M artificials: a cut is returned only when they are zero; validity does
  not depend on them because the constant comes from pricing.
- `cut_to_model`: signs for `a < 0`, the slack substitution for `<=` and `>=`
  rows (`row.B` is `total` for `>=`), chord constants and `tvar` dictionaries
  are correct; confirmed numerically in both orientations.
- `clean_cut`: the dropped term is bounded by `max(c*lb, c*ub)`, correct for a
  `>=` cut. If a `w` bound were infinite the right-hand side would become
  `-inf`; `_range` always returns finite bounds, so this does not occur.
- Fixed-charge gap with the `1e-9 * u` jump: for `0 < v <= 1e-9 u` the code
  uses `g(v)` instead of `c + g(v)`. This understates the gap, which can only
  weaken a cut. The function is not concave on `[0, 1e-9 u]`, but its minimum
  over any clipped interval is still at an endpoint. No invalid cut in either
  orientation.
- `residual_bounds`, `closed_form_rows`, `equal_width_inequality_rows`,
  `floor(B/w + 1e-9)`: the rounding cases fall into the degenerate branch and
  return `None`. The thresholds `1e-7` allow residuals as small as `1e-7 w`,
  which gives rows `r * zeta <= z` with a coefficient ratio of `1e7`. These are
  valid but badly scaled; a threshold near `1e-4 w` would be safer. The data of
  the study (four decimals) never come close.
- `_row_point` clipping affects only the point being separated.
- Validity of every cut relies on `is_concave(f)`, which trusts the `Piece`
  annotation. `instances._concave` sets it "by construction (no certification
  run)". The cost families used are concave, so this is fine here, but a
  non-concave function declared concave would give invalid cuts without any
  warning.

## 2. Experiment integrity

`review_code/recompute_tables.py` recomputes everything from
`results/main_gurobi.jsonl`, `main_fc_gurobi.jsonl`, `main_others.jsonl`;
`review_code/compare_optima.py` compares optimal values between the forms.

Reproduced exactly: all three family tables; Gurobi 96 / 123 of 130, 28 only
with cuts, 1 only without (`transport-random-sqrt-8x12-s2`, status 13);
shifted geometric means 22.3 / 10.4 s; 95 solved by both, cuts faster on 43;
`transport-random-quad-10x15` 2.5 times fewer nodes and 1.5 times more time;
fixed charge 37 / 40 and 12.9 / 6.8 s; SCIP 18 / 42 of 45 and 102 / 27 s;
BARON 15 / 44 of 50; status-13 gaps `3.65e-4` and `1.58e-4`; the BARON record
(72.9288 at 0 nodes after 0.8 s against 66.864); five SCIP `orig` cells and one
`cuts` cell without a result (I reproduced "SCIP: error in LP solver!" on
`transport-random-log-8x12-s1` after 25 s); closure ranges 64.3–88.2
(transport), 65.8–80.6 (netflow), 74.8–92.4 (fixed charge); the table in
`results/bb_nodes_5x7.txt` is identical to the one in the note; the
objective-form control numbers; the root-bound control within 0.1 percentage
points.

Discrepancies:

1. "On the 53 instances that `orig` solves in under 10 s the cuts are slower on
   47." `orig` solves 54 instances in under 10 s; the cuts are slower or fail on
   48. The quoted 53 / 47 is the subset also solved with cuts (the excluded
   instance is the status-13 run). The Summary of the results file repeats
   "47 of the 53". Fix: say "54 ... 48" or add "and that are also solved with
   cuts".
2. "BARON ... mean time 130 s against 61 s." 130.2 s is obtained when the wrong
   "optimal" run is counted at its own 0.8 s. The family table counts that run
   as unsolved at 300 s; on that convention the mean is 144.3 s (142.2 s if the
   instance is dropped). The error favours `orig`, so the conclusion is
   unaffected, but the number is inconsistent with the table.
3. "Exact separation on node boxes reduces nodes by a further factor of 7 to
   30" (results file: "7–30 times fewer nodes"). The ratios `R/L` in
   `bb_nodes_5x7.txt` are 9.1, 29.2, 10.4, 8.9, 20.6, 13.9, 7.4, 5.2, 8.6: the
   range is 5 to 29. The `bb_cf.py` counts 564, 243, 586 are not stored in any
   results file.
4. "the Python cut loop costs 2–6 s for unequal widths": the recorded range is
   1.3–13.5 s (median 3.6 s; 8–9 s means for `sqrt` at 10x15).
5. README and note: "`total_time` includes instance construction". In
   `run_one.py` the clock starts after the instance is built (line 25). It is
   the same for both forms and negligible, but the sentence is wrong.

Fairness of the accounting:

- `cuts` receives `tl - elapsed` for the solve (`run_one.py` line 35), so the
  300 s limit covers the cut loop; no run exceeds 301 s for Gurobi, 312 s for
  BARON. `orig` includes IR and model construction. Fair.
- Both forms are the same IR (`cut_ir` extends `original_ir`), same `w` bounds,
  same parameters, same thread counts (Gurobi 4, SCIP and BARON 1).
- The two forms of an instance are adjacent in the sweep order, so they ran
  under similar load. Load was high: eight 4-thread Gurobi cells on 36 logical
  cores, and `bb_nodes_5x7.txt` was written at 13:20 while the Gurobi sweep
  (13:08–13:49) was running. Times are noisy, as the note says. No instance
  solved only with cuts was a near miss for `orig`: the smallest final gap of
  `orig` on those 28 instances is `5e-3`, the median `4.8e-2`.
- `results/code_version.sha256` matches the current `rowhull/*.py`,
  `instances.py`, `run_one.py`, `sweep.py`; file times are before the hash file
  (13:07). Not hashed: `sob/backends.py` and `sob/model.py` (solver settings
  live there; both are committed and unmodified in git), `summarize.py`,
  `bb.py`, `bb_cf.py`, `scip_sepa.py` (modified 14:08), `root_bounds.py`,
  `run_objform.py`. `run_queue.sh` rewrites the hash file on every run, so the
  file records the last start, not a freeze.
- `sweep.py` discards stderr; a failed cell is stored as
  `IndexError('list index out of range')`. The note's "error in LP solver"
  cannot be read from the results files (I confirmed one cell by hand).
- "Root gap closed" uses the best primal value over the runs in the same file.
  For 6 Gurobi instances (and 3 SCIP, 6 BARON within `main_others.jsonl`)
  this value is not proven optimal. An unproven upper bound makes the
  denominator larger, so the closure is understated, never overstated. The
  definition is appropriate. It uses linear-programming bounds of the cut
  loop, not solver root bounds, and the note says so; the new root-bound
  control shows the relevant comparison for fixed charges (Gurobi's own root
  closes most of the term-wise gap; the row-hull rows halve the rest).

## 3. Fairness and overclaims

- **Instance design.** `uniform` has unit capacities and supplies in
  `[1.2, 3.8]` rounded to four decimals: equal widths and a fractional residual
  on every row, exactly the hypothesis of Theorem 2. 23 of the 28 instances
  solved only with cuts are `uniform`. Split of the Gurobi study:
  `uniform` (50 instances) 24 against 47 solved, 68.5 s against 9.6 s;
  `random` and `uncap` and `netflow-random` (80 instances) 72 against 76
  solved, 10.8 s against 10.9 s. The note describes both regimes in words; the
  Summary's "from 96 to 123 of 130" should be accompanied by this split, and
  should say that with integral supplies and unit capacities the residual is
  zero and the method adds nothing.
- **Epigraph form.** The control has finished (30 `quad` cells). Objective
  form / `orig` / `cuts`: 28 / 27 / 30 solved, 6.2 / 7.1 / 6.2 s. The epigraph
  form costs Gurobi at most about 40% on a family and does not explain the
  gains on `uniform`. On `random` and `uncap` with `quad` costs the direct
  objective form is the fastest of the three. The control covers only `quad`
  and only Gurobi; `log` and `sqrt` have no alternative statement.
- **Statistics.** Five seeds per family, one run per cell, no dispersion
  reported, noisy machine. Family means of 5 runs with a 300 s cap support
  "large effect on `uniform`" and "no clear effect or a loss on easy unequal
  instances", not the individual ratios. Single-instance closure ranges are
  wider than the family means quoted (55–90% transport, 56–86% netflow,
  62–96% fixed charge).
- **"Valid cuts always"** (Summary, general widths) and "the cut is valid
  whatever the LP accuracy" (`separate.py` docstring) and "pricing lower bounds
  with and without interval merging" (Checks) are claims about the algorithm.
  The implementation violated them on the study's own data (1.1). After the
  fix the wording is supported by my tests up to floating-point tolerances; it
  should still say "up to floating point", as the `pricing.py` docstring does.
- **"0 violations attributable to cuts"** should be weakened: the check has a
  tolerance twice the gap limit and cannot detect a cut that removes the
  optimum but leaves a solution within `1e-4`.
- **SCIP and BARON.** BARON solved nothing on the four `netflow` families
  without cuts and returned one wrong optimum; `sqrt` was dropped for both
  solvers because of solver failures. The counts are correct, but they say as
  much about these solvers on this epigraph form as about the cuts.
- What the evidence supports: the closed form is exact and cheap on
  equal-width rows and turns unsolved `uniform` instances into easy ones for
  all three solvers; separated cuts close 64–82% of the term-wise LP gap on
  unequal widths and reduce nodes on most families (not on `netflow-*-quad`),
  which as static dense root cuts does not pay in time on instances that take
  seconds. What it does not
  support: a general speed-up claim, any claim about non-synthetic models, or
  (before the fix) exactness of the reported optima on the `random` families.

## 4. Reproducibility

- `uv run --project ../minlp_solver_lab python -m pytest -q test_rowhull.py`:
  136 passed in 1.7 s.
- `run_one.py 4 5 0 random quad {orig,cuts,cf} gurobi`, `f3 4 0 random quad
  cuts gurobi`, `g8 2 0 random log cuts scip`: all run and agree on the optimum.
  `gams` and `baron` are on the path (BARON cell not rerun).
- The README lists commands for the main sweeps, `run_queue.sh`, `table.py`,
  `lll_closure.py`, `check_lll_subfamily.py`. Missing: `summarize.py` (it, not
  `table.py`, produces the tables in the note), `bb.py` and `bb_cf.py`
  (`bb_nodes_5x7.txt` and the mode `C` counts), `run_objform.py`,
  `root_bounds.py`, `scip_sepa.py`, `proto_aggregate.py`, the `cknap`
  experiment of finding 4 (no script in `code/row_hull` mentions `cknap`), and
  the numbers of finding 3. These files are also missing from the Layout list.
- `--workers 8` with 4 threads each assumes a 32-thread machine.

## Files written by this review

- `code/row_hull/review_code/check_pricing.py`, `check_pricing_patched.py`,
  `patched_pricing.py` (proposed fix), `check_row_cuts.py`,
  `check_problem_cuts.py`, `check_experiment_cuts.py`,
  `check_optimum_cut_off.py`, `run_one_patched.py`, `recompute_tables.py`,
  `compare_optima.py`.
- Outputs: `problem_check_unpatched.jsonl`, `experiment_cuts.jsonl`,
  `optimum_cut_off.jsonl`, `patched_reruns.jsonl` in the same directory.
