# Second independent audit of facet-curvature-rank precision

Date: 2026-09-05. Verdict: PASS on the full
[facet extension](convex-vector-facet-curvature-rank-precision.md).

I independently checked the new coupled-body steps, constants, rank-zero
case, and rational encoding, using the separately audited box curvature-rank
theorem and dense scalar compiler as stated dependencies. No correction is
required.

Nonnegative facet coefficients make every normalized facet function convex.
Their chord gaps are exactly `A_k g_F/b_k`; thus the projected nonnegative
midpoint error in `K` bounds every selected facet midpoint gap by one.
The original-facet barycentric basis has nonnegative basis gaps, so its
signed coefficient representation still gives the claimed domination.
Refining the exact-basis scalar sum to `1/2` produces at most `8r-1` cells
per parity hull and puts the full vector chord gap in `K/2`.

The half-body band is correctly symmetric. The exact graph belongs because
its displacement from the chord is minus that gap; every admitted error is
the sum of two vectors in `K/2`. It therefore belongs to `K`. This step does
not make the invalid inference that the difference of arbitrary vectors in
`K` remains in `K`.

For the constructive theorem, the approximate basis doubles facet-gap
domination. Scalar tolerance `1/4` gives exact sum chord gap `13/64` and
facet gaps at most `13/32`. The rounded-endpoint vector belongs to `K/16`
because the row-sum bound times the chosen coordinate precision is at most
`1/16` in every normalized facet. Convex interpolation preserves that bound.
Hence the rounded center differs from the graph by a vector in `15K/32`.
The `K/2` band both contains the graph and admits error only in `31K/32`.
All signs and factors have been checked directly.

The linear absolute-value auxiliary formulation projects exactly to the
band: nonnegative `A` makes `A|w-y|<=As` a valid implication, and choosing
`s=|w-y|` gives the converse. These are continuous variables. Rational row
sums, rounding depths, polynomial evaluations, and the new output arithmetic
have polynomial bit length. The same indexed scalar grid and interpolation
weight serve every output, so no extra integer selectors occur.

The partition count `(16r-1)2^p` and scalar factor `486` give
`K_cells<7776r2^p<8192r2^p`, proving `p+13+ceil(log2 r)`.
Compactness of `K` forces a positive coefficient in every column of `A`;
when all facet functions are affine, their nonnegative gap sums can vanish
only if every component gap vanishes. Thus the rank-zero branch is exact.

The weighted-l1 consequence has one nonaffine facet whenever any component
is nonaffine, and therefore has finite overhead three and constructive
overhead thirteen, independent of the output count. Its scope and distinction
from unrelated fixed scalarizations are stated correctly.
