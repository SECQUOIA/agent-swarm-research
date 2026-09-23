# Priority audit: localized inverse factors and noisy Markov design

Date: 2026-09-12. This is a bounded audit of mathematical prior work for the
[finite-memory design result](research-20260912-noisy-markov-memory.md).
It does not establish publication priority. The approximation formula,
inverse-factor residual metric, localization principle, and elementary
precision-to-Fisher implication are established ideas. The two requested
sources do not directly provide the explicit chronological-window certificate.
A more general decay-algebra argument may already imply qualitative uniform
convergence; that implication needs separate review before being used.

## 1. Rubensson, Artemov, Kruchinina, and Rudberg

Source: [published author-hosted PDF](https://uu.diva-portal.org/smash/get/diva2%3A1302978/FULLTEXT01.pdf),
*Localized inverse factorization*, IMA Journal of Numerical Analysis 41
(2021), 729–763, DOI 10.1093/imanum/drz075. Inspected published §§3–5,
particularly Theorems 4.1, 5.1–5.2, and 5.6. The
[2019 preprint](https://arxiv.org/html/1812.04919v2) numbers theorems differently.

- Theorem 4.1, pp. 739–740: exact inverse factors of two principal diagonal
  blocks initialize a refinement with residual spectral norm at most
  `1-lambda_min(S)/lambda_max(S)`. Equation (4.10) bounds refinement iterations.
- Theorem 5.1, p. 741: uniform exponential entry decay and polynomial metric-ball
  growth imply a uniform bound on significant entries per row/column.
- Theorem 5.2, pp. 741–742: products preserve exponential entry decay at any
  strictly smaller exponent.
- Theorem 5.6, pp. 746–748: both the input matrix and initial block inverse
  factors must have uniform exponential decay; condition numbers must be
  uniformly bounded. Its refinement matrices retain decay, including localization
  near the partition cut. The output factor need not be triangular.

These are strong locality results. They concern different factors and require
decay of the starting inverse factors. They do not identify the finite-calendar
Vecchia factor or its explicit error constant. No Fisher-design graph or
certified schedule optimization appears in the inspected results.

The printed ball-growth assumption applies to all `R>=0`, although a ball
including its center has size at least one for arbitrarily small positive
`R`. Its proof only needs integer radii at least one. Interpreting the growth
bound for `R>=1`, or using `gamma max(1,R)^beta`, removes this minor issue.
This interpretation should be stated if applying that theorem.

## 2. Kaminetz thesis

The distinct March 2026 paper with Webber is assessed in the
[subsequent source audit](research-20260912-kaminetz-webber2026-priority-audit.md).
The counterexample below concerns the thesis only.

Source: [author-hosted PDF](https://math.ucsd.edu/sites/math.ucsd.edu/files/Eagan%20Kaminetz%20Thesis%20Final.pdf),
*Everything is Vecchia: Unifying Column Nyström and Sparse Vecchia
Approximations*, 25 pages, accessed 2026-09-12. Inspected §§2–4, especially
Theorems 3.1 and 4.1–4.3.

Theorem 3.1 identifies a low-rank-plus-sparse factor with a Vecchia sparsity
pattern. Theorem 4.1, pp. 9–10, restates the Schäfer et al. localization result:
boundary-conditioned Matérn covariance, specified half-integer smoothness,
bounded domain, reverse-maximin order, geometry-dependent constants, and
`O(log(n/epsilon)^d)` neighbors give KL and covariance-Frobenius error below
`epsilon`. The adjacent paragraph explicitly excludes nonzero nugget from
that result. Theorem 4.2, pp. 10–11, extends this framework to chosen Nyström
pivots, with constants depending on those pivots. Neither result matches our
noisy chronological-window assumptions or supplies our constants.

Theorem 4.3, p. 13, asserts a general supermodularity-based greedy guarantee
for a pivot-set KL objective. The calculation below contradicts its stated
supermodularity claim, as confirmed by fresh independent review against the
primary text. It invalidates the displayed proof. The fresh reviewer also found that the
final exponential greedy bound fails under the literal fixed-order convention;
that additional conclusion does not carry over unchanged to pivot-first CNV.
The [independent review](research-20260912-vecchia-supermodularity-independent-review.md)
separates these two statements. That bound should not be used without another
valid justification. This issue does not invalidate the
underlying Vecchia formula or the separately reviewed Markov theorem.

## 3. Exact counterexample to the thesis's supermodularity step

Use the rational covariance

```text
R = [[1,   0,   3/5],
     [0,   1,   3/5],
     [3/5, 3/5, 1  ]].
```

Its leading principal minors are `1,1,7/25`, so it is SPD. Fix order
`1<2<3`. For pivot set `I`, retain in row `j` exactly the conditioning
variables `{i in I: i<j}`, as in the theorem's displayed sparsity pattern.
Let `Q_I` be the resulting working precision and

```text
g(I) = KL[N(0,R) || N(0,Q_I^(-1))].
```

Every normalized local residual has unit variance, hence `tr(Q_I R)=3`.
Consequently `exp(2g(I))=product_j d_j(I)/det(R)`. Direct rational
conditioning gives:

| `I` | Local conditional variances | `exp(2g(I))` |
| --- | --- | ---: |
| empty | `1,1,1` | `25/7` |
| `{1}` | `1,1,16/25` | `16/7` |
| `{2}` | `1,1,16/25` | `16/7` |
| `{1,2}` | `1,1,7/25` | `1` |

Supermodularity would require
`g(empty)+g({1,2})>=g({1})+g({2})`. Instead its slack is

```text
(1/2) log(175/256) < 0.
```

The thesis's additional positive scaling of its objective does not change
this failure. The same example can be represented by reordering each pivot
set before the remaining variables: the chosen pivots here are uncorrelated,
so the table is unchanged. Thus this is not repaired by that ordering
convention. The displayed marginal identity (4.9) is not valid for this
matrix. In general, adding a pivot changes several conditional variances;
their sum of logarithms cannot be replaced by a residual logdet without an
additional independence condition.

Author verification used exact SymPy rational arithmetic to construct all
four residual maps and precisions, checked every `tr(Q_I R)=3`, and obtained
the table and `175/256` exactly. Numerical approximation is unnecessary for
the sign because `175<256`.
The fresh reviewer independently reconstructed the rational matrices and
checked the thesis's definitions and inequality (4.10). The ordering-independent negative result is the asserted supermodularity
and associated proof. The independent review separately records the stronger
fixed-order failure of the final approximation ratio.

## 4. Stronger prior at the qualitative level

[Krishtal, Strohmer, and Wertz](https://math.ucdavis.edu/~strohmer/papers/2013/matrixfactorization.pdf),
*Localization of Matrix Factorizations*, DOI 10.1007/s10208-014-9196-x,
provides a broader framework. Inspected the 2013 preprint's Definition 2.3,
Theorem 2.4, and Corollary 5.1, pp. 4–5 and 12. Corollary 5.1 gives Cholesky
inheritance in strongly decomposable inverse-closed matrix algebras satisfying
its embedding assumptions. Inverse closure then controls inverse factors.
Its examples include polynomial and stretched-exponential decay. Admissible
weights satisfy the GRS condition; a fixed exponential weight fails that
condition. One must not silently infer preservation of the identical
exponential rate from this corollary.

[Benzi and Tůma](https://www.cs.emory.edu/~benzi/Web_papers/bt.pdf),
*Orderings for factorized sparse approximate inverse preconditioners* (2000),
Theorem 4.1, pp. 1857–1858, directly bounds inverse-Cholesky entries for an SPD
band matrix with normalized diagonal. Its constants depend on bandwidth and
extreme eigenvalues. Our noisy observation covariance is generally dense, so
that theorem alone is not the desired application. Benzi, Boito, and Razouk,
DOI 10.1137/100814019, was also routed as a relevant general matrix-decay
source; its strongest applicable result was not fully audited here.

The following is a historical implication considered in this audit. Its
direct-sum/factorization-inheritance route was not established or independently
reviewed, and no further work on that route is part of the closed continuation.
Whiten scalar observation noise and embed each selected covariance in the
calendar grid by making omitted coordinates independent unit variables.
Writing `b=Pbar/rmin`, every such matrix `A_S` satisfies

```text
I <= A_S <= [1+b(1+rho)/(1-rho)]I,
|(A_S)_ij| <= b rho^abs(i-j),    i != j,
(A_S)_ii <= 1+b.
```

These inequalities follow directly from noise positivity and the covariance
row sum. They hold uniformly for all horizons and subsets. A block-diagonal
direct sum over the countable collection of all finite subsets therefore
defines one bounded, uniformly positive infinite matrix in every polynomial
decay algebra. Applying factorization inheritance to that operator is a route
to uniform inverse-Cholesky tail decay across the entire collection.

A further transfer is still needed: the local Vecchia factor reoptimizes each
regression; it does not simply truncate the exact inverse factor. Local
least-squares optimality bounds each row's prediction error by that of a
truncated full-history predictor. Uniform eigenvalue bounds convert this to
coefficient error. Combining the window's finite bandwidth with factor-tail
decay can then control both row and column sums. This is a plausible route to
qualitative `sup_(n,S)||C_L(S)-I||_2 -> 0`, with weaker or implicit rates.
This transfer/direct-sum argument has not undergone fresh independent review
and is not asserted here as a completed theorem. The later
[general-covariance result](research-20260912-general-covariance-memory-bound.md)
and its [independent review](research-20260912-general-covariance-memory-independent-review.md)
give an explicit local-regression proof under their stated decay and positive
covariance assumptions. The separate Kaporin metric example and pair-bound
refinements do not prove this historical direct-sum argument.

Thus the broad existence of uniform local precision approximations should not
be advertised as a new principle. The specific reviewed result supplies an
explicit rate, constants based on the noise and contraction bounds, and a
particular finite-state optimization model. Whether that combination is a
substantial contribution still depends on deeper priority review and practical
performance. A generic precision residual certificate yields Fisher and
logdet bounds by elementary congruence and monotonicity; that implication
itself is not new.

## 5. KL bounds already imply relative Fisher bounds

The difference between a KL guarantee and a relative information guarantee
must not be overstated. For any SPD covariance `R` and working precision `Q`,
let `lambda_j` be the eigenvalues of `R^(1/2) Q R^(1/2)`. Direct evaluation of
the Gaussian KL divergence gives

```text
2 KL[N(0,R) || N(0,Q^(-1))]
  = sum_j [lambda_j-log(lambda_j)-1].
```

Every summand is nonnegative. If the KL divergence is at most `epsilon`,
each eigenvalue lies between the two positive roots of
`x-log(x)-1=2epsilon` (with both roots equal to one at zero error).
Consequently a global KL guarantee gives a relative precision sandwich and,
by congruence, a relative mean-Fisher sandwich without a sensitivity-norm
assumption. This calculation is elementary and does not require a new theorem.

The relevant distinctions from the inspected KL results are the permitted
noise/model assumptions, the chronological calendar window, explicit constants,
and a window length independent of the horizon. The earlier
`log(n/epsilon)` neighborhood bounds cannot simply be called uniform in `n`.
Conversely, our spectral guarantee permits total KL error to increase with
the number of observations; it does not prove a uniformly bounded total KL
error at fixed `L`.

## 6. Retrieval and audit record

The published Rubensson PDF was downloaded with the approved direct `lit.py
get` command to `/tmp/research-20260912-localized-inverse.pdf`; the path was
sent to the sole maintenance agent. The thesis and additional sources were
read from primary author or repository pages. Further queries included
`"Localized inverse factorization" arxiv`, `Benzi Boito Razouk 2013 theorem
9.2 inverse Cholesky decay dense matrix`, and `"Localization of Matrix
Factorizations"`. All identified missing sources were routed to
`/root/literature`; no knowledge-base files were edited by this audit.
