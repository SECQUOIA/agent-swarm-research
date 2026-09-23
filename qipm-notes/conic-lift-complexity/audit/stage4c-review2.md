# Stage 4C independent review 2

I personally read all seven new sections, `10a` through `10g`, the Stage 4C author audit, the reduction and selection results in `01-foundations.tex`, and the relevant covering, splitting, and submersion arguments in `08a` and `08e`. I did not consult another reviewer's report, delegate this review, or edit manuscript files.

**Assessment: no major issue found. Three minor precision corrections are recommended.** None changes a conclusion or requires a new mathematical argument.

## Minor corrections

1. **Specify the angle range in the rotating conditioning example.** In `10g-conditioning-counterexamples.tex`, lines 89–106, the stated norms are `k sin(theta)` and a residual with numerator `2(1+tau) sin(theta/2)`, although theta has not yet been restricted. These formulas require an angle range on which both sines are nonnegative. The later applications use small positive angles, so the simplest repair is to introduce the example with `0 < theta < pi` (or, more restrictively, `0 < theta < pi/2`). Alternatively use absolute values in both norm formulas. The signed one-sided derivative and the `cos(theta)` mixed-channel formula should retain their signs.

2. **Make the relative domain of the recourse derivative explicit.** In `10e-projected-compilers.tex`, lines 73–81, smoothness and the KKT derivative are valid on the affine compatibility space when W is rank deficient. Deleting dependent rows does not make the original recourse feasible for arbitrary transverse perturbations of x. The earlier subsection correctly retains compatibility equalities, so this is a local scope clarification: say that x varies in `{x: h_i - Tx in range W}`, and that the displayed derivative is for a tangent direction h, with the same independent-row reduction applied to W and T. Smoothness holds on the relative open subset with a strictly positive feasible recourse vector. For example, with `W=(1,0)^T`, the second right-hand-side coordinate must stay zero; an arbitrary transverse h is not a direction of the recourse map.

3. **State the positive constants in the bit-count consequence.** In `10g-conditioning-counterexamples.tex`, lines 151–154, explicitly assume `C > 0`, `K_0 > 0`, and `q > 0` before dividing by q and taking the logarithm. These are new symbols; the preceding sentence's positive-constant and positive-exponent convention refers to `c_K,c_H,a,b`. With these assumptions the displayed consequence is correct. Under the existing `delta < mu`, finite `H_B`, and positive epsilon assumptions, the earlier inequality itself already forces `K_A > 0`, so that earlier division does not need a separate substantive hypothesis.

## Detailed checks

### Conditioned approximation and global refinements

- Recomputed the sphere stencil: its mixed difference is `-h^2 I - tau^2 11^T`. Four entrywise slack errors give the stated `4 r epsilon` operator bound.
- Checked the cone-wise nonnegativity bounds, including the difference of two numbers in `[0,tau+epsilon]`, the projector singular values in the independent and parallel cases, and the rank-zero treatment of rays and zero base factors.
- The two-term decomposition is valid: retain the projected first factor in the second difference. It gives `V alpha + U beta` without an additional `alpha beta gamma`. Truncating the remaining projector product costs `UV gamma`.
- The finite uniform threshold and the `epsilon^(1/3)` sampling scale have the right constants. The bounded two-point orthant example has exact mixed differences but insufficient relative conditioning, as claimed.
- The finite-radius interpolation formula handles both zero defect and zero second-derivative bound. The smooth slack retains the exact mixed derivative because the support term depends only on the dual variable.
- Minimum-norm primal fibers and minimum-norm attained dual-multiplier fibers are closed, nonempty, convex, and definable after the foundational reduction. Common C2 cells give the claimed local patch without a uniform regularity assertion.
- Recomputed the uniform smooth error using `sum sqrt(delta_i) <= sqrt(k epsilon)`. The separate ray contribution and the lower bound on `L sqrt(H)` are correct.
- In the global splitting argument, `gamma < 1` makes the selected vectors independent. The canonical intersection spaces have constant dimension, and the difference between the two-normal projector product and the intersection projector has norm gamma. This supplies continuous forms, avoiding a pointwise-choice gap. Rank saturation and an invertible sum give the claimed direct-sum images.
- The line-bundle, Adams, and even-dimensional Euler-class consequences are used with the appropriate hypotheses. The fixed-gauge infimum is invariant in the stated sense and does not assert a Newton-conditioning bound.
- Recomputed the rank-one critical-phase identity and both choices of radial derivative. The minimum of the two resulting bounds is valid even though the two critical points may differ. The positive rank-one saturated-channel corollary does not need continuity of the chosen approximants.
- The higher-rank obstruction correctly uses a one-sided derivative. A critical point of the normalized map gives rank at most r minus one, and the remaining rank-one perturbation gives the claimed singular-value bound. Its sphere-submersion exception list agrees with the earlier compact-source argument. The final saturated-profile counting argument correctly guarantees a forbidden target rank.

