# Review: computation/scaling-study.md (SCIP versus chain DP branch and bound)

Date: 2026-09-29. Reviewer: independent adversarial review (computational
global optimization). Scope: `computation/scaling-study.md`, `tables.md`,
`chain_bb.py`, `instances.py`, `lotsizing.py`, `verify_instances.py`,
`run_scip.py`, `data/`, `logs/`, with `PROGRAM.md` as context. No file
under `computation/` was edited. Review scripts and outputs are in
`reviews/computation-review-checks/` (scripts) and
`reviews/computation-review-checks/logs/` (outputs).

## Overall verdict

The central computational claims hold. The prototype's lower bounds are
valid: I found no flaw in the argument or the code, and an independent method
reproduces the optimal values. SCIP's node counts reproduce exactly, and the
settings were applied. The study needs several corrections, but none of them
changes its main conclusions:

- one factual error about multistart at `n = 1000` (item 2);
- a wrong justification for why lot-sizing violates the premise (item 4);
- an inaccurate caveat about which SCIP separators were active (item 3);
- some wording that is stronger than the evidence (items 3 and 5).

| item | verdict |
|---|---|
| 1. Validity of prototype lower bounds (4.2, 4.3) | **Valid.** Independent optimum agrees; adversarial tests find no violation. The 4.3 rounding justification needs rewording. |
| 2. Uniqueness / interiority / nondegeneracy certificates | **Positive certificates: rigorous up to floating-point rounding** (independently reproduced). **Negative claims (amp 0.3): evidence only in the study**, now made rigorous for 9 instances here. One factual error (multistart failures at `n = 1000`). |
| 3. SCIP claims | **Node counts reproduce exactly; parameter names valid and applied.** "OBBT at every node" needs qualifying. The "RLT/SDP/intersection cuts not tested" caveat is inaccurate. The exponential-versus-polynomial discussion is fair, but a stronger diagnostic is available. |
| 4. Lot-sizing family | **Definition consistent** (SCIP and prototype models match; bounds valid). **The stated reason for violating the premise is wrong.** The optimum is a nondegenerate *boundary* minimizer, not a degenerate one. |
| 5. Caveats | **Mostly appropriate.** Summary bullets on SCIP growth and prototype scaling should carry the caveats already stated in Section 7. |

---

## 1. Validity of the prototype's lower bounds

### 1.1 Code and argument review (`chain_bb.py`, `instances.py`, `lotsizing.py`)

I checked each step of the argument in 4.2 against the code.

- **Identity (4.2.1).** The unary piece receives `-Q x^2 + L x` (lines 237-238,
  `unary_lb(..., Qt, Lt)`), and the pair receives `+rho x^2 - alpha x` (`pair_lb`). The
  signs cancel exactly, so validity is independent of the transfers. This is confirmed
  by the perturbed-transfer test below.
- **Probe3 unary bound.** `Hlo = 2(1-Q) - 12 kappa max(p^2, q^2)` is the exact
  infimum of `phi''` on the cell for `kappa >= 0`. `taylor2_lb` handles the
  concave or linear case (`Hlo <= 0`) with the endpoint formula
  `-|g| r + Hlo r^2 / 2`, which is correct.
- **`quad_box_min`.** In mode `quad`, `A = C = 0.4` and `B = 0.8`. The
  computed `det = 4*0.4*0.4 - 0.8^2` is exactly 0 in floating point (both
  products round the same real number), so the positive-definite branch never
  fires. The boundary-candidate argument still covers this case: a PSD-singular
  quadratic on a box has a boundary minimizer. The code enumerates exactly the
  needed candidates.
- **Lot-sizing pair bound.** The Taylor centre `pm` can lie outside the band
  `[0, P]`. The bound stays valid because `Hlo = g''(plo)` uses the
  *unclipped* production range of the box, `plo = s - q + d`. That range
  contains the whole segment between the centre and any point. This detail is
  load-bearing: clipping `plo` at 0 would make the bound invalid. It deserves a
  comment in the code.
