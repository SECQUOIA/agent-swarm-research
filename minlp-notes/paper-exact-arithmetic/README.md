# Exact arithmetic in polynomial optimization

The anonymous manuscript, *Exact Arithmetic in Polynomial Optimization: Values, Optimizers, and Certificates*, covers all 97 developments in the repository's exact-arithmetic inventory. It distinguishes approximate values, approximate optimizers, exact comparisons, and exact representations of optimizers or certificates. The paper supplies complete proofs, explicit input and output models, related work, and explanations of the uses and limits of the results.

- [main.pdf](main.pdf): compiled manuscript.
- [main.tex](main.tex): manuscript entry point.
- [submission-source.zip](submission-source.zip): standalone anonymous sources, formatted bibliography and build instructions. It excludes internal development records.
- `sections/` and `appendices/`: statements and complete proofs.
- `references.bib`: bibliography.
- `evidence/`: source coverage, author reports, independent proof reviews, literature comparisons, and revision decisions. These are development records, separate from the submission source.
- `verification/`: targeted document verification.

The [coverage map](evidence/final-coverage.md) locates all 97 developments.
The [verification record](verification/FINAL-VERIFICATION.md) distinguishes
actual document checks, analytic proof reviews, literature checks and source
access limits. See [status](evidence/STATUS.md) for the review and package status.

Build from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python verification/check_manuscript.py
```

The source check verifies included files, labels, cross-references, citation keys, and unfinished text. It is a document check, not a proof checker. [BUILD.txt](BUILD.txt) also gives a build sequence without `latexmk`. Computational experiments were not rerun for this manuscript.
