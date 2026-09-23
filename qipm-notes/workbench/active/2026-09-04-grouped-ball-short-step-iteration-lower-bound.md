# A path-independent small-step iteration lower bound for grouped ball lifts

Status: Proved; headline and supporting tube theorems independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

The grouped product-ball barrier admits an actual iteration lower bound
that is stronger than a central-path statement.  From one late central
start, every algorithm assembled from bounded local-norm moves needs
\(\Omega(\sqrt L\log(\Delta/\epsilon))\) moves, even if all later iterates
leave every central neighborhood.  The conclusion does not follow from the
barrier parameter alone.

Let \(C=(B_2^s)^k\).  Partition each source ball into \(h\) nonempty
coordinate groups and put \(L=kh\).  On the grouped lift interior

\[
 \Omega=\left\{(s_{aG},w_{aG}):
 q_{aG}:=s_{aG}-\|w_{aG}\|^2>0,
 \quad\sum_Gs_{aG}=1\quad(a\in[k])\right\},             \tag{1}
\]

use the restricted standard barrier

\[
                         F=-\sum_{a,G}\log q_{aG}.       \tag{2}
\]

For each \(a\), choose a unit vector \(c_a\in\mathbb R^s\) whose
restriction \(c_{aG}\) to every group is nonzero, and maximize

\[
                         \ell(w)=\sum_{a=1}^kc_a^Tw_a.   \tag{3}
\]

Its optimum is \(k\), and every group inequality is active at the unique
optimum.  Let \(z(\tau)\) minimize \(F-\tau\ell\) on \(\Omega\).

Here is the headline theorem.  Fix \(\tau_0\geq0\), put

\[
 \bar z=z(\tau_0),\qquad
 q_0={2\over\sqrt{h^2+\tau_0^2}+h}.
\]

Let \(0\leq\rho<1\), \(0<R<1\), and \(m\geq1\) be fixed.  Start at any
\(x_0\in\Omega\) with \(\|x_0-\bar z\|_{\bar z}\leq\rho\).  Suppose each
of \(T\) outer rounds consists of at most \(m\) successive chords, every
chord stays in \(\Omega\) and has starting-point local norm at most \(R\).
No centrality or path-parameter condition is imposed after \(x_0\).  If the
last point \(x_T\) satisfies \(k-\ell(x_T)\leq\epsilon\) for
\(\epsilon>0\), then

\[
 \boxed{
 T\geq {\left[
       \sqrt L\log\!\left({q_0L\over2\epsilon}\right)
       -\log{1\over1-\rho}\right]_+
       \over m\log{1\over1-R}}.}
\]

Here \([u]_+=\max\{u,0\}\).  At the analytic center \(\tau_0=0\),
\(q_0=1/h\), so the logarithm is \(\log(k/(2\epsilon))\).  This already
gives \(\Omega(\sqrt L\log(k/\epsilon))\) moves from the standard
initialization.  If \(\tau_0>0\), define

\[
 \Delta={L\over\tau_0},\qquad
 r_0={\tau_0\over\sqrt{h^2+\tau_0^2}+h};
\]

then \(q_0L/2=r_0\Delta\).  In particular, if
\(\tau_0\geq\alpha h\) for a fixed \(\alpha>0\), then
\(r_0\geq\alpha/(\sqrt{1+\alpha^2}+1)>0\), and the theorem gives

\[
                  T=\Omega\!\left(\sqrt L
                         \log{\Delta\over\epsilon}\right)
\]

whenever the logarithmic term dominates the fixed initialization
subtraction.  This covers arbitrary bounded-step classical or quantum
computation between moves; it is not restricted to a path-following
update rule.

The standard short-step method for the same barrier has
\(O(\sqrt L\log(k/\epsilon))\) iterations from its analytic-center
initialization, up to conventional constant-neighborhood and accuracy
normalizations.  Thus the dependence on \(L\) and \(\epsilon\) is matched
within the bounded-Dikin-move model.

For comparison and as a second proof under different hypotheses, the note
also records a tube-specific path-parameter theorem.  Fix constants
\(\alpha>0\), \(0\leq\rho<\gamma_\alpha\), \(0<R<1\), and a positive
integer \(m\), where

\[
 \gamma_\alpha:=1+\alpha-\sqrt{1+\alpha^2}\in(0,1).
\]

An \((\alpha,\rho,R,m)\)-bounded-substep tube sequence is a finite
sequence \((z_j,\tau_j)\) such that

