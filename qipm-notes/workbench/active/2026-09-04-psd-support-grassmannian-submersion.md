# Saturated PSD factors induce Grassmannian submersions

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Headline theorem

Let \(C\subset\mathbb R^{n+1}\), \(n\geq1\), be a compact convex body with
\(0\in\operatorname{int}C\).  Assume that

\[
                         P=\partial C,\qquad D=\partial C^\circ
\]

are \(C^1\), strictly convex hypersurfaces.  Suppose their full slack has a
globally labelled \(C^1\) real-PSD factorization

\[
  1-\langle x,z\rangle
   =\sum_{i=1}^k\operatorname{tr}\bigl(X_i(x)Y_i(z)\bigr),
 \quad X_i(x),Y_i(z)\in\mathbb S_+^{r_i}.                    \tag{1}
\]

Put

\[
                         c_i=\left\lfloor{r_i^2\over4}\right\rfloor.
\]

The local PSD curvature theorem gives \(\sum_i c_i\geq n\).  If equality
holds, then for every positive-capacity block (\(c_i>0\)) there is a fixed
balanced integer

\[
 p_i\in\{\lfloor r_i/2\rfloor,\lceil r_i/2\rceil\},
 \qquad q_i=r_i-p_i,                                        \tag{2}
\]

such that

\[
 \operatorname{rank}X_i(x)=p_i,qquad
 \operatorname{rank}Y_i(z)=q_i                              \tag{3}
\]

at every contact \(\langle x,z\rangle=1\).  For each such block, the support
map

\[
 \boxed{
 \pi_i:P\longrightarrow \operatorname{Gr}_{p_i}(\mathbb R^{r_i}),
 \qquad \pi_i(x)=\operatorname{Ran}X_i(x)
 }                                                           \tag{4}
\]

is a proper surjective \(C^1\) submersion.  Its target dimension is exactly
the block capacity:

\[
 \dim\operatorname{Gr}_{p_i}(\mathbb R^{r_i})=p_iq_i=c_i.   \tag{5}
\]

Thus maximum PSD curvature is not merely a local \(p_iq_i\)-dimensional
linear channel.  Global saturation forces that channel to integrate to the
entire Grassmannian of support subspaces.  This is stronger than the
universal cone-base map, whose target has the much larger dimension
\(\dim\mathbb S_+^{r_i}-2\).

## Differential proof

Fix a contact pair \((x,z)\).  Mixed differentiation of (1) in independent
charts on \(P\) and \(D\) gives

\[
 \langle u,v\rangle
  =\sum_i H_i(u,v),\qquad
 H_i(u,v)=-\operatorname{tr}\bigl(dX_i(x)u\,dY_i(z)v\bigr). \tag{6}
\]

The pairing on the left is nondegenerate.  Indeed,
\(T_xP=z^\perp\), \(T_zD=x^\perp\), and the Euclidean pairing between these
two \(n\)-planes has zero kernel because \(\langle x,z\rangle=1\).

Write \(p=\operatorname{rank}X_i(x)\) and
\(q=\operatorname{rank}Y_i(z)\).  Complementarity
\(\operatorname{tr}(X_iY_i)=0\) implies
\(\operatorname{Ran}X_i\perp\operatorname{Ran}Y_i\), hence \(p+q\leq r_i\).
The PSD tangent calculation gives

\[
                \operatorname{rank}H_i\leq pq
                \leq\left\lfloor{r_i^2\over4}\right\rfloor=c_i. \tag{7}
\]

If \(\sum_i c_i=n\), rank subadditivity in (6) makes every inequality an
equality at every contact.  For \(c_i>0\), therefore \(p+q=r_i\), \((p,q)\)
are the two balanced integers in (2), and
\(\operatorname{rank}H_i=pq=c_i\).  A zero-capacity scalar block merely has
\(\operatorname{rank}H_i=0\); saturation does not constrain its two
complementary scalar ranks.

For a positive-capacity block, the ranks in (3) are locally constant.  For
even \(r_i\) this is immediate.
For odd \(r_i\), a change would interchange \(p\) and \(q\).  Matrix rank is
lower semicontinuous: if the rank of \(X_i\) dropped at a transition, the
complementary rank of \(Y_i\), whose sum with it is constantly \(r_i\),
would have to jump upward there, which lower semicontinuity forbids.  Since
normalized supporting polarity gives a continuous one-to-one contact
correspondence because both boundaries are \(C^1\) and strictly convex.  Its graph
is homeomorphic to \(P\cong S^n\), hence connected, so one choice of \(p_i\)
holds globally.
Constant-rank \(C^1\) PSD families have \(C^1\) range projections, for
example from the local constant-rank formula for the Moore--Penrose inverse.
Thus (4) is \(C^1\).

