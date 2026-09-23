# Independent review of the covariance-space Liu oracle

Date: 2026-09-12. Reviewer: `/root/noisy_solver_review`, separate from the
implementation author. The final covariance-innovation and reverse-adjoint
implementation passes the mathematical and bounded numerical checks described
below. Review found and helped repair two issues in the initial covariance
implementation. No new relaxation, filtering algorithm, exact floating-point
certificate, or mixed-integer performance result is established.

The reviewed source is
[covariance_dense_oracle.py](../code/research_20260912/covariance_dense_oracle.py),
SHA-256 `db32a250b9d7313c0d71264860849512c77d3bba7ae06794de2fbbe58b35ce2d`.
The [independent verifier](../code/research_20260912/review_covariance_dense_oracle.py)
and [report](../code/research_20260912/results/covariance-dense-oracle-independent-review.json)
record the inputs, old and repaired outputs, reference comparisons, hashes and
package versions. The implementation author made the core changes; the reviewer
proposed and checked the reverse-adjoint repair and wrote the separate verifier.

The target is the established fixed-split Liu objective. For stationary latent
covariance `K_ij=P rho^|i-j|`, observation covariance `R=K+r I`, valid split
`0<a<lambda_min(R)`, and `D=diag(z/a)`, it is

```text
V = [I+(R-a I)D]^(-1) F,
J = prior + F^T D V,
phi = logdet J,
gradient_i = V_i J^(-1) V_i^T / a.
```

The prior is positive definite and the mean sensitivities and covariance are
fixed. The covariance-space implementation evaluates the same function and
gradient. The [author derivation](research-20260912-covariance-dense-oracle.md)
attributes the filtering and matrix identities to established work. This
review identified no additional literature requiring acquisition.

An independent reference follows from the active virtual covariance. Let
`A={i:z_i>0}` and

```text
C = K_AA + diag(r+a(1-z_i)/z_i : i in A),
B = C^(-1) F_A.
```

Then `J=prior+F_A^T B`. For active rows, `V_i=(a/z_i) B_i`; for zero-weight
rows, `V_i=F_i-K_iA B`. The reviewer computes these matrices directly with
100–400 decimal digits, rather than using a Kalman or smoothing reference.
Using `(a/z_i) B_i` on active rows also avoids cancellation in that independent
high-precision calculation. Every input float is interpreted as its exact
binary value before the high-precision operations. These computations are
strong numerical comparisons, not interval bounds.

The forward information calculation is correct. With predicted latent mean
`m_i`, predicted variance `P_i`, innovation `e_i=F_i-m_i`, and

```text
beta_i = a(1-z_i)+r z_i,
q_i = P_i z_i+beta_i,
w_i = z_i/q_i,
```

the ordinary innovation factorization gives
`J=prior+sum_i w_i e_i^T e_i`. The implementation forms this as a Gram matrix
of rows `sqrt(w_i)e_i`. Its variance update multiplies by the positive ratio
`beta_i/q_i`. At a zero weight the mean update is skipped exactly, the
information contribution is zero and no infinite virtual variance is formed.

The initial implementation obtained `V` from Rauch–Tung–Striebel smoothed
latent means using `V_i=a(F_i-m_i_smoothed)/beta_i`. This identity is correct
in exact arithmetic. However, the subtraction is poorly conditioned when
the latent-to-noise variance ratio is large, and multiplication by `a/beta_i`
can magnify its error.

The concrete new review witness has

```text
n=3, p=1, F=(1,2,-1)^T, rho=0.5,
r=1, prior=1/P, z=(1,1,1), split_fraction=0.5.
```

At `P=1e20`, the initial covariance oracle returned gradient `(0,0,0)`.
The high-precision reference is approximately
`(9.72e-42, 0.2187793920, 0.1400188109)`. At `P=1e30`, its first gradient
entry was approximately `2.426997786e26`, whereas the reference was
`9.72e-62`. Its log determinant still agreed to displayed double precision.
Thus objective agreement alone did not validate its tangents.

This latter discrepancy produces an actual invalid binary cut. Evaluate the
initial tangent from `z=(1,1,1)` at the size-two design `(0,1,1)`. Its
underestimation of the candidate objective is approximately `2.427e26`.
The verifier reconstructs that failure by importing the archived
[initial source](../code/research_20260912/results/covariance-dense-oracle-rts-initial-source.txt),
whose hash is
`a0cf6289d9583d5b700d44cdcfe27c4633b7c9a561f5d7ae8d33525c3f4dd2f8`.
The original author report is also
[preserved](../code/research_20260912/results/covariance-dense-oracle-rts-validation.json).
That earlier report had passed its tested domain; the present counterexample
lies outside its variance-ratio tests.

The repair reverses the innovation quadratic directly. For one column of
`F`, consider `Q(F)=1/2 sum_i w_i e_i^2`. The forward mean recursion is

```text
m_(i+1) = rho[(1-P_i w_i)m_i+P_i w_i F_i].
```

Writing `b_i` for the negative derivative of the remaining quadratic with
respect to `m_i`, the chain rule yields

```text
b_n = 0,
b_i = w_i e_i + rho(1-P_i w_i)b_(i+1),
dQ/dF_i = w_i[e_i-rho P_i b_(i+1)].
```

Since `dQ/dF=DV`, and `1-P_i w_i=beta_i/q_i`, the stable reverse evaluation is

```text
V_i = (a/q_i)[e_i-rho P_i b_(i+1)],
b_i = w_i e_i + rho(beta_i/q_i)b_(i+1).
```

