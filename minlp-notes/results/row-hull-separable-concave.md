# Row hulls: joint convexification of separable concave terms along a linear row

Date: 2026-09-21. Status: theory, implementation and experiments by the root
agent; literature check by a separate research agent completed. The
[independent theory review](../notes/review-row-hull-theory.md) confirmed the
hull statements in 385 exact-versus-LP comparisons written from the statements
alone, and found one misstated theorem (2(c) lacked `0 <= z_i <= w y_i`), one
false universal remark and several missing conventions; all are corrected here.
The [independent code and experiment review](../notes/review-row-hull-code-experiments.md)
found a bug in the pricing routine that produced invalid cuts on data with few
decimals (two recorded runs lost the true optimum within the gap tolerance);
it was fixed, a regression test added and every affected run repeated. The
numbers below are from the repeated runs.
Experimental details and negative results are in
[the experiment record](../notes/row-hull-experiments.md).

A further audit on 2026-09-22 repaired the merged-pricing approximation proof,
the mixed-row pricing expression and two scope remarks below. It also found
that inverse affine rounding could evaluate a downward endpoint jump inside
the interval and assign a false nonzero endpoint gap. Exact normalized
endpoints now use the original endpoint values and zero chord gaps; a
singleton-row regression independently checks that pricing and separation
do not exclude its feasible point. The targeted suite passes 217 tests.
These checks do not rerun or recertify the historical benchmark results.

## Summary

Global solvers relax each univariate concave term `t_i >= f_i(x_i)` by its
chord and intersect the result with the linear rows. A conservation row
`sum_i a_i x_i = b` makes the terms interact: at every vertex of the row
polytope at most one variable is strictly inside its interval, so at most one
term can be away from its chord at the same time, and when no subset of the
widths sums to the right-hand side exactly one must be. The
term-by-term relaxation misses this. The repository already proves that spatial
branch-and-bound needs `2^Omega(n)` nodes to recover it
([lower bound](spatial-bb-exponential-lower-bound.md)).

This note studies the **row hull**

```
Q = conv{ (x, t) : sum_i a_i x_i = b,  l <= x <= u,  t_i >= f_i(x_i)  (i in I) },
```

the joint convex hull of all concave terms on one row, as a source of cutting
planes for multi-row models.

- **Closed form for equal widths (Theorem 2; equivalent to a classical
  description, see below).** If all
  widths `|a_i|(u_i - l_i)` equal `w` and the right-hand side leaves a residual
  `0 < r < w`, the row hull is the term-wise relaxation plus **one** concave
  piecewise-linear inequality,
  `sum_i min{ z_i/r, (w - z_i)/(w - r), tau_i/delta_i } >= 1`,
  in normalized variables `z_i`, chord gaps `tau_i` and `delta_i = gamma_i(r)`.
  It has a compact extended form with `n` extra continuous variables and no
  binaries. A [focused source check](../notes/row-hull-ktr-overlap-check.md)
  showed that this polyhedron is the constant-capacity single-node flow
  polyhedron of Padberg, Van Roy and Wolsey (1985) in other variables: `Q`
  depends on `gamma_i` only through `delta_i`, and a fixed charge with the same
  `delta_i` has the same hull. What is added here is the observation that their
  description is the row hull of *arbitrary* concave terms, the single-inequality
  and extended forms, inequality rows (2(b)), and indicators together with
  concave variable costs (2(c)). The tilted flow covers of Lim, Linderoth and
  Luedtke (2018), specialized to this set, are a strict subfamily of the
  linearizations.
- **General widths (Propositions 3–5).** The same inequality with residual
  intervals `[a_i, b_i]` is valid but not the hull. Optimizing over `Q` is
  NP-hard (known). Exact separation is a concave-residual knapsack; an interval
  subset-sum dynamic program gives exact separation for well-scaled data and
  otherwise cuts that are valid up to floating point.
- **Limits (Proposition 6).** Intersecting the row hulls of all rows is not the
  joint hull of the model: in a three-variable example the row hulls give the
  bound 0 while the optimum is 1/2. Row hulls of aggregated rows repair that example.
