# A genuinely coupled symmetric box barrier still has a growing centrality tax

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the construction and asymptotic proof; targeted literature screen complete, priority not claimed

## Result

Let \(r\geq2\), \(K=(-1,1)^r\), and consider
\[
 F_r(x)=-\sum_{i=1}^r\log(1-x_i^2)
        -\log(r-\|x\|_2^2).                                   \tag{1}
\]
This is a genuinely coupled, hyperoctahedrally invariant
self-concordant barrier with
\[
                            \nu(F_r)=r+1.                      \tag{2}
\]
Nevertheless its positive-objective central paths have worst
same-endpoint arc-to-distance ratio at least
\[
 \boxed{\displaystyle
 \sup_{w_i>0,\ s_0<s_1}
 {L_{F_r}(x_w|_{[s_0,s_1]})\over
       d_{F_r}(x_w(s_0),x_w(s_1))}
 \ \geq\ \Gamma_{r-1},}\qquad
 \Gamma_n^2=\sum_{i=1}^n(\sqrt i-\sqrt{i-1})^2.               \tag{3}
\]
Thus the ratio is at least \(\Theta(\sqrt{\log r})\).  Full cube
symmetry, genuine Hessian coupling, and an \(O(r)\) barrier parameter do
not by themselves remove the separable centrality tax.

The conclusion is existential for the explicit barrier (1).  It is not a
lower bound for every hyperoctahedrally invariant or every
\(O(r)\)-parameter barrier on the box.

## 1. Barrier and parameter

Write
\[
 U(x)=-\sum_i\log(1-x_i^2),\qquad
 G(x)=-\log(r-\|x\|_2^2).                                     \tag{4}
\]
The first term is the \(r\)-parameter product interval barrier.  After
the linear scaling \(x\mapsto x/\sqrt r\), the second is the standard
one-parameter reduced ball barrier.  Restriction from the open ball to
the open cube preserves self-concordance, and \(U\) supplies blow-up on
every cube boundary point.  The sum rule therefore gives
\(\nu(F_r)\leq r+1\).  For the reverse inequality, approach the positive
vertex on the segment \(x=(1-\tau)\mathbf1\).  The \(r\) interval
determinants and the additional ball determinant each vanish to first
order:
\[
 1-(1-\tau)^2=2\tau+O(\tau^2),\qquad
 r-r(1-\tau)^2=2r\tau+O(\tau^2).
\]
Thus \(F_r=-(r+1)\log\tau+O(1)\), and the one-dimensional barrier-gradient
inequality gives \(\nu(F_r)\geq r+1\).  This proves (2).

The barrier is invariant under every signed permutation.  It is genuinely
coupled because, with \(S=r-\|x\|^2\),
\[
 \nabla^2G(x)={2\over S}I+{4\over S^2}xx^T,                    \tag{5}
\]
whose off-diagonal entries are nonzero when two coordinates of \(x\) are
nonzero.

## 2. Objectives which leave one regularizing channel

Put \(n=r-1\) and
\[
 \alpha_i=\sqrt i-\sqrt{i-1},\qquad i=1,\ldots,n.              \tag{6}
\]
For \(T>0\), choose the strictly positive weights
\[
 w_i(T)=e^{T\alpha_i}\quad(i\leq n),\qquad
 w_r(T)=e^{-T^2}.                                               \tag{7}
\]
Let \(x_T(s)\) be the central path defined by
\[
                    \nabla F_r(x_T(s))=e^s w(T),qquad s\leq0. \tag{8}
\]
All weights are positive, so the linear objective has the unique optimizer
\({\bf1}\) on the closed cube.