\[
\begin{gathered}
 \alpha h\leq\tau_0\leq\tau_1\leq\cdots\leq\tau_T,\\
 \|z_j-z(\tau_j)\|_{z(\tau_j)}\leq\rho.             \tag{4}
\end{gathered}
\]

Moreover, each outer transition \(z_j\to z_{j+1}\) must admit points

\[
 x_{j,0}=z_j,x_{j,1},\ldots,x_{j,m_j}=z_{j+1},
 \qquad x_{j,i}\in\Omega,\quad 1\leq m_j\leq m,       \tag{5}
\]

with

\[
       \|x_{j,i+1}-x_{j,i}\|_{x_{j,i}}\leq R
       \qquad(0\leq i<m_j).                           \tag{6}
\]

All norms in (4)--(6) are the local Hessian norms of the fixed barrier
(2), restricted to the affine hull of (1).  The intermediate points need
not be central.  Thus a round may contain a predictor and one or more
correctors; their directions and all other internal computations are
arbitrary.

Define the initialization scale \(\Delta=L/\tau_0\).  If the final
iterate has primal objective error

\[
                            k-\ell(z_T)\leq\epsilon,     \tag{7}
\]

then

\[
 \boxed{
 T\geq c_{\alpha,\rho,R,m}\sqrt L\,
 \log\left(\frac{(\gamma_\alpha-\rho)\Delta}{\epsilon}\right),}
                                                                    \tag{8}
\]

whenever the logarithm is positive.  Here
\(c_{\alpha,\rho,R,m}>0\) is an explicit constant independent of
\(k,h,s,L,\Delta,\epsilon\).  Thus this
class genuinely needs

\[
                     \Omega\bigl(\sqrt L\log(\Delta/\epsilon)\bigr)
\]

outer rounds on this instance.  In particular, it covers any standard
predictor--corrector implementation with a fixed number of uniformly
bounded local-norm substeps per round, provided its accepted outer iterates
remain in the fixed tube.  This is a lower bound on a narrow algorithmic
class, not on arbitrary IPMs, QIPMs, or even arbitrary path-following
implementations.

Because \(\gamma_\alpha\uparrow1\), every fixed tube radius
\(\rho<1\) is covered after moving the initial path parameter far enough
into the late regime.  Explicitly, \(\gamma_\alpha>\rho\) exactly when

\[
             \alpha>\frac{\rho(2-\rho)}{2(1-\rho)}.
\]

## A reusable concave-slack lemma

The distance argument has a simple abstract form.  Let
\(q_1,\ldots,q_L>0\) be twice differentiable concave functions on a convex
domain, and suppose

\[
                         F=-\sum_{i=1}^L\log q_i
\]

is a nondegenerate self-concordant barrier.  Let (ggeq0) be an objective
gap.  Assume every point with (g\leq\epsilon\) satisfies

\[
             \left(\prod_{i=1}^Lq_i\right)^{1/L}
                  \leq {A\epsilon\over L}.               \tag{L1}
\]

At a reference point \(x_*\), put
\(\bar q_*=(\prod_iq_i(x_*))^{1/L}\).  Then

\[
 d_F\bigl(x_*,\{x:g(x)\leq\epsilon\}\bigr)
 \geq\left[\sqrt L\log{\bar q_*L\over A\epsilon}\right]_+. \tag{L2}
\]

Indeed,

\[
 D^2(-\log q_i)[u,u]
 ={(Dq_i[u])^2\over q_i^2}-{D^2q_i[u,u]\over q_i}
 \geq\bigl(D\log q_i[u]\bigr)^2,                        \tag{L3}
\]

and integration plus Cauchy--Schwarz proves (L2).  If the actual start is
within center-norm \(\rho<1\) of \(x_*\), and every counted move has
starting local norm at most \(R<1\), the corresponding move lower bound is

\[
 {\left[
   \sqrt L\log(\bar q_*L/(A\epsilon))
       -\log(1/(1-\rho))\right]_+
  \over \log(1/(1-R))}.                                  \tag{L4}
\]

A fixed cap of \(m\) moves per outer round divides (L4) by \(m\).

There is a complementary barrier-height version that does not require
concave scalar slacks.  For any \(\nu\)-self-concordant barrier, its
gradient inequality implies along every curve

\[
              |F(y)-F(x)|\leq\sqrt\nu\,
                         \operatorname{length}_F(x\leadsto y). \tag{L5}
\]

Hence if \(F=-\log Q\), \(Q(x_*)=\bar q_*^L\), and accuracy forces
\(Q(y)\leq(A\epsilon/L)^L\), then

