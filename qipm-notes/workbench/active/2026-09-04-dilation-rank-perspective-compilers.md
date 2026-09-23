# Dilation rank characterizes finite-statistic perspective compilers

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on apparent novelty of the compiler interpretation

## Exact summary-dimension theorem

Let \(h:(0,\infty)\to\mathbb R\) be continuous and define its dilation rank

\[
 R_h=\dim\operatorname{span}\{r\mapsto h(\lambda r):\lambda>0\}.
\]

Consider common-ray scalar perspective scenarios

\[
 \Phi(U,V)=\sum_{i=1}^N w_i c_iU\,
 h\!\left(\frac{d_i}{c_i}\frac VU\right),qquad U,V>0.       \tag{1}
\]

If \(R_h=R<\infty\), choose a basis \(h_1,\ldots,h_R\) and coefficients
\(m_\ell(\lambda)\) such that

\[
 h(\lambda r)=\sum_{\ell=1}^R m_\ell(\lambda)h_\ell(r).
\]

Then (1) is reconstructed exactly from the \(R\) scalar moments

\[
 M_\ell=\sum_i w_ic_i m_\ell(d_i/c_i),qquad
 \Phi(U,V)=U\sum_{\ell=1}^R M_\ell h_\ell(V/U).              \tag{2}
\]

Conversely, the number \(R_h\) is necessary in the following precise model.
Select \(R\) scales \(\lambda_i\) with linearly independent dilates and let
the positive coefficient vector range over \(\mathbb R_{++}^R\).  If a
continuous encoder \(E:\mathbb R_{++}^R\to\mathbb R^m\) admits an exact
deterministic decoder that recovers
\(\sum_iw_i h(\lambda_i r)\) for every \(r>0\), then \(E\) is injective.
Topological invariance of domain therefore forces

\[
 \boxed{m\geq R_h.}                                          \tag{3}
\]

For \(R_h=\infty\), (3) holds for every finite \(R\); no fixed-dimensional
continuous real summary exists.  Decoder continuity is not needed.  The
continuity and finite-real-vector restrictions on the encoder matter:
discontinuous encodings of unbounded precision and function-valued summaries
lie outside the theorem.

Thus the exact continuous reusable-summary dimension is the dilation rank.
This is a source-evaluation theorem, not a lower bound on the barrier parameter
or on arbitrary optimization algorithms.

## Classification

Set \(f(y)=h(e^y)\).  Dilation of \(h\) becomes translation of \(f\).
The classical Anselone--Korevaar finite-translation-space theorem gives

\[
 R_h<\infty
 \quad\Longleftrightarrow\quad
 h(r)=\sum_j r^{\rho_j}P_j(\log r),                           \tag{4}
\]

with complex-conjugate terms paired for real-valued \(h\).  In particular,

- \(-\log r\) has rank two;
- \(r^\alpha\) has rank one;
- finite sums of powers times log-polynomials have finite rank; and
- \(e^r\) has infinite rank because the functions \(e^{\lambda r}\) are
  linearly independent.

Equation (4) is classical, not a new approximation-theory classification.
The apparent new step is to use it as the exact sufficient-statistic boundary
for common-ray conic perspective data.

## Two-moment Umegaki relative-entropy compiler

Use the uncorrected homogeneous Umegaki convention

\[
 D(X\|Y)=\operatorname{tr}X(\log X-\log Y).
\]

For positive weights and scalar scales, put

\[
 A=\sum_iw_ic_i,qquad
 B=\sum_iw_ic_i\log(c_i/d_i),qquad
 D_{\rm eff}=Ae^{-B/A}.                                     \tag{5}
\]

The scaling identity

\[
 D(cX\|dY)=cD(X\|Y)+c\log(c/d)\operatorname{tr}X
\]

gives, even for noncommuting \(X,Y\),

\[
 \boxed{
 \sum_iw_iD(c_iX\|d_iY)=D(AX\|D_{\rm eff}Y).}              \tag{6}
\]

