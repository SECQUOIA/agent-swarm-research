# Structured bilevel manuscript

This folder contains the LaTeX manuscript and its staged development records.
The current draft contains stage 1 only; it is not a completed paper.

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

`main.tex` defines notation and environments and includes completed stage files.
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
