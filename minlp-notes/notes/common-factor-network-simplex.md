# Network–simplex investigation

The twice-reviewed universality and unit-capacity coefficient obstruction are now
preserved in [the standalone result](../results/network-simplex-universality.md).
The proof is maintained there. Its novelty is limited to the transfer from known
transportation universality to sparse bilinear hulls; no claim concerns individual
EC&R multipliers, separation hardness, or large extension complexity.

## 1. Scope of the literature question

Khademnia–Davarnia, *Convexification of Bilinear Terms over Network Polytopes*,
Mathematics of Operations Research 50(2), 1019–1041 (2025),
[open preprint](https://arxiv.org/abs/2302.14151), studies

\[
H(G,O)=\operatorname{conv}\{(x,y,z):x\in\Xi(G),\ y\ge0,
y_1+y_2\le1,\ z_{e,k}=x_e y_k\ ((e,k)\in O)\}.
\]

The observation set \(O\subseteq E(G)\times\{1,2\}\) can be sparse.
Their Appendix, equation (25), already gives a polynomial extended hull for every
simplex dimension. The unresolved structural issue is a complete description in
the original, sparse product coordinates. Their Proposition 1 gives unit
aggregation weights for dimension one; Example 2 exhibits a weight of two for
dimension two. Their higher-dimensional forest procedure covers a special class
of aggregations rather than the full hull.

The later [Davarnia–Rahimian preprint, arXiv:2510.15861](https://arxiv.org/html/2510.15861v1),
Section 1 and Section 3, treats a different bilinear/simplex representation of
chance constraints. It does not state the universality or coefficient obstruction
below. Searches on 2026-09-04 for combinations of bilinear/network/simplex,
universality, and unbounded coefficients found no direct match. This is a limited
novelty search, not proof of priority.

An older adjacent formulation is the marginal cone of three-way contingency
tables. [Rinaldo's 2005 thesis](https://www.stat.cmu.edu/~brian/720-2007-source/nice%20materials/rinaldo-thesis.pdf),
Section 4.3, studies its facets and records a full collapsing description when one
table dimension is two (Proposition 4.3.3), while the three-level case is more
complicated. Our network construction retains the three pairwise margins and a
selected set of individual table cells. Thus it is also a selected-cell extension
of that classical marginal-polytope setting. This connection reinforces the need
to describe the result as an application of known transportation universality.


## Positive structural result

[Cycle and theta blocks](../results/network-simplex-cycle-theta-hull.md) give an exact sparse
original-space hull for arbitrary simplex dimension. The graph may contain
arbitrarily many cycles, provided every biconnected block has at most two
independent cycles. The formulas use five local interval conditions and six
aggregate min/max supports per theta block, with only observed states retained.
Both independent proof audits pass, including the constructive decomposition. A complete
linear inequality family has all flow/product coefficients in {−1,0,1}, providing
a direct complement to the unrestricted-network coefficient obstruction.

## Subsequent development of the broader directions

For an equality-constrained network of cycle rank r, a fundamental-cycle matrix
has entries in {−1,0,1}, so there are at most 3^r distinct arc normal vectors in
cycle coordinates. Sparse simplex-state slices share these normals. Their
Minkowski sum therefore admits a common normal-fan refinement depending only on
r: enumerate possible edge directions from r−1 independent normals, then refine
by the hyperplanes orthogonal to those directions. Support inequalities on the
refinement rays and local Farkas circuits would give an explicit original-space
oracle with parameter-dependent work per observed state. This was an unproved
outline in the initial investigation. The 2026-09-07 continuation completed and
independently reviewed it in the [bounded-block-rank theorem](../results/network-simplex-bounded-rank-hull.md),
including a rank-only coefficient bound and a sharp coefficient-two K4 example.
The cycle/theta result remains the simpler two-dimensional specialization.

The [parallel-path extension](../results/network-simplex-parallel-path-hull.md)
now resolves the suggested k-path subclass: arbitrary many internally disjoint
paths per block retain exact subset cuts and unit flow/product coefficients.
Both independent audits pass. Its proof reduces directly to classical
transportation feasibility; it does not claim new general separation tractability.
The [series–parallel Fibonacci construction](../results/network-simplex-series-parallel-coefficient-growth.md)
now rules out uniform coefficient bounds on the larger class, even with sparse
observations, unit capacities, unit flow, planarity and maximum degree three.
The [fixed-state flat-chain theorem](../results/network-simplex-flat-chain-fixed-states.md)
gives a complementary positive oracle for the same flat topology at fixed
simplex dimension. Fixed simplex dimension on arbitrary nested series–parallel
graphs remains unresolved; the completed flat-profile argument does not compose
automatically over multiple interacting profile vectors.
