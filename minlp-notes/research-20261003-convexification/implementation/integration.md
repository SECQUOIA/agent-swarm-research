# Native-preserving original-row aggregation

`solver/integration.py` strengthens the model from `solver/model.py` without
replacing its nonlinear rows or adding graph variables. Baseline, `all`, and
`auto` use exactly the same builder, declared variable bounds, domain guards,
objective epigraph, native constraints, presolve settings, and native handlers.
Only `all` and `auto` install an additional global root separator. The builder's
optional domain witnesses preserve partial-function domains; they occur in
all modes and are described in `numerics/model-contract.md`.

Discovery runs at the first eligible root LP callback. A model solved before
that callback pays no discovery, sample, support, or cut cost. A run that finds
no cuts retains the same original native formulation, although callbacks and
analysis still cost time. No native aggregation or handler is disabled to make
cuts easier to insert.

## Original-row projection

For a signed source side, write

\[
h_r(x)+d_r^T v\le b_r.
\]

Here `v` contains the original variables and, if present, the original objective
epigraph. Each finite upper side uses sign `+1`; each finite lower side uses
sign `-1`; equality rows supply both. For minimization the objective epigraph
side is `objective_expression - objective_epigraph <= 0`; maximization negates
this side. Constants are included in `b_r` exactly.

An exact source expression is expanded additively and multiplicatively, without
multinomial expansion of powers. Rational affine summands are extracted; all
remaining summands form `h_r`. This is an exact value identity on the original
source domain. It never deletes the native expression or its domain guards.

Given nonnegative binary64 multipliers `lambda_r`, the support oracle certifies

\[
a^T x+\sum_r\lambda_r h_r(x)\ge\beta.
\]

Substitution yields a row on original variables:

\[
a^T x-\sum_r\lambda_r d_r^T v\ge
\beta-\sum_r\lambda_r b_r.
\]

The elimination uses exact rational arithmetic. `solver/row_certificate.py`
then rounds the resulting coefficients to their actual binary64 values. For
coefficient error `e = exported - exact`, it adds the rigorous lower bound
`sum min(e_i L_i, e_i U_i)` to the exact right-hand side and rounds that right-hand
side downward. A nonzero rounding error on an unbounded coordinate is rejected.
This includes the unbounded objective epigraph: its coefficient must remain
exact. Zero coefficients, cancellation, duplicate affine terms, underflow, and
rational constants are handled without a heuristic safety shift.

Before insertion, the separator checks SCIP's actual row coefficients, bound,
constant, scope, and source-to-transformed variable mapping. Unsupported native
substitutions or merged columns cause rejection. No presolve identity is assumed
without a certificate. This check may discard useful rows; it does not modify
presolve to retain them. Rows are global, root-only, and removable.

## Discovery and prospective activation policy

Candidate domains have at most four nonlinear coordinates with finite globally
proved bounds. Single rows and overlapping row groups are considered, with
at most six signed nonlinear sides per group, 32 groups, and 16 original affine
domain sides per group. Multivariate nonpolynomial blocks are skipped. Polynomial
rows have degree at most eight; quadratic blocks use the new exact polytope
oracle subject to its enumeration budget. The inherited certified support
kernel supplies supported fallback bounds. Bound-tightening certificates and
original affine domain row identities are retained for replay.

The `auto` policy was fixed before the new benchmark outcomes. It admits only
quadratic blocks containing a signed quadratic that is not proved convex and
having either a non-axis affine domain restriction or at least two distinct
nonlinear source rows. Convex-only, elementary, and unrestricted single-row
blocks are skipped. Two support failures deactivate a block for the remaining
callbacks. `all` tries every discovered supported block within the same resource
limits. These are policies for this prototype, not mathematical assertions
about the usefulness of other blocks.

Defaults are three root callbacks, 12 cuts, four cuts per callback, 24 support
calls, and three LP exchange attempts per block per callback. Callback work
receives `min(1 second, 5% of requested total time)`. Time is checked between
operations, including individual source rows, additive terms, and block-group steps during
discovery. An expired discovery budget stops the separator, discards its
unfinished discovery, and records `discovery_incomplete` and `budget_exhausted`.
It supplies no coverage or hull-membership conclusion. One in-progress exact
oracle, symbolic row analysis, or LP may overrun
that allowance. The experiment worker's process cap provides a separate hard
limit. Setup and callbacks are charged to the total solve budget.

