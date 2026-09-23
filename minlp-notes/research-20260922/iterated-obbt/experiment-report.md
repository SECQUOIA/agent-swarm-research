# Adaptive iterated OBBT as a presolve for Gurobi 13 and SCIP 10: experiment report

Date: 2026-09-23. Status: complete first study; independently reviewed (Section 0).

Code: `code/` (`qcqp.py`, `relax.py`, `solvers.py`, `pipeline.py`, `analysis.py`, `validate.py`,
`setup_instances.py`). Raw data and tables: `results/`. The existing `code/tangent_map.py` was not changed.

## 0. Corrections after independent review

An [independent review](review-experiment.md) recomputed every headline number
from the raw data with separate scripts; solved counts, time and node ratios,
gap-closed tables and contraction counts match. It found and this section
corrects the following (the main conclusion is unchanged):

- Hard instances against the control: node ratios are not uniformly 0.96–1.1;
  for SCIP `ad0.8` they are 0.87 (all hard instances) and 0.78 (hard instances
  whose box changed).
- Two SCIP runs that returned wrong optimal values were counted as solved:
  the SCIP control solves 573 (not 574) and SCIP `pipe-r5` 563 (not 564).
- "Fixed point after 1 round on 104 instances" is wrong: on 100 of them round 1
  changed nothing, on 7 round 1 hit the 400 s cap; only 23 converge after one
  tightening round. Round 1 tightens on 239 instances (not 241); the `ad0.8` stop
  fractions are 46–54% (not 43–54%).
- The `crudeoil_lee1_05` explanation is wrong: that control run had no incumbent.
- Finding 4 is overstated: requiring at least 4 moving rounds excludes fast
  trajectories, so the data do not show that slow contraction is typical, and
  they cannot separate a stall from the `sqrt(epsilon)` floor.
- Added by the review: even with zero OBBT time, the tightened boxes give the
  same final-solve time as the control (ratio 0.99–1.02), so finding 1 does not
  depend on the OBBT implementation's speed. SCIP's one-round and `ad0.8`
  overheads are marginal (about 5%, 95% bootstrap interval [1.00, 1.12]).
- Some secondary tables (Gauss–Seidel/Jacobi and filtering box counts) depend on
  a comparison tolerance and were produced by code not saved in `analysis.py`.

## 1. Main findings

1. **As an external presolve, iterated OBBT does not pay off on MINLPLib QCQPs with a realistic
   cutoff.** Every stopping rule makes the shifted geometric mean (SGM) of total time worse than the
   solver's defaults, for both solvers. No rule solves more instances. On the 678 instance–seed pairs
   (339 instances, 2 seeds, 600 s):
   - Gurobi: 640 solved by default. OBBT pipelines solve 637–638 and are 1.31× (one round) to
     1.73× (fixed point) slower.
   - SCIP: 575 solved by default. OBBT pipelines solve 561–571 and are 1.21× to 1.32× slower.
2. **Where OBBT tightens the box a lot, trees shrink a lot, but these instances are easy.** Take the
   pairs where the fixed-point box closes at least 50% of the McCormick-LP gap. Against a control run
   that has the same incumbent but no OBBT, node counts fall 5.7× (Gurobi) and 5× (SCIP). Base times on
   these pairs average only 1–5 s, so the OBBT time dominates. Where OBBT closes less than 50%, node
   counts fall by at most about 25%. On hard instances (default time at least 10 s, or unsolved), node
   ratios are 0.96–1.1 against the control.
3. **More rounds do help the relaxation, with diminishing returns.** With the known optimum as cutoff,
   the mean share of the McCormick-LP root gap closed (over 305 instances with a positive gap) is
   0.236 after 1 round, 0.274 after 2, 0.322 after 5 and 0.346 at the fixed point. With a realistic
   incumbent (median relative slack 3–4%), the fixed point reaches 0.250 (Gurobi incumbent) and 0.287
   (SCIP incumbent).
