# Second independent review: weighted quadratic covariance precision

Date: 2026-09-05. Reviewer: `potential_flow_review`.

Reviewed candidate: [quadratic-weighted-covariance-precision.md](quadratic-weighted-covariance-precision.md), including the later geodesic-convexity observation.

**Verdict: PASS after the formulation-size notation correction, which the author applied.** The finite determinant characterization, its dimension-only constants, and the binary upper construction are correct for all positive component tolerances. The fourth-moment and volume arguments were independently derived. No novelty or efficient matrix-optimization claim is certified.

## Determinant problem

The optimization is over real symmetric matrices in `0<=P<=I`. For positive semidefinite `P` and symmetric `H`,

```
tr(H P H P)=||P^(1/2) H P^(1/2)||_F^2>=0.
```

The feasible set is compact. A sufficiently small positive scalar multiple of the identity satisfies every energy inequality because all tolerances are strictly positive and there are finitely many Hessians. Thus the maximum determinant is positive, every determinant maximizer is positive definite, and the eigenvalues used by the upper construction belong to `(0,1]`. Zero Hessians cause no exception.

## Parity classes and the moment identity

Collect all graph inputs admitting at least one feasible lift of each parity. Any two lifts with the same parity have an integer midpoint, so the componentwise graph-error condition gives

```
|(1/2)(x-y)^T H_j(x-y)|<=4epsilon_j.
```

This holds independently for every Hessian. Closing the classes within the compact cube preserves the inequalities and the cover; no closedness or measurability of the original lifted set is used.

For a positive-volume closed class, its uniform distribution has positive definite covariance: a zero variance in a nonzero direction would place it almost everywhere in a hyperplane, contradicting positive ambient volume. Center this distribution and take independent copies `X,Y`. Put `A=X^T H X`, `B=Y^T H Y`, and `C=X^T H Y`. Expanding one quarter of `(A+B-2C)^2` gives

```
(1/2)E[A^2]+(1/2)(E[A])^2+E[C^2].
```

The terms `E[AC]` and `E[BC]` vanish by independence and zero means. Direct covariance multiplication gives `E[C^2]=tr(H Sigma H Sigma)`. This proves the displayed fourth-moment identity, including all coefficients. Each term is nonnegative, even for an indefinite Hessian. The pairwise bound therefore implies energy at most `16epsilon_j^2`.

The cube range of `v^T X` has width `||v||_1<=sqrt(n)` for every unit vector, so the elementary interval variance bound yields `Sigma<=(n/4)I`. With `c_n=max(4,n/4)`, the scaled matrix `P=Sigma/c_n` respects both the matrix cap and every energy inequality, since energy scales quadratically in that scalar. Hence `det Sigma<=c_n^n D`. No simultaneous-diagonalization or positive-curvature assumption appears in this argument.

## Volume-covariance inequality and lower constant

Whitening the centered class makes its covariance the identity and transforms its volume to `vol(S)/sqrt(det Sigma)`. The whitened distribution has mean squared radius `n`. A centered ball minimizes the radial second-moment integral among sets of equal volume: points outside the equal-volume ball have at least its boundary squared radius, while missing points inside have at most that radius. Comparing the two integrals proves the assertion without assuming convexity of the class.

A radius-`R` ball has average squared radius `nR^2/(n+2)`. Thus the equal-volume ball for the whitened class has `R<=sqrt(n+2)`, giving

```
vol(S)<=omega_n(n+2)^(n/2)sqrt(det Sigma).
```

Combining with covariance scaling gives class volume at most `2^A_n sqrt(D)` with exactly the stated `A_n`. Zero-volume classes satisfy the same bound. There are at most `2^p` classes and their union covers the unit-volume cube, so

```
1<=2^p 2^A_n sqrt(D),
p>=Phi-A_n.
```

Adding the trivial nonnegative lower bound proves the left side of the theorem. This controls unrestricted general integer coordinates, not just binaries, and its constants do not depend on the Hessians, number of outputs, or relative tolerances.

## Rotated grid and exact prefix products

A determinant-maximizing covariance has a real orthogonal eigendecomposition. The width of the rotated cube in coordinate `i` is the one-norm of column `i` of the rotation. It lies between one and `sqrt(n)`, since that column has Euclidean norm one. Translation changes only the affine parts of the output quadratics. Retaining the original cube's linear inequalities ensures the formulation still uses the intended input domain despite constructing on a larger rotated bounding box.

The depth `L_i` is nonnegative and its residual width satisfies `h_i<=sqrt(lambda_i/n)`. The dyadic prefix and residual cover the entire interval, including the last endpoint. For every actual feasible assignment, the identity

```
y_i y_k=A_i y_k+rho_i A_k+rho_i rho_k
```

is exact. Both prefix terms are sums of products of an existing binary and a bounded continuous variable. The standard four linear inequalities enforce each such product exactly, without new binary variables. This also works for squares: the two prefix terms sum to `A_i^2+2A_i rho_i`.

The residual bilinear McCormick envelope has maximum absolute graph error `h_i h_k/4`. For a residual square, the proposed lower tangents at zero and `h_i`, together with the endpoint secant, have maximum absolute error `h_i^2/4`; the lower and upper errors both attain this at the midpoint. Consequently the monomial error claims are valid in both cases.

