# Stage 3 independent review — reviewer 5

Reviewed `05-classifications.tex`, `06-lp-limits.tex`, `07-fractional-sdp.tex`, the new bibliography entries, and `stage3-author-notes.md`. I did not consult any other Stage 3 review.

## Decision

No major issues. One minor terminology correction is required. The mathematical arguments and displayed constants checked below are sound.

## MINOR 1 — distinguish the path parameter from the barrier parameter

In Theorem `thm:fractional-spectrum`, immediately before `eq:fractional-gap-mu`, the sentence says “its barrier parameter satisfies” and then displays a formula for `mu`. Throughout the general theory, the barrier parameter is `nu`, while `mu` parameterizes the central path. In this example the canonical ambient log-det barrier has parameter 3; that parameter does not tend to zero with the objective gap.

**Fix:** replace “and its barrier parameter satisfies” with “and the corresponding central-path parameter satisfies”. Keep the equation unchanged. This makes the terminology consistent with the setup and avoids confusing the two sources of dependence in the all-barrier claims.

## Mathematical verification

### Classification and simplex

The error-bound upper estimate correctly yields only an upper conditioning rate at a singleton optimum; the matching-rate statement separately assumes attained diameter growth. The polytope proof establishes weak sharpness directly without nondegeneracy. The positive-dimensional-face versus singleton dichotomy is exhaustive under the stated compact LP assumptions.

The curved 2-by-2 example uses the Frobenius metric correctly: both coordinate tangent vectors have squared norm two, giving the two displayed Hessian eigenvalues and the leading condition constant 1/2 in gap.

The simplex family has a fixed feasible body, fixed objective range one, and projected objective squared norm between 1/2 and 2/3. Its diameter bounds are uniform in the perturbation parameter. The exact limiting generalized Rayleigh quotient has Gram matrix `[[2,1],[1,2]]` and numerator `Diag(vartheta^2,1)`. Its two eigenvalues are the displayed `(1+vartheta^2 +/- sqrt(1-vartheta^2+vartheta^4))/3`, with product `vartheta^2/3`. This verifies the iterated plateau limit 4/3. The distinction between that iterated limit and the joint gap estimate is correctly maintained.

### LP endpoint and active-set constants

The full-column-rank argument for `A_B` is valid even at a degenerate vertex. Strictly positive limiting inactive slacks then make the compressed limiting quadratic form positive definite. The exact complementarity identity gives operator-norm convergence, and the eigenvalue/condition limits follow without a hidden differentiability assumption at the endpoint.

The active-set dual-center optimization has a compact optimal face after including its boundary: a fixed positive primal point bounds all dual slacks, and full row rank bounds the multiplier. Strict concavity on the equality tangent gives uniqueness. The stated Loewner sandwich and each eigenvalue and condition-number bound follow in the correct direction.

For the compact numerical witness, I checked the strictly feasible point, dual-slack parameterization, stationary quadratic, nullspace basis, and Gram matrix. The generalized eigenvalue formulation preserves the specified Euclidean metric. The unbounded witness satisfies the centrality equations directly and has compact positive objective sublevels; its scaled Hessian is exactly `Diag(1,M^2)` in the given orthonormal basis.

### Fractional SDP and facial reduction

The principal-minor estimates establish the upper diameter rates. The two signed chord witnesses are positive definite: their determinant is `g^(3/2)(a/2-1/4)`, positive on the stated range, and their Frobenius separation is exactly `g^(1/4)`. The restricted witness gives the square-root lower bound.

Both facial-reduction chains are valid in the current face's dual cone. The first-step certificate calculation correctly excludes a one-step reduction, including the extra two equality multipliers for the restricted formulation. This proves degree two for the *optimality systems*, while the original feasible systems have degree zero. The optimal dual-slack calculation also correctly forces `E22`, ruling out strict complementarity while permitting strict dual feasibility.

The full and restricted spectrahedra share the computed central matrix by sign symmetry and strict convexity. Differentiating `-log b-log q` gives the displayed centrality equation and positive root. The path asymptotics `b~sqrt(mu/2)` and `q~mu` are consistent.

The off-block Hessian's factor two cancels its Frobenius Gram factor, giving `A_2^(-1)/b` and constants `sqrt(2)` at exponents 1/2 and 3/2. The other tangent Gram matrix is `[[4,1],[1,2]]`; the coordinate Hessian has scaled limits `(6,-sqrt(2),1)`. Consequently its large generalized eigenvalue has constant 4/7, and its determinant gives the smaller constant one. The condition constants `2sqrt(2)/7` in mu and `3sqrt(3)/7` in gap, and the restricted constants `4/7` and `6/7`, follow correctly. Transfer to other fixed barriers preserves orders rather than these leading constants, as stated.

## Literature and originality

I inspected the local Adler–Monteiro full text around Theorem 3.3 and its centered-dual-path discussion, and the local Drusvyatskiy–Wolkowicz text around Definition 4.2.1, Theorem 4.5.1, Example 4.5.2, and Section 4.7. The nested constraints and attribution to Sturm support the manuscript's explicit treatment of the quarter-power construction as classical. The endpoint corollary is also properly identified as classical.

The compact-set singularity-degree error bound is applied to the added optimality equation through a fixed affine-system right inverse. The argument does not incorrectly infer attainment from an upper error bound. The paired examples make a valid formulation-specific distinction between degree and the attained conditioning exponent.

Targeted online searches for the Sturm construction, quarter-power central-path Hessians, and four reduced eigenvalue scales did not identify a competing exact-constant statement. They did surface the familiar broader SDP central-path and Schur-spectrum literature, including the primary Alizadeh–Haeberly–Overton paper at https://cs.nyu.edu/overton/papers/pdffiles/pdsdp.pdf . The manuscript correctly distinguishes that matrix and regularity setting. The qualified novelty sentence is narrow enough for the evidence: it identifies the exact four leading constants for this trace-normalized construction and the all-barrier transfer, while explicitly excluding novelty of the underlying error-bound example or SDP clustering generally. This review does not establish exhaustive priority.

No other corrections are requested for this stage. The deferred solver, numerical, and front-matter work is outside this report.
