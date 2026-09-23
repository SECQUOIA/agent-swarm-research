# A structured comparator for the Liu correlated-noise selection relaxation

**Status: exact algebra and moderate-correlation benchmarks pass; fresh review found a floating-point instability near unit correlation, described below. A [separate covariance-innovation repair](research-20260912-covariance-dense-oracle.md) has now passed fresh independent review. No novelty claim.** The [prototype](../code/research_20260912/structured_dense_oracle.py) is algebraically equivalent to `DenseLiuOracle` in [noisy_markov_design.py](../code/research_20260912/noisy_markov_design.py). The [saved validation and timing report](../code/research_20260912/structured_dense_oracle.json) records the numerical environment and source hashes. No full mixed-integer solves were run for this comparison.

The existing comparator uses a dense solve for each oracle call. With stationary AR(1) latent noise plus a positive independent nugget, the same calculation reduces to an SPD tridiagonal solve. This matters for comparison: an advantage over avoidable dense linear algebra is not evidence that a new design relaxation or optimization algorithm is better.

## 1. The same objective and gradient

Let \(F\in\mathbb R^{n\times p}\), let \(J_0\succ0\) be prior information, and let

\[
R=K+rI,\qquad K_{ij}=s\rho^{|i-j|},\qquad
s\ge0,\quad r>0,\quad |\rho|<1.
\]

Fix \(0<a<\lambda_{\min}(R)\), write \(S=R-aI\succ0\), and for \(z\in[0,1]^n\) set \(D=\operatorname{diag}(z/a)\). The existing implementation evaluates

\[
V=(I+SD)^{-1}F,\qquad
J(z)=J_0+F^TDV,\qquad \phi(z)=\log\det J(z).
\tag{1}
\]

