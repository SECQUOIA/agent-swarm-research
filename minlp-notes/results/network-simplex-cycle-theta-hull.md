# Exact sparse network–simplex hulls for cycle and theta blocks

Status: independently verified, 2026-09-04. Both [first audit](../notes/review-common-factor-network-positive.md)
and [second audit](../notes/review-network-positive-second.md) pass; the second
audit also checks the constructive decomposition corollary. The constituent
disaggregation and planar Minkowski-sum facts are classical. The proposed result
is their explicit sparse original-space network formulation and separation bound;
priority is not established.

## 1. Model and graph class

Let \(D\) be a directed graph, \(A\) its node–arc incidence matrix, and
\(\Xi=\{x:Ax=b,\ 0\le x\le u\}\), with finite rational capacities.
Consider

\[
H=\operatorname{conv}\{(x,y,z):x\in\Xi,\ y\in\mathbb R_+^m,
\mathbf1^Ty\le1,\ z_{ej}=x_e y_j\ ((e,j)\in O)\}.
\tag{1}
\]

Assume every biconnected block of the underlying undirected graph is a bridge,
a simple cycle, or a theta graph: three internally vertex-disjoint paths joining
the same two endpoints. Arbitrarily many such blocks may meet at articulation
vertices. Thus total cycle rank is unrestricted, while each block has at most two
independent cycles. Arc orientations are arbitrary. Parallel arcs are permitted
if blocks and paths are interpreted in the underlying multigraph; self-loops can
instead be treated as independent scalar cycle blocks.

The equality balance assumption is material. Replacing inequalities by slack arcs
can change the block structure, so the result must be applied to the resulting
graph, rather than assuming that it covers every network-inequality model.

## 2. Cycle coordinates and observed products

First obtain any reference vector \(v\) satisfying \(Av=b\), without requiring
its bounds. A spanning-forest solve gives it in linear arithmetic time; failure
of total balance on a connected component certifies an empty model.

The circulation space splits over the undirected blocks. In a cycle block there
is one coordinate \(s\); on each arc \(e\),
\(x_e=v_e+\epsilon_e s\) with \(\epsilon_e\in\{-1,1\}\).
Collecting its arc bounds gives a finite interval \([L_s,U_s]\).

In a theta block, orient all three paths conceptually from one endpoint to the
other. A circulation has constant signed deviations \(s,t,-s-t\) on the three
paths. Absorb the last minus sign and actual arc orientations into arc signs.
Every arc consequently has the form

\[
x_e=v_e+\epsilon_e h_e(s,t),\qquad
h_e\in\{s,t,d\},\quad d=s+t,\quad\epsilon_e\in\{-1,1\}.
\]

Its feasible coordinate polygon is

\[
P_B=\{(s,t):L_s\le s\le U_s,\ L_t\le t\le U_t,
L_d\le s+t\le U_d\}.
\tag{2}
\]

The constants follow by intersecting the signed arc intervals. Bridges have
\(x_e=v_e\). A circulation cannot transfer a net imbalance across an articulation
vertex between blocks, so these coordinate choices and bounds are independent
between blocks. Equivalently, the original flow polytope is an affine image of
the Cartesian product of these intervals and polygons, with bridge coordinates
fixed. This also provides a direct test for emptiness.

For a block \(B\), let \(J_B\) contain the simplex indices observed on at least
one arc of that block. Use one state for each \(j\in J_B\), with weight
\(\lambda_j=y_j\), and one additional state \(*\), with weight

\[
\lambda_*=1-\sum_{j\in J_B}y_j.
\tag{3}
\]

Thus all unobserved simplex states, including the original residual vertex, are
merged within this block. For each explicit observed state and every observation
on an arc with coordinate type \(h_e\), define the affine quantity

\[
q_{ej}=\epsilon_e(z_{ej}-y_jv_e).
\tag{4}
\]

In each state \(j\), initialize \(\ell_{h,j}=\lambda_j L_h\) and
\(u_{h,j}=\lambda_j U_h\). Intersect with all its observations of type \(h\):

\[
\ell_{h,j}=\max\bigl\{\lambda_jL_h,q_{ej}:h_e=h\bigr\},\qquad
u_{h,j}=\min\bigl\{\lambda_jU_h,q_{ej}:h_e=h\bigr\}.
\tag{5}
\]

