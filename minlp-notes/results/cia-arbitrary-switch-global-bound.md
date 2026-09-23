# A general CIA bound, exact plateau, and sharp first mode-count correction

Status: developed 2026-09-04 and [independently reviewed](../notes/review-cia-universal-heavy-mode.md), including its universal heavy-mode dependency and all transfer algebra. The arbitrary-block one-sided dependency has a [separate independent audit](../notes/review-cia-arbitrary-block-one-sided.md). The proof is analytic.

Let F_{n,s}(T) be the continuous worst-case full cumulative CIA error over all measurable n-mode relaxed controls when at most s integer-mode switches are allowed. Write k=s+1 for the allowed number of activation blocks.

**Theorem.** For every n≥2 and integer 1≤k<n,

\[
 \boxed{F_{n,k-1}(T)\le T\max\left\{\frac1{k+1},
 \frac{n(n-1)+(n-k)(n-k-1)}{nk(2n-k-1)}\right\}.} \tag{1}
\]

All relaxed profiles are included, without restrictions on their terminal mode masses. No higher-order distinct-mode reach conjecture or computer-assisted certificate is used.

## Proof of the general bound

Write C_{n,k} for the rational coefficient in (1), and set E=T max{1/(k+1),C_{n,k}}.

If some terminal mode mass exceeds E, then T≤(k+1)E and the [universal heavy-mode theorem](cia-universal-heavy-mode-rounding.md) supplies at most k−1 switches with full error at most E.

Otherwise every terminal mass is at most E. The [arbitrary-block one-sided theorem](cia-arbitrary-block-one-sided-bound.md) supplies at most k distinct blocks whose negative discrepancy is at most C_{n,k}T≤E. Every positive discrepancy is at most its mode's terminal mass, hence at most E. This proves (1). ∎

## Exact plateau for a general range of modes and switches

**Corollary.** For every integer k≥2 and every integer n satisfying

\[
 k+1\le n\le\frac{k(k+1)}2,
\]

we have

\[
 \boxed{F_{n,k-1}(T)=\frac{T}{k+1}.} \tag{2}
\]

Equivalently, for every s≥1 the exact value is T/(s+2) whenever

\[
 s+2\le n\le\frac{(s+1)(s+2)}2.
\]

**Proof.** The coefficient difference factors as

\[
 C_{n,k}-\frac1{k+1}
 =\frac{2(n-k-1)(n-k(k+1)/2)}
 {nk(k+1)(2n-k-1)}.
\]

The denominator is positive, and the numerator is nonpositive throughout the stated interval. The upper bound (1) therefore equals T/(k+1).

For the matching lower bound, let the relaxed control successively take k+1 distinct pure modes, each for a duration T/(k+1). Any integer control with at most k−1 switches uses at most k distinct modes and omits at least one of these k+1 modes. Its final error is at least T/(k+1). ∎

The lower witness is classical in the switching-budget literature. The matching arbitrary-profile upper establishes this whole parameter range. This is a sufficient exact-plateau range, not a claim that the plateau ends at n=k(k+1)/2. The sharper results for k=2,3,4 extend its upper endpoint.

For example, the general theorem gives exact error T/6 with four switches for every n=6,...,15, exact error T/7 with five switches for every n=7,...,21, and exact error T/11 with nine switches for every n=11,...,55.

## Sharp first correction for every fixed switching budget

For each fixed k, the uniform-control lower coefficient is

\[
 L_{n,k}=\frac1{n((n/(n-1))^k-1)}
 =\frac1k-\frac{k+1}{2kn}+\frac{k^2-1}{12kn^2}
 +O_k(n^{-3}).
\]

The rational upper coefficient has expansion

\[
 C_{n,k}=\frac1k-\frac{k+1}{2kn}+\frac{k^2-1}{4kn^2}
 +O_k(n^{-3}).
\]

For all sufficiently large n, C_{n,k}>1/(k+1), so these two coefficients squeeze the full arbitrary-profile minimax:

\[
 \boxed{F_{n,k-1}(T)=\frac Tk-\frac{(k+1)T}{2kn}
 +O_k(T/n^2).} \tag{3}
\]

In switch-budget notation, this is

\[
 F_{n,s}(T)=\frac{T}{s+1}
 -\frac{(s+2)T}{2(s+1)n}+O_s(T/n^2)
 \qquad\text{for every fixed }s\ge0.
\]

The explicit upper and uniform lower coefficients differ by

\[
 C_{n,k}-L_{n,k}=\frac{k^2-1}{6kn^2}+O_k(n^{-3}).
\]

The leading T/(s+1) is a known coarse-block rounding consequence. The coefficient of 1/n is determined sharply here for every fixed switch budget. An exact finite-n formula beyond the proved plateau and the separately resolved small switch budgets remains open.
