# Convex hulls of univariate curves for variables with several nonlinear terms

Date: 2026-09-23. Author: experiment agent; saved by the coordinator from the
agent's output (the agent's harness blocked Markdown writes). Status: independently
reviewed ([review](review.txt)); see "Corrections after independent review". Code and raw results: `code/`. Prior work in the
repository: `../../results/shared-variable-term-links.md` (pairwise links and
the `(x, x^2, x^3)` moment hull on `waterno2_06/09/12/18`). The hull theory
of vectors of univariate functions is known (Ballerstein, ETH thesis 2013);
this study contributes a general certified separator and a benchmark run.

## Summary

- **Separator.** `code/curvehull.py` separates a point from the convex hull of
  the curve `(t, f_1(t), ..., f_k(t))`, `t in [l, u]`, for any univariate `f_j`
  given as a sympy expression. The direction comes from a semi-infinite LP
  solved by cutting planes on `t`; the constant is certified by outward-rounded
  interval arithmetic on `f_j` and `f_j''`, assuming the float64 library
  functions are accurate to better than `1e-14` relative. After a rounding fix
  (2026-09-25), all 16,539 saved cuts were re-certified without a solver
  (Section 1), so no run had to be repeated. In tests, every cut
  holds at 20,000 random curve points in 10 families. For `(t, t^2, t^3)` it
  agrees with the exact two-cone moment hull on 1,600 of 1,600 random points.
- **Pipeline.** `code/model.py` gives every univariate term of a selected
  variable an auxiliary variable; `code/run.py` solves the root with a callback
  that separates the root relaxation point, then adds the cuts as static rows
  and solves again (Gurobi 13.0.3, `NonConvex=2`, 1 thread, 1800 s including
  the root phase). Controls: `orig` (original model), `sub` (substituted, no
  cuts), `soc` (exact `(x, x^2, x^3)` cone hull enforced at every node).
- **Beyond the listed bounds: waterno2_06/09/12/18/24.** Final dual bounds with
  cuts are 229.7, 636.6, 1555, 3226 and 4464, against 112.9, 196.1, 323.2,
  677.2 and 796.3 for the original model and MINLPLib's best listed dual bounds
  (2026-09-23) of 165.19, 273.90, 479.51, 770.74 and 1095.13. Seed-1 replicates
  give 1578, 3192 and 4418 on `_12/_18/_24`. The cone hull gives 232.7, 644.3,
  1502, 3092 and 4305, so root-only static cuts capture the hull's effect.
  `waterno2_24` was not covered by the earlier note. These are single,
  uncertified floating-point runs. The cut files of these earlier seed-0 runs
  were overwritten (`_12/_18/_24`) or use an older scaling (`_06/_09`);
  seed-0 reruns with the current code and saved cuts give 225.7, 656.0, 1573,
  3144 and 4442 (see "Regenerated runs (2026-09-23)").
- **Gains below the listed bounds:** ex8_4_2 (0.413 to 0.448; cone hull 0.482;
  listed 0.48514), ghg_2veh (7.150 to 7.405; listed 7.4335), btest14 (-61.94 to
  -60.51; listed -59.817). On these, substitution alone hurts and the cuts more
  than recover it.
- **lnts100: small and seed dependent.** Cuts beat the original model in 3 of 3
  seeds and exceed the listed 0.55299 in 2 of 3, by at most 6e-4. Not counted
  as robust.
- **No gain or worse:** chp_partload, super3t, ghg_3veh, feedtray, ex8_3_13,
  lnts50/200/400, wastepaper5/6, ex8_5_4/6.
- **No cuts found:** water, waterx, 4stufen (no violated root point), ex8_5_1/2
  (root LP not optimal), uselinear (root LP not solved within 900 s).
- **Numerically unreliable, excluded:** gams02, ex8_4_7, ex7_3_5 (Section 4).
- **Not applicable:** rocket*, truck, ex8_1_4/5, ex8_6_1 (unbounded variables),
  beuster (numerically rejected), blendgap (`erf` unsupported), kriging_peaks
  (no variable with two atoms).

## Corrections after independent review

