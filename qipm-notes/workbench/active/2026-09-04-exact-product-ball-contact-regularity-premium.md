# Exact contact-regularity premium for Lorentz lifts of product balls

Status: Proved; literature-screened; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

## Executive theorem

Let

\[
 C=(B_2^s)^k,\qquad s\geq3,\qquad k\geq1,\qquad
 p=s-1,
\]

and impose a Lorentz block-dimension cap \(d\geq3\).  Put

\[
 c=d-2,\qquad h_0=\left\lceil {p\over c}\right\rceil .
\]

Consider arbitrary finite-dimensional exact affine lifts over
\(\prod_{i=1}^LQ_{m_i}\), \(3\leq m_i\leq d\).  No Slater hypothesis and no
global regularity of their boundary fibers are imposed.  Write

\[
 T=\sum_{i=1}^L(m_i-2),\qquad
 D_{\rm amb}=\sum_{i=1}^Lm_i=T+2L .
\]

For a lift without Slater, barrier complexity is charged after the
minimal-face reduction in Section 1.  If \(L_{\rm full}\) coordinate faces
are full Lorentz cones and \(L_{\rm ray}\) are rays, the reduced product
cone has exact normal-barrier parameter

\[
             \nu_F=2L_{\rm full}+L_{\rm ray};             \tag{0}
\]

zero faces are omitted.  This is the operational parameter for an IPM on
the reduced lift.  The unreduced ambient product itself has parameter
\(2L\), but when Slater fails the restriction of its standard barrier to
the affine slice has empty domain.

All minima denoted by \(\nu_{F,0}\) and \(\nu_{F,1}\) below refer to this
operational minimal-face parameter.

Then the simultaneous exact unrestricted minima are

\[
 \boxed{
 T_0=kp,\qquad L_0=kh_0,\qquad
 D_0=k(p+2h_0),\qquad \nu_{F,0}=2kh_0.}                   \tag{1}
\]

Separate arbitrary-arity Lorentz norm trees attain all four values.  They
can be chosen with globally labelled Lipschitz primal and dual factors on
the full extreme slack operator.

The independently audited
[everywhere-differentiable contact-gap theorem](2026-09-04-everywhere-differentiable-lorentz-contact-gap.md)
shows that this Lipschitz endpoint is sharp for one ball: everywhere
Fréchet differentiable factors already require total capacity \(p+1\) and
attain the regular values below.  For \(k>1\), everywhere differentiability
forces at least \(kp+1\), while the full additive \(k(p+1)\) conclusion
below still uses global \(C^1\) regularity.

Now require the lift to admit globally labelled \(C^1\) primal and dual
factors on the full extreme slack operator.  If \(c<p\), put

\[
 h_1=\left\lceil {p+1\over c}\right\rceil
     =\left\lceil {s\over d-2}\right\rceil .
\]

The simultaneous exact contact-regular minima are

\[
 \boxed{
 T_1=k(p+1)=ks,\qquad L_1=kh_1,\qquad
 D_1=k(p+1+2h_1),\qquad \nu_{F,1}=2kh_1.}                 \tag{2}
\]

If \(c\geq p\), one direct \(Q_{p+2}=Q_{s+1}\) factor per ball is allowed,
is globally analytic, and both classes have the same exact quadruple

\[
 \boxed{(T,L,D_{\rm amb},\nu_F)=(kp,k,k(p+2),2k).}        \tag{3}
\]

Thus the exact regularity premium in the nontrivial small-cap regime is

\[
\begin{aligned}
 \Delta T&=k,\\
 \Delta L&=k\delta,\qquad
 \Delta D=k(1+2\delta),\qquad
 \Delta\nu_F=2k\delta,                                    \tag{4}\\
 \delta&=\mathbf1_{\{c\mid p\}} .
\end{aligned}
\]

For pure \(Q_3\) lifts, \(c=1\), so the premium is exactly

\[
                 (\Delta T,\Delta L,\Delta D,\Delta\nu_F)
                            =(k,k,3k,2k).                  \tag{5}
\]

