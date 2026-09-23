# Smooth full product-ball \(Q_3\) factorizations: a fundamental-class obstruction

Status: Proved; independently hostile-audited; targeted literature-screened  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Theorem

Let
\[
 C=(B_2^s)^k,\qquad p=s-1,\qquad s\geq3,\qquad k\geq2,
\]
and \(M=(S^p)^k\).  Its full polar-extreme slack rows are
\[
                         S_a(x,z)=1-x_a^Tz,
 \qquad a\in[k],\quad x\in M,\quad z\in S^p.               \tag{1}
\]
Suppose they have globally labelled \(C^1\) \(Q_3\) factors
\[
 1-x_a^Tz=\sum_{i=1}^L\langle A_i(x),B_i^a(z)\rangle,
 \qquad A_i:M\to Q_3,\quad B_i^a:S^p\to Q_3.               \tag{2}
\]
Then, without a parity restriction,
\[
                              \boxed{L\geq k(p+1)=ks}.       \tag{3}
\]
The polynomial coordinate-square factorization attains \(L=ks\).
Consequently the exact globally selected \(C^1\) count is \(ks\).  In
particular, the first flat-switch candidate \(k=2,s=3\) cannot use four or
five channels: its exact count is six.

This improves the analytic no-sharing theorem in regularity.  Channels may
switch source blocks across flat cone-vertex regions; the proof below does
not prohibit that.  Instead it combines pointwise no-sharing of nonzero
curvature with a global cup-length obstruction.

## 1. Positive rank-one diagonal curvature

The contact cylinder \(z=x_a\) makes the left side of (2) zero.  Every
summand is nonnegative by self-duality of \(Q_3\), so
\[
                 \langle A_i(x),B_i^a(x_a)\rangle=0.        \tag{4}
\]
On \(E_a:=\pi_a^*TS^p\to M\), define
\[
 H_i^a(x)(u,v):=-\langle d_aA_i(x)u,dB_i^a(x_a)v\rangle .
                                                                    \tag{5}
\]
If either factor in (4) is the vertex, its derivative is zero.  Indeed, a
derivative and its negative both lie in the tangent cone \(Q_3\), whose
lineality space is zero.

Otherwise the two factors are nonzero complementary boundary vectors.  On
a neighborhood where they remain nonzero, uniquely write
\[
 A_i(x)=\alpha_i(x)(1,q_i(x)),\qquad
 B_i^a(u)=\beta_i^a(u)(1,-r_i^a(u)),                        \tag{6}
\]
with \(\alpha_i,\beta_i^a>0\) and \(q_i,r_i^a\in S^1\).
Equation (4) gives
\[
                         q_i(x)=r_i^a(x_a).                 \tag{7}
\]
Let \(J\) be rotation by \(\pi/2\) in \(\mathbb R^2\), and put
\[
 \eta_i^a(x)(u)=\langle Jq_i(x),d_aq_i(x)u\rangle.          \tag{8}
\]
Differentiating (6)--(7) cancels all scale and radial terms and gives
\[
        H_i^a=\alpha_i\beta_i^a\,\eta_i^a\otimes\eta_i^a.   \tag{9}
\]
Thus \(H_i^a\) is positive semidefinite of rank at most one.  Mixed
differentiation of (2) yields the round metric
\[
                       g_a=\sum_{i=1}^L H_i^a.              \tag{10}
\]
For
\[
                    n_a(x)=\#\{i:H_i^a(x)\neq0\},           \tag{11}
\]
rank subadditivity therefore gives
\[
                              n_a(x)\geq p.                 \tag{12}
\]
Only first derivatives of the two separately parametrized factors occur,
so \(C^1\) regularity suffices.

## 2. Active curvature is pointwise row-disjoint

