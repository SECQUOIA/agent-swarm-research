# Rounding switching controls under a hard switch budget

This directory contains the manuscript and its review/verification records.
The author field is deliberately empty: authorship must be supplied by the
researchers responsible for submission.

Build from this directory with a TeX Live installation that includes `latexmk`,
BibTeX, and the standard LaTeX packages used by `main.tex`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The output is `main.pdf`. To remove intermediate build files while keeping the
PDF, run `latexmk -c`.

`main.tex` holds the article scaffold; `sections/` holds the mathematical text;
`references.bib` holds manuscript-specific bibliography records. `PROCESS.md`
records sequential stages. Author, review, and adjudication reports are in
`process/`; validation programs and logs are in `verification/`.

Current manuscript status: stage 1 draft (foundations, uniform-input formulas,
continuous one-switch minimax for at least three modes, and the three-cell
special case). Later stages will extend the abstract, related work, and results. No later-stage assertion
is used to prove a stage 1 result.

Stage 1 verification uses only Python 3 and its standard library. Rerun it
from this directory, or from the root of a frozen snapshot:

```sh
python verification/reference/uniform_certificate.py
python verification/reference/one_switch_certificate.py
python verification/stage01/check_boundaries.py
```

These exact-arithmetic checks supplement the mathematical proofs. They do not
replace the proofs over all measurable input controls.

The reference scripts are bundled unchanged. Their repository source paths
and SHA-256 hashes are recorded in `verification/reference/origin-manifest.json`.
The boundary checker imports the bundled copy. Frozen snapshots therefore
contain every program needed by these commands. The original round 1 snapshot
is retained as reviewed; its verification dependency defect is corrected in
subsequent snapshots.