4. **Contraction is mostly slow, not linear-and-fast.** Take the 149 instances with at least 4 rounds
   in which some variable moved. The median contraction ratio of the moving variables over rounds 3–10
   exceeds 0.95 on 79 of them: a long crawl. It is at most 0.5 on 34 of them: fast convergence. The
   theory's stall and `sqrt(epsilon)`-floor regimes are therefore the typical case on this test set.
5. **The adaptive rule works as designed but has little to exploit.** With `theta = 0.8`, OBBT stops
   after round 1 on 43–54% of instances and costs 3–10% more OBBT time than one round. Nodes fall
   (0.90× Gurobi, 0.88× SCIP against default), but total time is still 1.37× and 1.21× the default.
   Restricting later rounds to moved variables and their bilinear partners saved only 3% of the LPs.
6. **Validity: no violations.** Of the 4,589 tightened boxes, 4,573 belong to instances with a
   reference optimal solution. In every one of them, the reference solution lies inside the box
   (tolerance `1e-6 (1 + |x|)`). Two SCIP runs returned a wrong "optimal" value
   (`crudeoil_lee1_05`, `crudeoil_lee1_09`: -79.35 instead of -79.75). One of them is in the control
   arm without OBBT, and both boxes contain the optimum, so these are SCIP failures after a restart
   with an incumbent, not invalid bounds.

## 2. Setup

### 2.1 Instances

The candidates are MINLPLib instances with the following properties:

- quadratic problem type (`probtype` containing `Q`);
- not flagged convex;
- 5–2000 variables;
- no semicontinuous or SOS variables;
- a known optimum (relative gap between primal and dual bound at most `1e-4`).

This gives 377 candidates. My own FBBT (termwise interval propagation over linear, square and
bilinear terms) must leave every variable in a nonlinear term with finite bounds of magnitude at most
`1e7`. 38 candidates fail this: the `squfl*`, `sssd*` and `ex9_*` instances, `kissing2`, and others.
That leaves **339 instances in 85 families**. 129 of them are in the earlier probe's pool (`pool.csv`).

All results are also reported on two subsets: a family-capped subset (at most 3 per family, 165
instances) and the probe-pool subset. Both give the same picture (`results/arm_tables.csv`).

The OSiL files are parsed directly (`qcqp.py`); all 377 encode their nonlinearities as `qTerm`s.
Reference solutions come from the MINLPLib `.pK.sol` file whose objective matches the MINLPLib primal
bound; `p1` is not always the best one. 275 of the 339 have such a file. For 63 more, the reference is
the Gurobi default solution (seed 0), which must be optimal, match `f*` within `1e-4` and be feasible
within `1e-5`. One instance has no reference: `portfol_robust200_03`. The MINLPLib website
rate-limited the downloads, so some `.sol` files are missing.

### 2.2 Relaxation and OBBT (`relax.py`)

The relaxation is an LP built in Gurobi, with integrality dropped:

- **Bilinear terms:** for each distinct `x_i x_j` (`i != j`), a variable `w_ij` and all four McCormick
  inequalities.
- **Squares:** for each `x_i^2`, a variable `s_i`, tangents at 5 equally spaced points of `[l_i, u_i]`,
  and the secant. For binary `x_i`, `x_i^2` is replaced by `x_i`.
- **Rows:** every original row, with its quadratic terms replaced by `w` and `s`.
- **Cutoff:** a row `f_relax <= U`.

When a bound changes, the rows of the affected terms are rewritten in place (`chgCoeff` and `RHS`), and
Gurobi warm-starts from the previous basis.

OBBT LP settings:

- Presolve is off. It was about 30% slower on warm starts. With the tight known-optimum cutoff, it
  also declared thin but feasible LPs infeasible.
- An LP reported infeasible is ignored (no tightening). This happened for 2 LPs in total, in
  `crudeoil_lee1_05` and `crudeoil_lee1_10`.

Each new bound is relaxed by `1e-6 (1 + |b|)`, and integer bounds are rounded. A tightening is
accepted only if it shrinks the width by at least `1e-4` (relative).

