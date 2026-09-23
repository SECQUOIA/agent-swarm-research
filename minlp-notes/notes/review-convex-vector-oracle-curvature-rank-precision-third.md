# Independent audit: oracle error bodies and curvature-rank precision

Date: 2026-09-05. Reviewer: potential_flow_review. Verdict: full PASS.

I independently checked the complete transfer in
[the candidate](convex-vector-oracle-curvature-rank-precision.md), including
its effective coordinates, both geometric bases, finite comparison,
constructive constants, subspace-preserving rounding, and rational compiler
requirements. I also read the supporting spanner statement and verified
its hypotheses at both applications. Its
[first full audit](review-rational-polar-spanner-oracle.md) and
[second full audit](review-rational-polar-spanner-oracle-second.md) now both
pass, closing the constructive dependency. No unresolved mathematical issue
was found. This is a correctness audit, not a publication-priority claim.

## Effective coordinates and separation

For a polynomial curve, the span of deviations from its endpoint secant
equals the span of coefficient columns of degree at least two. Indeed,
the scalar functions `x^j-x`, `j>=2`, are linearly independent, as follows
by inspecting their degree-at-least-two coefficients. Thus the proposed
rational rank computation identifies exactly the stated nonlinear image.

Choosing independent columns for `V` and taking its rational left inverse
gives polynomial-bit coordinate polynomials `q`, with both endpoint values
zero. These coordinate functions need not be convex. Only their original
positive scalarizations are used in the scalar convex compiler.

The effective body `C=V^(-1)K` is full-dimensional in its `r`-dimensional
coordinate space, compact and centrally symmetric. The inner radius follows
from `||V||_2<=sum|V_ij|`; the outer radius follows from `z=L(Vz)` and
`||Vz||_2<=sqrt(m)R<=mR`. Both displayed rational radii are therefore valid.
A violated ambient strong separator pulls back to a nonzero separator:
if its pullback vanished, its value at the query and at zero would agree,
contradicting strict separation from a body containing zero.

## Positive-polar reduction

The positive polar is a compact convex body with nonempty interior. Its
projected image spans `R^r`, since small nonnegative coordinate-axis vectors
are feasible and the rows of `V` span. It need not contain a ball centered
at zero, and the argument never assumes that it does.

Representing a projected polar vector in the selected basis makes the
corresponding scalarized output equal to that same linear combination of
selected scalarizations plus an affine function. Affine terms have zero
chord gap. The selected scalarizations are convex, because their weights
are nonnegative. Consequently even signed basis coefficients bounded by
`c` give `0<=g_(H_lambda)<=c sum_s g_(H_s)`.

Unconditionality is used at the correct place: the polar is unconditional,
so a nonnegative vector's gauge is the supremum over nonnegative polar
normals. Every original vector chord gap is nonnegative and belongs to the
nonlinear image. This proves equation (6) without requiring convexity of
the coordinate functions or a finite facet representation.

For positive rank, the scalar `Psi` cannot be affine. If its sum of
nonnegative scalar chord gaps vanished, every selected scalarization would
be affine; projected-basis independence would then force the entire nonlinear
image to vanish. The author added this case explanation during review.

## Inner band and finite count

Feasible columns of `B`, together with their negatives, generate a
crosspolytope contained in the centrally symmetric effective body. A basis
coefficient bound `d` gives its enclosing parallelotope. Scaling the inner
parallelotope by `1/r` therefore proves exactly

```
P subset K intersect S subset dr P.
```

This remains valid when `P` has lower dimension in the original ambient
output space. Linear equations for its image enforce that subspace exactly.

Maximum-absolute-determinant bases in the two compact spanning sets exist
and have coefficient bound one by a one-column replacement and Cramer's
rule. On each parity-contact hull, every selected polar scalarization has
midpoint gap at most one; hence the scalar full chord gap is at most `2r`.
Refining to tolerance `1/(2r)` uses at most `8r^2-1` intervals. Their vector
chord gaps lie in `P/2`. The symmetric band `P/2` around the exact chord
therefore contains the graph and has whole-projection error in `P`.

