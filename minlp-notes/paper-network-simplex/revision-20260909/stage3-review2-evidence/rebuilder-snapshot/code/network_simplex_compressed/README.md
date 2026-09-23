# Sparse extended hulls on arbitrary flow graphs

This implementation constructs the exact rational extended formulation from
[the compressed-hull development](../../notes/network-simplex-reopened-compressed-hull.md).
It accepts an arbitrary bounded directed flow graph, a simplex, and selected
flow–simplex products. SciPy/HiGHS solves the resulting LP numerically. The
formulation is exact; floating point solver answers are not exact certificates.

```python
from types import SimpleNamespace
from fractions import Fraction as F
from network_simplex_compressed import CompressedNetworkSimplex, separate

# Incoming minus outgoing equals balances. Parallel arcs are distinct.
model = CompressedNetworkSimplex(
    arcs=[(0, 1, 2), (0, 1, 3)],
    balances=[-2, 2],
    simplex_size=2,
    observations=[(0, 0)],
    eliminate_observed=True,
)
# Original order: x for each arc, y for each label, sorted observed z.
optimum = model.optimize([0, 0, 0, 0, -1])
point = SimpleNamespace(x=(1, 1), y=(F(1, 2), 0), z={(0, 0): F(1, 2)})
membership = model.membership(point)
certificate = separate(model, point)
```

Run with `PYTHONPATH=code` from the repository root. Dependencies are NumPy and
SciPy. Exact certificate objects reuse `network_simplex.separator.Cut`.

The constructor performs iterative biconnected-block decomposition, obtains a
rational unconstrained reference flow, and computes fundamental-cycle rows.
Rows equal up to sign share one interval bound. This performs the relevant
degree-two path compression without constructing a separate suppressed graph.
Self-loops are rank-one blocks. Bridges, disconnected graphs, isolated vertices,
parallel edges, zero capacities, and infeasible base models are handled.
Infeasible base models produce infeasible LPs rather than constructor errors;
invalid input indices raise `ValueError`.

For a block of rank `r` with `a` observed labels, the initial formulation uses
`r*a` auxiliary coordinates. Labels with no observations in that block share
one residual state, whose coordinates are eliminated through the aggregate x.
Passing `eliminate_observed=True` additionally pivots the observed equations
using exact fractions. A label with observed-row rank `d` then uses only `r-d`
auxiliary variables. This is the cycle rank of its unobserved-edge subgraph.
In particular, observing an edge set that intersects every undirected cycle
removes every auxiliary variable for that label. This is a dimension count for
this construction, not a lower bound on every possible extended formulation.
The option defaults to `False` to retain the uneliminated experimental baseline.

`model.eq` and `model.ub` retain pairs `(coefficient_dict, right_hand_side)`
with exact `Fraction` coefficients. `model.bounds` is rational too.
`model.matrices()` performs the floating point CSR conversion.
`model.optimize(c, y_fixed=...)` minimizes a linear objective and returns the
SciPy `OptimizeResult`, augmented with `original_point`, `model_stats`,
`assembly_seconds`, and `solve_seconds`. Construction must be timed separately;
`assembly_seconds` covers conversion of the retained model for that solve.
`model_stats.rows` counts matrix rows, excluding variable bounds.
`model_stats.matrix_bytes` counts CSR arrays, excluding Python rational objects,
solver memory, objectives, bounds, and right-hand sides. These statistics must
not be reported as complete process memory. The row-count theorem does not
bound sparse matrix nonzeros by the same expression: individual cycle rows and
residual rows can have many entries.

`separate(model, point)` runs a phase-I LP, then checks recovered dual weights
using exact rational arithmetic. It returns one of:

- `certified_outside`: a globally valid original-variable cut, with exact
  nonnegative multipliers that cancel every extension variable and certify
  strictly positive cut violation at the supplied rational point;
- `numerically_feasible`: phase I returned zero, without an exact membership
  certificate;
- `uncertified_outside`: phase I was positive but exact multiplier recovery
  failed;
- `solver_failure`: the numerical phase-I solver did not succeed.

Certificate recovery first rationalizes dual weights and, if needed, solves the
supported kernel equations by exact elimination. Every returned cut is checked
after recovery. This uses classical Farkas projection, and is not a claim of a
new separation theorem. Tiny infeasibilities can be missed by floating point
phase I. Float input denotes its Python decimal text; supply `Fraction` values
when exact intended data matter. No exact feasible decomposition is returned.

The hull is for the original flow polytope and simplex product graph. Additional
linking constraints can be imposed on this hull as a relaxation; doing so does
not generally yield the hull of the additionally constrained product graph.

## Reproducible verification

```bash
PYTHONPATH=code python -m network_simplex_compressed.verify
```

The deterministic seed-0-to-99 test generates arbitrary directed multigraphs,
including graphs outside the parallel-path class. Both the initial and
observation-eliminated formulations are compared with the independently
implemented full-state formulation in `network_simplex_benchmarks/baselines.py`.
The balance convention there is the opposite, so the test explicitly negates
balances. The current run passes 600 objective comparisons, 758 membership
checks, and 476 recovered exact cut certificates. Each cut is additionally
maximized over the independent full-state hull as a numerical global-validity
check. Auxiliary counts are compared with independently computed cycle ranks
of unobserved subgraphs, and every extension coefficient is checked to be
`0`, `1`, or `-1`. Six additional models test empty/degenerate and infeasible
inputs. These finite checks supplement the proof and independent review;
they do not establish exactness on their own.

The integration command

```bash
PYTHONPATH=code python -m network_simplex_compressed.integration
```

checks the new sharp K4 section and the series–parallel Fibonacci sections at
`q=5` and `q=8`. Both formulations recover exact violated cuts whose two free
product coefficients have ratios `2`, `5`, and `21`, respectively. Multiplier
cancellation is checked again independently, and every returned cut is
maximized over the full-state extended hull. Recorded results are in
[integration-output.json](integration-output.json). This confirms that the
general implementation handles the structural examples beyond the specialized
parallel-path separator, including their required nonunit coefficients.