\[
 d_F(x_*,\{g\leq\epsilon\})
 \geq\left[{L\over\sqrt\nu}
       \log{\bar q_*L\over A\epsilon}\right]_+.           \tag{L6}
\]

For the grouped barrier, \(\nu=L\), so (L6) reproduces (L2).  Formula
(L6) also applies to linked Lorentz norm trees and matrix log-determinants,
where a termwise concavity argument is unavailable; inserting their exact
restricted gradient parameters can improve constants.

For the grouped Euclidean-ball slice, (L1) holds with \(A=2\).  The same
endpoint algebra suggests \(A=p\) for slacks
\(s-\|w\|_p^p\) in the regime where the supporting objective is positive.
However, the raw barrier \(-\log(s-\|w\|_p^p)\) is generally not a
nondegenerate standard self-concordant barrier when \(p\ne2\): it lacks the
needed smoothness for many \(p<2\), while its Hessian degenerates at
\(w=0\) for \(p>2\).  No non-Euclidean iteration lower bound is claimed
without a valid self-concordant barrier and a replacement metric argument.

## Exact central path

Write

\[
                         D(\tau)=\sqrt{h^2+\tau^2}.
\]

The stationarity equations for \(F-\tau\ell\), including one multiplier
for each equation \(\sum_Gs_{aG}=1\), give

\[
 q_{aG}=q(\tau):=\frac{2}{D(\tau)+h},\qquad
 w_{aG}=\frac{\tau q(\tau)}2c_{aG}.                    \tag{9}
\]

Put

\[
 r(\tau)=\frac{\tau q(\tau)}2
           =\frac{\tau}{D(\tau)+h}\in(0,1).
\]

Then

\[
 w_{aG}=r(\tau)c_{aG},\qquad
 s_{aG}=q(\tau)+r(\tau)^2\|c_{aG}\|^2,          \tag{10}
\]

and the allocation equation is exactly

\[
                  hq(\tau)+r(\tau)^2=1.                \tag{11}
\]

Strict convexity makes this stationary point the unique center.  Its
objective value and gap are

\[
                 \ell(z(\tau))=kr(\tau),\qquad
                 g(\tau)=k\bigl(1-r(\tau)\bigr).      \tag{12}
\]

For \(u=\tau/h\), direct simplification gives

\[
 \frac{\tau g(\tau)}L
   =1+u-\sqrt{1+u^2}=: \gamma_u.                     \tag{13}
\]

The function \(\gamma_u\) is increasing from zero to one.  In
particular, \(\tau g(\tau)\geq\gamma_\alpha L\) whenever
\(\tau\geq\alpha h\).

## Exact local-metric speed and length

Let \(H_\tau=\nabla^2F(z(\tau))\) on the affine hull.  Differentiating
the central-path equation gives

\[
                         H_\tau z'(\tau)=\nabla\ell.
\]

Consequently the squared local speed per unit logarithmic path parameter
is

\[
\begin{aligned}
 \beta(\tau)^2
 &:=\left\|\frac{dz}{d\log\tau}\right\|_{z(\tau)}^2
   =\tau^2\langle\nabla\ell,H_\tau^{-1}\nabla\ell\rangle\\
 &=\tau^2\frac d{d\tau}\ell(z(\tau))
   =k\tau^2r'(\tau)\\
 &=\frac{kh\tau^2}{D(\tau)(D(\tau)+h)}
   =L\left(1-\frac h{D(\tau)}\right).                 \tag{14}
\end{aligned}
\]

In particular,

\[
 b_\alpha\sqrt L
       \leq\beta(\tau)<\sqrt L
       \qquad(\tau\geq\alpha h),                     \tag{15}
\]

where

\[
             b_\alpha:=\sqrt{1-\frac1{\sqrt{1+\alpha^2}}}>0.
\]

There is also a closed form for the exact central-path Riemannian arc
length.  Define

\[
 y(\tau)=\frac{r(\tau)}{\sqrt{1+r(\tau)^2}},\qquad
 \Phi(y)=\sqrt2\,\operatorname{artanh}(\sqrt2y)
                       -\operatorname{artanh}(y).       \tag{16}
\]

For \(0<\tau_0<\tau_1\), its length is

\[
 \boxed{
 \mathcal L(\tau_0,\tau_1)
  =\sqrt{2L}\,\bigl[\Phi(y(\tau_1))-\Phi(y(\tau_0))\bigr].} \tag{17}
\]

