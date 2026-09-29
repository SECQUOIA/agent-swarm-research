# Independent review of the uniformly conditioned short-arc star gap

Date: 2026-09-25.

## Verdict and reviewed assumptions

The construction in [Every proper leaf subset can miss a quadratic-star
hull under uniform conditioning](star-uniform-condition-subset-gaps.md)
is correct for the specified subsetwise moment relaxation. The signed-sum
witness, strict compatibility thresholds, positive definite local scalar
realizations, fixed spectrum, and projected epigraph gap pass independent
adversarial review. This review also gives a direct affine inequality in
the original variables, which makes passage to the closed hull immediate.
No claim of publication novelty follows from this review.

The geometric argument was checked under the slightly more general
assumptions

\[
 N\ge2,\qquad 0<\delta\le\pi/6,\qquad
 -\delta/2=t_0<t_1<\cdots<t_{N-1}=\delta/2.
\]

Strict ordering is necessary: repeated angles could make an edge tangent
undefined. The primary note takes the valid special case of equally spaced
angles and \(\delta=\pi/6\). Its notation is used below:
\(p_i=(\cos t_i,\sin t_i)\), \(p=\operatorname{perim}
(\operatorname{conv}\{\pm p_i\})\), and \(p_-\) is the maximum perimeter
after deleting one opposite pair. The center and leaf continuous variables
are unrestricted real numbers. The center indicator is one at the candidate.

The relaxation shares the total center moment matrix \(M\) and the
single-leaf matrices \(M_i\). Each proper leaf subset may use its own joint
parent. It does not identify the joint pattern matrices on intersections
of different subsets. This distinction is part of the theorem's scope.

## Polygon identities and sign radius

Write \(u_i\) for the unit tangent from \(p_i\) to \(p_{i+1}\), for
\(i<N-1\), and put

\[
 u_{N-1}=\frac{-p_0-p_{N-1}}{\|-p_0-p_{N-1}\|}=(-1,0),
 \qquad u_{-1}=-u_{N-1},\qquad g_i=u_{i-1}-u_i.
\]

Direct summation gives \(\sum_i g_i=(2,0)\). Summation by parts gives

\[
 \begin{aligned}
 \sum_i g_i\cdot p_i
 &=\sum_{i=0}^{N-2}u_i\cdot(p_{i+1}-p_i)
     -u_{N-1}\cdot(p_0+p_{N-1})\\
 &=\sum_{i=0}^{N-2}\|p_{i+1}-p_i\|
     +\|p_0+p_{N-1}\|=p/2.
 \end{aligned}
\]

For \(i<N-1\), the angle of \(u_i\) is
\(\pi/2+(t_i+t_{i+1})/2\). The directions of the nonzero \(g_i\)
are strictly increasing and lie in

\[
 (-\pi/4-\delta/4,\ \pi/4+\delta/4).
\]

Consequently the boundary of \(Z=\sum_i[-g_i,g_i]\) is traced by flipping
the generators in this angular order and then following the opposite path.
After a prefix is flipped, its vertex is

\[
 \sum_i g_i-2\sum_{i=0}^j g_i=2u_j.
\]

The initial vertex is \(-2u_{N-1}\). Thus the vertices are precisely
\(\{\pm2u_i:0\le i<N\}\), with no missing factor of two. They all have
norm two. Their convex hull lies in the radius-two disk, and at least one
signed sum attains that radius. Therefore

\[
 \max_{\varepsilon\in\{-1,1\}^N}
       \left\|\sum_i\varepsilon_i g_i\right\|=2.
\]

Every \(p_i\) is a strict vertex of the full symmetric polygon. Deleting
an opposite pair replaces the two incident edges at each vertex by their
strictly shorter chord. For \(N\ge3\), this proves a strict perimeter
decrease. For \(N=2\), the remaining body is a unit-radius segment and
has perimeter four under the stated convention, while

\[
 p=4[\sin(\delta/2)+\cos(\delta/2)]>4.
\]

Hence \(4\le p_-<p\) in every case. The primary note's midpoint choice
\(\eta=(4/p+4/p_-)/2\) satisfies \(0<\eta<1\), \(\eta p>4\), and
\(\eta p_-<4\), including \(N=2\).

## Rotation, positivity, and the exact spectrum

Let \(T\) rotate by \(-\pi/3\), and write

\[
 q_i=Tp_i,\qquad Tg_i=(c_i,-w_i).
\]

The rotated gradient angles lie in
\((-7\pi/12-\delta/4,-\pi/12+\delta/4)\), which is contained in the
open lower half-plane for the reviewed values of \(\delta\).
In particular, the primary note's interval
\((-5\pi/8,-\pi/24)\) at \(\delta=\pi/6\) is correct. Thus every
\(w_i>0\), and