Each signed source row first supplies a single-row support direction, including
the objective row. A bounded sample LP then searches joint directions: coordinate
normals are free in sign and normalized into `[-1,1]`, while nonlinear row
multipliers lie in `[0,1]` before positive rescaling. Exact support minimizers are
added to the heuristic sample when available, followed by a bounded retry.
Floating samples, their filtering, the LP, and scaling propose candidates only;
none establishes a lower bound. The final support is recertified for the actual
binary64 direction. Candidates are accepted only after final coefficient
conversion and a sufficient original-coordinate violation. The default scaled
violation is `1e-5` for `all` and `5e-4` for `auto`.

## Evidence and limits

Each inserted row records the original signed source sides, support features,
source-coordinate box, original affine domain row identities, binary64 support
direction, support witness, exact elimination/rounding certificate, and actual
SCIP row. The result also retains the common source-model/domain/bound metadata,
original-variable incumbent, numerical SCIP bounds, timing, selection decisions,
and failure counters. Original side identities are the replay authority; text
renderings of nonlinear expressions are explanatory and are not executed.

This is a certified-cut prototype, not a certified SCIP solve. The common
builder checks its submitted expression DAG, not every later native numerical
transformation. Primal and dual bounds are numerical SCIP results. Failure to
find a cut does not prove membership in a projected hull. The bounded practical
row-multiplier search is separate from the complete finite-tolerance graph
separation procedure documented in the theory work. Neither method makes
arbitrary-dimension exact quadratic optimization polynomial time.

Unsupported input syntax is a structured refusal. Unsupported cut blocks simply
retain native SCIP. Timeouts, rejected rows, unfavorable solve outcomes, and
models not admitted by the importer must remain visible in experimental reports.

## Targeted checks

Commands actually run during implementation:

```sh
PYTHONPATH=research-20261003-convexification code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/solver/test_integration.py
PYTHONPATH=research-20261003-convexification code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/solver/test_row_certificate.py
```

The integration checks cover signed source sides and objective constants,
nonnegative row multipliers, exact row projection, source-value decomposition,
lazy discovery, actual inserted SCIP row replay, unchanged graph variable count,
fixed automatic activation, unsupported dimension fallback, and structured parse
failure. The row arithmetic tests cover rounding boundaries and changed-input
replay rejection. Independent review and campaign replay are recorded separately.
No project-wide checks or CI inspection are part of this work.

## Frozen campaign and final source

The campaign snapshot froze `solver/integration.py` at SHA-256
`5620d3f26473e56e0f0f0b086412508caa416bc190e207d85ea6c815db73e1be`.
Three final defensive changes reached the live source while that freeze was
being communicated: reject a converted right-hand side at SCIP's infinity
sentinel, reject such a bound in the actual-row audit, and catch a failed
heuristic evaluation of an exact support minimizer without discarding its
already valid support result. That intermediate live hash was
`9f5f791277166c01be07726c0268eb273d348f8e8a0abd8193e45a4a580a1572`.
The frozen implementation and every outcome remain preserved. These changes
do not alter the activation policy, support mathematics, or original model.

All reported campaign timings belong to the frozen source. Independent replay
checks the recorded row bounds against the infinity sentinel; any worker
exception remains part of the evidence. Live-source performance has not been
substituted for the frozen results. The final integration and row arithmetic
test command above passed 70 tests. An earlier combined collection attempt
failed because the row arithmetic test used a bare module import; its import
was corrected to the project package before that passing run.

The frozen campaign subsequently exposed a distinct sparse-model defect in
`chp_partload` and `waterno2_06`: constructing each term's polynomial with every
global model symbol exceeded SymPy's recursion depth. The correction uses only
symbols present in that term. Rational constants are handled directly;
nonrational coefficients remain in the nonlinear remainder, as required by the
rational affine contract. An oversized product that still exceeds polynomial
recursion limits also remains in the nonlinear remainder and is declined by
the existing block dimension cap. A 1,200-variable sparse regression and a
1,400-variable single-product regression cover both paths.

Actual discovery then completed on both original diagnostic models, but its
sequential work exceeded the existing callback allowance. The final correction
checks that same allowance between source rows and group steps, with the
explicit incomplete result described above. No activation threshold or model
selection rule changed. The final source hash is
`128fe10b13d22874aa6f76d86ed2a11f73076ddb747967cc7e468225c3203210`.
All 75 targeted integration and row arithmetic tests pass. On the original
2,248-variable `chp_partload` model, a direct one-second discovery allowance
returned the explicit incomplete result after 1.00262 seconds. Frozen failures
remain in the primary evidence; separately identified matched diagnostic
reruns use the corrected source. Their timings must not replace the primary
campaign's results.