Indeed, \(\tau=2hr/(1-r^2)\), and (12) reduces the length element to

\[
             \sqrt{2L}\frac{\sqrt{1+r^2}}{1-r^2}\,dr.
\]

The substitution \(y=r/\sqrt{1+r^2}\) has antiderivative (16).
Equations (15)--(17) show directly that late-path length is
\(\Theta(\sqrt L\log(\tau_1/\tau_0))\).

## Distance to the entire accurate set

The headline result is not obtained by treating central-path arc length as
geodesic distance.  Instead, every slack logarithm is itself Lipschitz in
the barrier metric.  For any tangent direction
\(\dot z=(\dot s_{aG},\dot w_{aG})\), direct differentiation gives

\[
 \|\dot z\|_z^2
 =\sum_{a,G}\left[
   \left({\dot q_{aG}\over q_{aG}}\right)^2
       +{2\|\dot w_{aG}\|^2\over q_{aG}}\right]
 \geq\sum_{a,G}\left({d\over dt}\log q_{aG}\right)^2. \tag{G1}
\]

Thus any piecewise \(C^1\) curve from \(x\) to \(y\) has length at least

\[
 \left\|\bigl(\log q_{aG}(y)-\log q_{aG}(x)\bigr)_{a,G}
       \right\|_2.                                      \tag{G2}
\]

This follows by integrating (G1) and applying the Euclidean triangle
inequality to the log-slack curve.  It applies to every path, including
shortcuts far from the central path.

Now let \(y\in\Omega\) have objective gap at most \(\epsilon\), and set

\[
 \delta_a=1-c_a^Tw_a(y),\qquad
 Q_a=\sum_Gq_{aG}(y)=1-\|w_a(y)\|^2.
\]

Each \(\delta_a\geq0\), \(\sum_a\delta_a\leq\epsilon\), and
Cauchy--Schwarz gives

\[
 Q_a\leq1-(c_a^Tw_a)^2
      =\delta_a(1+c_a^Tw_a)\leq2\delta_a.              \tag{G3}
\]

Apply AM--GM first to the \(h\) group slacks of each ball and then to the
\(k\) numbers \(\delta_a\).  Since \(L=kh\),

\[
 \prod_{a,G}q_{aG}(y)
 \leq\prod_a\left({2\delta_a\over h}\right)^h
 \leq\left({2\epsilon\over kh}\right)^{kh}
 =\left({2\epsilon\over L}\right)^L.                  \tag{G4}
\]

At \(\bar z=z(\tau_0)\), every group slack equals
\(q_0=2/(\sqrt{h^2+\tau_0^2}+h)\).  Equations (G2)--(G4) and
Cauchy--Schwarz in \(\mathbb R^L\) therefore show that the Riemannian
distance to the entire \(\epsilon\)-accurate set obeys

\[
d_F\bigl(\bar z,\{y:k-\ell(y)\leq\epsilon\}\bigr)
 \geq\left[\sqrt L\log{q_0L\over2\epsilon}\right]_+
 =\left[\sqrt L\log{r_0\Delta\over\epsilon}\right]_+
 \quad(\tau_0>0).                                      \tag{G5}
\]

At \(\tau_0=0\), the first expression in (G5) remains valid and equals
\([\sqrt L\log(k/(2\epsilon))]_+\).

It remains only to convert distance to moves.  If
\(\|y-x\|_x=r\leq R<1\), the Dikin segment lies in \(\Omega\), and
self-concordant Hessian comparison bounds its length by

\[
 \int_0^1{r\over1-tr}\,dt=-\log(1-r)
       \leq\log{1\over1-R}.                            \tag{G6}
\]

If the initial point is within center-norm \(\rho<1\) of \(\bar z\), the
same segment estimate and the triangle inequality lose at most
\(\log(1/(1-\rho))\) from (G5).  Concatenating all bounded chords gives the
headline bound after using at most \(mT\) chords in \(T\) rounds.  Notice
that no property of the intermediate points beyond membership in
\(\Omega\) and the local step bounds is used.

More generally, no uniform bound \(R\) is needed.  If the successive chord
norms are arbitrary \(r_j<1\), then the exact movement-budget consequence
is

\[
 \sum_j\log{1\over1-r_j}
 \geq\left[
   \sqrt L\log{q_0L\over2\epsilon}
       -\log{1\over1-\rho}\right]_+.                    \tag{G7}
\]

For \(M\) chords, (G7) forces at least one

