# Exact sparse network–simplex separator

`separator.py` implements the graph-to-cut pipeline in the
[cycle/theta theorem](../../results/network-simplex-cycle-theta-hull.md) and
[parallel-path extension](../../results/network-simplex-parallel-path-hull.md).
The separator uses only the Python standard library and exact `Fraction`
arithmetic. SciPy is needed only for the independent LP comparisons in the tests.

For a serial chain of two-arc gadgets with one outer bypass and unit flow/capacity
data, the separate [fixed-state flat-chain oracle](FLAT_CHAIN.md) covers a larger
graph class when the number of simplex states is small.

The model is

\[
\operatorname{conv}\{(x,y,z):Ax=b,\ 0\le x\le u,\ y\ge0,
\ \sum_j y_j\le1,\ z_{ej}=x_e y_j\ ((e,j)\in O)\}.
\]

Here incidence means **incoming minus outgoing**. Node indices index the balance
vector, edge indices index the arc list, and explicit simplex states start at
zero. The residual simplex vertex has index `simplex_size`.

## Example

Run from the repository root with `PYTHONPATH=code`:

```python
from fractions import Fraction as F
from network_simplex import NetworkSimplex, Point

model = NetworkSimplex(
    arcs=[(0, 1, 1)] * 3,
    balances=[-1, 1],
    simplex_size=2,
    observations=[(e, j) for e in (0, 1) for j in (0, 1)],
)
point = Point(
    x=[F(1, 3)] * 3,
    y=[F(1, 3)] * 2,
    z={o: 0 for o in model.observations},
)
result = model.separate(point)
assert not result.feasible
assert result.cut.evaluate(point) == F(1, 3)
print(result.cut.coefficients, result.cut.constant)
```

The returned inequality is always
`constant + sum(coefficients[key] * original_variable[key]) <= 0`.
Variable keys have forms `("x", edge)`, `("y", state)`, and
`("z", edge, state)`. Fractions are not scaled to primitive integer coefficients.
`Cut.reason` identifies the violated family. Every rejected point has a strictly
positive exact cut evaluation.

For an accepted point, `result.decomposition.weights` contains the original
simplex weights followed by the residual weight. Calling
`result.decomposition.flow(j)` materializes the feasible flow at any state with
positive weight. The object stores one normalized default path vector per block
and exceptions for the positive-weight states observed in that block. This avoids
materializing the full state-by-edge matrix. `separate(point, decompose=False)`
skips construction when membership and a cut are sufficient.

## Implemented scope

- Iterative multigraph block extraction and a spanning-forest balance solve.
  Parallel arcs, arbitrary orientations, loops, bridges, disconnected components,
  and isolated nodes are supported. A loop is an independent scalar block.
- Recognition of every nontrivial block as internally vertex-disjoint paths
  between two terminals. Simple cycles are represented by two paths.
- Reference flows need not satisfy capacities. Exact path-bound intersections
  test base feasibility. Empty base polytopes raise `InfeasibleModel`.
- Sparse observation grouping, repeated observations of a path coordinate,
  merged unobserved states, and zero state weights.
- Complete constant-support separation and suffix-based constructive
  decomposition for two/three-path blocks, and interval separation for loops.
- Exact rational Edmonds–Karp transportation flow for larger blocks. An
  unsaturated maximum flow supplies a subset inequality; active endpoint and
  subset branches produce its valid affine original-coordinate cut.

Unsupported blocks raise `UnsupportedGraph`, rather than returning a hull answer.
In particular, general series–parallel graphs are outside the implemented class.
Additional original-variable constraints can use these cuts as a relaxation, but
intersecting them with this hull does not in general give their exact joint hull.

Integers, fractions, and rational strings are appropriate inputs. Floats are
interpreted through their decimal string, with no feasibility tolerance. A point
from a floating-point LP may therefore violate an exact flow equality before a
nonlinear hull cut is considered. A production floating-point solver adapter
needs its own feasibility and rounding policy; this module does not implement it.

Graph extraction is linear in graph size. Observation and state-label sorting
occur at model construction and take up to `O(|O| log |O|)` comparisons. For
cycle/theta blocks, arithmetic work and compact output scale
linearly with graph size, simplex dimension, and observations. Larger blocks incur the
transportation network size and exact Edmonds–Karp cost. Dense rational Python
operations are a correctness-oriented implementation; no optimized solver-callback
performance is claimed.

## Verification

```sh
PYTHONPATH=code python -m unittest network_simplex.test_separator -v
```

The six tests include 160 full graph-to-hull comparisons against an independently
assembled full disaggregated LP with all original states retained. Accepted
points have their decomposition checked using exact arithmetic against original
balances, bounds, observations, and aggregate flows. Rejected cuts are maximized
over each simplex vertex and the original flow polytope using independent LPs.
The fixed cases check a joint-state theta obstruction, a four-path transportation
min-cut obstruction, original linear constraints, empty/unsupported models,
zero weights, fixed arcs, no observations, and a 1,500-edge chain that rules out
recursive graph-traversal limits. All passed on 2026-09-07. These numerical LP
comparisons supplement the proofs; they do not replace them.

## Attribution

Simplex disaggregation, bounded transportation, and max-flow/min-cut separation
are classical. The implementation follows the repository's graph-coordinate and
sparse-state specialization. A close general comparator is Kis–Horváth,
[*Ideal, non-extended formulations for disjunctive constraints admitting a network
representation*](https://link.springer.com/article/10.1007/s10107-021-01652-z),
Section 5.9, Proposition 22, equations (30)–(31). The earlier full network–simplex
extended formulation is in
[Khademnia–Davarnia](https://arxiv.org/abs/2302.14151), Appendix (25).
This implementation is not a new general polynomial-time separation result.
