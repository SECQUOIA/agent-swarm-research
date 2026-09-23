# Beyond theta blocks: exact subset cuts for parallel-path blocks

Status: independently verified, 2026-09-04. Both the [first audit](../notes/review-common-factor-network-parallel-paths.md)
and [second audit](../notes/review-network-parallel-paths.md) pass.
The transportation feasibility and minimum-cut facts used here are classical.
The proposed application extends the explicit original-space hull and unit
flow/product coefficient property beyond the reviewed three-path result.
It is not a new general polynomial-time separation claim.

## 1. Structural extension

Use the equality-constrained sparse network–simplex model and reference vector
from [the cycle/theta theorem](../results/network-simplex-cycle-theta-hull.md).
Replace its block assumption by the following: each non-bridge block consists of
\(k\ge2\) internally vertex-disjoint paths joining two common terminal vertices.
The number \(k\), the number of blocks, and the simplex dimension are unrestricted.
The graph may therefore have arbitrarily large cycle rank within one block.
General series–parallel graphs need not have this block structure.

Orient the paths conceptually from the first terminal to the second. Their
circulation deviations \(\delta_i\) satisfy

\[
\sum_{i=1}^k\delta_i=0,\qquad L_i\le\delta_i\le U_i.
\tag{1}
\]

For every arc on path \(i\), \(x_e=v_e+\epsilon_e\delta_i\), with
\(\epsilon_e\in\{-1,1\}\). Bounds on the arcs determine \(L_i,U_i\).
Observations in state \(j\) specify
\(\delta_{ij}=\epsilon_e(z_{ej}-y_jv_e)\). Retain only states observed in this
block and one merged residual state, with the weights defined in the prior
theorem. The state's tightened path intervals are

\[
\ell_{ij}=\max\{\lambda_jL_i,\epsilon_e(z_{ej}-y_jv_e): e\text{ observed on path }i\},
\]
\[
u_{ij}=\min\{\lambda_jU_i,\epsilon_e(z_{ej}-y_jv_e): e\text{ observed on path }i\}.
\tag{2}
\]

For the merged state there are no observations. Its weight includes the original
residual simplex vertex and every explicit simplex state unobserved in the block.

Given aggregate deviations \(\bar\delta_i\) extracted from \(x-v\), exact block
membership is the existence of a matrix \(d=(d_{ij})\) with

\[
\ell_{ij}\le d_{ij}\le u_{ij},\qquad
\sum_i d_{ij}=0,\qquad \sum_jd_{ij}=\bar\delta_i.
\tag{3}
\]

This follows from the same simplex disaggregation and independent block gluing
as before. In particular, merging states remains exact: the unobserved state
domains are scaled copies of the same convex polytope (1).

## 2. Explicit original-space hull

Every state must satisfy

\[
\ell_{ij}\le u_{ij}\quad\forall i,j,\qquad
\sum_i\ell_{ij}\le0\le\sum_i u_{ij}\quad\forall j.
\tag{4}
\]

For every subset \(S\subseteq\{1,\ldots,k\}\), impose

\[
\boxed{\quad
\sum_{i\in S}\bar\delta_i
\le
\sum_j\min\left\{\sum_{i\in S}u_{ij},
-\sum_{i\notin S}\ell_{ij}\right\}.
\quad}
\tag{5}
\]

**Theorem.** The original linear flow and simplex conditions, bridge
observation equalities, and (4)–(5) for every parallel-path block describe the
exact sparse bilinear hull. In particular, the hull has a finite linear inequality
description in which all coefficients on \(x\) and \(z\) are in
\(\{-1,0,1\}\). The simplex coefficients retain the network data. This statement
does not constrain EC&R multipliers or primitive rescaling of rational coefficients.

**Proof.** Necessity of (4) is immediate. In any column of (3),

\[
\sum_{i\in S}d_{ij}\le\sum_{i\in S}u_{ij},\qquad
\sum_{i\in S}d_{ij}=-\sum_{i\notin S}d_{ij}
\le-\sum_{i\notin S}\ell_{ij},
\]

so (5) is necessary.

For sufficiency put

\[
g_{ij}=d_{ij}-\ell_{ij},\quad C_{ij}=u_{ij}-\ell_{ij},\quad
r_i=\bar\delta_i-\sum_j\ell_{ij},\quad c_j=-\sum_i\ell_{ij}.
\tag{6}
\]

Then (3) asks for a nonnegative capacitated transportation matrix with row sums
\(r_i\), column sums \(c_j\), and bounds \(g_{ij}\le C_{ij}\).
Conditions (4) give \(C,c\ge0\). The row sums are also nonnegative: (5) for
\(S=\{1,\ldots,k\}\setminus\{i\}\), and \(\sum_i\bar\delta_i=0\), yield

\[
-\bar\delta_i\le\sum_j\min\{\sum_{h\ne i}u_{hj},-\ell_{ij}\}
\le-\sum_j\ell_{ij}.
\]

