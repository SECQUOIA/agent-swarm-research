# Review of experiment-report.md (iterated OBBT as a presolve)

Date: 2026-09-23. Reviewer: independent review (fresh context).
Scope: `experiment-report.md` against the raw data in `results/` and the code in `code/`
(`pipeline.py`, `relax.py`, `analysis.py`, `validate.py`, `solvers.py`, `qcqp.py`). I did not
edit the report or the experiment code.

Check scripts: `code/review_checks/experiment/`. They read the raw files directly and do not
import `analysis.py`. Run them with `~/miniconda3/envs/exact-quadratic-hull/bin/python`
(`obbt3.py` needs `PYTHONPATH=code`).

## Summary

The main conclusion holds. As an external presolve, iterated OBBT does not pay off on this
test set. The result is robust:

- Every headline solver-level number is correct. I recomputed them independently from
  `final.jsonl`, `roots.jsonl`, `obbt.jsonl` and the box files.
- The McCormick relaxation is correct. On five small instances, one OBBT round agrees with an
  independently built LP to within the safety margin, and every bound contains the exact
  nonconvex bound.
- Timing is consistent across the separately run batches.
- Even if OBBT cost nothing, the final solves on the tightened boxes would take the same time
  as the control (ratio 0.99–1.02).

Some secondary statements are wrong or overstated:

1. The report says that on hard instances, node ratios against the control are 0.96–1.1. For
   SCIP `ad0.8` the ratio is 0.87 on all hard instances and 0.78 on hard instances whose box
   changed.
2. The contraction-regime conclusion ("stall is the typical case") rests on a sample that was
   selected for slow convergence.
3. "Fixed point after 1 round on 104 instances" is wrong. On 100 of these, round 1 changed
   nothing.
4. The explanation of the `crudeoil_lee1_05` wrong answer is wrong: that run had no incumbent.
5. Wrong answers count as solved in the tables, although Section 2.3 says otherwise.
6. Several Section 3 and 4.2 numbers come from code that is not in `analysis.py`. I could
   reproduce some of them but not all.

None of these changes the main conclusion.

## 1. Recomputation of the headline numbers

Script: `recompute.py`. My outcome logic follows the stated metric. Unsolved runs count 600 s.
The pipeline total is root time + OBBT time + final-solve time. A root run that already proved
optimality is charged its own time. Shared final runs are matched by box hash.

**All 339 instances, against the default (report Section 4.1): every entry matches.**

| solver | arm | solved | SGM time (s) | time × | nodes × |
|---|---|---|---|---|---|
| Gurobi | `OBBT=3` | 640 | 2.49 | 1.051 | 0.818 |
| Gurobi | control | 642 | 2.57 | 1.084 | 1.045 |
| Gurobi | r1 / r5 / ad0.5 / ad0.8 / fp | 637 / 638 / 637 / 637 / 637 | 3.11 / 3.40 / 3.14 / 3.23 / 4.08 | 1.314 / 1.438 / 1.328 / 1.365 / 1.726 | 0.992 / 0.834 / 0.967 / 0.897 / 0.768 |
| Gurobi | known-fp (238 pairs) | 217 vs 220 | 9.26 vs 4.50 | 2.055 | 0.699 |
| SCIP | control | 574 | 8.30 | 1.157 | 1.111 |
| SCIP | r1 / r5 / ad0.5 / ad0.8 / fp | 570 / 564 / 570 / 571 / 561 | 8.67 / 8.84 / 8.71 / 8.69 / 9.50 | 1.208 / 1.231 / 1.213 / 1.210 / 1.323 | 1.049 / 0.851 / 0.983 / 0.882 / 0.727 |
| SCIP | known-fp (273 pairs) | 220 vs 221 | 15.1 vs 12.3 | 1.233 | 0.553 |

**Pipeline against the control (Section 4.2), on instances where OBBT ran.** These match:

- Gurobi, time: 1.269, 1.330 and 1.788 (r1, ad0.8, fp). Nodes: 0.930, 0.809 and 0.653.
- SCIP, time: 1.053, 1.055 and 1.173. Nodes: 0.957, 0.769 and 0.620.
- Solved: 435/440 for Gurobi. For SCIP: 438, 439 and 429, against 442.

