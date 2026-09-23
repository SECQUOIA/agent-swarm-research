# Eliminating observed directions: auxiliaries count unobserved cycles

Date: 2026-09-07. Status: **independently verified**. The derivation was written
by `review_compression`, developed from the root author's pivoting observation.
The separate reviewer `review_separator` passed the theorem, corollary, and
completion statement, with 204 exact observation-pattern checks; see the
[independent review](review-network-simplex-observed-rank-elimination.md).
This establishes correctness, not literature priority; the direct reduced-RLT
precursor and the narrower proposed contribution are discussed below.

This refines the [compressed blockwise hull](network-simplex-reopened-compressed-hull.md).
The ingredients are classical simplex disaggregation, network-matrix total
unimodularity, and elimination of observed state flows. The proposed useful
statement combines them into an observation-sensitive size bound and an
original-variable hull criterion. It is not a claim of a new general
polynomial-time hull-membership method.

## Statement

Use the bounded equality-constrained network-flow domain and sparse
network–simplex graph from the linked note. Let `B` be a cyclic undirected
biconnected block, let `r_B` be its cycle rank, and let `J_B` be the labels
observed in that block. For `j in J_B`, let `O_Bj` be the observed arcs in
that block with label `j`. Define

```
rho_Bj = cycle_rank((V_B, E_B \ O_Bj))
       = |E_B \ O_Bj| - |V_B| + components(V_B, E_B \ O_Bj).
```

Isolated vertices are counted in the last component count. Parallel arcs
remain distinct, and a self-loop is a rank-one block.

**Theorem.** The sparse graph hull has an exact rational linear
extended formulation with

```
sum_B sum_{j in J_B} rho_Bj
```

additional continuous variables, and the same row bound as the linked
compressed formulation:

```
O(|V|+|E|+m+|O| + sum_{B:J_B nonempty} r_B(|J_B|+1)).
```

Every coefficient on an original flow variable, observed product variable,
or additional variable can be chosen in `{0,-1,1}`. Simplex coefficients and
right sides contain the rational network data and have polynomial encoding
length. The variable count is an upper bound for this formulation, not a
lower bound on extension complexity or a claim that every auxiliary is
necessary when capacities impose additional affine restrictions.

**Forest-complement corollary.** Suppose, for every block and every label
observed in that block, the arcs not observed with that label form a forest.
Then the same construction uses no additional variables. It is an exact
original-variable linear hull description with unit flow/product
coefficients, on arbitrary underlying network graphs. Equivalently, each
active block/label observation set intersects every undirected cycle of
its block. Blocks in which a label is entirely unobserved impose no such
condition, since that label is merged into the block's residual state.

This condition can be checked by a spanning-forest computation on each
unobserved subgraph. It concerns the flow graph, not the interaction graph
of bilinear terms. The criterion is sufficient, not necessary: earlier
cycle/theta and parallel-path results also give original-space formulas
in cases where some unobserved cycles remain.

## Proof

Suppress degree-two block paths as in the linked note. Fix a block, suppress
the block subscript, and let `C` be its `k by r` fundamental-cycle matrix,
with identity chord rows. It is a totally unimodular network matrix with
additional identity rows: every square minor is `0,+1,-1`. This standard
network-matrix property also follows by expressing cycle coefficients with
a reduced node–arc incidence matrix and a spanning-tree basis; each minor
is the determinant of another incidence-basis matrix divided by the tree
basis determinant. Reversing path or row orientations preserves the property.

For a label `j`, the original compressed formulation uses `h_j in R^r`.
An observed arc `e` on path `p` has

```
(C h_j)_p = q_ej,     q_ej = epsilon_e (z_ej - v_e y_j).
```

Let `D_j` consist of `d_j` independent observed path rows of `C`, and
choose one actual observed arc for each selected row. Its corresponding
vector is `q_j`. Different selected rows use distinct observed products.
All observation equations, including repeated observations along a path,
will be retained after substitution; only these independent ones are used
for elimination.

Since `D_j` has row rank `d_j`, choose `d_j` columns `I_j` with nonsingular
square submatrix `B_j=D_j[:,I_j]`. Write the other columns as `F_j` and use
`g_j=h_j[F_j]` as the retained variables. Total unimodularity gives
`det(B_j)=+1` or `-1`, and

```
h_j[I_j] = B_j^-1 (q_j - D_j[:,F_j] g_j).
```

For each core path row `c_p`, define

```
W_pj = c_p[I_j] B_j^-1,
R_pj = c_p[F_j] - W_pj D_j[:,F_j],
phi_pj = W_pj q_j + R_pj g_j.
```

Every entry of `W_pj` is a ratio of a `d_j by d_j` minor obtained by
replacing one selected row, and `det(B_j)`. Every entry of `R_pj` is a
ratio of a bordered `(d_j+1) by (d_j+1)` minor and `det(B_j)`.
Thus both `W_pj` and `R_pj` have entries in `{0,-1,1}`. The selected
observation rows reduce to identities. When `d_j=r`, `F_j` is empty and
`phi_pj=W_pj q_j` has no retained variables.