- **Computation.** On synthetic concave-cost transportation and network-flow
  families the row-hull cuts close 64–88% (family means) of the root gap left by
  the term-wise relaxation. As static root cuts handed to unmodified solvers
  (time limit 300 s, including cut generation, model construction and solving;
  instance generation excluded) they raise the number of solved
  instances from 96 to 124 of 130 for Gurobi 13, from 18 to 41 of 44 for SCIP 10
  and from 15 to 44 of 50 for BARON. **Most of that gain comes from the
  equal-width families built to satisfy Theorem 2** (Gurobi: 24 to 47 of 50,
  68 s to 10 s); with unequal widths Gurobi goes from 72 to 77 of 80 and from
  10.8 s to 8.8 s mean time, and 45 of the 54 instances it solves in under 10 s
  become slower. The bound is only modestly stronger than the exhaustive
  closure of the tilted flow covers, and a structural scan finds an applicable
  row in only 4.8% of MINLPLib. See [Computational results](#computational-results).

## Setting and normalization

A row `sum_i a_i v_i (<=, =, >=) b` with bounds `l <= v <= u` is rewritten with
`z_i = a_i (v_i - l_i)` for `a_i > 0` and `z_i = |a_i| (u_i - v_i)` for
`a_i < 0`, so that `0 <= z_i <= w_i := |a_i| (u_i - l_i)`,
`B = b - sum_{a_i>0} a_i l_i - sum_{a_i<0} a_i u_i`, and

```
X = { z : sum_i z_i = B,  0 <= z_i <= w_i },
```

after adding one slack item (with its own width) for an inequality. Variables
without a concave term, relaxed integer variables and the slack are items with
`gamma = 0`. Items with `a_i = 0` or `l_i = u_i` are removed (the latter into
`B`), and `0 <= B <= sum_i w_i` is assumed so that `X` is nonempty. For an item
with `f_i` concave and finite on the closed interval (this allows a downward
jump at an end point, as for a fixed charge; the value `f_i(l_i)` is arbitrary
because only the chord gap is used) define the chord gap

```
gamma_i(z) = f_i(v_i(z)) - chord_i(v_i(z)) >= 0,       tau_i = t_i - chord_i(v_i),
```

which is concave on `[0, w_i]` and zero at both ends. The term-wise relaxation
is `tau >= 0`. The object of study is

```
Q = conv{ (z, tau) : z in X,  tau_i >= gamma_i(z_i) for all i }.
```

Because `X` and the chords are affine images, `Q` describes the row hull in the
original variables. `Q` is a valid relaxation of any model that contains the
row, the bounds and `t_i >= f_i(x_i)` (or `t_i = f_i(x_i)`), for any subset of
the terms, whatever its other constraints. With equality terms the cuts are
valid but the hull of the graph is smaller than `Q`; a model that contains only
`t_i <= f_i(x_i)` is not covered. By Proposition 1, `Q` is a polytope plus a
polyhedral cone, so no closure is needed even with end-point jumps.

A vertex of `X` has at most one coordinate strictly inside its interval
(textbook). Write a vertex as `(S, j, r)`: `z_i = w_i` on `S`, `z_j = r =
B - w(S) in [0, w_j]`, zero elsewhere. `X` is *nondegenerate* if no subset sum
of widths equals `B`; then every vertex has exactly one interior coordinate.

## Proposition 1 (vertex generation; classical)

`Q = conv{ (v, gamma(v)) : v vertex of X } + {0} x R^n_+`.

*Proof.* Let `z in X` and write `z = sum_v lambda_v v` over vertices. For every
`i`, concavity gives `gamma_i(z_i) >= sum_v lambda_v gamma_i(v_i)`. The same
multipliers work for all `i` simultaneously, so `(z, gamma(z))` lies in the
right-hand side, which is convex and closed under increasing `tau`. The other
inclusion is clear. QED

This is the Falk–Hoffman vertex argument applied to all terms at once. The
point is only that a single convex combination serves every term, so the hull
of the *vector* of terms, not just of their sum, is vertex generated.

**Corollary 1' (when the term-wise relaxation is already the hull).** The
argument of Proposition 1 uses nothing about `X` except that it is a polytope.
So for any polytope `P` (any number of rows) the joint hull of the concave
terms over `P` equals the term-wise relaxation `{x in P, tau >= 0}` if and only
if no vertex of `P` has a concave item with `gamma_i(v_i) > 0`, equivalently,
every vertex keeps all nonaffine concave items at their bounds. Strict
concavity is not required: a nonzero concave gap with zero endpoint values
is positive throughout the open interval. (If a vertex `v` has
`gamma_i(v_i) > 0`, the point `(v, 0)` is term-wise feasible, and its only
representation by vertices is `v` itself.) Examples where combining the
individual relaxations loses nothing: totally unimodular rows with unit-width
boxes and integral right-hand sides; one row with equal widths and `r = 0`.
Everywhere else the loss at a vertex is exactly the sum of the gaps of its
interior concave items. This is a direct consequence of vertex generation (in
the spirit of Tardella 2008) and is not claimed as new.

## Theorem 2 (equal widths)

Let `w_i = w > 0` for all `i`, `B = k w + r` with `k` integer, `0 <= k <= n-1`
and `0 < r < w`, and
`delta_i = gamma_i(r)`. Then

```
Q = { (z, tau) : z in X,  tau >= 0,
      sum_i min{ z_i / r,  (w - z_i)/(w - r),  tau_i / delta_i } >= 1 },          (RH)
```

where the third entry is omitted when `delta_i = 0`. Equivalently `(z, tau) in Q`
iff `z in X` and there is `zeta` with

```
sum_i zeta_i = 1,   zeta >= 0,   r zeta_i <= z_i,   (w - r) zeta_i <= w - z_i,
delta_i zeta_i <= tau_i.                                                           (EF)
```

If `r = 0`, `Q` is the term-wise relaxation `{z in X, tau >= 0}`.

*Proof.* (EF) and (RH) are equivalent: a `zeta` as in (EF) exists iff the upper
bounds `m_i = min{z_i/r, (w - z_i)/(w - r), tau_i/delta_i}` are nonnegative
(true on `X`, `tau >= 0`) and sum to at least one.

*`Q` satisfies (RH).* The left-hand side of (RH) is a concave function of
`(z, tau)`, nondecreasing in `tau`. By Proposition 1 it suffices to check vertex
points. At `(S, j, r)` the `j`-th term is `min{1, 1, gamma_j(r)/delta_j} = 1`
and the other terms are nonnegative.

*(EF) implies membership.* Given `(z, tau, zeta)`, put `y_i = (z_i - r
zeta_i)/w`. Then `y >= 0`, `y_i + zeta_i <= 1`, `sum zeta = 1`, and `sum y =
(B - r)/w = k`. The constraint matrix of
`T = {(y, zeta) >= 0 : sum y = k, sum zeta = 1, y_i + zeta_i <= 1}` has two
ones per column, one in the rows `{sum y, sum zeta}` and one in the rows
`{y_i + zeta_i}`; it is the incidence matrix of a bipartite graph, hence
totally unimodular, and `T` is integral. So `(y, zeta) = sum_p lambda_p
(1_{S_p}, e_{j_p})` with `|S_p| = k`, `j_p` not in `S_p`. The points
`v^p = w 1_{S_p} + r e_{j_p}` are vertices of `X` with `gamma(v^p) =
delta_{j_p} e_{j_p}`, and `sum_p lambda_p v^p = w y + r zeta = z`,
`sum_p lambda_p gamma(v^p) = (delta_i zeta_i)_i <= tau`. QED

**Linear description.** (RH) holds iff every selection of one entry per `min`
sums to at least one. With `F` the items that select `tau_i/delta_i`, `T_1`
those that select `z_i/r` and `T_2` those that select `(w - z_i)/(w - r)`:

```
sum_{i in F} tau_i/delta_i + sum_{i in T_1} z_i/r + sum_{i in T_2} (w - z_i)/(w - r) >= 1.      (F, T_1, T_2)
```

Separation is `O(n)`: take the smallest entry of each `min`.

**Interpretation.** The row forces one unit of "interior mass" `zeta`. Item
`i` can absorb at most the tent `min{z_i/r, (w - z_i)/(w - r)}` of it, and pays
`delta_i` per unit. On the repository's lower-bound family (`w = 1`, `r = 1/2`,
`gamma_i(z) = c_i z(1-z)`), (RH) gives `sum_i tau_i/c_i >= 1/4` directly, so the
root relaxation is exact, while every spatial branch-and-bound that only
branches and uses term-wise relaxations needs `2^Omega(n)` nodes. For the
quadratic family a [classical clique inequality](../notes/spatial-bb-known-clique-cut.md)
in lifted product variables also closes the root gap; (RH) needs no lifted
variables and holds for arbitrary concave terms.

