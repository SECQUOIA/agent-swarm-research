# Sphere submersions force a strict curvature-capacity gap

Status: Proved; primary-source-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Main result

Let \(C\subset\mathbb R^{n+1}\) be a compact full-dimensional convex body
with \(0\in\operatorname{int}C\). Assume that both
\[
               P=\partial C,\qquad D=\partial C^\circ
\]
are \(C^1\) strictly convex hypersurfaces; in particular,
\(P,D\cong S^n\). Suppose the full slack operator has globally labelled
\(C^1\) factors over proper cones \(K_i\):

\[
 s(x,z)=1-\langle x,z\rangle
       =\sum_i\langle A_i(x),B_i(z)\rangle,
 \qquad A_i(x)\in K_i,\quad B_i(z)\in K_i^* .                 \tag{1}
\]

Write

\[
                 c_i=(\dim K_i-2)_+,
 \qquad S=\sum_i c_i,
 \qquad k_+=|\{i:c_i>0\}|.                                  \tag{2}
\]

The local mixed-rank argument gives \(S\geq n\). The new global
conclusion is:

\[
 \boxed{
 S=n\quad\Longrightarrow\quad
 \text{exactly one positive-capacity block, with }c_i=n.}    \tag{3}
\]

Equivalently, every globally \(C^1\) factorization having at least two
positive-capacity blocks,
and every factorization whose positive blocks all have \(c_i<n\), obeys the
strict integer gap

\[
                              S\geq n+1.                       \tag{4}
\]

This closes the exceptional sphere dimensions left by tangent-bundle
splitting alone. The shortest proof is joint: the maps induced by all
saturated blocks assemble into a same-dimensional local diffeomorphism
from \(S^n\) to a product of their target spheres. Covering-space theory
and cohomology then force that product to have one factor. The argument has
no exceptional Hopf dimensions.

Section 2 retains the stronger classical Browder--Serre classification of
an *individual* sphere-to-sphere submersion. It supplies an independent
blockwise proof but is no longer needed for the saturated-collection
theorem. No classification of maps up to bundle equivalence is claimed.

The primal and polar contact spheres use independent charts. No
differentiable Gauss identification and no positive-curvature assumption
is required.

This note records the individual Browder--Serre theorem and the exact
cap-dependent frontier. The more general joint-covering theorem is
[Joint saturation forces a covering by sphere factors](2026-09-04-joint-saturated-block-covering-rigidity.md).
The companion
[saturated-factor submersion note](2026-09-04-saturated-factor-submersion-obstruction.md)
is the independently audited low-regularity bridge and rank-one stepping
stone. The
[saturated-block reconstruction](2026-09-04-saturated-block-submersion-rigidity.md)
is an independent proof of that bridge; its headline conclusions are
subsumed here.

## 1. The factor-to-submersion lemma

The detailed low-regularity proof is in
[Saturated cone factors force sphere-to-sphere submersions](2026-09-04-saturated-factor-submersion-obstruction.md).
The essential argument is recorded here to make the present theorem
self-contained.

At a contact pair \((x,z)\in P\times D\), so
\(\langle x,z\rangle=1\), define

\[
 M_i(x,z)=-dA_i(x)^*dB_i(z):
 T_xP\longrightarrow T_z^*D.                                 \tag{5}
\]

Since \(z\) and \(x\) are the supporting normals at the two \(C^1\)
boundaries,

\[
                         T_xP=z^\perp,\qquad T_zD=x^\perp.
\]

The Euclidean pairing between these two tangent spaces is nondegenerate:
if \(v\in z^\perp\) annihilates \(x^\perp\), then
\(v\in\operatorname{span}x\); but
\(\operatorname{span}x\cap z^\perp=\{0\}\) because
\(\langle x,z\rangle=1\). Mixed differentiation of (1) therefore gives a
rank-\(n\) contact pairing

\[
 \sum_i M_i(x,z)(v,w)=\langle v,w\rangle=:G_{x,z}(v,w)
 \quad(v\in T_xP,\ w\in T_zD).                               \tag{6}
\]

Each channel has rank at most \(c_i\). If \(S=n\), then

