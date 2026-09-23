# Series–parallel blocks do not retain unit product coefficients

Date: 2026-09-07. Status: the initial family and the stronger sparse Fibonacci
family passed [independent review](review-network-simplex-reopened-series-parallel.md).
The strongest result is maintained in the
[standalone theorem](../results/network-simplex-series-parallel-coefficient-growth.md).
This development note retains the smaller examples and intermediate arguments.
The construction uses the known exact simplex disaggregation. Literature priority
remains provisional.

## 1. Main finding

The unit flow/product coefficient property of parallel-path blocks does **not**
extend to all series–parallel blocks. For every integer \(M\ge2\), a sparse
network–simplex hull on a directed two-terminal series–parallel graph has a facet
whose coefficients on two observed product coordinates have ratio \(M\).
All arc capacities and the total source-to-sink flow are one. The hull is a
0/1 polytope. The underlying graph is planar and has treewidth two.

The construction has \(M+2\) explicit simplex states, \(M+3\) vertices,
\(2M+5\) arcs, cycle rank \(M+3\), and \(1+M(M+1)\) observed products.
The simplex dimension grows with \(M\). This does not establish unbounded ratios
at fixed simplex dimension or superpolynomial coefficient growth in model size.
Those distinctions matter: the earlier universality construction establishes
stronger arithmetic growth and fixed simplex dimension, on a broader graph class.

The obstruction comes from coupling a shared state-throughput vector across
several serial routing choices. Each choice separately gives elementary subset
constraints; a fractional exact cover combines them with unequal multipliers.

## 2. Network and coordinate section

Set \(k=M+1\ge3\) and \(n=k+1\). Construct vertices
\(v_0,\ldots,v_{k+1}\). For each \(i=0,\ldots,k\), put two parallel arcs
\(a_i,b_i:v_i\to v_{i+1}\), and add a bypass arc
\(h:v_0\to v_{k+1}\). Give every arc capacity one and require unit
source-to-sink flow. This is the parallel composition of one arc and a serial
chain of two-arc parallel gadgets, hence is directed two-terminal series–parallel.
It is one biconnected block; its cycle rank is \(2k+3-(k+2)+1=k+2\).

Use \(n\) explicit simplex coordinates and fix every \(y_j=1/n\), so the
residual state has weight zero. Let

\[
a=\frac1{2n},\qquad c=\frac a4=\frac1{8n},\qquad p=na=\frac12.
\]

Define subsets of the explicit state labels by

\[
S_0=\{1,\ldots,k\},\qquad S_i=\{i,n\}\quad(1\le i\le k).
\]

Observe exactly the products \(z_{a_i,j}\) with \(j\notin S_i\).
There are no observed products on \(b_i\) or \(h\). Fix all aggregate flow
coordinates to

\[
x_h=1-p,\quad x_{a_0}=ka+c,\quad
x_{a_i}=2a+(k-1)c\ (i\ge1),\quad x_{b_i}=p-x_{a_i}.
\tag{1}
\]

Fix every observed product to \(c\), except the two coordinates

\[
u=z_{a_0,n},\qquad v=z_{a_1,2},
\tag{2}
\]

which remain free. The index \(2\notin S_1\) exists because \(k\ge3\).
All fixed numbers are rational, nonnegative, and satisfy aggregate conservation
and capacity constraints.

## 3. Necessary inequality with coefficient ratio \(M\)

The exact disaggregated hull has one state flow \(f^j\) of value
\(1/n=2a\) per state, with \(\sum_j f^j=x\) and every observed entry fixed
to its product coordinate. Let \(w_j\) be the state flow through the serial
branch. Conservation forces this to be the same at every gadget. Then

\[
0\le w_j\le2a,\qquad \sum_jw_j=p.
\tag{3}
\]

For each gadget, its allowed-state contribution to \(a_i\) cannot exceed
\(w(S_i)=\sum_{j\in S_i}w_j\). Consequently

