# Rounding switching controls under a hard switch budget

The manuscript is `main.pdf`; `main.tex` is its entry point. It covers sharp
continuous minimax values through three switches in the stated mode ranges,
general and seeded bounds, exact finite-grid results, exact small-budget
instance algorithms, and certified coarsening. It includes complete proofs,
exact computer-assisted certificates, and a reproducible public-data study.
The author field is empty so the responsible researchers can supply authorship.
The staged review snapshots and their verification records (completed
2026-09-07) remain historical. The manuscript sources were revised afterwards:
Lean-driven proof clarifications for the
[September 20 documentation follow-up](../notes/lean-verification-documentation-followup.md),
commit `aee2afbf` (2026-09-24), and any 2026-09-25 audit follow-up edits.
The current PDF was last rebuilt in commit `aee2afbf`. The staged reviews do
not cover these later revisions.

Build from this directory with TeX Live, `latexmk`, and BibTeX:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

All figures and generated tables are included. Building the paper needs no
Python packages or network access. `latexmk -c` removes intermediate files
while retaining the PDF.

Run the complete portable verification suite with Python 3.10 or later:

```sh
python verification/run_all.py
```

The proof and algorithm checkers use the standard library and exact rational
arithmetic. Do not use Python's `-O` option, because assertions are part of the
checks. The runner executes the stage-specific suites sequentially and writes
logs under `verification/`; it may take several minutes. It also validates all
archived derived experiment tables without downloading data. Run a copied
bundle if its current files must remain read-only.

The original repository checkers and certificate data are bundled unchanged
under `verification/reference/`. Their source paths and SHA-256 hashes are in
`origin-manifest.json`. The four-block theorem uses complete finite and
polynomial dual certificates, not floating-point solver output. The
three-mode floor-history enumeration and the additional chronological-chamber
certificate have their exact scope stated in the paper and stage READMEs.
Optional numerical discovery programs are separate from proof verification.

Separate Lean packages verify selected mathematical results. [Topic 01](../formal/topics/01-switching-control/COVERAGE.md)
proves the exact five-, six-, and seven-cell three-mode values and the
continuous three-mode two-switch value `T/5`, including measurable inputs.
[Topic 17](../formal/topics/17-grid-switching/COVERAGE.md) proves the
arbitrary-grid one-switch formula, sharp transfer, coarsening certificates,
and the supporting unrestricted instance algorithms. Its one-switch
half-mesh certificate holds on arbitrary grids.

Their linked coverage and verification records delimit the guarantee. They
do not verify the whole manuscript, the Python implementations, reported
timings, bit-cost claims, or bibliographic novelty. Topic 01 does not verify
the chamber counts or optimal-switch histograms. The recorded Lean checks
are historical; the subsequent manuscript corrections and provenance links
do not constitute new proof execution.

Reproduce the public-data computations, including the original 12,000-cell
input and the continuous one-switch optimum:

```sh
python verification/stage06/experiments.py --fetch
python verification/stage06/render_results.py
```

The first command downloads one pinned public CSV and checks its hash before
using it. To work with a previously downloaded file, replace `--fetch` with
`--data /path/to/mmlotka_nt_12000_400.csv`. Input normalization, quantization,
exact outputs, and fresh timing samples are documented in
`verification/stage06/README.md`. Reproduction overwrites stage 6 results and
tables, including timings; a run on another machine should agree on exact
values, not elapsed times. The source CSV itself is not redistributed here.

To regenerate the standalone PDF figures, install Matplotlib and run:

```sh
python verification/stage06/render_results.py --figures
```

The exact data, algorithms, and proofs do not depend on Matplotlib. The
coarsener and a small exact continuous LP benchmark are in
`verification/stage05/`; its README explains rational input and dwell-time
contracts. APIs use zero-based mode labels; manuscript examples use the
mathematical labels stated in their text.

The general five-block reach theorem and the exact continuous three-mode,
three-switch minimax value remain research questions. No established theorem
or certificate assumes their resolution. The paper reports cumulative
rounding error, not an unverified nonlinear objective or trajectory guarantee.

`PROCESS.md` and `process/` document the requested staged author/reviewer
workflow, immutable review snapshots, source audits, and adjudications. The
comprehensive source-to-result map is `process/claim-coverage.md`. These are
internal verification records, not external journal peer review.

All six authoring stages and the separate five-reviewer whole-manuscript
review are complete. All valid findings from that review were addressed;
its acceptance is recorded in `process/stage07-acceptance.md`. The later
Lean review prompted the Section 8 proof clarifications and the more general
one-switch certificate described in
[topic 17's review record](../formal/topics/17-grid-switching/REVIEW.md).