Sharing one approximated value per unordered monomial across outputs preserves the simultaneous graph: setting every residual value to its exact product is jointly feasible. The error proof does not require other residual-product consistency equations, because it bounds every admitted monomial error separately before summing.

## Componentwise accuracy and integer count

The factor one half in the quadratic definition and the monomial error one quarter give the factor one eighth in the output error. Off-diagonal monomials appear twice in the displayed full matrix sum, exactly matching their usual coefficient in the quadratic polynomial. Thus

```
error_j <= (1/8)sum_(i,k)|G_(j,ik)|h_i h_k.
```

The residual width bounds contribute `1/n`. The entrywise absolute sum of an `n` by `n` matrix is at most `n` times its Frobenius norm by Cauchy–Schwarz. The two factors cancel, leaving

```
error_j <= (1/8)sqrt(tr(H_j P H_j P))<=epsilon_j/8.
```

The intentional error margin is therefore real, not a missing coefficient. This argument works independently for every output, so no factor depending on `m` enters the tolerance or integer count.

Summing the ceilings gives

```
p_grid<=-(1/2)sum log2(lambda_i)
        +sum log2(w_i)+(n/2)log2(n)+n
       <=Phi+n log2(n)+n.
```

Every binary linear formulation is also a convex integer formulation. Therefore `p_conv<=p_bin<=p_grid<=Phi+B_n`, proving the right side of the theorem. Normalizing another full-dimensional box by an invertible diagonal affine map changes the Hessians as stated and preserves the reasoning.

## Formulation-size correction

The direct construction count is

```
O(n p_grid+n^2+mn^2),
```

because every coordinate bit is used in at most a constant times `n` exact products; residual monomials and output equations account for the remaining terms. The original draft instead put the **minimum** `p_bin` in this row-count expression. That was not justified by the construction. Only `p_grid<=p_bin+O(n log(n+1))` follows from the two precision bounds, so expressing size in terms of the minimum would introduce an additional `O(n^2 log(n+1))` term.

Both independent reviewers flagged this distinction. The author corrected the statement to use `p_grid` and explicitly bound it by `Phi+B_n`. The main integer-dimension inequality was never affected. Arbitrary real coefficients and eigenspaces remain allowed; no rational encoding or computation guarantee is implied.

## Weighted graph specialization

For an ordinary edge `(i,k)` with distinct endpoints, direct multiplication of its two-entry Hessian gives

```
tr(H_(ik)P H_(ik)P)=2(P_ii P_kk+P_ik^2).
```

Replacing a feasible matrix by its diagonal keeps entries in `[0,1]`, hence preserves the matrix cap, and removes the nonnegative square term from every edge energy. Hadamard's inequality gives no smaller determinant. A diagonal maximizer consequently exists.

At such a maximizer all diagonal entries are positive. Substituting `P_ii=2^(-2s_i)` gives objective `Phi=sum s_i` and constraints

```
s_i>=0,
s_i+s_k>=log2(sqrt(2)/epsilon_(ik)).
```

The factor `sqrt(2)`, inequality direction, and objective scaling are correct. Negative right-hand sides are redundant. No diagonal restriction is justified by this argument for arbitrary quadratic systems.

## Geodesic-convexity addition

For `P(t)=P_0^(1/2)exp(tA)P_0^(1/2)`, cyclic invariance of trace and diagonalization of the symmetric `A` give exactly

```
tr(H_j P(t)H_j P(t))
=sum_(i,k)C_(j,ik)^2 exp(t(a_i+a_k)).
```

Symmetry of `C_j` is essential for the coefficients to be squares and is satisfied here. Each summand is convex in `t`. For a nonzero Hessian at least one coefficient is positive, so the energy's logarithm is the usual convex log-sum-exp. The log determinant is affine in `t`.

For the geodesic between two feasible matrices, scalar weighted arithmetic–geometric mean applied by spectral calculus and congruence gives `P(t)<=(1-t)P_0+tP_1<=I`. Both the cap and energy sublevel constraints are therefore geodesically convex. A local determinant maximizer within the positive definite feasible set must be global: a geodesic to any better point would provide arbitrarily close feasible points with strictly larger log determinant. The candidate carefully restricts this statement to the positive definite feasible set.

This is compatible with failure of ordinary Euclidean convexity, illustrated correctly by the energy `2ab` on positive diagonal matrices for an off-diagonal Hessian. It supplies no iteration, conditioning, or rational bit-complexity bound on finding the optimum.

The stated operator-norm comparison is also valid. If `D_op` is the analogous determinant optimum with operator norms, then

```
n^(-n/2) D_op<=D<=D_op,
```

because scaling an operator-feasible covariance by `1/sqrt(n)` makes it Frobenius-feasible while preserving the cap. Hence the induced precision quantities differ by at most `(n/4)log2(n)`.

## Verification scope

This second review independently checked the general algebra and constants before reading the author's computational results. The reported finite checks are consistent with the proof, but neither they nor this review establish novelty. The finite covariance characterization is valid independently of the previously reviewed noncommutative-rank theorem; no rank machinery was imported into its proof.
