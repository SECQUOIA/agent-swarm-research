# Component elimination can multiply treewidth

The graph bound in Lemma 7 of Khajavirad's February 2026 preprint is false
under its stated assumptions. A five-vertex counterexample suffices. The
error affects the proof of its logarithmic-parameter formulation-size claim;
it does **not** establish that the claimed polynomial-size SDP formulations
cannot exist by another construction.

Source versions matter. The related polynomial-optimization preprint was
revised on 19 August 2026: its current Theorem 1 assumes small residual
treewidth directly and is not contradicted by this audit. The same false
elimination bound remains in its Lemmas 3–4 and in the proof of Corollary 1.

A valid replacement bounds the treewidth after elimination by a product of
the original treewidth and the largest component boundary. Subdivided
complete graphs show that a quadratic increase really occurs when these
two parameters are comparable. These graph facts are supporting corrections,
not claimed as original graph-theoretic advances.

## 1. The exact source claim and its counterexample

The source examined was Aida Khajavirad, [*Tight semidefinite programming
relaxations for sparse box-constrained quadratic programs*, arXiv:2601.18545v2,
12 February 2026](https://arxiv.org/html/2601.18545v2#S5), specifically
Lemmas 7–8 and Theorem 6. Lemma 7 assumes only that `G[C]` is connected.
After deleting `C` and making its external neighborhood a clique, it asserts

\[
\operatorname{tw}(H)\leq
\max\{\operatorname{tw}(G),\ |N_G(C)|-1\}.
\tag{1}
\]

Take the complete bipartite graph with parts
`{a,b}` and `{u,v,w}`, and set `C={a}`. A tree decomposition with bags

\[
\{a,b,u\},\quad\{a,b,v\},\quad\{a,b,w\}
\]

arranged in a path has width two. The graph has a cycle and hence a
`K_3` minor, so its treewidth is exactly two. Deleting `a` and completing
`{u,v,w}` creates `K_4` on `{b,u,v,w}`. Therefore

\[
\operatorname{tw}(H)=3>2=\max\{2,3-1\}.
\]

This also refutes Lemma 8, whose one-component case includes the example.

The proof of Lemma 7 adds one bag containing `N(C)` at an arbitrary node
whose bag intersects `C`. Its running-intersection argument finds a path
inside the union of the occurrence subtrees of vertices in `C`. That does
not put the path inside a given neighbor's occurrence subtree. In the
displayed decomposition, attaching `{u,v,w}` to the first bag leaves the
bags containing `v` disconnected after `a` is removed.

## 2. A valid replacement bound

The same incorrect bound appears as Lemmas 3–4 of Khajavirad's
[*A polynomial-time solvable class of sparse box-constrained polynomial optimization problems*](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/26/26T_007.pdf),
dated April 27, 2026, Lehigh report 26T-007. Those statements and the proof
of Theorem 1 on printed pages 5–7 were inspected directly. That proof
uses Lemma 4 to assert logarithmic treewidth after elimination. The
counterexamples here invalidate that step as well.

The publication-readiness review found and checked the newer
[arXiv:2604.25033v2, 19 August 2026](https://arxiv.org/html/2604.25033v2).
Its Theorem 1 now assumes `tw(\bar G)=O(log |V|)` for the residual graph
itself. That theorem does not need the invalid implication audited here;
we have not audited its remaining algorithmic proof. Lemmas 3–4 still
assert the false maximum bound. Section 2.3 invokes them to derive
Corollary 1, whose assumptions use the original graph's treewidth and
the component-boundary size together with a component nonconvexity
parameter. On the padded family in Section 4, each eliminated component
is a singleton with a positive diagonal, so that nonconvexity parameter
is zero. The family therefore also refutes the width implication used
in the current Corollary 1's proof. It does not satisfy the current
Theorem 1's direct residual-width hypothesis.

These are gaps in the stated proofs and their width guarantees, not a
proof that every algorithm for the claimed problem classes requires
superpolynomial time. The direct torso-width assumption or the corrected
product bound below supplies a valid replacement for the graph step,
with its corresponding complexity.

Let `G=(V,E)` be a finite graph, `S⊆V`, and `R=V\S`. Let
`C_1,...,C_p` be the nonempty connected components of `G[S]`. Every
external boundary `N_i=N_G(C_i)` lies in `R`. Let `H` be the graph on `R`
obtained from `G[R]` by making every `N_i` a clique. Equivalently, `H` is
the **torso** of `G` on `R`: two retained vertices are adjacent if an
original edge or a path with all internal vertices in `S` connects them.

Set

\[
\Delta=\max_i|N_i|,\qquad d=\max\{1,\Delta\},
\]

with `Δ=0` when `p=0`. Suppose `(T,(B_t))` is a given tree decomposition
of `G` of width at most `κ`. Define

\[
B'_t=(B_t\cap R)\ \cup\!
\bigcup_{i:B_t\cap C_i\ne\varnothing}N_i.
\tag{2}
\]

**Proposition.** The bags in (2), on the same tree, give a tree
decomposition of `H`. In particular,

\[
\begin{split}
\operatorname{tw}(H)
&\leq \max_t|B'_t|-1\\
&\leq \max_t\left(
|B_t\cap R|+\sum_{i:B_t\cap C_i\ne\varnothing}|N_i|
\right)-1\\
&\leq (\kappa+1)\max\{1,\Delta\}-1.
\end{split}
\tag{3}
\]

Empty bags may be kept or removed; they cause no difficulty. If the torso
has no vertices, use treewidth `−1`.

**Proof.** Every retained vertex remains in its original bags. Every
original edge within `R` remains covered. For a newly added edge with both
endpoints in `N_i`, any original bag meeting `C_i` becomes a bag containing
all of `N_i`, so that edge is covered.

For a vertex `v`, let `T_v` be its original occurrence subtree. Write

\[
T_{C_i}=\bigcup_{u\in C_i}T_u.
\]

This is connected: each edge along a path inside `G[C_i]` makes the
occurrence subtrees of its endpoints intersect. If `v∈N_i`, an edge from
`v` to `C_i` gives `T_v∩T_{C_i}≠∅`. The occurrence nodes of a retained
vertex `v` in (2) are exactly

\[
T_v\ \cup\!\bigcup_{i:v\in N_i}T_{C_i}.
\]

They form a connected subtree, since every added connected set intersects
the connected set `T_v`. This proves the running-intersection condition.

Finally, a bag meets at most `|B_t∩S|` distinct components, and each
contributes at most `Δ` vertices. Thus

\[
|B'_t|\leq |B_t\cap R|+\Delta|B_t\cap S|
\leq d|B_t|\leq d(\kappa+1).
\]

Taking an optimal input decomposition yields (3) with
`κ=tw(G)`. The construction itself applies to every supplied decomposition;
its bound uses that decomposition's width. ∎

This is the familiar neighborhood-substitution mechanism behind converting
incidence structure to primal structure. After contracting each `C_i` to
one vertex, the boundary sets act as hyperedges. No novelty is asserted for
this mechanism or for the coarse product bound. For comparison,
[Harvey and Wood, *The Treewidth of Line Graphs*](https://users.monash.edu.au/~davidwo/papers/HarveyWood-TreewidthLineGraphs-arXiv.pdf)
discuss the analogous classical bound
`tw(L(F))≤(tw(F)+1)Δ(F)−1`, as well as sharper line-graph bounds.

The middle expression in (3) can be substantially smaller than the product.
It counts the combined boundary load of components meeting each bag. In
particular, overlap among boundaries makes the exact `|B'_t|` bound better
still. For a single nonempty component with `Δ≥1`, the same construction
also gives `tw(H)≤κ+Δ−1`. These are upper bounds, not exact characterizations.
When every component has at most two boundary vertices, `H` is a minor
of `G`, so the stronger bound `tw(H)≤tw(G)` holds.

## 3. A quadratic increase from independent eliminated vertices

For `k≥3`, let `G_k` be the graph obtained by subdividing every edge of
`K_k` once. Denote its original vertices by `a_1,...,a_k`, and its
subdivision vertices by `b_ij`, `1≤i<j≤k`. Thus `b_ij` is adjacent exactly
to `a_i` and `a_j`.

Eliminate `S={a_1,...,a_k}`. This is an independent set, so every
eliminated component is a singleton, with boundary size `k−1`. Completing
these boundaries makes `b_ij` and `b_pq` adjacent exactly when
`{i,j}∩{p,q}≠∅`. Hence the torso is the line graph

\[
H_k=L(K_k).
\tag{4}
\]

The original graph has treewidth `k−1`. Contracting subdivision edges
produces a `K_k` minor and gives the lower bound. For the upper bound, use
one central bag `{a_1,...,a_k}` and, for every pair `i<j`, attach a leaf
bag `{a_i,a_j,b_ij}`. The width is `max{k−1,2}=k−1`.

The torso has treewidth of order `k²`. The exact established formula is

\[
\operatorname{tw}(L(K_k))
=\left\lfloor\frac{(k-1)^2}{4}\right\rfloor+k-2.
\tag{5}
\]

This is Theorem 1 of Daniel J. Harvey and David R. Wood,
[*Treewidth of the Line Graph of a Complete Graph*, Journal of Graph Theory
79(1), 48–54 (2015)](https://users.monash.edu.au/~davidwo/papers/HarveyWood-JGT14.pdf),
DOI `10.1002/jgt.21813`. The author PDF was downloaded and its theorem was
checked directly; it is stored in [treewidth-sources](treewidth-sources/).

For completeness, the following elementary weaker estimate is sufficient
for all consequences in this note:

\[
\operatorname{tw}(L(K_k))\geq\left\lceil k^2/4\right\rceil-1.
\tag{6}
\]

**Proof of (6).** In any tree decomposition of `L(K_k)`, the edges incident
to an original vertex `i` form a clique and therefore all occur together
in some bag `t_i`. The clique-in-a-bag property follows from the Helly
property of subtrees of a tree applied to occurrence subtrees.

Place one label at `t_i` for each `i`, counting multiplicity. Choose a
weighted centroid `t` of the decomposition tree: every component of
`T−t` contains at most `k/2` labels. Such a centroid exists, for instance
by moving toward a component containing more than half the total weight
until no such component remains. Write the component label counts as
`s_1,s_2,...`; labels at `t` are excluded, so `Σs_j≤k`.

The line-graph vertex `ij` occurs in both `t_i` and `t_j`, and therefore
along their entire connecting path. It belongs to bag `t` unless both
labels lie in the same component of `T−t`. Consequently,

\[
\begin{split}
|B_t|&\geq\binom{k}{2}-\sum_j\binom{s_j}{2},\\
\sum_j\binom{s_j}{2}
&\leq \frac{k/2-1}{2}\sum_j s_j
\leq \frac{k(k-2)}4.
\end{split}
\]

Thus `|B_t|≥k²/4`, which proves (6). ∎

Here `κ=Δ=k−1`, while `tw(H_k)=Θ(κΔ)`. Therefore a generic bound of
order `max{κ,Δ}` or `κ+Δ` is impossible. The product dependence in (3) is
necessary up to a constant along this parameter regime; we do not claim
its coefficient is optimal or that it is tight for every pair `(κ,Δ)`.

## 4. The simultaneous logarithmic assumptions do not control the torso

The preceding core has only order `k²` vertices. To test assumptions
expressed in terms of the logarithm of the total input size, construct the
following connected family explicitly. Attach a path with `2^k` new
vertices to one subdivision vertex of `G_k`. Retain every new vertex.
Call the resulting graph `\widehat G_k` and its torso `\widehat H_k`.

The total vertex count is

\[
n_k=2^k+k+\binom{k}{2},\qquad \log n_k=\Theta(k).
\]

Attaching a pendant path does not change treewidth here: append its
two-vertex bags to a bag containing its attachment vertex. All eliminated
vertices keep their original neighborhoods. Hence

\[
\operatorname{tw}(\widehat G_k)=k-1=O(\log n_k),\qquad
\Delta=k-1=O(\log n_k),
\]

but the torso contains `L(K_k)` and satisfies

\[
\operatorname{tw}(\widehat H_k)=\Theta(k^2)
=\Theta((\log n_k)^2).
\tag{7}
\]

Assign plus loops exactly to the original `a_i` vertices. The plus-vertex
set is independent, so there are no connected triples of plus vertices.
Their numbers of distinct other neighbors are `k−1`; counting a loop
toward degree only adds a fixed constant. The increased degree of the
retained attachment vertex is irrelevant to that condition. Thus this family meets the
graph-side assumptions of the cited Theorem 6. The added path is deliberate
size padding, disclosed here because the claim being tested quantifies over
all graphs satisfying those assumptions. Connectedness does not rescue the
claimed logarithmic torso bound.

Theorem 6 asserts polynomial-size SDP formulations when the positive-vertex
components have size at most two and both original treewidth and positive
degrees are logarithmic. Its proof obtains a Boolean residual hypergraph,
uses Lemma 8 to assert logarithmic torso width, and then applies an explicit
tree-decomposition formulation. Equation (7) disproves this intermediate
width assertion for that residual graph.

More concretely, a formulation which introduces a probability variable for
every binary assignment of every bag must have at least

\[
2^{\operatorname{tw}(\widehat H_k)+1}
=2^{\Omega(k^2)}
=n_k^{\Omega(\log n_k)}
\]

variables in a largest bag. Thus the usual full-table junction-tree
construction on this residual graph cannot provide a uniform polynomial
size guarantee under the two separate logarithmic assumptions.

This conclusion concerns that explicit construction. It is **not** a
lower bound on arbitrary linear, SOC, or SDP extensions of the original
quadratic hull. A different formulation could retain eliminated variables,
exploit special local algebra, or compress distributions without full bag
tables. This audit does not resolve existence of such formulations.

## 5. What the corrected parameter bound supports

Suppose a component-based convexification has exact local hull pieces of
manageable size, and its residual Boolean problem is represented by full
bag assignment tables. The sufficient structural condition for that part
of the construction is directly

\[
\operatorname{tw}(H)=O(\log n).
\]

Given a decomposition of the original graph with polynomially many bags,
the stronger, checkable conditions supplied by (2)–(3) are respectively

\[
\max_t|B'_t|=O(\log n),
\quad\text{or more coarsely}\quad
(\kappa+1)\max\{1,\Delta\}=O(\log n).
\]

With both factors separately logarithmic, the corrected generic conclusion
is only `O(log² n)` torso width, giving quasipolynomial table size. A
constant bound on either factor, together with a logarithmic bound on the
other, retains the polynomial conclusion. In particular, the graph issue
alone does not undermine the constant-treewidth specialization.

These statements are conditional on the local hull formulations and a
suitable supplied decomposition. This audit did not reprove the source's
local SDP hull identities, nor analyze the algorithms for finding an input
decomposition. It therefore does not claim a complete replacement theorem
for every assertion in that source.

The useful conceptual point for MINLP is that individually small component
boundaries need not combine into globally small separators. Exact
decomposition must account for how many different component boundaries
cross the same decomposition region. The load in (2) measures this loss
of sparsity directly, while original treewidth and maximum degree alone
can hide their multiplicative interaction.

## 6. Review, computation, and limits

The five-vertex counterexample was first flagged by the separate direction
audit and was reconstructed here from the source's exact assumptions. A
fresh reviewer checked (2)–(3) and the padded family. It correctly required
that the displayed `κ` bound refer to the width of the supplied
decomposition; taking an optimal decomposition then yields a treewidth
bound. A separate reviewer supplied and checked the centroid argument,
and its own fresh reviewer independently checked the two graph proofs.

The targeted command actually run was:

```text
python research-20260925/check_treewidth_elimination.py
```

It passed. The dependency-free script exhausts elimination orders with
memoization for the small graphs, confirming treewidth `2→3` for the
`K_(2,3)` example, `2→2` for `S(K_3)`, and `3→4` for `S(K_4)`. It also
checks the torso/line-graph identity for `k=3,...,8`. These finite checks
support the constructions and arithmetic; they do not prove the infinite
family, the bound (3), or any extension-complexity statement. Those claims
use the proofs above. No Lean formalization was attempted. No project-wide
checks or CI inspection were performed.

Sources examined in this audit were the exact arXiv v2 statements and
proofs named above, including the August revision of the polynomial
optimization preprint and the older Lehigh report; Harvey and Wood's exact complete-line-graph theorem;
their broader line-graph treewidth paper; and searches under torso,
incidence/primal treewidth, component elimination, and line-graph bounds.
No claim that this correction has not appeared elsewhere is made. The
literature search supports identifying a concrete error and an appropriate
classical replacement mechanism, not a novelty certificate.

The independent publication-readiness audit, including the source-version
comparison, is recorded in [publication-treewidth-review.md](publication-treewidth-review.md).
