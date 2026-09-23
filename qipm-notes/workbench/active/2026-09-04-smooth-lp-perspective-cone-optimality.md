# Exact contact-smooth granularity of \(\ell_p\) balls

Status: Proved; targeted literature screen complete; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Main theorem

Fix \(1<p<\infty\), let \(q=p/(p-1)\), and let \(N\geq3\). Consider
proper exact lifts of \(B_p^N\) over products of proper cones of dimension
at most \(d\), with globally labelled \(C^1\) primal and dual factor
selections on the full paired boundaries

\[
             \partial B_p^N\times\partial B_q^N.               \tag{1}
\]

Equivalently, at lift level one may require compact \(C^1\) primal and
normalized-dual contact sheets whose projections to the two boundaries are
diffeomorphisms. Let \(S=\sum_i(m_i-2)_+\), let \(k_+\) count the
positive-capacity factors, and let \(M_+\) be their total dimension.

The exact optima are

\[
\boxed{
\begin{array}{c|c|c|c}
\text{block cap}&S_{\min}&k_{+,\min}&M_{+,\min}\\ \hline
3\leq d<N+1
 &N&\left\lceil\dfrac{N}{d-2}\right\rceil
 &N+2\left\lceil\dfrac{N}{d-2}\right\rceil\\[2mm]
d\geq N+1&N-1&1&N+1.
\end{array}}                                                   \tag{2}
\]

Thus contact smoothness creates an exact phase transition. Below the
natural cone dimension \(N+1\), it costs one additional unit of curvature
capacity compared with unrestricted exact lifts. At and above \(N+1\), the
single \(p\)-order cone is optimal.

The lower bound in (2) applies to products of arbitrary proper cones. The
matching small-block construction below uses explicit perspective-
\(p\) cones. When \(p=2\), these cones are Lorentz cones, and the result also
gives the exact ambient-product LHSC barrier parameter

\[
             \nu_{\min}=2\left\lceil\frac{N}{d-2}\right\rceil
             \quad(3\leq d<N+1).                              \tag{3}
\]

For \(p\ne2\), the exact barrier parameter of the nonsymmetric perspective
cones is not established here. The general product lower bound
\(\nu\geq2k_+\) still applies to the ambient product, but (2) makes no
matching ambient-barrier claim.  On the reduced grouped affine slice, a
separate embedded-cube argument gives the intrinsic lower bound
\[
       \vartheta_{\rm slice}\geq
       \left\lceil\frac{N}{d-2}\right\rceil
\]
for every possibly coupled self-concordant barrier: fix the positive
allocation variables and vary one coordinate in every group.  This is exact
for \(p=2\); for \(p\ne2\), a matching reduced barrier remains open.  See
[Coupling cannot lower the barrier parameter of the grouped ball
slice](2026-09-04-coupled-barrier-grouped-ball-slice.md).

## Lower bound

The boundaries of \(B_p^N\) and its polar \(B_q^N\) are \(C^1\) and
strictly convex. At a paired contact \(x\cdot y=1\),

\[
 T_x\partial B_p^N=y^\perp,
 \qquad T_y\partial B_q^N=x^\perp.                             \tag{4}
\]

The Euclidean pairing between these two tangent hyperplanes is
nondegenerate: its left kernel is
\(\operatorname{span}\{x\}\cap y^\perp=\{0\}\), and similarly on the
right. Hence independent mixed differentiation of the slack
\(1-x\cdot y\) has rank \(N-1\), without differentiating the Gauss map or
assuming positive curvature.

The universal curvature theorem first gives

\[
                              S\geq N-1.                       \tag{5}
\]

If equality held, the saturated-factor submersion theorem and the
Browder--Serre sphere-submersion classification would force exactly one
positive-capacity factor, of capacity \(N-1\) and dimension \(N+1\).
Therefore a cap \(d<N+1\) rules out equality. Integrality strengthens (5)
to

\[
                              S\geq N.                         \tag{6}
\]

Since each positive factor contributes at most \(d-2\),

\[
 k_+\geq\left\lceil\frac{N}{d-2}\right\rceil,
 \qquad
 M_+=S+2k_+
 \geq N+2\left\lceil\frac{N}{d-2}\right\rceil.               \tag{7}
\]

When \(d\geq N+1\), the universal bounds \(S\geq N-1\), \(k_+\geq1\),
and \(M_+\geq N+1\) are attained by the direct \(p\)-order cone

\[
                 K_{p,N+1}=\{(t,x):t\geq\|x\|_p\}             \tag{8}
\]

with the slice \(t=1\).

## The grouped perspective cone

For a group size \(r\geq1\), define the closed perspective cone

