Fresh independent review of the LB-ESH research harness, 2026-09-19.

Verdict: the reviewed witness, adapter, timeout, and summary contracts pass the
targeted independent checks after correction. This approves the harness for
controlled numerical experiments. It does not establish algorithmic correctness,
independently certify solver dual bounds, or establish publication readiness of
the research results.

The review covered `lbesh_research/benchmark.py`, `validation.py`, `summarize.py`,
the author's `test_harness.py`, and the revised historical
`summarize_gdp_final.py`. The reviewer authored only this note and the two
`test_independent_harness*.py` files. The harness author made the implementation
corrections. No project-wide checks or CI inspection were performed.

Findings corrected during review:

- A transformed standalone Boolean could retain its initialization after its
  associated binary changed. Filtering the transformed witness to original
  variable names removed the generated binary, leaving the wrong Boolean.
  Witness extraction now derives Boolean truth from an integral associated
  binary. Validation still rejects an explicitly supplied Boolean/binary
  mismatch. The independent regression reproduces the stale initialization.
- Loading an automatic Boolean truth could round the associated numeric witness
  before evaluating rows and the objective. The validator now assigns Boolean
  truth without changing the retained numeric values. An independent fixture
  checks a binary value 0.9999995 in a row with coefficient 1e9: its integrality
  residual is tolerated but its 500-unit row violation must still be rejected.
- The LB-ESH adapter used an extra objective-sense conversion and the wrong
  bound field for maximization. The root reviewer identified this defect;
  independent tests verify that `stats.obj` and `stats.bound` retain their
  original objective sense, including an open-gap maximization fixture.
- Missing objective sense could be interpreted as maximization by the scorer.
  Such records now cannot receive a solved assessment.
- The old historical scorer made unvalidated solved claims using one-sided
  comparisons and status shortcuts. It now reports descriptive raw data only,
  with an explicit statement that witnesses and certification are absent.
- A real affine GDP failed through GAMS/SHOT because Pyomo inferred model type
  MIP, which its SHOT interface rejects. The adapter now explicitly invokes
  SHOT's MINLP interface for affine cases too. An independent real-solver
  regression verifies the correction.
- A subsequent SHOT tolerance configuration rejected its MIP solver's numerical
  optimum because a linear residual of 1e-6 exceeded SHOT's requested primal
  acceptance tolerance of 1e-8. The MIP solver had itself been asked for 1e-8;
  its log nevertheless reported the larger residual. SHOT retained objective 1
  for a maximization problem with optimum 3 and correctly reported an open gap.
  The harness correctly classified it as unsolved. Aligning SHOT's linear
  acceptance tolerance to 1e-6, within the common original-model validation
  tolerance, resolved the fixture. Nonlinear and integer tolerances remain
  1e-8. The final independent real-solver regression passes.
- The exact conic adapter lost standalone Boolean truth when the conic builder
  transformed a clone: the original Boolean had no association with the clone's
  generated binary. The conic solver now exports truth by original Boolean
  name, and the adapter loads it without rounding numeric indicators. An
  independent real-solver fixture verifies a Boolean initialized false but
  constrained to be true.
- A worker exiting between timeout detection and process-group termination
  could raise `ProcessLookupError` and abort the schedule. The exception is now
  handled. A deterministic regression verifies that a timeout record survives.
- Hashing only `gdp_instances.py` did not identify its external mutable model
  sources and data. Legacy-run metadata now also hashes the GDPlib and Pyomo
  example trees, excluding caches and Git metadata.
- Inferring the full schedule from observed records could hide an entirely
  missing method or instance. Summaries now accept the explicit schedule, and
  the CLI loads the adjacent schedule automatically. A regression checks
  missing methods, missing instances, an empty result file, and rejection of
  unscheduled records.

The independent witness fixtures also check fixed Boolean values before binary
loading can change them, missing numeric and Boolean values, selected versus
inactive disjunct constraints, finite discrete domains, objective consistency,
and stale Boolean rejection. The author's complementary fixtures check fixed
numeric values, variable bounds, integrality, logical constraints, XOR
disjunctions, and nonfinite values. Original-model validation retains raw and
tolerance-normalized residuals; its result is numerical feasibility at the
recorded tolerances.