**One round** minimizes and maximizes every variable that appears in a nonlinear term, subject to the
relaxation and the cutoff. It uses Gleixner-style filtering: a direction is skipped for the rest of the
round if some LP solution of the round already sits at that bound. Two update modes were run:

- Gauss–Seidel (bounds updated after each LP);
- Jacobi (all bounds applied at the end of the round).

**Per-round statistics** (`results/obbt_rounds.csv`):

- `rho`: the sum of normalized widths (width over FBBT width) after the round divided by the sum
  before, over the variables whose width shrank by at least 0.1%;
- the geometric mean of the per-variable width ratios;
- the total normalized width;
- the relaxation bound;
- the time and the number of LPs.

**Stopping rules.** All are prefixes of a trajectory, so each trajectory is computed once:

- `r1`: 1 round;
- `r5`: 5 rounds;
- `fp`: fixed point, capped at 50 rounds or 400 s;
- `ad0.5` and `ad0.8`: adaptive. After each round, stop if `rho > theta`, if no bound changed, or if
  the cumulative OBBT time has reached 120 s (20% of the budget). Rounds 2 and later only process the
  variables whose bounds changed in the previous round and their bilinear partners (variables sharing
  a term). The restricted trajectory continues from the box of the shared round 1; the rebuild is
  counted in its time.

### 2.3 Cutoffs, pipelines and baselines

- **Incumbent phase (realistic cutoff).** One root-node run of the target solver per instance, with
  seed 0 and a 30 s limit (Gurobi `NodeLimit=1`, SCIP `limits/nodes=1`). If this run already proves
  optimality (Gurobi 101 instances, SCIP 66), the pipeline stops there and is charged the run's time.
  Otherwise the cutoff is `U = incumbent + 1e-6 max(1, |incumbent|)`, or `U = +inf` if the run found
  no solution (18 Gurobi, 20 SCIP). The relative slack `(U - f*)/max(1, |f*|)` has these quantiles
  (10/25/50/75/90%):
  - Gurobi: 0 / 0 / 0.028 / 0.19 / 0.83;
  - SCIP: 0 / 0 / 0.037 / 0.53 / 2.6.
- **Pipeline arm (`pipe-<rule>`).** The root run, then OBBT with `U`, then the final solve on the
  tightened box. The final solve gets the incumbent as a start solution and `U` as a cutoff (Gurobi
  `Cutoff`; SCIP objective limit). Its time limit is 600 s minus the root and OBBT time. Total time =
  root + OBBT (including building the relaxation) + final solve.
- **Control arm (`pipe-none`).** Added to separate the effect of the box from the effect of the restart
  with an incumbent. It is identical to the pipeline arm but uses the FBBT box, with no OBBT.
- **Baselines.** The solver's defaults on the original model with 600 s: Gurobi (`NonConvex=2`,
  `Threads=1`) and SCIP (1 thread). A second Gurobi baseline adds `OBBT=3` (aggressive).
- **Known-optimum reference (`known-fp`, kept separate).** `U = f* + 1e-6 max(1, |f*|)`, the
  fixed-point box, no root run, and no start solution. It uses seed 0 only and was run only on
  instances where the solver's root run did not solve the problem (238 for Gurobi, 273 for SCIP). Its
  time counts the OBBT.
- **Seeds and deduplication.** The final solves use seeds 0 and 1 (Gurobi `Seed`; SCIP
  `randomization/randomseedshift`). When two rules produce the identical box, one final run is shared
  and each rule is charged its own OBBT time.

Metrics:

- solved: proven optimal within 600 s in total, with the objective within `1e-3` (relative) of `f*`.
  Otherwise the run is flagged wrong.
- time: SGM with shift 1 s over instance–seed pairs, where unsolved runs count 600 s;
- nodes: SGM with shift 10 over pairs solved by both arms;
- final gap: `(P - D)/max(|P|, |D|)`, capped at 1;
- root gap closed: `(root bound of arm - root bound of base)/(f* - root bound of base)`, using the
  solver's own root bound (the Gurobi callback at node 0, SCIP `getDualboundRoot`).

