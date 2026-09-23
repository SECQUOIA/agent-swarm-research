# Stage 1 literature audit

Review date: 2026-09-09. Scope: the contribution and prior-work claims in the abstract, introduction, Section 2.2, and conclusion of the anonymous network–simplex manuscript. This is a claim-driven review of relevant primary literature, not a proof of absence of every possible predecessor. Mathematical results and computational claims remain subject to the later stages.

## Search and evidence collection

Online search terms used during this stage included:

- `"Convexification of Bilinear Terms over Network Polytopes"`
- `"network" "simplex" "convex hull" "cycle rank"`
- `"network" "bilinear" "observed" "convexification"`
- `"Ideal, non-extended formulations" transportation`
- `"sparse" "bilinear" "simplex" "network" convex hull`
- `"network" "simplex" "Fibonacci" polytope`
- `"A Unifying Convexification Framework" simplex`
- `"bilinear" "cycle rank" polytope`
- `"series-parallel" "bilinear" "convex hull"`
- `Davarnia Richard Tawarmalani 2017 simultaneous convexification pdf`
- `"network polytopes" convexification 2026 2025 sparse`
- `"16M1066166" pdf Davarnia`

Representative raw search returns and primary-page retrievals are saved in `literature/search1.json`, `search2.json`, and `primary1.json` under this revision directory. Those records include discovery hits that were not used as evidence. Technical assertions below are grounded in primary papers or primary publisher/author records, not search-result summaries or third-party literature synopses.

The author research page, https://sites.google.com/view/danialdavarnia/research, was checked for recent relevant work. It lists the Davarnia–Rahimian paper as submitted, so the new bibliography entry explicitly identifies arXiv version 2 as a preprint. The 2026 decision-diagram paper listed on that page concerns graph representations of general MINLPs, not the equality-flow circulation structure here; its existence is not evidence for or against the specific residual-cycle and coefficient statements.

## Sources inspected and claim comparison

### Khademnia and Davarnia, Mathematics of Operations Research 50(2), 1019–1041 (2025)

- DOI: https://doi.org/10.1287/moor.2023.0001.
- Primary full text downloaded from https://par.nsf.gov/servlets/purl/10546393 and retained as `literature/khademnia-published.pdf`. This is the publisher's Articles in Advance version with publication metadata headed 2024 and article page numbers 1–23; the issue citation is 2025.
- The arXiv record https://arxiv.org/abs/2302.14151 and the local full text in `literature/papers/khademnia2025-convexification-of-bilinear-terms-over/` were also inspected. Published numbering is used in the manuscript.
- Published Theorem 1, Section 2: the complete EC&R class gives the hull. This includes the sparse product selection permitted by the model. The paper must not imply that the general multi-label hull was previously unknown.
- Published Section 3, including the paragraph defining positive and negative balance inequalities: equality balances are represented by both signs. The present equality-flow domain is included in that earlier framework.
- Published Theorem 2: explicit tree construction in the one-simplex-variable case. Published Theorem 3: a structured forest construction for several simplex variables. The latter recipe is narrower than the complete Theorem 1 framework. The distinction is stated in Section 2.2.
- Published Example 2, article page 9: a dual aggregation assignment has a multiplier of two. The revised Section 2.2 explicitly credits this precedent. A nonunit multiplier does not alone establish an unavoidable ratio between retained product coefficients in every hull description. The present proofs use coordinate sections and invariance under affine-hull equations to obtain that stronger statement on specified graphs.
- The direct electronic-companion URL returned HTTP 403 in this stage, and web retrieval failed. No new companion-specific assertion is made. The former equation-(25) locator and supplementary footnote were replaced with the directly inspected published Theorem 1.

### Davarnia, Richard, and Tawarmalani (2017), and Davarnia dissertation (2016)

- Journal DOI and publisher abstract: https://epubs.siam.org/doi/10.1137/16M1066166.
- Author repository record: https://optimization-online.org/2017/02/5864/.
- The publisher and author records establish simultaneous convexification of bilinear functions over a general polytope times a simplex. The manuscript claims this established general framework and does not assign a new theorem number to the journal paper.
- Important local-source correction: the file in `literature/papers/davarnia2017-simultaneous-convexification-of-bilinear-functions/original.pdf` is actually the 2016 dissertation. Its title page and extracted text were checked. The local folder name cannot be used as proof of the journal paper's detailed numbering.
- The dissertation was downloaded independently from https://ufdcimages.uflib.ufl.edu/UF/E0/05/02/79/00001/DAVARNIA_D.pdf, retained as `literature/davarnia-dissertation.pdf` and `.txt`.
- Dissertation Proposition 2.6, printed pages 28–29: separate convexification of Cartesian components sharing a simplex is exact. This precise dissertation locator remains in the manuscript. Block gluing is identified as a constructive specialization, not an original general principle.
- Attempts to recover a journal PDF through guessed historical Optimization Online paths did not yield a PDF. The detailed gluing claim is supported by the actual dissertation rather than conflating the two works.

