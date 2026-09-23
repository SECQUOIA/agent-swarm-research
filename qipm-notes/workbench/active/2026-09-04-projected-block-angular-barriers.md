# Projected block-angular barriers: positive compilers and a locality obstruction

Status: Proved results with scoped novelty  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on mathematics; mixed novelty  
Question: When can many recourse blocks be compiled into a low-parameter
first-stage barrier with locally reconstructible recourse?

## Shared-normal-fan compiler

Consider

\[
 \min c^Tx\quad\text{s.t.}\quad x\in X_0,\quad
 Wy_i=h_i-Tx,\quad y_i\geq0\quad(i\in[N]).
\]

Suppose the public dual cone has \(L=\operatorname{poly}(p)\) extreme rays:

\[
 \{z:W^Tz\geq0\}=\operatorname{cone}\{z_1,\ldots,z_L\}.
\]

Farkas' lemma shows that all recourse constraints are exactly

\[
 a_\ell^Tx\geq\beta_\ell,qquad
 a_\ell=-T^Tz_\ell,qquad
 \beta_\ell=\max_i(-z_\ell^Th_i).
\]

Quantum maximum finding computes every \(\beta_\ell\) in
\(\widetilde O(L\sqrt N)\) block queries. If \(G\) is a \(\nu_0\)-barrier
for \(X_0\), then

\[
 F(x)=G(x)-\sum_{\ell=1}^L\log(a_\ell^Tx-\beta_\ell)
\]

is a \((\nu_0+L)\)-barrier with explicit derivatives. Every later IPM round
is independent of \(N\), and the iteration count is

\[
 O(\sqrt{\nu_0+L}\log(1/\epsilon)).
\]

A canonical recourse point is the unique minimizer

\[
 y_i^c(x)=\arg\min_{Wy=h_i-Tx,y>0}
 \left(\tfrac12\|y\|^2-\sum_j\log y_j\right).
\]

Its KKT system and derivative use only \((h_i,W,T,x)\), so recourse coordinate
access is local and nonrecursive. A scalar OR instance proves the
\(\Theta(\sqrt N)\) quantum versus \(\Theta(N)\) randomized scenario-query
exponent is optimal.

When each \(W_i\in\mathbb R^{q\times p}\) has fixed \(q\), its dual cone has
at most \({p\choose q-1}\) extreme rays. Local enumeration followed by the
Apers--Gribling Lewis-weight QIPM gives an end-to-end projected method with

\[
 \widetilde O(\sqrt N\,\operatorname{poly}(p,k))
\]

block queries and an explicit first-stage \(k\)-vector. This is a useful new
block-angular corollary of an existing QIPM, not a fundamentally new barrier.

## Ordered symmetric-cone compiler

For recourse constraints

\[
 h_0+\alpha_i e-Tx\in\mathcal C
\]

over a symmetric cone with \(e\in\mathcal C\), every scenario is equivalent
to the worst one \(\alpha_*=\min_i\alpha_i\). Quantum minimum finding costs
\(\widetilde O(\sqrt N)\), after which

\[
 F(x)=G(x)+\Phi_{\mathcal C}(h_0+\alpha_*e-Tx)
\]

has parameter \(\nu_0+\operatorname{rank}(\mathcal C)\), explicit
derivatives, and immediate local recourse reconstruction. This covers ordered
SOC and PSD uncertainty, not arbitrary offsets.

## Quadratic-recourse rotated-SOC compiler

A less ordered positive family uses genuinely different local normals. Consider

\[
 \min\ \tau\quad\text{s.t.}\quad
 r_i=A_ix-b_i,\quad t_i\geq\|r_i\|_2^2,\quad
 \tau\geq\sum_i t_i,\quad x\in X_0.
\]

Each local quadratic epigraph is one rotated SOC block. The product
formulation has canonical parameter \(2N+1\), plus any \(X_0\) barrier: two
per rotated cone and one for the coupling slack. Eliminating \((r_i,t_i)\)
gives
\(\tau\geq q(x):=\sum_i\|A_ix-b_i\|_2^2\). Writing
\(C_i=[A_i,-b_i]\), \(\xi=(x,1)\), and

