# Independent audit: block PSD precision with unconditional error bodies

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the block PSD unconditional extension](block-psd-unconditional-error-precision.md) and [the direct rational block log-determinant oracle](rational-block-logdet-convex-body-oracle.md). The finite constants, exact feasible allocation, polynomial bit model, and intrinsic block-rank overhead are correct. No correction was needed.

## Expected Jensen vector and the whole error body

The quadratic Jensen vector is `J_j=(1/8)sum_b Delta x_b^T H_jb Delta x_b`. It is nonnegative because each Hessian block is positive semidefinite. Its expectation under independent uniform support points is `sum_b tr(H_jb Sigma_bb)/4`. Closure of parity supports preserves membership in the closed body, and convexity places the expected vector in that body.

For `P_b=Sigma_bb/c_b` with `c_b=max(4,d_b/4)`, the block caps hold. Every trace is nonnegative, so `0<=E(P)<=EJ` coordinatewise even though the scaling factors differ among blocks. Unconditionality then gives `E(P) in K`. This proves that the block determinant and volume lower bound retain exactly the original finite constant.

The reviewed grid gives simultaneous coordinatewise error at most `E(P)/8`. Hence unconditionality controls the full admitted error vector. The shared residual construction contains the exact graph and requires no linear description of the curved output body. After rational spectral rounding, `P_tilde_b<=P_b/2` makes `0<=E(P_tilde)<=E(P)`, so the same argument preserves exact budget feasibility. Its determinant cost is only a factor `8^N`.

## Direct log-determinant oracle: coordinate factors and compactness

The independent-coordinate representation counts each upper off-diagonal entry once. Consequently matrix Frobenius norm is at most `sqrt(2)` times coordinate Euclidean norm, and trace maps and log-determinant gradients have the stated factor two on off-diagonal coefficients. These factors are used consistently throughout the oracle proof.

The signed linear map in the general oracle need not preserve positivity. The small common covariance is nevertheless feasible because its image lies in the supplied inner ball of `K`. It gives `D>=delta^N>0`. Feasible covariances lie in the compact semidefinite cap, and the preimage of closed `K` is closed. Thus the determinant maximum is attained and positive. Since all eigenvalues are at most one, every eigenvalue at a maximizer is at least `delta^N`. Imposing the lower spectral cap `a=delta^N/4` excludes no maximizer.

The log-determinant hypograph is convex: the second derivative in a symmetric direction is `-tr(P^{-1} A P^{-1} A)<=0` for each block. The spectral caps and the last-coordinate bounds make it compact and full-dimensional once the displayed inner ball is verified. Its optimum last coordinate is exactly `log D`.

## Inner and outer ball constants

I checked each margin in independent-coordinate Euclidean norm. A displacement at most `sigma` changes every block in operator norm by at most `2sigma`. Because `sigma<=delta/(32N)`, the spectrum around `P_0=(delta/2)I` stays above `delta/4` and below one. Since `a<=delta/4`, both spectral caps hold.

The center's image has norm at most `rho_0/8`, using `delta N c<=rho_0/4`; its displacement has norm at most `c sigma<=rho_0/8`. Thus it remains strictly inside the known ball of `K`.

The independent-coordinate gradient norm is bounded by `sqrt(2)||P^{-1}||_F<=4sqrt(2N)/delta<=8N/delta` throughout this ball. Its variation in objective is therefore at most one quarter. At the center, the objective is `-N(b+1)ln2>=t_0+2`; perturbing the last coordinate costs at most another one quarter. The lower last-coordinate margin is `t_0+B_0=Nb(N-1)+N+2>=3`. This proves the full closed inner ball inclusion.

All independent matrix entries under the spectral caps have absolute value at most one, and the last coordinate lies in `[-B_0,0]`. The proposed outer radius `2(B_0+q+1)` about the center is conservative. All centers, radii, and spectral bounds have polynomial rational encoding, including potentially exponentially small lower bounds.

## Weak separator and exact rational repair

The last-coordinate bounds give exact linear separators. Rational symmetric elimination supplies negative quadratic-form witnesses for either failed semidefinite cap, with polynomial encoding as in the previously audited correlation oracle. Pullback of a violated body inequality cannot have zero normal because the map is linear and the body contains zero.

After these tests, every block is rational positive definite with the known lower spectral cap. Determinants and inverse entries are exact rationals of polynomial encoding. Scalar logarithm approximations produce an interval of the requested total accuracy for the sum of log determinants. The upper endpoint plus the exact rational matrix-inverse tangent is a globally valid affine upper bound by concavity. Its last-coordinate coefficient equals one, satisfying the cited normal normalization convention.

When the tangent test does not separate, lowering only the last coordinate by at most the requested tolerance reaches the hypograph. This does not violate its lower bound because `g(P)>=N log a=-N(Nb+2)ln2>-B_0`. The oracle therefore meets exactly the already checked GLS weak-separation interface, with explicit inner and outer radii.

The classical weak optimizer returns a rational point within distance `rho` of the body and objective at least `log D-rho`. Its convex combination with the inner-ball center, with weights specified in the note, is exactly feasible by the same central-ball argument as the scalar oracle. The loss is at most `rho+(rho/sigma)B_0`, which is less than `nu/4` for the chosen `rho` and therefore satisfies the asserted `nu` guarantee. Matrix reconstruction from the repaired independent coordinates is linear and rational, so the returned blocks are exactly feasible and positive definite.

The least determinant logarithm is bounded by a polynomial in `N,b`, and matrix inverse entries have polynomial bit length by rational determinant bounds. All GLS query lengths, scalar logarithm accuracies, matrix operations, and exact repair operations therefore remain polynomial in the full input and accuracy encoding. The body dimension `q+1` may grow; the imported convex optimization theorem is polynomial in this dimension and does not require it fixed. No matrix-function or real-arithmetic eigensolver assumption enters this allocation routine.

## Intrinsic block ranks and final overhead

The previously reviewed blockwise common-kernel quotient acts only on input coordinates and preserves PSD Hessian blocks by congruence. The affine output adjustment leaves the error body unchanged; no output mixing that could destroy unconditionality is performed. The quotient domain is a product of zonotopes with exact rational linear lifts. Separate rational normalization gives the same individual rank-dependent volume losses as the block PSD theorem.

Using `nu=1` gives constant log-determinant loss in allocation. Rational block spectral rounding costs `O(N)` binaries, and all other finite and domain-volume terms are `O(sum_b r_b log(r_b+1))` after quotienting. Thus the stated universal additive guarantee follows, including linear overhead for bounded nonzero block rank. Output count and radius encoding affect runtime and continuous formulation size but not the additive integer-count bound.

This audit certifies the mathematical deductions and bit-complexity interface. Novelty assessment remains separate; the note correctly attributes the underlying log-determinant and weak-optimization methods as established tools.
