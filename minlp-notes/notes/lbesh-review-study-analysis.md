# Independent review of the frozen-study analysis

Date: 2026-09-19. This review was performed by a fresh agent that did not
author the solver, harness, study analyzer, or declared study protocol.
The review concerns the standalone post-freeze analysis, not a completed
performance study. No optimization was run and no frozen executable source
was changed.

**Verdict:** the repaired analyzer is accepted for use on the declared study.
All 21 independent checks and 10 author checks pass. This is acceptance of the
analysis program, not publication readiness or acceptance of results that
were still running during this review. The final complete evidence and its
interpretation still require independent review.

## Scope and findings

I read `lbesh_study_analysis.py`, its author tests, the analysis-method note,
the frozen-study protocol, the supplementary schedule, and the legacy scope
audit. I checked the imported numerical assessment rule and relevant worker
metadata and cone-reference output formats.

The analyzer's basic numerical assessment is conservative. A numerical solve
requires a fresh original-model feasible witness, a finite reported global
bound marked usable, a completed worker, and the declared absolute/relative
gap. Minimization and maximization use opposite bound directions correctly.
An optimal status or objective consensus cannot replace those requirements.
The fresh check reuses the independently reviewed harness validator; this is
an analysis review, not a second independent implementation of primal
feasibility validation.

The input gate checks complete Cartesian schedules, rejects duplicate and
unscheduled rows, matches the primary schedule against the declared plan,
and verifies worker source hashes, lock hash, settings, and environment
against the enclosing schedule. A killed worker may lack its own provenance
but remains a failure under the schedule provenance. An incomplete file
produces no analysis output. The final complete data still require review;
a gate on each supplied file does not establish that all planned files were
supplied.

Cross-method and cross-repetition bound checks use feasible original-model
witnesses, including supplied fixed-assignment references. Invalid witnesses
cannot refute another run. Contradictory bounds or infeasibility statuses
disqualify a numerical solve. Ordinary invalid witnesses remain failures
even when their saved and fresh rejection agree and therefore produce no
new-disagreement warning.

Summary and paired tables remain separate by input-run label. Legacy rows
are labeled `legacy` in family, size, and split fields. Core common-solved
timings use identical instance sets, and PAR10 retains every scheduled
instance. Related generated instances are not treated as independent
statistical samples. Repetition tables retain each runtime and category;
they do not select the fastest repetition. Runtime ranges include failed
runs and must be interpreted together with their categories. Component-time
tables do not add overlapping callback, NLP, and cut-generation times.

I found three analysis gaps and requested coordinated author fixes:

1. The oracle plot checked that each present quadratic geometry had both
   policies, but deleting both policy rows for a geometry silently changed
   the displayed aggregate. The declared full geometry design must be
   checked, not only pairing of whatever rows remain.
2. Diagnostic provenance checked only hash entries that happened to be
   supplied. The required script and solver-source entries must be present.
3. The new `nonlp` and `usercuts` supplementary methods received summary
   rows but no matched ESH/ECP pair rows, because matching recognized only
   the unsuffixed core names. Pairing must preserve the same variant and
   keep these supplementary pairs separate from primary figures.

I also requested truthful labels when plotting a supplied schedule without
`--primary`, and explicit accounting for planned supplementary files. These
are reporting safeguards; they do not require changing frozen experiments.

## Independent verification

The adversarial tests are in
`code/minlp_solver_lab/test_lbesh_study_analysis_independent.py`.
They invoke no solver. Fixtures cover both objective senses, unusable and
missing bounds, timeouts, invalid witness exclusion, contradictions across
repetitions, fixed-reference infeasibility contradiction, empty common sets,
PAR10 denominators, repetition retention and omission, schedule omissions,
unscheduled records, source/environment mismatches, and real-witness
revalidation and corruption. A mixed primary/legacy/ablation fixture checks
pairing isolation.

The first independent run passed 14 of 15 checks and reproduced the missing
quadratic-geometry failure. The author corrected the geometry gate, required
source fingerprints, and variant-aware pairing. All 19 expanded independent
checks then passed, including an extra geometry, omitted required source
fingerprints, external/ablation isolation, and supplementary omission/order.

The combined 29-test run exposed a concurrent integration change: the
supplementary plan gained a non-Cartesian cone-reference collection. The new
supplementary checker initially assumed every job was a benchmark schedule,
so the author test failed on the reference job's absent `--order-seed`.
The author repaired this integration: reference coverage is checked through
the declared reference inputs, including all 42 roots and all 27 distinct
assignments for each of 14 small enumerations. Two additional independent
checks now reject an omitted root or assignment and keep unresolved
assignments explicit. Complete numerical evaluation is not treated as an
optimality certificate. `--require-complete-study` now gates all declared
benchmark and reference collections; the final study command should use it.

The final targeted command, run from `code/minlp_solver_lab`, was:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python -m unittest \
  test_lbesh_study_analysis_independent test_lbesh_study_analysis -v
```

All 31 tests passed in 0.477 seconds. The execution used Python 3.13.11,
Pyomo 6.10.1, and Matplotlib 3.11.2. Accepted analyzer SHA-256:
`98ea75b8cc68eb3db8c9417000bd92ea67799269240a0584dd62914eb96eaa37`.
Independent-test SHA-256:
`418d63f5d79d2f5a26c70dc7eeaadef15cbd3d666996c008ecc213c2d9001193`.

The actual main-file CLI was exercised at 181 of 663 rows and correctly
rejected the incomplete schedule before output creation. Separately, the
saved `gams-gurobi-bigm` witness on `lbesh.trig.large.s104729` was rechecked:
its disjunct cost-row residuals still exceeded the common tolerance, and
the analyzer classified it `invalid_witness`, with `numerical_solved=false`.
The checker was not relaxed. These were correctness checks, not partial
performance conclusions.

No project-wide verification or CI inspection was performed.
