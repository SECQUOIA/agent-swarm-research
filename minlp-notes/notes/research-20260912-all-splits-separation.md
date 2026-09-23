# Certified separation from every admissible scalar covariance split

**Status: [accepted by fresh independent review](research-20260912-all-splits-independent-review.md) for the implementation and original six certificates, with a [separate accepted review of four kinetics artifacts](research-20260912-kinetics-dense-certificate-review.md). No novelty claim for virtual-noise monotonicity.** This strengthens [the fixed-split comparison](research-20260912-exact-dense-design-certificates.md). In all six benchmark cases, the exact memory bound is strictly smaller than the optimum of every admissible scalar-split Liu/virtual-noise continuous relaxation. The conclusion survives tuning the scalar split to the spectral boundary.

The [separate implementation](../code/research_20260912/certify_all_splits.py) does not modify the core under review. [Its six certificates](../code/research_20260912/results/dense-all-splits-certificates.json) contain the rational spectral witnesses, feasible points, information matrices, logarithm enclosures, comparison data, and source hashes.

## 1. Pointwise monotonicity gives a uniform lower bound

Let \(\mathcal Z_k=\{z\in[0,1]^n:\sum z_i=k\}\). For a fixed feasible \(z\), let \(I=\{i:z_i>0\}\). At every scalar \(a>0\), define the virtual-noise point value

\[
J_a(z)=J_0+F_I^T\left[R_{II}+a\operatorname{diag}_{i\in I}
\left(\frac{1-z_i}{z_i}\right)\right]^{-1}F_I,
\qquad \phi_a(z)=\log\det J_a(z).
\tag{1}
\]

If \(I\) is empty, the information is \(J_0\). This expression is well-defined for every positive \(a\), whether or not that value defines a concave Liu relaxation. For an admissible split \(0<a<\lambda_{\min}(R)\), it equals the existing Liu objective, including zero weights by support restriction.

**Proposition.** If \(\bar a\ge\lambda_{\min}(R)\) and \(z\in\mathcal Z_k\), then

\[
\max_{x\in\mathcal Z_k}\phi_a(x)\ge\phi_{\bar a}(z)
\quad\text{for every }0<a<\lambda_{\min}(R).
\tag{2}
\]

**Proof.** The diagonal coefficient of \(a\) in (1) is nonnegative. Increasing \(a\) therefore increases the virtual covariance in positive semidefinite order. Matrix inversion reverses that order, multiplication by \(F_I\) preserves it, and adding \(J_0\) preserves positive definiteness. Monotonicity of the log determinant gives \(\phi_a(z)\ge\phi_{\bar a}(z)\) whenever \(a\le\bar a\). Feasibility of \(z\) gives \(\max_x\phi_a(x)\ge\phi_a(z)\). Combining the two inequalities proves (2). ∎

The same argument includes \(a=\lambda_{\min}(R)\) when the boundary formulation is defined through (1). It does not require optimizing \(z\) at \(\bar a\), proving concavity at \(\bar a\), or differentiating there. In particular, an upper tangent at an inadmissible split would be unjustified and is never used.

An exact lower enclosure of \(\phi_{\bar a}(z)\) now lower-bounds the entire family of continuous relaxation optima. If a separately verified bound \(U\) satisfies

\[
\max_{\text{feasible binary }x}\phi(x)\le U
<\underline\phi_{\bar a}(z),
\tag{3}
\]

then every admissible scalar-split continuous relaxation is strictly weaker than \(U\). This conclusion does not depend on knowing the integer optimum or on the quality of a particular numerical algorithm for the Liu relaxation.

## 2. Exact spectral and information witnesses

For \(R=K+rI\), \(K_{ij}=s\rho^{|i-j|}\), \(s>0\), use \(K=cM^{-1}\), where the scaled precision \(M\) is tridiagonal and SPD. As shown in the structured-oracle note,

