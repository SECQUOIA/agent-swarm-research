# Original-space separation and coefficient bounds at bounded block cycle rank

Status: independently reviewed theorem and complete proof, 2026-09-07;
[the independent audit](../notes/review-network-simplex-reopened-bounded-rank.md)
passed for both the general theorem and the later sharp K4 example. Author and
independent implementation checks are recorded below and in that report.
The normal-fan refinement and network-matrix
facts are classical. No general polynomial-separation novelty is claimed.

## 1. Statement and interpretation

Use the equality-constrained sparse network–simplex hull

\[
H=\operatorname{conv}\{(x,y,z):Ax=b,\ 0\le x\le u,\ y\ge0,
\mathbf1^Ty\le1,\ z_{ej}=x_e y_j\ ((e,j)\in O)\}.
\]

Capacities and balances are finite rational data. Let \(r_B\) be the cycle rank
of an undirected biconnected block and let \(r=\max_B r_B\), excluding bridges.
The number of blocks and the total cycle rank are unrestricted. Parallel arcs
are permitted; a self-loop is an independent rank-one block. A network with no
cycles needs only its flow, simplex, and fixed-flow observation equations.

**Theorem.** For each graph block, one can precompute finitely many local
feasibility certificates and support-dual bases. Their number and encoding length
are bounded by functions of \(r_B\) alone. After graph and observation grouping,
this gives the following properties.

1. Exact hull membership and a violated original-variable affine inequality, when
   one exists, require
   \[
   2^{O(r^2)}(|V|+|E|+m+|O|)
   \]
   rational arithmetic operations, including preprocessing. There is no LP solve
   in the online oracle. Ungrouped observations may additionally require
   \(O(|O|\log|O|)\) comparisons for sorting.
2. The hull has a finite affine-inequality description whose coefficients on
   **every flow and observed product variable are integers of magnitude at most**
   \[
   H_r=\max\{1,\lfloor(r-1)^{(r-1)/2}\rfloor\}.
   \]
   For \(r=1\), use \(H_1=1\). Thus the bound is one at ranks one and two,
   two at rank three, and five at rank four. Simplex coefficients retain the
   rational network data. This is a bound in the specified representative of
   each inequality, not a bound after clearing its rational simplex denominators.
3. Each block uses only its observed simplex-state labels and one merged residual
   state. Arithmetic work is linear in the number of such labels after the
   parameter-dependent library is fixed. Zero weights and lower-dimensional
   state polytopes are included.

The factor \(2^{O(r^2)}\) is large. The theorem supplies an explicit finite
original-space oracle and an arithmetic structural boundary, not evidence that
this implementation beats a compressed extended formulation. In particular,
rank-three blocks extend the prior cycle/theta result to new graph structures,
while the separate parallel-path theorem remains preferable for its graph class
at arbitrary rank.

The bound also applies blockwise: a block of rank \(r_B\) uses \(H_{r_B}\).
The common \(H_r\) is a convenient uniform bound.

## 2. Compressed state inequalities in cycle coordinates

Choose a reference vector \(v\) with \(Av=b\). An imbalance in a connected
component certifies emptiness. Choose a spanning tree in each cyclic block, with
its \(r_B\) chords as coordinate arcs. Its fundamental-cycle matrix \(C\),
with rows indexed by arcs, satisfies

\[
x_B=v_B+C\theta,\qquad C_{\text{chords}}=I.
\]

The matrix \(C\) is totally unimodular. To see this, delete a redundant incidence
row and partition the incidence matrix into tree and chord columns \([T,N]\).
Then \(C=[-T^{-1}N;I]\), up to row order and signs; \(T^{-1}N\) is a network
matrix and is totally unimodular. Appending identity rows and changing signs
preserves total unimodularity. In particular, every nonsingular square submatrix
has determinant \(\pm1\).

Let \(\mathcal A\) contain the distinct signed nonzero rows of \(C\), both signs
included. Write \(M\) for the matrix with these rows. It has rank \(r_B\), is
TU, includes \(\pm e_i\), and has at most \(3^{r_B}-1\) rows. All constraints
with the same row normal can be combined by taking the smallest right-hand side.

For each \(a\in\mathcal A\), precompute \(\beta_a\) so that the block domain is
\(P=\{\theta:a\theta\le\beta_a\ (a\in\mathcal A)\}\). Specifically, each arc
gives \(C_e\theta\le u_e-v_e\) and \(-C_e\theta\le v_e\); \(\beta_a\) is
the minimum of the corresponding constants. Bounded capacities make \(P\)
bounded. It may be empty or lower-dimensional.