\[
 M=\sum_iC_i^TC_i,
\]

one has \(q(x)=\xi^TM\xi\). The projected epigraph is an affine preimage of a
single rotated Lorentz cone, so

\[
 F(x,\tau)=G_{X_0}(x)-\log(\tau-q(x))
\]

is a \((\nu_0+1)\)-barrier, independent of \(N\) and the local residual
dimension. With \(s=\tau-q(x)\),
\(Q=\sum_iA_i^TA_i\), \(g=\sum_iA_i^Tb_i\), and
\(d=2(Qx-g)\),

\[
 \nabla F=\nabla G+(d/s,-1/s),
\]

\[
 \nabla^2F=\nabla^2G+
 \begin{bmatrix}2Q/s&0\\0&0\end{bmatrix}
 +\frac{(d,-1)(d,-1)^T}{s^2}.
\]

All projected geometry is captured by the \((k+1)\times(k+1)\) Gram matrix
\(M\). Quantum spectral approximation of the stacked \(Np\)-row matrix
computes \(\widetilde M\approx_\varepsilon M\) in

\[
 \widetilde O\!\left(\frac{\sqrt{Np(k+1)}}\varepsilon\right)
\]

row queries. Safe inflation
\(\widehat M=\widetilde M/(1-\varepsilon)\) gives

\[
 M\preceq\widehat M\preceq
 \frac{1+\varepsilon}{1-\varepsilon}M.
\]

Solving the explicit projected SOCP is feasible for the original and gives a
\((1+O(\varepsilon))\)-approximation for pure least-squares recourse. All
later IPM work and the iteration count are independent of \(N\).

Reconstruction is local: query block \(i\), return
\(r_i=A_ix-b_i\) and \(t_i=\|r_i\|^2\). Full recourse materialization costs
\(\Omega(N)\), while a coherent local oracle uses one block query. The scalar
weight-zero/one promise \(b_i\in\{0,1\}\) gives optimum zero or one and proves
an \(\Omega(\sqrt N)\) quantum versus \(\Omega(N)\) randomized lower bound.

Quantum Gram approximation and quadratic epigraphs are known. The apparently
new conjunction is the exact \(\Theta(N)\)-to-one projected-barrier collapse, its
end-to-end QIPM ledger, and honest local reconstruction. A dedicated collision
search remains appropriate before promotion.

There is a matrix-valued analogue. For
\(R_i(x)=B_{i0}+\sum_jx_jB_{ij}\in\mathbb R^{d_i\times s}\), the projection

\[
 Y\succ\sum_iR_i(x)^TR_i(x)
\]

has barrier

\[
 -\log\det\!\left(Y-\sum_iR_i(x)^TR_i(x)\right)
\]

of exact parameter \(s\), independent of \(N\) and \(\sum_i d_i\). All data
again reduce to a Gram tensor of dimension \((k+1)s\), enabling the same
spectral-sketch compiler. This is a sparse SDP sufficient-statistic extension;
the underlying matrix-epigraph barrier calculus is classical.

The parameter-one claim follows directly. Along any direction write
\(a=Ds[h]\) and \(b=-D^2s[h,h]=D^2q[h,h]\geq0\). Then

\[
 D^2(-\log s)[h,h]=a^2/s^2+b/s,
\]

so the squared Newton decrement is at most one, while
\(D^3(-\log s)[h,h,h]=-2a^3/s^3-3ab/s^2\) satisfies standard
self-concordance.

## Factorized-Cramér normalization obstruction

Let a measure on a convex body \(K\) have log-Laplace transform

\[
 f(\theta)=\log\int_K e^{\langle\theta,u\rangle}d\mu(u),
 \qquad F=f^*.
\]

For independent copies and their average \(Z=N^{-1}\sum_iX_i\), exact
factorization gives

\[
 f_Z(\theta)=Nf(\theta/N),\qquad f_Z^*(x)=NF(x).
\]

The support is still \(K\), but the squared Newton decrement and barrier
parameter are multiplied by \(N\). Dividing by \(N\) repairs identical
copies, so this identity alone is not a no-go.

