# Whole-manuscript editorial corrections

The separate correction pass implemented all seven accepted items in [the round 1 adjudication](whole-round1-adjudication.md). This agent was not one of the five whole-manuscript reviewers. The work changes editorial framing, navigation, physical terminology, and one bibliography entry. Final acceptance and publication artifact refresh remain with root.

## Corrections

1. **Abstract precision and hierarchy — WR1-O1, WR3-M1, WR2-O1.** The abstract now assigns bounded local degrees and fixed finite data specifically to the no-bypass, many-pool existential-real construction. It retains the algebraic-witness consequence for both constructions, says “all four layer degrees,” and states input out-degree at most two explicitly. The contracted feasibility qualification remains separate from the fixed-data threshold result. The shorter secondary-results passage retains the physical representation/optimization distinction, the isolated-margin general-cost conjecture, fixed-interaction-rank tractability, and exact and uniform approximate conic bounds. See `sections/00-introduction.tex`, PDF p. 1.

2. **General path-tool role — WR1-O2, WR2-O3, WR4-O2, WR5-O2.** Section 5.1 now identifies the general parameterized relation and strip results as symbolic-elimination tools that describe the open boundary. It explicitly says that the physical polynomial classifications use rational endpoint projection, conservation, signed cuts/support, or the separate two-vector convex reduction, and do not invoke the general strip theorem. Both general theorems and their complete proofs remain. See `sections/05-contract-algorithms.tex:102`, PDF p. 63.

3. **Reading routes — WR4-O1, WR5-O2.** A two-sentence guide after the model/encoding conventions directs readers to the algebraic constructions while identifying the remaining foundations as independently readable structural results. The introduction adds one sentence identifying the isolated margin model at the start of Appendix B as the entry to the independent Appendices B/C route. See `sections/01-foundations.tex:170` and `sections/00-introduction.tex:204`, PDF pp. 7 and 3.

4. **Restricted-hardness dependency guide — WR2-O2, WR4-O3.** New Table 2 (`s3:refinement-guide`) sits immediately before the copy subsection on p. 36. It has three rows, checked against the actual proofs:

   - The value-preserving branch uses `s3:base-bypass`, `s3:half`, `s3:cycles`, and `s3:upper-only`. It retains ordinary threshold hardness and equality of optimum values up to the stated offset; its large data do not yield strong hardness.
   - The finite-data branch uses the cycle gadgets in `s3:linear-circuits`, then the construction in `s3:constant-thm`. The source threshold is already physically encoded in its contracted network before completion removes positive lower bounds and introduces the bounded economic target.
   - The contracted-feasibility refinement `s3:five-thm` starts from that physically encoded threshold circuit before completion, and gives at most three input and two product exceptions, with the redundant common pool bound.

   The guide expressly preserves private midpoint supplies and separate full and half cycles, and says the routes are not one implication chain. No proof dependency or theorem hypothesis was added or removed. The existing two-product feasibility boundary remains untouched.

5. **Repeated synthesis explanation — WR3-O1.** The open-question paragraph now states the two retained-information obstacles: unknown pool-quality parameters and missing pool mass/quality aggregates and objectives. It gives exact references to the quasipolynomial parameter result, the detailed warning after the path algorithm, and the abstract slab obstruction. All open-question assumptions remain, including fixed pool count, fixed affine rank, degree-two bypasses, unbounded attachments, general intervals, and the separate feasibility/dense-profit scopes. The full algorithm warning and Appendix A slab proof are unchanged. See `sections/06-synthesis.tex:103`, PDF pp. 83–84.

6. **Physical terminology — WR2-O4.** Physical terminal nodes are consistently called products in Section 3's statements, proofs, degree/count summaries, tables and figure text, and in the affected passages of Sections 2, 5, 6 and Appendices A/B. The full/half figure caption uses product terminology too. Each context was checked; corresponding article agreement was repaired. Algorithm output, returned coefficient/encoding descriptions, logical output ports, mathematical output maps, existing labels and the internal TikZ `output` style remain unchanged. Pool feeds and outlets retain their arc meaning. Cited titles are unchanged. This is a terminology change inside some formal statement/proof prose, not a change to its mathematical content.

