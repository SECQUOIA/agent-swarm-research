# LB-ESH development benchmark protocol

The experiment unit is one original GDP instance and one method in a fresh
Python process. A feasible witness and a global solver bound are separate
pieces of evidence. This protocol makes numerical optimization claims; it
does not provide exact arithmetic certificates or independently prove solver
dual bounds.

## Methods and controlled comparisons

`lbesh_research.benchmark.CORE_METHODS` contains all eight combinations of
ESH/ECP separation, hull/big-M cut reformulation, and single/multi-tree search.
The ECP variant sets `esh=False` in the same implementation. Both separation
rules otherwise retain the same initial cuts, LP phase, reduced NLP policy,
absolute and relative gap settings, feasibility tolerance, and solver thread
count. These are controlled algorithm ablations, not independent solvers.

Default baselines are GDPopt LOA with Gurobi and Ipopt, GAMS SHOT on Pyomo
big-M and declared-convex hull reformulations, and an independently implemented exact conic
hull solved with Gurobi where supported. Optional baseline method names are
`gams-gurobi-bigm`, `gams-gurobi-hull`, `gams-scip-bigm`, and
`gams-scip-hull`. Standard Pyomo nonlinear hull is the package's numerical
perspective formulation; it is not the exact conic baseline. Unsupported
expressions in the conic adapter are explicitly recorded as unsupported.

The primary SHOT hull method is named `gams-shot-hull-convex`; the automatic
convexity-detection method `gams-shot-hull` remains available as a supplementary
baseline. Declared convexity is permitted only for analytically verified
generated instances. Their hull rows use the perspective of a convex
function with a positive affine denominator, plus the affine epsilon
correction. The trigonometric family's argument stays in its verified convex
domain because the disaggregated variable bounds limit the perspective
argument. This declaration supplies the convexity knowledge that LB-ESH and
GDPopt also assume; it is explicitly recorded rather than hidden in status
interpretation.