Every central coordinate is nonnegative.  In the last coordinate,
stationarity and \(u'(t)=2t/(1-t^2)\geq2t\) for \(t\geq0\) give
\[
        0\leq x_{T,r}(s)\leq {e^sw_r(T)\over2}
                    \leq {e^{-T^2}\over2}.                    \tag{9}
\]
Consequently, throughout the relevant path and the comparison path used
below,
\[
 S=\sum_i(1-x_i^2)\geq1-x_r^2\geq{1\over2}                    \tag{10}
\]
for all large \(T\).  Equations (5) and (10) imply the uniform bounds
\[
 \|\nabla G(x)\|_\infty\leq4,
 \qquad 0\preceq\nabla^2G(x)\preceq C_r I,                    \tag{11}
\]
where one may take \(C_r=4+16r\).  The radial term is therefore a bounded
smooth coupling along these paths, even though it becomes singular at a
cube vertex when every coordinate approaches its endpoint.

## 3. Central-speed lower bound without path separability

Set \(z_i(s)=e^sw_i(T)\), \(D=\nabla^2U(x_T(s))\), and
\(H=\nabla^2F_r(x_T(s))=D+\nabla^2G(x_T(s))\).  Differentiating (8) gives
\[
 H\dot x_T=z,qquad
 \|\dot x_T\|_{F_r,x_T}^2=z^TH^{-1}z.                          \tag{12}
\]
For any coordinate subset \(A\), the variational formula for the inverse
quadratic form, restricted to trial vectors supported on \(A\), and (11)
give
\[
 z^TH^{-1}z
 \geq z_A^TH_{AA}^{-1}z_A
 \geq\sum_{i\in A}{z_i^2\over u''(x_{T,i})+C_r}.               \tag{13}
\]
Stationarity also says
\[
                    u'(x_{T,i})=z_i-(\nabla G)_i,
 \qquad |(\nabla G)_i|\leq4.                                  \tag{14}
\]
Because
\[
 {u'(t)^2\over u''(t)}={2t^2\over1+t^2}\longrightarrow1
 \quad(t\uparrow1),                                           \tag{15}
\]
for every \(\varepsilon>0\) there is a fixed
\(Z=Z(r,\varepsilon)>1\) such that
\[
             z_i\geq Z
 \quad\Longrightarrow\quad
 {z_i^2\over u''(x_{T,i})+C_r}\geq1-\varepsilon.              \tag{16}
\]
This implication is uniform in \((T,s)\).

The activation times of the first \(n\) coordinates at level \(Z\) are
\[
                      \tau_i=\log Z-T\alpha_i,                 \tag{17}
\]
and satisfy \(\tau_1<\cdots<\tau_n<0\) for large \(T\).  On
\([\tau_j,\tau_{j+1}]\), the first \(j\) coordinates obey (16); on
\([\tau_n,0]\), all first \(n\) do.  Integrating (12)--(16) yields
\[
\begin{aligned}
 L_{F_r}(x_T|_{(-\infty,0]})
 &\geq\sqrt{1-\varepsilon}\left[
   \sum_{j=1}^{n-1}\sqrt j\,T(\alpha_j-\alpha_{j+1})
   +\sqrt n\,(T\alpha_n-\log Z)\right]\\
 &=\sqrt{1-\varepsilon}
       \left[T\Gamma_n^2-\sqrt n\log Z\right].               \tag{18}
\end{aligned}
\]
The last identity is summation by parts and uses
\(\alpha_j=\sqrt j-\sqrt{j-1}\).

## 4. Actual coupled-metric endpoint distance

Let
\[
 \rho(t)=\int_0^t\sqrt{u''(q)}\,dq,
 \qquad y_{T,i}=\rho(x_{T,i}(0)).                               \tag{19}
\]
For \(i\leq n\), (14), (7), and the standard interval asymptotic
\[
 \rho((u')^{-1}(e^a))=a+c+o(1)\qquad(a\to\infty)               \tag{20}
\]
give, for fixed \(r\),
\[
                  y_{T,i}=T\alpha_i+O_r(1),qquad
                  y_{T,r}=o(1).                                \tag{21}
\]
Hence
\[
                         \|y_T\|_2=T\Gamma_n+O_r(1).           \tag{22}
\]

The origin is the analytic center of \(F_r\).  Join it to \(x_T(0)\) by
the coordinatewise \(U\)-geodesic
\[
                 \rho(\gamma_i(q))=q y_{T,i},\qquad0\leq q\leq1.
                                                                    \tag{23}
\]
Its \(U\)-length is exactly \(\|y_T\|_2\).  Along it the last coordinate
still satisfies (9), so (10)--(11) hold.  Moreover each coordinate of
\(\gamma\) is monotone, whence
\[
 \int_0^1\|\dot\gamma(q)\|_2\,dq
 \leq\sum_i|x_{T,i}(0)|\leq r.                                \tag{24}
\]
Using \(\sqrt{a+b}\leq\sqrt a+\sqrt b\), (11), and (24),
\[
\begin{aligned}
 d_{F_r}(0,x_T(0))
 &\leq L_{F_r}(\gamma)\\
 &\leq L_U(\gamma)+L_G(\gamma)
 \leq\|y_T\|_2+r\sqrt{C_r}
 =T\Gamma_n+O_r(1).                                           \tag{25}
\end{aligned}
\]

Divide (18) by (25), first send \(T\to\infty\), and then send
\(\varepsilon\downarrow0\).  This proves (3), with the analytic-center
start understood as the limit \(s_0\to-\infty\); finite starts approximate
the same ratio.

## Scope and novelty boundary

The theorem concerns the exact primal Hessian metric and exact central
paths of the explicit barrier (1).  It proves a continuous same-endpoint
tax, not a distance-to-objective-sublevel theorem, a central-neighborhood
round lower bound, or a query lower bound.  The exponentially varying
weights are mathematical real inputs; no finite-bit encoding claim is
made here.

The ball and interval barriers, barrier sum rule, and inverse-quadratic
variational formula are standard.  The candidate contribution is the
bounded-channel construction showing rigorously that genuine full cube
symmetry and coupled curvature do not suffice to eliminate the growing
centrality tax.  Priority remains provisional after the targeted screen
below.

### Targeted primary-source screen (2026-09-04)

The closest explicit alternative cube barrier located is Papa Quiroz and
Oliveira,
[*New Self-Concordant Barrier for the
Hypercube*](https://doi.org/10.1007/s10957-007-9220-2).  Their barrier on
\((0,1)^r\) is
\(\sum_i(2x_i-1)[\log x_i-\log(1-x_i)]\), has parameter
\(3r/2\), and induces a diagonal product metric for which they compute
geodesics and analyze path-following algorithms.  It is therefore a direct
antecedent for nonstandard cube barriers and their Riemannian geometry, but
it is separable rather than genuinely coupled and does not state an
arc-to-same-endpoint-distance lower bound growing as
\(\sqrt{\log r}\).

Nesterov--Todd,
[*On the Riemannian Geometry Defined by Self-Concordant Barriers and
Interior-Point Methods*](https://doi.org/10.1007/s102080010032), compute
exact product distances and include an explicit separable hypercube model.
Nesterov--Nemirovski,
[*Primal Central Paths and Riemannian Distances for Convex
Sets*](https://doi.org/10.1007/s10208-007-9019-4), prove the general
bounded-domain \(O(\nu^{1/4})\) comparison and use the standard separable
box logarithmic barrier in Example 5.1.  These results supply the classical
metric and comparison framework.  They do not analyze the redundant radial
term in (1), nor do they give the sharp prefix coefficient \(\Gamma_{r-1}\)
for a coupled cube barrier.

There is substantial prior art showing that a redundant description can
change a logarithmic central path.  Deza--Nematollahi--Terlaky,
[*How Good Are Interior Point Methods? Klee--Minty Cubes Tighten
Iteration-Complexity Bounds*](https://doi.org/10.1007/s10107-006-0044-x),
use many asymmetrically placed redundant linear inequalities to force a
Klee--Minty central path near exponentially many vertices.  That is a much
stronger worst-case winding/iteration phenomenon in a different model.  It
does not cover one hyperoctahedrally invariant nonlinear redundant
inequality, preserve an \(r+1\) barrier parameter, or compare its central
arc to the same-endpoint geodesic in its own Hessian metric.

Lee--Yue's
[*Universal Barrier Is \(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011)
and Chewi's
[*The Entropic Barrier Is \(n\)-Self-Concordant*](https://arxiv.org/abs/2112.10947)
give the optimal dimension parameter for two canonical barriers.  On a
Cartesian box, however, the universal polar-volume formula and the entropic
log-partition both factor coordinatewise, as calculated in the companion
canonical-box note.  Thus those sources do not settle whether genuine
coupling can remove the tax; (1) is an explicit negative example, not a
barrier-independent answer.

The targeted screen did not locate the specific barrier (1), a symmetric
coupled-box analogue with the same bounded-channel proof, or the exact
\(\Gamma_{r-1}\) conclusion.  The conservative label is **candidate explicit
coupled-barrier counterexample synthesized from standard barrier-sum and
Hessian-metric ingredients**.  It should not be described as the first
nonseparable cube barrier, the first demonstration that redundant
constraints distort central paths, or a lower bound for all symmetric
barriers.  This was a targeted screen through 2026, not an exhaustive
novelty or priority determination.

## Audit targets

1. Verify that the reduced ball term has parameter one on the larger ball
   and that restriction plus summation justifies (2).
2. Check the last-coordinate bound and uniform derivative bounds
   (9)--(11).
3. Check the restricted variational inequality (13), including its first
   inequality in the presence of the omitted coordinates.
4. Verify the uniform tail implication (16) and the activation integral
   (18).
5. Check that the comparison path proves an upper bound in the actual
   coupled metric, especially (24)--(25).

## Independent hostile audit

**PASS, after strengthening (2) to the exact value \(r+1\).**  The ball
term is the standard parameter-one barrier on the radius-\(\sqrt r\)
ball, restricted to the cube.  Barrier summation gives the upper bound
\(r+1\); the positive-vertex segment has \(r+1\) independent first-order
logarithmic zeros, giving the matching lower bound.  Formula (5) confirms
genuine coupling and full signed-permutation symmetry.

For the selected objectives, coordinatewise stationarity has a positive
coefficient multiplying every \(x_i\), proving nonnegativity and (9).
The last coordinate keeps \(S\geq1/2\), so the gradient and Hessian bounds
in (11) hold on both the central and comparison paths.  The first
inequality in (13) follows by restricting the variational formula
\[
 z^TH^{-1}z=\max_h(2z^Th-h^THh)
\]
to vectors supported on \(A\).  Since
\((\nabla^2G)_{AA}\preceq C_rI\), inverse order gives the second
inequality.  Bounded \(\nabla G\), the interval endpoint asymptotics, and
\(u'^2/u''\to1\) make (16) uniform.  The prefix activation integral and
summation by parts in (18) are exact.

Finally, (23) is only used as a comparison curve.  Its \(U\)-length is
\(\|y_T\|_2\), while monotonicity bounds its Euclidean total variation
and hence its added \(G\)-length by \(r\sqrt{C_r}\).  This proves an upper
bound in the actual \(F_r\) metric, not merely in the product metric.
Together with (21), division gives \(\Gamma_{r-1}\).  The tiny last
weight is strictly positive throughout, so no limiting zero-objective
coordinate is hidden.  No extension to all coupled barriers follows.
