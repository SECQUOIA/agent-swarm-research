# Structured bilevel manuscript

This folder contains the LaTeX manuscript and its staged development records.
The current draft contains accepted stages 1 through 4, including the fixed-core,
inverse-approximation and quantitative-bounds appendices. Each passed five
independent reviews and separate correction of all accepted minor issues.
Stage 5 (structural and arithmetic boundaries, including the path geometry
appendix) is authored and awaiting its five-reviewer gate. Later stages remain;
this is not a completed paper.

Build from this folder:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The output is `build/main.pdf`. Requirements are a standard TeX Live installation
with pdfLaTeX, BibTeX, and latexmk. No shell escape is needed. To remove build
intermediates while preserving the PDF, run:

```sh
latexmk -c -outdir=build main.tex
```

`main.tex` defines notation and environments and includes the current stage files.
Its commented future inputs are a build scaffold, not missing theorem statements
in the compiled manuscript. `references.bib` is this paper's own bibliography;
it does not modify the generated bibliography in `../literature/`.

`process/coverage.md` maps source developments to manuscript stages and records
scope boundaries. Author, reviewer, assessment, correction, and verification
records belong in `process/`. Each stage must pass the user's five-reviewer gate
before the next stage begins. The finished manuscript will receive the same full
review cycle. Historical repository reviews are evidence to inspect, not a
substitute for these new reviews.

Later computation stages will add reproduction commands and their actual logs.
Historical benchmark values must remain explicitly distinguished from reruns.
No user-supplied literature originals are copied into this folder.

Stage 2 author verification is recorded in `verification/stage02-author/`.
The additional support-tuple recovery diagnostic runs with Python and SymPy:

```sh
python verification/stage02-author/check_support_recovery.py
```

Stage 3 author verification is recorded in `verification/stage03-author/`.
The two exact diagnostics run from the repository root:

```sh
python code/bilevel_reopened/nearoptimal_second_review.py
python code/bilevel_reopened/screening_review_checks.py
```

These finite diagnostics support specified boundary and certificate checks; they
do not implement the general quantifier-elimination algorithms or replace proofs.

Stage 4 author verification is recorded in `verification/stage04-author/`,
with exact command outcomes and input hashes in `manifest.json`. Its additional
active-pattern modulus diagnostic runs from this folder with Python and SymPy:

```sh
python verification/stage04-author/check_sharp_modulus.py
```

The manuscript proves a global accuracy-bit construction. These finite checks do
not implement its general quantifier-elimination backend or certify practical
solver performance.

Stage 5 author verification is recorded in `verification/stage05-author/`.
From the repository root, run the eight distinct existing diagnostics with:

```sh
python paper-structured-bilevel/verification/stage05-author/run_checks.py
```

The manifest records commands, input hashes, exit codes and elapsed times. The
additional exact check of the padded path-follower construction and the
projected-gradient/continued-fraction oracle runs from this folder with:

```sh
python verification/stage05-author/check_padding_and_recovery.py
```

These checks validate finite instances and exact certificates. They do not
implement the general quantifier-elimination constructions or measure production
solver performance.
