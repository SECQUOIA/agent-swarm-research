# Exact Lorentz-block complexity of the Euclidean ball

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the proof; moderate on novelty

## Sharp theorem

Write

\[
 B_2^N=\{x\in\mathbb R^N:\|x\|_2\leq1\},
 \qquad
 Q_m=\{(t,u)\in\mathbb R\times\mathbb R^{m-1}:t\geq\|u\|_2\}.
\]

Consider an exact extended formulation of \(B_2^N\) whose inequality
cone is

\[
 K=\prod_{i=1}^k Q_{m_i},\qquad m_i\geq2,
\]

and which otherwise permits arbitrary affine equalities, projections, and
unrestricted free variables. Then

\[
 \boxed{\sum_{i=1}^k(m_i-2)\geq N-1.}                 \tag{1}
\]

Consequently, if every block has dimension at most \(d\geq3\),

\[
 \boxed{k\geq
   \left\lceil\frac{N-1}{d-2}\right\rceil.}           \tag{2}
\]

The standard norm tree attains (2): an internal node with \(j\leq d-1\)
children uses one \(Q_{j+1}\) constraint, and a rooted tree with \(N\)
leaves satisfies

\[
 N-1=\sum_{v\ \mathrm{internal}}(\deg(v)-1).
\]

Explicitly, put
\(k=\lceil(N-1)/(d-2)\rceil\), and split \(N-1\) into \(k\) positive
integers \(b_i\leq d-2\). Make the internal nodes a chain: node \(i<k\)
has \(b_i\) leaf children and the next internal node as one additional
child, while the last node has \(b_k+1\) leaf children. Its arities are
at most \(d-1\), and it has exactly \(N\) leaves. Associate a scalar to
each internal node, impose that the parent scalar bounds the Euclidean
norm of its child values, and fix the root scalar to one. Recursive
elimination gives exactly \(\|x\|_2\leq1\).

Thus the exact minimum number of Lorentz blocks of dimension at most \(d\)
is

\[
 \boxed{k_d(B_2^N)=
   \left\lceil\frac{N-1}{d-2}\right\rceil}             \tag{3}
\]

for \(N\geq2\), with one block when \(d\geq N+1\). In particular, an
exact formulation by three-dimensional Lorentz cones needs exactly
\(N-1\) blocks.

For \(d=2\), (1) rules out every finite lift, consistently with the fact
that products of \(Q_2\) are polyhedral. Rotated second-order cones are
included because they are linearly isomorphic to Lorentz cones of the
same dimension.

The stronger weighted inequality (1) is the useful invariant. A full
\(Q_m\) block can carry at most \(m-2\) independent directions of positive
boundary curvature. Two-dimensional Lorentz blocks, ray faces, and zero
faces carry none.

## Lift model and reduction to a proper face

The general lift may be written

\[
 B_2^N=\{Pz+Qu+p:z\in K,\ u\in\mathbb R^f,
                 \ Az+Bu=a\}.                           \tag{4}
\]

If \(v\in\ker B\), feasibility is unchanged by replacing \(u\) by
\(u+tv\). Boundedness of the image forces \(Qv=0\). Hence
\(\ker B\subseteq\ker Q\), so \(Q=RB\) for a linear map \(R\). On the
feasible set,

\[
 Pz+Qu+p=(P-RA)z+Ra+p.
\]

The free variables therefore disappear, leaving an affine image of
\(K\cap L\) for an affine subspace \(L\).

This affine image can be taken linear on the ambient space. Indeed,
\(0\notin L\): otherwise \(K\cap L\) is a cone, and a bounded affine image
of it is a singleton. If \(L=z_0+L_0\), then
\(z_0\notin L_0\), so the affine output map on \(L\) extends to a linear
map on the ambient space.