\[
 n=\operatorname{rank}G_{x,z}
 \leq\sum_i\operatorname{rank}M_i(x,z)
 \leq\sum_i c_i=n,
\]

so

\[
                       \operatorname{rank}M_i(x,z)=c_i        \tag{7}
\]

for every \(i\) and every contact pair \((x,z)\).

Fix \(i\) with \(c=c_i>0\), put \(m=\dim K_i=c+2\), and abbreviate

\[
 a=A_i(x),\quad b=B_i(z),\quad X=dA_i(x),\quad Y=dB_i(z).
\]

Positive channel rank rules out \(a=0\) and \(b=0\). Indeed, the derivative
of a two-sided \(C^1\) curve in a pointed cone through its vertex belongs to
both the cone and its negative, and is therefore zero. Nonnegativity of
each cone pairing and its zero value on the contact diagonal give, by
holding one variable fixed,

\[
 X(T_xP)\subset b^\perp,
 \qquad
 Y(T_zD)\subset a^\perp.                                     \tag{8}
\]

Thus \(M_i\) factors through the nondegenerately paired \(c\)-dimensional
quotients

\[
 b^\perp/\mathbb Ra,
 \qquad
 a^\perp/\mathbb Rb.                                         \tag{9}
\]

Equation (7) forces the first quotient map

\[
 \overline X:T_xP\longrightarrow b^\perp/\mathbb Ra
\]

to have rank \(c\).

Choose \(\ell\in\operatorname{int}K_i^*\), let

\[
 \Delta=K_i\cap\{\ell=1\},\qquad J=\partial\Delta,
 \qquad p_i(x)={A_i(x)\over\ell(A_i(x))}.                     \tag{10}
\]

The base \(\Delta\) is a compact convex body of affine dimension \(c+1\), and
\(J\) is topologically \(S^c\). Direct differentiation shows

\[
 dp_i(x)u=0
 \quad\Longleftrightarrow\quad
 Xu\in\mathbb Ra
 \quad\Longleftrightarrow\quad
 \overline Xu=0.                                              \tag{11}
\]

Hence \(dp_i\) has rank \(c\) everywhere. The constant-rank theorem and
invariance of domain show that \(p_i(P)\) is relatively open in
\(J\); it is also compact and therefore closed. Since \(J\) is connected,
\(p_i(P)=J\). The regular image patches make \(J\) an embedded
\(C^1\) hypersurface. Radial projection from an interior point is then a \(C^1\)
diffeomorphism \(J\cong S^c\): the radial direction is transverse to every
supporting tangent hyperplane. Consequently every positive saturated block
induces a \(C^1\) submersion

\[
                              S^n\longrightarrow S^{c_i}.     \tag{12}
\]

This bridge needs only \(C^1\) factor selections and no a priori
smoothness of the cone boundary. The rank-one target \(S^1\) can already be
excluded at \(C^1\) regularity by lifting the map to a real-valued function
on simply connected \(S^n\) and taking an extremum. For general rank, use
standard \(C^1\) smoothing:
surjectivity of the derivative is open and uniform on the compact source,
so a sufficiently close smooth approximation remains a submersion and is
automatically onto.

## 2. Exact dimension pairs for sphere submersions

### Theorem (Browder--Serre corollary)

Let \(1\leq r<n\). A \(C^1\) submersion

\[
                              f:S^n\longrightarrow S^r        \tag{13}
\]

exists if and only if

\[
                         (n,r)\in\{(3,2),(7,4),(15,8)\}.       \tag{14}
\]

The three positive cases are the classical complex, quaternionic, and
octonionic Hopf maps.

### Proof

For \(r=1\), \(n\geq2\) and \(S^n\) is simply connected. The map lifts
through \(\mathbb R\to S^1\) to a \(C^1\) real-valued function on \(S^n\).
At an extremum its derivative vanishes, contradicting submersivity.

Suppose \(r\geq2\). Smooth \(f\), if necessary, as described above.
Because the source is compact, \(f\) is proper, so Ehresmann's theorem
makes it a locally trivial smooth fiber bundle