**Load.** Runs executed in parallel on a 36-thread (18-core) machine, with at most 24 concurrent
single-thread jobs and a load average of about 23–25 during the solves. All times are wall-clock
times under that load, including OBBT times.

## 3. OBBT-level results (`results/obbt_summary.csv`, `results/obbt_rounds.csv`)

**Gap closed, full Gauss–Seidel trajectory.** The table gives the mean share of the McCormick-LP gap
closed after k rounds (trajectories that stopped earlier keep their final value), with the SGM of the
cumulative OBBT time in parentheses:

| cutoff | n | k=1 | k=2 | k=3 | k=5 | k=10 | k=50 (fp) |
|---|---|---|---|---|---|---|---|
| known f* | 305 | 0.236 (1.1 s) | 0.274 | 0.296 | 0.322 | 0.338 | 0.346 (2.2 s) |
| Gurobi root incumbent | 235 | 0.147 (1.4 s) | 0.181 | 0.203 | 0.231 | 0.247 | 0.250 (2.9 s) |
| SCIP root incumbent | 267 | 0.176 (1.1 s) | 0.213 | 0.237 | 0.260 | 0.278 | 0.287 (2.1 s) |

The median gap closed is 0 for every rule. With the known cutoff, 71 instances reach at least 50%
closure after round 1 and 103 at the fixed point. The fixed point adds at least 10 points over round 1
on 64 instances (known cutoff), 47 (Gurobi cutoff) and 54 (SCIP cutoff). These closures are measured
on my McCormick LP. The earlier probe measured the SCIP root with cuts, so the numbers are not directly
comparable.

On the 235 instances that have both cutoffs, the Gurobi incumbent closes 0.250 at the fixed point and
the known optimum closes 0.268. The realistic cutoff costs little on average, because on many
instances the root incumbent is already optimal (slack 0 at the 25% quantile).

**Cost.**

- OBBT time (known cutoff): median 0.04 s for 1 round and 0.23 s at the fixed point. It is heavy-tailed:
  36 instances need more than 10 s for round 1 and 14 need more than 120 s. The fixed point hits the
  400 s cap on 18.
- The per-LP time is inherent. On `crudeoil_lee4_05` (10k rows), a warm-started OBBT LP still takes
  hundreds of simplex iterations (70–110 ms). Primal simplex, dual simplex and `LPWarmStart=2` made no
  difference.
- On large binary QPs, round 1 takes 30–360 s and changes no bound, for example
  `maxcsp-geo50-20-d4-75-36`, `chimera_*` and `gilbert`.

**Rounds used by the adaptive rules** (known / Gurobi / SCIP cutoff):

- `ad0.5` stops after round 1 on 231/339, 188/238 and 213/273 instances.
- `ad0.8` stops after round 1 on 156/339, 129/238 and 147/273 instances, and runs 5 or more rounds on
  30, 18 and 21 instances.

**Contraction regimes.** These use the known cutoff and the full trajectory.

- Round 1 tightens some bound on 241 of 339 instances.
- The trajectory reaches a fixed point after 1 round on 104 instances (nothing changes after round 1)
  and runs 5 or more rounds on 155.
- On the 149 instances with at least 4 rounds in which a variable moved, the median of `rho` over
  rounds 3–10 is:

  | median rho | ≤0.3 | 0.3–0.5 | 0.5–0.7 | 0.7–0.8 | 0.8–0.9 | 0.9–0.95 | >0.95 |
  |---|---|---|---|---|---|---|---|
  | instances | 16 | 18 | 9 | 2 | 12 | 13 | 79 |

Example trajectories:

- `waterund08`: `rho` = 0.35, 0.68, 0.77, 0.75, 0.80, 0.87, 0.92, … This is linear contraction that
  slows toward 1 as the box approaches the floor set by the cutoff slack.
- `ex5_2_2_case1`: `rho` = 0.84, 0.45, 0.72, 0.002. A slow first round is followed by collapse, so
  `theta`-rules stop too early here.