\[
 r_j\geq1-\exp\!\left(-{1\over M}\left[
   \sqrt L\log{q_0L\over2\epsilon}
       -\log{1\over1-\rho}\right]_+\right).             \tag{G8}
\]

Thus a method that beats the \(\sqrt L\)-scale move count in this metric
must use a genuinely long step approaching the unit Dikin radius.

## From path length to accepted-step count

Arc length alone does not lower-bound the number of arbitrary chords: a
method could leave the path and cut across a curved arc.  Conditions
(4)--(6) exclude that possibility quantitatively.  The following direct
argument is stronger than merely dividing (17) by a step length.  It also
allows the predictor and corrector substeps to leave the central tube.

Work in affine coordinates and abbreviate \(\|\cdot\|_z\) and
\(\|\cdot\|_{z,*}\) for the primal and dual Hessian norms.  Put

\[
 B_\rho=\frac{\rho}{(1-\rho)^2},\qquad
 A_{\rho,R,m}=(1-R)^{-m}-1
                 +B_\rho\bigl(1+(1-R)^{-m}\bigr).      \tag{18}
\]

Standard self-concordant Hessian comparison and integration of the Hessian
along the segment from \(z(\tau_j)\) to \(z_j\) give

\[
 \|\nabla F(z_j)-\tau_j\nabla\ell\|_{z_j,*}\leq B_\rho. \tag{19}
\]

For one substep in (6), self-concordance gives

\[
\begin{aligned}
 \|\nabla F(x_{j,i+1})-\nabla F(x_{j,i})\|_{x_{j,i},*}
    &\leq\frac R{1-R},\\
 \|v\|_{x_{j,i},*}&\leq\frac1{1-R}
                         \|v\|_{x_{j,i+1},*}.         \tag{20}
\end{aligned}
\]

Put \(a=(1-R)^{-1}\).  Repeated norm transfer in (20), followed by a
geometric sum, shows for \(n=m_j\leq m\) that

\[
\begin{aligned}
 \|v\|_{x_{j,0},*}&\leq a^i\|v\|_{x_{j,i},*},\\
 \|\nabla F(x_{j,n})-\nabla F(x_{j,0})\|_{x_{j,0},*}
 &\leq \sum_{i=0}^{n-1}a^i\frac R{1-R}
  =a^n-1\leq a^m-1.                                  \tag{21}
\end{aligned}
\]

Subtracting the two approximate centrality equations (19), transferring
the endpoint residual back through at most \(m\) substeps, and using (21)
yields

\[
 (\tau_{j+1}-\tau_j)\|\nabla\ell\|_{z_j,*}
       \leq A_{\rho,R,m}.                              \tag{22}
\]

The outer-neighborhood condition and Hessian comparison with the exact
center give, using (15),

\[
 \tau_j\|\nabla\ell\|_{z_j,*}
 \geq(1-\rho)\beta(\tau_j)
 \geq(1-\rho)b_\alpha\sqrt L.                         \tag{23}
\]

Therefore every outer round satisfies

\[
 \log\frac{\tau_{j+1}}{\tau_j}
 \leq\frac{A_{\rho,R,m}}
 {(1-\rho)b_\alpha\sqrt L}.                           \tag{24}
\]

This proves the path-parameter part of (8), with

\[
 c_{\alpha,\rho,R,m}
      =\frac{(1-\rho)b_\alpha}{A_{\rho,R,m}}.          \tag{25}
\]

It remains to connect \(\tau_T\) to objective accuracy.  By Cauchy--Schwarz
in the center metric, (4), and \(\beta(\tau)\leq\sqrt L\),

\[
 |\ell(z_T)-\ell(z(\tau_T))|
 \leq\rho\|\nabla\ell\|_{z(\tau_T),*}
 =\frac{\rho\beta(\tau_T)}{\tau_T}
 \leq\frac{\rho\sqrt L}{\tau_T}.                    \tag{26}
\]

Since \(\sqrt L\leq L\), equations (7), (12)--(13), and (26) imply

\[
 \tau_T\geq\frac{(\gamma_\alpha-\rho)L}{\epsilon}. \tag{27}
\]

Combining (24), (27), and \(\tau_0=L/\Delta\) proves (8).

## Comparison with norm-tree barriers

For \(s\geq2\) and Lorentz dimension cap \(d\geq3\), a count-minimal
capped norm tree for one \(s\)-ball can use

\[
                  b=\left\lceil\frac{s-1}{d-2}\right\rceil
\]

