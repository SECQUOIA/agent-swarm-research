# Cluster-free spatial branch-and-bound at nondegenerate constrained minima

Date: 2026-09-22. Status: proof written by the root agent; numerical
illustration in `code/cluster_problem/` (see Section 5); literature check done
(Section 6); an initial independent review was followed by an adversarial audit that
corrected the nearby-point counterexample, domain-reduction claims, and
counting qualifications (see the [review record](../notes/review-cluster-free-branch-and-bound.md)). Novelty: addresses the clustering motivation behind
the question left open in the conclusion of Kannan and Barton,
"Convergence-order analysis of branch-and-bound algorithms for constrained
problems", J. Global Optim. 71 (2018) 753–813 ("whether full-space lower
bounding schemes can achieve second-order convergence on a neighborhood of
constrained minima that are KKT points"). An unsuccessful literature search does
not establish novelty.

**Attribution correction (2026-09-22 continuation).** The central
off-feasible growth inequality follows directly from classical quadratic
growth of exact penalties: Anitescu (2005), Section 1.3, equations
(1.18)–(1.19), citing Bonnans–Shapiro (2000), Theorem 3.113. Substituting the
relaxation's second-order constraint residuals gives the mixed bound below.
The result is therefore an application to spatial search, not a new
optimality or error-bound principle. A
[shorter projection proof](../notes/research-20260922-error-bound-transfer.md)
also removes LICQ and strict complementarity when feasible quadratic growth
and a linear constraint error bound hold. The
[independent review](../notes/review-20260922-error-bound-transfer.md)
confirmed this comparison. The box-counting application, corrected
neighborhood counterexample, and conditional reduced-space result are retained.

## Summary

Spatial branch-and-bound suffers from the *cluster problem* when many boxes
near a global minimizer cannot be fathomed. Under quadratic growth, classical
worst-case covering bounds scale as `eps^{-n/2}` for first-order relaxations
at width `delta ~ eps`, and remain bounded for second-order relaxations at
width `delta ~ sqrt(eps)` (Du–Kearfott
1994; Wechsung, Schaber, Barton 2014). For constrained problems, Kannan and
Barton (2017) showed that second-order convergence of the lower bounding scheme
*on a neighborhood* of the minimizer suffices at KKT points where the critical
cone is nontrivial (and wrote in 2018 that it "may be required"), and in 2018 they proved second-order convergence
of standard convex-relaxation schemes at an interior KKT point itself (their
Theorem 5 and Corollary 4, via the Lagrangian with the KKT multipliers), but
left open whether it holds on a neighborhood.

This note shows that the neighborhood question can be bypassed: the same fixed
multipliers give, for every box `Z` near a nondegenerate minimizer `z*`, the
bound

```
L(Z) >= f* + c_1 dist(Z, z*)^2 - c_2 w(Z)^2,                                   (*)
```

valid whether or not `Z` contains `z*`, with constants depending only on the
problem data at `z*` and the relaxation constant. The bound has the two
ingredients the cluster analysis needs: quadratic growth in the distance to the
minimizer and quadratic decay in the box width. It follows (Theorem 2) that the
number of disjoint boxes at each fixed scale, with uniformly comparable side
lengths, that cannot be fathomed inside a fixed neighborhood of `z*` is bounded
by a constant independent of the tolerance and of that scale. This is a local
count, not a bound on the entire search tree or solver runtime. There is no
clustering in this sense at KKT points satisfying LICQ, strict
complementarity and the standard second-order sufficient condition, provided
the relaxations of the objective and of all constraints are second-order
pointwise convergent (as McCormick relaxations with envelopes and αBB
relaxations of twice continuously differentiable factorable functions are).

The proof needs only three elementary facts: on the relaxed feasible set of a
box, constraint violations are `O(w(Z)^2)`; LICQ turns constraint values into a
bound on the normal component of `z - z*`; and the Lagrangian with fixed
multipliers grows quadratically along the critical cone and, through the
active-constraint slacks weighted by the positive multipliers, at least
linearly in the inward normal directions. The linear growth is what makes the
argument work when the Hessian of the Lagrangian is not positive definite on
the whole space, which is the typical situation with active inequality
constraints.

## 1. Setting

```
(P)   minimize f(z)   subject to   g_j(z) <= 0 (j = 1..m),   h_k(z) = 0 (k = 1..r),   z in X,
```

`X subset R^n` a box, `f, g_j, h_k` twice continuously differentiable on an
open set containing `X`. Let `z*` be a global minimizer with `f* = f(z*)`, and
assume:

