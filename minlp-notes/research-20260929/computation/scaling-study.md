# Scaling study: single-tree spatial B&B (SCIP) versus a chain DP branch and bound

Date: 2026-09-29. Status: computational evidence; revised after an
independent review (`../reviews/computation-review.md`, see section 9). Everything
here is floating-point computation with one solver version (SCIP 10.0 via
PySCIPOpt 6.2.1) on one machine. Nothing here is a proof of an asymptotic
statement.

## Summary

Question: on chain-structured (treewidth 1) nonconvex problems with a unique
nondegenerate global minimizer, does single-tree spatial B&B (SCIP) scale
exponentially in `n`, and does a decomposition-aware B&B scale polynomially?

- **SCIP's node count grows by about 5x per two variables on `n = 4..10`**
  (step factors 4-8). Probe3 chain, eps 1e-4, 5 seeds: the geometric mean is 220-240 nodes at
  `n = 4`, 1500-1800 at `n = 6`, 7100-7800 at `n = 8`, and 29,000-37,000 at
  `n = 10`, a factor of about 5 per two added variables. Most `n = 12`
  instances and all `n >= 14` instances are unsolved after 300 CPU s. At
  `n = 14`, even 1800 CPU s leave gaps of 3.6e-3 to 1e-2. The gap left after
  300 s grows to about 0.7 at `n = 20`, whereas the optimal values are about
  -0.07 to -0.48.
- **The growth persists under the six variations tried:** best-first
  search, OBBT at every node with a solved LP, the objective as one
  nonlinear constraint, optimality emphasis, all four combined, and an
  optimal start point. All give growth factors of 4.6-5.6 per two
  variables; they change only the constant. The
  optimal start point barely changes node counts, so the work is the proof
  of the lower bound.
- **Exponential or steep polynomial?** On the fully solved sizes
  (`n = 4..10`) an exponential and a power law of degree 5-6 fit equally
  well. The power law extrapolated from `n = 4..10` already underestimates
  `n = 14`: runs with 1.7-2.5 times the predicted total node count are
  still unsolved. At eps 1e-2, with solved sizes up to `n = 12`, the
  exponential fits better, and the unsolved `n = 14` runs again exceed the
  power-law prediction (by 1.7-2.2 times). The local power-law exponent
  `ln(ratio)/ln((n+2)/n)` rises with `n`: 4.7, 5.3, 7.7, 8.1 at eps 1e-2, and
  4.8, 5.4, 6.3 at eps 1e-4. A fixed-degree polynomial would keep it
  constant. This is evidence for exponential growth, not proof: 5 seeds, a
  narrow range, and single seeds deviate from the geometric mean by up to
  3x.
- **The premise holds on the amp 0.2 family.** A certificate computed with
  the prototype shows that all 75 instances (`n` up to 1000, 5 seeds) have a
  unique, interior, nondegenerate global minimizer, while the sum is
  nonconvex on the box. SCIP's growth there is the same as on probe3.
  Correction to PROGRAM.md: probe3 itself (amp 0.3) has boundary global
  minimizers for some seeds from `n = 12` on, and for all 5 seeds at
  `n = 1000`. In this study that was evidence only (eps-optimal points with
  coordinates at ±1; the certificate runs hit the pair cap). The review
  proved it rigorously for 9 instances (section 1.3).
- **A chain DP branch and bound with valid bounds scales polynomially in
  these experiments** (fitted exponents up to `n = 8192`, not a proof).
  It uses cell partitions per variable, min-sum DP with min-marginal pruning,
  and exact reparametrization of the pieces (Lagrangian plus quadratic
  transfers). With the same absolute tolerance, it solves every amp 0.2
  instance up to `n = 8192`; the median is below 0.1 s up to `n = 128` and
  13-19 s at `n = 8192`. Work grows as about `n^1.6-1.8` (`n^2.4` on probe3,
  `T^2.4-2.6` on lot-sizing). It has failures and heavy tails: on probe3
  (amp 0.3), one of five seeds exceeds the cap of pair bounds per iteration
  at `n = 2048`, no refinement setting solves `n = 8192`, and the cost across
  seeds reaches up to 1800 times the median. **Time units differ:** SCIP
  times are CPU seconds (apparently user time only), while prototype times
  are Python wall-clock seconds on a loaded machine. Its optimal values agree with SCIP's to within SCIP's
  feasibility tolerance (at most 6.9e-6, SCIP always lower; `F` evaluated at
  SCIP's points confirms this). The reparametrization is essential: with
  plain constant cell bounds the DP fails at eps 1e-6 from `n = 10`.
- **Application-like family (lot-sizing with economies of scale).** SCIP's
  node count grows about 2.8 times per period (`T = 4..9`), and no instance
  with `T >= 12` is solved in 300 s. The prototype solves `T = 128` in
  21-25 s (wall clock). The optima batch production, so they lie on the
  boundary. At the three optima checked they are strict, nondegenerate boundary
  minimizers (positive definite reduced Hessian, strict complementarity), so
  the family fails the premise only through interiority.
- **Main caveats.** One solver version; bounds validated by argument,
  floating-point margins and sampling, not by interval arithmetic; the
  prototype handles paths only; and an unexplained collapse of SCIP's node
  rate late in the search at `n = 12` (section 3.2).


## 1. Instances

### 1.1 Probe3 chain family (`instances.py`)

    F(x) = sum_{i=1}^{n} (x_i^2 - kappa x_i^4 + c_i x_i) + b sum_{i=1}^{n-1} x_i x_{i+1},
    x in [-1, 1]^n,   kappa = 0.1,   b = 0.8,
    c = numpy.random.default_rng(seed).uniform(-amp, amp, n).

- `amp = 0.3` is exactly the probe3 instance of `../scratch/probe3.py` and
  PROGRAM.md (called "probe3" below). `amp = 0.2` uses the same random stream,
  so its `c` is probe3's `c` times 2/3. Instances are nested in `n`: the
  instance for `n` is a prefix of the instance for any larger `n` with the
  same seed.
- Seeds 0-4 for the main runs, seeds 0-2 for the solver-setting variants.
- SCIP formulation (`instances.build_scip`): probe3's formulation, variables
  `x_i in [-1, 1]`, free `t_i`, constraints
  `t_i >= x_i^2 - 0.1 x_i^4 + 0.8 x_i x_{i+1}` (last one without the product),
  objective `sum t_i + sum c_i x_i`. Variant `single` instead uses one free
  variable `t` and one constraint `t >= F(x)`.
- Structure: the interaction graph is a path (treewidth 1). Every constraint
  is nonconvex (its Hessian `[[2 - 1.2 x_i^2, 0.8], [0.8, 0]]` is indefinite).
  The Hessian of `F` is `diag(2 - 1.2 x_i^2) + 0.8 (off-diagonal)`. In the
  Loewner order it is smallest at the corners, so its smallest eigenvalue over
  the box is that of the constant tridiagonal matrix with diagonal 0.8 and
  off-diagonal 0.8, which is negative for every `n >= 3` (for `n = 2` it is
  exactly 0, so the `n = 2` instances are convex on the box).

### 1.2 Lot-sizing chain (`lotsizing.py`), the application-like family

Production planning with economies of scale and overtime:

    periods t = 1..T, inventory s_t in [-3, 3] (negative = backlog), s_0 = 0,
    production p_t = s_t - s_{t-1} + d_t in [0, 2.5],  d_t ~ U(0.5, 1.5) (seeded),
    minimize  sum_t g(p_t) + 0.5 sum_t s_t^2,
    g(p) = p - 0.6 p^2 + 0.15 p^3.

`g` is increasing (`g' >= 0.2`), concave for `p < 4/3` (economies of scale) and
convex beyond (overtime). SCIP model: variables `p_t, s_t, z_t, w`, linear
balances `s_t = s_{t-1} + p_t - d_t`, nonconvex constraints `z_t >= g(p_t)`,
convex constraint `w >= 0.5 sum s_t^2`, objective `sum z_t + w`. In the
inventory variables the problem is a chain with unary pieces `0.5 s_t^2` and
pair pieces `g(s_t - s_{t-1} + d_t)` on the band `0 <= s_t - s_{t-1} + d_t <= 2.5`.

This family does **not** have an interior minimizer. The optimal plans batch
production: 35-40% of the periods have `p_t = 0`, so the band constraint is
active there. The optima are still strict, nondegenerate boundary
minimizers (`lotsizing_kkt_check.py`, `data/lotsizing_kkt_check.jsonl`):

| T | seed | active bands | smallest eigenvalue of the reduced Hessian | smallest active multiplier | largest inactive multiplier |
|---|---|---|---|---|---|
| 50 | 0 | 18 | 0.80 | 0.128 | 4e-7 |
| 12 | 0 | 4 | 0.80 | 0.187 | 4e-8 |
| 32 | 1 | 12 | 0.85 | 0.228 | 8e-8 |

The reduced Hessian is taken on the tangent space of the active bands.
(The first version of this note cited the indefinite *full* Hessian, for
example -2.50 at `T = 50`, seed 0. At a boundary point that matrix does not
decide nondegeneracy.) So the family fails the premise only through
interiority; uniqueness was not checked. It is included as a realistic chain
with boundary optima.

Modelling choices: there is no terminal-inventory condition (a final backlog
is only penalized by `0.5 s_T^2`). The SCIP model puts the whole holding cost
in one convex constraint `w >= 0.5 sum s_t^2`, so SCIP's constraint graph links
all periods, although the problem is a chain in the `s` variables.

### 1.3 Does each instance have a unique interior nondegenerate minimizer?

Method: section 4.4 (certificate), plus multistart. Columns: number of
seeds (out of 5) with a certificate; number of seeds where multistart found
more than one local minimizer; the smallest eigenvalue of the full Hessian at
the best point found (minimum over seeds); the smallest eigenvalue over the
box (it is the same for all seeds); and the largest `|x_i|` at the best point.

"Not certified" means only that the capped certificate run stopped at the
limit of pair bounds per iteration, which happened in all 24 non-certified
cases. It is not a proof that the premise fails. The best point is the
multistart point, except in the `n = 1000` row. There multistart missed the
optimum for 4 of 5 seeds, so that row was recomputed at the prototype's
eps-optimal points (eps 1e-6; `recheck_n1000.py`,
`data/recheck_n1000_amp0.3.jsonl`). For points on the boundary, the full
Hessian eigenvalue says nothing about nondegeneracy.

| amp | n | certified unique+interior | multistart: instances with >1 local min | min lambda_min(H) at x* | lambda_min(H) over box | max abs x*_i |
|---|---|---|---|---|---|---|
| 0.2 | 2 | 5/5 | 0 | 1.192 | -0.000 | 0.106 |
| 0.2 | 4 | 5/5 | 0 | 0.653 | -0.494 | 0.237 |
| 0.2 | 6 | 5/5 | 0 | 0.487 | -0.642 | 0.284 |
| 0.2 | 8 | 5/5 | 0 | 0.429 | -0.704 | 0.290 |
| 0.2 | 10 | 5/5 | 0 | 0.391 | -0.735 | 0.298 |
| 0.2 | 12 | 5/5 | 0 | 0.370 | -0.754 | 0.301 |
| 0.2 | 14 | 5/5 | 0 | 0.365 | -0.765 | 0.301 |
| 0.2 | 16 | 5/5 | 0 | 0.362 | -0.773 | 0.339 |
| 0.2 | 18 | 5/5 | 0 | 0.339 | -0.778 | 0.374 |
| 0.2 | 20 | 5/5 | 0 | 0.331 | -0.782 | 0.373 |
| 0.2 | 32 | 5/5 | 0 | 0.329 | -0.793 | 0.373 |
| 0.2 | 64 | 5/5 | 0 | 0.329 | -0.798 | 0.373 |
| 0.2 | 100 | 5/5 | 0 | 0.329 | -0.799 | 0.373 |
| 0.2 | 256 | 5/5 | 0 | 0.298 | -0.800 | 0.419 |
| 0.2 | 1000 | 5/5 | 1 | 0.265 | -0.800 | 0.450 |
| 0.3 | 2 | 5/5 | 0 | 1.182 | -0.000 | 0.160 |
| 0.3 | 4 | 5/5 | 0 | 0.576 | -0.494 | 0.370 |
| 0.3 | 6 | 5/5 | 0 | 0.366 | -0.642 | 0.464 |
| 0.3 | 8 | 5/5 | 0 | 0.308 | -0.704 | 0.480 |
| 0.3 | 10 | 5/5 | 1 | 0.252 | -0.735 | 0.505 |
| 0.3 | 12 | 4/5 | 1 | -0.679 | -0.754 | 1.000 |
| 0.3 | 14 | 4/5 | 1 | -0.679 | -0.765 | 1.000 |
| 0.3 | 16 | 3/5 | 2 | -0.679 | -0.773 | 1.000 |
| 0.3 | 18 | 3/5 | 1 | -0.680 | -0.778 | 1.000 |
| 0.3 | 20 | 3/5 | 1 | -0.680 | -0.782 | 1.000 |
| 0.3 | 32 | 3/5 | 1 | -0.680 | -0.793 | 1.000 |
| 0.3 | 64 | 3/5 | 1 | -0.680 | -0.798 | 1.000 |
| 0.3 | 100 | 2/5 | 2 | -0.627 | -0.799 | 1.000 |
| 0.3 | 256 | 1/5 | 5 | -0.694 | -0.800 | 1.000 |
| 0.3 | 1000 | 0/5 | 5 | -0.741 (recomputed) | -0.800 | 1.000 |

Findings:

- **amp 0.2: certified for every `n` and seed tested (75 instances,
  `n <= 1000`).** The certificate gave a smallest eigenvalue of at least
  0.244 for the Hessian lower bound `M` on the localization box (0.181 for
  the certified amp 0.3 instances). The review reproduced these certificates
  with an independent grid DP (0.245 at `n = 1000`, seed 3). The sum is nonconvex on the box for
  every `n >= 3`, with a smallest eigenvalue over the box of -0.49 to -0.80.
  At `n = 1000`, multistart found several local minimizers for one seed. The
  certificate shows that the global one is still unique and interior.
- **amp 0.3 (probe3 as in PROGRAM.md): the premise fails for some seeds from
  `n = 12` on.** Certified: all seeds up to `n = 10`; 4/5 at `n = 12, 14`;
  3/5 at `n = 16-64`; 2/5 at `n = 100`; 1/5 at `n = 256`; 0/5 at `n = 1000`.
  For the non-certified seeds, the eps-optimal point certified by the
  prototype (eps = 1e-6) has 2-27 coordinates at +1 or -1 (for example
  `n = 12`, seed 4: 0-based indices 3-7; at `n = 1000`, 4-27 per seed). In this
  study, that the *global* minimizer is on the boundary was therefore
  evidence, not a certificate. The review proved it for 9 instances: a
  rigorous lower bound of `min F` over `[-0.99, 0.99]^n` exceeds a feasible
  value by 1.6e-3 to 3.2e-2 (`n = 12`, seed 4; `n = 16`, seeds 0 and 4;
  `n = 100`, seed 4; `n = 1000`, seeds 0-4;
  `../reviews/computation-review-checks/logs/indep_cert.jsonl` and
  `indep_boundary_n1000.jsonl`). In the cases checked
  (`n = 16`, seeds 0 and 4), the local minimizer reached from `x = 0` is worse
  by 6e-3 to 7e-3. In 6 instances (`n = 100` and `256`,
  seed 4; `n = 1000`, seeds 0, 2, 3, 4), 250-start multistart missed the
  global optimum, by 9.8e-4 to 1.1e-2. The prototype found it, and its
  values match the review's independent method to 1.4e-14. (The first
  version said 3 instances; it compared multistart only with the capped
  certificate run.) The mechanism: where consecutive `c_i`
  alternate in sign with `|c_i|` near 0.3, the alternating corner pattern
  costs about `0.9 - 0.8 - |c_i|` per coordinate, which beats the interior.
  PROGRAM.md's statement that probe3 has a unique interior minimizer is
  therefore true for `n <= 10` (all five seeds), and for most but not all
  seeds at `n = 12-64`.