Total row and column sums agree, again because the aggregate deviations sum to
zero. The standard bipartite flow network has source-to-row capacity \(r_i\),
row-to-column capacity \(C_{ij}\), and column-to-sink capacity \(c_j\).
For a fixed source-side set \(S\) of rows, minimizing a cut independently over
the side of each column gives cut capacity

\[
\sum_{i\notin S}r_i+
\sum_j\min\{\sum_{i\in S}C_{ij},c_j\}.
\]

Every such capacity is at least \(\sum_i r_i\) exactly when

\[
\sum_{i\in S}r_i\le\sum_j\min\{\sum_{i\in S}C_{ij},c_j\}.
\]

Adding \(\sum_{i\in S,j}\ell_{ij}\) converts this inequality into (5).
The classical [Ford–Fulkerson maximum-flow/minimum-cut theorem](https://www.cs.yale.edu/homes/lans/readings/routing/ford-max_flow-1956.pdf)
therefore supplies the matrix in (3).
Refine merged states and assemble the independent block coordinates to obtain a
full simplex-state flow decomposition. This proves sufficiency.

For the coefficient assertion, choose branches in every minimum and maximum in
(2), (4), and (5). Each state contribution in (5) selects either upper endpoints
from the paths in \(S\), or negated lower endpoints from the complementary paths.
Each observed product occurs at most once, because every observation has one path
and one state. Its coefficient is \(\pm1\). Local feasibility has the same
property, allowing cancellation of an identical observation. The aggregate left
side uses one signed representative arc from each path in \(S\), also without
repetition. These branches give the asserted complete inequality family. ∎

For \(k=3\), only six nonempty proper subsets occur; their supports are precisely
the six min/max formulas in the earlier theta theorem after eliminating
\(\delta_3=-\delta_1-\delta_2\). For arbitrary \(k\), (5) can contain
exponentially many inequalities, but separation avoids enumerating them.

## 3. Separation and construction

First check the original linear constraints, bridge equalities, and (4). If a row
sum \(r_i\) in (6) is negative, the valid inequality
\(\bar\delta_i\ge\sum_j\ell_{ij}\) separates the point; it is implied by (5).
Otherwise build the transportation network. A flow of value \(\sum_i r_i\)
certifies this block's membership and constructs its state coordinates. A smaller
maximum flow supplies a source-side row set whose cut violates (5).

As in the theta theorem, the right side of (5) is concave piecewise affine in the
original variables. Freeze the active alternatives in each minimum, and the
active affine endpoints in (2), to obtain a globally valid affine upper bound
with the same value at the tested point. This is an explicit violated linear
inequality in the original variables. Local violations similarly produce affine
cuts. No flow variables are added to the original formulation.

If a block has \(k_B\) paths and \(a_B\) observed simplex-state labels, the flow
network has \(k_B+a_B+3\) nodes and
\(k_B(a_B+1)+k_B+a_B+1\) arcs. Building all these networks takes

\[
O\left(|V|+|E|+m+|O|+\sum_B k_B(a_B+1)\right)
\]

arithmetic operations, followed by one standard capacitated maximum-flow solve
per block. Rational data have polynomial encoding length. This is polynomial
bit complexity using a polynomial-time rational max-flow implementation; it is
**not** the earlier linear arithmetic oracle when \(k_B\) is unbounded.

The returned matrices construct a convex decomposition at the simplex vertices.
Unobserved states again share one default path-coordinate vector per block, while
explicit states use the returned vectors. Compact storage is proportional to the
sum of the displayed transportation-network sizes; writing all full state flows
can still require \(\Theta(m|E|)\) entries.
Only positive state weights are divided when reconstructing graph points. A
zero-weight state has every deviation forced to zero by its scaled path bounds,
and can be omitted.

## 4. Novelty and remaining boundary

This extension is an application of classical capacitated transportation
feasibility, also treated in [Ford–Fulkerson's transportation paper](https://doi.org/10.1287/mnsc.3.1.24).
Its potentially useful statement is that **arbitrary parallel-path
blocks retain a complete unit flow/product coefficient hull description**, even
with arbitrary simplex dimension, sparse observations, and unbounded cycle rank
within a block. The general sparse network hull is already known to have a
polynomial extended formulation. No new complexity class conclusion is claimed.

The larger class of all series–parallel networks is not covered. A serial chain
of parallel gadgets inside an outer parallel branch produces shared internal
state-flow profiles between different gadgets, which need not reduce to one
transportation matrix. The 2026-09-07 [series–parallel coefficient theorem](network-simplex-series-parallel-coefficient-growth.md)
turns this issue into an explicit obstruction: even unit-capacity and unit-flow
networks require superpolynomial product-facet coefficient magnitudes as the
number of observed simplex states grows. Thus the unit-coefficient conclusion
cannot extend to that larger class.

[The verification script](../code/common-factor-parallel-paths-verify.py) compares
the full subset family evaluated with exact rational arithmetic with an
independently assembled bounded-matrix feasibility LP. All 300 instances passed
(207 feasible, 93 infeasible); the independent reviewer reran this check.
The numerical LP comparisons do not test graph preprocessing or a max-flow
implementation and do not establish literature priority.