### Liberti and Pantelides, Journal of Global Optimization 36, 161–189 (2006)

- DOI: https://doi.org/10.1007/s10898-006-9005-4.
- Local primary manuscript: `literature/papers/liberti2006-an-exact-reformulation-algorithm-for/original.pdf`; layout text retained as `literature/liberti-pantelides.txt`.
- Theorem 3.1, manuscript pages 7–8: for a full-row-rank system Ax=b with m equations and n variables, multiplied equations allow a selection of n−m product equations to recover the remaining products. Thus product elimination and the underlying rank-nullity fact are established.
- Discussion immediately following Theorem 3.1, manuscript pages 8–10: eliminating bilinear equations does not in general make their McCormick relaxations redundant.
- Present development: identify the relevant nullspace with cycles supported on unobserved arcs; merge unobserved labels separately by circulation block; retain both state and residual capacity bounds; prove unit coefficients after graph-specific elimination. The manuscript's completion count is explicitly restricted to individual-product completion on the ambient circulation space, not arbitrary extension complexity.

### Kis and Horváth, Mathematical Programming 194, 831–869 (2022)

- DOI and primary full text: https://link.springer.com/article/10.1007/s10107-021-01652-z.
- Local PDF and extraction: `literature/papers/kis2022-ideal-non-extended-formulations-for/`; layout extraction retained as `literature/kis-horvath.txt` in this revision.
- Sections 5.7 and 5.9: network representations of simplex/Cayley disjunctions and transportation projection.
- Section 5.9, Proposition 22, equations (30)–(31): lower-bound shift, a feasible transportation flow characterization, and complete cut inequalities. These are close precedents for the present parallel-path separator.
- Present development: specialize these established operations to observed state slices, including recovery. The paper does not claim a new transportation-cut theorem.

### Minkowski sums and zonotope refinements

- Gritzmann and Sturmfels (1993), https://doi.org/10.1137/0406019; local primary PDF in `literature/papers/gritzmann1993-minkowski-addition-of-polytopes-computational/`.
- Onn and Rothblum (2004), https://doi.org/10.1007/s00454-004-1138-y; open preprint https://arxiv.org/abs/math/0309083.
- Gritzmann–Sturmfels Lemmas 2.1.4–2.1.5 identify support faces of sums and the common refinement of normal fans; the corresponding local full-text passages were read. The Onn–Rothblum open primary PDF was downloaded to `literature/onn-rothblum.pdf` and extracted to `.txt`. General support geometry and refinements by finitely many edge directions are credited as established. The novelty claim is limited to the manuscript's graph-specific complete libraries, coefficient control from the totally unimodular cycle matrix, stated separation and recovery bounds, and treatment of all state slices. This stage did not redo the full bounded-rank proof; that belongs to Stage 2.

### De Loera and Onn, SIAM Journal on Optimization 17(3), 806–821 (2006)

- DOI: https://doi.org/10.1137/040610623.
- Author-hosted primary PDF downloaded from https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf and retained as `literature/deloera-onn.pdf` and `.txt`.
- Theorem 1.1, printed pages 807–808: universality of slim three-way transportation polytopes, with a coordinate-erasing bijection.
- Theorem 1.2 and accompanying discussion, printed page 808: bitransportation universality and its two-commodity-flow interpretation are already known.
- Section 3.3, printed page 816: the coordinate injection places retained coordinates in one layer; this is the ingredient cited in the manuscript's transfer proof.
- Present development: fix all original sparse-hull coordinates except selected actual product cells, with two explicit simplex labels and a common unit network normalization. Neither transportation universality nor two-commodity universality is claimed as new.

### General coefficient and facet-transfer precedents

- Alon and Vu (1997), https://doi.org/10.1006/jcta.1997.2780, author PDF https://web.math.princeton.edu/~nalon/PDFS/av1.pdf: large coefficients for 0/1 polytopes are classical.
- Fiorini (2006), https://doi.org/10.1016/j.disopt.2005.10.007, author PDF https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf: transfers of facets to graph polytopes are established.
- These are retained as general precedents rather than independent new priority claims. The manuscript's exact restricted graph and coordinate conditions are essential to its stated originality. This stage did not independently reprove these classical results.

### Almoghrabi, Skutella, and Warode (2026)

- Published DOI: https://doi.org/10.1007/s10107-026-02392-8.
- Local primary PDF: `literature/papers/almoghrabi2026-integer-and-unsplittable-multiflows-in/original.pdf`; text retained as `literature/almoghrabi-et-al.txt`.
- The remark after the first main theorem distinguishes total arc flow integrality from decomposition of the full vector of individual commodity flows. The local preprint labels the remark without a number; the published Remark 1 locator was independently verified on the publisher full-text page on 2026-09-09.
- This distinction is relevant because retained products encode individual-state flows. It does not prove the coefficient theorems here, but prevents an incorrect inference from aggregate series–parallel integrality.

