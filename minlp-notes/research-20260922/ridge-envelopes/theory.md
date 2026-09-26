# Convex envelopes of univariate functions of a linear form over a box

Date: 2026-09-22. Status: author draft by the coordinator. A separate
[novelty check](novelty.md) found Step 2 in Mao and Wang (2015) and the
concave and S-shaped special cases in the literature; the characterization for
arbitrary continuous `sigma`, form (D) with its cuts, and the localization
corollaries were not found. An [independent proof review](review-theory.md)
found no wrong theorem or corollary; its fixes (hypotheses on `sigma`,
attainment, exact concavity for cut validity, sign conditions in Corollary 2,
merging equal values in Corollary 3) are applied below.

## Setting

Let `B = [l, u]` be a box in `R^n`, `a in R^n`, `b in R`, and let `sigma` be a
lower semicontinuous real function (for example a continuous one) on the interval `I = {a^T x + b : x in B}`. The
function

```
f(x) = sigma(a^T x + b)
```

is a ridge function; examples are one neuron of a trained network with any
activation, `exp`, `log` or a power of a linear expression, `sin(theta_i - theta_j)`,
and Weymouth or Hazen–Williams laws applied to potential differences.
Factorable solvers relax `f` by an auxiliary variable `w = a^T x + b` and the
envelope of `sigma` over `I`. That relaxation ignores the box, and it is not
the convex hull of the graph of `f` over `B`.

**Normalization.** Coordinates with `a_i = 0` can be dropped: the envelope over a
product box of a function that does not depend on one factor is the envelope
over the other factors. Coordinates with `l_i = u_i` are fixed and are dropped as well. Replacing `x_i` by `l_i + (u_i - l_i) x_i` when
`a_i > 0` and by `u_i - (u_i - l_i) x_i` when `a_i < 0` is an affine bijection
of boxes; convex envelopes commute with affine bijections. Absorbing `b`
into `sigma`, we assume from now on

```
B = [0,1]^n,  a_i > 0 for all i,  I = [0, a_1 + ... + a_n],  f(x) = sigma(a^T x).
```

**Staircase data of a point.** For `x in B` choose a permutation `pi` with
`x_pi(1) >= ... >= x_pi(n)` and set `x_pi(0) = 1`, `x_pi(n+1) = 0`,

```
v_k = e_pi(1) + ... + e_pi(k),   t_k = a^T v_k,   p_k = x_pi(k) - x_pi(k+1),   k = 0..n.
```

Then `p >= 0`, `sum_k p_k = 1`, `x = sum_k p_k v_k`, and `0 = t_0 < t_1 < ... < t_n`.
The vertices `v_0, ..., v_n` span the staircase (Kuhn) simplex `Delta_pi` that
contains `x`. Write `T_x` for the discrete law `sum_k p_k delta_{t_k}`. It is
the law of `a^T X` when `X_i = 1[U <= x_i]` for one uniform `U`, that is, for
comonotone Bernoulli coordinates. It does not depend on how ties in `x` are
broken.

Convex order: for laws `mu, nu` with finite means, `mu <=_cx nu` means
`int phi dmu <= int phi dnu` for every convex `phi`.

## Main theorem

**Theorem 1.** For every `x in B`,

```
vex_B f (x) = min { int sigma dmu : mu a law on I, mu <=_cx T_x }                  (P)
            = sup { sum_k p_k psi(t_k) : psi concave on I, psi <= sigma on I }        (D)
```

The minimum in (P) is attained. The supremum in (D) is attained whenever
`p_0 > 0` and `p_n > 0`, in particular at every interior point of `B`, ties
included; at other boundary points it can fail to be attained (for `sigma(s) = -sqrt(s)`
and `x = 0`, no finite concave `psi <= sigma` has `psi(0) = 0`). Moreover, for every concave `psi <= sigma` on `I`,
the function

```
g_psi(x) = sum_k p_k(x) psi(t_k(x))
```

