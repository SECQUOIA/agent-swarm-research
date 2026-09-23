# Everywhere differentiability already forbids saturated Lorentz contact capacity

Status: Proved; literature-screened; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Executive result

Let

\[
 C=(B_2^{p+1})^k,\qquad p\geq2,
\]

and suppose its full extreme slack rows have a globally labelled
factorization

\[
 1-x_a^Tz=\sum_{i=1}^L\langle A_i(x),B_i^a(z)\rangle,
 \qquad x\in (S^p)^k,\quad z\in S^p,                     \tag{1}
\]

over Lorentz cones \(Q_{r_i+2}\), where \(1\leq r_i\leq c\).  Assume only
that every displayed factor map is everywhere Fréchet differentiable.
Their derivatives need not be continuous.  Put

\[
 T=\sum_i r_i,\qquad h_0=\left\lceil\frac p c\right\rceil .
\]

If \(c<p\), then

\[
 \boxed{T\geq kp+1.}                                      \tag{2}
\]

For the following lift consequences, assume that the displayed maps are
globally differentiable primal selections and dual certificates of an
affine lift after reduction to its minimal product face.  Let
\(L_{\rm full}\) be the number of full Lorentz components.  Then

\[
 \boxed{
 L_{\rm full}\geq kh_0+\mathbf 1_{\{c\mid p\}},\qquad
 D_{\rm amb}\geq kp+1+
       2\bigl(kh_0+\mathbf 1_{\{c\mid p\}}\bigr),\qquad
 \nu_F\geq2\bigl(kh_0+\mathbf 1_{\{c\mid p\}}\bigr).
 }                                                        \tag{3}
\]

Here \(D_{\rm amb}=\sum_i(r_i+2)\) counts the original Lorentz
coordinates, while
\(\nu_F=2L_{\rm full}+L_{\rm ray}\) is the operational normal-barrier
parameter on the minimal face.  Extra ray or zero components cannot weaken
(3).

For a **single ball** (\(k=1\)), these inequalities are exact
simultaneously:

\[
 \boxed{
 T_{\rm diff}=p+1,\quad
 L_{\rm diff}=\left\lceil\frac{p+1}{c}\right\rceil,\quad
 D_{\rm diff}=p+1+2\left\lceil\frac{p+1}{c}\right\rceil,\quad
 \nu_{\rm diff}=2\left\lceil\frac{p+1}{c}\right\rceil
 }                                                        \tag{4}
\]

when \(c<p\).  Grouped coordinate-square Lorentz lifts attain (4) with
polynomial, hence analytic, contact factors.  When \(c\geq p\), the direct
\(Q_{p+2}\) lift has \((T,L,D,\nu)=(p,1,p+2,2)\), so there is no
regularity premium.

In contrast, arbitrary-arity norm trees attain the smaller unrestricted
single-ball values

\[
 \left(p,\left\lceil\frac pc\right\rceil,
 p+2\left\lceil\frac pc\right\rceil,
 2\left\lceil\frac pc\right\rceil\right)                 \tag{5}
\]

with globally labelled **Lipschitz** primal and dual contact maps.  Thus
the exact one-ball threshold lies strictly between global Lipschitz
regularity and everywhere differentiability.  For \(k>1\), (2)--(3) prove
a strict global differentiability premium, but do not prove the additive
\(+k\) capacity premium forced by global \(C^1\) selections.  No exact
claim is made in that remaining interval.

There is also a heterogeneous form.  For
\(C=\prod_{a=1}^kB_2^{p_a+1}\), \(p_a\ge2\), put

\[
 P=\sum_ap_a,\qquad H_0=\sum_a\left\lceil\frac{p_a}{c}\right\rceil .
\]

If \(c<\max_ap_a\), every everywhere-differentiable selected
factorization satisfies

\[
 \boxed{
 T_{\rm full}\ge P+1,\qquad
 L_{\rm full}\ge H_0+\mathbf1_{\{c\mid p_a\ {\rm for\ every}\ a\}}.
 }                                                        \tag{5a}
\]

Consequently,

\[
 D_{\rm amb}\ge P+1+
 2\left(H_0+\mathbf1_{\{c\mid p_a\ \forall a\}}\right),\qquad
 \nu_F\ge2\left(H_0+\mathbf1_{\{c\mid p_a\ \forall a\}}\right). \tag{5b}
\]

This is a lower theorem, not an attainment claim for heterogeneous
products.  Equations (5a)--(5b) were added after the independent audit of
the homogeneous theorem; their separate hostile audit has now passed.

## 1. Contact curvature with no derivative continuity

