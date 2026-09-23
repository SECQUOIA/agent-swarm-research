# Globally smooth exact Lorentz-product factorizations of the Euclidean ball

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Main result

Let

\[
 Q_3=\{(u,v,w)\in\mathbb R^3:u\geq\sqrt{v^2+w^2}\}.
\]

For every \(N\geq2\), the Euclidean ball \(B_2^N\) has an exact affine lift
over \(Q_3^N\) whose primal boundary fibers are unique and whose primal and
dual contact factors are globally \(C^\infty\) and nowhere zero.

For \(x,y\in S^{N-1}\), define

\[
\begin{aligned}
 A_i(x)&=\left({1+x_i^2\over2},{1-x_i^2\over2},x_i\right),\\
 B_i(y)&=\left({1+y_i^2\over2},-{1-y_i^2\over2},-y_i\right).
\end{aligned}                                                    \tag{1}
\]

Both vectors lie on the positive boundary sheet of \(Q_3\), and

\[
 \langle A_i(x),B_i(y)\rangle={1\over2}(x_i-y_i)^2.              \tag{2}
\]

Consequently

\[
 \boxed{
 1-\langle x,y\rangle
   =\sum_{i=1}^N\langle A_i(x),B_i(y)\rangle.}                   \tag{3}
\]

Thus the apparent differential-integrability issue for the natural
overcomplete rank-one frame has an exact solution.

Combining this construction with the saturated-factor submersion
obstruction gives a sharp regularity count. In the class of exact
\(Q_3^k\)-factorizations of the ball slack having globally labelled \(C^1\)
primal and dual selections over the full contact sphere,

\[
 k_{\mathrm{smooth}}(B_2^N)=N
 \quad\text{for every }N\geq3.                                 \tag{4}
\]

\(k_{\mathrm{smooth}}(B_2^2)=1\), because the disk is itself an affine
section of one \(Q_3\). Formula (4) is a regularity theorem for factor
selections, not a
lower bound on the existence of an underlying nonsmooth lift. Standard
norm-tree lifts use \(N-1\) blocks in every dimension but have selection
singularities.

## Direct affine lift

Introduce \(q_i=(u_i,v_i,w_i)\in Q_3\), impose

\[
 u_i+v_i=1\quad(i=1,\ldots,N),\qquad
 \sum_{i=1}^N(u_i-v_i)=1,                                      \tag{5}
\]

and project by \(x_i=w_i\). Put \(s_i=u_i-v_i\). Since \(u_i+v_i=1\),
the Lorentz constraint is equivalent to

\[
                         s_i\geq x_i^2.                         \tag{6}
\]

Equations (5)--(6) imply \(\sum_i x_i^2\leq1\). Conversely, if
\(\|x\|_2\leq1\), choose any \(s_i\geq x_i^2\) with \(\sum_i s_i=1\) and
set

\[
              u_i={1+s_i\over2},\qquad v_i={1-s_i\over2}.
\]

This proves that the projection is exactly \(B_2^N\).

The slice is strictly feasible: at \(x=0\), take \(s_i=1/N\). Every
\(q_i\) is then in \(\operatorname{int}Q_3\). Hence the minimal face of the
ambient product cone containing the feasible slice is all of \(Q_3^N\);
none of the factors is hidden in a proper face.

If \(x\in S^{N-1}\), then (6) and \(\sum_i s_i=1=\sum_i x_i^2\) force
\(s_i=x_i^2\) for every \(i\). The boundary fiber is therefore unique and
equals \(q_i=A_i(x)\). In particular, its dependence on \(x\) is globally
polynomial.

## Dual contact certificate

For a feasible lift point with coordinate \(s_i=u_i-v_i\), direct
calculation gives

\[
 \langle q_i,B_i(y)\rangle
 ={s_i+y_i^2\over2}-x_i y_i.                                   \tag{7}
\]

Summing (7), using \(\sum_i s_i=\sum_i y_i^2=1\), proves

\[
                \sum_i\langle q_i,B_i(y)\rangle
                =1-\langle x,y\rangle.                          \tag{8}
\]

This also verifies the affine-dual normalization, rather than relying only
on the boundary identity. Give the \(i\)-th equality \(u_i+v_i=1\) the
multiplier \(\lambda_i=y_i^2/2\), and give the final equality in (5) the
multiplier \(\lambda_0=1/2\). Subtracting the lifted objective \(y_iw_i\)
produces exactly