is the staircase interpolation of the set function `S -> psi(a(S))` (its
Lovász extension up to the constant `psi(0)`; it is not positively
homogeneous when `psi(0) != 0`). It is convex on `B`, satisfies `g_psi <= f`
on `B`, and every one of its affine pieces
`h_{psi,pi}(x) = sum_k p_k^pi(x) psi(t_k^pi)` (with `p^pi(x)` the affine
barycentric coordinates of the simplex `Delta_pi`, extended affinely to `R^n`)
is a valid affine underestimator of `f` on all of `B`. Consequently

```
vex_B f = sup { g_psi : psi concave, psi <= sigma on I },
```

and a cut is obtained from any feasible `psi`, that is, any `psi` that is
concave on `I` and satisfies `psi <= sigma` there. Feasibility alone gives validity
on the whole box; with `pi` consistent with the order of `x`, optimality in
(D) gives the deepest cut at `x`. Concavity is essential: node values that
only satisfy the segment-chord constraints of the program below give an
affine function valid on `Delta_pi` but not necessarily on `B` (for
`sigma(s) = s`, `n = 2`, `a = (1,1)`, `y = (0, -10, 2)` gives `h(0,1) = 12 > f(0,1) = 1`).

The concave envelope follows by applying the theorem to `-sigma`: it is the
maximum of `E sigma(S)` over `S <=_cx T_x` (for upper semicontinuous `sigma`), and the infimum of
`sum_k p_k phi(t_k)` over convex majorants `phi >= sigma`.

### Proof

*Step 1 (envelope as an infimum over laws).* For a lower semicontinuous function on a
compact convex set, `vex_B f(x) = min { E f(X) : X random in B, E X = x }` over
finitely supported laws, where one may restrict to laws with at most `n+2` atoms
(Carathéodory applied to the convex hull of the graph). The same infimum over
all laws is not smaller: `E f(X) >= E vex_B f(X) >= vex_B f(E X)` by Jensen's
inequality for the convex, lower semicontinuous `vex_B f`. Lower semicontinuity
is needed: for `sigma(0) = 1` and `sigma = 0` on `(0,1]`, (P) = 1 but (D) = 0 at `x = 0`.

*Step 2 (the attainable laws of `a^T X`).* Let `M_x` be the set of laws of `a^T X`
over random vectors `X` in `B` with `E X = x`. We claim `M_x = {mu : mu <=_cx T_x}`.

(i) `M_x` is contained in the right side. Let `phi` be convex on `I`. The set
function `F(S) = phi(a(S))` is supermodular because `a >= 0` and `phi` is convex
(increasing differences of a convex function). Its Lovász extension `L_F` is
therefore concave on `B`, and `L_F(y) = E phi(T_y)` by the staircase formula.
On each staircase simplex `Delta_pi`, the function `phi(a^T y)` is convex and
`L_F` is affine and agrees with it at the vertices; hence
`phi(a^T y) <= L_F(y)` on `B`. For `X` in `B` with `E X = x`, Jensen's inequality
for the concave `L_F` gives

```
E phi(a^T X) <= E L_F(X) <= L_F(E X) = L_F(x) = E phi(T_x).
```

(ii) The right side is contained in `M_x`. Let `mu <=_cx T_x`. By Strassen's
theorem there is a pair `(S, T)` with `S ~ mu`, `T ~ T_x` and `E[T | S] = S`.
Because the `t_k` are distinct, `T = t_K` for a random index `K` with
`P(K = k) = p_k`. Put `X = E[v_K | S]`. Then `X` lies in `Delta_pi`, contained in `B`,
`a^T X = E[t_K | S] = S`, and `E X = sum_k p_k v_k = x`.

Steps 1 and 2 give `vex_B f(x) = inf { int sigma dmu : mu <=_cx T_x }`. The
set of such laws is weakly compact (they are supported in `I`, and the convex
order is closed under weak limits of laws on a compact interval), and
`mu -> int sigma dmu` is weakly lower semicontinuous (portmanteau theorem:
`sigma` is lower semicontinuous and bounded below on the compact `I`), so the
minimum in (P) is attained.
The proof of (ii) also shows that the envelope over `B` at `x` equals the
envelope over the simplex `Delta_pi`: all minimizing laws can be realized in
`Delta_pi`.