- **(KKT)** `z*` is a KKT point with multipliers `mu* in R^m_+`, `lambda* in R^r`:
  `grad f(z*) + sum_j mu*_j grad g_j(z*) + sum_k lambda*_k grad h_k(z*) = 0`,
  `mu*_j g_j(z*) = 0`. Bound constraints of `X` that are active at `z*` are
  included among the `g_j` (they are affine and have exact relaxations).
- **(LICQ)** the gradients `{grad g_j(z*) : j in A} cup {grad h_k(z*) : k}` are
  linearly independent, where `A = {j : g_j(z*) = 0}` is the active set.
- **(SC)** strict complementarity: `mu*_j > 0` for all `j in A`.
- **(SOSC)** `d^T grad^2 L(z*) d >= gamma |d|^2` for all `d` in the critical cone
  `C = {d : grad g_j(z*)^T d = 0 (j in A), grad h_k(z*)^T d = 0 (k)}`, for some
  `gamma > 0`, where `L(z) = L(z; mu*, lambda*) = f(z) + sum_j mu*_j g_j(z) + sum_k lambda*_k h_k(z)`.

Under (SC), `C` is a linear subspace. Let `V = C^perp` be the span of the active
gradients.

**Lower bounding scheme.** For a box `Z subseteq X` let `f^cv_Z`, `g^cv_{j,Z}`
be convex underestimators and `h^cv_{k,Z} <= h_k <= h^cc_{k,Z}` convex and
concave relaxations on `Z`, with a constant `tau > 0` (independent of `Z`; a
positive constant may also be chosen for exact relaxations) such that

```
0 <= f - f^cv_Z <= tau w(Z)^2,   0 <= g_j - g^cv_{j,Z} <= tau w(Z)^2,   0 <= h_k - h^cv_{k,Z} <= tau w(Z)^2,   0 <= h^cc_{k,Z} - h_k <= tau w(Z)^2   on Z,
```

where `w(Z)` is the width (largest side length) of `Z`. This is second-order
pointwise convergence in the sense of Bompadre–Mitsos and Kannan–Barton
(Definition 13 of the 2018 paper). The lower bound is

```
L(Z) = inf { f^cv_Z(z) : z in R(Z) },   R(Z) = { z in Z : g^cv_{j,Z}(z) <= 0, h^cv_{k,Z}(z) <= 0 <= h^cc_{k,Z}(z) },
```

with `L(Z) = +infinity` if `R(Z)` is empty. Only the value `L(Z)` is used; the
argument makes no claim about where the relaxed minimizer lies.

## 2. The neighborhood bound

**Theorem 1.** Under (KKT), (LICQ), (SC), (SOSC) and second-order pointwise
convergence there exist `rho > 0` and constants `c_1 = gamma/4`, `c_2 > 0`,
depending only on the data of (P) at `z*` (and on `tau`), such that for every box
`Z subseteq B(z*, rho)` and every `z in R(Z)`,

```
f^cv_Z(z) >= f* + (gamma/4) |z - z*|^2 - c_2 w(Z)^2,
```

and consequently

```
L(Z) >= f* + (gamma/4) dist(Z, z*)^2 - c_2 w(Z)^2,       dist(Z, z*) = min_{z in Z} |z - z*|.
```

*Proof.* Fix a box `Z subseteq B(z*, rho)` with `rho` to be chosen, write
`w = w(Z)`, and let `z in R(Z)` be arbitrary (if `R(Z)` is empty, `L(Z) = +infinity`
and there is nothing to prove). Then `f^cv_Z(z) >= f(z) - tau w^2`. Put
`d = z - z*`; then `|d| >= dist(Z, z*)` and `|d| <= rho`. No attainment of the
minimum in `L(Z)` is needed: the pointwise bound is proved for every `z in R(Z)`
and the second display follows by taking the infimum.

*Step 1: constraint values on the relaxed set.* From `g_j <= g^cv_{j,Z} + tau w^2`
and `g^cv_{j,Z}(z) <= 0`: `g_j(z) <= tau w^2` for all `j`. From the two
relaxations of `h_k`: `|h_k(z)| <= tau w^2`.

*Step 2: the Lagrangian identity.* Since `mu*_j = 0` for `j notin A`,

```
f(z) = L(z) - sum_{j in A} mu*_j g_j(z) - sum_k lambda*_k h_k(z)
     >= L(z) + sum_{j in A} mu*_j (-g_j(z))_+ - |mu*|_1 tau w^2 - |lambda*|_1 tau w^2,
```

