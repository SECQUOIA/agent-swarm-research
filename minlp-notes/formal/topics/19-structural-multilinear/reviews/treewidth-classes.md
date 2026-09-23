# Independent review of the final treewidth-two gap assembly

Reviewed 2026-09-20 against W02 and W03 in [CLAIMS.md](../CLAIMS.md).
The reviewer did not author or edit `StructuralTreewidthClasses.lean` or its
class-law and TU dependencies. The reviewer previously implemented the
positive-box flower calculation; that calculation is not independently
reviewed here.

**No mathematical or statement defect found. The final public gap theorems
use actual incidence treewidth at most two and construct the required TU
class laws. Their hypotheses do not assume a coloring, integrality,
simultaneous envelope attainment or the desired gap inequality.**

`structuralScopeGraph` is the ordinary original factor-variable incidence
graph, written with the factors on the left and variables on the right.
Its edges are exactly the nonzero entries of the 0/1 scope matrix. There
is no graph built from a polynomial expansion. `rowFactor` marks exactly
factor vertices. `treewidthTwo_cardinality_bound` proves this graph is
bipartite and invokes the completed W01 theorem on its supplied actual tree
decomposition. Restricting the resulting coloring to factor vertices is
valid because goodness constrains colors only at factor vertices.

`colorClassMatrix_totallyUnimodular` embeds a color-class incidence graph
into the original graph by the injective subtype inclusion on factors and
the identity on variables. Every simple cycle remains simple after that
map. Every factor on it has the chosen class color; pulling back factor
parity therefore proves that it has even factor count. The matrix is
explicitly 0/1, so the proved all-cycle TU criterion applies. Both class
matrices are obtained from the actual graph coloring; TU is not an input
to the final treewidth theorem.

`cardinality_two_TU_classes_bound` then constructs one prescribed-mean law
per class through `TUSlab.exists_cardinality_scopeLaw`. Every factor attains
its lower envelope under its own class law, and the other class law is
bounded by that factor's upper envelope. The common threshold law attains
the upper envelope of every convex cardinality factor. The equal mixture
therefore realizes at least half the sum of local widths as a deficiency
from the common upper endpoint. The conclusion uses actual graph-hull
widths through `factorSum_two_law_bound`. Table values and slopes may be
negative; only finite discrete convexity is required. Empty classes, empty
factor families, unused coordinates, boundary means and zero gaps are not
excluded.

The weighted monomial theorem specializes the final-jump convex count table
without changing scopes. Its imported specialization proves equality of the
actual envelope slices, not just agreement of a scalar upper bound. The
zero-lower-box theorem applies the exact coefficient-rescaling transfer, so
fixed zero side lengths do not require division or add any factor incidences.
The common-aspect theorem uses the original indexed monomial factors, removes
fixed coordinates from each count support, and proves the resulting graph is
a subgraph of the original scope graph. The same tree decomposition therefore
remains valid. It then applies the exponential convex-table transfer with the
newly proved cardinality bound. Equal reduced supports retain their separate
original factor labels, and ratio one and zero coefficients are included.

`structuralScopeGraph_treewidth_of_incidence` supplies the required incidence
orientation bridge through the injective `Sum.swap` homomorphism. Its width
parameter is arbitrary; it does not discard an extra graph condition.
`treewidthTwo_flower_membership` applies this bridge to the already proved
flower support decomposition. Consequently the actual sharpness family's
original supports satisfy exactly the graph hypothesis appearing in the
final monomial theorem, despite the two files' opposite sum-type conventions.
The physical flower uses those same supports, so its scaling does not create
a further graph-membership obligation.

This completes the W02 row-class application and W03 graph-to-gap assembly.
The separate [treewidth-coloring review](treewidth-coloring.md),
[TU-criterion review](tu-criterion.md),
[TU-integrality review](tu-integrality.md) and
[aggregation review](aggregation.md) cover the supporting constructions.
The conclusion is a scalar gap bound, not equality of a lifted factor
polytope with its relaxation. No unrestricted unequal-aspect positive-box
frequency theorem is implied.

Both targeted commands passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralTreewidthClasses --wfail
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-treewidth-classes-review.lean
```

The temporary file printed axioms for class TU, the actual cardinality gap
bound, the incidence-swap and flower-membership bridges, and all three
original-monomial/box bounds. Each uses only `propext`, `Classical.choice`
and `Quot.sound`; none uses `sorryAx`. No proof edits, project-wide local
verification or CI inspection were performed for this review.

Reviewed SHA-256:

```text
9d72b20632d99b98967228aa241af523a1e62fd7931af7d1da939d8d76e26cf1  StructuralTreewidthClasses.lean
```
