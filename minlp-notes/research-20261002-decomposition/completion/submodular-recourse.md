# Implemented mixed concave/convex submodular recourse

The mixed recourse theorem now has a general exact implementation for its
stated box-QP class. It constructs its own greedy-base mixture certificate;
it does not enumerate all endpoint labels as its optimization method. The
original small diagnostic remains an independent reference check.

The implementation is an exact finite cutting-plane method. Its worst-case
cut count is factorial, and its convex-QP backend has an exponential active-face
fallback. It does **not** implement the polynomial-time oracle-LP algorithm
used in the [theorem](../conditional-messages/mixed-submodular-recourse.md).

## Supported models and output

[The solver](../solver/submodular_recourse.py) accepts the common `BoxQP` model
with objective `constant + b'x + x'Ax/2`, finite rational boxes, and any valid
supplied tree decomposition. Its optimization method does not use that
width. Decompositions are retained for compatibility and model binding.

After excluding fixed coordinates, it recognizes a partition into endpoint
coordinates `D` and continuous coordinates `C`. It checks:

- Every diagonal in `D` is nonpositive.
- The `C` principal Hessian is positive semidefinite, including singular cases.
- Signs in `{−1,1}` make every active off-diagonal coefficient nonpositive.
- Native integer coordinates belong to `D`; their effective integer box
  endpoints are used without enumerating intermediate integers.

Automatic partitioning puts all nonpositive diagonal entries in `D`. A caller
can supply `D` in any order. Sign propagation recognizes a consistent signed
graph; callers can alternatively supply the signs. Fixed coordinates may have
any diagonal or integrality and are substituted in every conditional problem.
Additional coupled constraints and integer coordinates in `C` are outside
this backend's contract.

A successful result contains a rational global optimizer, its value, and a
JSON certificate. A positive requested tolerance may stop earlier with a
certified gap. With `exact=True`, a positive tolerance does not permit an
approximate success status. Unsupported classes and resource limits retain
an independently checkable global interval and feasible incumbent.

## Algorithm and finite termination

For a subset `S` of `D`, the exact conditional query fixes oriented endpoints
and minimizes over `C` with the shared rational convex-box-QP backend. The
solver caches its rational completion and value `g(S)`. Product-box
submodularity and exact partial minimization make `g` submodular.

A permutation `pi` produces a greedy vector `b^pi` from its successive prefix
values. The solver begins with one permutation, then solves the finite LP

```
minimize t
subject to t >= g(empty) + b^pi y       for every stored permutation pi
           0 <= y <= 1.
```

Sorting the current `y` in decreasing order identifies a maximally violated
greedy-base inequality. Every violated inequality is new. There are at most
`|D|!` permutations, so without exhausted caps the method terminates after
finitely many master LPs and exact queries. This is a finite bound, not a
useful polynomial complexity guarantee.

The master LP's nonnegative cut multipliers sum to one. Their weighted greedy
vector `w` proves

```
g(S) >= g(empty) + sum(min(0, w_i))       for every endpoint label S.
```

Every computed prefix supplies a feasible upper bound. If separation finds no
violation, the Lovasz extension is minimized globally. Its value is a convex
combination of those prefix values, so a queried prefix attains the same bound.
The code also stops as soon as an already constructed mixture and an incumbent
prove the requested gap. No numerical tolerance enters any acceptance test.
The shared QP backend may use floating-point proposals for active faces, but
accepts them only after rational PSD and KKT checks.

## Independent replay and resource limits

[The verifier](../solver/verify_submodular_recourse.py) checks the embedded
model, the expected model when supplied, the partition, the edge signs, and
positive semidefiniteness. For each recorded query it checks the oriented
endpoint label, box and integer feasibility, exact value, and the continuous
box KKT signs. It reconstructs every greedy increment from checked chain
values, validates the mixture, and recomputes the lower bound. It also verifies
the final feasible point and gap. It invokes no LP, QP, search, or submodular
optimizer. Tests explicitly disable optimization functions during replay.

Before a whole greedy chain or any query completes, an independent sum of
factorwise minima supplies a valid coarse lower bound. Interrupted searches
retain the strongest completed mixture and all completed conditional
witnesses. Query attempts, cuts, master calls, QP faces, and simplex pivots are
reported separately. In particular, the attempted-query counter may exceed
the number of completed witnesses after a cap or interruption.

The API exposes:

- `max_cuts`: number of greedy inequalities stored.
- `max_queries`: uncached convex-QP calls, including interrupted calls.
- `max_faces`: active faces per conditional QP.
- `max_pivots`: cumulative simplex pivots over master LPs and conditional QPs.
- `time_limit` and `check`: cooperative deadlines and an external budget hook.

A zero cap is valid. Time checks do not preempt an individual rational
arithmetic operation. Native external process limits remain appropriate for
hard time and memory caps. A `BudgetExceeded` exception from the common budget
hook produces a valid limited result; unrelated external exceptions propagate.
A resource limit is never an infeasibility or nonconvexity conclusion.

The result embeds all completed cached query witnesses. Certificate storage
therefore follows the query cap; this implementation does not claim the
polynomial certificate-size bound of the oracle-LP existence theorem.

## Usage and integration

Run from the solver directory, or put it on `PYTHONPATH`:

```python
from submodular_recourse import solve_submodular
from verify_submodular_recourse import verify_submodular

result = solve_submodular(problem, exact=True, max_cuts=100,
                          max_queries=10000, max_faces=10000,
                          max_pivots=10000, time_limit=10)
assert verify_submodular(result, problem)
```

The [recourse pipeline](../solver/recourse.py) exposes `backend="submodular"`
and uses this backend automatically for supported remaining mixed models.
The outer certificate binds every preprocessing transformation, the inner
proof, and the lifted original-model point. See the
[pipeline completion note](recourse.md) for discovery and fallback details.

## Targeted verification completed

The command actually run was:

```
python3 -B -m unittest discover -s research-20261002-decomposition/solver -p test_submodular_recourse.py -v
```

All **11 tests passed**. They cover the nontrivial equal-weight mixture fixture,
signed coupled convex blocks, a singular convex block, fixed positive-diagonal
integer coordinates, effective integer endpoints, arbitrary rational boxes,
permuted endpoint indices, empty `D` or `C`, all-fixed models, and 18 independent
full-face comparisons. They also check eight resource-cap settings, an
interruption after successful queries, exact-versus-approximate status,
unsupported classes, malformed options, JSON replay, model binding, and
certificate corruption.

The two-endpoint mixture fixture has four conditional values
`0, 13/16, 13/16, 0`. A single greedy base gives the strictly weaker lower bound
`−13/16`. The implementation queries four labels, constructs two cuts, obtains
weights `1/2,1/2`, and certifies exact optimum zero.

An [independent review](reviews/submodular-recourse-review.md) found no
correctness issue. In addition to reading the proof and code, the reviewer
checked 180 independent exact random comparisons: 120 signed scalar-convex
models and 60 signed models with a singular coupled convex block. The reviewer
also checked capped/interrupted runs and malformed proofs. Those exploratory
checks are recorded in the review; the reproducible regression suite is the
command above. No project-wide checks or CI inspection were performed.

This completes the finite exact backend for the stated mixed recourse class.
Replacing its exponential worst-case components with a practical polynomial
oracle-SFM implementation would be a separate performance project. Neither
this implementation nor its tests resolve unrestricted submodular box QP or
general treewidth-only conditional recourse.
