# Reduced log-Hessian limit at a unique degenerate LP vertex

Status: Proved and independently audited; close classical antecedent found  
Started: 2026-09-04  
Paper status: Not incorporated; corrects the discussion in Section 4  
Confidence: High on the theorem; low on standalone novelty

## Result

Consider the strictly feasible primal--dual pair

\[
 \min\{c^Tx:Ax=b,\ x\geq0\},\qquad
 A^Ty+s=c,\quad s\geq0,                                      \tag{1}
\]

where \(A\in\mathbb R^{m\times n}\) has full row rank and the primal
optimum \(x^*\) is unique. Put

\[
 B=\{i:x_i^*>0\},\qquad N=[n]\setminus B,                    \tag{2}
\]

and let \((x(\mu),y(\mu),s(\mu))\) be the logarithmic central path,
normalized by

\[
 x_i(\mu)s_i(\mu)=\mu.                                      \tag{3}
\]

Let \(s^a=\lim_{\mu\downarrow0}s(\mu)\). This is the relative analytic
center of the dual optimal slack face, and strict complementarity gives

\[
 s_B^a=0,\qquad s_N^a>0.                                     \tag{4}
\]

If \(W\in\mathbb R^{n\times(n-m)}\) has orthonormal columns spanning
\(\ker A\), define the equality-reduced primal log-barrier Hessian

\[
 H_{\rm red}(\mu)=W^T\operatorname{Diag}(x(\mu)^{-2})W.      \tag{5}
\]

Then

\[
 \boxed{
 \mu^2H_{\rm red}(\mu)\longrightarrow
 L:=W^T\operatorname{Diag}((s^a)^2)W\succ0.}                 \tag{6}
\]

Thus, for every increasingly ordered eigenvalue,

\[
 \mu^2\lambda_j(H_{\rm red}(\mu))\longrightarrow\lambda_j(L),
 \qquad
 \kappa_2(H_{\rm red}(\mu))\longrightarrow\kappa_2(L)<\infty.
                                                                    \tag{7}
\]

The statement is nonvacuous when \(n>m\). When \(n=m\), the feasible affine
space has dimension zero and the reduced matrix is empty.

The main point is that uniqueness, not primal nondegeneracy, is sufficient.
At a unique degenerate vertex one has \(|B|<m\), but all reduced-Hessian
modes still grow at the common scale \(\mu^{-2}\); degeneracy creates no
second spectral scale in this formulation.

## Proof

Complementarity (3) gives the exact identity

\[
 \mu^2H_{\rm red}(\mu)
 =W^T\operatorname{Diag}(s(\mu)^2)W.                          \tag{8}
\]

The classical LP central-path convergence theorem gives
\(s(\mu)\to s^a\), so the right side converges to \(L\) in operator norm.
It remains to prove that \(L\) is positive definite.

First, \(A_B\) has full column rank. If \(A_Bv=0\) for nonzero \(v\), then
\(x_B^*\pm tv>0\) for sufficiently small \(t>0\). Extending these two
vectors by zero on \(N\) gives distinct primal feasible points. For any
dual optimum, complementary slackness gives \(c_B=A_B^Ty^*\), and hence

\[
 c_B^Tv=(y^*)^TA_Bv=0.                                      \tag{9}
\]

Both perturbed points would therefore be optimal, contradicting uniqueness.

Now take \(z\in\ker A\) with
\(z^T\operatorname{Diag}((s^a)^2)z=0\). Equation (4) forces \(z_N=0\).
Then \(A_Bz_B=0\), so the full-column-rank property gives \(z_B=0\). Thus
the diagonal quadratic form is positive definite on \(\ker A\), proving
\(L\succ0\). Operator-norm convergence and continuity of ordered eigenvalues
and of \(\kappa_2\) on the positive-definite cone prove (7).

## Direct active-set formula and explicit bounds

The limiting slack can be computed without tracing the path. The dual
analytic-center point is the unique solution of

