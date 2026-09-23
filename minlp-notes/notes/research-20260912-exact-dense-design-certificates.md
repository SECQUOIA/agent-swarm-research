# Exact Liu relaxation certificates and a certified bound comparison

**Status: [accepted by fresh independent review](research-20260912-dense-certificate-independent-review.md) for the validated rational input domain. No originality claim.** The [certificate generator](../code/research_20260912/certify_dense_design.py) is separate from the reviewed optimization code. It uses exact decimal input from [the extended benchmark](../code/research_20260912/results/noisy-markov-extended-benchmark.json). All six certificates, including rational witnesses and source hashes, are retained in [dense-design-exact-certificates.json](../code/research_20260912/results/dense-design-exact-certificates.json).

This is a useful competing bound: the same continuous Liu relaxation can be evaluated and certified cheaply by structured exact arithmetic. In the six cases below, its remaining gap is much larger than the uncertainty in the continuous optimum. Moreover, its continuous lower bound exceeds a separately certified upper bound on the true integer problem. The comparison therefore does not depend on assuming that the saved integer incumbent is optimal.

## Certificate construction

Use the notation and derivation in [the structured oracle note](research-20260912-structured-dense-oracle.md): \(R=K+rI\), \(K_{ij}=s\rho^{|i-j|}\), \(J_0\succ0\), and \(0<a<\lambda_{\min}(R)\). The generator interprets every JSON decimal as an exact rational. It proposes a rational \(a\) near \(0.99\lambda_{\min}(R)\), rounded down to a grid of spacing \(10^{-12}\). Positive pivots in the exact tridiagonal factorization of \(cI+(r-a)M\) certify the split. Zero latent variance is handled directly. A failed exact split check aborts the certificate.

No continuous tangent point was saved in the source benchmark. SLSQP therefore proposes a point on \(\{z\in[0,1]^n:\sum z_i=k\}\), using the structured numerical oracle. The point is rounded to rational coordinates on a \(10^{-8}\) grid, and exact integer adjustments preserve the cardinality equality. Solver success is recorded, but it is not a premise of the certificate.

At that rational point, exact tridiagonal solves give \(J\) and the gradient

\[
g_i=\frac1aV_iJ^{-1}V_i^T.
\]

Since the log determinant objective \(\phi_a\) is concave for the verified split,

\[
\max_{x\in[0,1]^n,\,\sum x_i=k}\phi_a(x)
\le \phi_a(z)+\sum_{i\in I_k(g)}g_i-g^Tz,
\tag{1}
\]

where \(I_k(g)\) contains \(k\) largest exact rational gradient entries. The implementation imports the independently reviewed rational logarithm enclosure from [certify_noisy_markov.py](../code/research_20260912/certify_noisy_markov.py) to bound \(\log\det J\) outward. Thus (1), including its intercept, is a rigorous rational upper bound. The log determinant's lower enclosure at the feasible reference gives a continuous lower bound. Their difference is the exact first-order gap plus the tiny logarithm enclosure width.

A tangent point need not satisfy \(\sum z_i=k\) for (1) to hold. The reusable certificate function permits that case but reports no continuous lower bound from an infeasible point. Every automatically generated point in the six-case run is exactly feasible. The integer lower bound is recomputed by exact selected-observation Kalman information for every distinct saved incumbent, choosing the largest exact determinant. Numerical objective labels in the input do not select the best incumbent.

The floating structured prototype has a known instability near unit correlation. That affects its usefulness as a point generator, not the validity of an issued exact certificate: the split, point feasibility, information, gradient, pricing, and logarithm bounds are all recomputed exactly. A numerical failure can prevent generation; it cannot justify silently issuing a certificate. The six current cases have moderate correlation \(\rho=0.4\).

## Six-case results

The input cases use \(p=3\), \(s=r=1\), \(\rho=0.4\), and \(k=n/3\), with seeds 0–2 at each size. Every entry below is rounded for display; the rational report carries the certificate.

