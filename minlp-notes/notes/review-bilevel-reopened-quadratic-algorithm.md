# Independent review of the scalar quadratic response prototype

Date: 2026-09-06. Status: passed after one certificate-interface correction
and two claim clarifications. Includes the later quadratic upper objective
and complete aligned rank-one sweep refinements.

Scope: [quadratic_solver.py](../code/bilevel_reopened/quadratic_solver.py),
and [algorithm note](bilevel-reopened-quadratic-algorithm.md), implementing the scalar-leader specialization of the
[fixed-rank quadratic corollary](bilevel-fixed-rank-quadratic-corollary.md).
This review was conducted by a separate agent from the implementation author.
It does not establish novelty or performance on industrial models.

## Mathematical audit

For a proposed active pattern, let `F` and `A` denote its free and upper-bound
coordinates. The fixed upper coordinates contribute `U_A^T 1` to the aggregate.
Writing `D_F=Diag(d_F)` and `G=U_F^T D_F^{-1} U_F`, the free system is

```
(D_F + U_F H U_F^T) z_F = b_F,
w_F = (I + G H)^{-1} U_F^T D_F^{-1} b_F,
z_F = D_F^{-1}(b_F-U_F H w_F).
```

The implementation uses these equations with the correct order `G H`.
Positive definiteness of `Q` implies positive definiteness of the free
principal submatrix. The determinant identity

```
det(D_F + U_F H U_F^T) = det(D_F) det(I + G H)
```

therefore establishes invertibility of the small system. It does not require
`H` to be positive semidefinite, invertible, or full rank. Empty free sets
and zero aggregate dimension remain valid. The exact constructor verifies
positive definiteness through a dense fallback when `H` is indefinite and has
dimension greater than one. For a negative scalar `H=(h)`, it uses the exact
equivalent test `1+h*sum_i u_i^2/d_i>0`.

Each response component and gradient component is affine in the scalar
leader. Free components must lie in the unit interval; gradients must be
nonnegative at the lower bound, zero at free coordinates, and nonpositive
at the upper bound. Intersecting these affine inequalities with the leader
interval gives the full validity interval of the proposed pattern. Weak
inequalities preserve zero-length intervals. At a zero-length interval,
checking a free-coordinate gradient at that point is sufficient; it need
not vanish outside the interval.

The certificate verifier checks bounds and KKT conditions at both interval
endpoints. Since all involved expressions are affine, this verifies the
whole interval. The constructor's positive definiteness assumption makes
each such response the unique global follower optimizer. Thus overlapping
certified intervals agree wherever they overlap, including degenerate
clipping boundaries, without a separate continuity assumption.

The path verifier checks every interval, the extreme domain endpoints, and
absence of gaps in the sorted union. Together these conditions establish
full domain coverage, including a singleton leader domain. The adaptive
algorithm samples the midpoint of an uncovered open interval. A recovered
singleton may split this interval but cannot incorrectly establish coverage.
For an empty interval family and a singleton domain, it explicitly recovers
the response at the singleton.

Upper affine constraints are intersected with each certified interval by
exact arithmetic. Affine objective minima occur at endpoints of the resulting
closed intervals. Comparing their rational objective values therefore returns
a global optimizer, or certifies infeasibility when every interval becomes
empty. This remains valid for disconnected feasible sets, isolated feasible
leaders, and equality constraints encoded by two weak inequalities. The added
upper terms `o_xx*x^2+x*o_xz^T*z` become a univariate quadratic after substitution.
Checking its interval endpoints and its stationary point when the leading
coefficient is positive gives the exact minimum, including concave and affine
degeneracies. The implementation uses the correct coefficients without an
implicit factor of one half.

## Complete aligned rank-one sweep

For `Q=D+h*u*u^T` and `C=gamma*u`, `gamma>0`, put
`t=gamma*x+h*u^T*z`. The box response is
`z_i(t)=clip(-(c_i+u_i*t)/d_i)`. Its weighted aggregate has derivative
`A'(t)=-sum_free u_i^2/d_i` on each threshold interval. Hence

```
x'(t) = (1+h*sum_free u_i^2/d_i)/gamma > 0.
```

For negative `h`, strict positivity follows from the full rank-one SPD test;
for nonnegative `h` it is immediate. The map is continuous, and its tails
are affine with positive slope because every nonzero-loading coordinate
eventually clips. Therefore it is an increasing bijection of the real line.
This proves that the sorted two thresholds per nonzero loading cover the full
response, including signed loadings and negative coupling.

The implementation initializes each coordinate at its correct negative-infinite
tail value, processes all events at the same threshold together, and updates
weighted affine coefficients for the objective and each constraint. The zero
loading case is constant and requires no threshold. Its interval inversion
`t=(gamma*x+h*A_0)/(1-h*A_1)` and transformed response coefficients are correct.
Both adjacent cells include a threshold; their response values agree there.
Clipping against upper constraints preserves isolated feasible leaders.

There are at most `2N+1` intervals. Each coordinate changes its formula twice,
so the `O(N log N+N(m+1))` rational operation bound follows by sorting and
updating `m+3` weighted sums. This count includes scanning the upper constraints
on every interval; it does not reconstruct all `N` response coordinates there.
Only the winning response is reconstructed. Polynomial rational bit size
follows because the aggregate coefficients are sums of polynomially many
explicit rational input terms; breakpoint mapping and objective minimization
use a bounded number of operations on those sums. As usual the displayed
operation count assumes `N>=1`; the empty-follower case remains supported.