\[
R-\bar aI=M^{-1/2}G_{\bar a}M^{-1/2},\qquad
G_{\bar a}=cI+(r-\bar a)M.
\tag{4}
\]

The new certificate records the first nonpositive pivot in an exact tridiagonal elimination of \(G_{\bar a}\), together with all preceding positive pivots. The corresponding leading principal determinant is the product of these pivots and is nonpositive. Sylvester's criterion implies that \(G_{\bar a}\) is not positive definite. Congruence in (4) gives \(R-\bar aI\not\succ0\), hence \(\lambda_{\min}(R)\le\bar a\). Zero pivots are valid witnesses; there is no division by a nonpositive pivot. For zero latent variance, the certificate checks \(\bar a\ge r\) directly through the diagonal matrix.

The program proposes \(\bar a\) on a \(10^{-12}\) rational grid near the spectral value inferred from the earlier fraction-0.99 split. The proposal is not trusted. If needed, it increases the candidate until the exact nonpositive-pivot witness is obtained, within a stated finite search cap. Failure returns no certificate.

To evaluate (1), the program skips zero-weight rows and applies an exact scalar Kalman recursion with observation-specific independent noise

\[
r_i^{\mathrm{virtual}}=r+\bar a(1-z_i)/z_i>0.
\]

Between retained observations it uses the exact transition \(\rho^{t_i-t_{i-1}}\) and stationary process innovation variance. Innovation sensitivities accumulate the information matrix. This value-only route avoids latent precision coordinates and does not compute a gradient. All arithmetic is rational; the reviewed logarithm routine supplies the final lower enclosure.

## 3. Six exact comparisons

The feasible points are the rational points from the earlier continuous certificates. Exact problem data are checked for equality before comparing with the existing calendar-memory \(L=8\) certificates.

| Candidates | Seed | Uniform lower bound for every scalar split | Memory true-objective upper bound | Certified separation | Additional total time |
|---:|---:|---:|---:|---:|---:|
| 48 | 0 | 7.746566516 | 7.699350373 | 0.047216142 | 0.0102 s |
| 48 | 1 | 7.797065612 | 7.761129966 | 0.035935645 | 0.0121 s |
| 48 | 2 | 8.324678975 | 8.278288697 | 0.046390278 | 0.0099 s |
| 96 | 0 | 10.488729910 | 10.449595357 | 0.039134553 | 0.0303 s |
| 96 | 1 | 10.173482779 | 10.150720758 | 0.022762022 | 0.0251 s |
| 96 | 2 | 10.572107249 | 10.545755976 | 0.026351273 | 0.0351 s |

Displayed decimals are rounded; rational differences in the certificate are strictly positive. These times exclude the earlier numerical point generation and memory-bound computation. The previous note reports those stages separately. This is a certified comparison of bounds, not a runtime comparison between complete integer solvers.

The two-candidate example also has an exact limiting certificate. With \(R=\left(\begin{smallmatrix}2&1\\1&2\end{smallmatrix}\right)\), \(F=(1,-1)^T\), prior 1, cardinality 1, and \(\bar a=1=\lambda_{\min}(R)\), the midpoint has information 2. Every binary choice has information \(3/2\). The spectral witness has a zero final pivot, and the uniform separation is \(\log 2-\log(3/2)>0\).

### Four smooth kinetics cases

The same unchanged module was then applied to the four kinetics inputs described in [the exact dense note](research-20260912-exact-dense-design-certificates.md). The new artifacts are [dense-all-splits-kinetics-n48-certificates.json](../code/research_20260912/results/dense-all-splits-kinetics-n48-certificates.json) and [dense-all-splits-kinetics-n96-certificates.json](../code/research_20260912/results/dense-all-splits-kinetics-n96-certificates.json). At each size, cases 0 and 1 are the fast and slow regimes.

