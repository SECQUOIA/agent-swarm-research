# A path-independent small-step lower bound for Lorentz norm trees

Status: Proved; core argument independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the fixed-lift, fixed-barrier, bounded-Dikin-chord model

## Result

The standard restricted barrier of a Lorentz norm tree has an actual
small-step iteration lower bound.  The argument is path-independent: after
starting near the analytic center, every later iterate may leave every
central neighborhood.

Let \(T\) be any rooted norm tree with \(N\geq2\) leaves and \(b\geq1\)
internal nodes.  Use one copy of the same tree for each of \(k\geq1\)
Euclidean balls.  For source ball \(a\) and internal node \(v\), write

\[
 q_{av}=t_{av}^2-
       \sum_{u\in I(v)}t_{au}^2-
       \sum_{j\in J(v)}w_{aj}^2,                           \tag{1}
\]

where \(I(v)\) and \(J(v)\) are its internal-child and leaf-child sets.
Fix every root coordinate to one and require that every block lies on the
positive Lorentz sheet: \(t_{av}>0\) and \(q_{av}>0\).  (The determinant
inequality alone would also admit the negative sheet and would not define
the convex norm-tree domain.)  Use

\[
                         F=-\sum_{a,v}\log q_{av}.          \tag{2}
\]

Put \(L=kb\).  For each \(a\), choose a unit vector
\(c_a\in\mathbb R^N\) with every coordinate strictly positive, and maximize

\[
                         \ell(w)=\sum_{a=1}^kc_a^Tw_a.     \tag{3}
\]

The maximum over the closed feasible lift is \(k\), uniquely attained in
the projected variables at \(w_a=c_a\).  Its norm-tree boundary fiber is
unique, every internal subtree norm is positive, and all \(L\) determinants
in (1) vanish there.  Equivalently, \(k\) is the supremum on the open
barrier domain.

Let \(\nu_T\) be the exact restricted parameter of one tree barrier.  By
the [companion exact-parameter
theorem](2026-09-04-norm-tree-reduced-barrier-parameter.md),

\[
 \nu_T=
 \begin{cases}
  2b-2,&\text{every root slot is an internal-child axis},\\
  2b-1,&\text{the root has a free leaf slot},
 \end{cases}
 \qquad \nu=k\nu_T.                                      \tag{3a}
\]

The last equality is exact because the \(k\) root slices are independent.

Let \(n_v\) be the number of internal nodes in the subtree rooted at \(v\).
The explicit analytic center \(\bar z\) is

\[
               \bar w_a=0,
 \qquad        \bar t_{av}^2={n_v\over b},
 \qquad        \bar q_{av}={1\over b}.                    \tag{4}
\]

Fix \(0\leq\rho<1\), \(0<R<1\), and an integer \(m\geq1\).  Start at any
\(x_0\) with \(\|x_0-\bar z\|_{\bar z}\leq\rho\).  Suppose each of \(S\)
outer rounds consists of at most \(m\) successive feasible chords, each
having local norm at its starting point at most \(R\).  Directions,
intermediate iterates, and all computation between chords are arbitrary.
If \(\epsilon>0\) and the final point \(x_S\) satisfies

\[
                         k-\ell(x_S)\leq\epsilon,           \tag{5}
\]

then

\[
 \boxed{
 S\geq
 {\left[
   {L\over\sqrt\nu}\log\!\left({k\over2\epsilon}\right)
   -\log{1\over1-\rho}
  \right]_+
  \over
  m\log{1\over1-R}}.}                                     \tag{6}
\]

Thus, with the one-sided center-to-optimum scale \(\Delta=k\), every such
method requires

\[
                  \Omega\!\left(\sqrt L
                         \log{\Delta\over\epsilon}\right) \tag{7}
\]

bounded-Dikin-step rounds whenever the logarithmic term dominates the fixed
initialization subtraction.  This holds for every tree shape and arity.
Moreover, the exact central path is tree-shape-independent and can be
partitioned into
\(O(\sqrt L\log(\Delta/\epsilon))\) such chords.  Hence the displayed
order is tight for the fixed barrier and fixed chord radius.
It is a lower bound for the fixed standard norm-tree barrier and this
bounded-feasible-chord algorithmic class, not for unrestricted IPMs or
QIPMs.

## 1. Telescoping determinants

For each source ball, every nonroot internal variable appears positively
in its own determinant and negatively in its parent's determinant.
Therefore

\[
                         \sum_vq_{av}=1-\|w_a\|^2.          \tag{8}
\]

For any feasible point \(y\), put

\[
                         \delta_a=1-c_a^Tw_a(y).
\]

Since \(\|w_a\|<1\) and \(\|c_a\|=1\), each \(\delta_a>0\).  If (5) holds,
then \(\sum_a\delta_a\leq\epsilon\), and