The residual state has no observations. Repeated observations of the same signed
path coordinate are handled by these intersections. For bridges enforce the
original-space affine equalities \(z_{ej}=v_e y_j\).

## 3. Explicit state and aggregate inequalities

For a cycle block, every state must satisfy \(\ell_{s,j}\le u_{s,j}\), and the
aggregate coordinate \(s(x)\) must satisfy

\[
\sum_j\ell_{s,j}\le s(x)\le\sum_j u_{s,j}.
\tag{6}
\]

For a theta block, each state has a polygon

\[
Q_j=\{(s,t):\ell_{s,j}\le s\le u_{s,j},\
\ell_{t,j}\le t\le u_{t,j},\
\ell_{d,j}\le s+t\le u_{d,j}\}.
\]

Its exact nonemptiness conditions are the five inequalities

\[
\ell_{h,j}\le u_{h,j}\quad(h=s,t,d),\qquad
\ell_{s,j}+\ell_{t,j}\le u_{d,j},\qquad
\ell_{d,j}\le u_{s,j}+u_{t,j}.
\tag{7}
\]

When (7) holds, define its tight coordinate bounds

\[
\begin{array}{ll}
a_{s,j}=\max\{\ell_{s,j},\ell_{d,j}-u_{t,j}\},&
b_{s,j}=\min\{u_{s,j},u_{d,j}-\ell_{t,j}\},\\
a_{t,j}=\max\{\ell_{t,j},\ell_{d,j}-u_{s,j}\},&
b_{t,j}=\min\{u_{t,j},u_{d,j}-\ell_{s,j}\},\\
a_{d,j}=\max\{\ell_{d,j},\ell_{s,j}+\ell_{t,j}\},&
b_{d,j}=\min\{u_{d,j},u_{s,j}+u_{t,j}\}.
\end{array}
\tag{8}
\]

The six aggregate inequalities are

\[
\sum_j a_{h,j}\le h(s(x),t(x))\le\sum_j b_{h,j},
\qquad h=s,t,d.
\tag{9}
\]

Every sum in (6)–(9) uses the block's observed states and its single residual
state. It need not range over every simplex coordinate.

**Theorem.** A point belongs to (1) if and only if it satisfies the original linear
flow constraints, the simplex constraints, the bridge observation equalities,
every cycle state's \(\ell_{s,j}\le u_{s,j}\) together with (6), and (7)–(9)
for all theta blocks, using (3)–(5).
These conditions give an exact original-space description by sums of explicit
minima and maxima of affine expressions. They permit exact membership and linear
inequality separation with \(O(|V|+|E|+m+|O|)\) rational arithmetic operations,
given the block/path representation and observation indices grouped by block and
simplex state. Preprocessing the graph representation is linear time; sorting
ungrouped observation indices adds \(O(|O|\log|O|)\) comparisons if needed.

**Corollary (unit flow/product coefficients).** The same hull has a finite exact
linear inequality description in which every coefficient on a flow variable
\(x_e\) or an observed product \(z_{ej}\) belongs to \(\{-1,0,1\}\).
Coefficients on the simplex variables may depend on the network data. This is
an existence statement about an inequality family, and does not prescribe EC&R
aggregation multipliers or primitive integer scaling of its rational coefficients.

**Constructive corollary.** A rational hull point also admits a
rational convex decomposition using at most \(m+1\) graph points at the simplex
vertices. A shared block representation of this decomposition is computable in
the same linear arithmetic bound. Writing all dense flow vectors may require
\(\Theta(m|E|)\) output entries; the compact representation uses one default
coordinate per block and exceptions only for observed block/state pairs.

## 4. Proof

The standard simplex disaggregation says that hull membership is equivalent to
the existence of state flows \(f^j\in\lambda_j\Xi\) summing to \(x\), with
their observed entries equal to \(z_{ej}\). It follows by expanding every graph
point over the simplex vertices and, conversely, dividing every positive-weight
state flow by its weight. At weight zero the state flow is zero, since the flow
polytope is bounded. This argument is valid even though the chosen reference
\(v\) need not itself satisfy bounds.

