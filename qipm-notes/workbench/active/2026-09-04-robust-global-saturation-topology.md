# Robust topological obstruction for approximate minimum-block factorizations

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem under its explicit hypotheses

## Result

Let \(n=N-1\), and let

\[
                   B_2^N\subseteq C_\epsilon
                   \subseteq(1+\epsilon)B_2^N.                  \tag{1}
\]

Suppose the support slack on the full sphere has a globally labelled
\(C^2\) factorization through exactly \(n\) three-dimensional proper cones:

\[
 h_{C_\epsilon}(v)-\langle u,v\rangle
 =\sum_{i=1}^n\langle A_i(u),B_i(v)\rangle,qquad u,v\in S^n.    \tag{2}
\]

Here \(A_i(u)\in K_i\), \(B_i(v)\in K_i^*\), and \(\dim K_i=3\).
For every base point \(x\in S^n\), use an orthonormal geodesic chart of a
fixed radius \(r_0\), and write

\[
 a_i=A_i(x),\quad b_i=B_i(x),\quad
 X_i=dA_i(x),\quad Y_i=dB_i(x),\quad
 \delta_i=\langle a_i,b_i\rangle.                               \tag{3}
\]

Assume uniform bounds

\[
 \|a_i\|,\|b_i\|\geq\mu>0,qquad
 \|X_i\|,\|Y_i\|\leq L,                                        \tag{4}
\]

and assume the following explicit contracted second-derivative bounds. For
every unit \(w\in T_xS^n\), \(|t|\leq r_0\), and center-based geodesic
\(\gamma_{x,w}(t)=\exp_x(tw)\), hold the opposite factor fixed at the center
and require

\[
 \begin{split}
 |\langle (A_i\circ\gamma_{x,w})''(t),b_i(x)\rangle|&\leq H,\\
 |\langle a_i(x),(B_i\circ\gamma_{x,w})''(t)\rangle|&\leq H .    \tag{4a}
 \end{split}
\]

If \(\sqrt{2\epsilon/H}\leq r_0\), define

\[
 \mathfrak E(\epsilon)=
 {2L\sqrt{2Hn\epsilon}\over\mu}
 +{L^2\epsilon\over\mu^2}
 +{2H\epsilon^2\over\mu^4}.                                    \tag{5}
\]

### Theorem

If \(\epsilon<\mu^2\) and \(\mathfrak E(\epsilon)<1\), then \(S^n\) is
parallelizable. Therefore, for \(N\notin\{2,4,8\}\), every factorization
(2) satisfying (3)--(4), \(\epsilon<\mu^2\), and the chart-radius condition
must obey

\[
                       \boxed{\mathfrak E(\epsilon)\geq1.}       \tag{6}
\]

In particular, if the last two terms of (5) are at most \(1/2\), then

\[
                 L\sqrt H\geq
                 {\mu\over4\sqrt{2n\epsilon}}.                  \tag{7}
\]

Thus, outside dimensions \(N=2,4,8\), even a pointwise capacity-saturating
minimum \(3\)-dimensional-block count cannot remain globally smooth and
uniformly conditioned while converging to the ball.  This is stronger than
the local approximate-curvature theorem in this equality case: the local
rank budget \(n\) is sufficient at every point, but the corresponding rank-
one channels cannot be assembled into a global frame.

The conclusion concerns global factor selections, not existence of the
underlying approximate lift.  It is also not a coordinate-invariant QIPM
condition-number lower bound; \(\mu,L,H\) retain the coordinate caveat in the
companion KKT-invariance note.

## Proof

At every \(x\in S^n\), nonnegativity of the block pairings and (1)--(2) give

\[
          \delta_i(x)\geq0,qquad
          \sum_i\delta_i(x)=h_{C_\epsilon}(x)-1\leq\epsilon.    \tag{8}
\]

Mixed differentiation of (2) in orthonormal tangent directions gives the
exact identity

\[
                  \sum_i-X_i(x)^TY_i(x)=I_{T_xS^n}.              \tag{9}
\]

The support term depends only on the second variable and therefore
disappears from the mixed derivative.

The quantitative near-complementarity lemma bounds each matrix in (9) by a
rank-one matrix with error \(e_i(x)\).  For the topological argument we use a
canonical continuous choice.  Since

