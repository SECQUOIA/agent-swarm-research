# Structured bilevel manuscript

This folder contains the LaTeX manuscript and its staged development records.
The draft is now complete, including its abstract, contribution and literature
comparison, six substantive sections, conclusions and four supporting
appendices. Authors are left blank. Stages 1 through 6 have been accepted under
the requested review process. Stage 7 synthesis and the subsequent independent
whole-manuscript review still require their review gates; a complete draft is
not a claim that those gates have passed.

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

`main.tex` defines notation and environments and includes all manuscript sections
and appendices. The build needs only the source files, this bibliography,
`figures/contacts.pdf` and the three generated table inputs in `data/`; it does
not read files from `process/`, `verification/` or the surrounding repository. `references.bib` is this paper's own bibliography;
it does not modify the generated bibliography in `../literature/`.

`process/coverage.md` maps source developments to manuscript stages and records
scope boundaries. Author, reviewer, assessment, correction, and verification
records belong in `process/`. Each stage must pass the user's five-reviewer gate
before the next stage begins. The finished manuscript will receive the same full
review cycle. Historical repository reviews are evidence to inspect, not a
substitute for these new reviews.

Stage 6 reproduction commands and the locations of their logs are given below.
Historical benchmark values must remain explicitly distinguished from reruns.
No user-supplied literature originals are copied into this folder.

Stage 2 author verification is recorded in `verification/stage02-author/`.
The additional support-tuple recovery diagnostic runs with Python and SymPy:

```sh
python verification/stage02-author/check_support_recovery.py
```

Stage 3 author verification is recorded in `verification/stage03-author/`.
The two exact diagnostics run from the repository root:

```sh
python code/bilevel_reopened/nearoptimal_second_review.py
python code/bilevel_reopened/screening_review_checks.py
```

These finite diagnostics support specified boundary and certificate checks; they
do not implement the general quantifier-elimination algorithms or replace proofs.

Stage 4 author verification is recorded in `verification/stage04-author/`,
with exact command outcomes and input hashes in `manifest.json`. Its additional
active-pattern modulus diagnostic runs from this folder with Python and SymPy:

```sh
python verification/stage04-author/check_sharp_modulus.py
```

The manuscript proves a global accuracy-bit construction. These finite checks do
not implement its general quantifier-elimination backend or certify practical
solver performance.

Stage 5 author verification is recorded in `verification/stage05-author/`.
From the repository root, run the eight distinct existing diagnostics with:

```sh
python paper-structured-bilevel/verification/stage05-author/run_checks.py
```

The manifest records commands, input hashes, exit codes and elapsed times. The
additional exact check of the padded path-follower construction and the
projected-gradient/continued-fraction oracle runs from this folder with:

```sh
python verification/stage05-author/check_padding_and_recovery.py
```

These checks validate finite instances and exact certificates. They do not
implement the general quantifier-elimination constructions or measure production
solver performance.

## Scalar algorithms and fresh computations (stage 6)

From this folder, using Python with SymPy, NumPy, SciPy and Matplotlib:

```sh
python code/check_full_task.py
python code/run_diagnostics.py
python code/run_experiments.py
python code/summarize_experiments.py
python code/plot_contacts.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The experiment driver writes `data/stage06-instances.json`,
`data/stage06-convex-screening-inputs.json` and `data/stage06-results.json`.
The full run uses three serial repetitions in separate processes; each worker
has a 90-second limit. Numerical thread variables and the HiGHS thread option
are set to one. No machine isolation is assumed. The tested environment used
Python 3.13.11, SymPy 1.14.0, NumPy 2.5.1 and SciPy 1.18.0. `threadpoolctl` is
not required; effective native pool sizes were not separately inspected.
Tables are generated from raw records by `summarize_experiments.py`.
`--resume` skips already recorded worker keys; use it only for an interrupted
run with unchanged solver inputs/code, not to combine different implementations.
The default command starts a new run and replaces this paper's fresh results;
repository historical outputs are never overwritten.

`code/compressed_solver.py` contains two measured local changes to the original
scalar solver: rational sign decisions before symbolic cancellation and rational
midpoints when both interval endpoints are rational. A later correction
materializes upper constraints once before validation so one-shot iterators
retain every row. All algebraic fallback and contact logic remain.
`code/original_faces.py` is an independent full-price,
full-upper-task baseline. It checks every nonempty principal Hessian minor,
rejects singular minors, enumerates original stationary faces, compares original
quadratic values over the entire price interval and retains all exact ties.
Its exponential enumeration is intended for small instances. It accepts only
rational input data and maximizes tariff `x*(u.T*z)` with affine upper rows;
its two semantics are optimistic and universally feasible pessimistic. It does
not call the compressed solver. The compressed solver separately supports flat
intervals, zero/signed loadings, fixed boxes and reversed tariff coefficients.
The convex prototype instead minimizes its specified quadratic upper objective.

`run_diagnostics.py` reuses distinct repository tests while redirecting scalar
imports to the paper copy. It writes all logs and commands below
`verification/stage06-author/`; one test file is copied there with only its
solver import path changed. The new full-task checks validate response sets,
exact global upper values/attainment, and every attained optimizer witness
against the original-coordinate candidate values at its returned price.
Numerical convex comparisons supplement exact KKT/coverage checks.

The reported measurements and input hashes are in `data/stage06-results.json`.
The measured compressed solver is preserved as
`verification/correction-agent/stage06/measured-compressed-solver.py`; its hash
matches the recorded solver hash. The later iterator correction was not part
of those measurements. The measured calls used reusable lists or tuples, so
their results remain valid; the raw timings have not been changed or relabeled
as measurements of the corrected version. Source-version mappings and new
correctness checks are recorded in `process/stage06-corrections.md` and
`verification/correction-agent/stage06/manifest.json`.
The measured driver source is preserved as
`verification/stage06-author/measured-run-experiments.py` with its matching
recorded hash. Later driver changes only add prepared-input archival and create
missing output directories outside worker timing; their provenance is recorded
in `process/stage06-author.md`. Initial missing optional-package and native
stdout/JSON transport failures, the successful partial run, and the resumed
run are retained in the same verification folder. Worker result files now use
separate JSON transport, preserving native stdout and stderr in the report.
These were harness failures, not silently accepted solver results.

Large scalar runs with 1000 variables have only two repeated coordinate types;
the heterogeneous family is reported through 48 variables. The separate convex
sweep is reported through 10,000 variables. The exact screening prototype lost
all four archived and both fresh-size MILP comparisons after preprocessing was
included. Numerical zero-gap reports are distinguished from exact certificates,
including the retained default-tolerance discrepancy and tighter follow-up.