- `n = 2` is convex on the box (smallest eigenvalue 0), so it is not a
  nonconvex instance.


## 2. SCIP setup

- SCIP 10.0 through PySCIPOpt 6.2.1, single thread, default settings unless
  stated. Every run sets `limits/absgap = eps`, `limits/gap = 0`,
  `limits/time = 300` (or 1800 for the extended runs), and
  `timing/clocktype = 1` (CPU time). Feasibility tolerances are SCIP defaults
  (`numerics/feastol = 1e-6`).
- Variants (probe3, amp 0.3, eps 1e-4, seeds 0-2, `run_scip.py`):

  | name | change |
  |---|---|
  | `default` | none |
  | `single` | objective as one nonlinear constraint `t >= F(x)` |
  | `bestfirst` | `nodeselection/bfs/stdpriority = 10^7`, `nodeselection/bfs/maxplungedepth = 0` (pure best-bound selection) |
  | `obbt` | `propagating/obbt/freq = 1`: OBBT is called at every node with a solved LP (default 0 = root only). At `n = 6` it ran at 228 of 320 nodes, against 2 calls in default. It keeps its per-call LP-iteration limit and `onlynonconvexvars = TRUE`. |
  | `emph_opt` | `setEmphasis(OPTIMALITY)`: changes 64 parameters, mainly aggressive separation (for example RLT every 20 levels, interminor intersection cuts at the root; 44 interminor cuts applied at `n = 6`) |
  | `combo` | `single` + `emph_opt` + `bestfirst` + `obbt` together |
  | `warm` | the optimal point (local minimizer from `x = 0`) is passed to SCIP with `addSol` before solving |

  `setSeparating(AGGRESSIVE)` was also tried in a smoke test (n = 4, 6); it
  produced node counts identical to `emph_opt`, so it was dropped.
- Machine: 36 cores, shared with another agent's jobs; load average between
  17 and 130 during the runs. SCIP runs used 3-6 parallel workers per batch,
  with up to four batches at a time.
  A first batch used SCIP's default wall-clock time limit; because the load
  made wall-clock limits unreliable, all SCIP data used below were rerun with
  CPU-time limits. The first batch (`data/wallclock/`) is used only for a
  determinism check. A partial wall-clock batch for amp 0.2 was stopped and
  deleted.

## 3. SCIP results

### 3.1 Default settings

In the tables, "+" marks a run stopped by the time limit, where the node
count is only a lower bound. "Solved" means SCIP stopped with
`absgap <= eps` (status `optimal` or `gaplimit`).

Probe3 (amp 0.3), eps 1e-4, CPU limit 300 s:

| n | solved | nodes per seed | geo. mean nodes (solved) | median CPU s | max final gap (unsolved) |
|---|---|---|---|---|---|
| 2 | 5/5 | 1 11 1 11 29 | 5 | 0.0 | - |
| 4 | 5/5 | 217 351 141 234 301 | 238 | 0.3 | - |
| 6 | 5/5 | 1055 2941 1889 1511 2267 | 1822 | 1.7 | - |
| 8 | 5/5 | 4447 8991 7141 4669 21281 | 7773 | 6.1 | - |
| 10 | 5/5 | 28954 43762 21577 22604 117011 | 37311 | 38.5 | - |
| 12 | 1/5 | 92370+ 201782+ 79804+ 108186+ 89085 | 89085 | 300.6 | 5.79e-03 |
| 14 | 0/5 | 131857+ 135560+ 138695+ 128148+ 134370+ | - | 300.0 | 7.90e-02 |
| 16 | 0/5 | 98777+ 100303+ 85766+ 85179+ 102719+ | - | 300.0 | 2.39e-01 |
| 18 | 0/5 | 75067+ 83011+ 76382+ 78689+ 84805+ | - | 300.0 | 4.56e-01 |
| 20 | 0/5 | 70330+ 73553+ 68620+ 71700+ 72633+ | - | 300.0 | 6.94e-01 |

Amp 0.2 (certified unique interior minimizer), eps 1e-4:

| n | solved | nodes per seed | geo. mean nodes (solved) | median CPU s | max final gap (unsolved) |
|---|---|---|---|---|---|
| 2 | 5/5 | 1 1 1 1 1 | 1 | 0.0 | - |
| 4 | 5/5 | 221 291 211 171 211 | 218 | 0.2 | - |
| 6 | 5/5 | 1161 2029 1168 1836 1521 | 1504 | 0.9 | - |
| 8 | 5/5 | 5258 6783 7583 7484 8815 | 7084 | 6.0 | - |
| 10 | 5/5 | 23136 28181 30622 19975 52951 | 29169 | 142.4 | - |
| 12 | 0/5 | 82412+ 115665+ 96501+ 78359+ 172042+ | - | 300.5 | 8.18e-03 |
| 14 | 0/5 | 151100+ 132559+ 116274+ 123444+ 149927+ | - | 300.0 | 6.07e-02 |
| 16 | 0/5 | 86982+ 94343+ 82714+ 84182+ 109783+ | - | 300.0 | 2.50e-01 |
| 18 | 0/5 | 87779+ 79031+ 82460+ 71982+ 84072+ | - | 300.0 | 4.72e-01 |
| 20 | 0/5 | 71087+ 75860+ 66292+ 70108+ 74390+ | - | 300.0 | 7.00e-01 |

With eps 1e-6 the node counts are almost the same: per instance they are
at most 2% higher for `n = 8, 10`, and at most 25-43% higher for
`n = 4, 6` (tables in `tables.md`). This is consistent with SCIP's `absgap`
acting only as a stopping rule for the whole solve, not as a pruning
tolerance.

Growth fits, by least squares on the log of the geometric mean over 5 seeds,
using only sizes where all 5 seeds were solved (from `n = 4`):

| family | eps | sizes | exponential fit: factor per +2 variables (R^2) | power-law fit: exponent (R^2) |
|---|---|---|---|---|
| probe3 (amp 0.3) | 1e-4 | 4..10 | 5.27 (0.9943) | 5.42 (0.9944) |
| probe3 (amp 0.3) | 1e-6 | 4..10 | 5.09 (0.9961) | 5.30 (0.9927) |
| amp 0.2 | 1e-2 | 4..12 | 5.20 (0.9983) | 5.97 (0.9837) |
| amp 0.2 | 1e-3 | 4..10 | 5.46 (0.9905) | 5.56 (0.9986) |
| amp 0.2 | 1e-4 | 4..10 | 5.07 (0.9947) | 5.30 (0.9961) |
| amp 0.2 | 1e-6 | 4..10 | 4.99 (0.9944) | 5.25 (0.9962) |
| lot-sizing | 1e-4 | T = 4..9 | 7.73, i.e. 2.78 per period (0.9945) | 6.28 (0.9813) |