- `crudeoil_lee1_05`: 0.61, then 0.98–0.999 for 49 rounds. Many tiny moves; this is the crawl or stall
  case.

**Width versus cutoff slack.** This is a rough check of the `sqrt(epsilon)` floor. Take continuous
variables that converged under the known cutoff (width below 1% of the FBBT width). The two-point
exponent `log(w_realistic/w_known)/log(eps_realistic/1e-6)` has these per-instance medians:

- Gurobi cutoff, 13 instances: median 0.21, interquartile range 0.00–0.54;
- SCIP cutoff, 22 instances: median 0.49, interquartile range roughly 0.0–0.92.

Values near 0.5 (for example `pooling_adhya*stp`, `pooling_adhya1tp`) match the quadratic-growth
prediction. Values near 1 (`pooling_foulds2stp`, `st_fp8`, `waterund08`) match the sharp-minimum
prediction of Proposition 2. Values near 0 (`wastewater*`) mean the tightening does not come from the
cutoff. The sample is small, and each slope rests on only two points.

**Gauss–Seidel versus Jacobi** (known cutoff, 339 instances):

- Median rounds to the fixed point: 4 for both.
- Total LPs: 289,941 (GS) and 300,710 (Jacobi). Total time: 12,031 s and 12,053 s.
- After round 1, the GS box is smaller on 165 instances and the Jacobi box on 1.
- At the fixed point, the GS box is smaller on 16 instances and the Jacobi box on 5. The mean gap
  closed is 0.346 for both.

GS gains within a round, and both reach nearly the same limit.

**Filtering** (round 1, known cutoff):

- LPs: 25,712 with filtering and 87,443 without (3.4× fewer). Time: 5,277 s and 7,834 s.
- In Gauss–Seidel mode, filtering is a heuristic. It gives a slightly weaker box on 26 instances and a
  stronger one on 9. The mean gap closed is 0.236 with filtering and 0.239 without.

**Restriction** to moved variables and their partners: 105,878 LPs against 109,107 for the same number
of unrestricted rounds. It saves only 3%, because bilinear neighbourhoods cover almost all nonlinear
variables.

## 4. Solver-level results (`results/arm_tables.csv`, `results/final_outcomes.csv`)

### 4.1 All 339 instances

The unit is instance × seed (678 pairs; `known-fp` uses seed 0 only). "Time ×" is the SGM total-time
ratio to the default; "nodes ×" is the node ratio on pairs both solve. "Root gc" is the root gap
closed, relative to the default root bound.

| solver | arm | solved | SGM time (s) | time × | nodes × | root gc | mean OBBT+root time (s) |
|---|---|---|---|---|---|---|---|
| Gurobi | default | 640 | 2.37 | 1.00 | 1.00 | – | 0 |
| Gurobi | `OBBT=3` | 640 | 2.49 | 1.05 | 0.82 | 0.113 | 0 |
| Gurobi | control (root run + incumbent) | 642 | 2.57 | 1.08 | 1.05 | -0.009 | 0.5 |
| Gurobi | pipe-r1 | 637 | 3.11 | 1.31 | 0.99 | 0.089 | 14.2 |
| Gurobi | pipe-r5 | 638 | 3.40 | 1.44 | 0.83 | 0.164 | 17.6 |
| Gurobi | pipe-ad0.5 | 637 | 3.14 | 1.33 | 0.97 | 0.106 | 14.5 |
| Gurobi | pipe-ad0.8 | 637 | 3.23 | 1.37 | 0.90 | 0.131 | 15.3 |
| Gurobi | pipe-fp | 637 | 4.08 | 1.73 | 0.77 | 0.178 | 30.8 |
| Gurobi | known-fp (238 pairs) | 217 / 220 | 9.26 / 4.50 | 2.06 | 0.70 | 0.217 | 48.5 |
| SCIP | default | 575 | 7.18 | 1.00 | 1.00 | – | 0 |
| SCIP | control | 574 | 8.30 | 1.16 | 1.11 | 0.000 | 3.8 |
| SCIP | pipe-r1 | 570 | 8.67 | 1.21 | 1.05 | 0.064 | 16.2 |
| SCIP | pipe-r5 | 564 | 8.84 | 1.23 | 0.85 | 0.107 | 19.7 |
| SCIP | pipe-ad0.5 | 570 | 8.71 | 1.21 | 0.98 | 0.055 | 16.5 |
| SCIP | pipe-ad0.8 | 571 | 8.69 | 1.21 | 0.88 | 0.084 | 17.1 |
| SCIP | pipe-fp | 561 | 9.50 | 1.32 | 0.73 | 0.087 | 31.4 |
| SCIP | known-fp (273 pairs) | 220 / 221 | 15.1 / 12.3 | 1.23 | 0.55 | 0.105 | 43.1 |

