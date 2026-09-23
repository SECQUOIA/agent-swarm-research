# Sources for positive rational approximation of fractional flow laws

Date: 2026-09-05. Status: bounded source and novelty audit. The network theorem is developed and reviewed separately in [the fractional additive investigation](potential-flow-fractional-additive-investigation.md).

Positive rational approximation of fractional powers with root-exponential uniform error is established mathematics. In particular, the endpoint zero can be handled directly from a published scalar estimate by inversion. The proposed contribution should be the resulting network optimization theorem, including its bit model and uncertainty class, rather than the approximation principle.

## A primary theorem that includes zero after inversion

[Bonito and Pasciak, *Numerical Approximation of Fractional Powers of Elliptic Operators*](https://arxiv.org/pdf/1307.0888), inspected 27-page preprint, Section 3.3, equation (37), Lemma 3.4, and Remark 3.1, PDF pp.14–15, give

```
Q_beta(lambda) = (2 k sin(pi beta)/pi)
                 sum_(ell=-N)^N exp(2 beta ell k)
                                  /(1+exp(2 ell k) lambda),
k=1/sqrt(N).
```

For fixed `0<beta<1`, their explicit error bound is uniform over `lambda>=lambda_0>0` and is `O(exp(-c sqrt(N)))`. Equation (40) bounds its strip constant using only `beta` and `lambda_0`. All quadrature coefficients and nodes are positive. Their Section 3.2, PDF pp.10–13, also studies weighted Gaussian quadrature on dyadic panels, with a different parameter choice from the repository's construction. Published version: *Mathematics of Computation* 84 (2015), 2083–2110, DOI 10.1090/S0025-5718-2015-02937-8.

**Immediate scalar consequence.** Set `lambda_0=1` and `lambda=1/t`. Then

```
Q_beta(1/t) = sum_ell a_ell t/(t+s_ell),
a_ell>0, s_ell>0.
```

The estimate holds uniformly on `(0,1]`; assigning zero at `t=0` makes both the target and approximant continuous there and extends the bound to `[0,1]`. Consequently `O(p^2)` terms suffice for `O(2^-p)` error. This substitution is an inference from the scalar theorem, not a separate result claimed by its authors.

## Related sinc literature and a scope warning

[Bonito, Lei, and Pasciak, *On Sinc Quadrature Approximations of Fractional Powers of Regularly Accretive Operators*](https://arxiv.org/pdf/1709.06619), inspected version dated February 5, 2018, equations (1)–(2), PDF p.1, uses the Balakrishnan integral and a positive weighted sum of shifted resolvents. Theorem 3.2 and Remark 3.1, PDF pp.6–7, give exponential-in-inverse-step error with quadrature counts quadratic in inverse step. Published DOI: 10.1515/jnma-2017-0116.

This is useful attribution for the general sinc method. Its operator estimates contain coercivity and boundedness parameters. For the specific scalar endpoint claim, use the uniform half-line estimate above and inversion rather than silently sending an operator's smallest eigenvalue to zero.

[Aceto and Mazza, *Exploring Rational Approximations of Fractional Power Operators for Preconditioning*](https://link.springer.com/article/10.1007/s11075-026-02359-y), Theorem 2 and Remark 1, provides another explicit uniform half-line sinc bound with positive exponential nodes, its root-exponential rate, and attribution to earlier Bonito–Pasciak analysis. It corroborates that this approximation ingredient is known. No novelty should be assigned to the rate, positivity, or exponential change of variables.

## Rigorous polynomial-bit construction of Gaussian nodes and weights

[Johansson and Mezzarobba, *Fast and Rigorous Arbitrary-Precision Computation of Gauss–Legendre Quadrature Nodes and Weights*](https://marc.mezzarobba.net/ecrits/JohanssonMezzarobba_Legendre_v3_2018.pdf), *SIAM Journal on Scientific Computing* 40(6), C726–C747 (2018), DOI 10.1137/18M1170133, supplies a direct primary computational reference for the repository's alternative Gauss construction.

Equation (3), PDF p.1, gives the positive weight formula from Legendre roots. PDF p.2 recalls exactness for polynomials through degree `2n-1`. PDF p.3 states a `soft-O(n^2 p)` bit bound for all degree-`n` nodes and weights to `p`-bit accuracy and gives a faster theorem when precision and degree grow proportionally. Section 7.2, PDF p.18, describes rigorous root and weight enclosures using interval Newton refinement. The general polynomial bound already suffices here; no optimal-complexity implementation is needed.

These results support the author's use of rational enclosures for positive Gauss coefficients. They do not themselves prove the repository's particular dyadic fractional-integral error bound or the physical-flow perturbation estimate.

## What still needs an explicit bit argument

The inspected fractional-operator sources give real coefficients involving exponentials, powers, and normalization constants. I did not locate a theorem phrased exactly as the repository needs: positive rational coefficients with a specified total encoding length, uniform fractional-law error, and a dense rational numerator/denominator suitable for fixed-dimensional elimination.

The candidate's proposed supplement is elementary but should remain in its proof: bound every positive denominator parameter away from zero by a number with polynomial encoding length; bound coefficient magnitudes; approximate nodes and weights to enough absolute precision; preserve their positivity; then account for expansion and normalization. For a single term `a t/(t+s)`, the estimates

```
|partial/partial a| <= 1,
|partial/partial s| <= a/s       (t>=0, s>0)
```

explain why exponentially small nodes need only polynomially many extra precision bits when their logarithmic range is polynomial. They do not permit rounding nodes to zero. The normalized dyadic-Gauss construction in the investigation avoids computing the transcendental prefactor by dividing by its value at one. Its quantitative normalization and rounding claims are author-derived and require the separate proof audit.

Positivity has a concrete use beyond approximation: terms `a t/(t+s)` produce an odd rational flow law through `x R(x^2/T^2)`, with derivative nonnegative and strict increase away from a constant function. This monotonicity-preserving use, the network stability estimates, and the bounded-block-rank optimization reduction must be proved together. A generic best rational approximant would not automatically provide these properties.

## Qualified novelty assessment

The bounded search did not find the proposed joint nomination/resistance optimization theorem for the fixed fractional law on graphs of fixed maximum biconnected-block cycle rank. This absence does not establish priority. The source-supported claim is narrower: the necessary positive rational approximants and efficient Gaussian coefficient construction are available from known numerical analysis, so any new theorem should credit them and identify its contribution in the network structure and certified bit-complexity transfer.

Exact arc-threshold SRS-hardness is compatible with a high-precision additive algorithm. The latter must return its stated approximation guarantee and cannot decide equality or an arbitrarily close threshold without additional separation information. Nothing in these approximation sources removes that distinction.
