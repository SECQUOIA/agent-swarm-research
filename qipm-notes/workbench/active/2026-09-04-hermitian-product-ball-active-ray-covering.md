# Active rays do not enlarge the Hermitian saturation profiles

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Let

\[
 C=\prod_{a=1}^h B_2^{s_a},\qquad
 M=\prod_{a=1}^h S^{p_a},\qquad
 p_a=s_a-1\geq1,\qquad n=\sum_a p_a.                 \tag{1}
\]

Suppose the full family of extreme-row slacks has globally labelled
\(C^1\) factors over finitely many real, complex, or quaternionic
Hermitian PSD blocks and finitely many scalar rays:

\[
\begin{split}
 1-x_a^Tz
  ={}&\sum_i\operatorname{Re}\operatorname{tr}
             \bigl(X_i(x)Y_i^a(z)\bigr)\\
    &+\sum_j\alpha_j(x)\beta_j^a(z),                    \tag{2}\\
 &X_i,Y_i^a\in H_+^{r_i}(\mathbb F_i),\quad r_i\geq2,\\
 &\alpha_j,\beta_j^a\geq0,\qquad
   \mathbb F_i\in\{\mathbb R,\mathbb C,\mathbb H\}.
\end{split}
\]

Write

\[
 a_i=\dim_{\mathbb R}\mathbb F_i,\qquad
 c_i=a_i\left\lfloor\frac{r_i^2}{4}\right\rfloor.       \tag{3}
\]

Then \(n\leq\sum_i c_i\).  If equality holds, the positive-block support
maps assemble into a finite covering

\[
 \Pi:M\longrightarrow
 \prod_i\operatorname{Gr}_{\lfloor r_i/2\rfloor}
                  (\mathbb F_i^{r_i}).                  \tag{4}
\]

The covering topology first implies:

1. every complex or quaternionic block has order \(r_i=2\);
2. every real block has order \(r_i\in\{2,3,4\}\); and
3. the source-sphere dimensions have the candidate multiset described below.

Associate to each positive block the multiset

\[
\mathcal D_i=
\begin{cases}
 \{1\},&(\mathbb F_i,r_i)=(\mathbb R,2),\\
 \{2\},&(\mathbb F_i,r_i)=(\mathbb R,3)
                  \text{ or }(\mathbb C,2),\\
 \{2,2\},&(\mathbb F_i,r_i)=(\mathbb R,4),\\
 \{4\},&(\mathbb F_i,r_i)=(\mathbb H,2).
\end{cases}                                             \tag{5a}
\]

Then the covering theorem alone forces

\[
                 \boxed{\ \{p_a:a\in[h]\}
                       =\mathop{\biguplus}_i\mathcal D_i\ }.            \tag{5b}
\]

The two real entries of orders three and four in (5a) are topological
possibilities only.  The independently audited
[cylinder-integrability theorem](2026-09-04-real-low-order-cylinder-exclusion-product-balls.md)
excludes both for the full slack identities (2), even with the active ray
terms.  Therefore actual equality forces every positive block to have
order two and the exact profile

\[
 \boxed{
 \{p_a:a\in[h]\}
 =\biguplus_i
 \begin{cases}
   \{1\},&(\mathbb F_i,r_i)=(\mathbb R,2),\\
   \{2\},&(\mathbb F_i,r_i)=(\mathbb C,2),\\
   \{4\},&(\mathbb F_i,r_i)=(\mathbb H,2).
 \end{cases}}                                               \tag{5c}
\]

If a forbidden block occurs or (5c) fails, integrality gives the strict gap

\[
                         \sum_i c_i\geq n+1.             \tag{6}
\]

For a fixed complex field, equality is possible only for products of
three-dimensional balls represented by \(H_+^2(\mathbb C)\cong Q_4\).
For a fixed quaternionic field, equality is possible only for products of
five-dimensional balls represented by
\(H_+^2(\mathbb H)\cong Q_6\).  More generally, if real blocks are allowed
only at order two, (5c) is exactly the order-two division-algebra
classification.  Zero ray terms may of course be appended.

The intermediate covering classification leaves two real low-order
covering-space possibilities:

