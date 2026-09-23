# Stage 1 corrections

Correction author: `/root/stage01_corrections`. Date: 19 September 2026.

Read the lead disposition and all five independent round-1 review reports. All accepted issues were minor; all are addressed below. Changes are confined to `paper-lbesh`. Reserved later sections and the original research record remain unchanged.

## Finding-to-change record

1. **Hull versus big-M scope (reviewers 1, 3, 4, 5).** `sections/related-work.tex` now identifies the perspective inequality as the hull ECP/ESH construction, identifies the big-M original-variable deactivated tangents, and restricts the disaggregated-master comparison with Kronqvist–Misener to our hull variant. The shared radial policy is distinguished from the master representation.
2. **Introductory numerical aggregates (all reviewers).** `sections/introduction.tex` now names common-solved shifted geometric mean wall time and explicitly attaches the 4–6% result to single-tree comparisons across the three schedules. It describes cut counts and LP iteration counts as arithmetic cohort means. The numerical values are unchanged.
3. **Convex GDP definition (reviewer 5).** The opening definition now includes a convex minimization objective, convex inequality functions, and affine equality constraints.
4. **Quadratic CEHR notation (reviewer 4).** The related-work paragraph now states the original quadratic row, positive-semidefinite matrix assumption, and nonnegative auxiliary variable before displaying the lift.
5. **SHOT precedent (reviewer 2).** Added `lundell2022` with publisher-verified metadata and a related-work paragraph acknowledging its ESH/ECP separation, fixed-integer NLP heuristics, fallback, and tree policies. The paragraph distinguishes the present matched GDP policy experiment from both SHOT's algorithmic precedent and the separate SHOT reformulation baselines in this study. Inspected the primary publisher article, especially sections 2, 2.2.2, 2.3 and 7.2.4; this supports the stated relationship without asserting that SHOT already supplies the present GDP experiment. The consulted source is recorded in `evidence/literature.md`.
6. **Optional direct historical citation (reviewer 1).** Added `veinott1967` and a narrow sentence attributing the interior-to-exterior radial boundary construction. The publisher abstract explicitly describes this construction and its record supplies the bibliographic metadata. The full article was not consulted, and no detailed theorem claim is attributed to it. This source and limit are recorded in `evidence/literature.md`.
7. **Coverage map implementation precision (lead).** Replaced the unsupported prospective “cut de-duplication/stalls” item with “cut retention and stall handling” in `evidence/coverage.md`.

## Targeted verification actually run

- From `paper-lbesh`, ran `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex > process/stage01-corrections-build.log 2>&1`. Passed; resulting `main.pdf` contains five pages.
- Scanned the final `main.log` with a Python check for actual TeX/package warnings, undefined references or citations, overfull/underfull boxes, and errors. No diagnostic lines were found. An initial overly broad scan matched the package-description phrase “Providing info/warning/error messages” and raised an assertion; narrowing the expression to actual diagnostic lines corrected that false positive. No TeX defect was involved.
- Ran a Python citation inventory over all manuscript `.tex` files and `references.bib`: 18 entries, 18 distinct keys, no missing cited keys, and no uncited entries. Passed.
- Ran `pdftotext -layout main.pdf process/stage01-corrections-rendered.txt` and inspected the changed passages and rendered bibliography, including both new references and Veinott's name suffix. Ran `pdfinfo paper-lbesh/main.pdf` to confirm the build output.
- Read the SHOT baseline entries in `notes/lbesh-study-results.md` to confirm the manuscript's narrow statement that SHOT is an actual baseline. This is a source check, not a new benchmark or raw-data audit.

No project-wide verification, solver experiment, or CI inspection was performed. No unresolved accepted Stage 1 finding remains.