Equations (1)--(5) separate two notions that are often conflated.  Every
finite-dimensional affine Lorentz lift has semialgebraic primal and dual
data, hence generically analytic selected factors; this is enough for the
local capacity lower bound (1), but not for the global topological
increment.  A globally selected \(C^1\) contact factorization costs exactly
(4).  Requiring both selected factor maps merely to be globally Lipschitz
does not create any premium: the norm trees already attain (1) with that
regularity.

## 1. Minimal-face reduction and one common regular stratum

Let \(K=\prod_iQ_{m_i}\), and write an exact lift as

\[
                 C=\pi\bigl((w_0+\mathcal L)\cap K\bigr).  \tag{6}
\]

This finite-dimensional affine representation is automatically
semialgebraic.  Arbitrary real entries in \(w_0,\mathcal L\), and \(\pi\)
are allowed as parameters in the defining polynomial formulas; no
rationality or separately imposed definability assumption is needed.
This also covers conventions that allow additional free variables.  In a
formulation

\[
 x=Pw+Qu+p_0,\qquad Aw+Bu=b,\qquad w\in K,
\]

boundedness of \(C\) forces \(\ker B\subseteq\ker Q\), since otherwise a
free feasible line would have an unbounded image.  Hence \(Q=RB\) for some
linear \(R\), and on the feasible set
\(x=(P-RA)w+Rb+p_0\); the condition \(b-Aw\in\operatorname{im}B\) is just
an affine constraint on \(w\).  Thus free variables can be eliminated
without changing any cone block or resource count, giving (6).

Put \(\mathcal S=(w_0+\mathcal L)\cap K\), choose
\(\bar w\in\operatorname{ri}\mathcal S\), and let \(F\) be the minimal face
of \(K\) containing \(\bar w\).  Then \(\mathcal S\subseteq F\).  Indeed,
for any \(w\in\mathcal S\), relative interiority lets the segment from
\(w\) through \(\bar w\) extend slightly to a point of \(\mathcal S\);
the face property then puts \(w\) in \(F\).  Moreover
\(\bar w\in\operatorname{ri}F\), so the same affine slice is a proper lift
over \(F\), viewed in \(\operatorname{span}F\).

Every face of a product is a product of coordinate faces, and the only
faces of a Lorentz cone of dimension at least three are the zero face, an
extreme ray, and the full cone.  Consequently

\[
 F=\prod_iF_i,\qquad
 F_i\in\{\{0\},\ \mathbb R_+v_i,\ Q_{m_i}\}.              \tag{6a}
\]

This is a fixed semialgebraic cone.  Relative Slater regularity and the
lift/factorization theorem give factors of the full slack

\[
 1-x_a^Tz=\sum_{i=1}^L
       \langle A_i(x),B_i^a(z)\rangle,
 \quad x\in M:=(S^p)^k,\quad z\in S^p,\quad a\in[k].       \tag{7}
\]

The factors may be selected semialgebraically.  Indeed, the primal fiber
correspondence

\[
 x\longmapsto\{w\in(w_0+\mathcal L)\cap K:\pi(w)=x\}
\]

is semialgebraic and nonempty.  For a polar extreme row \(e_a\otimes z\),
the relative conic-dual certificate set over \(F\) is also a nonempty
semialgebraic correspondence: relative Slater gives attainment, and its
defining cone membership and affine equations depend polynomially on
\(z\).  Semialgebraic choice therefore supplies the maps in (7), with
values in the coordinate factors of \(F\) and their relative duals.

Every semialgebraic map is real analytic on a dense open subset of its
domain after a finite Nash stratification.  Hence there are dense open sets

\[
 U\subseteq M,\qquad V_a\subseteq S^p\quad(a\in[k])
\]

on which all primal factors and, respectively, all row-\(a\) dual factors
are analytic.  The set

\[
                 U_*:=U\cap\bigcap_{a=1}^k\pi_a^{-1}(V_a) \tag{8}
\]

