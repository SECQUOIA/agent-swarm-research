# A sparse blockwise extended hull in cycle coordinates

Date: 2026-09-07. Status: proved and
[independently reviewed](review-network-simplex-reopened-compressed-hull.md).
The [literature comparison](network-simplex-reopened-literature.md) credits
classical disaggregation, product-domain gluing and network linear algebra.
The stronger [observation-sensitive refinement](network-simplex-observed-rank-elimination.md)
counts only cycles supported entirely on unobserved arcs. This is an implementation-oriented
compression of classical simplex disaggregation, not a claim of newly tractable
general hull membership.

## Theorem

Let `Xi={x:Ax=b, 0<=x<=u}` be a bounded rational equality-constrained
network-flow polytope, let `y>=0, sum(y)<=1` have `m` coordinates, and retain
the products `z_ej=x_e y_j` for `(e,j)` in an observation set `O`.
Let `B` range over non-bridge undirected biconnected blocks, let `r_B` be
their cycle ranks, and let `a_B` count the distinct simplex labels observed
in block `B`. A self-loop is treated as a separate rank-one block.

The exact sparse graph hull has a rational extended formulation with

```
sum_B r_B a_B
```

additional continuous variables and

```
O(|V|+|E|+m+|O| + sum_{B:a_B>0} r_B(a_B+1))
```

linear constraints. The bound counts the ordinary input-domain constraints.
These are variable and row counts; for growing rank, the number of matrix
nonzeros can be larger by a rank-dependent factor.
Every extension-variable coefficient can be chosen from `{0,-1,1}`.
Network data occur in the original-coordinate coefficients and right sides.
All coefficients have polynomial rational encoding length. In particular,
fixed maximum block cycle rank gives a formulation of size linear in the
graph, simplex list and observation count; no factor `m|E|` is required.

The theorem applies to arbitrary graphs; its parameter counts their actual
block cycle ranks. No claim that the coefficient matrix is totally unimodular
is made. Product bounds and additional constraints can be intersected with the
hull as a relaxation; that intersection need not be the hull of the constrained
original graph.

## Construction and proof

Obtain a rational reference vector `v` with `Av=b`, without requiring capacity
feasibility. Failure of component balance proves that `Xi` is empty. The
circulation space splits over biconnected blocks. Bridges have `x_e=v_e`.
Consequently the candidate must satisfy the original flow bounds and balances,
the simplex inequalities, and `z_ej=v_e y_j` for observed bridges.

In each cyclic block suppress maximal paths whose internal vertices have
block degree two, retaining the signs of the original arc orientations. A
rank-one block is a cycle and is represented by a one-edge loop. For `r>=2`,
the suppressed core has minimum degree three and at most `2r-2` vertices and
`3r-3` edges (loops count twice in degrees). Write its edge count as `k_B`.
Every circulation has the form

```
x_e = v_e + epsilon_e delta_p,      e on core path p,
```

where `epsilon_e` is `+1` or `-1`, and the core deviations have zero divergence.
Original arc bounds give `L_p<=delta_p<=U_p` by intersection along each path.
Different blocks have independent circulation coordinates even when they share
articulation vertices.

Choose a spanning forest of the core and its fundamental-cycle matrix `C_B`,
of size `k_B` by `r_B`. Orient its chord rows to form the identity, so
`delta=C_B t` and all entries of `C_B` are `0,+1,-1`. Each coordinate of `t`
is one signed original-arc deviation, a linear function denoted `t_B(x)`.
The original flow constraints guarantee all path identities used here.

Let `J_B` be the observed labels in `B`. Introduce one vector `h_Bj` of
`r_B` real variables for each `j` in `J_B`. Define

```
lambda_* = 1-sum_{j in J_B} y_j,
h_*      = t_B(x)-sum_{j in J_B} h_Bj.
```

Impose, for each explicit label,

```
y_j L_p <= (C_B h_Bj)_p <= y_j U_p       for all core paths p,
z_ej = y_j v_e + epsilon_e (C_B h_Bj)_p  for each observed (e,j),
```

and impose the residual bounds

```
lambda_* L_p <= (C_B h_*)_p <= lambda_* U_p.
```

If `J_B` is empty these constraints add nothing: the residual is exactly the
original feasible block circulation. Thus no auxiliary vector is needed there.

To prove exactness, start with classical simplex-vertex disaggregation. For
each simplex state the flow is its weight times `v`, plus an independent
circulation in every block. The displayed bounds and observations are precisely
the conditional state-flow constraints in core coordinates. All states
unobserved in a given block have the same unscaled convex domain, so their
weighted Minkowski sum is that domain scaled by their total weight. This proves
necessity of merging them into `*` and proves sufficiency by proportional
refinement. The global state weights remain `y_1,...,y_m,1-sum y`; different
blocks can use different merged sets because their circulation coordinates are
independent. Combining the refined block coordinates gives each global state
flow. Zero-weight states have zero circulation deviations because all path
bounds are finite and the chord rows of `C_B` form the identity.

There are `r_B a_B` extension variables, `2 k_B(a_B+1)` bound rows for an
active block, and one equation per observed product. The core-size bounds give
the displayed count. Every extension-variable coefficient comes from a cycle-matrix
entry, a path orientation, or the residual subtraction; hence it is `0,+1,-1`.
Reference flows, path interval intersections and cycle matrices have polynomial
encoding length. This completes the proof.

## Why this may matter

The standard full disaggregation uses a state flow on every original arc for
every simplex label. There are two independent possible savings here: only
labels observed within a block need explicit state variables, and long
degree-two paths need one circulation coordinate rather than per-arc state
flows. For fixed rank per block, the formulation can therefore remain linear
in sparse input size even when both the graph and simplex dimension grow.

These are structural size bounds, not runtime or memory measurements. Benchmark
against this compressed formulation as well as the naive full formulation;
otherwise a separator can appear beneficial solely because the baseline ignores
the same sparsity. The simple block/state and path reductions may have prior
equivalents and require a targeted source comparison before any novelty claim.