\[
 \sum_vq_{av}
 =1-\|w_a\|^2
 \leq1-(c_a^Tw_a)^2
 =\delta_a(1+c_a^Tw_a)
 \leq2\delta_a.                                           \tag{9}
\]

Apply AM--GM first to the \(b\) node determinants within each ball and
then to the \(k\) objective deficits.  Since \(L=kb\),

\[
 \prod_{a,v}q_{av}(y)
 \leq\prod_a\left({2\delta_a\over b}\right)^b
 \leq\left({2\epsilon\over kb}\right)^{kb}
 =\left({2\epsilon\over L}\right)^L.                      \tag{10}
\]

This estimate applies to the entire \(\epsilon\)-accurate set and uses no
central-path condition.

## 2. The barrier metric controls all log determinants

For one Lorentz block let \(f_v=-\log q_v\).  Its standard barrier parameter
is two, so the defining gradient inequality gives, for every linked tangent
direction \(\dot z\),

\[
                \bigl(d\log q_v[\dot z]\bigr)^2
                =\bigl(Df_v[\dot z]\bigr)^2
                \leq2D^2f_v[\dot z,\dot z].               \tag{11}
\]

Affine linking and restriction preserve (11).  Summing it over the blocks
gives the exact comparison needed here:

\[
 \|\dot z\|_{F,z}^2
 =\sum_{a,v}D^2f_{av}[\dot z,\dot z]
 \geq{1\over2}\sum_{a,v}
             \bigl(d\log q_{av}[\dot z]\bigr)^2.          \tag{12}
\]

Consequently every piecewise \(C^1\) feasible curve from \(x\) to \(y\)
has barrier-metric length at least

\[
 {1\over\sqrt2}
 \left\|\bigl(\log q_{av}(y)-\log q_{av}(x)\bigr)_{a,v}
 \right\|_2.                                               \tag{13}
\]

The factor \(1/\sqrt2\) is the only loss relative to the grouped
paraboloid barrier.  A termwise Hessian expansion does not have a manifestly
positive remainder for a Lorentz determinant; the parameter-two gradient
inequality bypasses that obstruction and remains valid after all links.

## 3. Distance from the analytic center to every accurate point

The identity \(n_v=1+\sum_{u\in I(v)}n_u\) proves (4)'s slack formula.
At \(w=0\), differentiation with respect to a nonroot \(t_{av}\) gives

\[
        -{2t_{av}\over q_{av}}+{2t_{av}\over q_{a,parent(v)}}=0,
\]

because all slacks equal \(1/b\); all leaf derivatives vanish.  Strict
convexity of (2) on the linked root slice makes (4) its unique analytic
center.

At \(\bar z\), every log determinant is \(-\log b\).  For an accurate
point \(y\), (10), Cauchy--Schwarz, and (13) give

\[
\begin{aligned}
 d_F(\bar z,y)
 &\geq {1\over\sqrt{2L}}
   \left|\sum_{a,v}\log{q_{av}(y)\over1/b}\right|\\
 &\geq
 \left[\sqrt{L/2}\log\!\left({k\over2\epsilon}\right)\right]_+.
                                                               \tag{14}
\end{aligned}
\]

The absolute value in the first line and the positive part in the second
handle the vacuous large-\(\epsilon\) regime.  Taking the infimum over all
accurate \(y\) proves the same lower bound on the distance to the entire
accurate set.

The exact total parameter in (3a) sharpens this guarantee.  Equation (10)
also says directly that

\[
 F(y)-F(\bar z)
 \geq L\log{L\over2\epsilon}-L\log b
 =L\log{k\over2\epsilon}.                              \tag{14a}
\]

The global gradient inequality
\(|DF[u]|\leq\sqrt\nu\,\|u\|_{F}\), integrated along any feasible curve,
therefore yields

\[
 d_F(\bar z,\{\mathrm{gap}\leq\epsilon\})
 \geq\left[{L\over\sqrt\nu}
             \log{k\over2\epsilon}\right]_+.           \tag{14b}
\]

Since \(\nu<2L\), (14b) strictly improves the universal Lorentz-block
constant in (14).  It also records the root topology: an all-internal root
has \(\nu_T=2b-2\), while a root leaf gives \(2b-1\).  At \(b=1\), it
recovers the direct-ball coefficient \(\sqrt{k}\) exactly.

### Entropy-sensitive heterogeneous refinement

The same theorem holds when source \(a\) uses its own tree with
\(b_a\geq1\) internal blocks and its own objective weight
\(\lambda_a>0\).  Put

\[
 L=\sum_ab_a,\qquad \nu=\sum_a\nu_a,\qquad
 p_a={b_a\over L},\qquad
 \Delta_{\rm eff}=\prod_a\left({\lambda_a\over p_a}\right)^{p_a},
 \tag{H1}
\]