### Conditioning separations

- Verified the Hessian congruence, exact Schur invariance, and the boosted Lorentz Hessian condition number `lambda^(-4)`. The explicit hyperboloid factors are complementary on the diagonal and have unchanged transverse derivatives at zero.
- Verified the radial example's exact Jordan centrality, bounded Hessian and inverse-Hessian spectra for fixed tau, and the scaling-point eigenvalues. The derivative supremum k is attained where the sphere coordinate is zero.
- Verified the rotating example's constant defect, one-sided derivative, mixed channel, and residual formula, subject to the minor angle qualification above. Both fixed small theta and theta equal to `k^(-1/2)` give the stated separation.
- The changing-right-hand-side identity-equality illustration is explicitly separated from a single lift of a fixed body. The concluding conditioning and bit-count statements remain conditional on an independently proved sensitivity theorem.

### Other new sections

- In `10a`, checked the fixed-product positive-branch cross-ratio construction, whole-product dualization for p greater than two, perspective-cone dual scaling, scalar partial-minimization derivatives, and the distinction between existential parameter bounds and the evaluable barrier. Recomputed the characteristic exponents, derivative asymptotics, univariate necessary scale, strict separation calculation, ansatz failures, and endpoint expansions. No new issue found.
- In `10b`, checked the recession certificate and its product combination, the exponential dual isomorphism, entropy compatibility derivatives, closure with inactive columns, exact product count, and block Hessian factorization. The zero-column repair is necessary and correct. The general results are attributed as specializations, rather than claimed as new barrier theorems.
- In `10d`, checked the lattice proof and output-format restriction, minimum-query contracts, disk-arc obstruction, continuous-summary lower bound, finite translation-space argument, matrix entropy scaling convention, three-cone binomial construction, full graph curvature lower bound for product cosh, and the polyhedral approximation counterexample. No new issue found.
- In `10e`, checked Farkas signs and lineality equations, effective-rank ray enumeration, scalar and matrix quadratic self-concordance proofs, Loewner inflation and objective consequences, the convolution normalization example, reusable boundary interrogation, and the weighted-local-logarithm lower bound. The recourse derivative qualification above is the only issue found in this section.

## Primary-source checks

I independently consulted [Hildebrand's primary preprint](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf), particularly Theorem 5.4 and Section 7, to check the positive branch, logarithmic-homogeneity qualification, and the common scalar lower bound. These support the way `10a` uses the result.

I also consulted [Apers and Gribling's primary manuscript](https://arxiv.org/html/2311.03215v2), especially Theorem 3.1. Its Loewner convention and row-query guarantee agree with the reduction in `10e`; the manuscript correctly keeps the arithmetic and initialization issues separate. The attempted direct AMS retrieval of Browder's short paper failed, so the topology assessment additionally relies on the stated earlier proof and the classical theorem, rather than claiming successful retrieval of that AMS file.

The current stage does not overstate the characteristic-family bounds as universal optimal parameters, or interpret contact sensitivity as intrinsic Newton conditioning. The remaining final-manuscript organization and synthesis work is outside this stage review.