\[
w(S_0)\ge ka+c-u,\qquad
w(S_1)\ge2a+c-v,\qquad
w(S_i)\ge2a\quad(2\le i\le k).
\tag{4}
\]

Each state belongs with multiplicity \(k\) to the collection that takes
\(k-1\) copies of \(S_0\) and one copy of each \(S_1,\ldots,S_k\).
Multiplying (4) accordingly yields

\[
kp\ge(k-1)(ka+c-u)+(2a+c-v)+(k-1)2a.
\]

Since \(p=(k+1)a\), this simplifies to

\[
\boxed{\ (k-1)u+v\ge kc.\ }
\tag{5}
\]

Thus every point in the coordinate section satisfies an inequality with the
claimed ratio. Necessity alone would not establish an ambient facet coefficient
claim; the next construction supplies the needed two-dimensional section edge.

## 4. Exact local sufficiency and a section edge

Write \(u=c+s\), \(v=c+t\). Take
\(\varepsilon=a/(8k)\) and restrict \(|s|,|t|<\varepsilon\).
Then the section is feasible **if and only if**

\[
D=(k-1)s+t\ge0.
\tag{6}
\]

Necessity is (5). For sufficiency set

\[
w_n=a+s,\quad w_1=a+(k-2)s,\quad
w_i=a-s\quad(2\le i\le k).
\tag{7}
\]

Their sum is \(p\). Each \(w_j\) lies strictly between zero and \(2a\):
in fact \(w_1\in(7a/8,9a/8)\), and every other \(w_j\) is closer to \(a\).
Construct state arc flows as follows:

- On gadget \(0\), set \(f^j_{a_0}=w_j\) for \(j\le k\), and
  \(f^n_{a_0}=u\).
- On every gadget \(i\ge2\), set \(f^j_{a_i}=w_j\) for \(j\in S_i\),
  and \(f^j_{a_i}=c\) otherwise.
- On gadget \(1\), use \(f^1_{a_1}=w_1-D\), \(f^n_{a_1}=w_n\),
  \(f^2_{a_1}=v\), and \(f^j_{a_1}=c\) for its remaining states.
- Set \(f^j_{b_i}=w_j-f^j_{a_i}\) and \(f^j_h=2a-w_j\).

The condition \(D\ge0\) gives \(f^1_{a_1}\le w_1\). Moreover
\(D<k\varepsilon=a/8\), so \(f^1_{a_1}>3a/4\). Every observed value
\(c,u,v\) is positive and less than its corresponding \(w_j\), since
\(c+\varepsilon<a/2\) whereas every \(w_j>7a/8\).
All state arc flows are therefore between zero and \(2a\), their scaled
capacities. They satisfy state conservation and have state value \(2a\).

The aggregate values of \(a_0\) and \(a_i\), \(i\ge2\), follow directly
from (7). On gadget 1 the allowed-state contribution is
\(w_1+w_n-D=2a-t\), and the observed contribution is
\((k-1)c+t\), giving exactly (1). The aggregate flows on \(b_i,h\) then
follow by subtraction. Every observed coordinate is respected. This proves
sufficiency using the full disaggregation, rather than only the subset tests.

The section therefore agrees locally at \((c,c)\) with a closed half-plane
having boundary (5). It is two-dimensional and contains an open segment of that
boundary. For any finite linear description of the ambient hull, affine-hull
equations restrict to identities in \((u,v)\), and an inequality must restrict
to the boundary line at its relative interior. Its two product coefficients have
ratio \(k-1=M\). Applying this to a facet description proves the main finding.
This is the same elementary facet-restriction argument used in the earlier
universality result; a triangular section is unnecessary.

Each original unit-flow vertex is an incidence vector of one directed path, and
each simplex vertex is zero or a coordinate vector. The ambient sparse hull is
therefore a 0/1 polytope despite the rational values used to define its section.
For any primitive integer facet representative with this ratio, one product
coefficient has magnitude at least \(M\). Adding affine-hull equations cannot
alter these two coefficients, since their restrictions to the full-dimensional
two-coordinate section are zero.