is a finite intersection of dense open semialgebraic subsets of \(M\):
each product projection \(\pi_a:M\to S^p\) is open and surjective, so
\(\pi_a^{-1}(V_a)\) is dense.  Hence \(U_*\) is nonempty.  Fix
\(x\in U_*\).  All
contact derivatives below are simultaneously legitimate at
\((x,x_1),\ldots,(x,x_k)\).  This common-point step is why separate generic
strata for the primal and polar selections suffice.

## 2. Pointwise row-disjoint capacity

Put \(r_i=m_i-2\).  At contact, nonnegativity and (7) give

\[
                   \langle A_i(x),B_i^a(x_a)\rangle=0.     \tag{9}
\]

Define

\[
 H_i^a(x)(u,v)=
  -\langle D_aA_i(x)[u],DB_i^a(x_a)[v]\rangle ,
 \qquad u,v\in T_{x_a}S^p.                                \tag{10}
\]

Mixed differentiation of (7) gives

\[
                         g_{S^p,x_a}=\sum_iH_i^a(x).       \tag{11}
\]

If \(F_i=Q_{m_i}\), then \(H_i^a\) is positive semidefinite and has rank at
most \(r_i\).  At a cone vertex the corresponding derivative vanishes
because the Lorentz cone is pointed.  Otherwise the complementary factors
have positive scales and one common phase \(q_i\in S^{r_i}\); scale
derivatives cancel and

\[
                    H_i^a=\alpha_i\beta_i^a(Dq_i^a)^*Dq_i^a.
                                                                    \tag{12}
\]

If \(F_i\) is a ray, its primal and dual factors are complementary
nonnegative scalars.  At least one is zero at contact, and its derivative
vanishes because a differentiable nonnegative function has zero derivative
at a zero.  Thus \(H_i^a=0\).  A zero face is trivial.  Hence only original
blocks whose minimal-face component is the full \(Q_{m_i}\) can carry
contact curvature.

The active labels of two source rows are disjoint at this same point.  If
\(H_i^a(x)\neq0\), then \(A_i(x)\) and \(B_i^a(x_a)\) are nonzero.  Holding
\(x_a\) fixed in (9) while varying a different block \(x_b\) pins the
projective ray of \(A_i\), so \(D_bq_i(x)=0\).  Equation (12), including
the vertex cases, gives

\[
 H_i^a(x)\neq0\quad\Longrightarrow\quad H_i^b(x)=0
 \qquad(b\neq a).                                         \tag{13}
\]

Since the metric in (11) has rank \(p\),

\[
 \sum_{i:H_i^a(x)\neq0}r_i\geq p,\qquad
 \#\{i:H_i^a(x)\neq0\}\geq\left\lceil{p\over c}\right\rceil.
                                                                    \tag{14}
\]

Here the active indices necessarily have \(F_i=Q_{m_i}\).  Summing (14)
over the pointwise disjoint active sets proves

\[
                         T\geq kp,\qquad L\geq kh_0.       \tag{15}
\]

These are bounds for the original lift: ray and zero minimal-face
components still consume their original block capacity \(m_i-2\) and one
original label, so discarding them from the curvature sum can only weaken
the resource lower bounds.

It follows that

\[
                         D_{\rm amb}=T+2L\geq k(p+2h_0).   \tag{16}
\]

After facial reduction, the operational cone is
\(\prod_{F_i\ {\rm full}}Q_{m_i}\times\mathbb R_+^{L_{\rm ray}}\); zero
faces disappear.  Its optimal logarithmically homogeneous
self-concordant (normal) barrier parameter, even among coupled barriers,
is \(\nu_F\) in (0).  The product of the standard Lorentz and scalar-log
barriers attains this value.  Conversely, restrict any coupled normal
barrier to a two-dimensional orthant section of each full Lorentz factor
and to every ray factor.  The resulting orthant has dimension
\(2L_{\rm full}+L_{\rm ray}\), which gives the matching lower bound.