\[
 (\lambda_i+\lambda_0,\lambda_i-\lambda_0,-y_i)=B_i(y)\in Q_3.
\]

The multiplier objective is
\(\sum_i\lambda_i+\lambda_0=1\), the support value of the unit ball.
Thus \(B(y)\) is a globally smooth conic-dual contact certificate. No
uniqueness of the entire dual multiplier fiber is needed or claimed.

In the incidence language, the primal boundary incidence is exactly

\[
 \mathcal S_P=\{(x,A(x)):x\in S^{N-1}\},
\]

because the boundary fiber is unique. The selected normalized-dual contact
incidence contains

\[
 \mathcal S_D=\{(y,\lambda(y)):y\in S^{N-1}\},\qquad
 \lambda(y)=(y_1^2/2,\ldots,y_N^2/2,1/2).
\]

Both are graphs of \(C^\infty\) maps over the compact sphere. They are
therefore compact embedded \(C^\infty\) sheets, and their projections onto
the contact sphere are diffeomorphisms. Thus the displayed affine lift is
bi-contact-regular in the incidence-sheet definition.

## Boundary-ray and differential interpretation

Let

\[
 p(t)=\left({1-t^2\over1+t^2},{2t\over1+t^2}\right)\in S^1,
 \qquad \alpha(t)={1+t^2\over2}.                                \tag{9}
\]

Then

\[
 A_i(x)=\alpha(x_i)(1,p(x_i)),\qquad
 B_i(y)=\alpha(y_i)(1,-p(y_i)).
\]

The phase \(p(t)\) is stereographic and has the global lift
\(\theta(t)=2\arctan t\). Its elementary chordal identity is

\[
 1-p(s)\cdot p(t)
 ={2(s-t)^2\over(1+s^2)(1+t^2)},                               \tag{10}
\]

which explains (2). There is no phase-winding obstruction because each
phase factors through the real coordinate \(x_i\).

Mixed differentiation of (2) on the contact diagonal gives

\[
 -d_xd_y\langle A_i(x),B_i(y)\rangle\big|_{y=x}
                         =dx_i\otimes dx_i.                     \tag{11}
\]

With \(P_x\) the tangent projection in \(\mathbb R^N\),
\(dx_i\) is dual to \(P_xe_i\), and

\[
       \sum_{i=1}^N(P_xe_i)(P_xe_i)^*=I_{T_xS^{N-1}}.            \tag{12}
\]

Thus the construction integrates the canonical overcomplete Parseval
frame exactly. Individual channels are allowed to vanish:
\(P_xe_i=0\) at \(x=\pm e_i\). This rank dropout is precisely why the
\(N\)-channel construction avoids creating \(N\) global line subbundles.

## Grouped construction under a block-dimension cap

The coordinate construction groups without losing any of its regularity.
Let \(\mathcal G\) be a partition of \(\{1,\ldots,N\}\). For a group
\(G\) of size \(r_G\), define

\[
\begin{aligned}
 A_G(x)&=\left({1+\|x_G\|^2\over2},
                    {1-\|x_G\|^2\over2},x_G\right),\\
 B_G(y)&=\left({1+\|y_G\|^2\over2},
                   -{1-\|y_G\|^2\over2},-y_G\right)
             \in Q_{r_G+2}.
\end{aligned}                                                    \tag{G1}
\]

Then

\[
 \langle A_G(x),B_G(y)\rangle
             ={1\over2}\|x_G-y_G\|^2,
\qquad
 \sum_{G\in\mathcal G}\langle A_G(x),B_G(y)\rangle
             =1-\langle x,y\rangle.                             \tag{G2}
\]

The matching affine lift has
\(q_G=(u_G,v_G,w_G)\in Q_{r_G+2}\),

\[
 u_G+v_G=1,\qquad
 \sum_G(u_G-v_G)=1,\qquad x_G=w_G.                              \tag{G3}
\]

Writing \(s_G=u_G-v_G\), these constraints are equivalent to

\[
                         s_G\geq\|x_G\|^2,\qquad \sum_Gs_G=1.   \tag{G4}
\]

Thus the projection is the ball. Taking \(x=0,s_G=1/|\mathcal G|\)
proves Slater and full minimal face. On the sphere the fiber is unique,
because every nonnegative difference
\(s_G-\|x_G\|^2\) must vanish. The dual multipliers

