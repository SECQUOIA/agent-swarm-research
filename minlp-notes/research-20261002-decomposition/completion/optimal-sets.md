# Implemented optimal-set discovery and certificates

The former diagnostic examples are now reusable algorithms over the same
`BoxQP` model as the sparse solver. Both return JSON certificates, and the
separate verifier reconstructs the claims with exact rational arithmetic.
No optimizer, optimal component, or growth constant is supplied to either
discovery API.

## Endpoint class

[`solve_endpoint_set`](../solver/optimal_sets.py) requires nonpositive
diagonal Hessian entries on every nonfixed coordinate. Continuous and native
integer coordinates are supported. Integer bounds are rounded inward by
`BoxQP`; fixed coordinates can have arbitrary curvature.

The solver runs exact endpoint dynamic programming on the supplied tree
decomposition. The certificate records the upward Bellman messages and
nonnegative bag residuals, their exact minimum, and an attaining point.
The verifier checks every local recurrence and minimum attainment. Endpoint
interpolation then describes **every** optimizer through two conditions:

- A strict negative diagonal forces that coordinate to an endpoint.
- Every positive Bellman residual must have zero independent-rounding
  support at the proposed point.

These are compact factored polynomial equations, implemented directly by
`contains(certificate, point)`. They do not expand or enumerate the optimal
faces. Zero-diagonal free integer coordinates can have arbitrarily many
interior labels; only their endpoints occur in the certificate tables.

Construction has at most two labels per nonfixed coordinate. Exponential
dependence is on supplied bag size, not the numerical integer interval
width or number of optimal components. The proof and precise scope remain
in [the endpoint theorem](../degeneracy/endpoint-optimal-set.md).

## Unknown-growth diagonal-certificate class

`discover_diagonal_set` supports continuous nonfixed coordinates. It
actually runs the finite geometric proximal trials with conditioning
guesses `K=1,2,4,...`. Each trial starts from the original lower endpoints,
uses fresh original-box intersections, and minimizes the corrected
proximal objective by sparse exact DP. The stationary-polytope arithmetic
height determines a finite target stage. Fixed coordinates are substituted
when deriving that height.

At an attempted acceptance, nearby original bounds are selected and the
remaining **original** stationarity equations are solved as rational linear
feasibility. The code then checks original box KKT conditions and positive
semidefiniteness of the maximally shifted Hessian. The test includes
singular matrices and checks nonzero off-diagonals at zero pivots. No
guessed global lower bound is used to accept a candidate.

By default the independent test is attempted after every stage, which can
save work. `early_accept=False` attempts it only at the theorem's full
finite target stage. Both modes retain the same sound acceptance criterion.
The output describes the entire optimal set by the shifted-Hessian kernel
and endpoint products for positive shifts. It can describe tilted,
disconnected continua without listing their components.

The optional `diagonal_certificate(problem, point)` API certifies a supplied
point; automatic discovery never calls it with a supplied optimizer. A
failed test returns `None`. On success its certificate is valid regardless
of the way that candidate was obtained.

The mathematical discovery theorem is
[unknown-growth-diagonal-class.md](../degeneracy/unknown-growth-diagonal-class.md).
The implementation uses the shared exact simplex LP helper. Simplex is
bounded by a configurable pivot limit; this implementation does **not**
inherit the theorem's polynomial-time rational-LP bound. Its actual finite
search and output validation are implemented, but no polynomial-time/FPT
performance claim is made for the Python implementation.

## API, resource limits, and replay

From a Python process with `solver/` on its import path:

```python
from optimal_sets import solve_endpoint_set, discover_diagonal_set
from verify_optimal_sets import verify_certificate, contains

result = discover_diagonal_set(problem, time_limit=30, max_trials=8)
if result["status"] == "certified":
    certificate = result["certificate"]
    exact = verify_certificate(certificate, problem)
    assert contains(certificate, exact["point"], problem)
```

Both functions accept a time limit and a total bag-table-state cap.
Discovery also accepts per-trial stage, trial-count, and LP-pivot limits.
The LP and PSD checks cooperate with the time budget. A single large
rational arithmetic operation is not preempted.

Endpoint budget exhaustion returns `resource_limit`. Discovery exhaustion
returns `inconclusive` with its reason and per-trial counts. Neither status
includes a purported optimal-set certificate. In particular a failed
conditioning trial is not evidence of nonmembership in the diagonal
class. Outside that class the uncapped procedure may never accept.

[`verify_optimal_sets.py`](../solver/verify_optimal_sets.py) uses the input
model but imports no optimization routine, LP solver, or certificate
producer. Passing the original `problem` binds replay to that exact model.
Without it, replay verifies the model serialized in the certificate.
`contains` replays before evaluating the compact equations; it returns
false for infeasible points, including noninteger interior labels on native
integer coordinates. Malformed or invalid certificates raise
`CertificateError`, including floating-point substitutions.

## Targeted verification

Command run:

```sh
python3 -m unittest discover -s research-20261002-decomposition/solver -p test_optimal_sets.py -v
```

All **10 tests passed**. They exercise actual automatic discovery, complete
finite trials, rational LP recovery, singular PSD matrices, fixed and tiny
intervals, permuted branching decompositions, mixed integer membership,
resource limits, and independent certificate corruption rejection.

The nonglobal-KKT trap
`x²+y²−3xy+63(x+y)/128` rejects the complete `K=1,2,4` trials and accepts
the exact optimum `(1,1)` during `K=8`. Thus the test covers an invalid
growth guess that really persists through a full trial, rather than only
an isolated supplied-point certificate check.

An independent review and reproducible additional checks are recorded in
[optimal-sets-review.md](reviews/optimal-sets-review.md). No project-wide
verification or CI inspection was performed.
