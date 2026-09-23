# Unequal quadratic output accuracies: investigation record

Date: 2026-09-05. The candidate was independently reviewed twice and
promoted to [the result file](../results/quadratic-weighted-covariance-precision.md).
The finite law determines arbitrary convex-lift integer dimension and
compact binary linear precision to additive `O(n log(n+1))` through a
maximum covariance determinant with one constraint per output tolerance.

Both [the first audit](review-quadratic-weighted-covariance-precision.md)
and [the second audit](review-quadratic-weighted-covariance-precision-second.md)
passed after correcting the compact formulation-size statement to use
the constructed binary count `p_grid`, rather than the unknown optimum
`p_bin`. No mathematical error in the finite bounds was found.

The result also proves geodesic convexity of the determinant optimization.
Algorithmic iteration and rational encoding consequences remain separate
work in progress; the result does not yet claim polynomial-time construction.