- **Pruning / coverage (4.2.4).** The argument is correct. One wording fix:
  cells are closed and share endpoints, so a coordinate can lie in a removed
  cell and a surviving cell at once. State step 4 as: "let `t` be the first
  iteration after which `x` is no longer covered by the product of current
  cells; some coordinate `x_j` then has all its containing cells removed at
  `t`, so `F(x) >= m_j(a) >= pruned_min`."
- **`K.min() == 0` exit (line 301).** The run stops without testing
  `LB >= UB - eps`. The test is implied, because every removed marginal is
  `>= UB_t - eps >= UB - eps`, so this exit is correct.
- **`unary_lb_sub` (negligible).** The last sub-interval ends at
  `min(p + 16w, q)`, which can fall one ulp short of `q`. The uncovered sliver
  changes the bound by about 1e-16, far below the 1e-13 margin. Setting the
  last endpoint to `q` exactly would remove the question.
- **Localization mode.** `keep = marg <= UB + delta`, and the hull is taken
  after pruning. The claim "every `x` with `F(x) <= UB_final + delta` lies in
  the hull" follows because thresholds only decrease.

### 1.2 Independent optimum (different method)

`indep_grid_dp.py` is a value-function DP on a uniform grid. It uses no
transfers, no Taylor bounds and no pruning. Its lower bound rests on one fact:
every value function satisfies "`V_i(x) - x^2` is concave". The reason is that
`u_i - x^2 = -kappa x^4 + c x` is concave, and `min_y [b x y + V(y)]` is
concave in `x`. So on a grid interval of width `h`, the continuous minimum is
at least the smaller endpoint value minus `h^2/4`. This gives a rigorous
bracket with discretization loss `n h^2 / 4` (up to rounding, about 1e-13).
The upper bound (UB) is `F` at the grid argmin path, polished with L-BFGS-B.

Results (`logs/compare_proto.jsonl`, `logs/compare_proto_small.jsonl`). The
prototype was rerun with the study's settings (`quad`, `unary_sub = 16`) at
eps 1e-4 and 1e-6 on 33 instances:

- amp 0.2: `n = 6, 10, 20, 50`, seeds 0-4; `n = 2, 4`.
- amp 0.3: `n = 4`; and the boundary-optimum cases `n = 12` (seed 4),
  `16` (seeds 0, 4), `100` (seed 4), `256` (seed 4).

| check | result |
|---|---|
| prototype LB - independent UB (must be <= 0) | max **-7.1e-8** over 66 runs (never positive) |
| prototype UB - independent UB | between -1.1e-15 and +3.6e-15: the same point |
| prototype UB - independent LB | at most 1.24e-5, always within `eps` + discretization loss |
| independent bracket width, amp 0.2, n = 50 | 2.2e-6 to 2.4e-6 |

For amp 0.3, both methods find the same boundary optimum. Coordinates at ±1:
5 (`n = 12`, seed 4), 2 and 5 (`n = 16`, seeds 0 and 4), 5 (`n = 100`,
seed 4), 17 (`n = 256`, seed 4).

### 1.3 Adversarial tests of the prototype

`adversarial_proto.py` (`logs/adversarial_proto.log`) ran 75 runs:

- five parameter sets `(kappa, b, amp)`: (0.1, 0.8, 0.2), (0.1, -0.8, 0.3),
  (0.3, 0.9, 0.5), (0.25, -1.2, 0.1), (0, 1.5, 0.4);
- `n = 5, 9, 16`;
- modes `quad`, `affine`, `plain`, with `unary_sub` 1 and 16;
- transfers computed at an incumbent perturbed by Gaussian noise of standard
  deviation 0.3 or 1.0.

The largest value over all iterations of (LB - rigorous upper bound on
`f*`) was **-2.4e-12**. There were no violations. Twenty-one runs with noisy
transfers hit the pair cap, as expected: tightness depends on the transfers,
validity does not.

