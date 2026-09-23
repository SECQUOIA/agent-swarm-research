# Certified rational approximation of positive polynomial inverses

Date: 2026-09-05. Author: potential_flow_review. Status: independently
reviewed supporting lemma. Both the
[first full audit](review-certified-positive-polynomial-inverse-approximation.md)
and [second full audit](review-certified-positive-polynomial-inverse-approximation-second.md)
passed the analytic proof, rational bit bounds, and bilevel transfer.

A positive-coefficient polynomial marginal has a uniformly controlled
complex inverse neighborhood away from zero. Expanding at a rational
response value, rather than an irrational inverse value, makes every
Taylor coefficient rational exactly. This gives a polynomial-time piecewise
polynomial inverse approximation with complexity in accuracy bits, uniformly
over coefficient conditioning. Only the stated nonnegative-coefficient
scope is claimed.

The later [signed-coefficient extension](certified-monotone-polynomial-inverse-approximation.md)
handles every strictly increasing dense rational polynomial, including
interior derivative zeros. Its broader construction retains polynomial
complexity but has Taylor degrees depending on coefficient encoding; the
more explicit bounds below remain specific to positive coefficients.

## Statement

Let

```
g(z)=sum_(k=1)^P a_k z^k,       a_k>=0 rational,
sum_k a_k>0.
```

Let `G=g(1)>0`, and define its clipped inverse response by

```
z(t)=0                         if t<=0,
z(t)=g^(-1)(t)                 if 0<t<G,
z(t)=1                         if t>=G.
```

Given a positive rational tolerance `eta`, one can construct rational
breakpoints and rational polynomial branches approximating this response
uniformly within `eta`. The construction is polynomial in the coefficient
encoding, the numerical degree bound `P`, and `log(1/eta)` (with tolerance
above `1/2` replaced by `1/2`). Each branch has degree `O(log(1/eta))`.
There are `O(P^2 log(1/eta))` nonconstant branches and two constant branches.
Every coefficient and breakpoint has polynomial rational bit length.

Thus this is polynomial-time in the usual input length for dense or unary
degree encoding. It is not a polynomial-time claim for sparse binary-encoded
large exponents.

Divide by `G` and use the target variable `t/G`, so it suffices to prove the
statement for

```
g(z)=sum_(k=1)^P b_k z^k,       b_k>=0,       sum_k b_k=1.           (1)
```

This rational normalization has polynomial bit complexity. Throughout the
proof below the target variable is normalized, with saturation threshold one.

## 1. Elementary real bounds

For `0<=z<=1`,

```
z^P<=g(z)<=z,        0<=g'(z)<=P.
```

For `z>0` one also has

```
g(z)<=z g'(z)<=P g(z).                                           (2)
```

These follow term by term. The polynomial is strictly increasing on
`[0,1]`, even if its derivative vanishes at zero. Its normalized inverse
is consequently well defined.

Put `m=ceil(log2(1/eta))` and `K=Pm`. For all `t<=2^(-K)`, the zero
response approximation has error at most `2^(-m)<=eta`; this includes
negative targets, where the true clipped response is zero. For `t>=1`,
use the exact constant branch one.

## 2. A relative complex inverse disk

Fix any real `z_0 in (0,1]` and write `t_0=g(z_0)>0`. Define

```
r_z=z_0/(4P),              R_t=t_0/(8P).
```

For complex `w` with `|w|<=r_z`, coefficient nonnegativity gives

```
|g'(z_0+w)-g'(z_0)|
 <=g'(z_0)[(1+1/(4P))^(P-1)-1]
 <=g'(z_0)(exp(1/4)-1)
 <g'(z_0)/3.                                                     (3)
```

Indeed, apply the binomial majorant to every term of the derivative and
use `k-1<=P-1`. The final numerical inequality follows from
`exp(1/4)<1/(1-1/4)=4/3`, for example by comparing the exponential and
geometric series. Integrating the derivative difference along the segment
from zero to `w` gives

```
|g(z_0+w)-t_0-g'(z_0)w| <= g'(z_0)|w|/3.                         (4)
```