\[
                         F\longrightarrow S^n\longrightarrow S^r.          \tag{15}
\]

The fiber is connected: the base is simply connected and the total space
is connected, so the homotopy exact sequence on components leaves only one
fiber component.

Browder's Theorem 1 states that the connected fiber of a fiber bundle whose
total space is a sphere has the homotopy type of \(S^d\) with

\[
                              d\in\{1,3,7\}.                   \tag{16}
\]

Here \(F\) is also a closed manifold of geometric dimension \(n-r\).
Mod-two Poincare duality gives \(H_{n-r}(F;\mathbb F_2)\neq0\), so its
geometric dimension equals the homotopy-sphere dimension \(d\).

It remains to determine \(r\). In the mod-two cohomological Serre spectral
sequence of (15), the only nonzero rows are \(q=0,d\), and the only nonzero
columns are \(p=0,r\). Since the total-space cohomology has no classes in
the two intermediate degrees, the fiber and base generators must cancel.
The only possible differential is

\[
 d_r:E_r^{0,d}\longrightarrow E_r^{r,d-r+1}.
\]

Its target must be \(E_r^{r,0}\), which forces

\[
                              r=d+1.                           \tag{17}
\]

Therefore \(n=r+d=2d+1\), and (16) gives exactly (14). Conversely, the
three Hopf maps are smooth submersions. This proves the theorem.

## 3. Joint covering rigidity of a saturated rank profile

Let \(p_i:S^n\to S^{c_i}\) be the maps in (12). If a tangent vector \(v\)
lies in every \(\ker dp_i\), then (11) makes every \(dA_i(v)\) radial.
At a contact point, differentiating
\(\langle A_i(x),B_i(z)\rangle=0\) in the polar tangent direction shows
that a radial first derivative annihilates the entire mixed channel.
Zero-capacity channels already have rank zero. Thus
\(M_i(v,\cdot)=0\) for every block, and (6) forces \(v=0\).

Consequently the product map

\[
       p=(p_i):S^n\longrightarrow\prod_{i:c_i>0}S^{c_i}     \tag{18}
\]

has injective derivative. Its source and target both have dimension \(n\),
so it is a local diffeomorphism and, by compactness, a finite covering.
A capacity-one factor is impossible because a submersion
\(S^n\to S^1\) lifts to a real function and has a critical point. All
target factors are therefore simply connected, so (18) is a
diffeomorphism. A product of at least two positive-dimensional spheres has
nonzero cohomology below its top degree, whereas \(S^n\) does not. Hence
the product has exactly one factor, of dimension \(n\), proving (3).

This elementary joint argument supersedes the older arithmetic use of
(14). The individual Browder--Serre theorem remains useful when the maps
are not known to form a saturated full-rank collection.

## 4. Strict block, dimension, and barrier consequences

Write the body dimension as \(N=n+1\). If every positive block has
\(c_i<n\), then (4) gives

\[
                              \sum_i c_i\geq N.                \tag{19}
\]

For \(k_+\) positive blocks, their ambient cone dimension is exactly

\[
                  M_+=\sum_{i:c_i>0}\dim K_i
                      =\sum_{i:c_i>0}c_i+2k_+,
\]

and hence

\[
                              M_+\geq N+2k_+.                  \tag{20}
\]

For uniform \(m\)-dimensional blocks with \(m-2<n\),

\[
                  k\geq\left\lceil{N\over m-2}\right\rceil,
 \qquad
                  M=mk\geq
                  m\left\lceil{N\over m-2}\right\rceil.     \tag{21}
\]

In particular, \(m=3\) gives

\[
                         k\geq N,\qquad M\geq3N.              \tag{22}
\]

For Lorentz factors \(Q_3^k\), every possibly coupled logarithmically
homogeneous self-concordant barrier on the full ambient product has
\(\nu\geq2k\): restrict it to the product of the two-dimensional orthant
sections of the factors. The standard product barrier attains \(2k\).
Thus (22) gives the sharp smooth-selection ambient-product costs

\[
                         k\geq N,qquad M\geq3N,
                         \qquad \nu\geq2N.                    \tag{23}
\]