Every active set counted in (14) consists of full-face components, and
the rowwise active sets are disjoint.  Hence
\(L_{\rm full}\geq kh_0\), so \(\nu_F\geq2kh_0\).  This is the
operational barrier lower bound in (1).  Although the unreduced product
cone has parameter \(2L\), its barrier is not available to an IPM when the
affine slice misses the cone interior.

This proves every lower bound in (1).  Notice that no continuity is required
away from the one common regular stratum.  In particular, codimension-two
norm-tree singularities are allowed.

## 3. Arbitrary-arity norm trees attain the unrestricted bounds

For one ball, choose positive integers

\[
                       r_1+\cdots+r_{h_0}=p,\qquad
                       1\leq r_j\leq c,                    \tag{17}
\]

for example \(r_1=\cdots=r_{h_0-1}=c\) and
\(r_{h_0}=p-(h_0-1)c\).  Put \(b_j=r_j+1\).  A rooted tree with
\(s=p+1\) leaves and internal
outdegrees \(b_1,\ldots,b_{h_0}\) exists: starting from one leaf, replace a
leaf successively by \(b_j\) children.  The number of leaves increases by
\(\sum_j(b_j-1)=p\).

Leaves carry the signed coordinates \(x_\ell\), every proper internal node
has an auxiliary scalar \(t_v\), and the root scalar is fixed to
\(t_{\rm root}=1\).  The auxiliary variables become descendant-coordinate
norms on the boundary; they are not defined to be those norms throughout
the affine formulation.

For an internal node of outdegree \(b_v\), impose

\[
              \left(t_v,(t_w)_{w\text{ child of }v}\right)
                    \in Q_{b_v+1}=Q_{r_v+2}.               \tag{18}
\]

All blocks respect the cap \(r_v+2\leq d\).  The squared cone slacks
 telescope:

\[
 1-\|x\|^2
   =\sum_{v\ {\rm internal}}
      \left(t_v^2-\sum_{w\text{ child of }v}t_w^2\right).  \tag{19}
\]

Thus the lift projects exactly to \(B_2^s\).  At a boundary point every
summand in (19) is nonnegative and their sum is zero, so every cone
constraint is tight.  Induction and nonnegative leading coordinates give
the unique boundary fiber \(t_v=\|x_{S_v}\|\).  At \(x=0\), choose
\(0<\rho<1/\sqrt{d-1}\) and set
\(t_v=\rho^{\operatorname{depth}(v)}\) at every proper internal node.  With
the leaf coordinates zero, every cone inequality, including the root one,
is strict, so this is a Slater point.

There are \(h_0\) full factors, total capacity \(\sum r_j=p\), ambient
dimension \(p+2h_0\), and operational barrier parameter \(2h_0\).  Taking
\(k\) separate trees proves attainability in (1).

The matching full-slack factors have stronger regularity than continuity.
For \(x,z\in S^p\), let \(t_v(x)=\|x_{S_v}\|_2\) at every internal node,
let \(t_\ell(x)=x_\ell\) at a leaf, and use \(t_{\rm root}=1\).  For every
internal node define

\[
\begin{aligned}
 A_v(x)&=\left(t_v(x),(t_w(x))_{w\text{ child of }v}\right),\\
 B_v(z)&=\left(t_v(z),(-t_w(z))_{w\text{ child of }v}\right).
                                                               \tag{19a}
\end{aligned}
\]

Both vectors lie in \(Q_{b_v+1}\), and cancellation of every nonroot
internal term gives

\[
 \sum_{v\ {\rm internal}}\langle A_v(x),B_v(z)\rangle
 =t_{\rm root}(x)t_{\rm root}(z)-\sum_{\ell=1}^sx_\ell z_\ell
 =1-x^Tz.                                                   \tag{19b}
\]

For the product of balls, the primal factors for a node in tree \(a\) use
\(x_a\); the row-\(a\) dual factors use \(z\) in that tree and are the cone
vertex in every other tree.  Thus (19b) is the full factorization (7).

Every leaf coordinate is linear, and every subtree norm is
\(1\)-Lipschitz.  More precisely, because the child subtrees partition
\(S_v\),