| Candidates | Regime | Uniform lower bound for every scalar split | Memory true-objective upper bound | Certified separation | Additional total time |
|---:|---|---:|---:|---:|---:|
| 48 | fast | 15.059809889 | 14.950572423 | 0.109237466 | 0.0437 s |
| 48 | slow | 10.043391642 | 9.959610621 | 0.083781022 | 0.0460 s |
| 96 | fast | 17.080044803 | 16.975678758 | 0.104366046 | 0.2227 s |
| 96 | slow | 11.983533366 | 11.895819868 | 0.087713498 | 0.2079 s |

[The comparison script](../code/research_20260912/compare_kinetics_certificates.py) verifies exact equality of the source, dense, all-splits, and existing memory-certificate problem data, and records exact positive differences in [its report](../code/research_20260912/results/kinetics-dense-memory-certified-comparison.json). This uses the independently checked saved mean sensitivities and a stylized noise model; it is not an experimental validation of the covariance. The figures isolate relaxation strength from incomplete outer approximation and scalar split choice. They do not compare complete integer solve times. The accepted core is unchanged. A [separate fresh review](research-20260912-kinetics-dense-certificate-review.md) reproduced all four additional dense and all-splits values exactly and accepted their matching data, hashes, and positive separations.

## 4. Relation to virtual-noise design literature

[Pázman, Hainy, and Müller (2022)](https://arxiv.org/abs/2103.02989) establishes the convex virtual-noise design approach. [Hainy, Müller, and Pázman (2025)](https://arxiv.org/html/2504.17651) explicitly proves its equivalence to the Liu continuous information formula in Proposition 3, using the normalized measure \(\xi=z/k\), including zero weights. The latter paper also studies stronger optimization implementations of that same measure problem. Faster convergence of those algorithms cannot change the optimum compared in (2).

The 2025 paper's modified variance formula uses \(\tilde\kappa R_{ii}(1-z_i)/z_i\), with \(\tilde\kappa\) bounded by the smallest eigenvalue of the correlation matrix. In our six original cases \(R_{ii}=s+r=2\) is constant. Substitution \(a=2\tilde\kappa\) makes the modified formulation exactly the same scalar family, with \(a\le\lambda_{\min}(R)\). The four kinetics cases have the same reduction with the constant variance \(R_{ii}=0.0025\). Thus the uniform comparison also covers that modified virtual-noise family for these homoscedastic cases. This mapping is a direct specialization of the published formulas. It does not claim equivalence for heterogeneous variances.

The proposition above is an elementary use of established virtual-noise monotonicity. The useful capability is a short rational witness that a stronger competing bound remains stronger for all admissible scalar split choices. This does not cover arbitrary diagonal or matrix-valued splits, additional valid inequalities, integer branch and bound, or other convex relaxations. Those could supply stronger competitors.

The 2025 paper and the current VNDesign software were routed to the shared literature agent. No knowledge-base files were changed by this researcher.

## 5. Validation and reproduction

[The independent dense-arithmetic verifier](../code/research_20260912/verify_all_splits.py) checks the value against explicitly formed rational covariances with heterogeneous virtual noise. [Its report](../code/research_20260912/all-splits-validation.json) records 216 exact value equalities, 144 positive-semidefinite monotonicity comparisons, 36 spectral-witness checks, 36 valid-split point-bound comparisons, six malformed-input rejections, and the two-candidate limiting example. It covers zero weights, zero latent variance, zero and negative correlations, singleton models, and zero-pivot witnesses. These reference calculations were written by the implementing researcher. The subsequent [fresh-agent review](research-20260912-all-splits-independent-review.md) independently checked the core and all six original certificate values, spectral assertions, logarithm enclosures, and positive comparisons, and accepted their scope.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/verify_all_splits.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_all_splits.py code/research_20260912/results/dense-design-exact-certificates.json code/research_20260912/results/dense-all-splits-certificates.json --memory-dir code/research_20260912/results
```