The explicit coordinate-square \(Q_3^N\) construction attains all three
bounds; see
[A globally smooth exact \(Q_3^N\) factorization of the Euclidean ball](2026-09-04-smooth-q3n-ball-factorization.md).

These are regularity-conditioned factorization and ambient-product barrier
bounds. They do not rule out nonsmooth norm-tree lifts, do not say that an
arbitrary cone lift automatically supplies global factor selections, and
do not lower-bound a barrier defined only on the affine feasible slice.

## 5. Exact cone-product frontier under every block-dimension cap

For the Euclidean ball, the strict gap and a grouped-coordinate construction
determine the whole smooth-selection frontier. Fix \(N\geq3\) and an integer
block-dimension cap \(d\geq3\). Among exact globally \(C^1\) factorizations
over products of arbitrary proper cones

\[
                         K_1\times\cdots\times K_k,
 \qquad m_j=\dim K_j,\quad 3\leq m_j\leq d,                  \tag{24}
\]

with full-product ambient barriers, the simultaneous optima are

\[
\begin{array}{c|c|c|c}
\text{cap}&k_{\min}&M_{\min}&\nu_{\min}\\ \hline
3\leq d<N+1&
\left\lceil N/(d-2)\right\rceil&
N+2\left\lceil N/(d-2)\right\rceil&
2\left\lceil N/(d-2)\right\rceil\\[2mm]
d\geq N+1&1&N+1&2
\end{array}                                                   \tag{25}
\]

Here \(M=\sum_jm_j\). The value of \(\nu\) is the least possible parameter
of a possibly coupled logarithmically homogeneous self-concordant barrier
on the entire chosen cone product. It is not a feasible-slice barrier
claim.

### Lower bounds

If \(d<N+1\), every capacity \(c_j=m_j-2\) is strictly below \(n=N-1\).
Therefore (4) gives

\[
 \sum_jc_j\geq N,
 \qquad
 k\geq\left\lceil{N\over d-2}\right\rceil,
 \qquad
 M=\sum_j(c_j+2)
   \geq N+2\left\lceil{N\over d-2}\right\rceil.              \tag{26}
\]

Every proper cone of dimension at least two has a two-dimensional linear
section through an interior point that is itself a proper two-dimensional
cone, hence is linearly isomorphic to \(\mathbb R_+^2\). Restricting any
full-product barrier to the product of these sections gives a barrier on
\(\mathbb R_+^{2k}\). The orthant barrier lower bound gives
\(\nu\geq2k\), proving the last lower bound in the first row of (25).

If \(d\geq N+1\), local curvature already gives
\(M=\sum_j(c_j+2)\geq n+2=N+1\), while \(k\geq1\) and the same
two-dimensional-section argument gives \(\nu\geq2\).

### Matching grouped-coordinate lift

Assume \(3\leq d<N+1\), set \(c=d-2\), and partition
\(\{1,\ldots,N\}\) into

\[
                       k=\left\lceil{N\over c}\right\rceil   \tag{27}
\]

nonempty groups \(G\), each of size \(g_G\leq c\). The final group may be
smaller. Use one block \(Q_{g_G+2}\) for each group and define, for
\(x,y\in S^{N-1}\),

\[
\begin{aligned}
 A_G(x)&=\left({1+\|x_G\|^2\over2},
                 {1-\|x_G\|^2\over2},x_G\right),\\
 B_G(y)&=\left({1+\|y_G\|^2\over2},
                -{1-\|y_G\|^2\over2},-y_G\right).
\end{aligned}                                                 \tag{28}
\]

Both lie on the positive Lorentz boundary and

\[
                 \langle A_G(x),B_G(y)\rangle
                       ={1\over2}\|x_G-y_G\|^2.               \tag{29}
\]

Summing (29) over the coordinate partition gives

\[
                 \sum_G\langle A_G(x),B_G(y)\rangle
                      ={1\over2}\|x-y\|^2
                      =1-\langle x,y\rangle.                  \tag{30}
\]

The associated affine lift is equally explicit. For
\(q_G=(u_G,v_G,w_G)\in Q_{g_G+2}\), impose

