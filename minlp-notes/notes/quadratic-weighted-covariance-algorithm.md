# Computing the finite quadratic precision benchmark: investigation record

Date: 2026-09-05. The candidate was independently reviewed twice and
promoted to [the result file](../results/quadratic-weighted-precision-polynomial-construction.md).

The deterministic polynomial-time construction produces a rational MILP
within additive `O(n log(n+1))` binaries of the integer dimension allowed
by arbitrary convex lifts with unrestricted general integers. It uses
an exact geodesic penalty, a ball of polynomial radius, established
projected subgradient convergence, explicit local rounding budgets,
and [rational exactly orthogonal Jacobi rotations](rational-jacobi-matrix-functions.md).

The [first audit](review-quadratic-weighted-precision-algorithm.md) and
[second audit](review-quadratic-weighted-precision-algorithm-second.md)
passed after correcting component-gradient precision, requiring rational
affine coefficients, and making initialization explicit.
The [novelty note](quadratic-weighted-precision-algorithm-novelty.md)
credits the established numerical and geometric ingredients.