`lotsizing_pair_adversarial.py` tested 14,965 feasible boxes. They included
boxes straddling the band lines (centre outside the band), boxes of width 1e-4
to 3, and singular models with `rho = 0` (so `det = 0`). The largest value of
LB minus the sampled minimum was **-1.0e-11**, which is the safety margin.

The study's own `test_bounds.py` reproduces as reported
(`logs/test_bounds_rerun.log`).

### 1.4 Floating point (4.3)

`dp_rounding.py` (`logs/dp_rounding_n8192.log`) recorded the final-iteration
piece bounds for amp 0.2, `n = 8192`, seed 0, eps 1e-6, and redid the DP in
`np.longdouble`. The difference from float64 is **8.7e-17**. The largest
|partial sum| is 47.7, so the rigorous recursive-summation bound is
`2n * 47.7 * u = 8.7e-11`. The conclusion of 4.3 holds.

**Fix (wording).** The justification "at most `2n` terms of size at most about
10 ... below 1e-9" does not follow. With the standard bound
`(2n) u sum|t_i|`, those numbers give about 3e-7 at `n = 8192`. The relevant
quantity is `sum_k |S_k| u` over the partial sums `S_k`, which I measured at
8.7e-11. Also, "the margins add up to a comparable amount" should say that the
margins are *subtracted*: they add safety, not error. They do not cover the DP
summation error, which is covered only by the measured 8.7e-11 being far
below eps.

**Verdict on item 1:** valid. The only gap is the one the study states: there
is no interval arithmetic. I found no case where the DP bound exceeds the true
optimum.

---

## 2. Uniqueness / interiority / nondegeneracy certificates (1.3, 4.4)

### 2.1 Positive certificates (amp 0.2, and amp 0.3 where certified)

**Rigorous up to floating-point rounding.** The logic is sound:

1. Every point with `F <= UB + delta` lies in the hull `R` (item 1).
2. `M = tridiag(2 - 1.2 max_R x_i^2, 0.8)` is a Loewner lower bound of the
   Hessian on `R`.
3. `lambda_min(M) > 0` and `R` inside the open box `(-1, 1)^n` together give a
   unique, interior, nondegenerate global minimizer.

The eigenvalue test has a threshold of 1e-8, while the certified margin is at
least 0.18. So LAPACK rounding is irrelevant, and the only non-rigorous
element is the DP's floating-point arithmetic.

**Independent reproduction.** `indep_cert.py` (`logs/indep_cert.jsonl`) builds
localization boxes from forward/backward grid-DP marginals. The marginal
`M_i(t) = Ff_i + Vb_i - u_i` satisfies "`M_i(t) - 2 t^2` is concave", so the
grid loss is `h^2/2`. Results for amp 0.2:

| instance | box interior | `lambda_min(M)` (this review) | `lambda_min(M)` (study) |
|---|---|---|---|
| `n = 20`, seed 0 | yes | 0.329 | – |
| `n = 256`, seed 4 | yes | 0.289 | – |
| `n = 1000`, seed 3 (three local minima found by multistart) | yes | 0.245 | 0.244 |

**Fix.** Section 1.3 says the certificate gave "at least 0.18" for amp 0.2.
The amp 0.2 minimum is **0.244**; 0.181 is the amp 0.3 minimum.

The multistart columns are heuristic, as the study says.

### 2.2 Negative claims (amp 0.3: premise fails)

- **Non-certification is not evidence of failure.** All 25 non-certified amp 0.3
  cases in `data/verify.jsonl` ended with `cert_status = pair_limit`. The
  "certified" column counts successes of a capped run. Its complement means
  "no certificate obtained", not "certified boundary minimum". The table
  header or a note should say this.