\[
 u_G+v_G=1\quad\text{for every }G,
 \qquad
 \sum_G(u_G-v_G)=1,
 \qquad x_G=w_G.                                              \tag{31}
\]

Writing \(s_G=u_G-v_G\), the Lorentz constraint and \(u_G+v_G=1\)
are equivalent to

\[
                              s_G\geq\|x_G\|^2.               \tag{32}
\]

Thus (31)--(32) project exactly to \(\|x\|\leq1\). Strict feasibility
holds at \(x=0\) by choosing any \(s_G>0\) summing to one. On the boundary,
\(\sum_Gs_G=\sum_G\|x_G\|^2=1\) forces
\(s_G=\|x_G\|^2\) for every group, so the primal boundary fiber is unique
and equals (28).

For the normalized dual contact sheet, assign multiplier

\[
             \lambda_G={\|y_G\|^2\over2}
 \quad\text{to }u_G+v_G=1,
 \qquad
             \lambda_0={1\over2}
 \quad\text{to }\sum_G(u_G-v_G)=1.                            \tag{33}
\]

Subtracting the lifted objective \(\sum_G\langle y_G,w_G\rangle\)
produces the dual Lorentz vector

\[
 (\lambda_G+\lambda_0,\lambda_G-\lambda_0,-y_G)=B_G(y),
\]

and the multiplier objective is
\(\sum_G\lambda_G+\lambda_0=1\). Hence both contact selections are
globally polynomial and the incidence sheets are regular. The construction
has

\[
 \sum_G(g_G+2)=N+2k,
 \qquad
 \nu=2k,                                                      \tag{34}
\]

which matches (26), including when the last block is smaller than the cap.

For \(d\geq N+1\), the single direct factorization

\[
             A(x)=(1,x),\qquad B(y)=(1,-y)\in Q_{N+1},        \tag{35}
\]

has pairing \(1-\langle x,y\rangle\). Equivalently, the affine slice
\((1,x)\in Q_{N+1}\) projects to the ball, is strictly feasible at \(x=0\),
and has a unique polynomial boundary contact sheet. It attains the second
row of (25).

The grouped construction is standard rotated-SOC epigraph modeling in
larger coordinate groups. What appears new is its exact optimality under
global contact regularity for every cap \(d\), obtained from the strict
submersion gap.

## 6. Literature boundary

The topological ingredients are classical:

- Ehresmann's proper-submersion theorem appears in C. Ehresmann,
  [*Les connexions infinitesimales dans un espace fibre differentiable*](https://www.numdam.org/item/SB_1948-1951__1__153_0/)
  (1950/1951).
- W. Browder,
  [*Fiberings of spheres and H-spaces which are rational homology spheres*](https://doi.org/10.1090/S0002-9904-1962-10747-2),
  Bulletin of the AMS 68 (1962), 202--203, states as Theorem 1 that the
  connected fiber has homotopy type \(S^1,S^3\), or \(S^7\).
- J. F. Adams,
  [*On the non-existence of elements of Hopf invariant one*](https://doi.org/10.2307/1970147),
  Annals of Mathematics 72 (1960), 20--104, is the primary source behind
  the exceptional dimensions.

A targeted search found the classical sphere-fibration results and the
standard cone-lift/factorization literature, but no source connecting full
mixed-curvature rank of an individual cone factor to a sphere submersion,
or deriving the strict capacity gap (4). The topology is not new. The
apparently new contribution is the factor-integrability bridge and the
joint common-kernel observation that turns all saturated sphere maps into
one local diffeomorphism onto their product. Novelty remains subject to
specialist review.

An independent hostile audit checked the fixed-variable annihilation and
quotient-rank bridge, induced boundary regularity, \(C^1\) smoothing,
Ehresmann and Browder hypotheses, fiber connectedness and Poincaré duality,
the Serre differential forcing \(r=d+1\), saturated-partition arithmetic,
and every grouped lift, dual-certificate, dimension, and ambient-barrier
formula. No mathematical error was found.
The later joint-covering replacement for the arithmetic step was separately
hostile-audited in the abstract contact-kernel setting, including its
strictly convex sphere specialization.