Local power-law exponents (after review; `tables.md`). A fixed-degree
polynomial keeps them constant, and an exponential makes them grow like
`c / ln((n+2)/n)`:

| family, eps | step n -> n+2 | ratio | local exponent | exact 5x-per-2 exponential |
|---|---|---|---|---|
| amp 0.2, eps 1e-4 | 4 -> 6 | 6.90 | 4.77 | 3.97 |
| amp 0.2, eps 1e-4 | 6 -> 8 | 4.71 | 5.39 | 5.59 |
| amp 0.2, eps 1e-4 | 8 -> 10 | 4.12 | 6.34 | 7.21 |
| amp 0.2, eps 1e-2 | 4 -> 6 | 6.69 | 4.69 | 3.97 |
| amp 0.2, eps 1e-2 | 6 -> 8 | 4.58 | 5.29 | 5.59 |
| amp 0.2, eps 1e-2 | 8 -> 10 | 5.58 | 7.70 | 7.21 |
| amp 0.2, eps 1e-2 | 10 -> 12 | 4.40 | 8.13 | 8.83 |
| amp 0.3, eps 1e-4 | 4 -> 6 | 7.67 | 5.02 | 3.97 |
| amp 0.3, eps 1e-4 | 6 -> 8 | 4.27 | 5.04 | 5.59 |
| amp 0.3, eps 1e-4 | 8 -> 10 | 4.80 | 7.03 | 7.21 |

The exponents rise with `n` in all three series and track the exponential
pattern. The raw step ratios fall (6.9, 4.7, 4.1 at amp 0.2, eps 1e-4),
which alone would suggest sub-exponential growth. But they fall more slowly
than any fixed-degree polynomial allows, and that is what the rising local
exponent measures. The caveats are 5 seeds and a narrow range.

On the fully solved ranges the two models fit about equally well. The
exponential fits better on lot-sizing and at eps 1e-2 (the longest solved
range); the power law fits slightly better at eps 1e-3. A factor of about 5
per two variables means about 2.25 per variable. `n = 2` is excluded from
the fits because those instances are convex on the box.

### 3.2 Beyond the solved range

Extended runs, CPU limit 1800 s. The last column gives the node count
predicted for that `n` by the 300 s fits of 3.1 (amp and eps matching):

| amp | n | seed | status | nodes | CPU s | final gap | 300 s-fit prediction (nodes) |
|---|---|---|---|---|---|---|---|
| 0.2 | 12 | 0 | timelimit | 82977 | 1801 | 7.2e-03 | 166375 (exp) / 67293 (pow) |
| 0.2 | 12 | 1 | gaplimit | 115937 | 696 | 1.2e-05 | 166375 (exp) / 67293 (pow) |
| 0.2 | 12 | 2 | timelimit | 97047 | 1801 | 7.3e-03 | 166375 (exp) / 67293 (pow) |
| 0.2 | 14 | 0 | timelimit | 331425 | 1804 | 8.1e-03 | 844291 (exp) / 152433 (pow) |
| 0.2 | 14 | 1 | timelimit | 379826 | 1803 | 6.1e-03 | 844291 (exp) / 152433 (pow) |
| 0.2 | 14 | 2 | timelimit | 367813 | 1801 | 1.0e-02 | 844291 (exp) / 152433 (pow) |
| 0.3 | 12 | 0 | timelimit | 93012 | 1800 | 3.6e-03 | 213427 (exp) / 84359 (pow) |
| 0.3 | 12 | 1 | gaplimit | 203755 | 1426 | 6.2e-05 | 213427 (exp) / 84359 (pow) |
| 0.3 | 12 | 2 | timelimit | 80553 | 1800 | 4.8e-03 | 213427 (exp) / 84359 (pow) |
| 0.3 | 14 | 0 | timelimit | 346944 | 1802 | 7.2e-03 | 1124811 (exp) / 194662 (pow) |
| 0.3 | 14 | 1 | timelimit | 435434 | 1800 | 3.6e-03 | 1124811 (exp) / 194662 (pow) |
| 0.3 | 14 | 2 | timelimit | 326565 | 1801 | 8.0e-03 | 1124811 (exp) / 194662 (pow) |

- At `n = 14`, all six runs processed 327k-435k nodes and still had gaps of
  3.6e-3 to 1.0e-2. That is 1.7-2.5 times the total predicted by the power
  law fitted on `n = 4..10`, so the power-law extrapolation already
  underestimates the work at `n = 14`. The exponential prediction
  (0.84-1.1 million) is consistent with the data. The prediction is a
  geometric mean, while single seeds deviate from it by up to 3.1 times at
  `n = 10`. The comparison is cleanest for amp 0.2: seeds 0-2 were at
  0.79-1.05 times the `n = 10` geometric mean, and at 2.2-2.5 times the
  power-law prediction at `n = 14`, still unsolved. For amp 0.3, seeds 0-2
  were at 0.58-1.17 and 1.7-2.2 times respectively.
- The loose-tolerance runs point the same way. At eps 1e-2 all sizes up to
  `n = 12` are solved, and the exponential fit is better (R^2 0.998 against
  0.984). At `n = 14`, all five seeds are unsolved after 200k-258k nodes, with
  gaps of 0.017-0.040, still 2-4 times the target. The power law fitted on
  `n = 4..12` predicts 119k nodes for `n = 14`, and the exponential fit
  predicts 391k.
- At `n = 12`, two of the six extended runs finished. They needed 116k and
  204k nodes, above the power-law predictions (67k, 84k) and below the
  exponential ones (166k, 213k).
- **Throughput collapse (unexplained).** At `n = 12`, SCIP's node rate drops
  by a factor of about 50 late in the search. On amp 0.3, seed 0, SCIP
  processed 90,000 nodes in 71.5 s (gap 4.7%), then only 2,348 nodes in
  the next 129 s; the 1800 s run ended with 93,012 nodes, against 92,370
  after 300 s. SCIP's statistics attribute only about 50 s of 280 s to LP
  solving, nonlinear constraint handling, and node switching; heuristics,
  propagators, separators, conflict analysis and NLP solves each took at
  most 1.4 s (`logs/scip_stats_n12_amp0.3_seed0_tl280.txt`,
  `logs/scip_display_n12_amp0.3_seed0.log`). The solved `n = 12` runs pass
  through the same slow phase: amp 0.3, seed 1 had 201,782 nodes at 300 s
  and finished at 1426 s with 203,755. The cause was not found. It inflates
  SCIP's times at `n = 12` and makes time-limited node counts there
  unreliable. It does not affect the node counts of solved runs, which are
  what the fits use.
- For `n >= 14`, the gap left after 300 s grows steadily with `n`. With
  default settings and eps 1e-4 the largest remaining gaps were 0.06-0.08
  at `n = 14`, 0.24-0.25 at `n = 16`, 0.46-0.47 at `n = 18`, and about 0.7 at
  `n = 20`. The optimal values are between -0.05 and -0.48 for these sizes,
  so SCIP's dual bound is not yet useful. At eps 1e-2 the gap after 300 s is
  1.1 at `n = 24`.

### 3.3 Robustness to solver settings

Probe3 (amp 0.3), eps 1e-4, seeds 0-2, CPU limit 300 s. Each entry is the
geometric-mean node count when all three seeds were solved:

| variant | n=2 | n=4 | n=6 | n=8 | n=10 | n=12 | n=14 | factor per +2 (fit) |
|---|---|---|---|---|---|---|---|---|
| default | 2 | 221 | 1803 | 6585 | 30125 | 0/3 solved; gap<= 5.8e-03 | 0/3 solved; gap<= 6.8e-02 | 4.98 (R^2 0.989, n=4..10) |
| single | 1 | 123 | 748 | 2930 | 15601 | 0/3 solved; gap<= 7.6e-02 | 0/3 solved; gap<= 2.9e-01 | 4.90 (R^2 0.997, n=4..10) |
| bestfirst | 2 | 109 | 749 | 2850 | 14301 | 67715 | 0/3 solved; gap<= 5.1e-02 | 4.86 (R^2 0.997, n=4..12) |
| obbt | 2 | 63 | 340 | 1315 | 5653 | 32368 | 0/3 solved; gap<= 1.4e-01 | 4.61 (R^2 0.998, n=4..12) |
| emph_opt | 2 | 220 | 1847 | 7091 | 25341 | 0/3 solved; gap<= 1.0e-02 | 0/3 solved; gap<= 9.3e-02 | 4.75 (R^2 0.983, n=4..10) |
| combo | 1 | 36 | 245 | 1192 | 6589 | 0/3 solved; gap<= 4.1e-02 | 0/3 solved; gap<= 2.5e-01 | 5.61 (R^2 0.998, n=4..10) |
| warm | 1 | 221 | 1803 | 6565 | 27848 | 0/3 solved; gap<= 5.7e-03 | 0/3 solved; gap<= 7.2e-02 | 4.86 (R^2 0.988, n=4..10) |

Determinism check: 144 solved runs repeated with identical node counts, 0 differ (first batch with wall-clock limits vs. second batch with CPU-time limits).

Every variant shows the same growth, a factor of 4.6-5.6 per two variables.
The settings change the constant: `obbt` and `combo` need 3.5-6 times fewer
nodes than `default`, but each node is 2-15 times slower (median nodes per
CPU second at `n = 10-14`: `default` 310-610, `obbt` 110-270, `single` 46-180,
`combo` 43-130). As a result, no variant solves `n = 14`, and only
`bestfirst` and `obbt` solve `n = 12`. The warm start (optimal point given)
leaves node counts identical for `n <= 6`, and changes them by -27% to +19%
for `n = 8, 10`.
SCIP finds the optimum early; the work is the proof of the lower bound.


## 4. The decomposition-aware prototype (`chain_bb.py`)

### 4.1 Algorithm

The prototype solves `min F(x) = sum_i phi_i(x_i) + sum_e psi_e(x_e, x_{e+1})`
over a box, with optional pairwise constraints `(x_e, x_{e+1}) in G_e`.

1. Each variable's interval is partitioned into cells (initially one cell).
2. Every iteration computes a constant lower bound `u_i(a)` of the unary
   piece on every cell `a`, and a constant lower bound `P_e(a, a')` of the
   pair piece on every product of adjacent cells (`+inf` if the product misses
   `G_e`). The count of these pair bounds is the work measure ("pair bounds").
3. Forward and backward min-sum dynamic programming over the path gives the
   DP bound `LB_dp = min over cell sequences of sum u + sum P`, and for every
   cell its min-marginal `m_i(a)`, the smallest sequence sum through `a`.
4. Upper bound: local optimization (L-BFGS-B; for lot-sizing in production
   space) started at the midpoints of the cells on the DP argmin path.
   `UB` is the best objective value of a feasible point found.
5. A cell with `m_i(a) >= UB - eps` is removed, and its marginal is kept in
   `pruned_min`. Every other cell is bisected (`theta = 1`; section 5.4 tests
   partial refinement).