\[
 \|A_v(x)-A_v(x')\|_2,\ \|B_v(x)-B_v(x')\|_2
 \leq\sqrt2\,\|x_{S_v}-x'_{S_v}\|_2.                       \tag{19c}
\]

Consequently the concatenated factor maps of an \(h_0\)-node tree are
globally \(\sqrt{2h_0}\)-Lipschitz; the same bound holds for the product
primal map and for each polar-row dual map with the natural product
Euclidean metrics.  They are semialgebraic and analytic wherever no proper
internal subtree vanishes.  When \(h_0>1\), a proper subtree norm is not
differentiable on its nonempty zero set, so these displayed selections are
not globally \(C^1\).  This proves sharply that global Lipschitz regularity cannot
replace global \(C^1\) regularity in the premium theorem.

## 4. The globally \(C^1\) frontier

The independently audited
[top-class no-sharing theorem](2026-09-04-c1-euler-no-sharing-product-balls.md)
applies to globally labelled \(C^1\) factors of (7).  When \(c<p\), its
capacity and label bounds are

\[
                         T\geq k(p+1),\qquad
                         L\geq k\left\lceil{p+1\over c}\right\rceil.
                                                                    \tag{20}
\]

As in Section 2, every label carrying the capacity in this argument has a
full Lorentz minimal-face component.  Thus the stronger count
\(L_{\rm full}\geq kh_1\) holds and (0) gives
\(\nu_F\geq2kh_1\), even if unused ray or zero components are present.

Their proof does not continue individual channels.  Instead, Lorentz
positivity gives pointwise row-disjoint active capacity.  If total capacity
or label count is below (20), the exact-activity sets cover \(M\).  On every
finite clopen label stratum, the joint dual phase map is locally
diffeomorphic from a proper open subset of \(S^p\) to a product of spheres.
The ordinary top class of \(S^p\) therefore vanishes on each corresponding
open cover piece.  The relative cup product would force the product of the
\(k\) sphere top classes to vanish, contradicting the fundamental class of
\((S^p)^k\).

Grouped coordinate-square factors attain (20).  Partition the \(s=p+1\)
coordinates into \(h_1\) nonempty groups \(G\), \(|G|\leq c\), and use

\[
\begin{aligned}
 A_G(x)&=\left({1+\|x_G\|^2\over2},
               {1-\|x_G\|^2\over2},x_G\right),\\
 B_G(z)&=\left({1+\|z_G\|^2\over2},
              -{1-\|z_G\|^2\over2},-z_G\right)
              \in Q_{|G|+2}.                              \tag{21}
\end{aligned}
\]

Their pairing is \(\|x_G-z_G\|^2/2\).  Separate groups and source balls
therefore attain (2) with polynomial, globally nonzero primal factors and
globally \(C^\infty\) dual components (inactive components are identically
the cone vertex).  More explicitly, these are the boundary factors of the
affine lift

\[
 \left({1+y_G\over2},{1-y_G\over2},x_G\right)
       \in Q_{|G|+2},\qquad \sum_Gy_G=1.                  \tag{21a}
\]

A block in (21a) is feasible exactly when
\(y_G\geq\|x_G\|^2\), so the projection is the ball.  On the sphere every
inequality is tight, which gives \(A_G(x)\) in (21).  Because \(c<p\)
implies \(h_1\geq2\), \(x=0,\ y_G=1/h_1\) is a Slater point.

When \(c\geq p\), the direct factors

\[
                 A_a(x)=(1,x_a),\qquad
                 B_a^b(z)=\mathbf1_{\{a=b\}}(1,-z)
                 \quad\text{in }Q_{p+2}                   \tag{22}
\]

are allowed and attain (3).  Pointwise capacity and row-disjointness give
the matching lower bounds \(T\geq kp\), \(L\geq k\).  This includes the
edge \(c=p\), where the tempting formula
\(\lceil(p+1)/c\rceil=2\) is inapplicable: one full-capacity
\(Q_{p+2}\) phase is globally valid.

