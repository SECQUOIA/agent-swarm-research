# Interface guide

Run Python from the supplement root with `PYTHONPATH=code`. Explicit labels in
code are `0,...,m-1` and the residual state is `m`, whereas the paper labels its
residual state `0`. Incidence in the production models means incoming minus
outgoing. Arc indices distinguish parallel arcs. Floats passed to exact APIs
denote their decimal text; use integers, rational strings, or `Fraction` values
for intended exact inputs.

## Parallel-path blocks

```python
from fractions import Fraction as F
from network_simplex import NetworkSimplex, Point

model = NetworkSimplex(
    arcs=[(0, 1, 1)] * 3,
    balances=[-1, 1],
    simplex_size=2,
    observations=[(e, j) for e in (0, 1) for j in (0, 1)],
)
point = Point(x=[F(1, 3)] * 3, y=[F(1, 3)] * 2,
              z={o: 0 for o in model.observations})
answer = model.separate(point)
assert not answer.feasible
assert answer.cut.evaluate(point) == F(1, 3)
```

Each arc is `(tail, head, capacity)`. Supported blocks are internally disjoint
parallel paths, including cycles and theta graphs. Arbitrary orientations,
bridges, loops, disconnected components, and isolated nodes are supported.
Unsupported blocks raise `UnsupportedGraph`; an empty base raises
`InfeasibleModel`. General series–parallel graphs need not belong to this class.

A cut means `constant + sum(coefficients[key] * variable[key]) <= 0`, with keys
`("x", edge)`, `("y", label)`, and `("z", edge, label)`. A feasible result includes
`decomposition.weights`, followed by the residual weight. For each positive
weight, `decomposition.flow(j)` materializes a normalized feasible flow. Compact
storage shares defaults across labels absent from a block. Pass
`decompose=False` to request only membership or a cut.

## Flat chains

`from network_simplex.flat_chain import FlatChainSimplex` exposes
`FlatChainSimplex(gadgets, simplex_size, observations)`, using the same point,
cut, and result conventions. Gadget `i` has arcs `2*i` and `2*i+1` from `i` to
`i+1`; the bypass is arc `2*gadgets`. Flow and capacities are one. Observations
may use either pair arc or the bypass. Arbitrary input graph recognition is not
part of this interface.

Unused labels share a default profile. Zero, one, and two observed labels need
no circuit library; three use 16 reduced positive circuits with both flow-balance
repairs. Recovery at three or more observed labels uses finite inverse bases.
Library size grows exponentially with observed-label count. `labels`,
`group_weights`, `group_profile`, and `group_arc_a` retain compact output. Dense
compatibility accessors incur the corresponding output cost.

## General compressed formulation

`from network_simplex_compressed import CompressedNetworkSimplex, separate`
exposes the same arc, balance, simplex-size, and observation inputs.
`eliminate_observed=False` builds the initial formulation;
`eliminate_observed=True` pivots the observed equations. Both store exact
rational equations, inequalities, and bounds and convert them to sparse floating
point matrices for SciPy/HiGHS. An infeasible base is represented by an infeasible
LP, rather than raising the specialized separator's empty-model exception.

`model.optimize(c, y_fixed=...)` minimizes an original-coordinate objective in
the order all x, all y, then sorted observed z. The result adds `original_point`,
`model_stats`, `assembly_seconds`, and `solve_seconds` to SciPy's OptimizeResult.
Construction time is separate. `model.membership(point)` is numerical.
`separate(model, point)` returns `certified_outside` only after exact checks of
nonnegative multipliers, auxiliary cancellation, and positive cut violation.
Other statuses are `numerically_feasible`, `uncertified_outside`, and
`solver_failure`; none is an exact certificate. There is no exact feasible
decomposition in this general interface.

All interfaces describe the original equality-flow component hull. Intersecting
it with additional linking rows gives a valid relaxation but need not give the
hull of the additionally constrained product graph. The bounded-rank routines
in the independent checks are verification prototypes, not a general production
graph oracle.