Mean final gaps (with unsolved runs counted) are 0.010–0.012 for all Gurobi arms. For SCIP they are
0.045 (default) and 0.054–0.060 (pipelines): the OBBT time is taken out of the tree search on hard
instances.

The family-capped subset gives Gurobi time ratios of 1.25–1.56 and SCIP 1.14–1.25. The probe-pool
subset gives Gurobi 1.17–1.33 and SCIP 1.09–1.17. The order of the rules is the same in both.

### 4.2 Effect of the box alone (pipeline against control)

Both arms have the same root run and incumbent, so the comparison isolates the box. This is the
`ref = pipe-none` block of `arm_tables.csv`. On the instances where OBBT ran (Gurobi 238, SCIP 273):

| solver | rule | time × | nodes × | final-solve time × | solved (control) |
|---|---|---|---|---|---|
| Gurobi | r1 | 1.27 | 0.93 | 1.02 | 435 (440) |
| Gurobi | ad0.8 | 1.33 | 0.81 | 0.98 | 435 (440) |
| Gurobi | fp | 1.79 | 0.65 | 0.98 | 435 (440) |
| SCIP | r1 | 1.05 | 0.96 | 1.02 | 438 (442) |
| SCIP | ad0.8 | 1.06 | 0.77 | 1.00 | 439 (442) |
| SCIP | fp | 1.17 | 0.62 | 0.96 | 429 (442) |

The tightened box reduces nodes but not the time of the final solve (ratio about 1.0), and the OBBT
time is pure overhead.

Split by the McCormick-LP gap closed by the rule's box (pairs solved by both arms; node ratio and
final-solve time ratio against the control):

| solver, rule | gc ≥ 0.5 | 0 < gc < 0.5 | gc = 0 |
|---|---|---|---|
| Gurobi fp | 112 pairs: nodes 0.18, solve 0.87 (mean control time 4.9 s) | 98: 0.77, 0.95 (24 s) | 219: 0.96, 1.00 (27 s) |
| Gurobi ad0.8 | 86: 0.42, 0.89 (6.4 s) | 96: 0.84, 0.95 (22 s) | 247: 0.96, 1.00 (25 s) |
| SCIP fp | 142: 0.20, 0.65 (1.2 s) | 76: 0.83, 1.02 (50 s) | 198: 0.97, 1.00 (61 s) |
| SCIP ad0.8 | 108: 0.43, 0.81 (1.5 s) | 91: 0.75, 1.01 (50 s) | 223: 0.95, 1.01 (57 s) |

**Hard instances.** These have a default time of at least 10 s or are unsolved in some seed: 69
instances for Gurobi and 122 for SCIP. There the pipelines give:

- Gurobi: node ratios 0.99–1.02, time ratios 1.15–1.23, and 97–98 solved against 100;
- SCIP: node ratios 1.06–1.26, time ratios 1.27–1.51, and 127–137 solved against 141.

Gurobi's own `OBBT=3` is the best of the OBBT variants. It gives nodes 0.82× and time 1.05× overall,
the same solved count, and 1.01× time on hard instances. Its bound tightening is integrated into the
solver and needs no second root.

**Instance-level changes in solved status** (both seeds pooled):

