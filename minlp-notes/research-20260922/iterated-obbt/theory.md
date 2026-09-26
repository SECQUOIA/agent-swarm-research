# Contraction theory of iterated OBBT

Date: 2026-09-23. Status: author draft by the coordinator; an
[independent adversarial review](review-theory.md) found no false claim; its
fixes (rate claims as upper bounds except in the eigenvector case, Jacobi versus
sequential rounds, non-strict row condition, assumptions, stale text) are applied.
A [literature check](literature.md) found no published convergence rates for
iterated OBBT. Known: existence and characterization of limits in special
cases and order independence (Caprara and Locatelli, Math. Program. 2010,
Theorem 1, Corollary 1, Proposition 1), exact limits for a two-variable class
and examples with no reduction at all (Caprara, Locatelli and Monaci, COAP
2016, Theorem 1 and Section 3.1), and FBBT fixed points (Belotti et al.
2012). Proposition 2 below is a two-line consequence of the marginals-based
range-reduction bound `(U - L)/lambda` (Ryoo and Sahinidis 1995/1996) and is
not claimed as new. No counterpart was found for Theorems 4 and 6 or
Propositions 3, 7 and 8. A [second check](literature-cluster.md) read Wechsung's (2014) and Kannan's
(2018) theses, both Kannan–Barton papers, Du–Kearfott (1994),
Bompadre–Mitsos–Chachuat (2013) and Neumaier's and Schichl–Markót–Neumaier's
exclusion-region work: none defines a limit like `Q`, a map like `Phi` or a
constant like `r*`, and none analyzes bound-tightening rates; the scalar
threshold of Proposition 3 coincides with their cluster thresholds. Not
read: Bompadre–Mitsos (2012, closed access; used through restatements),
Locatelli–Schoen Section 5.5, the 2008 Caprara–Locatelli report.

## 1. Setting

Problem `P`: minimize `f(x)` over `x in X ∩ B_0`, where `B_0` is a box in `R^n`
and `X` is closed. Let `f*` be the optimal value and `x*` a global minimizer.

**Relaxation scheme.** For each box `B ⊆ B_0` let `phi_B : B -> R ∪ {+inf}` be
the relaxed objective in the original variables (for a lifted relaxation, the
minimum of the relaxed objective over lifted points above `x`, `+inf` if there
are none). We assume

- (R1) validity: `phi_B(x) <= f(x)` for `x in X ∩ B`;
- (R2) isotonicity: `B' ⊆ B` implies `phi_{B'}(x) >= phi_B(x)` for `x in B'`.

McCormick, alphaBB and the usual factorable relaxations satisfy (R1)–(R2),
with the qualification for composite McCormick relaxations below. For composite McCormick relaxations with natural interval extensions, (R2) is
Theorem 4 ("McCormick relaxations are partition monotonic") of Scott,
Stuber and Barton, "Generalized McCormick relaxations", J. Global Optim. 51
(2011) 569–606, checked in the open PDF. That theorem is proved for their
standard procedure (Definition 9), whose Step 6 clips each factor's convex and
concave relaxations to the factor's interval bounds; their Remark 2 warns that
omitting Step 6 can violate Theorem 4. Section 4b therefore uses the clipped
procedure; for the unclipped composition rule, (R2) is not established here.
The relaxations of Section 4 (exact convex squares and McCormick estimators of
products of two variables) satisfy (R2) directly, for all nested boxes of
`R^n`: the convex (concave) envelope of a function over a smaller box is at
least (at most) its envelope over a larger box. Where the tangent maps are computed by convex programs, we
also assume `phi_B` is convex and continuous on its domain.

**OBBT operator.** For a cutoff `U`, let

```
T_U(B) = box hull of { x in B : phi_B(x) <= U }
```

(the box hull is the smallest closed box containing the set, so every `T_U(B)`
is compact; `T_U(B)` is the empty set if there is no such `x`). One round of OBBT with exact LP/convex
solves computes `T_U(B)` when `phi_B` is the relaxation that the solver builds on `B`
and all `2n` bound problems are solved on that one relaxation ("Jacobi" rounds).
Solvers often tighten one variable at a time and rebuild the relaxation in between
("sequential" rounds). A sequential round ends in a box contained in `T_U(B)`
(every intermediate relaxation is built on a smaller box, so by (R2) every
intermediate set is smaller), so all upper bounds on widths and rates below apply
to it; the stall results (Theorem 6, Proposition 8) also apply, because a stall
witness keeps the first bound, hence the relaxation, unchanged. The lower bounds
on rates, and the exact rate of Proposition 7, are for Jacobi rounds only: for
`x^2 + y^2 + xy` a sequential round contracts by 0.7053 against 0.7247
(independent review, `review-theory.md`).
Iterated OBBT is `B_{k+1} = T_U(B_k)`. Write `epsilon = U - f* >= 0`.

