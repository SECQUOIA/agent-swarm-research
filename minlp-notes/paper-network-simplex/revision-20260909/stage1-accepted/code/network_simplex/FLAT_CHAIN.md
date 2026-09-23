# Exact flat-chain hull with few observed labels

`flat_chain.py` implements the flat-chain results in
[the manuscript](../../paper-network-simplex/sections/07-fixed-state-chains.tex).
The supplied topology is a serial chain of parallel arc pairs with one bypass,
unit capacities, and unit source-to-sink flow. The model does not recognize
arbitrary input graphs. Production arithmetic uses only Python's standard
library and exact `Fraction` values.

```python
from fractions import Fraction as F
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex

model = FlatChainSimplex(2, 2, [(0, 0), (2, 1)])
point = Point([F(3, 10), F(1, 5)]*2+[F(1, 2)], [F(1, 2)]*2,
              {(0, 0): F(3, 10), (2, 1): F(3, 10)})
answer = model.separate(point, decompose=False)
assert not answer.feasible
assert answer.cut.evaluate(point) == F(1, 10)
```

Gadget `i` has arcs `2*i` and `2*i+1`, both `i -> i+1`; the bypass is
arc `2*gadgets`. Explicit labels range from zero to `simplex_size-1`;
the residual state has index `simplex_size`. Observations may be on either
pair arc, both, or the bypass. Malformed pairs and Boolean/fractional or
out-of-range indices are rejected. Point dimensions and observation keys must
match the model. The example passes McCormick but requires two branch-state
flows of at least `3/10` each, exceeding the total branch flow `1/2`.

## Active labels and outputs

Let `a = len(model.labels)` be the number of labels observed anywhere. All
others share one merged default state, whose weight is one minus the sum of
the observed-label weights. Its profile coordinate is eliminated. Original
simplex constraints are still checked for every original label.

- `a=0`: use the aggregate flow as the normalized default, after domain checks.
- `a=1`: group interval endpoints and recover an interval value directly.
- `a=2`: group six endpoints, check five interval/sum inequalities, and recover
  the two coordinates explicitly. No library enumeration is called.
- `a=3`: use 16 reduced positive circuits. Both possible bypass coefficients
  of magnitude two are repaired with one original gadget flow equation.
  Every returned flow/product coefficient is unit.
- Larger `a`: enumerate the general reduced circuits and inverse bases.
  Their size is exponential in `a`.

The result uses the `Point`, `Cut`, and `SeparationResult` conventions in
[README.md](README.md). Rejected points receive a globally valid cut with
strictly positive exact evaluation. Feasible points optionally receive a
`FlatChainDecomposition`; no numerical LP establishes feasibility.

`decomposition.weights` retains all original weights followed by the residual
weight. `flow(j)` materializes the normalized feasible flow of a positive-weight
original state; `positive_states()` lists those indices. Stored `labels`,
`group_weights`, `group_profile`, and `group_arc_a` use only `a+1` columns,
with the default last. Unobserved labels share its normalized flow. The
compatibility properties `profile` and `arc_a` materialize the formerly dense,
weighted original-state arrays on demand; use the grouped fields or `flow(j)`
when compact output matters.

General recovery enumerates all full-rank bases of the reduced normals. It
does **not** impose the obsolete profile-sum equality on explicit coordinates.
Tests include an interior-residual instance with zero explicit profile but
positive residual branch flow.

## Costs and history

At fixed `a`, construction, separation, and compact recovery are linear in
chain length and observation count, plus a scan of all original weights.
Sorting costs up to `O(|O| log |O|)` comparisons. Tuple normals and hashing
add an `a` factor to some construction work compared with the manuscript's
preindexed-mask bound; the code does not claim that uniform bound as `a`
varies. Dense global-flow output can require `O((m+1)|E|)` operations.

`reduced_library(a)` and `_reduced_bases(a)` are cached; bases are generated
on the first successful decomposition query at `a>=3`. Neither is used at
`a<=2`. The old `circuit_library(d)` and `_profile_bases(d)` remain historical
counting/audit helpers: `1,5,41` counts refer to the unreduced signed-subset
universe, versus reduced counts `1,5,16`. The pre-upgrade oracle is retained
with hashes in `paper-network-simplex/verification/reference/stage06/flat_chain.py`,
not as another public production API.

The [new repeated comparison](../network_simplex_benchmarks/paper_stage06.py)
reports strengthened LP baselines, including cases where they are faster.
Float input denotes its decimal text; the exact oracle uses no tolerance.

## Verification

```sh
PYTHONPATH=code python -m unittest network_simplex.test_flat_chain -v
python code/network_simplex_review/verify_flat_chain_implementation.py
```

Tests cover arbitrary observations, zero weights, exact graph-point recovery,
both three-label repairs and exact global cut validity, the four-label ratio-two
obstruction, sparse labels among many original coordinates, no-library execution,
new unanchored bases, and malformed indices. The earlier independent audit's
old-basis checks remain historical evidence; new tests check reduced bases.
