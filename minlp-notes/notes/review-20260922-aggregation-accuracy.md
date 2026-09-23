# Adversarial review of finite good-aggregation accuracy

Date: 2026-09-22. Reviewer: independent agent assigned the completed
[accuracy note](research-20260922-aggregation-accuracy.md) and
[main construction](../results/infinite-quadratic-aggregation-hhc.md).
The author files were not edited. No further agents were used.

**Verdict:** the stated two-sided bound and objective-dependent exactness
proposition are correct. I found no substantive proof gap. The contribution
is a useful quantitative consequence of this particular construction, with
the significance limits already stated in the note. It is not evidence for
a new general convex-body approximation principle or an iteration lower
bound. Exact rational coefficients suffice for the same asymptotic rate;
ordinary independent rounding of coefficients is not automatically safe.

## 1. Upper bound and all endpoint cases

The nonnegative rank-one rays
`(cos²(theta),sin²(theta),2cos(theta)sin(theta))`, including the two
coordinate rays, generate the entire stated cone `K`. One explicit check
is that an element with positive first two coordinates decomposes into a
nonnegative multiple of `(lambda1,lambda2,2sqrt(lambda1lambda2))` and
coordinate rays. If its third coordinate is zero, only the coordinate
rays are needed. Thus testing the sampled rank-one family is consistent
with the full good cone, not merely a smaller family.

On the relaxation containing both coordinate cuts, each diagonal of
`A(x)` lies in `[0,1]` and the absolute off-diagonal entry is at most
`3/2`. Symmetry and the absolute row-sum bound give operator norm at
most `5/2`. The two terms in the displayed second derivative each have
absolute value at most `5`, so `|h''|<=10` is valid uniformly in dimension.

If a minimizing angle is an endpoint, its value is nonnegative. Otherwise
its derivative vanishes and its nearest mesh point has distance at most
`Delta/2`; Taylor's upper bound at that point is
`h_min + 5(Delta/2)²`. Combining this with the nonnegative sampled value
gives exactly `h_min >= -5Delta²/4`. The sign in this reasoning is correct.

The radial identity is exact because the nonconstant terms of `A` are
homogeneous quadratics. The smallest eigenvalue of `A(0)` is `1/2`, and
`s²=1/(1+2a)` therefore makes every nonnegative directional quadratic form
nonnegative. This repair also handles indefinite matrices `A(x)`; the
argument never incorrectly requires positive semidefiniteness of `A(x)`.
The repaired point belongs to the exact hull by the main result.

The inequality `1-(1+2a)^(-1/2)<=a` holds for every `a>=0`, so there is no
unstated small-error condition. Substituting the mesh size yields exactly
`5sqrt(2)pi²/[16(N-1)²]`. In particular, `N=2`, where there are only the
coordinate cuts, is covered. The constant is loose in that case, which
does not affect validity.

Each finite intersection is closed and convex and contains the nonempty
compact set `C`. The constructed intersection is bounded by the endpoint
cuts, hence compact. Its Hausdorff distance is therefore the supremum of
the distances of all relaxation points to `C`; the radial repair controls
that full supremum.

## 2. Lower bound, arbitrary multipliers, and constants

The Gram witnesses are strictly positive definite. Their diagonal lower
bound `4/5` and off-diagonal absolute upper bound `2/5` imply determinant
at least `12/25`. Their realization needs only two vector coordinates,
so all witness estimates apply to every `r>=2`.

Let `s=sqrt(lambda1lambda2)>0`. Exclusion of a witness means

```
e(lambda1/tau+lambda2*tau-lambda3) < eta*lambda3.
```

Using `lambda3<=2s` on both sides gives
`lambda1/tau+lambda2*tau-2s < (2eta/e)s =20eta*s`.
Division by `s` proves the claimed logarithmic exclusion interval. This
step is valid for interior good multipliers, including those with third
coordinate zero: such a cut simply cannot exclude a witness. When either
first or second coordinate vanishes, membership in `K` forces the third
coordinate to vanish and the cut is strictly satisfied at all witnesses.
Thus no multiplier case was omitted.

Since `t/tau+tau/t=2cosh(log(t)-log(tau))`, the interval radius is exactly
`arcosh(1+10eta)`. Its length is at most `4sqrt(5eta)`. With the chosen
`eta`, this becomes `(log 2)/(2N)`, so even counting overlaps as if they
were disjoint the union of at most `N` exclusion intervals cannot cover
`[0,log 2]`. The argument does not require a bound on `t`, attainment of
an optimal cut bank, or a strict slack in every surviving cut.

At the surviving witness the omitted multiplier has violation `2eta`.
Its quadratic matrix has eigenvalues `0` and `tau+1/tau<=5/2` per
coordinate block. The gradient is twice the matrix times the variable,
so its norm on the product of the unit balls is at most `5sqrt(2)`.
The segment from the witness to any point of `C` stays in that product.
The mean-value estimate therefore gives distance at least

```
2eta/(5sqrt(2)) = sqrt(2)(log 2)²/(1600N²).
```

An unbounded relaxation has infinite Hausdorff distance from compact
`C`, so it does not evade this lower bound. Empty families are harmless
for the same reason. The proof in fact supplies its positive lower
bound for singleton families as well; the theorem only states `N>=2`
because its upper-bound construction uses two endpoints.