\[
 \begin{split}
 \max_y\quad&\sum_{i\in N}\log(c_i-a_i^Ty)\\
 \text{subject to}\quad&A_B^Ty=c_B,\\
 &c_N-A_N^Ty>0,
 \end{split}                                                  \tag{10}
\]

and \(s_N^a=c_N-A_N^Ty^a\). Every feasible point of (10) is dual optimal,
because \(b=A_Bx_B^*\). Under the stated full-row-rank assumption, the
slack map \(y\mapsto c-A^Ty\) is injective, so \(y^a\) itself is unique.
If redundant equality rows are retained instead, only the slack vector is
intrinsic and unique.

Let \(R_N\) restrict a vector to its \(N\)-coordinates, and set

\[
 \sigma_N=\sigma_{\min}(R_NW)>0,\qquad
 \rho_N=\|R_NW\|_2\leq1.                                    \tag{11}
\]

Injectivity of \(R_NW\) is exactly the uniqueness argument above. With

\[
 s_{\min}=\min_{i\in N}s_i^a,\qquad
 s_{\max}=\max_{i\in N}s_i^a,                               \tag{12}
\]

the Loewner inequalities

\[
 s_{\min}^2(R_NW)^T(R_NW)
 \preceq L\preceq
 s_{\max}^2(R_NW)^T(R_NW)                                  \tag{13}
\]

give

\[
 s_{\min}^2\sigma_N^2\leq\lambda_{\min}(L)
 \leq s_{\max}^2\sigma_N^2,                                \tag{14}
\]

\[
 s_{\min}^2\rho_N^2\leq\lambda_{\max}(L)
 \leq s_{\max}^2\rho_N^2,                                  \tag{15}
\]

and therefore

\[
 \left({s_{\min}\over s_{\max}}\right)^2
 \left({\rho_N\over\sigma_N}\right)^2
 \leq\kappa_2(L)\leq
 \left({s_{\max}\over s_{\min}}\right)^2
 \left({\rho_N\over\sigma_N}\right)^2.                    \tag{16}
\]

These inequalities separate reduced-cost spread from the angle between
\(\ker A\) and the coordinate space supported on \(B\). They remain valid
for rectangular, full-column-rank \(A_B\), which is the degenerate-vertex
case.

## The limiting constant is not uniformly bounded

Boundedness in \(\mu\) is only an instancewise statement. For any \(M\geq1\),
consider

\[
 A=\begin{bmatrix}1&0&0&0\\0&1&-1&0\end{bmatrix},\qquad
 b=\binom{1}{0},\qquad c=(0,1,1,M)^T.                         \tag{17}
\]

The primal is strictly feasible, for example at \((1,1,1,1)\), and the dual
is strictly feasible, for example at \(y=(-1,0)\). Its unique optimum is
\(x^*=e_1\), which is degenerate because \(|B|=1<m=2\). The exact central
path is

\[
 x(\mu)=(1,\mu,\mu,\mu/M),\qquad
 s(\mu)=(\mu,1,1,M).                                        \tag{18}
\]

With

\[
 W=\begin{bmatrix}
 0&0\\ 2^{-1/2}&0\\2^{-1/2}&0\\0&1
 \end{bmatrix},                                             \tag{19}
\]

one gets the exact identity

\[
 \mu^2H_{\rm red}(\mu)=L=\operatorname{Diag}(1,M^2),
 \qquad\kappa_2(L)=M^2.                                    \tag{20}
\]

Rescaling the whole objective to unit norm does not change this condition
number. Hence (7) removes accuracy-driven blowup but supplies no
dimension-, bit-length-, or data-independent conditioning bound.

## Numerical audit of the original witness

For

\[
 A=\begin{bmatrix}1&1&1&1\\0&1&3/2&3\end{bmatrix},\qquad
 b=\binom{1}{3/2},\qquad c=(1,1,0,1)^T,                      \tag{21}
\]

the point \((2,3,3,3)/11\) is strictly primal feasible, and \(y=(-1,0)\)
is strictly dual feasible. The unique optimum is \(x^*=e_3\), so
\(|B|=1<m=2\). Writing \(y=(-3t/2,t)\) on the dual optimal face gives

