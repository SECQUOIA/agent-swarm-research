# Scalar Markov measurement-selection implementation

The prototype in
[`markov_design.py`](../code/research_20260912/markov_design.py) implements both
requested binary-exact formulations and a shared outer-approximation algorithm.
It supports multiple independent scalar AR(1) chains with one shared prior
information matrix and one total cardinality constraint. The adjacent
[`README.md`](../code/research_20260912/README.md) gives commands, APIs, and bound
semantics. This note records implementation and validation facts; theoretical
and prior-art claims belong in the separate research notes.

The path master has binary visits and continuous arc flows, including source,
sink, and empty-path arcs. Arc information uses the gap between consecutive
selected times, so it exactly accounts for marginalization over omitted times.
The dense master uses the binary-exact concave extension with a separate
`a = lambda_min(R)/2` for each chain. Both use analytic log-determinant gradients.

The integer algorithm rebuilds the branch-and-bound search through repeated
linear master solves. It adds full-selection and feasible-seed tangents before
the first solve. Subsequent tangents are evaluated at the returned integer
selection. Only the direct original dense subset objective updates the feasible
lower bound. The upper bound is the minimum of the full-selection value and all
finite Gurobi master bounds seen. Stopping uses an absolute log-determinant gap.
An independently implemented dense covariance solve checks the final formulation
objective. Models and environments are closed after each run.

The continuous solver uses the same implementation with relaxed visits and LP
masters. Its reported feasible relaxation value is deliberately separate from
the integer lower-bound field. Integer runs do not inherit relaxation cuts or
bounds; comparisons therefore measure the implemented formulations and basic
outer approximation without a separate root-seeding policy.

Initial validation used NumPy 2.5.3 and Gurobi 13.0.3 in the shared uv environment.
Every model used `Threads=1`, `Seed=0`, quiet output, `1e-9`
feasibility/integrality/optimality tolerances, and absolute master MIP gap at most
`1e-9`. No individual solve had a budget above 30 seconds.

The validation command passed the following checks:

- All 128 subsets of each of four seven-candidate, three-parameter generic
  instances, with correlations 0, 0.6, 0.95, and −0.4, and all 128 subsets of a
  two-chain, two-parameter instance. Both formulation information matrices were
  compared with original dense subset covariance solves. The largest relative
  matrix discrepancy was `4.53e-15`.
- Directional finite-difference derivatives at fractional points, with maximum
  relative discrepancy `5.91e-10`, plus tangent upper-bound checks at the two
  endpoints used to construct those points.
- Both integer formulations reached the enumerated optimum for all five
  instances, with a requested absolute gap of `1e-6`. Both continuous solvers
  closed their own gap to `1e-6` and returned bounds above the integer optimum.
- Cardinalities zero, one, and all five observations on an additional instance;
  a zero-round run that retained a valid feasible seed and reported
  `iteration_limit`; and analytic A → B → C sensitivities checked by finite
  differences in log parameters.

The full initial output is
[`validation-implementation.json`](../code/research_20260912/validation-implementation.json).
Runtime fields there describe one validation run and are not a performance study.

A separate smoke test used the reaction family with 16 candidate times,
cardinality five, and correlation 0.8. The path integer and continuous solvers
both closed the gap in two outer rounds at objective `11.837874832068607`. The
dense continuous optimum was enclosed by an upper bound `12.132255884807783`
with gap below `1e-6`. With a five-second budget, the dense integer run returned
the same feasible objective as the path solver but retained an upper bound
`12.139116023848816` and correctly reported `time_limit`. This illustrates the
bound/status handling and one relaxation-strength difference; it is not a
general runtime claim.

The implementation assumes fixed sensitivities, fixed known covariance
parameters, consecutive candidate indices, and scalar observations. It does not
fit kinetic parameters, optimize sampling times continuously, or implement
multivariate state-space covariance blocks. Its bounds rely on floating-point
linear algebra and solver tolerances. An upper bound can undershoot a feasible
value by roundoff; material contradictions receive a numerical-failure status.