*Step 3 (duality).* Let `F(lambda) = sigma(sum_k lambda_k t_k)` on the standard
simplex `Lambda`. The map `lambda -> sum_k lambda_k v_k` is an affine bijection from
`Lambda` onto `Delta_pi`, so `vex_{Delta_pi} f(x) = vex_Lambda F(p)`. `F` is
lower semicontinuous and bounded below on the compact `Lambda`, so the convex
hull of its epigraph is closed (in a limit of Carathéodory combinations, atoms
whose weight tends to 0 contribute at least that weight times `min F`, which
tends to 0). Hence `vex_Lambda F` is a closed proper convex function and equals
the supremum of its affine minorants (Rockafellar, Theorem 12.1), which are
the affine minorants of `F`. An affine function on `Lambda` is
`lambda -> sum_k lambda_k y_k`, so

```
vex_Lambda F(p) = sup { sum_k p_k y_k : sum_k lambda_k y_k <= sigma(sum_k lambda_k t_k) for all lambda in Lambda }.
```

Given such a `y`, let `psi_y(s) = max { sum_k lambda_k y_k : lambda in Lambda,
sum_k lambda_k t_k = s }` for `s` in `I`. It is the upper concave hull of the
points `(t_k, y_k)`, it is concave, it satisfies `psi_y <= sigma` by the
constraint, and `psi_y(t_k) >= y_k`. Conversely, a concave `psi <= sigma` gives a
feasible `y_k = psi(t_k)`, because
`sum_k lambda_k psi(t_k) <= psi(sum_k lambda_k t_k) <= sigma(sum_k lambda_k t_k)`.
Hence the supremum equals the value of (D).

It is attained when `p_0 > 0` and `p_n > 0`. The feasible set of `y` is closed
(an intersection of closed half-spaces, one for each `lambda`), and the value is
finite (the constant `y_k = min_I sigma` is feasible, and `y_k <= sigma(t_k)`).
Replacing a feasible `y` by the node values `y'_k = psi_y(t_k) >= y_k` keeps it
feasible (`psi_y` is piecewise linear with breakpoints among the `t_k`, so
`psi_{y'} = psi_y <= sigma`) and does not decrease the objective, because
`p >= 0`. So take a maximizing sequence of such concave-hull node vectors, with
objective at least some `c`. Each coordinate satisfies `y_k <= sigma(t_k)`.
The endpoint values are bounded below:
`p_0 y_0 >= c - sum_{k != 0} p_k sigma(t_k)`, and likewise for `y_n`, since
`p_0, p_n > 0`. Concavity of `psi_y` then bounds every interior value below:
`y_k >= ((t_n - t_k) y_0 + (t_k - t_0) y_n)/(t_n - t_0)`. The sequence
therefore lies in a compact set, and a limit point is an optimal `y`; its
`psi_y` is an optimal `psi` in (D), because `psi_y(t_k) >= y_k` and `p >= 0`.
Combining with Step 2 proves (P) = (D).

*Step 4 (the functions `g_psi` and the cuts).* Let `psi` be concave with
`psi <= sigma` on `I`. The set function `G(S) = psi(a(S))` is submodular, so its
Lovász extension `g_psi` is convex, and by Edmonds' greedy theorem it is the
maximum over permutations of the linear functions
`h_{psi,pi}(y) = psi(0) + sum_j (psi(t_j^pi) - psi(t_{j-1}^pi)) y_pi(j)`, which
coincides with `sum_k p_k^pi(y) psi(t_k^pi)`. (For `G(emptyset) = psi(0) != 0`,
apply the greedy theorem to `G - psi(0)`.) Thus each `h_{psi,pi} <= g_psi` on
`B`. Finally `g_psi(y) = E psi(T_y) <= psi(E T_y) = psi(a^T y) <= sigma(a^T y)`
by Jensen's inequality. At the point `x`, `g_psi(x) = sum_k p_k psi(t_k)`, which
is the objective of (D), so an optimal `psi` gives `g_psi(x) = vex_B f(x)`. QED.

*Remark on ties.* If `x` has ties, several permutations are consistent with its
order; `T_x` and the value are the same, while the linear cuts `h_{psi,pi}`
differ. Each is valid.

## Computing (D)