The [review](review.txt) (scripts in `code/review/`) confirmed: exact validity of
every saved cut on its whole curve for waterno2_06/09/12/18/24 (rational
arithmetic; worst slacks +1.5e-11 and +2.5e-12 on `_06` and `_24`); curve
intervals equal to the OSiL bounds; the relaxation property (row-by-row
comparison with an independent reader, feasibility at the MINLPLib best point);
the tables against raw results; and the gain itself (independent rebuild of
waterno2_06, 300 s: original 94.44, substituted 91.36, substituted plus saved
cuts 212.42). Corrections:

- The saved cut files for `_12/_18/_24` are from the seed-1 runs (1102/1751/2479
  cuts); `run.py` wrote every run to `cuts/<name>.json`, so the seed-0 cuts behind
  the table (1232/1664/2202) were overwritten and cannot be checked.
- The saved `_06`/`_09` cuts were generated under an earlier scaling (for example
  `t = 4 x^2` on `[0, 0.58]`), while the current `model.py` uses `t = x^2` there, so
  `check_models.py waterno2_06` now reports the substituted-plus-cuts model as
  infeasible with the saved cuts. Each run was self-consistent, so the results
  stand, but the statements in Sections 2 and 5 that waterno2 was "not
  affected" by the rescaling and that the model check passes are not true of the
  files now on disk. Reproducing the table requires regenerating the cuts with
  the current code (done; see "Regenerated runs (2026-09-23)").
- Wording: the root-bound ratio on waterno2 is 6.7–67 (waterno2_09: 6.69), not
  7–67; the lnts100 root value is 0.5275.

The review's checks above refer to the earlier cut files, now in
`code/cuts/superseded/`.

### Regenerated runs (2026-09-23)

`run.py` now writes cuts to `cuts/<name>[_pb]_<mode>_s<seed>.json`, and each
cut records the auxiliary variables it acts on: `t_j = funcs[j](x)`, and the
model term `keys[j](x) = factors[j] * t_j`. `check_models.py` takes a cuts file
and reports cuts whose recorded factors differ from the current `model.py`.
The earlier files were moved, not deleted:

- `code/cuts/superseded/waterno2_{06,09}.json`: earlier seed-0 cuts, old
  scaling (cannot be loaded into the current model).
- `code/cuts/superseded/waterno2_{12,18,24}.json`: seed-1 cuts, current scaling
  (no recorded factors).
- `code/results_superseded/waterno2_*_cuts_1800.out`: earlier seed-0 cuts
  results (logs in `code/logs/superseded/`).

The `cuts` mode was rerun for waterno2_06/09/12/18/24 with seed 0, the current
code and the Section 3 protocol (1800 s including phase 1, 1 thread,
`NonConvex=2`, `MIPGap=1e-4`; 5 jobs in parallel, `code/jobs_regen.txt`).
Dual bounds after 1800 s:

| instance | cuts, regenerated, seed 0 | root cuts | root bound | cuts, earlier, seed 0 | cuts, earlier, seed 1 | orig | listed best dual | best primal |
|---|---|---|---|---|---|---|---|---|
| waterno2_06 | 225.68 | 112 | 0.0 (see below) | 229.74 | - | 112.89 | 165.19 | 282.888 |
| waterno2_09 | 656.03 | 815 | 448.1 | 636.57 | - | 196.13 | 273.90 | 922.595 |
| waterno2_12 | 1572.66 | 1081 | 1152.4 | 1555.43 | 1578.30 | 323.19 | 479.51 | 2263.36 |
| waterno2_18 | 3144.48 | 1770 | 2535.8 | 3226.22 | 3191.63 | 677.20 | 770.74 | 5269.64 |
| waterno2_24 | 4441.52 | 2150 | 3544.9 | 4464.12 | 4417.70 | 796.29 | 1095.13 | 7332.72 |

Which files back which numbers:

- Regenerated seed 0: `code/results/waterno2_*_cuts_1800.out`, cuts in
  `code/cuts/waterno2_*_cuts_s0.json`, incumbents in
  `code/points/waterno2_*_cuts_s0_1800.json`.
- Earlier seed 0 (Section 4 table and Summary): results in
  `code/results_superseded/`. Their cuts are `code/cuts/superseded/waterno2_{06,09}.json`
  (old scaling); the `_12/_18/_24` seed-0 cuts are lost.
- Earlier seed 1: `code/results_seed/waterno2_*_cuts_s1.out`, cuts in
  `code/cuts/superseded/waterno2_{12,18,24}.json`.