\[
                    \lambda_G={\|y_G\|^2\over2},\qquad
                    \lambda_0={1\over2}                         \tag{G5}
\]

produce \(B_G(y)\), have objective one, and give compact embedded
\(C^\infty\) primal and normalized-dual incidence sheets exactly as in the
singleton construction.

Under a dimension cap \(3\leq d<N+1\), choose
\(r_G\leq d-2\) and as many full groups as possible. Then

\[
 k=|\mathcal G|=\left\lceil{N\over d-2}\right\rceil,\qquad
 \sum_Gr_G=N,\qquad
 M=\sum_G(r_G+2)=N+2k.                                         \tag{G6}
\]

Every ambient Lorentz product barrier has \(\nu\geq2k\), by restriction
to a product of two-dimensional orthant sections, and the standard product
barrier attains \(\nu=2k\).

The independently audited sphere-submersion classification makes these
values optimal, not merely achievable. If \(d<N+1\), every block capacity
is below \(N-1\); saturation at total capacity \(N-1\) would force a single
full-capacity block and is therefore impossible. The integer gap gives
total capacity at least \(N\), so

\[
 k_{\min}=\left\lceil{N\over d-2}\right\rceil,\qquad
 M_{\min}=N+2\left\lceil{N\over d-2}\right\rceil,\qquad
 \nu_{\min}=2\left\lceil{N\over d-2}\right\rceil.              \tag{G7}
\]

For \(d\geq N+1\), the direct \(Q_{N+1}\) representation instead gives the
simultaneous optima \(k_{\min}=1\), \(M_{\min}=N+1\), and
\(\nu_{\min}=2\). Here \(\nu_{\min}\) always refers to a possibly coupled
LHSC barrier on the full ambient Lorentz product, not to a barrier defined
only on its affine slice. The strict lower bound is proved in
[Sphere submersions force a strict curvature-capacity
gap](2026-09-04-sphere-submersion-curvature-gap.md).

## Sharpness and formulation cost

Every three-dimensional proper cone block has curvature capacity one, so
the local curvature theorem gives \(k\geq N-1\). If equality holds,
globally \(C^1\) factor selections already suffice to force every mixed
channel

\[
                         M_i=-dA_i^*dB_i                       \tag{13}
\]

to have rank one at every contact: their sum is the invertible sphere
metric, there are \(N-1\) channels, and each has rank at most one.

More generally, consider any saturated product-cone factorization with
block dimensions \(m_i\), capacities \(r_i=m_i-2>0\), and
\(\sum_i r_i=N-1\). Saturation gives
\(\operatorname{rank}M_i=r_i\). Choose
\(\ell_i\in\operatorname{int}K_i^*\) and normalize

\[
 p_i(x)={A_i(x)\over\ell_i(A_i(x))}
       \in\partial\{z\in K_i:\ell_i(z)=1\}.                    \tag{14}
\]

Full rank in (13) implies that neither \(A_i(x)\) nor \(B_i(x)\) can vanish:
at a cone vertex, two-sided differentiability and pointedness would make
the corresponding derivative zero. Exact diagonal complementarity then
puts \(p_i(x)\) on the boundary \(J_i\) of the compact
\((m_i-1)\)-dimensional convex base. Topologically,
\(J_i\cong S^{r_i}\).

The map \(dp_i\) has rank exactly \(r_i\) everywhere. If
\(dp_i(u)=0\), then \(dA_i(u)\) is radial. Differentiated complementarity
gives
\(\langle A_i,dB_i(v)\rangle=0\) for every \(v\), and hence
\(M_i(u,\cdot)=0\). Thus
\(\ker dp_i\subseteq\ker M_i\), so
\(\operatorname{rank}dp_i\geq r_i\). On the other hand, rank at least
\(r_i+1\) would make \(p_i\) locally open in the affine hull of the base by
the submersion theorem, impossible because its image lies in \(J_i\),
which has empty interior. Therefore

\[
                         \operatorname{rank}dp_i=r_i.           \tag{14a}
\]

