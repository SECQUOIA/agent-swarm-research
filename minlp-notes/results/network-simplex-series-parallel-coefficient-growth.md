# Exponential sparse-hull coefficients on series–parallel networks

Date: 2026-09-07. Status: [independently reviewed](../notes/review-network-simplex-reopened-series-parallel.md)
mathematical result; literature
priority remains provisional. The construction uses classical simplex
disaggregation, elementary linear algebra, and Fibonacci recurrences.
The [development note](../notes/network-simplex-reopened-series-parallel.md)
preserves a smaller coefficient-two example and the initial arbitrary-ratio
construction. No claim concerns separation hardness or extension complexity.

## 1. Statement and significance

Let

\[
H(G,O)=\operatorname{conv}\{(x,y,z):Ax=b,\ 0\le x\le\mathbf1,
\ y\ge0,\ \mathbf1^Ty\le1,\ z_{ej}=x_e y_j\ ((e,j)\in O)\},
\]

where \(A\) is the node–arc incidence matrix and \(b\) specifies unit flow
from one source to one sink. For every integer \(q\ge3\), there is an acyclic
directed two-terminal series–parallel network with \(2q\) vertices,
\(4q-1\) arcs, \(2q-1\) simplex coordinates, and \(5q-4\) observed
products, such that a facet of \(H(G,O)\), relative to its affine hull, has
coefficient ratio \(F_q\) on two observed product coordinates. Here
\(F_1=F_2=1\) and \(F_i=F_{i-1}+F_{i-2}\).

All capacities and the total flow are one. The ambient hull is a 0/1 polytope.
The underlying graph is planar and has treewidth two. The construction also
admits a simple graph of maximum degree three, with linear size and the same
number of observations. Thus no polynomial in the binary model description
length bounds all primitive integer facet-coefficient magnitudes on this class.

This rules out extending the complete unit flow/product coefficient description
of [parallel-path blocks](network-simplex-parallel-path-hull.md) to arbitrary
series–parallel blocks. It strengthens the earlier unrestricted-network
[coefficient obstruction](network-simplex-universality.md) by imposing treewidth
two, planarity, and a linear number of observations. The simplex dimension grows
with \(q\); unbounded growth at fixed simplex dimension on series–parallel
graphs is not established here.

## 2. An elementary incidence-to-section lemma

Let \(C\in\{0,1\}^{N\times N}\) be invertible, with every row nonempty
and proper. Suppose \(\alpha>0\) and \(\beta>0\) satisfy

\[
C^T\alpha=\beta\mathbf1.
\tag{1}
\]

Build a graph with vertices \(v_0,\ldots,v_N\), two parallel arcs
\(a_i,b_i:v_{i-1}\to v_i\) for each \(i=1,\ldots,N\), and one bypass
\(h:v_0\to v_N\). Use unit arc capacities and unit source-to-sink flow.
Use \(N\) explicit simplex states. For \(S_i=\{j:C_{ij}=1\}\), observe
exactly the cells \(z_{a_i,j}\) with \(j\notin S_i\).

Set \(a=1/(2N)\), \(c=a/4\), and fix a coordinate section by

\[
y_j=1/N,\quad x_h=1/2,\quad
x_{a_i}=|S_i|a+(N-|S_i|)c,\quad x_{b_i}=1/2-x_{a_i}.
\tag{2}
\]

Fix every observed product to \(c\), except one cell in row \(r\) and one
in a distinct row \(s\), denoted \(u,v\). The rows being proper guarantees
these cells exist. The section agrees locally at \((u,v)=(c,c)\) with

\[
\alpha_r(u-c)+\alpha_s(v-c)\ge0.
\tag{3}
\]

**Proof.** The known exact disaggregated hull has one state flow \(f^j\) of
value \(1/N=2a\) for each explicit state, summing to \(x\), with observed
entries equal to their product coordinates. The residual state has weight zero.
Conservation forces a common serial-branch throughput \(w_j\) in each state,
with \(0\le w_j\le2a\) and \(\sum_jw_j=1/2\).

Write \(\delta_r=u-c\), \(\delta_s=v-c\), and every other
\(\delta_i=0\). The total flow that gadget \(i\) can assign to its
unobserved states is at most \(\sum_{j\in S_i}w_j\). Therefore

