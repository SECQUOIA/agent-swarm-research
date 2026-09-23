# Covariance innovations for the Liu objective and gradient oracle

**Status: [accepted by fresh independent review](research-20260912-covariance-dense-oracle-independent-review.md) after two numerical corrections. No new relaxation or filtering algorithm is claimed.** The isolated [implementation](../code/research_20260912/covariance_dense_oracle.py) evaluates the same scalar-split Liu/virtual-noise design relaxation as the existing dense and tridiagonal comparators. It fixes every recorded near-unit-correlation numerical failure in the tests below. The optimization code and reviewed exact certifiers are unchanged.

The [earlier precision-space implementation](research-20260912-structured-dense-oracle.md) was algebraically correct but numerically unreliable near unit latent correlation. For the saved 12-candidate example with \(s=r=1\), prior \(0.1I\), \(\rho\) equal to the nearest floating-point number below one, and \(a=0.99\), it understated the objective by about 0.628 and produced gradient error about 1.136. Its computed tangent cut off 37 of the 495 cardinality-four designs, with maximum underestimation 0.848. The covariance matrix itself had condition number about 13. Thus the precision coordinates introduced an avoidable numerical problem.

The replacement uses scalar covariance filtering and a reverse derivative sweep. Let

\[
 K_{ij}=s\rho^{|i-j|},\quad R=K+rI,\quad
 s\ge0,\quad r>0,\quad |\rho|<1,
\]

and fix a valid split \(0<a<\lambda_{\min}(R)\). For \(z\in[0,1]^n\), define

\[
 D=\operatorname{diag}(z/a),\quad
 \beta_i=a(1-z_i)+rz_i>0,\quad
 \Pi=\operatorname{diag}(z_i/\beta_i).
\]

The established relaxation uses

\[
 V=[I+(R-aI)D]^{-1}F,\qquad
 J=J_0+F^TDV,\qquad \phi=\log\det J.
\tag{1}
\]

Set \(\mu=KDV\). Rearranging the first equation gives

\[
 \operatorname{diag}(\beta_i/a)V+\mu=F,
 \qquad DV=\Pi(F-\mu),
 \qquad \mu=K\Pi(F-\mu).
\tag{2}
\]

Let \(I=\{i:z_i>0\}\). The solution of (2) is the latent conditional mean for pseudo-observations with noise variance \(\beta_i/z_i\):

\[
 C=K_{II}+\operatorname{diag}_{i\in I}(\beta_i/z_i),\qquad
 \mu=K_{:I}C^{-1}F_I,
 \qquad J=J_0+F_I^TC^{-1}F_I.
\tag{3}
\]

Here each column of \(F\) is a separate deterministic right-hand side for the same linear filter. The outer products below recover all cross terms in the information matrix. Equations (2)–(3) also give the unobserved rows of \(V\), which are needed for derivatives at zero selection weights.

Start the forward recursion at \(P_0^-=s\) and \(m_0^-=0\). With the innovation row \(e_i=F_i-m_i^-\), compute

\[
 q_i=P_i^-z_i+\beta_i,\qquad
 w_i=z_i/q_i,\qquad
 m_i=m_i^-+(P_i^-w_i)e_i,\qquad
 P_i=P_i^-\,\beta_i/q_i.
\tag{4}
\]

The next prediction is

\[
 m_{i+1}^-=\rho m_i,\qquad
 P_{i+1}^-=\rho^2P_i+s(1-\rho)(1+\rho).
\tag{5}
\]

For \(z_i>0\), the innovation variance of the pseudo-observation is \(q_i/z_i\). Its standard innovations decomposition therefore gives

\[
 J=J_0+\sum_i w_i e_i^T e_i.
\tag{6}
\]

When \(z_i=0\), \(w_i=0\), the update is skipped, and its information contribution is zero. No infinite pseudo-observation variance is formed. The implemented covariance update uses the positive product in (4), avoiding the subtractive form \(P_i^- - K_i^2S_i\). The implementation forms (6) as a Gram matrix of rows \(\sqrt{w_i}e_i\).

The reverse recursion starts at \(b_n=0\). For \(i=n-1,\ldots,0\), compute

\[
 V_i=\frac a{q_i}\big(e_i-\rho P_i^-b_{i+1}\big),\qquad
 b_i=w_i e_i+\rho\frac{\beta_i}{q_i}b_{i+1}.
\tag{7}
\]