using `-g_j(z) >= (-g_j(z))_+ - tau w^2` (Step 1) and `|h_k(z)| <= tau w^2`.
Write `G = sum_{j in A} (-g_j(z))_+ >= 0` and `mu_min = min_{j in A} mu*_j > 0`
(if `A` is empty, `G = 0` and the terms below involving `G` disappear). Then
`sum_{j in A} mu*_j (-g_j(z))_+ >= mu_min G`.

*Step 3: Taylor expansions.* Let `M` bound the operator norms of the Hessians of
`f, g_j, h_k, L` on `B(z*, rho_0)` for some fixed `rho_0`, and let
`omega(t) = (1/2) sup_{|y - z*| <= t} ||grad^2 L(y) - grad^2 L(z*)||`, a
nondecreasing function with `omega(t) -> 0` as `t -> 0` by continuity of the
Hessian. Taylor's theorem with the integral (or Lagrange) remainder gives, on
`B(z*, rho_0)`, `|g_j(z) - grad g_j(z*)^T d| <= (M/2)|d|^2`,
`|h_k(z) - grad h_k(z*)^T d| <= (M/2)|d|^2` (using `g_j(z*) = 0` for `j in A`,
`h_k(z*) = 0`), and, since `grad L(z*) = 0` and `L(z*) = f*` by (KKT),

```
L(z) >= f* + (1/2) d^T grad^2 L(z*) d - omega(|d|) |d|^2.
```

(If the Hessian of `L` is Lipschitz with constant `2K`, then `omega(t) <= K t`
and the remainder is the familiar `K |d|^3`; only continuity is needed.)

*Step 4: the normal component is controlled by constraint values.* Decompose
`d = d_C + d_V` with `d_C in C`, `d_V in V`. By (LICQ) the linear map
`d_V -> (grad g_j(z*)^T d_V)_{j in A}, (grad h_k(z*)^T d_V)_k` is injective on `V`,
so there is `kappa_0` with `|d_V| <= kappa_0 ( sum_{j in A} |grad g_j(z*)^T d| + sum_k |grad h_k(z*)^T d| )`
(the forms vanish on `d_C`). By Step 3, `|grad h_k(z*)^T d| <= |h_k(z)| + (M/2)|d|^2 <= tau w^2 + (M/2)|d|^2`;
and `grad g_j(z*)^T d <= g_j(z) + (M/2)|d|^2 <= tau w^2 + (M/2)|d|^2` while
`-grad g_j(z*)^T d <= (-g_j(z))_+ + (M/2)|d|^2`, so
`|grad g_j(z*)^T d| <= (-g_j(z))_+ + tau w^2 + (M/2)|d|^2`. Hence

```
|d_V| <= kappa_0 G + kappa_1 (tau w^2 + (M/2)|d|^2),      kappa_1 = kappa_0 (|A| + r).
```

*Step 5: the quadratic form.* By (SOSC) on `d_C` and the bound `M` on the Hessian,

```
(1/2) d^T grad^2 L(z*) d >= (gamma/2)|d_C|^2 - M |d_C| |d_V| - (M/2)|d_V|^2
                          >= (gamma/2)|d|^2 - M' |d| |d_V|,        M' = gamma/2 + 3M/2,
```

using `|d_C|^2 = |d|^2 - |d_V|^2`, `|d_C| <= |d|` and `|d_V| <= |d|`.

*Step 6: assembling.* Combining Steps 2–5,

```
f(z) - f* >= (gamma/2)|d|^2 - M'|d||d_V| - omega(|d|)|d|^2 + mu_min G - (|mu*|_1 + |lambda*|_1) tau w^2
          >= (gamma/2)|d|^2 - omega(|d|)|d|^2 - M' kappa_1 (M/2)|d|^3 - M' kappa_1 tau w^2 |d|
             + G ( mu_min - M' kappa_0 |d| ) - (|mu*|_1 + |lambda*|_1) tau w^2.
```

Choose `rho <= rho_0` so small that for `|d| <= rho`: (i) `M' kappa_0 |d| <= mu_min`,
so the term in `G` is nonnegative and can be dropped; (ii)
`omega(rho) + M' kappa_1 (M/2) rho <= gamma/4`, so the remainder terms are at least
`-(gamma/4)|d|^2`. Also `M' kappa_1 tau w^2 |d| <= M' kappa_1 tau rho w^2`. Therefore

```
f(z) - f* >= (gamma/4)|d|^2 - c' w^2,    c' = tau ( |mu*|_1 + |lambda*|_1 + M' kappa_1 rho ),
```

and with `f^cv_Z(z) >= f(z) - tau w^2` and `|d| >= dist(Z, z*)`, taking the
infimum over `z in R(Z)` gives