**Split by gap closed (Section 4.2).** All 12 cells reproduce: pair counts, node ratios,
final-solve time ratios and mean control times. For example, Gurobi `fp` with gap closed at
least 0.5 gives 112 pairs, nodes 0.18, solve 0.87 and a mean control time of 4.9 s. Some pairs
have no defined gap closed (6 for Gurobi, 10 for SCIP). These pairs appear in no column.

**Hard instances against the default.** These match. Gurobi: nodes 0.99–1.02, time 1.15–1.23,
97–98 solved against 100. SCIP: nodes 1.06–1.26, time 1.27–1.51, 127–137 solved against 141.

**OBBT level (`obbtcheck.py`).**

- Mean gap closed per round, for k = 1, 2, 3, 5, 10 and 50. All three rows match exactly:
  - known cutoff: 0.236, 0.274, 0.296, 0.322, 0.338, 0.346;
  - Gurobi incumbent: 0.147, 0.181, 0.203, 0.231, 0.247, 0.250;
  - SCIP incumbent: 0.176, 0.213, 0.237, 0.260, 0.278, 0.287.
- Instance counts (305 / 235 / 267) and SGM OBBT times (1.1/2.2, 1.4/2.9, 1.1/2.1 s) match.
- The 235-instance comparison matches: 0.250 against 0.268.
- **Contraction regimes: 149 instances; 79 with a median above 0.95; 34 at most 0.5.** These
  reproduce exactly, and so does the whole histogram (16/18/9/2/12/13/79). They do not depend
  on whether "rounds 3–10" means round index or moving-round index.
- These also match:
  - median OBBT time 0.038 s (round 1) and 0.229 s (fixed point);
  - 36 instances above 10 s and 14 above 120 s in round 1;
  - 18 trajectories capped;
  - LPs and times for Gauss–Seidel and Jacobi: 289,941 against 300,710 LPs, 12,031 s against
    12,053 s;
  - filtering: 25,712 against 87,443 LPs (the report's 25,712 includes 2 bound LPs per
    instance, to match the no-filter count);
  - restriction: 105,878 against 109,107 LPs;
  - 2 infeasible LPs;
  - integer-only instances: 109, of which 25 changed in round 1.

**Discrepancies (minor unless noted):**

- **D1 (wrong answers counted as solved).** Section 2.3 says a solved run must have an
  objective within `1e-3` of `f*`. `analysis.py` sets `solved` from the status alone and only
  flags wrong answers. Under the stated definition:
  - SCIP control: 573, not 574 (all instances); 441, not 442 (OBBT-ran set);
  - SCIP `pipe-r5`: 563, not 564; 431, not 432.
  - Time ratios move by at most 0.005.
- **D2 (misdescribed count).** "Reaches a fixed point after 1 round on 104 instances (nothing
  changes after round 1)" is wrong. The 104 instances have a one-round trajectory:
  - On 100 of them, round 1 itself changed nothing, so the box is the FBBT box.
  - On 7 of the 104, round 1 hit the 400 s cap and did not finish. Examples:
    `maxcsp-geo50-20-d4-75-36`, `celar6-sub0`, `qspp_0_1{1,2}_*`, `sonet*`,
    `edgecross22-096`.
  - Only 23 trajectories converge after exactly one tightening round.
  - This also qualifies Section 3 "Cost": on the large binary QPs, round 1 "changes no bound"
    partly because it was cut off at 400 s.
- **D3.** "Round 1 tightens some bound on 241 of 339": I count 239, by both the `nchanged` field
  and a direct comparison of the r1 box with the FBBT box.
- **D4.** Section 1.5 says `ad0.8` stops after round 1 on 43–54% of instances. The counts are
  156/339, 129/238 and 147/273, which is 46–54%. It runs 5 or more rounds on 32, 19 and 22
  instances, not 30, 18 and 21.
- **D5.** The share of round-1 OBBT time on integer-only instances reproduces (92% against the
  reported 91%). The reported totals do not: 4,976 of 5,457 s. Summed over the three cutoffs, I
  get 12,981 of 14,115 s. The script that produced 5,457 is not in the repository.
- **D6.** The Gauss–Seidel-versus-Jacobi and filtering box comparisons are not reproducible from
  the saved code: "GS smaller on 165 / Jacobi on 1" after round 1, "16 / 5" at the fixed point,
  and filtering "weaker on 26 / stronger on 9". They depend on the tolerance. Comparing total
  normalized width `S`, with relative tolerances from `1e-6` to `1e-2`:
  - round 1: 116–168 against 0–1, which is qualitatively the same;
  - fixed point: 71/60 at `1e-6`, 18/20 at `1e-4` and 1/4 at `1e-2`, so Jacobi is sometimes
    ahead;
  - filtering: weaker on 10–19 instances and stronger on 0–4.

  "Both reach nearly the same limit" is right. The specific counts should be recomputed with
  a stated tolerance, or dropped.
