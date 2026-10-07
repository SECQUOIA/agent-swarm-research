# Independent review of the minimum-cut adapter

Reviewed `mincut_adapter.py` and `test_mincut_adapter.py`, including the
normalization, signed-cycle core search, exact-flow witnesses, adaptive-cell
trace, rational exact-output argument, and malformed JSON handling.

No remaining correctness defect was found in the stated supported class.
This is a review of the sufficient class and certificate contract, not a
claim that the adapter recognizes every tractable quadratic program.

## Mathematical and implementation checks

- Fixed coordinates are substituted before classification. Continuous core
  coordinates are mapped affinely to the unit interval. Residual coordinates
  retain their actual endpoints, including the rounded integer endpoints
  stored by `BoxQP`. Expanding the substitution gives the implemented
  diagonal, linear, interaction, and constant coefficients.
- A conflicting signed cycle must intersect every feasible additional core.
  Branching on its continuous vertices is therefore complete within the
  stated core-size and search-node limits. Positive residual diagonals remain
  outside this sufficient class, including positive diagonals on integer
  coordinates.
- A verified flow and cut certify the exact conditional endpoint minimum.
  Coordinatewise concavity justifies using endpoints for the residual.
  The cell error uses the normalized core curvature and preserves the global
  optimum throughout pruning. Replay checks all required corners and the
  complete retained-cell history.
- Exact completion uses a uniform rational denominator bound for at least
  one global optimum value. A feasible output with denominator at most the
  same bound inside an interval narrower than the separation of two such
  rationals is globally optimal. The final verifier performs this arithmetic
  directly; it does not need to repeat face enumeration or maximum flow.
- Passing the original `BoxQP` to `verify_mincut` binds the proof to that
  instance. Without that argument, the verifier certifies the embedded model.

## Resource issue found and fixed

The first version constructed every next-level child before checking the
next oracle-query budget. The imported reference replay also constructed
unused children after its final row. These could allocate substantially more
cells than the certificate or query budget required.

The revised solver checks corner demand while constructing children. The
revised replay omits final children, bounds intermediate cell count by the
certificate cache size, and checks `2**len(core) <= len(cache)` before
allocating corner offsets. The latter also prevents a short malformed proof
from triggering an exponential corner allocation.

A concrete regression is
`sum(x_i**2 - (2/3)*x_i)` on the unit box, with all coordinates in the core.
At level 1 all cells survive. With six coordinates and a 729-query budget,
the revised solver completes two levels and stops with a valid resource-limit
certificate before constructing the next 4,096 cells.

Cooperative deadline checks do not interrupt a reference maximum-flow call
or the final exact face-enumeration call while that call is running. The
query and core limits are structural budgets, not hard wall-clock limits.

## Targeted checks actually run

From this directory:

```sh
python3 -m unittest test_mincut_adapter -v
```

All nine tests passed after the resource changes. Tests patch optimization
routines to fail during certificate replay.

Additional independent exploratory checks were run with inline Python:

- With random seed `672044`, 180 rational instances with at most five
  coordinates and two core coordinates were checked against independent
  exact endpoint/core-face enumeration using SymPy. Arbitrary intervals,
  fixed coordinates, signed residual graphs, and integer residual coordinates
  were included. Every reported enclosure and certificate was valid.
- Continuing that random stream, 1,500 signed graphs with at most seven
  vertices were checked by exhaustive enumeration of allowed cores and
  endpoint flips. Core existence agreed in every case.
- 1,705 malformed-value or malformed-shape mutations of a serialized proof
  caused no uncaught exceptions. Equivalent representations and changes to
  non-proof metadata can remain valid; the check does not require rejecting
  those harmless changes.
- After replacement of the replay routine, 120 additional searches, using
  seed `1257`, agreed with the reference trace verifier. These included
  requests for exact output and bounded unfinished searches.
- The six-coordinate query-budget regression above passed. A malformed
  100-coordinate search with one cached corner was rejected before offset
  expansion, with the product constructor patched to raise if called.

These were local, targeted checks. No project-wide verification or CI
inspection was performed.
