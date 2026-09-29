# Branching-point parameters of SCIP 10 on nonconvex MINLPLib instances

Date: 2026-09-29. Status: empirical evidence from one solver version on a
57-instance MINLPLib subset, run on one machine. It is not a proof. Nothing
here has been independently reviewed.

Question: the theory notes predict that splitting closer to the relaxation
(LP) point, with less midpoint pull and less clamping, reduces node counts,
especially on instances with sharp or face-aligned optima. Does this hold for
SCIP 10 on real nonconvex MINLPLib instances? Theory sources:
[competitive-branching.md](../branching-competitiveness/competitive-branching.md)
(Theorem 1, Propositions 4 and 4'),
[face-exact-node-complexity.md](../spatial-face-exact/face-exact-node-complexity.md)
(Propositions 5.4–5.6, Theorem 5.3) and the synthetic SCIP validation in
[scip-node-exponents.md](../solver-validation/scip-node-exponents.md).

## Summary

On this benchmark the prediction does not hold as a general rule. The one
robust effect in the predicted direction is that pure midpoint splitting is
worse than the default. Moving the split to the LP point gives no reliable
gain, and removing the clamp does clear harm.

Node counts are shifted geometric means (shift 10) over 57 instances and 3
seeds, relative to SCIP's default rule (Section 3.3):

| Setting | Split rule | Nodes vs default | 95% CI | Wilcoxon p | Unsolved runs (of 171) |
|---|---|---|---|---|---|
| `lp` | LP point, clamp 0.2 | 1.03 | 0.83–1.26 | 0.18 | 5 |
| `lp_noclamp` | LP point, no clamp | 2.19 | 1.43–3.39 | <0.001 | 33 |
| `mix_noclamp` | default pull, no clamp | 1.35 | 1.03–1.85 | 0.75 | 17 |
| `mid` | midpoint | 1.15 | 1.03–1.28 | 0.009 | 2 |
| default | reference | 1 | | | 1 |

- **Seed noise is large.** Across three seeds, the median per-instance
  max/min node ratio under default is 1.51, and the 90th percentile is 5.65.
  Two seeds of the *same* setting differ by more than 10% on 42 of 57
  instances. Per-instance differences below about 2× cannot be told apart
  from seed noise on most instances (Section 3.2).
- **Why `clamp = 0` fails in SCIP.** On 11 of the 16 instances where
  `lp_noclamp` fails, the LP value of the branching variable sits on its
  domain bound in 42–100% of bounded continuous branchings. This includes
  nodes without an LP solution, where SCIP uses the pseudo-solution value, a
  bound.
  - Without the clamp, SCIP then splits about `1e-9 * max(1,|l|,|u|)` from
    the bound. The result is a chain of nearly identical nodes, with max
    depths in the thousands to tens of thousands.
  - On ex4_1_5, whose variables have infinite bounds, the tree is a single
    path: 378,210 nodes at depth 378,209.
  - The theory's exact-gap relaxations cannot produce this: their gap
    vanishes at the box endpoints, so a node whose relaxation minimizer is
    at an endpoint is pruned. SCIP's lifted LP relaxation has no such
    property (Section 4).
- **The default is already close to the LP point on most splits.** SCIP
  scales the midpoint pull by the local/global width ratio when the ratio is
  below 1/2. In the traces, a median of 70% of each instance's continuous
  splits happen at such widths.
- **Where the theory's direction shows.** On low-dimensional smooth
  polynomial problems the LP point wins clearly. The counts below are per
  seed.
  - mathopt5_4 (1 variable): `lp` 543/543/537 nodes against 31282/31297/31249
    for default and 18204/18474/18673 for `mid`.
  - prob09 (2 variables): `lp` about 1700 against about 4900 for default.
  - Both instances have optimum 0. SCIP accepts an incumbent at about −1e-6
    within the feasibility tolerance, so their trees close at a
    tolerance-set scale.
  - On the 19 continuous instances with at most 20 variables, `mid` needs
    1.43× the nodes of `lp` (CI 1.03–2.22, p = 0.036). Here `lp`/default is
    0.81, but that is not significant (CI 0.50–1.12).
- **Where it does not.** On larger instances the LP point can be much worse.
  - gsg_0001 (44 variables): default needs about 6000 nodes. `lp` hits the
    limit on two of three seeds, at 184,845 and 196,294 nodes, and needs
    141,397 on the third.
  - The LP values spread across the whole domain, and 42% of the `lp` splits
    land on the 20%/80% clamp.
  - The theory's positive result is one-dimensional. In `n >= 2`
    dimensions it is open.
- **Tolerance sweep (19 small continuous instances, seed 0).** The theory
  predicts that rules separate more as eps shrinks. The sweep does not show
  this beyond a single instance.
  - On the 13 instances solved by every setting at every tolerance,
    `lp`/default goes from 0.95 at `absgap = 1e-2 * |f*|` to 0.76 at SCIP's
    default gap 0.
  - That trend comes entirely from mathopt5_4. Without it, the ratio is
    0.95, 0.91, 0.90 and 1.04.
  - `mid`/`lp` stays between 1.5 and 1.8 with no trend (Section 3.5).
- **Optional settings (seed 0 only).** None differs from default beyond
  noise.
  - A Couenne-like point (LP weight 0.25, clamp 0.05): 1.01.
  - A constant 0.75 pull at all depths (`trig0`): 1.14, p = 0.046 on a
    single seed.
  - LP point with clamp 0.05 (`lp_c05`): 1.23. It avoids the no-clamp
    failures, with 57/57 solved.
- **Correctness.** 967 runs ended optimal. None reported a value worse than
  the MINLPLib best known by more than 2.2e-10 relative. No dual bound
  excluded a best known value by more than 1e-6.
  - Values *below* the best known are mostly within 1.4e-5 relative, which
    fits the 1e-6 feasibility tolerance.
  - There are two exceptions:
    - hs62 at −5e-5, within MINLPLib's own primal–dual gap;
    - hybriddynamic_varcc at −4.25e-4, the same in all 18 optimal runs, so
      it does not depend on the setting.
  - One run crashed with an LP solver error (wastewater05m2, `lp_noclamp`,
    seed 2).
- **Cost.** 1,927 recorded SCIP runs, plus 28 discarded trace runs and a
  few manual test runs. 5.6 CPU hours, single-threaded, at most 6 in
  parallel. Node counts are deterministic: 154/154 trace runs reproduced the
  main runs' node and LP-iteration counts exactly.

## 1. Predictions being tested

Write `lambda` for the weight on the LP (relaxation) point and `theta` for
the clamp, as in Proposition 4. The theory's predictions for each tested
rule, on a fixed sharp instance with `N_opt = 2` and tolerance eps, are:

| Setting | SCIP parameters | `(lambda, theta)` | Theory (1D sharp minimum; aligned McCormick kink) |
|---|---|---|---|
| `default` | midpull 0.75, midpullreldomtrig 0.5, clamp 0.2 | `(0.25, 0.2)` on nodes of at least half the global width; `(1 - 0.75 r, 0.2)` below, where `r` = local/global width | at least order `log(1/eps)` (Prop. 4'); numerically "between the two regimes" on aligned kinks (face-exact Section 5.3) |
| `lp` | midpull 0 | `(1, 0.2)` | order `log(1/eps)`, `kappa = 1/5` (Prop. 4); bounded except near a measure-zero set of kink positions (Prop. 5.4(c)) |
| `lp_noclamp` | midpull 0, clamp 0 | `(1, 0)` | below 4× optimal in 1D (Thm. 1); 3 nodes on the aligned-kink family (Prop. 5.4(b)) |
| `mix_noclamp` | clamp 0 | default pull, no clamp | numerically about `log log(1/eps)` on the Prop. 4' instance |
| `mid` | midpull 1, midpullreldomtrig 0 | `(0, ·)` | at least `c_n log(1/eps)` (Thm. 2); polynomial on aligned kinks (Thm. 5.3) |
| `trig0` | midpullreldomtrig 0 | `(0.25, 0.2)` at every depth | order `log(1/eps)` (Prop. 4) |
| `couenne` | midpull 0.75, midpullreldomtrig 0, clamp 0.05 | `(0.25, 0.05)` | order `log(1/eps)` (Prop. 4) |
| `lp_c05` | midpull 0, clamp 0.05 | `(1, 0.05)` | order `log(1/eps)` (Prop. 4, clip binding: `kappa = 0.05`) |

Scale of the predicted effects. On one sharp 1D minimizer, Proposition 4's
chain (`T >= 2K + 1`) adds `log(10) / log(1/kappa)` nodes per decade of eps. That is
about 1.4 nodes per decade for `lp` and 3.3 for bisection.

- Such additive losses are tiny next to trees of thousands of nodes and the
  seed noise measured below.
- Large effects are predicted only in two cases:
  - many sharp or aligned features combine;
  - oblivious rules meet face-aligned optimal sets, where the loss is
    polynomial in `1/eps`.

**Couenne's default.** The coordinator's note calls Couenne's default a
"midpoint weight 0.25 with clamp 0.05". This study follows the
repository's reading instead
([competitive-branching.md](../branching-competitiveness/competitive-branching.md)
§1.5; [competitive-review.md](../../reviews/competitive-review.md)). Under
that reading, `branch_midpoint_alpha = 0.25` weights the LP point:
`b = 0.25 x_LP + 0.75 mid`, clamp `closeToBounds = 0.05`. In SCIP terms
this is midpull 0.75 at every depth with clamp 0.05. The emulation omits
two things:

- Couenne's increase of alpha at small relative gaps;
- Couenne's own variable selection.

## 2. Setup

### 2.1 Software and hardware

- SCIP 10.0.2, with SoPlex 8.0.2 as LP solver and Ipopt 3.14.19 as NLP
  solver.
- PySCIPOpt 6.2.1 on Python 3.13.11.
- Linux 6.18 (WSL2), Intel Xeon w5-2565X with 36 logical CPUs.
- Details are in [`results/meta.json`](results/meta.json).

Each run is single-threaded, with OMP/OpenBLAS/MKL threads set to 1. At
most 6 runs ran in parallel. Other settings:

- `timing/clocktype = 1`: CPU time, so the time limits are CPU time.
- `limits/memory = 4000` MB.
- `display/verblevel = 0`.
- Everything else is SCIP's default, including `limits/gap = 0` and
  `limits/absgap = 0`.

### 2.2 How SCIP places the split

This section summarizes a reading of the SCIP 10.0.3 source: `branch.c`
(`SCIPbranchGetBranchingPoint`), `cons_nonlinear.c` and `branch_pscost.c`.
The runs used the 10.0.2 binary. No difference in these functions is
expected between the two versions, but this was not checked.

For a continuous variable with LP value `x`, local domain `[l, u]` and
global domain `[L, U]`:

```
r  = (u - l)/(U - L)                  (r = epsilon if L or U is infinite)
mu = midpull * (r if r < midpullreldomtrig else 1)
p  = mu (l+u)/2 + (1 - mu) x          (only if the node's LP was solved and l, u are finite)
p  = clip(p, l + clamp (u-l), u - clamp (u-l)),
     but at least 1.01*epsilon*max(1,|l|,|u|) away from both bounds
```

Details that matter for the interpretation:

- **Where midpull applies.** The pull is applied only when the node's LP
  was solved and the local domain is bounded.
  - For a variable with an infinite global bound, `r = epsilon`, so default
    SCIP already splits at the LP point, clamped.
  - For such variables `default` and `lp` coincide. This happens on
    ex4_1_5, for example.
- **The clamp has other jobs besides limiting the pull.**
  - At nodes whose LP was not solved (pseudo solutions), `cons_nonlinear`
    registers all unfixed variables of violated constraints as external
    candidates. The `pscost` rule then branches at the pseudo-solution
    value, which is a bound.
  - On half-infinite domains, SCIP guesses the missing bound and clamps.
  - In both cases, clamp 0 gives a split at the bound plus about 1e-9.
- **Tiny domains.** On domains narrower than about `2 epsilon` (relative),
  the point is the midpoint. The split bounds can then snap to the domain
  bounds. With clamp 0.2, a split within 1e-6 of a bound (relative
  position) is possible only on such tiny domains.
- **Variable selection changes too.** `cons_nonlinear` computes
  pseudocost scores at `SCIPgetBranchingPoint`. So these parameters also
  change which variable is chosen, not only where it is split.
- **Integer branching is unaffected.** Integer branching on fractional LP
  values does not use these parameters.

### 2.3 Benchmark selection

The local MINLPLib copy has 1632 OSiL files, not the 2085 the task
mentioned. Metadata comes from
`code/minlp_solver_lab/instances/instancedata.csv` (MINLPLib
`instancedata`, 1633 rows).

1. **Filter** ([`select_candidates.py`](select_candidates.py)). 486
   candidates remain after these exclusions:

   | Exclusion | Instances |
   |---|---|
   | convex flag True | 376 |
   | not solved in MINLPLib (no finite primal bound, or gap > 1e-4) | 524 |
   | no continuous variable in a nonlinear term | 138 |
   | more than 1000 variables or constraints | 108 |
   | no OSiL file | 1 |

   Instances with an empty convexity flag (undetermined) are kept. They are
   mostly nonconvex polynomials.
2. **Screen**: SCIP default, seed 0, 20 s CPU limit.
   - 360 solved to optimality, 125 hit the limit, and 1 failed (st_e35, "error
     in LP solver").
   - Of the 360: 287 took under 1 s, 221 needed under 50 nodes, and 67 took
     at least 1 s *and* at least 50 nodes.
   - The task suggested 1–120 s. The 20 s screen was a budget choice.
     Instances needing 20–120 s under default are therefore **not**
     represented.
3. **Family cap** ([`select_benchmark.py`](select_benchmark.py)).
   - At most 3 instances per name family. A family is the alphabetic
     prefix, with `exN_` kept separate and GLOBALLib/MacMINLP singletons
     (`st_`, `nvs`, `mathopt`, `prob`, `hs`, ...) treated as their own
     families.
   - Larger families were sampled with `random.Random(0)`.
   - Dropped: kall_circlesrectangles_c1r13, kall_congruentcircles_c51, _c62,
     _c63, _c72, kall_diffcircles_6, pooling_adhya1stp, pooling_bental5stp,
     sfacloc2_2_90 and sfacloc2_4_95.

Result: **57 instances** ([`selected.txt`](selected.txt)):

- Types: 18 NLP, 13 MBNLP, 12 QCP, 7 MBQCP, 2 MIQCP, 2 QP, 1 MBQCQP, 1 QCQP
  and 1 MINLP.
- 24 have integer or binary variables.
- Size: median 49 variables (range 1–936).
- Default screening time: median 3.3 s (range 1.0–19.3 s).
- Default nodes: median 2326 (range 59–79,035).

In the default seed-0 trace, 44 instances do at least half of their
branchings on continuous variables. Five do no continuous branching at all:

- carton7, carton9, portfol_robust100_09, portfol_shortfall050_68 and
  sfacloc2_3_95.
- The first four give identical node counts in every setting for each seed.

### 2.4 Runs

- **Main.** 5 core settings (`default`, `lp`, `lp_noclamp`, `mix_noclamp`,
  `mid`) × 3 seeds × 57 instances. That is 855 runs, with a 120 s CPU limit
  (6× the largest default screening time).
- **Seeds.**
  - Seed 0 is SCIP's default.
  - Seed `k = 1, 2` sets `randomization/permutationseed = k`,
    `randomization/permutevars = TRUE` and
    `randomization/randomseedshift = k`. This permutes constraints and
    variables and shifts all random seeds, including the LP seed.
- **Optional, seed 0 only.**
  - `trig0`, `couenne` and `lp_c05` on all 57 instances (171 runs, 120 s).
  - An absolute-gap sweep on the 19 instances with no integer variables and
    at most 20 variables. Settings `default`, `lp`, `lp_noclamp`, `mid`,
    with `limits/absgap = delta * max(1, |MINLPLib primal bound|)` for
    `delta` in {1e-2, 1e-4, 1e-6}. 228 runs, 60 s limit.
- **Traces (diagnostic, seed 0, 30 s limit).**
  - `default`, `lp` and `lp_noclamp` on all 57 instances (171 runs).
  - A re-trace of the 16 instances with an `lp_noclamp` failure, with one
    extra counter.
  - A `NODEBRANCHED` event handler records the relative split position, the
    relative LP position, and whether the domain has an infinite bound or a
    width ratio below 1/2.
  - The handler does not change the search: node and LP-iteration counts
    matched the main runs in all 154 comparable pairs.

Measures per run: status, total nodes (`getNTotalNodes`), solving time,
primal and dual bounds, gap, LP iterations, max depth, and branching counts
by origin from the statistics. Aggregates:

- Per instance, a shifted geometric mean over seeds.
- Across instances, a shifted geometric mean (shift 10 nodes / 1 s).
- Unsolved runs enter with their node count at the limit, which
  underestimates their true count, and with time equal to the limit.
- The 95% CI is a bootstrap over instances. The p-value is a two-sided
  Wilcoxon signed-rank test on per-instance log ratios.
- A "win" or "loss" is a per-instance ratio beyond 10%.
- A "separated" instance is one where all 3 seeds of one setting lie beyond
  all 3 of the other by more than 10%. Without the margin, chance alone
  separates a given direction with probability 1/20.

### 2.5 Commands

All commands were run in `research-20260928b/bb-complexity/minlplib-branching/`:

```
python3 select_candidates.py                                    # candidates.csv, screen_jobs.txt
python3 runner.py screen_jobs.txt results/screen.jsonl --jobs 6
python3 select_benchmark.py                                     # selected.txt, main/trace/optional job files
python3 runner.py main_jobs.txt results/runs.jsonl --jobs 6
python3 runner.py trace_jobs.txt results/trace.jsonl --jobs 6
python3 runner.py optional_jobs.txt results/runs.jsonl --jobs 6
python3 runner.py trace2_jobs.txt results/trace2.jsonl --jobs 6 # lp_noclamp failures (list below)
python3 features.py                                             # results/features.json
python3 analyze.py                                              # results/summary.md
```

One run is `python3 run_one.py INSTANCE SETTING SEED TIMELIMIT [--trace]`.
The settings dictionary is in [`run_one.py`](run_one.py).

`trace2_jobs.txt` lists every instance with a non-optimal `lp_noclamp` run,
as `INSTANCE lp_noclamp 0 30 --trace`.

Provenance notes:

- The first trace batch was stopped and rerun. The runner had overwritten
  each record's trace summary with a boolean flag, and the 28 affected
  records were discarded.
- The main-run records were rewritten once to rename that flag to `traced`.
  No values changed.

Checks run: only targeted runs of these scripts. No project-wide checks
were run, and no CI results are involved.

## 3. Results

Full tables are in [`results/summary.md`](results/summary.md), generated
from [`results/runs.jsonl`](results/runs.jsonl),
[`results/trace.jsonl`](results/trace.jsonl) and
[`results/trace2.jsonl`](results/trace2.jsonl).

### 3.1 Status and correctness

| Setting | Runs | Optimal | Time limit | Other |
|---|---|---|---|---|
| default | 171 | 170 | 1 (oil2, seed 2) | |
| lp | 171 | 166 | 5 | |
| lp_noclamp | 171 | 138 | 32 | 1 crash (LP solver error) |
| mix_noclamp | 171 | 154 | 17 | |
| mid | 171 | 169 | 2 | |
| trig0 / couenne / lp_c05 (seed 0) | 57 each | 56 / 57 / 57 | 1 / 0 / 0 | |

- **Objective values.** All 967 optimal runs of these settings were
  compared with the MINLPLib best known value.
  - No primal value is worse than the best known by more than 2.2e-10
    relative.
  - Twelve instances end *below* the best known.
  - For ten of them the deviation lies between −2.7e-7 and −1.4e-5
    relative. This fits SCIP accepting points that violate constraints by up
    to the feasibility tolerance 1e-6.
  - hs62 is at −5e-5. That is within MINLPLib's own primal–dual gap for the
    instance.
  - hybriddynamic_varcc is at −4.25e-4 in all 18 optimal runs, which looks
    tolerance-related: MINLPLib reports primal = dual = 1.536415161.
  - These deviations do not depend on the branching setting.
- **Dual bounds.** No dual bound excludes the best known value by more than
  1e-6.
- **Zero-optimum instances.** The objective of mathopt5_4 and prob09 is a
  sum of squares with optimum 0. Every setting ends "optimal" at about
  −9.7e-7, with a solution found by the `relaxation` heuristic that violates
  a constraint by less than 1e-6. Their trees therefore close at the
  tolerance scale.

### 3.2 Seed variability

- **Spread across seeds.** Per instance, the max/min node ratio over the
  three seeds has these quantiles:

  | Setting | Median | 75th percentile | 90th percentile |
  |---|---|---|---|
  | default | 1.51 | 2.04 | 5.65 |
  | lp | 1.34 | 1.89 | 4.09 |
  | mid | 1.45 | 1.83 | 3.21 |

  About 80–85% of instances vary by more than 10%.
- **Null comparison.** Comparing default seed 1 with default seed 0 gives 19
  "wins" and 23 "losses" beyond 10%, with an aggregate ratio of 0.999. Seed
  2 against seed 0 gives 19 and 19, with ratio 1.021. The win/loss counts
  in Section 3.3 must be read against this baseline.
- **Extreme cases.**
  - ex14_1_7: seeds 1 and 2 solve at the root (1 node) in every setting,
    while seed 0 needs 167–26262 nodes.
  - st_e03 default: 79035, 54205 and 1063341 nodes.
  - kall_circlespolygons_c1p13 default: 7859, 93484 and 99477 nodes.

### 3.3 Aggregate comparison

The baseline is default, averaged over the same seeds as each setting.

| Setting | Seeds | Inst. | Solved runs | Nodes ratio | 95% CI | p | Wins / losses | Separated wins / losses | Time ratio |
|---|---|---|---|---|---|---|---|---|---|
| lp | 0–2 | 57 | 166/171 | 1.033 | 0.83–1.26 | 0.18 | 13 / 22 | 4 / 5 | 1.09 |
| lp_noclamp | 0–2 | 57 | 138/171 | 2.185 | 1.43–3.39 | <0.001 | 11 / 32 | 5 / 19 | 1.96 |
| mix_noclamp | 0–2 | 57 | 154/171 | 1.348 | 1.03–1.85 | 0.75 | 9 / 14 | 2 / 7 | 1.37 |
| mid | 0–2 | 57 | 169/171 | 1.150 | 1.03–1.28 | 0.009 | 12 / 30 | 5 / 8 | 1.09 |
| trig0 | 0 | 57 | 56/57 | 1.139 | 0.96–1.41 | 0.046 | 12 / 23 | – | 0.97 |
| couenne | 0 | 57 | 57/57 | 1.014 | 0.90–1.13 | 0.14 | 12 / 20 | – | 0.94 |
| lp_c05 | 0 | 57 | 57/57 | 1.225 | 0.92–1.61 | 0.087 | 14 / 27 | – | 1.18 |

- **Restricted to instances where every run of both settings solved.**
  `lp` 0.95 (0.78–1.10, 53 instances), `lp_noclamp` 1.08 (0.81–1.40, 41),
  `mix_noclamp` 1.00 (49), and `mid` 1.15 (1.03–1.29, p = 0.011, 55).
  - The no-clamp penalty therefore comes from its failures.
  - Excluding the failures makes `lp_noclamp` look neutral, but that is a
    selection effect.
- **Restricted to the 44 instances where at least half the default
  branchings are continuous.** The same pattern holds, slightly amplified:
  `lp` 1.04, `lp_noclamp` 2.73, `mix_noclamp` 1.48, and `mid` 1.19
  (1.04–1.36, p = 0.013).
- **`mix_noclamp`.** Its CI excludes 1 but its Wilcoxon p is 0.75. Most
  instances are unchanged, and a few blow up: ann_peaks_exp, ex4_1_5,
  ex6_2_8, ex8_5_3, kriging_peaks-full010 and oil2.
- **Separated counts.** Every setting exceeds the exchangeable-seed
  expectation of about 2.9 separated instances per direction. Any parameter
  change alters the search path, so separation is common. The asymmetry is
  what matters:
  - `lp` is balanced, at 4 wins against 5 losses.
  - `mid` is mildly unbalanced, at 5 against 8.
  - `lp_noclamp` (5 against 19) and `mix_noclamp` (2 against 7) are clearly
    unbalanced.

### 3.4 Where the differences come from

**(a) The clamp guards against uninformative LP points.** In the `lp`
trace, the LP value of the branching variable lies on its local bound in at
least 10% of bounded continuous branchings on 10 of the 50 instances with at
least 10 such branchings. The per-instance median is 0.

On the 16 instances with an `lp_noclamp` failure, the re-trace (seed 0,
30 s) shows:

| Instance | Status | Max depth | Branchings | LP value on bound | Split at bound, wide domain |
|---|---|---|---|---|---|
| ex4_1_5 | limit | 102572 (= nodes − 1) | 102572 on half-infinite domains | – | – |
| hs62 | limit | 7773 | 95716 | 85% | 85% |
| inscribedsquare03 | limit | 6889 | 98216 | 94% | 94% |
| supplychainp1_030510 | limit | 1181 | 35304 | 91% | 90% |
| wastewater05m1 | limit | 8452 | 12932 | 69% | 69% |
| oil2 | limit | 1025 | 1943 | 60% | 60% |
| ann_peaks_exp | limit | 398 | 903 | 42% | 42% |
| ex8_5_3 | limit | 859 | 140550 | 100% | 0% (narrow domains) |
| kriging_peaks-full010 | limit | 17232 | 26170 | 99% | 0% |
| ex6_2_8 | limit | 19399 | 31263 | 62% | 0% |
| st_e03 | limit | 780 | 112783 | 84% | 0% |
| wastewater05m2 | optimal | 71 | 5786 | 15% | 3% |
| kall_circlespolygons_c1p13, kall_diffcircles_7, powerflow0009r, wastewater15m1 | limit or optimal | 34–1976 | 7820–31910 | 0% | 0% |

"Wide domain" means wider than `1e-6 max(1,|l|,|u|)`. With clamp 0 and the
LP value on the bound, the split is `1.01e-9 max(1,|l|,|u|)` from the bound.
On narrower domains this is not within 1e-6 in relative position, but the
child is still only about 1e-9 wide, and the depths show the same chains.

Some of these branchings happen at nodes without an LP solution. There the
recorded "LP value" is the pseudo-solution value, which is a bound by
construction.

- In the seed-0 `lp_noclamp` runs, `cons_nonlinear` enforced pseudo
  solutions 2011 times on ann_peaks_exp, 3167 times on oil2 and 15576 times
  on wastewater05m1. Under default the counts were 5, 15 and 0.
- On ex4_1_5, all 378,210 branchings went through the external-candidate
  (`pscost`) path.

The last row has no LP-at-bound branchings. There the no-clamp trees are
simply larger:

- In kall_diffcircles_7, about 54% of the LP values lie in the lowest fifth
  of the domain.
- Without a clamp the splits are very unbalanced, and nodes rise about 10×.

The theory's rules never face these situations (Section 4).

**(b) Unbalanced LP-point splits in higher dimensions.** gsg_0001 has 44
continuous variables, power terms and no LP-at-bound branchings. Default
needs 5761, 7209 and 6811 nodes. `lp` needs 184,845 (limit), 141,397 and
196,294 (limit).

- Under `lp`, LP values are spread over the whole domain, and 42% of splits
  sit exactly at the 20% or 80% clamp.
- Default's pull keeps early splits central, and `mid` is best here with
  about 4000 nodes.
- nous1 is a milder case: `lp` 4631/4251/4349 against default
  2642/1457/2705, all seeds separated.
- These are n-dimensional effects outside Theorem 1.

**(c) Low-dimensional smooth problems favor the LP point.** Node counts per
seed:

| Instance (variables) | default | lp | lp_noclamp | mix_noclamp | mid |
|---|---|---|---|---|---|
| mathopt5_4 (1) | 31282/31297/31249 | 543/543/537 | 543/543/541 | 37374/37372/37376 | 18204/18474/18673 |
| prob09 (2) | 4906/4933/4953 | 1730/1736/1701 | 1782/1811/1764 | 4037/4026/4037 | 5128/5126/4919 |
| rbrock (2) | 3223/3125/3075 | 2986/2982/2868 | 2495/2578/2571 | 2887/2852/2586 | 6302/5632/6204 |
| house (8) | 59492/58911/58472 | 58327/58335/58351 | 59407/58991/59419 | 58218/58055/57809 | 88051/88894/87283 |

The seed spread is small on these instances, so the differences are real
for SCIP 10.

- On mathopt5_4, the default trace shows 98% of branchings with the LP value
  on the node bound. 49% of splits land on domains narrower than about 1e-8,
  near `x = 1.00003`.
  - Default and `mix_noclamp` spend most of their nodes there, at the
    numerical resolution.
  - `lp` never reaches that regime.
- Direct inspection of events on mathopt5_4 confirmed that these are
  tiny-domain splits, not clamp failures.
- Both mathopt5_4 and prob09 are zero-optimum, tolerance-closed instances
  (Section 3.1).

### 3.5 Absolute-gap sweep

Setup: seed 0; `limits/absgap = delta * max(1, |f*|)`. `delta = 0` is the
main run, with gap limits 0 and a 120 s limit. Nodes are shifted geometric
means; mathopt5_4, prob09, rbrock and house are among the instances.

Over the 13 instances that every setting solved at every delta:

| delta | default | lp | lp_noclamp | mid | lp/default | lp_noclamp/default | mid/default | mid/lp |
|---|---|---|---|---|---|---|---|---|
| 1e-2 | 559 | 530 | 485 | 898 | 0.95 | 0.87 | 1.60 | 1.68 |
| 1e-4 | 1510 | 1293 | 1083 | 2123 | 0.86 | 0.72 | 1.40 | 1.64 |
| 1e-6 | 2463 | 2071 | 1803 | 3738 | 0.84 | 0.73 | 1.52 | 1.80 |
| 0 | 5110 | 3891 | 4056 | 6641 | 0.76 | 0.79 | 1.30 | 1.70 |

- **Advantage of `lp` over default.** Its apparent growth as the tolerance
  tightens comes from one instance.
  - mathopt5_4: default rises from 1391 nodes at 1e-6 to 31282 at gap 0,
    while `lp` stays near 540.
  - Without mathopt5_4, `lp`/default is 0.95, 0.91, 0.90 and 1.04 at
    `delta` = 1e-2, 1e-4, 1e-6 and 0.
  - st_e03 moves the other way at gap 0: default goes 4461 → 79035 and
    `lp` goes 1721 → 167093. This instance is very seed-sensitive.
  - Without both instances, the ratio stays at 0.93–0.98.
  - So the predicted growth with `log(1/eps)` is not visible beyond
    mathopt5_4.
- **`mid` against `lp`.** `mid` stays 1.6–1.8× worse at every delta, or
  1.3–1.7× without mathopt5_4, with no clear growth.
- **`lp_noclamp`.** It looks best here, but this subset excludes the 6
  instances where it fails at some delta (ex4_1_5, ex6_2_8, ex8_5_3, hs62,
  inscribedsquare03 and kall_diffcircles_7). Over all 19 instances its
  ratio to default is 1.9–2.9.
- **With 3 seeds.** At delta = 0, the 3-seed values on the same 13
  instances are `lp`/default 0.73, `mid`/`lp` 1.57 and
  `lp_noclamp`/default 0.85.

### 3.6 Instance characteristics

The table gives the median and shifted geometric mean of per-instance node
ratios against default, over seeds, by group. "Yes / no" means instances
with and without the characteristic.

| Characteristic (yes / no) | Inst. | lp | lp_noclamp | mid |
|---|---|---|---|---|
| LP value on a bound in ≥10% of `lp` branchings | 10 / 40 | 1.09, 0.93 / 1.04, 1.08 | 3.17, 6.21 / 1.49, 1.96 | 1.09, 1.13 / 1.17, 1.18 |
| ≥50% of branchings continuous | 44 / 13 | 1.07, 1.04 / 1.00, 1.00 | 1.70, 2.73 / 1.01, 1.02 | 1.18, 1.19 / 1.00, 1.02 |
| ≥50% of nonlinear continuous variables at a bound in the optimum | 11 / 46 | 1.02, 1.01 / 1.01, 1.04 | 1.32, 1.18 / 1.52, 2.53 | 1.19, 1.21 / 1.07, 1.14 |
| nonlinear variable with an infinite bound | 23 / 34 | 1.01, 1.05 / 1.05, 1.02 | 1.59, 2.88 / 1.26, 1.81 | 1.00, 1.17 / 1.17, 1.14 |
| integer or binary variables | 24 / 33 | 1.02, 1.03 / 1.01, 1.03 | 1.03, 1.63 / 1.75, 2.71 | 1.11, 1.18 / 1.10, 1.13 |
| only quadratic nonlinearities | 25 / 32 | 1.00, 1.13 / 1.02, 0.96 | 1.21, 1.63 / 1.56, 2.74 | 1.00, 1.14 / 1.11, 1.16 |

- **LP value on a bound.** This is the strongest association, and it is
  mechanistic: see Section 3.4(a).
- **Many optimal variables at bounds.** This is a rough proxy for
  face-aligned optima. These instances show a larger `mid` penalty (1.21)
  and a smaller no-clamp penalty. The direction matches the face-exact
  theory, but the evidence is weak: 11 instances, with overlapping
  distributions.
- **Kinks.** Only 2 instances contain `abs`: inscribedsquare03 and oil2.
  Both fail badly under `lp_noclamp`, through the LP-at-bound mechanism.
  Sharp or kink structure as the theory means it (Propositions 4 and 5.4)
  could not be tested on this benchmark.
- **Bilinear terms** (`bil` in the summary tables) show no consistent
  association.

## 4. Interpretation

- **What agrees with the theory.**
  - Relaxation information beats oblivious splitting. Pure midpoint is the
    worst clamped rule overall: 1.15× default, p = 0.009, and 1.43× `lp` on
    small continuous instances.
  - On one- and two-variable smooth problems, splitting at the LP point is
    much better than the default.
  - The advantage grows with a tighter tolerance only on mathopt5_4. The
    sweep shows no general growth with `log(1/eps)`.
  - The theory predicts only small additive losses per sharp feature.
    Aggregate effects of tens of percent do not conflict with it.
- **Why the default is hard to beat.**
  - Default SCIP is already close to an LP-point rule on most splits.
    - Once the width ratio `r` falls below 1/2, the pull is `0.75 r`, below
      0.375, and it shrinks further as `r` falls.
    - For variables with infinite global bounds the pull is essentially
      zero.
    - The full pull of 0.75 remains only on early, wide splits, where it
      keeps the tree balanced.
  - The theory's claim that "the clamp hurts" (Proposition 4') concerns
    sharp minimizers near node boundaries, and the predicted loss is a few
    nodes per decade of eps.
  - In SCIP, the clamp's main job is different: it is the only fallback
    when the LP point carries no information.
- **Assumptions of the theory that SCIP violates.**
  1. **Exact-gap relaxations vanish at box endpoints.** A node whose
     relaxation minimizer is at an endpoint is therefore pruned, and the
     pure minimizer rule never makes a degenerate split. SCIP relaxes a
     lifted formulation (auxiliary variables with separately relaxed terms,
     cut-based outer approximations). Its LP value for the chosen variable
     is often on the bound while the node stays open: 42–100% of branchings
     on the failing instances.
  2. **The branching variable is fixed (1D) or chosen by the rule.** SCIP
     chooses by violation and pseudocost scores, and the scores themselves
     depend on the branching point.
  3. **No pseudo-solution nodes and no unbounded domains.** SCIP has both.
     For example, ex4_1_5 under default enforces 1889 pseudo solutions and
     makes 4928 external-candidate branchings. At such nodes the clamp is
     the only safeguard.
  4. **Incumbent and tolerance model.** On zero-optimum instances, SCIP's
     incumbent sits about 1e-6 below `f*`, and the tree is closed at the
     numerical resolution.
- **The n-dimensional question.** Theorem 1 is one-dimensional, and the
  `n >= 2` case is open in the theory note. gsg_0001 and nous1 are
  real-instance examples where the relaxation-point rule, even with a
  clamp, is clearly worse than a midpoint-pulled rule.
- **Implication for solver rules.** A fair test of a pure
  relaxation-point rule in SCIP would need one of two things:
  - a fallback that triggers only when the LP value is on (or within
    epsilon of) the bound, or when the node has no LP solution;
  - variable selection that prefers variables with an interior LP value.

  Neither is available as a parameter. A custom branching rule (for
  example with `constraints/nonlinear/branching/external = TRUE` and a
  PySCIPOpt `branchexecext`) would be the next experiment. It would also
  change variable selection.

## 5. Limitations

- **Benchmark.** 57 instances whose default solving time is 1–20 s. The
  screen used 20 s, not 120 s, so harder instances with larger trees are
  missing. The family cap and the MINLPLib "solved" filter also shape the
  set. Results may differ for harder instances and for other solvers.
- **Seeds.** Three seeds for the core settings; seed 0 only for `trig0`,
  `couenne`, `lp_c05` and the sweep. Seed noise dominates most
  per-instance differences, so single-seed conclusions are weak.
- **Time limits.** Unsolved runs enter with their node count at the limit
  (120 s; 60 s in the sweep). This understates the losses of the failing
  settings. The sweep's delta = 0 runs had a longer limit than the other
  deltas.
- **Confounding with variable selection.** The parameters change both the
  split point and the pseudocost scores, and therefore variable selection.
  The study cannot separate the two.
- **Emulation.** The Couenne-like setting reproduces only Couenne's point
  rule, not its alpha schedule or its variable selection.
- **Tolerances.** Two of the clearest wins for the LP point (mathopt5_4 and
  prob09) are zero-optimum instances closed at the tolerance scale.
  MINLPLib best known values were the reference for the objective checks.
- **Time measurements.** With 6 runs in parallel, times are noisier than
  node counts. Node counts are deterministic.
- **Source version.** The split-point code was read in the 10.0.3 source,
  while the runs used the 10.0.2 binary.

## 6. Files

| File | Content |
|---|---|
| [`run_one.py`](run_one.py) | one SCIP run; settings; statistics parser; branching trace handler |
| [`runner.py`](runner.py) | parallel runner (at most 6), resumable, appends JSONL |
| [`select_candidates.py`](select_candidates.py), [`candidates.csv`](candidates.csv) | metadata filter and the 486 candidates |
| [`select_benchmark.py`](select_benchmark.py), [`selected.txt`](selected.txt) | screening criteria, family cap, job files |
| `*_jobs.txt` | job lists (screen, main, trace, optional and sweep, trace2) |
| [`features.py`](features.py), [`results/features.json`](results/features.json) | structural features and share of optimal variables at a bound |
| [`analyze.py`](analyze.py), [`results/summary.md`](results/summary.md) | all tables, including per-instance node counts for every seed |
| [`results/screen.jsonl`](results/screen.jsonl) | 486 screening runs |
| [`results/runs.jsonl`](results/runs.jsonl) | 1254 main, optional and sweep runs |
| [`results/trace.jsonl`](results/trace.jsonl), [`results/trace2.jsonl`](results/trace2.jsonl) | diagnostic trace runs |
| [`results/sols/`](results/sols/) | default seed-0 solutions (used for the share at a bound) |
| [`results/meta.json`](results/meta.json) | versions and run conditions |
