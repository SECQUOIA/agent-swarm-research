# Report verification

The completed report is **31 pages**. The report-only build succeeded from
this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The final `main.log` contains no LaTeX warnings, overfull or underfull boxes,
undefined references, undefined citations, or error markers. A scoped Python
check found 48 unique TeX labels and no unintended control characters in
the source. `pdfinfo main.pdf` confirmed the page count and blank author
metadata. The title page has no author or date. TeX auxiliary files are
ignored; the PDF and sources are retained.

The PDF was extracted with:

```sh
pdftotext -layout main.pdf /tmp/minlp-completion-final.txt
```

Pages 1, 10, 14, 28, 29, 30 and 31 were rendered with `pdftoppm` at 110 dpi
and visually inspected. They cover the title, general nonunique exact
recovery, piecewise curvature proof, new benchmark table, aggregate results,
claim map and bibliography. The final table edit was rebuilt and its last
two pages inspected again. Text, equations and tables fit the pages and
remain readable. Rendering checks do not establish mathematical correctness.

A final scoped Markdown-link check resolves every relative local link in
this document directory. TeX citation keys were checked against the local
bibliography, and source whitespace was checked. The check scans this
report and its review files, not the repository as a whole.

The original [core review](reviews/core-review.md) remains applicable to
the unchanged corrected-grid proof chain. The independent
[completion review](reviews/completion-review.md) checks the new
candidate-denominator rule, finite exact recovery for nonunique box QPs,
piecewise curvature composition, nonunique TU filtration, implementation
scope and numerical evidence. Its requested zero-dimensional guard and
precision-option wording correction were applied. No unresolved issue
remains in that review.

The report author independently recomputed the six main benchmark-lane
aggregates from their saved rows: 73 configurations, 61 completed requests,
72 valid replays, 54 exact-reference enclosures and 29 exact values. The
additional extension rows give 11 configurations, seven completed requests,
ten valid replays, eight numeric reference enclosures and two implicit
optimizer containment checks. These yield the reported **84 configurations,
82 valid replays and 68 completed requests**. The report reviewer separately
checked individual result files, selected state/query/timing figures and
the combined summary. Provisional archives are excluded; the original
74-run evidence is explicitly historical.

The completion's [combined targeted test output](../completion/targeted-tests.txt)
reports **158 tests passed in 4.114 seconds**. Its
[35-source manifest](../completion/targeted-tests-manifest.json) was checked
by the independent completion reviewer. This report work read those saved
results; it did not rerun solver experiments or duplicate component tests.
Module reviews and the benchmark artifact audits remain the primary
verification records for those implementations.

No project-wide verification or CI status/log inspection was performed.
