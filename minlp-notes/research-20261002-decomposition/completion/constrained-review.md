# Independent review of the constrained solver

The review covers the implementation of the integral TU filtered-grid
algorithm and its certificate checker. It does not claim a general constrained
MINLP algorithm or replace the fixed-width complexity qualification in the
[theorem](../constraints/tu-filtered-grid.md).

## Design review

The proposed finite-grid lower bound is valid when three properties are
checked: the continuous constraint matrix is TU, every continuous grid cell
is aligned with the integral fiber data, and the supplied curvature bound
holds on the actual feasible equality tangent space. Exact finite-state
dynamic programming then gives a feasible grid minimum `v`; subtracting
`n_c L h^2 / 8` gives a lower bound. Filtering must retain the complete
history needed to apply that lower bound to the original domain.

For exact output, a useful finite stopping certificate is rational value
separation. Let `V` be the proved upper bound on the reduced denominator of
the global optimum, let `L_B` be a certified global lower bound, and let a
feasible rational candidate have value `a/b` in lowest terms. If

`a/b - L_B < 1 / (b V)`,

the candidate is globally optimal. Indeed, any distinct rational optimum
with denominator at most `V` differs from `a/b` by at least `1/(b V)`.
This test does not depend on how the candidate was found and does not
require uniqueness or a supplied growth constant.

Enumerating independent active sets of the original inequalities and bounds
is one finite candidate method. A globally optimal point on a face of
smallest possible dimension has positive-definite Hessian on that face's
tangent space. Otherwise a null direction supplies a constant-objective
segment to a smaller face. The resulting KKT saddle matrix is nonsingular.
Thus enumeration of nonsingular systems includes a global optimizer even
when the optimal set is not a singleton. Explicit enumeration caps must be
reported as resource limits, not exactness or infeasibility evidence.

Artificial bounds introduced by filtering must not enter the original-data
denominator calculation. Original constraint rows whose hyperplanes do not
intersect the retained domain can safely be excluded from candidate active
sets. Under uniqueness, rational coordinate reconstruction from sufficiently
narrow retained hulls remains a less expensive exact-output route.

## Implementation review

The hull and union implementations and their independent verifier were read
in full. The integer-fiber model, structural TU checks, projected exact PSD
check, original-polytope height bound, min-marginal filtering, and asymmetric
rational-separation acceptance match the arguments above. The verifier
recomputes the Bellman recurrences and original-domain filtering history;
it does not call the optimizer, its filtering routine, or the tree-DP solver.
Input and rational linear-algebra primitives are shared and are therefore
part of the common trusted code.

The independent suite is
[test_constrained_review.py](../solver/test_constrained_review.py).
It checks correlated equality rounding; exact invariance after adding
`2^30 (x-y)^2` to an objective constrained by `x=y`; integer columns outside
`{0, ±1}` and nonconsecutive labels; an exact nondyadic optimizer recovered
with all face enumeration disabled; a singular ambient Hessian with a fixed
coordinate; branching messages with infeasible separator states; invalid TU,
alignment, curvature, and bag-scope inputs; empty fibers; explicit budget
limits; and forged message, height, and status claims. Forty additional
random rational quadratic equality fibers are checked against direct scalar
minimization, independent of the solver's DP and face enumeration.

The command actually run from `research-20261002-decomposition/solver` was:

```sh
python -m unittest test_constrained_review -v
```

No soundness defect was found. An inaccurate comment about canonicalized
integer bounds was reported and corrected by the implementation author.

The union extension preserves component membership when testing adjacent
cells. Its verifier independently traverses each previously retained
component, so a gap cannot silently become a feasible interpolation cell.
The additional regression has two disconnected optima,
`(0,1/3,1/3)` and `(1,1/3,1/3)`. With face enumeration disabled, union
filtration plus stationary recovery returns an exact checked result under
a 128-state table cap; the hull representation reaches that cap. Replacing
a certified union with its hull is rejected by the verifier.
Fixed-coordinate singleton components are also exercised. The initially
quadratic component search was replaced by independently implemented linear
component traversals in the optimizer and verifier, and the updated paths
passed the suite.

The stationary-face LP candidate method was also reviewed against the
[general-polytope recovery lemma](../../research-20261002/new-direction/proximal-polytope-recovery.md).
Its common coefficient scaling, original row system, native-label hulls,
slack threshold, fixed-label equations, and nullspace stationarity equations
match that lemma. A separate check recovers an exact member of the optimal
continuum `x+y=1/3` from a feasible nonoptimal point close to it. This is a
candidate-recovery test; no favorable grid count is claimed for a continuum.

The final independent suite has **10 passing tests**, including the 40
scalar comparisons. The coordinate-reconstruction test disables both
stationary LP recovery and active-face enumeration. The most recent run of
the command above passed in 0.378 seconds. An earlier invocation from the
repository root could not import this local test module; rerunning from the
documented solver directory succeeded.

The implementation uses an exact simplex LP backend with an explicit pivot
cap. Its certificates remain valid, but its pivot complexity is not the
polynomial-time LP bound used by the mathematical theorem. Table, stage,
face, pivot, and time limits can prevent exact output. The upper-curvature,
capacity, and XP-width qualifications remain in force.

No project-wide checks or CI inspection are part of this review.