**Lemma 1 (validity and monotonicity).** (a) Every `x in X ∩ B` with
`f(x) <= U` lies in `T_U(B)`, and `T_U(B) ⊆ B`. (b) `B' ⊆ B` implies
`T_U(B') ⊆ T_U(B)`. (c) The iterates decrease, all contain `x*`, and
converge to the box `B_inf = ∩_k B_k`.

*Proof.* (a) by (R1); (b) by (R2), since the set whose hull is taken shrinks;
(c) `x*` is feasible with `f(x*) = f* <= U`, so (a) keeps it in every iterate;
nested nonempty compact boxes converge to their intersection. QED.

Widths: `w(B) = max_i (u_i - l_i)`.

## 2. Two elementary contraction bounds

The next two statements are simple consequences of pointwise error bounds.
They are recorded because they fix the regimes. Proposition 2 is essentially
the marginals bound of Ryoo and Sahinidis; the radius `sqrt(2 epsilon/gamma)`
of the near-optimal set under quadratic growth is Kannan and Barton (2017,
Lemma 8).

**Proposition 2 (sharp minima: quadratic convergence).** Suppose there are
`kappa > 0` and `tau >= 0` such that for every box `B ⊆ B_0` containing `x*` and
every `x in B`,

```
phi_B(x) >= f* + kappa ||x - x*||_inf - tau w(B)^2.                (S)
```

Then `w(T_U(B)) <= 2 (epsilon + tau w(B)^2) / kappa`. Hence once
`w(B_k) <= kappa/(4 tau)`, the widths satisfy
`w_{k+1} <= (2 tau/kappa) w_k^2 + 2 epsilon/kappa`: quadratic convergence
down to width at most `4 epsilon / kappa` (for `epsilon` small enough that
`(2 tau/kappa)(4 epsilon/kappa)^2 <= 2 epsilon/kappa`).

*Proof.* A point `x` of the set whose hull is taken has
`kappa ||x - x*||_inf <= U - f* + tau w(B)^2`. QED.

(S) holds, for example, for a box-constrained problem whose minimizer is a
vertex of `B_0` with `f(x) - f* >= kappa ||x - x*||` on `B_0`, when the
relaxation has pointwise convergence order 2 with constant `tau`
(`phi_B >= f - tau w(B)^2` on `B`), as McCormick relaxations of factorable
functions do under standard conditions (Bompadre and Mitsos 2012).

**Proposition 3 (quadratic growth: a crude linear bound).** If instead
`phi_B(x) >= f* + mu ||x - x*||_inf^2 - tau w(B)^2` for all boxes `B ∋ x*` and
`x in B`, then `w(T_U(B)) <= 2 sqrt((epsilon + tau w(B)^2)/mu)`. If `tau < mu/4`
this is linear convergence with ratio at most `2 sqrt(tau/mu)` down to width
`2 sqrt(epsilon/(mu - 4 tau))`.

Proposition 3's threshold `tau < mu/4` is the domain-reduction analogue of the
published "no clustering" thresholds: with `mu = lambda_1/2` it is the
`K <= lambda_1/8` of Wechsung, Schaber and Barton (2014, Theorem 1(a)) and the
`tau* <= gamma/8` of Kannan and Barton (2017, Theorem 3); their prefactor bounds the
gap in minimum values, ours the pointwise gap over the box
([check](literature-cluster.md)). Proposition 3 is far from sharp: it bounds the relaxation error by its worst
case over the box and measures growth in the worst direction. For the model
problem of Section 4 it predicts no contraction at `a = 1`, while the true
ratio is 0.7247. Section 3 gives a sharper upper bound on the rate, which is
exact when the tangent map has a positive eigenvector (see the lower-bound
remark).

## 3. The tangent map and its cone spectral radius

Shapes: for `d = (d^-, d^+) in R^{2n}_{>=0}` let `D(d) = prod_i [-d_i^-, d_i^+]`.
Boxes near `x*` are written `x* + w D(d)` with `w > 0`.

**Assumption (T) (tangent relaxation).** There is a function `Q(d, xi)`,
defined for `xi in D(d)`, such that for every compact set `K` of shapes

```
sup_{d in K, xi in D(d)} | phi_{x* + w D(d)}(x* + w xi) - f* - w^2 Q(d, xi) | = o(w^2)   as w -> 0.
```

Consequences: `Q(lambda d, lambda xi) = lambda^2 Q(d, xi)` for `lambda > 0`;
`Q(d, 0) <= 0` (by (R1) at `x*`); and `d <= d'` componentwise implies
`Q(d, xi) >= Q(d', xi)` on `D(d)` (by (R2)). For a quadratic objective with a
box-interior minimizer and McCormick relaxations of its bilinear terms, (T)
holds with zero remainder (Section 4). For a smooth problem it expresses that
the scaled relaxations converge (compare Neumaier's remark, in his 2004 survey,
that an `o(eps^2)` error is sufficient to avoid clustering); Theorem 12 below
proves it for composite McCormick relaxations of factorable functions.