```
L(Z) >= f* + (gamma/4) dist(Z, z*)^2 - c_2 w(Z)^2,    c_2 = c' + tau.   □
```

**Remarks on Theorem 1.**

1. *Where each hypothesis is used.* (KKT) gives `grad L(z*) = 0`, so the
   Lagrangian has no linear term (Step 3). (SC) gives `mu_min > 0`, which is
   what makes the inward normal slack `G` harmless (Step 6); without it, a
   direction `d_V` into the interior of a degenerate active constraint (`mu*_j = 0`)
   would contribute to `|d_V|` but not to `G`, and the cross term `-M'|d||d_V|`
   could dominate. (LICQ) gives `kappa_0` (Step 4). (SOSC) gives `gamma` (Step 5).
   Second-order pointwise convergence gives the `w^2` terms in Steps 1–2 and in
   the passage from `f^cv_Z` to `f`. Strictly speaking (LICQ) is not used: Step
   4 only needs the active-gradient map to be injective on `V = C^perp`, which
   holds for any finite family (`kappa_0` is the reciprocal of its smallest
   singular value on `V`), so the theorem holds for any KKT multiplier pair
   satisfying (SC) and (SOSC) on `C`. (LICQ) is kept because it is the standard
   hypothesis making the multipliers unique and (SC) meaningful.
5. *Bound constraints.* `z*` need not be interior to `X`: active bounds are
   among the `g_j`, and (SC), (SOSC) are then required with them included. This
   is a small generalization of Kannan–Barton's Theorem 5, which assumes an
   interior KKT point.
2. *Only the value of the relaxation is used.* Kannan and Barton's Theorem 2
   requires the relaxed minimizer to lie within `O(w^2)` of the feasible set of
   `Z`; Theorem 1 does not, because the Lagrangian with fixed multipliers
   already penalizes constraint violation of the right order.
3. *Interior minimizers and unconstrained problems.* If `A` and the equalities
   are empty, `V = {0}`, `L = f`, and (SOSC) is positive definiteness of
   `grad^2 f(z*)`: the bound reads `L(Z) >= f* + (gamma/4) dist(Z, z*)^2 - 2 tau w^2`,
   the classical unconstrained estimate behind Wechsung–Schaber–Barton.
4. *The constant `c_2` is explicit* in terms of `tau`, the multipliers, the
   Hessian bound and the LICQ constant, and `c_1 = gamma/4` can be replaced by
   any constant below `gamma/2` at the cost of a smaller `rho`.

## 3. The cluster count

Consider a branch-and-bound method that maintains an incumbent value `UBD` and
fathoms a box `Z` when `L(Z) >= UBD - eps` for an absolute tolerance `eps > 0`.
As in Kannan–Barton (2017), assume the incumbent has reached the optimum,
`UBD = f*` (a larger incumbent `f* + eta` with `eta < eps` amounts to the
tolerance `eps - eta`; see Section 4). Call a box `Z` *unfathomable* if
`L(Z) < f* - eps`. Note that with `UBD = f*` every box with `L(Z) >= f* - eps` is
fathomed, including boxes containing `z*` once they are small.

**Theorem 2.** Under the hypotheses of Theorem 1, let `delta > 0` and let
`{Z_i}` be any collection of boxes contained in `B(z*, rho)` with pairwise
disjoint interiors and side lengths in `[delta/2, delta]`. Then the number of
unfathomable boxes among the `Z_i` is at most

```
N_max = ( 4 sqrt(c_2/c_1) + 4 sqrt(n) + 2 )^n,
```

a constant independent of `eps` and `delta`. If moreover `delta^2 <= eps / c_2`,
no box in the collection is unfathomable.

*Proof.* Let `Z_i` be unfathomable. By Theorem 1,
`f* - eps > L(Z_i) >= f* + c_1 dist(Z_i, z*)^2 - c_2 w(Z_i)^2`, so
`c_1 dist(Z_i, z*)^2 < c_2 delta^2 - eps <= c_2 delta^2`. If `c_2 delta^2 <= eps`
this is impossible, proving the last claim. Otherwise
`dist(Z_i, z*) < sqrt(c_2/c_1) delta =: R`, so `Z_i` (whose diameter is at most
`sqrt(n) delta`) is contained in the ball `B(z*, R + sqrt(n) delta)`, hence in
the cube `Q` of side `2(R + sqrt(n) delta)` centered at `z*`. The boxes have
disjoint interiors and volumes at least `(delta/2)^n`, and all lie in `Q`, so
their number is at most `vol(Q) / (delta/2)^n = (4(R + sqrt(n) delta)/delta)^n = (4 sqrt(c_2/c_1) + 4 sqrt(n))^n`.
(The `+2` in `N_max` is a harmless slack for boxes that touch the boundary of
`Q` if one prefers to count boxes of a fixed grid.) □