- **D7.** Section 1.2 says base times on the pairs with gap closed at least 0.5 "average only
  1–5 s". These are control times, and Gurobi `ad0.8` has 6.4 s. Section 4.1 says "the order of
  the rules is the same" in both subsets. For SCIP, `ad0.8` and `r1` swap in the subsets, with
  differences below 0.01.
- **D8 (substantive).** Section 1.2 says that on hard instances, "node ratios are 0.96–1.1
  against the control". No table in `arm_tables.csv` gives hard-versus-control for all hard
  instances, so I recomputed it:
  - Gurobi: 0.98–1.01 on all hard instances; 0.96–1.02 on hard instances with a changed box.
  - SCIP: 0.87–1.04 on all hard instances; 0.78–1.07 on hard instances with a changed box.
    `ad0.8` gives 0.87 and 0.78.

  Time against the control on hard instances is 1.16–1.24 (Gurobi) and 1.10–1.30 (SCIP), so
  the conclusion does not change. The stated range is too narrow for SCIP.
- **D9.** The Section 4.2 split table, the hard-instance statements, the width-versus-slack
  exponents, the integer-only statistics and the GS/Jacobi counts are computed outside
  `analysis.py`. The report lists `analysis.py` as the source of "the tables". Save the
  ad hoc code.

## 2. Methodology

### Fairness of the comparison

- **Time budget.** This is correct and consistent. The final solve gets 600 s minus the root
  time and the OBBT time. The total is capped at 600 s, and solved requires a total of at most
  600 s. The default gets 600 s. Relaxation build time and the initial bound LP are charged to
  OBBT. The build is small: about 20 s in total per cutoff source.
- **Root run shared across seeds.** The root run uses seed 0 and is charged to both final
  seeds. This slightly understates variance but is not biased.
- **Unsolved runs in the SGM.** They enter as 600 s. Every non-error unsolved run in fact ends
  near 600 s: recomputing with raw times gives the same ratios. SCIP `error` runs are counted
  as 600 s unsolved in the pipelines. A default-arm error would drop the pair instead, but none
  occurred. Nodes are compared only on pairs that both arms solve. This is standard, but it
  hides losses: for example, SCIP `fp` loses 13 pairs against the control.
- **Control arm.** It isolates the box well. The control gets the same root run, incumbent,
  start solution, cutoff and FBBT box, and differs only in the box. I confirmed that the
  setups are identical:
  - Where the r1 box equals the FBBT box, the `pipe-r1` final run has the same setup as the
    control.
  - On 143 Gurobi and 133 SCIP such pairs, node counts are identical in 100% of cases.
  - The SGM time ratio is 1.006 (Gurobi) and 1.008 (SCIP), with a median absolute log
    difference below 0.03.
  - The control was run in a later batch (`final_none.log`, 09:53) than the pipelines. These
    identical runs show that the batches were timed consistently under load, so batch load
    did not bias the comparison.
- **The control is not a neutral restart for SCIP.** On OBBT-ran instances the SCIP control is
  1.19× the default in time and 1.14× in nodes. On hard instances it is 1.16× in time and 1.30×
  in nodes. So the restart with an incumbent, an objective limit and the FBBT bounds hurts SCIP
  beyond the root time. The report calls this the "restart cost". It is partly a SCIP behaviour
  change, not only a second root. This does not affect the comparison of pipeline against
  control.
- **Cutoff direction.** This is correct for both senses:
  - The relaxation uses the minimization form: `sense*c`, `sense*q` and `fconst = sense*c0`,
    with the row `f <= U - fconst`.
  - The Gurobi `Cutoff` is `sense*U`, which for a maximization problem prunes below the
    incumbent minus the tolerance.
  - The SCIP objective limit is `setObjlimit(sense*U)`.
  - The tolerance makes the root incumbent strictly better than the cutoff, so the start
    solution is accepted. No pipeline run ended with status `cutoff` or `infeasible`.
- **`hard` is selected on the default's outcome.** This favours the other arms slightly
  (regression to the mean). The pipelines still lose, so the conclusion is conservative.
