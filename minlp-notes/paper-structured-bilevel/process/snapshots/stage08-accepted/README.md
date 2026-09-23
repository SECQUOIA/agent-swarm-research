# Structured bilevel manuscript

This folder contains the complete standalone paper *Structured bilevel
optimization with many follower variables: Global responses, accuracy, and
structural boundaries*, with blank authors, seven sections, four appendices
and its bibliography.

The submission artifacts are:

- [paper.pdf](paper.pdf): compiled manuscript.
- [LaTeX source ZIP](structured-bilevel-latex-source.zip): all manuscript inputs,
  a build README and a file hash manifest.
- [Computational supplement ZIP](structured-bilevel-computational-supplement.zip):
  code, exact diagnostics, data, historical comparisons, complete local import
  dependencies, measured source versions and portable provenance manifests.

All eight stages are complete, including the resumed synthesis stage and five
independent reviews of the entire manuscript. A separate agent corrected all
accepted minor findings, and root independently verified the final archives,
clean 78-page build, diagnostics, table regeneration and measured-source hashes.
No identified issue remains unresolved. The final paper has 54 references.
The final assessment is [process/assessments/stage08-round01.md](process/assessments/stage08-round01.md).
Author,
reviewer, assessment and correction records remain under `process/` and are
excluded from the submission archives. `process/coverage.md` maps the relevant
repository developments to the paper. No literature originals are redistributed.

## Build

From this folder, or from the extracted LaTeX archive:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The output is `build/main.pdf`. Requirements are a standard TeX Live installation
with pdfLaTeX, BibTeX and latexmk. No shell escape or surrounding repository is
needed. The complete build uses 17 scientific input files: `main.tex`, this
paper's `references.bib`, seven sections, four appendices, `figures/contacts.pdf`
and three generated table inputs in `data/`. It does not read process records
or computational scripts.

## Reproduce computations

The supplement contains its own standalone README. Its source is
[delivery/README-supplement.md](delivery/README-supplement.md), which gives exact
commands, dependencies, limits, output paths and measured-version provenance.
Keep the exported common parent of `paper-structured-bilevel/` and `code/`.
From that parent, the principal checks are:

```sh
python verify_archive.py
python paper-structured-bilevel/code/summarize_experiments.py
python paper-structured-bilevel/code/run_diagnostics.py
```

The first command applies to the extracted supplement. The latter two also run
from this repository's root. The three tables regenerate byte for byte from
60 completed worker records and the distinct historical screening records.
The five diagnostic families include independent comparisons of the complete
upper task and exact certificate checks. The supplement README also documents
all earlier support-recovery, modulus and structural-boundary diagnostics and
figure generation.

Raw timings and their measured input hashes are unchanged. The current solver
contains a later iterator correction; its exact measured predecessor, driver
and test helper are included and mapped in
[delivery/measurement-provenance.json](delivery/measurement-provenance.json).
Recorded calls used reusable lists or tuples. Current correctness checks do
not relabel the archived timings as measurements of the corrected source.
The supplement distinguishes historical comparison protocols, initial harness
failures, the completed runs, numerical MILP reports and exact certificates.
A new timing campaign is optional and should run only in a disposable copy,
as documented there.

The archive construction script is
[delivery/build_archives.py](delivery/build_archives.py). It exports a fixed
set of source and computational inputs and records every exported file hash
in [delivery/archive-manifest.json](delivery/archive-manifest.json). It excludes
internal review reports and original literature files. The source ZIP builds
independently; the supplement executes without importing this repository.
Final PDF and archive identities are recorded in
[delivery/final-artifacts.json](delivery/final-artifacts.json).
