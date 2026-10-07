# Shared finite optimization and decomposition construction

The quadratic, constrained, recourse, and polynomial solvers use one exact
finite-tree engine. Each caller supplies the mathematical meaning of its local
tables; the engine computes their minimum, an attaining assignment, every
unary min-marginal, and both directed messages on each tree edge. Independent
certificate checkers verify the model-specific bounds and filtering history.

## Interfaces

[`finite_dp.py`](../solver/finite_dp.py) provides:

```python
layout = prepare_tree(bags, edges, n)
answer = solve_tree(bags, edges, domain_sizes, local_tables,
                    layout=layout, check=resource_check)
```

Each bag table maps every tuple of local domain indices to an integer,
`Fraction`, or `None`. `None` means infeasible. Every original factor must
be assigned to exactly one containing bag. Empty separators, empty bags,
fixed coordinates, branching trees, and an entirely infeasible model are
supported. The result contains `lower`, `point_indices`, `marginals`,
`messages`, and `table_states`. An infeasible minimum or margin is `None`.

The validator checks the tree and running intersection. A prepared layout
reuses projections between refinement stages. It is a trusted internal
object, not an external certificate. The optional resource callback may
interrupt table validation or message computation; incomplete work is not
returned as a completed minimum.

The upward pass minimizes each source-side component conditional on the
separator. The downward pass sums all incoming finite costs and counts
infeasible contributions. Excluding one neighbor takes one subtraction or
one infeasibility-count update. This avoids repeatedly summing all other
neighbors at a high-degree bag. Projecting each state across incident edges
still incurs degree and separator-size costs. Arithmetic work is bounded by
`O(sum_b N_b (1+deg(b)) max(1,p))` with maximum bag size `p` and bag-state count
`N_b`, apart from rational-operation bit costs. No width-independent memory
or time guarantee follows: full bag tables and directed messages are stored.

[`decomposition.py`](../solver/decomposition.py) provides:

```python
result = build_decomposition(n, scopes, strategy="min_fill")
result = decompose_qp(A, strategy="min_table", weights=domain_sizes)
```

Each factor or constraint scope is completed to a clique. Deterministic
elimination uses `min_fill`, `min_degree`, or `min_table`; the latter weights
a candidate bag by the product of its supplied domain sizes. The returned
bags and edges are structurally validated and preserve every input scope.
Disconnected components are joined through empty separators. The result
also reports the order, maximum bag size, width, and number of fill edges.
These are heuristics and upper bounds on optimal width. They are not a
treewidth optimization algorithm, and their preprocessing is not covered
by the finite-table allocation cap.

## Targeted verification

Commands actually run:

```sh
python3 -B -m unittest discover -s research-20261002-decomposition/solver -p test_finite_dp.py -v
python research-20261002-decomposition/completion/reviews/finite-engine/check_finite_engine.py
```

The six implementation tests and eight independent review tests passed.
The independent tests include 40 random branching cases. For each directed
edge they delete that edge and exhaustively optimize its component, without
reusing the engine's recurrence or projections. They also check every
margin and attaining assignment, changes of root and coordinate home,
multiple simultaneous infeasibility causes, empty separators, malformed
inputs, and resource interruptions. The benchmark preparation separately
validated decompositions on 120 random graphs. See the
[independent review](reviews/finite-engine/REVIEW.md) for assumptions and
evidence. No project-wide checks or CI inspection were performed.
