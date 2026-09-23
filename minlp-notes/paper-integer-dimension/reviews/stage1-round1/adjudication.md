# Root adjudication: stage 1, round 1

All fifteen independent reports were received. Every reviewer read the entire 1,206-line stage and reported matching hashes for all five frozen files. Root independently checked the snapshot again after all reports: no mismatch. The reports contain 0 major and 35 minor findings, with repeated findings consolidated below. No next-stage drafting has begun.

## Decisions

All concrete findings are accepted. There are nine coherent correction actions. Their severity is minor because the central positive-rank, centered-box precision theorems and their proof mechanisms are sound; these changes correct local notation, make already-valid choices explicit, restore a simple original scope corollary, and improve attribution and coverage. No report identifies a counterexample to a main theorem or a nontrivial unfilled proof obligation in the completed stage.

| Action | Decision and reason | Required correction |
| --- | --- | --- |
| A1 | Accept all reports' Taylor notation finding. Literal commas are wrong, but the adjacent derivation uniquely determines the intended product. | Replace all three `C_0,2^{-T}` factors by multiplication spacing, including the factor two. |
| A2 | Accept the capacity pinpoint/credit finding. Root read GGOW's theorem statements and its p.237 discussion; the fact is supported, but the collective theorem locator is incomplete. | Separate rank/evaluation citations from the positive-capacity equivalence; credit Gurvits and point to GGOW Section 1.5's concluding discussion/p.237 and Section 2. Do not use the integral-data Theorem 2.18 as the arbitrary-real positivity theorem. |
| A3 | Accept reviewer03's classical disjunction credit. It is a proved lemma here, so lack of citation does not invalidate it, but the paper should credit this central established construction. | Add a brief attribution and accurate reference to Vielma, *Embedding Formulations and Complexity for Unions of Polyhedra*, Management Science 64(10):4721–4734 (2018), DOI 10.1287/mnsc.2017.2856, Proposition 1/Corollary 1; retain the self-contained proof and its stated real-coefficient/common-recession scope. Read the available primary source before citing. |
| A4 | Accept reviewer11's positive-rank qualification. The displayed finite bound divides by rank; the affine case is already handled separately. | Explicitly introduce the finite nc-rank formula with `r>0`; dispatch the affine case in the proof before division if needed. |
| A5 | Accept reviewer11/reviewer15 and root's origin-symmetry clarification. Centered errors are intended throughout. | Require `K=-K` or say symmetric about the origin in the definition of an error body. |
| A6 | Accept reviewer10's polynomial-construction specification and related suggestions in reviewer02/04/11. These are immediate domain restrictions and bounded-derivative choices, not a new construction. | Explicitly retain original affine coordinate identities and domain inequalities after normalization; enlarge the derivative/Taylor constant to cover the enclosing box. Give an explicit nonnegative depth T ensuring `2 C_0 2^{-T} <= epsilon`, with the zero-curvature case handled or a positive enlarged constant. |
| A7 | Accept reviewer13's eleven omitted audit records. Their supporting claims were mapped, but the audit index should include the correction evidence. | Add all eleven listed records at the appropriate stages, update counts, and inspect direct audit dependencies for further omissions. Preserve pending validity status of later stages. |
| A8 | Accept reviewer13's C² coverage omission. The full-rate claim under this regularity is a direct consequence of bounded-Hessian Taylor grids plus the already-proved strong-convexity lower bound. | Add a short precise C² strongly convex/concave box corollary with its Taylor-band/disjunction proof, preserving real-coefficient and unrestricted-size scope. Update coverage. |
| A9 | Accept reviewer14's exact one-sided depth. The error inequality gives the coefficient, but only a big-O choice is currently written. | With A the sum of signed-square absolute coefficients, choose L=max{0,ceil((1/2)log2(A/(4 epsilon)))} when A>0, and explicitly derive k_- L=(k_-/2)log2(1/epsilon)+O(1). Handle affine A=0 separately. |

## Per-report disposition

- reviewer01: findings 1–2 → A1, A2.
- reviewer02: findings 1–2 → A1/A6, A2.
- reviewer03: findings 1–3 → A1, A2, A3.
- reviewer04: findings 1–2 → A1/A6, A2.
- reviewer05: findings 1–2 → A2, A1.
- reviewer06: findings 1–2 → A1, A2.
- reviewer07: findings 1–2 → A1, A2.
- reviewer08: findings 1–2 → A1, A2.
- reviewer09: findings 1–2 → A1, A2.
- reviewer10: findings 1–2 → A1/A6, A6.
- reviewer11: findings 1–3 → A4, A1/A6, A5.
- reviewer12: findings 1–2 → A2, A1.
- reviewer13: findings 1–4 → A7, A8, A1, A2.
- reviewer14: findings 1–2 → A1, A9.
- reviewer15: findings 1–3 → A5, A1, A2.

There are no rejected concrete findings. Optional wording suggestions incorporated in A6 are justified by the same error-budget and domain specifications. The explicitly announced rational nc-rank bit proof remains a stage2 obligation; its deferral is not counted as a stage1 defect. Rank-changing smooth boundaries remain open and are not used as theorem premises.

## Gate status

Pending correction by a separate agent and root inspection/build. As there were no major findings, a second fifteen-reviewer stage1 round is not required by the user's stage rule. All corrected stage1 material will also be reviewed during the whole-paper rounds. If the correction exposes a substantive new mathematical issue, reopen this gate and run another fifteen-reviewer round.

## Root inspection of the correction patch

Root compared the corrected mathematical stage with the archived pre-correction source. The C² corollary chooses h=sqrt(epsilon/(M d)); every rectangular cell has diameter at most sqrt(d)h, so Taylor error is at most epsilon/2. An affine band of radius epsilon/2 both retains the exact graph and stays within epsilon. There are O(h^(-d)) bounded cells, hence the finite-disjunction count has coefficient d/2. This preserves the intended real-coefficient existence scope.

The explicit inertia depth satisfies A*2^(-2L-2)<=epsilon and contributes exactly the negative-inertia coefficient. As part of A9, root additionally requested the trivial k_-=0 lower branch be stated before using a positive-dimensional volume inequality. The positive-rank nc-rank qualification, origin symmetry, enlarged polynomial derivative bounds, and original-domain constraints are all consistent with the existing proofs. Two introduced wording/notation blemishes were sent back to the correction agent before its final build.

The A7 dependency closure may add directly linked relevant records beyond the eleven named by reviewer13. This is accepted within the inventory-reconciliation action; it must not mark unwritten claims verified. Final build and completed correction report are still pending.

## Final root gate decision

Gate passed. Root read the complete correction report and manuscript patch, independently reran the build and manuscript reference checker, and accepted A1–A9 as correctly resolved. There were no major findings and no substantive new issue in the correction pass, so no second stage-1 round is required by the agreed protocol. All material remains subject to the final whole-paper review. The 19-page PDF builds cleanly. Stage 2 may begin.