- orig, sub and soc: `code/results/`, unchanged.

The regenerated bounds are within -2.5% to +3.1% of the earlier seed-0 values,
2.0–5.6 times the original model's, and 1.37–4.08 times the listed best dual
bounds. They stay below the listed best primal values. The conclusions of
Section 4 hold. They are still single, uncertified floating-point runs.

On waterno2_06, phase 1 of the regenerated run stopped after 0.7 s and 7
separation calls, with 112 cuts and a recorded Gurobi bound of 0.0 (earlier run:
39.9 s, 39 calls, 673 cuts, root bound 140.0). The final bound is nevertheless
close to the earlier one. The cause of the early stop was not investigated.

Checks on the regenerated cut files (`code/checks_regen_s0.out`), all passing
on all five instances:

- `validate.py`: the MINLPLib best point lies inside every curve interval and
  satisfies every cut (minimum relative slack 2.9e-15); no cut is violated at
  2,000 random curve points (minimum relative slack 1.6e-15).
- `review/exact_cuts.py` (exact rational arithmetic): 0 of 5,928 cuts violated;
  worst absolute slack +1.5e-11 (`_06`).
- `check_models.py`: recorded factors match the current model for every cut;
  with the original variables fixed at the best point, orig, sub and sub+cuts
  are feasible with the same objective.

For comparison, `check_models.py waterno2_06 cuts/superseded/waterno2_06.json`
still reports sub+cuts as infeasible (IIS: a cut, `x366`, `t366_0`, `t366_1`).

## 1. Separator

Given a point `p` and the curve `phi(t)`:

1. Scale every coordinate to `[0, 1]` over the curve.
2. Solve `min c0 + c.s(p)` subject to `c0 + c.s(phi(t_i)) >= 0` for `t_i` in a
   sample `T` and `|c| <= 1` (HiGHS). `T` starts with 129 points.
3. Minimize `c.phi(t)` on a 4,097-point grid, refine the three best local minima
   with bounded scalar minimization, add them to `T`, and repeat until the
   direction is feasible to within `1e-3` of the violation. Only the direction
   is taken from the LP.
4. Unscale and zero coefficients contributing less than `1e-11` of the largest.
5. Set the constant to minus a certified lower bound of `g = c.phi` over
   `[l, u]`: on each of 4,096 pieces `[a, b]`, the larger of the interval
   extension of `g` and `min(g(a), g(b)) - max(0, M) (b-a)^2/8` with `M` an
   interval upper bound of `g''` on the piece (valid because `g` minus its chord
   vanishes at `a, b` and has second derivative at most `max(0, M)`; the clamp
   matters when `M < 0`, and `code/curvehull.py::_piece_lower` applies it).
   Operations are widened outward by `4e-16` (arithmetic) or `1e-14` (library
   functions) relative; loose pieces are bisected. The resulting shift is at
   most about `1e-8` of the cut's scale. The other roundings on this path have
   explicit margins: the factor `1 + 1e-15` on `max(0, M) (b-a)^2/8` covers
   its at most five roundings, and the error term of each linear bound
   `sum_j c_j y_j` (`_lin_lower`) is more than twice the rounding error of its
   products, sum and final subtraction. The final
   subtraction of `max(0, M) (b-a)^2/8` from `min(g(a), g(b))` in `_piece_lower`
   is rounded downward (one step toward `-inf` after round-to-nearest; exact when
   the subtrahend is 0). Before 2026-09-25 this step was only rounded to
   nearest; see "Saved cuts after the rounding fix" below.

**Saved cuts after the rounding fix (2026-09-25).** All saved cuts were
generated before the fix. `code/cuts_rounding_check.py` rebuilds each curve from
the funcs and interval recorded in the cut and recomputes the constant with the
corrected code, without a solver. It covers all 30 non-empty files in
`code/cuts/` and `code/cuts/superseded/` (16,539 cuts; output in
`code/cuts_rounding_check.out`):

- The previous code reproduces 16,536 saved constants exactly. For the other 3
  (feedtray), it gives a constant 8.9e-16 stronger than the saved one, which
  equals the corrected constant. The cause was not investigated; it does not
  affect validity.
