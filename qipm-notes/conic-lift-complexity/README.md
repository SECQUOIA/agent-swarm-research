# Curvature, support certificates, and barrier complexity of conic lifts

This directory contains a complete standalone anonymous manuscript draft on
conic reformulation, its geometric resources, and its computational contracts.
The paper includes full proofs, a model table, a notation guide, six thematic
parts, four technical appendices, and a bibliography. Its stated unresolved
parameter intervals are mathematical scope limits, not missing draft sections.

The entry point is [main.tex](main.tex); the built paper is [main.pdf](main.pdf).
[macros.tex](macros.tex) contains the shared notation, theorem environments,
and PDF metadata. [bibliography.bib](bibliography.bib) contains the references.
The `sections/` directory holds the introduction (`00`), mathematical sections
(`01`–`12e`, with lettered refinements), and closing synthesis (`13`).
`main.tex` determines reading order and appendix placement. The
[Makefile](Makefile) builds with `latexmk`, `pdflatex`, and BibTeX.

From this directory, use the project's existing environment:

```sh
conda run -n qipm --live-stream make
```

To remove intermediate TeX files and rebuild:

```sh
conda run -n qipm --live-stream make clean
conda run -n qipm --live-stream make
```

`make clean` preserves the PDF. The build needs no workbench notes, literature
archive, other manuscript, network access, or Python package installation.
The bibliography identifies the unpublished companion *The Cost of Following
the Central Path* where results overlap; the proofs used here are included.

The author and date fields are intentionally empty for anonymous review.
The actual authors supply their names and affiliations when unblinding.
No author identity or institutional affiliation has been invented.

The [source ledger](audit/source-map.md) inventories all 201 current workbench
notes, records final inclusion and exclusion decisions, and preserves the
development history. [workflow.md](audit/workflow.md) records the required
author, five-reviewer, assessment, and separate-fixer cycles. The `audit/`
directory contains these working records and build checks; it is not part of
the paper. The workflow record gives the current status of the stage reviews
and the separate five-reviewer whole-manuscript cycle. These internal checks
do not imply journal acceptance or replace external peer review.

The manuscript keeps ambient and restricted barrier parameters, intrinsic
fixed-domain parameters, certificate ranks, and metric movement distinct.
Its work and query claims retain their specified access, output, and charging
assumptions.