\[
 \sum_i c_i=1,\qquad W:=\sum_iw_i=\sqrt3.
\]

For

\[
 a=(2+\sqrt3)/2,\qquad b_i=\sqrt{w_i},\qquad
 Q=\begin{pmatrix}a&b^T\\b&I_N\end{pmatrix},
\]

the Schur complement is \(\gamma=(2-\sqrt3)/2>0\).
There are \(N-1\) eigenvalues equal to one. The other two are exactly

\[
 \lambda_\pm=
 \frac{4+\sqrt3\ \pm\sqrt{3+16\sqrt3}}4.
\]

They are approximately \(0.0475341536754\) and \(2.81849125011\).
The entire spectrum, apart from the multiplicity of one, is independent
of \(N\) and of the positions of the internal arc points. The primary
note's simpler bounds \(I/24\prec Q\prec3I\) and \(\kappa_2(Q)<72\)
therefore hold. Some individual edge weights can tend to zero as \(N\)
increases; this does not contradict the spectral bounds.

## Actual finite local scalar laws

The planar perimeter criterion used in the primary note is proved in
[the earlier regular-family note](star-hierarchy-specker-gap.md#why-every-proper-subfamily-is-compatible).
Its zonotope proof applies to these unequally spaced planar vectors as
well. Every proper subset has perimeter at most \(\eta p_-<4\), so its
effects have a joint PSD parent.

The strict inequality permits parents with positive definite pattern
matrices. The primary note's proof is valid: for any nonempty proper
subset \(J\), choose \(\eta'>\eta\) with its polygon perimeter still
below four, take a parent \(G'_S\) at \(\eta'\), and set

\[
 G_S=\frac\eta{\eta'}G'_S+
       \left(1-\frac\eta{\eta'}\right)2^{-|J|}I_2.
\]

These matrices are positive definite, sum to \(I_2\), and have the required
single-leaf marginals at \(\eta\). The identity contribution to each
single-leaf marginal is half of its contribution to the total matrix,
which verifies the scaling exactly. The empty subset is immediate.

An independent direct check used the polygon's zonotope parent.
If \(P_J=\sum_{j=1}^m[-h_j,h_j]\) and
\(s=1-\sum_j\|h_j\|>0\), add \(sI_2/(2m)\) to each of the two parent
effects \((\|h_j\|I_2\pm h_j\cdot\sigma)/2\). For each measurement,
the two response probabilities on an opposite pair sum to one. The
added terms therefore replace exactly the fair response to the original
residual outcome \(sI_2\). Every nonzero postprocessed pattern matrix is
positive definite.

For a matrix

\[
 G=\begin{pmatrix}\mu&\ell\\\ell&r\end{pmatrix}\succ0,
\]

take scalar atoms at
\(\ell/\mu\pm\sqrt{r/\mu-(\ell/\mu)^2}\), each of mass \(\mu/2\).
Their moment matrix is exactly \(G\). Labeling these atoms by their
patterns produces an actual local law of the center and indicators.
The total matrix \(I_2\) gives mass one, center mean zero, and center
second moment one. If leaf variables are also desired, define locally

\[
 Y_i=Z_i\left(\frac{y_i+b_i s_i^*}{z_i}-b_iX\right).
\]

This realizes the prescribed leaf means and attains the corresponding
conditional square-completion costs. The laws may differ between
subsets, exactly as allowed by the specified relaxation.

## A direct affine certificate in the original variables

There is a globally valid affine inequality that avoids the need to
extract a bounded sequence of moments. With the same star coefficients,
every original epigraph point satisfies

\[
 \boxed{\quad
 t+x_0+\sum_i\frac{2c_i}{b_i}y_i+
       \sum_i\left(w_i+\frac{c_i^2}{w_i}\right)z_i
       \ge-\gamma.\quad}                                      \tag{1}
\]

Here \(x_0\) is the center coordinate and \(y_i\) the leaf coordinate.
The inequality remains valid when the root indicator is free.

To prove it directly, let \(S\) be the active leaf support and set

\[
 h=2\sum_{i\in S}(c_i,-w_i)-\sum_i(c_i,-w_i).
\]

The sign-radius bound gives \(\|h\|\le2\). Put
\(W_S=\sum_{i\in S}w_i\) and \(C_S=\sum_{i\in S}c_i\). Then
\(h_x=2C_S-1\) and \(h_z=W-2W_S\). On this support there is the exact
identity

\[
\begin{aligned}
 &x^TQx+x_0+\sum_i\frac{2c_i}{b_i}y_i+
      \sum_i\left(w_i+\frac{c_i^2}{w_i}\right)z_i+\gamma\\
 &\quad=\sum_{i\in S}
        \left(y_i+b_ix_0+\frac{c_i}{b_i}\right)^2
       +\frac{(2+h_z)x_0^2-2h_xx_0+(2-h_z)}2.
                                                               \tag{2}
\end{aligned}
\]

The residual quadratic has coefficient matrix
\(\tfrac12\begin{pmatrix}2+h_z&-h_x\\-h_x&2-h_z\end{pmatrix}\)
with eigenvalues \((2\pm\|h\|)/2\), so it is nonnegative. For a point
with \(t\ge x^TQx\), add the nonnegative epigraph slack to (2).
This proves (1), including points with inactive leaves whose continuous
coordinates vanish. Linearity and continuity extend (1) to the closed
convex hull without assumptions about the approximating means.

At the primary note's candidate, set

\[
 v^*=1,\quad z_i=(1+\eta q_{i,z})/2,\quad
 s_i^*=\eta q_{i,x}/2,\quad r_i^*=(1-\eta q_{i,z})/2,
 \qquad y_i=-b_i s_i^*-z_i c_i/b_i.
\]

Substituting \(x_0=0\) and \(t=F(v^*,s^*,r^*)\) into the left side of
(1), and then adding \(\gamma\), gives exactly

\[
 2-\eta\sum_i(Tg_i)\cdot q_i
 =2-\eta p/2=-\Delta_N<0.
\]

Thus (1) certifies the stated projected gap \(\Delta_N\). The homogeneous
PSD witness and the exact tangent identity in the primary note also pass
review; its bounded-moment closure proof is valid. Inequality (1) provides
a shorter independent closure argument.

## Verification actually performed

One targeted inline command of the form `python - <<'PY' ... PY` used
NumPy and SymPy. It used random seed `702`, \(\delta=\pi/6\), and
\(N=2,\ldots,10\). For each \(N\), the endpoints were fixed and the
\(N-2\) internal angles were sampled independently and sorted. These
are checks of the more general reviewed construction, rather than the
primary note's equally spaced instances.

The command enumerated all \(2^N\) signs, checked both telescoping
identities, computed every one-leaf deletion perimeter, selected the
threshold midpoint, checked positive weights and strict local feasibility,
computed the star eigenvalues, and evaluated (1) at the candidate. The
largest floating-point discrepancy among the geometric identities was
`4.440892098500626e-16`. All assertions passed. The reported values were:

| \(N\) | Sign radius | Certified gap, rounded | Smallest eigenvalue | Largest eigenvalue |
|---:|---:|---:|---:|---:|
| 2 | 2 | 0.225 | 0.0475341536754 | 2.81849125011 |
| 3 | 2 | 0.000779 | 0.0475341536754 | 2.81849125011 |
| 4 | 2 | 0.000317 | 0.0475341536754 | 2.81849125011 |
| 5 | 2 | 0.000119 | 0.0475341536754 | 2.81849125011 |
| 6 | 2 | 0.00000437 | 0.0475341536754 | 2.81849125011 |
| 7 | 2 | 0.000000127 | 0.0475341536754 | 2.81849125011 |
| 8 | 2 | 0.000000715 | 0.0475341536754 | 2.81849125011 |
| 9 | 2 | 0.000000554 | 0.0475341536754 | 2.81849125011 |
| 10 | 2 | 0.00000237 | 0.0475341536754 | 2.81849125011 |

The same command checked the following polynomial identity exactly with
SymPy, using symbolic \(R,W,W_S,S_x,C_S,x\):

\[
 \left(\frac{R+W}{2}-W_S\right)x^2+(S_x-2C_S)x+
       \frac{R-W}{2}+W_S
 =\frac{(R+h_z)x^2-2h_xx+R-h_z}{2},
 \quad h_x=2C_S-S_x,\quad h_z=W-2W_S.
\]

It printed `PASS exact symbolic residual identity`. This verifies the
displayed algebraic transformation underlying (2). The geometric proof,
finite-law realization, compatibility criterion, and scope were checked
by mathematical reasoning. Floating-point enumeration tests only these
finite instances and does not prove the general result. No full-cone
optimization was run in this review, and no project-wide verification or
CI inspection was performed. Saving this review required no new tests.

## Limits of this review and of the result

The result concerns exactness of this particular subsetwise moment
relaxation. It does not prove a gap for hierarchies enforcing higher-order
overlap consistency, or a lower bound for arbitrary conic formulations.
Uniform conditioning does not provide a dimension-independent additive or
relative gap. The explicit coefficients use trigonometric values and
square roots; rational encoding guarantees were not established here.
This review checked the proof, not literature priority or practical solver
performance. The primary note's qualified novelty statement remains
necessary.
