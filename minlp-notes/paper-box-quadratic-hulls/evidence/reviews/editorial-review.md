# Editorial referee review

Reviewed `main.tex`, Sections 1–9, the pending edge-contact subsection, and Appendices A–E. This is an independent read of the manuscript text. No literature search, computational experiment, or project-wide check was performed.

The paper has a coherent central argument: valid quadratics define the moment hull; a named certificate system misses a concrete family; that family has a compact exact lift; and the joint hull itself stops admitting any finite lift after dimension three. The sparse graph results follow from that threshold. The numerical section correctly separates deliberately constructed gaps from benchmark findings. Definitions and proofs generally use plain, precise language. The main remaining editorial work is integrating the new contact-classification theorem, removing a few inconsistent claims and symbols, and reducing repeated qualifications.

## Required corrections

1. **Claim-level, raised with root:** the original Introduction contribution 3 said “boundary exposed-ray results,” and the original Discussion said “interior and boundary exposed rays.” The boundary theorem proves extremality through inherited zero and tangency conditions; it does not state or prove exposedness. Use “boundary extreme rays” and “interior exposed rays and boundary extreme rays.” These two passages appear to have been corrected during this review. Preserve that distinction throughout.

2. **Integration:** include `sections/05b-contact-classification.tex` and Appendix E after mathematical review. Reflect the classification in the abstract, contribution 3, the roadmap, and the discussion. It is a stronger developed result than the current description as only a strict sign-class reduction. State its hypotheses explicitly in the summary: positive square coefficients, positive mixed-coefficient product, negative principal two-by-two determinants, and positive values at every cube vertex. Do not suggest that this settles the unrestricted completeness question.

3. **Broken reference:** Section 5, line 374, refers to `sec:evidence`, while the numerical section is labeled `comp:section`. Replace the label.

4. **Notation:** Section 5b, line 49, and Appendix E, line 175, use `$D_3$` for the disjoint cone. Use `$\mathcal D_3$` consistently. Appendix D, line 166, introduces `\PSD_4` without defining this cone notation; use the already established `$\mathbb S^4_+$` instead.

5. **Undefined first use:** Section 8, lines 91–92, uses `$\mathcal M_3$` before its definition in Appendix D. Define it in the protocol as the normalized matrix form of `$\mathcal Q_3$`, or use `$\mathcal Q_3$` with moment-pair notation there. A short definition is enough:
   `For a triple, \(\mathcal M_3=\operatorname{conv}\{(1,x)(1,x)^\top:x\in C_3\}\) is the matrix form of \(\mathcal Q_3\).`
   Use a column vector, e.g. `\bar x=(1,x^\top)^\top`, in the actual TeX to avoid dimensional ambiguity.

6. **Protocol precision:** Section 8, line 23, says the comparisons introduce “no moment outside this pattern.” The disjoint system introduces higher moments. Replace this with “no additional first or second moment outside this pattern,” which states the intended quadratic-coordinate restriction.

7. **Source attribution:** Section 7, lines 76–79, says the result “strengthens the obstruction obtained” from a `$K_5$` minor, without identifying a prior result. Remove this paragraph unless the literature owner supplies a precise citation. The `$K_4$` theorem is already fully explained and important without an uncited comparison. If retained as an elementary consequence rather than prior work, say so explicitly and give the argument or a cross-reference.

## Readability improvements worth making

8. **Explain hull depth at its first substantive use.** Section 8 cites the appendix formula, but readers need its meaning to interpret the later audits. After the selection-rule sentence, add: “Hull depth is the minimum evaluation at the candidate moments of a cube-nonnegative quadratic whose integral over the cube is one.” The formal SDP can remain in Appendix D. Also replace “uniform mean one” in lines 92–94 with an explicit normalization `\(\int_{C_3}q(x)\,dx=1\)`.

9. **Remove duplicated shadow definition.** Section 2 already defines a finite semidefinite lift precisely. Section 6 repeats its full definition and terminology. Start Section 6 with a reference to Section 2 and retain only the closure properties and closed-cone duality needed there. The general normalization lemma adds material and should remain; it need not be removed just because the particular moment cones were already defined.

10. **Avoid repeating the symmetry formulas.** Section 2 gives the exact complement map, and Section 4 repeats all three formulas. Section 4 can refer to the earlier formulas and keep the substantive explanation that diagonal surplus is preserved and `$x,y$` interchange gives at most 24 orientations.

11. **Use unambiguous coefficient language.** Introduction contribution 1 originally called the example a “strictly positive-square quadratic.” Replace with “a nonnegative quadratic with strictly positive square coefficients.” It is distinct from the everywhere strictly positive perturbation later in Section 3.

12. **Identify the tabulated constructed instances.** The representative table omits the seed, while the companion records distinguish seeds. Add “All displayed instances use seed 1” to the caption if the records confirm it, or add the actual seed to each row. Explain that each slash separates the two reported values, rather than denoting a ratio, in the time/block headings or caption. The existing caption already identifies the time unit and excludes the common baseline stage.

13. **Keep the numerical-equality explanation close to the table.** Several displayed `$F$` and `$X$` closures differ by much more than the nominal solver tolerance. The accuracy discussion later explains the large chain example. Add a short cross-reference immediately after the table or in its caption: “Differences between `$F$` and `$X$` on the larger models reflect the accuracy limitations discussed in Section ….” Avoid a blanket claim that all displayed values tie within the nominal tolerance; the matched higher-accuracy comparisons provide the evidence for the practical tie.

14. **Reduce preparation history inside the paper.** Section 8, lines 306–310, explains that no campaigns were rerun while preparing the manuscript. That is useful in the repository verification record, but it is not a scientific conclusion. The paper can simply describe the companion’s records and reproducibility coverage. Similarly, “archived” need not qualify computations every time they appear in the abstract, introduction, and roadmap. Keep provenance and limitations once in the protocol/artifact paragraph.

15. **Consolidate repeated scope qualifications.** Most limitations are mathematically necessary and should remain: joint hull versus one epigraph; exact family enforcement versus family completeness; private versus shared higher moments; numerical estimates versus certificates; and mismatched selections/timing conditions. Some are repeated without adding information. In particular, the abstract’s last sentence, Introduction lines 143–147, Section 4 lines 324–327, and the end of the numerical section all deny a general speedup. One concise qualification in the introduction and the full evidence-based discussion in the numerical section suffice. Likewise Section 6 lines 175–182 repeats the separation/lift distinction already made in the prior-work subsection. Tightening these passages would make the paper more confident without strengthening any scientific claim.

## Overall assessment

No broad rewrite is needed. Retain the existing section order and the separation between the theorem-driven body and exact certificate/proof appendices. The main narrative is understandable to an optimization expert, and the extensive numerical caveats are substantive rather than generic. Resolve the required points above, integrate the reviewed classification, and run the usual manuscript-local reference/build checks. Bibliographic completeness and priority claims remain the literature owner's review responsibility.

## Final integrated pass, 2026-10-06

The same independent reviewer checked the integrated manuscript, submission
documents, and completed literature audit. Appendix F and the original-source
Hildebrand confirmation are now included. The classification now assumes only
positive square coefficients and positive values at all cube vertices; the
earlier, narrower hypothesis list above records a superseded draft.

The final pass found one precision edit: the introduction's sign-class
certificate statement needed the nonnegative-square-coefficient condition.
That condition has been added. The reviewer found no other editorial blocker
and confirmed that the classification, novelty claims, explicit open questions,
and literature attribution are consistent. This was an internal research
review, not journal peer review.