It remains to compute its derivative.  At the fixed contact, use the
orthogonal decomposition

\[
 \mathbb R^{r_i}=U\oplus V,qquad
 U=\operatorname{Ran}X_i(x),\quad V=\operatorname{Ran}Y_i(z),
\]

and write

\[
 X_i(x)=\begin{pmatrix}A&0\\0&0\end{pmatrix},\qquad
 Y_i(z)=\begin{pmatrix}0&0\\0&B\end{pmatrix},qquad A,B\succ0. \tag{8}
\]

Derivatives of two-sided curves in the PSD cone have the form

\[
 dX_i(x)u=\begin{pmatrix}*&C_u\\C_u^T&0\end{pmatrix},\qquad
 dY_i(z)v=\begin{pmatrix}0&E_v\\E_v^T&*\end{pmatrix}.        \tag{9}
\]

The lower-right and upper-left compressions vanish because a scalar
quadratic form that is nonnegative on a two-sided curve and zero at the
base point has zero derivative.  Equations (8)--(9) give

\[
                         H_i(u,v)=-2\operatorname{tr}(C_uE_v^T). \tag{10}
\]

Identify
\(T_U\operatorname{Gr}_p(\mathbb R^{r_i})\cong\operatorname{Hom}(U,V)\).
First-order eigenvector perturbation, or direct differentiation of the
range graph, gives

\[
                  d\pi_i(x)u=C_u^TA^{-1}\in\operatorname{Hom}(U,V). \tag{11}
\]

Consequently \(\operatorname{rank}H_i\leq\operatorname{rank}d\pi_i(x)\).
The target in (11) has dimension \(pq\), while saturation gives
\(\operatorname{rank}H_i=pq\).  Hence \(d\pi_i(x)\) is surjective at every
\(x\).  The image of a submersion is open; it is also compact and therefore
closed.  The real Grassmannian is connected, so (4) is onto.

No differentiable Gauss map and no positive-curvature assumption were used.
The primal and polar variables in (6) are independent.  Strict
complementarity and constant rank were conclusions of maximum-capacity
saturation, not extra hypotheses.

## The joint support map gives an all-order theorem

Under saturation, combine all positive-capacity support maps:

\[
 \Pi:P\longrightarrow
       \prod_{i:c_i>0}\operatorname{Gr}_{p_i}(\mathbb R^{r_i}),
 \qquad
 \Pi(x)=(\pi_i(x))_i.                                      \tag{12a}
\]

If \(d\Pi(x)u=0\), then (11) gives \(C_{i,u}=0\) for every block.
Equation (10) then gives \(H_i(u,v)=0\) for every \(i\) and every \(v\).
The nondegenerate total pairing (6) forces \(u=0\).  Since source and
target both have dimension

\[
                         n=\sum_i c_i=\sum_i p_iq_i,
\]

\(d\Pi\) is an isomorphism everywhere.  Compactness and connectedness make
\(\Pi\) a finite covering.

An order-two block would put an \(S^1\) factor in the target, whose
universal cover is noncompact; this contradicts the compact universal cover
\(P\cong S^n\).  For \(r_i\geq3\), the universal cover of the real
Grassmannian is its compact oriented Grassmannian.  Hence the covering
identifies

\[
 S^n\cong
 \prod_{i:c_i>0}
 \operatorname{Gr}_{p_i}^+(\mathbb R^{r_i}).               \tag{12b}
\]

There can be only one factor in (12b).  With two or more, the mod-two top
class of any one factor, tensored with unit classes on the others, gives
nonzero cohomology in a degree strictly between zero and \(n\).

The sole factor can only have order three.  Indeed,
\(\operatorname{Gr}_1^+(\mathbb R^3)\cong S^2\).  For \(r\geq4\), balanced
\(p,q\geq2\), and the homotopy exact sequence of

\[
 SO(p)\times SO(q)\longrightarrow SO(p+q)
       \longrightarrow \operatorname{Gr}_p^+(\mathbb R^{p+q})
\]

