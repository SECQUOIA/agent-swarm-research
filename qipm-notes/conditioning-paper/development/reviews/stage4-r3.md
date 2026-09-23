# Stage 4 independent review — reviewer 3

## Decision

No major mathematical, scientific, or attribution issues found. One minor clarification is requested for the approximate-center extension. I reviewed all three Stage 4 sections, the new bibliography entries, and the author record without reading other current reports.

## MINOR — specify which projector rate is extended to approximate centers

Location: `sections/08-lp-spectra.tex`, lines 132–135.

“Its spectral conclusions, including the O(g) projector estimate, also hold” can be read as extending every conclusion of the preceding theorem, including its sharper canonical O(g²) projector estimate. The immediately available cross-barrier argument establishes the eigenvalue scales and the general O(g) projector bound at points with bounded centrality residual. The displayed proof of the canonical O(g²) bound specifically uses the exact logarithmic endpoint decomposition and has not stated its approximate-point counterpart.

Action: say explicitly that “the ordered eigenvalue scales and the O(g) projector estimate also hold” at those approximate points. That narrow edit preserves all proved uses and avoids requiring another canonical approximate-point argument. This is a scope clarification, not a counterexample to a possible stronger logarithmic result.

## Mathematical verification

- The optimal-face tangent is identified correctly using both feasible displacement signs at a relative-interior optimum. Its dimension is f and the objective annihilates it. The logarithmic hard-block kernel is exactly this tangent; the bounded remaining block and positive centered endpoint slacks give the two spectral scales without a nondegeneracy assumption.
- Equal-gap Loewner comparison transfers every ordered scale with constants uniform over bounded barrier parameters. Evaluating the hard-projector lower quadratic form on the weak eigenspace gives the O(g) angle. Applying the inverse hard operator to the canonical eigenvector equation gives O(g²). The equal-rank orthogonal-projector identity has the correct operator norm interpretation.
- Exact parameter-changing Newton forcing is a scalar multiple of the projected objective, with the sign and inverse-mu factors correct. The weak RHS estimates are norm fractions, as stated. The restricted-solve residual decomposition uses the spectral projector's commutation with H and explicitly conditions on solving within the strong subspace. It does not claim a general inexact-IPM convergence result.
- The oscillatory barrier is certified globally. All first, second, and third derivatives of the perturbation have the displayed signs and factors. The estimates 2, 3, and 7 relative to H0 suffice; scaling by four satisfies differential self-concordance and yields a gradient parameter below 20. Positive definiteness and boundary divergence hold on the entire domain.
- At the indicated phase subsequence, exact centrality is valid with positive mu. The weak eigenvalue of H/4 tends to `2-epsilon²`, not 2, and the weak eigenvector's second coordinate is asymptotic to `-epsilon g`. The solution-component estimates follow after restoring the factor four. Orthogonality then gives relative direction error tending to one while the relative residual tends to zero.
- The nonconvergent endpoint conclusion is valid: for each small y the unique x solving stationarity has a negative y derivative, and opposite sine phases give distinct limiting x coordinates. A finite gradient parameter does not force a single optimal-face endpoint under the paper's C³ barrier assumptions.
- The Chebyshev construction covers ordinary and singleton intervals. The upper-interval factor is bounded by one on the lower interval and by one-half on the upper interval. The root-product bound controls growth of the lower-interval polynomial by `Lambda^m1`. The chosen exponent suppresses this growth and yields the stated degree. The CG conclusion correctly concerns exact-arithmetic energy-norm error, with the finite-dimensional termination alternative and no unproved floating-point guarantee.
- Ambient/reduced matrices are kept distinct. The transported ambient Hessian gives exact Schur invariance; the augmented matrix changes by congruence. The Lorentz boost preserves the cone barrier and has ambient Hessian condition `lambda^-4`, consistent with its singular values. The unbounded-cone example is explicitly not presented as a compact-set theorem application.
- Objective sensitivity has the correct `-H_F^{-1}/mu` scale. The unrestricted family-parameter example allows the objective derivatives to grow, so it does not falsely claim bad per-unit-data sensitivity under a Hessian lower bound.
- The inverse-power example satisfies the scalar differential self-concordance inequality because the polynomial difference is `3t²+8t³`. Its central points are justified directly without invoking a finite-parameter theorem. The condition law `eta g^-3` and gradient ratio `eta/(2g)` are correct and demonstrate the necessity of finite nu.

## Primary-source checks

I independently checked Orsucci–Dunjko Proposition 6 in the local primary extraction: it gives `Omega(min{kappa,N})` at constant precision with the stated sparse/block-encoding and RHS state-preparation oracles. The manuscript's dimension caveat is correct. Its claims do not import that worst-case lower bound as a lower bound for one fixed LP trajectory.

The publisher abstract of Apers–Gribling confirms row-query spectral approximation and avoidance of a Hessian-condition-number factor in gradient estimation:

<https://epubs.siam.org/doi/10.1137/25M1736098>

I also opened the version-specific Monteiro–da Silva source. Remark 11.1 explicitly records the lack of a finite global gradient parameter for its inverse-power perturbation:

<https://arxiv.org/html/2606.04348v1>

The present manuscript attributes only that distinction and proves its own scalar example. It appropriately relies on none of the preprint's broader matrix or iteration-complexity claims. The global-boundedness distinction between QSVT and the two-interval CG polynomial is also correctly limited: failure of this particular polynomial to supply a quantum implementation is not asserted as an all-algorithms quantum lower bound.

No unsupported priority claim or remaining proof gap was identified in the authored Stage 4 results.
