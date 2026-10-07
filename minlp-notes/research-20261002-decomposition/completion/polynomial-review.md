# Independent polynomial solver review

Reviewed `solver/polynomial_grid.py` and `solver/verify_polynomial.py` against
the corrected-grid argument and exact finite-state optimization contract.
The review did not change either implementation.

The implemented bound and pruning rules passed this review. The independent
tests are in `solver/test_polynomial_review.py`.

## Mathematical checks

- Repeated exact differentiation and monomial interval evaluation give valid
  upper bounds on each diagonal second derivative throughout the original
  box. Using nonnegative upper bounds is sufficient; absolute Hessian bounds
  are unnecessary for the interpolation inequality.
- Sequential coordinate interpolation gives the corrected-grid lower bound.
  The maximum adjacent cell length at each node charges every adjacent cell.
  Native integer unit gaps need no correction because they have no feasible
  interior labels.
- If a diagonal curvature cap is zero, the objective is concave in that
  coordinate with all other coordinates fixed. Endpoints alone suffice for
  the minimum, including for native integer coordinates. The pruning history
  still preserves interior optima when a coordinate is flat.
- Continuous filtering retains every cell whose endpoint minimum margin does
  not exceed the feasible upper bound. Integer filtering separately retains
  eligible grid labels and all interior integer labels of eligible skipped
  intervals. Taking hulls of these sets is conservative and preserves every
  global optimizer.
- A completed stage's lower bound remains valid for the original domain
  because earlier discarded regions contain no better point than the current
  incumbent. Restarting from the original box is valid. If the restarted
  computation is interrupted before completing another stage, the final
  replay domain must be the last completed stage's domain; the implementation
  does this.
- The checker recomputes interval bounds, local costs, all directed Bellman
  equalities, the attained grid minimum, all coordinate minimum margins,
  filtering, cumulative bounds, and the final claimed accuracy. It shares
  input parsing, decomposition validation, and exact objective evaluation
  with the producer; it does not call the producer's optimizer, grid
  construction, derivative-bound routine, or finite DP optimization routine.
- When every varying coordinate is native integer, substituting fixed
  rational coordinates makes each remaining monomial integer-valued up to
  its rational coefficient. If `D` is the least common multiple of those
  coefficient denominators, every feasible objective lies in `(1/D) Z`.
  A feasible upper bound `U` and a verified lower bound `L` with
  `0 <= U-L < 1/D` therefore prove that `U` is the exact optimum. The checker
  independently substitutes fixed coordinates, recomputes `D`, and validates
  the strict separation and the pre-lattice lower bound. This rule is not
  applied when any original continuous coordinate varies.

## Adversarial and reference checks

Run from `research-20261002-decomposition/solver`:

```sh
python -m unittest -v test_polynomial_review.py
```

Result: **11 tests passed**, approximately 0.4 seconds on the final review run.

The tests provide the following distinct checks:

- 24 random signed quartic factor models on a path: exhaustive enumeration
  of 81 grid assignments each agrees with the sparse DP minimum and all 288
  coordinate minimum margins.
- 1,326 exact rational comparisons against manually differentiated formulas
  for a polynomial with mixed signs and intervals crossing zero. Both
  implementations' intervals contain all sampled values.
- A mixed continuous/integer quartic model with a known unique global
  minimizer, obtained from a sum of nonnegative polynomials: every completed
  stage retains that minimizer, and final bounds contain its exact value.
- Ten dense coordinatewise concave quartic models: zero-curvature-cap endpoint
  optimization agrees with exhaustive corner enumeration, and each exact
  certificate replays.
- A genuinely quartic integer model: completion agrees with exhaustive
  enumeration of the full native integer domain.
- A shifted integer domain with rounded input bounds: a known optimal label
  lies strictly inside a skipped initial grid interval and survives every
  completed filtering step. A flat integer coordinate with a zero curvature
  cap preserves its entire interval of optimal labels while another
  continuous coordinate is refined.
- Explicit zero-stage, zero-time, and insufficient-table limits return valid
  replayable incomplete certificates. A forced trial restart followed by a
  time interruption preserves the previously narrowed domain `[0,1/2]`.
- Thirteen malformed-certificate mutations are rejected, including changed
  curvature, messages, minimum margins, witnesses, filtering, final domains,
  and a fabricated exact status.
- A normal geometric solve of a polynomial with two integer coordinates and
  one fixed rational coordinate triggers the new lattice rule after two
  stages. Substituting the fixed coordinate gives `D=18`; the verified lower
  bound `-71/8` is within `1/24 < 1/18` of the incumbent `-53/6`.
  Exhaustive enumeration of all 100 integer assignments confirms the exact
  value. Three malformed lattice proofs are rejected. Separate checks reject
  equality at the value-spacing threshold and a fabricated lattice proof
  for a varying continuous coordinate.

These are targeted local checks. No project-wide test run or CI inspection was
performed.

## Scope and remaining limits

The checker proves the reported objective bounds and pruning history. It does
not authenticate timing statistics or enforce the advertised conditioning
schedule from metadata. Complexity guarantees concern the producer algorithm
under the theorem's fixed-degree, supplied-decomposition, and growth
assumptions; certificate validity does not need those growth assumptions.

The generic polynomial solver certifies approximation. A zero gap is exact;
the reviewed coefficient-lattice rule also produces exact values when every
varying coordinate is native integer. General exact algebraic output is not
implemented by this grid routine.
The separate nonlinear boundary adapter has its own review.

Timing is cooperative. Expensive exact input evaluation, differentiation,
interval preprocessing, and integer exponentiation can finish after a
requested wall-clock limit before the next budget check. This is a resource
limitation, not a lower-bound or pruning defect. Extremely large exponents
are accepted inputs without a polynomial-time claim in the degree.