This specialization is a complete exact algorithm and does not share the
general path-discovery routine's numerical recovery limitation. This is a
correctness and complexity audit, not a new-algorithm novelty claim.

## Correction identified during review

Initially, a user-constructed `Segment` could contain floating-point fields.
For `Q=1`, `c=-1/3`, and `C=0`, a segment storing the floating approximation
`0.3333333333333333` passed a gradient equality after rounded cancellation.
The generated paths already used rational arithmetic, but the public verifier
and optimizer could incorrectly accept an externally supplied approximate
certificate as exact.

The author added exact normalization to `Segment.__post_init__` and rejects
floating-point interval and response fields. Evaluation also converts its
argument through the exact-input conversion function. The review regression
now passes. This was a certificate-interface correction, not a counterexample
to the mathematical corollary.

The main note also initially described increasing the numerical routine's
exhaustive-recovery threshold as a complete algorithm over all rational inputs.
The review exhibited `d=10^500`, which can overflow floating conversion before
that fallback executes. The note now correctly identifies `exhaustive_path`
as the finite exact exponential oracle and treats the midpoint process's
termination argument as conditional on exact recovery. Its per-pattern
operation bound also now includes the `O(N)` work present at zero rank.

## Independent executable checks

The reviewer wrote
[quadratic_review_checks.py](../code/bilevel_reopened/quadratic_review_checks.py)
without calling the author's exhaustive-path oracle or interval-construction
routine for its comparison solutions. Reproduce with:

```
python code/bilevel_reopened/quadratic_review_checks.py
```

The run returned:

```
{
  "aligned_exact_boundary_cases": 5,
  "dense_lp_comparisons": 33,
  "quadratic_dense_face_comparisons": 24,
  "quadratic_hand_cases": 5,
  "random_seed": 260906,
  "status": "passed"
}
```

The independent global comparator enumerates box faces and builds dense KKT
linear programs directly in `(x,z)`, using SciPy's HiGHS LP solver. This
avoids the implementation's low-rank elimination, response formulas, interval
clipping, and objective-endpoint selection. Global objective values agree
within `1e-7`; infeasibility classifications agree in all tested cases.
This numerical comparator is additional evidence, not an exact proof.

The suite also evaluates full dense `Q` KKT conditions in `Fraction`
arithmetic at interval endpoints and interior points. Direct SLSQP follower
solves agree with the certified responses within `3e-6` in infinity norm.
The cases include:

- A disconnected upper-feasible leader set, an isolated feasible clipping
  breakpoint, a prescribed non-breakpoint equality solution, and infeasibility.
- Simultaneous clipping events, persistent zero gradients at bounds, a
  singleton leader domain, and a zero-dimensional follower.
- Indefinite `H` with positive-definite `Q`, redundant aggregate coordinates,
  and aggregate dimension exceeding follower dimension.
- Twenty-four seeded rational random cases of dimensions two through four,
  with dense coupling and two response-dependent upper constraints.
- Incomplete or corrupted certificates, invalid dimensions, nonsymmetric
  `H`, singular or negative `Q`, and floating-point exact inputs.
- Deliberately wrong numerical active-pattern proposals: explicit failure
  with exhaustive recovery disabled, and exact recovery when enabled.
- An exhausted segment limit, which raises rather than returning a partial
  path as a complete certificate.
- Feasible and infeasible upper intervals separated by `10^-60`, checked
  against hand-computed exact responses without a numerical comparator.

For the quadratic extension, a second independent global comparison finds the
endpoints of each dense KKT face with LP, evaluates the upper objective at both
endpoints and their midpoint, and fits the univariate quadratic from those
three values. This checks 24 seeded signed rank-one cases against both the
complete sweep and the general response-path optimizer. Objective values agree
within `1e-7`, and the two exact algorithms also agree on their rational
objective and tie-broken leader choice. The tests include positive, zero,
and negative `h`, nonunit `gamma`, affine upper constraints, and concave or
convex upper pieces.

Five hand-computed cases separately check interior revenue maximization,
interior quadratic minimization, a concave endpoint minimum, exact quadratic
cancellation to an affine objective, and an isolated equality solution.
Five further sweep boundary cases cover simultaneous events, zero and signed
loadings, singleton or empty dimensions, a negative coupling with `10^-60`
SPD margin, and `10^500` input coefficients. The numerical proposal solver is
mocked to raise in those five cases; the sweep succeeds entirely in exact
arithmetic. Full dense KKT, objective values, and upper feasibility are checked
independently at every returned solution.

## Limits on the supported claim

The general response-path routine is a certifying prototype for one leader
coordinate, unit-box followers, a supplied diagonal-plus-low-rank Hessian,
the stated quadratic upper objective class, and affine upper constraints.
It does not implement the full fixed-dimensional hyperplane
arrangement algorithm. Its numerical pattern proposal can fail; exhaustive
recovery is restricted to small follower dimension by default, and response
path generation has an explicit resource cap. Consequently, a successful
run returns an exact globally verified answer, but this implementation is not
a complete polynomial-time algorithm for every input in the corollary.

The aligned rank-one sweep is complete within its narrower assumptions.
Dense positive-definiteness verification for higher-rank indefinite `H`, rational
arithmetic growth, and the number of response segments can affect runtime.
The independent checks support correctness of accepted answers. They do not
prove a favorable runtime bound or justify extrapolation from small synthetic
instances to arbitrary large systems.
