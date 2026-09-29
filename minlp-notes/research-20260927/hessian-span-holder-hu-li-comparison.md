# Hu–Li comparison and a conic derivation of the Hessian-span bound

Date: 2026-09-27. This is an independent primary-source comparison. The conclusion is that Hu–Li do not state the proposed bound, but the qualitative exponent follows by a short Hessian-span argument combined with established conic error bounds. The resulting prior-art concern is stronger than a resemblance between proof methods. No priority claim is justified by the absence of the exact formula in Hu–Li.

The primary sources inspected were:

- [Hu and Li, *Facial reduction for the Shor SDP relaxation of QCQPs*](https://asvao.biemdas.com/issues/ASVAO2023-2-5.pdf), Applied Set-Valued Analysis and Optimization 5 (2023), 181–191. Equation (3.2), printed p.184, defines the full Shor relaxation. Equation (4.1), p.185, replaces its PSD condition by PSD of the lower-right block. Theorem 4.2, p.186, obtains exposing vectors by a linear system when the quadratic matrices are PSD. Theorem 4.5, p.187, concerns the singularity degree of this further relaxation. The text on pp.183 and 185 explicitly limits recovery of Slater for the original Shor relaxation. Remark 3.2, p.185, distinguishes partial-polyhedral Slater from strict positivity of all slacks. No Hessian-matrix-span error exponent is stated.
- [Lourenço, Muramatsu, and Tsuchiya, *Facial reduction and partial polyhedrality*](https://optimization-online.org/wp-content/uploads/2015/11/5224.pdf), Proposition 8, printed pp.8–9 of the linked preprint. Phase 1 reaches the partial-polyhedral Slater condition, and its proof says that every reduction changes a nonpolyhedral factor.
- [Lourenço, *Amenable cones: error bounds without constraint qualifications*](https://optimization-online.org/wp-content/uploads/2017/11/6348.pdf), revised August 2019, Proposition 38, printed p.27. For a feasible affine intersection with a symmetric cone, bounded approximate points have error exponent \(2^{-d_{\rm PPS}}\). Here \(d_{\rm PPS}\) is the minimum number of reductions needed to reach partial-polyhedral Slater; see printed p.6. These are printed page numbers, not zero-based PDF indices.

There is a real obstacle to applying Hu–Li's further relaxation directly. For the scalar constraint \((x-1)^2\le0\), the true feasible set is \(\{1\}\). The full Shor constraints are
\[
Y=\begin{pmatrix}1&x\\x&X\end{pmatrix}\succeq0,
\qquad X-2x+1\le0,
\]
which force \(x=X=1\). The further relaxation only requires \(X\ge0\). It has the strict point \((x,X)=(2,1)\), and its projection contains infeasible original points. A distance bound to that relaxed set consequently does not repair original quadratic feasibility. This example is an independent calculation, not an example from the paper.

That obstacle does not protect the proposed qualitative result from a short conic derivation. The following argument uses the full Shor relaxation throughout. Its Hessian-span accounting is an inference made in this review; it is not attributed to the cited papers.

Write every quadratic as
\[
q_i(x)=x^TA_ix+2b_i^Tx+c_i,\qquad A_i\succeq0,
\qquad h=\dim\operatorname{span}\{A_i\}.
\]
Represent the polyhedron by additional affine inequalities, including both signs of any equality. Their matrices \(A_i\) are zero, so they do not increase \(h\). Translate a fixed feasible point to the origin. This preserves the Hessians and gives \(c_i\le0\) for every row. Set
\[
Q_i=\begin{pmatrix}c_i&b_i^T\\b_i&A_i\end{pmatrix},
\quad K=\mathbb S_+^{n+1}\times\mathbb R_+^m,
\quad \mathcal A=\{(Y,s):Y_{00}=1,\ \langle Q_i,Y\rangle+s_i=0\}.
\]
The point \((E_{00},-c)\) is feasible. The factor \(\mathbb R_+^m\) is polyhedral.

Apply Phase 1 of FRA-Poly to this affine conic system. At a current face, the PSD support has the form \(\mathbb Re_0\oplus U\): this follows inductively because the fixed feasible matrix \(E_{00}\) survives all reductions. Let \(J\) index the slack coordinates that have not been forced to zero. A reducing direction annihilating the affine equations has the form
\[
(W,y)=\left(\sum_i y_iQ_i,y\right).
\]
The multiplier of \(Y_{00}=1\) is zero because a reducing direction annihilates the affine right-hand side. The compression \(\widehat W\) of \(W\) to \(\mathbb Re_0\oplus U\) is PSD. The coefficients satisfy \(y_i\ge0\) on \(J\); the other coefficients need not be nonnegative. However, \(c_i=0\) off \(J\), since the feasible slack vector \(-c\) survives in the current face. Therefore
\[
0\le\widehat W_{00}=\sum_i y_ic_i\le0.
\]
A PSD matrix with a zero diagonal entry has a zero corresponding row and column. Thus
\[
\widehat W=\begin{pmatrix}0&0\\0&H\end{pmatrix},
\qquad H=\sum_i y_i(A_i|_U)\succeq0.
\]
Every Phase 1 reduction changes the PSD factor, because it is the only possible nonpolyhedral factor. Hence \(H\ne0\). The new support is \(\mathbb Re_0\oplus U'\), where \(U'=U\cap\ker H\). The restriction map
\[
\operatorname{span}\{A_i|_U\}\longrightarrow
\operatorname{span}\{A_i|_{U'}\}
\]
kills the nonzero element \(H\), and therefore decreases the span dimension strictly. There are at most \(h\) such steps. Consequently
\[
d_{\rm PPS}(K,\mathcal A)\le h.
\]
This reasoning uses the compressed exposing matrix; asserting that the unreduced full matrix \(W\) remains PSD after the first step would be incorrect. It also explains why the signs of deleted slack coordinates cause no problem.

The residual transfer is exact up to fixed norm constants. For an original point \(x\), take
\[
Y(x)=(1,x)(1,x)^T,\qquad s_i(x)=(-q_i(x))_+.
\]
This pair lies in \(K\), and its affine-equation residual is
\[
\bigl(0,(q_i(x))_+\bigr).
\]
Distance to the nonempty affine set \(\mathcal A\) is bounded by a fixed constant times this residual. The lifted pairs remain bounded when \(x\) does. Proposition 38 therefore gives distance to \(K\cap\mathcal A\) bounded by a constant times \(v(x)^{2^{-h}}\), initially for sufficiently small \(v\).

Finally, if
\[
Y=\begin{pmatrix}1&z^T\\z&X\end{pmatrix}
\]
is Shor-feasible, then \(X-zz^T\succeq0\). Since \(A_i\succeq0\),
\[
q_i(z)\le\langle Q_i,Y\rangle\le0.
\]
Thus the projection of the full Shor feasible set is exactly the original feasible set, and extracting \(z\) is a Lipschitz map. This proves the proposed original-space bound on bounded sets. Enlarging the constant handles residuals away from zero. For points already in the polyhedron, the added affine rows have zero positive residual.

The assessment is therefore: Hu–Li's stated algorithm and the error bound for their unshifted further relaxation do not directly imply the claim. But full Shor lifting, established partial-polyhedral facial reduction, the established conic error bound, and the short span-decrease observation do imply it. The span observation could still be worth stating and proving if it has not appeared explicitly, but it supports a modest refinement or corollary claim. It does not support presenting the qualitative mechanism or exponent derivation as a substantially new theory. This comparison does not assess the separate arithmetic bound on the error constant.

Verification consisted of reading the three primary PDFs and checking the displayed matrix identities and residual map symbolically. A second agent independently checked the conic derivation and the slack-sign issue. No numerical tests, formal verification, or CI checks were run.
