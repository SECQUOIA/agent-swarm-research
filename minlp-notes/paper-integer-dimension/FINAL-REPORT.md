> Historical preparation record. The September 2026 submission revision and
> its current review status are recorded in
> [revision-20260907/PROCESS.md](revision-20260907/PROCESS.md).

# Paper preparation report

The paper is **Integer Dimension in Convex Mixed-Integer Approximation of Nonlinear Graphs**, in [main.tex](main.tex), with the compiled version in [build/main.pdf](build/main.pdf). It uses the standard article class and leaves author metadata blank. The scope is the repository's integer-dimension research program, including its quadratic foundation and nonlinear extensions.

**Completed:** all four drafting stages and the mandatory fifteen-agent whole-paper review passed. Root read and adjudicated all **75 reports**. The final round found **zero major and zero minor issues**; no accepted issue remains. The final 84-page PDF compiles cleanly and matches the inspected version.

## Coverage and mathematical development

[coverage.md](coverage.md) maps 43 canonical result files and 34 distinct substantive supporting developments into the paper. It also indexes 196 research notes, predecessor variants and historical audits. The 273 source links represent 239 distinct repository files; every link and all 119 explicit theorem/equation mappings resolve. Historical audit verdicts were treated as leads to inspect, not as proof. Unrelated repository topics are outside this paper's scope.

The mathematical sequence covers:

1. Convex graph lifts, contact/parity lower bounds, scalar and bilinear laws, quadratic noncommutative rank, smooth constant-rank laws and perspective transfer.
2. Finite-accuracy covariance characterization, rational constructions and certificates, general error bodies, effective input rank, structured quadratic refinements and approximation hardness.
3. Scalar curvature geometry, certified integration and implicit compilation, positive powers and dense/sparse polynomials, separable comparisons, relative error and the rational MILP/SOC encoding separation.
4. Coupled vector outputs, shared curvature bases and oracle bodies, separable vector packing, exact binary/general-integer separations, nonconvex constructions and remaining boundaries.

The work goes beyond transcription. Proofs were reconstructed, input and error models were made consistent, distinct precursor arguments were retained, and computational assertions were separated from real-coefficient existence. Examples of completed or clarified details include the full rational nc-rank bit argument; exact rational covariance-certificate assumptions; original-coordinate gradient conjugation; explicit enclosing-domain and Taylor budgets; rational-tolerance promises in compilation; fixed-denominator spanner repairs and image-preserving rounding; whole-section validity in the exact convex product construction; and the extension of the finite inner/outer-ball comparison to nonsymmetric convex permitted-error sets. These are manuscript developments and corrections, not a claim that every ingredient is new in the literature.

The paper explicitly leaves unresolved the universal constant additive gap for one-input convex vector graphs with box error, rank-changing smooth scalar cases, and the compact mixed-coordinate nonlinear vector extension. It does not infer necessary logarithmic overheads from upper bounds alone.

## Requested review process

Each stage had one author. Only after that author stopped did fifteen agents independently review the completed stage, using different additional lenses. Root read every complete report, checked the reasoning behind findings, consolidated overlapping corrections and assigned a separate correction agent. Root inspected the complete resulting patch and validation evidence before releasing the next stage.

| Stage | Review reports | Reported major | Reported minor | Accepted correction actions | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| 1: foundations | 15 | 0 | 35 | 9 consolidated | Passed after separate correction |
| 2: finite quadratic theory | 15 | 0 | 8 | 5 consolidated | Passed after separate correction |
| 3: scalar theory and encoding | 15 | 0 | 3 | 2 consolidated | Passed after separate correction |
| 4: vector theory and synthesis | 15 | 0 | 0 | 1 root layout finding | Passed after separate correction |
| 5: whole paper | 15 | 0 | 0 | 0 | Passed; no correction required |

The 46 stage-review minor findings include overlapping reports of the same issues. They are not 46 distinct defects. The separate root layout finding concerned a one-word paragraph widow; a standard TeX penalty fixed it without changing mathematical text. No stage had an accepted major issue, so the requested major-triggered repeat rounds were not needed at those gates.

The final review covered the entire manuscript, including cross-section consistency, coverage, source credit and exposition. Its rule was stricter: any accepted correction, including a minor correction, would trigger another full fifteen-agent round. All fifteen final reviewers reported zero major/minor findings and no unresolved review question. Root accepted no additional correction, so no repeat round was required. In total there were 75 reports, four separate correction passes and 17 consolidated correction actions.

Usage limits interrupted root during the final report-reading step. On resumption, root completed the last unread report, recorded the remaining completed reads, verified the reviewed sources and PDF, and finished adjudication. The interruption did not bypass any stage or reviewer.

All report texts, source snapshots, SHA-256 hashes and root decisions are in [reviews/](reviews/). [PROCESS.md](PROCESS.md) records the gates. Separate correction reports and independent root source audits are in [verification/](verification/).

## Validation and literature

The four recorded core check runs contain **46 successful executions of 45 distinct scripts**: 7 in stage 1, 13 in stage 2, 17 in stage 3 and 9 in stage 4. One allocation checker is used in two stages. [The reconciliation record](verification/core-check-reconciliation.json) confirms that all passed and their source hashes still match. These are exact and numerical supporting checks, not proof verification or an implementation of the complete compiler and oracle algorithms. Additional focused author, reviewer and correction-agent checks are documented in their reports, including exact LP, interpolation, certificate, overlay, packing, spanner and separation cases.

The literature audit used local primary PDFs and targeted retrieval of original papers. It checked the hypotheses of consequential imported rank/capacity, optimization, approximation, encoding and combinatorial results, and credited close predecessors for parity, disjunctions, shared SOS2 breakpoints, barycentric spanners, approximate-oracle access and related methods. The audit records identify the passages actually read, URLs, downloaded-file hashes and retrieval failures. This is a bounded source audit, not an exhaustive novelty search. Original research and literature files were preserved.

The final PDF has **84 pages**, **258 resolved labels** and **39 bibliography entries**. The build and reference checks pass, with no warning, undefined-reference or overfull/underfull messages in the final TeX log. Root inspected every page for layout through contact sheets, with higher-resolution samples; the author inspected the new vector mathematics pages separately. After the widow correction, all 84 page renderings were compared and only pages 5–6 changed; root inspected both. Automated text bounds show no blank text page, off-page word or word within 30 points of a horizontal edge. [The layout record](verification/pdf-layout-review.md) states the inspection scope.

Rebuild and rerun instructions are in [README.md](README.md). The environment record distinguishes the actual Python interpreters used in the dated check runs. The standard LaTeX source, bibliography, compiled PDF and review evidence remain in this new folder. [The final validation record](verification/final-validation.json) identifies the delivered source/PDF hashes and clean checks.

## Assessment and limits

The intended standard is a self-contained research paper with explicit assumptions, complete contribution proofs and accurate source credit. Internal agent review, numerical checks and PDF inspection cannot guarantee correctness, exhaustive priority or journal acceptance. No accepted mathematical, coverage, citation or presentation issue remains after this process. The paper's length reflects the requested comprehensive scope; journal selection and a journal-specific template are intentionally left open.