## 5. Small concrete example

For \(M=2\), take \(k=3\), \(n=4\), \(a=1/8\), \(c=1/32\).
There are four serial two-arc gadgets and one bypass; the graph has five vertices,
nine arcs, and cycle rank five. Fix each \(y_j=1/4\), bypass flow \(1/2\),
\(x_{a_0}=13/32\), and \(x_{a_i}=5/16\) for \(1\le i\le3\).
The complements of \(\{123\},\{14\},\{24\},\{34\}\) determine seven
observed products. Keep \(u=z_{a_0,4}\) and \(v=z_{a_1,2}\) free and fix
the other five to \(1/32\). The section edge is

\[
2u+v=3/32.
\]

This graph is a structural counterexample to extending the complete unit
coefficient description to arbitrary series–parallel networks. It does not show
that every facet is complicated, nor that exact separation is hard: the known
extended hull still gives polynomial-time separation.

## 6. What the failed composition argument teaches

For a single parallel-path block, disaggregated feasibility is one transportation
problem. Here each serial gadget gives a transportation problem conditional on
the **same vector** \(w\). Retaining only the scalar aggregate branch flow loses
necessary information. Eliminating the common profile produces weighted
combinations such as (5). Therefore a recursive algorithm for series–parallel
graphs must preserve sufficient state-profile information, or use richer cuts.