gives nonzero \(\pi_2\): for \(p,q\geq3\), the kernel of
\(\mathbb Z_2\oplus\mathbb Z_2\to\mathbb Z_2\) contains the diagonal
element; if one rank is two, the kernel contains the nonzero even elements
of \(\pi_1(SO(2))=\mathbb Z\).  This cannot equal
\(\pi_2(S^{pq})=0\), since \(pq\geq4\).

Thus maximum-capacity saturation is possible only for \(n=2\) with one
order-three block.  For every \(n\geq3\), integrality sharpens the local PSD
budget to

\[
 \boxed{
   \sum_i\left\lfloor{r_i^2\over4}\right\rfloor\geq n+1=N,
   \qquad N\geq4.
 }                                                          \tag{12c}
\]

This is a global-selection result.  It does not claim that an arbitrary
semidefinite lift supplies globally \(C^1\) factors.

If all positive blocks have matrix order at most \(R\geq2\), write
\(c_R=\lfloor R^2/4\rfloor\), let \(k_+\) count them, and let
\(M=\sum_i r_i(r_i+1)/2\) be the real cone-coordinate dimension.  Since
the dimension-to-capacity and rank-to-capacity ratios decrease with the
matrix order, (12c) implies

\[
 \boxed{
 \begin{aligned}
 k_+&\geq\left\lceil{N\over c_R}\right\rceil,\\
 M&\geq\left(2+{1\over\lfloor R/2\rfloor}\right)N,\\
 \nu_{\mathrm{normal}}=\sum_i r_i&\geq {R\over c_R}N .
 \end{aligned}}                                             \tag{12d}
\]

The identity for \(\nu_{\mathrm{normal}}\) is the optimal ambient normal-
barrier parameter of the chosen PSD product, including coupled normal
barriers.  The bounds in (12d) are resource ledgers, not generally matched
for \(R>3\), and they are not iteration lower bounds.

## Independent topology audit

The longer Browder--Gysin classification of all individual balanced real
Grassmannian targets is recorded and independently audited in
[Sphere submersions onto balanced real Grassmannians](2026-09-04-sphere-submersions-balanced-real-grassmannians.md).
It separately handles positive-dimensional fibers, the apparent
\(\operatorname{Gr}_2^+(\mathbb R^5)\cong Q^3\) exception, and
zero-dimensional fibers.  The joint-map covering proof above is sufficient
for (12c), but the companion supplies an independent check that no single
order-four-or-larger support target can occur.
## Exact smooth frontier for order at most three

For the Euclidean ball \(B_2^N\), \(N\geq4\), (12c) is sharp already with
orders at most three.  Partition the coordinates into groups \(G\) of size
\(g_G\in\{1,2\}\).  Use one block in \(\mathbb S_+^{g_G+1}\) and define

\[
 A_G(x)=
 \begin{pmatrix}\|x_G\|^2&x_G^T\\x_G&I_{g_G}\end{pmatrix},\qquad
 B_G(y)={1\over2}
 \begin{pmatrix}1\\-y_G\end{pmatrix}
 \begin{pmatrix}1\\-y_G\end{pmatrix}^{T}.                  \tag{13}
\]

Then \(A_G(x),B_G(y)\succeq0\), their ranks are \(g_G\) and one, and

\[
                    \operatorname{tr}(A_G(x)B_G(y))
                         ={1\over2}\|x_G-y_G\|^2.            \tag{14}
\]

Summing (14) gives \(1-\langle x,y\rangle\).  The associated affine lift is

\[
 \begin{pmatrix}s_G&x_G^T\\x_G&I_{g_G}\end{pmatrix}\succeq0
 \quad\text{for every }G,\qquad \sum_Gs_G=1.                \tag{15}
\]

Schur complements show that it projects exactly to the ball.  It is
strictly feasible at \(x=0\) with every \(s_G>0\), and every boundary fiber
is unique, \(s_G=\|x_G\|^2\).  Equations (13) give polynomial primal and
normalized dual contact sheets.  Explicitly, use multiplier \(1/2\) for
\(\sum_Gs_G=1\) and multiplier \(y_Gy_G^T/2\) for each fixed lower block
\(I_{g_G}\).  The resulting PSD dual slack is \(B_G(y)\), and the dual
multiplier objective is
\(1/2+\sum_G\|y_G\|^2/2=1\).

For products of real PSD cones of matrix order at most three with global
bi-\(C^1\) factors, the simultaneous ball optima are therefore

\[
 \boxed{
 \begin{aligned}
 k_{\min}&=\left\lceil{N\over2}\right\rceil,\\
 M_{\min}&=3N,\\
 \nu_{\min}^{\mathrm{normal}}
   &=\left\lceil{3N\over2}\right\rceil.
 \end{aligned}}                                              \tag{16}
\]