\[
 {\langle a_i,b_i\rangle\over\|a_i\|\|b_i\|}
 \leq{\epsilon\over\mu^2}<1                                    \tag{10}
\]

by the explicit assumption \(\epsilon<\mu^2\), \(a_i\) and \(b_i\) are
linearly independent.  The line

\[
                   W_i(x)=a_i(x)^\perp\cap b_i(x)^\perp         \tag{11}
\]

therefore varies continuously.  Projecting \(X_i\) to \(b_i^\perp\),
\(Y_i\) to \(a_i^\perp\), and the cross-hyperplane pairing to \(W_i\)
gives a continuous rank-at-most-one bundle map

\[
 \begin{split}
 R_i(x)&:T_xS^n\longrightarrow T_x^*S^n,\\
 R_i(x)(u,v)&=-\langle P_{W_i(x)}X_i(x)u,
                         P_{W_i(x)}Y_i(x)v\rangle .              \tag{12}
 \end{split}
\]

The projection calculation in the conditioned curvature theorem gives

\[
 \left\|-X_i^TY_i-R_i\right\|\leq e_i(x),qquad
 \sum_i e_i(x)\leq\mathfrak E(\epsilon).                         \tag{13}
\]

The second inequality follows from
\(\sum_i\sqrt{\delta_i}\leq\sqrt{n\epsilon}\) and
\(\sum_i\delta_i^2\leq\epsilon^2\).

If (5) is below one, equations (9) and (13) show that

\[
                         R(x)=\sum_iR_i(x)                       \tag{14}
\]

is invertible at every point.  Since it is a sum of exactly \(n\) maps of
rank at most one on an \(n\)-dimensional space, every \(R_i(x)\) has rank
one and their image lines are in direct sum.  Continuity and constant rank
make

\[
                   \mathcal L_i=\operatorname{im}R_i\subset T^*S^n \tag{15}
\]

line subbundles with

\[
                         T^*S^n=\bigoplus_i\mathcal L_i.         \tag{16}
\]

For \(n\geq2\), every real line bundle on \(S^n\) is trivial because
\(H^1(S^n;\mathbb Z_2)=0\); \(T^*S^1\) is separately trivial.  Choosing a
nonzero section of each \(\mathcal L_i\) gives a global coframe, hence a
global frame of \(TS^n\).  The classical classification of parallelizable
spheres now forces \(n\in\{1,3,7\}\), equivalently
\(N\in\{2,4,8\}\).  This proves (6), and (7) follows by isolating the first
term of (5).

## Stronger saturated-rank theorem

The all-three-dimensional statement is a special case of a stronger
topological obstruction. Suppose (2) instead has \(k\) globally labelled
blocks of dimensions \(m_i\geq2\), put \(r_i=m_i-2\), and assume

\[
                         \sum_{i=1}^k r_i=n.                    \tag{17}
\]

Keep (4)--(4a), and replace (5) by

\[
 \mathfrak E_k(\epsilon)=
 {2L\sqrt{2Hk\epsilon}\over\mu}
 +{L^2\epsilon\over\mu^2}
 +{2H\epsilon^2\over\mu^4}.                                   \tag{18}
\]

If \(\epsilon<\mu^2\), the vectors \(a_i,b_i\) are linearly independent.
Thus \(W_i=a_i^\perp\cap b_i^\perp\) varies continuously and has dimension
\(m_i-2=r_i\). In every ambient dimension,

\[
 \left\|P_{b_i^\perp}P_{a_i^\perp}-P_{W_i}\right\|
 ={\langle a_i,b_i\rangle\over\|a_i\|\|b_i\|}.                  \tag{19}
\]

The two operators agree with the identity on \(W_i\); on
\(\operatorname{span}\{a_i,b_i\}\), the difference has sole nonzero
singular value equal to the normalized inner product in (19). Therefore

\[
 R_i(u,v)=-\langle P_{W_i}X_i u,P_{W_i}Y_i v\rangle             \tag{20}
\]

is canonical, continuous, and has rank at most \(r_i\). The same
near-complementarity calculation gives

\[
 \left\|I-\sum_iR_i(x)\right\|\leq\mathfrak E_k(\epsilon).       \tag{21}
\]

If \(\mathfrak E_k(\epsilon)<1\), then \(\sum_iR_i(x)\) is invertible and