In cycle coordinates, each state flow is
\(\lambda_jv+C\theta_j\). Since the weights sum to one, summing flows is exactly
summing their block coordinates to the aggregate block coordinates of \(x-v\).
Equations (4) and (5) express all observation and bound restrictions on these
state coordinates.

Merging unobserved states is exact. Their block polygons are scalar multiples of
the same convex polygon \(P_B\), so their Minkowski sum is
\((\sum_j\lambda_j)P_B\). Conversely, a point in this summed polygon splits
proportionally among the constituent weights. This operation can be performed
independently in each block and then assembled for every original simplex state;
the Cartesian-product decomposition guarantees that the resulting full flow is
feasible. The residual weight zero is harmless.

For intervals, membership in their Minkowski sum is exactly (6).
For a theta polygon, (7) states that the two individual coordinate intervals are
nonempty and that their attainable sum interval intersects
\([\ell_d,u_d]\). It is necessary and sufficient. Direct interval elimination
then gives (8); every displayed lower or upper bound is attained.

The edges of each nonempty polygon \(Q_j\) are parallel to one of the three
lines \(s=0,t=0,s+t=0\). A planar Minkowski sum has no new edge directions:
for any supporting normal, its maximizing face is the sum of the maximizing
faces of its summands. A one-dimensional face can therefore only use directions
already present in a summand. Thus \(\sum_jQ_j\) is described exactly by its
supports in the six normals \(\pm(1,0),\pm(0,1),\pm(1,1)\), which are the sums
in (8). The same argument covers segments and points: every segment direction
is among the three allowed directions, and its normal and endpoint bounds occur
among these six inequalities. This proves (9) and both directions of the theorem.

Each lower-bound expression in (5) and (8) is convex piecewise affine, and each
upper-bound expression is concave piecewise affine. Every condition is therefore
a family of valid linear inequalities in the original coordinates. When a
condition fails, choose active branches in its maxima and minima. The resulting
affine inequality is valid globally and has exactly the same violation at the
tested point. There is no differentiation or nonlinear optimization step.

For each block there is one residual state and at most as many explicit states
as observations on that block. Every state has a constant number of intervals
and support formulas. Aggregation over all blocks therefore uses only
\(O(|E|+|O|)\) state operations, in addition to checking the original flow and
simplex constraints. Rational bit lengths stay polynomial: the operations are
comparisons, additions, subtractions, and products of input data with candidate
coordinates; summing a linear number of rational terms has polynomial length.

To prove the corollary, expand all minima and maxima by choosing branches.
Each state contribution in (8) uses either one observation, or two observations
of different coordinate types. Different states have distinct observation
indices. Consequently an observed product occurs at most once in an aggregate
inequality, with coefficient \(1\) or \(-1\). A local state inequality combines
different types, or the same observation cancels between its lower and upper
bounds. The aggregate coordinates \(s(x),t(x)\) each use one reference arc with
sign \(\pm1\); \(d(x)=s(x)+t(x)\) uses two distinct reference arcs. The original
flow, bridge, and simplex inequalities also have the claimed coefficient form.
This proves the finite-description assertion. It contrasts with the
[unit-capacity universality obstruction](../results/network-simplex-universality.md)
for unrestricted network blocks, while making no statement about the number of
inequalities obtained by fully expanding all branches.

Here is a construction proving the last corollary. In a theta block, precompute
suffix sums of the six tight supports of its state polygons. If the remaining
aggregate coordinate is \(r\), then the next state coordinate must belong to
\(Q_i\cap(r-\sum_{j>i}Q_j)\). This intersection is another polygon of the same
form, with bounds

\[
\max\{\ell_{h,i},r_h-\sum_{j>i}b_{h,j}\}
\le h\le
\min\{u_{h,i},r_h-\sum_{j>i}a_{h,j}\},\qquad h=s,t,d.
\]

It is nonempty because the remaining aggregate belongs to the remaining
Minkowski sum. To choose a point in any nonempty such polygon, set
\(s=\max\{\ell_s,\ell_d-u_t\}\), then
\(t=\max\{\ell_t,\ell_d-s\}\). Formula (8) and feasibility show that both
upper bounds and the sum bounds hold. Subtract the chosen coordinate from \(r\)
and continue. Empty suffixes are the singleton \(\{0\}\), with all six supports
zero. Scalar cycle blocks use the analogous interval intersection.