| \(n\) | Seed | Best incumbent lower bound | Continuous upper bound | Continuous certificate gap | Upper bound minus incumbent |
|---:|---:|---:|---:|---:|---:|
| 48 | 0 | 7.696649647 | 7.749775864 | \(1.11\times10^{-7}\) | 0.053126217 |
| 48 | 1 | 7.759257673 | 7.799368589 | \(6.47\times10^{-8}\) | 0.040110916 |
| 48 | 2 | 8.274415875 | 8.326915720 | \(8.38\times10^{-8}\) | 0.052499844 |
| 96 | 0 | 10.447760539 | 10.491146791 | \(1.61\times10^{-7}\) | 0.043386252 |
| 96 | 1 | 10.148858427 | 10.175025276 | \(6.62\times10^{-8}\) | 0.026166849 |
| 96 | 2 | 10.543974367 | 10.574587461 | \(3.53\times10^{-7}\) | 0.030613094 |

Single-thread stage times in seconds:

| \(n\) | Seed | Numerical tangent | Exact tangent and upper bound | Exact incumbent | Total case |
|---:|---:|---:|---:|---:|---:|
| 48 | 0 | 0.0155 | 0.0406 | 0.0030 | 0.0617 |
| 48 | 1 | 0.0231 | 0.0416 | 0.0028 | 0.0691 |
| 48 | 2 | 0.0188 | 0.0319 | 0.0031 | 0.0559 |
| 96 | 0 | 0.0749 | 0.1394 | 0.0051 | 0.2223 |
| 96 | 1 | 0.0723 | 0.1247 | 0.0048 | 0.2047 |
| 96 | 2 | 0.0602 | 0.1809 | 0.0049 | 0.2485 |

Total time includes parsing, exact prior checks, and split selection; output serialization is outside the per-case timer. These are observed timings on a shared machine. There are no mixed-integer solves in this run.

## Separation from the exact memory certificates

[The comparison artifact](../code/research_20260912/results/dense-memory-certified-comparison.json) records exact equality of the problem data, source certificate hashes, and rational differences. For each case the continuous Liu **lower** bound exceeds the calendar-memory \(L=8\) certificate's upper bound on the true integer objective:

| \(n\) | Seed | Memory true-objective upper bound | Liu continuous lower bound minus memory upper bound |
|---:|---:|---:|---:|
| 48 | 0 | 7.699350373 | 0.050425379 |
| 48 | 1 | 7.761129966 | 0.038238558 |
| 48 | 2 | 8.278288697 | 0.048626939 |
| 96 | 0 | 10.449595357 | 0.041551273 |
| 96 | 1 | 10.150720758 | 0.024304452 |
| 96 | 2 | 10.545755976 | 0.028831133 |

This proves a strict bound separation for the recorded rational split near fraction \(0.99\). It does not compare fully solved integer formulations, and by itself it does not quantify the strongest admissible split. [The completed all-splits extension](research-20260912-all-splits-separation.md) uses virtual-noise monotonicity to certify strict separation for every admissible scalar split in all six cases. The exact memory certificate's own mathematical assumptions remain prerequisites for either comparison.

## Four smooth kinetics cases

The same unchanged certificate generator was run on [the 48-candidate kinetics input](../code/research_20260912/results/noisy-markov-kinetics-probe.json) and [the 96-candidate input](../code/research_20260912/results/noisy-markov-kinetics-n96-probe.json), each containing fast and slow regimes. The mean is consecutive first-order \(A\to B\to C\) kinetics, with sensitivities of \(B(t)\) to \(\log A_0,\log k_1,\log k_2\). The covariance is explicitly stylized: \(s=r=0.00125\), \(\rho=0.4\), prior \(0.01I\), and \(k=n/3\). These certificates concern the saved decimal sensitivities. They do not certify the exponential mean formula as an exact rational model or establish a measured noise covariance. Holding correlation per grid interval fixed when changing \(n\) changes the physical correlation scale.

| Candidates | Regime | Best incumbent lower bound | Continuous upper bound | Continuous certificate gap | Upper bound minus incumbent |
|---:|---|---:|---:|---:|---:|
| 48 | fast | 14.948664846 | 15.070950843 | \(5.18\times10^{-7}\) | 0.122285997 |
| 48 | slow | 9.957780910 | 10.053940387 | \(6.26\times10^{-7}\) | 0.096159477 |
| 96 | fast | 16.973742738 | 17.091639197 | \(6.63\times10^{-7}\) | 0.117896459 |
| 96 | slow | 11.893877158 | 11.994494888 | \(1.29\times10^{-6}\) | 0.100617730 |