To derive (7), consider one right-hand side and its innovation quadratic \(Q(F)=\tfrac12\sum_iw_i e_i^2\). The forward mean map is \(m_{i+1}^-=\rho[(1-P_i^-w_i)m_i^-+P_i^-w_iF_i]\). The negative adjoint with respect to \(m_i^-\) is therefore \(b_i=w_ie_i+\rho(1-P_i^-w_i)b_{i+1}\). The identity \(1-P_i^-w_i=\beta_i/q_i\) gives the numerically preferable positive ratio in (7). Differentiating with respect to \(F_i\) gives \(\partial Q/\partial F_i=w_i(e_i-\rho P_i^-b_{i+1})\). By (3), this is row \(i\) of \(DV\). For positive \(z_i\), cancellation of \(z_i/a\) proves the expression for \(V_i\). All quantities in that expression vary continuously as \(z_i\downarrow0\), so it also gives the zero-weight rows of the resolvent in (1).

The objective gradient is then

\[
 \frac{\partial\phi}{\partial z_i}=\frac1a V_iJ^{-1}V_i^T.
\tag{8}
\]

The derivative follows by differentiating (1), as in the earlier oracle derivation. It remains valid at zero weights by continuity of (1). A Cholesky factor of the small information matrix supplies the log determinant and gradient quadratics without an explicit inverse.

For a valid split, the new scale factor satisfies \(a/q_i\le1\) in exact arithmetic. Indeed, \(P_i^-+r\) is the prediction variance of observation \(i\) given earlier observations with added nonnegative virtual noise. Every residual \(Y_i-c^TY_{<i}\) has variance at least \(\lambda_{\min}(R)(1+\|c\|^2)\), and added virtual noise cannot reduce it. Minimizing over \(c\) gives \(P_i^-+r\ge\lambda_{\min}(R)>a\). Hence \(q_i=a(1-z_i)+(P_i^-+r)z_i\ge a\). Also \(|\rho\beta_i/q_i|\le|\rho|\). This removes the large \(a/\beta_i\) amplification discussed below. It is not a complete floating-point error bound.

