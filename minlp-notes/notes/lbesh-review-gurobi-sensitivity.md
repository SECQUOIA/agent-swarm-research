# Independent review of GAMS/Gurobi tolerance sensitivity

Review date: 2026-09-19. A fresh reviewer inspected the separate wrapper,
compared it with the frozen primary adapter, and ran solver-free checks.
The reviewed wrapper is accepted for the declared supplementary experiment.
This is approval of its design and implementation, not of results that have
yet to be produced.

## Scope and provenance

The reviewed file is
`code/minlp_solver_lab/lbesh_gurobi_sensitivity.py`, SHA256
`547376f941569cffaabaa4683200ffc04892832f5a4dd8a31ec27d407efd477d`.
Its copied adapter is `lbesh_research/benchmark.py`, SHA256
`dbfb95a4a9534ec4596a1b3423ac6563b22fac4d86034e5a47dc184707b02f5b`,
which matches `source_v1_manifest.json`. The saved declaration is
`results/lbesh_development/gurobi_trig_sensitivity_plan_v1.json` in the lab.
It identifies all nine trigonometric instances and records the wrapper hash,
frozen source hashes, package versions, random order, limits, and tolerances.

This experiment was triggered by numerical failures observed while the
primary study was running, after its source freeze. It is therefore an
outcome-triggered supplementary sensitivity, not a preregistered primary
comparison. The declaration includes cases that succeeded as well as those
that failed. It does not authorize replacing primary outcomes or choosing
the better of two runs.

## Findings

An independent differential test applied the frozen primary adapter and
the sensitivity adapter to separate builds of the same trigonometric GDP.
The active transformed constraint expressions matched exactly. After
removing run-directory paths, the solver-call arguments matched exactly
except for enabling the option file. That file contains only
`feasibilitytol 1e-8`. The sensitivity retains the 120-second solver limit,
150-second process wall limit, one solver thread, absolute gap `1e-6`,
relative gap `1e-4`, and default integer tolerance.

The wrapper also requires the native log to report `FeasibilityTol 1e-8`.
Missing or different reported values fail closed. Native GAMS `MODELSTAT`,
`SOLVESTAT`, `OBJEST`, and `OBJVAL` are retained. Native `OBJEST`, rather
than Pyomo's generic lower-bound field, supplies the reported bound. The
frozen status gates are preserved: local-solution status cannot supply a
global bound, and no reported solution means no initialized witness is
exported as an incumbent.

Every incumbent is captured from the solved model and checked against a
fresh untransformed model clone using the unchanged validator. A deliberately
invalid numerical witness failed this validation and the solved assessment.
The numerical feasibility and gap claims remain tolerance-based solver
claims, not exact certificates.

Each run receives an exclusive artifact directory and a fresh process.
On timeout the parent kills the process group; it also handles the race in
which that group has already exited. A partial result file is ignored after
a wall timeout. BLAS/OpenMP thread variables are set to one. Existing output
files and more than six requested workers are rejected before worker launch.
The root coordinator must still enforce the *combined* six-worker budget
across different experiment commands; this standalone runner cannot know
how many other batches are active.

The schedule always contains the full Cartesian set of all nine declared
trigonometric instances and the distinct method
`gams-gurobi-bigm-feas1e8`. Its schema is compatible with the study analyzer's
complete-schedule, frozen-core, witness, and bound checks. One analysis
provenance gap was reported and corrected: worker wrapper hashes are now
compared with the schedule hash, in addition to checking frozen imported
sources. The analyzer requires the separate declaration, checks its complete
instance set, order, solver options and checker tolerances, compares its
wrapper hash with the current source, and checks the copied adapter hash
against the frozen source manifest. Every sensitivity outcome, including a
timeout or crash, must carry matching wrapper hashes. The original primary
runner's timeout metadata exemption remains intact.