6. Stop when `min(LB_dp, pruned_min) >= UB - eps`.

Piece bounds use a **reparametrization** ("transfers"). For each edge `e` and
each endpoint, a univariate function `rho x^2 - alpha x` is added to `psi_e`
and subtracted from that endpoint's unary piece, so the sum of the pieces is
still exactly `F`. Modes:

- `plain`: no transfers. Constant cell bounds then have a first-order copy
  error: each copy of `x_i` may take a different value inside the cell.
- `affine`: linear transfers (Lagrange multipliers) chosen so that every pair
  piece is stationary at the incumbent `xhat`. Then every unary piece is
  stationary at an interior stationary `xhat` too, and the copy error becomes
  second order.
- `quad` (probe3): additionally `rho = |b|/2` on both sides, which makes every
  pair piece `0.4 (x + y)^2 - alpha x - beta y` convex and minimized at `xhat`.
  Near the minimizer the unary pieces `0.2 x^2 - 0.1 x^4 + ...` (interior
  variables) stay convex for `|x| < 0.577`.
- `split` (lot-sizing): `rho` from an edge-wise PSD splitting of the
  tridiagonal Hessian of `F` at `xhat` (sequential Schur complements; each pair
  block gets `[[u, b], [b, b^2/u]]` with `u = 0.7 * (remaining diagonal)`). An
  edge gets no quadratic transfer when the recursion meets a non-positive
  pivot. For pairwise constraints active at `xhat` (lot-sizing bands), the
  KKT multipliers, obtained by a backward recursion along the chain, are also
  shifted into the pair pieces, so that the unary pieces stay stationary.

Piece bounds:

- Probe3 unary `(1 - Q) x^2 - 0.1 x^4 + (c + L) x` on `[p, q]`: second-order
  Taylor expansion at the midpoint with the Lagrange remainder bounded by
  `inf phi'' = 2(1 - Q) - 1.2 max(p^2, q^2)`. The quadratic model is minimized
  exactly over the interval. The bound is the minimum of this over 16 equal
  sub-intervals (`unary_sub = 16`).
- Probe3 pair `0.8 x y + rho_L x^2 - alpha x + rho_R y^2 - beta y` on a box:
  exact minimum of a bivariate quadratic over a box (`quad_box_min`). The
  candidates are the corners, the clipped vertex on each edge, and the
  interior stationary point if the Hessian is positive definite.
- Lot-sizing unary `0.5 s^2 - Q s^2 + L s`: exact (quadratic).
- Lot-sizing pair `g(y - x + d) + transfers` on a box intersected with the
  production band: second-order Taylor expansion at the box center, with
  `g''(xi) >= g''(p_lo)` (`g''` is increasing and `p_lo` is the smallest
  production in the box). The quadratic model is minimized exactly over the
  polygon `box ∩ band` (`quad_band_min`: vertices, clipped edge minimizers,
  interior stationary point). The bound is `+inf` if the box misses the band.

### 4.2 Validity of the lower bound

Claim: at every iteration, `LB = min(LB_dp, pruned_min) <= F(x)` for every
feasible `x`, up to floating-point rounding (see 4.3). At termination,
`LB >= UB - eps`, and `UB` is the value of a feasible point, so that point is
eps-optimal and `[LB, UB]` contains the optimal value.

Argument.

1. *Identity.* For any transfer parameters,
   `sum_i phi~_i(x_i) + sum_e psi~_e(x_e, x_{e+1}) = F(x)` for all `x`, because
   every transfer term is added to one piece and subtracted from another with
   the same coefficients. Validity therefore never depends on how the
   transfers are chosen (the incumbent, the multipliers, the Hessian split);
   only tightness does.
2. *Piece bounds.* Each routine returns a number at most the minimum of its
   piece over the cell (or cell product intersected with `G_e`):
   - The Taylor bounds: for `z` in the cell,
     `phi(z) = phi(m) + phi'(m)(z - m) + 0.5 phi''(xi)(z - m)^2` with `xi` in
     the cell and `phi''(xi) >= H_lo`. In the lot-sizing pair the second-order
     term is `0.5 g''(xi) (dy - dx)^2 + rho_L dx^2 + rho_R dy^2`, and
     `(dy - dx)^2 >= 0`. The right-hand side is a quadratic lower model whose
     exact minimum over the cell is computed.
   - Exact minimization of a quadratic over a box or convex polygon: a
     minimizer exists by compactness. If one lies in the interior with a
     positive definite Hessian, it is the stationary point. Otherwise some
     minimizer lies on the boundary; the reason is that an interior minimizer
     with a singular Hessian lies on a line of minimizers that reaches the
     boundary, and an indefinite quadratic has no interior minimizer. On an
     edge the restriction is a univariate quadratic, minimized at an endpoint
     (a vertex) or at its clipped vertex. The routines enumerate exactly
     these candidates.
     Sampling tests (`test_bounds.py`) found no violation in 2000-4000 random
     cases per routine.
3. *DP.* If every coordinate of a feasible `x` lies in a current cell `a_i`,
   then by 1 and 2, `F(x) >= sum u_i(a_i) + sum P_e(a_e, a_{e+1}) >= LB_dp`, and
   `F(x) >= m_i(a_i)` for every `i`.
4. *Removed cells.* Cells are closed and neighbours share endpoints, so a
   coordinate can lie in a removed cell and a surviving cell at once. Take a
   feasible `x` that is not covered by the product of the current cells, and
   let `t` be the first iteration after which it is no longer covered.
   Bisection preserves coverage, so at iteration `t` every coordinate of `x`
   lay in a current cell, and some coordinate `x_j` had all its containing
   cells removed at `t`. By 3, `F(x) >= m_j(a)` for such a cell `a`, computed
   at iteration `t`, and `m_j(a) >= pruned_min`.
5. Hence `F(x) >= min(LB_dp, pruned_min)` for every feasible `x`. Removed cells
   have `m >= UB_then - eps >= UB_now - eps`, so the stopping test
   `min(LB_dp, pruned_min) >= UB - eps` certifies eps-optimality.

Termination (informal): all surviving cells are bisected each iteration; the
piece bounds converge to the exact piece minima as widths go to 0, and so
does the copy error; the DP argmin path concentrates near global minimizers,
so the local search started there converges to the optimal value. Every
prototype run in this study stopped with `LB >= UB - eps` except those that hit
an explicit cap on pair bounds per iteration; these are reported as unsolved.

### 4.3 Floating point

The bounds are not computed in interval arithmetic.

- *Piece bounds.* Each piece bound subtracts a safety margin:
  `1e-13 (1 + scale)` for the Taylor and box routines, and
  `1e-11 (1 + scale)` for the polygon routine, where `scale` is the sum of
  the absolute values of the terms. Each bound is a handful of operations, so
  its rounding error is a small multiple of `u * scale` (`u = 1.1e-16`), well
  inside the margin. The margins are subtracted, so they add safety, not
  error. They do not cover the rounding of the DP sums.
- *DP sums.* The forward DP adds two terms per edge and takes exact minima.
  Recursive summation along the chain therefore has error at most
  `u * sum_k (|a_k| + |S_k|)` over the partial sums `S_k` and the added
  intermediate values `a_k`. This depends on the sizes of the partial sums,
  not on `n` times the largest term. (The first version bounded it by
  "`2n` terms of size about 10, below 1e-9". That does not follow: the
  standard bound with those numbers is about 3e-7 at `n = 8192`.)
- *Measured.* `dp_rounding_check.py` (`logs/dp_rounding_check_n8192.log`)
  recorded all piece bounds of every iteration for amp 0.2, `n = 8192`,
  seed 0, eps 1e-6, and redid the forward and backward DP in `np.longdouble`.
  The largest difference over all iterations was 1.8e-13 for the DP bound
  and 3.2e-13 for any min-marginal. The first-order bound above evaluates to
  at most 4.4e-11. The review measured 8.7e-17 for the final
  iteration, with a bound of 8.7e-11. All of these are more than four orders
  of magnitude below the smallest `eps` used (1e-6).
- Transfer parameters are floating-point numbers, but the identity in 4.2(1)
  holds exactly for whatever values they have. Validity also relies on the
  exact derivative formulas coded in `instances.py` and `lotsizing.py`.

### 4.4 Uniqueness certificate (`verify_instances.py`)

The prototype also certifies that an instance has a unique, interior,
nondegenerate global minimizer. Run it with `eps = 1e-6` and
`localize_delta = 1e-4`: cells are removed only if `m_i(a) > UB + 1e-4`. By 4.2,
every `x` with `F(x) <= UB + 1e-4`, and in particular every global minimizer,
lies in the box `R` spanned by the surviving cells. The run stops once `R` is
inside the open box `(-1, 1)^n` and the matrix
`M = tridiag(2 - 1.2 max_{R} x_i^2, 0.8)` is positive definite.
`M` is a Loewner lower bound of the Hessian on `R`, so `F` is strictly
convex on `R`. The minimizer is then unique, interior, and nondegenerate. The
eigenvalue test is floating point, with threshold `lambda_min(M) > 1e-8`.
Multistart local optimization (200 random interior starts and 50 random
corners, L-BFGS-B) is reported alongside as heuristic evidence.

## 5. Prototype results and comparison with SCIP

Unless stated otherwise, the prototype runs use mode `quad`,
`unary_sub = 16`, `theta = 1`, at most 3e7 pair bounds per iteration
(`max_pairs`; a run that would exceed it stops as unsolved), and a 600 s
limit. Times are Python wall-clock seconds on the loaded machine (single
thread per process). The work count is the total number of pair bounds over
all iterations. SCIP nodes and pair bounds are different units: a SCIP node
solves an LP with cuts over all variables, while a pair bound costs a few
dozen floating-point operations. The meaningful comparison is growth in `n`,
plus CPU time.

### 5.1 Side by side on the same instances

SCIP default settings versus the prototype (mode `quad`), both with
`absgap = eps` and 5 seeds per row. The SCIP limit is 300 CPU s. Prototype
runs for larger `n` are in 5.2. SCIP was also run at eps 1e-3 (tables in
`tables.md`).

Amp 0.2, eps 1e-2:

| n | SCIP solved | SCIP nodes (geo. mean; + = lower bound) | SCIP median CPU s | SCIP median final gap | prototype solved | prototype median pair bounds | prototype median s |
|---|---|---|---|---|---|---|---|
| 2 | 5/5 | 1 | 0.0 | 7.1e-03 | 5/5 | 1 | 0.00 |
| 4 | 5/5 | 91 | 0.1 | 9.1e-03 | 5/5 | 3 | 0.00 |
| 6 | 5/5 | 610 | 0.4 | 9.5e-03 | 5/5 | 5 | 0.00 |
| 8 | 5/5 | 2793 | 2.7 | 1.0e-02 | 5/5 | 7 | 0.00 |
| 10 | 5/5 | 15582 | 14.9 | 1.0e-02 | 5/5 | 9 | 0.00 |
| 12 | 5/5 | 68567 | 78.1 | 1.0e-02 | 5/5 | 11 | 0.00 |
| 14 | 0/5 | 228094+ | 300.0 | 2.8e-02 | 5/5 | 13 | 0.00 |
| 16 | 0/5 | 135120+ | 300.0 | 1.8e-01 | 5/5 | 15 | 0.00 |
| 18 | 0/5 | 133905+ | 300.0 | 3.7e-01 | 5/5 | 17 | 0.00 |
| 20 | 0/5 | 104511+ | 300.0 | 6.2e-01 | 5/5 | 19 | 0.00 |
| 22 | 0/5 | 99392+ | 300.0 | 8.6e-01 | 5/5 | 21 | 0.01 |
| 24 | 0/5 | 76534+ | 300.0 | 1.1e+00 | 5/5 | 23 | 0.01 |

