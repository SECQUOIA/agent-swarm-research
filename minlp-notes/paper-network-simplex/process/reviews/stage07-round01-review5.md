# Stage 7, round 1 — independent review 5

**Verdict: no major or minor findings.** The completed framing accurately describes the proved results, the new integral-flow corollary is correct, and the new literature comparisons and presentation are suitable for this stage. I recommend accepting Stage 7 and proceeding to the required separate whole-manuscript review.

I reviewed the complete assigned Stage 7 changes in the frozen `process/snapshots/stage07-round01/`, compared them with `stage06-accepted` and `verification/stage07/source.diff`, and inspected their interfaces to the accepted proofs and computational evidence. I read the review guidance, author record, coverage map, validation manifest, README, and historical pointers. I did not read another current-round report, coordinate judgments, spawn agents, or edit shared sources. Evidence is confined to `verification/stage07-review5/`.

## Mathematical and scientific assessment

The new abstract, introduction, structural scope table, and conclusion consistently distinguish the following claims:

- The sum of unobserved-subgraph cycle ranks is the residual-coordinate count of the supplied construction. It is not an extension-complexity lower bound. The minimum individual-product completion statement has the stated ambient-circulation-space scope and concerns labels already observed in each block.
- The finite bounded-rank separation and recovery bounds have different parameter factors, `2^{O(r^2)}` and `2^{O(r^3)}`. The introduction retains the observation-grouping qualification and calls the output compact, rather than implying a bound independent of the cost of materializing all global state flows.
- Unit coefficients concern flow/product coordinates in the specified row scaling. Simplex coefficients can contain rational data. The scope-table caption prevents primitive-integer normalization from being confused with the stated bound.
- The rank-three sharpness refers to the coefficient bound, supported by the two-label, five-product K4 example. It does not claim that five products are a proved minimum observation count.
- The flat-chain threshold concerns the specified directed unit-data topology, arbitrary observations, and at most three labels observed anywhere. Four labels can fail. The text does not extend this threshold to arbitrary nested series–parallel networks or to the unrestricted two-label universality construction.
- The two-label five-test description comes after local checks and bound grouping. Three-label separation uses sixteen positive circuits and the two balance repairs. These summaries match the detailed accepted statements and their coefficient analysis.
- The sparse Fibonacci construction permits a growing number of labels and has a simple maximum-degree-three realization. The conclusion correctly infers that bounded treewidth alone is insufficient for a uniform coefficient bound. It separately states that a small label count alone is insufficient on unrestricted networks. Neither implication claims separation hardness or large extension complexity.

I checked the cited theorem locators and the relevant detailed statements in compression, bounded rank, universality, series–parallel growth, and observed-label chain recovery. No new overstatement or incompatible normalization was found.

### Integral-flow corollary

`sections/01-foundations.tex`, `cor:integral-flows`, has a complete argument. At a nonintegral feasible flow, the nonintegral-arc subgraph either contains a loop or has no incident vertex of degree one, since all other balance terms and the balance itself are integral. A finite nonempty loop-free multigraph with that property contains an undirected cycle, including a two-edge parallel cycle. Its signed circulation gives a nonzero two-sided perturbation supported only on nonintegral arcs. Those arcs lie strictly between their integral bounds. Consequently the point is not a vertex. Boundedness then gives an integral-vertex decomposition for every feasible flow.

Refining each positive simplex state's normalized flow into those integral vertices preserves its selected products, since the products are linear in flow when the simplex vertex is fixed. The refined weights reproduce the original x, y, and z. Zero states need no normalization or refinement; empty flow domains have empty hulls. This proves both inclusions of the stated equality.

The explanatory paragraph correctly limits the claim: the compact at-most-m+1 decomposition into continuous graph points need not have integral flows, and fractional coordinate sections need not be integral. This is especially helpful next to the later coordinate-section universality results. The result is properly presented as classical rather than a new integrality theorem.