The optimization in (D) depends on `x` only through the order `pi` (which
fixes the nodes `t_k`) and the weights `p_k`. Only the values `y_k = psi(t_k)`
matter, and a concave `psi <= sigma` with these node values exists if and only if
the piecewise-linear interpolant of `(t_k, y_k)` is concave and lies below
`sigma` on each segment `[t_k, t_{k+1}]`. Hence (D) is the convex program

```
maximize   sum_k p_k y_k
subject to (y_{k+1} - y_k)/(t_{k+1} - t_k) <= (y_k - y_{k-1})/(t_k - t_{k-1}),   k = 1..n-1,
           (1-theta) y_k + theta y_{k+1} <= sigma(t_k + theta (t_{k+1} - t_k)),   theta in [0,1], k = 0..n-1,
```

with `n+1` variables. Each segment constraint involves two variables and one
univariate function. Special cases:

- `sigma` convex on `I`: a supporting line at `a^T x` (when one exists; the
  slope can be infinite at an endpoint of `I`) is optimal and the envelope is `f` itself.
- `sigma` concave on `I`: `psi = sigma` is optimal and the envelope is the Lovász
  extension `sum_k p_k sigma(t_k)`. This is the staircase result for convex
  functions of a linear form (concave envelope side), known from the
  literature; see below.
- `sigma` with one inflection point (S-shaped, for example sigmoid and tanh):
  Carrasco and Muñoz give a recursive formula. We claim no closed form here.
- `sigma` with several inflection points (SiLU, GELU, `sin`, `cos`, cubic and
  higher polynomials, Hazen–Williams laws with sign changes): the program above
  still applies. No closed form is claimed.

For cut generation, validity requires a concave `psi <= sigma` exactly, not
just approximately. A robust repair of a numerical solution `y`: let `l_k` be
the line through `(t_k, y_k)` and `(t_{k+1}, y_{k+1})`, extended to all of `I`;
certify `l_k <= sigma` on `[t_k, t_{k+1}]` with univariate interval arithmetic
and shift `l_k` down by any certified violation; then `psi = min_k l_k` is
concave and below `sigma` on `I`, and the cut uses `psi(t_k) = min_j l_j(t_k)`.
The numerical solution of (D) affects only the strength of the cut.

## Extension to order polytopes and products of simplices

**Corollary 2 (order polytopes).** Let `Q` be a finite poset on `{1..n}` and
`O(Q) = {z in [0,1]^n : z_i >= z_j whenever i <=_Q j}` its order polytope. Let
`a > 0` and `f(z) = sigma(a^T z)`. Then `vex_{O(Q)} f = vex_{[0,1]^n} f` on `O(Q)`,
so Theorem 1 and its cuts apply verbatim on `O(Q)`.

*Proof.* For `z in O(Q)` choose `pi` sorting `z` in nonincreasing order and,
among ties, respecting `Q` (possible because `z` satisfies the order
constraints, so a linear extension of `Q` refined by the values of `z`
exists). Every vertex `v_k` of `Delta_pi` is the indicator of an initial
segment of a linear extension of `Q`, hence the indicator of a down-set (if `j` is in the set and
`i <=_Q j`, then `i` is in the set), so `v_k` lies in `O(Q)`
and `Delta_pi` is contained in `O(Q)`. Since `Delta_pi` is contained in `O(Q)`,
which is contained in the box, we have
`vex_box f(z) <= vex_{O(Q)} f(z) <= vex_{Delta_pi} f(z)`, and the
outer two terms are equal by the proof of Theorem 1 (Step 2 (ii)). QED.

Examples: the box (trivial poset); symmetry-breaking chains
`x_1 >= x_2 >= ... >= x_n` on a box; and products of simplices, below.
The same proof works for `a >= 0` (zero coefficients cannot simply be dropped,
because `O(Q)` is not a product; in Step 2 (ii) the atoms `t_k` may then
coincide, and one realizes `T_x` directly as `a^T v_K` with `K` distributed as `p`
instead of identifying atoms with indices). For `a <= 0`, apply the reflection
`z -> 1 - z` to all coordinates, which maps `O(Q)` to the order polytope of the
dual poset. Mixed signs fail: for the chain `z_1 >= z_2`, `a = (1,-1)`,
`sigma(s) = -s^2` and the point `(1/2,1/2)`, the envelope over `O(Q)` is 0 but
the envelope over the box is -1.

