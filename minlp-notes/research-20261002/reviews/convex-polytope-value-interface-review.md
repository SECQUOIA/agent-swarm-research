# Independent review of the rational-polytope value interface

Date: 2026-10-02. Status: fresh actual-file review passed. No unresolved
correction is requested.

This review covers
[convex-polytope-value-interface.md](../new-direction/convex-polytope-value-interface.md),
including the final version of the rational feasibility repair in
equation (7) and the explicit base-input definition in Section 2.
It checks the interface itself, not the coupled-polytope search or its
expected cell count. No diagnostic solver was run by this reviewer.

## Relative geometry has polynomial encoding length

Maximizing each row's slack correctly distinguishes the universally
tight rows. For every other row there is a rational feasible witness
with positive slack. Averaging those witnesses makes every such row
strict simultaneously. A sufficiently small neighborhood of the average
within the universally tight equation space remains feasible. This
proves that the equations define the full affine hull.

Rational elimination supplies a full-column-rank basis whose selected
free-coordinate rows form the identity. Consequently, in
`x=x_0+B w`, each reduced coordinate is an original free coordinate's
displacement from `x_0`. Its absolute value is bounded by that original
coordinate's supplied bounding-box width. The sum of those widths is
therefore a valid rational Euclidean outer radius.

After substitution, universally tight and other zero coefficient rows
can be removed. Every remaining right-hand side is positive. For a
nonzero row, `b'_i/||A'_i||_1` bounds a Euclidean ball about zero inside
that halfspace. Their minimum is positive and gives equation (4).
There is a remaining row in positive dimension because the polytope
is bounded. Relative dimension zero is correctly handled by direct
evaluation of the rational singleton.

Exact LP witnesses, their average, the basis, and the row ratios all
have polynomial binary length. A small numerical inner radius is not
an inverse-radius iteration factor: its logarithm is controlled by
these lengths. Expanding `phi(x_0+B w)` has polynomial size because
the degree is fixed. Convexity is needed on the reduced polytope, not
on the surrounding coordinate box used for coefficient bounds.

## Weak optimization and rational feasibility repair

The capped epigraph has the claimed inner ball centered at `(0,W+1)`
and outer radius. Linear-domain separation is checked before any
polynomial tangent is used, so the separation oracle respects the
assumption that convexity holds only on the feasible polytope.

The existing
[GLS bit interface](../new-direction/convex-patch-evaluation.md)
supplies the stated weak-optimization contract. Homothety toward the
known inner ball gives equation (6) with
`A_0=1+(2W+1)/r_K`.

For a weak output `(w,t)`, a point `(bar w,bar t)` in the epigraph
is within Euclidean distance `epsilon`. In particular, `bar w`
belongs to the rational feasibility system

```text
y in R,  |y_i-w_i|<=epsilon for every i.
```

Any rational feasible point returned by exact LP then has
`||y-bar w||_infinity<=2epsilon`. No nearest-point optimization or
error-bound constant is required. Since `G` bounds the gradient's
one-norm and both points are feasible, the segment between them gives

```text
psi(y) <= psi(bar w)+2G epsilon <= t+(1+2G)epsilon.
```

This verifies equation (8) without an additional dimension factor.
The resulting value interval and the chosen tolerance prove (1).
All query and output encodings remain polynomial in the rational
input length and the encoding length of the requested tolerance.

## Tangent and dual certificate

For the original representation `Ax<=b`, the minimization dual has the
correct sign:

```text
lambda>=0,  A^T lambda=-g,  lower linear value=-b^T lambda.
```

Indeed these equalities imply `g^T x>=-b^T lambda` on the polytope.
Exact primal-dual equality certifies the tangent LP optimum. Convexity
then gives the global lower value `phi(y)-g^T y+m`. Exact LP dual
certificates have polynomial bit length even when the original
polytope is lower-dimensional.

The tangent-gap conversion also checks. A feasible point with objective
error at most `delta=min(eta/2,eta^2/(8K_0))` satisfies

```text
gap <= delta/t+K_0 t/2,  0<t<=1,
```

along the feasible segment to a tangent-LP minimizer. If `eta<=2K_0`,
the chosen `t=eta/(2K_0)` gives a gap at most `eta/2`. Otherwise
`t=1` gives a gap below `3eta/4`. Thus the stated `eta` bound holds.
Coefficient bounds on the supplied box give a polynomial-bit `K_0`;
the extra requested accuracy has polynomial encoding length.

The final certificate can be checked from rational feasibility,
objective and gradient evaluation, the dual constraints, and the actual
gap. Reproducing the GLS computation is unnecessary.

## Exact fallback and the separation of bit costs

The final text explicitly defines `I` from the base polytope, its
bounding box, `F_0`, and the selected core indices, excluding sampled
coefficients and requested precision. This resolves the only notation
clarification identified during the review.

Replacing the box predicate in
[the canonical scalar fallback](../new-direction/polynomial-exact-fallback.md)
by `Ax<=b` preserves the two quantified blocks and one free scalar.
The atom count and degree are base-only. Compactness supplies one
canonical lexicographic optimizer even with a positive-dimensional
optimal set. The separately encoded coordinates therefore refer to
one common point. The reviewed coefficient-height bound and univariate
extraction keep the cost in the form

```text
B_0 (I+b_c+q+1)^c_d,  log B_0=poly_d(I),
```

with a fixed exponent on sampled height and precision. Lower-dimensional
domains do not add quantifier blocks or invalidate selection.

Rounding an algebraic optimizer does not preserve coupled constraints,
and the text correctly repairs it. If `w` approximates `x*` in infinity
norm to `epsilon`, the rational set
`Q intersect [w-epsilon,w+epsilon]` is nonempty because it contains
`x*`. Any rational LP solution `y` is within `2epsilon` of `x*`.
The gradient one-norm bound gives objective error at most
`2G_0 epsilon`. With `epsilon=2^(-q)/(4G_0)` and a value enclosure of
width `2^(-q)/2`, the feasible objective-gap contract follows.

The logarithm of `G_0` is polynomial in the base and sampled coefficient
lengths. LP work polynomial in possibly exponential algebraic-record
lengths merely enlarges the base exponential factor and the fixed
polynomial exponent. It does not introduce a coefficient-height
exponent depending on dimension or on requested accuracy.

## Verification performed

The reviewer read the complete actual interface and reread the revised
feasibility repair and base-input definition. A scoped document check
passed local-link existence, paired code fences, trailing whitespace,
and the final newline for this review. No numerical diagnostic,
external search, new agent, main-file edit, index edit, project-wide
verification, or CI inspection was performed.
