# Independent review of the covariance-decay memory theorem

The theorem in
[`research-20260912-general-covariance-memory-bound.md`](research-20260912-general-covariance-memory-bound.md)
passes this independent mathematical review. Off-diagonal block covariance
decay and a uniform positive lower eigenvalue bound suffice for the stated
finite-window relative precision estimate. The proof does not require an
upper bound on the diagonal covariance blocks. Its constants have no factor
depending on the horizon, selected subset, or observation block dimension.

The rational-metric extension, fixed partial latent observation corollary,
and weighted-trace approximation scheme also follow under the stated
restrictions. This review establishes correctness of the argument, not
priority over earlier inverse-decay or local-factorization theory. The broad
constants remain too large for the example in the source note to establish a
practical method.

## Independent proof audit

The weighted-conjugation argument is valid for an arbitrary principal
calendar subset. If \(E=W^{-1}R_{HH}W-R_{HH}\), then its diagonal blocks
are exactly zero even when the original diagonal blocks are arbitrarily
large. The scalar matrix of block operator norms has row and column sums at
most
\[
2C\left[\frac{\rho}{\theta-\rho}-\frac{\rho}{1-\rho}\right].
\]
The source's rational choice of \(\theta\) makes this expression exactly
\(m/2\), and satisfies \(\rho<\theta<1\). The block Schur bound is
dimension independent: apply the scalar matrix to the vector of block
Euclidean norms. There are at most two calendar blocks at any given positive
distance; block coordinates are not counted separately.

The perturbation is generally nonsymmetric, which causes no problem.
The bound \(\|R_{HH}^{-1}E\|\le1/2\) gives an inverse norm at most
\(2/m\) by a Neumann series. This uses only the lower eigenvalue bound on
\(R_{HH}\). Applying it to the whole weighted covariance row proves the
claimed regression constant \(B\); summing individual inverse-block
estimates instead would require a different constant.

For an old observation \(j<t-L\), all history indices \(u\) satisfy
\(u>j\). The product in the residual covariance bound is
\[
\theta^{t-u}\rho^{u-j}
=\theta^{t-j}(\rho/\theta)^{u-j}.
\]
Summing distinct positive distances gives exactly the source's
\(K_{\mathrm{old}}\). For a pair \(s<t\), regression orthogonality removes
observations inside the later history, while old terms from the earlier
history remain. The source correctly keeps those terms when the residual
windows overlap.

The finite geometric identity behind the row bound can be checked without
the source's closed form. Put \(q=\theta\). The contribution involving two
regression factors is
\[
\begin{aligned}
&B\sum_{h>L}q^h\sum_{d=1}^Lq^{2d}
 +B\sum_{h=1}^Lq^h\sum_{d=L+1-h}^Lq^{2d}\\
&\qquad=\frac{B}{1-q}\sum_{d=1}^Lq^{L+1+d}
=\frac{q^{L+1}}{1-q}\,
  \frac{Bq(1-q^L)}{1-q}.
\end{aligned}
\]
Adding the direct old-observation tail and the two sides of each row gives
equation (4) in the source note.

Every local conditional covariance is at least \(mI\). The Schur-complement
variational formula minimizes a principal covariance quadratic form over
history coordinates while fixing the current coordinates, so its value is
at least \(m\) times the squared norm of the fixed vector. Normalization
therefore costs at most \(1/m\). The normalized residual covariance has
identity diagonal blocks. Bounding its off-diagonal block row sums gives
the claimed operator norm. Finally, \(TT^T\) and \(T^TT\), with
\(T=D_L^{-1/2}A_LR_{SS}^{1/2}\), have the same eigenvalues; congruence then
gives both relative precision inequalities.

Deleting times does not change any of these bounds, because sums only lose
terms and principal matrices retain the same lower eigenvalue bound. The
independent-dummy padding argument in the source note is also valid. It
explains why subset uniformity alone should not be presented as a separate
priority distinction from an appropriate class-uniform full-calendar result.

The source's diagonal-normalization reduction is correct. Its inequalities
follow from \(\|R-D\|\le b\), \(R\succeq mI\), and \(D\succeq mI\).
Thus absence of a diagonal upper bound does not itself prevent comparison
with older bounded-spectrum results after a change of coordinates.

## Metrics and fixed partial observations

The rational block PSD promise in equation (14) is equivalent to the stated
whitened cross-block norm bound by congruence with the positive definite
metric blocks. The covariance lower bound transforms in the same way. These
tests require rational PSD checks, without numerical square roots.

