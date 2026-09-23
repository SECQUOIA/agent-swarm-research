# Independent audit: block PSD quadratic integer precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the block PSD precision candidate](block-psd-quadratic-precision.md), including the complete product-cone algorithm reuse and the common-kernel quotient. The finite constants and polynomial rational guarantee hold as stated. The intrinsic overhead is `O(sum_b r_b log(r_b+1))`, with a universal constant. No correction was needed.

## Finite lower bound

For a same-parity support, positivity of each block-diagonal output Hessian turns midpoint error into the nonnegative pairwise quadratic bound. Averaging gives `sum_b tr(H_jb Sigma_bb)<=4 epsilon_j`, with the same factor as in the previously audited diagonal PSD theorem. The projected range of a unit vector in the original `d_b`-cube is at most `sqrt(d_b)`, so its variance is at most `d_b/4`. Thus `Sigma_bb/c_b` respects the cap for `c_b=max(4,d_b/4)`.

Each trace term is nonnegative, so scaling blocks by different constants at least four preserves the aggregate trace constraint. This step would fail without the positive semidefinite assumption. The block determinant inequality `det Sigma<=product_b det Sigma_bb` follows by Schur complements, with continuity covering singular covariance matrices. Combining it with the volume-covariance estimate gives exactly the displayed constant `A`.

The parity-support closure convention from the general theorem remains valid because all pairwise inequalities are continuous. The global Gaussian volume factor has logarithm `O(N)`. Since every retained block has positive dimension, this is bounded by a universal multiple of `sum_b d_b log(d_b+1)`; it introduces no extra `N log N` term.

## Block grid upper bound

An orthogonal basis change within a block gives each coordinate a width at most `sqrt(d_b)`. With residual widths at most `sqrt(lambda_i/d_b)`, every normalized residual-error entry is bounded by `1/(4d_b)`. Its Frobenius norm, and therefore its operator norm, is at most one quarter.

The normalized Hessian remains positive semidefinite by congruence. The inequality `|tr(MZ)|<=tr(M)||Z||` for positive semidefinite `M` gives error at most `tr(H_jb P_b)/8` from each block. Summing block errors proves the stated output bound. Hessians need not commute; only the covariance block is diagonalized. Shared residual products across outputs and exact prefix products supply the same graph inclusion as the previously reviewed quadratic construction.

The sum of depth bounds is precisely at most `Phi+N+sum_b d_b log2 d_b`. The construction acts within the original disjoint coordinate blocks, so there are no omitted cross-block quadratic terms.

## Full finite-bit algorithm reuse

The product of positive definite block cones is a totally geodesic submanifold of the full positive definite cone under the same affine-invariant metric. Its distance, exponential, logarithm, and identity-centered radial projection are the restrictions of the full-matrix operations. Therefore the previously audited curvature bound and inexact projected-subgradient recurrence apply.

The energy here is linear rather than quadratic in covariance. The candidate correctly uses `log(E_j/epsilon_j)`, without the half-log factor. Along every block geodesic, positive semidefiniteness makes it a sum of exponentials with nonnegative coefficients. Its normalized tangent-gradient blocks are positive semidefinite and have total trace one, giving joint Frobenius norm at most one. The negative log determinant contributes norm `sqrt(N)`, so the same `2N` global Lipschitz bound is valid.

Common scaling by `exp(-h)` enforces every cap and trace constraint and has repaired negative log determinant exactly `F`. A feasible common dyadic covariance yields optimal determinant at least `delta^N`, hence a polynomial metric-radius bound. On the iterate ball, `E_j(P)>=lambda_min(P)E_j(I)` supplies the required polynomial-bit conditioning. Zero energies are omitted; for these PSD blocks, zero trace at the identity means every matrix in that output row vanishes.

The previously checked approximate branch-selection, tangent-error allocation, metric rounding, and upper repair factor carry over with `N` as dimension. Matrix-function and rounding routines can be applied blockwise so the prescribed zero off-block entries remain exact. The cap branch chooses a maximal eigenvalue from one block; ties require no eigengap. The trace values themselves are exact rational expressions on rational iterates, and the normalized gradients have the stated conditioning.

The rational spectral residual procedure is applied to each block. The sandwich between one eighth and one half of its feasible covariance preserves all trace constraints by positivity. The product determinant loses at most `8^N`, and its exactly orthogonal rational block bases retain the same width bounds. The additional binary count is therefore `O(N)`, while the operations, output rows, and coefficient encodings stay polynomial. This checks the actual bit proof rather than relying on a real-arithmetic optimization assertion.

## Intrinsic common block ranks

I also read the referenced input-rank quotient and normalization argument. In each original block, a rational basis of the common Hessian row space gives a rational right inverse and Hessian congruences that preserve positive semidefiniteness. Affine output subtraction and exact projection preserve both formulation minima, even if the affine output varies along fibers. The reverse formulation retains the original cube variables and the affine input/output equations.

Because the original blocks have disjoint input coordinates, the quotient domain is a product of centered zonotopes. Their rational LP separation and known-radius construction feed the already reviewed strong-oracle ellipsoid rounding. Rational LDL normalization avoids irrational coordinate coefficients. For a nonzero rank `r_b`, the resulting normalized factor lies in its unit cube and contains a cube of side `1/[2r_b(r_b+1)]`. Thus its volume is at least the displayed lower bound.

The transformed Hessians are still block diagonal PSD. Applying the cube upper construction and then imposing the exact zonotope lift gives a valid original formulation. In the lower bound, supports cover the product domain's volume; the sole additional term is `-log2 vol(Omega)`, bounded by the sum of the individual block volume losses. Every remaining term uses the reduced block sizes. This proves the intrinsic guarantee and its linear specialization for bounded nonzero block rank, even when ambient block dimensions grow.

The proof requires the common coordinate block partition and positivity. It does not assert that arbitrary low-rank or commuting Hessians automatically admit the same original-coordinate product-domain structure. Novelty assessment is separate from this correctness audit.
