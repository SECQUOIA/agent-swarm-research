# Independent review of the globally convex polynomial point oracle

Date: 2026-10-02. Status: fresh actual-file review passed.
No unresolved mathematical correction is requested. This review covers
Sections 1--7 of the saved
[globally-convex-polynomial-point-oracle.md](globally-convex-polynomial-point-oracle.md),
including the final input-length and zero-core clarifications and the
explicit unknown-tilt coefficient majorants. Prior comparison is separate;
this review makes no priority claim.

## Interpolation and the use of global convexity

Both elementary interpolation constants check. The denominator of each
Lagrange basis polynomial on the nodes `j/D` has magnitude at least
`D^(-D)`. Bounding its `D` numerator factors by `1+|t|` and summing the
`D+1` basis terms gives `C_D=(D+1)D^D`. At zero, differentiating the
numerator gives at most `D` terms, each with remaining factors of
magnitude at most one. Rescaling `[0,R]` gives the stated
`J_D=(D+1)D^(D+1)` bound on `|p'(0)|`.

For an optimizer `y`, convexity and constrained first-order optimality
give `0<=grad f(y)'(x-y)<=E`. The translated Bregman polynomial is
nonnegative on all of ambient space. On the feasible joining segment
it is at most `E`, so interpolation controls its extrapolation along
the whole line.

The midpoint inequality for `p_c(t)` is valid because convexity and
nonnegativity hold globally. Its points need not be feasible. With
`R=E^(-1/D)>=1`, the bound `E(1+2R)^D<=3^D` removes the dependence
of the upper bound on the gap. The coefficient majorants in equation
(9) are sufficient: `y` and `2c-y` lie in the box of radius `K=U+2D`,
and the supporting-plane term is bounded by `2G(D+U)`.

Thus derivative interpolation gives exactly the claimed row residual
of order `E^(1/D)`. The zero-gap argument is also complete: vanishing
on the segment makes the directional polynomial identically zero;
the midpoint inequality then bounds `p_c` on the entire real line,
forcing it to be constant. It does not rely on the existence of a
feasible positive-gap sequence.

This is the essential distinction from convexity only on a bounded
domain. That weaker assumption would not justify the midpoint or
extrapolation argument. The statement correctly keeps global convexity
as a promise or charged verification premise.

## Rational gradient rows and the optimizer set

The nonnegative integer nodes of total degree at most `D-1` are
unisolvent. In the product-binomial basis, a nonzero evaluation requires
the basis multiindex to be coordinatewise at most the node. Ordering by
total degree gives a triangular matrix whose diagonal is one. The node
count is polynomial in dimension for fixed `D`, and all evaluations of
the explicit rational gradient have polynomial bit length.

It follows that the kernel of the sampled-gradient matrix is precisely
the set of directions along which the polynomial is globally invariant.
The zero-gap row estimate puts every optimizer difference in this
kernel. Conversely such invariance preserves objective value, proving
the affine-slice characterization of `S`. Constant and affine objectives
are included; an affine slope is retained by the gradient rows.

The equality right-hand side may be irrational. Neither its exact
encoding nor an expanded optimizer representation is needed. Clearing
the rational matrix denominators has polynomial bit cost because there
are polynomially many entries, each of polynomial bit length.

## Uniform Hoffman bound and its explicit constant

The projection proof extends correctly from a box to a general rational
polytope. After choosing independent equality rows, conic elimination
modulo their span leaves active inequality normals independent of those
rows and of each other. There are at most `n` rows altogether. Their
integer Gram matrix has determinant at least one and eigenvalues at
most `(nC)^2`, giving the stated inverse singular-value bound.

The sign of the active-inequality contribution is correct: the projected
point lies on each active boundary, while the original point is feasible,
so its displacement has nonpositive inner product with each outward
normal. The remaining equality term is bounded by the full equality
residual. The constant is independent of the equality right-hand side.
Redundant rows, universally tight inequalities, and lower-dimensional
target slices do not invalidate this argument.

The replacement of `sqrt(N)` by `N` in stacking the row residuals is
conservative. Consequently equation (15) gives a valid computable
`Gamma>=1`. Integer powers in that expression have polynomial exponent
and polynomial-bit bases, so `log Gamma=poly_D(I)`. Numerical small
curvature and unknown algebraic heights do not enter the algorithm.
Ambient global convexity permits this proof even when `P` itself is
lower-dimensional; no ambient Hessian-positivity assumption is inferred
from relative convexity.

## Value precision and the fixed minimum-norm selector