On `|w|=r_z`, any target `s` with `|s-t_0|<=R_t` satisfies, by (2),

```
|s-t_0|<=t_0/(8P)<=g'(z_0)r_z/2.
```

Thus (4) plus this target shift is at most
`(5/6)g'(z_0)r_z`, strictly below the boundary linear magnitude.
Rouché's theorem, applied against the linear function
`g'(z_0)w`, proves that `g(z_0+w)=s` has exactly one zero inside this
disk, counting multiplicity. Equation (3) also excludes derivative zeros
throughout it. The holomorphic implicit-function theorem and uniqueness
therefore give one analytic inverse `Z(s)` on a neighborhood of the
closed target disk, with

```
Z(t_0)=z_0,       |Z(s)-z_0|<z_0/(4P),       |Z(s)|<2.            (5)
```

The strict boundary margin permits a slightly larger target disk, which
justifies using Cauchy bounds at radius `R_t` itself. For real targets in
`[0,1]` in this disk, this is the original increasing inverse. The branch
is real by conjugation and uniqueness, remains positive by the root-disk
bound, and the positive real polynomial is strictly increasing.

The underlying complex-analysis ingredients are classical. The primary
[NIST DLMF treatment](https://dlmf.nist.gov/1.10) states Rouché's theorem
and the associated Taylor/Cauchy framework. No new inverse-function theorem
is claimed here; the explicit relative radius and rational construction
are the needed application bounds.

## 3. Rational centers for a rational target partition

Partition each dyadic interval `[A,2A]`, `A=2^(-(k+1))`, for
`k=0,...,K-1`, into `32P` equal subintervals. Let `tau` be the rational
midpoint of one panel. Its half-width is at most `tau/(64P)`.

Use rational bisection on `[0,1]` to enclose the unique real root of
`g(z)=tau` in an interval of width at most

```
tau/(64P^2).
```

Take its midpoint `z_0`. It is positive and at most one. All comparisons
are exact rational polynomial evaluations. The global bound `g'<=P`
gives, for the exact rational value `t_0=g(z_0)`,

```
|t_0-tau|<=tau/(64P),       t_0>=(63/64)tau.                       (6)
```

This changes the expansion center, not the function being approximated:
we expand the exact inverse at `t_0`, whose exact inverse value `z_0`
has been chosen rational. No irrational Taylor coefficient needs rounding.

For every target `t` in the panel,

```
|t-t_0|<=tau/(32P),
|t-t_0| / [t_0/(8P)] <=16/63<1/2.                                (7)
```

Hence the entire panel lies in half the inverse-analytic disk from
Section 2. Since `tau>=2^(-K)`, this rational bisection needs at most
`K+O(log P)` iterations. The center encodings and all polynomial comparisons
are polynomial in the original coefficient length, `P`, and `m`.

## 4. Exact rational Taylor coefficients and uniform error

At the rational center, write

```
g(z_0+u)=t_0+sum_(h=1)^P A_h u^h/D,
```

using one positive integer denominator `D`, with integer `A_h>=0` and
`A_1>0`. Expanding around a rational point has polynomial coefficient bit
length in the given parameters. Set `a_h=A_h/D`.

The Taylor series of the inverse is

```
Z(t_0+v)=z_0+sum_(n>=1) c_n v^n.
```

Formal substitution gives rational coefficients recursively:

```
c_1=1/a_1,
c_n=-(1/a_1) sum_(h=2)^min(P,n) a_h
          [v^n](sum_(j=1)^(n-1) c_j v^j)^h,       n>=2.           (8)
```

The omitted `c_n` cannot affect the degree-`n` coefficient of any power
`h>=2`. Thus truncated polynomial arithmetic computes these coefficients
exactly with polynomially many rational operations.

There is also a uniform bit bound, not just an arithmetic-operation bound.
Induction in (8) gives integers `N_n` such that

```
c_n=D^n N_n/A_1^(2n-1).                                          (9)
```

The assertion is immediate for `n=1`. A product contributing to degree
`n` in a power `h` has denominator `A_1^(2n-h)` and a factor `D^n` in
its numerator. Multiplication by `a_h/a_1=A_h/A_1`, then conversion to
the denominator in (9), only multiplies its integer numerator by
`A_1^(h-2)`. This proves the induction.

By (5) and Cauchy's coefficient bound,

```
|c_n|<=2 R_t^(-n).                                               (10)
```

Both `log(1/R_t)` and the bit length of `A_1` are polynomially bounded.
Equations (9)--(10) therefore bound the common denominator and numerator
bit lengths polynomially for every `n` under consideration. Truncated
products in (8) multiply at most `n` earlier coefficients; the number of
degree-`n` compositions is at most exponential in `n`, with logarithm
`O(n)`. Thus intermediate products and sums also have polynomial bit
length, or one may maintain the explicit common denominator from (9).

Choose `q=m+3`. On the panel, (7) and (10) give

```
|Z(t)-[z_0+sum_(n=1)^q c_n(t-t_0)^n]|
 <=2 sum_(n=q+1)^infinity (1/2)^n
 =2^(1-q)
 <=eta/4.                                                       (11)
```

The displayed Taylor polynomial has exact rational coefficients and degree
`q`. Expansion into ordinary powers of `t`, if needed, preserves polynomial
bit length. At common panel endpoints, either adjacent polynomial satisfies
the same error bound. At the bottom truncation endpoint both the zero
branch and the adjacent Taylor branch satisfy the global `eta` guarantee;
the same holds with the constant-one branch at the upper endpoint.

## 5. Consequence for separable follower costs

Consider unit-box follower coordinates with costs

```
sum_(k=1)^(P_i) a_(i,k) z_i^(k+1)/(k+1) - ell_i(x)z_i,
a_(i,k)>=0 rational,       sum_k a_(i,k)>0,
```

where `ell_i` is rational affine. Their unique responses are precisely
the clipped inverses above, with rational target normalization by
`sum_k a_(i,k)`.

For a fixed leader dimension, a rational leader polytope inside a unit
box, and an affine upper objective in leaders and responses, this lemma
fits the [bounded-power accuracy-bit proof](bilevel-bounded-power-accuracy-bit-algorithm.md)
without altering its error ledger or rational leader recovery. Each
response has polynomially many rational breakpoints; their affine
preimages give polynomially many leader cells in fixed dimension. On
each cell the response approximation is a rational polynomial of degree
`O(log(1/eta))` and uniform error at most `eta`.

The polynomial surrogate may slightly exceed the unit response range.
Only its objective value is used; the returned leader's actual unique
clipped-inverse follower remains exactly feasible in its original unit box.

Choose the same weighted local tolerance as that proof, optimize the
rational cell polynomials by fixed-dimensional real-algebraic methods,
and recover a rational leader within the selected rational cell by
simplex-weight rounding. This gives additive optimization and rational
leader output in time polynomial in coefficient encoding, requested
accuracy bits, and the numerical maximum degree. Dense or unary degree
encoding therefore allows that degree to grow; binary sparse degree does
not, consistently with the existing output-length obstruction.

This transfer retains affine response-dependent objectives only. It does
not supply exact feasibility for additional response-dependent upper
constraints, signed polynomial marginal coefficients, or multivariate
coupled follower costs. Both this analytic lemma and its transfer passed
two independent full proof audits; their established ingredients do not
by themselves establish publication priority.

## Exact diagnostics

[The exact checker](../code/bilevel_bounded_power/check_positive_polynomial_inverse.py)
passed 90 exact rational Taylor reversions, 450 certified inverse-value
comparisons, and 360 Gaussian-rational derivative-disk inequalities. Cases
include monomials, mixed positive coefficients, and coefficient ratios of
`2^30` and `2^40`, at the first, middle, and last retained dyadic bands.
It verifies the exact composed Taylor identity, the common-denominator
claim, panel containment in the analytic disk, and inverse values against
separate rational bisection enclosures. The largest tested Taylor coefficient
encoding was 2,894 bits. These finite checks supplement the analytic proof;
they neither replace the universal disk argument nor enumerate all panels
for arbitrary input.