Let \(T_t=V_t^{-1/2}\) denote conceptual whitening. The transformed local
regression and covariance are \(b'_t=T_tb_tT_H^{-1}\) and
\(D'_t=T_tD_tT_t^T\). Hence original-coordinate local information produces
exactly the whitened information after transforming the sensitivities.
Normalized residual coordinates differ by the block matrix
\[
O_t=(D'_t)^{-1/2}T_tD_t^{1/2},\qquad O_tO_t^T=I.
\]
Thus the normalized residual operator norm is unchanged. This argument
permits poorly conditioned rational metrics; exact arithmetic complexity
depends on their encoding length, not numerical conditioning.

For fixed observation packets \(Y_t=H_tX_t+v_t\), independent observation
noise supplies \(R\succeq mI\). Independence of the innovations gives the
cross-covariance formula in the source. The transition, latent covariance,
and observation-map norm bounds then give
\(C=\overline H^2\overline P\). Full observation of the latent state is
unnecessary. Selection still acquires a whole fixed packet at a time; this
does not implement independent coordinate choices within that packet.

## Approximation guarantee and bit complexity

For positive semidefinite trace weight and prior, the precision sandwich
gives the same relative sandwich for the nonnegative weighted-trace
criterion, including its fixed prior. Maximizing the additive local
surrogate therefore gives the factor
\((1-\eta)/(1+\eta)\ge1-\epsilon\) with \(\eta=\epsilon/2\), including
zero-optimum instances.

With fixed rational decay and covariance-ratio bounds, the constants can
be chosen rational and independent of the instance dimensions. Minimality
of \(L\) gives
\(2^L\le\max\{1,(K/\eta)^{\log2/\log(1/\theta)}\}\); the exact
full-history cap cannot increase this estimate. Local matrix dimensions
are at most \(d(L+1)\), and graph states number
\(O(n(k+1)2^L)\). This is polynomial in the explicitly encoded input and
\(1/\epsilon\) when the decay and ratio bounds remain fixed.

Rational principal inverses and Schur complements have polynomial-size
entries by determinant bounds or fraction-free elimination. An individual
path adds at most \(n\) local weights; adding their denominator bit lengths
gives a polynomial bound on path-value size. Thus exact additions and
comparisons also have polynomial bit cost. Growing observation and
parameter dimensions change matrix work polynomially, not the number of
calendar masks exponentially. This argument would not give a uniform FPTAS
if the decay rate approached one or the covariance ratio grew without a
fixed bound. It does not cover log determinants, inverse-information trace,
or arbitrary side constraints.

Two wording clarifications were sent to the author: the dimensionless
constants depend only on \(C/m\), while \(K_{\mathrm{old}}\) itself scales
with covariance; the FPTAS statement should explicitly inherit rational
promise data and accuracy, and a nonempty feasible family when mandatory or
forbidden times are supplied. Neither changes the proof.

## Exact supplementary checks

The independent script
[`review_general_covariance_memory.py`](../code/research_20260912/review_general_covariance_memory.py)
constructs rational non-Markov covariances with signed off-diagonal blocks.
It forms explicit local residual maps and compares their precision matrices
with direct selected covariance inverses. Its PSD check uses exact symmetric
Schur elimination, including zero pivots. No production theorem or
certificate implementation is called.

Four models include varying block dimensions, several decay and covariance
ratios, and diagonal positive semidefinite additions with scales up to
\(10^9\). A rational block change of coordinates also checks the metric
form. Every nonempty subset and window is examined. The
[saved report](../code/research_20260912/results/general-covariance-memory-independent-review.json)
records the deterministic seed, exact model parameters, versions, and source
hashes.

| Exact check | Count |
| --- | ---: |
| Selected subset/window cases | 335 |
| Relative precision PSD inequalities | 670 |
| Regression block norm inequalities | 408 |
| Old-observation covariance inequalities | 280 |
| Local conditional covariance floors | 784 |
| Metric congruence identities | 60 |
| Rational metric cross-covariance promises | 6 |
| Finite geometric identities | 80 |

All passed. The run took 0.66 seconds with Python 3.13.11, NumPy 2.5.3, and
SymPy 1.14.0. Reproduce it with:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
uv run --project code/research_20260912 \
python code/research_20260912/review_general_covariance_memory.py
```

One elementary boundary example confirms why a fixed positive lower bound
cannot simply be dropped. Put two selected observations at calendar distance
\(h\), with covariance
\[
R_{SS}=\rho^h
\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix},
\]
and make intermediate observations independent. The off-diagonal decay
promise holds with \(C=1\). For any \(L<h\), the normalized local residual
covariance has off-diagonal entries \(1/2\), so its error norm stays
\(1/2\), even if \(L=h-1\) tends to infinity. Its smallest covariance
eigenvalue tends to zero. This does not contradict the theorem: its
constants are permitted to worsen with \(C/m\).
