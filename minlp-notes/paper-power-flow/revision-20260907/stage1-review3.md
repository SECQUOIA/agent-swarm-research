# Stage 1 independent review 3

Verdict: no major issue found in the Stage 1 changes; one minor clarification should be made. The revised introduction explains the main contribution, identifies the physical assumptions on which the reductions depend, and appropriately separates imported ideas from the electrical realization. This verdict concerns the frozen Stage 1 introduction and bibliography, assessed against their downstream statements; it is not a substitute for the planned full gadget audit.

I read the frozen introduction and bibliography in full, the author report and literature audit, the algebraic and numerical sections in full, and the relevant structural and AC definitions, statements, and proofs. I did not read other Stage 1 reviewer reports or rely on historical PASS records. No manuscript was edited.

## Finding requiring a minor correction

**R3-1 — Clarify that the Dynamic Toolbox discrepancy is not caused by a changed definition.** Locator: `sections/00-introduction.tex`, lines 196–201, particularly “under the rational equivalence used here.”

The mathematical criticism is supported, but this wording leaves the reader uncertain whether the manuscript and the cited preprint use different equivalences. Section 1.5 of Dynamic Toolbox defines its maps by rational coordinate functions with integer coefficients and requires a rational inverse. Integer versus rational coefficients makes no difference. Under the ordinary globally defined interpretation, this is the manuscript's definition. The manuscript therefore supplies an obstruction to the stated scope of that preprint theorem, not merely a result for a narrower choice of equivalence.

Proposed correction: explicitly state that the definitions agree under globally defined rational-coordinate maps, and that the counterexample rules out the preprint's broader scope under that definition. A short sentence suffices. Optionally give the exact failing Boolean step in a footnote or the arithmetic appendix: Lemma A, Step (3), moves nonnegativity constraints outside disjunctions while later assigning every auxiliary its associated polynomial value. For `x >= 0 or y >= 0`, at `(1,-1)` that proposed map assigns the second nonnegative auxiliary the invalid value `-1`; leaving that auxiliary free instead destroys the proposed unique extension. The basic-closed invariant and compact three-quadrant example already provide the decisive argument, so this optional illustration is not a prerequisite to accepting the mathematics.

This is minor exposition/source precision. No mathematical redevelopment is required.

## Findings checked and not upheld as objections