This constant-rank conclusion also supplies boundary regularity rather than
assuming it. A constant-rank chart contains an \(r_i\)-dimensional
transversal that maps regularly and injectively onto an embedded patch in
\(J_i\). Compose that patch with any radial homeomorphism
\(J_i\cong S^{r_i}\). Invariance of domain in dimension \(r_i\) shows that
the patch is relatively open in \(J_i\). Hence \(p_i(S^{N-1})\) is open;
compactness makes it closed, and connectedness of \(J_i\) makes it all of
\(J_i\). The relatively open regular patches give \(J_i\) a compatible
\(C^1\) embedded-hypersurface structure. Radial projection from an interior
base point is then a \(C^1\) diffeomorphism with the standard sphere.
Consequently every positive-capacity block in a globally \(C^1\) saturated
factorization induces a \(C^1\) submersion

\[
                              S^{N-1}\longrightarrow S^{r_i}.   \tag{14b}
\]

This general statement and the boundary-regularity argument are recorded
separately in
[Saturated cone factors force sphere-to-sphere
submersions](2026-09-04-saturated-factor-submersion-obstruction.md).

For a three-dimensional block \(r_i=1\). If \(N\geq3\), simple
connectivity lifts (14b) to a real \(C^1\) phase on \(S^{N-1}\). That phase
has a maximum, where its derivative—and therefore \(dp_i\)—vanishes,
contradicting (14a).

Thus \(k=N-1\) is impossible for all \(N\geq3\), and (1)--(3) attain the
next possible count \(k=N\). This factor-integrability argument is strictly
stronger than the general Adams obstruction: it also closes the \(N=4,8\)
cases. It also shows that the lower bound remains valid if the \(Q_3\)
blocks are replaced by arbitrary three-dimensional proper cones.

The explicit lift uses ambient cone dimension \(3N\). Moreover, every
possibly coupled logarithmically homogeneous self-concordant barrier on the
ambient product \(Q_3^N\) has parameter

\[
                              \nu\geq2N,                         \tag{15}
\]

and the standard product logarithmic barrier attains \(2N\). To see the
lower bound, restrict the barrier to the product of the two-dimensional
sections \(Q_3\cap\{w=0\}\), each linearly isomorphic to
\(\mathbb R_+^2\). This gives a barrier of the same parameter on
\(\mathbb R_+^{2N}\), whose parameter is at least \(2N\).

This is an ambient-product barrier statement, not a lower bound for an
arbitrary barrier defined only on the affine feasible slice. It and the
dimension \(3N\) are costs of insisting on
globally smooth, coordinatewise three-dimensional factors: the direct
\((N+1)\)-dimensional Lorentz-cone representation of the ball has barrier
parameter \(2\), and a norm tree has only \(N-1\) three-dimensional blocks
but loses global smoothness of its canonical factor selections.

## Literature boundary and hostile audit

Representing \(s_i\geq x_i^2\) by a three-dimensional rotated
second-order cone is standard conic modeling; see, for example, the
[MOSEK Modeling Cookbook, §3](https://docs.mosek.com/modeling-cookbook/cqo.html).
Rotated and ordinary three-dimensional Lorentz cones are linearly
isomorphic. Cone lifts and slack factorizations are related by
Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://doi.org/10.1287/moor.1120.0575).
Accordingly, neither the coordinatewise quadratic lift nor the elementary
identity (2) is claimed as new.

The apparently new result is the sharp global-selection regularity count
(4), obtained by matching the
[saturated-factor submersion obstruction](2026-09-04-saturated-factor-submersion-obstruction.md)
with a construction whose unique boundary fibers and dual certificates are
globally smooth.  The lower obstruction applies to arbitrary
three-dimensional proper cones and needs no regularity of their boundaries.
A
targeted search found standard rotated-SOC modeling and general cone
factorization results, but no source formulating this sharp smooth-contact
count. Novelty remains subject to specialist review.

The audit checks are explicit above: both factors are on the correct
positive Lorentz sheet; (2) fixes the sign and normalization; (5)--(6)
prove exact projection in both directions; the exhibited interior point
proves Slater and full minimal face; boundary fibers are unique; (7)--(8)
give a normalized dual certificate on every feasible fiber; and
(11)--(12) identify the integrated differential frame. The lower bound is
only for global \(C^1\) factor selections and is not misreported as a lift
nonexistence theorem. An independent hostile audit rechecked these points
and the normalized-base submersion contradiction (13)--(14b), including
cornered planar bases, and found no error. A
follow-up audit verified that both incidence graphs satisfy the proper
local-diffeomorphism definition and that restriction to the orthant section
proves the coupled ambient barrier lower bound (15), with the stated
feasible-slice caveat.
