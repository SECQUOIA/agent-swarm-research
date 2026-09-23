This package covers the mathematical results in the focused
[exact-count note](../../../results/convex-polynomial-box-error-exact-integer-gap.md).
It is not a verification of the entire integer-dimension manuscript.

For every natural dimension n, the polynomial graph with component pairs
`((7/4)(1-x_i)^32, (7/4)x_i^32)` has minimum integer count n and minimum binary
count `ceil(n log₂ 3)` at unit componentwise error. Both minima have rational
linear realizations, and requiring closed lifts leaves the minima unchanged.

The completion also covers the monotone variant obtained by adding `56 x_i`
to the first output. Both outputs are convex and nondecreasing on `[0,1]`, their
polynomials have degree 32, and the same counts hold for arbitrary convex,
closed convex, and rational linear lifts. The integer construction retains
three auxiliary weights and thirteen inequalities per input coordinate.
Monotonicity does not imply positive coefficients: the modified polynomial's
coefficient of degree three is exactly `-8680`.

| Location | Content |
|---|---|
| [`ExactBoxCounts.lean`](../../Formal/ExactBoxCounts.lean) | Original exact minima and strict count separation |
| [`AffineShear.lean`](../../Formal/AffineShear.lean) | Invertible shear, exact graph/error contract, all six lift classes, rational row substitution and size preservation |
| [`MonotonePolynomial.lean`](../../Formal/MonotonePolynomial.lean) | Derivative, monotonicity, convexity, polynomial degree and negative coefficient |
| [`ExactCountConsequences.lean`](../../Formal/ExactCountConsequences.lean) | Combined monotone theorem, one-input case, exact gap and linear growth bounds |
| [`StrictError.lean`](../../Formal/StrictError.lean) | Strict error below one for the boxes and every admitted integer slice |
| [`FixedData.lean`](../../Formal/FixedData.lean) | A single finite rational coefficient alphabet for every dimension |
| [`BoxHull.lean`](../../Formal/BoxHull.lean) | Connection from weighted-box constraints to actual labeled convex hulls |

The [coverage table](../../COVERAGE.md) records the exact mathematical scope.
The [verification record](VERIFICATION.md) records completed checks. No paper
or result-note text was changed as part of this completion.

All files share the project's pinned Lean and Mathlib environment. From
`formal/`, run `bash scripts/verify.sh` to verify the entire project, or check
this package's recorded fingerprints with:

```bash
sha256sum -c topics/00-exact-counts/verification/SHA256SUMS
```
