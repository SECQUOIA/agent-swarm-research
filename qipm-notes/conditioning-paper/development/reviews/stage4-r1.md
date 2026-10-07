# Stage 4 independent review — reviewer 1

Reviewed the three Stage 4 sections, bibliography additions, author notes, and verification script. I did not read other Stage 4 review reports.

**No major issues identified. One minor clarification is recommended to remove an ambiguous theorem extension.**

## Minor finding

**MINOR 1 — say exactly which conclusions extend to approximate centers.** At `sections/08-lp-spectra.tex:132–135`, “Its spectral conclusions, including the O(g) projector estimate, also hold” can be read as extending every conclusion of the theorem, including the sharper logarithmic `O(g^2)` projector estimate. The argument supplied there explicitly extends the eigenvalue orders and the general `O(g)` bound through equal-gap Loewner comparison; Loewner comparison alone does not prove the sharper rate. Replace this wording with “The eigenvalue orders and the general O(g) projector estimate also hold ...”. If the stronger logarithmic statement is intended for approximate centers too, provide its separate argument establishing a bounded soft block and the required hard-block lower bound at those points. This is a precision issue in the extension paragraph; the theorem as stated for exact centers is correct.

## Independent mathematical audit

- **Face tangent and eigenvalue counts.** The support definition of B and the two-sign feasible displacement argument correctly identify the complete optimal-face tangent. The logarithmic hard term has that exact kernel and order `mu^{-2}` on its orthogonal complement. The soft term is bounded by classical endpoint positivity. Weyl/minimax and the Dikin lower bound establish both clusters, including an empty weak cluster at a unique optimum. Equal-gap Loewner comparison transfers the ordered scales with the stated uniformity.

- **Projector estimates.** Evaluating the hard-projector quadratic lower bound on an orthonormal weak basis gives the general angle bound `O(g)`. Applying the hard-block inverse to the exact logarithmic weak eigenvector equation gives `O(g^2)`. The identity relating projector difference norm to the largest principal-angle sine is applied to equal-dimensional subspaces. No unproved endpoint differentiability is used.

- **Newton forcing and output contract.** At an exact center the parameter-change residual is the stated scalar multiple of the projected objective, with the correct sign and reciprocal parameters. The norm fractions and squared fractions are distinguished. The discarded-mode residual and solution identities are correct, as is the conditional restricted-solve residual estimate. The text correctly warns that an approximately central point has an additional forcing term and that Euclidean residual does not imply relative direction or quantum solution-state accuracy.

- **Global oscillatory barrier proof.** I independently differentiated the perturbation; its cubic is `-3(s+t)uv^2/y^2+x(3s+t)v^3/y^3`. The local-coordinate derivative bounds 2, 3, and 7 are valid over the entire rectangle. Scaling by four gives the stated self-concordance inequality, and the gradient-parameter bound is below 20. Bounded perturbation preserves boundary divergence. At the chosen subsequence the point is stationary for a positive path parameter. The weak eigenvalue tends to `4(2-epsilon^2)`, the weak RHS norm is asymptotic to `epsilon g`, and the weak versus strong solution norms have the stated constants. Their orthogonality proves relative solution error tending to one. The subsequent nonconvergent-endpoint argument is also valid: distinct sine subsequences have distinct fixed x values, while the associated positive path parameters tend to zero.

- **CG polynomial.** The normalized Chebyshev bounds and upper-factor degree make its contraction at most one half on the upper interval and at most one on the lower interval. The lower-factor roots give the upper-interval growth bound `Lambda^{m1}`. The chosen power suppresses this growth. The degree estimate includes ceiling terms and covers both singleton intervals. The polynomial-to-CG implication correctly concerns exact-arithmetic energy error, with dimension-limited termination and no finite-precision residual conclusion.

- **Formulation and finite-parameter boundaries.** The coordinate condition-number inequalities follow from singular-value bounds and the inverse transformation. The Schur identity uses the ambient Hessian and holds under the stated simultaneous transformation; the augmented matrix has congruence, not spectral identity. The Lorentz boost preserves the barrier and gives the claimed ambient condition number. Objective sensitivity has the correct `-1/mu` factor and the family-parameter example explicitly accounts for varying data derivatives. The inverse-power scalar self-concordance inequality, `eta g^{-3}` condition rate, and divergent gradient ratio are all correct.

## Sources and numerical verification

The local Orsucci–Dunjko primary text, Proposition 6, states the claimed constant-precision `Omega(min{kappa,N})` bound with its oracle assumptions. The draft properly distinguishes worst-case growing-dimensional families from one fixed-dimensional central path and does not claim a generic Gram-factor square-root speedup. The [Apers–Gribling publisher abstract](https://epubs.siam.org/doi/10.1137/25M1736098) supports the row-query, Hessian approximation, gradient estimation, and explicit-solution characterization.

I inspected [Monteiro–da Silva v1, Remark 11.1](https://arxiv.org/html/2606.04348v1). It explicitly notes the lack of a finite global barrier parameter for the inverse-power perturbation. The manuscript cites only that distinction and proves its own example; it does not rely on the preprint's other claims.

Running `/workspace/local-home/miniconda3/envs/qipm/bin/python conditioning-paper/development/stage4_verify.py` passes. The calculations reproduce the barrier derivative checks, sharp weak-mode and direction-error constants, polynomial bounds in all four test cases, and Lorentz/Schur identity. These are corroborating checks of the supplied analytic proofs.

No manuscript edits were made.