- **The boundary claim itself is true, and is now rigorous here for 9
  instances.** `indep_cert.py` computes a rigorous lower bound of `min F` over
  `[-0.99, 0.99]^n` and compares it with a feasible value. Every global
  minimizer then has a coordinate with `|x_i| > 0.99`. Amount by which the
  lower bound exceeds the optimum:

  | instance | margin |
  |---|---|
  | `n = 12`, seed 4 | 5.2e-3 |
  | `n = 16`, seed 0 | 1.6e-3 |
  | `n = 16`, seed 4 | 5.3e-3 |
  | `n = 100`, seed 4 | 5.3e-3 |
  | `n = 1000`, seeds 0-4 | 4.4e-3 to 3.2e-2 |

  (`logs/indep_cert.jsonl`, `logs/indep_boundary_n1000.jsonl`.) In the study,
  this claim rested on eps-optimal prototype points plus multistart, which is
  evidence, not a certificate. Suggest citing this check, or adding it to
  `verify_instances.py`.
- **Factual error.** Section 1.3 says: "In 3 instances (`n = 100, 256`, seed
  4; `n = 1000`, seed 2), 250-start multistart did not find the global
  optimum; the prototype did." At `n = 1000`, multistart missed the optimum
  for **four** seeds (`logs/indep_boundary_n1000.jsonl` against
  `verify.jsonl`):

  | seed | multistart worse by |
  |---|---|
  | 0 | 8.8e-3 |
  | 2 | 6.6e-3 |
  | 3 | 9.8e-4 |
  | 4 | 1.1e-2 |

  The capped localization run did not find the optimum for seeds 0, 3 and 4
  either. For seed 2 its UB is right but uncertified. For `n <= 256`, the
  study's statement is correct: I checked all 19 non-certified amp 0.3
  instances (`logs/indep_amp0.3_uncertified.jsonl`).

  Consequences:
  - The amp 0.3, `n = 1000` row of the 1.3 table ("min lambda_min(H) at x*",
    "max |x*_i|") is computed at non-global points for 4 of 5 seeds.
  - There is no prototype eps-optimal run at `n = 1000`; the main runs use
    `n = 1024`. So the claim "all 5 seeds at `n = 1000`" in 1.3 and in
    PROGRAM.md rested on multistart only. It is true, as shown above, but was
    unsupported.

  **Fix:** "multistart missed the global optimum in 6 instances (`n = 100`
  and `256`, seed 4; `n = 1000`, seeds 0, 2, 3, 4)". Recompute or footnote the
  `n = 1000` row, and cite the restricted-box check.

---

## 3. SCIP claims (Section 3)

### 3.1 Reruns (`scip_rerun.py`, `logs/scip_rerun.log`)

All runs used seed 0, eps 1e-4, and the study's own `run_scip.solve`. Node
counts, primal values and dual values are **identical** to the data:

| run | nodes (rerun = data) |
|---|---|
| default, amp 0.3, `n = 6` | 1055 |
| default, amp 0.3, `n = 8` | 4447 |
| default, amp 0.2, `n = 6` | 1161 |
| default, amp 0.2, `n = 8` | 5258 |
| `obbt`, `n = 6` | 320 |
| `bestfirst`, `n = 6` | 531 |
| `emph_opt`, `n = 6` | 1574 |
| `single`, `n = 6` | 460 |
| `combo`, `n = 6` | 175 |
| `warm`, `n = 8` | 3695 |

### 3.2 Were the settings applied?

The changed-parameter files are in `logs/scip_params_changed_*.set`, and the
statistics in `logs/scip_stats_*_n6_amp0.3_seed0.txt`.

- **Parameter names.** All are valid in SCIP 10.0 / PySCIPOpt 6.2.1:
  `nodeselection/bfs/stdpriority`, `nodeselection/bfs/maxplungedepth`,
  `propagating/obbt/freq`, `limits/absgap`, `limits/gap`, `timing/clocktype`.
  `setParam` raises an error on unknown names, and the written files show the
  values.
- **`single`.** The whole objective, including the linear terms, is in one
  constraint `t >= F(x)`. Correct.