## 3. Linear objectives and separation

The support-function interpretation is valid for bounded finite
relaxations: they are compact convex sets containing `C`. Projection
onto `C` supplies the separating unit vector needed for the reverse
Hausdorff inequality. An arbitrary adaptive selection rule still produces
a final family to which the same uniform lower bound applies. This says
nothing about how many cuts are needed for one prescribed objective.

I independently checked the single-objective proposition, particularly
the possible nonclosedness of `E`. Scalar convexity of every `f_lambda`
for `lambda in K` implies order convexity of `F`; the bipolar theorem
applies because `K` is closed. It follows that `E` is convex.
It has nonempty interior because `K*` contains the nonnegative orthant,
whose interior is nonempty, and the last coordinate can increase freely.

Feasibility of the optimizer gives `(0,v) in E`. No `(0,v-delta)` is in
`E`, since such membership would give a feasible point with objective
below `v`. Consequently `(0,v)` is a boundary point. A supporting
hyperplane exists for a convex set with nonempty interior at an included
boundary point; closedness of `E` is not required here. Equivalently,
support its closure, which has the same interior.

The upward recession directions force the signs `lambda in K, mu>=0`.
If `mu=0`, evaluation at zero contradicts
`f_lambda(0)<=-(lambda1+lambda2)/2<0` for every nonzero `lambda in K`.
Thus normalization to `mu=1` is valid. Evaluation at the optimizer then
forces complementary slackness, and `lambda=0` is ruled out by the
nonzero objective on the whole space. These steps also prove that the
single-cut minimum is attained at that optimizer, even if its feasible
set is unbounded. No boundedness assumption on the single cut is needed.

This is standard conic convex duality under a strict feasible point.
The note correctly avoids presenting it as a new duality theorem.

## 4. Coefficient representation and finite precision

The theorem as stated allows exact real multipliers. Equally spaced
angles may give irrational coefficients. This does not invalidate its
conclusion, but it does not alone prove a floating-point implementation
guarantee. In particular, perturbing three coordinates independently
can leave the good cone at its rank-one boundary.

The same rate has an elementary rational construction. For `N>=3`, set
`m=floor((N-1)/2)` and take the union of

```
(m²,j²,2mj), (j²,m²,2mj),   j=0,...,m.
```

There are exactly `2m+1<=N` distinct rays: the middle ray is shared.
Both coordinate rays occur. Every multiplier satisfies
`lambda3²=4lambda1lambda2` exactly. Their angles are `arctan(j/m)`
on the first half-interval and their reflections on the second.
Since `arctan` is 1-Lipschitz, successive angular gaps are at most `1/m`.
The same upper-bound proof therefore gives

```
d_H(C,P) <= 5sqrt(2)/(4m²) = O(N^-2).
```

The multiplier entries are nonnegative integers at most `2m²`, so each
has `O(log N)` bits. For `N=2`, the coordinate cuts are already rational.
This observation establishes an exact finite-representation rate with
a different explicit upper constant. It does not bound solver rounding
error, condition numbers, or errors in solving the relaxation. The
objective-dependent exact multiplier can still be irrational.

## 5. Literature and significance assessment

I independently opened Arya, da Fonseca, and Mount,
[Optimal Area-Sensitive Bounds for Polytope Approximation, v2](https://arxiv.org/html/2306.15648v2),
and inspected the introduction, Section 1.1, and Theorems 1 and 2.
It discusses the classical dimension-dependent facet and vertex
approximation rates and gives convex-function approximation bounds.
It does not directly address approximation by this fixed cone of
quadratic inequalities. The comparison in the author note is accurate.

The exponent here is consistent with ordinary approximation of a smooth
one-dimensional family. Dimension independence comes from the special
parameter geometry and uniform radial repair, not from circumventing
general polytope approximation lower bounds. Each quadratic cut itself
still acts on `2r` variables; the result counts inequalities, not encoding
or arithmetic complexity in `r`.

The lower bound's useful specificity is that arbitrary interior good
multipliers do not improve the rate. Together with the rational mesh and
the single-objective observation, this gives a precise comparison of
representation choices for the particular hull. It remains a modest
corollary of the main HHC construction. No source check here establishes
priority for that construction, and no claim of broad approximation
novelty should be inferred from this review.

## 6. Verification limits

I re-derived the analytic inequalities and separation argument above.
A targeted inline `python3` check using `fractions.Fraction` passed for
64 rational cut banks (`m=1,...,64`) and 10,100 Gram witnesses
(`n=1,...,100`, `tau=1+j/100`, `j=0,...,100`). It checked cut counts,
endpoint inclusion, exact cone-boundary identities, Gram determinant
bounds, and the exact violation `2eta`. The witness check used the
rational value `eta=1/(320n²)`, an upper bound on the theorem's smaller
value; it did not numerically evaluate `log 2` or establish the analytic
covering argument. No counterexample search is a proof of that argument.

No Lean formalization, project-wide verification, or CI inspection was
performed. The exact hull and HHC statements were taken from the main
construction; this review verifies their use in the accuracy note rather
than serving as a new independent review of all main-result proofs.