Amp 0.2, eps 1e-4:

| n | SCIP solved | SCIP nodes (geo. mean; + = lower bound) | SCIP median CPU s | SCIP median final gap | prototype solved | prototype median pair bounds | prototype median s |
|---|---|---|---|---|---|---|---|
| 2 | 5/5 | 1 | 0.0 | 6.4e-05 | 5/5 | 1 | 0.00 |
| 4 | 5/5 | 218 | 0.2 | 7.1e-05 | 5/5 | 3 | 0.00 |
| 6 | 5/5 | 1504 | 0.9 | 0.0e+00 | 5/5 | 25 | 0.01 |
| 8 | 5/5 | 7084 | 6.0 | 0.0e+00 | 5/5 | 35 | 0.01 |
| 10 | 5/5 | 29169 | 142.4 | 0.0e+00 | 5/5 | 45 | 0.01 |
| 12 | 0/5 | 104397+ | 300.5 | 7.6e-03 | 5/5 | 55 | 0.01 |
| 14 | 0/5 | 133937+ | 300.0 | 6.0e-02 | 5/5 | 65 | 0.02 |
| 16 | 0/5 | 91095+ | 300.0 | 2.3e-01 | 5/5 | 75 | 0.02 |
| 18 | 0/5 | 80884+ | 300.0 | 4.5e-01 | 5/5 | 85 | 0.01 |
| 20 | 0/5 | 71468+ | 300.0 | 6.8e-01 | 5/5 | 95 | 0.01 |

Amp 0.2, eps 1e-6:

| n | SCIP solved | SCIP nodes (geo. mean; + = lower bound) | SCIP median CPU s | SCIP median final gap | prototype solved | prototype median pair bounds | prototype median s |
|---|---|---|---|---|---|---|---|
| 2 | 5/5 | 28 | 0.0 | 0.0e+00 | 5/5 | 5 | 0.00 |
| 4 | 5/5 | 227 | 0.1 | 0.0e+00 | 5/5 | 27 | 0.01 |
| 6 | 5/5 | 1572 | 0.7 | 0.0e+00 | 5/5 | 65 | 0.01 |
| 8 | 5/5 | 7086 | 4.3 | 0.0e+00 | 5/5 | 91 | 0.01 |
| 10 | 5/5 | 29174 | 118.2 | 0.0e+00 | 5/5 | 121 | 0.02 |
| 12 | 0/5 | 104448+ | 300.8 | 7.6e-03 | 5/5 | 147 | 0.01 |
| 14 | 0/5 | 167505+ | 300.0 | 5.1e-02 | 5/5 | 177 | 0.01 |
| 16 | - | - | - | - | 5/5 | 211 | 0.03 |
| 18 | - | - | - | - | 5/5 | 237 | 0.02 |
| 20 | - | - | - | - | 5/5 | 263 | 0.02 |

Probe3 (amp 0.3), eps 1e-4:

| n | SCIP solved | SCIP nodes (geo. mean; + = lower bound) | SCIP median CPU s | SCIP median final gap | prototype solved | prototype median pair bounds | prototype median s |
|---|---|---|---|---|---|---|---|
| 2 | 5/5 | 5 | 0.0 | 5.0e-05 | 5/5 | 1 | 0.00 |
| 4 | 5/5 | 238 | 0.3 | 6.4e-05 | 5/5 | 15 | 0.01 |
| 6 | 5/5 | 1822 | 1.7 | 6.9e-05 | 5/5 | 25 | 0.01 |
| 8 | 5/5 | 7773 | 6.1 | 9.3e-05 | 5/5 | 35 | 0.01 |
| 10 | 5/5 | 37311 | 38.5 | 0.0e+00 | 5/5 | 45 | 0.01 |
| 12 | 1/5 | 107469+ | 300.6 | 3.7e-03 | 5/5 | 55 | 0.02 |
| 14 | 0/5 | 133679+ | 300.0 | 6.5e-02 | 5/5 | 905 | 0.02 |
| 16 | 0/5 | 94244+ | 300.0 | 2.3e-01 | 5/5 | 1463 | 0.02 |
| 18 | 0/5 | 79503+ | 300.0 | 4.3e-01 | 5/5 | 1705 | 0.02 |
| 20 | 0/5 | 71346+ | 300.0 | 6.6e-01 | 5/5 | 1879 | 0.02 |

On every instance where SCIP needs minutes or fails, the prototype needs
milliseconds. (SCIP times are CPU seconds, apparently user time only. Prototype times are
Python wall-clock seconds on a loaded machine, so they overstate its CPU
time, if anything.) On amp 0.2 the prototype's work grows roughly linearly over
this range of `n`. On probe3 the median jumps at `n = 14`, where
boundary-minimum seeds start to dominate. SCIP's node counts include every
node it processed, and the prototype's counts include every pair bound it
computed.

### 5.2 Prototype scaling to large n

Amp 0.2 (certified family):

| n | eps 1e-4: solved | median pair bounds | max pair bounds | median s | eps 1e-6: solved | median pair bounds | max pair bounds | median s | max cells per variable |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 5/5 | 1 | 1 | 0.00 | 5/5 | 5 | 9 | 0.00 | 2 |
| 4 | 5/5 | 3 | 15 | 0.00 | 5/5 | 27 | 39 | 0.01 | 2 |
| 6 | 5/5 | 25 | 25 | 0.01 | 5/5 | 65 | 69 | 0.01 | 4 |
| 8 | 5/5 | 35 | 35 | 0.01 | 5/5 | 91 | 95 | 0.01 | 4 |
| 10 | 5/5 | 45 | 45 | 0.01 | 5/5 | 121 | 125 | 0.02 | 4 |
| 12 | 5/5 | 55 | 55 | 0.01 | 5/5 | 147 | 151 | 0.01 | 4 |
| 14 | 5/5 | 65 | 65 | 0.02 | 5/5 | 177 | 185 | 0.01 | 4 |
| 16 | 5/5 | 75 | 351 | 0.02 | 5/5 | 211 | 367 | 0.03 | 4 |
| 18 | 5/5 | 85 | 745 | 0.01 | 5/5 | 237 | 745 | 0.02 | 4 |
| 20 | 5/5 | 95 | 887 | 0.01 | 5/5 | 263 | 927 | 0.02 | 6 |
| 32 | 5/5 | 155 | 1495 | 0.01 | 5/5 | 443 | 1535 | 0.04 | 6 |
| 64 | 5/5 | 603 | 3027 | 0.02 | 5/5 | 1195 | 3079 | 0.07 | 6 |
| 128 | 5/5 | 1287 | 6959 | 0.04 | 5/5 | 2511 | 7043 | 0.08 | 6 |
| 256 | 5/5 | 7743 | 39387 | 0.14 | 5/5 | 8871 | 39671 | 0.18 | 10 |
| 512 | 5/5 | 29831 | 131695 | 0.30 | 5/5 | 32179 | 131923 | 0.51 | 14 |
| 1024 | 5/5 | 61023 | 266763 | 0.76 | 5/5 | 65899 | 267207 | 0.69 | 14 |
| 2048 | 5/5 | 457355 | 2302539 | 2.31 | 5/5 | 458803 | 2316419 | 2.01 | 32 |
| 4096 | 5/5 | 977171 | 4634667 | 4.82 | 5/5 | 997763 | 4663731 | 6.67 | 32 |
| 8192 | 5/5 | 5825535 | 9494223 | 12.84 | 5/5 | 5837943 | 9549951 | 19.07 | 32 |

Amp 0.3 (probe3):

| n | eps 1e-4: solved | median pair bounds | max pair bounds | median s | eps 1e-6: solved | median pair bounds | max pair bounds | median s | max cells per variable |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 5/5 | 1 | 1 | 0.00 | 5/5 | 9 | 13 | 0.01 | 2 |
| 4 | 5/5 | 15 | 59 | 0.01 | 5/5 | 39 | 59 | 0.01 | 4 |
| 6 | 5/5 | 25 | 437 | 0.01 | 5/5 | 65 | 437 | 0.02 | 8 |
| 8 | 5/5 | 35 | 1083 | 0.01 | 5/5 | 95 | 1083 | 0.02 | 12 |
| 10 | 5/5 | 45 | 4749 | 0.01 | 5/5 | 125 | 4853 | 0.01 | 20 |
| 12 | 5/5 | 55 | 98087 | 0.02 | 5/5 | 151 | 107423 | 0.03 | 78 |
| 14 | 5/5 | 905 | 110745 | 0.02 | 5/5 | 905 | 121645 | 0.03 | 78 |
| 16 | 5/5 | 1463 | 96039 | 0.02 | 5/5 | 1463 | 108759 | 0.02 | 68 |
| 18 | 5/5 | 1705 | 97725 | 0.02 | 5/5 | 1705 | 111957 | 0.02 | 66 |
| 20 | 5/5 | 1879 | 109527 | 0.02 | 5/5 | 1879 | 125539 | 0.03 | 68 |
| 32 | 5/5 | 3139 | 164659 | 0.04 | 5/5 | 3139 | 191087 | 0.03 | 68 |
| 64 | 5/5 | 13747 | 345259 | 0.06 | 5/5 | 13795 | 401691 | 0.08 | 68 |
| 128 | 5/5 | 379803 | 661967 | 0.36 | 5/5 | 463343 | 772271 | 0.48 | 68 |
| 256 | 5/5 | 807599 | 4144059 | 0.61 | 5/5 | 973427 | 4678599 | 0.79 | 166 |
| 512 | 5/5 | 3699635 | 9700707 | 2.33 | 5/5 | 4602039 | 11160607 | 5.36 | 168 |
| 1024 | 5/5 | 19855211 | 50480047 | 16.84 | 5/5 | 22253535 | 54231759 | 16.39 | 274 |
| 2048 | 4/5 | 63798735 | 84266275 | 51.49 | 4/5 | 72122203 | 95852227 | 44.62 | 260 |

Power-law fits of the median pair-bound count (least squares on logs over
fully solved sizes `n >= 16`):

| family | eps 1e-4 | eps 1e-6 |
|---|---|---|
| amp 0.2, quad | n^1.80 (n = 16..8192, R^2 = 0.994) | n^1.60 (n = 16..8192, R^2 = 0.990) |
| amp 0.3, quad | n^2.38 (n = 16..1024, R^2 = 0.983) | n^2.43 (n = 16..1024, R^2 = 0.981) |
| amp 0.2, affine | n^1.90 (n = 16..256, R^2 = 1.000) | n^1.90 (n = 16..256, R^2 = 1.000) |

