# Final manuscript verification

The manuscript is 85 pages, with an abstract, nine numbered sections, six
technical appendices, and 21 cited sources. It has no author line, and its
PDF author field is empty. The submission source archive contains 23 files.
The PDF, source archive, and evidence companion are identified in
[delivery-manifest.json](delivery-manifest.json) and
[SHA256SUMS](../delivery/SHA256SUMS).

The original notes and experimental records were not modified. No numerical
experiment, optimization run, certificate search, or large archived
certificate replay was conducted for this manuscript. Symbolic and rational
arithmetic checked proofs and displayed witnesses; saved experimental
results were audited and transcribed with their limitations.

## Mathematical and literature review

The mathematical reviews cover the actual statements and proofs:

- [Corner and orbit foundations](../evidence/review-orbit-corners.md):
  unrestricted benchmark, attainment, algorithms, complexity, low-dimensional
  geometry, orbit, completion, tangent pencils, and exact obstructions.
- [Depth and closures](../evidence/review-closure-depth.md): quantitative
  bounds, conditioning, sharpness constructions, coefficient descriptions,
  tight combinations, closure gaps, and approximation factors.
- [Contact theorem](../evidence/review-contact.md): boundary perturbation,
  singular parameter limits, supremum equality, and attainment.
- [Minors and successive rounds](../evidence/review-minors-loop.md): minor
  orbit and rational certificates, convergence conditions, and the explicit
  stalling sequence.
- [Editorial integration](../evidence/review-editorial.md): notation,
  structure, empirical definitions and populations, references, and rendered
  pages.

The reviews found and resolved material defects in source statements and
proof explanations. The manuscript also completes the previously open
contact boundary case and supplies several new exact witnesses. The
[coverage record](../evidence/COVERAGE.md) identifies these developments and
corrections. Review reports distinguish direct mathematical checks from
historical certificate receipts. They are internal reviews, not journal
peer review. The last two cross-reference wording changes in Appendix B
preserve the mathematical content of its reviewed snapshot.

All literature research and acquisition used GPT Luna with max reasoning
and the requested literature skill. The
[literature audit](../evidence/literature-audit.md) records discovery rounds,
inspected versions, claim locators, bibliography corrections, and access
gaps. Source-specific SCIP formulas and experiments cite the inspected
2020 ZIB report. The algebraic and weak-oracle arguments cite the inspected
Renegar Part III and Grötschel–Lovász–Schrijver monograph. The introduction
acknowledges earlier depth and coefficient optimization and limits its
novelty statement to the precise results proved here.

## Targeted commands and results

The following commands were run from the manuscript directory unless a
different working directory is stated.

| Command | Final result |
| --- | --- |
| `python3 verification/check_document.py` | PASS: 19 TeX files, 200 unique labels, 251 reference occurrences, 21 cited sources; no missing input, citation, reference, or unfinished marker. |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` | PASS: 85-page PDF. Final `main.log` and `main.blg` contain no warning, undefined reference/citation, overfull box, or underfull box. |
| `pdfinfo paper.pdf` | Correct title; blank author; 85 letter-size pages. |
| `pdftotext -layout paper.pdf build/main.txt` | PASS: no unresolved-reference marker, duplicated “Equation equation”, or broken `waterund25` identifier. |
| `pdftoppm` with selected page ranges | Title, geometric figure, long formulas, and certificate/experimental tables inspected visually; final editorial report records its broader page review. |
| `python3 verification/package_sources.py` | Packaged all relative manuscript inputs, bibliography, compiled `main.bbl`, source checker, and build README. |
| `python3 verification/check_source_package.py` | PASS after extraction into a fresh temporary directory outside the repository: 23 files, clean 85-page build, blank author, identical extracted manuscript text and bibliography. |
| `python3 check_manifest.py`, from a fresh extraction of the delivered companion | PASS: 1,397 payload files, 80,710,667 bytes; all 1,393 original files preserved; 74 primary trajectory files, 5,160 trajectories, 220 baseline instances with matching cached denominators; R1–R8 mapping matches 12 retained survey rows. |
| `git status --short` | Only the new manuscript directory is reported. |

An initial portable-build harness assumed that a new BibTeX log would
always be produced. The included compiled bibliography can instead be
used directly, so that assumption was removed; the final check accepts
either route and verifies the bibliography actually used. Draft-stage
missing inputs and layout warnings were resolved before the final build.
No project-wide verification or CI inspection was performed.

The companion checks above establish byte integrity and consistency of
saved record metadata. They do not claim a new mathematical replay of its
large finite covers or a rerun of its experiments. The companion README
identifies complete saved certificates, verification receipts, numerical
records, omitted traces, and limits on portability and anonymity.

## Delivered artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `paper.pdf` | 836,086 | `632689918cc14302a2c594e6710442c3f8831be97a71b0dc80face2daf201bd0` |
| `delivery/quadratic-intersection-cuts-source.zip` | 128,433 | `1cbd3657d6efa713ce1b56c72c0ca25de26e7f8b85a17527189f7487bca2d4fd` |
| `delivery/quadratic-intersection-cuts-companion.tar.gz` | 12,387,186 | `f027b4f952f8ba25d3a291d59bb12c2bccf52702498145e87975c0bba0e9e0e6` |