- **Scope of electrical universality.** The main result map correctly distinguishes compact basic closed sets over the rationals up to rational equivalence from arbitrary compact semialgebraic sets up to semialgebraic homeomorphism. I independently checked the denominator-bound argument in Proposition `basic-invariance`: compactness supplies a common positive rational lower bound; the forward and substituted inverse denominators remain nonzero; membership in the target plus the inverse identity prevents extraneous ambient points. I also checked the parity argument for the three-quadrant example and the standard-simplex/nonface realization. I found no flaw in these arguments. No construction-size claim is silently added to triangulation or arbitrary basic-set realization.
- **Source theorem criticism.** Dynamic Toolbox Theorem 1 does state rational universality for arbitrary compact ETR solution sets. Its definition of rational equivalence and Boolean preprocessing were inspected directly in the repository primary extraction, and the pinned v1 was verified on arXiv. The criticism does not invalidate the independently imported decision hardness theorem. The revised introduction makes that separation adequately.
- **Known versus new residual scale.** Jeronimo–Perrucci–Tsigaridas Example 13 already uses a repeated-power chain with doubly exponential point separation. The manuscript now credits that scale and claims a fixed-data bounded-degree *electrical* family plus transfer bounds for its actual gadgets. Those are precise additional developments. The introductory restriction that all voltage bounds remain exact matters and is present. The introduction also expressly declines to transfer this quantitative claim through planarization. I checked the displayed recurrence and the inequalities in the numerical section; they support the summarized residual claim. The accuracy-bit consequence is stated as a limitation of residual thresholds, without converting it into an algorithmic time lower bound.
- **Other algebraic power-flow work.** Mareček–McCoy–Mevissen Theorem 1 and Corollary 2 concern generic complex root counts and positive-dimensional algebraic solution sets. The manuscript's prescribed compact real feasible sets with operating inequalities are a different statement. The revised comparison is accurate and does not imply that algebraic power-flow analysis originated here. The cited arXiv v2 date is correct.
- **Prior complexity and model assumptions.** The table and accompanying paragraphs match the Bienstock–Verma lossless fixed-magnitude setting and the Lehmann–Grastien–Van Hentenryck fixed-magnitude star construction. The manuscript does not purport to subsume their graph and physical restrictions. Independent singleton voltage and injection bounds at the same bus are prominently disclosed. The Gan–Low comparison is limited to sufficient relaxation-exactness hypotheses; the Jeeninga et al. distinction correctly concerns independent operating restrictions rather than signed demands. Jeeninga Theorem 3.22 addresses both exact feasibility and interior feasibility, while convexity is developed earlier in that source.
- **AC lineage and membership.** Farivar–Low Theorem 2 explicitly supplies cycle consistency modulo a full turn. Jafarpour et al. Theorem 3.6 supplies winding-cell potential coordinates. The manuscript properly credits these concepts and identifies its additional rational polynomial encoding. The short-arc crossing rule, cycle test, and general rational cosine scope in Section 4 support the introduction. The energy identity needs real differences strictly below pi, and that hypothesis appears in the result map. I found no unsupported claim that torus winding solutions disappear merely because local angles are small.
- **Certificates and approximation.** The gap-promise result is correctly treated as a supporting Lipschitz/rounding consequence. The Bienstock–Del Pia–Hildebrand citation is to the general certificate questions rather than an incorrectly imported variable-dimension theorem. I independently inspected the local Bienstock–Muñoz Theorem 7 and Corollary 8; their version-specific reference and scaled-tolerance comparison are correct.
- **New bibliography entries.** The five added sources are real and substantively relevant. The inspected primary copies and arXiv records support their author/title/version fields. I found no invented citation or materially incorrect bibliographic data.

## Minor item for the later numerical stage

The body at `sections/06-numerical.tex`, Proposition `residual-separation`, cites Jeronimo et al. “Theorem 1.1,” while the available local preprint numbers the bound Theorem 1. The formula used in the manuscript agrees with the inspected bound. Verify the journal numbering or explicitly cite the preprint's Theorem 1. This is a locator issue in an unchanged section, not a Stage 1 scientific error or a reason to repeat this stage's major-issue review cycle.

## Independent source work and limits

Primary local material inspected included Dynamic Toolbox Section 1.5, Theorem 1, and Lemma A; JPT Theorem 1 and Example 13; Mareček et al. Theorem 1 and Corollary 2; the Bienstock–Muñoz Theorem 7/Corollary 8 passages; Jeeninga et al. Theorems 3.18 and 3.22; the Bienstock–Verma model/introduction; Lehmann et al. model and star-construction introduction; and cached primary Gan–Low, Farivar–Low, and Jafarpour et al. passages. Where extraction loses formulas, I used the plainly recoverable statement and manuscript reasoning rather than treating missing glyphs as evidence.

Fresh searches included `"power flow" "universality" algebraic complexity existential`, `"power flow" "existential theory" hardness`, and `"Dynamic Toolbox" "basic" closed`. They did not locate a closer conflicting power-flow realization theorem; the results were noisy, so they are not evidence of exhaustive priority. The manuscript's qualified, model-specific novelty statement is appropriate.

Primary web records verified:

- [Dynamic Toolbox v1](https://arxiv.org/abs/1912.08674v1).
- [Power Flow as an Algebraic System v2](https://arxiv.org/abs/1412.8054v2).
- [Bienstock–Muñoz v15](https://arxiv.org/abs/1501.00288v15).
- [Delabays–Coletta–Jacquod](https://arxiv.org/abs/1512.04266).
- [Jafarpour et al. v4](https://arxiv.org/abs/1901.11189v4).
- [Bienstock–Del Pia–Hildebrand](https://arxiv.org/abs/2011.08347).

I did not rebuild the paper because this review identified no typesetting-dependent objection and the work was source/literature review. Full proof verification of every planar port, electrical gadget, and arithmetic range remains a separate authorized development stage.