Here \(M=\sum_i r_i(r_i+1)/2\) is the real cone-coordinate dimension.
Indeed, order two and three blocks have capacities one and two and cone
dimensions three and six, respectively, so \(M=3\sum_i c_i\geq3N\), and
each block contributes at most two capacity units.  The construction uses
\(N/2\) order-three blocks if \(N\) is even, and
\((N-1)/2\) order-three blocks plus one order-two block if \(N\) is odd.
The optimal normal-barrier parameter of a product of PSD cones is the sum
of their matrix ranks.  If \(a\) and \(b\) count the order-two and
order-three blocks, respectively, minimizing \(2a+3b\) subject to
\(a+2b\geq N\) gives \(\lceil3N/2\rceil\), yielding the last value in
(16); the standard product log-determinant barrier attains it.  Scalar ray
factors cannot improve any of these minima.

The regularity restriction is essential.  This theorem does not determine
the unrestricted PSD-block frontier, and it does not convert a normal-
barrier parameter into an intrinsic iteration lower bound for the projected
ball.

## Complex and quaternionic Hermitian extension

The joint-map proof works verbatim for Hermitian PSD cones over
\(\mathbb F=\mathbb C,\mathbb H\).  Put
\(a=\dim_{\mathbb R}\mathbb F\in\{2,4\}\).  At complementary ranks \(p,q\),
the cross block has real dimension \(apq\), and maximum capacity forces
balanced strict complementarity.  The support target is

\[
                  \operatorname{Gr}_p(\mathbb F^r),
       \qquad \dim_{\mathbb R}\operatorname{Gr}_p(\mathbb F^r)=apq. \tag{17}
\]

Here the Euclidean Jordan pairing is
\(\langle X,Y\rangle=\operatorname{Re}\operatorname{tr}(XY)\), and the
mixed cross-block formula corresponding to (10) is
\(-2\operatorname{Re}\operatorname{tr}(C_uE_v^*)\).  This real-part
convention is essential for quaternionic factors.

Thus saturation of
\(\sum_i a\lfloor r_i^2/4\rfloor=n\) makes the joint support map a
same-dimensional covering from \(S^n\) onto a product of
\(\mathbb F\)-Grassmannians.  These Grassmannians are simply connected, so
the covering is a diffeomorphism.  Product cohomology again leaves one
factor.

More generally, the factors may use different fields
\(\mathbb F_i\in\{\mathbb R,\mathbb C,\mathbb H\}\), with
\(a_i=\dim_{\mathbb R}\mathbb F_i\).  The same joint covering proof forces
one Grassmannian sphere.  The complete list is

\[
\begin{array}{c|c|c}
\text{field and order}&\text{oriented support target}&\text{capacity}\\ \hline
\mathbb R,\ r=2&S^1&1\\
\mathbb R,\ r=3&S^2&2\\
\mathbb C,\ r=2&\mathbb{CP}^1=S^2&2\\
\mathbb H,\ r=2&\mathbb{HP}^1=S^4&4.
\end{array}
\]

It follows that saturation for a classical Hermitian-PSD product can occur
only when the contact-sphere dimension is \(n\in\{1,2,4\}\).  Hence an
arbitrary mixture of real, complex, and quaternionic PSD factors obeys

\[
 \boxed{
 \sum_i a_i\left\lfloor{r_i^2\over4}\right\rfloor\geq N,
 \qquad N\geq2,\quad N\notin\{2,3,5\}.
 }                                                           \tag{17a}
\]

The exceptions are sharp for Euclidean balls: the direct
\(2\times2\) Hermitian cones over
\(\mathbb R,\mathbb C,\mathbb H\), respectively isomorphic to
\(Q_3,Q_4,Q_6\), attain \(B_2^2,B_2^3,B_2^5\).

For complex Grassmannians, \(H^2(\operatorname{Gr}_p(\mathbb C^r);\mathbb
Z)\cong\mathbb Z\).  It can have the cohomology of a sphere only in real
dimension two, namely
\(\operatorname{Gr}_1(\mathbb C^2)=\mathbb{CP}^1\cong S^2\).
For quaternionic Grassmannians, the analogous first class gives
\(H^4\cong\mathbb Z\); the only sphere case is
\(\operatorname{Gr}_1(\mathbb H^2)=\mathbb{HP}^1\cong S^4\).
Consequently,

