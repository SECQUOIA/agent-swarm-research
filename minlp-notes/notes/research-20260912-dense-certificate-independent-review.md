# Independent review of the exact dense design certificates

**Verdict: accepted for the validated rational input domain.** Fresh reviewer
`dense_exact_review` found no incorrect certificate in
[`certify_dense_design.py`](../code/research_20260912/certify_dense_design.py).
The six saved certificates reproduce exactly through independent dense covariance
calculations. Their continuous relaxation lower bounds all strictly exceed the
corresponding finite-memory upper bounds for the same integer design problem.
This proves a difference in bound strength on these six instances. It does not
establish a general ordering of the relaxations or a comparison of complete
mixed-integer solvers.

The reviewed source SHA-256 is
`0bb28391c819a6463d573e44f09790fc069986b062f31c3bc0de51c1f11d2f17`.
The reviewer did not modify the certificate implementation or run its author
validation as the independent check. The separate
[review script](../code/research_20260912/review_dense_certificate_independent.py)
and [saved report](../code/research_20260912/results/dense-certificate-independent-review.json)
record the checks, input hashes, exact differences, and implementation hashes.

## Certificate argument

For rational data, the implementation verifies that the covariance split
\(S=R-aI\) is positive definite. With positive latent variance, the scaled
precision \(M\) is SPD for \(|\rho|<1\), and
\[
R-aI=M^{-1/2}\{s(1-\rho^2)I+(r-a)M\}M^{-1/2}.
\]
Exact positive tridiagonal LDL pivots therefore prove the required split
condition. The one-observation and zero-latent-variance cases use the appropriate
diagonal conditions. A positive factorization of the structured oracle's solve
alone would not prove the split condition; this implementation performs the
separate necessary check.

For any \(z\in[0,1]^n\), let \(A=\{i:z_i>0\}\). The independent reference uses
\[
B=R_{AA}+\operatorname{diag}_{i\in A}\{a(1/z_i-1)\},\qquad
J(z)=J_0+F_A^TB^{-1}F_A.
\]
It forms this dense covariance directly, without using a latent precision or a
Kalman recursion. With \(X=B^{-1}F_A\), it recovers
\(V=F-S_{:A}X\) and the exact gradient
\(g_i=V_iJ(z)^{-1}V_i^T/a\). This also checks zero selection coordinates.
The empty active set gives \(J=J_0\) and \(V=F\).

The split establishes matrix concavity of \(J(z)\) and concavity of
\(\log\det J(z)\). Hence the rational tangent price
\[
U=\overline{\log\det J(z)}+\sum_{i\in T}g_i-g^Tz,
\]
where \(T\) contains the \(k\) largest gradient entries, is a valid upper bound
over the cardinality simplex and its binary points. A tangent point need not
satisfy the cardinality equality for this upper bound. The implementation only
reports its logarithm as a continuous lower bound when its exact coordinate sum
equals \(k\). Coordinate bounds are checked separately. Thus neither SLSQP's
success flag nor a numerical objective value enters certificate validity.

Every reported integer incumbent has exactly \(k\) distinct valid indices. Its
information is recomputed using the true selected covariance, and the candidate
with the largest exact determinant is retained. The prior is required to be SPD.

The imported logarithm routine was previously reviewed. This review additionally
enclosed each tested logarithm using a separate rational implementation with
160-bit dyadic rounding and 80 terms of the atanh series, with an explicit tail
bound. Its narrower intervals lie within every reported logarithm interval.

## Independent checks

The small cases use one, two, three, and five observations, signed and zero
correlations, correlations within \(10^{-12}\) of either endpoint, zero or
positive latent variance, non-diagonal positive priors, and selection coordinates
at zero, one, and fractional values. They passed:

- 120 exact information, gradient, and determinant comparisons against dense
  covariance calculations;
- 120 direct dense split classifications, including invalid and boundary splits;
- 160 binary-information identities and 160 exhaustive binary tangent comparisons;
- 40 additional fractional feasible-point tangent comparisons;
- 80 independent logarithm interval checks;
- 40 exact feasible rounding checks and off-cardinality lower-bound suppression
  checks;
- 36 malformed-input rejections, including invalid priors, covariance parameters,
  cardinalities, dimensions, non-exact numeric inputs, coordinates, and incumbents;
- six symbolic log-determinant derivative comparisons, including boundary points.

For each saved 48- or 96-observation certificate, the reviewer independently
recomputed the full exact information matrix, every gradient entry, and the
incumbent determinant using dense SymPy linear solves. The saved split factor was
reconstructed exactly, its pivots were checked positive, and its matrix was
checked against the dense covariance identity above. The top-\(k\) price, tangent
gap, upper-bound arithmetic, and all logarithm enclosures were also checked.

## Certified separation on the six saved instances

Both certificate families use exact rational interpretations of the same JSON
decimals. Their stored model data agree entry by entry, and every source input
hash equals
`a4031996b345b2f3898979c887b49722bda2db8d7564ffedaebddcbaa92359f6`.
The dense split is the saved exact rational value near
\(0.99\lambda_{\min}(R)\), independently verified admissible. The finite-memory
certificates use eight calendar steps. All instances have three parameters,
\(k=n/3\), \(\rho=0.4\), unit latent and nugget variances, and prior \(0.1I\).

| Candidates | Seed | Dense continuous lower minus memory upper | Dense continuous certificate gap |
|---:|---:|---:|---:|
| 48 | 0 | 0.0504253794944362 | 1.110e-7 |
| 48 | 1 | 0.0382385580688331 | 6.467e-8 |
| 48 | 2 | 0.0486269392419421 | 8.377e-8 |
| 96 | 0 | 0.0415512733242398 | 1.611e-7 |
| 96 | 1 | 0.0243044516948271 | 6.624e-8 |
| 96 | 2 | 0.0288311330780562 | 3.528e-7 |

These comparisons use exact rational differences; the table is a decimal
display. The finite-memory upper-bound algorithm and its theory were reviewed
separately in the
[memory certificate review](research-20260912-noisy-exact-independent-review.md).
This review checks the matching artifacts and the strict inequalities, and does
not claim to be a second independent reconstruction of the memory dynamic program.

Because each dense lower bound is attained by a feasible fractional design, no
more accurate optimization of that same continuous relaxation can reduce its
optimum below the displayed memory upper bound. Integer branching or additional
valid inequalities can still strengthen a dense mixed-integer solve. These six
instances do not support a universal dominance or novelty claim.

## Scope and reproduction

The command-line path constructs problems through `Problem.read`, which validates
the stated model domain. Direct construction of the dataclass is an internal
convention and does not itself validate its fields. The exact certificate core
remains independent of numerical tangent construction. The numerical proposal
can fail for extreme representations, or its rounded split can fail the exact
SPD test; these failures stop certificate generation. They do not produce false
certificates. The near-unit-correlation floating-point defect documented in the
[structured oracle note](research-20260912-structured-dense-oracle.md) does not
affect the exact rational calculations reviewed here.

Reproduce the independent checks with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_dense_certificate_independent.py
```

No additional literature was identified in this implementation review.

The later four chemical-kinetics artifacts received a separate
[exact replay and identity check](research-20260912-kinetics-dense-certificate-review.md)
with the same unchanged core.
