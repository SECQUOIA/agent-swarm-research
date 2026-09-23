# Stage 1 corrections

Completed 9 September 2026 by the separate correction author after reading
the root adjudication and all five Stage 1 reviewer reports.

## Disposition

- **S1-R1-01, S1-R2-01, R3-01, S1-R4-01, S1-R5-01 — fixed.** In
  `sections/00-introduction.tex`, the minimum number of additional individual
  products now determines the full state circulation for every locally
  observed block–label pair, from observations and balance equations on the
  ambient circulation space. In `sections/09-conclusion.tex`, the residual
  cycle count explicitly ranges over locally observed block–label pairs.
  This follows the existing proposition's scope; it does not claim unique
  determination of the separate flows of merged, locally unobserved labels.
  The existing proportional-refinement discussion is unchanged.
- **S1-R4-02 — fixed.** In `sections/01-foundations.tex`, changed “already
  exhibits” to “already exhibit” for the plural citation subject Khademnia
  and Davarnia.
- **Reviewer 4's optional abstract simplification — applied as adjudicated.**
  In `main.tex`, the count sentence starts with “For each locally observed
  block–label pair” and states one additional coordinate per independent
  cycle of the unobserved subgraph. A separate sentence states that the
  flow, product, and auxiliary coefficients are unit.
- **Reviewer 1's optional comparison-table separation — no change, as
  adjudicated.** The adjacent introduction and structural table already
  distinguish the parameters; this was not a required correction.

All accepted findings are resolved. No theorem, proof, executable source,
data, bibliography, frozen snapshot, historical review, or other paper
folder was edited. The main manuscript retains `\author{}` and `\date{}`.

## Validation

- Built from a fresh private source copy in `stage1-correction-build/` with
  `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
  The build succeeded: 49 pages, 611,027 bytes. The final `main.log` has no
  warnings, undefined references or citations, overfull or underfull boxes,
  missing characters, or TeX errors. `build.stdout`, `main.log`, `main.pdf`,
  and `build-validation.json` retain the evidence.
- Extracted the PDF text to `stage1-correction-build/main.txt` and checked
  the rendered locally observed scope and corrected citation-subject verb.
  This was a targeted text and build check, not a visual audit of all pages.
- Compared current manuscript sources against the frozen Stage 1 round.
  Only the four files listed above differ. All 66 theorem, lemma,
  proposition, corollary, and proof environments are byte-identical, as are
  all 1,290 extracted inline/display math spans. The comparison diff and
  counts are in `stage1-correction-build/corrections.diff` and
  `source-validation.json`.
- Checked all frozen snapshot hashes and compared the current frozen-scope
  executable/data files with that snapshot; counts are retained in
  `stage1-correction-build/frozen-validation.json`.
- `git diff --check -- paper-network-simplex` passes. No executable tests
  were rerun because these corrections change prose only.

The first automated log scan matched the package-description text
“info/warning/error messages”; the corrected scan checks actual diagnostic
markers and passes. No TeX defect was found or suppressed.

The root's final check and stage-acceptance decision remain separate from
this correction record.