### Theorem 2(b): inequality rows

Let all widths equal `w` and let the row be `sum_i z_i <= k w + r` or
`sum_i z_i >= k w + r` with `0 < r < w`. With the same `delta_i = gamma_i(r)`
and the same three-entry minimum `m_i(z_i, tau_i)`, the row hull is the
term-wise relaxation plus

```
sum_i m_i >= (sum_i z_i - k w) / r              for  "<=",
sum_i m_i >= ((k+1) w - sum_i z_i) / (w - r)    for  ">=".
```

*Proof.* For `<=`, the vertices of the row polytope are the points
`w 1_S` with `|S| <= k` and the points `w 1_S + r e_j` with `|S| = k`. The
points `w 1_S + r e_j` with `|S| < k` are feasible and have gap vector
`delta_j e_j`, so they may be added to the generators. The generators are the
integer points of `{(y, zeta) >= 0 : sum y <= k, sum zeta <= 1, y_i + zeta_i
<= 1}` under `z = w y + r zeta`, `tau >= delta o zeta`; the matrix is again a
bipartite incidence matrix with slacks. Eliminating `y_i = (z_i - r zeta_i)/w`
leaves `0 <= zeta_i <= m_i` and `(sum z - k w)/r <= sum zeta <= 1`, which is
solvable iff the stated inequality holds, because `sum z <= k w + r` makes the
right-hand side at most one. The `>=` case is the reflection `z -> w - z`,
which maps `r` to `w - r` and keeps `delta_i`. QED