SHOT uses Gurobi for MIP subproblems and the recorded thread count. Its
integer and nonlinear primal tolerances are `1e-8`, and its linear primal
tolerance is `1e-6`, with automatic
trust in subsolver linear feasibility disabled. The option file uses the
documented `name = value` syntax, and the retained `gams.log` confirms the
effective settings. The hull adapter initializes each disaggregated variable
as `nu = lambda*x`, preventing artificial domain errors when the writer
evaluates inactive perspectives. Purely affine SHOT models use its MINLP
interface. These settings follow the [GAMS SHOT documentation](https://www.gams.com/latest/docs/S_SHOT.html).

The linear setting matches the shared validator's absolute tolerance. A
review fixture showed that requesting `1e-8` linear accuracy could cause
SHOT to reject a Gurobi presolve result with an approximately `1e-6` residual
even though the common original-model validation accepted that residual.
The internal Gurobi log confirmed that SHOT propagated its requested
tolerances; this was not a missing-option fix. The tighter integer and
nonlinear settings are retained following invalid witnesses in the original
logarithmic pilot.

Optional LB-ESH suffixes are `-nonlp`, `-nolp`, and `-usercuts`. They disable
reduced NLPs, disable the LP phase, or enable fractional user cuts,
respectively. Report these as separate methods and retain their exact options.
Do not choose a winning method using held-out results and then describe that
same held-out set as an untouched test set.

The generated suite and its pilot/held-out split are defined in
`code/minlp_solver_lab/lbesh_research/instances.py`. The harness records
manifest metadata and parameter hashes for each run. Historical GDP-library
names are also accepted explicitly; they require their own interpretation of
convexity and do not silently become members of the generated test set.

## Primal validation and numerical success

After a solver reports an incumbent, the harness captures every original
numeric variable and Boolean variable. At extraction, Boolean truth is
derived from its associated integral binary when a transformation updates
only that binary. Solver reformulations and auxiliary variables are excluded
from the original witness. Missing original values are retained as missing,
not imputed from a best observed objective or a reference solution.

The witness is loaded into a clone taken before solver preprocessing. The
independent validator checks original bounds, integer domains, fixed values,
selected disjunct constraints, global constraints, XOR/OR disjunctions,
active logical constraints, and the original objective. Ancestors determine
whether a constraint in a nested block or disjunct is active. A supplied
Boolean and its original associated binary must agree. Undefined or
nonfinite original values and expression evaluation failures reject the
witness.

For a numerical row or bound, the tolerance is
`1e-6 + 1e-7 * max(1, abs(body), abs(bound))`; integrality uses `1e-6`.
The raw maximum residual and residual divided by its tolerance are retained.
The independently evaluated objective is also compared against the solver's
reported objective when available. Validation success establishes numerical
primal feasibility at these stated tolerances.

A record is counted as numerically solved only when its witness passes,
its adapter reports a usable global dual bound, the worker completes, and
the two-sided primal/dual discrepancy is at most
`1e-6 + 1e-4 * max(1, abs(objective))`. This check works in either objective
sense and rejects a materially reversed bound. A time-limit return can pass
if its actual reported gap is closed; an `optimal` status alone cannot pass.

The GAMS adapter captures native `MODELSTAT`, `SOLVESTAT`, `OBJEST`, and
`OBJVAL` through the versioned Pyomo DAT parser before generic status mapping.
For SHOT, SCIP, and Gurobi, it accepts finite `OBJEST` with native model status
1, 7, or 8 as a reported global bound; the independently validated primal and
gap remain necessary. A local-optimal status does not authorize a global
bound. Native statistics and preserved GAMS files permit auditing this
interpretation. SHOT's automatically detected hull can return a weak valid
bound when its expression parser does not recognize perspective convexity;
that bound is retained. The declared-convex method uses native `OBJEST` under
the stated analytic convexity assumption. No early completion heuristic or
internal heuristic objective substitutes for a bound.

Verified reference objectives are optional. A supplied reference must have
`verified: true` and a nonempty `evidence` description. Objective agreement is
two-sided, never `candidate <= reference + tolerance`. A reference comparison
does not replace a missing method-specific bound. The summarizer does not
construct references from consensus or the best observed objective.

## Runtime, failures, and comparisons

Reported `wall_time` starts before launching the worker and includes Python
imports, model construction, preprocessing, interior-point calculations,
optimization, witness validation, and serialization. `worker_time` and all
available solver component counters/times are additional diagnostics; they
are not substitutes for total wall time. The solver time limit and a separate
whole-process wall cap are recorded. Component times overlap: single-tree
`time_master` includes callback NLP and cut generation, so it must not be
added to `time_nlp` or `time_cuts` as a runtime decomposition. Default wall cap is solver time limit
plus 30 seconds, allowing normal startup and postsolve overhead without
unbounded execution. Use a common wall cap for all compared methods.

Every worker is a process-group leader. At the cap, the harness kills the
whole group, including solver descendants. Solver stdout and stderr are
written directly to files, avoiding blocked pipe buffers. The harness sets
OMP, OpenBLAS, MKL, NumExpr, and solver thread counts explicitly. The parent
limits concurrent workers; this study uses one solver thread per worker and
the root agent coordinates concurrent experiments against available CPU and
memory. The harness checks requested workers times threads against reported
CPU count, but does not infer a safe memory budget automatically.

`completed`, `wall_timeout`, `crash`, `unavailable`, `unsupported`, and `error`
are distinct outcomes. A returned invalid witness remains visible as a
completed computation with failed validation; it is never a solve. No failed
or timed-out incumbent is silently replaced with an initialization or bound.

The summarizer reports pairwise runtime statistics on the same instances
solved by both methods and also reports the intersection solved by every
method. It additionally reports all-instance PAR10 means and shifted
geometric means (one-second shift), charging ten times the common wall cap
for each missing or unsolved result. Unsupported methods must be shown in
the full report but should be compared for speed only on a prespecified
common applicable subset; do not interpret their penalty as solver slowness.
The CLI loads the adjacent schedule, so even a missing entire instance or
method remains in the comparison. Missing runs remain penalized, and duplicate instance/method records raise an
error. Repeated experiments use separate output paths and are summarized
separately; do not pool repetitions as if they were distinct instances.

## Reproduction and retained artifacts

Use the existing isolated environment and frozen `uv.lock`. Each run records
Python/package versions, SHA256 hashes of LB-ESH and research module source,
the historical instance builder, the project dependency declaration, and the
lockfile. Legacy runs also hash the vendored GDP-library and Pyomo-example
source/data trees, excluding caches and Git internals. The root environment probe records executable paths, actual solver
license checks, platform, and additional versions. Source hashes are required
because an experiment can run from a dirty worktree.

Each new output path gets an adjacent `.runs` directory containing the
prespecified schedule, per-run solver logs, native GAMS files, worker JSON,
and final JSON with wall time and exit code. The append-only aggregate JSONL
contains full original primal witnesses and validation reports. Existing
output or artifact paths are rejected so an accidental rerun cannot mix
protocol versions.

Launch order is reproducibly shuffled with `--order-seed` (default `0`). The
schedule retains the seed and the complete ordered instance/method pairs.
Each repetition uses the same method and instance sets with a different
prespecified order seed, reducing systematic method-order confounding.
Concurrent completion order may vary with solver runtime and system load.

The reviewed native logs identify GAMS 54.3.1 and SHOT 1.1a81275b4 with
internal Gurobi 13.0.2. These are distinct from the environment's Python
`gurobipy` 13.0.3 and `gamsapi` 54.4.0 package versions; do not report Python
package versions as the native GAMS solver versions.

Example, from `code/minlp_solver_lab`:

```sh
PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH uv run --frozen --no-sync python -m lbesh_research.benchmark --instances lbesh.quadratic.small.s104729 --methods all --time-limit 30 --wall-limit 60 --threads 1 --parallel 4 --out results/lbesh_development/example.jsonl
uv run --frozen --no-sync python -m lbesh_research.summarize results/lbesh_development/example.jsonl
uv run --frozen --no-sync python -m unittest lbesh_research.test_harness -v
```

The legacy `summarize_gdp_final.py` now reports historical raw statuses and
objective presence only. Its old records lack retained original primal
witnesses, so their former consensus-based solved counts are not validation
results and cannot be repaired by relabeling status strings.

Targeted development checks run for this implementation: seven validator and
summarizer regressions; one generated quadratic pilot instance through
LB-ESH hull multi-tree, GDPopt LOA, SHOT big-M, and exact conic hull. All four
adapters returned independently feasible witnesses and closed numerical
bounds. An initial check without Ipopt on PATH correctly recorded
`unavailable`; the corrected PATH run exercised the working adapter. These
are smoke checks, not the publication experiment or project-wide verification.
After baseline initialization and tolerance corrections, the logarithmic
pilot also passed both SHOT big-M and declared-convex hull checks. An
independent reviewer added tests for maximization, native GAMS status/bound
capture, standalone Boolean associations, and actual process-group timeout
cleanup with output exceeding ordinary pipe capacity. Its real affine
maximization adapter check passed for LB-ESH, exact conic hull, and SHOT.