For a block with observed labels \(J_B\), use \(\lambda_j=y_j\) for
\(j\in J_B\) and \(\lambda_*=1-\sum_{j\in J_B}y_j\). The state domain is

\[
Q_j=\{\theta:M\theta\le d_j\},\qquad
 d_{a,j}=\min\left\{\lambda_j\beta_a,
   z_{ej}-\lambda_jv_e:C_e=a,\ (e,j)\in O,
   -z_{ej}+\lambda_jv_e:-C_e=a,\ (e,j)\in O\right\}.
\tag{1}
\]

The residual state has no observations. Each displayed right-hand side is a
concave piecewise-affine function in the original variables. A repeated signed
normal is processed once per observation; state storage needs only
\(|\mathcal A|\) endpoint entries per retained state. At a zero weight, the base
constraints force \(\theta=0\), so any inconsistent observation makes \(Q_j\)
empty.

By simplex disaggregation and the independent circulation decomposition across
blocks, hull membership is equivalent to bridge equations together with

\[
Q_j\ne\varnothing\quad\text{for all retained states},\qquad
\bar\theta\in\sum_jQ_j\quad\text{in every block},
\tag{2}
\]

where \(\bar\theta_i=x_{e_i}-v_{e_i}\) uses the chord arcs. Unobserved states
merge because \(\sum_j\lambda_jP=(\sum_j\lambda_j)P\) for nonnegative weights
and nonempty convex \(P\). This follows from the earlier cycle/theta proof and
does not depend on its rank restriction. If \(P\) is empty, the original flow
constraints already have no solution.

## 3. Local feasibility certificates

Let \(\mathcal K\) contain one primitive generator of every extreme ray of

\[
K=\{q\ge0:M^Tq=0\}.
\]

Every such ray has inclusion-minimal support of size at most \(r_B+1\).
Its nonzero entries are all one: a minimal dependence among rows of a TU matrix
has nonzero coefficients in \(\{-1,1\}\), and here they must be positive.
This includes an opposite-normal pair. Enumerate subsets of size at most
\(r_B+1\), compute their nullspace, and retain exactly the one-dimensional
positive dependencies with minimal support. This takes parameter-only work.

Farkas' lemma gives

\[
Q_j\ne\varnothing\ \Longleftrightarrow\ q^Td_j\ge0
\quad(q\in\mathcal K).
\tag{3}
\]

The empty cone causes no difficulty, although the present centrally symmetric
normal set has opposite-pair certificates. For a failed test, choosing each
active minimum branch gives a globally valid affine inequality with the same
violation. Each observation belongs to one positive and one negative normal.
A local certificate using both opposite normals has only those two normals by
minimality. Hence a product coefficient is zero or \(\pm1\), including when the
same observation is chosen on both sides and cancels.

## 4. A common finite support set

Temporarily write \(s=r_B\). For every set of \(s-1\) independent rows of
\(M\), take the primitive integer null vector, with one chosen orientation.
Call the resulting deduplicated direction set \(\mathcal D\). At rank one,
use \(\mathcal D=\{1\}\). By the cofactor formula and TU,

\[
 d\in\{-1,0,1\}^s\setminus\{0\},\qquad
 Md\in\{-1,0,1\}^{|\mathcal A|}\quad(d\in\mathcal D).
\tag{4}
\]

For the second assertion, \(a^Td\) is, up to sign, the determinant obtained by
adding row \(a\) to the defining \((s-1)\)-row matrix. The cofactor vector is
already primitive because at least one nonzero cofactor is \(\pm1\).
The directions include every coordinate vector, since \(M\) includes the
identity rows, and \(|\mathcal D|\le(3^s-1)/2\).

Every one-dimensional face of every nonempty \(Q_j\) is parallel to a vector
in \(\mathcal D\). Indeed its active defining normals span dimension \(s-1\).
This statement remains true if \(Q_j\) is lower-dimensional: the constraints
tight throughout \(Q_j\) count among these normals. Points have no edges.

Form the central hyperplane arrangement \(d^Th=0\), \(d\in\mathcal D\), in
objective space. Its full-dimensional closed chambers are pointed because the
coordinate hyperplanes occur. Let \(\mathcal R\) contain both primitive
orientations of the null vector for every \(s-1\) independent directions from
\(\mathcal D\). At rank one, set \(\mathcal R=\{-1,1\}\).
Every extreme ray of every chamber belongs to \(\mathcal R\); keeping extra
such null vectors is harmless. The cofactor/Hadamard bound gives