- The corrected constant equals the saved one for 1,462 cuts. For the other
  15,077, the saved cut is stronger, by at most 2.8e-14 absolute (ex8_4_7) and
  1.7e-16 relative to the cut's scale `1 + sum_j |c_j| max |phi_j|`. No saved
  cut is weaker.
- For each of these 15,077 cuts, the saved constant itself was certified. The
  corrected code, bisecting until every piece's bound reaches minus the saved
  constant, certified 15,066. The other 11 (1 in chp_partload, 1 in ex8_5_4,
  1 in ghg_2veh, 6 in ghg_3veh, 2 in super3t) touch the curve so closely that
  the float enclosure margins exceed their slack: high-precision evaluation of
  the distinct ones gives minimum slacks of 3e-16 to 1.3e-14. They were
  certified with 200-bit interval arithmetic (`mpmath.iv`: branch and bound with
  the interval extension and a second-order Taylor bound, all constants
  converted exactly). As a control, the same check fails for all 11 when
  their constants are strengthened by `1e-13 max(1, |c0|)`. The slack values
  and this control are not in the saved output.

Every saved cut is therefore valid under the corrected certificate, and no solver
run had to be repeated because of this fix. This concerns the cut constants for
the recorded curves only. It does not cover cut files that were overwritten: the
earlier seed-0 cuts of waterno2_12/18/24 and, because `run.py` then used one file
per instance, the cuts of all but one run of each instance with replicates (for
example lnts100 and lnts400 seeds 0/1/2). The dual bounds remain uncertified floating-point
Gurobi output. The scaling version of controls that were not rerun is still
unknown (Section 2).

A first version bounded `g''` from the wrong side; the random-point test caught
it before any solver run. Speed: about 10 ms per cut.

## 2. Reformulation

- An atom of `x` is a maximal nonlinear subexpression in `x` alone after
  splitting sums, negations and constant factors; diagonal `x^2` terms count.
  Atoms are identified up to a constant factor.
- A variable is selected if it is not binary, has finite bounds, and has at
  least two atoms that are finite on `[l, u]` and linearly independent of each
  other and of `(1, x)`.
- Each atom becomes `t = g(x)`, with `g` a power-of-two rescaling of the atom;
  bounds of `t` come from the certified enclosure. For gams02 and ex8_5_*, curve
  intervals came from Gurobi presolve with `DualReductions=0`.
- **Scaling problems found and fixed.** An outer factor `2^-42` inside a nonlinear
  expression is treated as zero by Gurobi (made gams02 infeasible), so powers are
  scaled in the argument. Scaling every atom to order 1 multiplied Gurobi's
  absolute tolerance on `t = g(x)` by up to `2^18` (ex8_4_7), and Gurobi accepted
  points violating the original model by `8.6e-4`. Final rule: scale down only
  above `2^30`. The runs in `code/jobs_rescale.txt` (cuts, sub and, where used,
  soc for gams02, chp_partload, super3t, ghg_2veh, ghg_3veh, ex8_4_2, ex8_4_7 and
  ex7_3_5) were rerun; superseded runs are in `code/results_oldscale/`. The saved
  result files do not record the scaling factors, so they do not identify the
  scaling version of the other compared runs (for example the waterno2 `sub` and
  `soc` controls and the lnts runs). An earlier version of this report said that
  waterno2 was not affected; that was wrong. The rescaling changed some waterno2
  auxiliary variables (for example `t = 4 x^2` became `t = x^2` on `[0, 0.58]`),
  so the earlier seed-0 waterno2 cuts runs used the old scaling and the seed-1
  replicates the new one. Each run was self-consistent. The waterno2 cuts runs
  were regenerated with the current code (see "Regenerated runs (2026-09-23)").

Example curves: waterno2, 78–312 variables with `(x, x^2, x^3)`; chp_partload,
102 variables such as `(x, x^2, 1/x, x^3)`; lnts, `(x, cos x, sin x)` on
`[-pi/2, pi/2]`; ex8_3_13, `(x, x^0.3, x^1.8)` and `(x, e^-9632/x, e^-4816/x)`
(full list in `code/survey.out`).

## 3. Protocol