The fresh reviewer accepted this narrow analyzer extension at SHA256
`96c0ca65fe6f7f0f1fd771202d8065d7537adef794d6e63cbc08835cc5e2899a`.
Adversarial checks rejected changed run order, tolerance settings, option
settings, current wrapper content, and mismatched worker hashes for each
outcome class. Six allocated workers remain permitted by the declaration's
explicit concurrency flexibility even though its example schedule uses one.

## Verification and limits

From `code/minlp_solver_lab`, the command was:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --frozen --no-sync python -m unittest \
  lbesh_test_sensitivity_independent test_lbesh_gurobi_sensitivity \
  test_lbesh_study_analysis test_lbesh_study_analysis_independent
```

All 48 targeted tests passed: ten tests in the fresh sensitivity review,
five sensitivity author tests, and 33 analysis author/reviewer tests. The
independent file is `lbesh_test_sensitivity_independent.py`, SHA256
`1fdbd696791399f7d0cc11794746b19d640836ec60454599bc873032096af4a9`.
An earlier test invocation failed because the reviewer mock omitted the
native log required by a concurrent author improvement; updating the mock
to supply that log resolved the issue without a wrapper change. A later
reviewer test first passed in-memory job tuples to an analyzer expecting
JSON-decoded job lists; serializing the fixture as the runner does corrected
that fixture without an analyzer change. No real
solver runs, project-wide checks, or CI inspections were performed by this
reviewer. The frozen packages were not modified.

Before interpreting the experiment, confirm nine completed scheduled records,
matching wrapper provenance, effective parameter evidence, native versions,
and fresh original-model witness assessments. Report validation outcomes,
gap outcomes, and runtime changes for all nine cases beside the unchanged
primary outcomes. A tighter setting may improve feasibility while increasing
runtime or leaving the gap open; no result should be inferred in advance.

## Completed nine-run independent data audit

All nine declared runs completed and passed the independent artifact audit.
The tighter setting produced nine numerically feasible witnesses, compared
with three in the unchanged primary run. Six met the common gap target with a validated primal,
compared with three in the primary run. All three large instances retained
open gaps at the 120-second solver limit. This supports a numerical-tolerance
explanation for the six primary witness failures; it does not make all nine
cases solved or establish a general solver ranking.

The native GAMS DAT values match the stored statuses, objectives, and bounds.
Every native log confirms GAMS 54.3.1, Gurobi 13.0.2, one thread, and
`FeasibilityTol 1e-8`. The exact option files and all other retained options
match the declared comparison. Fresh original-model witness checks and an
independent gap calculation reproduce every stored assessment.

| Instance suffix | Primary feasible / numerically solved | Tighter feasible / numerically solved | Primary wall seconds | Tighter wall seconds |
| --- | --- | --- | ---: | ---: |
| `large.s104729` | no / no | yes / no | 121.56 | 121.34 |
| `large.s130363` | no / no | yes / no | 121.53 | 121.30 |
| `large.s155921` | no / no | yes / no | 121.44 | 121.87 |
| `medium.s104729` | no / no | yes / yes | 5.68 | 4.98 |
| `medium.s130363` | no / no | yes / yes | 10.84 | 14.96 |
| `medium.s155921` | no / no | yes / yes | 8.34 | 3.78 |
| `small.s104729` | yes / yes | yes / yes | 1.27 | 1.72 |
| `small.s130363` | yes / yes | yes / yes | 26.83 | 1.27 |
| `small.s155921` | yes / yes | yes / yes | 1.32 | 1.67 |

The observed runtime changes vary by instance. These are separate single
runs with an outcome-triggered setting change; no fastest-run selection or
replacement of primary outcomes is justified.

Reproduction command from the lab (use a new output path):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --frozen --no-sync python lbesh_review_supplementary_results.py trig \
  --out results/lbesh_development/independent_trig_sensitivity_audit_final.json
```

The audit artifact retains all nine paired rows, input/primary/plan/wrapper
hashes, individual log hashes, native statistics, and fresh validation
residuals. The audit ran no optimization.