In the language of Kannan and Barton (2017), Theorem 2 says that the estimate
of the number of boxes required to cover the region that cannot be fathomed is
`O(1)` in `eps`, which is the conclusion their Theorem 3 and Remark 5 draw from
second-order convergence of the scheme on a neighborhood. Theorem 1 supplies a
substitute for that hypothesis, namely the mixed bound `(*)`, whose second
term is second-order in `w(Z)` and whose first term is second-order in the
distance to `z*`. The scheme need not be second-order convergent at nearby
feasible points in their sense (Definition 14 of the 2018 paper, which measures
`min_{F(Z)} f - L(Z)` for boxes containing the point); what matters for
fathoming is the comparison with `f*`, not with `min_{F(Z)} f`. Indeed the
literal neighborhood property can fail for standard schemes even under (LICQ),
(SC), (SOSC). **Example (corrected and checked algebraically).**
`min -x_3 + 2 x_1^2 + 2 x_2^2` s.t. `g = x_3 + x_1^2 - x_2^2 + x_1 x_2 <= 0` on
`[-1, 1]^3`: `z* = 0`, `mu* = 1`, `gamma = 4 - sqrt 5 > 0` on the critical cone
`{d_3 = 0}`. The feasible points `y_b = (b, -2b, 5 b^2)` satisfy `g(y_b) = 0` and
`d g / d x_1 (y_b) = 0`. For the box
`Z = [b - w/2, b + w/2] x [-2b, -2b + w] x [5b^2, 5b^2 + w]`, take
`0 < b <= 1/4` and `0 < w < b`. Write a point in `Z` as
`(b+t, -2b+s, 5b^2+q)`, with `|t| <= w/2` and `s,q in [0,w]`. Then
`g = q + t^2 + s(5b+t-s)`, whose terms are nonnegative and vanish together
only at `t=s=q=0`. Thus `F(Z) = {y_b}` and `min_{F(Z)} f = 5b^2`.
For the αBB relaxation of `g` with `alpha = sqrt(5)/2`, put
`k = sqrt(alpha/(1+alpha))`. At `t=-kw/2`, `s=q=0`, the relaxed constraint
value is `(1+alpha)t^2-alpha w^2/4=0`, so this point is relaxed-feasible.
Keeping the convex objective exact therefore gives

```
min_{F(Z)} f - L(Z) >= 2 b k w - (k^2/2) w^2.
```

The objective is locally Lipschitz, so the gap is also `O(w)` for fixed `b`.
It is consequently `Theta(w)` at each `y_b`, ruling out the second-order
neighborhood property for this standard αBB scheme even arbitrarily near
`z*`. Theorem 1 nevertheless fathoms these boxes when they are sufficiently
small, since their distance from `z*` stays positive for fixed `b`. This
example does not rule out a different scheme attaining the neighborhood
property. The earlier version placed the `x_2` interval on the wrong side of
`y_b`; its singleton-feasible-set claim and reported gap limits were invalid.

## 3b. Reduced-space schemes and domain reduction

Kannan and Barton's second open question concerns *reduced-space* schemes:
variables are split as `z = (x, y)`, branching is done on `y` only, and for a
box `Z` in `y`-space a domain-reduction (bound-tightening) map returns a box
`X(Z)` in `x`-space with `X(Z) supseteq F_X(Z) := {x : (x, y) feasible for some y in Z}`;
the lower bound is the full-space bound on the product box,
`L_red(Z) := L(X(Z) x Z)`, computed with the same relaxations (this is the
Epperly–Pistikopoulos scheme in their Section 5, with `X(Z)` playing the role of
their bound-tightened set). Their Examples 16–18 show that with `X(Z) = X` such
schemes are first order and cluster, and that constraint propagation can
restore second order; they ask for sufficient conditions on the propagation.
Theorem 1 gives one immediately.

**Theorem 3 (width-tight domain reduction is cluster-free).** Assume the
hypotheses of Theorem 1 at `z* = (x*, y*)`, with `rho` and `c_2` as there. Let
the reduction map satisfy, for every box `Z subseteq B(y*, rho')` in `y`-space,

```
(WT)   X(Z) x Z subseteq B(z*, rho)   and   w(X(Z)) <= C w(Z)
```

for constants `rho' > 0`, `C >= 1`. Then for every such `Z`,

