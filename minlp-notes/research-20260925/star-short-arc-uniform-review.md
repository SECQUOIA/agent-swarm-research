# Independent audit of uniformly conditioned star moment gaps

Date: 2026-09-25. Status: the short-arc construction is valid, including
uniform spectral bounds. This audit supplies explicit indexing and checks
the transfer to the original epigraph. It does not establish novelty.

## Conclusion and precise scope

For every integer \(N\ge2\), the subsetwise \((N-1)\)-leaf compatibility
relaxation in [star-hierarchy-specker-gap.md](star-hierarchy-specker-gap.md)
has a strict projected gap for a quadratic star \(Q_N\) satisfying

\[
 \frac1{24}I\prec Q_N\prec3I.
\]

The original means have bounded Euclidean norm independently of \(N\), and
the activity means stay in a fixed compact subinterval of \((0,1)\).
Thus failure of exactness at every finite order does not require an
increasingly ill-conditioned quadratic or unbounded original means. The
certified gap in the equally spaced family below decreases as
\(\Theta(N^{-3})\). The result gives strict nonexactness, not a
dimension-independent gap or hardness of optimization.

Here a group has its own full joint PSD parent decomposition, while all
groups share the center moment matrix and the one-leaf moment matrices.
The proof does not address stronger hierarchies that share joint moments
of two or more leaves on group intersections.

## Explicit geometry and indexing

Set \(\beta=\pi/12\). Choose distinct angles

\[
 -\beta=\theta_1<\theta_2<\cdots<\theta_N=\beta,
 \qquad \widetilde u_i=(\cos\theta_i,\sin\theta_i).
\]

Equal spacing is optional until the quantitative calculation below. Write
\(\widetilde P=\operatorname{conv}\{\pm\widetilde u_i\}\), and define
the half-boundary unit edge tangents by

\[
 \widetilde e_0=(1,0),\qquad
 \widetilde e_i=
 \left(-\sin\frac{\theta_i+\theta_{i+1}}2,
        \cos\frac{\theta_i+\theta_{i+1}}2\right)
       \quad(1\le i<N),\qquad
 \widetilde e_N=(-1,0).
\]

The vector \(\widetilde e_0\) points from
\(-\widetilde u_N\) to \(\widetilde u_1\), while
\(\widetilde e_N\) points from \(\widetilde u_N\) to
\(-\widetilde u_1\). In particular, both long connecting edges are
accounted for, and \(\widetilde e_N=-\widetilde e_0\).

Put \(\widetilde g_i=\widetilde e_{i-1}-\widetilde e_i\).
Rotate every vector by \(-\pi/3\), and call the resulting vectors
\(u_i,e_i,g_i\). Coordinates after rotation are denoted by \((x,z)\).
Rotation does not change perimeters or scalar products. Write
\(P=\operatorname{conv}\{\pm u_i\}\) and \(p=\operatorname{perim}(P)\).

### The cone bound

Before rotation, the endpoint directions of \(\widetilde g_i\) are

\[
 \arg\widetilde g_1=-\frac\pi4+
                         \frac{\theta_1+\theta_2}4,
 \qquad
 \arg\widetilde g_N=\frac\pi4+
                         \frac{\theta_{N-1}+\theta_N}4.
\]

For \(1<i<N\), the direction is

\[
 \arg\widetilde g_i=
   \frac{\theta_{i-1}+2\theta_i+\theta_{i+1}}4.
\]

These formulas follow from
\(e^{i\alpha}-e^{i\tau}
=2\sin((\tau-\alpha)/2)e^{i((\alpha+\tau)/2-\pi/2)}\)
for \(0<\tau-\alpha<\pi\). All directions lie in
\([-7\pi/24,7\pi/24]\), and they are strictly increasing. After
rotation they therefore lie in

\[
 [-5\pi/8,-\pi/24].                                      \tag{1}
\]

Consequently \(w_i=-g_{i,z}>0\), and, by telescoping,

\[
 \sum_i g_i=e_0-e_N=2e_0=(1,-\sqrt3),\qquad
 W:=\sum_iw_i=\sqrt3.                                    \tag{2}
\]

