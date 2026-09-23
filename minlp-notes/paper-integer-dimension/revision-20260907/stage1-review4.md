# Stage 1 independent review 4

Reviewed the frozen `reviews/revision-stage1-round1/source` introduction and bibliography changes against git HEAD, the author and literature reports, and the corresponding unchanged headline theorem statements. I did not consult other reviewer reports or edit the manuscript. I read `literature/AGENTS.md`.

## Assessment

No major issue identified in this bounded stage. The revised introduction substantially improves the manuscript: it states the model before the results, credits minimum MICP rank and parity immediately, states the principal quadratic claim with its fixed-instance asymptotic quantifier, explains why joint rank matters through the cross-product example, and distinguishes finite existence from rational construction. The comparison table accurately groups the main antecedents and is readable in the rendered page 6. The novelty assertion is qualified and sufficiently narrow for an introduction; it does not claim novelty for rank, capacity, logarithmic encodings, adaptive segmentation, or shared breakpoints.

The headline formulas and claims agree with `thm:ncrank`, `thm:finite-covariance`, `thm:rational-finite`, `thm:vector-rank`, and the count-hardness theorem. I also read the symmetric shrinking proof supporting the real-subspace formulation. This is a framing/source audit, not certification of the untouched long technical proofs, which remain for the scheduled stages.

## Valid minor issues to fix

1. **Qualify the LinA comparison more precisely.** Introduction lines 241–246 discuss its convex-corridor routine and then contrast the general model allowing discontinuity with this paper's continuous graph band. The first assertion is literally true, but it omits the particularly relevant fact that LinA's convex-corridor output is continuous: Codsi et al., Section 4.1, Remark 3 explicitly establishes this. Its logarithmic oracle cost is for computing **one maximal linear segment**, not the entire potentially long partition, and the stated routine assumes continuously differentiable bounding functions with access to their derivatives. Say this explicitly in a short sentence, or remove the discontinuity contrast and emphasize the actual distinction: arbitrary-lift lower bounds and compact rational access without enumerating all segments. Evidence: `[[codsi2025-lina-a-faster-approach-to]] p.9-12`, especially Remark 3 on PDF p.10 and Algorithm 2 / oracle-count paragraph on p.12. The current distinction is not a false novelty claim, but it could mislead the intended reader about the nearest convex predecessor.

2. **Introduce input dimension before using it.** Introduction lines 56–72 invoke an unspecified `n` in the rank formula; the opening only gives `F:D→R^m`. Write `B⊂R^n` at line 57 (or `D⊂R^n` at first use). This also anchors the dimension in the finite determinant comparison. The meaning is inferable but the headline should be self-contained.

3. **Make the vector overhead statement quantitatively accurate.** Introduction lines 151–155 say the additional binary count is bounded “by the logarithm” of curvature rank. The actual finite theorem is `ceil(log_2(4r−1))`, and the rational construction has `ceil(log_2 r)+12`. Use “by the logarithm of the curvature rank plus an absolute constant” (with the affine rank-zero case understood or briefly noted). This avoids a literal bound that would claim zero overhead at rank one. The correct exact inequalities already appear in the referenced theorem, so this is a summary wording defect only.

4. **Clarify what sums to half the rank in the proof sketch.** Introduction lines 94–97 say the discretization depths are proportional to `0`, `1/2`, or `1` times `log_2(1/eps)`, “whose sum is ncrank/2.” It is the proportionality coefficients, not the depths themselves, that sum to half the rank. Write “the coefficients sum to ...”. The underlying construction and `eq:exponent-sum` are correct.

5. **Preserve the published IQS title exactly.** The bibliography update converts `iqs2018` to its published article, but retains “noncommutative” in the title. The publisher's title is “Constructive non-commutative rank computation is in deterministic polynomial time.” Restore the hyphen in the bibliography title; the manuscript's own preferred term can remain unchanged. The DOI, year, volume, pages, and explicit preprint theorem-locator note otherwise match the checked source.

## Independent evidence checks

- Lubin–Vielma–Zadik: read local primary Definition 4.3 and Lemma 4.1, including the closed-convex-lift definition and parity proof (`[[lubin2022-mixed-integer-convex-representability]] p.11-12`); checked the [arXiv record](https://arxiv.org/abs/1706.05135). The attribution and distinction between exact rank and accuracy-dependent minimization are accurate.
- Beach–Hildebrand–Huchette: read Section 2.1's square error estimate and Proposition 1's formulation size in the local primary manuscript (`[[beach2022-compact-mixed-integer-programming-formulations]] p.4-6`); checked [published metadata and abstract](https://link.springer.com/article/10.1007/s10898-022-01184-6). This supports the logarithmic-count antecedent, while making no arbitrary-lift minimum claim.
- Rebennack–Kallrath: read the primary abstract/model statement (`[[rebennack2015-continuous-piecewise-linear-delta-approximations]] p.1-2`) and checked [publisher metadata](https://link.springer.com/article/10.1007/s10957-014-0687-3). Minimum-breakpoint continuous approximation and shifted estimators are accurately credited.
- Codsi–Ngueveu–Gendron: read the local published model remark and convex-corridor Section 4.1, including Remark 3 and the Algorithm 2 complexity paragraph, rather than relying on the stage literature report. Checked [publisher metadata](https://link.springer.com/article/10.1007/s12532-024-00274-8). See minor finding 1.
- Lyu–Hicks–Huchette: read Proposition 1 and the merged-breakpoint/SOS2 discussion (`[[lyu2026-building-formulations-for-piecewise-linear]] p.7-8`). The claim that one SOS2 constraint can serve several same-input functions is explicit in this source.
- IQS: checked [published metadata](https://link.springer.com/article/10.1007/s00037-018-0165-7). See minor finding 5.

## Optional editorial preferences, not defects

The introduction now has a clear hierarchy, but its last contribution paragraph still contains many specialized extensions. A later whole-paper editorial pass could shorten this catalogue if the paper's overall length warrants it. No extra citation or extra theorem is needed just to satisfy this stage. The open growing-output vector gap is appropriately described as outside the established results, not as a dependency of them.
