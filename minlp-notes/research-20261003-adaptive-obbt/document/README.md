# Adaptive OBBT report

[Read the report](main.pdf). The source is [main.tex](main.tex), with separate
sections and the bibliography in [../literature/references.bib](../literature/references.bib).
[COVERAGE.md](COVERAGE.md) maps the principal claims to their assumptions and
reference implementation.

The 24-page report separates exact remaining-benefit certificates, numerical in-tree
bound tightening, and total solver performance. It has an empty author field.
The exact reference checker and the measured SCIP policy support different
relaxation families; the report states that distinction explicitly.

Build from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Targeted document checks actually run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
rg -n 'Warning|Overfull|Underfull' main.log
pdfinfo main.pdf
pdftotext -layout main.pdf main.txt
pdftoppm -f 1 -l 1 -r 110 -png -singlefile main.pdf /tmp/adaptive-obbt-report-title
pdftoppm -f 19 -l 19 -r 110 -png -singlefile main.pdf /tmp/adaptive-obbt-report-results
```

The build passed, the PDF author metadata is empty, and the resolved build has
no undefined references or citations and no overfull boxes. One bibliography
entry produces two harmless underfull-box warnings. Extracted text contained
the final outcome values and no unresolved-reference markers. Visual inspection
of the title/abstract and results pages found no clipped or overlapping text.
These are local document
checks; no project-wide verification or CI status/log inspection was performed.
The component checks and campaign evidence are recorded by their owning
modules and in the report's evidence section.

Two internal report-review passes checked the theorem transcription and
implementation claims. All reported corrections were applied: the ledger's
admission premise and rejected-entry costs, callback timing scope, real
variables versus rational data, optional objective-LP accounting, the
cutoff-frontier contract, the positive-width halving example, and the
zero-cutoff-slack qualifier in the repair asymptotics. The constrained-theory
author separately checked the integrated nonlinear repair theorem and constants.
Internal review does not establish external peer review or publication priority.
