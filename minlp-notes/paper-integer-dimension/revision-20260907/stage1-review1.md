# Stage 1 independent review 1

Reviewed the frozen source in `reviews/revision-stage1-round1/source`, the introduction and bibliography diff against `HEAD`, and the stage 1 author and literature reports. I did not consult other reviewers' reports or use previous review counts as evidence.

Verdict: no major issue found in this stage's introduction and bibliography revision. Two minor issues should be corrected before accepting the stage.

## Minor findings

1. **State the additive constant in the vector headline.** `sections/00-introduction.tex:151–156` says that the additional binary count is bounded “by the logarithm” of curvature rank. The actual box theorem (`sections/04-vector.tex:205–218`) gives `ceil(log_2(4r-1))` for the existential count and `ceil(log_2 r)+12` for the rational construction. In particular, “by the logarithm” can be read as a zero extra count at rank one, which is not the theorem. Say “by the logarithm of the curvature rank plus a universal constant,” or give the short actual formula. This is a scope-precision issue in the summary, not a defect in the theorem.

2. **Complete the LinA continuity comparison for the relevant convex case.** `sections/00-introduction.tex:241–246` accurately says that LinA's general corridor model permits discontinuous functions, but juxtaposes this with the present continuous convex scalar setting without saying that LinA already gives continuous approximations on convex corridors. Its Remark 3 explicitly establishes this: [[codsi2025-lina-a-faster-approach-to]] p.10; its Algorithm 2 and per-segment logarithmic numerical-precision oracle bound are on p.12. Since convex scalar functions with absolute error are exactly a convex-corridor case, the current contrast can leave the wrong impression about the closest predecessor. Add the convex-case continuity fact and make clear that the relevant advances here are the comparison against arbitrary convex integer lifts and polynomial total rational encoding without enumerating the partition. Those advances are already stated correctly in the following sentences. The primary publication is [Codsi, Ngueveu, and Gendron (2025)](https://link.springer.com/article/10.1007/s12532-024-00274-8).

## Findings on the headline quantifiers and mathematics

- The asymptotic quadratic statement in introduction lines 55–89 matches `thm:ncrank`: fixed system, full-dimensional bounded box, common componentwise absolute tolerance, arbitrary finite convex lifts with unbounded integer ranges allowed, and an additive constant depending on the fixed system and box. The explicit sentence that the minima need not agree at finite accuracy is useful and correct. The affine/rank-zero case is consistent with the displayed expansion.
- I read the principal-compression argument, real symmetric shrinking proof, contact covariance lemma, covariance determinant estimate, and both bounds in `thm:ncrank`. I found no gap in these arguments in this review. In particular, the real-subspace characterization is supported by the conjugation/supermodularity argument; symmetry then gives the required zero blocks. Principal compression justifies restricting the lower bound to a full-nc-rank coordinate slice, and the upper construction retains the original box constraints after changing coordinates. Thus the proof does not incorrectly replace a correlated domain by its bounding box.
- The cross-product illustration is supported: the scalar Hessians have rank four, while their squared sum is `2I_6`, certifying nc-rank six. It makes the reason for using a joint invariant intelligible without confusing maximum scalar rank with noncommutative rank.
- I read the finite covariance theorem and its proof. The constants `A_n` and `B_n` depend only on dimension; the contact covariance repair and grid bound establish the claimed uniformity in coefficients, positive tolerances, and output count. The introduction correctly distinguishes this finite uniformity from the fixed-system asymptotic constant.
- The rational finite theorem states the polynomial-time and encoding guarantees claimed in the introduction, including the independence of its additive-count constant from output dimension. I checked the theorem statement and algorithm's penalty/metric opening, but this framing review is not a full audit of the lengthy numerical and bit-complexity proof. That proof still belongs in the scheduled technical stage.
- The scalar two-bit statement matches the chord lemma, and its lack of rational-size control is stated. The dense polynomial eleven-bit theorem and sparse positive-polynomial construction are distinguished correctly. The examples and hardness discussion do not suggest that the finite-accuracy algorithm is an exact optimizer of integer dimension.

## Independent literature checks

I inspected primary local source text, rather than treating the stage 1 literature report as proof of its own comparisons:

- [[lubin2022-mixed-integer-convex-representability]] p.11–12: Definitions 4.2–4.3, Lemma 4.1, and its parity proof. The revised attribution of minimum MICP rank and the midpoint obstruction is accurate; the source requires a closed convex lift.
- [[beach2022-compact-mixed-integer-programming-formulations]] p.4–5: quadratic sawtooth approximation, error estimate, Proposition 1, and linear-in-depth formulation size. These support the revised acknowledgment that logarithmic reciprocal-error quadratic encoding is prior work.
- [[garg2020-operator-scaling-theory-and-applications]] p.4–5: Example 1.3 and Theorem 1.4. The noncommutative invariant, shrinking interpretation, and scalar-rank distinction are established algebraic antecedents, as the introduction says.
- [[lyu2026-building-formulations-for-piecewise-linear]] p.6–7: Section 3 and Proposition 1. The shared SOS2 attribution is accurate.
- [[codsi2025-lina-a-faster-approach-to]] p.10–12: continuity on convex corridors, maximal-segment characterization, and per-segment oracle complexity. These support the substantive attribution and the minor correction above.

I also checked the publisher pages for the newly cited LinA and Rebennack–Kallrath articles and the updated Ivanyos–Qiao–Subrahmanyam journal entry. The available publication metadata agrees with the revision. Targeted online searches for noncommutative rank and integer graph approximation did not identify a direct predecessor; this is bounded evidence, not proof of priority. The one explicitly qualified novelty claim is appropriately restricted to the connection between half the nc-rank and the minimum integer-dimension precision coefficient. It does not claim to introduce MICP rank, noncommutative rank, parity, shared discretization, or compact quadratic approximation.

## Editorial assessment and limits

The revised opening gives a reader a clear question, explains why ordinary partition counts are insufficient, identifies three main developments, and separates count from description complexity and optimization speed. The comparison table is useful, and the introduction now explains the importance of the developments through the precise formulation resources they measure. I do not see a need for a structural rewrite in this stage. The two minor findings above can be fixed locally.

This is an introduction/prior-work framing review with direct checks of the principal geometric arguments. It does not certify every theorem in the 86-page manuscript, the full rational compiler proofs, or absence of related results across the entire literature.
