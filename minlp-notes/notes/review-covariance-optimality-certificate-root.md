# Root review of the covariance determinant certificate

Date: 2026-09-05. Verdict: PASS for
[the certificate note](covariance-determinant-optimality-certificates.md).
The author is a separate research agent. This is an internal mathematical
review, not external peer review or a novelty assessment.

I independently derived the bound before reading the completed note, then
checked its full proof. The hypotheses are `0<P<=I`, all energy budgets
satisfied, `mu_j>=0`, and `S>=0`. The slack is nonnegative. The
Lagrangian value at `P` is `-log det P-c`, and its value at an optimal
feasible `P_star` is at most `-log D_star`. Geodesic convexity and the
gradient `P^(1/2) R P^(1/2)` therefore give the stated upper gap bound.

The distance estimate is valid: because both covariances are bounded by
identity and `det P_star>=det P`, their minimum eigenvalues are at least
`det P`. The relative eigenvalues lie between `det P` and its reciprocal.
Thus the affine-invariant distance is at most
`sqrt(n)(-log det P)`. The case `P=I` also causes no exception: feasible
identity already maximizes the determinant and has zero logarithmic term.

The residual square `tr(PRPR)` equals the Frobenius square of the symmetric
isometric gradient and is nonnegative even when `R` is indefinite. It is
rational for rational data. Exact complementarity and stationarity are
sufficient; no constraint qualification or necessity statement is used.
The proposed multiplier optimization is convex for fixed `P`, and the
correlated positive semidefinite budget version has the same proof.

One clarity suggestion: repeat `P<=I` explicitly at the definition of
feasibility, rather than relying on the linked benchmark's definition.
No mathematical correction is required.