The new 2026 work of Almoghrabi, Skutella, and Warode,
[*Integer and unsplittable multiflows in series-parallel digraphs*]
(https://link.springer.com/article/10.1007/s10107-026-02392-8), proves strong
multiflow feasibility results under shared total capacities. Its model does not
prescribe selected commodity-specific arc coordinates. In this construction the
prescribed observed products are essential; ordinary multiflow cut sufficiency
does not dispose of these additional restrictions. A direct literature comparison
is still needed before asserting novelty.

## 7. Verification and open refinements

The companion script `code/network_simplex_exploration/series_parallel_obstruction.py`
assembles the original graph's full state-flow LP independently of (3)–(4),
checks the proposed section support, compares local section membership with (6),
and verifies the explicit witness using exact rational arithmetic. All 460 local
membership comparisons passed for ratios 2, 3, 4, 7, and 11: 256 feasible cases
also passed exact rational state-flow witness checks, and 204 were infeasible.
Five independent LP support minimizations attained the proposed section bound.
These computations supplement the proof and do not establish literature priority.
Independent reviewer findings will be added when available.

Two further directions are distinct from the established construction:

1. Find a smaller-rank or fixed-simplex-dimension series–parallel obstruction.
2. Replace the simple exact-cover family by sparse set systems with rapidly
   growing positive balancing multipliers, to obtain larger coefficient growth
   relative to graph size. Such a claim requires an explicit construction and
   cannot be inferred from the present linear-size-in-\(M\) family.

## 8. Stronger extension: exponential ratios from Fibonacci covers

Status: independently reviewed; the standalone result is now authoritative. This section
supersedes the second open direction above: an explicit family gives exponential
coefficient ratios using a polynomial-size directed series–parallel hull.

### 8.1 A general balanced-incidence lemma

Let \(A\in\{0,1\}^{N\times N}\) be invertible. Assume every row is
nonempty and proper, and that positive rational \(\alpha\in\mathbb R^N\)
and \(\beta>0\) satisfy

\[
A^T\alpha=\beta\mathbf1.
\tag{8}
\]

Use the same network with \(N\) serial two-arc gadgets inside one bypass,
\(N\) equally weighted explicit states, and row allowed sets
\(S_i=\{j:A_{ij}=1\}\). Set \(a=1/(2N)\), \(c=a/4\), \(p=1/2\).
Fix

\[
x_h=1/2,\quad x_{a_i}=|S_i|a+(N-|S_i|)c,
\quad x_{b_i}=p-x_{a_i},\quad y_j=1/N.
\tag{9}
\]

Observe all complementary cells and fix them to \(c\), except one cell in
row \(r\), denoted \(u\), and one cell in a distinct row \(s\), denoted
\(v\). The rows being proper guarantees that these cells exist. The section
agrees locally at \((u,v)=(c,c)\) with

\[
\alpha_r(u-c)+\alpha_s(v-c)\ge0.
\tag{10}
\]

**Proof.** Let \(\delta_r=u-c\), \(\delta_s=v-c\), and all other
\(\delta_i=0\). For any disaggregated point, its common branch profile
\(w\) satisfies \(\mathbf1^Tw=p\), and

\[
A(w-a\mathbf1)\ge-\delta.
\tag{11}
\]

Multiplication by \(\alpha^T\) gives necessity of (10).
For sufficiency let \(\tau\) be zero except at row \(s\), where

\[
\tau_s=\frac{\alpha^T\delta}{\alpha_s}\ge0,
\qquad d=A^{-1}(-\delta+\tau),\qquad w=a\mathbf1+d.
\tag{12}
\]

Equation (8) implies \(\beta\mathbf1^Td=\alpha^T(-\delta+\tau)=0\),
so the profile sums to \(p\). As \((u,v)\to(c,c)\), both \(d\) and
\(\tau\) tend to zero. Hence an open neighborhood exists in which every
\(w_j\in(a/2,3a/2)\), every observed cell lies in \((0,a/2)\), and
\(\tau_s<a/2\).

In every gadget initially allocate \(w_j\) to \(a_i\) for allowed states,
and its prescribed observation for complementary states. The row sum is then
\(x_{a_i}+\tau_i\), by (11)–(12). On gadget \(s\), reduce one allowed
state's allocation by \(\tau_s\), which is possible because its profile
entry is greater than \(a/2\). All \(a_i\) entries lie between zero and
\(w_j\); set \(b_i\) to the remainder and the bypass to \(2a-w_j\).
This is a valid disaggregation with all aggregate and observed coordinates
correct. Thus (10) is locally sufficient. The same section-edge argument as
before forces an ambient facet with product-coefficient ratio
\(\alpha_r/\alpha_s\). ∎

This lemma also identifies the precise missing profile information in a scalar
series–parallel composition. It is not a claim of arbitrary projection
universality: its hypotheses include a square invertible subset-incidence
matrix and a strictly positive balancing vector.

### 8.2 Explicit Fibonacci incidence matrices

For integer \(q\ge3\), create \(q\) primary row labels
\(P_1,\ldots,P_q\) and \(q-1\) auxiliary row labels
\(H_0,H_3,\ldots,H_q\). Thus \(N=2q-1\). Define the \(N\) columns
of \(A\) by listing their incident rows:

\[
\{H_0,P_1\},\quad \{H_0,P_2\},
\tag{13}
\]

\[
\{H_i,P_i\},\quad\{H_i,P_{i-1},P_{i-2}\}
\quad(3\le i\le q),
\tag{14}
\]

and the final column

\[
\{P_q,P_{q-1}\}.
\tag{15}
\]

Every row is nonempty and proper. Let \(F_1=F_2=1\),
\(F_i=F_{i-1}+F_{i-2}\). Give the rows weights

\[
\alpha_{P_i}=F_i,\quad \beta=F_{q+1},\quad
\alpha_{H_0}=\beta-1,\quad
\alpha_{H_i}=\beta-F_i\quad(3\le i\le q).
\tag{16}
\]

All weights are positive, and each column has total weight \(\beta\).
To prove invertibility, suppose \(A^T\eta=0\). The first two columns give
\(\eta_{P_1}=\eta_{P_2}\); subtracting each pair in (14) gives
\(\eta_{P_i}=\eta_{P_{i-1}}+\eta_{P_{i-2}}\). Hence
\(\eta_{P_i}=F_i\eta_{P_1}\). The final column gives
\(F_{q+1}\eta_{P_1}=0\), forcing all primary and then all auxiliary entries
to zero. Thus \(A\) is invertible.

To keep the observation set sparse, apply the lemma to the **complementary**
matrix \(B=\mathbf1\mathbf1^T-A\). Put \(\sigma=\mathbf1^T\alpha\).
Every column of \(A\) is proper, so \(\sigma>\beta\), and
\(B^T\alpha=(\sigma-\beta)\mathbf1>0\). The matrix \(B\) is invertible:
if \(B^T\eta=0\), then \(A^T\eta=(\mathbf1^T\eta)\mathbf1\), so
\(\eta=(\mathbf1^T\eta)\alpha/\beta\); summing forces
\(\mathbf1^T\eta=0\) because \(\sigma\ne\beta\), and then \(\eta=0\).
Every row of \(B\) is again nonempty and proper.

The observed cells are now exactly the incidences of \(A\). Take the free
coordinate \(u\) on row \(P_q\) and the final column (15), and \(v\) on row
\(P_1\) and the first column (13). The two free observed coordinates have a
section edge

\[
\boxed{\ F_q u+v=(F_q+1)c.\ }
\tag{17}
\]

An ambient facet must have coefficient ratio \(F_q\) on these two product
coordinates. The graph has \(N+1=2q\) vertices, \(2N+1=4q-1\) arcs, and
cycle rank \(N+1=2q\). There are only \(5q-4\) observations, the number of
incidences in (13)–(15). Thus the model has \(O(q)\) variables, constraints,
and nonzero coefficients, with \(O(q\log q)\) binary description length under
a sparse encoding of indices and numerical entries.
Its sparse bilinear model has binary description length polynomial in \(q\),
while \(F_q\) grows exponentially in \(q\). Consequently no polynomial in
that model description length bounds the numerical magnitude of all primitive
integer facet coefficients even on this directed series–parallel, unit-capacity,
unit-flow, 0/1-hull family. Coefficient **bit lengths** are not shown to grow
superpolynomially; there is no contradiction to the compact extended hull.

The number of explicit simplex states is \(2q-1\), so this stronger family
still leaves fixed simplex dimension open. All fixed section coordinates have
denominators and magnitudes bounded polynomially in \(q\); the large facet
ratio does not come from large numerical network or section data.

The companion script
`code/network_simplex_exploration/series_parallel_fibonacci.py` verifies the
incidence balances and nonsingularity exactly, checks 120 exact rational
original-arc flow witnesses through ratio 377, and compares 150 local points with
the independently assembled full graph-state LP (71 feasible, 79 infeasible).
Five LP support minima attain the asserted section bounds. All checks passed.

## 9. Why the flat-chain family cannot settle fixed simplex dimension

Status: independently reviewed; maintained in the
[standalone fixed-state theorem](../results/network-simplex-flat-chain-fixed-states.md).
This observation applies
to the unit source-to-sink network consisting of an arbitrarily long serial chain
of parallel **pairs** inside one bypass. It allows arbitrary sparse observations
on either arc of every pair and on the bypass. It is not a result for arbitrary
nested series–parallel networks or for arbitrary balance/capacity data.

For \(d=m+1\) simplex states, including the residual state, hull membership can
be reduced to a system in one shared branch profile \(w\in\mathbb R^d\).
Every coefficient row of this system is a signed 0/1 subset indicator. Every
right-hand-side coefficient on an original flow or observed product is in
\(\{-1,0,1\}\). Consequently the hull has a finite inequality description
whose flow/product coefficients have magnitudes at most

\[
(d+1)\Delta_d,
\tag{18}
\]

where \(\Delta_d\) is the largest absolute determinant of a square 0/1 matrix
of order at most \(d\) (and is at least one). This bound depends on simplex
dimension, not the number of gadgets. It does not assert that the description
has a small number of inequalities.

**Reduction.** Write \(\lambda\) for the \(d\) simplex-state weights.
The profile satisfies \(0\le w_j\le\lambda_j\) and
\(\mathbf1^Tw=1-x_h\). A bypass observation forces
\(w_j=\lambda_j-z_{h,j}\).
In one gadget, partition states into \(A\) (only arc \(a\) observed),
\(B\) (only arc \(b\) observed), \(T\) (both observed), and \(U\)
(neither observed). Denote the observed values by \(u_j=z_{a,j}\) and
\(v_j=z_{b,j}\). All observed values must be nonnegative. Require

\[
w_j\ge u_j\ (j\in A),\quad w_j\ge v_j\ (j\in B),\quad
w_j=u_j+v_j\ (j\in T).
\]

Set

\[
R=x_a-\sum_{j\in A\cup T}u_j+\sum_{j\in B}v_j.
\]

Conditional on \(w\), the remaining exact aggregate feasibility conditions are

\[
\sum_{j\in B}w_j\le R\le\sum_{j\in B\cup U}w_j.
\tag{19}
\]

Indeed the state arc-\(a\) values are fixed to \(u_j\) on \(A\cup T\),
fixed to \(w_j-v_j\) on \(B\), and range independently over
\([0,w_j]\) on \(U\). Their sum attains every value between the two
endpoints giving (19). Individual arc capacities are automatic from
\(0\le f^j_a,f^j_b\le w_j\le\lambda_j\). Once each gadget is filled,
its state flow joins consistently with every other gadget through the common
profile, and the bypass carries \(\lambda_j-w_j\). This proves exactness.

**Coefficient bound.** Express equalities by two inequalities to obtain
\(Lw\le r(x,y,z)\), where each row of \(L\) is a signed subset indicator.
The nonnegative Farkas cone \(\{\mu\ge0:L^T\mu=0\}\) is pointed. Every
extreme ray has a minimally dependent support of at most \(d+1\) rows. Its
primitive integer entries are, up to a common divisor, signed minors of order at
most \(d\). Changing signs of rows turns those minors into 0/1 determinants,
so every ray entry is at most \(\Delta_d\). A zero row contributes a singleton
ray with coefficient one. Farkas' lemma says that the corresponding inequalities
\(\mu^T r(x,y,z)\ge0\) describe the projection exactly. At most \(d+1\)
right-hand sides contribute, each with unit flow/product coefficients, proving
(18). Original flow/simplex inequalities and product nonnegativity also satisfy
the bound.

For example, \(m=2\) gives \(d=3\), \(\Delta_3=2\), and the conservative
uniform bound eight. This is not a sharp facet classification, but it rules out
unbounded coefficient growth in this flat topology at fixed simplex dimension.
The proof does not extend automatically to nested series–parallel graphs, where
several interacting profile vectors remain after local elimination. Determining
whether fixed simplex dimension controls coefficients for those larger graphs
remains a separate question.

**Original-space separation.** First check the original flow constraints,
capacities, simplex conditions, and observed-product nonnegativity. Then there
are at most \(2(2^d-1)+1\) distinct
signed subset rows, including the zero row. Group all copies of the same row by
their minimum right-hand side. For fixed \(d\), precompute all positive circuits
of the signed-subset row universe. Each circuit uses at most \(d+1\) rows, so
there are at most \(2^{O(d^2)}\) candidates; exact rational nullspace computations
identify the positive ones. At a tested point, evaluate each present row's tightest
right-hand side and every circuit supported on present rows. A negative circuit
sum is a separating inequality. Freeze the minimizing original row in each
participating group to recover an explicit original-space affine cut. Zero-row
violations are tested separately. If none fail, Farkas' lemma certifies membership.

Given \(L\) serial gadgets, constructing their rows takes
\(O(dL+|O|+m)\) arithmetic operations, followed by \(2^{O(d^2)}\)
parameter-only work. The construction needs no profile variables in the target
formulation. At fixed \(d\), a feasible profile can instead be recovered by
solving the grouped linear program with at most \(2^{d+1}\) constraints and
\(d\) unknowns, after which a greedy interval fill constructs every gadget's
state arc flows in \(O(dL)\) additional work. Rational encoding lengths remain
polynomial. This is a structural original-space specialization, not a new
general separation complexity claim.