- **Instance selection** excludes 38 candidates without finite FBBT bounds on the nonlinear
  variables. That is appropriate for McCormick-based OBBT but limits scope. Root runs already
  solve 101 (Gurobi) and 66 (SCIP) instances, which dilutes the all-instance ratios; the
  OBBT-ran tables handle this.

### Relaxation and OBBT code (`relax.py`)

- **Bilinear rows.** The four rows `w - a x_i - b x_j (>=,>=,<=,<=) -ab` with
  `(a, b) = (l_j, l_i), (u_j, u_i), (u_j, l_i), (l_j, u_i)` are the standard McCormick
  inequalities.
- **Square rows.** The tangents `s - 2p x >= -p^2` at 5 points and the secant
  `s - (l+u) x <= -lu` are correct, with `s >= 0`. For binary squares, `x^2` is replaced by `x`.
- **Updates.** Rows are rewritten in place for the terms of a changed variable.
- **Integer bounds.** New bounds are rounded after the margin. Integrality is otherwise
  dropped, as stated.
- **Filtering** in Gauss–Seidel mode can miss tightenings, because an earlier LP point may be
  infeasible after later tightenings. It can never produce an invalid bound. The report calls
  it a heuristic, which is correct.
- **Ignoring infeasible LPs** is conservative (2 LPs).

**Tests (`relaxtest.py`).** Instances: `pointpack04` (maximization, squares), `nvs13` (general
integers), `ex5_2_2_case1` (pooling), `fuel` (mixed-integer) and `st_qpc-m3a`.

- **LP bound.** The McCormick LP bound on the FBBT box is at most `f*` on all five. It equals
  the bound of my independent LP (scipy/HiGHS, built from `QCQP` data with my own rows) to
  full precision. Examples: -1336.84 against `f*` = -585.2 for `nvs13`; 8422.05 against
  8566.12 for `fuel`.
- **One OBBT round.** I ran a Jacobi round without filtering, using the known cutoff. Every
  bound agrees with the independent HiGHS LP to within `1e-6` relative, which is the `MARGIN`.
  The one exception is integer rounding on `nvs13`: 0.4476 becomes 1.
- **Exact bounds.** Gurobi nonconvex min and max of each variable (up to 12 per instance),
  subject to the original model and `f <= U`, lie inside the OBBT bounds on every variable.
  There are 0 containment violations.
- **Reference solutions.** They lie inside the boxes. My first run flagged `pointpack04`, but
  only because its `.p1.sol` has objective 0. The validation reference (the Gurobi solution,
  objective -1) is inside.
- **Reproducibility.** Rerunning round 1 (Gauss–Seidel with filtering) reproduces the stored
  `r1` box on all five instances.
- **`validity.csv`.** It confirms 4,589 boxes, 16 of them without a reference, and 0 violations.
  The maximum relative violation is `1.9e-7`.

**Is the relaxation too weak?** The five-tangent outer approximation of squares is weaker than
the true envelope. Raising it to 65 tangents (`ntan.py`) changed the fixed-point box on none of
seven square-heavy instances. Only the root LP bound of `nvs18` changed. The tangent count does
not bias the results against OBBT.

### Timing

Load was at most 24 single-thread jobs on 18 cores / 36 threads, with wall-clock times. It is
consistent across batches (see the control-arm check above). All arms, OBBT included, ran under
comparable load. Absolute times are inflated by hyper-threading, but the ratios are not biased.
Python model building is negligible: at most 0.05 s on the largest instances.

### Design choices that affect the size of the overhead (not bugs)

- **Round 1 has no time bound below 400 s**, including for the adaptive rules. The 120 s
  adaptive cap is checked only between rounds. A few large binary QPs pay 240–450 s for a
  round that changes nothing. On the OBBT-ran set, an oracle that skips OBBT when the box does
  not change lowers the time ratio against the control:
  - Gurobi: 1.27 to 1.15 (r1), 1.33 to 1.20 (ad0.8), 1.79 to 1.62 (fp);
  - SCIP: 1.05 to 1.03 (r1).
- **Robustness.** The ratios stay above 1 in every variant I tried. With free OBBT (the OBBT
  time subtracted), the ratio against the control is 0.99–1.02 for all three rules and both
  solvers. With a 10 s shift, it is 1.04–1.66. The bootstrap 95% intervals over instances
  (2,000 resamples) are:
  - Gurobi r1: [1.19, 1.38];
  - Gurobi ad0.8: [1.23, 1.45];
  - SCIP r1: [1.002, 1.12];
  - SCIP ad0.8: [1.001, 1.12];
  - SCIP fp: [1.10, 1.26].

  The SCIP r1 and ad0.8 overheads are only marginally significant. The report should say
  "about 5%, barely distinguishable from zero" rather than present 1.05 as a firm cost.