For positive weights this follows by cancelling `z_i/a`. Every expression
in the final recursion is continuous at `z_i=0`, as is the original
resolvent, which proves the zero-weight extension. Applying the argument
columnwise handles all sensitivity right-hand sides. The reviewer checked
222 exact rational identities for both `V` and the innovation information
matrix, against direct inversion of the defining resolvent. These cover
`n=1,3,4`, correlations `-3/5,2/3`, and every selection vector in
`{0,1/2,1}^n`.

There is a useful exact-arithmetic explanation for the new scale. The
conditional variance `P_i+r` is the minimum variance of a residual formed
from the current observation and past observations with added nonnegative
virtual noise. For any coefficients `c`, the original covariance contributes
at least `lambda_min(R)*(1+||c||^2)`, and the added noise cannot reduce this.
Therefore `P_i+r>=lambda_min(R)>a`, which gives

```text
q_i=a(1-z_i)+(P_i+r)z_i >= a,
0<a/q_i<=1,
|rho beta_i/q_i|<=|rho|.
```

Equality `q_i=a` occurs at a zero weight. These relations remove the previous
`a/beta_i` amplification. They do not constitute a complete error analysis
of all floating-point operations.

The second review issue concerned process-variance arithmetic. Evaluating
`P*(1-rho)*(1+rho)` left to right can overflow its first product for negative
correlation even though `P*(1-rho^2)` is finite. With `P=1e308`, `rho=-0.9`,
unit observation noise and two candidates, the initial implementation failed;
the correct process variance is approximately `1.9e307`. The repaired code
forms the factor `(1-rho)*(1+rho)<=1` first and then multiplies by `P`.
Both signs of correlation now agree with a 400-digit covariance reference in
this finite-range test.

Boundary handling and denominator signs are consistent with the model.
`P=0`, `rho=0` and `n=1` use the correct diagonal formulas. The singleton
covariance is `P+r` regardless of correlation. At `z=0`, the result is
`J=prior`, `V=F`, with a generally nonzero gradient. An admissible split can
exceed `r`; `beta=a(1-z)+r z` remains positive because it is evaluated as a
positive sum. Negative correlation affects the signed mean and adjoint
recursions without changing variance positivity. Shape, finite-value, domain
and split checks reject malformed inputs.

The oracle reuses the structured implementation's constructor for the
numerical minimum-eigenvalue and split setup. It does not call that
implementation's unreliable precision-space objective or gradient method.
The reused constructor also builds some unused linear-size precision data;
this does not change the function evaluated or the claimed asymptotic memory
order. The split test is numerical, so an exact tangent still requires a
separately validated split and arithmetic.

The final independent run completed in about 3.1 seconds with one BLAS thread.
It used Python 3.13.11, NumPy 2.5.3, SymPy 1.14.0 and mpmath 1.3.0. Its
checks comprise:

| Check | Count |
| --- | ---: |
| Direct high-precision ordinary-domain comparisons | 240 |
| Binary selected-covariance objectives | 130 |
| Cases with boundary gradients | 160 |
| Gradient finite-difference directions | 40 |
| Ordinary numerical tangent comparisons | 160 |
| Exact rational adjoint and information identities | 222 |
| Extreme variance-ratio and mixed-weight cases | 42 |
| Covariance/prior scale-invariance checks at `1e-200,1e200` | 2 |
| Finite-range process-variance checks at `P=1e308` | 2 |
| Saved near-unit-correlation witness replays, both signs | 24 |
| Binary designs checked per near-unit sign | 495 |
| Malformed input rejection checks | 17 |

The greatest ordinary value discrepancy was `1.33e-15`, scaled gradient
discrepancy `1.38e-15`, and scaled derivative discrepancy `3.12e-11`.
The 42 extreme cases include latent-to-noise ratios through `1e100`, and
combine `P/r=1e30` with correlations immediately adjacent to both `1` and
`-1`. Their greatest scaled gradient discrepancy was `5.56e-16`.
Here a scaled gradient error divides each absolute error by
`max(1,abs(reference_entry))`; it is not a relative-accuracy claim for tiny
gradient entries.

The original precision-coordinate counterexample also reproduces. At the
nearest float below positive unit correlation, its tangent cuts off 37 of
495 size-four designs, with maximum underestimation `0.8478641735`. The
repaired covariance-adjoint tangent violates none at tolerance `1e-10`; its
smallest measured slack is `0.2639024664`. For the corresponding negative
correlation, the precision tangent violates nine designs, while the repaired
tangent violates none and has smallest measured slack `0.3147650748`.
Every candidate objective in these fresh comparisons is independently
evaluated with the high-precision active covariance reference.

The repairs remove these demonstrated errors, but floating-point tangents
are still not exact global certificates. On the new `P=1e30` witness, for
example, a gradient entry whose reference value is approximately `1e-61`
can still be returned around `1e-34`. This is negligible in the tested
absolute comparisons and has poor relative accuracy. Extreme arithmetic,
ill-conditioned information matrices and small residuals remain relevant
limitations. The separate
[exact dense-design certifier](research-20260912-exact-dense-design-certificates.md)
remains the authority for exact certificate claims.

No MIP or independent timing benchmark was run in this review. The author's
updated component benchmark reports that the Python covariance loops are
slower at small `n` and faster at large `n`; its latest 2,048-candidate ratio
is about 69, rather than the approximately 92 from the initial RTS version.
Those measurements do not establish an end-to-end mixed-integer speedup.

Reproduce the independent review from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/review_covariance_dense_oracle.py
```
