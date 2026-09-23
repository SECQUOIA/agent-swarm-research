# Stage 3 independent review — reviewer 3

## Decision

No major mathematical or scientific issues found. Two minor corrections are requested: consistent terminology for the path parameter, and one additional directly relevant literature comparator for the singularity-degree/spectral discussion.

I read all three new sections and the author record without consulting the other current review reports. I independently checked the constants, tangent metrics, degeneracy arguments, and implications from the Stage 2 theorem.

## MINOR 1 — reserve “barrier parameter” for nu

Location: `sections/07-fractional-sdp.tex`, line 184, “and its barrier parameter satisfies,” immediately before the formula for `mu=q/(1-b-2g)`.

Throughout the geometric theory, the barrier parameter is the complexity parameter `nu`, whereas `mu` parameterizes the central path or weights the barrier in the objective. Calling both quantities the barrier parameter is an avoidable terminology collision in a paper whose uniformity claims depend specifically on bounded `nu`.

Action: replace this phrase with “and the corresponding central-path parameter satisfies” or “and the corresponding value of mu satisfies.” Check analogous prose in the new sections for the same terminology.

## MINOR 2 — acknowledge later work linking singularity degree and spectral rates

Location: the prior-work paragraphs in `sections/07-fractional-sdp.tex`, especially lines 147–165 and the final paragraph.

A directly relevant comparator is Sremac, Woerdeman, and Wolkowicz, *Error Bounds and Singularity Degree in Semidefinite Programming*. Its author-posted 2019 manuscript is openly available:

<https://optimization-online.org/wp-content/uploads/2019/08/7334.pdf>

I inspected its introductory scope, Corollary 4.3, Theorem 4.4, and the statement of Theorem 4.7. For a family of external central paths, it studies the eigenvalue rates of primal/dual matrix iterates and connects slow or distinct rates with singularity degree. This is closer to the new discussion than the existing Wei–Wolkowicz instance-generation citation. Its matrices and path differ from the equality-reduced objective central-path Hessian studied here; I found no conflict with the four constants or paired-diameter proof.

Action: inspect the source's path definition and add a concise comparison distinguishing external regularization paths and primal/dual iterate eigenvalues from the present reduced Hessian at a primal objective gap. Add verified bibliographic metadata, or cite the openly inspected preprint if the published metadata has not been checked. This is a literature-completeness correction, not evidence that the new calculation is already known or that its qualified priority sentence is false.

## Mathematical checks and findings

- **Error-bound dictionary.** The diameter upper bound properly includes the diameter of the optimal set, and only an attained diameter exponent is used for a matching conditioning rate. The lower bound from the objective direction is valid for every gap in the objective range. The polytope proof establishes sharpness without a nondegenerate-basis assumption. The discussion correctly declines to infer a fractional LP asymptotic rate from finite-range slopes.
- **Curved 2-by-2 example.** The Frobenius Gram factors are both two. The two displayed Hessian eigenvalues and the asymptotic condition constant `1/(2g)` follow from the coordinate Hessian after dividing by these Gram factors. The centrality conversion is correct.
- **Simplex plateau.** The diameter bounds are uniform in the objective perturbation. The projected objective norm calculation and fixed feasible geometry justify uniform barrier-family conditioning constants. The generalized tangent eigenvalues are `(1+theta^2 +/- sqrt(1-theta^2+theta^4))/3`; their determinant gives the stated iterated `4/3` constant. The joint gap statement is correctly separated from the iterated limit.
- **Unique LP endpoint.** The exact scaled-Hessian identity and the cited centered dual-slack limit suffice. Uniqueness implies injectivity of both `A_B` and `R_N W`; no hidden primal nondegeneracy assumption is needed. The active-set Loewner bounds have the correct directions. Strict primal feasibility bounds the dual optimal slack face, and full row rank converts this to bounded multipliers, justifying the logarithmic face-center maximizer.
- **LP examples.** The compact example's strict point, optimal partition, derivative equation for its analytic center, nullspace matrix, Gram matrix, and generalized-Hessian entries are consistent. The unbounded example solves centrality exactly and has compact positive objective sublevels; it is explicitly outside global compactness and uses the localization proposition appropriately.
- **Paired SDP diameters.** Principal-minor bounds yield the stated upper exponents. The positive-definite chord witnesses have determinant `g^(3/2)(a/2-1/4)` and the stated Frobenius separation. The block-diagonal restriction has a square-root chord while eliminating the quarter-power off-block direction.
- **Singularity degree and complementarity.** Both original feasible systems are strictly feasible, while both optimality systems require two facial reductions. The first-step PSD exposing-combination calculation forces a multiple of `E22`, so one-step exposure is impossible even after adding the two off-block equalities. The same calculation with fixed objective coefficient gives the unique optimal slack `E22`, hence failure of strict complementarity. Dual strict feasibility is nevertheless directly established.
- **Exact fractional center.** Symmetry removes the two off-block entries; stationarity of `-log b-log q` gives the stated quadratic for `b` and the correct positive `mu`. The asymptotic conversions `b~sqrt(mu/2)`, `q~mu`, and `g~3mu/2` follow from the formulas.
- **Four Hessian scales.** The off-block Frobenius factor cancels correctly and yields the two eigenvalues of `A_2^{-1}/b`. On the remaining block, the Gram matrix is `[[4,1],[1,2]]`; the three rescaled Hessian-entry limits are `6,-sqrt(2),1`. The rank-one generalized limit gives the constant `4/7`, and the determinant gives the smaller constant one. The condition constants `2sqrt(2)/7` in mu and `3sqrt(3)/7` in gap are correct. Restricting to the block-diagonal section gives the stated `4/7` and `6/7` constants.
- **All-barrier transfer.** The equal-gap Loewner theorem legitimately transfers each ordered eigenvalue order, not its leading constant. The manuscript makes that distinction explicitly.

## Attribution check

The local primary extraction of Drusvyatskiy–Wolkowicz, Example 4.5.2 and Section 4.7, confirms the nested constraints and their attribution to Sturm. The new text correctly treats the quarter-power geometry and LP endpoint convergence as classical. Its exclusive novelty claim is restricted to the explicit reduced-spectrum calculation for the trace-normalized construction and is qualified. Subject to the additional comparator above, I found no unsupported novelty assertion in this stage.