### Theorem 2(c): fixed-charge indicators

Let `X^y = {(z, y, tau) : sum z = k w + r, 0 <= z_i <= w y_i, y binary,
tau_i >= gamma_i(z_i)}`, where `gamma_i` is the chord gap of the variable cost
on `[0, w]`. Then `conv(X^y)` is given by `0 <= z_i <= w y_i`, `y <= 1`,
`tau >= 0`, the row and

```
sum_i min{ z_i / r,  (w y_i - z_i)/(w - r),  tau_i / delta_i } >= 1.
```

*Proof.* As for Theorem 2 with the extra constraints `y_i + zeta_i <= Y_i <= 1`
in place of `y_i + zeta_i <= 1` (here `Y` is the indicator); the matrix stays
totally unimodular (sign the two sum rows `+` and the item rows `-`), and the
indicator of an unused arc is free. Eliminating the full-arc variable gives
`zeta_i <= (w Y_i - z_i)/(w - r)`. QED

Selecting the second entry on a cover `C` with `|C| = k+1` and the first entry
elsewhere gives, after using the row, the flow cover inequality
`sum_C z_i + r sum_C (1 - y_i) <= k w + r`. Selecting the third entry on
`F ⊆ C` gives the tilted flow covers below. So one inequality contains the
flow covers and their tilted versions, and its selections contain all facets
of the constant-capacity equality set. (The bounds `0 <= z_i <= w y_i` are
needed in the statement: they follow from the extended form but not from the
min-sum inequality alone.) The same elimination with Theorem 2(b) gives, for
`sum z <= k w + r` with indicators,
`sum_i min{z_i/r, (w y_i - z_i)/(w-r), tau_i/delta_i} >= (sum_i z_i - k w)/r`;
this remark was checked numerically by the reviewer and is not proved here.

All three parts are checked against brute-force vertex enumeration in
`code/row_hull/test_rowhull.py` (equality of support functions in random
directions, 70 random sets) and, independently and with exact vertex values,
in `code/row_hull/review/check_theorem2.py` (385 sets).

### Relation to tilted flow covers

Lim, Linderoth and Luedtke (2018) study the concave single-node flow set with
indicators `z_i` (their notation) and derive tilted simple generalized flow
cover inequalities from a cover `C` with excess `mu = u(C) - d`, tilting the
items `F ⊆ C` at the points `m_i = u_i - mu`. Their Theorem 4 coefficients at
`z = 1` give, in the present notation and after using the equality row,

```
sum_{i in F} tau_i/gamma_i(m_i) * (mu m_i / u_i) >= sum_{C\F} x_i + sum_F (mu/u_i) x_i + sum_F m_i - d.
```

For equal capacities `|C| = k+1`, `mu = w - r`, `m_i = r`, and this is exactly
`(F, T_1, T_2)` with `T_1 = N \ C` and `T_2 = C \ F` (derivation: substitute
`sum_{C\F} x_i = d - sum_F x_i - sum_{N\C} x_i` and multiply by
`w / (r (w - r))`). So their inequalities, restricted to this set, are the
selections with `|F| + |T_2| = k + 1` (covers with `|C| >= k+2` have
`mu >= w` and nothing to tilt). Their set has the row `sum x <= d`; without
using the equality, their inequality times `w/(r(w-r))` is identically the same
selection of the Theorem 2(b) inequality (reviewer's symbolic check,
`code/row_hull/review/check_lll.py`). An exact witness of strictness: `n = 3`,
`k = 1`, `w = 1`, `r = 1/2`, `delta_i = 1/4`, objective `sum_i tau_i/delta_i`;
the hull value is 1, but `z = (1/2,1/2,1/2)`, `tau = 0` satisfies every
selection with `|F| + |T_2| = 2`; the missing inequality is `F = N`. The script
`code/row_hull/check_lll_subfamily.py` optimizes random linear objectives over
both systems: the cover subfamily gave a strictly weaker bound in 6 of 30
random trials. Their paper gives complete descriptions of single-term sets and facet
conditions for the flow set, not a complete description of the flow set;
Theorem 2 supplies the complete description for the indicator-free
equal-capacity equality case.

