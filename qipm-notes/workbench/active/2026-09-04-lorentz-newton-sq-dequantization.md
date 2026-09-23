# Dimension-independent SQ sampling for few-cone Lorentz Newton systems

Status: Proved conditional one-step theorem; independently audited and literature-screened  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated access and conditioning assumptions

## Result

Few high-dimensional second-order cones do not by themselves create a
dimension-polynomial quantum advantage for Newton-state sampling.  For one
reduced Newton solve, a classical SQ algorithm has dimension-independent cost

\[
 d^{O(\sqrt{\kappa_S}\log(L\chi\kappa_S/\epsilon))}
 \operatorname{poly}
 (L,\chi,\kappa_S,\epsilon^{-1},\log(1/\delta_f)),            \tag{1}
\]

where \(d\) is the row/column sparsity of the equality matrix, \(L\) is the
number of Lorentz blocks, \(\chi\) controls their eccentricity,
\(\kappa_S\) is the condition number of a sparse base normal matrix, and
\(\delta_f\) is the failure probability.  The algorithm returns coordinate
queries and exact squared-coordinate sampling from a relative-\(\epsilon\)
approximate Newton direction in ideal real arithmetic.

The theorem assumes SQ/query/norm access to the current cone vectors and the
Newton right-hand side.  It is not an end-to-end classical IPM: maintaining
those data structures across dense updates and controlling \(\chi\) and
\(\kappa_S\) along the full path remain open.

## Lorentz inverse and sparse-plus-low-rank normal matrix

For one Lorentz block \(x=(t,z)\), put

\[
 r=\|z\|,qquad s=t^2-r^2,qquad d_x=s/2,
\]

and, when \(r>0\),

\[
 u_\pm=\frac1{\sqrt2}(1,\pm z/r).
\]

For the barrier \(F(x)=-\log(t^2-\|z\|^2)\), direct inversion gives

\[
 \boxed{
 H_F(x)^{-1}
 =d_xI+r(t+r)u_+u_+^T-r(t-r)u_-u_-^T.}                      \tag{2}
\]

Its eigenvalues are \((t+r)^2/2\) on \(u_+\),
\((t-r)^2/2\) on \(u_-\), and \(d_x\) on the tangential
subspace.  A centered block \(r=0\) has no rank correction.

For a product of \(L\) blocks, let

\[
 D=\operatorname{Diag}(d_{x,\ell}I),
\]

and collect the at most \(2L\) embedded vectors \(u_{\ell,\pm}\) into
\(U\).  Equation (2) has the form

\[
 H^{-1}=D+UCU^T,                                             \tag{3}
\]

where \(C\) is diagonal with one positive and one negative entry per
noncentered block.  Therefore the reduced normal matrix is

\[
 N=AH^{-1}A^T=S+(AU)C(AU)^T,qquad S=ADA^T.                  \tag{4}
\]

The base \(S\) is \(d^2\)-sparse regardless of cone dimensions.

Define the block eccentricities

\[
 \chi_\ell=\frac{t_\ell+r_\ell}{t_\ell-r_\ell},qquad
 \chi=\max_\ell\chi_\ell.
\]

The block eigenvalues in (2) imply

\[
 \chi^{-1}D\preceq H^{-1}\preceq\chi D,
\]

and hence, for full-row-rank \(A\),

\[
 \boxed{\chi^{-1}S\preceq N\preceq\chi S.}                 \tag{5}
\]

This comparison both controls conditioning after sparse-base preconditioning
and stabilizes the small indefinite Woodbury solve.

## Stable small correction

Write \(\widetilde A=AD^{1/2}\), absorb the magnitudes of \(C\) into the
columns of \(G\), and let \(J\) be diagonal with the corresponding
\(+1,-1\) signs.  With \(W=S^{-1/2}G\),

\[
 N=S^{1/2}(I+WJW^T)S^{1/2}.
\]

The spectrum of \(I+WJW^T\) lies in \([\chi^{-1},\chi]\).  Moreover

\[
 |H^{-1}-D|\preceq(\chi-1)D
 \quad\Longrightarrow\quad
 GG^T\preceq(\chi-1)S
 \quad\Longrightarrow\quad
 \|W\|^2\leq\chi-1.                                        \tag{6}
\]