**Tangent maps.** For `c` real, let `Phi_c(d)` be the shape of the box hull of
`{xi in D(d) : Q(d, xi) <= c}`, that is `Phi_c(d)_i^+ = max xi_i` and
`Phi_c(d)_i^- = -min xi_i` over that set (for `c >= 0` the set contains 0, so
`Phi_c(d) >= 0`). The map `Phi = Phi_0` is monotone
(`d <= d'` implies `Phi(d) <= Phi(d')`), positively homogeneous of degree 1,
and satisfies `Phi(d) <= d`. More generally
`Phi_c(t d) = t Phi_{c/t^2}(d)` for `t > 0`.

Define the contraction constant

```
r*(Phi) = inf { lambda : there are u >> 0 and delta > 0 with Phi_delta(u) <= lambda u }.
```

It is a Collatz–Wielandt-type upper cone spectral radius of `Phi`. Since
`Phi(d) <= d`, one always has `r*(Phi) <= 1`. The constant `r*` is an upper bound
on the local linear rate (Theorem 4). It equals the rate when `Phi` has an
eigenvector `u >> 0` and the remainder in (T) vanishes (lower-bound remark below);
equality in general would need a nonlinear Perron–Frobenius theorem for `Phi`
and continuity of `Phi`, which are not established here.

**Theorem 4 (local linear convergence, and its rate).** Assume (T). Let
`u >> 0`, `delta > 0` and `lambda in (0,1)` satisfy `Phi_delta(u) <= lambda u`.
Then there is `wbar > 0` such that, whenever the iteration starts from a box
`B ⊆ x* + w_0 D(u)` with `w_0 <= wbar` (and `x* + wbar D(u)` lies in the domain
`B_0` on which the relaxations are defined, so `x*` is interior in the directions
where `u > 0`):

(a) while `w_k^2 >= 2 epsilon / delta`, the iterates satisfy
`B_{k+1} ⊆ x* + lambda w_k D(u)`, where `B_k ⊆ x* + w_k D(u)` and
`w_{k+1} = lambda w_k`;

(b) the limit box satisfies `B_inf ⊆ x* + sqrt(2 epsilon/delta) D(u)`; for
`epsilon = 0`, `B_inf = {x*}` and the convergence is linear with ratio `lambda`
in the gauge of `D(u)`.

*Proof.* Choose `wbar` so that the remainder in (T) on `K = {u}` is at most
`delta w^2 / 2` for `w <= wbar`. Let `B = x* + w D(u)` with `w <= wbar` and
`epsilon <= delta w^2/2`. A point `x = x* + w xi` with `phi_B(x) <= f* + epsilon`
satisfies `w^2 Q(u, xi) <= epsilon + delta w^2/2 <= delta w^2`, so `xi` lies
in `{Q(u, .) <= delta}` and `T_U(B) ⊆ x* + w Phi_delta(u)-box ⊆ x* + lambda w D(u)`.
For a general iterate `B_k ⊆ x* + w_k D(u)`, Lemma 1(b) gives
`B_{k+1} = T_U(B_k) ⊆ T_U(x* + w_k D(u))`. This proves (a). For (b): the
contraction applies while `w_k >= sqrt(2 epsilon/delta)`; once `w_k` falls
below this value the iterates stay inside `x* + w_k D(u)` by Lemma 1(a). QED.

**Corollary 5.** If `r*(Phi) < 1`, iterated OBBT started in a small enough box
around `x*` converges linearly, with any ratio above `r*(Phi)` (in a suitable
box gauge), to a box of width `O(sqrt(epsilon))`.

**Theorem 6 (stalling).** Assume (T). Suppose there are a shape `v >= 0`,
`v != 0`, and `delta > 0` such that for every `i` with `v_i^+ > 0` some
`xi in D(v)` has `xi_i = v_i^+` and `Q(v, xi) <= -delta`, and likewise for every
`v_i^- > 0` with `xi_i = -v_i^-`. Then there is `wbar > 0` such that for all
`w <= wbar` and every cutoff `U >= f*`, `T_U(x* + w D(v)) = x* + w D(v)`. Consequently
every OBBT iterate from any `B_0 ⊇ x* + w D(v)` contains `x* + w D(v)`: iterated
OBBT stalls at a box of width at least `w max(v)`, however small `epsilon` is.

*Proof.* (Coordinates with zero extent in `v` need no witness: the box is already
degenerate there.) For the witness points, `phi_B(x* + w xi) <= f* - delta w^2 + o(w^2) < f* <= U`
for small `w`, so they lie in the set whose hull is taken; they attain every
extreme coordinate of `D(v)`. Monotonicity (Lemma 1(b)) gives the rest. QED.