At \(z=x_a\), every summand in (1) is nonnegative and their sum is zero.
Hence the two Lorentz factors are complementary.  Mixed differentiation
along \(u,v\in T_{x_a}S^p\) gives

\[
 g_{S^p,x_a}(u,v)=\sum_i H_i^a(x)(u,v),\qquad
 H_i^a=-\langle D_aA_i(x)[u],DB_i^a(x_a)[v]\rangle.       \tag{6}
\]

This calculation uses derivatives only at the displayed point.  If both
complementary factors are nonzero, write

\[
 A_i=\alpha_i(1,q_i),\qquad B_i^a=\beta_i^a(1,-q_i),
 \qquad q_i\in S^{r_i}.
\]

Then

\[
 H_i^a=\alpha_i\beta_i^a(D_aq_i)^*Dq_i,\qquad
 H_i^a\succeq0,\qquad \operatorname{rank}H_i^a\leq r_i.  \tag{7}
\]

At a cone vertex the derivative of a differentiable cone-valued map
vanishes: its linear image must lie in both the pointed tangent cone and
its negative, hence in the zero lineality space.  Thus (7), with zero
contribution in the vertex cases, holds everywhere without continuity of
the derivatives.

The cylindrical contact zeros also give pointwise row-disjointness.  If
\(H_i^a(x)\neq0\), the nonzero dual factor pins the projective primal ray
while every block \(x_b\), \(b\neq a\), varies.  Therefore

\[
 H_i^a(x)\neq0\quad\Longrightarrow\quad H_i^b(x)=0
 \quad(b\neq a).                                         \tag{8}
\]

Equations (6)--(8) yield the familiar pointwise local bounds

\[
 T_{\rm full}\geq kp,\qquad L_{\rm full}\geq kh_0.        \tag{9}
\]

For the abstract factorization in (1), all displayed Lorentz factors are
counted as full, so \(T_{\rm full}=T\) and \(L_{\rm full}=L\).  For the
lift consequences in (3), these symbols count only the full Lorentz
components of the minimal face; ray and zero components contribute no
mixed contact curvature.

The new point is that equality in the first bound is impossible under
everywhere differentiable selections when \(c<p\).

## 2. Aggregate saturation produces a nonsingular phase map

Sum all \(k\) slack rows and put

\[
 \widehat B_i(z_1,\ldots,z_k)=\sum_{a=1}^k B_i^a(z_a)
 \in Q_{r_i+2}.
\]

Then

\[
 k-\sum_{a=1}^k x_a^Tz_a
   =\sum_i\langle A_i(x),\widehat B_i(z)\rangle.          \tag{10}
\]

The aggregate dual is Lorentz-valued because a Lorentz cone is a convex
cone.  On the product diagonal \(z=x\), define

\[
 \widehat H_i(x)(u,v)
 =-\langle DA_i(x)[u],D\widehat B_i(x)[v]\rangle .
                                                                  \tag{10a}
\]

Mixed differentiation of (10) gives the product metric

\[
 g_{(S^p)^k,x}=\sum_i\widehat H_i(x).                    \tag{10b}
\]

At aggregate contact, \(A_i(x)\) and \(\widehat B_i(x)\) are complementary.
If they are nonzero, their normalized phases agree up to the complementary
sign, and differentiation along the product diagonal gives

\[
 \widehat H_i
 =\alpha_i\widehat\beta_i(Dq_i)^*Dq_i\succeq0,\qquad
 \operatorname{rank}\widehat H_i\leq r_i.                \tag{10c}
\]

The vertex, ray-face, and zero-face cases contribute zero exactly as in
Section 1.

Suppose equality held in the first part of (9):
\(T_{\rm full}=kp=\dim (S^p)^k\).  At every contact point, the rank of
the sum in (10b) is \(kp\), while the sum of the available ranks is exactly
\(kp\).  Consequently every full component is nonzero and uses all of its
rank at every point.  Its normalized primal phase is defined everywhere,
and

\[
 Q=(q_1,\ldots,q_{L_{\rm full}}):
 (S^p)^k\longrightarrow \prod_i S^{r_i}                 \tag{11}
\]

is everywhere differentiable with \(DQ\) an isomorphism at every point.
Ray and zero minimal-face components have no phase and no curvature, so
they do not enter (11).

Indeed, (10c) shows that \(DQ(x)u=0\) would imply
\(g_{(S^p)^k,x}(u,u)=0\), so \(DQ(x)\) is injective.  Its domain and target
both have dimension \(kp\), hence it is an isomorphism.

