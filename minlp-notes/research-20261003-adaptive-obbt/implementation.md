# Adaptive OBBT implementation

`solver/adaptive_obbt.py` implements additional optimization-based bound
tightening inside SCIP's branch-and-bound search. It is a working numerical
research implementation for bounded QCQPs. It does not certify a complete SCIP
solve, and its adaptive policy is not a theorem about minimum solving time.

## Interface and supported models

```python
result = solve_problem(problem, policy="adaptive", time_limit=10.0, seed=0)
```

`problem` uses the existing `QCQP` fields from
`research-20260922/iterated-obbt/code/qcqp.py`: variable names, types and bounds,
sparse linear rows, quadratic objective and row coefficients, the objective
sense, and `fmin`/`violation` methods. The experiment interchange class also
implements this interface. The implementation imports neither historical
solution files nor reference objectives. `initial_point` can supply an explicit
feasible test input; the public experiment protocol does not use it. There is no
reference-optimum or externally prescribed cutoff argument to `solve_problem`.

The implementation uses PySCIPOpt 6.2.1 and SciPy's HiGHS dual simplex. Both
solvers receive one-thread settings. There is no commercial solver dependency.
The native SCIP model uses a linear objective or a quadratic objective epigraph.
All returned objective and dual values use minimization form, including models
whose original sense is maximization. `objective_exact` records the incumbent's
exact rational objective under the stored binary64 coefficients and coordinates;
it does not certify the incumbent's feasibility.

Every callback reads bounds from SCIP's transformed versions of the original
variables. Finite bounds discovered by SCIP can therefore make an initially
unbounded model eligible. The sidecar requires every remaining original variable
to have finite current bounds, even if an unbounded variable appears only
linearly. Ineligible callbacks are logged and skipped; SCIP continues normally.
Quadratic expressions are supported, while general nonlinear expressions are
outside this implementation's model interface.

## Compared policies

All three arms retain SCIP's native propagators, including native OBBT and its
other nonlinear routines, with identical solver settings and seeds. This is a
comparison of additional work against an already capable solver.

| Policy | Additional work |
| --- | --- |
| `native` | No added propagator. |
| `fixed` | Bounded coordinate solves in deterministic variable order at eligible events. |
| `adaptive` | Rank nonlinear variables by coefficient-weighted envelope widths, check cached witnesses, and stop an unproductive pilot. |

Both added policies use the same event schedule and resource ceilings. A node's
first eligible visit triggers work. A later visit can retrigger work after the
first incumbent appears, after a sufficiently improved incumbent, or after a
sufficient contraction of a local variable domain. State is indexed by SCIP's
node number, so a sibling does not inherit the other sibling's stop decision or
local box.

The adaptive policy checks whether cached lifted LP points remain feasible in
the newly constructed relaxation. A feasible point close to a coordinate's
current endpoint bounds the possible reduction of that endpoint in this frozen
relaxation. Such a direction can be skipped. This certificate is checked again
after every domain or cutoff change; cached points are never trusted merely
because they were previously returned by an LP solver.

After two unscreened coordinate solves, the adaptive policy stops if accepted
normalized width reductions total less than `1e-3`. This is a heuristic pilot
rule. It does not rule out useful directions that have not been sampled, and
does not bound all future OBBT rounds. The fixed policy provides a direct
comparison for the benefit and cost of this screening and stopping choice.

## Relaxation and bound validation

Each callback builds one frozen local LP. It contains original lifted rows, the
objective cutoff when available, four McCormick rows per bilinear product, and
square tangents and secants. Continuous square auxiliaries have nonnegative
lower bounds whenever their domain crosses zero. Integer domains are relaxed
in the sidecar and remain integer in SCIP.

The implementation interprets stored binary64 data as exact dyadic rational
numbers when constructing new rows. A coefficient rounded to floating point is
accompanied by an outward right-hand-side correction over the finite lifted
box. Auxiliary interval bounds are rounded outwards. These steps ensure that
rounding a generated row does not exclude the exact product graph of the
stored model on the input box.

Coordinate optima reported by HiGHS are not directly installed as bounds. For a
minimization objective `c`, any nonpositive vector `y` gives the valid lower
bound

\[
y^T b+\min_{z\in[\ell,u]}(c-A^Ty)^Tz
\]

on an LP with `Az <= b`. The implementation clips returned inequality
multipliers to the required sign and encloses the residual arithmetic with
directed binary64 rounding. Thus numerical dual infeasibility is accounted for
by a finite-box residual correction. Nonfinite arithmetic, unsupported data,
LP errors, unbounded statuses, and infeasibility statuses yield no proposed
bound. In particular, a sidecar infeasibility report never prunes a SCIP node.
The interval validator assumes ordinary IEEE-754 binary64 arithmetic with
gradual underflow; it is not a portable formal proof checker.