If \(a\neq b\), the same channel cannot have both \(H_i^a(x)\neq0\) and
\(H_i^b(x)\neq0\).  Otherwise \(A_i(x),B_i^a(x_a),B_i^b(x_b)\) are all
nonzero.  They remain nonzero on a product neighborhood, where (7) gives
\[
                       q_i(x')=r_i^a(x'_a)=r_i^b(x'_b).     \tag{13}
\]
The variables \(x'_a,x'_b\) vary independently.  Fixing each in turn shows
that all three phases are locally constant.  The two phase derivatives in
(9) vanish, a contradiction.  Hence
\[
 \{i:H_i^a(x)\neq0\}\cap\{i:H_i^b(x)\neq0\}=\varnothing
 \quad(a\neq b).                                           \tag{14}
\]
This is deliberately only pointwise; flat switching elsewhere is allowed.

## 3. Minimum-activity pieces lie over proper phase regions

Assume \(L<k(p+1)\).  By (12)--(14), at every \(x\) some row has exactly
\(p\) active channels.  Therefore the sets
\[
                         Z_a=\{x:n_a(x)=p\}                 \tag{15}
\]
cover \(M\).  They are closed because each condition \(H_i^a\neq0\) is
open.

For a \(p\)-element label set \(P\subset[L]\), let \(Z_{a,P}\subset Z_a\)
be the points whose active labels are exactly \(P\).  The finitely many
\(Z_{a,P}\)'s are pairwise disjoint and clopen in \(Z_a\), hence compact.
Indeed, the \(p\) active labels at a point persist nearby; after restricting
to \(Z_a\), where exactly \(p\) labels are active, no different label can
enter.  Thus each active-label pattern is relatively open, and its
complement is the finite union of the other relatively open patterns.
At any such point, (10) is a sum of exactly \(p\) positive rank-one squares
equal to a rank-\(p\) metric, so \((\eta_i^a)_{i\in P}\) is a coframe.

Let
\[
 D_i^a=\operatorname{int}_{S^p}
       \{u:B_i^a(u)\in\partial Q_3\setminus\{0\}\},\qquad
 r_i^a:D_i^a\to S^1                                      \tag{16}
\]
be the globally defined dual phase in (6).  Every point of \(Z_{a,P}\)
projects into \(D_i^a\) for each \(i\in P\): activity makes both factors
nonzero at that point; after fixing all other primal blocks, the primal
factor remains nonzero for nearby \(x_a\), so complementarity forces the
nearby nonzero dual factors to remain on the boundary.  Thus the use of the
interior in (16) loses no active point.  With \(\omega\) the standard
angular one-form on \(S^1\), define
\[
 O_{a,P}=\left\{u\in\bigcap_{i\in P}D_i^a:
       ((r_i^a)^*\omega)_{i\in P}\text{ is a coframe of }T_u^*S^p
                  \right\}.                                \tag{17}
\]
This is open.  Equations (7)--(9) imply
\[
                       Z_{a,P}\subset\pi_a^{-1}(O_{a,P}).   \tag{18}
\]

The set \(O_{a,P}\) is proper.  If it were all \(S^p\), the product phase
map
\[
                    R_{a,P}=(r_i^a)_{i\in P}:S^p\to(S^1)^p \tag{19}
\]
would be a local diffeomorphism.  Its compact image would be open and
closed in the connected torus, hence it would be a covering.  This is
impossible for \(p\geq2\): \(S^p\) is simply connected, while the universal
cover of \((S^1)^p\) is the noncompact space \(\mathbb R^p\).

If \(u\) generates \(H^p(S^p;\mathbb R)\), every proper open subset of the
connected closed manifold \(S^p\) has zero degree-\(p\) real cohomology.
(Every component is a noncompact \(p\)-manifold.)  Thus
\[
                            u|_{O_{a,P}}=0.                 \tag{20}
\]
Normality and compactness now give pairwise disjoint open neighborhoods
\[
 Z_{a,P}\subset U_{a,P}\subset\pi_a^{-1}(O_{a,P}).          \tag{21}
\]
Set \(U_a=\bigsqcup_PU_{a,P}\).  For \(u_a=\pi_a^*u\), equations
(20)--(21) give
\[
                              u_a|_{U_a}=0.                 \tag{22}
\]
The \(U_a\)'s cover \(M\), because the \(Z_a\)'s do.

## 4. Fundamental-class cup-length contradiction

By (22), \(u_a\) lifts to a relative class in
\(H^p(M,U_a;\mathbb R)\).  Their relative cup product lies in
\[
 H^{kp}\!\left(M,\bigcup_aU_a;\mathbb R\right)
                   =H^{kp}(M,M;\mathbb R)=0.               \tag{23}
\]
Its absolute image is therefore zero.  The Kunneth formula instead gives
\[
             u_1\smile\cdots\smile u_k\neq0
                  \quad\text{in }H^{kp}(M;\mathbb R),       \tag{24}
\]
a contradiction.  This proves (3).

For even \(p\), one can replace Sections 3--4 by the weaker Euler shortcut:
the \(p\)-channel coframes trivialize \(E_a\) near \(Z_a\), killing
\(e(E_a)=\pm2u_a\), whose product is nonzero.  For odd \(p\), tangent-bundle
triviality alone cannot kill \(u_a\) (for example \(TS^3\) is globally
trivial).  The stronger Lorentz fact that the coframe comes from global
dual circle phases on \(O_{a,P}\) is exactly what removes the parity
restriction.

## 5. Matching factorization

Let
\[
\begin{aligned}
 U(t)&=\left({1+t^2\over2},{1-t^2\over2},t\right),\\
 V(t)&=\left({1+t^2\over2},-{1-t^2\over2},-t\right).
\end{aligned}
\]
These maps lie in \(Q_3\) and satisfy
\[
                         \langle U(t),V(v)\rangle
                              ={1\over2}(t-v)^2.            \tag{25}
\]
For \((b,j)\in[k]\times[s]\), set
\[
 A_{b,j}(x)=U((x_b)_j),\qquad
 B_{b,j}^a(z)=\mathbf1_{a=b}V(z_j).                         \tag{26}
\]
Then
\[
 \sum_{b,j}\langle A_{b,j}(x),B_{b,j}^a(z)\rangle
 ={1\over2}\|x_a-z\|^2=1-x_a^Tz.                           \tag{27}
\]
Thus the lower bound is exact.

The same proof is dimension-by-dimension.  For a heterogeneous product
\[
                    C=\prod_{a=1}^k B_2^{s_a},
             \qquad p_a=s_a-1\geq2,                         \tag{28}
\]
the full-row slack \(1-x_a^Tz\) satisfies
\[
                         L\geq\sum_{a=1}^k(p_a+1)
                           =\sum_{a=1}^ks_a.                \tag{29}
\]
If this sum were violated, the exact-\(p_a\) activity sets would again
cover the product.  Their label-pattern pieces lie over proper open subsets
of \(S^{p_a}\), killing the pulled-back degree-\(p_a\) generators, whose
external product is nonzero.  Separate coordinate-square factors attain
(29).

## Scope and literature boundary

The result closes the arbitrary-\(C^1\) versus analytic gap for the full
extreme slack of every product of balls covered above.  The flat-switch
witness in the analytic note still disproves unique continuation for one
channel, but (24) prevents such switches from completing a smaller full
factorization.

The lift/factorization framework is due to Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://doi.org/10.1287/moor.1120.0575).  Fawzi's general
second-order-cone factorization obstruction is in
[*On representing the positive semidefinite cone using the second-order
cone*](https://doi.org/10.1007/s10107-018-1233-0).  Neither source states
the smooth product-ball result here.

The topological ingredients are classical: top cohomology vanishes on a
proper open subset of a connected closed manifold, and relative cup
products give the standard cup-length obstruction; see Hatcher,
[*Algebraic Topology*](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).
Targeted searches for smooth cone/slack factorizations, second-order-cone
rank of products of balls, and topological lower bounds found no use of the
argument here.  The candidate new contribution is the combination of
pointwise full-row no-sharing (14), phase-region containment (18), and the
fundamental-class cover contradiction.  Novelty remains subject to
specialist review.

## Independent hostile audit

The audit checked all vertex and support-switching cases.  At a cone
vertex the corresponding first derivative is zero, while at a nonzero
complementary pair the phase-square formula (9) makes each mixed channel
symmetric, positive semidefinite, and rank at most one.  If one label were
active for two source rows at the same point, cylindrical complementarity
on a product neighborhood would force its phase to depend only on each of
two independently varying coordinates, hence to be locally constant.
Thus (14) is valid without analytic continuation.

The locus \(Z_a\) is closed because the locus of at least \(p+1\) active
labels is open.  Its fixed-label pieces are clopen in \(Z_a\), compact, and
separable by pairwise disjoint neighborhoods.  Activity supplies a genuine
open dual boundary-phase neighborhood, so no phase is normalized through a
zero or interior dual factor.  Exactly \(p\) positive rank-one summands
force the angular forms to be a coframe.  A full-sphere phase region would
give a local diffeomorphism from compact simply connected \(S^p\) to a
torus, which is impossible.  Finally, the top real class vanishes on every
proper phase region and hence on each disjoint union \(U_a\); the relative
cup product contradicts the nonzero Kunneth product fundamental class.
The heterogeneous-dimension extension uses the same argument in degrees
\(p_a\).  These checks leave no parity, nowhere-zero, or support-density
hypothesis.
