# Stage 1 author report

Completed 2026-09-09. Scope: literature-based positioning and exposition, with the manuscript kept anonymous. No theorem statement, proof, algorithm, experiment, historical review record, or prior verification artifact was changed.

## Manuscript changes

- `main.tex`: rewrote the abstract around the known disaggregation baseline, the observation-sensitive formulation, complete structural oracles, and coefficient boundaries. Removed specialized five-test/16-circuit implementation detail from the abstract. Explicitly identifies which observed labels contribute residual coordinates and distinguishes formulation-size evidence from runtime evidence. Author and date fields remain empty.
- `sections/00-introduction.tex`: places the closest predecessors in the opening discussion. Explains the conceptual difference between graph size and unobserved circulation freedom and gives the simple-cycle interpretation. Organizes contributions into three levels: the exact formulation; complete separation and recovery with structural bounds; and sharp coefficient boundaries. Makes the scientific importance explicit: smaller exact representations, complete certificates, and precise limits on simple projected inequalities. Adds a qualified novelty statement tied to the specific results and a comparison-table reference. Preserves normalization, extension-complexity, equality-domain, and flat-chain scope qualifications. Numerical claims remain unchanged.
- `sections/01-foundations.tex`, Section 2.2 only: rewrote the prior-work comparison around inspected primary sources. Credits KD's complete Theorem 1, distinguishes its tree/forest recipes, adds its published Example 2 as a precedent for nonunit aggregation weights, and explains why the present unavoidable product ratios are a different claim. Credits Davarnia's dissertation gluing proposition and Liberti–Pantelides product elimination including the warning about eliminated relaxations. Gives the close transportation-projection locators and delineates the universality transfer. Adds the current Davarnia–Rahimian preprint and a four-row established-ingredient/development comparison table with theorem references.
- `sections/09-conclusion.tex`: explains what the results enable for modeling and exact verification, while preserving the boundaries on direct coefficient descriptions, runtime evidence, side constraints, and general nested series–parallel networks.
- `references.bib`: adds `DavarniaRahimian2026`, explicitly a versioned preprint dated 11 August 2026, with the version-2 title and stable arXiv URL.

## Literature work

See `literature-audit.md` for search terms, retrieval date, primary URLs, inspected passages, claim comparisons, and access limitations. Newly downloaded PDFs and text extracts are under `literature/`; raw representative web returns and SHA-256 hashes are retained there.

Two distinctions materially improved the revision:

1. KD's published Example 2 already contains a nonunit dual multiplier. The manuscript now credits this directly and restricts originality to invariant product-coefficient ratios on the specified sparse hulls.
2. The local folder labeled as the 2017 Davarnia–Richard–Tawarmalani paper actually contains the 2016 dissertation. The manuscript uses the dissertation's actual Proposition 2.6 locator, and attributes only the general simultaneous-convexification framework to the journal article based on its publisher/author records. No false journal-specific locator was introduced.

The inaccessible KD electronic-companion equation locator was removed from the prior-work discussion; published Theorem 1 supplies direct evidence for general completeness. The new Davarnia–Rahimian version was checked in primary full text and is related through aggregation, but its binary simplex and x-space target do not establish the specific structural results here.

## Verification performed

- Built a private source copy in `stage1-build/` with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- Final private build: 49 pages, 610,933 bytes; no LaTeX warnings, unresolved references/citations, overfull boxes, or underfull boxes in `main.log`.
- Read the rendered PDF's extracted layout for the first six pages to check opening flow, theorem references, contribution hierarchy, and table content.
- `git diff --check` passes for all five edited manuscript files.
- Compared each edited manuscript source against the private build input; all five match.
- No code tests were run because this stage changes no executable behavior. The later stages must perform the mathematical and computational verification requested by the user.

Initial private-build setup omitted the tables directory; after copying all manuscript input directories, the clean build succeeded. A first latexmk invocation from the repository root found no main.tex and produced only a temporary log that was removed. Neither failure was a manuscript defect.

## Remaining review scope

I found no new mathematical defect in the targeted explanatory passages. I did not perform the Stage 2 proof-by-proof audit, so this report is not acceptance of the mathematical claims. Particular high-value checks remain the bounded-rank coefficient estimate and recovery complexity; all zero-weight and degenerate slice cases; the proof that coordinate sections force ratios invariant under affine-hull equations; and complete three-label flat-chain circuit/flow-balance repair enumeration. The stage text makes no assumption that these checks are already passed.

The new comparison table and qualified novelty wording should be judged by the five independent Stage 1 reviewers. The finite online search and source comparison support the restricted position stated, not an absolute priority guarantee. Published Almoghrabi–Skutella–Warode Remark 1 was independently checked on the publisher full-text page; its local preprint's unnumbered remark is not used to infer the published numbering.