### Davarnia and Rahimian, arXiv:2510.15861v2 (11 August 2026)

- Primary versioned record: https://arxiv.org/abs/2510.15861v2.
- Primary HTML: https://arxiv.org/html/2510.15861v2.
- PDF downloaded from https://arxiv.org/pdf/2510.15861v2 and retained as `literature/davarnia-rahimian-v2.pdf` and `.txt`.
- Current title: *A Unifying Convexification Framework for Chance-Constrained Programs with Finite Support via Bilinear Formulations over a Simplex*. The older initial-version title differs, so the current version's full title is used.
- Introduction, printed pages 3–4, and Section 3: the simplex variables are binary; products occur in constraints; the target hull is projected into x-space. The paper develops a general aggregation method and applications to mixing sets. These are a related current development, but do not establish the present graph-specific residual-coordinate count, fixed-label threshold, or restricted coefficient obstructions.
- New entry `DavarniaRahimian2026` explicitly says preprint, version 2, August 11, 2026. The author research page still labels it submitted; no journal publication is inferred from the PDF's manuscript-number field.

### Adjacent graph-bilinear literature screened

The primary publisher page for Gupte, Kalinowski, Rigterink, and Waterer, *Extended formulations for convex hulls of some bilinear functions*, Discrete Optimization 36 (2020), article 100569, https://doi.org/10.1016/j.disopt.2020.100569, was inspected during search. Its domain is the unit cube and the graph encodes monomials of a scalar bilinear function; cycles there are interaction-graph cycles, unlike cycles of an equality-flow domain. It was not added merely for keyword overlap.

## Resulting novelty assessment and limits

No directly matching theorem for the manuscript's residual-cycle formulation with coefficient control, its stated complete structural libraries and parameter bounds, the three-versus-four observed-label threshold on flat chains, or its sparse coordinate-preserving coefficient constructions was identified in this search and primary-source comparison. The introduction uses a single qualified “To the best of our knowledge” statement tied to those exact outputs and the detailed comparison table. It does not claim priority for general hull existence, disaggregation, polynomial separation, rank-nullity/product elimination, transportation projection, support refinements, or universality.

This evidence supports a qualified literature position. It is not exhaustive priority certification, and the mathematical validity of the specific results still requires the prescribed independent review. The online search is limited by indexing and access. Inaccessible journal/full-supplement sources were not represented as inspected full text. The source-integrity issues in the local knowledge base were recorded here without altering that separate collection.

## Additional root screening during the mathematical stage

On September 9, targeted online searches for network/simplex bilinear cycle-rank
results and Fibonacci coefficient obstructions returned the cited KD paper and
three adjacent primary sources. Their publisher abstracts/introduction were
inspected; this was a relevance screen, not a complete theorem audit. Raw tool
returns are in literature/root-additional-screening.json.

- Tawarmalani, *New finite relaxation hierarchies for concavo-convex, disjoint
  bilinear programs, and facial disjunctions*, Mathematical Programming 218,
  5–55 (2026), DOI 10.1007/s10107-026-02326-4. General barycentric/disjunctive
  hierarchy work; the introduction explains finite convergence and vertex
  representations. Our manuscript already credits generic disaggregation and
  makes no priority claim for general constructive convexification. The screened
  material provides no specific overlap with unobserved-cycle counts or the
  graph/label coefficient thresholds; no extra citation is necessary for the
  focused comparison. This is not a claim of exhaustive nonoverlap.
- Dey, Han and Wang, *Aggregation of bilinear bipartite equality constraints and
  its application to structural model updating problem*, Journal of Global
  Optimization 94, 1099–1135 (2026), DOI 10.1007/s10898-026-01607-8. Its model
  imposes two general bilinear equations on box variables and studies convexified
  aggregations; it does not use the equality-flow/shared-simplex component model
  of this manuscript. This is adjacent aggregation context, not the closest
  predecessor of the claimed structural results.
- Bärmann and Schneider, *Set characterizations and convex extensions for
  geometric convex-hull proofs*, Mathematical Programming 195, 475–515 (2022),
  DOI 10.1007/s10107-021-01705-3. General set-characterization methods extend
  constructive hull proofs to arbitrary polytopes and bilinear functions. Our
  constructive novelty claims are restricted to the stated network support and
  recovery libraries and their parameter bounds, not constructive hull proofs
  in general. A further general-background citation is optional, not essential.

This additional screen did not change the accepted precise contribution claims.
The strongest directly comparable literature remains the sources audited above.