- Gurobi: pipelines newly solve `tln7` (both seeds) and lose a few pairs to the OBBT time.
- SCIP pipelines:
  - newly solve `kall_diffcircles_9` (seed 1) and, with `ad0.8`, `waterund08` (seed 1);
  - lose `kall_circlespolygons_c1p12`, `kall_diffcircles_10`, `tln7` and `wastewater15m2` in some
    seeds.

### 4.3 Failures

- **SCIP "error in LP solver".** Three runs failed this way: `wastewater05m2` (pipe-r5 and pipe-fp,
  seed 1) and `wastewater02m2` (control, seed 0). They are counted as unsolved.
- **SCIP wrong optimal values.** There are two, both on `crudeoil_lee1_*` (see Section 1), and one of
  them is in the control arm.

Gurobi had no errors and no wrong answers.

## 5. Interpretation and what would change the conclusion

- The benefit of iterating OBBT is concentrated where the McCormick relaxation of the incumbent's
  neighbourhood tightens quickly (pooling, water networks, small `ex*`/`st_*` problems). These are
  instances that both solvers already solve in seconds. On the hard instances, OBBT from a root-level
  box changes almost nothing (gap closed is usually 0), whether iterated or not. This is consistent
  with the stall mechanism of Theorem 6 and the `sqrt(epsilon)` floor, and with the dominance of `rho`
  near 1 in the trajectories.
- An external presolve pays twice: a second root and the OBBT LPs. The control arm shows that the
  restart alone costs 1.08× (Gurobi) and 1.16× (SCIP). Integrated OBBT (Gurobi `OBBT=3`) avoids this
  and is close to neutral in time.
- The `theta`-rules do what the theory suggests. They stop when `rho` approaches 1 and run longer on the
  linearly contracting instances. Their OBBT time is close to one round's. The adaptive variant `ad0.8`
  has the best node ratio per unit of OBBT time among the realistic rules. It is still slower than the
  default because of the fixed cost of round 1 on large instances.
- Directions with some chance of a positive result:
  1. Skip OBBT when a cheap predictor says round 1 will be useless. On the 109 instances whose
     nonlinear variables are all integer, round 1 (with any of the three cutoffs) changed a bound on
     only 25 (mostly general-integer problems: `nvs*`, `ex126*`, `qspp*`, `tln*`). These instances
     account for 91% of all round-1 OBBT time (4,976 of 5,457 s summed over cutoffs). Skipping pure
     binary problems, or running round 1 on a sample of variables first, would remove most of the
     overhead.
  2. Run OBBT inside the solver after better incumbents are found, as the plan's re-trigger rule
     suggests: the floor scales with `sqrt(epsilon)`.
  3. Measure on a test set restricted to instances where the default needs more than 10 s. On that set
     here, no rule helped.

## 6. Files

- `code/qcqp.py`: OSiL parser, evaluation, FBBT, the Gurobi model and solution loading.
- `code/relax.py`: the McCormick LP with in-place updates, one OBBT round (GS or Jacobi, with
  filtering) and iterated OBBT with the stopping-rule snapshots.
- `code/solvers.py`: Gurobi and SCIP runs, including the root-bound capture.
- `code/pipeline.py`: stages `roots`, `obbt` and `final` (arms `base`, `obbt3`, `pipe`, `none`,
  `known`).
- `code/analysis.py`: the tables. `code/validate.py`: the box validity check.
- `results/instances.csv`: candidates, the scope decision and FBBT data.
- `results/roots.jsonl`: incumbent runs.
- `results/obbt.jsonl`: full trajectories.
- `results/final.jsonl`: all final solves.
- `results/obbt_summary.csv` and `results/obbt_rounds.csv`: OBBT-level tables.
- `results/final_outcomes.csv` and `results/arm_tables.csv`: solver-level tables.
- `results/validity.csv`: the validity check.
- `results/analysis_output.txt`: printed summary.
- `results/boxes/`, `results/fbbt/`, `results/roots_x/`, `results/final_x/`: boxes and solutions
  (`.npz` and `.npy`).

Verification actually run: the targeted scripts above on the full instance set. There is no CI check
for this experiment.