## 3. Are the conclusions supported?

- **Finding 1 ("does not pay off") is supported and robust.** The strongest form: even with
  zero OBBT cost, the tightened box does not reduce the final-solve time against the control
  (0.99–1.02). Add this free-OBBT number to the report. It is the cleanest evidence and does
  not depend on the implementation's OBBT speed.
- **Finding 2 is supported, but the hard-instance range must be corrected (D8).** The "5.7×"
  and "5×" node reductions are 1/0.18 = 5.6 and 1/0.20 = 5.0.
- **Finding 3 is supported.**
- **Finding 4 is overstated.** The 149 instances were selected because they have at least 4
  moving rounds, which excludes every fast-converging trajectory. The 104 one-round and 23
  two-round cases are not in the sample. So "79 of 149 crawl" cannot show that stalls are "the
  typical case on this test set". About 79 of the 239 instances where round 1 tightens
  anything (33%) show the crawl.
  - With the known cutoff (`epsilon` about `1e-6`), a `rho` near 1 cannot separate a stall of
    the fixed-point map from the approach to the `sqrt(epsilon)` floor.
  - The floor-exponent check rests on 13 and 22 instances with two points each; the report
    says so.
  - Rephrase: "among trajectories that run at least 4 moving rounds, most crawl".
- **Finding 5 is supported.** `ad0.8` time is 1.08–1.10× that of r1, which the report gives as
  3–10%. Fix the stop fractions (D4).
- **Finding 6 is supported**, but the `crudeoil_lee1_05` explanation is wrong. That control run
  (seed 1) had no incumbent: the SCIP root run found none (`start: null`, `cutoff: Infinity`).
  So the failure is SCIP on the FBBT box without an incumbent, not "after a restart with an
  incumbent". Its FBBT box contains the reference solution (`sol_out_fbbt` = 0). The two wrong
  runs are counted as solved (D1).
- **Section 5.** "On the hard instances, OBBT ... changes almost nothing (gap closed is usually
  0) ... consistent with the stall mechanism of Theorem 6." When round 1 already closes no gap,
  the instance tells us nothing about iteration dynamics. These are mostly binary or integer
  QPs, where LP-based OBBT without integrality cannot tighten much. Cite that as the reason,
  not Theorem 6. The recommendations (skip predictor, in-solver re-triggering, test set of
  harder instances) follow from the data.

## Requested changes (in priority order)

1. Correct the hard-instance node range against the control (D8). Add a hard-versus-control
   table to `arm_tables.csv`.
2. Add the free-OBBT ratio (final-solve time against the control) to Finding 1, together with
   bootstrap intervals. Soften the SCIP r1 and ad0.8 overhead to "about 5%, marginal".
3. Reword Finding 4 and the Section 5 link to Theorem 6: the sample is selected, and the
   crawl-versus-floor distinction is not identified.
4. Fix D2 (104 is the one-round count, not convergence after round 1; 7 rounds were capped),
   D3, D4 and the `crudeoil_lee1_05` explanation.
5. Either enforce the objective check in `solved` or change the Section 2.3 wording (D1).
6. Commit the ad hoc analysis code (D9), and recompute or drop the GS/Jacobi and filtering
   counts with a stated tolerance (D5, D6).

## Commands run (targeted; there is no CI check for this experiment)

- `recompute.py`: solved counts, SGMs and ratios against the default and the control, the
  gap-closed split, hard against control, bootstrap, shift 10, oracle skip, free OBBT.
- `obbtcheck.py`, `obbt2.py`, `obbt3.py`: OBBT-level statistics, round counts, integer-only
  statistics, the 235-instance cutoff comparison.
- `relaxtest.py pointpack04 nvs13 ex5_2_2_case1 fuel st_qpc-m3a`: relaxation validity, an
  independent LP, exact-bound containment, `r1` reproduction.
- `noise.py`: identical-setup runs across batches.
- `ntan.py`: tangent-count sensitivity on 7 instances.
- Ad hoc: the `validity.csv` summary, `pointpack04` reference containment, Python model-build
  timing.