\[
 \mathcal P_{p,r}=
 \operatorname{cl}\left\{(u,v,w)\in\mathbb R^2\times\mathbb R^r:
 u>0,\ v>0,\ u\geq\frac{\|w\|_p^p}{v^{p-1}}\right\}.          \tag{9}
\]

This is the conic epigraph of the perspective of the closed convex
function \(w\mapsto\|w\|_p^p\). It is closed by definition,
full-dimensional, and pointed; at \(v=0\), its closure forces \(w=0\) and
allows only \(u\geq0\). Thus \(\mathcal P_{p,r}\) is a proper cone of
dimension \(r+2\).

For \(x\in\mathbb R^r\) and \(y\in\mathbb R^r\), put

\[
 A(x)=(\|x\|_p^p,1,x),
 \qquad
 B(y)=\left(\frac1p,\frac{\|y\|_q^q}{q},-y\right).             \tag{10}
\]

Then \(A(x)\in\partial\mathcal P_{p,r}\). Scaled Young's inequality gives,
for every \((u,v,w)\in\mathcal P_{p,r}\),

\[
 \frac{u}{p}+\frac{v\|y\|_q^q}{q}-w\cdot y\geq0.             \tag{11}
\]

Therefore \(B(y)\in\mathcal P_{p,r}^*\). Equality is attained by the
usual duality map, so \(B(y)\) is a boundary dual factor. In particular,

\[
 \langle A(x),B(y)\rangle
 =\frac{\|x\|_p^p}{p}+\frac{\|y\|_q^q}{q}-x\cdot y.           \tag{12}
\]

## Matching grouped lift

Partition \(\{1,\ldots,N\}\) into

\[
 k=\left\lceil\frac{N}{d-2}\right\rceil                     \tag{13}
\]

nonempty groups \(G\) of size \(r_G\leq d-2\). Introduce
\((u_G,v_G,w_G)\in\mathcal P_{p,r_G}\), impose

\[
                         v_G=1\quad\text{for every }G,
 \qquad                 \sum_Gu_G=1,                          \tag{14}
\]

and project by \(x_G=w_G\). Equations (9) and (14) say

\[
                         u_G\geq\|x_G\|_p^p,
 \qquad                 \sum_Gu_G=1.                          \tag{15}
\]

Their projection is exactly \(B_p^N\). The affine slice is strictly
feasible at \(x=0\), \(u_G=1/k\), so its minimal cone face is the full
product. On \(\partial B_p^N\), equality of the sums in (15) forces the
unique boundary fiber

\[
                         u_G=\|x_G\|_p^p.                      \tag{16}
\]

For \(y\in\partial B_q^N\), assign the equality \(\sum_Gu_G=1\) the
multiplier \(1/p\) and the equality \(v_G=1\) the multiplier
\(\|y_G\|_q^q/q\). The resulting dual slack block is exactly \(B(y_G)\),
and the multiplier objective is

\[
                       \frac1p+\frac1q\sum_G\|y_G\|_q^q=1.   \tag{17}
\]

Thus the primal and normalized-dual contact graphs are compact global
\(C^1\) sheets projecting diffeomorphically to the two boundaries. Both
selections are \(C^1\) because \(|t|^p\) and \(|t|^q\) are \(C^1\) for
\(p,q>1\). Summing (12) over the groups gives the full slack identity

\[
 \sum_G\langle A(x_G),B(y_G)\rangle
 =\frac1p+\frac1q-x\cdot y
 =1-x\cdot y.                                                  \tag{18}
\]

The construction has

\[
 S=\sum_Gr_G=N,
 \qquad k=\left\lceil\frac{N}{d-2}\right\rceil,
 \qquad M=\sum_G(r_G+2)=N+2k,                                 \tag{19}
\]

so it attains every lower bound in the first row of (2).

## Scope and literature boundary

Perspective epigraphs, Young's inequality, and power-cone modeling are
standard convex-analysis tools. The single-cone representation (8) is also
standard. Neither construction is claimed as new.

The apparently new statement is their combination with the saturated
sphere-submersion obstruction to obtain the exact regularity-constrained
optima (2) for every \(1<p<\infty\). A targeted search found no source
connecting globally smooth primal-dual contact selections of \(\ell_p\)
balls to sphere-submersion rigidity, or deriving this one-unit capacity and
ambient-dimension phase transition. Novelty remains subject to specialist
review.

The cone construction and dual certificate were independently audited,
including closure, pointedness, Slater, unique boundary fibers, Young
scaling, multiplier normalization, and the \(C^1\) regularity at zero.
The lower theorem is independently audited in the companion
[sphere-submersion curvature-gap note](2026-09-04-sphere-submersion-curvature-gap.md).
For \(p\ne2\), one primal-dual side generally fails to be \(C^2\) at
coordinate zeros; the theorem deliberately uses the sharp \(C^1\) class.
