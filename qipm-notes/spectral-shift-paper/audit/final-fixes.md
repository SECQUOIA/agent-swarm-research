# Final review fixes

The one distinct accepted minor issue in `final-round1-assessment.md` is
addressed. It was reported as M1 by reviewers 3 and 5 and R4-1 by reviewer 4.

- Added `fawzi2017` to `bibliography.bib`: Fawzi, Saunderson, and Parrilo,
  *Equivariant Semidefinite Lifts of Regular Polygons*, Mathematics of
  Operations Research 42(2), 472–494 (2017), DOI 10.1287/moor.2016.0813.
  The entry separately records publication online on November 16, 2016.
- Added a concise comparison in `sections/01-introduction.tex`, citing
  Sections 3.1–3.2 and Appendix A, Lemma 1. It distinguishes finite-node
  interpolation from the present continuum minimax and query problem.
- Added an attribution immediately after the proof of `thm:thresholds`
  in `sections/04-fixed-accuracy.tex`. It identifies the extremizer's
  supporting-tangent representation. The self-contained proof and all
  mathematical results are unchanged.
- Updated `literature.md` with primary-source evidence. The fixer directly
  inspected the accepted manuscript's relevant sections and lemma and
  the publisher's issue and online dates, corroborating the root check.

Validation completed in the qipm environment:

```sh
conda run -n qipm --live-stream make
conda run -n qipm --live-stream make submission
```

Build output is in `final-fix-build.log` and packaging output in
`final-fix-submission.log`. The PDF has 31 pages. Final `main.log` and
`main.blg` contain no warnings, unresolved references/citations, or
overfull/underfull boxes. A preliminary case-insensitive log scan matched
the package description `info/warning/error` and BibTeX's `warning$ -- 0`
counter; both are informational text, and the diagnostic-specific check
passed.

Static checks found 19 distinct citation keys, all present in the
bibliography, with no duplicate bibliography keys. The new citation is
present in `main.bbl`. All 76 distinct referenced labels resolve, with no
duplicate labels. The source whitespace check passed.

`submission-source.zip` contains exactly 18 unique members. Every member
matches the corresponding working source byte for byte, including the
updated bibliography and `main.bbl`; the ZIP integrity check passed.
No figures were regenerated.

Rendered and visually inspected pages 4, 9, and 30, covering the changed
introduction paragraph, attribution, and bibliography entry. Their text,
citations, spacing, and page boundaries are clean. The inspection images
are `final-fix-page-4.png`, `final-fix-page-9.png`, and
`final-fix-page-30.png`. Workflow completion remains with root.