For maximization of a coordinate, the sidecar minimizes its negative and
negates the validated lower bound. It then adds a further outward numerical
margin. Proposals must improve the current interval by a configured threshold
and remain compatible with that interval. Integer proposals are checked for
compatibility after integer rounding before being passed to SCIP.

All accepted bounds use `tightenVarLb` or `tightenVarUb` on the current node.
SCIP owns inheritance and restoration. The sidecar never replaces global bounds
with a child's box. Each logged application records the variable, direction,
validated bound, proposed bound, and local bounds before and after application.

## Cutoff validity

The cutoff comes only from SCIP's current best solution. The original-model
numerical residual must be at most `1e-6`; otherwise the callback proceeds
without a cutoff and increments `rejected_cutoffs`. The objective is evaluated
exactly as a rational expression to avoid cancellation, rounded upward, and
given an additional nonnegative numerical margin. For example, terms
`1e16 + 1 - 1e16` are evaluated as one rather than zero.

These precautions do not prove that an approximately feasible SCIP solution is
an exactly feasible point. Therefore every exact sidecar bound involving a
cutoff is conditional on that cutoff being a valid upper bound. This limitation
also applies when an explicit initial point passes only a numerical feasibility
test. The full solve retains SCIP's ordinary numerical correctness contract.
The exact original-coefficient objective string does not upgrade that contract.

## Time and work accounting

Default settings are fixed before the held-out campaign:

| Setting | Default |
| --- | ---: |
| Total additional directional LPs | 64 |
| Root LPs per callback | 12 |
| Nonroot LPs per callback | 4 |
| Total eligible callbacks | 24 |
| Callbacks per node | 3 |
| Maximum node depth | 64 |
| Sidecar time share | 10% of the solve time limit |
| Individual LP time limit | 0.25 seconds |
| Relative incumbent improvement for retrigger | 1% |
| Relative local width reduction for retrigger | 10% |
| Retained witness count | 24 |
| Retained tangent pool per square | 25 |

Model construction, plugin setup, screening, interval validation, bound
application, and logging all contribute to `wall_time`. Model setup is
subtracted from SCIP's remaining time allowance. If setup has already exhausted
the allowance, the result is `setup_time_limit` and optimization is not started.
The sidecar's `time` includes complete entered callbacks, including unsupported
and unproductive callbacks. `lp_time` isolates the HiGHS call and subsequent
bound validation; `lp_calls` counts every attempted coordinate solve.

The callback checks both its remaining aggregate budget and the overall solve
deadline. LP construction checks its deadline every 64 rows; witness processing
checks between cached points. Individual construction, solver, and validation
operations are not preempted. Small budget overruns are possible and remain
charged in the actual measured times. The external experiment runner provides
a separate termination ceiling. A nominal time budget is not represented as an
exact maximum wall time.

## Relation to the theory

The implementation deliberately distinguishes three guarantees:

1. Validated numerical dual bounds support current-node domain changes,
   conditionally on the incumbent cutoff as described above.
2. Exactly checked primal witnesses support endpoint screening for one frozen
   LP, and are invalidated by a failed current-domain or cutoff check.
3. The separate protected-box and coupled-map theory concerns future
   tightening. The plugin does not use those certificates to claim that its
   pilot rule bounds all remaining benefit.

Square tangents are retained in a shared globally valid pool up to a fixed
capacity; current local knots are also included. After the retention cap, a
local knot can disappear on a later callback. Consequently the finite-tangent
implementation is not asserted to be an isotone relaxation family, and the
future-iteration theorems are not applied to its callback sequence.

The implementation is additive rather than a replacement for native OBBT. It
does not claim a general policy for allocating time between tightening,
separation, decomposition, and branching. The experiments measure whether this
specific, bounded policy is useful after its actual costs are included.

## Targeted verification

Run from the repository root:

```sh
cd research-20261003-adaptive-obbt/solver
../../code/minlp_solver_lab/.venv/bin/python -m unittest -v test_adaptive_obbt
```

The targeted tests check exact graph containment, outward dual correction,
both coordinate senses, cancellation-resistant objective evaluation,
infeasibility-status handling, cutoff and sibling witness invalidation,
no-incumbent behavior, actual in-tree bound applications, incumbent retriggers,
integer solutions, budgets, and local bound changes that leave global domains
unchanged. `solver/targeted-tests.log` records the author checks. The independent
review has additional tests in `reviews/test_solver_review.py`.

No project-wide verification or CI inspection is part of these local checks.
