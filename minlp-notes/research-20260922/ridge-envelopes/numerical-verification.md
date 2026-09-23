# Numerical verification of Theorem 1 and Corollary 3 (ridge envelopes)

Date: 2026-09-22. Independent computational check of `theory.md` (Theorem 1,
the special cases in "Computing (D)", and Corollary 3). `theory.md` was not
edited. Code: `code/`. Raw records: `code/results/*.json`.

## Summary

- No discrepancy was found. In 1800 box cases (15 functions `sigma`, both envelope
  sides, n = 1..5), the Theorem 1 value and an independent certified brute-force
  bracket always overlap. The largest gap between the two intervals is
  7.8e-13 R (floating-point noise), and the midpoints differ by at most 2.7e-8 R.
  R is the range of f over B.
- Every cut `h` from (D) is valid. The maximum of `h - f` over the box, computed
  exactly through a 1-D reduction, is at most 3.3e-14 R. On 1e5 random points
  plus all vertices per instance, it is at most 1.6e-15 R. Each cut is tight at x:
  `|h(x) - value|` is at most 2.7e-15 R.
- Corollary 3 (products of simplices) agrees with brute force in 300 cases. The
  comonotone merge and the tail-sum reduction differ by at most 4.7e-9 R, and the
  merge differs from brute force by at most 2.0e-8 R, with no interval separation.
  The tail-sum cuts are valid, with maximum violation 2.4e-12 R.
- The special cases in "Computing (D)" also check out. For convex `sigma` (360
  cases), vex = f to within 5.8e-8 R. For concave `sigma` (352 cases), vex equals
  the Lovász value `sum p_k sigma(t_k)` to within 1.3e-14 R. The S-shape
  structure (sigma at the right nodes and one line through the left nodes) is
  optimal in all 200 sigmoid and tanh cases, with a difference of at most 5.7e-9.
- The envelope over the box is often much tighter than the factorable relaxation
  `vex_I sigma`. The mean gain is 0.04 to 0.15 R for most nonconvex `sigma`, and
  the worst-point gain reaches 0.25 to 1.0 R (details below).

## Methods

**Theorem 1 (`code/ridge_envelope.py`).** The code applies the normalization
from `theory.md`: it drops coordinates with `a_i = 0`, flips coordinates with
`a_i < 0`, scales the box to `[0,1]^n` and absorbs `b` into `sigma`. It then
computes the staircase data `(pi, t_k, p_k)` and solves (D) by a cutting-plane
LP in `y` (Gurobi, feasibility and optimality tolerances 1e-9):

- Concavity of the interpolant is imposed exactly.
- The chord constraints are separated on a 401-point `theta` grid per segment.
  Every local maximum is refined by golden-section search.
- At the end, the chord violation is recomputed on a 20001-point grid with
  refinement, and all `y` are shifted down by it. The shifted `y` are therefore
  feasible, `p.y` is a lower bound of (D), and the last LP value is an upper
  bound of (D).
- The cut `h(x') = y_0 + sum_j (y_j - y_{j-1}) x'_{pi(j)}` is mapped back to the
  original coordinates.

**Brute force (`code/bruteforce.py`), independent of the staircase and of (D).**

- *Grid LP.* This is an upper bound: minimize `sum lam f(z)` over grid points
  `z` with barycenter x, in the original coordinates. The grid has 401, 61, 21,
  11 and 7 points per axis for n = 1..5.
- *Certified bracket.* This solves the semi-infinite LP over affine minorants of
  `sigma(b + sum_j c_j . lam_j)` on a product of simplices (a box is a product of
  two-vertex blocks) by cutting planes.
  - Separation is exact up to a 1-D search. For fixed `s = c.lam`, the maximum of
    `beta.lam` is the upper concave hull of the Minkowski sum of the block point
    sets `{(c_ji, beta_ji)}`, computed by merging hull edges by slope. The
    remaining problem `max_s alpha + M(s) - sigma(b+s)` is solved on a grid of
    2e5 points plus the hull breakpoints, followed by golden-section refinement.
  - The LP value is an upper bound on the envelope. The LP minorant shifted down
    by its exact maximum violation gives a lower bound.
  - The same 1-D reduction gives the exact maximum violation of each cut.

"Rigorous" here means rigorous up to this 1-D global search. The search uses no
interval arithmetic. For these smooth functions on intervals of width up to 8, a
grid spacing of about 4e-5 plus local refinement leaves no realistic room for a
missed maximum.

**Instances.**

- Boxes are `[l,u]`; half of them cross zero. The vector `a` is signed, and
  about 15% of the multi-dimensional instances have one `a_i = 0`.
- `a` and `b` are rescaled so that `I` has width U(0.5, 8) and center
  U(-3, 3). Every box instance therefore has at least one inflection of the
  non-convex functions inside `I`.
- Points are interior, have ties in normalized coordinates, lie on the boundary
  (so some `p_k = 0`), or are vertices.
- The functions `sigma` are: sigmoid, tanh, SiLU, GELU, sin, cos, s^3,
  s^3 - 3s, exp, -exp, log(1+s^2), softplus, s^5 - 5s^3 + 4s (inflections at 0
  and ±sqrt(1.5)), sign(s)|s|^1.852 and exp(-s^2).
- Each function is run as `vex` and as `cave` (the concave envelope, computed as
  `-vex(-f)`; task 6).