- **OBBT "at every node": needs qualifying.** With `freq = 1`, the obbt
  propagator ran **228 times in 320 nodes** (`combo`: 133 of 175; default:
  2). It runs only after a solved LP. It also uses a per-call LP-iteration
  limit (`propagating/obbt/itlimitfactor = 10` times the root LP iterations),
  and `onlynonconvexvars = TRUE`. **Fix:** "OBBT called at every node with a
  solved LP (`propagating/obbt/freq = 1`; 228 of 320 nodes at `n = 6`)".
- **Best-first.** The bfs selector has the highest priority, and plunging is
  off. "Pure best-bound selection" is a fair description.
- **Emphasis OPTIMALITY.** It changes 64 parameters. The ones that matter here
  are aggressive separation, including:
  - `separating/rlt/freq = 20` (default 0, root only);
  - `separating/interminor/freq = 0` (default off);
  - `eccuts`, `gauge`, `convexproj` at the root.

  The branching changes (relpscost, fullstrong priority) have no effect.
  `constraints/nonlinear/branching/external = FALSE`, so the nonlinear handler
  branches itself. This explains why `setSeparating(AGGRESSIVE)` gave
  identical counts.
- **Inaccurate caveat (7, "Other solvers and settings").** "Neither were
  SCIP's intersection-cut or RLT/SDP-type separators [tested]" is not right.
  - The **default** runs used the 2x2-minor (SDP-type) separator
    (`separating/minor/freq = 10`): 123 calls and 184 cuts applied at `n = 6`.
  - RLT ran at the root in the default runs (0 cuts).
  - `emph_opt` and `combo` ran interminor intersection cuts at the root (44
    applied) and RLT every 20 levels.

  What was *not* tested: `nlhdlr/quadratic/useintersectioncuts` (off), and
  RLT, minor or interminor at every node. **Fix the caveat accordingly.**

### 3.3 Tolerances

This is confirmed independently. SCIP's reported optimal values lie
**3.7e-6 to 6.5e-6 below a rigorous lower bound on `f*`**
(`logs/indep_scip_below.jsonl`):

| instance | SCIP value minus rigorous LB |
|---|---|
| amp 0.3, `n = 10`, seed 4 | -6.5e-6 |
| amp 0.3, `n = 10`, seed 3 | -6.1e-6 |
| amp 0.3, `n = 8`, seed 4 | -5.2e-6 |
| amp 0.2, `n = 8`, seed 1 | -3.7e-6 |

This supports the study's feasibility-tolerance explanation (5.6 and 7), and
its caveat that SCIP's eps 1e-6 runs are not true 1e-6 certificates.

At `n = 12` (amp 0.3, seed 0), SCIP's root incumbent (subnlp, 0.0 s) already
equals the optimum to 1e-7. The later "improvement" at node 84,939 is only
this tolerance effect. So "SCIP finds the optimum early" holds there too.

### 3.4 Exponential versus `n^5.3`: is the discussion fair?

It is fair in that the study states that both fits are equally good on
`n = 4..10`. Two refinements are needed.

- **Step ratios alone point the other way.** At amp 0.2, eps 1e-4, the ratio of
  geometric means per +2 variables falls: 6.9, 4.7, 4.1. Taken alone, that
  suggests sub-exponential growth. The more informative diagnostic is the
  **local power-law exponent** `ln(ratio) / ln((n+2)/n)`, which *rises*:

  | family and eps | local exponents | predicted by an exact 5x-per-2 exponential |
  |---|---|---|
  | amp 0.2, eps 1e-4 | 4.8, 5.4, 6.3 | 4.0, 5.6, 7.2 |
  | amp 0.2, eps 1e-2 | 4.7, 5.3, 7.7, 8.1 | 4.0, 5.6, 7.2, 8.8 |

  This argues against a fixed-degree polynomial on this range and is a better
  argument than comparing `R^2` values on 4 points. Suggest adding it, with
  the caveat of 5 seeds and a narrow range.
