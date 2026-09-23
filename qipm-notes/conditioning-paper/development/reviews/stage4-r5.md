# Stage 4 independent review — reviewer 5

Reviewed `08-lp-spectra.tex`, `09-clustered-solves.tex`, `10-formulation-scope.tex`, the added bibliography, and the Stage 4 author notes. I did not read other Stage 4 reports or edit manuscript sources.

## Decision

No major issue identified. Two minor clarifications will make the exact scope of the off-path statement and the conditional solve estimate unambiguous. The central spectral, oscillatory-barrier, and polynomial calculations are sound.

## MINOR 1 — specify which spectral conclusions extend off the exact path

Following `thm:lp-all-spectra`, the sentence “Its spectral conclusions, including the O(g) projector estimate, also hold at points satisfying ...” can be read as extending *all* conclusions of that theorem, including the canonical O(g^2) projector estimate. The proof's off-path Loewner comparison directly establishes the eigenvalue orders and the general O(g) estimate; it does not itself establish the canonical stronger estimate away from the exact logarithmic path.

**Fix:** replace the sentence's opening with “The eigenvalue orders and the O(g) projector estimate also hold at points satisfying ...”. This states exactly what the given argument proves. If the stronger canonical off-path rate is intended, add its separate argument instead. No strengthening is required to support the subsequent exact-Newton statements.

## MINOR 2 — explicitly put the approximate restricted solution in the strong subspace

Immediately before `eq:conditional-window-residual`, explicitly state that `tilde u_s` belongs to `range(I-Pi)`, and formulate its residual assumption as

`||(I-Pi)r - H tilde u_s|| <= delta ||(I-Pi)r||`.

The prose about “solving on the strong LP subspace” suggests this intended restriction, but “residual ... within that subspace” could alternatively mean only a projected residual is controlled. A projected residual alone does not bound an arbitrary weak component of `tilde u_s`, so it would not imply the displayed full residual bound.

**Fix:** add the explicit range condition and the displayed or inline norm assumption above. Orthogonality then proves the stated result immediately. This is a clarification of the intended conditional algorithm, not a request for a new solver.

## Independent mathematical checks

- The maximal optimal support gives exactly the face tangent. The proof correctly uses both displacement signs to establish zero objective increment, and nonconstant objective guarantees a nonempty strong cluster.
- The logarithmic decomposition has a fixed hard-block kernel and a bounded positive semidefinite soft block. Weyl/minimax and the compact-body Dikin lower bound give the two eigenvalue orders, including degenerate unique optima.
- The equal-gap lower quadratic-form bound against the normal-to-face projector gives the general O(g) subspace angle. Applying the inverse hard operator to the canonical weak eigenvector equation gives O(g^2). The equal-dimensional projector identity is used correctly, without an unproved endpoint differentiability assertion for general barriers.
- Exact centrality makes the actual Newton forcing a scalar multiple of the projected objective. The component estimates, squared-fraction distinction, discard identities, and Euclidean solution-error warning are correct.
- For the oscillatory perturbation, I independently differentiated all three displayed differentials. The relative gradient, quadratic, and cubic bounds 2, 3, and 7 hold globally. Scaling by four satisfies the standard self-concordance inequality and gives a valid global parameter below 20; the perturbation is bounded at every boundary approach.
- The specified gap sequence gives positive path parameters and exact centers. The weak eigenvalue of H/4 tends to `2-epsilon^2`, and its weak eigenvector's second-to-first component ratio is asymptotic to `-epsilon g`. The two inverse-weighted solution components have the stated constants. Their orthogonality shows the discarded weak component accounts asymptotically for the entire solution norm while its relative residual vanishes.
- The additional no-endpoint observation follows from the same global barrier: the stationary x-coordinate is a nonconstant function of `sin(log y)`, and the y-gradient remains negative. It is consistent with the general theorem, which assumes no endpoint for that barrier.
- The CG construction's normalized upper-interval Chebyshev factor is bounded by one below the upper interval and by one-half on it. The lower factor's roots give its upper-interval growth bound. Both singleton-interval exceptions work, and the stated degree follows after absorbing ceilings using `delta<=1/2`. The CG consequence correctly concerns exact arithmetic and H-energy error.
- The ambient Hessian, reduced tangent matrix, Schur complement, and augmented matrix are kept distinct. The transport identities and Lorentz-boost condition number `lambda^(-4)` are correct. The objective sensitivity includes the necessary `mu^(-1)` factor; the family-parameter example does not incorrectly claim unbounded sensitivity per unit data perturbation.
- The inverse-power example is differentially self-concordant, has an explicitly constructed central tail, and violates every finite global gradient-parameter bound. Its condition-number and gradient-ratio asymptotics are correct.

## Source and scientific-claim checks

I checked Orsucci–Dunjko's local primary full text around Proposition 6 and its access-model discussion. The dimension-limited worst-case lower bound is described correctly, and the text does not turn it into a fixed-dimensional central-path accuracy lower bound. QSVT's global polynomial contract is correctly distinguished from the two-interval CG polynomial guarantee; no generic square-root factor-access algorithm is inferred.

The primary publisher abstract of Apers–Gribling supports the qualitative row-access, tall-LP, explicit-solution, spectral-approximation discussion: https://epubs.siam.org/doi/10.1137/25M1736098 . This is appropriate positive context for the quantum boundary.

I also directly inspected Remark 11.1 of the version-specific Monteiro–da Silva preprint at https://arxiv.org/html/2606.04348v1 . It states the finite-global-parameter failure attributed to it. The manuscript appropriately proves its own elementary example and does not rely on the preprint's broader spectral or complexity claims. The preprint should continue to be cited only for the narrow checked statement.

Classical endpoint, spectral perturbation, and CG ideas are credited. The all-barrier transfer and sharp example are described as developments of the main theorem without an unsupported exclusive priority assertion. No further Stage 4 corrections are requested.
