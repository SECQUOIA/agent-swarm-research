# Stage 4 independent review — reviewer 2

## Decision

**No major or minor issues requiring correction identified.** The authored stage is ready to proceed to the numerical and synthesis stage. This is an assessment of the current proofs and carefully delimited claims, not a prediction that external reviewers will suggest no improvements.

Reviewed all three Stage 4 sections, the new bibliography entries, and the author notes without reading other Stage 4 reports. I checked the local Orsucci–Dunjko Proposition 6 and Apers–Gribling abstract/introduction, and independently opened the latter's publisher page and Monteiro–da Silva's version-specific Remark 11.1. I ran `development/stage4_verify.py` successfully. The analytical checks below are independent of the numerical samples.

## LP subspaces and all-barrier projector estimates

The identification of the optimal-face tangent is valid. At a relative-interior optimum every active-support null direction has both feasible signs, so optimality forces its objective increment to vanish. The converse follows from the zero coordinates on the whole face. Thus the hard logarithmic block has exactly the stated kernel and its positive eigenvalues have order `mu^-2` by endpoint positivity.

The bounded logarithmic block and compact-set Dikin lower bound correctly produce `f` eigenvalues of order one and `d-f` of order `g^-2`, including the empty weak cluster at a unique optimum. Equal-gap Loewner comparison transfers those orders with constants depending only on the fixed instance and the barrier parameter.

The quadratic-form projector argument is sound: on a normalized weak vector the Hessian is uniformly bounded, while its lower bound against `g^-2 P_(T-perp)` controls the normal component by `O(g)`. The canonical improvement uses the stronger exact equation `H_N Q = Q Lambda_w - H_B Q`, whose right side has bounded norm. Inverting only on `T-perp` yields `O(g^2)`. No derivative expansion of the endpoints is assumed. Equal subspace dimensions justify the stated projector-angle identity. The zero-dimensional case is explicitly covered.

The extension of the spectral conclusions to approximate centers uses the existing residual version of the same-gap comparison. It is appropriately separated from the forcing statement, which requires exact centrality.

## Newton forcing, restricted solves, and the sharp example

The exact Newton forcing has the correct sign and parameter scaling. Since it is a scalar multiple of the projected objective, its weak norm fractions follow from objective orthogonality to the face tangent. Squared fractions are distinguished from norm fractions.

The discarded-subspace identities are exact because the projector is spectral. For a computed vector in the strong subspace, its strong residual is orthogonal to the discarded weak residual, which proves the squared residual bound. The construction and representation assumptions for that restricted solve are explicit. The text does not replace this Euclidean residual result by a relative direction-error or inexact-IPM convergence claim.

I checked the oscillatory derivative formulas directly. In the normalized coordinates of the base Hessian, they give the displayed global constants `2`, `3`, and `7`. The lower quadratic bound is positive for `epsilon=0.01`; after scaling by four, the differential self-concordance inequality is exactly implied by `2+7 epsilon <= 4(1-3 epsilon)^(3/2)`. The corresponding gradient parameter is less than twenty. Boundedness of the perturbation preserves divergence at every boundary approach. This establishes the stated barrier on the whole open rectangle, rather than only on its central path.

At the chosen exact-gap subsequence the stationarity equations hold for positive `mu`. For `J=H/4`, trace and determinant give the weak eigenvalue limit `2-epsilon^2`, the strong eigenvalue scale `g^-2`, and weak eigenvector slope asymptotic to `-epsilon g`. Consequently the weak solution norm is order `g` and the strong solution norm is order `g^2`, with the exact constants stated. Orthogonality then makes the discarded weak component asymptotically all of the Euclidean solution. The residual still has norm asymptotic to `epsilon g`.

The additional nonconvergent-path observation is justified: each sufficiently small `y` has a unique stationary `x` depending on `sin(log y)`, and the objective derivative remains negative. The two sine subsequences yield distinct limiting horizontal coordinates. This does not conflict with the proved convergence of the weak subspace.