factors, compared with
\(h=\lceil s/(d-2)\rceil\) grouped factors.  For an objective whose
leaf coordinates are all nonzero, every norm-tree Lorentz determinant
vanishes simply at the unique optimum.  The active determinant gradients
are independent: leaf stationarity starts the induction, and every
positive subtree norm propagates it to the root.  The optimal KKT
multipliers are all positive (in fact, they are \(1/2\) under the usual
determinant normalization).  The reduced Lagrangian Hessian on the active
manifold is nonsingular, so the KKT system is strongly regular.

The analytic implicit-function theorem applied to the strongly regular KKT
system in \(\mu=1/\tau\) therefore gives the standard logarithmic-barrier
expansion, for \(k\) separate source trees,

\[
 k-\ell(z_{\rm tree}(\tau))=\frac{kb}{\tau}+O(\tau^{-2}),\qquad
 \left\|\frac{dz_{\rm tree}}{d\log\tau}\right\|^2
      =kb+O(\tau^{-1}).                              \tag{28}
\]

Thus the late standard-barrier path has the analogous geometric scale
\(\sqrt{kb}\), sometimes slightly below the grouped scale
\(\sqrt{kh}\).  The grouped formulation is special because (9)--(17) are
exact at every path parameter and its reduced Hessian has the separately
documented one-hub sparse structure.  Equation (28) does not claim the
exact global self-concordance parameter or an exact all-\(\tau\) path formula
for the norm-tree slice.

## Scope

The headline lower bound permits every point after initialization to leave
the central tube.  It counts all local moves, or outer rounds containing at
most a fixed number of such moves.  Directions and computation between
moves are arbitrary.  It does not cover:

- substeps of local norm at least one;
- a different barrier, lift, or objective;
- rounds with an unbounded number of substeps, or predictor arcs and
  higher-order moves not decomposed into bounded local chords; or
- classical or quantum algorithms whose internal state is not represented
  by such a sequence of feasible primal iterates.

The secondary theorem (4)--(8) additionally assumes that accepted outer
iterates remain in a fixed tube, but permits its predictor--corrector
substeps to leave.  Both theorems are movement-model results.  A barrier
parameter is an upper-complexity certificate and, by itself, is not an
iteration lower bound.

## Literature boundary

Nesterov and Nemirovskii's self-concordant path-following theory supplies
the Hessian-comparison inequalities and the familiar
\(O(\sqrt\nu\log(1/\epsilon))\) upper bound.  Nesterov and Todd,
*On the Riemannian Geometry Defined by Self-Concordant Barriers and
Interior-Point Methods*, Found. Comput. Math. 2 (2002), develop general
Riemannian-distance lower bounds for short-step sequences.  That theory
does not by itself turn a central-path arc length into the present result:
the distance to the target level set can be shorter than the central arc,
and an algorithm can leave the path.  Equations (G1)--(G5) supply the
missing instance-specific lower bound on the distance to the entire
accurate level set.  The residual proof (18)--(27) is a separate converse
for tube endpoints.

Nesterov and Nemirovski,
*Central path and Riemannian distances* (CORE Discussion Paper 2003/51),
study Riemannian lengths of central paths for general self-concordant
barriers.  Sturm and Zhang, *On a Wide Region of Centers and Primal-Dual
Interior Point Algorithms for Linear Programming*, Math. Oper. Res. 22
(1997), analyze upper iteration bounds for algorithms restricted to central
regions.  Recent LP work studies segment complexity of wide central-path
neighborhoods, a different model tied to piecewise-linear trajectories.

A targeted search found no source computing the grouped product-ball path
(9)--(17), the log-slack distance bound (G5), or the resulting bounded-move
lower bound.  The elementary log-slack and Dikin comparisons themselves
are standard; the potentially new part is their sharp application to this
grouped product-ball lift and fully activating objective.  Novelty remains
subject to specialist review.

## Independent audit

Two independent hostile audits verified the central path, objective gap,
metric speed, and arc antiderivative.  They separately checked the directions
of every Hessian and dual-norm comparison in (18)--(24): backward transfer
across \(n\) substeps costs \(a^n\), the gradient changes sum to
\(a^n-1\), and the two outer residuals give exactly
\(B_\rho(1+a^n)\).  They also verified the endpoint transfer (26)--(27) and
the norm-tree asymptotic under the stated independence and strict-multiplier
hypotheses.  A further independent audit rederived (G1)--(G6), including
both AM--GM steps, the positive part, the approximate-start subtraction,
and the division by the fixed substep cap.  No correction was required.