For pure quadratic objectives with zero remainder, Theorems 4 and 6 hold for
every `w`, not just small `w`.

**Lower bound on the rate.** If `Phi(u) = rho u` for some `u >> 0` and the
remainder in (T) is zero with `epsilon = 0`, then `T^k(x* + w D(u)) = x* + rho^k w D(u)`,
and by monotonicity the iterates from any `B_0` containing `x* + w D(u)` contain
`x* + rho^k w D(u)`. So the linear rate cannot be better than `rho`.

## 4. Quadratic objectives with McCormick relaxations

Let `f(x) = f* + (x - x*)^T H (x - x*)/2` with `x*` interior to `B_0`, and let
the relaxation keep the diagonal terms `H_ii (x_i - x_i*)^2/2`, assuming `H_ii >= 0`
(so that they are convex) and replace each off-diagonal product by its McCormick
underestimator (if `H_ij > 0`) or overestimator (if `H_ij < 0`) over the current
box. Translating `x*` to the origin, (T) holds with zero remainder and

```
Q(d, xi) = sum_i H_ii xi_i^2 / 2 + sum_{i<j} H_ij m_ij^{d}(xi),
```

with `m_ij^d` the appropriate McCormick estimator of `xi_i xi_j` on `D(d)`.
Each `Phi_c(d)` is computed by `2n` convex programs.

(The relaxation of `(x_i - x_i*)(x_j - x_j*)` coincides with the relaxation of `x_i x_j`
plus linear terms, because McCormick estimators commute with translation of
the box, so this is the relaxation a factorable solver builds.)

**Proposition 7 (two variables).** For `f = x^2 + y^2 + a x y` with `0 < a < 2`
(strictly convex, minimizer 0), McCormick on `x y`, and any box containing 0 in
its interior, iterated OBBT (Jacobi rounds) with `epsilon = 0` converges to `{0}` with
linear rate exactly

```
rho(a) = (sqrt(2 a^2 + 4 a) - a) / 2,
```

which increases from 0 to 1 as `a` goes from 0 to 2 (rho = 0.5406, 0.7247,
0.8702, 0.9748 at a = 0.5, 1, 1.5, 1.9). The same holds for `-2 < a < 0` with
`rho(|a|)`.

*Proof.* On `D = [-1,1]^2` the McCormick underestimator is
`m(xi) = max(-xi_1 - xi_2 - 1, xi_1 + xi_2 - 1) = |xi_1 + xi_2| - 1`, so
`Q(1, xi) = xi_1^2 + xi_2^2 + a(|xi_1 + xi_2| - 1)`. Maximize `xi_1 = t` subject to
`Q <= 0`. With `xi_2 = s - t`:
`Q = t^2 + (s - t)^2 + a|s| - a`. For `t > a/2`, the minimizing `s` is
`t - a/2`, and `Q_min(t) = t^2 + a^2/4 + a(t - a/2) - a = t^2 + a t - a^2/4 - a`.
Setting this to 0: `t = (-a + sqrt(a^2 + a^2 + 4a))/2 = (sqrt(2a^2 + 4a) - a)/2 = rho(a)`.
One checks `rho(a) > a/2` for `0 < a < 2` (equivalent to `2a^2 + 4a > 4a^2`, i.e.
`a < 2`), so this case applies, and `xi_2 = -a/2` lies in `[-1, 1]`. By the
symmetries `(xi_1, xi_2) -> (xi_2, xi_1)` and `xi -> -xi` of `Q(1, .)`, all four
extents equal `rho(a)`: `Phi(1) = rho(a) 1`. For the upper bound, let the
initial box `B` lie in a cube `C = [-w, w]^2`. `C` need not lie in the original
`B_0`, but the relaxation (exact squares plus McCormick of `xy`) is defined on
every box of `R^2` and satisfies (R2) for all nested boxes (Section 1), so
Lemma 1(b) with `R^2` in place of `B_0` gives `T_U^k(B) ⊆ T_U^k(C)`. Theorem 4
applied on `C` (with `u = 1`, zero remainder, hence every `w` allowed, and
`Phi_delta(1) -> Phi(1)` as `delta -> 0`) gives the upper bound on the
rate, and the lower-bound remark gives the matching lower bound for every
initial box containing a neighborhood of 0. QED.

Numerical check (`code/tangent_map.py`, power iteration of `Phi` with convex
programs in cvxpy/Clarabel from the asymmetric shape `[-1,1.3] x [-1.2,1]`):
ratios 0.540569, 0.724745, 0.870137, 0.973634 against the formula 0.540569,
0.724745, 0.870185, 0.974838 (the last two not yet converged after 40
iterations, as expected near 1). For the many-term example below: `n = 3`,
`a = 0.5` contracts with ratio 0.8229; `n = 5, a = 0.3`, `n = 10, a = 0.1`
and `n = 20, a = 0.1` give ratio 1 (stall), as the row condition predicts
(`a(n-1)(n-2)/2` = 0.5, 1.8, 3.6, 17.1).

