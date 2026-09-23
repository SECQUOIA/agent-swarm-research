# Exact constants beyond incidence treewidth two

Status: closed at the user's stop request, with unresolved conjectures explicitly retained. No theorem for treewidth three is claimed here. The [treewidth-two theorem](../results/positive-multilinear-treewidth-two-exact.md) proves the sharp constant two. The [general incidence result](../results/positive-multilinear-incidence-sharp-growth.md) proves worst ratio asymptotic to k at treewidth k, with lower bound k for every k≥2. Whether the exact constant is k for each k≥3 remains open.

## A sufficient matrix-partition target

If every 0/1 matrix whose bipartite support has treewidth at most k admits a partition of its rows into k balanced matrices, mixing the k classwise exact positive-monomial couplings would prove the sharp upper bound k. A partition into k totally unimodular matrices is stronger and would extend the same conclusion to arbitrary discrete-convex cardinality factors and common-ratio positive boxes.

The row partition is a sufficient mechanism, not known to be necessary for the scalar gap bound. Failure of this graph/matrix claim would not by itself disprove the gap conjecture.

## The stronger cycle property from width two does not extend

The width-two proof produces factor colors for which every monochromatic-factor cycle has an even number of factor vertices, including non-induced cycles. This particular property requires arbitrarily many colors at treewidth three.

Indeed, take G=K_(3,m), with three variable vertices and m factor vertices. Its treewidth is three for m≥3. Every three factor vertices, together with the three variable vertices, contain a six-cycle. Thus a color class satisfying the stronger cycle property contains at most two factor vertices, and at least ceil(m/2) colors are required.

This is a barrier only to the stronger graph invariant. The complete incidence matrix here consists entirely of ones and is totally unimodular: every square submatrix of order at least two has determinant zero. It already needs just one TU class. All six-cycles above have chords, so they do not obstruct balancedness either.

Therefore the next investigation must exploit induced-cycle structure or a more general determinant argument. Simply increasing the number of colors in the existing active/blocking invariant cannot prove an exact treewidth-k bound.

## Bounded three-balanced-class search

[The search script](../code/search_multilinear_treewidth_three_partition.py) generated 3,000 supports with six to eleven variable vertices. It accepts a support only when greedy elimination, including clique fill among remaining neighbors, supplies an elimination order of width at most three. Rejection by this greedy test does not certify that a graph has larger treewidth.

For each accepted support, the script enumerates induced incidence cycles with an odd number of factor vertices and solves the resulting nonmonochromatic factor-color constraints by exact backtracking. Every support admitted three balanced factor classes; 212 did not admit two classes. [The output](multilinear-treewidth-three-partition-search.jsonl) records the counts and the first support requiring three classes.

This is finite combinatorial evidence only. It is not a proof that three balanced classes always suffice, and it does not test the stronger requirement that each class be totally unimodular. The generator is biased toward supports accepted by one greedy elimination order.

## Bounded three-TU-class search

[A second script](../code/search_multilinear_tu_row_partitions.py) directly tested the stronger TU requirement on 300 generated supports with five to nine variables and certified incidence width at most three. Every support admitted three TU row classes. The search added 281 non-TU row obstructions beyond the initial balanced-matrix cycle constraints; [the saved output](multilinear-treewidth-three-tu-partition-search.jsonl) records the counts.

The bounded TU oracle applies the Ghouila-Houri criterion to the transpose: for every subset of columns, it enumerates all signings up to global negation and checks whether every row sum belongs to {−1,0,1}. A failed column-signing problem gives a non-TU row subset, which must not be monochromatic in a TU row partition. Exact backtracking proposes another coloring, and the process repeats. The oracle is exponential in the number of columns and is intended only for these small experiments.

As internal checks, the oracle accepted all-ones matrices, rejected the three-by-three odd-cycle incidence matrix, and rejected the balanced non-TU matrix with rows (1,1,1,1), (1,1,0,0), (1,0,1,0), (1,0,0,1). A separate run on 100 generated width-two supports found two TU classes in every case, consistent with the independently proved theorem. These experiments have not undergone a separate code audit and do not prove the universal three-class conjecture.

## Other direction retained without a claim

Planar incidence graphs may have a sharper universal constant than the general orientation bound. The bipartite planar edge bound supplies an orientation of maximum outdegree at most two, so a finite degree-independent bound already follows from the audited orientation theorem. The candidate sharp constant two, or a two-balanced-row partition for every planar bipartite support graph, was suggested but not investigated to completion. The variable-radix family with at least three levels contains K_(3,b) minors for large b and is not a planar counterexample. No new planarity theorem is claimed.