**Equivalence with Padberg, Van Roy and Wolsey (1985).** `Q` depends on
`gamma_i` only through `delta_i`. Take the fixed charge `h_i = delta_i w/(w-r)`
with indicator `y_i`; its chord gap at `r` is `delta_i`, and with
`tau_i = h_i (y_i - z_i/w)` one has `tau_i/delta_i = (w y_i - z_i)/(w - r)`.
So (RH) is the constant-capacity single-node flow polyhedron with equality row,
which their lifted flow cover inequalities describe completely (as stated by
Atamtürk, Gómez and Küçükyavuz 2016; the 1985 paper itself was not accessible,
only its abstract). The strictness witness `F = N` above is a lifted flow cover
with `|C| > k+1`. Theorem 2 is therefore a re-presentation of a classical
result, not a new polyhedron; Theorem 2(c) with linear variable costs is that
result itself. We did not find Theorem 2(b) or Theorem 2(c) with concave
variable costs in the sources we could read. The
correspondence above is our own derivation from their Theorems 3–4 and was not
checked against their code.

## Proposition 3 (general widths: a valid closed form)

Let `X` be nondegenerate. For each item `i` that is the interior coordinate of
some vertex, let `0 < a_i <= b_i < w_i` bound its value over those vertices,
and let `delta_i = min{gamma_i(a_i), gamma_i(b_i)}`. Then

```
sum_i min{ z_i / a_i,  (w_i - z_i)/(w_i - b_i),  tau_i / delta_i } >= 1
```

is valid for `Q`. Items that are never interior are left out of the sum, the
third entry is omitted when `delta_i = 0`, and `[a_i, b_i]` may be any valid
bounds, not only the exact extremes. If `X` is degenerate the inequality is
invalid (a vertex with all coordinates at bounds makes the left side zero).

*Proof.* The left-hand side is concave and nondecreasing in `tau`. At a vertex
`(S, j, r)`: `r / a_j >= 1`, `(w_j - r)/(w_j - b_j) >= 1`, and
`gamma_j(r) >= delta_j` because a concave function on `[a_j, b_j]` is at least
the smaller end value. All other terms are nonnegative. QED

*Lattice corollary.* If all widths are positive multiples of `g > 0` and
`B = q g + r` with `0 < r < g`, then `X` is nondegenerate and `a_i = r`,
`b_i = w_i - g + r` are valid.
This is the analogue of rounding arguments for mixed-integer rows: the
inequality exists because the right-hand side is off the lattice of the
capacities.

The inequality is the hull for equal widths and in general not the hull
otherwise (it can be: `w = (1,2)`, `B = 3/2`); on
random-capacity transportation rows it recovers only a fraction of what the
exact hull gives (see the experiment record).

## Proposition 4 (hardness; known)

Linear optimization over `Q` is NP-hard. With `gamma_i(z) = z (w_i - z)`,
`min{ sum_i tau_i : (z,tau) in Q } = 0` iff some subset of the widths sums to
`B`. This is the classical hardness of concave knapsack problems (Moré and
Vavasis 1991); Dey and Kocuk (2025, Proposition 1) give the same reduction for
the graph of `x^kappa` over a row. By the polynomial equivalence of optimization and
separation, separation is NP-hard as well.

## Proposition 5 (separation with a valid constant)

`(z^, tau^)` lies in `Q` iff the membership linear program

```
min s :  sum_v lambda_v v = z^,  sum_v lambda_v = 1,
         sum_{v : j(v) = i} lambda_v gamma_i(r_v) - rho_i s <= tau^_i,   lambda >= 0, s >= 0
```

is feasible with value zero (`rho_i = sup gamma_i` is a normalization; the
program is infeasible for `z^` outside `X`). Its duals
`(pi, pi_0, omega >= 0)` price a vertex `(S, j, r)` at

```
phi(S, j) = omega_j gamma_j(r) - pi_j r - sum_{i in S} pi_i w_i,       r = B - w(S) in [0, w_j].
```

For any `pi`, `omega >= 0` and any lower bound `L <= min_{(S,j)} phi(S, j)`,

```
sum_i omega_i tau_i >= sum_i pi_i z_i + L
```

is valid for `Q`. *Proof.* It holds at every vertex point by the definition of
`L`, and increasing `tau` preserves it; apply Proposition 1. QED