A certified value gap of `(epsilon/Gamma)^D` is at most one and gives
the requested distance to `S`. Its bit precision is polynomial in
`I+q` at fixed degree. The linked
[convex polytope value interface](convex-polytope-value-interface.md)
supplies exact rational feasibility as required.

The minimum-norm schedule also checks. Comparison with the minimum-norm
optimizer bounds both the regularized minimizer's norm and its original
objective gap. If its distance to `S` is `e`, the two inequalities in
equation (17) follow from the error bound and projection optimality of
the minimum-norm point. The chosen `tau` gives
`e<=epsilon^2/(8R_x)` and hence bias at most `epsilon/2`.
Moreover `tau R_x^2<=1` for every `D>=2`, so the small-gap hypothesis
used along the way is valid.

The objective with the original norm penalty has strong-convexity
modulus `2tau`, including when it is minimized over a lower-dimensional
polytope. Its value tolerance `eta=tau epsilon^2/4` gives the remaining
`epsilon/2` distance. All coefficient and precision lengths are
polynomial. Preserving the original norm preserves the stated selector.
The simultaneous objective-gap argument correctly uses a finer point
tolerance and an independent certified global value enclosure.

## Core completion with an unknown irrational tilt

The final Section 7 explicitly assumes `k>=1` for its formulas and sends
`k=0` to the deterministic theorem. Its input length charges `alpha`,
`sigma`, completion data, and verification data. These resolve the two
scope clarifications raised during this review.

Taking `beta=alpha+1` gives a strictly positive core penalty while
leaving the core-search parameter unchanged. On every draw,

```text
T_a=F_c+(beta/2)||v-a||^2 >= min_P F_c,
argmin_P T_a = S_a.
```

The fiber is therefore nonempty, compact and convex, and its minimum-norm
point is a fixed well-defined selector. Global convexity of `G` proves
global convexity of `T_a` despite its possibly irrational linear tilt.

Sections 2--3 use only coefficient magnitude bounds, not rationality,
until the sampled-gradient matrix is formed. Majorizing each unknown
linear coefficient by `beta+sigma` and the constant by `beta k/2`
therefore supplies uniform rational bounds. The sampled rows of
`grad G`, together with the core extraction rows, are rational and
independent of both the selected core and the sampled tilt.

The gap controls the core residual by `sqrt(2Delta/beta)`. The unknown
tilt contribution is consequently bounded by a known constant times
`sqrt(Delta)<=Delta^(1/D)`. The stacked rational rows satisfy the same
effective residual estimate. Their zero slice is exactly `S_a`: core
equality cancels the tilt, and the remaining sampled-gradient equalities
force global invariance of `G`. The Hoffman matrix thus has no unknown
irrational coefficient height. Its bound is uniform over all cores and
all draws in the noise support, including ties.

For the rational surrogate, omitting the irrelevant constant from
`T_a`, its uniform difference from the exact-core objective is at most
`beta sqrt(k)||b-a||`. The saved tolerance gives

```text
eta + 2 beta sqrt(k)||b-a||
 <= tau epsilon^2/8 + tau epsilon^2/(16sqrt(k))
 <= tau epsilon^2/4.
```

Strong convexity and the same bias calculation prove full distance
`epsilon` to the fixed minimum-norm point in the selected fiber.

The requested core precision has `poly_D(I)+O_D(q)` bits. As in the
reviewed [cubic completion](cubic-core-full-point-oracle.md), the ordinary
completion consumes a short dyadic core vector. Exact fallback refines
the selected core to that precision within its inherited budget; an
expanded rare algebraic record is not silently treated as a short input.
All remaining solves are polynomial in those short data. The common
random work factor, fixed finite law, and fixed core selector are
therefore inherited without a new event or resampling. The `alpha=0`
ordinary-polynomial specialization follows from the linked jointly
convex selected-core oracle.

## Review boundary and checks

The reviewer read the complete actual theorem, its final Section 7
clarifications, the linked value interface, the reviewed core interface,
and the existing short-output cubic completion. No new source search
or additional mathematical direction was undertaken. No numerical
fixture was needed or run for this review; the checks above are direct
inequality and bit-bound verifications.

Scoped document checks passed forbidden control characters, trailing
whitespace, paired code fences, the final newline, and local-link
existence. A no-index `git diff --check` against `/dev/null` emitted no
whitespace diagnostics; its exit status 1 records the new-file
comparison. No main-file edit, index edit, project-wide verification,
or CI inspection was performed. This completes the assigned review.