The sharp statement is a scalar multiplicative-normalization dichotomy. Any
factor depending only on \(N\) that reduces the replicated parameter to
\(o(N)\) must scale by \(o(1)\). Now take one nondegenerate block on
\([0,1]\) and \(N-1\) point masses at zero, if degenerate blocks are admitted.
The conjugate
has a tight \(-\log x+O(1)\) boundary singularity; multiplication by a factor
below one violates standard self-concordance. Therefore no single
\(N\)-dependent normalization both

1. remains a standard self-concordant barrier for every block collection, and
2. removes the \(N\)-growth on replicated blocks.

This is an apparently new obstruction for the natural family of local
product/convolution Cramér barriers. It does not rule out a nonfactorized
global entropic or universal barrier.

There is also a complementary exact-summary obstruction for general
exponential-cone recourse. Already with scalar first-stage and recourse
variables, consider projected epigraphs

\[
 \tau>q_w(x):=\sum_{i=1}^Nw_i e^{a_ix},
\]

where the \(a_i\)'s are fixed and distinct and \(w\in\mathbb R_{++}^N\).
Any continuous exact statistic \(S(w)\in\mathbb R^d\) from which the domain
can be decoded must have \(d\geq N\). Equality of decoded domains determines
\(q_w\); linear independence of distinct exponentials makes \(S\) injective
on the open set \(\mathbb R_{++}^N\), and invariance of domain forbids a
continuous injection into lower dimension. This rules out a finite Gram-like
exact compilation for arbitrary exponential scenarios, though it does not
preclude approximation or on-demand quantum mean estimation.

An even sharper obstruction already holds for constant-size rotated-SOC
scenario intersections. Let hidden \(z_i\in\{0,1\}\), put \(\gamma=1/4\),
and impose

\[
 t\geq x^2+2ix-i^2+\gamma z_i\qquad(i\in[N]).
\]

The projected boundary is

\[
 \varphi_z(x)=x^2+\max_j(2jx-j^2+\gamma z_j).
\]

At the public point \(x=i\), term \(i\) beats every other term by at least
\((i-j)^2-\gamma\geq3/4\), so

\[
 \varphi_z(i)=2i^2+\gamma z_i.
\]

Any reusable offline summary that, after preprocessing, answers all boundary
values (or sufficiently accurate membership queries) to error below
\(\gamma/3\) reveals the entire hidden string without further scenario
queries. Quantum oracle interrogation therefore requires \(\Omega(N)\)
preprocessing queries. Thus arbitrary sparse rotated-SOC intersections in
projected dimension two admit no sublinear-query universal reusable compiler,
even at constant accuracy. Fresh \(O(\sqrt N)\) Grover work per requested
point remains possible; the result separates max/intersection recourse from
the sum-of-squares family, whose additive structure has a Gram summary.

Replacing the common \(x^2\) term by a fixed rational power \(x^r\) or by
\(e^x\) transfers the same recovery proof to constant-size power- and
exponential-cone epigraphs. Thus the \(\Omega(N)\) reusable-compilation
obstruction is not specific to SOCP.

The same family proves a barrier-parameter no-go for every weighted additive
local construction

\[
 F(x,t)=\sum_iw_i[-\log s_i(x,t)].
\]

Each scenario owns an exposed boundary arc. Approaching that arc while all
other slacks stay positive makes the standard self-concordance cubic ratio tend
to \(1/\sqrt{w_i}\), forcing \(w_i\geq1\). Along any ray with fixed \(x\) and
\(t\to\infty\), the squared Newton decrement in the \(t\)-direction tends
\(\sum_iw_i\). Hence every such locally additive barrier has

\[
 \nu\geq\sum_iw_i\geq N,
\]

although the two-dimensional projection admits a nonlocal barrier of parameter
two. This identifies a locality cost, not an existential barrier lower bound.

## Novelty boundary

Farkas compilation, extreme-ray enumeration, maximum finding, symmetric-cone
barriers, and entropic barriers are established ingredients. The shared-normal-
fan and ordered-cone results close the projected-barrier target only on explicit
subclasses. The most plausible standalone novelty is the factorized-Cramér
normalization dichotomy; targeted searches found no matching locality-versus-
parameter statement, but priority is not guaranteed.
