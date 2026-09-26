# Integer Dimension in Convex Mixed-Integer Approximation of Nonlinear Graphs

The manuscript is in `main.tex`. The [compiled paper](build/main.pdf) includes the exact-count additions described below and the topic 20 scalar-quadratic verification notes. An earlier rebuild from clean sources was made for the [September 20 documentation follow-up](../notes/lean-verification-documentation-followup.md); the PDF was last rebuilt in commit `aee2afbf` (2026-09-24), which revised the manuscript sources again. Any 2026-09-25 audit follow-up edits are also later than the review records below. The [standalone LaTeX and PDF bundle](submission.zip) retains the 2026-09-07 version (commit `2a05c164`) and was not refreshed. The author block is intentionally blank, as requested.

## Build

From this directory, with a standard TeX Live installation and `latexmk`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python verification/check_manuscript.py
```

The source uses the standard `article` class. It does not assume a journal template. LaTeX packages are listed in `macros.tex`.

## Evidence and provenance

- [Revision final report](revision-20260907/FINAL-REPORT.md) records the completed 2026-09-07 revision, review findings, validation and deliverables.
- [Revision process](revision-20260907/PROCESS.md) records the September 2026 staged author and five-reviewer protocol. Its author, literature, reviewer and adjudication records document the 2026-09-07 revision and completed whole-paper gate; they do not cover the later source revisions described above.
- [Coverage inventory](coverage.md) maps the repository's canonical results and substantive supporting developments to manuscript locations. Its earlier fifteen-reviewer gates are historical.
- [Exact-count Lean completion](../formal/topics/00-exact-counts/VERIFICATION.md), completed September 11, verifies the mathematical results behind `thm:exact-box-gap` and its monotone affine shear. The [formal coverage table](../formal/COVERAGE.md) includes closedness invariance, strict integer-slice accuracy, and the explicit `3n`-auxiliary, `13n`-inequality rational formulation. It does not certify the rest of the manuscript, the hinge and Bernstein precursors, literature attribution, or serialized bit complexity. The source now includes the explicit formulation and its size and closedness consequences; the earlier paper review records and completed Lean verification fingerprints remain historical records of their checked sources.
- [Scalar-quadratic Lean coverage (topic 20)](../formal/topics/20-scalar-quadratic/COVERAGE.md) covers the exact square count; scalar Hessian-rank and one-sided inertia laws; contact-volume and slice arguments; finite linear upper constructions; exact convex one-sided product counts with arbitrarily small extra error for linear lifts; and the continuous square-epigraph row lower bound. The [verification record](../formal/topics/20-scalar-quadratic/VERIFICATION.md) records final targeted checks and source fingerprints. The formal constructions use explicit affine rows, proved spectral enclosures and complete unbounded epigraphs and hypographs. Vector quadratic systems (topic 26), other nonlinear results, literature attribution and whole-paper correctness are outside this verification scope.
- [Earlier final report](FINAL-REPORT.md) and [earlier process](PROCESS.md) preserve the previous preparation record; they do not certify the current revision.
- [Submission source instructions](SUBMISSION-README.md) describe the self-contained LaTeX files and build commands for the submission bundle.
- `reviews/` contains independent reviewer reports, root adjudications, frozen sources and content hashes.
- `verification/` contains source audits, separate correction reports, check scripts, execution manifests and captured output.
- `verification/environment.json` records the environment used for the checks.

The supplementary checks can be rerun from this directory:

```sh
python verification/run_checks.py --stage all --jobs 4
```

They use Python with NumPy, SciPy, SymPy and mpmath and refer to the original repository's `code/` directory. The runner records each script's hash, exit status and output in a new dated directory. Additional focused author/reviewer checks and their scope are recorded in the corresponding reports. Finite exact and numerical checks supplement the proofs; they do not formally verify universal mathematical statements or implement the entire formulation compiler.

Downloaded primary PDFs and extracted texts are cached under ignored `build/source-cache/`. Retrieval manifests preserve URLs, hashes and failures. The manuscript's references and local literature remain the source of citation provenance; generated review reports are not mathematical citations.

For a PDF layout audit, install Pillow and the Poppler command-line tools, then run:

```sh
python verification/inspect_pdf.py
```

This records text bounds and creates page contact sheets under `build/pdf-review/`; the sheets still require visual inspection. The environment record distinguishes the stage-1 interpreter from the interpreter used for later checks, and each execution manifest records its actual interpreter.
