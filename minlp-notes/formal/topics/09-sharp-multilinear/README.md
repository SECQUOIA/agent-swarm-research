This package verifies the sharp leading asymptotics of the worst termwise to
convex-hull gap ratio for positive multilinear polynomials on all finite
nonnegative boxes. The endpoint theorem `sharp_positive_growth` in
[`SharpAsymptotics.lean`](../../Formal/MultilinearGap/SharpAsymptotics.lean)
proves

```
R(d) / (ln d / ln ln d) → 1,
C(n) / (ln n / ln ln n) → 1.
```

R(d) is the supremum over polynomials of degree at most d in any finite
dimension. C(n) is the supremum over polynomials in exactly n coordinates.
Both range over finite boxes with 0 ≤ lower endpoint ≤ upper endpoint in
each coordinate, all points of those boxes, and nonnegative coefficients on
squarefree supports. Zero coefficients, constant and affine terms, unused
coordinates, and boundary points are allowed.
Ratios require a strictly positive hull gap. The gap definitions use the
original continuous graph hull and the original individual terms of the
polynomial.

The lower witnesses use the existing coefficient-one dyadic family with
L = floor(log₂ n)−1 levels. For every n ≥ 8 these witnesses fit both the
degree and dimension allowances, and the estimate H_L ≤ log₂ L+3 gives a
normalized lower bound tending to one. Padding with unused coordinates
preserves both gaps and gives exactly n coordinates. This argument covers
every sufficiently large integer allowance and does not depend on the
[exact finite hull formula](../08-exact-multilinear/README.md).

The upper bound constructs a single feasible probability law for all terms.
It mixes independent rounding, a reversed threshold law, and a harmonic law,
and proves that each term receives enough deficiency from at least one
component. The harmonic estimate uses the elementary bound z/(1+z) for an
independent union probability. With b = ln Λ, this gives the factor
1/(1+1/b²), which tends to one and preserves the sharp leading constant.
The resulting explicit bound is `sharpZ (sharpLambda d)`, where

```
Λ = max(exp 6, 1+ln d),
A = Λ/(ln Λ)²,
h = (1−1/ln Λ)/(1+1/(ln Λ)²) · (ln Λ−3 ln ln Λ)/Λ,
Z = 1/h + A + 2/(1−exp(−1)).
```

Affine substitution transfers the cube upper bound to every finite
nonnegative box, including boxes with fixed coordinates. The proof preserves
the full graph-hull gap and bounds the original termwise gap by the
termwise gap after expansion. Nonnegative expansion coefficients and degree
preservation then give the bound for the original polynomial on its box.

The [coverage table](COVERAGE.md) describes the eighteen modules and the
scope of the result. The analytic sources are the
[sharp-growth note](../../../results/positive-multilinear-sharp-degree-growth.md),
[lower-construction note](../../../results/positive-multilinear-gap.md), and
[manuscript](../../../paper-relaxation-limits/sections/02-universal-positive.tex).
The formal result proves the sharp leading term; it does not claim an
optimized fixed-point formula, a Lambert W formula, or a second-order term.

A next formalization target is the
[optimized finite upper-bound note](../../../results/positive-multilinear-second-order-upper.md):
first its fixed-point characterization and optimal mixture for the stated
scalar guarantees, then its Lambert W certificate and second-order upper
bound. That note does not claim a matching second-order lower bound.

To reproduce the endpoint build, run from `formal/` with the pinned Elan
toolchain on PATH:

```bash
lake build --wfail Formal.MultilinearGap.SharpAsymptotics
```

The [verification record](VERIFICATION.md) gives the project audit and kernel
replay commands, their scope, and their recorded results.