\[
\begin{array}{c|c}
r&\text{universal cover of the balanced real target}\\ \hline
3&S^2\longrightarrow\mathbb{RP}^2,\\
4&S^2\times S^2\longrightarrow
       \operatorname{Gr}_2(\mathbb R^4).
\end{array}                                             \tag{7}
\]

Accordingly, topology alone permits an order-three real block to account
for one \(S^2\) source factor and an order-four real block to account for
two \(S^2\) source factors.  This is only a necessary topological
possibility.  It does not construct a full slack factorization with active
rays.  Real orders \(r\geq5\) are excluded below, and the cylinder theorem
cited above excludes the remaining two by using the full slack identities.

## 1. Rays have zero mixed-curvature rank

Fix \(x\in M\) and put \(z=x_a\) in row \(a\).  Every term on the
right-hand side of (2) is nonnegative and their sum is zero.  Hence

\[
 \operatorname{Re}\operatorname{tr}
       \bigl(X_i(x)Y_i^a(x_a)\bigr)=0,\qquad
 \alpha_j(x)\beta_j^a(x_a)=0.                           \tag{8}
\]

Consider one ray term.  If \(\alpha_j(x)=0\), then
\(d\alpha_j|_{T_xM}=0\), because the nonnegative \(C^1\) function
\(\alpha_j\) has a local minimum at \(x\).  If \(\alpha_j(x)>0\), then
\(\beta_j^a(x_a)=0\), and
\(d\beta_j^a|_{T_{x_a}S^{p_a}}=0\) for the same reason.  Therefore

\[
 d_xd_z\bigl(\alpha_j(x)\beta_j^a(z)\bigr)=0             \tag{9}
\]

on the contact tangent spaces in every case.  Active rays can carry
zeroth-order slack away from contact, but they carry no mixed-curvature
channel at contact.

For block \(i\), let

\[
 q_i=\operatorname{rank}_{\mathbb F_i}\sum_aY_i^a(x_a),
 \qquad
 p_i'=\operatorname{rank}_{\mathbb F_i}X_i(x).           \tag{10}
\]