Centering the short arc directly on the negative \(z\)-axis would instead
give \(W=2\) and a singular quadratic. The fixed nonzero rotation is an
essential part of the construction.

### The signed-sum bound

One has the exact identity

\[
 \max_{\varepsilon\in\{-1,1\}^N}
       \left\|\sum_i\varepsilon_i g_i\right\|=2.          \tag{3}
\]

To prove the upper bound, fix a unit vector \(v\). The directions of the
\(g_i\) are ordered in an angular interval of length less than \(\pi\).
As the direction varies across this interval, \(v\cdot g_i\) changes
sign at most once. A choice of signs maximizing
\(v\cdot\sum_i\varepsilon_i g_i\) can therefore be chosen to have
at most one sign transition. The sums from those choices are

\[
 \pm\left(\sum_{i\le j}g_i-\sum_{i>j}g_i\right)
 =\mp2e_j\qquad(0\le j\le N),                            \tag{4}
\]

because \(\sum_{i\le j}g_i=e_0-e_j\) and
\(\sum_i g_i=2e_0\). Hence the support function of the zonotope
\(\sum_i[-g_i,g_i]\) is bounded above by 2 in every unit direction.
All its points have norm at most 2. Equality follows by taking all signs
positive, whose sum is \(2e_0\).

This proof also identifies the zonotope as
\(\operatorname{conv}\{\pm2e_j:0\le j<N\}\). It avoids assuming
that an arbitrary sign pattern itself has only one transition.

### The perimeter identity

The exact dual pairing is

\[
 \sum_i g_i\cdot u_i=\frac p2.                           \tag{5}
\]

Indeed, the left side telescopes to

\[
 e_0\cdot(u_1+u_N)+
 \sum_{i=1}^{N-1}e_i\cdot(u_{i+1}-u_i)
 =\|u_1+u_N\|+\sum_{i=1}^{N-1}\|u_{i+1}-u_i\|.
\]

This is one half of the boundary length of \(P\).

## Compatibility of every proper subfamily

Let \(p_{-i}\) be the perimeter after deleting \(u_i,-u_i\), using
twice the length as the perimeter of a segment. Every listed point is a
strict vertex of \(P\), since it is a distinct point on the unit circle.
Strict triangle inequalities at the removed vertices imply

\[
 4\le p_{-i}<p.
\]

The lower bound follows because the remaining polygon contains a unit
diameter segment. Choose

\[
 \frac4p<\eta<\min_i\frac4{p_{-i}}.                     \tag{6}
\]

The interval is nonempty and lies below or at 1, so \(0<\eta<1\).
By the planar unbiased-effect compatibility criterion proved in
[star-hierarchy-specker-gap.md](star-hierarchy-specker-gap.md), the effects

\[
 M_i^*=\frac12\left[I+\eta
             (u_{i,x}\sigma_x+u_{i,z}\sigma_z)\right]      \tag{7}
\]

are incompatible together and compatible on every proper subfamily.
Strictness in (6) gives positive scalar slack in the planar parent
construction. In particular, each proper subfamily has an actual finite
scalar-moment realization, rather than requiring only limiting
zero-mass, positive-variance atoms.

The compatibility criterion is prior work, as discussed in the linked
note. This audit verifies its use here; it makes no new claim for that
criterion or for the existence of arbitrary-order incompatibility.

## A homogeneous witness and its quadratic realization

Let \(B_i=g_{i,x}\sigma_x+g_{i,z}\sigma_z\). By (3),
\(\sum_i\varepsilon_iB_i\preceq2I\) for every sign pattern. Thus
every compatible tuple \(M,M_i\), with an arbitrary PSD total matrix
\(M\), satisfies

\[
 \sum_i\operatorname{tr}[B_i(2M_i-M)]\le2\operatorname{tr}M.
                                                               \tag{8}
\]

Indeed, expand the left side using a joint parent \(G_\varepsilon\)
and apply the matrix inequality separately to each positive semidefinite
parent. This step permits biased marginals and varying center variance;
a witness restricted to \(M=I\) would be insufficient.

