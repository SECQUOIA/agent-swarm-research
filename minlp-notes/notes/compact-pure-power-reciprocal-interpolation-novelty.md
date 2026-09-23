# Source audit: compact reciprocal interpolation for pure powers

Date: 2026-09-05. Bounded primary-source assessment of
[the compact construction](compact-pure-power-reciprocal-interpolation.md),
read while its positive rational approximation lemma was under independent
development. This note assesses attribution, not mathematical approval.

No exact prior theorem was found giving a polynomial-size rational MILP
within `O(r)` integers of every convex lift for this positive pure-power
class, uniformly in degrees under dense input. The claimed contribution
should be the combination of inverse-coordinate interpolation, shared-bit
evaluation, and the universal integer-count bound. Positive resolvent
approximation of fractional powers and binary product disaggregation are
established methods.

## A direct predecessor for the approximation lemma

Bonito and Pasciak,
[Numerical Approximation of Fractional Powers of Elliptic Operators](https://arxiv.org/pdf/1307.0888)
(2013 preprint, Mathematics of Computation 2015), Section 3.3, equation (37)
and Lemma 3.4, give

```
Q_b(lambda) = [2k sin(pi b)/pi]
  sum_(ell=-N)^N exp(2b ell k)/(1+exp(2ell k) lambda),
0<b<1,  k=1/sqrt(N),  lambda>=lambda_0>0.
```

The bound is uniform over the unbounded scalar interval and has explicit
exponential truncation terms involving `b` and `1-b`. Substitute
`lambda=1/t`, `lambda_0=1`, and `b=2/D`. Each summand becomes a positive
multiple of `t/(t+exp(2ell k))`, approximating `t^(2/D)` for `0<t<=1`.
Continuity supplies the endpoint zero. This is a direct derivation from
their displayed result, not a new approximation mechanism. Remark 3.1
also balances asymmetric truncation lengths. Their coefficients are real;
the checked theorem does not supply rational coefficient bit bounds or
exact normalization at one. Those remain implementation details requiring
the candidate's own proof. Dependence polynomial in the numerical degree
does not establish complexity polynomial in its binary encoding alone.

Braess and Hackbusch's
[On the approximation of Stieltjes functions by exponential sums and rational functions with applications to partial differential equations](https://link.springer.com/article/10.1007/s00211-025-01523-1)
(online December 2025, Numerische Mathematik 158, 455–490, 2026) is a further
recent predecessor. It treats rational approximation of Cauchy–Stieltjes
functions, positivity of coefficients, unbounded intervals, and sinc
quadrature. The scope and coefficient-positivity discussion in Section 3
were checked. It does not provide a mixed-integer graph formulation or the
integer-count comparison sought here. It reinforces that positive
Stieltjes approximation itself should receive classical attribution.

## Disaggregation and rational-program reformulations

Kolodziej, Castro, and Grossmann,
[Global optimization of bilinear programs with a multiparametric disaggregation technique](https://egon.cheme.cmu.edu/Papers/JGlobalOptMDTKolodziejCastroGrossmann.pdf),
Sections 1–3, develop digit representations and exact linearizations after
one product factor is discretized. Teles, Castro, and Matos's polynomial
parameterization papers extend this methodology to powers; the accessible
primary sources and their limits are recorded in the
[positive-polynomial source audit](positive-separable-polynomial-precision-novelty.md).
Reusing one coordinate's digit variables across several products is within
this established framework.

The candidate's equation `(a+beta)v=lambda`, where `a` is a binary-coded
grid point and `beta>0`, expands into binary-times-bounded-continuous
products. Its exact MILP representation is therefore a direct application
of classical binary product linearization. It should not be presented as
a new general theorem on exact rational-function reformulation.

Tawarmalani, Ahmed, and Sahinidis,
[Product Disaggregation in Global Optimization and Relaxations of Rational Programs](https://link.springer.com/article/10.1023/A:1021043227181)
(Optimization and Engineering 3, 281–303, 2002), is relevant earlier credit
for distributing products over sums and applying the resulting relaxations
to rational programs. The publisher abstract was checked, not its complete
proof. No claim is made here that this paper gives the exact interpolant
construction in the candidate.

The more specific construction combines two endpoint reciprocals with
right-hand sides `1-lambda` and `lambda`, so that a linear output equation
evaluates the chord through `R(a)` and `R(a+h)`. The same grid bits encode
the associated quadratic endpoint interpolation. This avoids listing the
exponentially many inverse-power knots. That synthesis is the useful
formulation device; no exact match was found in the inspected sources.

## Recommended claim and limits

Subject to the independent proof of rational approximation and bit bounds,
the candidate can claim a compact rational construction attaining a
degree-independent additive integer-count comparison for positive pure
powers with a common exponent per coordinate and unconditional output
error. Its continuous size and construction time may depend polynomially
on the numerical degrees, as permitted by dense input. The result does
not establish sparse binary-degree polynomial complexity.

The finite lower bound and its known midpoint-parity ingredients are
assessed in the [finite pure-power audit](pure-power-degree-independent-count-novelty.md).
This compact construction would strengthen that theorem's algorithmic
content. The approximation lemma, the reciprocal equality linearization,
and logarithmic disjunction coding should each be explicitly credited;
novelty belongs to the resulting whole-formulation guarantee rather than
to those separate tools.