- The design is 6 instances × 2 points for each n and side, which gives 60 cases
  per (sigma, side).

## Results

### Box (tasks 2, 3, 6), 1800 cases, all values divided by R

| quantity | worst over all cases |
|---|---|
| midpoint difference, Theorem 1 vs brute force | 2.7e-8 |
| separation of the two intervals (a disagreement would show here) | 7.8e-13 |
| width of the brute-force bracket | 1.2e-7 |
| Theorem 1 lower value minus grid-LP upper bound (must be <= 0) | 1.5e-15 |
| cut violation, 1e5 samples + vertices | 1.6e-15 |
| cut violation, exact 1-D reduction | 3.3e-14 |

These worst cases do not depend on the kind of point: interior, tie, boundary
and vertex points all give a midpoint difference of at most 3.1e-8. The tables
for each function are printed by `run_verification.py box`; no function exceeds
the values above.

Grid convergence (`run_verification.py grid`) was checked for n = 2 and 3. The
gap `(grid upper - Theorem 1)/R` is always >= 0. It shrinks from about 1e-3 at
N = 6 to 1e-6–1e-9 at N = 161 for n = 2, and to 1e-4–1e-10 at N = 41 for n = 3.
The slowest cases are sin and cos with n = 3, at about 1e-4 when N = 41. The
decrease is not strictly monotone because of how the grid aligns with the
optimal support points.

### Products of simplices (task 4), 300 cases

The instances have 2–3 blocks of sizes 2–4. About 30% of them contain a "none"
value of 0, and some block weights are 0. The value is computed in two ways: by
the comonotone merge of block quantile functions (`chain_law`, zero-weight
endpoints of I added) and by the tail-sum map to a chain order polytope plus
Theorem 1.

| check | result |
|---|---|
| merge vs tail-sum | 4.7e-9 R |
| merge vs certified brute force | 2.0e-8 R, separation 4.6e-15 R |
| grid LP on 90 cases (compositions, about 3e4 points) | Theorem 1 never exceeds the grid value (max excess 2.5e-16 R); the median grid gap is 4.2e-7 R |
| tail-sum cut mapped to one-hot variables | violation at most 3.1e-13 R on 2e4 samples + vertices, 2.4e-12 R exact |

### Strength gain (task 5)

The gain is `(vex_B f - vex_I sigma(a^T x + b))/R`. For the `cave` side it is
`(cave_I sigma - cave_B f)/R`. The data are 12 instances per row (n = 2, 3, 5)
with 150 random points each, and "worst" is a pattern search from the three best
of those points.

| sigma | vex: mean / worst | cave: mean / worst |
|---|---|---|
| sigmoid | 0.022 / 0.25 | 0.032 / 0.42 |
| tanh | 0.065 / 0.61 | 0.025 / 0.38 |
| SiLU | 0.002 / 0.14 | 0.074 / 0.75 |
| GELU | 0.038 / 0.45 | 0.060 / 0.88 |
| sin | 0.127 / 1.00 | 0.072 / 1.00 |
| cos | 0.045 / 0.94 | 0.071 / 0.86 |
| s^3 | 0.078 / 0.47 | 0.054 / 0.45 |
| s^3-3s | 0.053 / 0.58 | 0.052 / 0.57 |
| exp | 0 / 0 (convex) | 0.153 / 0.61 |
| -exp | 0.155 / 0.61 | 0 / 0 |
| log(1+s^2) | 0.019 / 0.13 | 0.074 / 0.88 |
| softplus | 0 / 0 (convex) | 0.072 / 0.50 |
| poly5 | 0.154 / 0.78 | 0.060 / 0.76 |
| Hazen–Williams | 0.039 / 0.28 | 0.025 / 0.28 |
| exp(-s^2) | 0.032 / 1.00 | 0.107 / 0.69 |

- The mean gain grows with n: 0.037 for n = 2, 0.055 for n = 3 and 0.085 for
  n = 5.
- Gains near 1 occur at or near vertices. There the box envelope equals f, while
  `vex_I sigma` is at the bottom of an oscillation or a bump.
- The smallest gain observed is -7.7e-8, which is solver tolerance.

### S-shape structure claim

Sigmoid and tanh were tested on 100 interior cases each (n = 2..5). For each
cut point k*, (D) was solved with `y_k = sigma(t_k)` for k > k* and
`y_0..y_{k*}` collinear. The best of these restricted values matched the
unrestricted (D) value within 5.7e-9 in every case. This supports the claim that
an optimal psi with this structure exists. Whether the line is tangent to sigma
was not checked separately.

## Not covered

- Corollary 2 for general posets was not tested, apart from the chain posets
  used by Corollary 3.
- Blocks with equal values `c_ji` were not tested.
- No interval arithmetic was used.

## Reproduction (targeted commands actually run)

```
cd code
PY=~/miniconda3/envs/exact-quadratic-hull/bin/python
$PY run_verification.py box      # 31 s on 30 processes
$PY run_verification.py grid
$PY run_verification.py simplex
$PY run_verification.py sshape
$PY run_verification.py gain     # 188 s
```

scipy is not installed in the environment, so nothing was installed. LPs use
gurobipy's scalar API, and the 1-D maximization is a vectorized golden-section
search with a grid. No CI checks were run or consulted.
