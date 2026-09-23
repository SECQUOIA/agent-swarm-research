# Stage 4 corrections

I read the root assessment and all five independent stage-4 round-1 reports.
This correction addresses all five accepted minor issues. No mathematical
development or checker change was requested or made.

1. `main.tex` and `README.md` now specify a prescribed fixed **lower bound
   on girth**, matching the theorem's inequality and avoiding an exact-girth
   interpretation.
2. `README.md` now requires Python 3.10 or newer for the four exact suites.
3. `appendices/verification.tex` now says that the 768 obtuse cases have
   **absolute principal angle** exceeding pi/2, covering both orientations.
4. `sections/00-introduction.tex` explicitly assigns Bienstock–Muñoz's
   Theorem 7 and Corollary 8 numbering to the arXiv version. The existing
   journal entry in `references.bib` identifies the full version as
   arXiv:1501.00288v15, 19 October 2016, and links to that version. The
   coverage map records the same precise version. This uses the root's
   verified original PDF header; I made no new source-verification claim.
5. The opening of `process/coverage.md` now distinguishes repository source
   paths from manuscript-relative `checks/`, `process/`, and `verification/`
   paths, while preserving the meaning of explicitly prefixed
   `paper-power-flow/` paths.

## Validation

A clean forced rebuild with
`latexmk -pdf -gg -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
completed successfully and preserved the 28-page PDF. The final LaTeX log
contains no warnings, unresolved references or citations, overfull or
underfull boxes, or errors. I rendered and visually inspected pages 1, 3,
26, and 28, covering every changed manuscript passage and the bibliography.
All are legible and fit without clipping.

Comparison against the stage-4 round-1 snapshot confirms that sections 01–06,
the arithmetic appendix, macros, and all four checkers remain byte-identical.
The exact suites were not rerun for these prose-only changes. The preexisting
root-owned change in `PROCESS.md` is recorded separately in the diff summary;
I did not edit that file, freeze a snapshot, or declare the stage accepted.

Evidence, relative to the paper directory:

- `verification/stage04-corrections.diff`: exact correction diff for the six
  edited source/documentation files.
- `verification/stage04-corrections-diff.json`: changed-file and unchanged-code
  summary.
- `verification/stage04-corrections-build.log`: actual forced build output.
- `verification/stage04-corrections-validation.log`: final-log checks, PDF
  metadata, and visual-inspection record.
- `verification/stage04-corrections-layout.txt`: extracted final PDF text.
- `verification/stage04-corrections-page1.png`, `page3.png`, `page26.png`, and
  `page28.png`, each with the same `stage04-corrections-` prefix: generated
  visual-inspection images, excluded by the existing ignore rules.

The corrected integration is ready for the root's check. The separate
whole-manuscript five-reviewer process remains required.