The implementation computes `L` by a sparse subset-sum dynamic program over the
items other than `j` (leave-one-out by divide and conquer). States are subset
sums with the best profit `sum_S pi_i w_i`; when more than `K` distinct sums
appear, neighbours are merged into intervals that keep the largest profit.
Since `r -> omega_j gamma_j(r) - pi_j r` is concave, its minimum over the
induced interval of `r` is at an end point, so the merged program still returns
a lower bound. The program is exact when the distinct subset sums fit
(equal or few distinct widths, integer data of moderate size) and an outer
approximation otherwise. A merged interval of `r` is clipped to `[0, w_j]`,
not discarded, and a clipped end point is evaluated with the true value
`gamma_j = 0`. The cut constant never depends on the accuracy of the
linear program. Validity is in floating point with a relative safety margin of
`1e-9`; no exact arithmetic is used.

**Accuracy of the merged program.** Consider the ideal arithmetic version,
with only exactly equal sums identified and merge grid `Delta = B/K`.
A state is an interval of subset sums of length at most `n Delta`: each
of the at most `n` merges along a path adds at most `Delta` to its maximum
length. The state retains the largest profit `P` of its subsets. Its
maximizing subset need not be feasible for the current interior item after
the residual interval is clipped, so a comparison only with feasible subsets
of that state does not prove an approximation bound.

A global comparison does. Suppose every `gamma_i` is `L_i`-Lipschitz and
put `C = max_i (omega_i L_i + |pi_i|)`. For the state and item `j` attaining
the returned lower bound, choose a clipped residual endpoint `r` attaining
its endpoint minimum and a retained subset `S` with profit `P`. The box
point `u = w 1_S + r e_j` has objective
`H(u) = sum_i omega_i gamma_i(u_i) - pi_i u_i = L`, and its row residual
has magnitude at most the state's length, hence at most `n Delta`.
Because `0 <= B <= sum_i w_i`, coordinates can be increased or decreased
within their bounds to obtain a point `v in X` with
`||v-u||_1 = |sum_i u_i-B|`. Thus `H(v) <= L + C n Delta`.
Concavity of `H` and vertex generation give `phi* <= H(v)`, proving

```
phi* - C n B / K <= L <= phi*.
```

The divide-and-conquer program handles `O(n K log n)` states. This is an
additive approximation guarantee for **pricing a fixed dual vector**; it
does not by itself establish an approximate separation guarantee for the
whole membership problem. The floating-point implementation additionally
merges nearby sums and evaluates functions without directed rounding, so
the displayed bound is an ideal-arithmetic statement, not a numerical
certificate. For continuous non-Lipschitz terms such as square roots, the
same repair argument gives the weaker error bound
`sum_i omega_i modulus_i(n Delta) + ||pi||_infinity n Delta`, where
`modulus_i(d) = sup{|gamma_i(a)-gamma_i(b)| : |a-b| <= d}` on the item
interval. At an endpoint jump no vanishing continuity bound is available;
only the pricing lower-bound argument remains.

## Proposition 6 (what row hulls cannot see)

Let `x in [0,1]^3`, rows `x_1 + x_2 + x_3 = 2` and `x_1 + x_2 - x_3 = 1`,
objective `min sum_i x_i(1 - x_i)`, so `gamma_i(x) = x(1 - x)`. Both rows have integral right-hand sides on unit
widths, so both row hulls equal the term-wise relaxation and the relaxation
bound is `0` (at `x = (3/4, 3/4, 1/2)`, `tau = 0`). Every feasible point has
`x_3 = 1/2` and `x_1 + x_2 = 3/2`; the feasible vertices are
`(1, 1/2, 1/2)` and `(1/2, 1, 1/2)` and the optimal value is `1/2`.
Subtracting the rows gives `2 x_3 = 1` and adding them gives
`2 x_1 + 2 x_2 = 3`; the row hulls of these two aggregated rows give
`tau_3 >= 1/4` and `tau_1 + tau_2 >= 1/4`, which is exact here. Row hulls of
linear combinations of rows are valid for the same reason as the original
ones; choosing combinations plays the role that row aggregation plays for
mixed-integer rounding cuts. No aggregation heuristic is implemented.

## Remark 7 (rows that also carry convex terms; not implemented)

Let the row also contain items `v in V` with convex terms `t_v >= g_v(z_v)`.
Fixing `z_V` and applying Proposition 1 to the remaining row shows that the
hull is generated by points in which at most one concave item is strictly
inside its interval; the convex items are arbitrary, so the generating set is
no longer finite. Pricing a dual vector then asks, for each subset `S` of full
concave items and each interior item `j`, for

```
min_sigma  G(sigma) + omega_j gamma_j(B - w(S) - sigma) - pi_j (B - w(S) - sigma)
           - sum_{i in S} pi_i w_i,
G(sigma) = min{ sum_v theta_v g_v(z_v) - pi_v z_v : sum_v z_v = sigma, z_V in its box },
```