## 5. Exact premium arithmetic

For \(c<p\),

\[
 \left\lceil{p+1\over c}\right\rceil
 -
 \left\lceil{p\over c}\right\rceil
 =
 \begin{cases}
 1,&c\mid p,\\
 0,&c\nmid p.
 \end{cases}                                               \tag{23}
\]

Subtracting (1) from (2) gives (4).  The dimension premium is always at
least one coordinate per source ball because global contact regularity
forces one additional unit of Lorentz phase capacity.  Factor count and
operational barrier parameter jump only when the unrestricted last block was
already full.

For \(d=3\), every capacity is one, so all four resources jump.  Separate
binary norm trees have

\[
 (T,L,D,\nu_F)=\bigl(k(s-1),k(s-1),3k(s-1),2k(s-1)\bigr),
\]

whereas globally \(C^1\) coordinate-square lifts have

\[
 (T,L,D,\nu_F)=(ks,ks,3ks,2ks).
\]

## 6. QIPM meaning and limitations

For bounded \(d\), both matching constructions are sparse: each cone block
touches at most \(d\) local variables, and tree or partial-sum equalities
can be organized with bounded incidence.  After minimal-face reduction,
the exact operational parameters \(\nu_F\) therefore enter standard IPM
and QIPM iteration upper bounds as
\(O(\sqrt{\nu_F}\log(1/\epsilon))\).  For both matching constructions every
face is full, so \(\nu_F\) equals the displayed \(\nu_{F,0}\) or
\(\nu_{F,1}\).  Equation (4) is a precise formulation cost of demanding
globally regular extreme-contact selections.

It is not an intrinsic barrier lower bound for the projected body or its
affine slice, nor a lower bound for formulations outside the stated
bounded-block Lorentz-product class.  Standard conic algorithms do not
require globally \(C^1\) boundary selections, and the norm trees in Section
3 are valid, strictly feasible SOCP formulations.  Consequently the
regular value (2) must not be inserted into an unrestricted QIPM lower
bound.  The theorem instead gives an exact boundary between:

- resource-optimal but singular norm-tree formulations, and
- globally contact-regular formulations to which covering and phase
  topology apply.

The difference is algorithmically relevant when a proposed QIPM analysis
uses smooth global boundary encodings, reusable normalized support states,
or uniform contact charts.  Such an assumption has the exact operational
cost (4); without it, the smaller resource law (1) is attainable.

For pure \(Q_3\) and fixed \(s\), both barriers still scale linearly in
\(k\), and the usual iteration bounds differ only by the exact factor
\(\sqrt{s/(s-1)}\).  Both tree and grouped-coordinate formulations also
admit linear-size sparse Newton systems.  The theorem therefore does not
create an asymptotic quantum advantage or disadvantage by itself; its role
is to prevent a regularity-conditional lower bound from being misreported
as a formulation-independent QIPM cost.

## 7. Literature boundary