Also, the scout's probe with exact OBBT on
`[-1, 1.3] x [-1.2, 1]` observed ratios 0.54, 0.725, 0.87, 0.974 for
`a = 0.5, 1, 1.5, 1.9`.

**Proposition 8 (row condition for a complete stall).** In the setting of this
section, suppose that for every `k`

```
H_kk / 2 + sum_{j != k} |H_kj|  <=  sum_{i<j} |H_ij|.
```

Then `T_U(B) = B` for every cube `B` centered at `x*` and every `U >= f*`. For a
box centered at `x*` with half-widths `h_1..h_n`, the same holds when the
condition is satisfied by `H' = S H S`, `S = diag(h)`.

*Proof.* On `[-1,1]^2` the McCormick underestimator of `xi_i xi_j` is
`|xi_i + xi_j| - 1` and the overestimator is `1 - |xi_i - xi_j|`, so with
`s_ij = sign(H_ij)`,
`Q(1, xi) = sum_i H_ii xi_i^2/2 + sum_{i<j} |H_ij| (|xi_i + s_ij xi_j| - 1)`.
At `xi = ± e_k` each pair containing `k` contributes `|H_kj|(|±1| - 1) = 0`,
and every other pair contributes `-|H_ij|`, so
`Q(1, ± e_k) = H_kk/2 - sum_{i<j, k not in {i,j}} |H_ij| = H_kk/2 + sum_{j != k}|H_kj| - sum_{i<j}|H_ij| <= 0`.
Since the remainder is zero, `phi_B(x* ± e_k) = f* + Q(1, ± e_k) <= f* <= U`, so these points
are kept and attain every face of the cube (this uses the zero remainder directly,
so the non-strict inequality suffices).
Theorem 6 with zero remainder and `v = 1` gives the claim for cubes. For half-widths
`h`, substitute `xi_i = h_i eta_i`: McCormick estimators commute with this scaling
(the estimator of `xi_i xi_j` on the box is `h_i h_j` times the estimator of
`eta_i eta_j` on `[-1,1]^2`), so `Q` becomes the same expression in `eta` with `H'`. QED.

**Example (strongly convex objective).** Let
`f = sum_i x_i^2 + a sum_{i<j} x_i x_j` with `a > 0` (so `H_kk = 2`,
`H_kj = a`), relaxed termwise with McCormick, and `B_0 = [-1, 1]^n`. The row
condition reads `1 + a(n-1) <= a n(n-1)/2`, that is `a (n-1)(n-2)/2 >= 1`. Then
`T_U(B_0) = B_0` for every `U >= 0 = f*`: OBBT does not tighten any bound, in
any round, although `f` is strongly convex whenever `a < 2`.

For example, `a = 0.1` and `n >= 6` (the independent review confirmed the stall at
`n = 6` numerically). The row condition is sufficient, not necessary: in the
review's test, 5 of 12 random `H` violating it also stalled. The failure is caused by the accumulated
relaxation gap at `x*` (here `a n(n-1)/2` times `w^2/4` on a box of width `w`)
exceeding the curvature along the coordinate directions. A solver that
recognizes convexity avoids this case, but the mechanism applies to nonconvex
objectives with many bilinear terms.

## 4b. Assumption (T) for factorable McCormick relaxations

**Setting.** A factorable function is a sequence of factors `v_1, ..., v_m`
with `v_i = x_i` for `i <= n` and, for `k > n`, one of `v_k = v_a + v_b`,
`v_k = c v_a`, `v_k = v_a v_b` or `v_k = h_k(v_a)` with `a, b < k`, where each
univariate `h_k` is `C^2` on an open interval around its argument's value at `x*`; `f = v_m`.
On a box `B` the (composite) McCormick relaxation computes, for every factor, an
interval `[v_k^L, v_k^U]` by natural interval arithmetic and convex and concave
relaxations `cv_k <= v_k <= cc_k` on `B`, using: sums and scalings exactly;
for products, the McCormick composition rule of McCormick (1976) / Mitsos,
Chachuat and Barton (2009); for univariate factors,
`cv_k = h^cv(mid(cv_a, cc_a, argmin))`, `cc_k = h^cc(mid(cv_a, cc_a, argmax))`,
with `h^cv, h^cc` the convex and concave envelopes of `h_k` on `[v_a^L, v_a^U]`.
As in Step 6 of Definition 9 of Scott, Stuber and Barton (2011), each factor's
relaxations are then clipped to its interval, `cv_k := max(cv_k, v_k^L)` and
`cc_k := min(cc_k, v_k^U)`, before they are used by later factors.
The relaxed objective is `phi_B = cv_m`.

