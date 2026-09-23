# Novelty screen: exact gap two at incidence treewidth two

Status: bounded primary-literature screening, 2026-09-04. No exact antecedent was located for either the one-sided cycle-coloring theorem or its two-TU-row-block consequence. No exact antecedent was located for the resulting sharp scalar gap comparison. This is provisional evidence, not a certification of originality. Mathematical correctness has separate independent reviews linked in [the result](../results/positive-multilinear-treewidth-two-exact.md); this note does not replace those reviews.

## Statements being screened

The graph statement is: if a finite simple bipartite graph G=(V,F;I) has treewidth at most two, F has a two-coloring such that every cycle with monochromatic F vertices has length divisible by four. The cycles need not be induced.

The matrix consequence is: every 0/1 matrix whose bipartite support graph has treewidth at most two admits a partition of its rows into two totally unimodular submatrices. The partition retains all columns in both blocks. It is neither an edge partition nor a signing of the whole matrix.

For sums of positive monomials this yields tbtgap <= 2 chgap pointwise, with sharp constant two. The same argument covers multiaffine interpolants of discrete-convex cardinality costs, and positive boxes with a common bound ratio within each monomial. The result file gives sharpness at every fixed common ratio greater than one. Arbitrary unequal ratios within one monomial are outside that extension.

The potentially original structural ingredient is the row partition. Camion's criterion, TU integrality, series-parallel decomposition, and the averaging argument that transfers a partition into a gap bound are classical tools or direct consequences of them. If the row partition is found in prior work, the novelty claim must be reduced to the precise gap comparison, extension, and sharpness examples.

## Classical ingredients and close terminology

**Camion and balanced-matrix integrality.** Camion's criterion converts the all-cycle property into total unimodularity: an Eulerian support subgraph decomposes into cycles, so its number of edges is divisible by four. Mixed packing/covering integrality for balanced matrices supplies the weaker integrality property needed for monomials. These are established results; see Theorems 6.5 and 6.13 in [Cornuejols' notes](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf). Neither criterion itself partitions an arbitrary support graph into two admissible row classes.

**Series-parallel matrices are a different class.** Walter defines binary series-parallel matrices through adjoining zero or unit rows/columns and duplicating rows/columns; the reverse operations recognize the class. Signed versions also allow sign changes. This terminology concerns matrix and matroid structure, not the assertion that the displayed bipartite support graph is series-parallel. See the introduction and Section 3.1 of [Walter, Recognizing Series-Parallel Matrices in Linear Time](https://arxiv.org/pdf/2111.07628).

A direct distinction is

    A = [1 1 0
         0 1 1
         1 0 1].

Its support is C6, hence has treewidth two. But det(A)=2, and A has no zero/unit row or column and no pair of duplicate rows or columns. Thus this matrix does not admit even a first series-parallel reduction. Results for Walter's class do not establish the proposed theorem for support treewidth two.

**Equitable colorings of balanced matrices ask for different output.** Zambelli's thesis characterizes k-balanced matrices by equitable colorings of every submatrix. In a two-color version, columns are colored so each row has sufficiently many entries of each color; the multicolor version has the corresponding row-count condition. See Chapter 6, especially Theorems 6.7 and 6.11, of [On Perfect Graphs and Balanced Matrices](https://personal.lse.ac.uk/Zambelli/papers/Thesis.pdf). The input is already k-balanced, and the conclusion balances counts. Here an input such as C6 is unbalanced, and the objective is a partition of its rows into TU matrices. The quantifiers and the matrix property required of the color classes are different.

For the same reason, the usual Ghouila-Houri signed-sum characterization of TU should not be confused with a fixed partition into two TU row blocks. Choosing a suitable signed bipartition for each row subset is a different assertion.

**Balanceable bipartite graphs are a relevant adjacent language.** Aboulker, Radovanovic, Trotignon, Trunck and Vuskovic define balanced bipartite graphs through induced cycles of length divisible by four. They define restricted balanceability by the existence of an edge assignment of +1/-1 whose sum on every cycle is divisible by four, including non-induced cycles. See the introduction of [Linear balanceable and subcubic balanceable graphs](https://algorithms.leeds.ac.uk/wp-content/uploads/sites/117/2017/09/ConfortiRaoConjecture.pdf). Our color classes satisfy this latter cycle-sum condition with every edge assigned +1. The paper studies structure of graphs already satisfying balanceability assumptions; no partition theorem for arbitrary bipartite partial 2-trees was located there.

**Signed-graph balanced coloring uses another convention.** In signed-graph coloring, a balanced vertex class means all its cycle sign products are positive; see Definition 4 in [Balanced-chromatic number and Hadwiger-like conjectures](https://arxiv.org/pdf/2308.01242). This is distinct from the preceding cycle-sum convention.

There is a concrete obstruction to identifying the desired cycle property with an edge signing on the original graph. Take a bipartite theta graph with three internally disjoint terminal paths of lengths 1, 3 and 5. Its three cycles have lengths 4, 6 and 8. Giving these cycles signs positive, negative and positive would make their product negative. In any edge signing, their product must be positive, because every edge occurs twice. Thus the natural sign prescription, positive exactly for cycle lengths divisible by four, is not a signed graph on this support. This rules out that direct reduction, not every possible auxiliary-graph construction.

## Important boundaries

The all-cycle property is stronger than total unimodularity. For G=K_(3,m), with the m-vertex side colored, each color can contain at most two vertices if all monochromatic cycles must have length divisible by four: any three give a 6-cycle. Thus this coloring needs at least ceil(m/2) colors. Yet its all-ones biadjacency matrix is TU. Consequently this particular cycle invariant cannot have a bounded-color extension to incidence treewidth three, even though this example requires only one TU block. Failure of the stronger invariant says nothing by itself about the optimal number of TU row blocks.

A stronger possible partition into two chordal-bipartite row classes remains unresolved here. Such a partition would exclude all monochromatic induced cycles of length at least six, whereas the written proof allows cycles of length eight. The author reports 5,000 generated support graphs passing a finite feasibility search for this stronger property; [the search output](multilinear-chordal-bipartite-partition-search.jsonl) is evidence only. No theorem is inferred from that search, and no exact prior partition result was found under chordal-bipartite or beta-acyclic terminology.

Exact extended formulations at bounded incidence treewidth are already known. Capelli, Del Pia and Di Gregorio's Theorem 1 gives polynomial-size multilinear-polytope formulations under bounded incidence treewidth; see [their paper](https://arxiv.org/pdf/2311.00149). The present comparison concerns the original termwise relaxation and the scalar convex-hull gap, rather than the ability to build a stronger exact formulation. Generic bounded-width tractability does not supply this numerical ratio. The broader distinction from CSP local polytopes is recorded in [the structural novelty screen](multilinear-structural-novelty.md).

## Search scope and defensible positioning

Queries combined row partition, two totally unimodular submatrices, unimodular coloring, balanced hypergraph partition, one-sided cycle coloring, cycles modulo four, restricted balanceability, partial 2-trees, series-parallel support, and chordal-bipartite/beta-acyclic partitions. Full primary texts were checked for the adjacent results identified above. Several apparently close uses of “balanced” refer instead to equitable color counts or signed-cycle products.

The defensible current claim is that this search found no prior statement of the two-TU-row partition for support treewidth two, nor of the exact scalar gap constant two with the stated extensions. The graph lemma deserves a separate literature check by a specialist in balanced matrices or bipartite graph structure before publication-level novelty is asserted. The sharp gap result remains mathematically useful regardless of whether that graph lemma has an older formulation.