and maximize \(\ell=\sum_a\lambda_ac_a^Tw_a\).  The separate analytic
centers still have \(q_{av}=1/b_a\).  If
\(e_a=\lambda_a(1-c_a^Tw_a)\), then accuracy gives
\(\sum_ae_a\leq\epsilon\), while telescoping and within-tree AM--GM give

\[
 \prod_v(b_aq_{av})
 \leq\left({2e_a\over\lambda_a}\right)^{b_a}.          \tag{H2}
\]

The weighted product on the right is maximized under
\(\sum_ae_a\leq\epsilon\) at \(e_a=\epsilon p_a\).  Therefore

\[
 \prod_{a,v}(b_aq_{av})
 \leq\left({2\epsilon\over\Delta_{\rm eff}}\right)^L,
 \qquad
 d_F(\bar z,\{\mathrm{gap}\leq\epsilon\})
 \geq\left[{L\over\sqrt\nu}
             \log{\Delta_{\rm eff}\over2\epsilon}\right]_+.
 \tag{H3}
\]

Consequently (6) remains valid after replacing
\(\log(k/(2\epsilon))\) by
\(\log(\Delta_{\rm eff}/(2\epsilon))\).  This identifies an effective
source count rather than losing all information to the largest or smallest
tree.  With equal objective weights,
\(\Delta_{\rm eff}=\exp(H(p))\), the exponential Shannon entropy of the
block-allocation proportions.  Equal tree sizes recover
\(\Delta_{\rm eff}=k\).  More generally,
\(\Delta_{\rm eff}\leq\sum_a\lambda_a\) by weighted AM--GM, with equality
exactly when the objective weights are proportional to the block counts.

## 4. Distance to bounded Dikin chords

If \(\|y-x\|_x=r\leq R<1\), self-concordant Hessian comparison along the
straight segment gives

\[
 \operatorname{length}_F([x,y])
 \leq\int_0^1{r\over1-tr}\,dt
 =-\log(1-r)
 \leq\log{1\over1-R}.                                     \tag{15}
\]

The same estimate bounds
\(d_F(\bar z,x_0)\leq\log(1/(1-\rho))\).  Concatenate all chords and use
the triangle inequality with (14b).  The resulting upper bound

\[
 d_F(\bar z,x_S)
 \leq\log{1\over1-\rho}
       +Sm\log{1\over1-R}                                 \tag{16}
\]

rearranges to (6).

## 5. Exact central path and matching bounded-chord upper construction

The same linked tree has a tree-shape-independent central path.  Let
\(z(\tau)\) minimize \(F-\tau\ell\), and let
\(C_{av}=\sum_{j\text{ below }v}c_{aj}^2\).  Stationarity in a nonroot
internal coordinate \(t_{av}>0\) gives

\[
 -{2t_{av}\over q_{av}}
 +{2t_{av}\over q_{a,\operatorname{parent}(v)}}=0.
\]

Hence every determinant in one tree equals a common \(q(\tau)\).  Leaf
stationarity then gives \(w_a=r(\tau)c_a\), where

\[
 D(\tau)=\sqrt{b^2+\tau^2},\qquad
 q(\tau)={2\over D(\tau)+b},\qquad
 r(\tau)={\tau\over D(\tau)+b}.                         \tag{C1}
\]

The remaining internal coordinates are uniquely

\[
                  t_{av}^2=n_vq(\tau)+r(\tau)^2C_{av}.   \tag{C2}
\]

Indeed, (C2) telescopes up each subtree, and its root equation is exactly
\(bq+r^2=1\).  Strict convexity makes this stationary point the unique
central point.  At \(\tau=0\), (C1)--(C2) recover the analytic center (4).