With this clipping, (R2) holds for all boxes `B ⊆ B_0` by their Theorem 4,
provided the relaxations are defined on `B_0` (their Assumption 1: the natural
interval of each univariate argument over `B_0` lies in the domain of `h_k`) and
each `h_k` is Lipschitz on that interval (so that exact ranges satisfy their
Assumption 4; envelopes satisfy their Assumption 5). Clipping changes the
values near `x*` only by `o(w^2)` ([proofs-12-11.md](proofs-12-11.md), property
(P_k) and Remark 2 of A.4), so Theorem 12 below holds for the clipped and the
unclipped rule alike. This expansion is local and asymptotic; it gives no
finite-box monotonicity. The finite-box uses of Lemma 1(b) for composite
McCormick relaxations, in Theorems 4 and 6, Corollary 9 and Proposition 11, are
therefore justified for the clipped rule; for the unclipped rule they need
(R2) as an additional assumption.

**Theorem 12 (second-order tangent expansion).** Full proof:
[proofs-12-11.md](proofs-12-11.md) (C^2 univariate factors suffice, with `o(w^2)`
remainders; `C^3`, or locally Lipschitz `h_k''`, gives `O(w^3)`). Let `x*` be any point
of `B_0` (interior or on the boundary; only smoothness of the factors near `x*`
is used), and `g = grad f(x*)`.
For every factor `k` there are functions `ell_k^L(d), ell_k^U(d)` (positively
homogeneous of degree 1 in `d`) and `E_k^cv(d, xi), E_k^cc(d, xi) >= 0` (positively
homogeneous of degree 2 in `(d, xi)`, continuous) such that, uniformly for `d` in
compact sets and `xi in D(d)`, with `B = x* + w D(d)` and `x = x* + w xi`,

```
v_k^{L,U}  = v_k(x*) + w ell_k^{L,U}(d) + O(w^2),
cv_k(x)    = v_k(x) - w^2 E_k^cv(d, xi) + o(w^2),
cc_k(x)    = v_k(x) + w^2 E_k^cc(d, xi) + o(w^2).
```

The first-order bounds `ell_k` are the natural interval extension of the
linearized factor sequence over `D(d)`, and the `E_k` are defined recursively from
the factor values `v_k(x*)` (through sign selections), the gradients, the `ell`'s,
and `h_k'(a*)`, `h_k''(a*)`. With `p_a = grad v_a(x*)^T xi`, `t^+ = max(t,0)`, `t^- = max(-t,0)`:

```
product:    E^cv_ab = b*^+ E_a^cv + b*^- E_a^cc + a*^+ E_b^cv + a*^- E_b^cc
                      + min{ (p_a - ell_a^L)(p_b - ell_b^L), (ell_a^U - p_a)(ell_b^U - p_b) },
univariate: E^cv_h  = (h''(a*)^- / 2)(p_a - ell_a^L)(ell_a^U - p_a) + h'(a*)^+ E_a^cv + h'(a*)^- E_a^cc,
```

and symmetrically for the concave side. The complete proof closes a gap in the
sketch below: when `h'(a*) != 0`, the `mid` rule's clipping at interval endpoints
is inactive at second order, because (up to `o(w^2)`) the relaxation is never weaker
than the interval bounds. Numerical checks (9 hand-picked and 25 random factorable
expressions, including inflections, critical points, zero-width intervals and zero
factor values) show the error `|(cv - v)/w^2 + E|` falling tenfold per decade of `w`
(`code/proofs_checks/`).
Consequently the relaxations satisfy

```
phi_{x* + w D(d)}(x* + w xi) = f(x*) + w g^T xi + w^2 Q(d, xi) + o(w^2),
Q(d, xi) = xi^T grad^2 f(x*) xi / 2 - E_m^cv(d, xi),
```

which is Assumption (T) when `g = 0` (an interior unconstrained minimizer), and the
expansion used in Proposition 11 on the boundary of `B_0`.

*Proof sketch (see the full proof).* Induction over the factors. Write `a = v_a(x)`, `a* = v_a(x*)`, and
`p_a = grad v_a(x*)^T xi`.

- Sums and scalings: the expansions add; `E` adds (with signs exchanged for negative
  scalars, which swap `cv` and `cc`).
- Intervals: natural interval arithmetic on `[a* + w ell_a^L + O(w^2), a* + w ell_a^U + O(w^2)]`
  gives first-order bounds equal to interval arithmetic on the linear parts; for `h`,
  the mean value theorem gives `h(a*) + w h'(a*) [ell_a^L, ell_a^U] + O(w^2)`.