Work depends only weakly on `eps`. Going from 1e-4 to 1e-6 multiplies the
median pair-bound count by at most 3 for `6 <= n <= 64` (by up to 9 for
`n <= 4`, where the counts are tiny), and by 1.02-1.25 for `n >= 128`. The cost is dominated by the middle iterations
(section 5.5), not by the final precision. Across seeds the cost is
heavy-tailed: on amp 0.3 the maximum over seeds is up to about 1800 times
the median (`n = 12`, eps 1e-4), driven by the seeds with boundary minima. On amp 0.3 at
`n = 2048`, one seed exceeded the cap of 3e7 pair bounds per iteration.

### 5.3 Ablation: what the reparametrization buys

Median pair bounds over 5 seeds (in parentheses: number of seeds solved within the caps of 3e7 pair bounds per iteration and 600 s):

| n | plain 1e-4 | affine 1e-4 | quad 1e-4 | plain 1e-6 | affine 1e-6 | quad 1e-6 |
|---|---|---|---|---|---|---|
| 2 | 1.66e+03 (5) | 549 (5) | 1 (5) | 1.37e+05 (5) | 881 (5) | 5 (5) |
| 4 | 1.66e+05 (5) | 8.54e+03 (5) | 3 (5) | 1.46e+07 (5) | 1.39e+04 (5) | 27 (5) |
| 6 | 8.79e+05 (5) | 3.07e+04 (5) | 25 (5) | 5.13e+07 (3) | 4.68e+04 (5) | 65 (5) |
| 8 | 1.44e+06 (5) | 6.09e+04 (5) | 35 (5) | 4.37e+07 (2) | 9.6e+04 (5) | 91 (5) |
| 10 | 2.27e+06 (5) | 1.03e+05 (5) | 45 (5) | 5.39e+07 (0) | 1.6e+05 (5) | 121 (5) |
| 16 | 2.72e+07 (5) | 2.92e+05 (5) | 75 (5) | 3.71e+07 (0) | 4.43e+05 (5) | 211 (5) |
| 20 | 5.59e+07 (4) | 4.47e+05 (5) | 95 (5) | 3.67e+07 (0) | 6.87e+05 (5) | 263 (5) |
| 32 | 5.42e+07 (1) | 1.08e+06 (5) | 155 (5) | 3.75e+07 (0) | 1.66e+06 (5) | 443 (5) |
| 64 | 3.79e+07 (0) | 4.12e+06 (5) | 603 (5) | 3.81e+07 (0) | 6.2e+06 (5) | 1.2e+03 (5) |
| 128 | 4.43e+07 (0) | 1.52e+07 (5) | 1.29e+03 (5) | 4.44e+07 (0) | 2.34e+07 (5) | 2.51e+03 (5) |
| 256 | 2.23e+07 (0) | 5.73e+07 (5) | 7.74e+03 (5) | 2.23e+07 (0) | 8.61e+07 (5) | 8.87e+03 (5) |

Without transfers (`plain`), the constant bounds have a first-order copy
error. Cells must then shrink to about `eps / n`, and near the minimizer
thousands of cells per variable survive (up to 2500). This mode reaches
`eps = 1e-6` only up to `n = 4-8`. Linear transfers (`affine`) make the error
second order: every instance up to `n = 256` is solved, with work growing as
about `n^1.9`, and 57-86 million pair bounds at `n = 256`. The quadratic
transfers (`quad`) make every piece convex and minimized at the incumbent
near the optimum. They cut the work at `n = 256` by another factor of 7000-10000.

### 5.4 Ablation: refinement rule

`theta_ablation.py` (seed 0, eps 1e-6, cap 4e7 pair bounds per iteration,
300 s; output in `logs/theta_ablation.log`). A cell is bisected only if its
marginal is below `LB_dp + theta (UB - eps - LB_dp)`:

| amp | n | theta | status | final gap | iterations | pair bounds | max cells/var | s |
|---|---|---|---|---|---|---|---|---|
| 0.2 | 1024 | 1.0 | optimal | 9.31e-07 | 6 | 61179 | 6 | 0.49 |
| 0.2 | 1024 | 0.5 | optimal | 7.39e-07 | 6 | 55355 | 5 | 0.51 |
| 0.2 | 1024 | 0.2 | optimal | 8.23e-07 | 6 | 50060 | 5 | 0.47 |
| 0.2 | 1024 | 0.05 | optimal | 9.10e-07 | 6 | 46058 | 5 | 0.46 |
| 0.2 | 1024 | 0.0 | optimal | 9.97e-07 | 10 | 60498 | 7 | 0.81 |
| 0.2 | 8192 | 1.0 | optimal | 8.53e-07 | 7 | 5928355 | 24 | 9.11 |
| 0.2 | 8192 | 0.5 | optimal | 8.53e-07 | 7 | 4850400 | 21 | 8.15 |
| 0.2 | 8192 | 0.2 | optimal | 9.91e-07 | 7 | 3846180 | 17 | 7.83 |
| 0.2 | 8192 | 0.05 | optimal | 9.20e-07 | 8 | 3532995 | 14 | 8.99 |
| 0.2 | 8192 | 0.0 | optimal | 1.00e-06 | 31 | 20370714 | 230 | 44.19 |
| 0.3 | 1024 | 1.0 | optimal | 1.00e-06 | 14 | 22253535 | 124 | 10.36 |
| 0.3 | 1024 | 0.5 | optimal | 1.00e-06 | 14 | 17010072 | 114 | 8.35 |
| 0.3 | 1024 | 0.2 | optimal | 1.00e-06 | 17 | 31196980 | 165 | 13.34 |
| 0.3 | 1024 | 0.05 | pair_limit | 2.55e-02 | 12 | 31353587 | 195 | 12.41 |
| 0.3 | 1024 | 0.0 | pair_limit | 6.89e-02 | 46 | 62154281 | 845296 | 41.13 |
| 0.3 | 8192 | 1.0 | pair_limit | 4.88e-01 | 7 | 44729547 | 64 | 23.55 |
| 0.3 | 8192 | 0.5 | pair_limit | 4.88e-01 | 7 | 44312230 | 64 | 24.02 |
| 0.3 | 8192 | 0.2 | pair_limit | 4.88e-01 | 7 | 38425827 | 63 | 21.33 |
| 0.3 | 8192 | 0.05 | pair_limit | 2.05e-01 | 8 | 52359404 | 72 | 27.93 |
| 0.3 | 8192 | 0.0 | pair_limit | 3.24e-01 | 32 | 56259375 | 694 | 51.21 |

Partial refinement (`theta` from 0.05 to 0.5) saves up to about 40% of the
pair bounds on the amp 0.2 family. Refining only the lowest-bound paths
(`theta = 0`) needs many more iterations and is worse. No setting solves
amp 0.3 at `n = 8192` within the cap. The main runs use `theta = 1`.

### 5.5 Why the prototype is super-linear

The per-variable error of the DP bound is small, but every cell's marginal
carries the error summed over all `n` pieces. For example, at `n = 8192`
(amp 0.2, seed 0) the DP bound is 0.36, 0.20, 0.075, 0.0055 and 8.5e-7 below
UB after iterations 2-6 (cell widths 0.5 down to 0.03). Until this total
falls below a cell's own excess, the cell cannot be pruned, so most of each
variable's range survives through the middle iterations (12-16 cells per
variable at width 0.125). A heuristic estimate: with a per-variable error of
order `w^3`, the survivors peak at about `n^(1/3)` cells per variable, which
gives about `n^(2/3)` pair bounds per variable and `n^(5/3)` in total. This
is in line with the fitted exponents 1.6-1.8. On probe3 (amp 0.3) and on lot-sizing,
near-degenerate stretches, boundary minima, and near-optimal alternative
plans add more surviving cells, which makes the growth steeper (about
`n^2.4`). Exact unary minima, or pruning tests that do not carry the global
error, could reduce this. They were not needed for the comparison and were
not pursued.

### 5.6 Consistency of optimal values

Probe3 family, prototype in mode `quad` at the same eps (`analyze.py`):

- **Both solved (104 runs, eps 1e-4 and 1e-6).** SCIP's reported optimal
  value minus the prototype's UB lies in [-6.9e-6, -1.9e-8]. SCIP's dual
  bound never exceeds the prototype's UB (the largest difference is -8.4e-7).
  The largest amount by which the prototype's certified LB exceeds SCIP's
  reported value is 6.6e-6.
- The negative differences come from SCIP's feasibility tolerance, not from
  an error in either code. `check_scip_solution.py` re-solved four
  instances, `n = 6, 8`, and read SCIP's solution (table below). SCIP's
  value is below a certified lower bound on the true optimum, because each
  `t_i` sits up to 1e-6 below its right-hand side. `F` evaluated at SCIP's
  `x` is slightly above the prototype's UB, as it must be. So both solvers
  agree on the optimal value to within SCIP's tolerances (about `n * 1e-6`),
  and the prototype's bracket `[LB, UB]` is consistent with SCIP's point.
- **SCIP stopped by the time limit (78 runs).** SCIP's dual bound is always
  at least 1.6e-4 below the prototype's UB, as it must be. In 76 runs SCIP's
  best point was already optimal to within 1e-4; SCIP had found it but
  could not prove optimality. In the other two (amp 0.3, seed 4,
  `n = 18, 20`, whose optimum has five coordinates at the bounds), SCIP's
  best point was 8e-3 worse than the prototype's.

