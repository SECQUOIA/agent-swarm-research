# Stage 1, round 2 — reviewer 11

Reviewed the complete `sections/01-foundations.tex` (lines 1–685) and all four entries of `bibliography.bib`, with emphasis on primary-source attribution and publication metadata. I followed the reviewer protocol and read `literature/AGENTS.md`; I did not inspect other reports or edit manuscript sources.

## Finding R11-1 — minor: author-name spelling differs from the primary source

**Location:** `papers/pooling/bibliography.bib:43`, author field of `gupte2017-relaxations-and-discretizations-for-the`.

The entry spells the fourth author's given name `Myun-Seok`, whereas the accepted manuscript title page and the publisher both give **Myun Seok Cheon**, without a hyphen. The [publisher's author list and affiliation](https://link.springer.com/article/10.1007/s10898-016-0434-4) independently confirm the spelling. This is a small bibliographic transcription defect, with no effect on the mathematical attribution.

**Correction:** change `Cheon, Myun-Seok` to `Cheon, Myun Seok`.

## Attribution and metadata checks

- Lines 195–201 correctly distinguish established destination disaggregation, the standard-pooling one-product approximation principle, and the previously stated sign question. In the actual Dey–Gupte article supplied at `/tmp/pooling-paper-sources/dey-gupte-article.txt`, Proposition 1 (manuscript pages 7–8) selects one output from an IPOP solution, and Section 4/Theorem 2 (page 12) gives the polynomial product-count approximation algorithm. These support the credit at lines 199–200. I did not rely on the locally packaged slides. The [INFORMS article record](https://pubsonline.informs.org/doi/10.1287/opre.2015.1357) confirms authors, title, 2015, volume 63(2), pages 412–427, and DOI.
- [[boland2016-new-multi-commodity-flow-formulations]] p.8 defines fractions according to the head of an incoming arc and output commodities, matching the construction credited at lines 195–196. Its Section 4.3 treats cycles ([[boland2016-new-multi-commodity-flow-formulations]] p.10–12), supporting the restrained attribution at lines 523–526. The manuscript proves its own singular-circulation treatment; it does not simply assume the source's broad invertibility assertion. The [publisher record](https://link.springer.com/article/10.1007/s10898-016-0404-x) confirms the title, authors, 2016, volume 66 and pages 669–710.
- [[gupte2017-relaxations-and-discretizations-for-the]] p.6 contains Remark 2.2 explicitly posing polynomial-time zero-optimality detection as an open question, matching line 201. The [publisher record](https://link.springer.com/article/10.1007/s10898-016-0434-4) confirms issue year 2017, volume 67, and pages 631–669. Its April 2016 online date is not a reason to change the bibliography's issue year.
- [[dey2020-convexifications-of-rank-one-based]] p.1–2 discusses rank-one sets with row/column bounds and their pooling applications, supporting lines 178–180. The [publisher record](https://link.springer.com/article/10.1007/s10898-019-00844-4) confirms the authors, title, volume 77, pages 227–272 and issue year 2020, despite online publication in October 2019.

## Mathematical verification

I checked all stated proofs, including the zero-flow conventions and compactness argument; the affine-rank substitution; the rank-one margins identity and physical-cost restriction; head-weighted destination decomposition; the exact single-product projection and rational reconstruction; approximation and relaxation inequality directions for minimization; shortest-path scaling, support size, and bit bounds; both conic-hull equalities; the capacity-reimposition counterexample; SCC reconstruction and the cyclic sign test; universal facial integrality and its converse; the recognition LP and bounded-dimensional face enumeration; and endpoint disjunctions, MILP bounds, and certificates.

I found no mathematical defect in those arguments under the explicitly stated model. In particular, the cyclic proofs separate isolated positive circulations before using an absorbing chain, the facial converse uses routing costs expressly allowed by the model, and the bounded-pool algorithm retains lower-bound infeasibility checks when deleting arcs.

## Verdict and limits

**Verdict: minor findings only.** One bibliographic spelling correction is requested; no major finding was identified.

This is a mathematical and source-attribution review of Stage 1 only. I did not run a numerical solver, formal proof checker, or manuscript build; verify later-stage claims; or establish exhaustive novelty against all pooling literature. For source arguments I used the relevant extracted primary-manuscript text and publisher records, not a complete comparison of every author manuscript with every published PDF. The Dey–Gupte source examined is an article manuscript rather than the final typeset version. These checks do not imply exhaustive correctness or external-review acceptance.