- **Seed dispersion.** The `n = 14` extrapolation argument (1.7-2.5 times the
  power-law prediction, still unsolved) compares 3 seeds with a
  geometric-mean prediction. At `n = 10`, a single seed deviates by up to 3.1x
  from the geometric mean (amp 0.3, seed 4: 117,011 against 37,311). The
  argument is stronger for amp 0.2: seeds 0-2 were at 0.79-1.05 times the
  `n = 10` geometric mean, and 2.2-2.5 times the prediction at `n = 14`.
  Suggest comparing seed by seed, or stating the dispersion.
- **Wording.** The summary heading "grows geometrically" presumes the model.
  Suggest: "grows by about 5x per two variables on `n = 4..10` (step factors
  4-8)". Likewise, "This does not depend on the settings tried" should read
  "persists under the six variations tried".
- **Throughput collapse (3.2).** It remains unexplained. The statistics
  attribute little of the time, and the study reports about 25% extra system
  time. That points to memory or allocator effects rather than to a solver
  component. Recording peak RSS, or a rerun on an idle machine, would settle
  it. It does not affect solved counts.

---

## 4. Lot-sizing family (Section 6)

- **Definition.** SCIP and prototype models agree: bounds, balances, `g`,
  holding cost. `g' >= 0.2`, with the minimum at `p = 4/3`, which is also the
  inflection point. Both statements are correct.

  Unstated modelling choices that should be mentioned:
  1. There is no terminal-inventory condition. A final backlog `s_T < 0` is
     allowed and penalized only by `0.5 s_T^2`.
  2. The SCIP model aggregates holding cost in one convex constraint
     `w >= 0.5 sum s_t^2`, which links all periods. So SCIP's constraint graph
     is not a path, although the chain structure is intact in the `s`
     variables.
- **Bounds.** Valid (1.1 and 1.3). The prototype LB exceeds SCIP's primal
  value in 41 of 120 comparisons, by at most 3.4e-6. This is the same SCIP
  tolerance effect as in 3.3. SCIP's gaps at `T = 12` are 0.36-0.60, as
  stated.
- **Wrong justification (1.2).** The study says the family "does not have an
  interior nondegenerate minimizer ... the Hessian on the free variables is
  indefinite at the optimum (-2.5 for `T = 50`, seed 0)". The -2.50 is the
  **full** Hessian in the inventory variables; I reproduce -2.496
  (`lotsizing_hessian.py`, `logs/lotsizing_hessian.jsonl`). At a boundary
  optimum that matrix is irrelevant. At the certified optimum for `T = 50`,
  seed 0, with 18 active band constraints:
  - the reduced Hessian on the tangent space of the active constraints is
    **positive definite** (`lambda_min = 0.80`);
  - the Hessian restricted to the 15 variables with no active incident
    constraint is also PD (0.83);
  - the multipliers of the active bands have magnitude at least 0.128.

  `T = 12` (seed 0) and `T = 32` (seed 1) give the same picture. So the
  optimum is a **strict, nondegenerate boundary minimizer**: second-order
  sufficient conditions and strict complementarity hold. The family violates
  the premise only through **interiority**; uniqueness was not checked.
  **Fix 1.2:** state that the optimum lies on the boundary (35-40% of periods
  idle, band active), and delete the indefiniteness argument.
- **Fits.**
  - The SCIP fit on `T = 4..9` uses 6 points with noisy step factors (3.0,
    3.1, 2.4, 2.2, 4.1). "Clearly better" (`R^2` 0.9945 against 0.9813) is
    weak; "better" suffices.
  - One period adds 3 SCIP variables, so per-period factors should not be
    compared with probe3's per-variable factors.
  - The prototype exponent "about `T^2.4`" depends on including the `T = 9`
    outlier (median 54,271). Without it, the fit on `T = 8, 10, ..., 128`
    gives 2.55. Report "2.4-2.6".
- **Conclusions.** The conclusions drawn in Section 6 follow once the premise
  wording is fixed: SCIP grows steeply with `T` and has large gaps from
  `T = 12`, while the prototype solves `T = 128` and 4 of 5 instances at
  `T = 256`.

---

## 5. Caveats and wording

Already appropriate:

