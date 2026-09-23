# Stage 3 independent review — reviewer 1

Reviewed the three new sections, their notation against the updated setup, the bibliography/main changes, the author record, and the verification script. No other Stage 3 review report was consulted.

**No major issues identified. One minor terminology correction is required.**

## Minor finding

**MINOR 1 — distinguish the path parameter from the barrier parameter.** In `sections/07-fractional-sdp.tex:184`, the theorem says “and its barrier parameter satisfies” before the formula for `mu`. The manuscript's barrier parameter is `nu` (equal to three for this log-det barrier); `mu` is the central-path or barrier-weight parameter. Change the phrase to “and its central-path parameter satisfies” or “the corresponding value of mu is”. The formula itself is correct. Keeping the terms distinct is particularly important in a paper whose uniformity assertions depend on bounded barrier parameters.

## Independent mathematical checks

- **Error-bound dictionary.** Nearest-point projection onto the compact optimal face proves the diameter upper estimate. An exactly attained objective level provides the linear lower diameter bound. An upper error bound is used only for an upper conditioning estimate at a singleton optimum. Matching exponents are invoked only after establishing matching diameter bounds. The face, vertex, and curved-optimum consequences are correct and are explicitly not advertised as an exhaustive classification of arbitrary convex sets.

- **Curved spectrahedron.** The Frobenius Gram matrix in the two displayed coordinates is `2 I`. Computing the log-det Hessian at the diagonal center gives exactly the two stated eigenvalues; their ratio has leading constant `1/2` in gap. The gap-to-mu formula and its positive interval are correct.

- **Simplex plateau.** Both diameter bounds hold uniformly in the objective perturbation. The projected objective norm is bounded above and below as claimed. The limiting generalized Rayleigh quotient has Gram matrix `[[2,1],[1,2]]` and diagonal numerator `diag(theta^2,1)`, giving the displayed eigenvalues and ratio. Their determinant and large-eigenvalue limit give the iterated constant `4/3`. The text properly distinguishes this from the uniform joint gap statement.

- **LP endpoint and active-set constants.** The exact complementarity identity proves matrix convergence from the classical centered-slack limit. Unique optimality makes the active columns independent and the inactive-coordinate restriction injective on the equality kernel. This proves positive definiteness without primal nondegeneracy. The active-set maximization has a bounded closed optimal slack face and a strictly concave log objective on its affine tangent, including the zero-dimensional case. All displayed spectral inequalities follow in the stated directions from the Loewner sandwich. The compact example satisfies its equalities, has a strict feasible point, and has the stated degenerate unique optimum. Its nullspace Gram matrix and dual-center equation are correct. The unbounded witness solves the central equations exactly and has compact positive objective sublevels.

- **Paired SDP geometry.** Both PSD interior witnesses are valid. The principal-minor bounds prove the respective quarter-power and square-root upper diameter bounds. The determinant computation for the signed chord construction is correct, including its Frobenius distance and constants. The block-diagonal witness gives the matching second lower bound.

- **Singularity degree and complementarity.** The two exposing steps are valid on the successive faces. A first-step PSD equality combination must have zero trace-equation coefficient; its zero first diagonal entry forces the first row to vanish, removing the coefficient that could expose the third coordinate. In the restricted system the additional off-diagonal coefficients vanish as well. Thus the only nonzero first certificate is a positive multiple of `E22`, establishing minimality. The same calculation with fixed objective coefficient gives the unique optimal dual slack `E22`; the rank sum is two. This verifies both non-strict complementarity and the claimed separation between equal singularity degree and unequal conditioning exponents.

- **Exact center and all four eigenvalues.** The sign-conjugation symmetry eliminates both off-block entries. Differentiating `-log b-log q` yields the displayed quadratic for `b` and the path-parameter formula. The small-gap asymptotics give `g ~ 3 mu/2`. The off-block eigenvalues are those of `A2^{-1}/b`, because the Frobenius factor two cancels. On the remaining coordinates the Gram matrix is `[[4,1],[1,2]]`. The limiting generalized large eigenvalue is `4/7`, while the determinant produces the smaller constant one. Together these give all four powers, the condition constant `2 sqrt(2)/7` in mu and `3 sqrt(3)/7` in gap, and the restricted constants `4/7` and `6/7`. The later all-barrier transfer uses the established equal-gap Loewner comparison correctly and does not claim invariant leading constants.

## Attribution, clarity, and verification

The local Drusvyatskiy–Wolkowicz primary text, Example 4.5.2 and its Section 4.7 attribution, confirms the nested constraints and their Sturm provenance. The draft appropriately credits the fractional error geometry as classical. It distinguishes the relevant reduced primal Hessian from prior Schur-system clustering and restricts the qualified novelty sentence to this specific explicit spectral calculation and its transfer. The Wei–Wolkowicz contextual statement is consistent with the [author's public abstract](https://www.math.uwaterloo.ca/~hwolkowi/henry/reports/ABSTRACTS.html), which concerns prescribed complementarity nullity and numerical difficulty. No broader priority claim is introduced.

I ran `/home/sgusev/miniconda3/envs/qipm/bin/python conditioning-paper/development/stage3_verify.py`. It passes and reproduces the stated high-precision asymptotic constants, the direct-versus-generalized Hessian agreement, centrality residual checks, and the compact LP limiting eigenvalues. These computations corroborate the independently checked proofs; they are not their basis.

No manuscript edits were made.