**Corollary 3 (products of simplices, one-hot blocks).** Let block `j` be a
simplex with vertex values `c_{j,1} < c_{j,2} < ... < c_{j,r_j}` (equal values
can be merged: the affine map that adds the coordinates of vertices with equal
values maps the product of simplices onto the smaller product, preserves `f`,
and a point `x` lifts representations of `A x` by the linear map that splits each
merged coordinate in the proportions of `x`, so envelopes correspond), `x_j` a point of the simplex, and
`f(x) = sigma(sum_j sum_i c_{j,i} x_{j,i})`. The tail sums
`z_{j,i} = x_{j,i+1} + ... + x_{j,r_j}`, for `i = 1..r_j - 1`, map the simplex affinely
and bijectively onto the chain `1 >= z_{j,1} >= ... >= z_{j,r_j - 1} >= 0`, and
`c_j^T x_j = c_{j,1} + sum_i (c_{j,i+1} - c_{j,i}) z_{j,i}` with positive increments.
The product of simplices is thus affinely equivalent to the order polytope of
a disjoint union of chains, and Corollary 2 applies. In the original variables,
`T_x` is the law of `sum_j Q_j(U)` for one uniform `U`, where `Q_j` is the
quantile function of the block law `sum_i x_{j,i} delta_{c_{j,i}}` (comonotone
sum of the block vertex laws).

The box is the case of two-vertex blocks. Mixed domains (some box
coordinates, some one-hot blocks, some chains) are covered in the same way,
with the sign condition of Corollary 2 on existing order constraints: box
coordinates (singleton chains) and one-hot blocks allow any coefficients, but
on each connected component of the order constraints among box variables the
coefficients must be all nonnegative or all nonpositive (reflect the
nonpositive components as after Corollary 2; mixed signs within a component
can fail, as shown there).

## Relation to known results

Details and page references are in [novelty.md](novelty.md).

- Step 2 (the attainable laws of `a^T X` are exactly the laws below `T_x` in
  convex order) is a special case of Mao and Wang, J. Multivariate Anal. 138
  (2015), Proposition 3.2, with the same Strassen and conditional-expectation
  proof. The inclusion (i) is Dhaene et al. (2002), Corollary 1, going back to
  Meilijson and Nádas (1979). The paper must cite these and not present Step 2 as new.
- Step 1 is classical (Rockafellar, Corollary 17.1.5; Kemperman's moment problem).
- Concave `sigma` (Lovász extension on staircase simplices): Tawarmalani,
  Richard and Xiong, Math. Program. 2013, Corollary 3.14; restated for convex
  activations by Tjandraatmadja et al. (NeurIPS 2020, Appendix A, Theorem 2).
  TRX Theorem 3.3 and Corollary 3.4 give the order-polytope geometry of
  Corollary 2 for supermodular functions; He and Tawarmalani (MOR 2022) and
  He, Liu and Tawarmalani (SIAM J. Optim. 2024) use the staircase on products
  of simplices, again under supermodularity.
- ReLU: Anderson, Huchette, Ma, Tjandraatmadja and Vielma, Math. Program. 2020.
- Convex, concave and S-shaped `sigma` over a box: Carrasco and Muñoz, Math.
  Program. 2026 (arXiv 2410.23362), Theorem 1, a recursive formula for
  functions with the "secant-then-function envelope" property. Their Table 1
  lists SiLU as S-shaped, but SiLU is concave, convex, then concave
  (`SiLU'' = 0` at `x = ±2.3994`), so their theorem covers SiLU only on
  intervals containing at most one of these points. GELU (inflection points
  `±sqrt 2`) is not treated.
- Not found in the accessible literature (bounded search): the
  characterization for arbitrary continuous `sigma`; form (D) as a supremum of
  Lovász extensions of concave minorants with cuts valid for any feasible `psi`;
  localization to the staircase simplex for arbitrary `sigma` and the
  resulting Corollaries 2 and 3. The law-level duality (P) = (D) is standard in
  kind and is not claimed as new.
