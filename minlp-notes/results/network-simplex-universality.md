# Sparse network–simplex hulls: universality at simplex dimension two

Status: independently verified structural result, 2026-09-04; novelty provisional.
Both [first audit](../notes/review-common-factor-network-simplex.md) and
[second audit](../notes/review-network-simplex-universality.md) pass the network embedding,
facet-restriction argument, normalization, and coefficient-size conclusion.
The transportation universality input is known. The proposed contribution is its
transfer to coordinate sections and facet coefficients of sparse bilinear hulls.
No claim of new polynomial optimization or separation is made.

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

## 2. Known transportation input

We use De Loera–Onn, *All Linear and Integer Programs Are Slim 3-Way
Transportation Programs*, SIAM Journal on Optimization 17(3), 806–821 (2006),
[author-hosted paper](https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf).
Theorem 1.1 gives a polynomial-time coordinate representation of every bounded
rational polytope in nonnegative standard form by a three-layer transportation
polytope. The construction has an additional property needed here: **all designated
coordinates lie in the first layer**. This follows from the explicit injection in
Section 3.3 (printed page 816):
\(\sigma(i,j,k)=((i,j),(1,k),1)\). Earlier representation maps compose with this
map. Integer standard-form data give integer margins.

Consequently, for any bounded rational polytope \(P\subseteq\mathbb R_+^d\),
including one initially described by inequalities, there are nonnegative integer
margins \(U_{ij},V_{ik},W_{jk}\) and designated distinct entries in layer one such
that their coordinate projection from

\[
T=\left\{t\ge0:
\sum_{k=1}^3t_{ijk}=U_{ij},\quad
\sum_jt_{ijk}=V_{ik},\quad
\sum_it_{ijk}=W_{jk}\right\}
\tag{1}
\]

is exactly \(P\). For inequality descriptions, first introduce nonnegative slacks
and retain only the designated coordinates of the original variables.
The construction size and data encoding length are polynomial in the description
length of \(P\).

We may require all three layer totals
\(D_k=\sum_iV_{ik}=\sum_jW_{jk}\) to be positive. Add one new row and one new
column, fix every cross entry between old and new indices to zero through its
\(U\) margin, and set the new corner's three entries to one through its margins.
This appends a unique, independent block and increases each \(D_k\) by one.

## 3. Network realization of a transportation projection

**Lemma 1.** Given (1) with positive layer totals, and any set \(J\) of designated
layer-one entries, its projection onto \(J\) is a coordinate section of a sparse
bilinear hull \(H(G,O)\). The network is a four-layer acyclic graph
\(s\to\{r_i\}\to\{c_j\}\to t\), all arcs have the same integer capacity, and
the simplex has dimension two. The only observed products are boundary-arc
products with both simplex coordinates and designated interior products with
the first simplex coordinate.

**Proof.** Write \(B=D_1+D_2+D_3>0\). Use arcs \(s r_i\), \(r_i c_j\),
and \(c_j t\), each with capacity \(B\). Let \(\Xi(G)\) be the polytope of
nonnegative flows of value \(B\), with flow conservation at every intermediate
node. Thus the network is feasible and integral.

Observe \(x_e y_k\) for each boundary arc \(e=s r_i\) or \(c_jt\) and each
\(k=1,2\). In addition, observe \(x_{r_ic_j}y_1\) exactly when \((i,j)\in J\).
There are no other interior product coordinates in \(H(G,O)\).

Form the coordinate section by fixing all flow coordinates to

\[
\bar x_{r_ic_j}=U_{ij},\quad
\bar x_{s r_i}=\sum_kV_{ik},\quad
\bar x_{c_jt}=\sum_kW_{jk},
\tag{2}
\]

fixing \(y_k=D_k/B\) for \(k=1,2\), and fixing the observed boundary products to

\[
z_{s r_i,k}=V_{ik},\qquad z_{c_jt,k}=W_{jk},\qquad k=1,2.
\tag{3}
\]

Only the designated interior product coordinates remain free.

To verify the section, use the standard exact disaggregated hull. Put
\(\lambda_1=y_1,\lambda_2=y_2,\lambda_3=1-y_1-y_2\).
A point belongs to \(H(G,O)\) exactly when there exist three nonnegative flows
\(f^k\) such that

\[
\sum_k f^k=x,\qquad f^k\in\lambda_k\Xi(G),\qquad
f^k_e=z_{e,k}\quad ((e,k)\in O).
\tag{4}
\]

For completeness, a feasible triple in (4) is the convex combination, with weights
\(\lambda_k\), of graph points having simplex coordinate \(e_1,e_2,0\) and
flow \(f^k/\lambda_k\); zero weights have zero flows. Conversely, expand every
graph point by the three simplex vertices while retaining its flow, then group
the resulting flows by simplex vertex. This proves (4).

At the fixed section, each \(f^k\) has value \(D_k\); (3) fixes its boundary
flows to \(V_{ik},W_{jk}\) for \(k=1,2\), and (2) fixes those for \(k=3\)
by subtraction. Setting \(t_{ijk}=f^k_{r_ic_j}\), conservation and the sum in
(4) are exactly (1). The scaled upper bounds are redundant: every arc flow in
a nonnegative acyclic flow of value \(D_k\) is at most \(D_k=B\lambda_k\).
Conversely, any table in (1) yields these three flows and hence a section point.
The free coordinates are precisely its entries in \(J\). ∎

**Theorem 2 (coordinate-section universality).** Every nonempty bounded rational
polytope in nonnegative coordinates is coordinate-isomorphic to a section of a
sparse network–simplex bilinear hull with simplex dimension two on a four-layer
acyclic single-source, single-sink network with uniform integer arc capacities.
The construction is polynomial in the input polytope description length.
All coordinates except designated interior products with \(y_1\) are fixed in
the section. The flow coordinates and boundary product coordinates are fixed to
integers; the simplex coordinates are rational.

