# Independent review of the rational LP and convex box-QP backend

Reviewed `solver/rational_optimization.py` independently of its author. This
review covers the two-phase simplex, its primal/dual and Farkas witnesses, the
PSD test, convex box-QP active-face search, and their input and resource-limit
behavior. It does not certify the callers or establish a polynomial running
time for these implementations.

**Outcome:** one iterable-input defect was found and fixed. No remaining
mathematical or witness-verification defect was found in the reviewed scope.

## Proof and implementation checks

- The LP's inequality multipliers have the correct sign for minimization with
  `G x <= h`. Optimality is checked through primal feasibility,
  `c + G^T lambda + E^T mu = 0`, nonnegative `lambda`, and equality of primal
  and dual values. Infeasibility is checked by a zero combined left-hand side
  and strictly negative combined right-hand side. An unbounded result requires
  both a feasible point and a strictly improving feasible recession ray.
- Phase-I row transformations retain all original constraint coordinates when
  redundant rows are removed. A zero artificial basic variable can be pivoted
  out with either pivot sign without changing feasibility. The entering and
  ratio-tie rules use the variable indices required by Bland's rule.
- The PSD test handles zero pivots and singular matrices: a zero diagonal in a
  PSD matrix forces its row to vanish; otherwise a positive diagonal permits
  an exact Schur-complement reduction.
- For each QP face, nonsingular free stationarity equations determine a
  candidate. Singular equations are combined with the active-coordinate
  gradient signs in an exact feasibility LP. Every accepted point is checked
  again for PSD, primal feasibility, complementary slackness, stationarity,
  and the objective value. Fixed coordinates allow either bound multiplier.
- The QP's floating coordinate-descent proposals supply only candidate faces.
  They do not participate in exact acceptance. Disabling them still solves
  the selected singular test cases.

## Defect found and correction checked

The call

```python
solve_convex_box_qp((row for row in [[2]]), [-1], [(0, 1)])
```

initially raised `ArithmeticError` after finding the correct minimizer. Final
self-verification reused the consumed original matrix iterator instead of the
normalized matrix. The author changed that call to use normalized `h` and added
a regression test. Independent rechecks passed for both an iterator of rows
and iterators nested inside the rows, with iterated coefficients and bounds.
Both produce the exact point `1/2` and value `-1/4`.

## Targeted experiments actually run

The independent randomized script ran with Python, SciPy 1.18.0, seed
`20261003`, and one BLAS/OpenMP thread:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python /tmp/review_rational_oracles.py
```

The script was an ephemeral review harness, not an additional maintained solver
test suite. Its results were:

| Check | Result |
| --- | --- |
| 1,600 random LPs, one to five variables, mixed inequality/equality rows, unrestricted or finite bounds, redundant and zero rows | All statuses agreed with SciPy HiGHS: 467 optimal, 946 infeasible, 187 unbounded. All exact witnesses replayed. Optimal values agreed within `1e-6`. |
| Invalidated LP witnesses in those 1,600 cases | All rejected: changed optimal value, zero improving ray, or zeroed Farkas multipliers, as appropriate. |
| 320 PSD box QPs, one to five variables, rational Gram matrices of ranks zero through five | All solved with exact PSD/KKT witnesses. Results agreed with successful SLSQP runs within `1e-5`; no numerical comparison supplied acceptance evidence. |
| Altered QP objective values and negative lower/upper multipliers | All rejected. |
| Three singular QPs with numerical proposals disabled | All solved and replayed exactly. |
| Coefficient scales `10^1000` and `10^-1000` | Both solved exactly; no float conversion was required for acceptance. |
| Classical degenerate simplex cycling example | Correct optimum `-1`; terminated in 20 pivots. |

Separate direct Python probes passed for empty-dimensional LPs and QPs,
contradictory zero rows, unrestricted unboundedness, redundant equalities, and
fixed boxes with either gradient sign. Another probe rejected 18 malformed or
invalid witnesses, checked three resource-limit statuses, four PSD/nonconvex
cases, and three invalid budget arguments. Following the iterator fix and
callback addition, two iterable-matrix checks, three callback interruption
checks, and a successful solve with a counting callback passed.

No project-wide test command or CI inspection was performed for this review.

## Limits of the evidence

The exact witnesses, rather than the floating reference solvers, establish the
reported LP and convex-QP conclusions. Random tests are useful implementation
evidence, not exhaustive correctness proofs. The LP can take exponentially
many pivots; the QP can visit exponentially many faces. The implementation
reports explicit pivot/face limits without turning them into infeasibility
claims. Callback checks permit cooperative interruption, rather than imposing
a hard operating-system time or memory bound.
