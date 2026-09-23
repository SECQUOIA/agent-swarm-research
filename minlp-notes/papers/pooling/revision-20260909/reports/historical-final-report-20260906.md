# Pooling paper: completion report

**Complete.** The final full-paper round has no accepted findings, and every accepted issue from earlier rounds is resolved. The process comprised 150 independent full reviews across ten rounds, with eight separate repair passes.

The manuscript is [The Complexity of Pooling: Algebraic Barriers and Structural Algorithms](main.pdf). Its [LaTeX driver](main.tex) includes an introduction and six substantive sections. The current PDF has 91 pages, 80 proof environments plus intervening arguments, and 49 references. [README.md](README.md) gives build commands and verification dependencies.

## Coverage and organization

The paper develops the repository's pooling research through six stages:

1. Physical models, exact arithmetic, destination decomposition, profitable-flow tests, cyclic steady-state models, conic hulls, and facial integrality.
2. Existential-real completeness, finite-data and one-pool refinements, algebraic witnesses, and basis-index NP certificates.
3. Degree and size restrictions, approximation barriers, positive tolerance, two-pool reductions, physical copy circuits, exact penalties, constant-data hardness, and five contract exceptions.
4. A fixed nonlinear core with independent polyhedral blocks, affine quality rank, bypass vertex integrity, planar composition, and bounded attachments.
5. Exact contracts, receiving products, signed quality-scaled flows, bounded exceptions, restrictive common capacities, throughput optimization, and two complete source-quality vectors.
6. Physical price-response geometry, isolated and strict local optima, exact LP hulls, low-interaction-rank costs, related convexification and network results, and precise open boundaries.

The [coverage inventory](process/coverage.md) identifies 295 source or supporting files and seven directories. It maps all 116 pooling-named result/note files and all 31 canonical results in the pooling, rank-one, common-factor and network-simplex families. These counts support the substantive review; filename matching alone is not evidence of mathematical completeness. Distinct restrictions are retained even when a stronger theorem supersedes an earlier argument. Adjacent conic, common-factor, network-simplex and power-flow programs receive scoped discussion and references, rather than unrelated full papers being inserted into this pooling manuscript. The [source index](source-index.md) gives exact titles, paths and SHA256 hashes for thirteen cited repository notes.

## Development and verification during writing

The work went beyond converting notes to LaTeX. The author and root records describe the derivations and independent checks. Notable completions and corrections include:

- Completed the output-count approximation and attainment argument for the stated cyclic algebraic model by handling isolated circulations explicitly.
- Corrected the missing concentration denominator in the historical small irrational example and supplied a global optimality proof in the paper. The original explanatory script is identified in the coverage audit as historical evidence, not silently treated as a correct proof.
- Verified the compact basic-closed route needed for algebraic singleton transfer, avoiding a broader source transformation whose inactive disjunction auxiliaries need not be unique. Exact symbolic and interval checks support the arithmetic diagrams actually used.
- Replaced an invalid arbitrary-parameter estimate in the consulted Matsui report with a complete proof for the large-parameter family required by the reductions. The comparison is explicitly limited to that report version.
- Completed the bounded-signal binary row construction, including intermediate bounds, gate occurrences, physical threshold encoding, and the constant-data/five-exception audit.
- Completed computable core and aggregate-slack bounds for compact formula-defined cores, with polynomial bit bounds and exact common-field recovery.
- Developed exact minimum and maximum pool throughput, and a linear pool-processing cost extension, from the common-capacity support construction. This does not claim arbitrary routing-cost optimization.
- Supplied a self-contained telescoping shadow direction, explicit physical economics and penalties, and careful distinctions among exponential response descriptions, local-optimum geometry, and polynomial optimization through an exact LP hull.
- Added independent exact checks for interaction-rank-two projected candidates and original physical interface constraints. Final coverage review also recovered the separate zero-lower/unit-upper margin-cost hardness refinement and verified its penalty argument.

These are improvements made in preparing this manuscript. They are not an assertion that every tool or intermediate observation is new to the literature.

## Author, review, and repair protocol

Each stage had one assigned author, followed by fifteen independent reviewers of the entire stage. Supplementary focus assignments did not replace whole-stage reading. Root read every report, assessed mathematical reasons and counterexamples, and assigned accepted repairs to a different agent. Accepted major findings triggered another full fifteen-reviewer stage round before advancing. The whole-paper phase repeats after any accepted finding, including minor findings.

| Stage | Completed full rounds | Completed reviews | Separate repair passes |
|---|---:|---:|---:|
| 1 — foundations | 2 | 30 | 2 |
| 2 — algebraic complexity | 1 | 15 | 1 |
| 3 — restricted hardness | 2 | 30 | 1 |
| 4 — structural algorithms | 1 | 15 | 1 |
| 5 — contract algorithms | 1 | 15 | 1 |
| 6 — synthesis and introduction | 1 | 15 | 1 |
| Whole paper | 2 | 30 | 1 |
| **Total** | **10** | **150** | **8** |