**Proof.** Apply the known transportation input and Lemma 1. ∎

**Important distinction.** This theorem concerns coordinate sections of the
**sparse original hull**. The hidden products were never original coordinates.
We do not infer anything about facets of a larger hull from facets of a projection.
The complete-product hull retains its familiar small-coefficient extended/RLT
description; the theorem does not contradict that fact.

## 4. Unbounded and superpolynomial original-space facet coefficients

**Lemma 3 (facet restriction).** Let \(H\) be a rational polytope and let \(L\)
fix all but two of its coordinates \(p,q\). Suppose \(H\cap L\), in these
coordinates, is the full-dimensional triangle

\[
P_M=\{(p,q):p\ge0,\ q\ge0,\ p+M q\le1\},\qquad M\ge1.
\tag{5}
\]

Then at least one facet-defining inequality of \(H\), relative to its affine
hull, has coefficients \(a_p,a_q\) with \(a_q=M a_p\ne0\). Indeed every finite
linear description of \(H\), together with affine-hull equations, has an
inequality with this coefficient relation.

**Proof.** Restrict such a finite description to \(L\). Affine-hull equations
restrict to identities: a nonzero equation in \(p,q\) would contradict the
two-dimensionality of (5). At a relative interior point of the sloping edge, at
least one restricted inequality must be tight and nonconstant. Otherwise this
point has an open two-dimensional neighborhood satisfying every nonconstant
restricted inequality strictly and cannot be a boundary point. Any supporting
line at the interior of that edge equals its line. Thus its coefficients are a
positive multiple of \((1,M)\). Apply this to a facet description of \(H\) for
the first assertion. ∎

**Corollary 4.** For every positive integer \(M\), a sparse hull on a four-layer
acyclic network with **unit arc capacities and unit flow value**, and simplex
dimension two, has a facet with coefficient ratio \(M\) on two observed product
coordinates. Every primitive integer representative of that facet inequality has
an absolute coefficient at least \(M\). The ratio is unaffected by adding an
affine-hull equation, since such equations have zero coefficients on the two
free section coordinates after restriction.

Moreover there is no polynomial in the binary model description length that
bounds all primitive integer facet coefficients of this class. Construct the
family from (5) with \(M=2^k\). Its sparse bilinear description has size bounded
by a fixed polynomial in \(k\), while a necessary facet has a coefficient of
size at least \(2^k\).

**Proof.** Apply Theorem 2 to (5). Normalize every flow coordinate and every
observed product coordinate by \(B\), leaving the simplex coordinates unchanged.
This linear isomorphism gives a network hull with unit capacities and unit flow
value. The free section coordinates now satisfy
\(p+M q\le1/B\); their facet coefficient ratio is unchanged. Lemma 3 and its
proof apply equally to this scaled triangle. For an integer
representative, the nonzero integer coefficient \(a_p\) has magnitude at least
one, and \(|a_q|=M|a_p|\). Polynomial construction size gives the last assertion. ∎

This establishes an arithmetic obstruction to extending the dimension-one
unit-weight picture. It does not yet quantify EC&R multipliers under a specified
normalization; large facet coefficients and large individual aggregation weights
are different statements. A multiplier lower bound needs that additional step.

The hull is an integral polytope when the network data are integral: first expand
the simplex into vertices, then decompose each network flow into integral network
vertices. Consequently the same statements apply if the original arc flows are
required to be integer before taking the convex hull. In the normalized
construction it is, more strongly, a **0/1 polytope**: each unit-flow vertex is a
single source-to-sink path, and each simplex vertex is \(0,e_1,e_2\). Thus the
coefficient obstruction comes from sparse joint convexification even with all
ambient numerical model data in \(\{0,1,-1\}\), rather than large capacities.

## 5. Limits and useful directions

The hull continues to have a polynomial-size extended formulation, so neither
membership nor separation is NP-hard as a consequence of this theorem. The
unbounded quantities are numerical coefficients, not their bit lengths. Nor is
there a superpolynomial extension-complexity claim.

The network has constant directed path length, but its underlying undirected
graph contains a large complete bipartite subgraph. This construction alone does
not settle restricted graph classes. The 2026-09-07 continuation supplies a
[rank-only coefficient bound](network-simplex-bounded-rank-hull.md), sharp at
rank three, and a separate [sparse Fibonacci obstruction](network-simplex-series-parallel-coefficient-growth.md)
showing superpolynomial coefficient magnitudes even on planar, treewidth-two,
directed series–parallel networks. The latter has growing simplex dimension;
the fixed-dimension restricted-graph boundary remains separate.

The present argument imports a deep classical universality theorem. Its novelty
claim must be limited to the explicit network–simplex realization and the
resulting original-space coefficient obstruction, subject to further literature
review. It is a structural answer to the general-m difficulty, not a complete
new facet classification.

In a process interpretation, \(x\) describes routing between supply and demand
nodes, and \(y\) is a common vector of two explicit fractions and a residual
fraction. Boundary and selected internal products describe component flows. Even
this shallow routing structure can require large coefficients in an exact
relaxation expressed only in the measured component-flow coordinates.

## 6. Verification

Besides the two independent proof audits linked above,
[the verification script](../code/common-factor-network-simplex-verify.py) compares
the projected transportation LP with a separately assembled convex combination
of every unit-flow path/simplex graph vertex. All 300 minimum/maximum support
comparisons on 150 random tables passed. This checks the embedding and unit-flow
normalization numerically. It does not implement the external universality
construction or enumerate the large-coefficient ambient facets.