```
L_red(Z) >= f* + (gamma/4) dist(Z, y*)^2 - c_2 C^2 w(Z)^2,
```

and the conclusion of Theorem 2 holds for boxes in `y`-space with `n` replaced
by `n_y = dim y` and `c_2` by `c_2 C^2`.

*Proof.* The product box `B = X(Z) x Z` lies in `B(z*, rho)` and has width
`w(B) = max(w(X(Z)), w(Z)) <= C w(Z)`; and `dist(B, z*) >= dist(Z, y*)` since
`|(x, y) - (x*, y*)| >= |y - y*|`. Theorem 1 applied to `B` gives the display.
The counting argument of Theorem 2 is unchanged in `y`-space. □

**When is (WT) available?**

1. *A certified local implicit branch.* Suppose `n_x` equality constraints
   have nonsingular `grad_x h(z*)`. The implicit function theorem supplies a
   unique local branch `x=x(y)`. To use it for domain reduction, restrict the
   current search box to this certified branch, or establish that no other
   feasible branches are present. Other constraints may further restrict the
   branch, so in general `F_X(Z) subseteq x(Z)`, not equality. Choose a local
   Lipschitz constant `Lip` in the infinity norm. Then the interval hull of
   `x(Z)` has width at most `Lip w(Z)`. More constructively, if `y_c` is the
   center of `Z` and a certified center estimate satisfies
   `|x_hat-x(y_c)|_infinity <= K w(Z)`, the box centered at `x_hat` with
   coordinate radius `(Lip/2+K)w(Z)` encloses `x(Z)` and has width at most
   `(Lip+2K)w(Z)`. For small enough `rho'` this proves (WT). Interval Newton
   or Krawczyk methods may certify the local branch and an enclosure, but an
   arbitrary regular starting enclosure or iteration does not by itself
   establish the claimed width bound. No generic `O(w(Z)^2)` excess-width
   guarantee is asserted here.
2. *Affine equations that uniquely determine `x`.* For a local representation
   `A(y)x=b(y)` with continuously differentiable data and a uniformly
   nonsingular square matrix `A(y)`, the same argument applies to the smooth
   map `x(y)=A(y)^{-1}b(y)`, provided the enclosure is certified. Affine
   constraints alone do not imply (WT): a feasible fiber `x in [0,1]` can have
   fixed positive width for every `y`, even when all its vertices are
   Lipschitz in `y`. Moreover, ordinary bound propagation need not recover a
   narrow fiber. For example, with `x_1+x_2=y`, `x_1-x_2=0`,
   `x in [-1,1]^2`, and `y in [-delta,delta]`, the exact fiber has
   `x_1=x_2=y/2`, while propagation of the individual equations can leave
   both `x` intervals unchanged. Exact optimization-based bound tightening
   would recover the true ranges in this linear example; no blanket claim
   is made for approximate OBBT or FBBT.
3. *What (WT) excludes.* Kannan–Barton's Examples 17–18 obtain second order
   without shrinking `X(Z)` (there `X(Z) = [-1, 1 - y^L]` has width of order
   one): the mechanism is that the relaxed minimizer is pushed onto a
   tightened face where the McCormick underestimator is exact ("anchoring"),
   not width control. Theorem 3 does not cover that mechanism. Its sufficient
   condition must be verified for the actual reduction map.
4. *Limits of the width-based estimate.* With `X(Z) = X` of fixed positive
   width and `w(Z) <= w(X)`, the product box has width `w(X)`. If it lies
   inside the neighborhood required by Theorem 1, that theorem gives only
   `L_red(Z) >= f* + (gamma/4) dist(Z, y*)^2 - c_2 w(X)^2`.
   This estimate alone does not prove convergence as `w(Z)` shrinks. If the
   product box leaves the neighborhood, Theorem 1 does not apply at all.
   Neither fact proves that domain reduction is necessary: a different
   argument, an exact relaxation, or an anchoring mechanism can still work.

## 4. Sharpness and limits

- **Degenerate minimizers.** Without (SOSC), this proof does not guarantee
  quadratic growth, and clustering can occur. In Kannan–Barton's Remark 4
  example (`min x_2` s.t. `x_1^4 <= x_2 <= 1`, `z* = 0`), `f` grows only
  quartically along the critical direction. At scale `delta ~ sqrt(eps)`,
  the `eps`-suboptimal feasible set has tangential extent `Theta(eps^{1/4})`
  and normal extent `O(eps)`, so its covering count is
  `Theta(eps^{1/4}/delta) = Theta(eps^{-1/4})`. This is a statement at that
  scale, not a formula for arbitrary `delta`. Whether boxes actually fail
  the fathoming test depends on the relaxation error and box bounds. With
  exact linear objective and `x_2 >= 0` imposed, every lower bound is at
  least the global optimum, so all boxes fathom for any positive tolerance.
  Example B below illustrates growth with a different constraint geometry.