This blockwise estimate is essential: the spectral bound on
\(I+WJW^T\) alone would not control \(W\) in the presence of indefinite
cancellation.

The at-most-\(2L\)-dimensional Woodbury core

\[
 K=J+W^TW
\]

is nonsingular and obeys

\[
 \|K^{-1}\|\leq\chi^2,qquad
 \kappa_2(K)\leq\chi^2(1+\chi-\chi^{-1}).                   \tag{7}
\]

Thus an indefinite positive/negative rank correction does not introduce an
uncontrolled cancellation parameter when \(\chi\) is bounded.

## SQ algorithm

Assume:

1. row-and-column \(d\)-sparse access to \(A\);
2. SQ/query/norm access to the Newton right-hand side \(b\) and every current
   \(z_\ell\), with \(t_\ell\) queryable;
3. public spectral bounds for \(S\), scaled so \(\lambda_{\max}(S)=1\), and
   \(\kappa_2(S)=\kappa_S\); and
4. ideal real arithmetic.

SQ access to \(u_{\ell,\pm}\) follows directly: half its squared mass is on
the time coordinate and half is distributed as \(z_\ell/r_\ell\).

Choose a Chebyshev polynomial \(P\) with

\[
 \|I-SP\|\leq\eta,qquad
 \deg P=O(\sqrt{\kappa_S}\log(1/\eta)).                     \tag{8}
\]

Sparse-walk expansion gives local access to \(P\).  Estimate the entries of

\[
 K_P=J+G^TPG,qquad h_P=G^TPb
\]

with unbiased SQ inner-product estimators, solve
\(K_Pz=h_P\) classically, and form

\[
 \widetilde y=Pb-PGz.                                       \tag{9}
\]

The useful dimension-free norm bounds are

\[
 \|\widetilde A^TP\widetilde A\|\leq1+\eta,qquad
 \|\widetilde A^TP\|=O(\sqrt{\kappa_S}).
\]

Together with (5)--(8), choosing \(\eta\) and the
\(O(L^2)\) entry-estimation errors to be
\(\epsilon/\operatorname{poly}(L,\chi,\kappa_S)\) proves

\[
 \|\widetilde y-N^{-1}b\|
 \leq\epsilon\|N^{-1}b\|
\]

with probability at least \(1-\delta_f\).

Finally, view (9) as a linear combination of \(Pb\) and the at most \(2L\)
vectors \(P\widetilde Au_a\).  Apply the sparse-transform rejection sampler
to each component, mix raw proposals using their known denominators, and on
an observed coordinate \(i\) accept with probability proportional to

\[
 \frac{|\widetilde y_i|^2}
 {(2L+1)\sum_a\alpha_a^2|w_{a,i}|^2}.
\]

Conditional on acceptance the output law is exactly
\(|\widetilde y_i|^2/\|\widetilde y\|^2\); (6)--(7) bound the expected
rejection overhead by \(\operatorname{poly}(L,\chi,\kappa_S)\), with no
extra cancellation promise.  Sparse-walk materialization and estimation give
(1).

## Boundary and prior art

The algebraic decomposition (2)--(4) is classical.  Goldfarb--Scheinberg's
product-form Cholesky method explicitly treats one positive and one negative
rank-one update per large Lorentz cone; the Alizadeh--Goldfarb SOCP survey and
Cai--Toh reduced augmented systems are also direct antecedents.  No novelty is
claimed for the decomposition.

A targeted search found no SQ/sample-query analogue of (1).  The closest
dequantization work handles scalar sparse-polynomial estimation rather than an
exact sampler for the Woodbury-corrected Newton direction.  The defensible
apparent novelty is the conditional one-step sampler and exclusion principle:
for fixed \(L,d,\chi,\kappa_S,\epsilon\), a growing Lorentz block dimension
cannot support a dimension-polynomial quantum advantage under matched
iterate-SQ access.

The one-cone Forrelation SOCP family in the companion note escapes this
theorem through \(\kappa_S=\Theta(\log^2N)\), already with \(\chi=1\).  This
matches the sparse-SQ conditioning frontier rather than contradicting it.
