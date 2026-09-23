# Equal coordinate marginals give a sharp factor-two bound

Date: 2026-09-04. Status: independently audited classical consequence, recorded for comparison with the new unequal-marginal constructions. See `notes/review-positive-multilinear-equal-marginals.md`.

At a point x=(u,...,u) of the unit cube, every positive multilinear polynomial satisfies tbtgap f(x)≤2 chgap f(x), regardless of degree or dimension. Thus unequal coordinate marginals are necessary for a ratio above two. The [two-marginal cubic family](positive-cubic-two-level-family.md) shows that two distinct values already suffice.

The elementary symmetric polynomial envelope used below is classical: Sherali's Theorem 3 and equation (13) give its convex envelope on the entire unit cube. The present extremal ratio formulation and elementary proof are recorded as consequences of that machinery, without an independent novelty claim. [Sherali (1997), original paper](https://math.ac.vn/uploads/files/9701245.pdf).

## Exact finite-dimensional formula

Fix n≥2 and 0<u<1, and optimize over polynomials with a nonzero nonlinear part. Ignore affine terms, which do not change either gap. For 2≤d≤n define

\[
T_d(u)=\min\{u,(d-1)(1-u)\}.
\]

Let b=⌊nu⌋ and θ=nu−b. Define

\[
q_{n,d}(u)=
\frac{(1-\theta)\binom bd+\theta\binom{b+1}d}{\binom nd},
\]

where a binomial coefficient is zero if its upper index is smaller than its lower index. The exact worst ratio over positive multilinear polynomials in n variables, at this prescribed equal-marginal point, is

\[
R_n^{\rm eq}(u)=
\max_{2\le d\le n}\frac{T_d(u)}{u-q_{n,d}(u)}.
\tag{1}
\]

A maximum-degree restriction 2≤D≤n is imposed simply by replacing the upper limit n in the maximum by D.

To prove the upper bound, let K equal b or b+1 with probabilities 1−θ and θ. Conditional on K, choose a uniformly random K-element success subset of the n coordinates. Each coordinate has success probability u, and each degree-d product has expectation q_{n,d}(u). For any positive polynomial, this one distribution gives hull gap at least the sum of its coefficients times u−q_{n,d}(u). Its termwise gap is the same weighted sum with T_d(u) in place of that deficiency. Their ratio is therefore at most the maximum in (1).

For attainment, choose the elementary symmetric polynomial E_d(x)=Σ_{|S|=d}∏_{i∈S}x_i. At a binary vertex its value is binom(K,d), where K is the total number of successes. This integer sequence is discretely convex: its first differences are binom(K,d−1), a nondecreasing sequence. Hence, among all integer-valued K with mean nu, its expected value is minimized by the two adjacent integers b,b+1. The uniform-subset construction attains that minimum while preserving every individual marginal. Thus its convex envelope is binom(n,d)q_{n,d}(u), its concave envelope is binom(n,d)u, and it attains the corresponding ratio in (1).

## A dimension-free formula and bound

The adjacent-count law minimizes every discretely convex function of K. Comparing it with K distributed as Binomial(n,u) gives

\[
q_{n,d}(u)\le u^d.
\]

Consequently

\[
R_n^{\rm eq}(u)\le
R_\infty^{\rm eq}(u):=
\max_{k\ge1}
\frac{\min\{1,k(1-u)/u\}}{1-u^k}.
\tag{2}
\]

For every fixed d, q_{n,d}(u)→u^d as n→∞. Taking the elementary symmetric polynomials of a maximizing degree in (2) therefore shows that the expression in (2) is the exact supremum over dimensions, and the finite-dimensional values in (1) converge to it.

To bound (2), put t=k(1−u)/u. Bernoulli's inequality gives

\[
u^{-k}=\left(1+\frac{1-u}{u}\right)^k\ge1+t.
\]

It follows that

\[
\frac{\min(1,t)}{1-u^k}
\le\min(1,t)\frac{1+t}{t}\le2.
\]

Thus the bound two holds for all degrees and dimensions. At u=1/2, the degree-two terms approach two as n grows, so it is the best constant uniform in u and n. For example, for even n, the complete bilinear polynomial has ratio 2(n−1)/n at the midpoint.

## Which degree is worst in the dimension-free limit?

Let ρ=u/(1−u). The maximum in (2) occurs at an integer k in

\[
\{\max(1,\lfloor\rho\rfloor),\max(1,\lceil\rho\rceil)\}.
\]

Indeed, when k≥ρ, the ratio is 1/(1−u^k), which decreases with k. When k≤ρ, it is

\[
\frac{k}{u+u^2+\cdots+u^k},
\]

which increases with k because the average of the decreasing sequence u,u²,...,u^k decreases. Only the two integers adjacent to ρ need be checked.

In particular, for 0<u≤1/2, k=1 is optimal and the limiting worst ratio is 1/(1−u). The equal-marginal restriction remains essential: the cubic family with marginal values 1/2 and 3/4 exceeds two despite having all coordinates in the upper half of the cube.

## Scope

These statements concern equal normalized coordinate values on the unit cube. They do not by themselves assert the same exact formulas for arbitrary nonnegative boxes after expansion of the original terms. The pointwise finite-dimensional envelope of E_d is established in the cited classical work; no claim is made that it originates here.

The independent audit verified 120,060 rational parameter cases in addition to the proof. It also checked the equivalence with Sherali’s original equation (13), rather than relying solely on secondary citations.