Choose \(\bar z\in\operatorname{ri}(K\cap L)\), and let \(F\) be the
smallest face of \(K\) containing \(\bar z\). Then \(K\cap L\subseteq F\).
To see this, for every \(z\in K\cap L\), relative interiority gives
\(\bar z-\epsilon(z-\bar z)\in K\cap L\) for some \(\epsilon>0\); the face
property then places \(z\) in \(F\). Moreover
\(\bar z\in\operatorname{ri}F\), so the resulting \(F\)-lift is proper.

Every face of a Cartesian product is a product of faces. Every face of a
Lorentz cone is the zero face, an extreme ray, or the whole cone. Thus

\[
 F=\prod_i F_i,
 \qquad
 F_i\in\{\{0\},\ \text{a ray},\ Q_{m_i}\}              \tag{5}
\]

up to the natural identification with its linear span.

## A regular slack factorization derived from the lift

The ball and its polar have the same extreme-point set
\(S^{N-1}\), and their slack kernel is

\[
 S(x,y)=1-\langle x,y\rangle,
 \qquad x,y\in S^{N-1}.                                 \tag{6}
\]

Work in the Euclidean space \(E=\operatorname{span}F\), where \(F\) is a
proper cone. Replace \(L\) by \(L\cap E\), which does not change the
lift because \(K\cap L=F\cap L\), and write the resulting affine slice as

\[
 L=w_0+L_0=\{z\in E:Mz=b\},
 \qquad w_0\in\operatorname{int}_E F,
 \qquad b=Mw_0,                                         \tag{7}
\]

where \(M:E\to\mathbb R^r\) is surjective and
\(\ker M=L_0\). Let \(\pi:E\to\mathbb R^N\) be the linear output map.
For each \(x\in S^{N-1}\), the primal fiber

\[
 \Gamma_A(x)=\{z\in F:Mz=b,\ \pi z=x\}                  \tag{8}
\]

is nonempty and closed. Define \(A(x)\) to be its unique minimum-norm
point.

For \(y\in S^{N-1}\), optimization over the ball and over its lift gives

\[
 1=\max\{\langle\pi^*y,z\rangle:Mz=b,\ z\in F\}.
\]

Slater's condition holds because \(w_0\in\operatorname{int}_E F\).
Conic strong duality and dual attainment therefore make the closed set

\[
 \Gamma_\lambda(y)=
 \{\lambda\in\mathbb R^r:
    M^*\lambda-\pi^*y\in F^*,\
    \langle b,\lambda\rangle=1\}                         \tag{9}
\]

nonempty. Choose its unique minimum-norm point \(\lambda(y)\), and set

\[
 B(y)=M^*\lambda(y)-\pi^*y\in F^*.                      \tag{10}
\]

For every pair \(x,y\in S^{N-1}\),

\[
 \begin{aligned}
 \langle A(x),B(y)\rangle
 &=\langle MA(x),\lambda(y)\rangle
   -\langle\pi A(x),y\rangle\\
 &=1-\langle x,y\rangle.                                \tag{11}
 \end{aligned}
\]

This derives, rather than merely invokes, the needed slack factorization.

No rationality or algebraicity assumption on the numerical coefficients is
needed: finite systems of Lorentz and affine constraints with arbitrary
real coefficients are semialgebraic with those coefficients as parameters.
The graphs in (8)--(9) are semialgebraic. The assertion that a point is
their unique norm minimizer is a first-order formula over the reals, so
quantifier elimination shows that \(A\) and \(\lambda\), hence \(B\), are
semialgebraic maps.

Take a finite \(C^1\) semialgebraic stratification of \(S^{N-1}\)
compatible with both maps, all sets \(\{A_i=0\}\) and \(\{B_i=0\}\), and
the rank strata of the Jacobians used below. The union of the
full-dimensional strata is relatively open and dense. Choose \(x_0\) on
one such stratum. After restricting to a small neighborhood inside that
stratum, all factor maps are \(C^1\), every zero/nonzero pattern is fixed,
and each relevant Jacobian rank is fixed. This supplies one common
differentiability point for all finitely many blocks; no regularity of an
arbitrary abstract slack factorization is being assumed.

