# Computational supplement

This archive accompanies *Structured bilevel optimization with many follower
variables: Global responses, accuracy, and structural boundaries*. It contains
rational test instances, scalar solvers, exact diagnostic scripts, raw benchmark
records, historical comparison records and all local dependencies of the
commands below. No surrounding repository is needed. The separate LaTeX source
archive contains the complete manuscript.

Keep the directory layout: `paper-structured-bilevel/` and `code/` must share
this parent directory. Run all commands below from this directory. Some script
and folder names retain their development-stage numbers so their relative
imports and recorded paths remain unchanged. They are computational tests and
records, not part of the manuscript's exposition.

## Environment and integrity

The recorded benchmark environment used Python 3.13.11, SymPy 1.14.0,
NumPy 2.5.1 and SciPy 1.18.0 on Linux. Figure generation was checked with
Matplotlib 3.11.1. The supplied `requirements.txt` records these package versions.
Use a Python environment whose `python` executable is on `PATH`; the boundary
diagnostic driver starts child processes by that name. For example:

```sh
python -m pip install -r requirements.txt
```

`SHA256.json` lists every exported file except itself. Before running commands
that write output, verify the files and the 11 measured input mappings with:

```sh
python verify_archive.py
```

The measurement mapping in `measurement-provenance.json` distinguishes the
current files from the exact source versions used in the reported timings.

## Reproduce the tables and correctness checks

Regenerate the three paper tables from the supplied records without running
any new benchmark:

```sh
python paper-structured-bilevel/code/summarize_experiments.py
```

This checks that all 60 workers completed, verifies the recorded screening
statuses and exact-solution flags, and writes the three `data/table-*.tex`
files. The regenerated tables are byte-identical to those supplied. This is
validation of the retained records; rerunning the exact algorithms is separate.

Run all five implementation diagnostic families, including the 18 complete
upper-task comparisons, with:

```sh
python paper-structured-bilevel/code/run_diagnostics.py
```

They check response sets, both upper semantics, exact values, attainment and
optimizer witnesses against an independent original-coordinate face baseline.
They also test flat responses, signed data, iterator constraints, convex
certificates, corrupted or incomplete certificates, and original contacts.
Each family has a 180-second limit. Logs and a command/exit-code record are
written under `paper-structured-bilevel/verification/stage06-author/`.
The original diagnostic outputs are preserved separately in
`paper-structured-bilevel/data/recorded-diagnostics/`.

Additional exact checks cover support-tuple recovery, near-optimal responses,
dense screening, the active-pattern modulus, structural hardness boundaries,
path padding and rational recovery:

```sh
python paper-structured-bilevel/verification/stage02-author/check_support_recovery.py
python code/bilevel_reopened/nearoptimal_second_review.py
python code/bilevel_reopened/screening_review_checks.py
python paper-structured-bilevel/verification/stage04-author/check_sharp_modulus.py
python paper-structured-bilevel/verification/stage05-author/run_checks.py
python paper-structured-bilevel/verification/stage05-author/check_padding_and_recovery.py
```

The boundary driver runs eight distinct scripts and writes its logs and
`manifest.json` in its own directory. The other checks report results on
standard output. Additional diagnostics and their local imports are retained
in the nine `code/bilevel_*/` and `code/parametric_path_lp/` directories.
These finite tests support the implementation and specified examples; they
do not replace the proofs or implement the general quantifier-elimination
algorithms.

Regenerate the contact figure with:

```sh
python paper-structured-bilevel/code/plot_contacts.py
```

This writes PDF and SVG files under `paper-structured-bilevel/figures/`.
PDF metadata may change even when the plotted content is unchanged.

## Measurements and source versions

`paper-structured-bilevel/data/stage06-results.json` is the unchanged record of
60 successful workers in 20 groups, with three serial repetitions per group,
individual times, exact outcomes, software and machine metadata, input hashes,
and native solver output. The three tables use medians for these runs.
Workers started in fresh processes with cleared SymPy caches and a 90-second
limit. The numerical thread environment and the forwarded HiGHS thread option
were one; effective native pool sizes were not separately inspected. The
machine was shared. These records support the stated scalar subclasses and
are not controlled estimates of industrial performance.

Three current source files differ from the recorded input hashes. Their exact
measured versions are included at the following paths:

| Current path under `paper-structured-bilevel/` | Measured path under `paper-structured-bilevel/` | Later change |
| --- | --- | --- |
| `code/compressed_solver.py` | `verification/correction-agent/stage06/measured-compressed-solver.py` | Materialize upper constraints once so one-shot iterators retain every row. |
| `code/run_experiments.py` | `verification/stage06-author/measured-run-experiments.py` | Archive prepared inputs and create output directories outside worker timing. |
| `code/check_full_task.py` | `verification/stage06-author/measured-check-full-task.py` | Create output directories and add iterator regression checks. |

Removing the single `constraints = tuple(constraints)` line from the current
compressed solver reproduces the measured solver byte for byte. The measured
calls used reusable lists or tuples. The iterator correction was not measured;
none of the raw times is presented as a timing of the corrected solver.
The JSON provenance maps all 11 recorded inputs to included files, with both
the measured and current hashes. The preserved measured driver and helper are
source evidence at archival paths, not alternate executable entry points.

Prepared scalar instances are in `data/stage06-instances.json`; prepared convex
and screening inputs are in `data/stage06-convex-screening-inputs.json`, both
under `paper-structured-bilevel/`. Archived comparisons are separate:

- `code/bilevel_nonconvex/benchmarks.json` and
  `benchmarks_pairwise_baseline.json`: earlier scalar and all-pair compressed
  comparisons.
- `code/bilevel_reopened/quadratic_benchmark_results.json` and
  `quadratic_tariff_benchmark_results.json`: earlier convex path and fused sweep.
- `code/bilevel_reopened/screening_milp_comparison.json`: four archived screening
  comparisons, needed by the table generator, including tolerance follow-ups.
- `code/bilevel_reopened/approximate_structure_checks.json` and
  `screening_second_review_results.json`: retained screening diagnostics.

The older comparisons used different repetition and cache protocols. They are
historical records, not reruns of the current source. In particular, the older
all-pair timing does not describe the new original-coordinate face baseline.
The default-tolerance MILP discrepancy and its tighter-tolerance follow-up
remain separate; numerical zero MIP gap is not an exact certificate.

`paper-structured-bilevel/data/recorded-diagnostics/` preserves the original
exact diagnostic outputs. `verification/stage06-author/` retains the initial
optional-package failure, failed native-stdout/JSON transport log, partial
record and resumed-run log. Those harness failures were not accepted as solver
results; they remain distinct from the 60 completed workers. No literature
originals, manuscript review reports or internal process logs are included.

## Optional new timing campaign

Use a disposable copy of this archive for a new campaign:

```sh
python paper-structured-bilevel/code/run_experiments.py
python paper-structured-bilevel/code/summarize_experiments.py
```

The first command replaces the fresh-result and prepared-input files in that
copy. It measures the current corrected source, so new results must be labeled
as a new campaign; they are not a reproduction of the historical timings or
hash manifest. Do not use `--resume` with the supplied historical records.
Use `--resume` only to continue your own interrupted campaign with unchanged
source and inputs. The driver reads `/proc/cpuinfo`, so the full campaign is
intended for Linux. New wall times will depend on the machine and environment.