7. **Published Grothey–McKinnon metadata — WR5-O1.** The existing `s6:grothey2020` key now records *Annals of Operations Research* 322, 691–711 (2023), DOI `10.1007/s10479-022-05156-7`. It retains the arXiv v1 URL and explicitly identifies the Section 3 locator as referring to arXiv:2002.10899v1. The metadata follows the publisher source independently verified by root and recorded in the adjudication: [publisher article](https://link.springer.com/article/10.1007/s10479-022-05156-7). The predecessor attribution in Appendix A is preserved. See `bibliography.bib:334`, PDF p. 103.

## Source and mathematical integrity

The complete [editorial diff](../checks/whole-corrections-build/source.diff) compares against the source-only `before/` snapshot. That snapshot was verified byte-for-byte equal to the reviewed `whole-round1/` sources, not an older revision. The changed manuscript files are the bibliography; Sections 0, 1, 2, 3, 5 and 6; Appendices A and B; and `figures/full-half-copy.tex`. `main.tex`, Section 4, Appendix C, and the other two figures are unchanged.

[The retained integrity check](../checks/whole-corrections-build/check_integrity.py) compares every complete formal environment and all inline/display mathematical fragments. [Its result](../checks/whole-corrections-build/integrity.txt) records:

- All **95 formal claims**, including three examples, plus two remarks and **93 proofs**, remain in place.
- Every formula fragment is byte-identical. Every complete formal statement and proof is identical after only output/product terminology and the necessary a/an normalization. In particular, theorem scopes, proof arguments, formulas and hypotheses are unchanged.
- All existing labels remain in order. The sole new label is the dependency table's `s3:refinement-guide`.

No mathematical verification suite was repeated: the accepted changes are prose-only and the source comparison found no changed mathematical fragment or proof argument. This check is an editorial integrity comparison, not a replacement for the independent mathematical reviews.

## Clean build and artifact inspection

The build ran in [checks/whole-corrections-build/source/](../checks/whole-corrections-build/source/), starting from only `main.tex`, `bibliography.bib`, the three required source directories, and the portable submission README copied as `README.md`. No shared PDF, old auxiliary file, or old BBL was copied. After final wording changes, generated files in this task-owned copy were removed and the final build was repeated from the same [source-only inventory](../checks/whole-corrections-build/final-clean-source-files.txt), using the README command:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The [final isolated PDF](../checks/whole-corrections-build/source/main.pdf) has **105 pages**. The new compact guide and normal reflow add one page relative to the reviewed 104-page artifact. The retained [build transcript](../checks/whole-corrections-build/latexmk.txt), [LaTeX log](../checks/whole-corrections-build/source/main.log), [BibTeX log](../checks/whole-corrections-build/source/main.blg), and [artifact checks](../checks/whole-corrections-build/artifact-checks.json) show zero LaTeX/BibTeX warnings, zero overfull/underfull boxes, no missing citations/references, and no duplicate labels. All 39 distinct citations match the 39 generated bibliography entries; all 273 source labels resolve.

I rendered and visually inspected **43 pages**: 1–5, 7, 27–49, 62–63, 68, 71, 74, 81, 83–86, 88, 90, 94 and 103. These cover the edited front matter and reading guides; the terminology changes and affected diagrams throughout Section 3; the new table; the path-tool guide and affected contract passages; the synthesis; affected appendix passages; and the published reference. Adjacent pages were included where reflow matters. The [render inventory](../checks/whole-corrections-build/rendered-pages.txt), page PNGs and eight contact sheets are retained in [renders/](../checks/whole-corrections-build/renders/). Pages 1, 3, 36, 63 and 103 were also inspected as individual full-page renders. The new map stays with its introductory paragraph immediately before Section 3.4; its columns, caption and references are readable. No clipping, overlap, missing symbol, or abnormal spacing was found.

No issue remains in this correction pass. The isolated build sources match the shared manuscript sources. The shared `main.pdf` was hash-checked and remains unchanged. Root owns final acceptance, status/README/report refresh, the shared PDF, and source ZIP packaging; this report does not mark publication complete.