For independent executable evidence, I wrote a different verification from the author's vertex enumeration. `independent_integral.py` recursively perturbs rational flows along a null direction supported on nonintegral arcs, decomposes each point into the two resulting bound endpoints, and continues until the flows are integral. It uses exact Fraction/SymPy arithmetic, no LP, and no production oracle. On 20 oriented multigraphs with loops, parallel arcs, and an isolated vertex, it exactly refined 80 normalized flows and checked 60 original graph-point mixtures, with simplex sizes zero, one, and three and a zero-weight state. It encountered 404 integral terminal flows. All aggregate, simplex, observed-product, and convex-weight identities passed.

I also ran a private copy of the author's exact check: 18 multigraphs, 78 integral vertices, 54 exact refined decompositions, empty and zero-dimensional cases, and the m=0 decomposition-count counterexample passed. These finite checks supplement the proof; they are not its justification.

## Literature, implementation interfaces, and coverage

The new Fiorini comparison is supported by the [open author manuscript](https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf): its abstract and introduction explicitly describe transforming 0/1-polytope facets into acyclic-subgraph facets. The paper appropriately distinguishes its own sparse bilinear coordinate sections and does not claim facet transfer or large graph-polytope coefficients as new general phenomena. I also checked the new journal year, volume, issue, pages, and DOI against the [publisher record](https://www.sciencedirect.com/science/article/pii/S1572528606000168).

The [Hoffman–Kruskal primary reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/kruskalhoffman.pdf) supports the integrality attribution. Its PDF page 4 explicitly identifies the original 1956 publication, editors, publisher, and pages 223–246. The bibliography correctly uses the original publication rather than the reprint's date. The supplied direct proof avoids dependence on an unstated imported result.

I checked Khademnia–Davarnia Section 4.2 in the repository's full text. It does introduce route/service cost products in transportation with conflicting services. The new computation paragraph explicitly calls the present model a two-supplier specialization with a common simplex. It does not suggest that the predecessor used exactly that restriction. The common-domain assumptions and the limitations of adding external constraints remain explicit.

The new introduction's computational counts and rounded times match the accepted data: 7,215 full/global state-flow variables versus 495 and 367 total compressed variables, with approximately 30 ms versus 10 ms for full and initial compression on the all-labels-observed control. The introduction and conclusion retain the stronger global-merger baseline and the negative long-chain runtime finding. They do not replace exact certificates with numerical feasibility or imply industrial validation. The revised provenance paragraph removes process chronology while retaining the scientifically relevant distinction between the measurement collections and their reproducible archived sources.

The coverage map now has the intended final locators. The README distinguishes current results from the earlier 41-circuit oracle, older K4 examples, and superseded runtime assessments. The two added historical-note pointers preserve the older investigations while making their status clear. No material source-development omission was identified in the assigned integration stage.

## Reproduction and visual presentation

My `check_stage07.py` verified all **88 manifest hashes**, **193 unique labels** and their references, **21 bibliography keys** and cited-key resolution, README links, all **483 stored timing summaries**, and the new introductory numerical claims. No production code or accepted benchmark was altered by this stage.

A private snapshot copy built to **48 pages** with no final warnings, undefined references/citations, or overfull/underfull boxes. I inspected rendered pages 1–3, 30, and 46. The abstract is dense but readable; the contribution list gives useful distinctions; the scope table is legible and has working locators. The G4 diagram has the correct five vertices, eight serial-pair arcs, forward bypass, and shared state-profile equations. It appears after the topology and profile are defined. The conclusion fits the preceding results, and the reproduction command remains correctly formatted.

## Findings and limitations

**Enumerated findings: none.** No optional preference is a condition for acceptance.

This is a review of the complete Stage 7 additions and their integration, not a replacement for the next mandated whole-paper review. I inspected relevant accepted theorem interfaces but did not repeat every earlier proof audit or rerun the unchanged production benchmark suite. The new integral-flow argument received an independent proof check and exact constructive verification. The additional literature checks establish the accuracy of these comparisons, not absolute priority or an exhaustive search for all prior work. Shared-host timing and numerical-solver limitations remain those already disclosed in the manuscript.