Write

\[
 M=\begin{pmatrix}1&0\\0&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix},\qquad
 a=\frac{2+W}{2},\qquad b_i=\sqrt{w_i}.
\]

Expanding (8), without imposing unbiasedness on the variable tuple,
gives

\[
 L(v,s,r):=av+\sum_i[-2g_{i,x}s_i-w_ir_i]\ge
 C:=\sum_i g_{i,z}z_i-\frac{2+\sum_i g_{i,z}}2.             \tag{9}
\]

The candidate from (7) has

\[
 v^*=1,\qquad z_i=\frac{1+\eta u_{i,z}}2,\qquad
 s_i^*=\frac{\eta u_{i,x}}2,\qquad
 r_i^*=\frac{1-\eta u_{i,z}}2.
\]

Equations (5) and (9) give the exact violation

\[
 C-L(v^*,s^*,r^*)=\eta\frac p2-2>0.                       \tag{10}
\]

Choose the original center mean to be zero and the leaf means to be

\[
 y_i=-b_i s_i^*-\frac{z_i g_{i,x}}{b_i}.                  \tag{11}
\]

For the quadratic star \(Q_N=\left(\begin{smallmatrix}a&b^T\\b&I\end{smallmatrix}\right)\),
leaf elimination gives the moment objective

\[
 F(v,s,r)=av+\sum_i\left[
          \frac{(y_i+b_is_i)^2}{z_i}-w_ir_i\right].
\]

The exact identity

\[
 F(v,s,r)-F(v^*,s^*,r^*)=
 L(v,s,r)-L(v^*,s^*,r^*)+
 \sum_i\frac{w_i}{z_i}(s_i-s_i^*)^2                      \tag{12}
\]

follows by expanding the squares and using (11). Therefore the true closed
indicator epigraph at these fixed original means and activities has lower
boundary at least

\[
 F(v^*,s^*,r^*)+\eta\frac p2-2,
\]

while the subsetwise \((N-1)\)-leaf relaxation has value at most
\(F(v^*,s^*,r^*)\). The closed-hull passage is justified by coercivity of
\(Q_N\), exactly as in the linked regular-family note: bounded epigraph
coordinates bound the second moments, so the compatible parent matrices
have a convergent subsequence. The limiting \(z_i\) here are positive.

## Uniform spectral and data bounds

By (2), \(\|b\|^2=W=\sqrt3\) and

\[
 a=1+\frac{\sqrt3}{2},\qquad
 \gamma:=a-W=1-\frac{\sqrt3}{2}>\frac18.
\]

On the leaf subspace orthogonal to \(b\), the eigenvalue of \(Q_N\)
is 1. Its two remaining eigenvalues are those of

\[
 \begin{pmatrix}a&\sqrt W\\\sqrt W&1\end{pmatrix},
\]

and hence are exactly

\[
 \lambda_\pm=1+\frac W4
          \pm\frac{\sqrt{W(W+16)}}4.                     \tag{13}
\]

Their product is \(\gamma\), and their sum is
\(a+1=2+\sqrt3/2<3\). Both are positive. Thus
\(\lambda_+<3\) and
\(\lambda_-=\gamma/\lambda_+>1/24\), proving the claimed uniform
bounds and a condition-number bound below 72. In fact the full nontrivial
spectrum is independent of \(N\), not just bounded uniformly.

The rotated \(u_i\) have angles in \([-5\pi/12,-\pi/4]\). Thus

\[
 \frac{1-\cos(\pi/12)}2\le z_i<\frac12.                  \tag{14}
\]

The lower bound uses only \(\eta<1\), so it is uniform in \(N\) and
the choice in (6). By (1),
\(|g_{i,x}|/w_i\le\cot(\pi/24)\). Equations (11),
\(|s_i^*|\le1/2\), and \(z_i\le1\) therefore give

\[
 |y_i|\le\sqrt{w_i}\left(\frac12+\cot\frac\pi{24}\right),
 \qquad
 \sum_i y_i^2\le\sqrt3
                  \left(\frac12+\cot\frac\pi{24}\right)^2. \tag{15}
\]

