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
continuous one-switch minimax, and the three-cell special case). Later stages
will extend the abstract, related work, and results. No later-stage assertion
is used to prove a stage 1 result.

Stage 1 verification can be rerun from the repository root:

```sh
python code/cia_tv_conjecture/uniform_certificate.py
python code/cia_tv_conjecture/one_switch_certificate.py
python paper-switching-control/verification/stage01/check_boundaries.py
```

These exact-arithmetic checks supplement the mathematical proofs. They do not
replace the proofs over all measurable input controls.
