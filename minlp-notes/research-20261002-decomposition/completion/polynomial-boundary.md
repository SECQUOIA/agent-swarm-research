# Automatic exact polynomial boundary output

[`polynomial_boundary.py`](../solver/polynomial_boundary.py) now discovers a
certified boundary face and returns an exact implicit global optimizer for
the supported class. It uses the actual explicit-polynomial grid solver;
the user supplies no optimizer, face, growth constant, or active-gradient
margin.

The output is either an explicit rational global optimizer or a rational
box on a selected face together with the original polynomial objective.
In the latter case a finite certificate proves that the restricted
objective is uniformly strongly convex and that its unique minimizer is a
global optimizer of the original problem. The coordinates and value of
that minimizer may be irrational. An implicit patch is not presented as
an explicit rational point or value.

## Implemented search and proof

`discover_boundary` runs the certified polynomial grid solver with target
gaps `1, 1/4, 1/16, ...`, subject to time, state, stage, and round limits.
After each run it performs these exact checks:

1. Independently replay the complete global grid/pruning certificate. Its
   retained box contains every original global optimizer. A certified
   zero global gap already gives an explicit rational optimizer.
2. Require singleton native-integer coordinates for a continuous patch.
   The polynomial solver now includes individual integer-label filtering,
   so neighboring unit intervals do not prevent this step indefinitely.
3. Repeatedly scan unfixed continuous coordinates. If a verified derivative
   interval is nonnegative and the original lower bound is still present,
   substitute that bound; use the analogous rule for a nonpositive
   derivative and original upper bound. Recompute signs after every
   substitution and rescan until no reduction succeeds.
4. For the remaining coordinates, evaluate the midpoint Hessian and an
   exact interval enclosure of every Hessian entry on the selected face.
   Bound the maximum absolute row sum of the difference by `delta`. Exact
   rational positive-definiteness of `H(midpoint) − delta I` proves a
   uniformly positive-definite Hessian throughout the face box.

Each monotone substitution preserves the minimum value and at least one
optimizer. A **weak** sign can remove other optimal points. The certificate
therefore constructs one original global optimizer; it does not certify
uniqueness in the original domain or describe its full optimal set.
If every coordinate is fixed, the result is an explicit rational point.

The remaining strongly convex box problem is an exact, finite descriptor:
its box KKT conditions have one primal solution, even if that solution is
algebraic. There is no numerical optimizer or tolerance assumption inside
the acceptance test.

The interval row-sum argument is elementary. For each point of the face,
the symmetric Hessian perturbation has spectral norm at most its maximum
absolute row sum, which is bounded by `delta`. Therefore its Hessian is
bounded below by the verified positive-definite matrix. Compactness gives
existence; strong convexity gives uniqueness. Global containment followed
by minimum-preserving reductions gives original global optimality.

## Independent certificate replay

[`verify_polynomial_boundary.py`](../solver/verify_polynomial_boundary.py)
replays the underlying grid certificate and every subsequent reduction.
It recomputes derivative intervals and midpoint Hessian entries through
the grid verifier's independent monomial interval evaluator, rather than
calling the discovery model's derivative/Hessian methods. It recomputes
the uniform perturbation bound and performs its own exact matrix
elimination. It does not run boundary discovery or optimize the patch.

```python
from polynomial_boundary import discover_boundary
from verify_polynomial_boundary import verify_certificate

result = discover_boundary(problem, time_limit=30, max_rounds=16)
if result["status"] == "certified":
    exact_descriptor = verify_certificate(result["certificate"], problem)
```

JSON artifacts bind the original polynomial model and complete global
trace. Passing `problem` to the verifier also binds replay to the caller's
model. Malformed artifacts and altered signs, Hessians, face bounds, or
grid traces are rejected. Verification and discovery accept cooperative
time-budget checks. Individual rational arithmetic operations are not
preempted.

## Results and limits

The implementation discovers a genuinely irrational optimizer for
`(x²−1/2)² + y + xy²` on the unit square. Four accuracy rounds produce a
verified face `y=0` and a strongly convex interval containing
`x=1/sqrt(2)`. No algebraic optimizer was supplied to search.

For `(x−1/4)² + y−y²` with `0≤y≤1/2`, the full Hessian has the negative
entry `−2`. A weak derivative bound `[0,1]` nevertheless certifies `y=0`
and leaves a strongly convex one-dimensional problem. Sequential
reductions also handle `y²+z(1−y)`: fixing `z=0` makes the previously
ambiguous derivative in `y` nonnegative. Some zero-margin active
coordinates are therefore handled, without claiming the general
growth-only boundary theorem.

The mathematical strict-complementarity result remains
[boundary-active-face.md](../degeneracy/boundary-active-face.md). This
Python implementation uses a bounded restart search rather than that
theorem's bit-step dovetail. It makes no implementation-level FPT
running-time claim. Its sufficient interval tests can remain inconclusive;
the symmetric quartic with two separated interior minima is an explicit
tested example. Resource or test failure returns `inconclusive`, never an
unproved global optimizer. Arbitrary weakly complementary boundary optima
remain outside the termination guarantee of the theorem.

Targeted command run:

```sh
python3 -m unittest discover -s research-20261002-decomposition/solver -p test_polynomial_boundary.py -v
```

All **10 tests passed**. Coverage includes the actual irrational search,
negative full Hessian, sequential and upper-bound reductions, native
integer filtering, flat original optimal sets, exact-grid output, resource
limits, and certificate corruption. The independent
[review](reviews/polynomial-boundary-review.md) and its
[reproducible checks](reviews/check_polynomial_boundary_review.py) report
no unresolved soundness finding. No project-wide verification or CI
inspection was performed.
