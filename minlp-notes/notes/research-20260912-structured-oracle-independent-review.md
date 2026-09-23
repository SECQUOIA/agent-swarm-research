# Independent review of the structured Liu oracle

**The algebra is correct, and the ordinary test domain passed. The floating-point implementation has a material limitation near unit latent correlation: it can return an inaccurate value and gradient even when the observation covariance is well conditioned.** A resulting numerical outer-approximation cut can underestimate a feasible binary objective. This limitation does not apply to a tangent recomputed and checked in exact arithmetic.

This fresh review examined [structured_dense_oracle.py](../code/research_20260912/structured_dense_oracle.py), its [derivation](research-20260912-structured-dense-oracle.md), and the existing `DenseLiuOracle` in [noisy_markov_design.py](../code/research_20260912/noisy_markov_design.py). It did not modify author code. The reviewed structured source hash is `f835c8e1fe2d5757b15e9806ad48e10e505ff61cbd8af1838ea01df6bec36769`. The [independent script](../code/research_20260912/review_structured_dense_oracle.py) and [saved report](../code/research_20260912/results/structured-dense-oracle-independent-review.json) retain source hashes, environment, checks, and numerical witnesses.

## Algebra and independent reference

For positive selection weights on index set \(I\), define the virtual observation covariance

\[
T_I=R_{II}+a\operatorname{diag}(1/z_I-1).
\]

Then the information matrix is

\[
J(z)=J_0+F_I^T T_I^{-1}F_I.
\]

This is a direct covariance-space reference that avoids both the author's tridiagonal precision system and the existing dense oracle's nonsymmetric system. Zero-weight observations are absent from \(T_I\). Their derivatives use the residual sensitivity \(F_j-R_{jI}T_I^{-1}F_I\); for positive weights, differentiating \(T_I\) gives the corresponding derivative directly. Both yield the displayed gradient in the author's note. The script uses this independent reference for objective, derivative, and concavity checks.

Multiplying the original system by \(Q=K^{-1}\), then setting \(U=WV\), correctly gives

\[
(Q+DW^{-1})U=QF,\qquad
w_i=[a(1-z_i)+rz_i]/a>0.
\]

The scaled tridiagonal implementation matches this identity. The gradient \(V_iJ^{-1}V_i^T/a\) follows by differentiation, and it remains valid at zero weights. The requirement \(0<a<\lambda_{\min}(R)\) gives the stated concavity and global upper tangents. Solvability of the structured system by itself does not establish this split condition.

The cases \(n=1\), zero latent variance, zero correlation, an all-zero selection vector, negative correlation, and a valid split exceeding the nugget have the correct branches or algebra. For \(n\ge2\) and positive latent variance, the proposed exact split test

\[
R-aI\succ0\quad\Longleftrightarrow\quad
s(1-\rho^2)I+(r-a)M\succ0
\]

is correct. For one observation the condition is instead the direct scalar inequality \(a<s+r\). The prototype's numerical eigenvalue comparison is explicitly not an exact split certificate.

The stated total cost \(O(np^2+p^3)\), for a fixed split, correctly includes the information matrix and gradient work. No new algorithmic or theoretical priority is claimed for this covariance/precision conversion.

## Checks that passed

The ordinary numerical grid used \(n\in\{1,2,5,11\}\), correlations \(-0.98,-0.6,0,0.7,0.98\), latent/nugget pairs \((0,0.3),(0.001,2),(1,0.01),(1,1),(100,0.2)\), split fractions \(0.25,0.99\), and random three-column sensitivities with positive definite, generally nondiagonal priors. Selection points included all-zero, all-one, binary, interior, and mixed zero/positive weights.

| Check | Count |
|---|---:|
| Independent virtual-covariance objective and gradient comparisons | 1,000 |
| Same-split comparisons with the existing dense oracle | 1,000 |
| Binary true-objective checks | 650 |
| Fourth-order central directional derivatives of the independent reference | 200 |
| Concave tangent inequalities at other feasible points | 800 |
| Automatic split comparisons with covariance eigenvalues | 200 |
| Exact symbolic interior gradient entries | 12 |
| Exact symbolic boundary gradient entries | 48 |
| Exact symbolic objective values | 6 |
| Rational covariance/precision split-equivalence checks | 75 |
| Malformed selection or split input rejections | 19 |

Maximum absolute objective discrepancy was \(1.25\times10^{-14}\); maximum componentwise scaled gradient discrepancy was \(4.27\times10^{-14}\). The directional derivative discrepancy was below \(4.25\times10^{-11}\) after scaling by \(\max(1,|d\phi|)\). No tested concavity tangent inequality failed. These results establish numerical agreement in the stated grid, not exact upper bounds for floating-point tangents or accuracy for every accepted input.

## A material numerical limitation

The following reproducible data produce large error:

```python
n = 12
F = np.random.default_rng(492).normal(size=(12, 3))
prior = 0.1 * np.eye(3)
rho = np.nextafter(1.0, 0.0)
latent_variance = nugget_variance = 1.0
z = np.linspace(0.2, 0.8, 12)
split_fraction = 0.99
```

The observation covariance has condition number approximately 13, yet the structured oracle's objective error is about \(-0.628\), with maximum gradient error about 1.14. The direct covariance calculation agrees with an independent 90-digit calculation to within \(5\times10^{-13}\). The saved report contains the complete input arrays, split, high-precision references, and output errors.

The inaccurate tangent has an observable consequence for cardinality-four design. For the zero-based selected set \(\{1,6,7,8\}\), the true objective is approximately 4.58889008, while this tangent gives approximately 3.74102591. It underestimates that feasible binary objective by 0.84786417. Of all 495 cardinality-four subsets, 37 violate the computed tangent by more than \(10^{-10}\). Thus a solver using such a floating-point tangent as a global upper cut can lose validity.

This is not solely a representational overflow example. At \(\rho=1-10^{-12}\), with the same other data, the objective and gradient errors are already around \(10^{-5}\) and \(10^{-4}\). With latent variance \(10^{-8}\) or \(10^{-20}\), nugget one, and the most extreme correlation above, the observation covariance is almost the identity, but the structured computation raises a linear-algebra exception.

The reason is the choice of coordinates. The tridiagonal system uses a nearly singular latent precision scaling and a right-hand side \(MF\), introducing cancellation and poor conditioning even when the original covariance with its nugget is well conditioned. Avoiding explicit division by a small latent variance does not remove this issue.

The author and root researcher were informed. The current benchmark correlations of 0.4 and 0.6 lie inside the reviewed ordinary range; this witness does not invalidate those saved comparisons. Before relying on the implementation across its full accepted input range, a stable covariance/filtering calculation or another justified mitigation is needed. An exact rational tangent computed independently from proposed numerical weights is a separate valid route. The review does not prescribe an untested numerical threshold or treat a generic solver tolerance as a remedy for this error.

## Reproduction

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
  code/research_20260912/review_structured_dense_oracle.py
```

The recorded environment uses Python 3.13.11, NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0, and mpmath 1.3.0. No mixed-integer benchmark or literature addition was needed for this scoped review.
