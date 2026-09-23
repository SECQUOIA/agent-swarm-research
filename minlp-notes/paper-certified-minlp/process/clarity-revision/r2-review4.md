# R2 independent review 4

## Verdict

No major or minor issues requiring correction were identified in the assigned R2 scope. The revised experimental section answers its scientific questions directly, while Appendix B preserves the detailed accounting needed to interpret and reproduce the evidence. I recommend accepting this revision and proceeding to the planned review of the complete revised manuscript.

## Scope and checks

I read the clarity plan and R2 author report, the current Section 6 and new Appendix B in full, the changed introduction roadmap and Appendix A context, and the current README and relevant repository/literature maps. I checked the 33-page PDF's text and inspected rendered pages 22, 24, 26, and 30, covering the principal result table, failure and primal-audit exposition, transition to the conclusion, and the appendix accounting table. I also checked the manuscript's labels and references: no duplicate labels or unresolved internal references were found. I did not read other R2 reviews, run numerical generation or replay, or inspect the large archive contents.

## Assessment

1. **The organization now follows scientific questions.** Section 6 states the capability, failure-mechanism, and cost questions and gives their principal answers before presenting supporting detail. Section 6.1 explains the 203 accepted artifacts out of 289 attempted models, distinguishes this from 198 successful producer returns, and then addresses bound strength and exact primal completion. Section 6.2 organizes evidence by what it establishes: invalid discrete inferences, failure of sufficient nonlinear tests, and original-variable infeasibility or matching primal evidence. Section 6.3 explains the practical replay and storage costs. This is a coherent account of the result rather than an order determined by development history.

2. **The main text retains the context needed to interpret its claims.** Moving the full protocols to Appendix B does not leave the denominator, model semantics, time limits, concurrency, or reference metric unexplained. The main section retains the 299-to-289 selection accounting, exact loaded-model qualification, requested search budgets, outer process limit, separate replay limit, and worker count. The signed reference difference is defined before interpretation and is explicitly distinguished from an optimality gap. The catalogue of 222 models from 405 records is identified as a collection spanning protocols, so it cannot reasonably be mistaken for a stronger result from the uniform experiment.

3. **The failure discussion preserves the important distinctions.** The three externally accepted invalid proof steps are evidence of unsound submitted inferences, not a claim that their final bounds are false. The historical audit is similarly explicit about first-failure evidence. The nonlinear example demonstrates failure of a sufficient intercept test without treating that as proof that the affine cut is globally false. Returned-point audits give the actual violated rows, tolerances associated with displayed coordinates, and exact source-model interpretation needed for the stronger conclusions. The synthesis at the end of the failure discussion makes these distinctions easier to retain.

4. **Appendix B is appropriately supporting material.** Its frozen protocols, phase accounting, historical replay costs, and separately versioned representation repairs support the principal results without controlling the main narrative. The V1/V2/V3 distinctions are still necessary to avoid combining different experiments. In particular, the anticipated full V3 tally is clearly an expectation rather than a newly performed campaign. Repeated totals in the appendix are useful in their accounting context; I did not find bloated repetition that requires deletion.

5. **Integration and presentation are sound.** The introduction points readers to both appendices; Appendix A retains the reproduction instructions and points to Appendix B for protocols and accounting. The README's reading route agrees with these roles. The reference-comparison and solver-audit labels now sit within the appropriate scientific subsections and still lead to the intended explanations. Tables 4 and 5 remain legible, with captions that explain the reference metric and phase-timing populations. The inspected PDF pages show ordinary continuous pagination, adequate spacing, and no clipped content or awkward float isolation. The increase to 33 pages is not itself a defect: the additional appendix structure preserves necessary detail while improving the main narrative.

6. **Cost and availability claims remain proportionate.** Accepted-record sums, all-record sums, and elapsed concurrent time are distinguished, and the text does not infer a speed advantage or peak-memory bound from them. The portable core, separate bulk archive, checker dependencies, generator dependencies, and limited log redactions have clear roles. The source/archive refresh is documented by the author; this review does not independently certify its hashes or rebuild the package, which falls outside the assigned exposition review.

## Required changes

None identified. This verdict applies to R2's organization, explanatory sufficiency, cross-reference integration, and presentation; it does not replace the planned final review of the complete revised paper.
