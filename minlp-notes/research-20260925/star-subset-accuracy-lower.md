# A quantitative accuracy obstruction for subsetwise star moments

Date: 2026-09-25.

Status: explicit real and rational theorems, with
[independent adversarial review](star-subset-accuracy-review.md) and targeted
symbolic and exact rational checks.
The underlying planar measurement geometry is prior work. Publication novelty
of this quantitative optimization consequence has not been established.
The completed publication pass adds a
[fresh proof audit](publication-star-proof-review.md), a
[primary-source priority comparison](publication-star-priority-review.md),
and a [claim and evidence assessment](publication-star-assessment.md).

## Main conclusion and the relaxation being bounded

For every integer \(k\ge1\), there is an indicator-constrained positive
definite quadratic on a star with \(2k\) leaves for which imposing exact
scalar second-moment compatibility on **every subset of at most \(k\)
leaves** leaves an additive gap at least \(c/k^2\). The matrices satisfy

\[
 \frac1{24}I\prec Q_k\prec3I.                         \tag{1}
\]

The prescribed continuous means have bounded Euclidean norm, all leaf activity
means lie in a fixed compact subinterval of \((0,1)\), and the true hull
cost is positive and bounded above, uniformly in \(k\). Consequently the
relative gap also has a lower bound \(c'/k^2\), for an absolute
\(c'>0\). This strengthens the strict nonexactness result in
[the uniformly conditioned construction](star-uniform-condition-subset-gaps.md)
to an accuracy lower bound on the required subset order.

The relaxation considered here shares the center moment matrix and each
single-leaf moment matrix across subsets. Different subsets have separate
joint pattern matrices. It does **not** share higher-order pattern moments
on intersections. The result is specific to that construction; it gives
no lower bound for stronger hierarchies with those extra consistency
equations, unrestricted conic formulations, or the complexity of optimizing
quadratics on stars.

Write the star center as \(X\), its leaves as \(Y_i\), and their binary
indicators as \(Z_i\). The center indicator is fixed to one and the center
mean to zero. For prescribed \(\mathbb E Y_i=y_i\) and
\(\mathbb E Z_i=z_i\), introduce

\[
 M=\begin{pmatrix}1&0\\0&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}.
\]

A subset \(J\) is compatible when it has PSD matrices \(G^J_S\),
\(S\subseteq J\), satisfying

\[
 \sum_{S\subseteq J}G^J_S=M,\qquad
 \sum_{S\ni i}G^J_S=M_i\quad(i\in J).                 \tag{2}
\]

Let \(R_k\) be the infimum of

\[
 F(v,s,r)=av+\sum_i\left[
       \frac{(y_i+b_i s_i)^2}{z_i}-b_i^2r_i\right]       \tag{3}
\]

over moments satisfying (2) for every \(|J|\le k\). Here the star matrix
has center diagonal \(a\), leaf diagonals one, and center-leaf entries
\(b_i\). Let \(H_k\) be the lower boundary at \((0,y,1,z)\) of the
closed convex hull of its original binary-indicator epigraph. Formula (3)
is conditional square completion, as derived in
[the moment-gluing note](tree-indicator-moment-gluing.md).

Put

\[
 \beta=\frac\pi{12},\qquad S_\infty=\cos\beta+\beta,
 \qquad c_0=\frac{\beta^2\sin\beta}{8S_\infty}>0,
 \qquad C_0=\cot\frac\pi{24},
 \qquad T_0=\sqrt3(2+C_0^2).                            \tag{4}
\]

**Theorem.** The instances constructed below satisfy

\[
 \begin{split}
 &0\le R_k\le F_k^*<H_k\le T_0,\qquad
   F_k^*\ge1-\frac{\sqrt3}{2}>0,\\
 &H_k-R_k\ge\frac{c_0}{k^2},\qquad
   \frac{H_k-R_k}{H_k}\ge\frac{c_0}{T_0k^2},\\
 &\|y\|_2^2\le\frac{\sqrt3}{4}(1+C_0)^2,\qquad
   \frac{1-\cos\beta}{2}\le z_i<\frac12.
 \end{split}                                          \tag{5}
\]

Here \(F_k^*\) is the objective value of an explicit feasible relaxed
moment tuple. The constants are deliberately conservative. For orientation,
\(c_0\) is about \(0.001806\) and \(T_0\) about \(103.4\).

Thus any dimension-independent guarantee of relative error at most
\(\varepsilon\) for this relaxation on the stated class requires
\(k\ge\sqrt{c_0/(T_0\varepsilon)}\). This is a necessary order bound,
not a convergence upper bound or a claim about computational work as a
function of \(k\).

## The perimeter deficit from seeing only k leaves

Take \(N=2k\) unit vectors

\[
 p_i=(\cos\theta_i,\sin\theta_i),\qquad
 \theta_i=-\beta+\frac{2\beta i}{2k-1},
 \quad 0\le i<2k.
\]

Let \(P_k\) denote the perimeter of
\(\operatorname{conv}\{\pm p_i:0\le i<2k\}\), with the convention
that a segment has perimeter twice its length. Then

\[
 P_k=4\left[\cos\beta+(2k-1)\sin\frac\beta{2k-1}\right]. \tag{6}
\]

Define the following upper bound on all \(k\)-subset perimeters:

\[
 U_1=4,\qquad
 U_k=4\left[\cos\beta+(k-1)\sin\frac\beta{k-1}\right]
       \quad(k\ge2).                                  \tag{7}
\]

**Lemma.** Every nonempty subset \(J\) of at most \(k\) directions has
perimeter at most \(U_k\). Moreover,

\[
 P_k>U_k\ge4,\qquad
 P_k-U_k\ge\frac{\beta^2\sin\beta}{2k^2}
       \quad(k\ge2).                                  \tag{8}
\]

**Proof.** A singleton gives a unit diameter segment and perimeter four.
For \(m\ge2\) selected directions, write their angular span as
\(s\le2\beta\) and their consecutive gaps as \(d_1,\ldots,d_{m-1}\).
Their perimeter divided by four is

\[
 \sum_{j=1}^{m-1}\sin(d_j/2)+\cos(s/2)
 \le(m-1)\sin\frac{s}{2(m-1)}+\cos(s/2),               \tag{9}
\]

by concavity of sine. For \(r=m-1\ge1\), the right side increases
with \(s\in[0,2\beta]\), because its derivative is

\[
 \frac12\left[\cos\frac{s}{2r}-\sin\frac s2\right]>0.
\]

Indeed, the first term is at least \(\cos\beta\) and the second at
most \(\sin\beta\), with \(\beta<\pi/4\). For fixed \(\beta\),
the function \(f(u)=u\sin(\beta/u)\), \(u\ge1\), is strictly
increasing, since

\[
 f'(u)=\sin\frac\beta u-\frac\beta u\cos\frac\beta u
       =\int_0^{\beta/u}t\sin t\,dt>0.                \tag{10}
\]

These facts prove (7) as an upper bound for every \(m\le k\). They
also give \(P_k>U_k\). The lower bound \(U_k\ge4\) follows from
\(\cos\beta+\sin\beta>1\) for \(k\ge2\).

For the quantitative estimate, concavity gives
\(\sin t\ge(\sin\beta/\beta)t\) on \([0,\beta]\). Therefore

\[
 f'(u)\ge\frac{\beta^2\sin\beta}{3u^3}.
\]

Integrating from \(r=k-1\) to \(R=2k-1\) yields

\[
 P_k-U_k\ge\frac{2\beta^2\sin\beta}{3}
                 \left(\frac1{r^2}-\frac1{R^2}\right)
 >\frac{\beta^2\sin\beta}{2r^2}
 >\frac{\beta^2\sin\beta}{2k^2},                       \tag{11}
\]

where \(R>2r\). This proves the lemma. \(\square\)

Set

\[
 \eta_k=\frac12\left(\frac4{P_k}+\frac4{U_k}\right).
                                                               \tag{12}
\]

Then \(0<\eta_k<1\), \(\eta_kU_k<4<\eta_kP_k\), and

\[
 \Delta_k:=\frac{\eta_kP_k}{2}-2
           =\frac{P_k-U_k}{U_k}
           \ge\frac{c_0}{k^2}\quad(k\ge2),             \tag{13}
\]

because \(U_k\le4S_\infty\). For \(k=1\), (6)--(7) give
\(P_1=2\sqrt6\) and
\(\Delta_1=\cos\beta+\sin\beta-1\).
This also exceeds \(c_0\): since \(0<\beta<1\), the elementary
bounds \(\sin\beta\ge\beta-\beta^3/6\) and
\(\cos\beta\ge1-\beta^2/2\) give
\(\Delta_1\ge\beta/3\), whereas
\(c_0<\beta^3/8<\beta/3\). Here \(S_\infty>1\), because
\(\cos\beta\ge1-\beta^2/2\).

The certificate has order exactly \(k^{-2}\). Expanding sine in
(6)--(7) gives

\[
 k^2\Delta_k\longrightarrow
                \frac{\beta^3}{8S_\infty}>0.          \tag{14}
\]

This is the asymptotic size of the displayed certificate. It is not an
upper bound on the actual relaxed epigraph gap.

## Uniform quadratic and locally realizable candidate moments

The transfer now uses the short-arc construction already proved in
[the uniform-conditioning note](star-uniform-condition-subset-gaps.md)
and independently audited in
[the short-arc review](star-short-arc-uniform-review.md). The details
needed to identify the resulting original instance follow.

Let \(u_i\) be the unit tangent from \(p_i\) to \(p_{i+1}\) for
\(i<N-1\), set \(u_{N-1}=(-1,0)\), \(u_{-1}=(1,0)\), and let
\(g_i=u_{i-1}-u_i\). Rotate all vectors by \(-\pi/3\), writing
the rotated vectors as \(q_i\) and \((c_i,-w_i)\), respectively.
The established short-arc identities are

\[
 \begin{gathered}
 w_i>0,\qquad \sum_iw_i=\sqrt3=:W,\qquad
 \sum_ic_i=1,\qquad |c_i|/w_i\le C_0,\\
 \left\|\sum_i\varepsilon_i(c_i,-w_i)\right\|\le2
       \quad(\varepsilon\in\{-1,1\}^N),\qquad
 \sum_i(c_i,-w_i)\cdot q_i=P_k/2.                       \tag{15}
 \end{gathered}
\]

Define

\[
 a=1+\frac{\sqrt3}{2},\qquad b_i=\sqrt{w_i},\qquad
 Q_k=\begin{pmatrix}a&b^T\\b&I_N\end{pmatrix},\qquad
 \gamma=a-W=1-\frac{\sqrt3}{2}>0.                       \tag{16}
\]

The nontrivial two-dimensional block of \(Q_k\) is
\(\left(\begin{smallmatrix}a&\sqrt W\\\sqrt W&1\end{smallmatrix}\right)\).
Its determinant is \(\gamma>1/8\), its trace is less than three,
and all other eigenvalues are one. Consequently (1) holds, independently
of \(k\).

Take

\[
 \begin{split}
 v^*&=1,&
 z_i&=\frac{1+\eta_kq_{i,z}}2,&
 s_i^*&=\frac{\eta_kq_{i,x}}2,&
 r_i^*&=\frac{1-\eta_kq_{i,z}}2,\\
 y_i&=-\sqrt{w_i}\,s_i^*-\frac{z_ic_i}{\sqrt{w_i}}.
 \end{split}                                          \tag{17}
\]

The corresponding effects are
\(M_i^*=[I+\eta_k(q_{i,x}\sigma_x+q_{i,z}\sigma_z)]/2\).
The planar compatibility criterion says that they have a joint PSD
parent exactly when the perimeter of their centrally symmetric vector
polygon is at most four. A self-contained proof and prior-work comparison
appear in [the regular-family note](star-hierarchy-specker-gap.md#why-every-proper-subfamily-is-compatible).
Every subset of at most \(k\) has perimeter at most
\(\eta_kU_k<4\), so it is compatible; the full family is incompatible.

Each local parent can be made positive definite. Choose
\(\eta'>\eta_k\) close enough that \(\eta'U_k<4\) and \(\eta'<1\).
If \(G'_S\) is a parent at \(\eta'\), then

\[
 G_S=\frac{\eta_k}{\eta'}G'_S+
       \left(1-\frac{\eta_k}{\eta'}\right)2^{-|J|}I
                                                               \tag{18}
\]

is a positive definite parent at \(\eta_k\). Each \(G_S\) is the
moment matrix of a finite nonnegative scalar measure with at most two
atoms. Combining these pattern measures gives an actual finite law for
the center and the indicators in \(J\), satisfying the prescribed
moments. Thus local candidate feasibility is actual scalar realizability,
without limiting zero-mass atoms. Equation (3) gives
\(R_k\le F_k^*:=F(v^*,s^*,r^*)\).

## A valid cut in the original variables proves the gap

For the matrix (16), the following affine inequality is valid for the
original indicator-quadratic epigraph and its closed convex hull:

\[
 t+X+\sum_i\frac{2c_i}{\sqrt{w_i}}Y_i
       +\sum_i\left(w_i+\frac{c_i^2}{w_i}\right)Z_i
       \ge-\gamma.                                    \tag{19}
\]

Here validity even allows the center indicator to vary. To verify it,
take \(S=\{i:Z_i=1\}\) and put
\((h_x,h_z)=\sum_i(2Z_i-1)(c_i,-w_i)\). After substituting
\(t=x^TQ_kx\), the left side of (19) plus \(\gamma\) is

\[
 \sum_{i\in S}\left(Y_i+\sqrt{w_i}X+
                            \frac{c_i}{\sqrt{w_i}}\right)^2
 +\frac12[(2+h_z)X^2-2h_xX+(2-h_z)].                   \tag{20}
\]

Inactive leaves have \(Y_i=0\). The last quadratic is nonnegative
because \(h_x^2+h_z^2\le4\), by (15); its symmetric matrix is PSD.
Increasing \(t\) preserves the inequality. Affine continuity proves
validity for the closed convex hull directly, so no projection-closure
claim is needed here.

Substitute the candidate original point
\((t,X,Y,Z)=(F_k^*,0,y,z)\) into (19). Since
\(y_i=-\sqrt{w_i}s_i^*-z_ic_i/\sqrt{w_i}\), its left side plus
\(\gamma\) equals

\[
 a+\gamma-2\sum_ic_is_i^*+\sum_iw_i(z_i-r_i^*)
 =2-\eta_k\sum_i(c_i,-w_i)\cdot q_i
 =-\Delta_k.                                          \tag{21}
\]

The coefficient of \(t\) is one, so (19) proves
\(H_k\ge F_k^*+\Delta_k\). Together with (13), this yields the
additive claim in (5) in the original epigraph coordinates.

## Bounded means, bounded costs, and relative error

The \(q_i\) directions lie in \([-5\pi/12,-\pi/4]\).
Consequently (17) gives

\[
 \zeta:=\frac{1-\cos\beta}{2}\le z_i<\frac12.
\]

From \(|s_i^*|\le1/2\), \(z_i\le1/2\), and
\(|c_i|/w_i\le C_0\),

\[
 |y_i|\le\frac{\sqrt{w_i}}2(1+C_0),\qquad
 \sum_i y_i^2\le\frac W4(1+C_0)^2.                    \tag{22}
\]

At the candidate, \(0\le r_i^*\le1\) and
\(y_i+b_i s_i^*=-z_ic_i/b_i\), whence

\[
 \gamma\le F_k^*
   =a+\sum_i\frac{z_ic_i^2}{w_i}-\sum_iw_ir_i^*
   \le a+\frac W2 C_0^2.                              \tag{23}
\]

To bound the true hull cost, use the finite feasible law with \(X=0\),
independent Bernoulli indicators of means \(z_i\), and
\(Y_i=y_iZ_i/z_i\). Its expected quadratic cost is
\(\sum_i y_i^2/z_i\). Positive semidefiniteness of \(M_i^*\)
gives \((s_i^*)^2/z_i\le r_i^*\le1\). Therefore

\[
 \begin{split}
 H_k&\le\sum_i\frac{y_i^2}{z_i}\\
 &\le2\sum_i\frac{w_i(s_i^*)^2}{z_i}
       +2\sum_i\frac{z_ic_i^2}{w_i}
 \le2W+WC_0^2=T_0.                                   \tag{24}
 \end{split}
\]

For any feasible relaxed tuple, singleton compatibility gives
\(v\ge0\) and \(0\le r_i\le v\). The nonnegative square terms
in (3) then imply \(F\ge(a-W)v=\gamma v\ge0\), so
\(R_k\ge0\). Equations (13), (21), and (24) establish every claim
in (5), including the relative gap.

If a unit upper bound on true cost is desired, replace \(Q_k\) by
\(Q_k/T_0\). All costs and additive gaps scale by \(1/T_0\), while
the condition number and relative gap are unchanged. The scaled spectral
bounds are \(I/(24T_0)\prec Q_k/T_0\prec3I/T_0\); the data
remain uniformly bounded. This is only a normalization, not a stronger
conditioning claim.

## Rational data give the same inverse-square order

The rational construction already developed in
[the uniform-conditioning note](star-uniform-condition-subset-gaps.md#rational-data-with-a-uniform-spectral-bound)
also gives the quantitative conclusion. This section completes that
construction with a different choice of its rational noise parameter.

**Rational refinement.** For every integer `k>=1`, there is a rational
instance with `N=2k` leaves and total nonzero-data encoding
`O(k^2 log(k+1))` such that

\[
 \frac1{39}I\prec Q\prec12I,\qquad
 0\le R_k\le F_k^*<H_k<122,
 \qquad F_k^*\ge\frac1{13},
\]

\[
 H_k-R_k\ge\frac1{466560k^2},\qquad
 \frac{H_k-R_k}{H_k}\ge\frac1{56920320k^2}.
 \tag{25}
\]

Here the leaf diagonals can differ from one. Define `R_k` using the same
subset constraints (2) and the general-diagonal square-completion formula
(21) of the linked note. All leaf activity means satisfy
`11/416 <= z_i < 1/2`, and `||y||_2^2 <= 486/13`.

**Perimeter proof.** Use the rational directions in (19) of that note,
with angles `theta_i=4 arctan(tau_i)` and
`tau_i=(2i-(N-1))/(64(N-1))`. Let `P` be their full symmetric polygon's
perimeter, and set

\[
 \ell=\frac1{11664(N-1)^3},\qquad
 D=k\ell,\qquad U=P-D,\qquad
 \eta=\frac12\left(\frac4P+\frac4U\right).
 \tag{26}
\]

Every consecutive angular gap in the full symmetric polygon is at least
`1/[9(N-1)]`. Removing a pair of opposite vertices only increases the
surviving gaps. If at least two directions remain before a deletion, the
two gaps `A,B` adjacent to a removed vertex satisfy `A+B<=pi`.
The perimeter loss from removing the opposite pair is

\[
 16\sin(A/4)\sin(B/4)\sin((A+B)/4)
 \ge \frac{AB(A+B)}{32}\ge\ell.
\]

This includes the final deletion from two directions to one: the two
gaps then sum to `pi`, and the one-direction perimeter is four. To reach
any nonempty subset of at most `k` directions, delete at least `k`
opposite pairs. Its perimeter is therefore at most `U`. Conversely,
any subset of exactly `k` directions has perimeter at least four, so
`U>=4`. Thus `0<eta<1`, `eta U<4<eta P`, and every required subset
has a positive definite parent after the same noise-mixture construction.

The original-variable affine cut (23) in the linked note is unchanged.
Its violation at the new candidate is

\[
 \Delta=\eta P/2-2=\frac D U
 >\frac D5
 =\frac{k}{58320(2k-1)^3}
 \ge\frac1{466560k^2},
\]

using `P<5` and `U<P`. This proves the additive bound in (25).

**Uniform normalization and encoding.** Retain the rational rotation,
weights, dyadic edge coefficients and leaf diagonals from the linked
construction. Then `a=25/13`, `W=sum_i w_i=24/13`, and
`a-W=1/13`, with the displayed spectral bounds. The pre-rotation
gradient has positive first coordinate and angle in `(-pi/3,pi/3)`.
Writing the ratio of its second coordinate to its first as `t` gives
`|t|<sqrt(3)<7/4` and

\[
 \frac{|c_i|}{w_i}
 =\frac{|5+12t|}{12-5t}<8.
\]

Each direction before rotation has angle `|theta_i|<1/16`. Its rotated
second coordinate is
`v_i=(-12 cos(theta_i)+5 sin(theta_i))/13`, hence
`-197/208 <= v_i < 0`. The lower bound follows from
`cos(theta_i)<=1` and `sin(theta_i)>=-1/16`; the upper bound follows
from `cos(theta_i)>=1-1/512` and `sin(theta_i)<=1/16`.
Therefore `(1+eta v_i)/2` lies in the stated interval for `z_i`.

The rational mean formula is
`y_i=-(w_i s_i^*+z_i c_i)/b_i`, where
`b_i^2/d_i=w_i`, `1<=d_i<4`, `|s_i^*|<=1/2`, and `r_i^*<=1`.
It gives `|y_i|<=9 sqrt(w_i)/2`, proving the norm bound. The candidate
cost is

\[
 F_k^*=a+\sum_i z_i c_i^2/w_i-\sum_iw_i r_i^*
 \ge a-W=1/13.
\]

For a true feasible law take the center to be zero, independent indicators,
and active leaf values `y_i/z_i`. By `(s_i^*)^2/z_i<=r_i^*<=1`,

\[
 H_k\le\sum_i d_i y_i^2/z_i
 \le2W+64W=\frac{1584}{13}<122.
\]

Singleton compatibility still gives `0<=r_i<=v`, so every relaxed cost
is at least `(a-W)v>=0`. The relative bound follows. Finally, replacing
the old one-deletion perimeter by `U=P-k ell` uses only rational
arithmetic of polynomial bit length. The encoding proof in the linked
note therefore still gives `O(N^2 log N)` bits. No rationality of the
finite supporting atoms is asserted or needed.

## What is established and what remains open

The new implication is an explicit accuracy obstruction: even with a
single continuous separator, treewidth one, fixed spectral bounds, bounded
continuous means, and bounded true objective, this subsetwise construction
cannot promise arbitrarily accurate dimension-independent bounds at fixed
order. A necessary order is \(\Omega(\varepsilon^{-1/2})\).
The degree grows with \(k\); bounded-degree trees are not addressed.

Neither the planar compatibility criterion nor a polygon's quadratic
approximation rate should be presented as new. The contribution being
investigated is their quantitative realization as an original-variable
indicator-quadratic epigraph gap with all the stated bounds simultaneously.
The argument provides a concrete valid inequality exposing the defect and
indicates that a useful formulation needs global compatibility information,
stronger shared moments, or an approximation theorem with growing order.
It does not yet provide an algorithm for obtaining that information.

The strongest immediate follow-up questions are whether the order
\(\varepsilon^{-1/2}\) is sufficient on a meaningful class, whether
sharing higher-order overlap moments removes this obstruction, and whether
an analogous bounded-data obstruction survives bounded center degree.

## Literature comparison and verification record

Sources inherited from and examined through the preceding local notes:

- Andrejic and Kunjwal, *Joint measurability structures realizable with
  qubit measurements: Incompatibility via marginal surgery*, Physical
  Review Research 2, 043147 (2020),
  [arXiv:2003.00785](https://arxiv.org/abs/2003.00785), Corollary 8.
  Arbitrary-order qubit incompatibility is established prior work; the
  present assertion adds a bounded-data quantitative star-epigraph transfer.
- Bluhm and Nechita, *Joint measurability of quantum effects and the matrix
  diamond*, Journal of Mathematical Physics 59, 112202 (2018),
  [arXiv:1807.01508](https://arxiv.org/abs/1807.01508). Common PSD parents
  and their matrix-convex interpretation are prior theory, rather than a
  new formulation concept introduced here.
- Carmeli, Heinosaari, and Toigo, *Quantum incompatibility witnesses*,
  Physical Review Letters 122, 130402 (2019),
  [arXiv:1812.02985](https://arxiv.org/abs/1812.02985), Theorems 1--2.
  Turning incompatibility witnesses into optimization separations is
  broadly established; the present transfer has the specific quadratic,
  sparsity, normalization, and conditioning requirements stated above.
- Choi, Fattahi, Han, Gómez, and Lozano, *Convexification of mixed-integer
  quadratic optimization via decision diagrams*,
  [arXiv:2608.22815](https://arxiv.org/abs/2608.22815), Section 7.2.
  Their exact tree formulation concerns a different construction and has
  a size bound with rooted-leaf count as a parameter. This lower bound
  does not contradict that formulation.

The completed [publication priority review](publication-star-priority-review.md)
adds three especially important comparisons. Sun, Wang, Li-Jost, and Fei,
[*A Note on the Hierarchy of Quantum Measurement Incompatibilities*](https://doi.org/10.3390/e22020161),
Section 2, already define `(n,k)`-compatibility as compatibility of every
`k`-member subfamily. Zhang, Zhang, and Chitambar,
[*Cost of Simulating Entanglement in Steering Scenario*](https://arxiv.org/abs/2302.09060v3),
Proposition 4 and Corollary 2, obtain an inverse-square-root lower bound
for the number of outcomes of a global planar parent measurement. This is
a different parameter from the size of separately tested subsets, but is
close prior work for the geometric exponent. Porto, Designolle, Pokutta,
and Quintino,
[*Measurement incompatibility and quantum steering via linear programming*](https://arxiv.org/abs/2506.03045v3),
Theorem 1 and Section 3.3, provide convergent global LP approximations with
polynomial dependence on measurement count and inverse accuracy in fixed
dimension. The present obstruction to separate subset parents does not
rule out their approach. Their robustness accuracy is not automatically
an objective-error bound for the star model.

None of the examined statements supplies the simultaneous rational,
uniformly conditioned, original-epigraph theorem proved here. This scoped
comparison does not establish priority. Neither the compatibility hierarchy
nor the planar exponent is claimed as new; the candidate contribution is
their restricted optimization realization with the stated quantitative
bounds.

The perimeter lemma was independently derived and checked by a separate
geometry reviewer before the complete theorem was submitted for a fresh
adversarial review. The geometric reviewer also exhaustively checked the
maximum subset perimeter for \(k=2,\ldots,7\) in floating point; these
checks support finite cases and do not establish the theorem or novelty.
The displayed integral argument proves the lower bound for all orders.
The completed [independent review](star-subset-accuracy-review.md) accepted
the original-variable cut, closure argument, cost and spectral bounds,
relative-gap conclusion, and rational refinement. The reviewer wrote and
ran `python research-20260925/check_star_subset_accuracy_review.py`: all
eight generic three-leaf support identities and the candidate-cut identity
passed exact symbolic checks; 4,706 real-family subset perimeters passed
floating-point checks for `k=1,...,7`.

The command `python research-20260925/check_star_subset_accuracy.py` was run
by both the author and reviewer. It passed five rational instances and
852 exact subpolygon checks, including gap, mean, and cost bounds. These
finite calculations support the construction; the displayed arguments
prove the all-order assertions. No project-wide verification or CI
inspection was performed.

The fresh publication review additionally wrote and ran
`python research-20260925/check_publication_star_parents.py`.
It independently builds 215 local laws through order four using 1,964
positive definite rational pattern matrices, and checks all totals and
marginals exactly. Unlike the perimeter checker, it imports none of the
author's polygon helper functions. The publication assessment inspected
and reran this checker successfully. This is additional finite evidence
for actual local realizability, not a replacement for the all-order proof.
