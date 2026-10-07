# Decomposition-aware dual bounds for open MINLPLib chain instances

Date: 2026-09-29. Status: computational results with proofs sketched in this
file. An independent verifier rechecked all 11 dual bounds with separate code
and found them valid (Section 11). Every "verified" bound was recomputed in
rigorous interval arithmetic (mpmath `iv`, or outward-rounded IEEE interval
arithmetic in `ivnp.py`) and cross-checked by a second route (listed per
instance). Primal points were evaluated from the OSIL data in 50-digit
arithmetic (`osil_eval.py`); the reported violations are exact violations of
the stated float vectors.

Code, logs, and downloaded MINLPLib solution files are in this directory
(file list at the end). All runs were single-threaded on a shared machine
(load average 33–56 on 36 cores from other agents), so runtimes are
indicative only.

## 1. Summary

Baselines. The MINLPLib metadata `dualbound` (from
`treewidth-census/instancedata.csv`) is a value reported by at least three
solvers. The instance pages (fetched 2026-09-29; site updated 2026-09-14)
list tighter single-solver dual bounds, and all 11 instances are listed as
open. Both baselines are shown below. The starting gap is measured against
the best listed bound and the listed primal value. "Gap after" is our
primal minus our verified dual bound.

| instance | listed primal | metadata dual (≥ 3 solvers) | best listed dual (solver) | starting gap vs best (rel.) | our verified dual bound | our primal (max abs. violation) | gap after | method | time |
|---|---|---|---|---|---|---|---|---|---|
| lnts50 | 0.5546687649 | 0.5258315547 | 0.55464755 (GUROBI) | 3.8e-5 | 0.554668764883 | 0.554668764939 (4.6e-15) | 5.5e-11 | Lagrangian over the chain, monotone in h | < 1 s |
| lnts100 | 0.5545954012 | 0.5089747974 | 0.55299042 (GUROBI) | 0.29% | 0.554595401111 | 0.554595401167 (6.2e-15) | 5.5e-11 | same | < 1 s |
| lnts200 | 0.5545770161 | 0.5054303434 | 0.55219867 (GUROBI) | 0.43% | 0.554577016048 | 0.554577016103 (6.3e-15) | 5.5e-11 | same | 1 s |
| lnts400 | 0.5545724137 | 0.5015530698 | 0.55204395 (GUROBI) | 0.46% | 0.554572413645 | 0.554572413701 (6.9e-15) | 5.5e-11 | same | 3 s |
| dtoc5 | 5.389672119 | 0.000627 | 0.00243096 (BARON) | ≈ 100% | 5.3896721191811325 | 5.3896721191811405 (2.4e-20) | 8e-15 | Lagrangian = affine value functions | 5 s |
| camshape100 | −4.284147122 | −4.474993552 | −4.28415233 (ANTIGONE) | 1.2e-6 | −4.28414712174674 | −4.28414712174674 (3.9e-16) | 0 (exact optimum) | bound propagation along the chain | < 1 s |
| camshape200 | −4.278500233 | −4.831866586 | −4.63229055 (ANTIGONE) | 8.3% | −4.27850023299272 | −4.27850023299272 (2.8e-16) | 0 (exact optimum) | same | < 1 s |
| camshape400 | −4.275696633 * | −5.013185607 | −4.97265746 (ANTIGONE) | 16.3% | −4.27568847892554 | −4.27568847892554 (3.2e-16) | 0 (exact optimum) | same | < 1 s |
| camshape800 | −4.274306866 * | −5.144374942 | −5.12584096 (GUROBI) | 19.9% | −4.27427414195419 | −4.27427414195419 (4.8e-16) | 0 (exact optimum) | same | < 1 s |
| optcdeg2 | 293.8760751 | 4.399551855 | 292.41713458 (GUROBI) † | 0.50% | 293.869993850 | 293.876075096 (8.9e-16) | 6.1e-3 (2.1e-5 rel.) | Lagrangian + exact head block (monotonicity certificate) | 1 min bound, 3 min primal |
| lukvle10 | 352.2380254 | 0.0508058324 | 351.223393 (SCIP) | 0.29% | 352.238025369 | 352.238025406 (3.5e-15, MINLPLib point p5) | 3.7e-8 (verifier's bound: 1.4e-9) | partial Lagrangian + 2-D interval branch and bound | 8.5 min |

Notes on the table:

- \* The camshape400/800 listed primal values come from MINLPLib points p2,
  which violate constraints by 3.0e-10 and are accepted under MINLPLib's
  1e-8 feasibility tolerance. Our bounds hold for exactly feasible points
  and lie *above* these listed values (by 8.2e-6 and 3.3e-5). They are the
  exact optima: the envelope point attaining them is exactly feasible,
  which the verifier confirmed in rational arithmetic (Section 5).
- † The GUROBI bound for optcdeg2 equals the objective of MINLPLib point p2,
  which violates rows by up to 1e-6. It is therefore consistent only up to
  that tolerance.
- For camshape, "exact optimum" means our bound equals the objective of an
  exactly feasible point, so the remaining gap is zero.

Main findings.

1. All 11 bounds are valid and close the gaps: to rounding level for lnts
   and dtoc5; exactly for camshape; to 3.7e-8 absolute for lukvle10 (1.4e-9
   with the verifier's tighter recomputation); and to 2.1e-5 relative for
   optcdeg2.
   - Measured against the best listed single-solver bounds, the starting
     gaps differ widely:
     - 1.2e-6 (camshape100) and 3.8e-5 (lnts50);
     - 0.29–0.50% (lnts100–400, optcdeg2, lukvle10);
     - 8–20% (camshape200–800);
     - about 100% (dtoc5).
   - For camshape100 and lnts50 the improvement over the state of the art
     is marginal. For camshape200–800 and dtoc5 it is large.
   - The best MINLPLib solution files that satisfy the rows to 4e-10 or
     better are optimal to our tolerances.
2. The bounds come from decomposition along the chain, but not from the
   generic method of the program (cells on separators, cell-constant bounds,
   dynamic programming). What worked:
   - Lagrangian relaxation of the chain rows with multipliers from a primal
     point, which separates into one-stage or one-pair problems;
   - interval bound propagation along the chain;
   - exact treatment of short sub-chains where the Lagrangian is nonconvex:
     a monotonicity certificate for optcdeg2, and a 2-D interval branch and
     bound for lukvle10.

   Branching was needed only inside 2-D subproblems.
3. The generic separator-cell dynamic program was tested on camshape100 and
   optcdeg2 and did not reach useful accuracy (Section 8). For discretized
   continuous problems, the per-stage constraint scale shrinks with the step
   size, and cell-constant bounds lose a first-order amount at every stage.
4. The large metadata gaps are not evidence of exponential single-tree
   branching on these instances. Their causes are:
   - free variables without bounds (dtoc5, optcdeg2, lukvle10);
   - long chains of nonconvex equality rows;
   - weak relaxations of reverse-convex rows (camshape).

   Some single solvers already do much better (GUROBI on lnts, ANTIGONE on
   camshape100). SCIP 10 with 600 s ends at 7.0% (camshape100) and 9.96%
   (lnts50).
5. The certificates use known mechanisms. The value here is the rigorous
   certificates for these instances, not new mechanisms:
   - dtoc5: a discrete-time Mangasarian/Arrow-type sufficiency argument (the
     Lagrangian, equivalently the Hamiltonian, is convex at the costate);
   - camshape: a discrete Sturm comparison;
   - lnts: rests on the classical linear-tangent structure (Bryson & Ho);
   - optcdeg2 and lukvle10: standard partial Lagrangian relaxations with
     small exact blocks.

## 2. Common conventions

- Minimization as in the OSIL files. A dual bound is a number `L` with
  `L <= f(x)` for every feasible `x` of the OSIL model (exact feasibility).
- Decimal constants of the OSIL (for example `2e-05`, `1.99984519984971`)
  are treated as exact decimals. mpmath intervals enclose them; `ivnp.const`
  encloses them by widening the nearest double by one ulp on each side.
- `ivnp.py` interval arithmetic: every `+ - * / sqrt` is an IEEE
  round-to-nearest operation (error at most 0.5 ulp) followed by one
  `nextafter` step outward, so results enclose the exact values.
- Structure claims are not taken from the task description: each script
  asserts the exact row and bound pattern of the OSIL file before using it
  (`extract`/`pattern_check` functions).
- Lagrangian notation: for rows `c_j(x) = 0` and multipliers `lam_j`, weak
  duality gives `f(x) = f(x) + sum_j lam_j c_j(x) >= min_{x in X} [...]` for
  every feasible `x`, where `X` is any set known to contain all feasible
  points. When the rows couple only neighboring stages, the minimization
  splits into small independent problems.

## 3. lnts50/100/200/400

### 3.1 Structure (asserted in `lnts_bound.extract`)

Variables:

- controls `th_0..th_N` in `[-1.5707963267949, 1.5707963267949]`;
- states `px, py, vx, vy` (N+1 each);
- time step `h >= 0`.

Objective: `min N h`. Rows for `i = 0..N-1` (trapezoidal rule, `a = 100`):

    px_{i+1} - px_i - h/2 (vx_i + vx_{i+1}) = 0,   py likewise with vy,
    vx_{i+1} - vx_i - h/2 (a cos th_i + a cos th_{i+1}) = 0,
    vy_{i+1} - vy_i - h/2 (a sin th_i + a sin th_{i+1}) = 0.

Fixed values: `px_0 = py_0 = vx_0 = vy_0 = 0`, `py_N = 5`, `vx_N = 45`,
`vy_N = 0`.

Tree decomposition: stage bags contain the state, two controls, and `h`,
so the separator is `(py, vx, vy, th, h)` with dimension 5. `px` can be
dropped: it appears only in its own recursion and `px_N` is free. The
global `h` is in every separator.

### 3.2 Reformulation

For fixed `h`, the dynamics are linear. Summing the rows gives, for every
feasible point:

    vx_N = a h sum_j w_j cos th_j,   vy_N = a h sum_j w_j sin th_j,
    py_N = a h^2 sum_j c_j sin th_j,

where:

- `w` are the trapezoid weights (1/2 at both ends, 1 inside);
- `c_j = sum_k w_k W_kj`, with `W_kj = ([j <= k-1] + [1 <= j <= k])/2`;
- `c_j` is an exact rational.

The identities were checked with random controls to 1e-40. Feasibility
therefore requires

- `h > 0`;
- `sum w cos th = A(h) := 45/(a h)`;
- `sum w sin th = 0`;
- `sum c sin th = B(h) := 5/(a h^2)`.

### 3.3 Certificate and validity

For `mu` (any sign) and `nu >= 0`, let
`S(mu,nu) = sum_j sqrt(w_j^2 + (mu w_j + nu c_j)^2)`. If
`S(mu,nu) - nu B(h2) < A(h2)`, then no feasible point has `h <= h2`.

Proof: for such a point, adding the vanishing terms
`mu sum w sin th` and `nu (sum c sin th - B(h))` gives

    A(h) = sum_j [w_j cos th_j + (mu w_j + nu c_j) sin th_j] - nu B(h)
         <= S - nu B(h)
         <= S - nu B(h2)
         < A(h2) <= A(h).

The first inequality uses `max_th (w cos th + b sin th) = sqrt(w^2 + b^2)`;
the second and last use that `B` and `A` decrease in `h` and `nu >= 0`.
This is a contradiction, so `N h2` is a lower bound.

This is a Lagrangian decomposition of the chain (per-stage closed-form
maxima). Monotonicity in the global separator `h` replaces branching on
`h`.

### 3.4 Computation

- Primal: the linear tangent law `tan th_j = mu + nu c_j/w_j` (the
  maximizer in the certificate). The three equations are solved for
  `(mu, nu, h)` by Newton's method in 60-digit mpmath. The states come from
  the forward recursion.
- Dual: `h2 = h* (1 - 1e-10)`. The inequality is checked in mpmath
  interval arithmetic; the margins are −8.6e-9 to −6.9e-8.
- Independent recheck (`verify_independent.py`): cvxpy solves the convex
  relaxation `max sum w_j sqrt(1 - s_j^2)` subject to `sum w s = 0` and
  `sum c s >= B(h)`. It is infeasible at `h2 (1 - 1e-5)` and feasible at
  `h2 (1 + 1e-5)` for all four sizes.

| instance | verified dual | primal (max viol.) | MINLPLib primal / metadata dual / best listed dual (GUROBI) |
|---|---|---|---|
| lnts50 | 0.554668764883212 | 0.554668764938679 (4.6e-15) | 0.5546687649 / 0.5258315547 / 0.55464755 |
| lnts100 | 0.554595401111452 | 0.554595401166911 (6.2e-15) | 0.5545954012 / 0.5089747974 / 0.55299042 |
| lnts200 | 0.554577016047626 | 0.554577016103084 (6.3e-15) | 0.5545770161 / 0.5054303434 / 0.55219867 |
| lnts400 | 0.554572413645230 | 0.554572413700687 (6.9e-15) | 0.5545724137 / 0.5015530698 / 0.55204395 |

Runtime: under 4 s for all four.

Assessment: gap closed to the chosen 1e-10 relative margin. The verifier
also certified the margin 1e-12, which gives gaps of about 5.5e-13.
Against the best listed bounds (GUROBI), the starting gaps were 3.8e-5
relative for lnts50, a marginal improvement, and 0.29–0.46% for
lnts100–400. The treewidth/separator structure is irrelevant here; what
matters is that the dynamics are linear in the state for fixed `h`. The
certificate's maximizer is the classical linear-tangent law (Bryson & Ho);
the contribution is the rigorous discrete certificate.

## 4. dtoc5

### 4.1 Structure (asserted in `dtoc5_bound.pattern_check`)

Variables `u_0..u_{T-1}` (x2..x50000) and `y_0..y_T` (x50001..x100000),
`T = 49999`, all free except `y_0 = 1`. With `h = 2e-5` (8e-5 = 4h exactly):

    min  h * sum_{t=0}^{T-1} (u_t^2 + y_t^2)
    s.t. -h u_t + y_t - y_{t+1} + 4h y_t^2 = 0,   t = 0..T-1.

`y_T` does not appear in the objective.

### 4.2 Decomposition

Each `u_t` appears linearly in one row with coefficient `-h != 0` and is
free, so `u_t = (y_t + 4h y_t^2 - y_{t+1})/h` eliminates it. The reduced
problem is a chain in `y` with one-dimensional separators `y_t`. The bound
below uses the original variables.

### 4.3 Method and validity

With multipliers `lam_t` on `y_{t+1} - y_t - 4h y_t^2 + h u_t = 0`, the
Lagrangian is separable:

    L = sum_t [h u_t^2 + h lam_t u_t]
      + sum_{t=1}^{T-1} [h (1 - 4 lam_t) y_t^2 + (lam_{t-1} - lam_t) y_t]
      + lam_{T-1} y_T + h (1 - 4 lam_0) - lam_0.

If `lam_{T-1} = 0` and `lam_t < 1/4`, minimizing over the free variables
gives the dual function

    d(lam) = h(1 - 4 lam_0) - lam_0 - (h/4) sum_{t=0}^{T-1} lam_t^2
             - sum_{t=1}^{T-1} (lam_{t-1} - lam_t)^2 / (4h (1 - 4 lam_t)),

and every feasible point has objective `>= d(lam)`. No bounds on the free
variables are needed. This is the program's "affine child bound": the
certificate is a family of affine functions of the separators.

Multipliers: the primal costate `lam_t = -2 u_t` of the Newton solution
(`dtoc5_primal.py`, banded Newton on the reduced problem), with
`lam_{T-1} = 0` exactly. The primal has `u_t >= 0`, so `lam_t <= 0 < 1/4`,
and the Lagrangian is strictly convex in `(u, y)`. A KKT point of a
problem whose Lagrangian is convex at its multipliers is a global minimizer
of that Lagrangian, so the dual bound equals the primal value up to the
accuracy of the multipliers: the gap is zero, and no branching is needed.
This is a discrete-time Mangasarian/Arrow-type sufficiency argument: the
Lagrangian, equivalently the Hamiltonian, is convex at the costate. The
mechanism is classical; what is new is the rigorous certificate for this
instance.

### 4.4 Results

- Dual bound: `d(lam) in [5.3896721191811325, 5.3896721191811325]`
  (mpmath interval, 30 digits, `h = 1/50000` exact). Float recomputation:
  5.389672119181132.
- Primal: objective 5.3896721191811405, max row violation 2.4e-20. The
  controls are recomputed from the states in 50-digit arithmetic and then
  rounded once.
- The gap is 8e-15. The verifier, using polished 40-digit multipliers,
  certifies 5.38967211918114046 and finds the primal 5.3896721191811405, so
  the optimum is 5.38967211918114 to about 16 digits.
- An earlier version of this report computed the controls in double
  precision. That left row violations of 8e-17 and a primal value 1.6e-14
  below the bound. The overshoot was an artifact of the double-precision
  controls and is gone with accurate controls.
- MINLPLib: metadata dual 0.00063; best listed dual 0.00243096 (BARON).
  Runtime: 5 s for the bound and the 50-digit primal check, plus a few
  seconds for Newton.

Assessment: gap closed. The instance is hard for spatial branch and bound
only because the variables are unbounded and the equality rows are
nonconvex. It has hidden convexity: its Lagrangian at the KKT multipliers is
convex.

## 5. camshape100/200/400/800

### 5.1 Structure (asserted in `camshape_model.extract`)

Variables `r_1..r_n` and `d_1..d_{n-1}`. Objective `min -c0 * sum r_i`
(`c0 = pi/n` as a 15-digit decimal). Rows:

    G_1: -r_1 + c r_2 - r_1 r_2 <= 0
    G_i: -r_{i-1} r_i + c r_{i-1} r_{i+1} - r_i r_{i+1} <= 0   (i = 2..n-1)
    G_n: c2 r_{n-1} - 2 r_n - r_{n-1} r_n <= 0
    E:   c r_n^2 - 4 r_n <= 0             (implied by r_n <= 2 < 4/c)
    D_i: r_i - r_{i+1} + d_i = 0          (i = 1..n-1)

Bounds: `r_1 in [1, ub_1]`, `r_i in [1, 2]`, `r_n in [lb_n, 2]`, `d_1`
free, `|d_i| <= alpha` for `i >= 2`. The constants `c = 2 cos(dtheta)`,
`c2` (about `2c`; not exactly `2c` for n = 400), `alpha`, `ub_1`, and `lb_n`
are read from the file. Tree decomposition: path of bags
`{r_{i-1}, r_i, r_{i+1}}`, separators `(r_i, r_{i+1})` (dimension 2).

### 5.2 Reformulation

Since `r >= 1 > 0`, dividing `G_i` by the product of its variables gives the
equivalent rows `g_i >= 0` with `u_j = 1/r_j`, `u_0 = 1`, `u_{n+1} = 1/2`:

    e_j := u_{j-1} - c u_j + u_{j+1} >= 0   (j = 1..n-1),
    g_n = u_{n-1} + 1/2 - (c2/2) u_n >= 0.

These rows are linear in `u`.

### 5.3 Bound (bound propagation along the chain)

Let `S_0 = 1`, `S_1 = 1/ub_1`, `S_{j+1} = c S_j - S_{j-1}`. For a feasible
point, `z_j = u_j - S_j` satisfies `z_0 = 0`, `z_1 = u_1 - 1/ub_1 >= 0`,
and `z_{j+1} = c z_j - z_{j-1} + e_j`. Therefore

    z_j = U_{j-1}(c/2) z_1 + sum_{k=1}^{j-1} U_{j-1-k}(c/2) e_k,

where `U_m` are Chebyshev polynomials of the second kind,
`U_m(cos th) = sin((m+1) th)/sin th`. These are nonnegative for `m <= n-1`
because `n th < pi` (`n th/pi = 0.396` to `0.3995`). So `u_j >= S_j` and,
since `S_j >= 0.3097 > 0`, `r_j <= R_j := 1/S_j` for all `j`. This is a
discrete Sturm comparison: `R` is the straight line `r = 1/cos` in polar
coordinates, the extreme convex shape. The comparison principle is
classical; what is new is its use as a rigorous certificate for these
instances.

With `B_j = min(R_j, ub_j)` and the slope rows (pairs `j = 2..n-1`, since
`d_1` is free), every feasible `r` satisfies

    r_j <= E_j := min_k (B_k + alpha * dist(j, k)),

where `dist` counts slope-constrained pairs between `j` and `k`. This is a
forward and a backward min-plus pass along the chain. Hence
`f = -c0 sum r >= -c0 sum_j E_j`.

The envelope `E` is itself feasible: a straight-line phase where the
convexity rows are active, a slope-`alpha` phase, and then `r = 2`. The
convexity rows hold at the kinks because `u` only bends upward there. So
the bound is exact. Using `E` as the primal point confirms this (Section
5.4). The verifier recomputed `E` in exact rational arithmetic. `E`
satisfies every row, bound, and slope constraint exactly (63/127/255/512
convexity rows active with slack exactly 0), and its objective equals the
bound. So each reported bound is the exact optimum over exactly feasible
points.

Rigor: `U_m`, `S_j`, `R_j`, the envelope, and the sum are computed in
mpmath interval arithmetic from the decimal constants. The three-term
recurrence has no numerical instability, but naive interval evaluation
widens intervals by about `1 + sqrt 2` per step (dependency effect). The
working precision is therefore `0.4 n + 60` digits. At fixed 60 digits the
enclosures for n >= 200 blew up; this was detected and fixed. Envelope
additions keep the upper ends of interval sums.

### 5.4 Results

| n | verified dual | primal = envelope (row viol., bound viol.) | MINLPLib p1 file obj (viol.) | independent LP recheck |
|---|---|---|---|---|
| 100 | −4.284147121746744 | −4.284147121746743 (3.9e-16, 2.1e-17) | −4.284147121746719 (2.0e-14) | −4.284147121746805 |
| 200 | −4.278500232992722 | −4.278500232992723 (2.8e-16, 6.6e-17) | −4.278500232993864 (1.8e-14) | −4.278500232993643 |
| 400 | −4.275688478925543 | −4.275688478925543 (3.2e-16, 2.2e-16) | −4.275688478934241 (2.5e-14) | −4.275688478932913 |
| 800 | −4.274274141954194 | −4.274274141954194 (4.8e-16, 1.9e-17) | −4.274274141954209 (3.9e-10) | −4.274274141956520 |

Independent recheck (`verify_independent.py`): `R_j` from the closed form
`S_j = cos(j th) + (1/ub_1 - cos th) sin(j th)/sin th`, and the relaxation
`max sum r` subject to `r_j <= B_j`, slope rows, and lower bounds solved as
an LP with HiGHS. It agrees to about 1e-12. A local NLP solve (SLSQP) of
camshape100/400 reaches the same values up to its own 1e-9 violations.
Runtime: under 1 s per instance.

### 5.5 Tolerance sensitivity

The chain is ill-conditioned: the Chebyshev weights reach about
`sin(1.25)/sin th`, which is 76 for n = 100 and 600 for n = 800. Small
violations of the convexity rows therefore accumulate into visible
objective gains.

- MINLPLib point p2 of camshape400 (objective −4.275696633, the metadata
  primal value) violates rows by 3.0e-10 and lies 8.2e-6 below our bound.
- For camshape800, the p2 point (objective −4.274306866, violation 3.0e-10)
  lies 3.3e-5 below our bound.
- SCIP 10's camshape100 incumbent (−4.2841998026) violates rows by 1.0e-8
  and bounds by 2.0e-8 (within SCIP's tolerances) and lies 5.3e-5 below the
  exact optimum.

- The p1 points of camshape200/400 (violations about 2e-14) also lie
  slightly below the exact optimum, by 1e-12 and 9e-12 (verifier's exact
  evaluation).

Our bounds are for exact feasibility. The exact optima are the values in
the table. MINLPLib accepts points within a 1e-8 feasibility tolerance, so
it lists the p2 values as primal bounds for camshape400/800. Our bounds lie
*above* those listed primal values. This is not a contradiction: the p2
points are not exactly feasible. Anyone comparing our bounds with the
MINLPLib listing, or submitting them, must state the exact-versus-tolerance
distinction.

### 5.6 Assessment

Gap closed exactly, in closed form, by propagating bounds along the chain.
No branching and no Lagrangian were needed. Measured against the best
listed single-solver bounds, the starting gaps were 1.2e-6 relative for
camshape100 (ANTIGONE −4.28415233), a marginal improvement, and 8–20% for
n = 200–800. A pure Lagrangian bound is
weak here: with the KKT multipliers the terms `r_j + kappa_j/r_j` have
`kappa_j > 0`, so they are convex and are maximized away from the optimum.
The generic separator-cell DP is analyzed in Section 8.

## 6. optcdeg2

### 6.1 Structure (asserted in `optcdeg2_bound.pattern_check`)

`h = 4e-4`, `N = 50000`. Variables: controls `u_0..u_{N-1}`
(x2..x50000 and x50002), positions `y_0..y_N` (x50003..x100003), and
velocities `v_0..v_{N-1}` (x100004..x150003) plus `v_N` = x50001:

    min (h/2) sum_{t=0}^{N} y_t^2
    y_{t+1} = y_t + h v_t
    v_{t+1} = v_t + h (u_t - 0.02 y_t - 0.2 v_t^2)
    y_0 = 10, v_0 = 0, v_N = 0, v_t >= -1, |u_t| <= 0.2, y free.

Separator: the state `(y_t, v_t)`, dimension 2.

### 6.2 Derived bounds (with proofs)

- A one-line bound, for scale only: `v_0 = 0` gives `y_1 = 10`, and
  `v >= -1` gives `y_t >= 10 - (t-1)h`. Hence
  cost `>= (h/2) sum max(0, 10 - (t-1)h)^2 = 166.70` (float value, not used
  below). This alone is 38 times the metadata dual bound (4.40), but far
  below the best listed dual (292.42).
- State bounds `Y_t`, `V_t` by interval propagation along the chain
  (`optcdeg2_bound.state_bounds`, mpmath intervals):
  - Forward: `V_{t+1} = g(V_t) + h[-0.2, 0.2] - 0.02 h Y_t` and
    `Y_{t+1} = Y_t + h V_t`, intersected with `v >= -1`.
  - Backward: `Y_t = Y_{t+1} - h V_t` and
    `V_t = g^{-1}(V_{t+1} - h[-0.2, 0.2] + 0.02 h Y_t)`.
  - Here `g(v) = v - 0.2 h v^2` is increasing for `v < 6250` (asserted:
    all `V_t` stay below 6000), so `g` and its inverse branch map intervals
    to intervals through their endpoints.
  - Proof: induction over `t`. Each feasible state lies in the boxes
    because the recurrences hold exactly and every operation is an interval
    enclosure.

### 6.3 Lagrangian bound

Dualize all rows with multipliers `(mu_t, lam_t)`. The Lagrangian separates
into convex quadratics in each free `y_t`, linear terms in each `u_t`
(minimum `-0.2 h |lam_t|`), and quadratics `A_t v_t^2 + B_t v_t` with
`A_t = 0.2 h lam_t` over `v_t in V_t`. Multipliers are the discrete costates
of the MINLPLib point p1. They are computed by the backward adjoint
recursion; its one free parameter `lam_{N-1}` (`v_N` is fixed) is set so
that `lam` vanishes at the second control switch.

- Result: 293.2500703 (mpmath intervals; `ivnp` recomputation
  293.2500703375), a gap of 0.626.
- Per-term analysis: 0.620 of the gap comes from `t < 3092` and 0.006 from
  `t >= 47290`. In both windows `lam_t < 0`, so the `v_t`-terms are concave
  and their minimum sits at an end of the reachable interval (for example
  `v_t` near 0 at t = 0.5, while the optimum has `v_t = -0.20`).

### 6.4 Exact head block with a monotonicity certificate (`optcdeg2_head.py`)

Keep the rows `t < m` (the head) exact and dualize the rest with the same
multipliers:

    bound = min_{u in [-0.2,0.2]^m} J(u) + (separable terms for t > m),
    J(u) = (h/2) sum_{t<m} y_t^2 + Phi(y_m, v_m),
    Phi = (h/2) y^2 + (-mu_m + 0.02 h lam_m) y + (-h mu_m - lam_m) v + 0.2 h lam_m v^2.

The gradient is `dJ/du_t = h p_v(t+1)`, where `p` solves the discrete
adjoint recursion. It is evaluated in interval arithmetic over the forward
reachable intervals of all controls in the box (no feasibility
intersections). If every `p_v(t+1) > 0`, then `J` is nondecreasing in each
coordinate on the box: apply the mean value theorem along each coordinate.
So `min J = J(-0.2, ..., -0.2)`, evaluated by interval simulation.

- The check passes at `m = 3080` (`min p_v = 0.448`) and fails at
  `m = 3100`, just after the optimal switch at step 3091. The verifier
  found that it also passes at `m = 3090` (`min p_v = 0.084`, bound
  293.8700386118, a gain of 4.5e-5); the reported bound keeps `m = 3080`.
- With `m = 3080` the bound is 293.8699938501 (`ivnp`). An independent
  mpmath recomputation (`optcdeg2_verify.py`: separate code for reachable
  intervals, adjoint, corner simulation, and all separable terms) gives
  293.8699938542.
- Reported: **293.86999385**.

### 6.5 Primal

`optcdeg2_primal.py` uses bang-bang control `-0.2 / +0.2 / -0.2` with
fractional controls at two switching steps. It finds the second switch by
bisection so that `v_N = 0`, and scans the first. Result: objective
293.876075095886, max row violation 8.9e-16. There is one formal bound
violation of 1.1e-17: the double 0.2 used for `u` exceeds the decimal
bound `.2`. The verifier found it; our evaluator compares against the
parsed double and reports 0. The
MINLPLib point p1 (from an interior method, not exactly bang-bang)
evaluates to 293.876075102017 (violation 1.2e-14).

### 6.6 Assessment

Gap reduced to 6.1e-3 absolute (2.1e-5 relative), which closes 99.6% of
the starting gap. The starting gap was:
- 0.50% relative to the best listed dual (GUROBI 292.41713458). That bound
  equals the objective of MINLPLib point p2, which violates rows by up to
  1e-6, so it is valid only up to that tolerance.
- 98.5% relative to the metadata dual (4.40).

The remaining 0.006 comes from the last 2700 steps, where `lam < 0` again. A mirror-image exact tail block would need to handle the
terminal row `v_N = 0`, so the coordinate-monotonicity argument does not
apply directly; this was not attempted.

A literal separator-cell DP was tried and failed (Section 8.2). A quick
L-BFGS maximization of the nonsmooth dual function over the head and tail
multipliers (`optcdeg2_dualopt.py`) stopped after one iteration without
improvement.

## 7. lukvle10

### 7.1 Structure (asserted in `lukvle10_bound.pattern_check`)

    min sum_{i=0}^{499} f(x_{2i}, x_{2i+1}),   f(a,b) = (a^2)^(b^2+1) + (b^2)^(a^2+1),
    c_j = -x_j + 3 x_{j+1} - 2 x_{j+2} - 2 x_{j+1}^2 + 1 = 0,   j = 0..997,

with all 1000 variables free. Row `j` determines `x_{j+2}` from
`(x_j, x_{j+1})`, so the feasible set is a 2-parameter family (the orbit of
a planar map with Jacobian determinant 1/2). The fixed points are
`x = +-1/sqrt 2`, with pair cost 0.70711. `+1/sqrt 2` is attracting;
`-1/sqrt 2` is a saddle with eigenvalues 2.73 and 0.18. The best MINLPLib
point p5 (352.2380254) follows the saddle for about 490 steps, with cheap
transients at both ends; its total saving versus 500 × 0.70711 is 1.315.
Separators: `(x_j, x_{j+1})`, dimension 2.

### 7.2 Method: partial Lagrangian

Rows `j < m = 994` are dualized. The rows `j = 994..997` inside the last
three pairs are kept exact. Weak duality gives

    optimum >= sum_{i<497} min_{R^2} l_i + min_{R^2} tau + sum_{j<m} lam_j,

where:

- `l_i(a,b) = f(a,b) + beta_{2i} a + q_{2i} a^2 + beta_{2i+1} b + q_{2i+1} b^2`
  for the head pairs;
- `tau(a,b) = f(s) + f(P s) + f(P^2 s) + (same form in a, b)`, with
  `s = (x_994, x_995)` and `P` the two-step map of the kept rows;
- `beta` and `q` are exact rationals built from the float multipliers.

Multipliers: KKT multipliers of p5 by least squares (residual 4.6e-14).
For `j = 30..960`, where the KKT values agree to 5e-10, they are replaced by
a common constant (any multipliers are valid). This makes 464 middle pair
problems identical (`beta = 0`, same `q`), leaving 34 distinct pair
problems plus the tail block.

With all rows dualized, a float grid estimate of the bound is 352.152. Its
gap of 0.086 sits in pairs 497–498 (the end transient). Keeping the last
three pairs exact removes it.

### 7.3 Reduction to boxes (proof)

- Pair problems: `f(a,b) >= phi(a) + phi(b)`, where `phi(t) = t^2` if
  `|t| >= 1` and 0 otherwise. For `|a| >= 1` we have `a^2 >= 1` and
  exponent `>= 1`, so `(a^2)^(b^2+1) >= a^2`; otherwise the term is
  `>= 0`.
- Hence `l >= psi_a(a) + psi_b(b)`, with `psi(t) = phi(t) + q t^2 + beta t`.
  Since `q = -2 lam >= -0.82 > -1`, `psi` grows like `(1+q) t^2` outside
  `[-1, 1]`.
- For each problem, a radius `R` is computed so that
  `psi_a(t) + min psi_b > U + 1` for `|t| >= R`, where `U` is the value at
  the primal pair (an interval upper bound). The inequality is checked in
  interval arithmetic.
- The minimum over `R^2` therefore equals the minimum over the box
  `[-R_a, R_a] × [-R_b, R_b]`: R is about 3.08 for middle pairs, and
  `[-5.05, 5.05] × [-2.31, 2.31]` for the tail.
- The tail uses the same bound, since `f(P s), f(P^2 s) >= 0`.

### 7.4 Interval branch and bound

`lukvle10_bound.bnb` works entirely in mpmath intervals (30 digits):

- Box lower bound: the maximum of the natural enclosure and a mean-value
  form. The interval gradient comes from forward-mode differentiation with
  intervals and is used only when no argument of `f` contains 0.
- Incumbent: the interval upper end at box centers, which is a valid upper
  bound of the minimum.
- Pruning: boxes with lower bound above the incumbent are discarded.
- Stopping: incumbent minus the minimum open-box lower bound `<= 1e-11`
  for the grouped middle problem and `<= 1e-9` otherwise. The certified
  bound is the minimum lower bound over the open boxes.

Box counts:

- middle group: 4643 boxes;
- other pair problems: 900–3800 boxes each;
- tail: 48628 boxes.

### 7.5 Results

- Dual bound **352.238025369202** (interval lower end).
- Primal: MINLPLib point p5, objective 352.238025406496, max violation
  3.5e-15 (re-evaluated by `osil_eval.py`; we did not compute our own
  lukvle10 point).
- Gap 3.7e-8. It equals the sum of the branch-and-bound tolerances, so the
  partial Lagrangian has no duality gap at these multipliers.
- MINLPLib: metadata dual 0.0508; best listed dual 351.223393 (SCIP), a
  starting gap of 1.01 (0.29%). Runtime 509 s, single core.
- Independent recheck: the verifier, with its own multipliers and its own
  interval branch and bound (tolerance 1e-12 for pairs), certifies
  **352.2380254050785**, a gap of 1.4e-9 to p5. Our bound lies 3.6e-8
  below it and is consistent with it.
- Float recheck (`lukvle10_sanity.py`, not a proof): each of the 35
  problems was sampled on a 1501 × 1501 grid of its box and locally
  minimized from the 20 best points. No sampled value falls below its
  certified lower bound (smallest margin 9.8e-12).
- Limitation: both our certificate and the verifier's rely on mpmath's
  interval `exp`/`log`. Their code is independent, but the library is a
  shared dependency.

### 7.6 Assessment

Gap closed. The chain Lagrangian is exact except at the end transient,
where the saddle structure makes the pair Lagrangian nonconvex. There, a
three-pair exact block (a 2-D problem whose map is iterated twice) is
enough. This is the closest instance to the program's picture: branching
happens only on a 2-dimensional separator (the tail's entry state
`(x_994, x_995)`), combined with Lagrangian child bounds for the rest of
the chain.

## 8. The generic separator-cell dynamic program

### 8.1 camshape100 (`camshape_celldp.py`)

Rigorous forward DP over cells of the separator `(r_i, r_{i+1})`. It uses a
uniform r-grid of width `d`, a band of slope-feasible cell pairs,
cell-constant upper bounds on the prefix value, and cell-level feasibility
tests of the convexity rows (made permissive by 1e-12, with a 1e-11 safety
margin per stage). Results:

| d | cells per stage | dual bound | time |
|---|---|---|---|
| 1e-3 | 3.9e4 | −5.279 | 0.2 s |
| 4e-4 | 2.4e5 | −5.096 | 1.1 s |
| 2e-4 | 9.4e5 | −4.900 | 4.6 s |
| 1e-4 | 3.7e6 | −4.711 | 22 s |
| 5e-5 | 1.5e7 | −4.580 | 109 s |
| 2.5e-5 | 5.9e7 | −4.451 | 461 s |

The exact value is −4.2841 and MINLPLib has −4.475. The finest grid we
ran (d = 2.5e-5: 5.9e7 cells per stage, 461 s, 4.9 GB) only just beats
MINLPLib and leaves an error of 0.167. The error shrinks by 0.13–0.20 per
halving of `d`, while time and memory grow about 4-fold. The next halving
would need about 2.4e8 cells per stage, which is out of reach for this
implementation.

The convexity rows constrain second differences of `u = 1/r` at the scale
`(2 - c) u`, about 1.5e-4 for n = 100 and falling as `1/n^2`. A cell of
width `d` relaxes each row by `O(d)` and lets the relaxed path drift
in every stage. Useful accuracy needs `d` of order 1e-5 or below
(3.7e8 cells per stage at 1e-5 for n = 100) and `d = O(1/n^2)` in general. The method
stays polynomial, but with a high degree. This is the practical obstacle
to the program's generic scheme on discretized continuous models: the
separator partition must resolve the per-stage scale, not only the
solution's accuracy.

### 8.2 optcdeg2 block DP with fixed multipliers (`optcdeg2_blockdp.py`)

Setup:

- The head and tail windows are split into blocks of 128 steps.
- At block boundaries, the separator component `v` is partitioned into 50
  cells; `y` is left unpartitioned because its Lagrangian terms are convex.
- Interior `v_t` must lie in the forward-reachable interval from the entry
  cell intersected with the backward-reachable interval from the exit cell.
- Block bounds for all cell pairs are combined by DP.

Result: 293.25417 versus 293.25007 without cells, a gain of 0.004 out of
the 0.626 gap.

Reason: with fixed multipliers the Lagrangian decouples `y` from `v`. The
DP picks a cheap `v`-path (for example `v` near 0, which is reachable with
`u = +0.2`) whose position consequences are not charged. Branching on part
of the separator does not restore the coupling. The separator cells would
need to carry both state components, or the multipliers would need
re-optimizing per cell. The exact head block of Section 6.4 does the
former for the one window that matters.

## 9. SCIP 10 baseline (PySCIPOpt 6.2.1, default settings, 1 thread, 600 s)

| instance | status | primal | dual | gap | nodes |
|---|---|---|---|---|---|
| camshape100 | time limit | −4.2841998026 (row viol. 1.0e-8, bound viol. 2.0e-8) | −4.5858 | 7.04% | 116405 |
| lnts50 | time limit | 0.5546687648 | 0.5044 | 9.96% | 6892 |

Both SCIP incumbents lie slightly below our exact-feasibility bounds, by
5.3e-5 and 4.9e-11; they are feasible only within tolerance. Logs:
`logs/scip_*.log`, `logs/scip_baseline.jsonl`,
`logs/scip_primal_check.jsonl`.

## 10. What this says about the program's practical claim

- **Positive.**
  - Decomposing along the chain gave valid, tight bounds in time linear in
    the chain length for every attempted instance.
  - The rigorous work per instance is a sum of per-stage (or per-pair)
    computations plus one or two small exact blocks. This matches the
    "decomposition certificate" picture: local certificates per bag,
    combined along the tree.
  - The single-tree solver gaps were larger on every instance, though by
    very different factors:
    - best listed single-solver bounds: from 1.2e-6 relative
      (camshape100) and 3.8e-5 (lnts50) up to 8–20% (camshape200–800)
      and about 100% (dtoc5);
    - metadata bounds and SCIP with 600 s: much larger.
- **Negative / qualifying.**
  - The workhorse was not branching on separators with cell-constant
    bounds. It was Lagrangian (affine) child bounds with good multipliers,
    plus bound propagation.
  - The generic cell DP converged far too slowly on camshape100 (Section
    8.1).
  - Branching only on part of the separator failed on optcdeg2 (Section
    8.2).
  - Four of the five families have hidden convexity or monotonicity that a
    simple dual or comparison argument exposes:
    - dtoc5: Lagrangian convex at KKT;
    - lnts: concave per-stage maxima;
    - camshape: linear rows in `u` with a nonnegative Green's function;
    - optcdeg2: monotone head.

    These mechanisms are known: Mangasarian/Arrow-type sufficiency
    (dtoc5), discrete Sturm comparison (camshape), and the linear-tangent
    law (lnts). The contribution is rigorous certificates for these
    instances, not new mechanisms.
  - lukvle10 needed exact treatment of a 2-D sub-block only where the
    Lagrangian was nonconvex.
- **Suggested capability.**
  - Chain (tree) Lagrangian decomposition with multipliers from a local
    solution.
  - Detection of the stages where the stage Lagrangian is nonconvex.
  - Exact treatment of those short windows: a monotonicity or convexity
    certificate, or a low-dimensional interval branch and bound on the
    window's entry separator.
  - Bound propagation along the chain for unbounded variables.
  - Cell-based DP with constant bounds seems unsuitable for discretized
    continuous models unless the cells carry affine or quadratic minorants.
- **Not tested.** waterno2 was only examined structurally; rocket was not
  attempted.
  - waterno2_06 has 6 periods of 166 variables, 9 binaries, and 206 rows
    each. The periods are interleaved in the scalar OSIL model.
  - A 20-minute attempt to recover the period partition (spectral ordering
    of the variable graph) did not isolate the inter-period rows cleanly,
    so the separator dimension is unknown.
  - The period subproblems are MINLPs, so a Lagrangian over periods would
    need global subproblem solves, whose bounds we could not verify
    independently.

## 11. Verification

An independent verifier rechecked all 11 dual bounds, the primal points, and
the camshape p2 claim, using separate code (a new OSIL reader that keeps
decimal constants exactly; exact rational arithmetic for camshape;
`mpmath.iv` elsewhere). Report:
`research-20260929/reviews/open-instances-verification/verification-report.md`.

Main outcomes:

- All bounds are valid and agree with ours to the stated precision.
- camshape: exact optima, with the envelope exactly feasible in rational
  arithmetic.
- lnts: certified also at the tighter margin 1e-12, with gaps about
  5.5e-13.
- dtoc5: 5.38967211918114046.
- optcdeg2: 293.8699938542 at m = 3080 and 293.8700386118 at m = 3090.
- lukvle10: 352.2380254050785, a gap of 1.4e-9.

The verifier also found the minor issues corrected above:

- the dtoc5 double-precision controls;
- the optcdeg2 1.1e-17 bound violation;
- the uncommented camshape200/400 p1 deviations;
- the baseline framing of Section 1.

The verifier did not recheck:

- the SCIP baseline and SCIP camshape100 incumbent claims (Section 9);
- the generic cell DP and block DP experiments (Section 8);
- the optcdeg2 dual-optimization attempt;
- the cvxpy (lnts) and SLSQP/LP (camshape) float rechecks;
- the lukvle10 full-Lagrangian estimate 352.152 (Section 7.2).

Other caveats:

- optcdeg2 was verified with our multiplier arrays as input. This does not
  affect validity, but the verifier's implementation follows our method,
  so it checks the arithmetic and code rather than an alternative argument.
- For lukvle10 both certificates share the mpmath interval library.

## 12. Files

- Model checks and evaluation:
  - `osil_eval.py` (50-digit OSIL evaluator);
  - `inspect_osil.py`;
  - `ivnp.py` (outward-rounded numpy intervals).
- lnts: `lnts_bound.py` → `logs/lnts_*.json`, `logs/lnts_*_primal.txt`.
- dtoc5: `dtoc5_primal.py`, `dtoc5_bound.py` → `logs/dtoc5_bound.json`,
  `logs/dtoc5_y.npy`.
- camshape:
  - `camshape_model.py`, `camshape_bound.py` → `logs/camshape*_bound.json`,
    envelopes `logs/camshape*_envelope.npy`;
  - generic cell DP: `camshape_celldp.py` → `logs/camshape_celldp.jsonl`.
- optcdeg2:
  - main: `optcdeg2_common.py`, `optcdeg2_bound.py` (state bounds, full
    Lagrangian), `optcdeg2_head.py` (exact head block), `optcdeg2_verify.py`
    (mpmath recheck), `optcdeg2_primal.py`;
  - failed attempts: `optcdeg2_blockdp.py`, `optcdeg2_dualopt.py`;
  - logs: `logs/optcdeg2_*`.
- lukvle10: `lukvle10_lagr.py`, `lukvle10_bound.py`, `lukvle10_sanity.py`
  → `logs/lukvle10_bound_K3.{json,log}`, `logs/lukvle10_sanity.json`.
- Rechecks: `verify_independent.py` → `logs/verify_independent.json`.
- SCIP: `run_scip_baseline.py`, `scip_primal_check.py`.
- Downloaded MINLPLib points (www.minlplib.org/sol): `minlplib_sol/`.