\[
C(w-a\mathbf1)\ge-\delta.
\tag{4}
\]

Multiplying by \(\alpha^T\) proves necessity of (3).
For sufficiency let \(\tau\) be zero except at row \(s\), with

\[
\tau_s=\frac{\alpha^T\delta}{\alpha_s}\ge0,\qquad
d=C^{-1}(-\delta+\tau),\qquad w=a\mathbf1+d.
\tag{5}
\]

Equation (1) gives \(\beta\mathbf1^Td=\alpha^T(-\delta+\tau)=0\),
so \(\sum_jw_j=1/2\). In a sufficiently small open neighborhood of
\((u,v)=(c,c)\), every \(w_j\in(a/2,3a/2)\), every prescribed observed
cell lies in \((0,a/2)\), and \(\tau_s<a/2\).

In gadget \(i\), initially put \(w_j\) on \(a_i\) for states in
\(S_i\), and the prescribed observed value on \(a_i\) for states outside
\(S_i\). The aggregate is \(x_{a_i}+\tau_i\), by (4)–(5). In gadget
\(s\), reduce one allowed state's allocation by \(\tau_s\); its allocation
remains nonnegative. All resulting \(a_i\) entries lie between zero and
\(w_j\). Set \(f^j_{b_i}=w_j-f^j_{a_i}\), and \(f^j_h=2a-w_j\).
These state flows respect conservation, capacities, aggregate flows, and every
observed coordinate. This proves local sufficiency. ∎

The section is two-dimensional and has an open boundary segment on the line in
(3). Restrict any finite linear description of the ambient hull to this section.
Every affine-hull equation becomes an identity in \(u,v\). At a relative
interior point of the segment, some inequality must restrict to its supporting
line. Its two product coefficients consequently have ratio
\(\alpha_r/\alpha_s\). Applying this observation to a facet description
gives an ambient facet with that ratio. Adding affine-hull equations cannot
change these two coefficients, since their restrictions to this two-dimensional
coordinate section are zero.

## 3. A sparse Fibonacci construction

Use \(q\) primary row labels \(P_1,\ldots,P_q\) and \(q-1\) auxiliary
row labels \(H_0,H_3,\ldots,H_q\), so \(N=2q-1\). Define a square
0/1 matrix \(D\) by listing the incident rows of its columns:

\[
\{H_0,P_1\},\quad\{H_0,P_2\};
\tag{6}
\]

\[
\{H_i,P_i\},\quad\{H_i,P_{i-1},P_{i-2}\}
\quad(3\le i\le q);
\tag{7}
\]

and finally

\[
\{P_q,P_{q-1}\}.
\tag{8}
\]

Every row and column is nonempty and proper. Let \(\gamma=F_{q+1}\), and
give the rows positive weights

\[
\alpha_{P_i}=F_i,\quad \alpha_{H_0}=\gamma-1,\quad
\alpha_{H_i}=\gamma-F_i\quad(3\le i\le q).
\tag{9}
\]

Each column has weight \(\gamma\), so \(D^T\alpha=\gamma\mathbf1\).
The matrix \(D\) is invertible: if \(D^T\eta=0\), the first two columns
give \(\eta_{P_1}=\eta_{P_2}\), and subtracting each pair in (7) gives the
Fibonacci recurrence for the primary entries. The final column then forces
\(F_{q+1}\eta_{P_1}=0\); all primary and auxiliary entries are zero.

Apply the lemma to the complementary matrix \(C=\mathbf1\mathbf1^T-D\).
For \(\sigma=\mathbf1^T\alpha\), every proper column of \(D\) has
weight \(\gamma<\sigma\), so
\(C^T\alpha=(\sigma-\gamma)\mathbf1>0\).
This matrix is also invertible. Indeed \(C^T\eta=0\) implies
\(D^T\eta=(\mathbf1^T\eta)\mathbf1\), hence
\(\eta=(\mathbf1^T\eta)\alpha/\gamma\). Summing and using
\(\sigma\ne\gamma\) forces \(\eta=0\).

The observed products are precisely the incidences of \(D\), of which there
are \(4+5(q-2)+2=5q-4\). Take the free observed coordinate \(u\) in row
\(P_q\) and the final column (8), and \(v\) in row \(P_1\) and the first
column (6). Equation (3) becomes