\[
 n\leq\sum_i\operatorname{rank}R_i(x)
   \leq\sum_i r_i=n.
\]

Every inequality is an equality, so

\[
 \operatorname{rank}R_i(x)=r_i,\qquad
 T^*S^n=\bigoplus_{i:r_i>0}\operatorname{im}R_i.                \tag{22}
\]

Constant rank makes every image in (22) a continuous vector subbundle.
This proof needs neither symmetry nor positivity of the \(R_i\)'s.

Two topological consequences follow.

1. Let \(q=\#\{i:m_i=3\}\). Each such block supplies a line summand in
   (22), and these lines are trivial for \(n\geq2\). Their nonzero sections
   are pointwise independent, so Adams's theorem gives

   \[
                              q\leq\rho(N)-1.                   \tag{23}
   \]

   The \(S^1\) case obeys the same bound separately. When all blocks are
   three-dimensional, (17) says \(q=n\), recovering
   \(N\in\{2,4,8\}\).

2. If \(N\geq3\) is odd, then \(n=N-1\) is positive and even. Every real
   vector bundle over \(S^n\) is orientable because
   \(H^1(S^n;\mathbb Z_2)=0\). If (22) had two positive-rank summands
   \(E,F\), grouping all remaining summands into \(F\), both ranks would
   lie strictly between \(0\) and \(n\). Hence \(e(E)=e(F)=0\), because
   \(H^j(S^n;\mathbb Z)=0\) for \(0<j<n\). The Whitney product formula
   would give \(e(TS^n)=e(E)\smile e(F)=0\), contradicting
   \(\langle e(TS^n),[S^n]\rangle=\chi(S^n)=2\). Therefore exactly one
   block has positive \(r_i\), and it must satisfy

   \[
                         r_i=n,\qquad m_i=N+1.                  \tag{24}
   \]

   Thus, for odd \(N\geq3\), a conditioned globally smooth saturated
   factorization with every \(m_i\leq d<N+1\) is impossible once
   \(\mathfrak E_k(\epsilon)<1\).

A one-dimensional proper cone is a ray. Under (4), its normalized
primal-dual pairing equals one, so \(\delta_i\geq\mu^2\), contradicting
\(\sum_i\delta_i\leq\epsilon<\mu^2\). Thus rays cannot occur under these
hypotheses. Without the norm lower bound, set \(R_i=0\) and use the
separate ray error \(\|X_i^TY_i\|\leq\alpha_i\beta_i\), but no uniform
estimate follows near a zero factor. This is an allowed escape, not a
missing case.

## Blockwise-gauge-invariant degeneration index

The common bounds \(\mu,L,H\) depend on the Euclidean coordinates used for
each cone block.  The same proof has a stronger form that is invariant under
every fixed blockwise invertible reparameterization.

For \(S_i\in GL(m_i)\), replace

\[
 A_i\mapsto S_iA_i,\qquad B_i\mapsto S_i^{-T}B_i,\qquad
 K_i\mapsto S_iK_i.                                             \tag{25}
\]

At each center \(x\), let \(H_{A,i}(x)\) and \(H_{B,i}(x)\) be the least
bounds in the two lines of (4a), respectively, and put

\[
 \psi_{r_0}(\delta,H)=\inf_{0<s\leq r_0}
 \left(\frac{\delta}{s}+\frac{Hs}{2}\right).                  \tag{26}
\]

When \(a_i,b_i\ne0\), define

\[
\begin{aligned}
 U_i^S&=\|S_iX_i\|, &V_i^S&=\|S_i^{-T}Y_i\|,\\
 \alpha_i^S&=\frac{\psi_{r_0}(\delta_i,H_{A,i})}
                    {\|S_i^{-T}b_i\|},
 &\beta_i^S&=\frac{\psi_{r_0}(\delta_i,H_{B,i})}
                    {\|S_i a_i\|},\\
 \gamma_i^S&=\frac{\delta_i}
 {\|S_i a_i\|\,\|S_i^{-T}b_i\|}.                            \tag{27}
\end{aligned}
\]

For \(m_i\geq2\), set

\[
 e_i^S=U_i^S\beta_i^S+V_i^S\alpha_i^S
       +\alpha_i^S\beta_i^S\gamma_i^S+U_i^SV_i^S\gamma_i^S,   \tag{28}
\]

and for a one-dimensional ray set
\(e_i^S=\alpha_i^S\beta_i^S\).  If either base factor vanishes at
any point, assign the corresponding gauge the value \(+\infty\). Otherwise
define

\[
 \Gamma(S)=\sup_{x,i}\gamma_i^S(x),\qquad
 E(S)=\sup_x\sum_i e_i^S(x),\qquad
 \mathcal D=\inf_{S\in\prod_iGL(m_i)}
                 \max\{\Gamma(S),E(S)\}.                     \tag{29}
\]

### Gauge-invariant theorem

Assume the saturated budget (17). If the rank profile
\((r_i)_i=(m_i-2)_+\) is topologically obstructed, meaning that

\[
 T^*S^n\not\cong\bigoplus_i\mathcal E_i,
 \qquad \operatorname{rank}\mathcal E_i=r_i,                  \tag{30}
\]

then

\[
                              \boxed{\mathcal D\geq1}.         \tag{31}
\]

Indeed, \(\mathcal D<1\) would give a gauge with
\(\Gamma(S)<1\) and \(E(S)<1\). The first inequality excludes rays and
ensures that \(S_i a_i\) and \(S_i^{-T}b_i\) are nonzero and nonparallel.
Thus

\[
 W_i^S=(S_i a_i)^\perp\cap(S_i^{-T}b_i)^\perp,
 \qquad
 R_i^S(u,v)=-\langle P_{W_i^S}S_iX_i u,
                       P_{W_i^S}S_i^{-T}Y_i v\rangle           \tag{32}
\]

vary continuously and have rank at most \(r_i\).  The exact
near-complementarity lemma gives
\(\|-X_i^TY_i-R_i^S\|\leq e_i^S\).  Equations (9) and (29) make
\(\sum_iR_i^S\) invertible.  Saturation then forces every
\(\operatorname{rank}R_i^S=r_i\), and their images give the forbidden
direct sum (30).

The scalar slack, \(\delta_i\), chart radius, and contracted second
derivatives are exactly unchanged by (25).  If the original factorization
is first reparameterized by \(T=(T_i)\), a later gauge \(S'\) ranges through
the same net gauges \(S'T\) as \(S\) ranges through the full product of
general linear groups. Hence \(\mathcal D\) is blockwise-\(GL\)-invariant.
The Euclidean spaces \(W_i^S\) and their projectors need not themselves be
gauge-covariant; the proof reapplies the estimate separately in each
transformed Euclidean realization.

This removes the fixed-coordinate loophole from the topological
degeneration statement. It does not identify \(\mathcal D\) with a
self-concordant-barrier, Newton-system, or quantum-linear-system condition
number. It also still depends on a chosen global \(C^2\) primal-dual factor
selection and on the sphere parameterization.

## Scope and novelty

The proof combines the audited quantitative near-complementarity estimate
with the audited tangent-bundle obstruction.  It requires fixed block labels,
global \(C^2\) factor maps, nonvanishing base factors, and uniform derivative
control.  Ordinary definable lifts guarantee only local smooth strata and do
not meet these hypotheses automatically.

No source found in the targeted searches for approximate cone
factorizations or vector fields on spheres states this robust combination.
The cone-factor approximation background is Gouveia--Parrilo--Thomas,
[*Approximate Cone Factorizations and Lifts of
Polytopes*](https://doi.org/10.1007/s10107-014-0848-z); the topological input
is Adams,
[*Vector Fields on Spheres*](https://doi.org/10.2307/1970213).  Apparent
novelty remains subject to specialist review.

Adjacent work on moving Parseval frames for vector bundles, such as
Ballas--Needham--Shonkwiler,
[*On the Existence of Parseval Frames for Vector
Bundles*](https://arxiv.org/abs/2312.13488), starts with a vector bundle and
studies frame existence. It does not derive (22) from conditioned
approximate cone factors and a saturated curvature budget.

The independent audit checked (5) and (18), the dimension-independent
projection identity (19), continuity and constant rank, the nonsymmetric
direct-sum argument, the Adams and Euler-class corollaries, and the ray
case. A second audit checked (25)--(32), including invariance of the
contracted derivatives, the infimum argument, zero and ray factors, and the
distinction from a QIPM condition number. No mathematical error was found
under the stated hypotheses.