Up to 17 single-thread runs in parallel on an 18-core Xeon w5-2565X;
`MIPGap = 1e-4`. Phase 1: `NodeLimit = 1` with the separation callback (up to 60
calls), 1–100 s, counted against the 1800 s. Phase 2: a fresh model plus the
cuts as static rows. Separation inside the tree was tried on waterno2_06 (69 s
on 5 nodes) and dropped. Listed bounds from the MINLPLib pages on 2026-09-23
(`code/listed_bounds.json`): the best dual over all solvers and the bold best
primal with its solution file.

## 4. Results (1800 s, seed 0)

| instance | root cuts | root bound orig / cuts | orig | sub | cuts | soc | listed best dual | best primal |
|---|---|---|---|---|---|---|---|---|
| waterno2_06 | 673 | 18.5 / 140.0 | 112.89 | 117.42 | 229.74 | 232.72 | 165.19 (SCIP) | 282.888 |
| waterno2_09 | 1006 | 68.0 / 454.8 | 196.13 | 215.72 | 636.57 | 644.32 | 273.90 (SCIP) | 922.595 |
| waterno2_12 | 1232 | 17.3 / 1162.8 | 323.19 | 438.20 | 1555.43 | 1501.67 | 479.51 (GUROBI) | 2263.36 |
| waterno2_18 | 1664 | 351.2 / 2505.4 | 677.20 | 727.50 | 3226.22 | 3091.66 | 770.74 (SCIP) | 5269.64 |
| waterno2_24 | 2202 | 392.9 / 3550.7 | 796.29 | 816.51 | 4464.12 | 4305.12 | 1095.13 (SCIP) | 7332.72 |
| ex8_4_2 | 78 | 0 / 0 | 0.4132 | 0.3611 | 0.4479 | 0.4816 | 0.48514 (GUROBI) | 0.485152 |
| ghg_2veh | 101 | 0 / 0 | 7.1497 | 6.9975 | 7.4051 | 7.2954 | 7.4335 (SCIP) | 7.77090 |
| btest14 | 26 | -4.8e5 / -5.2e5 | -61.938 | -63.880 | -60.513 | -61.169 | -59.817 (LINDO) | -59.817 |
| ghg_3veh | 132 | 0 / 0 | 6.0606 | 5.0093 | 5.8829 | 5.1454 | 7.7543 (ANTIGONE) | 7.75401 |
| chp_partload | 601 | 20.159 / 20.159 | 20.497 | 20.465 | 20.459 | 20.504 | 23.298 (XPRESS) | 23.298 |
| super3t | 174 | -1 / -1 | -1 | -1 | -1 | -1 | -1 | -0.68597 |
| feedtray | 81 | -68.68 / -68.68 | -60.07 | -56.95 | -58.27 | - | -21.31 (GUROBI) | -13.406 |
| ex8_3_13 | 7 | -100 / -100 | -49.84 | -49.84 | -49.84 | - | -43.09 (BARON) | -43.089 |
| lnts50 | 51 | 0.531 / 0.45 | 0.554613 | 0.554577 | 0.554613 | - | 0.554648 | 0.554669 |
| lnts100 | 101 | 0.527 / 0.45 | 0.551896 | 0.552126 | 0.553019 | - | 0.552990 | 0.554595 |
| lnts200 | 201 | 0.45 / 0.45 | 0.552033 | 0.551342 | 0.551142 | - | 0.552199 | 0.554577 |
| lnts400 | 401 | 0.45 / 0.45 | 0.550419 | 0.545491 | 0.552197 | - | 0.552044 | 0.554572 |
| wastepaper5/6 | 10/17 | 0 / 0 | ~0 | ~0 | ~0 | - | 0.00081924 / 0 | 0.00082 / 0.00013 |

The waterno2 rows of the root-cuts, root-bound-with-cuts and cuts columns are the
earlier seed-0 runs (old scaling on `_06/_09`); their raw results are now in
`code/results_superseded/`. Regenerated seed-0 runs are in "Regenerated runs
(2026-09-23)".

ex8_5_4 / ex8_5_6 (presolve bounds; 22 / 64 cuts) report "optimal" values below
the listed optimum in all modes (tolerance artefacts); not interpreted.

Replicates: waterno2 cuts, seed 1: 1578.30 / 3191.63 / 4417.70 (`_12/_18/_24`).
lnts100, seeds 0/1/2: cuts 0.553019 / 0.552836 / 0.553572; orig 0.551896 /
0.550800 / 0.551767. lnts400: cuts 0.552197 / 0.546537 / 0.546754; orig
0.550419 / 0.549874 / 0.548441.