PSD complementarity gives \(p_i'+q_i\leq r_i\), and the Hermitian support
differential has real rank at most \(a_ip_i'q_i\).  Mixed differentiation
of (2), together with (9), therefore gives

\[
 n\leq\sum_i a_ip_i'q_i
   \leq\sum_i a_i\left\lfloor\frac{r_i^2}{4}\right\rfloor.
                                                               \tag{11}
\]

This proves the capacity bound.

## 2. Equality gives a covering despite active rays

Assume equality in (11).  Every positive block saturates both rank
inequalities at every \(x\).  It is strictly complementary with balanced
constant ranks.  If its primal rank is \(\lfloor r_i/2\rfloor\), use the
range of \(X_i(x)\); if its rank is \(\lceil r_i/2\rceil\), use its kernel.
This defines a \(C^1\) map to the balanced Grassmannian in (4).

The standard support differential identifies the block mixed channel with
the tangent space of that Grassmannian.  If \(v\in\ker d\Pi_x\), every
block mixed form annihilates \(v\).  Equations (9) and (11) then say that
the nondegenerate product-sphere metric annihilates \(v\), so \(v=0\).
The source and target of (4) both have dimension \(n\); hence \(\Pi\) is a
local diffeomorphism.  A local diffeomorphism from compact \(M\) has open
and closed image in the connected target and is proper, so it is a finite
covering.

Unlike the no-active-ray theorem, (2) does not make \(\Pi\) injective:
ray terms can distinguish two source points having the same positive-block
supports.  The covering conclusion is the exact statement that survives.

## 3. Universal-cover obstructions

Let \(t\) be the number of \(S^1\) factors in \(M\), let \(u\) be the
number of real order-two blocks, and let \(v\) be the number of real
blocks of order at least three.  The relevant fundamental groups are

\[
\begin{split}
 \pi_1(M)&\cong\mathbb Z^t,\\
 \pi_1\!\left(\prod_iG_i\right)
   &\cong\mathbb Z^u\times(\mathbb Z/2)^v.               \tag{12}
\end{split}
\]

Here \(G_i\) denotes the target factor in (4).  Complex and quaternionic
Grassmannians are simply connected.  Also
\(\operatorname{Gr}_1(\mathbb R^2)=S^1\), while every real balanced
Grassmannian of order at least three has fundamental group
\(\mathbb Z/2\).  The latter follows directly from the homotopy exact
sequence of

\[
 S(O(k)\times O(r-k))\longrightarrow SO(r)
       \longrightarrow\operatorname{Gr}_k(\mathbb R^r): \tag{13}
\]

the identity component of the fiber surjects on \(\pi_1(SO(r))\), and the
fiber has two components.

A finite covering identifies \(\pi_1(M)\) with a finite-index subgroup of
the target group.  Free-abelian rank is invariant under passage to finite
index, so (12) gives \(t=u\).

Lift (4) to universal covers.  The lift is a covering between simply
connected manifolds and hence a diffeomorphism.  The universal cover of
\(M\) is homotopy equivalent to

\[
                         \prod_{p_a\geq2}S^{p_a}.         \tag{14}
\]

In its positive-degree mod-two cohomology, every element has square zero:
the square of each sphere generator vanishes, and in characteristic two
the square of a sum is the sum of the squares.

For a complex balanced Grassmannian of order \(r\geq3\), the degree-two
Schubert class satisfies

\[
                         \sigma_1^2=\sigma_2+\sigma_{1,1}\ne0,          \tag{15}
\]

with terms outside the defining rectangle omitted.  For the corresponding
quaternionic Grassmannian, the degree-doubling cohomology isomorphism gives
the same nonzero relation in degree eight.  These targets are simply
connected, so the classes in (15) survive unchanged in the universal
cover of the full target.  Künneth then contradicts (14).  This proves
that every complex and quaternionic block has order two.

Now consider a real balanced block of order \(r\geq6\), with
\(k=\lfloor r/2\rfloor\) and \(r-k\geq3\).  Its universal cover is the
oriented Grassmannian.  The homotopy exact sequence of

\[
 SO(k)\times SO(r-k)\longrightarrow SO(r)
       \longrightarrow\operatorname{Gr}_k^+(\mathbb R^r)              \tag{16}
\]

gives

\[
 \pi_2\!\left(\operatorname{Gr}_k^+(\mathbb R^r)\right)
  =\ker\!\left[(\mathbb Z/2)^2\longrightarrow\mathbb Z/2\right]
  \cong\mathbb Z/2.                                      \tag{17}
\]

The map on fundamental groups is addition, so the oriented Grassmannian
is simply connected.  Hurewicz gives \(H_2\cong\mathbb Z/2\).  In a
product of simply connected target factors this torsion remains a direct
summand of \(H_2\), whereas (14) has torsion-free \(H_2\).  Thus no real
order \(r\geq6\) can occur.

At \(r=5\), the universal cover is the complex quadric

\[
       \operatorname{Gr}_2^+(\mathbb R^5)\cong Q^3\subset\mathbb CP^4.
                                                               \tag{18}
\]

Its integral cohomology has generators
\(x\in H^2(Q^3;\mathbb Z)\) and \(y\in H^4(Q^3;\mathbb Z)\) with

\[
                              x^2=2y.                    \tag{19}
\]

Indeed, \(x\) is the hyperplane class and \(Q^3\) has projective degree
two.  Hence the degree-four part of the graded integral indecomposable
quotient

\[
       H^{>0}(Q^3;\mathbb Z)/
                \bigl(H^{>0}(Q^3;\mathbb Z)\bigr)^2       \tag{20}
\]

contains \(\mathbb Z/2\), generated by \(y\) modulo \(2y=x^2\).
Indecomposables of tensor products of connected torsion-free cohomology
rings split as the direct sum of the factor indecomposables.  By this
point all other possible universal-cover factors have torsion-free
integral cohomology.  A product of spheres has a free-abelian
indecomposable quotient, so the universal-cover diffeomorphism rules out
the order-five block.

The only remaining target factors have universal covers

\[
\begin{array}{c|c}
(\mathbb F,r)&\text{universal-cover factor}\\ \hline
(\mathbb R,2)&\mathbb R,\\
(\mathbb R,3),(\mathbb C,2)&S^2,\\
(\mathbb R,4)&S^2\times S^2,\\
(\mathbb H,2)&S^4.
\end{array}                                             \tag{21}
\]

We already matched the number of \(\mathbb R\) factors through
free-abelian rank in (12).  The graded mod-two indecomposable quotient
records one generator in each remaining sphere dimension.  Applied to
the universal-cover diffeomorphism, it gives precisely the multiset
identity (5b).

## Scope and literature boundary

The covering part of this note strengthens
[Hermitian curvature saturation for products of
balls](2026-09-04-hermitian-product-ball-capacity-rigidity.md), whose
global injectivity argument excluded active rays.  Here active rays are
allowed, at the price of retaining only a finite covering.  The
universal-cover obstruction leaves the two intermediate real possibilities
in (7); the companion cylinder theorem eliminates them for the full
product-ball slack.

The Hermitian support differential is developed in
[Saturated PSD factors induce Grassmannian
submersions](2026-09-04-psd-support-grassmannian-submersion.md).
Sankaran and Sarkar,
[*Degrees of Maps between Grassmann
Manifolds*](https://www.imsc.res.in/~sankaran/Papers/grassojm.pdf),
record the degree-doubling integral cohomology-ring isomorphism from complex
to quaternionic Grassmannians used in (15).  The Grassmannian topology and
Schubert formula are classical.  The real \(H_2\) and quadric calculations
also appear in
[Sphere submersions onto balanced real
Grassmannians](2026-09-04-sphere-submersions-balanced-real-grassmannians.md).
The new ingredient appears to be the
combination of the zero-rank ray lemma with the joint support covering for
the full product-ball row family.  No literature source for this
formulation consequence was found, but priority is not established.

The combined result is conditional on globally labelled \(C^1\) factor selections.
It is not an unrestricted conic-extension lower bound and not an IPM/QIPM
iteration lower bound.  The real coverings in (7) are not existence claims
for full slack factorizations and, by the companion theorem, cannot occur
in them.

## Independent hostile audit

The audit rederived the zero-mixed-rank lemma for every ray status and
confirmed that equality leaves a proper local diffeomorphism on the
positive-support factors, hence a finite covering.  Passing to universal
covers preserves the product decomposition.  The fundamental-group count,
the complex and quaternionic Schubert-square obstruction, and the
indecomposable-degree multiset argument all check.  The audit also confirmed
the precise intermediate scope: real orders three and four remain
topologically possible before full-slack cylinder integrability is imposed,
and no realization is claimed.

The audit checked in particular:

1. the \(C^1\) zero-mixed-rank lemma (9) for every ray status;
2. balanced Hermitian equality and the odd-order range/kernel convention;
3. proper local diffeomorphism and universal-cover lifting;
4. all fundamental groups in (12), including real order four;
5. the complex and quaternionic nonzero squares in (15);
6. the indecomposable-degree multiset argument; and
7. the precise nonexistence versus unresolved-realizability language in
   (7).

The subsequent real-order completion (16)--(21) also passed an independent
hostile audit.  For balanced \(r\geq6\), the audit checked
\(\pi_2=H_2=\mathbb Z/2\) and persistence of that torsion under products.
At \(r=5\), it checked the quadric relation \(x^2=2y\), the resulting
\(\mathbb Z/2\) integral indecomposable, and splitting of indecomposables
under tensor products of the torsion-free factor cohomology rings.  It
then verified the complete universal-cover list (21) and the multiset
ledger (5a)--(5b).  The real order-three and order-four entries remain
correctly scoped as necessary topological possibilities only.

Three independent hostile audits of the companion cylinder theorem then
verified that a fixed unrelated dual range forces an order-four support
restriction into the diagonal or antidiagonal
\(S^2\subset S^2\times S^2\), incompatible with a ruling.  They also
checked that the order-three case reduces exactly to the independently
audited one-ball \(\mathbb S_+^3\)-plus-rays impossibility theorem.  Thus
the combined full-slack conclusion is the order-two profile (5c).