Replace every `(C h_j)_p` in the parent formulation by `phi_pj`. Explicitly,
retain original flow and simplex constraints, bridge observation equalities,
and the following for each active block:

```
y_j L_p <= phi_pj <= y_j U_p                 (j in J_B, all paths p),
q_ej = phi_pj                               (all observations),
(1-sum_j y_j) L_p <= s_p(x)-sum_j phi_pj
                  <= (1-sum_j y_j) U_p      (all paths p).
```

Here `s_p(x)=epsilon_e (x_e-v_e)` for any one actual arc of path `p`.
Using this direct original-arc expression avoids expanding an aggregate
path coordinate into several chord coordinates. Its equality to the path
deviation follows from the original flow equations and block decomposition.

Elimination is reversible: any retained `g_j` and original observations
determine the discarded coordinates by the displayed inverse formula.
Conversely, any feasible parent-formulation vector yields these retained
coordinates. Therefore the projection is exactly the same hull.

Coefficient claims follow row by row. A state-bound row uses each selected
observed product at most once, with coefficient `+1` or `-1`. A nonselected
observation adds its own distinct product with coefficient `+1` or `-1`;
a selected observation gives an identity that is omitted. In a residual
row, different labels use disjoint products and retained variables, and
the aggregate uses one original flow coordinate. Hence no repeated-column
addition can create magnitude greater than one on flow, product, or
retained variables. Only the simplex coefficients collect data-dependent
reference offsets and path bounds.

It remains to identify the number of retained variables. The kernel of the
map restricting a block circulation to its observed arcs consists exactly
of circulations supported on `E_B \ O_Bj`. Its dimension is `rho_Bj` by
the incidence-rank formula, with loops and isolated vertices included.
Since `C` parametrizes the full `r_B`-dimensional block circulation space,
rank-nullity gives

```
r_B-d_j = rho_Bj.
```

This proves the auxiliary count and the forest-complement corollary.
Elimination adds no constraints; some observation identities disappear.
The row and rational-encoding bounds therefore follow from the parent
formulation. As in that formulation, the row bound is not a sparse-matrix
entry bound for unrestricted rank; fixed block rank gives linear sparse
matrix size.

## What this says in concrete cases

- In a rank-one cycle block, observing any one arc for a label removes its
  only auxiliary coordinate. Repeated observations on that path become
  affine consistency equations.
- In a theta block, observations on two independent paths remove both
  state coordinates. Observing only one path leaves one unobserved cycle
  and one retained coordinate in this formulation.
- In a K4 block, the rank is three. Observing three arcs complementary to
  a spanning tree gives an original-variable state description even
  though K4 is outside the prior cycle/theta and parallel-path classes.
- A self-loop requires observation with the relevant explicit label to
  remove its one hidden coordinate. A two-edge undirected multigraph
  cycle is broken by observing either of its arcs.

The extension gives a stronger baseline for computational comparisons:
the relevant hidden dimension is the number of cycles supported entirely
on unobserved arcs, not simply block rank times active labels. Runtime
benefits require measurement. Extra restrictions on the original nonlinear
graph still do not preserve hull exactness automatically.

## Minimum completion by individual product coordinates

For a block and label, `rho_Bj` is also the smallest number of additional
individual arc-product coordinates needed to determine the entire state
circulation from the existing observations and linear balance equations.
Here determination is in the full ambient circulation space; capacity
constraints that reduce its affine dimension and zero-weight simplex strata
are not included in this count.

Indeed, one extra scalar arc observation increases observation rank by at
most one, so at least `r_B-d_j=rho_Bj` are required. For attainment, choose
a spanning forest in the unobserved subgraph and add the product coordinate
on each of its nonforest edges. There are exactly `rho_Bj` such edges.
The remaining unobserved arcs are a forest, so the completed observations
have full rank by the kernel argument above. One may therefore use these
additional **individual missing products** as the theorem's auxiliary
coordinates, and apply the forest-complement original-space description
to the completed observation set. This is a practical model-construction
interpretation of the variable bound; it is not an extension-complexity
lower bound among arbitrary linear lifts.

## Literature positioning to complete

The general disaggregated extended hull is classical; see
[Khademnia–Davarnia, Appendix (25)](https://arxiv.org/html/2302.14151v2).
Recovering unobserved flows on a forest from observations and balance is
also elementary network linear algebra. A direct predecessor for product
reconstruction by rank is Liberti and Pantelides, *An exact reformulation
algorithm for large nonconvex NLPs involving bilinear terms* (2006),
Theorem 3.1 and Section 2: [open author manuscript](https://citeseerx.ist.psu.edu/document?doi=36b3c1506b43939d697d6e167c3aaa2ece357ba4&repid=rep1&type=pdf).
Their reduced RLT reformulation keeps a complementary set of common-factor
products and replaces the other product equations by multiplied linear
equations. The repository's [literature audit](network-simplex-reopened-literature.md)
records this direct overlap.

A publication should credit these ingredients and frame any contribution
as the explicit network forest-complement criterion, sparse blockwise
simplex hull, and coefficient/size statements. The generic rank-elimination
mechanism should not be presented as new. No priority claim is made for
the combined statement without further targeted comparison.