Differentiated central stationarity gives
\(H_\tau z'(\tau)=\nabla\ell\).  Therefore the squared speed per unit
\(\log\tau\) is

\[
 \beta(\tau)^2
 =\tau^2{d\over d\tau}\ell(z(\tau))
 =L\left(1-{b\over\sqrt{b^2+\tau^2}}\right).             \tag{C3}
\]

This is independent of every feature of the tree except its block count.
It is also exactly the speed of the \(b\)-group smooth lift.  Put

\[
 y(r)={r\over\sqrt{1+r^2}},\qquad
 \Phi(y)=\sqrt2\,\operatorname{artanh}(\sqrt2y)
                    -\operatorname{artanh}(y).
\]

Since \(\tau=2br/(1-r^2)\), integration of (C3) gives the exact arc length
from the center to the point with scalar profile \(r\):

\[
                  \mathcal L(0,r)=\sqrt{2L}\,\Phi(y(r)). \tag{C4}
\]

For objective error \(\epsilon\in(0,k)\), take
\(r_\epsilon=1-\epsilon/k\).  Then

\[
 \mathcal L(0,r_\epsilon)
 =\sqrt L\log{k\over\epsilon}+O(\sqrt L)
 \quad(\epsilon/k\downarrow0).                           \tag{C5}
\]

This arc produces a matching feasible-chord upper construction.  If a
metric arc segment has length \(a\), self-concordant norm transport along
the arc gives

\[
 \|x_{\rm end}-x_{\rm start}\|_{x_{\rm start}}
 \leq\int_0^a e^s\,ds=e^a-1.
\]

Partitioning the central arc into pieces of length at most
\(\log(1+R)\) therefore yields straight feasible chords of starting-point
local norm at most \(R\).  Thus an accurate point is reachable in

\[
 K\leq
 \left\lceil{\sqrt{2L}\,\Phi(y(1-\epsilon/k))
                    \over\log(1+R)}\right\rceil          \tag{C6}
\]

such chords.  Together with (6) at \(\rho=0,m=1\), this proves that the
minimum number of bounded feasible Dikin chords for this fixed barrier is
\(\Theta(\sqrt L\log(k/\epsilon))\) as
\(\epsilon/k\downarrow0\).  The lower bound is path-independent, while
the exact central path supplies the matching-order witness.

More precisely, if \(K_R^*(\epsilon)\) is the minimum over all such chord
paths and \(K_R^{\rm cp}(\epsilon)\) is the count from (C6), then

\[
 \limsup_{\epsilon/k\downarrow0}
 {K_R^{\rm cp}(\epsilon)\over K_R^*(\epsilon)}
 \leq
 \sqrt{\nu\over L}\,
 {\log(1/(1-R))\over\log(1+R)}
 <\sqrt2\,
 {\log(1/(1-R))\over\log(1+R)}.                         \tag{C7}
\]

Thus even arbitrary off-path shortcuts improve on the central path by at
most a constant depending only on the permitted Dikin radius; the
tree-dependent part of that constant is strictly below \(\sqrt2\).

## 6. Novelty and scope

The proof adapts the log-slack geodesic method introduced in
[the grouped-ball small-step theorem](2026-09-04-grouped-ball-short-step-iteration-lower-bound.md).
The new ingredients are the exact tree telescoping identity (8), the
shape-independent center (4), and use of the Lorentz parameter-two gradient
inequality to obtain the simultaneous log-determinant estimate (12).  The
exact reduced parameter strengthens the resulting distance constant, while
the all-determinants-equal stationarity law gives a shape-independent
central path and a matching bounded-chord construction.

The self-concordant gradient inequality, Hessian comparison, and Dikin
containment are classical; see
[[nesterov1994-interior-point-polynomial-algorithms-convex]] p.12-18,
p.31-48.  The use of Riemannian distance as a lower bound for short-step
methods is also classical: Nesterov and Nemirovski, *Primal Central Paths
and Riemannian Distances for Convex Sets*, Foundations of Computational
Mathematics 8 (2008), 533--560,
DOI [10.1007/s10208-007-9019-4](https://doi.org/10.1007/s10208-007-9019-4).
The claim here is narrower: the explicit distance to the **entire**
accurate set for the linked norm-tree barrier, obtained from simultaneous
control of every tree determinant.  The general 2008 theorem compares
central-path length to geodesic distance within a factor
\(O(\nu^{1/4})\).  Here the special norm-tree geometry gives the
dimension-independent asymptotic factor
\(\sqrt{\nu/L}<\sqrt2\) before chord-discretization constants, and compares
to the whole accurate set rather than only the endpoint.  A targeted search
of the local corpus and the cited Riemannian-distance literature found no
earlier bound of this form.  Priority remains subject to specialist
literature review.

The theorem permits arbitrary classical or quantum computation between
accepted moves, but it assumes that progress in the classical primal
iterate is realized by a fixed number of feasible chords of uniformly
bounded starting-point Dikin norm.  It does not cover long steps, infeasible
iterates, a change of lift or barrier, coherent progress with no such primal
trajectory, or an output-only lower bound.  The result is exact-real
geometric; finite-precision implementation and conditioning are separate.

## 7. Audit record

An independent hostile audit verified the Lorentz gradient inequality
(11) after affine linking, the telescoping identity, both AM--GM steps, the
analytic-center formula for every rooted tree shape, and the conversion of
Riemannian distance to bounded Dikin chords.  It also checked the fully
active positive objective, the \(1/\sqrt2\) constant, and strict convexity
on the linked positive-sheet domain.  No central-path assumption is used
after initialization.  A separate hostile check verified the heterogeneous
weighted-product optimization, exact parameter additivity, the
barrier-height sharpening, and every constant in (H1)--(H3).
It also verified the exact central profile and speed (C1)--(C3), the arc
integral (C4), and the self-concordant arc-partition estimate leading to
(C6).  Equation (C7) is their direct asymptotic ratio.