**Interpretation.** On waterno2 the root bound is 7–67 times and the final bound
2.0–5.6 times higher than for the original model, above the listed bounds by
factors of 1.4–4.2, in both seeds where replicated; substitution alone adds
little, so the cuts carry the gain. On ex8_4_2, ghg_2veh and btest14 the cuts
recover the loss caused by substitution and add some, without exceeding the
listed bounds. ghg_3veh: net negative. lnts: small and seed dependent; part of
the lnts100 gain may come from substitution alone.

**Excluded as numerically unreliable.** gams02 (presolve bounds `[6324, 15810]`,
`x^3` about `4e12`; equality rows with `1e12` terms must cancel to `1e-6`): the
cuts run "proves" 1.784e8 against a known point of 8.947e7. (An earlier version
also said that the substituted model rejects MINLPLib's best point. No saved run
shows this: `code/modelcheck.out` reports orig, sub and sub+cuts feasible there
with objective 89466860.66. That the known point satisfies the cuts does not
show whether the fault lies in solver numerics, the modeling or a version
mismatch.)
ex8_4_7: incumbents violate the original model by `9e-4` in every mode.
ex7_3_5: "optimal" values 1.2035–1.2046, below the listed dual 1.20665, in all
modes; the substituted model rejects the best point.

## 5. Validation

- The bold MINLPLib best point satisfies every saved cut (minimum relative slack
  `3e-15` to `0.17`, never negative) and lies inside every curve interval
  (`code/validate.out`, `code/modelcheck_rescaled.out`). Exception: in
  `modelcheck_rescaled.out` the lnts100 check failed with a JSON decode error on
  `cuts/lnts100.json`. The file now parses and passes on rerun (2026-09-25,
  `code/modelcheck_lnts100.out`): the best point lies in the curve interval and
  satisfies all 101 cuts (minimum relative slack 2.2e-6), and orig, sub and
  sub+cuts are feasible with objective 0.5545954. Its constants are certified
  (see Section 1). The run that wrote this file is not recorded: seeds 0, 1 and 2
  each found 101 root cuts and wrote to the same file name, and the file was last
  modified at 13:40 on 2026-09-23, after all three runs. So the check does not
  validate the cut set of a specific reported run.
- Every cut holds at 2,000 random points of its curve.
- With the original variables fixed at the best point, orig, sub and sub+cuts
  are feasible with the same objective on every instance with a saved successful
  check except ex7_3_5, whose substituted model is infeasible in
  `code/modelcheck_rescaled.out` (`code/check_models.py`; see also
  `code/modelcheck.out`).
  lnts100 passes on its current cut file (see above). gams02
  passes in `modelcheck.out` (objective 89466860.66 in all three models);
  `modelcheck_rescaled.out` has no gams02 entry.
- Correction: for waterno2 these checks were run on cut files that are now
  superseded (`_06/_09` before the rescaling, in `code/modelcheck.out`;
  `_12/_18/_24` with the seed-1 files). With the current `model.py`, the
  superseded `_06` file fails `check_models.py`. The regenerated seed-0 files
  pass all three checks and the exact check (`code/checks_regen_s0.out`; see
  "Regenerated runs (2026-09-23)").
- These are necessary checks; validity rests on the certification. Dual bounds
  are uncertified floating-point Gurobi output, and the MINLPLib pages do not
  state solver versions, settings or times, so the comparison with listed
  bounds is not like-for-like.

## 6. Side observation: primal points

The waterno2 cuts runs report incumbents below the listed primal values (seed
0, not saved: 2234.09 / 5090.69 / 6962.67 on `_12/_18/_24`; seed 1, saved in
`code/points/`: 5077.88 on `_18`, 7082.77 on `_24`). The seed-1 points have
maximum float violation about `9.9e-7` in the original model: feasible at
`1e-6`, not at `1e-8`, and not polished. The regenerated seed-0 runs (saved in
`code/points/`) report 282.917 / 909.180 / 2238.91 / 5072.44 / 7062.45 on
`_06/_09/_12/_18/_24`, with maximum violations 5.0e-7 to 9.97e-7 in the original
model; the same caveat applies.