a one-dimensional minimization of a convex plus a concave function (closed form
for quadratics: the sum is a quadratic on each piece of `G`). Restrict `sigma`
to the range for which `G` is finite and the residual lies in `[0,w_j]`.
For equal concave-item widths, the one-dimensional part depends on `S` only
through `|S|`; its full-item profit still depends on the selected items.
For each cardinality and `j`, choose the largest profits `pi_i w_i` among
items other than `j`. Thus optimization over the mixed row hull is polynomial
given that one-dimensional oracle. Cases with every concave item at a bound
are covered by allowing residual endpoints; if there are no concave items,
the remaining problem is convex. We did not find a closed form:
inside one type `(|S|, j)` the set is the simultaneous hull of convex epigraphs
and one concave function of a linear form, which is the object of Liers et al.
(2021). At a vertex where a linear item's coordinate is strictly inside its
interval, every concave item is at a bound. Vertices with a positive concave
gap therefore have every linear item at a bound. The resulting hull cuts
can nevertheless strengthen points where a linear item is interior:
for `z_1+z_2+s=3/2`, `z_1,z_2 in [0,1]`, `s in [0,3/2]`, and gaps
`z_i(1-z_i)`, the point `z_1=z_2=3/5`, `s=3/10`, `tau=0` violates
Theorem 2(b). For
`x^3`-like terms the envelope gap ends at a tangent point, and the best concave
minorant with the right end values is the chord, so the concave device adds
nothing there.

## Context: the Shapley–Folkman gap

Let the concave terms enter only the objective, let there be `m` rows in total
besides bounds, and no integrality constraints. A basic optimal solution of
the term-wise relaxation has at most `m` variables strictly inside their
intervals, so its gap is at most the sum of the `m` largest `rho_i` (classical;
the general Shapley–Folkman form is due to Aubin and Ekeland). The gap is small
relative to the objective when `n >> m`, yet the repository's lower bounds show
that spatial branching with term-wise (and SDP–RLT) node relaxations cannot
close it in polynomial size even for `m = 1`. For one row the set `Q` has no
gap; computing with it is easy for equal widths and NP-hard in general. For several rows it closes a
measured 64–88% (family means) on the transportation families below (where `m` is of the order
of `sqrt(n)`); we have no worst-case guarantee for `m >= 2`, and Proposition 6
shows that none of the form "a fixed fraction" can hold without aggregation.

## Computational results

Full tables, setup, solver errors and negative findings are in the
[experiment record](../notes/row-hull-experiments.md). All runs: 300 s limit on
the total time including the Python cut loop, relative gap `1e-4`, seeds 0–4,
frozen code, unmodified solvers receiving plain linear rows.

1. **Root gap.** Family means of the closed root gap lie between 64% and 88%
   for transportation (uniform, random and uncapacitated arcs; quadratic,
   logarithmic and square-root costs), 66–81% for sparse transshipment networks,
   and 75–92% for fixed charge plus concave cost.
2. **Gurobi 13 (4 threads), 130 instances.** Solved: 96 without, 124 with cuts;
   28 only with cuts, none only without. Shifted geometric mean time 22.3 s
   against 9.1 s. The split matters: on the 50 `uniform` instances (unit
   capacities and fractional supplies, so Theorem 2 applies to every row and
   no cut loop is needed) 24 against 47 are solved and the mean time drops from
   68.5 s to 9.6 s; on the 80 instances with unequal widths 72 against 77 are
   solved and the mean time goes from 10.8 s to 8.8 s, with gains on hard
   families (`transport-random-sqrt-10x15`: 170 s against 36 s) and losses on
   easy ones (45 of the 54 instances solved in under 10 s become slower). A
   control with the quadratic stated directly in the objective changes Gurobi's
   times by at most about 40% and no conclusion.
3. **SCIP 10 and BARON (1 thread).** SCIP 18 against 41 of 44; BARON 15 against
   44 of 50; no instance is solved only without cuts. Both solvers are weak on
   these models to begin with.
4. **Fixed charges.** With Gurobi's flow covers active in both forms: 37
   against 40 of 40, mean time 12.9 s against 6.5 s; `uniform` 18.8 s against
   2.7 s, unequal widths 8.8 s against 14.0 s. Gurobi's own root cuts leave a
   2–7% root gap; adding the row-hull rows leaves 0.7–3.9%.
5. **Inside the tree (measured; negative).** In a minimal best-bound spatial
   branch-and-bound, exact row-hull separation on every node box needs 5–29
   times fewer nodes than root cuts alone. In SCIP 10 this does not transfer: a
   PySCIPOpt separator on node boxes reduces SCIP's nodes by a factor 1.3–3.4
   at full depth and by 5–20% to depth 8, while the callback (column generation,
   since branching makes local widths unequal) makes the runs 4–5 times slower
   than root-only separation, which is the best configuration on every family
   tested (`8x12`, four families, five seeds, 300 s).
