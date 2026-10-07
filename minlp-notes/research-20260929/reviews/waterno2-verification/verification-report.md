# Independent verification: waterno2 period-decomposition bounds

Date: 2026-09-30. Verifier: independent reviewer (did not produce the results).
Claims reviewed: `open-instances-wave2/waterno2/report.md` and its code/logs.
All verifier code and logs are in this directory
(`research-20260929/reviews/waterno2-verification/`). Nothing under
`open-instances-wave2/waterno2/` was edited; its scripts were only run
read-only (with `PYTHONDONTWRITEBYTECODE=1`).

## Summary of verdicts

| item | claim | verdict |
|---|---|---|
| 1 | Period structure: T × (166 vars, 9 binaries, 203 rows), 3(T−1) link rows, one horizon row | **Confirmed** for T ∈ {1,2,3,4,6,9,12,18,24} by a different recovery rule; partition identical to the authors'. |
| 2 | Lagrangian bound μ·c + Σ φ_t is valid; implied bounds are valid | **Confirmed.** Signs and horizon-row direction are right. Every implied bound in `implied_TT.json` (T = 6…24) is reproduced or beaten by the verifier's exact FBBT + exact-OBBT; tank-3 bounds also proved by hand. |
| 3 | `rbb.py` is a rigorous B&B; the waterno2_06 bound is 263.735099441 | **Confirmed** (no validity error found). All six periods of waterno2_06 were re-certified to the authors' exact per-period values with the verifier's own exact-rational B&B (periods 1–3 with the verifier's own implied bounds), so 263.735099441 is independently reproduced. One period each of waterno2_09 and waterno2_24 was also re-certified. Exact sums reproduced for all T. |
| 4 | SCIP 10.0.2 reports `optimal` 1.0–2.4 above feasible points | **Confirmed, and strengthened**: the cheaper points were repaired to **exactly feasible rational points**; SCIP's own `checkSol` accepts the original points; tighter tolerances do not remove the error. It is a genuine wrong answer (node-level domain reduction), not a tolerance effect; presolve is not the cause. |
| 5 | Primal points 09–24 feasible to ≤ 4.4e-9 | **Confirmed** (exact rational evaluation, independent evaluator). |
| 6 | MINLPLib listed bounds | **Confirmed** (pages fetched 2026-09-30). |

## 1. Structure

**Verdict: confirmed.**

Method (`vstruct.py`, log `logs/vstruct.log`). The OSIL files are read with
`osilx.py`. I checked that no OSIL file has a `constant=` attribute
(`grep -c 'constant='` gives 0 for all nine files) and that `osilx` records
objective and row constants (it does; `vstruct.analyse` asserts they are "0").
The recovery rule differs from `wmodel.partition`:

1. Remove the horizon row and **all** copy rows (−x_a + x_b = 0, both bounds 0),
   not only those between tank-balance variables.
2. The remaining rows give exactly T "cores" of 165 variables plus T singleton
   variables.
3. Each copy row is then classified by the atoms of its two variables:
   inside a core, core-to-singleton (attaches the singleton to its period),
   or core-to-core (a link row).

Results, for T ∈ {1, 2, 3, 4, 6, 9, 12, 18, 24}:

- every period has 166 variables, 9 binaries, 9 objective (cost) variables
  and 203 rows;
- there are exactly 3 link rows per transition, 3(T−1) in total; all have the
  form −x_end(t) + x_start(t+1) = 0;
- there is exactly one horizon row; all other rows lie inside one period;
- the periods form a chain; period 0 has 4 fixed variables (3 initial levels
  and x446 = 49), the others 1;
- compared with waterno2_01's single period (row signatures up to variable
  renaming), period 0 is identical and later periods differ in 2 signature
  entries (the demand row) or 20 (demand plus the 9 cost rows with a
  different energy price) — matching the report's description.

waterno2_06: link rows e111–e125 (e111: −x243 + x244 = 0), horizon row
e56: x188 + … + x193 ≥ 1.752499999 (= sum of the six demands).