The identity extends to the usual positive-semidefinite/support closure.  It
does not hold in this form for the corrected unnormalized divergence that adds
\(\operatorname{tr}Y-\operatorname{tr}X\); that convention leaves an
additional explicit linear trace term.

After the two moments in (5) have been acquired once, every subsequent value,
gradient, and Hessian evaluation uses one standard quantum-relative-entropy
term and makes no query to the \(N\) source scenarios.  When \(c_i=1\) and
the weights sum to one, \(D_{\rm eff}\) is the weighted geometric mean of the
\(d_i\).

This statement requires fixed weights and scalar scales and an epigraph or
objective involving their sum.  It does not retain \(N\) separate epigraph
outputs or inequalities.  If the scales are optimization variables or change
between iterations, the two-moment online conclusion does not apply.

For bounded coherent value access, additive-error acquisition of the averaged
moment \(B\) has the standard quantum mean-estimation cost

\[
 \widetilde O(\min\{N,1/\eta\})
\]

versus randomized
\(\widetilde O(\min\{N,1/\eta^2\})\).  Exact acquisition, or error below a
constant times \(1/N\), can encode exact Hamming weight and requires
\(\Omega(N)\) quantum queries.  One-sided confidence bounds on \(B\) give
globally safe inner and outer scalar epigraphs because the boundary error is
\((\widehat B-B)\operatorname{tr}X\), with \(X\succeq0\).

## Barrier and access are different resources

No barrier novelty is claimed.  Fawzi--Saunderson already prove optimal
self-concordant barriers for epigraphs of noncommutative perspectives, and
He--Saunderson--Fawzi explicitly treat quantum relative entropy composed with
positive maps and shared block-diagonal outputs.  Their result gives a
\((2n+1)\)-parameter barrier for (6), independent of \(N\), and in fact gives
an input-size-controlled barrier for much more general operator-concave
generators even when the dilation rank is infinite.

Dilation rank instead answers whether the source dependence can be replaced
by finitely many scalar moments and evaluated without revisiting all scenarios.
The distinction is real.  For symmetric scalar KL

\[
 J(u,v)=D(u\|v)+D(v\|u),
\]

take \(u=x_1\), \(v_i=e^{-z_i}x_2\), and
\(\Phi_z=\sum_iJ(u,v_i)\), where \(z\) has Hamming weight zero or one.  At
the public point \(x=(1,1)\),

\[
 \Phi_z=
 \begin{cases}
 0,&|z|=0,\\
 1-e^{-1},&|z|=1.
 \end{cases}
\]

At \(t=2(1-e^{-1})\), the standard constant-parameter epigraph barrier value
therefore changes by exactly \(\log2\).  A value oracle accurate to less than
\(\log2/3\) distinguishes unique search, requiring \(\Omega(\sqrt N)\)
quantum or \(\Omega(N)\) randomized source queries.  A small barrier parameter
does not itself compile source access.

## Prior-art boundary

The classification (4) is the 1964
[Anselone--Korevaar theorem](https://doi.org/10.2307/2034591).  The relevant
barriers are in
[Fawzi--Saunderson](https://arxiv.org/abs/2205.04581) and the structured
positive-map formulation is in
[He--Saunderson--Fawzi](https://arxiv.org/abs/2407.00241).
The homogeneous positive-matrix convention used in (6) is also explicit in
[Audenaert--Eisert](https://arxiv.org/abs/1105.2656).

A targeted search found no explicit statement of (6) as a two-moment reusable
source compiler, nor an application of finite translation/dilation rank as the
necessary-and-sufficient summary-dimension criterion for perspective families.
That compiler interpretation and the separation between barrier parameter and
source-summary dimension are the defensible apparent novelty.  The
translation-space classification, QRE barrier, mean-estimation bounds, and
invariance-of-domain argument themselves are established ingredients.
