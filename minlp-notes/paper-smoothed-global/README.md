# Smoothed exact global optimization beyond convexity

This directory contains the manuscript and its supporting verification records.
The manuscript develops exact optimization of a sampled rational objective;
its guarantees depend on the stated noise law, structural assumptions, and
output representation.

## Files

- `main.tex`, `macros.tex`, `sections/`, and `appendices/`: manuscript sources.
- `references.bib`: manuscript bibliography.
- `main.pdf`: anonymous 182-page manuscript with full proof appendices.
- `evidence/`: source coverage, literature audit, and independent review records.
- `verification/`: targeted source and build checks.
- `delivery/smoothed-exact-global-optimization-source.zip`: portable submission sources.

The submission archive contains the manuscript, bibliography, generated
bibliography file, and build instructions. Internal development and review
records stay in this directory.

## Build

Run from this directory with a TeX distribution containing the packages used in
`main.tex`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python3 verification/check_sources.py
```

No optimization experiments need to be rerun to build or check the manuscript.
The status and targeted verification commands are recorded in
`evidence/STATUS.md` and `verification/FINAL-VERIFICATION.md`. The final source
snapshot is `evidence/snapshots/submission-addendum-r2/`. The late companion
attribution and mathematical repairs are documented in
`evidence/addendum-disposition.md`.

The three anonymous, undated companion manuscripts produce standard BibTeX
sorting warnings. Their citations resolve, and the bibliography supplies
their exact titles without inventing authors or dates.