| amp | n | seed | SCIP value - prototype LB (eps 1e-6) | F(SCIP's x) - prototype UB | sum of `g_i(x) - t_i` over constraints |
|---|---|---|---|---|---|
| 0.3 | 8 | 4 | -4.9e-6 | 7.9e-7 | 6.1e-6 |
| 0.2 | 8 | 1 | -3.6e-6 | 1.1e-6 | 4.8e-6 |
| 0.3 | 6 | 1 | -3.3e-6 | 5.3e-7 | 4.0e-6 |
| 0.2 | 6 | 3 | -2.3e-6 | 6.6e-7 | 3.4e-6 |


## 6. Application-like family: lot-sizing chain

Instances: section 1.2, `T` periods, seeds 0-4. SCIP uses default settings,
eps 1e-4, and a 300 s CPU limit. The prototype uses mode `split`,
`theta = 1`, a 900 s limit, and a cap of 4e7 pair bounds per iteration.

SCIP (the last column is the largest gap among runs stopped by the time
limit):

| T | solved | nodes per seed | geo. mean nodes (solved) | median CPU s | max final gap (unsolved) |
|---|---|---|---|---|---|
| 2 | 5/5 | 5 80 7 7 9 | 11 | 0.0 | - |
| 3 | 5/5 | 31 59 57 81 96 | 61 | 0.1 | - |
| 4 | 5/5 | 109 293 71 192 317 | 169 | 0.1 | - |
| 5 | 5/5 | 441 343 406 366 1561 | 512 | 0.4 | - |
| 6 | 5/5 | 1763 1693 963 2104 1591 | 1573 | 1.8 | - |
| 7 | 5/5 | 2517 9598 1784 2423 7309 | 3772 | 3.2 | - |
| 8 | 5/5 | 12825 10470 4301 8420 8314 | 8343 | 11.2 | - |
| 9 | 5/5 | 38223 61040 12891 40938 37994 | 34199 | 61.7 | - |
| 10 | 4/5 | 145152+ 63235 72500 44404 74418 | 62388 | 135.6 | 1.03e-01 |
| 12 | 0/5 | 81420+ 81955+ 115687+ 109043+ 96855+ | - | 300.0 | 5.99e-01 |
| 14 | 0/5 | 68912+ 72926+ 76469+ 75422+ 71432+ | - | 300.0 | 1.41e+00 |
| 16 | 0/5 | 55080+ 55886+ 59175+ 58951+ 59342+ | - | 300.0 | 2.32e+00 |

Fits on `T = 4..9` (geometric means, `analyze.py`): the exponential fit
gives a factor of 2.78 per period (7.73 per two periods), with R^2 0.9945;
the power-law fit gives `T^6.28`, with R^2 0.9813. The exponential fits
better, but the step factors are noisy (3.0, 3.1, 2.4, 2.2, 4.1). One period
adds three SCIP variables (`p_t, s_t, z_t`), so per-period factors are not
comparable with probe3's per-variable factors.

Prototype:

| eps | T | solved | median pair bounds | max pair bounds | median s | max cells/var | idle periods (median) |
|---|---|---|---|---|---|---|---|
| 1e-06 | 2 | 5/5 | 450 | 640 | 0.02 | 12 | 1 |
| 1e-06 | 3 | 5/5 | 3717 | 9739 | 0.03 | 44 | 1 |
| 1e-06 | 4 | 5/5 | 4420 | 77644 | 0.03 | 92 | 2 |
| 1e-06 | 5 | 5/5 | 6039 | 7469 | 0.03 | 36 | 2 |
| 1e-06 | 6 | 5/5 | 8980 | 90154 | 0.05 | 110 | 2 |
| 1e-06 | 7 | 5/5 | 9491 | 891569 | 0.06 | 324 | 3 |
| 1e-06 | 8 | 5/5 | 12724 | 21724 | 0.05 | 42 | 3 |
| 1e-06 | 9 | 5/5 | 54809 | 180949 | 0.08 | 108 | 3 |
| 1e-06 | 10 | 5/5 | 22984 | 60576 | 0.07 | 70 | 4 |
| 1e-06 | 12 | 5/5 | 35058 | 48958 | 0.08 | 62 | 5 |
| 1e-06 | 14 | 5/5 | 59866 | 133564 | 0.13 | 84 | 5 |
| 1e-06 | 16 | 5/5 | 74382 | 665490 | 0.13 | 154 | 6 |
| 1e-06 | 32 | 5/5 | 503258 | 1185182 | 0.68 | 218 | 11 |
| 1e-06 | 64 | 5/5 | 2826934 | 5400506 | 4.02 | 332 | 22 |
| 1e-06 | 128 | 5/5 | 13905354 | 24953492 | 21.38 | 536 | 46 |
| 1e-06 | 256 | 4/5 | 66056308 | 155355142 | 108.52 | 918 | 88 |
| 0.0001 | 2 | 5/5 | 370 | 490 | 0.02 | 12 | 1 |
| 0.0001 | 3 | 5/5 | 3345 | 8813 | 0.03 | 44 | 1 |
| 0.0001 | 4 | 5/5 | 3742 | 66590 | 0.03 | 88 | 2 |
| 0.0001 | 5 | 5/5 | 5903 | 7027 | 0.03 | 36 | 2 |
| 0.0001 | 6 | 5/5 | 8770 | 88500 | 0.04 | 106 | 2 |
| 0.0001 | 7 | 5/5 | 9073 | 808055 | 0.04 | 288 | 3 |
| 0.0001 | 8 | 5/5 | 12524 | 21074 | 0.04 | 42 | 3 |
| 0.0001 | 9 | 5/5 | 54271 | 171125 | 0.07 | 104 | 3 |
| 0.0001 | 10 | 5/5 | 22142 | 58620 | 0.07 | 70 | 4 |
| 0.0001 | 12 | 5/5 | 34216 | 48460 | 0.07 | 60 | 5 |
| 0.0001 | 14 | 5/5 | 59146 | 130010 | 0.11 | 84 | 5 |
| 0.0001 | 16 | 5/5 | 73578 | 586342 | 0.12 | 146 | 6 |
| 0.0001 | 32 | 5/5 | 500624 | 1182014 | 0.64 | 218 | 11 |
| 0.0001 | 64 | 5/5 | 2804154 | 5393382 | 3.82 | 332 | 22 |
| 0.0001 | 128 | 5/5 | 13850380 | 24773576 | 25.46 | 536 | 46 |
| 0.0001 | 256 | 4/5 | 65651598 | 153966360 | 107.06 | 902 | 88 |

The prototype solves every instance up to `T = 128`, and 4 of 5 at
`T = 256`; the fifth hit the cap. The median work grows as about `T^2.43`
(`T = 8..128`, R^2 0.98, both tolerances). Without the `T = 9` outlier the
fit gives `T^2.55` (R^2 0.999), so the exponent is 2.43-2.55. That is steeper than on probe3:
the optimal plans batch production, leaving about 35-40% of the periods
idle ("idle periods" column), and many near-optimal plans keep many cells
alive (up to 900 cells per variable at `T = 256`). SCIP at `T = 12` already
leaves gaps of 0.36-0.60 after 300 s, while the prototype needs about
0.07 s at `T = 12` and 21-25 s at `T = 128` (wall clock).

Consistency (SCIP value minus the prototype UB, over the same instances at eps 1e-4):

- Both solved: 44 runs; SCIP primal - prototype UB in [-3.75e-06, -1.73e-07]; max(SCIP dual - prototype UB) = -1.73e-07
- SCIP time limit: 16 runs; SCIP primal - prototype UB in [-1.95e-07, -1.26e-07]; max(SCIP dual - prototype UB) = -1.03e-01

SCIP's value is always slightly below the prototype's feasible value, by
at most 3.8e-6. This is the same feasibility-tolerance effect as in 5.6. On
the runs that hit the time limit, SCIP had already found the optimal plan
(within 2e-7), but its dual bound was still 0.1 or more below it.


## 7. Caveats: what is and is not shown

Shown (on these instances, with this SCIP version and these settings):

- SCIP's node count grows by a roughly constant factor, about 5 per two added
  variables, over the range where it finishes. Beyond that range, the final
  gap after a fixed CPU budget grows with `n`. This holds for the default
  settings and for all six tested variations (formulation, best-first,
  OBBT at every node with a solved LP, optimality emphasis, all combined,
  optimal start point). The warm start barely changes node counts, so the effort is spent
  on the lower-bound proof, not on finding the optimum.
- It also holds on instances where the premise was checked: the amp 0.2
  family has a certified unique, interior, nondegenerate global minimizer
  for every tested `n` and seed.
- A chain DP branch and bound with valid bounds (4.2) closes the same
  instances to the same absolute tolerance. It takes milliseconds up to
  `n = 64`, and handles `n = 8192` (amp 0.2) in about 10-20 s, with work
  growing polynomially (fitted exponents 1.6-2.4, depending on the family).
- The reparametrization of the pieces matters a great deal. Without it
  (`plain`), the first-order copy error makes the DP fail at `eps = 1e-6`
  already for `n >= 10`, within the same caps.

Not shown:

- **Exponential versus steep polynomial.** On the fully solved ranges at
  eps 1e-4 and 1e-6 (`n = 4..10`), an exponential fit and a power-law fit
  with exponent about 5.3 are equally good. At eps 1e-2 (`n = 4..12`) and on
  lot-sizing, the exponential fits better. The local power-law exponents
  rise with `n` (4.7 to 8.1 at eps 1e-2), close to the exponential pattern.
  The unsolved `n = 14` runs already exceed the power-law extrapolations by
  1.7-2.5 times, and the gap left after a fixed budget grows with `n`. All of
  this is indirect. The solvable range is narrow (up to `n = 12`), there are
  only 5 seeds, and single seeds vary by up to 3 times. Growth faster than
  any fixed polynomial over this range is not the same as exponential
  growth asymptotically.
- **Other solvers and settings.** Only SCIP 10 was run. BARON, Gurobi,
  Couenne and ANTIGONE were not tested.
  - *Already active.* The first version said SCIP's intersection-cut and
    RLT/SDP-type separators were untested; that was wrong. The default runs
    use the 2x2-minor (SDP-type) separator, which applied 184 cuts at `n = 6`
    (123 calls), and RLT at the root (1 call, 0 cuts). `emph_opt` and
    `combo` add interminor intersection cuts at the root (44 applied at
    `n = 6`) and RLT every 20 levels (`scip_settings_check.py`,
    `logs/settings_check_*_n6.txt`).
  - *Not tested.* The quadratic handler's intersection cuts
    (`nlhdlr/quadratic/useintersectioncuts`, off by default); RLT, minor or
    interminor separation at every node; other branching rules; and a
    reformulation that separates the convex part of `F`.

  Any of these could change the constant, and possibly the growth.
- **SCIP tolerances.** SCIP accepts solutions whose epigraph variables are
  up to `feastol = 1e-6` below their right-hand sides, so its reported
  optimal value can be below the true optimum by up to about `n * 1e-6`
  (observed: up to 6.6e-6 at `n = 10`, below the prototype's certified lower
  bound; `data/scip_solution_check.jsonl`). The `eps = 1e-6` SCIP runs are
  therefore certified only relative to SCIP's own tolerance model. They
  were kept because the node counts are nearly identical to `eps = 1e-4`.
- **Prototype validity** rests on hand-derived derivative and
  second-derivative bounds, exact enumeration arguments, and floating-point
  margins (4.3). There is no interval arithmetic. Sampling tests found no
  violated bound. The independent review reproduced the optimal values
  (33 instances, different method: a grid DP with a rigorous concavity-based
  bracket) and the uniqueness certificates. It found no violation in 75
  adversarial prototype runs with perturbed transfers and other parameters. The UB is always `F` at an actual point that satisfies the
  constraints (checked explicitly in lot-sizing).
- **Prototype scope.** Paths only, one continuous variable per stage,
  problem-specific bounding routines, and transfers that depend on a good
  incumbent. There is no tree decomposition with larger bags, no separator
  of width greater than 1, and no integer variables. Its work grows
  super-linearly (5.5), and instance-dependent near-degeneracy makes the
  cost heavy-tailed across seeds (max/median pair bounds up to about 1800x
  on probe3).
- **Premise.** Probe3 as defined in PROGRAM.md (amp 0.3) does *not* always
  have an interior minimizer. From `n = 12` some seeds have boundary minima
  and several local minima, and by `n = 256` most seeds do. Here this rested
  on eps-optimal points and capped certificate runs, which is evidence only.
  The review made it rigorous for 9 instances (section 1.3). SCIP's growth on
  amp 0.3 and amp 0.2 is nearly the same, so the SCIP conclusion does not
  depend on this, but PROGRAM.md's statement about probe3 should be
  corrected. The lot-sizing family violates only the interiority part of the
  premise: at the three optima checked, they are strict, nondegenerate
  boundary minimizers.
- **Timing.** The machine was shared, and the load changed during the runs
  (load average 17-130 on 36 cores). SCIP uses CPU-time limits, and its node
  counts are deterministic: repeated solved runs gave identical counts.
  SCIP's CPU clock appears to count user time only. The SCIP worker
  processes also spent about 25% extra CPU in system time (for example,
  2100 s user and 540 s system for one worker), which the time limits do
  not include. Prototype times are wall-clock under load; the pair-bound
  counts are deterministic.
- The work units differ (a SCIP node versus a pair bound). The comparison is
  about growth rates and CPU time, not about per-unit cost.


## 8. Files and commands

All paths are relative to `research-20260929/computation/`.

| file | content |
|---|---|
| `instances.py` | probe3 family: coefficients, `F`, gradient, local optimizer, SCIP model builder, chain class with bounds and the Hessian certificate |
| `lotsizing.py` | lot-sizing family: definition, local optimizer, chain class with bounds, SCIP model |
| `chain_bb.py` | the prototype (DP B&B, transfers, bound helpers `quad_box_min`, `quad_band_min`, `taylor2_lb`) |
| `test_bounds.py` | sampling validity tests for the probe3 bounds and the reparametrization identity (`logs/test_bounds.log`) |
| `verify_instances.py` | multistart and uniqueness certificate (`data/verify.jsonl`) |
| `run_scip.py`, `run_proto.py`, `run_lotsizing.py` | batch runners writing JSONL |
| `theta_ablation.py` | refinement-rule ablation (`logs/theta_ablation.log`) |
| `check_scip_solution.py` | evaluates `F` at SCIP's solutions (`data/scip_solution_check.jsonl`) |
| `scip_stats_probe.py`, `scip_display_probe.py` | SCIP statistics and progress log for the `n = 12` throughput collapse (`logs/scip_stats_*.txt`, `logs/scip_display_*.log`) |
| `recheck_n1000.py`, `scip_settings_check.py`, `lotsizing_kkt_check.py`, `dp_rounding_check.py` | checks added after review (section 9) |
| `analyze.py` | produces all tables and fits in this note (`tables.md`) |
| `data/*.jsonl` | raw results, one JSON object per run |
| `data/wallclock/` | first SCIP batch with wall-clock limits (determinism check only) |

Commands (run in the directory above, with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`):

    python3 test_bounds.py
    python3 run_scip.py --variants default --eps 1e-4 --n 2 4 6 8 10 12 14 16 18 20 --seeds 0 1 2 3 4 --tl 300 --workers 5 --amp 0.3 --out data/scip_default_amp0.3.jsonl
    python3 run_scip.py --variants default --eps 1e-6 --n 2 4 6 8 10 12 14 --seeds 0 1 2 3 4 --tl 300 --workers 5 --amp 0.3 --out data/scip_default_amp0.3.jsonl
    (the same two commands with --amp 0.2 --out data/scip_default_amp0.2.jsonl)
    python3 run_scip.py --variants single bestfirst obbt emph_opt warm combo --eps 1e-4 --n 2 4 6 8 10 12 14 --seeds 0 1 2 --tl 300 --workers 6 --amp 0.3 --out data/scip_variants_amp0.3.jsonl
    python3 run_scip.py --variants default --eps 1e-4 --n 12 14 --seeds 0 1 2 --tl 1800 --workers 3 --amp 0.2 --out data/scip_long_amp0.2.jsonl
    python3 run_scip.py --variants default --eps 1e-4 --n 12 14 --seeds 0 1 2 --tl 1800 --workers 3 --amp 0.3 --out data/scip_long_amp0.3.jsonl
    python3 run_scip.py --variants default --eps 1e-2 1e-3 --n 2 4 6 8 10 12 14 16 18 20 22 24 --seeds 0 1 2 3 4 --tl 300 --workers 6 --amp 0.2 --out data/scip_loose_amp0.2.jsonl
    python3 run_scip.py --variants default --eps 1e-2 1e-3 --n 2 4 6 8 10 12 14 --seeds 0 1 2 3 4 --tl 300 --workers 6 --amp 0.2 --out data/scip_loose_small_amp0.2.jsonl   (same jobs, started in parallel to get them sooner; duplicates are counted once)
    WORKERS=3 python3 verify_instances.py data/verify.jsonl 0.3 2 4 6 8 10 12 14 16 18 20 32 64 100 256 1000
    WORKERS=3 python3 verify_instances.py data/verify.jsonl 0.2 2 4 6 8 10 12 14 16 18 20 32 64 100 256 1000
    python3 run_proto.py --modes quad --amp 0.2 --eps 1e-4 1e-6 --n 2 4 6 8 10 12 14 16 18 20 32 64 128 256 512 1024 2048 4096 8192 --workers 3 --out data/proto_amp0.2.jsonl
    python3 run_proto.py --modes quad --amp 0.3 --eps 1e-4 1e-6 --n 2 4 6 8 10 12 14 16 18 20 32 64 128 256 512 1024 2048 --workers 3 --out data/proto_amp0.3.jsonl
    python3 run_proto.py --modes affine plain --amp 0.2 --eps 1e-4 1e-6 --n 2 4 6 8 10 12 14 16 18 20 32 64 128 256 --workers 3 --tl 600 --out data/proto_ablation_amp0.2.jsonl
    python3 run_proto.py --modes quad --amp 0.2 --eps 1e-2 1e-3 --n 2 4 6 8 10 12 14 16 18 20 22 24 --workers 2 --out data/proto_loose_amp0.2.jsonl
    python3 theta_ablation.py > logs/theta_ablation.log
    python3 run_lotsizing.py scip --T 2 3 4 5 6 7 8 9 10 12 14 16 --seeds 0 1 2 3 4 --eps 1e-4 --tl 300 --workers 4 --out data/lotsizing_scip.jsonl
    python3 run_lotsizing.py proto --T 2 3 4 5 6 7 8 9 10 12 14 16 32 64 128 256 --seeds 0 1 2 3 4 --eps 1e-4 1e-6 --tl 900 --workers 2 --out data/lotsizing_proto.jsonl
    python3 check_scip_solution.py > data/scip_solution_check.jsonl
    python3 scip_stats_probe.py 280; python3 scip_stats_probe.py 600; python3 scip_display_probe.py > logs/scip_display_n12_amp0.3_seed0.log
    python3 recheck_n1000.py > data/recheck_n1000_amp0.3.jsonl
    python3 scip_settings_check.py
    python3 lotsizing_kkt_check.py > data/lotsizing_kkt_check.jsonl
    python3 dp_rounding_check.py 8192 > logs/dp_rounding_check_n8192.log
    python3 analyze.py > tables.md

Checks run locally for this note: `test_bounds.py` (all five checks passed;
the largest value of LB minus the sampled minimum was -1e-13 for the box and
Taylor routines and -1.4e-11 / -3.8e-11 for the polygon and lot-sizing
routines, that is, the safety margins), and SCIP's reproduction of the
PROGRAM.md node counts (217, 351, 1055, 2941 for n = 4, 6, seeds 0, 1). After
the review, the four checks in section 9 were also run. No project-wide
checks were run, and CI was not inspected.

## 9. Revision after review

An independent review (`../reviews/computation-review.md`, checks in
`../reviews/computation-review-checks/`) found the main conclusions sound.
It confirmed that the prototype's bounds are valid, reproduced the optimal
values and certificates by an independent method, and reproduced SCIP's
node counts exactly. It asked for the corrections below. Each was checked
here before it was made.

| # | change | how it was checked here |
|---|---|---|
| 1 | 4.3: the DP rounding justification ("`2n` terms of size 10, below 1e-9") did not follow. It was replaced by the recursive-summation argument and measurements. The margins are now described as subtracted safety, not error. The conclusion is unchanged. | `dp_rounding_check.py 8192`: all 7 iterations, forward and backward DP redone in long double. Largest difference 1.8e-13 (bound) and 3.2e-13 (marginals); first-order bound 4.4e-11. The review's final-iteration value is 8.7e-17. |
| 2a | 1.3: "not certified" means the capped run hit the pair limit. The boundary-minimum claim for amp 0.3 was evidence in this study; the review's rigorous check for 9 instances is cited. | `data/verify.jsonl`: all 24 non-certified runs have status `pair_limit` (the review counts 25; the per-row counts in 1.3 add to 24). |
| 2b | 1.3: multistart missed the optimum in 6 instances, not 3. At `n = 1000` it missed for seeds 0, 2, 3 and 4. The `n = 1000` row was recomputed at eps-optimal points (smallest full-Hessian eigenvalue -0.741, not -0.694). | `recheck_n1000.py`: the prototype (eps 1e-6) solves all 5 seeds. Its UB matches the review's independent optimum to 1.4e-14, with the same number of coordinates at the bounds (4-27). Multistart was worse by 9.8e-4 to 1.1e-2 for seeds 0, 2, 3, 4. |
| 2c | 1.3: the amp 0.2 certificate eigenvalue bound is 0.244, not 0.18 (0.181 is the amp 0.3 minimum). | minimum of `cert_lmin` in `data/verify.jsonl`: 0.2438 (amp 0.2), 0.1809 (amp 0.3). |
| 3a | 2, 3.3, 7: "OBBT at every node" now reads "at every node with a solved LP". | `scip_settings_check.py`: obbt propagator called 228 times in 320 nodes (`n = 6`), 2 times in default. |
| 3b | 7: the claim that SDP-type, RLT and intersection cuts were untested was wrong. The caveat now lists what was active and what was not. | same script: default applied 184 minor (2x2 SDP-type) cuts at `n = 6`; RLT had 1 root call; `emph_opt` applied 44 interminor cuts. `nlhdlr/quadratic/useintersectioncuts` is `False` by default. |
| 3c | 3.1, Summary, 7: the local power-law exponents were added (4.7, 5.3, 7.7, 8.1 at eps 1e-2; 4.8, 5.4, 6.3 at eps 1e-4), as was the seed dispersion behind the `n = 14` extrapolation. The summary wording was softened ("about 5x per two variables on `n = 4..10`", "persists under the six variations tried"). | `analyze.py` (new "local exponents" table in `tables.md`); seed ratios recomputed from `data/`. |
| 4 | 1.2, 6, 7: the lot-sizing optimum is a strict, nondegenerate *boundary* minimizer. The indefinite-Hessian argument (full Hessian, irrelevant at a boundary point) was removed. The premise fails only through interiority. The prototype exponent is 2.43-2.55. The modelling choices (no terminal condition, aggregated holding-cost constraint in SCIP) are now stated. | `lotsizing_kkt_check.py` (`T = 50/12/32`): reduced Hessian eigenvalues 0.80, 0.80, 0.85; active multipliers at least 0.128; inactive at most 4e-7; full Hessian -2.50, -1.46, -1.45. `analyze.py`: fit without `T = 9` gives `T^2.55`. |
| 5 | Summary: the prototype's amp 0.3 failures and heavy tails are stated, and so is the time-unit mismatch (SCIP CPU user seconds against prototype wall-clock seconds). 5.1 and 6 also carry the time units. | from `data/proto_amp0.3.jsonl` (4/5 solved at `n = 2048`), `logs/theta_ablation.log` (no `theta` solves `n = 8192`), and the maximum/median ratio of 1783 at `n = 12`. |
| – | Smaller fixes: the 4.2 step 4 wording (closed cells share endpoints); a code comment in `lotsizing.py` that the Taylor range must stay unclipped (behavior unchanged). | – |

Not changed: the review's optional suggestions to set the last sub-interval
endpoint in `unary_lb_sub` to `q` exactly (an effect of about 1e-16, far
inside the margin), and to rerun the `n = 12` throughput collapse on an idle
machine with peak-memory recording. The collapse remains unexplained.

