# Stage 7 author report: complete synthesis and literature positioning

Date: 2026-09-09. Sole author: stage07_author. This report completes the author
assignment; it does not mark stage 7 or the whole paper accepted. No delegation
was used. Stages 1–6 were read as accepted work, with the renewed user instruction
requiring a complete standalone paper and carefully supported novelty.

## Delivered draft

The manuscript is now complete: abstract, keywords, blank authors/date,
introduction, five scoped contribution paragraphs, related work, a comparison
table, notation/roadmap, six substantive sections, conclusion, data/code statement,
four complete supporting appendices and bibliography. The live and isolated
builds each have 77 pages. There are no future-section placeholders.

The contribution overview distinguishes:

1. Complete fixed-dimensional global response compression, polynomial joint
   regimes and original-variable recovery, with explicit common-field and
   attainment scope.
2. Measurement-fiber near-optimal robustness, and a separate exact dense
   screening/recovery theorem with preprocessing excluded from the M*3^t count.
3. Global accuracy-bit optimization, uniform inverse approximation, effective
   sharp 1/P response modulus, rational base-domain recovery and qualified
   response-dependent upper feasibility.
4. Restriction-preserving hardness and arithmetic output boundaries, separate
   from the attributed growing-leader classification and sparse-shadow lemma.
5. Exact scalar implementations and an independent full-task reference solver,
   with no claim that face enumeration, envelopes or contact identities are new.

The introductory model explanation distinguishes many variables of one jointly
optimizing follower from a game between independently strategic followers.
The paper does not claim a calibrated application or industrial superiority.

No theorem or computational algorithm changed. Section 4 attribution was
corrected to give Hochbaum–Shanthikumar full credit for approximating the solution
vector, not merely the allocation objective. Section 6 adds actual full-original
Gardiner–Lucet locators and explicitly credits classical stationary-face
enumeration. Exact proofs, original computational source/data, and the stage 6
measured-version/correction mapping were preserved.

## Literature evidence and novelty scope

I read `literature/AGENTS.md`; generated literature metadata and user originals
were not modified. Repository novelty notes are a search guide only. Their
conclusions were checked against originals and current primary sources, with
root conducting a complementary independent search recorded in
`process/assessments/stage07-root-literature.md`.

### Sources checked directly in this stage

- **Hochbaum–Shanthikumar (1990)**, local original, printed pp. 844, 846–847,
  Sections 1.2–1.3 and Theorem 1.1. Direct original text and rendered p. 847
  confirm solution-vector accuracy, logarithmic precision dependence, numerical
  subdeterminant dependence and the function-value oracle. This prevents an
  incorrect novelty distinction based only on response error versus objective
  error. Our distinction is global upper optimization over all leaders under
  the stated input-bit and fixed-shared-dimension hypotheses.
- **Vigneron (2014)**, local original, Sections 2.1, 2.3 and Theorems 6/9.
  The full text describes nonnegative algebraic terms of constant description
  complexity and FPTAS bounds polynomial in inverse relative accuracy. Section
  2.3 expressly permits the bit model with additional polynomial factors.
  The comparison therefore credits that bit-model treatment; signed upper
  objectives and accuracy-bit dependence are the different joint guarantee.
- **Gardiner–Lucet (2010)**, newly available local user-supplied original,
  printed pp. 470–471 and 478, Propositions 3.1 and 4.3. Text plus rendered
  p. 478 confirm quadratic and linear arithmetic-time convex-envelope methods.
  No rational-bit theorem is imported, and no faster envelope claim is made.
  Earlier access limitations in stage 6 reports remain historical facts.
- **Jeyakumar–Lasserre–Li–Pham (2016)**, local original, Theorem 2.3 and its
  model context. It is the already credited one-sided local solution-set
  regularity predecessor. The manuscript's explicit pairwise structured 1/P
  modulus, varying affine resources and polynomially encoded constant have
  their own complete proof in Appendix C; no new general Hölder theorem is
  attributed to this paper.
- **Giesen–Jaggi–Laue (2012)** and **Giesen–Müller–Laue–Swiercy (2012)**,
  local originals and the repository's source audit. The latter's Lemma 4/
  Theorem 5 retain parameter-range and slope-variation factors. Existing
  parametric-path and optimizer-error methods are credited; the cost-space
  saturation and coefficient-encoding scope are the actual added guarantee.
- **Chen–Ji–Zhang (2026)**, local original first pages and current arXiv v4
  abstract/history, https://arxiv.org/abs/2511.22331v4. It concerns oracle
  complexity for stationarity, not the present global constrained-response
  optimization. Only this precise distinction is cited; none of its rates is
  imported or claimed improved. The arXiv submission date is August 11 even
  though the PDF title page is dated August 12.
- **Flocco–Schiewe–Gabriel (2026)**, actual May 30 primary manuscript,
  https://optimization-online.org/wp-content/uploads/2026/05/Nested_Benders_for_Bilevel_Optimization_Initial_Submission.pdf,
  pp. 1–4, especially model (1). Its LP followers decouple once the leader is
  fixed. The paper receives a short computational-positioning sentence; no
  performance comparison with that different model is made. The bibliography
  uses its primary short permalink https://optimization-online.org/?p=35001.
- **Nie–Wang–Ye (2017)**, actual published original in root's verification
  directory, first pages and global comparison in (1.5), DOI
  10.1137/15M1052172; **Nie–Wang–Ye–Zhong (2021)**, actual published original,
  formulation/approach and Theorem 3.6 context, DOI 10.1137/20M1352375; and
  **Nie–Ye–Zhong (2026)**, actual arXiv:2304.00695v2, Sections 1.2 and 2.2,
  DOI of published work 10.1137/24M1635624. The introductions and sparse
  support decomposition retain original primal follower variables. We credit
  globally quantified comparisons, multiplier expressions, conic support
  reduction and disjunctive models as established. Our blockwise primal
  elimination and polynomial realizable-joint-regime bound supply the
  different fixed-dimensional bit conclusion. The 2026 published bibliographic
  metadata was independently checked by root; no preprint theorem number is
  incorrectly assigned to the published version.
