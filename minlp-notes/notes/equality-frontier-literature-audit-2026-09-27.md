# Equality certification and conditioning: prior-art audit

Research audit, 2026-09-27. This note records primary sources examined for the
equality-certification direction. It is a literature and claim-boundary note,
not a claim of a new general theorem.

## Robust roots and finite interval information

Franek, Ratschan, and Zgliczynski, *Quasi-decidability of a Fragment of the
First-order Theory of Real Numbers*, Journal of Automated Reasoning 57 (2016),
157–185, [author manuscript](https://arxiv.org/html/1309.6280), is directly
relevant:

- Theorem 1 gives a sound procedure terminating on robust bounded formulas
  built from specified systems of continuous, interval-computable equations
  and inequalities. The basic blocks have at least as many equations as
  variables, or have no equations.
- Theorem 6 characterizes robust zeros of square continuous maps by nonzero
  Brouwer degree on some interior open subregion. Its domain is a nonempty
  bounded closed region whose interior has that region as its closure.
- Lemma 8 proves a finite-information obstruction using padded interval
  answers. A terminating run sees finitely many strict enclosures; a
  sufficiently small perturbation with the opposite truth value can produce
  identical answers. Thus this argument is explicit prior art.

A zero total degree on the originally chosen box does not imply failure of
robustness: nonzero degrees of distinct root neighborhoods can cancel.
An impossibility claim must specify the oracle representation and its allowed
answers; exact symbolic information can break the indistinguishability.

Franek and Krcal, *Robust Satisfiability of Systems of Equations*,
[author manuscript](https://arxiv.org/html/1402.0858), already extend beyond
degree through extension problems for sphere-valued maps. For piecewise
linear data, their Theorem 1.2 gives polynomial-time decidability for fixed
codomain dimension n in the stable range dim K <= 2n−3. Theorem 1.3 proves an
undecidability statement for odd n > 2 at dimension 2n−2. The parity and
dimension restrictions matter; the abstract's short description must not be
used as an unrestricted threshold theorem.

## Original-system singular roots versus nearby-system certificates

Rump and Graillat, *Verified error bounds for multiple roots of systems of
nonlinear equations* (2010),
[author PDF](https://www-pequan.lip6.fr/~graillat/papers/nlss.pdf), certify a
multiple root of a slightly perturbed system and bound the perturbation.
Such a conclusion alone is insufficient to certify feasibility for the
original nonlinear program.

Akoglu, Hauenstein, and Szanto, *Certifying solutions to overdetermined and
singular polynomial systems over Q*,
[2014 author manuscript](https://arxiv.org/html/1408.2721), do certify roots
of the original rational-coefficient system. They combine exact rational
univariate representations with numerical refinement and exact polynomial
remainder checks. Determinantal isosingular deflation reduces isolated
singular roots to regular roots of an overdetermined system. Their
Introduction explicitly distinguishes this from certification of nearby
perturbed systems.

The same Introduction gives the inconsistent quadratic system
f1=x1−1/2, fi=xi−x(i−1)^2 for 2 <= i <= n, and f(n+1)=xn.
At the unique zero of the first n equations, the final residual is
2^(−2^(n−1)). Repeated squaring as a barrier to residual-based certification
is therefore explicit prior art.

## Exponential error-bound exponents at fixed degree

Kollár, *An Effective Łojasiewicz Inequality for Real Polynomials* (1999),
[author manuscript](https://arxiv.org/html/math/9904161), Example 1, uses
f1=x1^d and fi=x(i−1)−xi^d. The arc
(t^(d^(n−1)),...,t) proves that the exact local error-bound exponent is d^n.
For d=2 the equation interaction graph is already a path. Theorem 4 gives
the isolated-real-zero upper exponent B(n−1)d^n, where B(r) is the largest
binomial coefficient in row r. Its Remark 5 raises improvement to d^n as a
question; this audit does not assert that this historical question remains
open.

Basu and Mohammad-Nezhad, *Improved effective Łojasiewicz inequality and
applications*, Forum of Mathematics, Sigma (published 2024-12-03),
[publisher full text](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improved-effective-lojasiewicz-inequality-and-applications/022BF859F5714FDA8050F6DC1992E48B),
Theorem 2.11, provide error bounds on compact semialgebraic sets with
exponent d^O(n^2) for general nonempty basic semialgebraic feasible sets.
For zero-dimensional feasible sets their bound is (8d)^(2(n+7)).
Example 2.4 repeats a degree-chain lower bound of the product of the
individual degrees, citing Solernó (1991), page 2, and Ji–Kollár–Shiffman
(1992), Example 15. Their discussion still compares against Kollár's
stronger bound for the isolated-zero special setting.

## Interpretation of the proposed robust quadratic chain

The candidate system

    y1=x^2,  y(j+1)=yj^2,  x*yk=a

reduces exactly to x^(2^k+1)=a. For k >= 1 it has one real solution, and
the objective x^2 takes the value |a|^(2/(2^k+1)). The origin has equality
residual |a|. Consequently a guarantee based only on a coefficient or
residual uncertainty δ needs, in the worst case,

    δ <= ε^((2^k+1)/2)

to bound the resulting objective error by ε. The odd reduced exponent is
the distinction from the usual repeated-squaring example: it retains a
robust real root rather than an even-multiplicity zero.

This is a modest adaptation of the established degree-chain barrier.
It is not a lower bound for every algorithm on exact rational inputs:
exact syntax identifies a=0 immediately, and compressed exponents can
represent small nonzero numbers without writing a long binary mantissa.
All positive-order derivatives of the displayed equations are independent
of a, so derivative evaluations alone do not resolve uncertainty in a.

## Local MINLP comparison and verification scope

The local full texts of Füllner–Kirst–Stein (2021) and
Füllner–Kirst–Otto–Rebennack (2024) were examined. Their convergence theory
uses LICQ at global minimizers and a Miranda-based verification mechanism;
the 2024 work adds treatment of inequalities through approximate active
sets. Neither supplies a general solution to singular original-feasibility
certification. They do establish relevant convergent upper-bounding
frameworks, so a new direction should be compared against those frameworks
as well as the broader topology and symbolic-certification literature.

This audit checked theorem statements and the cited examples in primary
full texts. It did not formally verify the papers, establish an exhaustive
novelty search, or run project-wide checks. The equations in the preceding
section are direct substitutions, not a computational benchmark.