Divide every positive-weight explicit block state by its weight. Divide a
positive-weight residual block coordinate by its merged weight; this normalized
coordinate is the shared default for every constituent unobserved state. A
zero-weight merged state is unused and can be assigned any feasible block
coordinate as its default. Refine the states and assemble blocks as in the proof
above. The resulting \(m+1\) potential graph points have weights
\(y_1,\ldots,y_m,1-\sum_jy_j\); omit the zero weights. There are at most
\(|O|\) exceptional block/state coordinates and one default per block, which
gives the claimed compact size and arithmetic construction bound.

## 5. Literature and scope

The disaggregated extended hull is already in Khademnia–Davarnia's
[network–simplex paper](https://arxiv.org/abs/2302.14151), Appendix (25), and in the
earlier general polytope–simplex work of Davarnia, Richard, and Tawarmalani,
[SIAM Journal on Optimization (2017)](https://doi.org/10.1137/16M1066166).
The present specialization eliminates the state flow variables explicitly.
It is not a new general polynomial-time separation theorem.

Searches on 2026-09-04 for network/simplex convexification with cactus, theta, and
cycle-rank structure found no direct result with this model and these formulas.
There is adjacent [Gupte–Kalinowski–Rigterink–Waterer work](https://arxiv.org/abs/1702.04813)
on bilinear functions over boxes whose *interaction graph* is a cactus. That graph
is different from the *flow constraint graph* here, and its domain is different.
No priority conclusion is drawn from this targeted search.

The graph class allows many independent routing loops, but it excludes general
series–parallel networks whose biconnected blocks have more than two cycles.
The reviewed [parallel-path extension](network-simplex-parallel-path-hull.md)
allows any number of internally disjoint paths in each block, replacing the
six-support linear oracle by classical transportation subset cuts and max-flow
separation. The 2026-09-07 [bounded-block-rank extension](network-simplex-bounded-rank-hull.md)
now gives an original-variable oracle and coefficient bounds at every fixed
rank, with a sharp necessary coefficient two on K4 at rank three. General
series–parallel blocks remain outside both earlier statements, and their unit
coefficient extension is ruled out by the [sparse Fibonacci construction](network-simplex-series-parallel-coefficient-growth.md).
Original-point bounds on the products, extra linking inequalities, or nonlinear
flow physics are not covered by simply intersecting this hull with those
restrictions. The valid inequalities remain usable as relaxations in such models.

## 6. Verification and a small joint-state obstruction

[The verification script](../code/common-factor-network-positive-verify.py) uses
exact rational arithmetic for (3)–(9), then compares feasibility with an independently
assembled LP retaining all original simplex states separately in every block.
All 400 comparisons passed: 193 feasible and 207 infeasible cases. They include
zero state weights, degenerate polygons, repeated observations, and several
blocks with different observed-state sets. Every accepted instance also passed
exact rational decomposition and refinement checks against all original,
unmerged state bounds, observations, and aggregate sums. The second reviewer also supplied an independent exact test,
[checking 400 sums of 1,860 state polygons](../code/audit-network-positive-decomposition.py),
including degenerate cases. These checks do not test graph block
extraction or replace the proof of the structural decomposition.

Even one theta block can require mixing information from several simplex states.
Take three parallel source-to-sink paths carrying unit total flow. Write the
first two path flows as \(s,t\), so \(s,t\ge0\) and \(s+t\le1\). Let the
aggregate be \(s=t=1/3\), let \(y_1=y_2=1/3\), and set all four observed
products \(sy_1,ty_1,sy_2,ty_2\) to zero. Each simplex coordinate separately
admits a valid one-coordinate hull decomposition, placing its state on the third
path. Both states cannot do that simultaneously because the aggregate third-path
flow is only \(1/3\). The violated joint inequality is

\[
z_{s1}+z_{t1}+z_{s2}+z_{t2}
\ge s+t-(1-y_1-y_2).
\]

The right side is \(1/3\), while the left side is zero. Formula (9) supplies this
inequality through the residual state's upper bound on \(s+t\). This example is
an illustration of known disaggregation logic, not a separate novelty claim.