- Products `v_a v_b`: every McCormick estimator has the form
  `ab - (a - a^1)(b - b^1)` or `ab + (a - a^1)(b^2 - b)` with `a^1, b^1, b^2` interval
  endpoints, evaluated at `cv`/`cc` values of the factors through `min`/`max`
  selections. Substituting the expansions, `(a - a^L)(b - b^L) = w^2 (p_a - ell_a^L)(p_b - ell_b^L) + O(w^3)`,
  and replacing `a` by `cv_a` or `cc_a` changes the value by `w^2 b* E_a + o(w^2)` (the
  interval endpoints of `b` equal `b* + O(w)`). The `min`/`max` of finitely many
  expansions with the same zeroth- and first-order terms is an expansion whose
  second-order term is the `min`/`max` of the second-order terms. So `E_k` exists and
  is continuous and 2-homogeneous.
- Univariate `h(v_a)`: on the interval `I_w = [a^L, a^U]` of width `O(w)`, if
  `h''(a*) > 0` then `h` is convex on `I_w` for small `w` and `h^cv = h`; if
  `h''(a*) < 0`, `h^cv` is the secant, and
  `h^cv(a* + w t) - h(a* + w t) = w^2 (h''(a*)/2)(t - ell^L)(ell^U - t) + O(w^3)` (nonpositive, since `h''(a*) < 0`)
  with `ell^{L,U} = ell_a^{L,U}`; if `h''(a*) = 0`, `|h^cv - h| = O(w^3)` on `I_w`
  (the envelope of a function whose second derivative is `O(w)` on `I_w`). The
  composition with `mid(cv_a, cc_a, .)` perturbs the argument by `O(w^2)` with a
  limit, and `h^cv` has derivative `h'(a*) + O(w)` there, so
  `E_k^cv = (second-order envelope gap) + h'(a*) * (limit of the argument shift)`,
  with the sign convention of the `mid` rule. The concave side is symmetric.

The remainders are uniform on compact shape sets because every step is uniform
in `(d, xi)` on `D(d)` and `D(d)` is compact. The `argmin`/`argmax` points of the
`mid` rule and sign changes of `h''` inside `I_w` are treated in the full proof. (In
the case `h''(a*) = 0`, the bound `|h^cv - h| = O(w^3)` above needs `C^3`; under `C^2`
it is `o(w^2)`, which suffices.) QED (sketch).

**Remark (auxiliary-variable relaxations).** Solvers relax lifted
(auxiliary-variable) reformulations rather than McCormick compositions. For
QCQPs whose auxiliary variables appear only in the objective, `phi_B` is the
termwise sum used in Section 4, so Section 4 is exact for them. For general
lifted relaxations, the analogous statement (the scaled lifted relaxations
converge to a tangent lifted relaxation) is expected but not proved here.

## 5. Consequences

**Corollary 9 (root gap after iterated OBBT is O(epsilon)).** Under the
hypotheses of Theorem 4, let `G = -min { Q(u, xi) : xi in D(u) } >= 0` and
`L(B) = inf_{x in B} phi_B(x)` (the relaxation bound on `B`). If `epsilon` is small
enough that `sqrt(2 epsilon/delta) <= wbar`, then

```
L(B_inf) >= f* - (2 G / delta) epsilon - epsilon.
```

In the sharp case of Proposition 2, if some iterate satisfies Proposition 2's
entry condition `w(B_k) <= kappa/(4 tau)`, then
`L(B_inf) >= f* - tau (4 epsilon/kappa)^2 = f* - O(epsilon^2)`.

*Proof.* By Theorem 4(b), `B_inf ⊆ B' := x* + w D(u)` with `w = sqrt(2 epsilon/delta)`.
By (R2), `phi_{B_inf} >= phi_{B'}` on `B_inf`, so
`L(B_inf) >= inf_{xi in D(u)} phi_{B'}(x* + w xi) >= f* - G w^2 - delta w^2/2`, using the
remainder bound `delta w^2/2` from the proof of Theorem 4, and `delta w^2/2 = epsilon`. For the
sharp case, (S) gives `phi_B(x) >= f* - tau w(B)^2` for all `x in B ∋ x*`. From the
entry iterate on, the widths decrease and Proposition 2 gives
`w_{j+1} <= (2 tau/kappa) w_j^2 + 2 epsilon/kappa <= w_j/2 + 2 epsilon/kappa`, so
`w(B_inf) <= 4 epsilon/kappa` (this limit bound needs no further condition on
`epsilon`). QED.

So, in the contracting regime, the gap left at the root is proportional to
the incumbent's suboptimality `epsilon`, and an exactly optimal incumbent
closes it in the limit. This is consistent with Castro (2023, reported in
`literature.md`; his instances are not shown to satisfy the hypotheses above): with the optimal cutoff the gap fell from 3.5% to 0.0003%,
with a cutoff 20% worse it stayed at 3.5%. It also shows why OBBT should be
repeated after incumbent improvements.

