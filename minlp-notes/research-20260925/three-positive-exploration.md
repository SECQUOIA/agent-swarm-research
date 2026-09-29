# Sparse quadratic hulls: three-variable construction and a five-variable obstruction

Date: 2026-09-25. Status: research note; independent reviews linked below.

The main outcome is an exact three-variable counterexample resolving the stated
open question about a recent disjoint-support SDP relaxation. A quadratic with
positive square coefficients has true box minimum zero, while a rational point
satisfying every relaxation matrix strictly has value `−1/40`. The full proof,
moment table, and independent checks are in
[the counterexample note](three-positive-disjoint-counterexample.md).
Its parameterized extension yields
[one order-five SDP block for an infinite family of valid cuts](three-positive-family-sdp.md).
This formulation result is the constructive companion to the
counterexample; its completeness for the full hull is open.

There is also a structural boundary. Positive-variable components of size at most
three admit an explicit SDP lift by combining established constructions. At the
other end, a `K_5` minor in the graph on positive-square variables rules out
**every finite SDP lift** of the joint quadratic hull. A rational five-variable
Horn witness below gives a second failure mechanism for the disjoint-support
relaxation; it was found before the sharper three-variable witness.

These statements have different novelty levels. The three-variable lift
construction is a short combination of known results. The nonrepresentability theorem transfers
an established copositive-cone obstruction to sparse box quadratic hulls; its
minor construction and the explicit moment witness are the concrete additions
investigated here. The three-variable counterexample answers an explicit question
in the latest source examined. The completed
[publication assessment](publication-quadratic-assessment.md) records the
claim scope, current-source comparisons, targeted verification, and limits
of the priority evidence.

## 1. Definitions and scope

Let `G=(V,E,L^+,L^-)` be a graph whose diagonal coordinates have prescribed signs.
Define `H(G)` as the convex hull of points satisfying

\[
0\le x_i\le1,\qquad Y_{ij}=x_ix_j\quad(ij\in E),\qquad
Y_{ii}\ge x_i^2\quad(i\in P),\qquad
Y_{ii}\le x_i^2\quad(i\in M),
\]

where `P` and `M` are the positive- and negative-loop vertices, respectively.
There is no diagonal coordinate at other vertices. The complete graph with all
loops positive gives `H_n^+`. This is a joint hull in first moments, edge products,
and diagonal epigraph coordinates; it is not the epigraph of one fixed objective.

Write `K(G)` for the compact hull obtained by imposing equality at every existing
diagonal coordinate. Then

\[
H(G)=K(G)+D,
\]

where `D` consists of nonnegative positive-loop diagonal slacks and nonpositive
negative-loop diagonal slacks. This identity follows directly by taking convex
combinations. In particular, `H(G)` is closed: its first summand is compact and
its second summand is a closed cone.

## 2. What the current literature establishes

[Khajavirad, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2)
is still the latest listed version, dated 12 February 2026, when checked on
25 September. Her relaxation uses affine-square localizing matrices with
disjoint variable supports. Its exactness for the complete three-positive-loop
graph is left open in Section 3. Theorem 5 supplies an SDP hull when every
positive-vertex component has size at most two. Her polynomial-size claim
requires correction to its graph-width argument; see the
[independent treewidth audit](treewidth-elimination-review.md).

[Anstreicher and Burer, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf)
already give an exact SDP lift of the full three-variable box moment hull:
triangulate the cube and use complete positivity equals double nonnegativity
for matrices of order at most four. Thus finite SDP representability for a
three-variable quadratic box hull is not an open question.