\[
 (s_1,s_2,s_4)=(1+3t/2,1+t/2,1-3t/2).                       \tag{22}
\]

The derivative of the sum of their logarithms vanishes at

\[
 t={-6+4\sqrt3\over9}.                                      \tag{23}
\]

The objective in (10) is strictly concave on its interval, so this is the
unique analytic center. A direct orthonormal-nullspace calculation gives

\[
 \operatorname{spec}(L)
 \approx(0.24888160,1.14289062),\qquad
 \kappa_2(L)\approx4.59210571.                              \tag{24}
\]

These values reproduce the candidate calculation.

## Literature screen and novelty assessment

The matrix packaging (6)--(16) is useful, but its mathematical ingredients
are close prior art rather than a new publishable theorem.

- Adler and Monteiro prove convergence to the centered dual optimum in
  their Theorem 3.3 and, for unit weights, the stronger endpoint formula
  \(x_N(\mu)/\mu\to(s_N^a)^{-1}\) in Theorem 5.1. On the following page they
  explicitly observe that a zero-dimensional optimal face makes \(A_B\)
  full column rank. Combining their statements with (5) immediately yields
  (6). See [Adler--Monteiro 1991](https://doi.org/10.1007/BF01594923),
  especially pp. 40 and 44--45.
- Güler proves analytic-center convergence and finite endpoint derivatives
  for weighted LP central paths. Halická later proves a genuine analytic
  extension through \(\mu=0\). These results also sharpen (6) to
  \(\mu^2H_{\rm red}(\mu)=L+O(\mu)\). See
  [Güler 1994](https://doi.org/10.1007/BF01581702) and
  [Halická 1999](https://doi.org/10.1007/s101070050025).
- Wright and Orban treat log-barrier minimizers with dependent active
  gradients in nonlinear programming and characterize their first-order
  approach under strict complementarity. The LP result here is a much
  simpler special case. See
  [Wright--Orban 2002](https://doi.org/10.1287/moor.27.3.585.312).
- M. H. Wright's earlier Hessian-spectrum analysis assumes linearly
  independent active gradients, so it does not by itself cover the
  degenerate active set considered here. See
  [Wright 1994](https://doi.org/10.1007/BF01582224).

No source found in the targeted search states exactly the orthonormal
compression and two-sided condition-number bounds (6)--(16). Nevertheless,
because (6) is an immediate corollary of Adler--Monteiro's endpoint formulas,
it should be cited as a classical corollary and not advertised as novel.

## QIPM consequence and limits

For an exact-central, equality-reduced primal formulation with an
orthonormal nullspace basis, a unique optimum prevents any
\(\epsilon^{-1}\)-driven growth of the spectral condition number, even when
the vertex is degenerate. This corrects the sentence in
`paper/sections/04-spectra.tex` that attributes the full-rank restriction
\(\operatorname{rank}(R_NW)=n-m\) only to a unique *nondegenerate* optimum.
Uniqueness alone gives that rank.

This does not yet improve an end-to-end QIPM complexity bound:

1. \(\kappa_2(L)\) can be arbitrarily large, as (17)--(20) show;
2. building \(W\) can destroy sparsity or require hard nullspace
   preprocessing;
3. the normal equations and full primal--dual KKT matrix have different
   spectra; and
4. block-encoding normalization, right-hand-side preparation, tomography,
   and inexact-neighborhood requirements are not controlled by (6).

The result is therefore a useful formulation-specific obstruction to a
blanket claim that primal degeneracy forces late-path QLSA ill-conditioning,
not a quantum speedup theorem.

## Audit record

The audit checked the central-path hypotheses, complementarity identity,
the equivalence between uniqueness and injectivity of \(R_NW\), every
eigenvalue inequality in (14)--(16), and both examples. It also removed an
inconsistent suggestion that \(y^a\) may be nonunique while \(A\) has full
row rank. The literature screen found the decisive Adler--Monteiro
collision, which changes the status from candidate novelty to an audited
classical corollary.
