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

Current manuscript status: stages 1–3 accepted through the documented review
process. Stage 2 adds the universal heavy-mode reduction, exact continuous
two- and three-switch minimax values, equal-terminal-mass minimax results,
the complete four-block certificate proof, and structural counterexamples.
Later stages will extend the abstract, related work, and results. No later-stage
assertion is used to prove a stage 1 result.

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

Stage 2 checks also use only Python 3 and its standard library. Run all of
them, including artifact integrity, with:

```sh
python verification/stage02/run_checks.py
```

Do not use Python's `-O` option: the exact checkers require assertions.
Individual logs are written under `verification/stage02/`. The four-block
theorem depends on the bundled exact certificate checker and JSON data; the
other scripts provide checks of analytic constructions, retained special-case
proofs, or explicit counterexamples. In particular, `check_new_results.py`
checks the exact one-sided optimum of the three-mode counterexample through
the analytic sensitivity arithmetic and direct evaluation of its matching
schedule. It also independently rules out every three-block word at error
one by exact switching-time polygon feasibility. The exact instance optimum
does not determine the three-mode minimax value.

Stage 3 adds mode removal for both terminal-mass choices, general and seeded
upper bounds, exact plateau and equal-mass consequences, analytic predecessor
bounds, and a precise higher-block investigation. The general five-block reach
question remains open. An exact certificate proves only the stated single
chronological chamber result; no general theorem depends on that result.

Run the portable standard-library stage 3 suite with:

```sh
python verification/stage03/run_checks.py
```

See `verification/stage03/README.md` for certificate scope and optional numerical
discovery. All original verification files remain unchanged in the bundled
reference directory, with recorded source hashes.