\[
|h_i|\le H_s\quad(h\in\mathcal R).
\tag{5}
\]

**Support lemma.** For any collection of nonempty bounded polytopes with edge
directions in \(\mathcal D\),

\[
\bar\theta\in\sum_jQ_j
\quad\Longleftrightarrow\quad
h^T\bar\theta\le\sum_j\sigma_j(h)\quad(h\in\mathcal R),
\qquad \sigma_j(h)=\max_{\theta\in Q_j}h^T\theta.
\tag{6}
\]

Proof: within the interior of an arrangement chamber no edge is orthogonal to
an objective vector. A maximizing face of positive dimension has an edge, so
the maximizer in each summand is a unique vertex. Along a path within that
chamber the maximizing vertex cannot change without an intervening nonunique
maximizer. Therefore each support function is linear throughout the chamber,
and by continuity throughout its closure. This also covers point and segment
summands. The sum support is consequently linear there. Every vector in the
pointed chamber is a nonnegative combination of its extreme rays, so the ray
inequalities imply the support inequality for every objective vector. The usual
support characterization of a compact convex set finishes the proof.

Equivalently, this uses the classical fact that the zonotope generated by a set
covering all edge directions has a normal fan refining the polytope's normal fan.
The argument is included to make the treatment of degeneracies explicit.

## 5. Support formulas and bounded multipliers

For \(h\in\mathcal R\), let \(\mathcal B(h)\) contain every nonsingular
\(s\)-row submatrix \(B\) of \(M\) for which
\(q_B=B^{-T}h\ge0\). Extend \(q_B\) by zeros outside those rows. Because the
normal set contains both signs of each coordinate vector, this list is nonempty.
LP duality and the basic-feasible-solution theorem give, for nonempty \(Q_j\),

\[
\sigma_j(h)=\min_{B\in\mathcal B(h)}q_B^T d_{B,j}.
\tag{7}
\]

The dual feasible region is pointed because it is contained in a nonnegative
orthant. A finite attained optimum has an optimal basic solution. If its support
has fewer than \(s\) entries, extend the independent supporting rows to a basis;
the additional multipliers are zero. Thus (7) holds without primal
full-dimensionality or nondegeneracy assumptions.

A stronger bound than naive matrix multiplication is available:

\[
q_B\in\mathbb Z_+^s,\qquad (q_B)_i\le H_s.
\tag{8}
\]

To prove it, take independent directions \(d_1,\ldots,d_{s-1}\) whose primitive
orthogonal vector is \(h\). By (4), the vectors \(Bd_i\) are ternary. They
remain independent. Their primitive integer orthogonal vector is
\(B^{-T}h\), up to sign, because \(B\) is unimodular; unimodular maps preserve
primitive integer vectors. Cofactors and Hadamard therefore bound its entries
by \(H_s\). This proves (8), including bases whose row normals are not chord
normals. For rank one the assertion is immediate.

Equations (3), (6), and (7), with (1), are the announced complete original-space
hull. Each right-hand side in (7) is concave piecewise affine: the multipliers
are nonnegative. Expand a failed support inequality by choosing an active basis
and active endpoint branches separately in each state. The resulting affine
upper bound is globally valid and equals the support sum at the tested point.
It therefore separates that point exactly. Local failures use (3).

For the coefficient bound, a nonsingular basis cannot contain both \(a\) and
\(-a\). An observation therefore occurs at most once in each state's selected
support expression, with coefficient magnitude at most \(H_s\). Different
states use different observed-product coordinates. The aggregate side uses one
chord variable per component with coefficients \(h_i\), bounded by (5). Local
certificates have unit product coefficients as proved above. Original network,
simplex, and bridge constraints have unit flow/product coefficients. Together
these facts prove the stated finite-description bound. No restriction is claimed
for coefficients on \(y\), which include \(v\), \(\beta\), and residual weights.

## 6. Arithmetic and bit complexity

There are at most \(3^s-1\) distinct signed normals and
\((3^s-1)/2\) primitive directions. Enumerating their subsets of size at most
\(s+1\), all arrangement-ray candidates, and all dual bases therefore needs
\(2^{O(s^2)}\) operations and storage. Cofactor, rank, and sign computations
have parameter-bounded integer encoding length. The product of the number of
rays and bases is still \(2^{O(s^2)}\).

