# Independent review of certificates covering every scalar split

**Verdict: accepted.** Fresh module reviewer `dense_exact_review` independently
checked [`certify_all_splits.py`](../code/research_20260912/certify_all_splits.py),
its argument, and all six saved certificates. For each recorded instance, the
continuous Liu relaxation optimum exceeds the finite-memory upper bound for
**every admissible scalar split** \(0<a<\lambda_{\min}(R)\). The exact positive
separations range from 0.0227620 to 0.0472161 in log-determinant objective.

This strengthens the earlier
[fixed-split review](research-20260912-dense-certificate-independent-review.md).
It rules out scalar split tuning as an explanation for the observed bound
separation. It does not cover other relaxation families, arbitrary diagonal
splits, additional valid inequalities, or complete mixed-integer solution times.
No new theorem or literature priority claim is made for the monotonicity argument.

The reviewed source SHA-256 is
`27a1977f6c7ba51aa64207a71bfe0b508c21aa1b7d3a14bf75e37da1b15bcf14`.
The [independent script](../code/research_20260912/review_all_splits_independent.py)
and [saved report](../code/research_20260912/results/all-splits-independent-review.json)
record exact values and hashes. The reviewer did not change the author code and
did not use the author's validation results as independent evidence.

## Why one point certifies every admissible scalar split

Let \(R\succ0\), \(J_0\succ0\), and
\(Z=\{z\in[0,1]^n:\sum_i z_i=k\}\). For a fixed \(z\in Z\), let
\(A=\{i:z_i>0\}\). For every positive scalar \(a\), define
\[
B_a(z)=R_{AA}+a\operatorname{diag}_{i\in A}\left(\frac{1-z_i}{z_i}\right),
\qquad J_a(z)=J_0+F_A^TB_a(z)^{-1}F_A.
\]
For an empty active set, \(J_a(z)=J_0\). Otherwise \(B_a(z)\succ0\), because
the added diagonal matrix is PSD. Thus this point value exists even when
\(a\) exceeds \(\lambda_{\min}(R)\).

If \(0<a\le b\), then \(B_a(z)\preceq B_b(z)\), so
\(J_a(z)\succeq J_b(z)\) and
\(\log\det J_a(z)\ge\log\det J_b(z)\). For any certified
\(\bar a\ge\lambda_{\min}(R)\), it follows that
\[
\max_{w\in Z}\log\det J_a(w)
\ \ge\ \log\det J_a(z)
\ \ge\ \log\det J_{\bar a}(z)
\ \ge\ \underline{\log\det J_{\bar a}(z)}
\quad\text{for every }0<a<\lambda_{\min}(R).
\]
The last quantity is the reported rational lower bound. The proof needs exact
feasibility of \(z\), an upper bound on the smallest covariance eigenvalue, and
an exact point evaluation with an outward logarithm bound. It does not need
optimization at \(\bar a\), concavity at \(\bar a\), or any tangent at
\(\bar a\). The implementation correctly keeps these distinctions.

## Spectral upper-bound witness

For positive latent variance and at least two candidates, write
\(R=rI+s(1-\rho^2)M^{-1}\), with the usual SPD scaled AR(1) precision \(M\).
The matrix
\[
G_{\bar a}=s(1-\rho^2)I+(r-\bar a)M
\]
is congruent to \(R-\bar aI\). Its failure to be SPD proves
\(\lambda_{\min}(R)\le\bar a\).

The code identifies the first nonpositive exact LDL pivot. Every earlier pivot
is positive, so the relevant leading determinant is the product of a positive
prefix and the nonpositive pivot. Sylvester's criterion establishes failure of
positive definiteness, including a zero pivot. The code stops before dividing
by that pivot. One candidate and zero latent variance receive their appropriate
diagonal formulas.

The numerical eigenvalue estimate is only a proposal. The routine rounds upward
and makes finitely many small adjustments until the exact witness succeeds.
Failure to find a witness raises an exception. An inaccurate proposal cannot
create a false spectral assertion.

The independent small tests compare this classification with direct leading
principal minors of the dense covariance. For the saved large cases, the reviewer
also computed the exact dense determinants of \(R-\bar aI\) without using the
precision representation or the LDL routine. Both distinct covariance/split
matrices have negative determinants, directly proving they are not SPD. The saved
LDL factors were separately reconstructed exactly. This checks the spectral
claim through two different calculations.

## Independent results

All 360 small point evaluations matched independently constructed dense
covariances with their added virtual noise. These include signed correlations
within \(10^{-12}\) of either endpoint, zero correlation, zero latent variance,
one through six candidates, three parameters, non-diagonal positive priors, zero
and unit weights, and positive weights as small as \(10^{-20}\).

Further checks passed:

- 240 information monotonicity comparisons, with PSD checked through every
  principal minor of the exact matrix difference;
- 120 spectral upper-bound classifications against dense covariance matrices;
- 80 comparisons between all-splits lower bounds and exact point values at
  admissible smaller splits;
- 50 failed-pivot witnesses reconstructed from exact leading determinants of
  independent test matrices;
- 20 malformed input or impossible proposal rejections;
- the exact two-candidate example with an all-splits information lower bound
  of \(2\), versus integer information \(3/2\).

For each saved certificate, the independent dense calculation reproduced the
information matrix and determinant exactly. A separate rational logarithm
enclosure lies inside the saved interval. The fractional point is exactly
cardinality feasible. The dense input certificate hash, exact model data,
matching memory certificate hash, and exact subtraction all agree.

| Candidates | Seed | All-splits lower minus memory upper |
|---:|---:|---:|
| 48 | 0 | 0.0472161421013502 |
| 48 | 1 | 0.0359356454160979 |
| 48 | 2 | 0.0463902777717963 |
| 96 | 0 | 0.0391345532281320 |
| 96 | 1 | 0.0227620218446652 |
| 96 | 2 | 0.0263512732265613 |

The table displays decimal approximations of positive rational differences. The
memory upper bounds retain the assumptions and independent verification in the
[memory certificate review](research-20260912-noisy-exact-independent-review.md).
This review checks those artifacts and their identity with the present models;
it does not rerun the memory dynamic-programming verifier.

The command-line path validates model data through `Problem.read`. As in the
fixed-split module, direct dataclass construction is an internal convention that
does not itself validate fields. The optional memory comparison consumes a saved
certificate and records its hash; its correctness presupposes a valid memory
certificate. The six artifacts used here were matched to the previously reviewed
ones. No false certificate was found for valid inputs.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_all_splits_independent.py
```

No additional literature was identified in this module review.

The later four chemical-kinetics artifacts received a separate
[exact replay and identity check](research-20260912-kinetics-dense-certificate-review.md)
with the same unchanged core.