[Bodirsky, Kummer and Thom, Corollary 3.18](https://content.ems.press/assets/public/full-texts/serials/jems/no-issue/14297974/online-first/10.4171-jems-1509-online-first.pdf)
prove that the copositive cone of order at least five is not a spectrahedral
shadow. The article appeared online in 2024 and in JEMS 28 (2026), 2233–2259.
Closed-cone duality, discussed in their Remark 3.17, gives the same conclusion
for the completely positive cone. This deep result is an external input below.

## 3. Exact lifts for components with at most three positive vertices

Let `C` range over the connected components of `G[P]`; put `R=V\P` and
`B_C=N(C)⊆R`. Let `T` be the graph on `R` containing the original edges within
`R`, with every `B_C` made a clique.

**Proposition 1.** If `|C|≤3` for every component, `H(G)` has a finite SDP lift.
Given a tree decomposition of `T` of width `τ`, an explicit lift has size

\[
O\!\left(|\mathcal B|2^{\tau+1}
 +\sum_C |C|!\,2^{|B_C|}\right),
\]

counting variables, affine constraints, and bounded-order matrix blocks, plus
the original coordinates. Counting every encoded nonzero coefficient can add
component-boundary factors. Here
`\mathcal B` is the supplied decomposition's bag family. All semidefinite blocks
have order at most four. This statement assumes the decomposition is supplied;
it does not assert that an optimal decomposition is computable in polynomial
time.

**Proof.** First, vertices in `R` can be made binary. Given a generating point,
round each such coordinate independently to a Bernoulli variable with its
original mean, keeping coordinates in `P` fixed. All first moments and edge
products are preserved. Negative-loop diagonal coordinates can be restored by
downward slack, since the rounded square has mean `x_i≥x_i²`. Positive-loop
diagonal coordinates are unaffected. The reverse inclusion holds because binary
points are allowed. It is therefore enough to describe mixtures of these points.

For a component with `k≤3` variables, triangulate `[0,1]^k` into the `k!` order
simplices. For each simplex let `V_π` be its `k×(k+1)` vertex matrix. Its
homogenized quadratic moment hull of mass `λ` is

\[
W_\pi\succeq0,\quad W_\pi\ge0\text{ entrywise},\quad
\lambda=\mathbf1^TW_\pi\mathbf1,
\quad m=V_\pi W_\pi\mathbf1,\quad
Z=V_\pi W_\pi V_\pi^T.
\]

Exactness follows from `CP_{k+1}=DNN_{k+1}`. Indeed, in a completely positive
decomposition `W=Σ_rr_rr_r^T`, normalize each nonzero `r_r` by its sum; its
squared sum is the atom's mass. Summing the simplex pieces gives the box hull.
Zero mass forces `W=0`, because all entries are nonnegative. Add the required
diagonal slack separately.

Use binary marginal tables on the bags of the decomposition of `T`, with
nonnegative entries, total mass one, and equality of adjacent separator
marginals. These tables admit a joint binary distribution: root the tree and
attach each child by its conditional distribution on the separator; zero-mass
separator states have no effect. This elementary construction proves the
required marginal consistency.

Every `B_C` is a clique and hence is contained in a bag. For every assignment
`b∈{0,1}^{B_C}`, attach a copy of the component's simplex formulation with total
mass equal to the marginal probability of `b`. Sum component moments across
these assignments. An edge from `i∈C` to `j∈B_C` has moment obtained by weighting
the conditional first moment of `i` by `b_j`; moments on `R` come from bag
tables. All original coordinates are linear projections of these variables.

For exactness in the reverse direction, start with the joint binary law on `R`.
Conditionally on each binary vector, sample the continuous components
independently from their distributions indexed by `b`. There are no edges
between distinct components. This law realizes every prescribed coordinate.
The size count follows from the number of tables and simplex copies. ∎

For finite representability alone, one may use one bag containing all of `R`.
Polynomial size follows when a supplied torso decomposition has logarithmic
width and the displayed total size is polynomial. It does **not** follow from
the uncorrected assertion that original treewidth and component-neighborhood
size separately logarithmic imply logarithmic torso width.

This construction concerns graph quadratic moments. It does not supply a
three-variable cubic moment, so it does not extend unchanged to a complete
hypergraph containing the product of all three continuous variables.

## 4. An obstruction to every finite SDP lift

Let

\[
\mathrm{CP}_r=\operatorname{cone}\{uu^T:u\in\mathbb R_+^r\},\qquad
\mathcal B_r=\{Z\in\mathrm{CP}_r:\mathbf1^TZ\mathbf1=1\}.
\]

The base `\mathcal B_r` is compact: its entries are nonnegative and sum to one.
It is the convex hull of `uu^T` over the probability simplex. To see this,
normalize each rank-one summand of a completely positive decomposition by the
sum of its vector's coordinates.

**Lemma 2.** A compact nonempty base `\mathcal B_r` has a finite SDP lift only
if `\mathrm{CP}_r` does.

**Proof.** Write a lift as
`Z∈\mathcal B_r ⇔ ∃w: A_0+A(Z)+D(w)⪰0`.
Homogenize it to

\[
t\ge0,\qquad tA_0+A(Z)+D(w)\succeq0.
\]

At positive `t` this projects onto positive multiples of the base. If a feasible
point with `t=0` had `Z≠0`, adding arbitrary nonnegative multiples of its lifted
direction to any feasible base lift would make `Z` a nonzero recession
direction of the compact base. This is impossible. The zero-mass fiber therefore
projects only to zero. The projection is exactly `cone(\mathcal B_r)=CP_r`. ∎

**Theorem 3.** If the graph `G[P]` contains a `K_5` minor, then `H(G)` is not a
spectrahedral shadow and has no finite SDP extended formulation.

**Proof.** Choose disjoint connected branch sets `C_1,…,C_5⊆P` witnessing the
minor, a spanning tree in each nonsingleton branch set, and one original edge
between each pair of branch sets. On `H(G)` the following affine expression is
nonnegative:

\[
F=\sum_{ij\text{ in the chosen trees}}(Y_{ii}+Y_{jj}-2Y_{ij}).
\]

At every generating atom its summands are `(x_i−x_j)²` plus the two nonnegative
diagonal slacks. Hence on the face `F=0`, atomwise the coordinates are equal
within each branch set, and the diagonal slack vanishes at every vertex of a
nonsingleton branch set. This follows for arbitrary face points by their finite
convex decompositions, because all summands are nonnegative.

Pick a representative `r_a∈C_a`. Set `u_a=x_{r_a}`, use `Y_{r_ar_a}` for `Z_aa`,
and use the selected interbranch edge for `Z_ab`. At each atom of the face,
`Z_ab=u_au_b` for `a≠b`, and `Z_aa≥u_a²`. Therefore the affine expression

\[
L=1-2\sum_{a=1}^5u_a+\sum_{a=1}^5Z_{aa}
       +2\sum_{1\le a<b\le5}Z_{ab}
\]

is nonnegative on that face. Its zero slice forces `Σ_au_a=1` at every atom
and kills any remaining representative diagonal slack, including at singleton
branch sets. Its `Z` projection is contained in `\mathcal B_5`.

Conversely every simplex vector `u` extends to an allowed generating point:
give every variable in `C_a` value `u_a`, put all outside variables at zero,
and set every available diagonal coordinate to its square. This point has
`F=L=0`. Mixtures show that the projected slice is exactly `\mathcal B_5`.

Affine sections and linear projections preserve finite SDP representability.
If `H(G)` had such a lift, `\mathcal B_5` would have one, then Lemma 2 would
give one for `CP_5`, contradicting the cited result of Bodirsky–Kummer–Thom and
closed-cone duality. ∎

In particular `H_n^+` has no finite SDP lift for `n≥5`. The theorem permits
arbitrarily long subdivisions of `K_5`, so the obstruction does not require a
five-vertex clique. For a small sparse example, the all-positive Petersen graph
has no finite SDP lift: contract its five spokes; the outer cycle supplies
distance-one edges and the inner star supplies distance-two edges, giving `K_5`.
This example has ten vertices and maximum degree three.
The theorem does not characterize all representable sparse hulls;
four-positive-variable components and other graphs without a `K_5` minor remain
outside these sufficient conditions.

## 5. A rational gap for the full disjoint-support relaxation

The nonrepresentability theorem does not by itself locate a gap in a particular
SDP. The following witness does so. Number five variables cyclically. Let `H`
have diagonal entries one, entry minus one on each edge of the five-cycle, and
entry plus one on each other off-diagonal position. Thus

\[
p(x)=x^THx=(\sum_ix_i)^2-4\sum_{i=1}^5x_ix_{i+1}.
\]

This classical Horn form is nonnegative on the nonnegative orthant. An elementary
proof normalizes `Σx=1`, then maximizes the cycle-edge sum. If two positive
coordinates are nonadjacent, transferring their combined mass to one or the
other leaves this sum affine in the transfer; an endpoint does not decrease it.
Iterating leaves support on a clique. A five-cycle has no triangle, so the
remaining edge product is at most `1/4`. The zero vector shows the box minimum
of `p` is zero. All five square coefficients are strictly positive.

Define a linear moment functional on squarefree monomials and monomials with
exactly one squared coordinate. Put `ε=10^{-6}` and

\[
y_S=\varepsilon^{|S|}\alpha_S,\qquad
\alpha_\varnothing=1,\quad \alpha_{\{i\}}=\tfrac1{10},\quad
\alpha_{\{i,j\}}=\begin{cases}13/20&ij\text{ is a cycle edge},\\1/10&\text{otherwise},\end{cases}
\quad\alpha_S=1\ (|S|\ge3),
\]

\[
y_{i^2}=\varepsilon^2,\qquad
y_{i^2S}=40\varepsilon^{|S|+2}
\quad(\varnothing\ne S\subseteq[5]\setminus\{i\}).
\]

There are 112 moments. For every partition `[5]=A⊔B⊔R`, impose

\[
M_{A,B,R}
=L_y\!\left[\prod_{a\in A}x_a\prod_{b\in B}(1-x_b)
          v_R(x)v_R(x)^T\right]\succeq0,
\qquad v_R=(1,(x_i)_{i\in R})^T.
\]

These are all 243 maximal disjoint-support localizing matrices, including the
32 scalar inequalities. They are the full `P=V, M=∅` relaxation, with no
omission of the high-degree diagonal moments.

**Proposition 4.** The moment assignment above makes every one of these matrices
positive definite, but `L_y(p)=−ε²/2=−1/(2·10^{12})<0`.

**Proof of feasibility.** Congruence-scale the constant row by one and each
variable row by `ε^{-1}`, and divide the matrix by `ε^{|A|}`. Its leading matrix
as `ε→0` is the same expression with all `(1−x_b)` factors omitted.

When `A=∅`, every leading matrix is a principal submatrix of

\[
\begin{pmatrix}1&\mathbf1^T/10\\\mathbf1/10&X\end{pmatrix},
\]

where `X` has diagonal one, cycle entries `13/20`, and other entries `1/10`.
The eigenvalue on the all-ones vector is `5/2`; the other eigenvalues are
`(25±11√5)/40`, each twice. The smaller one exceeds `1/100`, since
`√5<123/55`. On the constant/all-ones two-dimensional subspace, subtracting
`(1/100)I` leaves positive diagonal entries and determinant `24151/10000>0`.
Thus every such leading matrix exceeds `(1/100)I`.

When `A≠∅` and `R≠∅`, the leading matrix has form `[a,v^T;v,D]`, with
`D=39I+\mathbf1\mathbf1^T`. If `|A|=1`, `a=1/10` and `||v||²≤169/100`.
If `|A|=2`, `a≥1/10` and `||v||²≤3`. If `|A|≥3`, `a=1` and `||v||²≤2`.
Using
`2u v^Tw≥−(||v||²/35)u²−35||w||²`
shows that each leading matrix exceeds `(1/100)I`; the smallest bound needed is
`1/10−3/35=1/70>1/100`. If `R=∅`, its scalar leading value is at least `1/10`.

Every entry of the perturbation has magnitude at most
`40((1+ε)^5−1)<240ε`. Its matrix order is at most six, so its spectral norm is
less than `1440ε=0.00144<0.01`. All scaled matrices, and hence all original
matrices, remain positive definite.

Finally `L_y(p)=ε²(5−10·13/20+10·1/10)=−ε²/2`. ∎

This disproves full disjoint-support exactness in general with five positive
variables. By itself it does not decide the three- or four-variable cases;
the later three-variable counterexample is stronger in that respect. The small
absolute gap is an artifact of making a particularly simple rational witness
strictly feasible; no computational-performance claim is attached to it.

There is also a useful algebraic explanation. In any polynomial preordering
certificate for a homogeneous quadratic vanishing at the origin, the degree-two
part consists of an SOS quadratic plus nonnegative cross monomials. Terms with
one `x_i` factor have zero constant multiplier because the degree-one part must
vanish. Hence such a certificate for the Horn form would imply `H=S+N` with
`S⪰0` and `N` entrywise nonnegative. Its zeros `e_i+e_{i+1}` force `S` to
annihilate five linearly independent vectors, so `S=0`, contradicting the negative
cycle entries of `H`. Proposition 4 supplies the strict SDP gap directly,
without relying on a dual-attainment argument.

## 6. Three-variable counterexample and discovery limits

The stronger counterexample found later in this investigation is

\[
p(x,y,z)=x^2+y^2+9z^2+6xy-12xz-12yz-x-y+9z+\tfrac14.
\]

It is nonnegative on the cube and has five edge zeros. Its square coefficients
are strictly positive. The linked result note gives both a direct certificate
of nonnegativity and a zero-set proof excluding every disjoint-support affine-SOS
certificate. More decisively, its 20-entry rational moment table satisfies all
27 localizing matrices strictly and has `L_y(p)=−1/40`. Three independent
implementations checked the table, including the standard-library checker
`checks/three_positive_gap_certificate.py`. This is a strict primal relaxation
gap; no assumption about dual attainment is needed.

Two targeted randomized experiments compared all 27 three-variable localizing
matrices against exhaustive face-stationarity enumeration: 1,000 moderate-scale
instances and 20,000 logarithmically scaled instances, with strictly positive
diagonals and positive cross coefficients. Neither search found a gap above
`10^{-7}`. The subsequent exact counterexample shows why these searches could
not justify an exactness conjecture. Face enumeration solves every nonsingular free-coordinate stationarity
system and checks the box; random instances avoid singular systems with probability
one in an ideal continuous model. Some conic solves reported inaccurate status,
so those runs cannot establish exactness even for the sampled instances.

Section 6 of Khajavirad's v2 has a separate indexing mismatch: its total-degree
bound `deg(σf)≤d`, with `d≤n`, does not match the later admissibility test
`|A|+|B|+|R|≤d`. For example `x_i²x_jx_k` has degree four in the full
three-variable formulation. Our tests and counterexample use the explicit
localizing matrices above, not the inconsistent degree label. This issue does
not invalidate the validity of those matrices.

## 7. Verification and practical meaning

Targeted commands run:

```
python research-20260925/checks/three_positive_horn_certificate.py
python research-20260925/checks/three_positive_gap_certificate.py
```

The Horn exact rational checker verified strict positivity of every leading principal
minor of all 243 congruence-scaled matrices and the objective value
`−1/2000000000000`. Sylvester's criterion certifies the matrix claims. It does
not prove copositivity of the Horn matrix or the nonrepresentability theorem;
those require the arguments above and the cited external result. The
three-variable checker separately verified all 27 matrices and objective `−1/40`.

The discovery searches used the existing conic environment's Python interpreter
on the two search scripts under `checks/`; these are floating-point explorations,
not exact verifiers. No project-wide checks or CI checks were run.

Independent reviews:

- [Compact-base and copositive obstruction review](three-positive-cp5-review.md).
- [Horn witness and graph-minor review](three-positive-horn-minor-review.md).
- [Three-variable component construction review](three-positive-component-review.md).
- [Three-variable counterexample review](three-positive-disjoint-counterexample-review.md).

For solver design, the positive result supplies exact small-component blocks
coupled through binary marginal tables. The obstruction explains why increasing
the local SDP order cannot yield one finite exact formulation for every sparse
graph in this class. These are theoretical capabilities and limitations;
exploiting the small blocks in a global solver still requires a separation or
formulation strategy, numerical assessment, and attention to the size of the
binary separator tables.

The main unresolved research targets are completeness and useful separation of
the new three-variable family, finite SDP representability in the four-variable case, and sharper
graph conditions between components of size three and a positive `K_5` minor.
The present work does not establish a complete graph characterization.