- **Failure of strict complementarity.** Removing (SC) while keeping
  positivity only on the equality tangent subspace is insufficient:
  `min x_1^2 + x_2^4` s.t. `-x_2 <= 0` has the unique global minimizer `0`,
  `mu* = 0`, LICQ, and Hessian positivity with `gamma = 2` on `{d_2 = 0}`.
  This is not standard SOSC on the actual critical cone when (SC) fails.
  Boxes containing `(0,a)` have `L(Z) <= a^4`, contradicting the asserted
  quadratic distance bound for sufficiently small `a` and `w/a`.
  The same proof works with `A` replaced by the strongly active set if the
  Hessian is positive definite on the larger linear subspace annihilating
  its gradients and the equality gradients. This condition is stronger
  than standard SOSC on the actual critical cone, which also includes
  the weakly active inequalities; that weaker extension is not proved here.
- **First-order relaxations.** Replacing required second-order error bounds
  by `tau w` gives `-c w` in place of `-c_2 w^2`. At scale `delta ~ eps`,
  the resulting packing argument gives a worst-case upper bound
  `O(eps^{-n/2})`, not a universal matching lower bound. A relaxation can
  remain effective despite a loose first-order error bound. The proof
  requires second-order error bounds for the objective, equalities and
  active inequalities. Inactive inequalities do not enter the estimates
  and can use weaker valid underestimators.
- **Reduced-space schemes and domain reduction.** Theorem 3 covers
  reduced-space schemes whose bound tightening keeps the unbranched box within
  a constant factor of the branching width; the anchoring mechanism of
  Kannan–Barton's Examples 17–18 (second order without width control) is not
  covered, see `notes/screen-cluster-problem-domain-reduction.md`.
- **Incumbent.** With `UBD = f* + eta`, a box is unfathomable iff
  `L(Z) < f* - (eps - eta)`, so for `eta < eps` the same count holds with
  `eps` replaced by `eps - eta`. At `eta = eps`, the scale-wise packing
  bound still holds, but there is no positive width threshold forcing
  fathoming; a box containing `z*` is fathomed only if its lower bound
  equals `f*`. At `eta > eps`, such boxes cannot be fathomed. Thus finite
  termination by this argument requires a sufficiently accurate incumbent.

## 5. Numerical illustration

`code/cluster_problem/count_boxes.py` runs a minimal spatial branch-and-bound
(bisection of the widest side, best-bound selection, incumbent fixed at `f*`,
fathoming at tolerance `eps`) with the same generic second-order relaxation of
the nonlinear constraint in both examples, `g^cv = g - alpha sum_i (x_i - l_i)(u_i - x_i)`
with `alpha = 1` (error `<= alpha n w^2/4`), convex objectives kept exact, and
counts the nodes processed and the maximal number of simultaneously open boxes:

- **A (nondegenerate).** `min x_1^2 + x_2^2` s.t. `x_1 x_2 >= 1`, `x in [0.5, 2]^2`;
  `z* = (1, 1)`, `mu* = 2`, critical cone `{d_1 + d_2 = 0}`, Hessian of the
  Lagrangian `[[2, -2], [-2, 2]]`, positive definite on the critical cone but
  singular on `R^2`. The recorded number of open boxes is at most 6 across
  the tested tolerances, and the node counts are consistent with logarithmic growth (7 to
  41 nodes as `eps` falls from `6e-2` to `1e-6`).
- **B (degenerate).** `min x_2 - x_1` s.t. `x_2 >= x_1 + (x_1 - 1)^4`,
  `x in [0, 2] x [0, 3]`; `z* = (1, 1)`, `mu* = 1`, Hessian of the Lagrangian
  zero at `z*` (quartic growth along the critical direction, so (SOSC) fails).
  Recorded node and open-box counts are consistent with `eps^{-1/4}` growth (18 to 362 nodes, 6 to 65 open
  boxes over the same range of `eps`).

The table is in the code README. These finite, floating-point runs are an
illustration, not certified node counts or evidence for an asymptotic rate or
the theorem's constants. The script uses numerical primal objective values
as estimates of relaxation optima and accepts inaccurate solver statuses;
neither these values nor reported infeasibility are rigorous lower-bound
certificates. The existing log includes an accuracy warning. (A first attempt with
Kannan–Barton's textbook examples `min -x_1 x_2, x_1 + x_2 <= 1` and
`min x_2, x_1^4 <= x_2` was uninformative: box bounds make their lower bounds
exact after one bisection, so both fathom immediately.)