The matrix \(D(I+SD)^{-1}\) is symmetric positive semidefinite. If \(z\) is binary with selected set \(I\), (1) reduces to \(J_0+F_I^T R_{II}^{-1}F_I\), so the binary objective is the true selected marginal information criterion. The covariance split is the established construction in [Liu et al. (2016)](https://arxiv.org/abs/1508.03690).

For a diagonal perturbation \(dD\), direct differentiation gives

\[
d\{D(I+SD)^{-1}\}=(I+DS)^{-1}(dD)(I+SD)^{-1}.
\]

Thus, writing \(V_i\) for row \(i\),

\[
\frac{\partial J}{\partial z_i}=\frac1a V_i^TV_i,
\qquad
\frac{\partial\phi}{\partial z_i}=\frac1a V_iJ^{-1}V_i^T.
\tag{2}
\]

These formulas remain valid at zero selection coordinates; no inverse of \(D\) is needed. The usual matrix-concavity argument follows from

\[
D(I+SD)^{-1}
=S^{-1}-S^{-1}(S^{-1}+D)^{-1}S^{-1}.
\]

Consequently \(\phi\) is concave and its tangents are upper bounds on the continuous relaxation. The condition on \(a\) is needed for this argument and for valid outer-approximation upper bounds; the structured linear system's solvability alone does not establish it.

## 2. Tridiagonal evaluation

Assume first \(s>0\), so \(Q=K^{-1}\succ0\). Multiplying the system for \(V\) by \(Q\) gives

\[
\big[Q+(I+(r-a)Q)D\big]V=QF.
\tag{3}
\]

Define

\[
W=I+(r-a)D,
\qquad w_i=\frac{a(1-z_i)+rz_i}{a}>0.
\]

Then the matrix in (3) is \(QW+D\). Set \(U=WV\); the equation becomes

\[
\underbrace{\big(Q+DW^{-1}\big)}_{H\succ0}\,U=QF,
\qquad V=W^{-1}U.
\tag{4}
\]

The added matrix is diagonal and nonnegative, so \(H\) is SPD and has the same tridiagonal sparsity as \(Q\). This formulation avoids square roots, which is convenient for a later rational certificate. Equivalently, \(QW+D\) is similar to the SPD matrix \(W^{1/2}QW^{1/2}+D\).

For \(n\ge2\), use the scaled precision

\[
Q=M/c,\qquad c=s(1-\rho^2),
\]

where \(M\) has endpoint diagonal entries \(1\), interior entries \(1+\rho^2\), and off-diagonal entries \(-\rho\). With \(t_i=a(1-z_i)+rz_i\), (4) becomes

\[
\left[M+c\operatorname{diag}(z_i/t_i)\right]U=MF,
\qquad V_i=\frac a{t_i}U_i,
\qquad (DV)_i=\frac{z_i}{t_i}U_i.
\tag{5}
\]

The scaled formulation avoids dividing the precision by a small latent variance. Evaluating \(t_i\) as the displayed positive sum avoids subtractive cancellation in \(1+(r-a)z_i/a\) when \(a>r\) and \(z_i\) is near one. The prototype uses SciPy's SPD banded solver, then the unchanged small information matrix and gradient formulas (1)–(2).

Factorization and solving for \(V\) cost \(O(np)\). Forming \(J\), solving with \(J\), and obtaining all gradient entries cost \(O(np^2+p^3)\) in total. Thus the complete oracle is linear in \(n\) for fixed \(p\); claiming \(O(np)\) for the entire value-and-gradient calculation would omit the information-matrix work. Storage is \(O(np+p^2+n)\).

## 3. Splitting and boundary cases

- **Positive latent variance, \(n\ge2\).** Since \(R=rI+cM^{-1}\), its smallest eigenvalue is \(r+c/\lambda_{\max}(M)\). One selected tridiagonal eigenvalue computes the same numerical split fraction as the dense covariance eigensolve. The prototype's default setup uses that calculation. Selected-eigenvalue computation is a separate setup cost; the linear oracle count above concerns a fixed split.
- **One observation.** \(K=[s]\), \(Q=[1/s]\), and \(\lambda_{\min}(R)=s+r\). The general endpoint formula divided by \(s(1-\rho^2)\) would be wrong for \(n=1\). The code uses direct diagonal evaluation.
- **Zero latent variance.** \(Q\) does not exist. Here \(R=rI\), and direct diagonal evaluation is exact: \(V_i=aF_i/[a(1-z_i)+rz_i]\). No limiting precision matrix is constructed.
- **Zero correlation.** \(R=(s+r)I\), so the same direct formula uses total variance \(s+r\) in place of \(r\). This also covers \(n=1\) for every allowed correlation.
- **Zero selection vector.** \(V=F\), \(J=J_0\), and the gradient is still \(F_iJ_0^{-1}F_i^T/a\). The implementation returns this without solving a tridiagonal system.
- **Negative correlation.** The off-diagonal precision signs change, but positive definiteness and the derivation are unchanged.
- **A split exceeding the nugget.** This is allowed when \(a<\lambda_{\min}(R)\). Positivity of \(w_i\) follows from \(a(1-z_i)+rz_i>0\); one must not unnecessarily impose \(a<r\).

The proof assumes \(r>0\) and \(z\in[0,1]^n\). At zero nugget and selected coordinates, \(W\) can be singular, so (4) is not an applicable implementation. That different noiseless model has its own Markov methods. Floating-point evaluation near extreme conditioning or the representational range remains numerical; the prototype does not convert a numerical eigenvalue or Cholesky factorization into an exact certificate.

**Observed numerical defect.** Fresh reviewer `structured_oracle_review` found substantial error when \(\rho\) approaches one, even though the nugget keeps \(R\) well-conditioned. For \(n=12\), \(s=r=1\), \(\rho\) equal to the nearest floating-point number below one, prior \(0.1I\), `F=np.random.default_rng(492).normal(size=(12,3))`, \(z\) equally spaced from \(0.2\) to \(0.8\), and split fraction \(0.99\), the structured value differs from the dense value by about \(-0.628\) and the maximum gradient error is about \(1.14\), while \(\operatorname{cond}(R)\approx13\). Correlation \(1-10^{-12}\) already gives value error around \(1.3\times10^{-5}\). The precision coordinates, rather than the physical covariance, cause the instability. The current implementation must not be treated as numerically reliable across the entire admitted parameter range. A stable latent Kalman/smoother formulation is a possible repair; exact rational evaluation of (5) is unaffected. The reported timings concern moderate correlation and remain separately reproducible.

## 4. An exact split and tangent certificate is feasible

For rational \(\rho,s,r,a\), the split condition can be verified without forming a dense covariance. With the scaled precision above,

\[
R-aI=M^{-1/2}\big[cI+(r-a)M\big]M^{-1/2}.
\tag{6}
\]

Therefore \(a<\lambda_{\min}(R)\) is equivalent to positive definiteness of the **tridiagonal rational** matrix \(G_a=cI+(r-a)M\). A tridiagonal \(LDL^T\) factorization with exact positive pivots proves this using \(O(n)\) field operations. It allows a rational split chosen near a numerical estimate to be checked exactly. For \(s=0\), the exact condition is simply \(0<a<r\).

A simpler sufficient choice is \(a=\gamma(r+c/G)\), with rational \(0<\gamma<1\) and a Gershgorin bound \(G\ge\lambda_{\max}(M)\). This can be conservative, whereas (6) can certify a tighter candidate directly.

If the design data, prior, split and query point are rational, (5) gives rational \(V\), \(J\), and gradient (2) by exact linear algebra. A global upper tangent then needs only an outward upper bound on \(\log\det J\) for its intercept. For a cardinality domain, maximizing its rational linear part amounts to summing the appropriate largest gradient entries. This route has since been implemented in the [independently reviewed exact dense certifier](research-20260912-exact-dense-design-certificates.md). Bit complexity and rational denominator growth are distinct from the field-operation counts. No new theorem is claimed for these elementary algebraic observations.

## 5. Isolated numerical comparison

The run used Python 3.13.11, NumPy 2.5.3 and SciPy 1.18.1 with `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`. All test problems have \(p=3\), \(\rho=0.6\), \(s=r=1\), prior \(0.1I\), and split fraction \(0.99\). Both oracles used exactly the same stored floating-point value of \(a\) for the timed evaluations. Timing includes each method's value and full gradient; setup is reported separately.

| Candidates \(n\) | Dense evaluation | Structured evaluation | Dense / structured | Dense setup | Structured setup |
|---:|---:|---:|---:|---:|---:|
| 48 | 36.9 µs | 45.6 µs | 0.81 | 0.187 ms | 0.089 ms |
| 96 | 76.6 µs | 48.6 µs | 1.58 | 0.459 ms | 0.131 ms |
| 512 | 3.928 ms | 89.8 µs | 43.7 | 13.86 ms | 0.312 ms |
| 2048 | 758.6 ms | 175.0 µs | 4335 | 981.3 ms | 0.935 ms |

Evaluation times are medians of 9 dense and 101 structured calls, cycling through four deterministic interior random points after warm-up. Setup times are single observations. These are local timings on a shared machine, not end-to-end solver speedups. At \(n=48\), the structured Python/SciPy overhead is larger than the small dense solve. At large \(n\), the dense solve is an avoidable bottleneck. The existing design comparisons at small \(n\) may still be dominated by master optimization and relaxation strength; a complete solve comparison is needed to distinguish those costs.

Validation passed 291 comparisons with the dense oracle, 216 binary true-objective comparisons, 72 central directional-derivative checks, four malformed-input rejections, and one exact rational three-observation identity containing both zero and nonzero selection weights. The main edge-case sweep had maximum absolute value error \(1.14\times10^{-13}\), gradient error \(2.90\times10^{-12}\), and scaled directional-derivative error \(2.80\times10^{-8}\). Additional near-unit correlations and a latent variance of \(10^{-12}\) passed their stated tolerances. These checks validate numerical agreement in the tested domain, not exact floating-point upper tangents.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/structured_dense_oracle.py
```

## 6. Prior art and implications

[Rybicki and Press (1995)](https://arxiv.org/pdf/comp-gas/9405004), equations (13), (17), and (18), already combine latent tridiagonal precision with diagonal measurement noise for fast filtering and generalized least squares. Their treatment includes missing measurements through zero precision weights. This is direct prior art for the core solve, not merely a distant analogy.

[Foreman-Mackey et al. (2017)](https://arxiv.org/html/1703.09710) develops exact semiseparable covariance calculations for mixtures of exponentials and nonuniform independent measurement noise. It supplies broader structured-covariance implementation context. Both sources were sent to the shared literature agent for the local knowledge base.

The contribution here is to strengthen the existing comparator and remove an implementation bias. The algebra extends to any SPD sparse latent precision: adding \(DW^{-1}\) preserves its sparsity pattern, though factorization cost depends on fill. Nothing here improves the continuous Liu relaxation or its binary optimum. Future claims about memory-truncated or path formulations should compare against this structured evaluation, retain the same split and stopping conditions, and report master-solver work separately from oracle time.