In particular, arbitrarily small interior coupling coefficients do not
cause the prescribed means to diverge. The bounds are deliberately loose.
They establish bounded data, not a useful constant-size relative gap.

There is also a true feasible law with uniformly bounded objective value:
set the center identically to zero, and let an active leaf have value
\(y_i/z_i\). Its expected cost is \(\sum_i y_i^2/z_i\). With
\(T=\cot(\pi/24)\), the candidate PSD condition gives
\((s_i^*)^2/z_i\le r_i^*\le1\), and (11) gives

\[
 \sum_i\frac{y_i^2}{z_i}
 \le2\sum_i w_i\left[\frac{(s_i^*)^2}{z_i}
                   +z_i\left(\frac{g_{i,x}}{w_i}\right)^2\right]
 \le2\sqrt3(1+T^2).
\]

## Size of the equally spaced certified gap

Take \(\theta_i=-\beta+2\beta(i-1)/(N-1)\), and put
\(h=\beta/(N-1)\). Then

\[
 S:=\frac p4=\cos\beta+(N-1)\sin h.
\]

For \(N\ge3\), deleting an interior opposite pair reduces \(p/4\)
by

\[
 d=2\sin h-\sin(2h)>0.                                  \tag{16}
\]

Deleting an endpoint opposite pair reduces \(p/4\) by
\(\sin h+\cos\beta-\cos(\beta-h)\), which is strictly larger.
For completeness, the chord-excess identity

\[
 \sin A+\sin B-\sin(A+B)
 =4\sin(A/2)\sin(B/2)\sin((A+B)/2)
\]

shows this by setting \(A=h\), and comparing \(B=h\) with
\(B=\pi/2-\beta\). The latter value is larger, and all factors
involving \(B\) increase throughout the relevant interval. Hence
\(\max_i p_{-i}/4=S-d\).

Choose the midpoint

\[
 \eta=\frac12\left(\frac1S+\frac1{S-d}\right).
\]

Its certified gap is exactly

\[
 \eta\frac p2-2=\frac d{S-d}.                            \tag{17}
\]

Since \(d=h^3+O(h^5)\) and
\(S\to\cos\beta+\beta>0\), the right side is
\(\Theta(N^{-3})\). This is the size of the proved lower bound;
the calculation does not give an upper bound on the actual projected gap.
For \(N=2\), each proper nonempty polygon is a segment, and the midpoint
choice \(\eta=(1/S+1)/2\) gives certified gap \(S-1>0\).

## Review and verification record

The half-boundary indexing, cone directions, signed-sum bound, perimeter
pairing, homogeneous witness, square remainder, spectral calculation,
bounded original means, and gap asymptotics were checked directly. A second
reviewer independently checked the angle formulas, eigenvalues, transfer
algebra, and bounded-mean conclusion. This is mathematical review, not
formal verification or a guarantee of correctness.

The targeted command actually run was

```text
python research-20260925/check_star_short_arc.py
```

It passed for \(N=2,\ldots,12,32,128,512\), checking the cone signs,
telescoping identities, spectral bounds, activity and mean bounds, and
the exact-form tangent identity on unrelated moment perturbations. For
\(N\le12\), it also enumerates all sign patterns and all single-pair
deletions. For example, the certified gaps for \(N=3,12,128\) were
approximately \(1.82351\cdot10^{-3}\), \(1.09794\cdot10^{-5}\), and
\(7.13499\cdot10^{-9}\). The scaled quantity
\((N-1)^3d/(S-d)\) approaches \(0.0146152\).

The script uses floating-point arithmetic. It can expose indexing,
scaling, and algebra errors; it does not certify exact compatibility,
strict inequalities for arbitrary \(N\), or novelty. Those mathematical
claims depend on the proofs above.

This note does not claim that the hierarchy is optimal among formulations,
that higher consistency requirements fail, or that the result is new in
optimization. The prior-work discussion in the linked note remains
necessary. No project-wide verification or CI inspection was performed.