These are the standard projection/quantifier-elimination and
semialgebraic-stratification facts; see Chapters 2 and 5 of
[Basu, Pollack, and
Roy](https://perso.univ-rennes1.fr/marie-francoise.roy/bpr-ed2-posted3.pdf).

Decompose (11) by product factors:

\[
 1-\langle x,y\rangle
   =\sum_{i=1}^k\langle A_i(x),B_i(y)\rangle.            \tag{12}
\]

Every summand is nonnegative. Setting \(y=x\) in (12) gives

\[
 \langle A_i(x),B_i(x)\rangle=0
 \quad\text{for every }i\text{ and }x\in S^{N-1}.       \tag{13}
\]

## Mixed-derivative curvature identity

Let \(\phi:U\subset\mathbb R^{N-1}\to S^{N-1}\) be a smooth local chart
with \(\phi(0)=x_0\) and \(D\phi(0)\) an isometry. Put
\(a_i(u)=A_i(\phi(u))\) and \(b_i(u)=B_i(\phi(u))\).

First consider a full Lorentz factor \(F_i=Q_{m_i}\). If both
\(a_i(0)\) and \(b_i(0)\) are nonzero, Lorentz complementarity in (13)
and continuity give, locally,

\[
 a_i(u)=\alpha_i(u)(1,n_i(u)),\qquad
 b_i(u)=\beta_i(u)(1,-n_i(u)),                           \tag{14}
\]

where \(\alpha_i,\beta_i>0\) and
\(n_i(u)\in S^{m_i-2}\). Differentiating the bilinear summand once in
each argument gives

\[
 -D_uD_v\langle a_i(u),b_i(v)\rangle\big|_{u=v=0}
 =\alpha_i(0)\beta_i(0)\,Dn_i(0)^T Dn_i(0).             \tag{15}
\]

All derivatives of the scale factors cancel explicitly. Namely,

\[
 \begin{aligned}
 Da_i[h]
 &=D\alpha_i[h](1,n_i)+\alpha_i(0)\,(0,Dn_i[h]),\\
 Db_i[k]
 &=D\beta_i[k](1,-n_i)+\beta_i(0)\,(0,-Dn_i[k]).
 \end{aligned}
\]

Here every unmarked quantity on the right is evaluated at \(u=0\).

The scale--scale term vanishes because
\(\langle(1,n_i),(1,-n_i)\rangle=0\). The two scale--direction terms
vanish because \(n_i^TDn_i=0\). The remaining term is
\(-\alpha_i\beta_i\langle Dn_i[h],Dn_i[k]\rangle\), which proves
(15). It is positive semidefinite after negation and has rank at most
\(m_i-2\).

If \(a_i(0)=0\), then \(Da_i(0)=0\). Indeed, a differentiable map from
an open neighborhood into a pointed cone has zero derivative whenever
its value is the cone vertex: the two one-sided derivatives in directions
\(h\) and \(-h\) put \(Da_i(0)h\) in both the cone and its negative.
The same holds if \(b_i(0)=0\). Such a block contributes zero to the mixed
derivative. A ray factor also contributes zero: complementary nonnegative
scalars have at least one zero, and the same vertex argument applies.
The zero face is trivial. Formula (15) also covers a full \(Q_2\): its
direction set is \(S^0\), hence \(Dn_i=0\).

On the other hand,

\[
 -D_uD_v\bigl(1-\langle\phi(u),\phi(v)\rangle\bigr)
       \big|_{u=v=0}=I_{N-1}.                            \tag{16}
\]

Combining (12), (15), and (16) yields the exact curvature decomposition

\[
 I_{N-1}
 =\sum_{i\in\mathcal A}
   \alpha_i(0)\beta_i(0)\,Dn_i(0)^T Dn_i(0),             \tag{17}
\]

where \(\mathcal A\) contains the nonzero full-cone blocks at \(x_0\).
Rank subadditivity now gives

\[
 N-1
 \leq\sum_{i\in\mathcal A}\operatorname{rank}Dn_i(0)
 \leq\sum_{i\in\mathcal A}(m_i-2)
 \leq\sum_{i=1}^k(m_i-2),
\]

which proves (1).

## General local curvature theorem

The preceding argument is not special to a sphere. Let \(C\subset\mathbb
R^N\) be a full-dimensional compact convex body with \(0\in\operatorname
{int}C\), and suppose \(C\) has an exact lift by
\(\prod_iQ_{m_i}\). Such a body is automatically semialgebraic, even when
this was not assumed in advance, because it is an affine projection of a
finite system of quadratic and affine constraints.

Consider a relatively open semialgebraic \(C^2\) boundary patch \(W\) on
which the primal points and their normalized polar contacts are exposed.
Choose a semialgebraic \(C^2\) local chart

\[
 x:U\subset\mathbb R^{N-1}\longrightarrow W
\]

and let \(y(u)\in\partial C^\circ\) be the unique contact normalized by

\[
 \langle x(u),y(u)\rangle=1.                            \tag{18}
\]

Suppose \(y\) is \(C^1\). Define the mixed slack-curvature matrix

\[
 \mathcal K(u)=Dx(u)^T Dy(u).                            \tag{19}
\]

Rerun the minimum-norm primal/dual selection construction in
(8)--(11), now with \(x\in\operatorname{ext}C\) and
\(y\in\operatorname{ext}C^\circ\), to obtain semialgebraic slack factors
on these two exposed patches.

At every point where the semialgebraic slack factors are \(C^1\), the
same computation as above gives

\[
 \boxed{
 \mathcal K(u)
 =\sum_{i\in\mathcal A(u)}
 \alpha_i(u)\beta_i(u)\,
 Dn_i(u)^TDn_i(u).}                                     \tag{20}
\]

Indeed, apply the slack factorization to

\[
 1-\langle x(u),y(v)\rangle
   =\sum_i\langle A_i(x(u)),B_i(y(v))\rangle.
\]

It vanishes on \(u=v\), so Lorentz complementarity gives the same paired
boundary directions as in (14). Taking the negative mixed derivative
gives (20), since
\[
 -D_uD_v[1-\langle x(u),y(v)\rangle]_{u=v}
 =Dx(u)^TDy(u).
\]

The maps \(A\circ x\) and \(B\circ y\) are semialgebraic. Their common
\(C^1\) locus is dense and relatively open after semialgebraic
stratification. Therefore, if

\[
 r=\max_{u\in U}\operatorname{rank}\mathcal K(u),
\]

then the set on which some \(r\)-minor is nonzero is open and nonempty
and meets that regular locus. At such a point, (20) and rank
subadditivity imply the general curvature budget

\[
 \boxed{\sum_i(m_i-2)\geq r.}                            \tag{21}
\]

To connect (19) with ordinary curvature, let \(n(u)\) be the outward unit
normal and put \(h(u)=\langle x(u),n(u)\rangle>0\). The normalized polar
contact is

\[
 y(u)=\frac{n(u)}{h(u)}.
\]

Because \(Dx(u)^Tn(u)=0\),

\[
 \mathcal K(u)
 =\frac{1}{h(u)}Dx(u)^TDn(u),                            \tag{22}
\]

the second fundamental form up to the positive support-number factor
\(h(u)^{-1}\). It is positive semidefinite for a convex body under this
outward-normal convention, and its rank is the rank of the shape
operator. The rank is independent of the chosen boundary coordinates,
because a coordinate change acts by congruence.

Here a \(C^2\) boundary point means a point possessing a relatively open
\(C^2\) boundary neighborhood. If \(C\) has even one such point of
strictly positive curvature, positive definiteness persists on a smaller
neighborhood. Strict curvature makes \(x\) exposed: a second contact of
its supporting hyperplane would put a nontrivial boundary segment through
\(x\) and force zero normal curvature in its direction. Smoothness at
\(x\) makes its normal ray unique, so \(x\) exposes the normalized polar
contact \(y\) as a singleton face of \(C^\circ\); hence \(y\) is exposed
as well. Equation (21) therefore applies with \(r=N-1\):

\[
 \boxed{\sum_i(m_i-2)\geq N-1}                           \tag{23}
\]

for every exact Lorentz lift of any such body. The ball is the case where
\(\mathcal K=I_{N-1}\), and its norm tree shows that this universal
positive-curvature lower bound is sharp.

## Exact ambient-barrier consequence

Each Lorentz cone has symmetric-cone rank two, and the rank of their
product is \(2k\). The homogeneous-cone theorem of
[Güler and Tunçel](https://doi.org/10.1007/BF01584844) identifies the
optimal normal-barrier parameter with cone rank. Therefore the product
ambient cone has optimal normal-barrier parameter \(2k\). Equations
(2)--(3) sharpen the bounded-granularity law to the exact value

\[
 \boxed{\nu_{\mathrm{normal},\leq d}(B_2^N)
 =2\left\lceil\frac{N-1}{d-2}\right\rceil.}             \tag{24}
\]

This is a statement about the ambient product-cone representation, not an
intrinsic barrier lower bound for the projected ball. It also does not by
itself prove an iteration lower bound for every IPM or QIPM. It says that
the familiar norm-tree formulation is exactly optimal in both block count
and ambient normal-barrier parameter among all exact bounded-dimensional
Lorentz lifts, even those using arbitrary consensus equations, projections,
and free variables.

## Literature boundary

[Gouveia, Parrilo, and Thomas](https://arxiv.org/abs/1111.3164) prove the
cone-lift/slack-factorization equivalence, including reduction of
nonproper lifts through faces for nice cones. Their factors are not
required to be linear. [Fawzi](https://arxiv.org/abs/1610.04901) introduces
second-order-cone rank for products of three-dimensional Lorentz cones and
uses slack-factorization obstructions to rule out finite SOC lifts of
\(S_+^3\). [Scheiderer](https://arxiv.org/abs/2004.04196) studies
semidefinite extension degree, which controls maximum LMI block size but
not the minimum number of bounded-size SOC blocks. His Example 1.5 records
the standard lift of an \((N+1)\)-dimensional Lorentz cone by \(N-1\)
three-dimensional Lorentz cones, but gives no matching count lower bound.
Scheiderer's newer
[positive-curvature existence theorem](https://arxiv.org/abs/2509.17121)
shows that every compact convex semialgebraic body with Nash-smooth,
strictly positively curved boundary has some exact lift by \(2\times2\)
PSD blocks, equivalently \(Q_3\) blocks. It does not bound the number of
blocks. Equation (23) supplies the complementary universal lower bound of
\(N-1\) such blocks.
The recent work of
[Aubrun, La Piana, and
Müller-Hermes](https://arxiv.org/abs/2606.27825) studies positive-map
factorization through direct sums of Lorentz cones; it does not state the
ball block-count formula (3) or the curvature budget (1).

A targeted search for Euclidean-ball SOC extension complexity,
second-order-cone rank of the ball slack kernel, bounded-block Lorentz
lifts, and curvature lower bounds for cone factorizations found no
explicit statement of (1)--(3). The norm-tree upper bound is classical.
The lower bound should therefore be described as apparently new pending
specialist review, not as an established priority claim.

## Audit checklist

- Verify the free-variable elimination and the extension of the affine
  output map to a linear map.
- Verify that passage to the minimal face preserves a proper lift and that
  product Lorentz faces have only the three types in (5).
- Verify the existence of common \(C^1\) semialgebraic slack factors.
- Check the zero-factor derivative argument and the signs in (15)--(17).
- Search specifically for differential or curvature lower bounds on the
  SOC rank of \(1-x^Ty\).

The independent audit checked every item above, including the general
curvature theorem, and found no counterexample. Its requests for a more
explicit \(L\cap E\) replacement, homogeneous-cone citation,
\(C^2\)-neighborhood convention, and exposed primal/polar roles have all
been incorporated.
