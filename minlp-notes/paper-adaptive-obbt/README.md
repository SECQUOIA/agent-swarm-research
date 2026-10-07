# Adaptive optimization-based bound tightening

[Read the manuscript](main.pdf). [main.tex](main.tex) is its anonymous LaTeX
entry point; `sections/` and `appendices/` contain the statements, explanations,
and proofs. [BUILD.txt](BUILD.txt) gives the build commands.

The manuscript develops the repository's iterated and adaptive OBBT results
into a self-contained account of contraction, stalling, finite certificates,
cutoff changes, constrained tightening, and computational cost. It distinguishes
proved properties of a specified relaxation operator from the performance of
an additional numerical solver policy. The existing experiments are retained;
no computational experiment was rerun for the manuscript.

[submission-source.zip](submission-source.zip) contains the standalone anonymous
manuscript sources and bibliography. The separate
[reproducibility-companion.zip](reproducibility-companion.zip) and its
[README](companion/README.md) contain the reference
implementations, archived experimental sources, results, and retained inputs.
Its [archive](companion/archive.tar.gz) preserves their original relative paths.

`evidence/` records the mathematical and literature audits, corrections,
coverage, and independent reviews. These development records are separate from
the submission sources. `verification/` contains the targeted document checks.
The original research reports and their evidence remain available under
`research-20260922/iterated-obbt/` and `research-20261003-adaptive-obbt/` in the
repository.

From this directory, check the manuscript source and build it with:

```sh
python3 verification/check_sources.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The source check checks included files, labels, citations, and unfinished text.
It does not check proofs. Document builds, analytic proof review, source
comparisons, and experimental evidence provide different kinds of verification.
Local work is limited to targeted checks; project-wide verification belongs to CI.

The [literature audit](evidence/literature-audit.md) records the support for the
37 scientific references and the complete list of source-access gaps. The
[software citation audit](evidence/literature-software-audit.md) covers nine
additional benchmark and software references. All 46 entries are cited. The
paper credits established methods and states its contributions for the
specified relaxation families. [Review responses](evidence/REVIEW-RESPONSES.md) record the corrections
and independent reviews; [artifact digests](verification/artifacts.json) identify
the PDF and both ZIP files.