The inverse-function theorem for everywhere differentiable
finite-dimensional maps says that a map whose derivative is invertible at
every point is a local homeomorphism; continuity of the derivative is not
needed.  Applying it in manifold charts is legitimate: differentiability
makes \(Q\) continuous, so one may restrict a source chart to the preimage
of a target chart, and the coordinate derivative is invertible everywhere
there.  Thus (11) is a local homeomorphism.  The domain is compact, so
\(Q\) is proper; its image is both open and closed in the connected target,
and the standard proper-local-homeomorphism theorem makes it a finite
covering.

Because \(p\geq2\), \((S^p)^k\) is simply connected.  If some \(r_i=1\),
the universal cover of the target has a noncompact Euclidean factor, so it
cannot be the compact domain.  If every \(r_i\geq2\), the target is simply
connected and the covering is a homeomorphism.  All positive cohomology
of the domain below degree \(p\) vanishes.  A target sphere with
\(r_i<p\) would itself give a nonzero class in degree \(r_i\), so every
\(r_i\geq p\).  The degree-\(p\) cohomology rank is therefore exactly the
number of factors with \(r_i=p\), and it must equal \(k\).  These \(k\)
factors already exhaust \(\sum_i r_i=kp\).  Thus the target profile is
exactly \(k\) copies of \(S^p\), which is impossible under
\(r_i\leq c<p\).  Hence

\[
                         T_{\rm full}\geq kp+1.           \tag{12}
\]

which proves (2).

The same argument proves the heterogeneous capacity bound in (5a).  If
\(T_{\rm full}=P\), the aggregate phase map would be a finite covering

\[
 \prod_aS^{p_a}\longrightarrow\prod_iS^{r_i}.
\]

The source is simply connected.  Circle targets are excluded as before;
otherwise the covering is a homeomorphism.  Equality of Poincaré
polynomials gives

\[
                       \prod_a(1+t^{p_a})=\prod_i(1+t^{r_i}). \tag{12a}
\]

This identity determines the exponent multiset.  Its smallest positive
exponent and coefficient give the smallest exponent and its multiplicity;
divide by the corresponding power of \(1+t^m\) and iterate.  Hence
\(\{r_i\}\) must equal \(\{p_a\}\), impossible when every
\(r_i\le c<\max_ap_a\).  Therefore \(T_{\rm full}\ge P+1\).

## 3. Label, dimension, and barrier arithmetic

The local bound in (9) gives \(L_{\rm full}\geq kh_0\).
The global capacity bound (12) also gives

\[
 L_{\rm full}\geq\left\lceil\frac{kp+1}{c}\right\rceil.
\]

Write \(p=qc+r\), \(0\leq r<c\).  If \(r=0\), the second bound is
\(kq+1=kh_0+1\).  If \(r>0\), then

\[
 \left\lceil\frac{kp+1}{c}\right\rceil
 =kq+\left\lceil\frac{kr+1}{c}\right\rceil
 \leq kq+k=kh_0.
\]

Taking the maximum of this aggregate count and the local count in (9)
proves the label bound in (3).  Since original zero and ray factors still
consume labels and cone-coordinate dimensions,

\[
 D_{\rm amb}=T+2L
 \geq kp+1+2\bigl(kh_0+\mathbf1_{\{c\mid p\}}\bigr).
\]

On the reduced face,
\(\nu_F=2L_{\rm full}+L_{\rm ray}\), which proves the last part of (3).

For the heterogeneous statement, pointwise row-disjointness gives
\(L_{\rm full}\ge H_0\), while \(T_{\rm full}\ge P+1\) gives
\(L_{\rm full}\ge\lceil(P+1)/c\rceil\).  The unused capacity in the local
label bound is

\[
 W=cH_0-P=\sum_a\left(c\left\lceil\frac{p_a}{c}\right\rceil-p_a\right).
\]

If \(W=0\), equivalently \(c\mid p_a\) for every \(a\), the global bound
adds one label.  If \(W\ge1\), then \(cH_0\ge P+1\), so it adds none.
This proves (5a)--(5b).

For \(k=1\),

\[
 h_0+\mathbf1_{\{c\mid p\}}
 =\left\lceil\frac{p+1}{c}\right\rceil .
\]

Partition the \(p+1\) coordinates into groups \(G\) of size at most \(c\)
and impose

\[
 \left(\frac{1+y_G}{2},\frac{1-y_G}{2},x_G\right)
 \in Q_{|G|+2},\qquad \sum_G y_G=1.                      \tag{13}
\]

This projects exactly to \(B_2^{p+1}\), is proper, and has polynomial
contact factors.  It attains all four values in (4).

## 4. What is and is not settled for products

For pure \(Q_3\), (2)--(3) specialize to

\[
 T\geq kp+1,\qquad L_{\rm full}\geq kp+1,\qquad
 D_{\rm amb}\geq3(kp+1),\qquad \nu_F\geq2(kp+1).          \tag{14}
\]