The midpoint argument uses exact contacts and their limits, so it applies
to arbitrary nonclosed convex lifts and unbounded integer coordinates.
Their errors elsewhere may lie outside the nonlinear image; the midpoint
Jensen vectors used here automatically lie inside it. Finite binary
disjunction encoding gives the claimed finite count with real coefficients.

## Constructive oracle hypotheses

The generic spanner lemma is applied to full-dimensional bodies, rather
than assuming a strong oracle for a lower-dimensional projected image.
For the positive-polar application, its seeds are small coordinate-axis
vectors at independent rows of `V`. For the primal application, they are
small coordinate-axis vectors of the effective body's known inner ball.
All seeds have polynomial-bit rational coordinates and a nonzero rational
image determinant.

The ambient coordinate radius is correctly replaced by the rational
Euclidean radius `mR`. The effective radii and separator satisfy the
other application directly. The supporting proof's weak polar separator,
exact central-ball repair, fixed denominator grid, determinant exchanges,
and dimension-one padding cover these uses. Thus it returns exactly
feasible rational bases with coefficient bound `9/4`, safely relaxed to
three in the main proof. No approximate support value is silently used as
an exact polar-feasibility test.

Polynomial-bit rational basis entries imply polynomial-bit exact inverses.
The supporting lemma also supplies a uniform polynomial bound before
iterative calls, rather than relying on potentially accumulating oracle
denominators. Both requirements needed by the main construction are met.

## Rounding, bands, and binary count

With `c=d=3`, the two geometry bounds give
`||e||_K<=3g_Psi` and `K intersect S subset 3rP`. At
`tau=1/(36r)`, the scalar compiler's exact endpoint chord gap at most
`13tau/16` therefore yields

```
e in (13/(192r))K intersect S subset (13/64)P.
```

The endpoint coordinate rounding is also valid. If its infinity-norm
error is at most `1/(16r L_B)`, multiplication by `B^(-1)` gives
infinity norm at most `1/(16r)`. Thus the error belongs to `P_0/16`.
Interpolation with the common input weight preserves this membership.
Restoring the affine output part exactly and applying `V` keeps the
rounding error exactly in `S`, and the center error belongs to `(17/64)P`.

The final `P/2` band contains the exact graph because it is larger than
this symmetric center-error set. Every admitted output error lies in
`(17/64+1/2)P=(49/64)P subset K`. Rounding the original output coordinates
independently would not have justified this conclusion; the proposed
coordinate rounding is the necessary step.

The scalar grid covers all input points even if successive rational knots
are repeated or reversed. At a repeated knot the exact chord gap is zero;
the same rounding and band estimates remain valid. Dense rational coordinate
evaluation, fixed offsets and precision, affine restoration, and explicit
band equations have polynomial encoding and use only continuous auxiliaries
beyond the shared global index bits.

The level-cut bound is `N_tau<=(144r^2-1)2^p`. The reviewed scalar compiler
has at most `486N_tau` actual cells, so

```
K_cells<69984r^2 2^p<2^17 r^2 2^p.
```

Taking a ceiling gives the stated safe upper bound
`p+17+2ceil(log2 r)`. Rank zero is the exact affine case. There is no
dependence on the unknown comparator in the construction itself.

## Independent exact diagnostics

[The separate mixed-coordinate checker](../code/quadratic_rank/check_oracle_curvature_rank_mixed_coordinates.py)
passed 70 positive-polar coefficient representations and 9,216 exact
rounding/band checks. Its four convex outputs use a rank-two mixed-sign
basis whose coordinate functions are not individually convex, and a
nontrivial inverse band matrix. Every rounded band remains in the nonlinear
image and inside the ambient unit-cube error body. These tests add a
distinct check of the subspace mechanism; the general oracle and compiler
guarantees follow from the full proofs, not from the finite diagnostics.