\[
\boxed{\ F_q u+v\ge(F_q+1)c.\ }
\tag{10}
\]

Its boundary is an actual local section edge. The lemma's facet-restriction
argument proves the main coefficient-ratio assertion.

The graph has \(N+1=2q\) vertices and \(2N+1=4q-1\) arcs, with cycle
rank \(N+1=2q\). It is the parallel composition of one arc and a serial
chain of parallel pairs. Its unit-flow vertices are directed path incidence
vectors; combining these with the simplex vertices proves that the ambient
bilinear hull is a 0/1 polytope.

There are \(O(q)\) variables, constraints, and nonzero model coefficients,
and \(O(q\log q)\) binary description length under a sparse encoding.
Since \(F_q\) grows exponentially in \(q\), primitive integer facet
coefficients cannot have a polynomial magnitude bound in model description
length: a nonzero integer coefficient paired with ratio \(F_q\) forces another
coefficient of absolute value at least \(F_q\). All section data in (2) have
polynomially bounded numerators and denominators. Large coefficients arise from
sparse joint convexification, rather than large numerical network or section data.

## 4. Simple graphs of maximum degree three

The parallel arcs and degree-four joins are unnecessary. At each internal serial
join, split the vertex into an incoming vertex and an outgoing vertex connected
by one forward arc. Then subdivide every \(b_i\) arc once. The resulting
graph is simple, directed two-terminal series–parallel, and has maximum undirected
degree three. With \(N=2q-1\), it has \(3N=6q-3\) vertices and
\(4N=8q-4\) arcs. Its cycle rank remains \(N+1=2q\).

Give the new arcs unit capacities. Their flows are uniquely determined by the
old flows: a join arc carries the branch throughput, and both pieces of a
subdivided arc carry its original flow. These capacities are redundant for a
nonnegative acyclic unit flow. Observe the same \(5q-4\) products on the
unchanged \(a_i\) arcs. In the section fix the new join flows to \(1/2\)
and each subdivided flow to its old aggregate value. The state-flow argument and
the two free product coordinates are unchanged, so the same coefficient ratio
is necessary. This also gives the planar, treewidth-two claim without requiring
a multigraph convention.

## 5. Interpretation, literature, and verification

All gadgets share a hidden state-throughput vector. Enforcing each gadget's
transportation conditions separately after discarding that vector is insufficient.
Eliminating the profile can require unequal positive combinations of subset
constraints, even in a narrow serial network. This is a structural reason to
retain profile variables or allow richer inequalities in recursive formulations.

The exact disaggregated extended hull is already given in Appendix (25) of
[Khademnia–Davarnia](https://arxiv.org/abs/2302.14151), and in the earlier
[polytope–simplex convexification work](https://doi.org/10.1137/16M1066166).
The result here concerns facets in the sparse original coordinates, not a new
polynomial-time separation claim or an extension-complexity lower bound.

Almoghrabi, Skutella, and Warode's 2026
[*Integer and unsplittable multiflows in series-parallel digraphs*]
(https://link.springer.com/article/10.1007/s10107-026-02392-8) gives strong
feasibility and integrality results for total commodity flows. Its Remark 1
explicitly distinguishes total-flow integrality from integrality of the full
commodity-flow vector. Our construction prescribes selected commodity-specific
arc coordinates, and so lies outside a conclusion based only on total arc flows.
Targeted open-literature searches found no matching coefficient-growth result
for these sparse product coordinates; that is not a proof of priority.

The [verification script](../code/network_simplex_exploration/series_parallel_fibonacci.py)
checks incidence balances and nonsingularity exactly, 120 rational full-arc
state-flow witnesses through \(F_{14}=377\), 150 local membership comparisons
against a separately assembled full graph-state LP, and five LP support minima.
All checks passed. An independent reviewer additionally checked exact witnesses
through \(F_{30}=832040\) and used convex combinations of path–simplex vertices
as an independent LP formulation. These computations supplement the proof.

The number of simplex states grows with the construction. Fixed simplex dimension
on arbitrary nested series–parallel blocks remains open here. The theorem gives
superpolynomial numerical coefficient magnitudes, not superpolynomial coefficient
bit lengths, and does not change the known tractability of the extended hull.
