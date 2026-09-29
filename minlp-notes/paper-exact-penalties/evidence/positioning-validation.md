# Contribution revision validation

Baseline: `b63317ab072109d74ba5e27ee74759374ee24be9`.
All changes are within `paper-exact-penalties/` and concern positioning,
literature attribution, source evidence, and the compiled manuscript.

Targeted checks run on September 27, 2026:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from
  the paper directory: passed; final PDF has 23 pages, versus 22 before
  this revision. The final log has no LaTeX/package warnings, undefined
  references or citations, or overfull/underfull boxes.
- `pdftotext -layout paper-exact-penalties/main.pdf -`, followed by an
  inline Python check: extracted text has no unresolved `??` markers
  and includes the revised contribution and literature passages.
  The extraction was saved only to the already ignored
  `verification/main-text.txt`.
- Inline Python reference audit: 79 unique labels; every reference
  resolves; all 20 cited bibliography keys resolve.
- Inline Python baseline comparison using `git show`: all 60 complete
  theorem, proposition, lemma, corollary, proof and displayed-equation
  environments matched by the check are byte-identical to baseline.
  The source diff was also inspected; no mathematical result or proof
  was edited. The unchanged mathematical checkers were not rerun.
- `git diff --check -- paper-exact-penalties`: passed.
- In-memory `pdftoppm` rendering of page 2: visually inspected the
  contribution hierarchy, formulas, prior-work paragraph and typography;
  no clipping or layout issue observed. No rendering files were created.

A first edit attempt used a relative path from the paper directory and
stopped with FileNotFoundError before any mutation; it was rerun from the
repository root. The successful subsequent build and checks above apply
to the complete revision. No project-wide checks or CI inspection ran.


## Localized corrections after independent review

The accepted corrections clarify the norms and existential upper bounds,
the independent nonlinear-count bound, native constraints, the
perturbation assumptions and probability statement, and the precise
Bhardwaj/Boland/Feizollahi comparisons. The discussion now attaches the
numerical-size and subproblem caveats to the positive guarantees. No
mathematical result or proof changed.

After these corrections, the same targeted `latexmk` build, inline Python
label/citation/log and baseline-environment comparisons, text extraction,
and `git diff --check -- paper-exact-penalties` all passed again. The PDF
remains 23 pages, with 79 unique labels, 20 resolved citations and all 60
checked theorem/proof/display environments byte-identical to baseline.
There are no LaTeX/package warnings, unresolved references, or overfull
or underfull boxes. The unchanged mathematical checkers were not rerun.

The four automatic Claude PDF cache artifacts identified in
`positioning-sources.md` were moved into the paper's ignored source
directory. `git check-ignore -q` confirmed that each is ignored. No
other cache file was modified. No project-wide verification or CI
inspection was performed.