6. **Against tilted flow covers.** The exhaustive closure of the
   Lim–Linderoth–Luedtke family at `z = 1` recovers 85–100% of the row-hull
   bound improvement on small instances.
7. **Failures.** Easy instances become slower; one `sqrt` run with cuts ended
   with Gurobi status 13; the first implementation produced invalid cuts on
   two-decimal data (found by the code review, fixed, rerun); the general-width closed form, dense general rows and
   aggregated rows gain little; MINLPLib reach is 77 of 1,601 instances.

## Literature

- Lim, Linderoth, Luedtke, *Valid inequalities for separable concave
  constraints with indicator variables*, Math. Program. 172 (2018): tilted flow
  cover and tilted `(l,S)` inequalities for concave single-node flow and
  lot-sizing sets with indicators; facet conditions; BARON experiments. Closest
  prior work. No complete description, no extended formulation, no general
  separation.
- Dey, Kocuk, *Convexification of a separable function over a polyhedral
  ground set*, arXiv 2510.16595 (2025): graph of `x_j^kappa` over a row and
  other polytopes; NP-hardness; conic relaxations; exact hulls in low
  dimension. Two-sided convex terms rather than one-sided concave ones.
- Liers, Martin, Merkert, Mertens, Michaels, J. Glob. Optim. 80 (2021):
  simultaneous convexification at degree-three gas junctions after eliminating
  one flow.
- Padberg, Van Roy, Wolsey (1985): lifted flow covers describe the
  constant-capacity single-node flow set; equivalent to Theorem 2 (above).
  Kim, Tawarmalani, Richard (2022) permute `x` alone and do not give the joint
  hull of a vector of terms ([check](../notes/row-hull-ktr-overlap-check.md)).
- Keha, de Farias, Nemhauser (2006); Zhao, de Farias (2013): cuts for a
  knapsack row in SOS2 variables of piecewise-linear functions; no complete
  description.
- Qu et al., J. Optim. Theory Appl. 209 (2026), Lemma 2.2: count-plus-remainder
  optimum for identical concave terms on one row, as an integer reformulation.
- Kim, Tawarmalani, Richard, Math. Oper. Res. 47 (2022): convexification of
  permutation-invariant sets over congruent bounds. With equal widths *and
  identical* `gamma_i` the set behind `Q` is permutation invariant and may be
  within their framework (not checked theorem by theorem; the literature agent
  read the arXiv version and found no item-dependent terms or weights).
  Item-dependent `gamma_i` break the invariance. For `k = 0` (RH) reduces to the
  classical simplex envelope `tau_i >= delta_i z_i / r` (orthogonal
  disjunctions, Tawarmalani–Richard–Chung 2010).
- Falk, Hoffman (1976); Horst, Tuy: vertex-generated envelopes of concave
  functions over polytopes. Tardella (2008): sum decomposition of vertex
  polyhedral envelopes.
- Repository: [vertex binarization](separable-vertex-binarization.md) uses the
  same vertex structure as an optimality-based binary reformulation. Row-hull
  cuts are relaxation cuts: they stay valid with any other constraints and with
  `t_i = f_i(x_i)` used elsewhere in the model.

Claim: Theorem 2 is equivalent to the Padberg–Van Roy–Wolsey description. To
our knowledge the following are not in the sources we could read: the
observation that this description is the row hull of arbitrary separable
concave terms (no indicators needed), its single-inequality and extended forms,
Theorem 2(c) with concave variable costs, the residual-interval inequality of
Proposition 3, the interval dynamic program for valid separation on general
rows, and the computational use as solver-independent root cuts. Wolsey and
Yaman (2021) on generalizations of the constant-capacity flow set was seen in
abstract only. The literature agent could not access
several items (listed in the experiment record), and an unsuccessful search
does not establish novelty.

## Limitations

- Only terms that are concave on the whole current interval are used. Terms
  with convex parts contribute nothing; rows with convex terms are reduced to a
  one-dimensional pricing problem in Remark 7 but not implemented.
- Cuts are generated once at the root. They remain valid in the tree but do
  not tighten with branching. Local separation was implemented as a SCIP
  separator and measured; with column-generation separation at nodes it does
  not pay (item 5 above). The closed form is not available below the root
  because branching destroys equal widths.
- The cuts are dense in the row. On easy instances the cut loop and the slower
  node relaxations cost more than they save.
- Rows with more than 63 items are skipped by the prototype.