The lift/slack-factorization correspondence is due to Gouveia, Parrilo, and
Thomas, [*Lifts of convex sets and cone
factorizations*](https://doi.org/10.1287/moor.1120.0575).  The elementary
minimal-face argument in Section 1 supplies the required properness before
that correspondence is invoked.  Fawzi's
[second-order-cone factorization
framework](https://doi.org/10.1007/s10107-018-1233-0) provides the standard
SOC-rank language.  Lorentz norm trees are standard modeling devices; the
new claim is not their existence.  The semialgebraic-choice and dense Nash
stratification steps are standard consequences of semialgebraic geometry;
see Bochnak, Coste, and Roy,
[*Real Algebraic Geometry*](https://doi.org/10.1007/978-3-662-03718-8).

Two closer formulation sources still do not supply the regularity premium.
[Kobayashi--Kim--Kojima, *Sparse Second Order Cone Programming
Formulations for Convex Optimization
Problems*](https://doi.org/10.15807/jorsj.51.241) compares auxiliary-variable
SOCP formulations and their Schur-complement sparsity, but gives no exact
dimension-capped factor lower bound and imposes no global contact-selection
regularity.  [Aubrun--La Piana--Müller-Hermes, *Factorization Through
Lorentz Cones*](https://arxiv.org/abs/2606.27825) studies positive linear
maps through direct sums of Lorentz cones, not nonlinear slack factors or
globally labelled boundary support maps.

Targeted searches did not locate the exact comparison (1)--(5), the common
dense-stratum pointwise row-disjoint lower bound for product balls, or the
global-contact regularity premium.  Novelty is plausible pending specialist
review, but only under the explicit factorization/selection hypotheses;
neither sparse SOCP formulation theory nor general cone factorization turns
it into an unconditional IPM lower bound.  The unrestricted theorem covers
arbitrary finite-dimensional exact
affine lifts: their real affine and Lorentz data are automatically
semialgebraic, and reduction to the minimal product face supplies relative
Slater, definable primal and dual selections, and a common Nash stratum.
The regular theorem is a selected-factor theorem; its transfer to a lift
requires the displayed global \(C^1\) selections.

## 8. Independent hostile audit

An independent audit passed the removal of the Slater hypothesis.  A
relative-interior feasible point puts the whole affine feasible slice in
its minimal face and makes the reduced lift proper.  Every product-Lorentz
minimal face splits into full Lorentz cones, rays, and zero factors.
Relative Slater duality gives nonempty attained certificate
correspondences; primal fibers and dual certificates are semialgebraic, so
definable choice applies.  A finite Nash stratification gives dense open
analytic loci, and their finite pullback intersection in (8) supplies one
common contact point for every row.  Ray and zero factors have zero mixed
contact curvature; original blocks restricted to such faces still count
toward \(T,L,D_{\rm amb}\).  The operational facially reduced cone has
normal-barrier parameter \(2L_{\rm full}+L_{\rm ray}\), and every
curvature-active factor is full, so it still obeys the displayed lower
bound.  Thus facial reduction loses no claimed resource minimum.  The
full-cone vertex derivative and pointwise
row-disjointness arguments were also rechecked.

The same audit found that “semialgebraic lift” was an unnecessary
qualification.  Under the finite-dimensional representation (6), affine
sets, Lorentz membership, primal fibers, and relative dual-certificate
sets are semialgebraic with arbitrary real coefficients as parameters.
Any explicit free variables reduce to (6) by the bounded-image kernel
argument given in Section 1.
Tarski--Seidenberg and semialgebraic choice therefore give the selections
used above without any extra hypothesis.  Closedness causes no gap: the
minimal face is closed, the reduced slice has relative Slater, every polar
support value is finite and attained through the exact projection, and
conic strong duality supplies attained dual certificates after redundant
affine equations are removed.

The audit also passed the arbitrary-arity norm-tree side: every partition of
\(p\) into positive capacities is realized by successive leaf expansions,
the squared slacks telescope, boundary nonnegativity forces the unique norm
fiber, and geometrically decreasing positive internal values give Slater
feasibility.  The residual block and all \(T,L,D_{\rm amb},\nu_F\) counts are
correct.  The bilinear node factors (19a) telescope to every full product-
ball slack row.  Subtree norms and signed leaf coordinates give globally
Lipschitz primal and dual factor maps, with the explicit bounds (19c), while
a proper zero subtree destroys differentiability.  Thus the unrestricted
minimum remains exact even under global Lipschitz selection regularity.

Finally, the edge \(c=p\), the ceiling identity (23), and the premium
arithmetic were checked directly.  The imported top-class theorem has
exactly the globally labelled bi-\(C^1\) hypotheses used here, and the
explicit affine lift (21a) simultaneously attains its capacity, label, and
dimension bounds with Slater feasibility.  The normal-barrier claim is
correctly scoped to the minimal-face product, including coupled barriers
via orthant restriction; the unreduced product value \(2L\) is the barrier
parameter of the ambient cone, not an operational parameter for the
non-Slater slice.  Neither the unrestricted nor regular quadruple is
presented as an intrinsic projected-body or iteration lower bound.