| Candidates | Regime | Numerical tangent | Exact tangent and upper bound | Exact incumbent | Total case |
|---:|---|---:|---:|---:|---:|
| 48 | fast | 0.0295 s | 0.1555 s | 0.0049 s | 0.1919 s |
| 48 | slow | 0.0437 s | 0.1425 s | 0.0036 s | 0.1916 s |
| 96 | fast | 0.1139 s | 1.0780 s | 0.0053 s | 1.2021 s |
| 96 | slow | 0.1042 s | 0.9883 s | 0.0063 s | 1.1013 s |

The outputs are [dense-design-kinetics-n48-certificates.json](../code/research_20260912/results/dense-design-kinetics-n48-certificates.json) and [dense-design-kinetics-n96-certificates.json](../code/research_20260912/results/dense-design-kinetics-n96-certificates.json), with cases 0 and 1 denoting fast and slow regimes respectively. [The exact comparison report](../code/research_20260912/results/kinetics-dense-memory-certified-comparison.json) matches all problem data and records the certificate hashes. The [all-splits note](research-20260912-all-splits-separation.md) gives the stronger comparison that removes scalar split tuning. No additional integer optimization was performed. A [separate fresh review](research-20260912-kinetics-dense-certificate-review.md) independently reproduced all four additional dense and all-splits certificates, checked model equality and hashes, and accepted the positive comparisons.

To reproduce, run the same certificate command with each kinetics input and its corresponding output path. The two all-splits outputs use those dense certificate files as inputs. Then run:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/compare_kinetics_certificates.py
```

## An exact two-candidate example

Root supplied the following useful illustration. Let \(p=1\), prior information \(j>0\), \(k=1\),

\[
R=\begin{pmatrix}v&c\\c&v\end{pmatrix},\qquad
F=(1,-1)^T,\qquad 0<c<v.
\]

Either binary choice has information \(j+1/v\). The Liu objective is symmetric in the two weights and concave, so on \(z_1+z_2=1\) it attains a maximum at \((1/2,1/2)\). At that point its information is

\[
j+\frac{2}{v-c+a},\qquad 0<a<v-c.
\]

Even the limit \(a\uparrow v-c\) retains information \(j+1/(v-c)>j+1/v\). In contrast, the exact information hull of the two feasible selections is the singleton \(j+1/v\). This is a simple relaxation-strength example, not a novelty claim about the formulation.

The test suite checks \(v=2\), \(c=1\), \(j=1\), \(a=99/100\) exactly. It uses the compatible positive-nugget model \(s=3/2\), \(r=1/2\), \(\rho=2/3\). Continuous information is \(399/199\), integer information is \(3/2\), and the exact first-order gap at the midpoint is zero.

## Validation and reproduction

[The reference verifier](../code/research_20260912/verify_dense_certificate.py) forms exact dense covariances and inverses independently of the tridiagonal code. [Its saved results](../code/research_20260912/dense-certificate-validation.json) record 8 exact tridiagonal solve comparisons, 54 information/gradient comparisons, 36 split checks, 72 enumerated tangent comparisons, two symbolic log-determinant derivatives, 48 feasible-rounding checks, seven malformed-input rejections, and the two-candidate example. These are independent computational formulations written by the implementing researcher. The subsequent [fresh-agent review](research-20260912-dense-certificate-independent-review.md) used a separate implementation, independently reproduced all six certificates and their logarithm enclosures, and accepted the stated scope.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/verify_dense_certificate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_dense_design.py code/research_20260912/results/noisy-markov-extended-benchmark.json code/research_20260912/results/dense-design-exact-certificates.json
```

The environment is the repository's isolated research project. Rational certificates can contain integer strings longer than Python's default conversion limit; the command-line tools disable that limit for these bounded research calculations. Arithmetic operation counts do not bound rational bit growth. The present \(n\le96\), \(p=3\) experiments establish practical cost only for this scale and data.