The two accepted major stage findings concerned essential upper-quality-only hypotheses: first in the endpoint disjunction, then in the restricted NP-completeness statements using its certificate. Both were repaired and received another complete stage review. Other accepted corrections concerned bounds, objective and certificate wording, degenerate products, source attribution, citation versions, and reproducible source locators.

Whole-paper round 1 produced fourteen no-findings reports and one minor related-result coverage finding. Root accepted the missing zero-lower/unit-upper margin-cost restriction, checked its proof, and assigned a separate repair. The corrected entire paper then received a fresh fifteen-reviewer round. All fifteen reports had no findings, and root accepted no new issue. Interrupted unfinished reviews were resumed and counted only after their reports were complete.

The full chronological record is in [process/status.md](process/status.md). Frozen drafts, individual reports, adjudications, exact repair diffs and validation records are retained under [process/](process/).

## Computational and source evidence

Finite exact checks and numerical experiments are distinguished throughout the audits. Representative retained evidence includes:

| Area | Evidence and scope |
|---|---|
| Foundations | 240 exact cyclic decompositions, 80 conditioning examples, 406 nonfacial witnesses, and endpoint-scope checks with a rejected lower-quality counterexample. |
| Algebraic constructions | 104 exact one-pool physical witnesses covering 980 equations and 1,775 pins; bounded-chain cases; exact diagram identities and full-box rational interval enclosures. |
| Restricted hardness | Exact source-bound, copy/averaging, penalty and tolerance checks; independent numerical physical LP and nonlinear models for degree restrictions, constant data and five exceptions. |
| Structural and contract algorithms | Exact arc ownership, planar composition, scalar/vector cut identities, binary clamp, divergence-support and strip checks; separate numerical physical feasibility comparisons. These are not full implementations of general quantifier elimination. |
| Response and geometry | 8,190 vertex/exposure checks, 2,044 distinct local-optimum values and 18,432 directed-edge derivative checks; exact slab/padding checks; 4,482 exact original physical reconstruction cases. |
| Cost rank and new coverage refinement | 24 interaction-rank-two instances and 104 rational slices, with 342 exact exposing and eight exact convex-combination certificates; 2,000 exact saturated-margin repair/penalty cases. |

The final full-paper reviewers added 1,200 exact integer-flow/cut comparisons (177 feasible cases also checked greedy support), three symbolic residual-equation identities, 252 interface/exposure cases and 972 small slab comparisons. Their scripts and outputs are retained beside their reports.

Commands, dependencies, per-check limitations and logs are linked from [README.md](README.md) and the stage root audits. Numerical solver agreement is not described as an exact proof. Finite tests are not used to establish universal complexity bounds. Unchanged passing suites were not repeatedly run to inflate validation counts.

Primary-source work used original papers where available, with version-specific locators. The local Dey–Gupte package contained slides, so article claims were checked against the actual article. The ETR, Matsui, algebraic-LP, conic, transportation and network-disaggregation sources retain their inspected-version qualifications. Source PDFs were not redistributed in the manuscript folder. Literature priority assessments remain limited to the sources and searches actually examined.

## Build and artifact checks

The workspace force build and an independent source-only build both succeeded at 91 pages, with identical extracted PDF text. A negative control that removed a required section failed compilation as intended. The driver cannot silently compile an incomplete paper.

Root inspected all 91 revised pages for layout, plus enlarged views of the repaired paragraph and new reference. No clipping or overlapping content was found. All 245 labels and 305 reference uses resolve; all 49 bibliography keys are cited; all thirteen indexed note hashes match. The build has no unresolved references/citations or overfull boxes. Eight mild underfull bibliography diagnostics are visually acceptable. Two empty-year BibTeX warnings retain honestly undated consulted sources.

Exact source and PDF hashes and check results are recorded in [verification/final-validation.json](verification/final-validation.json). Build evidence is in [verification/logs/](verification/logs/); the independent final artifact audit is [process/whole-round-02/root-check.md](process/whole-round-02/root-check.md).

## Remaining research and publication scope

The paper explicitly leaves open the unrestricted fixed-pool, fixed-quality-rank, degree-two-bypass setting with unbounded attachments and general interval contracts. It does not assert one-upper-attribute existential-real hardness, combine incompatible contract/capacity hypotheses, or infer algorithmic hardness from exponential geometry alone. These are stated research boundaries, not missing premises in the selected theorems.

The manuscript uses a general article format and leaves authorship blank because no author information was supplied. Journal-specific formatting and submission are outside this task. Internal agent reviews and exact finite checks cannot guarantee external acceptance, establish exhaustive priority, or rule out every possible future referee finding. The final internal review found no issue requiring a manuscript change. That is the review outcome, not a guarantee against future findings.