**Lemma 10 (the near-optimal set limits OBBT).** For every cutoff `U`, every
iterate contains the box hull of `{x in X ∩ B_0 : f(x) <= U}`. In particular, if
`P` has two global minimizers `x* != x**` (for example, related by a symmetry of
the model), then `B_inf` contains the box hull of `{x*, x**}` for every
`epsilon >= 0`, and the root gap after iterated OBBT is at least the relaxation
gap on that box.

*Proof.* Lemma 1(a) and induction. QED.

Iterated OBBT at the root is therefore effective only when the `epsilon`-optimal
set is concentrated. Symmetric models (permutations of identical units, pools,
points) defeat it unless symmetry is broken first; branching separates the
near-optimal points, and OBBT at the nodes then enters the local regime of
Theorem 4.

**Proposition 11 (minimizers on the boundary of the box).** Full proof in
[proofs-12-11.md](proofs-12-11.md), where the needed uniformity is the expansion below
on compact sets of admissible shapes (`d_A^- = 0`) including shapes with small or zero
active extents, with `Q` continuous there (Theorem 12 supplies it); after one
preliminary step the free widths contract by a factor at most `lambda` per round in the `u_F`
gauge (`lambda` is the chosen admissible bound, not a proved exact asymptotic rate). As in Theorem 4, the local boxes (of admissible shape) must lie in `B_0`.
Suppose `x*`
lies on the boundary of `B_0`: `x*_i = l_i` for `i` in an index set `A`, with
`partial_i f(x*) = g_i > 0` for `i in A` (strict complementarity), and `x*` is
interior in the other coordinates `F`. Suppose the scaled relaxations satisfy

```
phi_{x* + w D(d)}(x* + w xi) = f* + w g^T xi + w^2 Q(d, xi) + o(w^2)
```

uniformly for shapes in compact sets with `d_i^- = 0` for `i in A`, where
`g_i = 0` for `i in F` and `Q` is continuous. Let `Phi^F` be the tangent map in the free
coordinates obtained from `Q` with zero extents in `A`. If `Phi^F_delta(u_F) <= lambda u_F`
for some `u_F >> 0`, `delta > 0`, `lambda < 1`, then locally the free widths contract
linearly with ratio at most `lambda` (after one preliminary step, in the `u_F` gauge) down to `O(sqrt(epsilon))`, and the active widths
satisfy `width_i(B_{k+1}) <= (epsilon + O(w_k^2)) / g_i`, that is, they shrink
quadratically relative to the free widths, down to `O(epsilon)`.

*Sketch.* A point `x* + w xi` kept by OBBT satisfies `w g^T xi <= epsilon + w^2 G' + o(w^2)`
with `G'` a bound on `-Q`, and `xi_A >= 0`, so `xi_i <= (epsilon/w + w G' + o(w))/g_i` for
`i in A`. In scaled units the active extents are `O(w + epsilon/w)`; once they are
small, continuity of `Q` lets the free extents follow `Phi^F` up to an error that
vanishes with them, and the argument of Theorem 4 applies. This needs a
uniformity statement for `Q` near shapes with vanishing active extents; the complete proof in
[proofs-12-11.md](proofs-12-11.md) states it as Assumption (T_∂), which Theorem 12 supplies,
and proves the precise bounds (B.3). Numerical check (`code/proofs_checks/prop11_obbt.py`):
for `x1 + x2^2 + x3^2 + x2 x3 + 0.5 x1 x2` with `x1` at its lower bound, the free-width
ratio is 0.724745 (= rho(1)); for `epsilon` from 1e-3 to 1e-7 the final free width is
`2.3094 sqrt(epsilon)` and the active width `2.333 epsilon`, as predicted.

## 6. Practical rule and open questions

- The asymptotic ratio of successive widths is a power-iteration estimate of
  `r*(Phi)`. This justifies a stopping rule: continue iterating while the
  observed ratio is below a threshold `theta` (the probe used 0.5); stop when
  the ratio approaches 1, which signals `r* = 1` (Theorem 6) or the
  `sqrt(epsilon)` floor.
- The floor scales with `sqrt(epsilon)` and the remaining root gap with
  `epsilon` (Corollary 9), so OBBT should be re-run after incumbent improvements.
- Iterating at the root cannot help when the near-optimal set is spread out,
  for instance by symmetry (Lemma 10).
- Branch and bound: if `r*(Phi) < 1` or (S) holds, running iterated OBBT at nodes
  near `x*` gives width-tight domain reduction; relate to the repository's
  cluster-free theorem (`results/cluster-free-branch-and-bound-constrained-minima.md`).
- Open: the constrained case (general constraints beyond bounds) (active constraints give sharp directions); conditions
  on `H` and the sign pattern for `r* < 1`; the relation to the classical
  convergence-order prefactor condition for the cluster problem
  (Wechsung, Schaber and Barton 2014).
