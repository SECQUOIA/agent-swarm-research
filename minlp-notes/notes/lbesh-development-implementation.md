# LB-ESH implementation development, 2026-09-19

The repaired implementation accepts incumbents only after numerical validation
of the original GDP and its original objective. Its status `optimal` means
that a numerically accepted incumbent and the master solver's numerical bound
agree within the configured objective tolerance. It does not certify exact
feasibility, an exact upper bound, or an interval enclosure of the optimum.
The result states `rigorous_certificate=False`, records
`incumbent_validation="numerical_within_tolerance"`, and reports
`feasibility_tolerance` and `max_primal_violation`.

## Correctness repairs

- Single-tree big-M now accepts validated master incumbents with reduced NLPs
  disabled. The previously failing example `min x`, `0 <= x <= 4`, with
  `x >= 1` XOR `x >= 3`, returns the known optimum 1 in all four formulation
  and tree combinations.
- Every incumbent is checked for finite values, variable bounds, fixed values,
  integer values, XOR selection, global rows, and selected-disjunct rows.
  Integer values within the feasibility tolerance are rounded before row
  validation. Inactive disjunct constraints are not required.
- The objective is reevaluated from the original Pyomo expression. A relaxed
  nonlinear-objective epigraph value or an NLP termination code cannot by
  itself establish an incumbent. Validated nonlinear-objective solutions set
  their epigraph value to the recomputed original objective in minimization
  form. Both objective senses are tested.
- Single-tree optimality requires a finite, closed numerical gap. Large
  inconsistencies between incumbent and master bound cannot imply optimality.
  Bounds are no longer silently clamped to an incumbent. Ambiguous or cutoff
  master terminations are not reported as infeasible. Infeasibility after an
  accepted incumbent is reported as a numerical error.
- Callback exceptions terminate the solve and produce `numerical_error` with
  the exception detail. Nonfinite nonlinear values, gradients, or required
  separating cuts fail closed. Initial cuts use bounded deterministic retries
  and raise an error if no finite tangent can be initialized. Outside a
  callback, evaluation failures propagate as exceptions rather than generating
  a successful solve record.
- Multi-tree no longer applies an incumbent objective cutoff based on a merely
  tolerance-feasible point. `nlp_at_integer=False` now also avoids reduced NLPs
  in the multi-tree algorithm.
- Disjunctive bound propagation includes the selected branch's own indicator
  in the union. Previously, an explicit global constraint linking the
  indicators could incorrectly force both indicators to zero.
- OBBT logging now has an initialized clock during solver construction. Bound
  propagation and OBBT remain floating-point preprocessing, not certified
  interval procedures.
- Active orphan disjuncts, nested disjuncts, OR disjunctions, objectives inside
  disjuncts, SOS constraints, nonlinear equalities, two-sided nonlinear rows,
  nonfixed GDP indicators inside disjunct rows, and unknown formulation names
  are refused. Convexity and differentiability
  remain user assumptions; the code does not verify them.
- Constant infeasible rows remain rows. A constant contradiction in one
  disjunct excludes that branch without incorrectly rejecting a feasible
  alternative. Declared variables are retained even when absent from rows,
  so inconsistent bounds on an otherwise unused variable are not ignored.
- Fresh review identified a further fixed-variable mutation risk in reduced
  NLP seeding. Fixed variables are now left unchanged; primal validation
  normalizes tolerance-sized fixed-value deviations to the exact stored fixed
  value before evaluating constraints and the objective.
- Fresh review also showed that treating another native XOR indicator as an
  ordinary disaggregated coordinate can weaken the claimed individual
  polyhedral hull. The supported input scope now refuses all nonfixed GDP
  indicator references inside disjunct rows. Global logic linking indicators
  remains supported. This matches the independent conic baseline's scope.
- Zero cut coefficients do not create `0 * infinity` big-M calculations.
  `add=False` no longer adds constraints during separation.

## Experimental accounting

ESH and ECP retain the same interior-point initialization policy for controlled
comparison. `time_interior` records the whole initialization phase separately,
while `interior_nlps` counts actual NLP attempts. Existing `time_nlp` measures
reduced NLP work. In single-tree mode `time_master` includes callback work,
so these times must not be added as disjoint costs. `time_setup` measures
construction and preprocessing; `time_total` and the solve time budget include
that setup cost. OBBT LPs receive the remaining Gurobi time limit; default
Ipopt calls receive a remaining CPU-time limit. Exhausted budgets suppress
further interior attempts and single-tree optimization. These are solver
limits, not a guarantee of hard wall-clock preemption; arbitrary non-Ipopt
NLP plugins do not have a portable generic timeout in this implementation.

The LP phase reports `lp_end_reason`: no separating cuts, stagnation, iteration limit,
time limit, or master status. A stagnation or limit exit does not establish
fractional-point feasibility. The existing lambda threshold remains in use;
no weighted-residual theorem or certified skipping rule was implemented.
`lp_bound` retains the best optimal LP objective reached, including when cuts
were added after that solve; it is reported in the original objective sense.
`last_lp_max_perspective_violation` evaluates `max λ[g(ν/λ)]_+` over every
positive-weight hull branch, including weights below the separation cutoff.
It is `None` for big-M, and infinity if evaluation is undefined. This is a
floating-point residual, not an interval-certified bound.

## Targeted verification

Working directory: `code/minlp_solver_lab`. The final targeted command is:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH \
uv run --no-sync python -m unittest discover \
  -s lbesh/tests -p test_publication_contracts.py -v
```

The 12 test methods include four linear formulation/tree combinations, four
nonlinear maximization combinations, and eight exponential instances across
ESH/ECP, hull/big-M, and multi/single-tree with reduced NLPs enabled. The latter
have the analytic optimum `log(2)`; all returned values differed by less than
`7.5e-9`, with maximum accepted row residual below `1.5e-8`. Other checks cover
invalid candidates, callback failure, nonfinite separation, objective-gap
requirements, input refusals, OBBT initialization, constant infeasible
branches, unused contradictory bounds, and the indicator-bound regression.
All solver instances use one thread. Gurobi's available academic license
successfully solved the test instances.

Earlier invocation mistakes used an incorrect working directory or import
path; those commands ran no semantic tests and were corrected. A separate
inline `uv run --no-sync python -` exponential oracle check also passed all
eight combinations before being retained in the test module. `git diff
--check -- code/minlp_solver_lab/lbesh` passed. No project-wide verification or
CI inspection was performed.

Reproduction environment: Python 3.13.11; Pyomo 6.10.1; gurobipy 13.0.3; NumPy
2.5.3; SymPy 1.14.0; SciPy 1.18.1; Ipopt 3.14.20 with ASL 20231111. Dependencies
came from the existing isolated project `.venv`; no package installation was
needed. The exponential integration method skips if `ipopt` is absent from
`PATH`, so reproduction must include the indicated solver path or equivalent.

A fresh independent review is requested separately; this note records the
implementation author's checks and does not claim independent review.