The authors' partition (`wmodel.structure`) gives identical period variable
sets, identical period row sets and the same link order for T = 6, 9, 12,
18, 24 (`logs/compare_partition.log`).

## 2. Validity of the Lagrangian bound

**Verdict: confirmed.**

For any feasible x of the full problem: link rows give −x_end(t,k) +
x_start(t+1,k) = 0, and the horizon row (lb = 1.752499999, ub = INF, i.e. a ≥ row)
gives c − Σ_t h_t ≤ 0. For any real λ and μ ≥ 0,

f(x) ≥ f(x) + Σ λ_{t,k}(−x_end(t,k) + x_start(t+1,k)) + μ(c − Σ h_t)
     = μc + Σ_t [period-t Lagrangian of x] ≥ μc + Σ_t φ_t(λ, μ).

Checks:

- Signs in code (`rbb.Window.objective`, `period.window_objective`):
  −λ on the end level in period t, +λ on the start level in period t+1,
  −μ on each horizon variable, +μc added once. Correct.
- μ ≥ 0 is asserted in `certify.py` and again in my `vsum.py`.
- My own objective builder (`vmodel.period_objective`) gives exactly the
  same coefficients as `rbb.Window.objective` for all periods of T = 6 and
  T = 24 at the certificate multipliers (`logs/compare_objective.log`).
- The objective is exactly Σ (9T cost variables, coefficient 1), constant 0.

**Implied bounds.** Adding bounds that hold for every feasible point of the
full problem does not change its optimum, so the Lagrangian of the tightened
problem is still a valid bound.

*Hand proof of the tank-3 lower bounds (waterno2_06).* Row e105 of period 0
reads 3600·x224 − 3600·x236 + 1600·x266 − 1600·x267 = 0, with x236 = 0.296666667
(row e81), x224 ∈ [0, 5] and x266 = 4 (fixed). Hence
x267 = 4 + 2.25(x224 − 0.296666667) ≥ 4 − 0.66750000075 = 3.33249999925.
The link row e121 gives x268 = x267. The same row type in periods 1 and 2
(demands 0.294444444 and 0.283888889) gives x269 ≥ 2.67000000025 and
x271 ≥ 2.03125 exactly, with x270 = x269 and x272 = x271. One more step would
give 1.4075, below the OSIL bound 2, so the chain stops. The authors' values
(3.3324999992334576, 3.332499999218251, 2.6700000002022537,
2.670000000187582, 2.0312499999222715, 2.0312499999082383) are all at or
below these exact bounds.

