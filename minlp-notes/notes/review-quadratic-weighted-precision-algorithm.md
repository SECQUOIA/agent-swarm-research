# Independent audit: computing the quadratic covariance precision benchmark

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

The candidate is [the weighted covariance algorithm note](quadratic-weighted-covariance-algorithm.md). **PASS.** The complete revised argument, including the [self-contained rational spectral routine](rational-jacobi-matrix-functions.md), passes this independent proof audit. It establishes a deterministic polynomial-time rational construction with binary count at most the unrestricted-integer convex-lift minimum plus `O(n log(n+1))`. This is a complexity result; the conservative iteration bound does not establish practical efficiency.

## Imported geometric result

I read Corollary 8 and the proof of Theorem 9 in [Zhang and Sra, First-order Methods for Geodesically Convex Optimization](https://proceedings.mlr.press/v49/zhang16b.pdf). Corollary 8 applies to the exponential update followed by metric projection. Its distance comparison depends on the distance from the current point to the comparator, so the candidate's stored iterates may lie in the slightly enlarged ball while projecting onto the original ball. The proof of Theorem 9 bounds the arithmetic mean of objective gaps before constructing a geodesic average; selecting a best iterate is therefore valid here.

I also checked Proposition I.1 of [Criscitiello and Boumal](https://arxiv.org/pdf/2008.02252), which gives the sectional-curvature lower bound `-1/2` for the stated affine-invariant positive definite metric. The weaker bound `-1` used in the candidate is valid. Projection is nonexpansive on this Hadamard manifold; the radial formula follows directly from the reverse triangle inequality and the radial geodesic.

## Exact penalty and radius

Let `h=max(0,log lambda_max(P),max_j .5 log(E_j(P)/epsilon_j^2))`, omitting zero Hessians. Scaling by `exp(-h)` enforces both the matrix cap and every energy inequality. Consequently `F=-log det P+n h` equals the negative log determinant of the repaired matrix exactly. Its global minimum is the original constrained optimum, including when every Hessian is zero.

Each energy log is a log-sum-exp along an affine-invariant geodesic. For the cap, each fixed nonzero vector gives a log-sum-exp Rayleigh branch, and their supremum is `log lambda_max`. Thus `h` is geodesically convex. Its component gradients in isometric tangent coordinates are positive semidefinite with trace one, or zero. Their Frobenius norm is at most one. The displayed energy gradient `M_j^2/tr(M_j^2)` is correct. Therefore `F` is globally Lipschitz with constant at most `n+sqrt(n)`.

The rational feasible covariance `2^(-b)I` implies every optimal eigenvalue is at most one and the negative log determinant is at most `nb log 2`. The Euclidean norm of its vector of log eigenvalues is bounded by their absolute sum. Hence `R=1+nb` contains an optimum, with polynomial radius in the binary input length.

## Inexact recurrence and constants

The approximate subgradient inequality has the correct sign. Applying the imported comparison bound to the conceptual exponential update and then nonexpansive projection gives the displayed telescoping inequality. Replacing the projected matrix by a point at metric distance at most `xi` costs at most `(2D xi+xi^2)/(2eta)`, since the projected point and the optimum both belong to the radius-`R` ball.

For `eta=1/(16Z(3n)^2)`, `T>=16D^2/eta`, `e<=1/32`, and `xi<=eta/(128(D+1))`, the initial-distance, curvature, oracle, and rounding terms are respectively at most `1/32`, `1/32`, `1/32`, and `1/64`. Best-iterate selection using objective estimates within `1/64` adds at most `1/32`. The claimed gap below `1/2` is conservative.

A branch selected from estimates within `tau` is a `2tau`-subgradient of the maximum. An additional tangent-gradient error `nu` contributes at most `D nu`. The candidate's choices yield `2n tau+D nu<1/32`. Approximating the cap with a nearly maximal Rayleigh branch adds a further branch error; decreasing `tau` by a constant factor handles it. No eigenvalue gap is required.

## Conditioning and rational repair

Every stored matrix lies in the radius-`R+1` ball, so its eigenvalues lie between `exp(-(R+1))` and `exp(R+1)`. Relative operator error at most `u<=1/2` gives metric error at most `2sqrt(n)u`, proving that polynomially many absolute accuracy bits suffice for the required metric tolerances.

For nonzero rational `H`, `tr(HPHP)>=exp(-2(R+1))||H||_F^2`; this follows from the least singular value of two-sided multiplication by `P^(1/2)`. Hence energy-gradient normalization has only exponentially large conditioning with a polynomial exponent. The exact update has eigenvalues within the same type of bounds because `||eta G||_op<=3n eta`.

A rational upper approximation to the repair factor within relative `exp(1/(4n))` loses at most `1/4` in log determinant and makes feasibility exact. Such an upper approximation can be certified with rational eigenvalue intervals and rational square-root intervals. The resulting rational covariance has log determinant at least `log D_star-1`.

## Rational formulation conversion

The preliminary approximate-basis argument is sound: if rational `Q` and diagonal scales produce `P_hat/8<=P_tilde<=P_hat/2` with `||Q^{-1}||<=2`, then energies remain feasible by their monotonicity in the positive semidefinite order. Specifically the derivative in a positive semidefinite direction `A` is `2tr(H P H A)>=0`. The determinant loss is at most a factor `8^n`.

The coordinate widths are at most `2sqrt(n)`. The residual-grid energy identity holds for every invertible `Q`; orthogonality is unnecessary. The determinant contribution from `Q` is bounded using `||Q||<=3/2`. Thus the extra binary count is `O(n)`, beyond the reviewed `O(n log(n+1))` finite-law gap. Polynomial-bit exact rational orthogonal diagonalization with small residual would simplify this further.

## Elementary spectral checks supplied to the author

For symmetric matrices `A,B` and any scalar `L`-Lipschitz function on their combined spectra,

```
||f(A)-f(B)||_F <= L ||A-B||_F.
```

Indeed diagonalize both matrices conceptually. The squared norms are the sums of `(f(lambda_i)-f(mu_j))^2 |u_i^T v_j|^2` and `(lambda_i-mu_j)^2 |u_i^T v_j|^2`, respectively. This proves the claim term by term. It avoids an invalid inference from scalar Lipschitz continuity to dimension-free operator-norm Lipschitz continuity. Applied in Frobenius norm, it covers every matrix function needed here on the bounded spectral ranges.

For maximum-pivot Jacobi, the exact off-diagonal squared norm changes by `-2b_pq^2+2b'_pq^2`. While that norm exceeds `tau^2`, the maximum pivot has magnitude at least `tau/n`. It is enough to approximate an annihilating rotation so that its new pivot has magnitude at most `tau/(4n)`. This guarantees a uniform contraction until the target is attained. Rational half-angle parametrization gives an exactly orthogonal rational rotation. A common-denominator representation makes the bit-length increase per rotation additive in the rotation's bit length; an unexamined recurrence for individually unreduced fractions would obscure this bound.


## Final read of the rational Jacobi implementation

The author replaced the preliminary approximate-eigenbasis argument by exact rational orthogonal rotations and small spectral residuals. I independently checked every step of the resulting supporting lemma.

For `N=n(n-1)`, the exact maximum-pivot rotation gives squared off-norm at most `(1-2/N)s^2`. Since `sqrt(1-2/N)<=1-1/N`, the stated rational approximation yields off-norm at most `(1-1/N)s+sigma/(4N)`. While `s>sigma`, this is at most `(1-3/(4N))s`. The proposed `ceil(2N log(M/sigma))+1` step bound is conservative, including `n=2`; `n=1` is handled separately. A rational half-angle with fixed polynomial accuracy gives an exactly orthogonal rotation, so there is no reconstruction or orthogonality drift. The common-denominator growth argument is valid for both transformed matrices and accumulated rotations.

The matrix-function estimates in the final lemma are stronger operator-norm bounds than the alternative Frobenius argument above, and they are valid for the functions used. The logarithm follows by the resolvent integral. The square-root difference solves the stated Sylvester equation, whose integral solution gives `1/(2sqrt(a))`. The inverse-difference identity then gives `1/(2a^(3/2))`. Duhamel's identity gives the exponential bound on a fixed operator-norm interval. Scalar bisection, dyadic logarithmic range reduction and its convergent series, and exponential range reduction require only polynomial precision bits on the stated spectral ranges.

The diagonal Rayleigh branch has additive eigenvalue error at most the spectral residual and requires no eigenvector gap. Metric projection can first be applied to the nearby exactly diagonalized matrix: nonexpansiveness controls this substitution, and its remaining scalar formula has denominator at least `R>=1`. Rounding the result to a rational symmetric matrix with the prescribed metric error therefore implements the inexact iteration in polynomial bit time.

In the final grid, set `lambda_tilde_i=B_ii/4` after rational orthogonal diagonalization of the feasible covariance to off-norm at most half its least eigenvalue. The resulting matrix lies between one eighth and one half of that covariance. Orthogonality makes the cube widths at most `sqrt(n)` and its determinant exactly the product of the scales. Thus the displayed final binary count follows with no hidden basis-conditioning loss. All affine coefficients of the requested quadratic map must be rational for the complete formulation to have a rational encoding; the revised scope states this.

The revised oracle paragraph also correctly requests component-gradient accuracy `nu/n`, yielding total tangent accuracy `nu` after multiplication by `n`. Taking the smaller `tau<=1/(256n)` absorbs the extra Rayleigh-branch error. These updates resolve the prior implementation boundary.