Fundamental cycles can be formed in \(O(r|E|)\) arithmetic/graph operations.
Repeated arc normals are combined once, and each observation updates two state
endpoint entries. Initializing a block's retained states, checking its circuits,
and evaluating all precomputed supports costs
\(2^{O(r_B^2)}(a_B+1)\), where \(a_B=|J_B|\). Because each retained explicit
block/state label has at least one observation,
\(\sum_B a_B\le|O|\). There are at most \(|E|\) blocks. Adding flow and simplex
checks proves the advertised arithmetic bound.

Online operations are affine evaluations with rational input constants,
comparisons, and additions with parameter-bounded integer multipliers. Their
bit lengths remain polynomial in the total rational input/candidate encoding
length and the parameter-dependent library encoding length. The arithmetic
bound is not a unit-cost claim for unbounded rational integers.

A convex decomposition exists by (2). This theorem does not claim the same
linear arithmetic bound for constructing one: the simplest construction solves
the small block/state extended feasibility systems and refines residual states.
That construction is polynomial and sparse, but a special direct constructive
oracle comparable to the rank-two result is a separate question.

## 7. Relation to existing results and practical scope

The exact general extended hull is already in Khademnia–Davarnia,
[*Convexification of Bilinear Terms over Network Polytopes*](https://arxiv.org/abs/2302.14151).
This result does not improve general separation tractability. Grouping states,
splitting blocks, and suppressing degree-two paths also give a compact extended
baseline; computational comparisons must include that baseline.

The normal-fan tool is classical. The earlier Gritzmann–Sturmfels,
*Minkowski Addition of Polytopes: Computational Complexity and Applications to
Gröbner Bases* (1993), gives the sum-fan refinement in Lemma 2.1.5, the edgotope
refinement in Proposition 2.1.8, and the edge-orthogonal arrangement algorithm
in Algorithm 2.3.6; see the
[local full text](../literature/papers/gritzmann1993-minkowski-addition-of-polytopes-computational/fulltext.md).
See also Onn–Rothblum,
[*Convex Combinatorial Optimization*](https://arxiv.org/abs/math/0309083), and
Onn–Rozenblit,
[*Convex Integer Optimization by Constantly Many Linear Counterparts*](https://arxiv.org/abs/1208.5639),
whose Lemma 2.1 states the edge-direction zonotope refinement. Network-flow edge
directions are treated by Onn–Rothblum–Tangir,
[*Edge-Directions of Standard Polyhedra with Applications to Network Flows*](https://doi.org/10.1007/s10898-004-4313-z).
The new candidate specialization is the complete sparse network–simplex
original-coordinate oracle and its **block-cycle-rank-only coefficient bound**,
including the unimodular change-of-basis argument (8). A targeted open search on
2026-09-07 found these classical foundations and the direct network–simplex
literature, but no matching block-rank statement. This is not proof of priority.

The coefficient result complements the unrestricted-network universality
obstruction: bounded block rank rules out its unbounded flow/product coefficient
ratios. It gives a concrete extension beyond cycle/theta blocks without asserting
that rank alone captures every useful class; arbitrary parallel-path blocks have
unit coefficients even at unbounded rank.

Potential practical use is strongest for repeated separation on a fixed small
block: precompute its modest actual direction/basis library and reuse it across
many candidates and sparse states. The worst-case universal library should not
be treated as a promising production implementation at moderate or large rank.
Benchmarking and independent verification remain required before that claim.

## 8. Sharpness already at rank three: a seven-observation K4 section

Status of this example: author and independent proof reviews passed, with
independent graph-level exact witnesses and LP checks. It shows that the
rank-three bound two cannot be replaced by one, even
with unit capacities and only seven observed products.

Take the acyclic orientation of \(K_4\) on \(0,1,2,3\), with each arc directed
from the smaller endpoint to the larger. Order the arcs as
\((12,13,23,01,02,03)\). Use unit capacities, reference flow
\(v_e=1/2\) on every arc, and balances \(b=Av\). The tree consists of
\(01,02,03\), and the chord-coordinate matrix is

\[
C=\begin{pmatrix}
1&0&0\\0&1&0\\0&0&1\\1&1&0\\-1&0&1\\0&-1&-1
\end{pmatrix}.
\]

Thus the coordinate domain is \(P=\{\theta:|C\theta|\le1/2\}\).
The example uses multiple supply/demand nodes; it is not asserted to be a
single-source/single-sink instance. It is a biconnected rank-three graph.

Use three explicit simplex coordinates, fixed to
\(y_1=y_2=y_3=1/4\), so the unobserved residual vertex also has weight \(1/4\).
Fix every aggregate flow coordinate by setting
\(\bar\theta=(1/8,0,1/8)\), equivalently

\[
\bar x=(5/8,1/2,5/8,5/8,1/2,3/8).
\]

Observe exactly

\[
O=\{(12,1),(13,1),(02,1),(12,2),(03,2),(23,3),(01,3)\}.
\]

Fix all observed products except \(U=z_{12,1}\) and \(V=z_{13,1}\) to \(1/8\).
Write \(p=U-1/8\), \(q=V-1/8\). In disaggregated cycle coordinates the first
three state polytopes are consequently

\[
\theta^1=(p,q,p),\qquad
\theta^2=t(0,1,-1),\quad |t|\le1/8,\qquad
\theta^3=s(1,-1,0),\quad |s|\le1/8,
\]

with the additional first-state bound \(|C(p,q,p)|\le1/8\). The residual state
satisfies \(|C\theta^*|\le1/8\), and all four states sum to \(\bar\theta\).

For \(h=(1,1,1)\), every residual state has \(h^T\theta^*\le1/4\): add its
constraints \(\theta^*_1\le1/8\) and
\(\theta^*_2+\theta^*_3\le1/8\). The second and third states have zero
\(h\)-value. Since \(h^T\bar\theta=1/4\), every feasible point in the section
therefore satisfies

\[
2p+q\ge0,\qquad\text{equivalently}\qquad
\boxed{2U+V\ge3/8.}
\tag{9}
\]

Conversely, assume \(|p|,|q|<1/32\) and put \(w=2p+q\ge0\). Choose

\[
t=-q/2,\qquad s=q/2,\qquad
\theta^*=(1/8-w/2,0,1/8-w/2).
\]

These four state vectors sum to \(\bar\theta\). The first state's bounds hold
because \(|p|,|q|<1/32\) and \(|p+q|<1/16\). The second and third states have
\(|t|,|s|<1/64\). Finally \(0\le w<3/32\), so the residual coordinates lie
between zero and \(1/8\) and meet every residual arc bound. This constructs a
feasible decomposition. Hence the coordinate section, in a neighborhood of
\((U,V)=(1/8,1/8)\), is **exactly the half-plane** (9).

The section has two-dimensional interior and a nontrivial boundary segment with
normal \((2,1)\). Restrict any finite linear description of the ambient hull to
this two-coordinate section. Its affine-hull equations restrict to identities,
and at an interior point of that segment at least one defining inequality must
restrict to its supporting line. Therefore every finite description requires
an inequality with product coefficient ratio two on \(U,V\), and the same
holds for a relative facet description. Unit product coefficients cannot give
a complete description. Together with the theorem, the rank-three bound two
is sharp. This argument concerns actual free product coordinates, so changing
flow-equation representatives cannot remove the ratio.

## 9. Implementation checks

The [verification script](../code/network-simplex-bounded-rank-verify.py) constructs
exact integer libraries for a cycle, theta, K4, and a rank-four wheel. It checks
every basis determinant/inverse, the ternary transformed-edge property, and the
claimed multiplier bound. Candidate formulas use exact rational arithmetic;
160 comparisons against independently assembled raw-state feasibility LPs all
passed, including zero weights, repeated observations, local inconsistency, and
aggregate-only violations. A further 218 exact primal-vertex/dual-support
comparisons passed. An additional 81-point local grid checks the sharp K4
section against the raw-state LP; all 43 accepted points also pass the explicit
exact rational decomposition checks. See the
[recorded output](../code/network-simplex-bounded-rank-verify-output.json).

The actual K4 library has seven edge directions, 18 support rays, 128 bases,
and 120 distinct sparse support duals summed over the rays. The wheel library
has 13 edge directions, 62 rays, 720 bases, and 1,034 sparse support duals.
These counts are more informative for small-block implementation than the
universal worst-case bound. This script tests specified fundamental-cycle
matrices, not graph extraction, and the external feasibility LP is numerical.

The direct Khademnia–Davarnia weight-two antecedent should be distinguished
from Section 8. Their Example 2 uses an eight-arc graph consisting of a four-cycle
with pendant arcs and balance inequalities; it exhibits a projection-cone
aggregation multiplier two. Section 8 uses equality balances on K4 and proves
a necessary ratio between actual free observed-product coordinates through a
coordinate-section boundary. The earlier example is an antecedent for weighted
cancellation, but does not by itself establish the rank-three sharpness claim.