## CG polynomial

The normalized Chebyshev bound and its exponential relaxation have the correct factors. The upper-interval factor is bounded by one below that interval and by one-half on it. The lower factor has all roots in the lower interval, so its product representation gives the claimed upper-interval growth bound `Lambda^m1`.

The selected exponent `j` dominates that growth and the target accuracy simultaneously. On the lower interval the other factor cannot increase the magnitude. Degree counting gives both terms in the displayed bound. The singleton-interval substitutions preserve normalization and all required magnitude estimates. The exact-arithmetic energy-norm CG conclusion follows from its error-polynomial minimization, and the finite-dimensional termination alternative is correctly included. The ensuing matrix–vector count makes no finite-precision or oracle-construction promise.

## Formulation, sensitivity, and finite-parameter boundaries

The fixed-coordinate condition-number inequality follows by singular-value bounds and inversion of the coordinate map. Fixed maps therefore preserve gap exponents; varying whitening maps need not. The Schur identity correctly uses the ambient Hessian and transports the equality matrix along with the variables. The augmented matrix undergoes congruence rather than spectral equality.

For the Lorentz boost, its extreme eigenvalues are `lambda` and `lambda^-1`, with unit eigenvalues on the remaining coordinates. Transporting the Hessian `2I` gives `2G^-2` and condition number `lambda^-4`. The example is explicitly separated from the compact-set theorem. The intrinsic length identity follows by transporting both the metric and tangent vector.

Implicit objective differentiation gives `-H^-1/mu`, so the sensitivity paragraph correctly distinguishes absolute spectral scale from condition number. In the sinusoidal family example the objective derivative changes too; the text expressly avoids claiming excessive sensitivity per unit objective perturbation.

For the inverse-power perturbation, the scalar third-derivative inequality reduces to the stated nonnegative polynomial difference. Summing the component bounds proves differential self-concordance. Direct centrality gives the small-gap path without invoking the finite-parameter theorem. The Hessian and gradient-ratio asymptotics establish both the `g^-3` condition growth and the absence of any finite global gradient parameter.

## Quantum and literature claims

The block-encoding normalization is correctly separated from the matrix condition number. The global polynomial boundedness requirement prevents an automatic use of the CG polynomial as a QSVT implementation. The manuscript does not claim that boundedness alone would be sufficient or overlook state preparation and output requirements.

The local primary Orsucci–Dunjko Proposition 6 states the cited constant-precision worst-case lower bound with `min(kappa,N)` and the specified access models. The manuscript preserves this dimensional qualification and does not turn it into an accuracy lower bound along one fixed-dimensional path.

The qualitative Apers–Gribling account is supported by the primary abstract: a tall-LP algorithm returns an explicit feasible approximate solution and uses spectral approximation to avoid the direct Hessian-conditioning dependence. [Publisher source](https://epubs.siam.org/doi/10.1137/25M1736098).

Monteiro–da Silva's Remark 11.1 explicitly distinguishes the absence of a finite global barrier parameter for inverse-power perturbations. The manuscript cites only that narrow fact and proves its own example; it neither imports that preprint's additional claims nor requires them. The version-specific bibliography entry is appropriate. [Primary version](https://arxiv.org/html/2606.04348v1).

The stage attributes classical endpoint, spectral perturbation, and CG ingredients rather than presenting them as new techniques. Its developed all-barrier projector theorem and sharp example are stated with complete proofs and precise limits. I found no overclaim requiring revision in the current stage.

## Reproduction check

The retained verification script passes. Its outputs agree with the stated weak-eigenvalue limit, projection fraction, solution-component constants, polynomial bounds on sampled intervals, and Lorentz Schur identity. These finite calculations are consistent with, and clearly subordinate to, the universal analytical proofs. No deferred numerical experiment or front-matter item has been counted as an omission in this review.