*Machine proof of all implied bounds* (`vimplied.py`, logs
`logs/vimplied_TT.log`): exact-rational FBBT on the full model (all period
rows and link rows; the horizon row is left out, which only weakens it),
followed by OBBT whose bounds are computed exactly (Neumaier–Shcherbina with
Fraction arithmetic over the verifier's relaxation). A bound of theirs counts
as confirmed when my rigorous bound is at least as tight.

| T | implied bounds tighter than OSIL | reached by exact FBBT | confirmed after exact OBBT |
|---|---|---|---|
| 6 | 74 (tank-3 levels and flow/speed upper bounds) | 4 | 74 (2 rounds) |
| 9, 12, 18 | 6 each | 4 | 6 |
| 24 | 8 (incl. L3 ≥ 2.30422718658 at the start of period 23) | 4 | 8 |

The upper bound 5.9361972377 on x267/x268 depends on the pump curves
(station-D flow ≤ 1.15719877; my bound 1.1571987726234374 ≤ theirs
1.1571987726813557), so it is proved by OBBT, not by the hand argument.

## 3. The per-period bounding code `rbb.py`

### 3.1 Code review

**Verdict: no validity error found.** Points checked:

- *Data enclosure.* `dec_iv` uses the correctly rounded `float(s)`, which is
  exact or widened by one ulp each way. Variable bounds are widened the same
  way. Implied bounds are floats read back exactly from JSON.
- *FBBT.*
  - Row propagation uses interval products (`imul` rounds min/max outward).
    Infinite terms are counted separately. Each float sum gets the margin
    `MARG = 1e-12`·Σ|terms|, far above the (n−1)·2⁻⁵³ bound for these row sizes.
  - Square backward uses `sqrt`, rounded one ulp outward.
  - Cube backward is accepted only after an outward-rounded re-cubing check.
  - Bilinear backward divides only by strictly positive intervals.
  - Binary rounding `ceil(lo − 1e-9)`, `floor(hi + 1e-9)` only rounds inward
    when the proven bound excludes the other value (a lower bound of 1e-10
    stays 0).
  - Emptiness is declared only when lo > hi.
- *Relaxation rows.*
  - Square tangents −w + 2a·x ≤ up(a·a) are valid for any float a.
  - Square and cube secants use C ≥ max(x^p − s·x) at the two endpoints,
    valid because x^p − s·x is convex there.
  - Cube tangents use a constant ≤ min over [l,h] of (x³ − g·x). The minimizer
    √(g/3) is enclosed and clipped to [l,h]; the arguments are ≥ 0 (asserted).
  - McCormick rows: I checked all four inequalities and the rounding direction
    of their right-hand sides (up(lx·ly), up(hx·hy), −dn(lx·hy), −dn(hx·ly)).
- *Node bound.* `safe_bound` computes min over the box of (c + Aᵀy)·z − y·b.
  - y is clamped to ≥ 0 on ≤ rows.
  - Coefficient intervals are propagated into [rlo, rhi]; the ±1e-300 shift
    makes any unbounded variable give −∞.
  - The right-hand-side interval end is chosen by the sign of y.
  - Corner products are rounded down, and a final margin is subtracted.
  - This is valid for any y, so HiGHS (including the elastic LP) only
    supplies hints. Confirmed.
- *Pruning.*
  - A node is closed only if its bound is ≥ target or FBBT proves it empty.
  - Reduced-cost tightening G_j = up(up(target − B) + term_j) removes only
    points with c·x ≥ target. I checked the four sign cases of the division.
  - Root OBBT adds the cutoff row c·x ≤ target. Both are valid for the
    statement φ ≥ min(target, open bounds). The returned bound is
    min(target, open heap bounds, bounds of unbranchable leaves).
  - Children use the parent's bound, which is valid because their boxes are
    subsets.
  - Branching splits binaries into {0} and {1} and continuous variables into
    covering halves.
- *certify.py.* Target choice affects only speed. The sum uses `Fraction` and
  is rounded down.

Minor, not affecting validity: the module docstring of `rbb.py` still says
the margin is "4e-14 … for n ≤ 300" whereas the code uses 1e-12 (the report
text states 1e-12 correctly). Termination is not guaranteed in general, but
node and time limits are enforced and a limit returns a valid, lower bound.

### 3.2 Independent re-bounding (verifier's B&B `vbb.py`)

`vbb.py` shares no code with `rbb.py`. Its certificate arithmetic is exact
rational:

- FBBT computes every new bound in `Fraction` and rounds it outward to a double.
- Roots are rounded outward and checked by exact squaring or cubing.
- Relaxation rows have exact rational coefficients: tangents w ≥ 2p·x − p²
  and w ≥ 3p²·x − 2p³ at the ends and quartiles, exact secants, McCormick.
- The node bound min over the box of (c + Aᵀy)·z − y·b is evaluated exactly.

HiGHS (scipy) only supplies y. There is no reduced-cost tightening and no
cutoff-based OBBT (root OBBT without cutoff). The branching point is the LP
value clipped to the middle half.

Each run below was given the authors' certified per-period value as the target;
"certified" means `vbb` proved φ_t ≥ that value exactly. All six periods of
waterno2_06 are re-certified. The verifier's per-period values are therefore
identical to the authors', and so is their exact sum 263.735099441… (3.3).

| instance, period | implied bounds used | authors' certified φ_t | vbb result | nodes / time |
|---|---|---|---|---|
| 06, 0 | none | 158.44542021914268 | **certified** | 1835 / 121 s |
| 06, 1 | verifier's own (`logs/my_implied_06.json`) | 3.3200165915325814 | **certified** | 5441 / 357 s |
| 06, 2 | verifier's own | 0.05585209119252331 | **certified** | 5935 / 390 s |
| 06, 3 | verifier's own | 0.011863658606134687 | **certified** | 8129 / 530 s |
| 06, 4 | none | −5.762328864166388 | **certified** | 6869 / 456 s |
| 06, 5 | none | −218.06733936023628 | **certified** | 1997 / 124 s |
| 09, 6 | none | −759.9355220257974 | **certified** | 2287 / 150 s |
| 24, 19 | none | 795.585216392664 | **certified** | 5419 / 363 s |

Multipliers are from `logs/mult_TT_w1_impl.json`.

**Periods 1–3 need the implied bounds.** Without them, BARON finds points
with lower values: 2.248168 in period 1, −0.540242 in period 2 and −0.009791
in period 3. These points start tank 3 at level 2.0, which the proven implied
bounds exclude (3.3325, 2.67 and 2.03125). My B&B runs without implied bounds
(`logs/vbb_06_p{1,2,3}_noimplied_stopped.log`) stalled near those values.
With the bounds, BARON gives 3.320424, 0.055986 and 0.012210, all above the
certified values. The implied bounds are therefore essential to the reported
263.735 (the report's 262.702 → 263.735 statement is consistent with this).

**Consistency with feasible points** (certified value ≤ value of a feasible point):

- *Exactly feasible rational points.* These were built by `vrepair.py` from
  SCIP points with the pump configuration fixed (feastol 1e-9), at the
  certificate multipliers. Each was checked exactly on all rows and bounds:

  | period | exact value | certified | gap |
  |---|---|---|---|
  | 0 | 158.445520677814 | 158.445420219 | 1.0e-4 |
  | 4 | −5.761955224208 | −5.762328864 | 3.7e-4 |
  | 5 | −218.067074954988 | −218.067339360 | 2.6e-4 |

  So these three certified values are within 4e-4 of the true optima.
- *BARON 26.5.27* (GAMS 54.3, optcr = 0; points feasible to BARON's tolerance)
  at the certificate multipliers: 158.445521, 3.320424 (with implied bounds),
  0.055986 (implied), 0.012210 (implied), −5.762110, −218.067169. All are ≥ the
  certified values (`logs/vbaron_cert06*.log`).
- *Negative control* (period 0 at the SCIP-repro multipliers). With an
  unreachable target, the exact feasible value + 0.05, `vbb` stops with status
  `limit` and rigorous bound 168.10865202980798. This is 9.8e-15 below the
  exactly feasible value 168.108652029808
  (`logs/vbb_06_p0_repro_unreachable.log`). With target = feasible − 1e-3 it
  certifies (`logs/vbb_06_p0_repro_reach.log`).
- *Second control* (period 1 without implied bounds, certificate
  multipliers). `vbb` with the unreachable target 2.3 stops at 1200 s with
  rigorous bound 2.248637310 (`logs/vbb_06_p1_noimplied_control.log`). An
  exactly feasible point has value 2.248638319
  (`logs/cert_exact_point_p1_noimplied.json`), so the bound is 1.0e-6 below
  it, as it should be. BARON's "optimal" point for the same problem has value
  2.248168, *below* this rigorous bound. Its maximum row violation is 6.3e-7
  (`logs/vbaron_eval_p1_noimplied.log`), so BARON exploits its tolerance by about 5e-4 in
  objective. This confirms the report's remark that tolerance-feasible
  solver values can lie noticeably below exact optima. The authors' targets
  were taken 1e-4 below SCIP values; where the SCIP value was too low, `rbb`
  simply certified a slightly weaker bound.

### 3.3 Exact sum

`vsum.py` (`logs/vsum.log`) recomputes μ·rhs + Σ_t B_t in `Fraction` from the
certificate JSON files. It also checks that the multipliers match
`mult_TT_w1_impl.json`, that μ ≥ 0, that the windows are the T single
periods, and that every period is `certified` with bound = target.

- waterno2_06: μ·rhs = 325.731615106, and the sum is
  148469661946242564611253309/562949953421312000000000 = 263.735099441651…,
  which rounds down to **263.735099441**. This equals the stored exact value.
- Also reproduced exactly:
  - waterno2_09: 824.834692454
  - waterno2_12: 2089.754565439
  - waterno2_18: 4790.820715376
  - waterno2_24: 6576.151388415
  - waterno2_02: 39.314005760
  - waterno2_03: 74.068040651
  - waterno2_04: 132.529333260
- The small-instance bounds lie below the known optima (39.5714, 115.0045,
  145.4398), as they must.

## 4. SCIP 10.0.2 wrong "optimal" claims

**Verdict: confirmed; genuine wrong answer by SCIP, not a tolerance effect
and not caused by presolve.**

Versions: SCIP 10.0.2 (SoPlex 8.0.2, 8-byte precision, no GMP), PySCIPOpt
6.2.1. The model is single-threaded (`parallel/maxnthreads = 1`,
`lp/threads = 1`). The multipliers are those in `logs/scip_repro_mult.json`.

**Reproduction.** `scip_unreliable.py` reproduced every number of the
authors' log exactly (`logs/repro_scip_unreliable.log`), for example
period 0 default 169.950327 vs noprop 168.108652.

**Independent model.** `scip_check.py` builds the SCIP model from osilx data
(not with `period.build`) and reproduces the errors: period 0 default gives
169.950327, period 5 −229.759028 and period 4 −5.723535.

**Cheaper points.** Each point comes from SCIP with the cheaper
configuration fixed at feastol 1e-9 (`logs/scip_check.log`):

| period | configuration | value | max row violation | bounds | integral | SCIP `checkSol` (original problem, default tolerances) |
|---|---|---|---|---|---|---|
| 0 | all off | 168.108652030 | 1.0e-9 (e949) | ok (3.6e-16) | yes | feasible |
| 4 | [1,1,0,…] | −6.730644411 | 1.0e-9 (e1018) | ok | yes | feasible |
| 5 | [1,0,…] | −232.172857393 | 1.0e-9 (e1032) | ok | yes | feasible |

So none of the three SCIP points is exactly feasible (violations about
1e-9). `vrepair.py` (`logs/vrepair.log`) then built nearby **exactly
feasible** rational points:

- the binaries are fixed;
- the flows and speeds are seeded with 10-decimal roundings;
- all other variables are solved exactly from equality rows, including the
  implied equalities formed by the big-M head rows of running pumps.

All rows and bounds are then checked in `Fraction` arithmetic.

| period | exactly feasible value | SCIP's claimed optimum (default) | excess |
|---|---|---|---|
| 0 | 168.108652029808 | 169.950327 | 1.84 |
| 4 | −6.730643699816 | −5.723535 | 1.01 |
| 5 | −232.172853003462 | −229.759028 | 2.41 |

BARON confirms the true optima: 168.108652 (all off), −6.730795 (config
[1,1,0,…]) and −232.172945 (config [1,0,…]), each with status optimal.

**Tolerances do not explain it.**

- With `numerics/feastol = 1e-9` (SCIP silently uses 1e-10 for the LP), the
  claims stay wrong: 169.951313 in period 0, −228.342591 in period 5 and
  −4.645996 in period 4. The last two are worse than the default runs.
- Adding `numerics/dualfeastol = 1e-9`, or emphasis NUMERICS combined with
  feastol 1e-9, is also wrong in all three periods.
- Emphasis NUMERICS alone is right in periods 0 and 5 but wrong in period 4.

**Presolve is not the cause.**

- For the default run of period 0, the global bounds of the transformed
  problem contain x* after presolve and at node limits 1, 2, …, 400
  (`logs/scip_diag2_p0.log`).
- Given as a start solution, x* is accepted and survives presolve. SCIP then
  ends optimal at 168.108652 (`logs/scip_diag_p0.log`).

**Where it happens.** `scip_trace.py` (`logs/scip_trace_p0.log`) traces
the default run of period 0 through its event handler:

- x* lies inside the local boxes of nodes 1 → 2 → 22 → 42 → 288.
- At node 288 (depth 4), the cutoff is −64.900 in transformed objective
  space, and x*'s transformed value is −79.502, below the cutoff.
- The node's own inferred bound changes (type PROPINFER, the type SCIP stores
  for inferences at the focus node that have no constraint attached) include
  b44 ≥ 1, x362 ≥ 0.2521, x267 ≥ 3.8998 and x146 ≤ 13.412. All of them
  exclude x*.
- The node LP bound (−88.91) is still below x*. So an invalid node-local
  domain reduction removed the optimal region.

**Which component** (`logs/scip_check.log`, `logs/scip_bisect*.log`;
default settings plus one change each):

- Only these changes give the right answer in all three periods:
  - `propagating/maxrounds = 0` together with `propagating/maxroundsroot = 0`;
  - `propagating/maxrounds = 0` (nodes only);
  - `constraints/nonlinear/maxproprounds = 0`;
  - `constraints/nonlinear/propfreq = 0` or `−1`;
  - `constraints/nonlinear/varboundrelax = n` or `a`.
- Turning off all ten propagator plugins but keeping the nonlinear handler's
  propagation still fails in periods 4 and 5. Additionally setting
  `constraints/nonlinear/propfreq = −1` fixes all three.
- Many switches fix period 0 or period 5 only by changing the search path,
  for example no OBBT, separation off or emphasis numerics. Of the 48
  settings tried, 1 crashed and the rest ended as follows:

  | period | wrong | right |
  |---|---|---|
  | 0 | 28 | 19 |
  | 4 | 38 | 9 |
  | 5 | 31 | 16 |

  The settings right in all three periods are exactly those listed above,
  plus the combination "all propagator plugins off + nonlinear propfreq −1".
- Conclusion: the evidence points to node-level domain propagation of the
  nonlinear constraint handler (possibly its bound-relaxation logic). A debug
  build would be needed to pin it down.

**Other SCIP defects observed:**

- `presolving/maxrounds = 0` and `setPresolve(OFF)` both segfault (exit 139)
  on period 0 (`logs/scip_presolve_off_*.log`), as the report says.
- `constraints/nonlinear/maxprerounds = 0` aborts with "cannot change bounds
  of multi-aggregated variable" (`tree.c:1996`, called from probing) and then
  segfaults, in all three periods.

**Consequence.** The authors' decision to use SCIP only as an oracle, never
as a bound, is necessary. It also means the bundle's "fixes" were needed. The
listed MINLPLib SCIP dual bounds for waterno2 were not examined; they are far
below the certified bounds, so they do not conflict with them.

## 5. Primal points (waterno2_09–24)

**Verdict: confirmed.** `veval.py` evaluates rows directly from the OSIL
expression trees (`osilx.ev_row` with `Fraction`), independently of `evalpt.py`,
both for the decimal strings and for the exact binary doubles
(`logs/veval_primal.log`):

| instance | exact objective | max row violation (row) | max bound violation (var) | binaries |
|---|---|---|---|---|
| 09 | 914.011970350 | 1.000e-09 (e1677) | 5.726e-11 (x1443) | integral |
| 12 | 2233.821335282 | 1.000e-09 (e2097) | 3.090e-10 (x1739) | integral |
| 18 | 5023.982735143 | 4.437e-09 (e299) | 8.939e-10 (x2915) | integral |
| 24 | 6963.795154460 | 1.000e-09 (e3896) | 9.002e-10 (x3633) | integral |

These points are not exactly feasible; they are within MINLPLib's 1e-8
acceptance threshold for listed primal bounds. waterno2_06 p4:
282.888037387, violation 1.08e-11 (e94); p1: 307.045516202, 6.55e-10.

## 6. MINLPLib status

**Verdict: confirmed** (pages downloaded 2026-09-30 to `web/`).

| instance | listed primal | best listed dual (solver) | certified dual | gap before → after |
|---|---|---|---|---|
| 06 | 282.8880374 | 165.1902989 (SCIP) | 263.735099441 | 71.25% → 7.26% |
| 09 | 922.5952898 | 273.8958303 (SCIP) | 824.834692454 | 236.84% → 10.81% |
| 12 | 2263.358374 | 479.5051427 (GUROBI) | 2089.754565439 | 372.02% → 6.89% |
| 18 | 5269.638815 | 770.7361733 (SCIP) | 4790.820715376 | 583.71% → 4.87% |
| 24 | 7332.721691 | 1095.126488 (SCIP) | 6576.151388415 | 569.58% → 5.89% |

"After" uses the verifier-confirmed primal values of Section 5 (and p4 for
06). Other listed duals for 06: ANTIGONE 89.07, BARON 107.95, COUENNE 94.21,
GUROBI 162.19, LINDO 34.03, XPRESS 108.40, SHOT 0.
Novelty beyond MINLPLib (for example published bounds elsewhere) was not
checked.

## What remains unchecked

- `rbb.py` outputs for the 48 periods of waterno2_09–24 other than the two
  re-bounded ones. They rely on the reviewed code, which I found sound, and
  on implied bounds, which I proved.
- The authors' test scripts (`test_relax.py`, `test_rbb2.py`,
  `crosscheck_plain.py`), the bundle runs, the runtimes, the gap-closing
  experiments (Section 7 of the report) and the claim that no better point
  exists for 06. None of these affects validity.
- The exact SCIP component at fault (needs a debug build).

## Commands run (targeted checks only; no project-wide checks, no CI)

From this directory unless noted; `OMP_NUM_THREADS=1` for all solver runs.

```
python3 vstruct.py 1 2 3 4 6 9 12 18 24                # logs/vstruct.log
python3 veval.py T <authors' primal_TT_w2.json | .sol>  # logs/veval_primal.log
python3 vimplied.py 6 2; python3 vimplied.py {9,12,18,24} 3   # logs/vimplied_TT.log, logs/my_implied_06.json
python3 vsum.py 6 9 12 18 24; python3 vsum.py 2 3 4     # logs/vsum.log
python3 vbb.py 6 {0,4,5} <mult_06_w1_impl.json> <their B_t> 40000|60000 1800|2400
python3 vbb.py 6 {1,2,3} <mult_06_w1_impl.json> <their B_t> 60000 2400 logs/my_implied_06.json
python3 vbb.py 9 6 ... ; python3 vbb.py 24 19 ...        # logs/vbb_*.log
python3 vbb.py 6 0 <scip_repro_mult.json> {168.158652029808,168.107652029808} 20000 1200
python3 vbb.py 6 1 <mult_06_w1_impl.json> 2.3 30000 1200     # control, no implied bounds
python3 vbaron.py 6 t <mult> 300 [logs/my_implied_06.json]; python3 vbaron_eval.py ...
(cd ../../open-instances-wave2/waterno2 && PYTHONDONTWRITEBYTECODE=1 python3 scip_unreliable.py)
python3 scip_check.py 0,5,4 <settings>; python3 scip_bisect.py t [settings]
python3 scip_diag.py 0 default no_obbt feastol1e-9; python3 scip_diag2.py 0 default; python3 scip_trace.py 0 default
python3 vrepair.py 0; python3 vrepair.py 5; python3 vrepair.py 4 10 x528=1/100000000 x286:x202:1/2
WV_MULT=<mult_06_w1_impl.json> python3 vtight.py t <config>; WV_POINT=... python3 vrepair.py t
curl https://www.minlplib.org/waterno2_TT.html
```