Summary checks cover both objective senses, bounds on the wrong side of a
feasible objective, missing or untrusted bounds, failure and timeout outcomes,
two-sided reference comparisons, duplicate rejection, common paired instance
sets, and penalties for unsuccessful or missing runs. Raw status text alone
does not establish a solved result. A closed numerical primal-dual gap can be
reported even if a solver stops at a limit; the summary explicitly describes
the dual bound as solver-reported rather than an independently checked
certificate. GAMS adapter fixtures verify that native `OBJEST` overrides the
generic Pyomo bound and that native locally optimal status does not authorize
a global-bound claim.

The timeout test uses a real worker that starts a child process and writes more
than 200 KB of output. At a 0.5-second cap, the worker receives SIGKILL, the
child is terminated, and the result and file logs remain readable. Output goes
to files, so a full pipe cannot deadlock the parent. The exit-race test is
separate from this real process-group test.

Targeted commands run from `code/minlp_solver_lab`:

```text
.venv/bin/python -m unittest lbesh_research.test_independent_harness lbesh_research.test_harness -v
env LBESH_RUN_SOLVER_REVIEW=1 .venv/bin/python -m unittest lbesh_research.test_independent_harness_solvers -v
env LBESH_RUN_SOLVER_REVIEW=1 .venv/bin/python -m unittest lbesh_research.test_independent_harness lbesh_research.test_harness lbesh_research.test_independent_harness_solvers -v
```

The final combined command passed 28 tests: 17 independent fixture tests,
nine author tests, and two independent real-solver tests. Each real solve was
limited to one thread and five solver seconds. For
`max x`, `0 <= x <= 4`, and `(x <= 1) OR (x <= 3)`, LB-ESH big-M single-tree,
the exact conic hull adapter, and GAMS/SHOT all returned independently validated
primal objective and dual bound 3 within the protocol's numerical tolerance.
The LB-ESH case disabled its NLP and LP
phases. Executable paths came from the retained environment record; no new
dependencies were installed. The separate standalone Boolean fixture also
passed through the exact conic adapter with objective and bound zero and a
true Boolean witness. Earlier failing runs identified the corrections above;
the final combined run passed all tests without evaluation-error diagnostics.

Additional targeted `.venv/bin/python -` fixtures reproduced the Boolean defect
and the affine SHOT defect before correction. A quadratic maximization fixture
with `(x^2 <= 1) OR (x^2 <= 9)` verified actual GAMS native `MODELSTAT=1`,
`SOLVESTAT=1`, and objective/`OBJEST` equal to 3 within rounding. These were
small adapter checks, not performance experiments.

After the combined run, the harness added a seeded permutation of the scheduled
jobs and records both the seed and the complete order in `schedule.json`.
The targeted independent test
`test_shuffled_schedule_is_complete_and_reproducible` passed with
`.venv/bin/python -m unittest lbesh_research.test_independent_harness.IndependentAdapterTests.test_shuffled_schedule_is_complete_and_reproducible -v`.
It verifies that all nine fixture jobs occur exactly once, the same seed
reproduces the order, and a second fixed seed changes it. Source inspection
confirms the executor submits that recorded order.

The retained GAMS log identifies executable version 54.3.1, SHOT 1.1 at Git
revision `a81275b4`, and its internal Gurobi 13.0.2. These differ from Python
package versions `gamsapi==54.4.0` and `gurobipy==13.0.3`; package versions alone
should not be used to label the GAMS solver binaries.

For publication tables, retain the adjacent schedule and each run's source
hashes, options, environment, witness, and validation record. Use comparable
solver budgets and thread settings, disclose declared-convexity options, and
describe unsupported methods separately from solver failures. A paired timing
comparison uses the same solved instances for both methods; it should be read
alongside the full scheduled-set failure penalties. Historical records lacking
witnesses cannot be upgraded to validated results by the new scorer.