The forward recursion is classical linear Kalman filtering; the reverse sweep is the ordinary adjoint of its innovation quadratic. The filter and smoothing recursions are given in Theorems 6.6 and 12.2 of [Särkkä and Svensson, *Bayesian Filtering and Smoothing*, second edition (2023)](https://users.aalto.fi/~ssarkka/pub/bfs_book_2023_online.pdf), which were read for this derivation. The original smoothing paper is [Rauch, Tung, and Striebel (1965)](https://doi.org/10.2514/3.3166); its publisher full text was not accessible in this run. Related classical work is [Koopman (1993), *Disturbance smoother for state space models*](https://academic.oup.com/biomet/article-abstract/80/1/117/228156), whose primary abstract was read but whose full text remains unretrieved. These sources were routed to the shared literature delegate. [Rybicki and Press (1995)](https://arxiv.org/pdf/comp-gas/9405004) already supplies directly relevant fast covariance/precision calculations with diagonal noise. None of these filtering, adjoint, or covariance identities is presented as new research.

An initial covariance-space implementation computed \(V_i=a(F_i-m_i^{\mathrm s})/\beta_i\) from Rauch–Tung–Striebel smoothed means. This identity is exact, but fresh review found a second numerical failure: when \(s/r\) is large, subtracting two nearly equal means can destroy the residual before multiplication by \(a/\beta_i\). With \(F=(1,2,-1)^T\), \(n=3\), \(\rho=0.5\), \(s=10^{20}\), \(r=1\), \(J_0=10^{-20}\), \(z=(1,1,1)\), and split fraction 0.5, it returned zero gradients although two true gradient entries were about 0.2188 and 0.1400. At \(s=10^{30}\), the first returned gradient was spuriously about \(2.43\times10^{26}\). Its objective remained accurate. The [initial source](../code/research_20260912/results/covariance-dense-oracle-rts-initial-source.txt) and [initial test report](../code/research_20260912/results/covariance-dense-oracle-rts-validation.json) are preserved, including source hash `a0cf6289d9583d5b700d44cdcfe27c4633b7c9a561f5d7ae8d33525c3f4dd2f8`. The current implementation uses (7) instead.

Review also found an arithmetic range issue in the process variance. Evaluating \(s(1-\rho)(1+\rho)\) left-to-right can overflow for negative \(\rho\) even when the final result is finite. The current code first forms \((1-\rho)(1+\rho)\le1\), then multiplies by \(s\). The case \(s=10^{308},\rho=-0.9\) is retained as a regression check.

The boundary cases are explicit. If \(s=0\), the covariance is \(rI\), so the implementation uses the diagonal formula and never divides by a zero latent variance. If \(\rho=0\) or \(n=1\), the diagonal variance is \(s+r\). The one-observation formula therefore does not depend on \(\rho\). If every weight is zero, \(J=J_0\), \(V=F\), and the gradient is still generally nonzero. Negative correlation changes the signs of the mean-transition and smoothing gains, without changing variance positivity. Splits \(a>r\) remain admissible when \(a<\lambda_{\min}(R)\); \(\beta_i\) is positive throughout the cube in that case as well.

The split setup reuses only the existing structured constructor's selected tridiagonal eigenvalue calculation. It does not call its defective value or gradient method. This setup computes \(\lambda_{\min}(R)=r+s(1-\rho^2)/\lambda_{\max}(M)\), with the same diagonal special cases as before. The spectral calculation and split check remain numerical. A verified exact split and an outward log determinant are still required for an exact tangent certificate; the [rational certifier](research-20260912-exact-dense-design-certificates.md) remains the authority for such claims.

The [author validation report](../code/research_20260912/results/covariance-dense-oracle-validation.json) records these checks:

- 1,200 equalities with the original dense solve and 1,200 with the separately implemented active virtual-covariance reference.
- 650 binary true-objective comparisons, 200 directional derivatives, 600 numerical tangent comparisons, and 200 automatic split comparisons.
- 81 exact rational comparisons of the innovation information matrix and reverse-adjoint residual rows against explicitly inverted dense matrices, with matching numerical gradients. These include zero latent variance, zero and negative correlation, singleton problems, zero weights, and splits exceeding the nugget.
- All 12 saved conditioning witnesses and 12 additional copies with negative correlation. Maximum value and gradient errors were both below \(1.8\times10^{-15}\). The three saved high-precision references also agreed within the stated tolerances.
- The full 495-design tangent check on the original failure witness. No violation exceeded \(10^{-10}\); the smallest numerical slack was 0.2639024664.
- Nineteen rejected malformed query points or split values.
- Ten new high-precision comparisons for latent-to-nugget ratios from \(10^8\) through \(10^{30}\), with both signs of correlation, and the two finite-range cases \(s=10^{308},\rho=\pm0.9\).

The numerical sweep's largest objective error was \(3.20\times10^{-14}\), scaled gradient error \(5.19\times10^{-14}\), and scaled directional-derivative error \(6.55\times10^{-11}\). These are tested numerical agreements, not rigorous floating-point error bounds.

The [fresh independent verifier](../code/research_20260912/review_covariance_dense_oracle.py) and [saved report](../code/research_20260912/results/covariance-dense-oracle-independent-review.json) accepted final source hash `db32a250b9d7313c0d71264860849512c77d3bba7ae06794de2fbbe58b35ce2d`. They check 222 exact rational identities, 240 direct high-precision ordinary comparisons, 42 extreme variance-ratio and mixed-weight cases through \(s/r=10^{100}\), scaling by \(10^{-200}\) and \(10^{200}\), and the finite-range process-variance cases. The largest scaled gradient discrepancy in the extreme sweep was \(5.56\times10^{-16}\). The reviewer reproduced the old precision tangent's 37 positive-correlation and nine negative-correlation violations among 495 designs per sign. The repaired tangent had none in either test. The archived initial RTS implementation's spurious \(2.43\times10^{26}\) gradient was also shown to produce an invalid binary cut. These findings and both repairs are retained in the independent review.

The complete value and gradient require \(O(np^2+p^3)\) operations and \(O(np+p^2+n)\) storage. Python loops make this first implementation slower on small problems, despite linear growth in \(n\) for fixed \(p\). The same-split, one-thread timings used four deterministic interior points, \(p=3\), \(\rho=0.6\), \(s=r=1\), and split fraction 0.99. Values are medians after warm-up: 9 calls for the dense oracle and 31 for the covariance oracle.

| Candidates | Dense evaluation | Covariance evaluation | Dense / covariance |
|---:|---:|---:|---:|
| 48 | 0.0459 ms | 0.3109 ms | 0.148 |
| 96 | 0.0736 ms | 0.5522 ms | 0.133 |
| 512 | 3.5327 ms | 2.9217 ms | 1.209 |
| 2,048 | 775.0777 ms | 11.1641 ms | 69.426 |

Single observed setup times are retained separately in the report. This is a shared-machine component benchmark; it does not establish an end-to-end mixed-integer solve speedup. No MIP was run for this task. The immediate benefit is removal of the documented numerical cut error, not faster small-instance evaluation.

Numerical limits remain. Ill-conditioned information matrices, cancellation in very small residual rows, and values outside floating-point range can still prevent reliable evaluation. On the \(s=10^{30}\) regression, a gradient entry of order \(10^{-61}\) can still be returned at order \(10^{-34}\). Its absolute error is small in the reported tests and its relative error is large. The implementation rejects nonpositive or nonfinite innovation and predicted variances, and nonfinite outputs, but it does not certify every rounding error. The covariance-space calculation removes the identified ill-conditioned precision solve; it does not turn floating-point gradients into guaranteed global cuts.

Reproduction in the existing isolated environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/verify_covariance_dense_oracle.py
```

Use `--validate-only` to skip timing. The report records Python 3.13.11, NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0, thread settings, and all relevant source hashes. No dependency was added.
