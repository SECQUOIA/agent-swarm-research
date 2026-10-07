# Reusable certified solver for TU-constrained quadratic problems

The implementation now covers general supplied tree decompositions, exact
feasible filtering, independently replayed original-domain certificates, and
exact rational quadratic output. It replaces the earlier two-bag diagnostic
as the reusable implementation of the
[constrained theorem](../constraints/tu-filtered-grid.md). The optional union
filter and stationary-face recovery also implement the new
[nonunique-optimum extension](theory/nonunique-tu-exact.md).

## Files and input contract

- [constrained_grid.py](../solver/constrained_grid.py): `ConstrainedQP`, TU
  verification, curvature checking, feasible grids, filtering and exact output.
- [verify_constrained.py](../solver/verify_constrained.py): separate Bellman
  and pruning-history replay; it never invokes the solver or its DP routine.
- [finite_dp.py](../solver/finite_dp.py): shared two-pass finite-tree DP,
  including branching trees, empty separators and infeasible assignments.
- [rational_optimization.py](../solver/rational_optimization.py): shared exact
  PSD, linear-system and LP operations used by candidate recovery.

The objective is `constant + b'x + x'Hx/2`, with symmetric rational `H`.
The continuous bounds are integral. Native discrete coordinates have explicit
nonempty finite sets of distinct integer labels; the labels need not be
consecutive. Each constraint is an integral row with an integral right side
and sense `<=` or `==`. Its entire scope, including native labels, must occur
in a decomposition bag. Quadratic interaction scopes must also be covered,
and the input model validates the tree and running-intersection property.

Only the continuous-column constraint matrix must be TU. Integer columns can
have arbitrary integral coefficients. The implementation checks one of three
explicit certificates:

1. `{"kind": "network"}`: after optional supplied row sign changes, each
   continuous column has at most two nonzeros, and two nonzeros have opposite
   signs. This is the directed node-arc incidence sufficient condition, with
   rows possibly omitted.
2. `{"kind": "consecutive_ones", "row_order": [...]}`: after optional row
   sign changes, each nonempty column has a constant sign and a contiguous
   nonzero block in the supplied row ordering. Column sign changes then give
   the consecutive-ones criterion.
3. `{"kind": "all_minors"}`: enumerate every square minor within an explicit
   checker budget, and verify that every determinant is `0`, `1`, or `-1`.

Every option first checks entries in `{-1,0,1}`. A model is never accepted
merely because its matrix is described as TU. The bounded fallback is exact
but exponential; no general polynomial-time TU-recognition implementation is
claimed. Equalities are stored once; adding the opposite inequality preserves
TU in the feasible-rounding proof.

For a quadratic, curvature is checked exactly. The default `L` is the maximum
absolute row sum of the continuous Hessian. A supplied
`{"L": ..., "mode": "full"}` must satisfy `L I-H_cc` PSD. Mode
`"equalities"` checks PSD after restriction to the nullspace of the actual
continuous equality rows. This avoids charging positive curvature in
directions that feasible rounding cannot move. `L=0` is allowed when this
check succeeds; the initial feasible integer mesh then solves the problem
exactly. A diagonal-only curvature bound is not accepted for coupled fibers.

Arbitrary rational right sides or unaligned continuous bounds are rejected.
The implementation does not silently rescale them and assume TU survived.

## Solver and certificate behavior

At level `j` the common continuous spacing is `h=2^-j`. The solver enumerates
only feasible bag states, computes the grid minimum and every min-marginal,
and subtracts the verified feasible-rounding error
`E=n_c L h^2/8`. It keeps exactly the continuous cells and native labels whose
min-marginals can still attain the feasible incumbent. The default stores
the hull of surviving cells. `retain_unions=True` instead stores their union,
merges only touching components, and retains passing singleton nodes. Neither
the next grid nor the checker reconnects a removed gap.

Every completed stage saves its mesh, all directed DP messages, min-marginals,
attaining feasible point, retained domains and bound. The verifier checks
the Bellman equations and every filtering transition from the **original**
domain. A final restricted-domain computation alone is not accepted as a
global certificate. Impossible separator states are represented by `None`;
finite sums and infeasibility counts avoid subtraction of infinities.

`solve` returns one of `epsilon`, `exact`, `infeasible`, or `limit`.
Infeasibility is certified from the empty initial feasible TU grid.
Cooperative time, per-stage state, stage-count, LP-pivot and optional
active-face limits are explicit. A limited run can return valid bounds from
its completed stages. If no stage finished, its bounds are `None`. A limit
never becomes an infeasibility or exactness conclusion. The checker has its
own per-stage, total-state and TU-minor budgets.

## Exact rational output

The exact certificate uses a rational value-separation argument on the
original polytope. Write the input objective as
`F=(x'Qx+c'x+e)/D` with integral coefficients. For `n_c>0`, set

```
M = max(1, max |2 Q_cc|)
R = (2 n_c M)^(2 n_c)
V = D R^2.
```