## 6. Literature

- **Anitescu (2005), SIAM J. Optim. 15(4):1203–1236**,
  [open preprint](https://optimization-online.org/wp-content/uploads/2004/08/918.pdf),
  Section 1.3, equations (1.18)–(1.19): exact penalties have quadratic growth
  off the feasible set under the stated generalized growth and multiplier
  assumptions. Under MFCQ, Section 1.2 relates this to feasible quadratic
  growth. This already supplies the core inequality needed here. The paper
  attributes it to Bonnans–Shapiro, Theorem 3.113; that book theorem was not
  directly inspected in this continuation.
- **Du, Kearfott (1994), J. Global Optim. 5:253–265; Wechsung, Schaber, Barton
  (2014), J. Global Optim. 58:429–438.** Unconstrained cluster problem: the
  classical covering estimates at width `delta ~ eps^{1/beta}` scale as
  `eps^{n(1/2 - 1/beta)}` for quadratic growth and convergence order `beta`
  in the relevant first-/second-order cases; second order suffices.
- **Kannan, Barton (2017), J. Global Optim. 69:629–676.** Constrained cluster
  problem: first order suffices when `f` grows linearly along feasible
  directions (trivial critical cone); second order on a neighborhood is
  sufficient under their assumptions otherwise (Lemma 8, Theorem 3, Remark 5); Remark 4 gives the quartic
  degenerate example.
- **Kannan, Barton (2018), J. Global Optim. 71:753–813.** Convergence orders of
  lower bounding schemes; Theorem 2 (second order at a feasible point given
  condition (3) on the relaxed argmin), Theorem 5 and Corollary 4 (second order
  at an interior KKT point via the Lagrangian with fixed multipliers, for the
  dual and the convex-relaxation schemes), reduced-space results, and the open
  question quoted above. Theorem 1 of this note is the Theorem 5 computation
  carried out at points `z != z*` of the relaxed feasible set, with (LICQ) and
  (SC) supplying the control of the normal component that is automatic at
  `z = z*`.
- **Bompadre, Mitsos (2012), J. Global Optim. 52:1–28; Najman, Mitsos (2016).**
  Second-order pointwise convergence of McCormick relaxations of factorable
  functions with envelopes and of αBB relaxations; the hypothesis of Theorem 1
  is met by the standard schemes.
- **Neumaier (2004), Acta Numerica; Schichl, Neumaier (2005); Schichl, Markót,
  Neumaier (2014).** Exclusion regions around solutions of equations and around
  KKT points for complete search; related in spirit (a box near a
  nondegenerate KKT point can be certified), different in mechanism (interval
  Newton and Kantorovich-type conditions rather than lower bounding).
- **Initial literature check (2026-09-22, subagent; superseded in its novelty
  assessment by the exact-penalty comparison above).** No published statement
  of this particular spatial-search application was found. Kannan–Barton (2017) take the neighborhood
  convergence order as a hypothesis (their Definition 8 and Theorems 2–4) and,
  in Remark 2 after Lemma 8, suggest estimating the growth constant `gamma` from
  the Lagrangian with fixed multipliers on the *feasible* set; the present
  Theorem 1 bounds the Lagrangian on the *relaxed* feasible set of a box, which
  is what fathoming needs. Kannan–Barton (2018) and Kannan's MIT thesis (2018,
  p. 304) repeat the neighborhood question as future work. Neumaier (2004),
  Acta Numerica 13, Section 15, remarks without proof that for constrained
  problems "similar arguments as for the unconstrained case apply in a reduced
  manifold" with `n` replaced by `n - a`, `a` the number of active constraints
  with independent gradients; Theorem 2 is a proof of a statement of that kind
  (with the count exponent `n`, not `n - a`, since the box collection is
  `n`-dimensional; the reduced-manifold count concerns covering the feasible
  near-optimal set). Robertson, Cheng, Scott (2025), J. Global Optim. 91, treat
  Hausdorff convergence orders of value-function relaxations in the reduced
  space and state that high order is necessary but not sufficient to avoid
  clustering; no constrained neighborhood result. The exclusion-region
  literature (Schichl, Markót, Neumaier 2014; Kearfott 2015) certifies boxes
  around Karush–John points by interval Newton tests, a different mechanism, and
  gives no `eps`-independent count. An unsuccessful search does not establish
  novelty.
