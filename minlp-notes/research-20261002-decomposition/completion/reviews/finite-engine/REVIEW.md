# Independent finite-engine review

Reviewed `solver/finite_dp.py`, `solver/decomposition.py`, and
`solver/test_finite_dp.py`. No correctness defect was found in the reviewed
finite min-sum recurrence, traceback, all-coordinate margins, or decomposition
construction. This conclusion concerns exact finite tables; each caller must
still establish what its factors mean and how their optimum bounds its
continuous model.

## Mathematical checks

Deleting a decomposition edge separates the bags into two components. Running
intersection ensures that the variables shared by those components are exactly
the edge separator. A directed message therefore equals the minimum sum of
the source component's factors with the separator fixed. The upward recurrence
implements this identity, and its stored minimizing bag states support a
consistent global traceback.

The downward pass adds every finite incoming cost once and separately counts
infeasible contributions. When it excludes one neighbor, it subtracts that
neighbor's finite contribution or removes its single infeasibility count.
An infeasible local factor remains counted. Thus a message can become finite
after exclusion of its only infeasible neighbor, but cannot become finite when
another infeasible contribution remains. This also holds for empty separators.

Adding all incoming messages to a bag factor gives its global conditional
minimum. Minimizing this expression over the states containing a chosen
coordinate value produces the exact unary margin, regardless of which
containing bag is designated as that coordinate's home.

The structural validator establishes tree connectivity, unique edges, complete
coordinate coverage, and running intersection. Its occurrence-edge count test
is sufficient because every induced subgraph of a tree is a forest. The
decomposition heuristic completes each original scope to a clique. During
elimination it completes the remaining neighbors, so the earliest eliminated
one of those neighbors has a bag containing the whole later-neighbor set.
Joining roots of disconnected components introduces only empty separators.

## Independent computational checks

`check_finite_engine.py` uses full enumeration of original factors as its
reference. For **every directed edge**, it removes that edge, collects the
source component, and independently enumerates its conditional optimum. This
oracle does not reuse the implementation's message recurrence, layout,
projection indices, or decomposition validator.

The eight tests cover:

- A branching star with two-coordinate separators, variable ordering changes,
  fixed coordinates, six choices of root, and different coordinate home bags.
- Forty reproducible random branching trees with varying bag intersections,
  rational costs, infeasible states, and independently chosen home bags.
- Disconnected variable components connected through empty separators, empty
  bags, and an infeasible variable-free factor.
- Global infeasibility caused by two different leaves, including outgoing
  messages that recover feasibility after exclusion of one leaf.
- Zero variables, a single bag, and wholly infeasible finite tables.
- Incorrect table coverage, malformed indices, inexact costs, invalid domain
  sizes, invalid home bags, and a mismatched cached layout.
- Invalid trees, failed running intersection, invalid scopes, asymmetric QP
  input, and independently checked connected coordinate occurrences for each
  decomposition heuristic.
- Propagation of an exception from the resource-check callback.

The checks also compare every unary margin and verify that each returned
traceback attains the enumerated optimum. The final targeted command was:

```sh
python research-20261002-decomposition/completion/reviews/finite-engine/check_finite_engine.py
```

Result: **8 tests passed**. No project-wide checks or CI checks were run.

## Scope and remaining integration obligations

The engine assumes that callers assign each original factor exactly once.
It cannot infer this property from bag tables. A cached `TreeLayout` is a
trusted internal object created by `prepare_tree`, not an authenticated
external certificate. Reusing a layout validates its decomposition identity;
it does not harden against deliberately forged or mutated internal fields.

The exclusion pass avoids recomputing every other incoming sum separately
for every outgoing edge. Its work still includes projecting each bag state
across its incident edges, so an arithmetic work bound must retain a factor
proportional to bag degree and projection size. This review does not establish
bit-complexity bounds or minimum-width guarantees for the heuristic.

The existing solver README still described decomposition inference as absent
when this review began. Root was notified; documentation updates and solver
integration checks are owned by the root and integration authors.
