# Reopened network–simplex literature audit

Date: 2026-09-07. Scope: the original-space hull, separation, and formulation
size of sparse products between an equality-constrained bounded network flow
and a simplex vector. This is a focused primary-source search, not a proof of
literature priority. It supplements the earlier
[investigation](common-factor-network-simplex.md).

## Assessment

The general hull, simplex-vertex disaggregation, and polynomial separation are
known. Blockwise common-simplex gluing, the geometry of Minkowski sums, and
transportation/min-cut projection also have direct predecessors. A paper should
claim the graph-specific original-coordinate formulas, the precise sparsity and
cycle-rank size bounds, any verified structural obstruction, and measured
computational advantages. It should not claim a new general convexification or
separation principle.

The closest additional predecessor found in this pass is Kis–Horváth's
network representation of Cayley hulls. The strongest current series–parallel
comparison is Almoghrabi–Skutella–Warode (2026), which makes especially clear why
aggregate-flow results do not automatically control retained state-flow
coordinates.

## 1. Direct bilinear predecessors

**Khademnia–Davarnia, Mathematics of Operations Research 50(2), 1019–1041
(2025).** [Open preprint](https://arxiv.org/abs/2302.14151) and
[open published article](https://par.nsf.gov/servlets/purl/10546393).

Their Appendix gives simplex disaggregation for arbitrary simplex dimension;
their original-variable EC&R description is complete generally as a projection
procedure, and the explicit tree family is complete for one simplex coordinate.
The forest/pairwise-cancellation construction is not a full original-space
description for general simplex dimension. Their use of flow-balance inequalities
is more general than the equality-constrained topology developed here.

The proposition numbering differs between the available versions. The existing
repository comparisons using Proposition 1, Example 2, and Appendix (25) refer to
the published-style version; the arXiv v2 HTML has reorganized numbering. Cite a
specific version consistently in a manuscript. Local evidence:
[[khademnia2025-convexification-of-bilinear-terms-over]] p.1-9, p.24-27.

For the rank-three coefficient comparison, their Example 2 specifically proves
that a projection-cone extreme point has an aggregation weight of two. Its
eight-arc graph has a four-cycle and pendant arcs, simplex dimension two, and
flow-balance inequalities. It does not prove a necessary product-coordinate
facet ratio of two for an equality-constrained rank-three K4 network. These
claims should remain distinct. Local evidence:
[[khademnia2025-convexification-of-bilinear-terms-over]] p.11.

**Davarnia–Richard–Tawarmalani (2017), with open thesis precursor.** The local
package is explicitly an open 2016 dissertation despite its journal-article
metadata. Its Proposition 2.6 already proves that separately convexifying
Cartesian-product domains sharing the same simplex yields the joint hull.
After circulation coordinates factor across biconnected blocks, the repository's
block gluing is an application of this principle. Proposition 2.7 treats sums
over the component domains. Local evidence:
[[davarnia2017-simultaneous-convexification-of-bilinear-functions]] p.28-30.
The [open thesis](https://ufdcimages.uflib.ufl.edu/UF/E0/05/02/79/00001/DAVARNIA_D.pdf)
is the correct source for those locators, not journal pagination.

## 2. Network representations of disjunctive hulls

**Kis–Horváth, “Ideal, non-extended formulations for disjunctive constraints
admitting a network representation,” Mathematical Programming 194, 831–869
(2022), online 2021.**
[Open primary article](https://link.springer.com/article/10.1007/s10107-021-01652-z).

Their §1 represents a Cayley hull by state-rooted trees that share coordinate
leaves; tree-arc capacities have the form constant times simplex weight.
Corollary 1 gives the complete cut description, and Theorems 1–2 characterize
facet-producing cuts. Section 5.9, Proposition 22 and equations (30)–(31), shifts
lower bounds and projects a transportation network into subset inequalities.
That is a close predecessor of the parallel-path proof, not merely a generic
max-flow reference.

The repository also retains selected internal state-flow coordinates through
the products z. Those observations make interval endpoints depend on z as well
as simplex weights. The cited network representation does not directly state
this sparse network–simplex application or the graph block/path compression
bound. Thus the possible contribution is the explicit application and its
structure; the cut-projection method is established. No equivalence reduction
covering all observed coordinates was found in this audit.

## 3. Bounded-cycle-rank geometry

**Gritzmann–Sturmfels (1993).** Lemma 2.1.5 identifies the normal fan of a
Minkowski sum as the common refinement of the summands' fans. Proposition 2.1.8
uses an edge-generated zonotope to refine a polytope's fan. Algorithm 2.3.6
constructs the arrangement perpendicular to candidate edges and samples its
cells. These are precisely the classical geometric ingredients for the proposed
fixed-rank network oracle. Local evidence:
[[gritzmann1993-minkowski-addition-of-polytopes-computational]] p.8-9, p.12-14.
This local copy is user-supplied; do not redistribute it.

**Onn–Rothblum (2004).** Their edge-direction framework supplies another direct
source for zonotope refinement and fixed-dimensional enumeration. Algorithm 2.5
and Theorem 2.6 reduce convex combinatorial optimization to linear-oracle calls.
The network application here is continuous and parametric in observations, so
the paper is a geometric foundation, not a direct statement of our desired
oracle. Local evidence: [[onn2004-convex-combinatorial-optimization]] p.4-6.
[Open primary preprint](https://arxiv.org/abs/math/0309083).

**Fukuda (2004).** Proposition 2.1 and Theorem 3.3 provide compatible-face
decomposition and an output-sensitive Minkowski-sum method for explicit
V-polytopes. This is another useful comparator, although the repository starts
with implicitly described state slices. Local evidence:
[[fukuda2004-from-the-zonotope-construction-to]] p.3-5, p.7-9.
[Open author manuscript](https://www.cs.mcgill.ca/~fukuda/download/paper/minksum030111.pdf).

The potentially distinctive fixed-rank statement is a uniform finite set of
support directions and dual certificates depending only on rank, with work
linear in the number of retained state labels after that preprocessing. Merely
polynomial separation at fixed rank would not be a new complexity result.

## 4. General-graph compressed extended formulation

The proposed formulation combines three reductions:

1. Pass to a reference circulation and factor its degrees of freedom across
   biconnected blocks.
2. Suppress degree-two paths, retaining signed representative deviations and the
   strongest path bounds.
3. For each block retain its observed state labels and combine all other labels
   into a single residual weight.

The third reduction is exact because, for a convex P and nonnegative scalars,
lambda P + mu P = (lambda+mu)P. It is stronger information than merely sharing
an inequality matrix: the unobserved state domains are homothetic copies of the
same P. General observed state slices cannot be merged on that argument.

The first reduction uses the established common-simplex product-domain gluing
principle above; the second is elementary network elimination. Searches did not
locate the combined extra-variable/row bound
O(sum_B r_B(a_B+1)), plus input and observations, for sparse network–simplex
hulls. This is a possible application-level contribution, not a new
disaggregation principle. The numerical comparison should include both the
full EF and its ordinarily presolved version, so that trivial elimination is
not mistaken for an intrinsic solver advantage.

### Observation-rank reduction: direct RRLT predecessor

The later refinement eliminates state variables determined by observed products.
For an r-dimensional cycle matrix C and a state's observed rows C_O of rank d,
the undetermined circulation has dimension r-d. This is an exact linear
elimination count, not an extension-complexity lower bound.

There is a direct precursor: **Liberti–Pantelides, “An exact reformulation
algorithm for large nonconvex NLPs involving bilinear terms,” Journal of Global
Optimization 36, 161–189 (2006), DOI 10.1007/s10898-006-9005-4.**
[Open author manuscript copy](https://citeseerx.ist.psu.edu/document?doi=36b3c1506b43939d697d6e167c3aaa2ece357ba4&repid=rep1&type=pdf).
Theorem 3.1 uses a full-row-rank system Ax=b to replace rank(A) common-factor
product equations by Aw=yb, retaining products on a complementary basis.
Section 2 also introduces absent products and eliminates them by combining
multiplied equations. Their RRLT construction is therefore a direct antecedent
of product reconstruction by rank, although it does not state the network
observation-complement criterion or the exact simplex hull consequence here.
The same algebra appears in the
[open thesis](https://www.lix.polytechnique.fr/~liberti/phdthesis.pdf), §3.7,
printed pp.88–89. The latter describes Gaussian elimination with pivoting.

For a network, the graph interpretation is particularly simple. Let U be the
unobserved edges of a block, retaining all block vertices. Then

```
r-rank(C_O) = dim ker(A_U) = |U|-|V_B|+components(V_B,U).
```

The first equality follows by identifying cycle-coordinate vectors vanishing
on O with circulations supported on U. Thus full observation rank is equivalent
to U being a forest. All missing state-flow products can then be recovered by
leaf elimination in that forest from multiplied balances. More generally,
retain one free product for every chord of a spanning forest of U. Tree-cut
equations have coefficients 0,+1,-1, so this reconstruction avoids arbitrary
Gaussian coefficients. Self-loops count as cycles and must be observed or
retained as free coordinates.

The exact hull follows from retaining every reconstructed state-flow bound and
the residual-state bounds of full simplex disaggregation. Omitting those bounds
would generally weaken the formulation. If every active state has full
observation rank, the resulting complete hull is explicit in original
coordinates for arbitrary graph topology. This is a useful graph-specific
specialization of established RLT elimination, not a new general principle of
bilinear linearization. No exact prior statement with this sparse observation
criterion and coefficient conclusion was found in the focused search.

## 5. Series–parallel multiflow comparison

**Almoghrabi–Skutella–Warode, “Integer and unsplittable multiflows in
series-parallel digraphs,” Mathematical Programming (2026), published June 29.**
[Open primary article](https://link.springer.com/article/10.1007/s10107-026-02392-8).

Theorem 1 reduces feasible multiflows on directed two-terminal series–parallel
graphs to single-commodity flow and proves an integrality property for total arc
flows. Theorem 3 gives a sufficient strengthened cut condition. Crucially,
Remark 1 and Figure 2 state that this total-flow integrality does not extend to
the vector of individual commodity flows. Their model bounds aggregate arc
flow; it does not prescribe the repository's arbitrary selected state-flow
coordinates or state-specific interval bounds. Accordingly it neither supplies
our hull nor contradicts a coefficient obstruction in retained product
coordinates. The paper's digraphs are consistently oriented series/parallel
compositions, a narrower orientation class than arbitrary orientations of an
undirected series–parallel graph.

For a final manuscript, cite **Remark 1 explicitly**, rather than only the
main theorem: even their three-commodity example fails the proposed
commodity-vector decomposition although its aggregate vector has the desired
decomposition. This is a precise primary-source warning against inferring a
state-specific hull theorem from aggregate-flow integrality.

**Cornaz–Grappe–Lacroix, “Trader multiflow and box-TDI systems in
series–parallel graphs,” Discrete Optimization 31, 103–114 (2019).**
[Open author paper](https://www.lamsade.dauphine.fr/~rgrappe/papers/tradermultiflow.pdf).
Its box-TDI characterizations concern aggregate undirected cut/cycle/T-join and
related polytopes. They do not directly give a description in selected
commodity-flow coordinates. They are useful context when explaining why a
small-coefficient aggregate-flow theorem is compatible with more complicated
state-specific projections.

### Final Fibonacci family and classical large-coefficient results

Large facet coefficients in 0/1-polytopes are classical. **Alon–Vu,
“Anti-Hadamard matrices, coin weighing, threshold gates and indecomposable
hypergraphs,” Journal of Combinatorial Theory A 79, 133–160 (1997)** constructs
0/1 matrices with extremely large inverse entries and derives related geometric
and threshold-weight consequences; see the Main Theorem and §3 of the
[open author manuscript](https://web.math.princeton.edu/~nalon/PDFS/av1.pdf).
The manuscript file carries a later revision date. **Fiorini, “How to recycle
your facets,”** explicitly states the resulting large-facet-coefficient bound
for general 0/1-polytopes in §1, printed p.2, and transfers arbitrary facet
structure to dicycle-cover and acyclic-subgraph polytopes in §3.
[Open author manuscript](https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf).
Thus exponential numerical coefficients, Fibonacci recurrences, and the broad
idea of transferring coefficients between polytope families are not themselves
new contributions.

The proposed distinction in
[the final series–parallel construction](network-simplex-reopened-series-parallel.md#8-stronger-extension-exponential-ratios-from-fibonacci-covers)
is the restrictive network realization. It forces a scale-invariant ratio F_q
between two retained product coefficients on an ambient facet of a sparse
network–simplex hull. The underlying graph is planar and directed two-terminal
series–parallel, has 2q vertices and 4q-1 arcs, and uses unit capacities and unit
source–sink flow. There are 2q-1 explicit states and only 5q-4 observed products;
the complete model has O(q log q) sparse binary description length. The hull is
a 0/1-polytope. Fixing original coordinates gives the two-coordinate section
used in the proof; arbitrary affine rescaling does not manufacture the ratio.

Neither the classical matrix construction nor Fiorini's graph-polytope transfer
provides these particular network, sparse observation, and coordinate-section
properties. No exact prior realization was found in the focused open-source
search, including its citation chains; this is a bounded-search assessment,
not a proof of novelty. The general balanced-incidence lemma should be stated
with its invertibility, proper-row, and positive-balancing hypotheses rather
than called unrestricted universality.

The result is compatible with Almoghrabi–Skutella–Warode's Remark 1 above:
aggregate-flow integrality does not imply the required description in individual
state coordinates. It establishes growth of numerical coefficient magnitudes,
not superpolynomial coefficient bit length, separation hardness, or an
extension-complexity lower bound. Its explicit-state dimension grows with q.

## 6. Practical applications and benchmark boundary

Khademnia–Davarnia §4.2 uses transportation with service conflicts: flow costs
depend bilinearly on service-choice variables. Its random complete bipartite
networks have 50/100 nodes and 20/30 services. Only conflict pairs are used as
simplex blocks. Therefore these instances are useful application inspiration,
but they do not match an arbitrary-dimensional simplex or the parallel-path
topology without modification.

A direct matching structured example is two-supplier transportation with k
customers. Its underlying graph is K_{2,k}, a union of k internally disjoint
length-two paths. Customer balances eliminate one supplier's flow at each
customer, and the remaining supplier balance is one bounded-sum constraint.
Mutually exclusive service options, with sparse route-specific cost changes,
give exactly the desired sparse products. This is a model specialization
deduced here, not a located published benchmark collection. No open instance
collection matching all these assumptions was identified.

For larger general networks, the compressed EF may have broader application
than the parallel-path oracle. Report generated structured instances honestly;
do not call them empirical industry validation. Compare time, memory, rows,
variables, nonzeros, and cuts. A fully enforced exact EF and exact projected
hull must give the same bound for the same block. Improvements in bound
quality should be measured against McCormick or an incomplete cut family.

## 7. Source-boundary issue retained

Lee–Bernal Neira's shared-coefficient reaggregation discussion must not be used
as an unconditional exactness theorem. The statement needs additional
conditions; see the explicit counterexample and source inspection in
[the separate boundary note](network-simplex-reaggregation-source-boundary.md).
This issue does not affect the homothetic-state merger used here.

## Search coverage and unresolved comparison

Queries combined bilinear/network/simplex with sparse, biconnected, cycle rank,
series-parallel, original-space, Minkowski, edge directions, multicommodity,
coefficients, universality, and reaggregation. Citation chains included the
EC&R papers, Kis–Horváth, classical Jeroslow/Blair/Balas reaggregation, and
recent series–parallel multiflow work. No exact combined sparse-state/block
size theorem or selected-product series–parallel coefficient result was found.
The absence of a match is evidence of search coverage, not certified novelty.

Before submission, the manuscript should explicitly compare any final
series–parallel obstruction with both the 2026 multiflow result and the known
three-way marginal/transportation transfer already documented in this repo.
It should also determine which special cases of the proposed original-space
cuts are direct applications of Kis–Horváth rather than separately novel.
