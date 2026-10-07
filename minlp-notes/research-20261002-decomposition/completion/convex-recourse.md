# Changing-active-set convex recourse is implemented

The [solver](../solver/convex_recourse.py) now accepts an arbitrary rational
`BoxQP` and supplied disjoint continuous private blocks with PSD Hessians.
Each block can have a singular Hessian, tied conditional minimizers, fixed
private coordinates, and any number of retained attachment coordinates.
Native integer variables can remain in the global search. Distinct private
blocks must have no direct interaction. Invalid partitions are rejected.

The original quadratic and the complete partition determine every local
oracle problem. The solver does not require a globally affine response or an
explicit piecewise representation. It solves conditional convex box QPs
only at attachment grid points and caches their exact values and KKT
witnesses. A scope-preserving min-fill heuristic supplies the retained tree
decomposition unless the caller supplies one. Width after elimination is
the relevant width; the original decomposition does not imply that width.

```python
from fractions import Fraction
from certified_grid import BoxQP
from convex_recourse import solve_convex_recourse, verify_convex_recourse

problem = BoxQP(
    [[6, -4], [-4, 2]], [-3, 1], [(0, 1), (0, 1)], [],
    [(0, 1)], [], name="clipped_response",
)
certificate = solve_convex_recourse(
    problem, blocks=[[1]], epsilon=Fraction(1, 1000),
    max_levels=64, max_table_states=100000, time_limit=30,
)
assert verify_convex_recourse(certificate, problem)
```

The conditional response in this example is `y=0`, `y=2z-1/2`, and `y=1`
on three successive intervals. The local oracle therefore crosses both
active-set transitions during a normal solve.

The global search uses the geometric coordinate grid and incident-node
curvature corrections from the filtered-grid theorem. For each private
block its value function is an infimum of affine functions of the retained
parameters, hence is concave. Consequently the original direct retained
diagonal `A[i][i]` is an upper bound on that coordinate's curvature in the
partially minimized objective. A node's correction is
`max(0,L[i]) * ell**2 / 8`, where `ell` is its largest adjacent interval and
`L[i]` initially equals the direct diagonal; integer unit intervals have zero
correction. Coordinates with nonpositive certified curvature need only their
current endpoints. Fixed coordinates have one state.

For a block with just one attachment coordinate, the optional scalar
constructor can improve `L[i]` across active-set changes. It constructs a
complete exact interval partition, certifies the affine response and KKT
identities on each interval, and computes the maximum second derivative of
the private conditional value. This maximum is nonpositive and is added to
the original retained diagonal before clamping at zero. Multiple certified
scalar blocks add their bounds. The solver independently binds each
partition to the original coefficients; the checker verifies coverage and
all identities before using the sharper correction. Private blocks with
multiple attachments continue to use the direct curvature bound.

The constructor requires a positive definite private Hessian and nonfixed
private/attachment intervals; unsupported cases keep the original bound.
It enumerates active patterns and is capped by `max_scalar_patterns=81`
(at most four private coordinates). `scalar_curvature=False` disables
this preprocessing. This is a checked cancellation of large positive
retained curvature in suitable changing-active-set examples, not a general
negative-curvature theorem. The
[piecewise-curvature theorem](theory/piecewise-recourse/piecewise-curvature.md)
gives the proof and exact constructor scope.

The shared finite-tree DP computes the corrected minimum, a traceback, and
every coordinate min-marginal. A cell is removed only when both endpoint
marginals exceed the feasible incumbent. The retained hull preserves every
global optimizer. Native integer coordinates use the same hull rule;
omitting their intermediate grid states is interpolation, not a claim that
those integer labels are infeasible. The complete history carries each
lower bound back to the original domain.

The default schedule starts with `theta=2^-2` and capped geometric trials.
Each trial refines `h=s*2^-j`, uses the coordinate cap
`100*theta^-1*ceil(log2(n+2))`, and restarts on the original box if the cap or
accuracy-stage limit is exhausted. Larger trials reduce `theta`. This is
the unknown-conditioning schedule of the oracle theorem, applied to the
retained variables. `grid_mode="uniform"` provides a zero-slope ablation.
The implementation's local convex oracle uses bounded active-face search
and rational LP; that implementation is not a polynomial-time convex-QP
oracle. Therefore the theoretical parameterized bit complexity is not a
running-time guarantee for this Python implementation.

`exact=True` adds original-QP rational-height recovery. The shared recovery
code proposes feasible rational points from the incumbent, coordinate
reconstruction, and an active-face stationarity system. None of these
proposals proves optimality. If the original optimum has denominator at
most `Q` and a feasible candidate value `v` has denominator `d`, distinct
values differ by at least `1/(Q*d)`. The solver accepts exactness only when
its independently certified lower bound `L` satisfies `v-L < 1/(Q*d)`.
The height bound comes from the original rational quadratic, not its
nonsmooth partially minimized value function. In exact mode the internal
accuracy target keeps decreasing; resource caps can still stop before an
exact certificate is found. A zero approximate tolerance also refines the
target, but `exact=True` is the intended finite rational-output interface.

Every result is JSON serializable and contains the original model, block
partition, residual decomposition, exact oracle witnesses, full completed
grid history, feasible original point, and original-objective bounds.
`verify_convex_recourse(certificate, problem)` binds the proof to the
expected original input. It verifies PSD and KKT, reconstructs all local
factors, reruns the exact finite-tree calculations, and replays every
pruning step. It does not call a QP or LP optimizer. The checker also
recomputes rational heights for an exact-separation certificate.

`level_limit`, `table_limit`, `time_limit`, and `oracle_limit` preserve the
last valid original-model bound. An interruption before the first complete
grid retains the independent-factor interval bound and a feasible point.
`max_faces` and `max_pivots` are per local convex-QP query; the table cap is
per complete global stage. Time limits are cooperative, so one rational
arithmetic operation can cross the deadline. `max_levels` caps attempts,
including failed coordinate-capped trials.

The targeted command is:

```sh
cd research-20261002-decomposition/solver
python3 -B -m unittest test_convex_recourse -v
```

It passed nine tests covering clipped responses, singular and fixed
private blocks, exact interior recovery, native integers, multiple scopes,
supplied-decomposition rejection, four resource-limit exits, JSON replay
with the optimizers disabled, corrupted proofs, and active-set curvature
cancellation with stiffness parameters 1 and 100. Independent review and
additional analytic comparisons are recorded in
[the review](convex-recourse-review/review.md).
Its reproducible harness passed 48 comparisons against independent exact
minima, rejected 138 corrupted proofs, and completed 21 replays with
optimization disabled. It also checked eight resource cases. For three
changing-active-set instances with stiffness 1, 100, and `10^6`, the certified
curvature remained six; each took eight levels and nine local value queries
to reach the same certified gap `27/1048576`. These are controlled correctness
and mechanism checks, not evidence of broad solver superiority.

This closes the changing-active-set *box* recourse implementation gap.
General private polytope constraints and an implementation with a
polynomial-time exact convex-QP oracle remain outside this backend. The
general negative-curvature complexity question remains open: the direct
retained diagonal can still be large after eliminating a convex block.
