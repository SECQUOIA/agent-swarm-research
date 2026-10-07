# Targeted implementation validation

## Completed implementation suite

The final combined command was restricted to this topic's solver directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B -m unittest discover -s research-20261002-decomposition/solver -p 'test_*.py' -v > research-20261002-decomposition/completion/targeted-tests.txt 2>&1
```

**All 158 tests passed in 4.114 seconds.** The
[saved output](../completion/targeted-tests.txt) identifies every test. The
suite covers the shared finite-tree engine, the original grid solver,
exact rational output, exact LP and convex QP, recourse transformations and
all four backends, TU constraints, optimal sets, polynomial factors, and
polynomial boundary output. It includes the independent constrained and
polynomial review tests. This was an integration rerun after the final
shared-code and interface changes, not a project-wide check.

Additional component reviews and proof checks are linked from the
[completion map](../completion/README.md). The final
[integration review](../completion/reviews/integration/REVIEW.md) independently
checks cross-module model binding, exact references, JSON round trips, and
replay with optimization entry points disabled. Its two suites report
81 rejected mutations, 12 exact-output runs, 27 pipeline runs, three
constrained runs, 15 set-membership checks, and 16 further workflow
round trips. Later recourse shortcuts were also compared against 63
complete-LP fallback cases; the final combined suite includes their regressions.

The [new bounded benchmarks](../completion/benchmarks/README.md) have
separate frozen sources, solve/replay limits, original-model references,
and resource-failure records. They are separate experiments, not additional
unit tests or CI results. Only topic-specific checks were run. No
project-wide verification or CI status/log inspection was performed.

The final benchmark aggregate is 84 configurations, 68 completed requests,
14 checked partial or unsupported intervals, and two certificate-free
outcomes. All 82 available certificates replayed successfully. The
[benchmark verification record](../completion/benchmarks/VERIFICATION.md)
provides the precise commands and independent audit, including 62 numerical
reference enclosures and two implicit-optimizer containment checks.

A separate CLI round trip ran the documented two-variable rational example
with `--exact --max-stages 256 --time-limit 2 --max-table-states 20000`, then
ran `verify_certificate.py` on the saved JSON. Both returned exact value
`-145/36` at `(1/6,2)` after 34 stages and 362 aggregate table states. The
first attempt used the CLI's default 24-stage cap and correctly returned a
replayed partial interval with gap `1/65536`; an assertion expecting exact
completion failed. Increasing the explicit stage cap completed the check.
The README exact-mode command now supplies that cap. No solver change was
needed. Inputs and outputs for this command were temporary files.

An inline `python3 -B - <<'PY'` artifact check parsed all 87 Python files
outside the historical source snapshots, checked trailing whitespace in
Python/Markdown/TeX, and resolved 453 local links across 79 Markdown files
within this topic. It also verified that all 35 source hashes from the final
test run were unchanged. The check passed after the document reviewer saved
the previously pending review file; no broken link remained. Results are
saved in `completion/artifact-checks.json` relative to this topic's root.

## First-release record

Date: 2026-10-02. The following describes the original release and its saved
source snapshots. No project-wide checks or CI inspection were run.

The command

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m unittest discover -s research-20261002-decomposition/solver -p 'test_certified_grid.py' -v
```

passed all 15 tests in 0.295 seconds in the final implementation test run.
An independent review followed without further source changes.
Earlier runs passed 13 and then 14 tests as the input-iterator and
outer-trial regressions were added. These were targeted reruns after actual
changes, not project-wide verification.

The finite-grid comparison covers five separate six-variable rational
objectives on a branching decomposition with four bags of size three.
Every corrected minimum and every unary min-marginal agrees with exhaustive
enumeration of all 729 grid assignments. Other tests compare analytic
continuous and mixed optima, exercise exact convex certificates and endpoint
reduction, and reject deliberately corrupted messages and filters.

A root review found that a one-pass iterator supplied as `integers` was
consumed during validation before conversion to a set. That could silently
change an integer model into its continuous relaxation. The implementation
now materializes the iterable once. A behavioral regression verifies that
`(x-1/2)^2` with `x` integer in `[0,1]` returns the exact value `1/4`.
Bounds supplied as a one-pass iterable are also materialized once.

The outer schedule was additionally exercised directly on `(x-y)^2` over
`[-1,1]^2`, with exact convex presolve and primal polishing disabled. At
tolerance `1/50` it used 18 completed stages across slopes `1/4`, `1/8`, and
`1/16`, evaluated 1,895 aggregate bag states, and returned an independently
replayed gap about `0.01204`. The solve took about 0.032 seconds in that
diagnostic. This example has a nonunique optimal line and forces actual
restarts, so it checks behavior that the normal convex presolve would hide.
It is now included in the targeted tests.

The [independent implementation review](reviews/review.md) found no
unresolved correctness defect. Its own targeted command was

```bash
timeout 10s python research-20261002-decomposition/solver/reviews/review_checks.py
```

It passed 32 exact-optimum cases covering 88 DP stages, plus controlled
interruptions during initial improvement, after a complete DP, and during
trial grid generation. The [recorded output](reviews/review-checks.txt)
includes the reviewed solver and checker source hashes.

A local Python check of the two solver documentation files' relative links
and trailing whitespace passed. `git diff --check --
research-20261002-decomposition/solver` also exited successfully; the files
are new and untracked, so that command is not a substantive source check.

The separately run bounded original-
objective comparisons, including actual solve/check/total time and peak
memory, are recorded under [extra-benchmarks/](extra-benchmarks/). The
benchmark corpus uses materialized integer sets, so the iterator bug did
not alter its earlier mathematical results; the final benchmark run uses
the fixed source and records its hash.