Use `R=1` when there are no continuous coordinates. A minimum-dimensional
optimal face has a positive-definite tangent Hessian. Its nonsingular
original-face KKT matrix has dimension at most `2 n_c` and integral entries
bounded by `M`. Cramer's rule therefore gives an optimal point with a common
denominator at most `R`, and the optimum value has reduced denominator at
most `V`. Integer labels and right sides affect numerators only. Artificial
filtered endpoints do not enter this height argument.

For any exactly feasible candidate with value `f`, let `d_f` be its reduced
denominator. Once a replayed original-domain bound `LB` satisfies

```
0 <= f - LB < 1 / (d_f V),
```

the candidate is globally optimal: two distinct rationals with denominators
`d_f` and at most `V` cannot be that close. The checker recomputes the height,
feasibility, objective and strict inequality. It does not trust the candidate
generator or a growth estimate.

Candidate discovery uses three paths:

- Continued-fraction reconstruction from a retained interval. This eventually
  finds a unique rational optimizer when the intervals contract sufficiently.
- Stationary-face recovery through the shared exact LP. It selects nearly
  active **original** rows at the current grid point using the explicit slack
  threshold in the [general-polytope recovery lemma](../../research-20261002/new-direction/proximal-polytope-recovery.md).
  It fixes the actual native labels, imposes the selected face, and requires
  the gradient to be orthogonal to that face's tangent space. A nullspace
  basis eliminates unrestricted multipliers. This works even with a singular
  Hessian or a continuum of minimizers. Premature recovery or an LP limit
  cannot cause false acceptance because value separation is still required.
- Optional bounded enumeration of original active-face KKT systems,
  controlled by `max_exact_faces`. Its default is zero; it is an optional
  candidate search, not the exactness proof or the general recovery method.

The stationary LP is solved once per selected-face/label pattern. Its
coefficients come from original data, not high-denominator grid coordinates.
Without resource limits, qualitative quadratic set growth and the recovery
lemma imply eventual exact output even when minimizers are nonunique. Grid
sizes can nevertheless grow rapidly around an optimal continuum. When each
optimal coordinate projection is finite, union filtering gives the bounded
per-level state counts proved in the new theorem. These are XP-width bounds,
not width-FPT bounds. Initial integral capacities remain pseudopolynomial.
The exact simplex implementation is finite and certified; it does not claim
the polynomial worst-case running time of the theorem's abstract LP oracle.

## Example

Run from the `solver` directory:

```python
from fractions import Fraction as F
from constrained_grid import ConstrainedQP, solve
from verify_constrained import verify

p = ConstrainedQP(
    H=[[2, 0], [0, 2]], b=[F(-2, 3), F(-4, 3)],
    bounds=[(0, 1), (0, 1)], labels={},
    rows=[[1, 1]], rhs=[1], senses=["=="],
    bags=[(0, 1)], edges=[], tu_certificate={"kind": "network"},
    constant=F(5, 9),
)
certificate = solve(p, exact=True, retain_unions=True)
assert certificate["point"] == ["1/3", "2/3"]
assert verify(certificate)["upper"] == "0"
```

`ConstrainedQP.to_dict()` and `ConstrainedQP.from_dict()` provide the JSON
model representation. The solver result itself is JSON serializable.

## Targeted verification and scope

The author ran:

```
python -m unittest -v test_constrained_grid.py test_constrained_review.py
```

All 24 tests passed: 14 author tests and 10 independent review tests. Targeted
`py_compile` also passed for the four constrained solver/test modules; all
nine local links in this document resolved, and owned-file whitespace checks
passed.

The suite covers exact non-dyadic answers, coordinate-only reconstruction,
stationary LP recovery, branching resource/equality trees, native nonconsecutive
labels, arbitrary integral label-column coefficients, equality-tangent
curvature, infeasible fibers, structural TU certificates, invalid TU matrices,
unaligned data, missing history, tampered bounds/cells/heights, union gaps,
fixed coordinates and honest resource-limit results. The independent suite
also checks 40 random equality fibers against a separate exact scalar formula.
Final counts and review conclusions are recorded in the
[independent review](constrained-review.md).

On the two-optimum fixture
`x0(1-x0)+(x1-1/3)^2+(x2-1/3)^2`, subject to `x1=x2` on the unit box,
union filtering with stationary LP recovery returns an exact optimizer after
43 levels and 2,248 total bag states. The hull mode reaches a 20,000-state
per-stage cap after 15 completed levels. Both histories replay. This is a
targeted illustration of the theorem's domain representation; it is not a
general performance claim. Frozen comparison runs are maintained separately
in the [completion benchmarks](benchmarks/).

This implementation accepts quadratic objectives. The fixed-degree polynomial
constrained theorem and general rational-grid alignment remain theoretical
extensions; they are not silently claimed as supported input formats. No
project-wide checks or CI status/log inspection were performed.
