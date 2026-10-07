# Prior-art audit: SPN graphs and bounded treewidth

Date: 2026-10-02. This focused audit asks whether sparse graph structure can
make the copositive cone equal to the tractable SPN cone, and whether that
literature already gives curvature- or margin-dependent decompositions. It
does not claim a complete SPN-graph classification.

## Main finding

Treewidth at most two is not sufficient for every graph to be SPN. The
five-vertex fan `F5` is a width-two graph and is explicitly proved non-SPN.
There are useful positive classes: all forests, graphs whose every block has
at most four vertices, and graphs assembled at cut vertices from known SPN
blocks. In particular, cacti (whose blocks are edges or cycles) are SPN.
For these graph classes, copositivity reduces to SPN membership, represented
by a positive-semidefinite-plus-entrywise-nonnegative decomposition. This is
a standard SDP feasibility model; the papers call it tractable, but the
claim here is about the cone reduction, not a bit-complexity guarantee for
exact semidefinite feasibility.

The strongest broad classification remains open. Hogben and
Shaked-Monderer conjecture that a graph is SPN exactly when it has no `F5`
minor. Their 2019 paper reduces the minor-free side to a precise list of
blocks, but the unresolved cases are subdivisions of the graphs `T_k` for
larger `k`. The 2025 survey still reports the characterization as open.

## Definitions that matter for the solver comparison

For a symmetric matrix `A`, the graph `G(A)` has an edge `ij` exactly when
`i != j` and `A_ij != 0`. A graph `G` is SPN if every copositive matrix with
exact off-diagonal support graph `G` is SPN, where SPN means `A=P+N`,
`P` positive semidefinite and `N` entrywise nonnegative. This uses all
nonzero off-diagonal entries, regardless of sign. It is different from the
graph of negative interactions.

That distinction matters for the Horn-based example in
[`geometric-copositive-certificate.md`](../new-direction/geometric-copositive-certificate.md)
and the box-jet example: `Q=J-2A(C5)+I/5` has negative entries on the cycle,
but positive entries on every nonedge of the cycle. Its nonzero-pattern
graph is `K5`, not `C5`; the `C5` negative-entry graph has width two, while
the graph used in the SPN-graph theorems is dense and has treewidth four.
The graph results therefore do not supply a width-two SPN test for that
matrix.

## Exact positive and negative graph results

Shaked-Monderer proves the following in “SPN graphs: When copositive = SPN”
([arXiv:1604.02172](https://arxiv.org/abs/1604.02172), published in *Linear
Algebra and its Applications* 509 (2016), 82–113,
[DOI 10.1016/j.laa.2016.07.018](https://doi.org/10.1016/j.laa.2016.07.018)):

- Corollary 4.4: a graph is SPN exactly when each of its blocks is SPN.
- Corollary 5.3: if each block has at most four vertices, the graph is SPN;
  forests are a special case.
- Theorem 5.4: if `G(A)` is acyclic, then `A` is copositive exactly when it
  is SPN, and exactly when the matrix formed from the diagonal and the
  negative off-diagonal entries of `A` (zeroing its nonnegative
  off-diagonals) is positive semidefinite. This gives a direct PSD test for
  forest support.
- Theorem 9.1: every cycle is SPN. Thus every cactus graph is SPN by the
  block criterion.
- Theorem 7.3: on five vertices, `G` is SPN exactly when it does not contain
  `F5` as a subgraph. Lemma 7.1 supplies the counterexample: the displayed
  copositive matrix has exact support `F5` and is not SPN.

`F5` is the fan formed by adding a universal vertex to a four-vertex path.
The path decomposition with bags `{h,v1,v2}`, `{h,v2,v3}`, `{h,v3,v4}` has
width two. Consequently, the class of all treewidth-two graphs contains a
non-SPN graph, so a uniform reduction from copositivity to SPN membership
cannot cover that class.

Hogben and Shaked-Monderer, “SPN Graphs,” *Electronic Journal of Linear
Algebra* 35 (2019), 376–386 ([official article/PDF](https://doi.org/10.13001/1081-3810.3747)),
give a stronger obstruction and state the outstanding classification:

- Theorem 1.1 and Corollary 1.2: a subdivision of `K4` is SPN exactly when
  at most one of the original `K4` edges is subdivided.
- Conjecture 1.3: `G` is SPN iff it has no `F5` minor. The paper proves the
  equivalence between “no `F5` minor” and its listed block structure, but
  leaves open whether all graphs in that structure are SPN.
- Theorem 5.1: `G` has no `F5` minor exactly when every block is an edge,
  a `DR_k`, or a subdivision of some `T_k`. The paper records that `DR_k`
  are SPN; subdivisions of `T_k` are known SPN for `k=3,4`, and `T_5`
  itself is SPN, while the general larger-subdivision cases remain open.

This gives useful affirmative width-two subclasses, but not all width-two
graphs. Examples include forests, cacti, graphs with every block of order
at most four, and cut-vertex unions of cycles, `T_5`, `K_{2,4}`, and other
individually established SPN blocks. It would overstate the literature to
promote the no-`F5`-minor conjecture to a theorem or to claim that all
treewidth-two copositivity reduces to SPN.

The current-state survey, Shaked-Monderer, “CP graphs and SPN graphs,”
*Communications in Optimization Theory* (2025),
[DOI 10.23952/cot.2025.3](https://doi.org/10.23952/cot.2025.3), §4,
explicitly says the SPN-graph characterization is not solved. Its Theorem
4.1 lists known forbidden subgraphs; this is not a characterization. The
extracted text of Theorem 4.2 ends with “completely positive” despite the
surrounding discussion being about possible SPN blocks, so this audit does
not rely on that line for an SPN theorem. The 2016 paper plus the 2017
corrigendum and 2019 article provide the specific positive results used
above.

## Decomposition, scaling, and quantitative margins

The SPN papers provide a qualitative decomposition when the graph is in a
known SPN class. Shaked-Monderer notes that if `A` is SPN, one may choose
`A=P+N` with `diag(P)=diag(A)` and `diag(N)=0`; positive diagonal congruence
preserves both copositivity and SPN status. These are structural
normalizations, not bounds on `||P||`, `||N||`, or their size in terms of a
strict copositivity margin, negative curvature, or `L/g`.

The sources checked here establish no quantitative extraction bound of the
form sought by the sparse-certificate work. The Horn and SPN results are
qualitative cone-membership and graph-class theorems. In particular, a
strictly copositive matrix on an SPN graph admits some SPN decomposition,
but these results do not control how a selected PSD part or copositive
residual behaves under the condition ratios in the candidate algorithm.
Positive diagonal scaling is allowed as a cone symmetry, but no theorem
found ties its scaling factors to a prescribed curvature/growth ratio.

## Source access and version caveat

The primary arXiv HTML for the 2016 paper, the author’s 2017 corrigendum,
the official 2019 journal PDF, and the 2025 survey PDF were inspected.
Shaked-Monderer’s corrigendum ([arXiv:1712.05115](https://arxiv.org/abs/1712.05115))
corrects the claim that every `T_n` (triangles sharing a common base) is SPN:
the proof error invalidates that result and its `K_{2,n}` consequence for
`n>4`; only the `n=5` case is restored. The original arXiv HTML has theorem
numbering that differs from the journal paper/corrigendum and retains the
retracted general claim, so no result about general `T_n` or `K_{2,n}` is
used here. These three sources and the 2025 survey have been queued to the
designated literature reader for local package verification; the KB has
not been edited in this audit.