- **Hladík–Černý–Rada (2021)**, actual original arXiv:1911.10877 supplied by
  root, introductory model and stationary-face discussion. The fixed rank is
  that of the whole matrix. Publication metadata was also checked directly at
  https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html, DOI
  10.1007/s11590-021-01711-6. This supports both the fixed-total-rank distinction
  and attribution of the classical face-enumeration baseline principle.
- **Sugishita–Carvalho (2026)** now has an IPCO chapter, DOI
  10.1007/978-3-032-28691-8_28, LNCS 16588, pp. 426–440, confirmed by root from
  publisher/author sources. The original v2 citation remains separately in the
  bibliography because the boundary proof uses its verified Theorem 1 locator.
  Full published chapter access was not claimed.

I also inspected the new local 2026 lifted Lasserre/Wasserstein expectation
paper. It is not a close bilevel predecessor and was not added as an irrelevant
citation. The main exact/block, near-optimal, network-scaling, conditioned-path,
fixed-core and arithmetic source audits remain in the coverage map, with
primary references retained in their theorem sections.

### Current online searches

Queries included:

- `bilevel separable polynomial fixed dimension logarithmic accuracy global optimization`
- `polynomial inverse approximation monotone polynomial bit complexity logarithmic accuracy`
- `bilevel quadratic near identity Hessian NP hard bounded condition number`
- `"separable" "bilevel" "logarithmic" approximation`
- `"bilevel" "Hölder" "polynomial" response`
- `"bilevel" "near identity" hardness`
- `"separable" "bilevel" "fixed" polynomial algorithm`

Results were filtered to actual papers and primary repositories. These searches
identified the contemporary stationarity and nested-decomposition work above,
but no matching complete theorem for the exact quadratic-block or global
accuracy-bit classes. Root's independent search additionally refreshed recent
fixed-dimension bilevel classifications and the important polynomial-bilevel
multiplier-expression lineage.

The manuscript's one “To the best of our knowledge” passage is restricted to
those complete theorem classes, unbounded follower dimension, fixed shared
quantities and specified arithmetic outputs. This is a bounded literature
assessment, not a certification of priority. No first claim is made for global
comparison, KKT/Carathéodory reductions, multiplier arrangements, polynomial
inversion, fixed-dimensional real algebra, convex envelopes, face enumeration,
or transferred W[1]/ETH classifications. The sharp modulus and padded/output
refinements are presented as proved results with precise scope, not as universal
priority claims.

## Consistency and preservation

I read the manuscript's model and semantic definitions, exact construction,
robust/screening arguments, accuracy construction and ledgers, boundary
constructions, inverse and quantitative appendices, fixed-core and path
appendices, scalar algorithms and empirical account. The new overview and
conclusion were checked against the theorem hypotheses and outputs. The
following distinctions remain explicit: XP versus FPT; numerical versus sparse
binary degrees; one selected common field versus all unrelated witnesses;
fixed-normal optimistic attainment versus moving/pessimistic infima; exact
base feasibility versus conditional response-row feasibility; certification
versus proposal success; heterogeneous versus repeated-type populations;
historical versus fresh timings; and exact versus numerical certificates.

An inventory recheck found only two additional path-cut/base-polyhedron notes
outside the coverage list. They concern binary submodular path cuts and a
separate physical pooling-capacity result, so the coverage record now explains
their exclusion from this continuous bilevel paper. The reopened literature
audit is also explicitly mapped to synthesis.

`verification/stage07-author/preservation-check.json` compares scientific inputs
with the immutable stage06-accepted snapshot. The only changed preexisting
scientific source files are Sections 1, 4 and 6 as described above. All other
sections, all appendices, all executable code and all data match byte for byte.
No timings or functional tests were rerun because executable behavior did not
change; stage 6's accepted exact checks and measurement provenance remain valid.

## Validation

- Live `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
  succeeds, 77 pages, with no undefined references/citations, LaTeX/BibTeX
  warnings, overfull boxes or underfull boxes.
- A fresh isolated directory receives exactly 17 required manuscript files and
  successfully builds the same 77-page manuscript without any parent-repository,
  process or verification input. Source SHA256 values, exit status, page count
  and zero-warning result are in `standalone-manifest.json`; its full log is
  `standalone-build.log`.
- Rendered pages 1–6, including the contribution overview and comparison table,
  and page 58 (conclusion) and page 75 (new bibliography entries) were inspected.
  Text, tables and citations fit their pages. The narrow comparison columns
  use ragged-right alignment; a primary short permalink avoids a long-URL
  overflow without changing the source.
- Source scans find no TODO/TBD/future-section placeholder or dependency on an
  internal note for a proof. The phrase “not proved NP-hard” is the intended
  Square Root Sum boundary qualification, not an incomplete claimed proof.
- Source originals used during the audit remain in the literature folder.
  Temporary extracted full texts and source page images are not manuscript
  or submission inputs; copies created for this author audit are removed from
  the paper folder after preserving source hashes. No user-supplied literature
  original is redistributed.

Stage 7 is ready for the required five independent reviews. After its accepted
corrections, the entire manuscript still needs the separately mandated final
five-reviewer process. No known unresolved issue in a claimed theorem is
intentionally deferred to that review.