- one solver version;
- prototype restricted to paths with problem-specific bounds;
- no interval arithmetic;
- SCIP's tolerance model;
- the machine-load caveat;
- the correction to PROGRAM.md's probe3 premise, which this review confirms
  rigorously for 9 instances.

Precise fixes beyond those above:

1. **Summary, prototype bullet.** "scales polynomially" is empirical: it rests
   on fitted exponents up to `n = 8192`. Add the known failures to the bullet
   itself, not only in 5.2 and 5.4: on amp 0.3, one of five seeds exceeds the
   cap at `n = 2048`, and no `theta` setting solves `n = 8192`. Costs are
   heavy-tailed across seeds, up to 1800 times the median.
2. **Time units.** Where CPU times are compared (Summary; 5.1: "milliseconds"
   versus minutes), state next to the comparison that SCIP times are CPU
   seconds, while prototype times are Python wall-clock seconds on a loaded
   machine.
3. **Section 7, "Prototype validity".** Mention that an independent method
   (this review) reproduces the optimal values and certificates on the tested
   instances. The bounds remain floating point.
4. **Section 7, "Other solvers and settings".** Correct the separator statement
   as in 3.2.
5. **Sections 1.3 and 2.** Replace "0.18" by "0.244" for amp 0.2. Correct the
   multistart failure count, and qualify the `n = 1000` row. Note that
   "not certified" means "certificate run hit the pair cap".
6. **Section 4.3.** Reword the rounding justification as in 1.4.

---

## What I verified myself, and commands run

All commands were run from `research-20260929/reviews/computation-review-checks/`
unless noted, with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, `nice`, and
`timeout`. Each run was a single process; the longest took about 3 minutes.
These are targeted checks only. No project-wide verification was run, and CI
status and logs were not inspected; this review makes no statement about CI.

| command | purpose | result |
|---|---|---|
| `python3 indep_grid_dp.py 4001` | independent bracket, amp 0.2, `n = 6, 10, 20, 50`, seeds 0-4 | `logs/indep_grid_dp_amp0.2.jsonl` |
| `python3 compare_proto.py 4001 '[25 instances]'`; `python3 -B compare_proto.py 8001 '[8 small instances]'` | prototype against independent bracket | max(proto LB - f* UB) = -7.1e-8 |
| `python3 adversarial_proto.py` | perturbed transfers, other `kappa`/`b`, all modes | no violation (worst -2.4e-12) |
| `python3 dp_rounding.py 8192` | DP rounding at `n = 8192` | 8.7e-17 measured, 8.7e-11 bound |
| `python3 indep_cert.py 2001 '[...]'` (two invocations) | independent certificates; restricted-box boundary checks | amp 0.2 certified; 9 amp 0.3 boundary cases certified |
| `python3 indep_grid_dp.py 2001 '[19 amp 0.3 non-certified instances, n <= 256]'` | multistart against true optimum | only `n = 100` and `256`, seed 4, missed |
| `python3 indep_grid_dp.py 8001 '[4 instances]'` | SCIP value against rigorous LB | SCIP 3.7e-6 to 6.5e-6 below |
| `python3 scip_rerun.py '[10 cases]'` | SCIP node counts, parameters, statistics | identical counts; parameters applied |
| `python3 lotsizing_hessian.py '[[50,0],[12,0],[32,1]]'` | lot-sizing second-order conditions | reduced Hessian PD |
| `python3 lotsizing_pair_adversarial.py` | lot-sizing pair bound | no violation (-1.0e-11) |
| `python3 test_bounds.py` (in `computation/`) | study's own tests | reproduced, all pass |

Inline Python over `computation/data/*.jsonl` and `tables.md` was used for:

- local growth exponents;
- the lot-sizing fit sensitivity;
- the certificate eigenvalue minima;
- lot-sizing consistency with SCIP;
- the `n = 12` SCIP statistics and progress log.

Python imports created `computation/__pycache__/`. I deleted it, so
`computation/` is as I found it.