Global \(C^1\) selections have the stronger exact values
\((T,L,D,\nu)=(k(p+1),k(p+1),3k(p+1),2k(p+1))\).
The proof of that additive theorem uses continuity of the contact
derivatives to make exact-label strata clopen and then applies a relative
top-class cover argument.  Everywhere differentiability supplies local
inversion only after a single label profile is nonsingular everywhere; it
does not make those derivative-defined strata closed.  Therefore the
present argument rigorously proves the strict \(+1\) gap (14), but does not
justify replacing it by \(+k\).

Nor is (14) a counterexample to the \(+k\) statement: no differentiable
non-\(C^1\) construction attaining \(kp+1\) is presently provided.  The
valid sharp conclusion is:

- Lipschitz contact selections can attain the unrestricted \(kp\)
  capacity by separate norm trees;
- everywhere differentiable selections require at least \(kp+1\);
- global \(C^1\) selections require and attain \(k(p+1)\).

For \(k=1\), the last two values coincide, giving the exact threshold (4).

## 5. QIPM scope

The theorem concerns a regularity cost of reusable, globally labelled
contact encodings.  It is not an intrinsic barrier lower bound for the
projected product of balls, and standard SOCP IPMs do not require such
selected boundary factors.  When an algorithm does require everywhere
differentiable normalized support states or contact charts, (2)--(4)
prevent it from claiming the saturated norm-tree resource count.

The barrier quantity is always the operational minimal-face parameter
\(\nu_F\).  The unreduced product value \(2L\) must not be inserted into an
iteration bound if the affine slice misses the product interior.

## 6. Literature boundary

The nonsmooth inverse theorem used above is due to Jean Saint Raymond,
[*Local inversion for differentiable functions and the Darboux
property*](https://doi.org/10.1112/S0025579300016132), *Mathematika* 49
(2002), 141--158.  It proves local inversion for everywhere
differentiable finite-dimensional maps with nowhere-vanishing Jacobian.
Tao gives a later expository proof in
[*The inverse function theorem for everywhere differentiable
maps*](https://terrytao.wordpress.com/2011/09/12/the-inverse-function-theorem-for-everywhere-differentiable-maps/).

Targeted searches located the nonsmooth inverse theorem, but no application
to cone slack factorizations, Lorentz phase-capacity saturation, or the
Lipschitz-versus-differentiable resource threshold above.  Novelty is
plausible pending specialist review.

## 7. Independent hostile audit

The audit passed the \(k>1\) strict \(+1\) theorem.  It checked that each
aggregate dual \(\widehat B_i=\sum_aB_i^a\) remains in its Lorentz cone and
that (10) is the exact aggregate slack.  The product-diagonal calculation
(10a)--(10c) gives positive-semidefinite rank-\(r_i\) Gram channels.  At
\(T_{\rm full}=kp\), equality in the rank budget makes every full component
nonvertex at every point and makes the stacked phase derivative \(DQ\) a
linear isomorphism everywhere.

Saint Raymond's finite-dimensional theorem has exactly the regularity used
here: everywhere Fréchet differentiability and a nowhere-singular
derivative, without derivative continuity.  Its application in manifold
charts gives a local homeomorphism.  Compactness upgrades this to a finite
covering.  The covering classification has no missed \(p\geq2\) case:
an \(S^1\) target factor gives a noncompact universal cover; without such a
factor the target is simply connected, and integral cohomology below degree
\(p\), degree-\(p\) rank, and total dimension force precisely \(k\) copies
of \(S^p\), contradicting \(r_i\leq c<p\).

The audit also checked the ceiling/divisibility arithmetic, the distinction
between original ambient dimension and the operational minimal-face barrier
parameter, and the grouped coordinate-square lift.  For \(k=1\), that lift
is proper, its group sizes sum to \(p+1\), and it simultaneously attains
all four values in (4).  For \(k>1\), no matching \(kp+1\) construction is
claimed.

The later heterogeneous audit checked that capacity saturation makes the
aggregate phase map a finite covering of products of spheres.  Circle
targets are excluded by their noncompact universal cover.  Otherwise both
products are simply connected, so the covering is a homeomorphism.  The
Poincaré-polynomial identity
\(\prod_a(1+t^{p_a})=\prod_i(1+t^{r_i})\) determines the exponent multiset:
read the smallest positive exponent and its multiplicity, divide out the
corresponding binomial factors, and iterate.  Thus the cap
\(c<\max_ap_a\) excludes saturation.  Finally, the unused local label
capacity is zero exactly when \(c\) divides every \(p_a\), which is exactly
the condition for the strict extra label in (5a).  No correction was
required.