\[
\begin{array}{ll}
\displaystyle
\sum_i2\left\lfloor{r_i^2\over4}\right\rfloor\geq N,
 &\mathbb F=\mathbb C,\quad N\geq4,\\[3mm]
\displaystyle
\sum_i4\left\lfloor{r_i^2\over4}\right\rfloor\geq N,
 &\mathbb F=\mathbb H,\quad N\geq3,\ N\neq5 .
\end{array}                                                  \tag{18}
\]

The excluded dimensions are genuine: one complex order-two block
(\(\mathbb H_2(\mathbb C)_+\cong Q_4\)) saturates at \(N=3\), and one
quaternionic order-two block
(\(\mathbb H_2(\mathbb H)_+\cong Q_6\)) saturates at \(N=5\).
For quaternionic \(N=3,4\), (18) also follows from the divisibility of every
positive capacity by four.

There are matching fixed-order-two ball frontiers.  Encode a coordinate
group of size at most two as one complex scalar, or a group of size at most
four as one quaternion.  The \(2\times2\) Hermitian Schur-complement matrix
and its rank-one dual are exactly (13), with transpose replaced by conjugate
transpose.  Therefore

\[
\begin{array}{c|c|c|c}
\text{blocks}&\text{range}&k_{\min}&(M_{\min},\nu_{\min}^{\rm normal})\\ \hline
\mathbb H_2(\mathbb C)_+&N\geq4&
\lceil N/2\rceil&(4\lceil N/2\rceil,\ 2\lceil N/2\rceil)\\[1mm]
\mathbb H_2(\mathbb H)_+&N\geq6&
\lceil N/4\rceil&(6\lceil N/4\rceil,\ 2\lceil N/4\rceil).
\end{array}                                                  \tag{19}
\]

At the exceptional quaternionic dimension \(N=5\), the direct single block
has \((k,M,\nu)=(1,6,2)\).  As before, these are exact only in the
global-factor regularity class and for the full ambient normal barrier.

## Literature boundary

The PSD tangent-capacity calculation is proved independently in
[A curvature-capacity lower bound for block-diagonal PSD lifts](2026-09-04-psd-block-curvature-capacity.md).
Gouveia--Parrilo--Thomas provide the general cone-lift/slack-factorization
framework.  Browder's 1962 theorem classifies the connected fiber of a
sphere-total-space bundle as homotopy equivalent to \(S^1,S^3\), or \(S^7\);
the companion
[sphere-submersion note](2026-09-04-sphere-submersion-curvature-gap.md)
checks the proper-\(C^1\) fibration and sphere-target consequences.  The
normal-barrier statement in (16) uses Güler--Tunçel's theorem that the
optimal normal-barrier parameter of a homogeneous cone is its
Carathéodory number.

A targeted search found PSD-rank and semidefinite-lift papers, PSD-cone
approximations using Grassmannian packings, and the classical topology of
Grassmannians and sphere fibrations.  It found no source deriving a support-
Grassmannian submersion from a saturated PSD slack factor, or the strict gap
(12c), its Hermitian analogues (18), or the exact smooth frontiers
(16) and (19).  Novelty remains subject to specialist review.

## Independent hostile audit

The audit verified the nondegeneracy of the primal--polar tangent pairing,
the PSD tangent blocks and factor \(2\) in (10), the support-map derivative
(11), and the common-kernel argument making the joint map a local
diffeomorphism.  It also checked the universal-cover classification,
including the noncompact order-two cover, the product cohomology
obstruction, and the nonzero \(\pi_2\) of every balanced oriented
Grassmannian of order at least four.  The strict all-order integer gap, the
order-at-most-three construction and simultaneous optima, and all three
cap-\(R\) resource inequalities were rederived independently.

One scope correction was required and incorporated: saturation constrains
balanced complementary ranks only for positive-capacity blocks.  A scalar
PSD block has zero curvature capacity and may have arbitrary complementary
scalar ranks; all joint-map and resource arguments already discard or
harmlessly retain such blocks as appropriate.

A second independent audit covered the mixed real, complex, and
quaternionic extension.  It checked the real cross-channel dimension
\(a_i p_iq_i\), the \(\operatorname{Re}\operatorname{tr}\) convention for
quaternionic pairing, the Grassmannian universal covers and cohomology
obstructions, all four low-order sphere targets, and the fixed-order-two
frontiers.  Its only substantive notation request—the real part in the
quaternionic trace pairing—has been incorporated.
