# Stage 4 independent review — reviewer 4

**Decision: no major or minor issues identified in the submitted Stage 4 material.** I read no other Stage 4 reports and made no manuscript edits.

## Material checked

I read `08-lp-spectra.tex`, `09-clustered-solves.tex`, `10-formulation-scope.tex`, the new bibliography entries, and `stage4-author-notes.md`. I checked the proofs directly against the earlier fixed-gap theorem and established LP hypotheses. I independently inspected the local primary Orsucci–Dunjko Proposition 6 and the online primary Apers–Gribling publisher abstract and Monteiro–da Silva Remark 11.1. The current integrated manuscript builds; no warning, overfull-box, or undefined-reference matches appear in its log. Later front matter and numerical work are deliberately outside this stage.

## Mathematical verification

### LP spectra and projectors

The maximal optimal support B correctly identifies the face tangent: both sufficiently small signs of a feasible B-supported displacement remain feasible, and optimality forces zero objective increment. The hard Hessian summand has this fixed kernel, irrespective of the variation in its positive eigenvalues. Endpoint slack positivity and the fixed restriction matrix give the claimed lower quadratic form on its orthogonal complement. Weyl/minimax bounds and a global Dikin lower bound establish the two eigenvalue scales, including the empty weak cluster when f=0.

The arbitrary-barrier projector proof controls every unit vector in the weak subspace by its bounded Rayleigh quotient and the hard-projector lower bound. It therefore yields an operator-norm O(g) estimate without assuming convergence of the arbitrary barrier's center. For the logarithmic barrier, applying the inverse hard operator on the fixed complementary subspace to the eigenvector equation improves the estimate to O(g²). The equal-dimension projector/principal-angle identity gives the stated projector distances. Uniformity follows from the bounded-parameter and bounded-residual versions of the equal-gap comparison, with the fixed reference LP held unchanged.

### Newton forcing and the sharp barrier

At an exact center, changing μ produces precisely the displayed scalar multiple of c_V. Orthogonality of c_V to the face tangent therefore gives the projected RHS norm bounds. The text consistently distinguishes norm fractions from their squares and correctly withholds the same assertion for a general centering residual.

The restricted-solve identity follows because a spectral projector commutes with H. Orthogonality of the discarded and retained residual components proves the squared residual inequality. The requirement to obtain the projection and remain in its complementary subspace is retained; no Newton-direction or IPM convergence claim is inferred from a Euclidean residual alone.

I independently differentiated ψ=x sin(log y). The displayed first, second, and third differentials are correct. In the H0 coordinates, the bounds 2, 3 and 7 are conservative valid global bounds. The Hessian lower bound is positive at ε=0.01. Scaling by four satisfies `2+7ε <= 4(1−3ε)^(3/2)` and gives gradient parameter `4(2+2ε)²/(1−3ε)<20`. Boundedness of ψ preserves boundary divergence. This proves a finite-parameter barrier on the entire domain, not merely along the selected sequence.

At g_k, the center condition and positivity of μ_k hold. For J=H/4, the trace and determinant give the weak eigenvalue limit `2−ε²` and strong eigenvalue scale g⁻². The eigenvector equation then gives weak RHS norm asymptotic to εg. Dividing the two orthogonal RHS components by the corresponding eigenvalues yields the stated solution components. Their orders g and g² prove that the relative discarded-direction error tends to one while relative residual tends to zero. The later nonconvergent-endpoint observation is also valid: the x-stationarity equation has a unique interior root for every phase, F_y is negative for sufficiently small y, and the two phase subsequences have distinct limiting x coordinates.

### CG construction

The normalized Chebyshev estimate, the monotonicity bound on [0,a2], and the singleton-interval replacements are correct. Because every lower-factor root is in [a1,b1], its growth on the upper interval is at most Λ^m1. The selected power of the upper filter suppresses that growth and preserves the lower-interval contraction. Its degree has the advertised bound, with the unlisted lower-order m1 term absorbed by the first term. The exact CG variational property converts the polynomial estimate to relative energy-norm error from any initial vector. Exact termination in the matrix dimension and the separate one-cluster case are correctly retained. No finite-precision theorem is implied.

### Formulation and finite-parameter limits

The fixed congruence condition bounds follow from singular-value extremal inequalities and inversion of the coordinate map. The ambient Schur identity has the correct inverse transports; the augmented matrix undergoes congruence rather than spectral equality. The Lorentz transformation has eigenvalues λ and λ⁻¹, so its transformed ambient Hessian has condition number λ⁻⁴. The illustration is expressly outside the compact-cone theorem's scope.

Objective differentiation has the correct factor −μ⁻¹. The sinusoidal family example varies the data derivatives as well, so it does not contradict a uniform inverse-Hessian sensitivity bound. This qualification is stated clearly.

For the inverse-power boundary example, direct squaring reduces differential self-concordance to the displayed polynomial inequality. Adding the remaining affine logarithms preserves it. Exact stationarity is established independently of the finite-ν existence proposition. At x=0 the Hessian condition is asymptotic to ηg⁻³, and the gradient-to-Hessian ratio diverges as η/(2g). Thus this example proves the necessity of the finite gradient parameter without invoking an external theorem.

## Literature and scientific claims

The classical logarithmic splitting, subspace perturbation mechanism and CG principle are appropriately credited. The new content is the consequence of equal-gap comparison and the explicit sharp finite-parameter example.

- The local primary Orsucci–Dunjko Proposition 6 states the queried `Ω(min{κ,N})` bound with matrix and RHS preparation oracles. The manuscript correctly distinguishes that worst-case family from a fixed-dimensional path and retains the normalization/decomposition qualifications of structured positive results.
- The [Apers–Gribling publisher abstract](https://epubs.siam.org/doi/10.1137/25M1736098) supports the row-query, explicit feasible solution, spectral approximation, and avoidance of direct Hessian-condition dependence described here. The paragraph draws no unsupported end-to-end comparison.
- [Monteiro–da Silva Remark 11.1](https://arxiv.org/html/2606.04348v1) explicitly distinguishes differential self-concordance from a finite global gradient parameter for the inverse-power perturbation. The manuscript cites only that narrow observation and proves its own example. It does not import the preprint's other results or its stronger algorithmic conclusions.

The QSVT paragraph correctly identifies a necessary global bounded-polynomial contract and does not suggest that this contract alone is sufficient for implementation. Thus the lack of a CG-to-QSVT query bound follows without needing to develop a complete quantum polynomial theorem here.

## Outcome

No corrections requested on this review. Proceed after the coordinating author assesses all five reports. The complete-manuscript review should retain the current distinctions among spectral rates, RHS fractions, solution error, access assumptions, and formulation-dependent matrices.
