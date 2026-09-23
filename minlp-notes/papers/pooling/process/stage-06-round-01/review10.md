# Stage 6, round 1 — review 10

I reviewed the entire introduction and Section 6, including every new proof, with extra attention to the common-factor and network–simplex summaries, canonical scope, and source attribution. I did not edit the manuscript, inspect other round reports, or run a build.

## Findings

### 1. Minor: the nonlinear leaf has ambient dimension one, not dimension one

Location: `sections/06-synthesis.tex:729` (`s6:parametric`).

The text calls `P_i={sqrt(a_i)}` a “compact convex singleton of dimension one.” A singleton has affine and semialgebraic dimension zero. The intended property is that it is a scalar leaf, contained in a one-dimensional ambient space. This does not affect the Square-Root Sum reduction or its arithmetic conclusion.

Correction: write “Each leaf is a compact convex singleton in one scalar variable” or “in a one-dimensional ambient space.”

### 2. Minor: the established network–simplex extended hull lacks its direct primary citation

Location: `sections/06-synthesis.tex:829–840`, especially the sentence at lines 832–833; corresponding bibliography.

The sentence correctly says that simplex disaggregation “already” gives a compact extended hull, but the paragraph cites only the separate repository results and De Loera–Onn. The direct predecessor for the precise network–simplex model is Khademnia–Davarnia, *Convexification of Bilinear Terms over Network Polytopes*, Appendix (25), which explicitly records this extended hull and credits the earlier polytope–simplex work of Davarnia–Richard–Tawarmalani. That primary model/formulation attribution is present in the canonical network notes but is lost in the manuscript summary. De Loera–Onn supports transportation universality, not this disaggregation attribution.

Correction: add a direct citation to Khademnia–Davarnia, Appendix (25), to the established-hull sentence; optionally cite Davarnia–Richard–Tawarmalani as its earlier general source. This is a local attribution omission, not a changed contribution claim: the manuscript already identifies the construction as established and correctly distinguishes it from original-space coefficient universality.

Evidence: `literature/papers/khademnia2025-convexification-of-bilinear-terms-over/fulltext.md`, p.30, Appendix; [primary arXiv version](https://arxiv.org/html/2302.14151v2). The canonical `results/network-simplex-cycle-theta-hull.md`, section 5, gives both primary references.

### 3. Minor: adjacent unpublished results need a reader-facing locator

Location: `bibliography.bib:374–445`, cited throughout `sections/06-synthesis.tex:742–855`.

The adjacent research-note entries contain a title, year, and “Unpublished research note,” but no author, URL, repository path, or identifier. Their exact theorem proofs are intentionally outside the manuscript. A reader of the manuscript cannot locate those proofs from the bibliography alone, even though the internal coverage map identifies them precisely. This affects verifiability of the general-margin, conic, common-factor, network, and power-flow summaries, rather than their mathematical scope.

Correction: supply an actual repository/document locator for each note, or a supplementary-material index mapping each cited title to its included file. There is no need to infer authorship or publish anything during this review. Repository-relative paths can make the current draft reviewable pending permanent public identifiers.

## Mathematical and scope checks

- Re-expanded the weighted endpoint products and checked the exposing inequality, distinct terminal values, and polynomial encoding. The two-variable Fourier–Motzkin argument and the three-coordinate simplex counterexample are sound for coordinate projections.
- Checked both physical path maps, the reset equality, the revenue differences, and the uniform penalty. The `N^N` constant follows from `s3:hoffman` with integral coefficient bound one; retained upper contracts make every removed-contract deficit nonnegative. The final varying revenue remains the only varying price. The graph/epigraph line-factor lower bound concerns formulas in price and value alone and does not obstruct the stated short evaluation recurrence.
- Checked the nonlinear interface equations, all new capacities and quality bounds, profit cancellation, and unique extension. The strict-local-maxima proof has the correct negative edge derivatives and tangent-cone argument. The parity proof allows unbounded integer coordinates. The LP hull proof correctly requires returning an optimal hull vertex. The reset-price refinement and general-supply telescoping identity preserve the claimed scope; the nonlinear throughput-contract counterexample is feasible.
- Checked both dense-slab reductions, including nonempty domains, rational endpoint certificates, the padding upper bounds, and the distinction between ordinary hardness and physical pooling hardness.
- Checked the minimum-rank centering identity, projected-box enumeration, slice-vertex coverage, feasible interpolation, treatment of equal totals and zero total, stationary-point sign cases, and quadratic-field recovery. The rank-one cost sweep and irrational example agree with the formulas. The Lagrangian cost has interaction rank at most the attribute rank, and the perturbation error bound follows from total mass.
- Checked the two-LP sign disjunction for a rank-one matrix perturbation, including `z=0`, unbounded LP objectives, and rational recovery; the fixed-one column is necessary for measuring a parameter-dependent right-hand side. The convex-leaf example gives exactly Square-Root Sum, with the dimension wording corrected as above.
- Compared the common-factor discussion with all four canonical anchored/fixed-linking results. Signed and integer scalar optimization, the fixed linking-row count, common distribution requirement, rational envelope separation, and consecutive-integer telescoping scope are preserved. In particular, the final exclusion of added original-point product/linking restrictions is essential and correct. The full-hull note also identifies classical convex-order and lift-zonoid foundations; a direct acknowledgment of those foundations in this short summary would be useful, but I do not treat that optional addition as a separate defect.
- Compared all three canonical network results. The statement concerns equality-balanced bounded flow polytopes, selected products, and original-space coordinate sections/coefficient ratios. It does not infer optimization hardness from universality. Independent block gluing, merged unobserved simplex states, transportation subset cuts, unit flow/product coefficients, and the restriction to internally disjoint parallel-path blocks support the summary. The slack-arc and physical-mixing qualifications are retained.
- Checked the correlation-face atom argument and compared the exact and approximate conic summaries with their three canonical notes. The accuracy constants, entrywise norm, different LP/SDP transfer mechanisms, and objective-family limitations agree. The power-flow paragraph retains the real-angle qualification and makes no pooling theorem inference.
- Cross-checked introductory certificate, degree-boundary, contract-exception, and two-vector claims against the cited statements in Sections 2–5. The objective and lower-bound qualifications in the table and closing discussion are consistent with those results. The open degree-two attachment problem is distinguished from the resolved unrestricted one-pool hardness questions.

## Sources and limits

I read the reviewer protocol, coverage map, and `literature/AGENTS.md`; examined the cited canonical common-factor/network results and relevant Stage 6 result/investigation files; and checked the applicable earlier manuscript statements. Primary-source checks included Gärtner et al.'s sparse-shadow construction and Khademnia–Davarnia's Appendix, plus De Loera–Onn Theorem 1.1 and the explicit first-layer injection on printed p.816 in the [author-hosted paper](https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf). The latter supports the extra first-layer property used in the canonical network embedding. A direct fetch of the Müller–Scarsini preprint timed out; no independent primary-source claim about its theorem is needed for a finding above.

I independently assessed every new proof in Section 6. I did not reprove every theorem in accepted Sections 1–5 or every deep external conic lower-bound theorem, and did not conduct an exhaustive priority search. No numerical tests were needed for the findings; their evidence is the displayed definitions and source locations.

**Verdict: minor findings only.** No major mathematical defect identified within these checks.
