# Certified rational approximation of monotone polynomial inverses

Date: 2026-09-05. Status: independently reviewed supporting lemma.
The [first audit](review-certified-monotone-polynomial-inverse-approximation.md)
and [second audit](review-certified-monotone-polynomial-inverse-approximation-second.md)
both pass the full proof and the box-follower bilevel transfer.

Let `g` be a densely encoded rational polynomial of degree `D>=1`, strictly
increasing on `[0,1]`, with `g(0)=0` and `g(1)=1`. Its coefficients may have
arbitrary signs and its derivative may vanish inside the interval. For a
positive rational tolerance `eta`, the clipped inverse of `g` admits a
uniform rational piecewise-polynomial approximation of error at most `eta`,
constructible in time polynomial in coefficient encoding, numerical `D`,
and the requested accuracy bits. Formally one may supply `eta=2^(-B)`
through the nonnegative integer `B`, with running time polynomial in `B`;
for an arbitrary rational `eta`, its encoding length is included as well. The number of pieces, degrees, and all rational encodings
are polynomial in these parameters. Strict increase can either be promised
or checked by univariate polynomial sign methods.

This extends the [positive-coefficient lemma](certified-positive-polynomial-inverse-approximation.md),
whose sharper degree and panel bounds remain useful. Here the Taylor degree
also depends on the coefficient encoding. Sparse binary-encoded degrees
are outside the polynomial-time claim. The construction does not require
a positive lower bound on `g'`.

## 1. An explicit uniform inverse modulus

For any interval `[a,a+h]` inside `[0,1]`, let
`mu=g(a+h)-g(a)`. Interpolate `g-g(a)` at the `D+1` equally spaced nodes
`a+jh/D`. All its node values lie in `[0,mu]`. At any `x in [0,1]`, each
numerator factor in a Lagrange basis polynomial has absolute value at most
one, whereas the absolute denominator of basis `j` is
`(h/D)^D j!(D-j)!`. Consequently

```
|g(x)-g(a)| <= mu (D/h)^D 2^D/D! <= mu (2D/h)^D.
```

Evaluate at zero and one and use `g(1)-g(0)=1` to obtain

```
g(a+h)-g(a) >= (h/(2D))^D/2.                           (1)
```

Replace `eta` by `min(eta,1/2)` and put

```
e = eta/4,       delta = (e/(2D))^D/4.
```

If `0<=s<=t<=1` and `t-s<=delta`, then
`g^(-1)(t)-g^(-1)(s)<e`: otherwise apply (1) to the first response interval
of length `e`, obtaining a target increase at least `2 delta`.
All these rationals have polynomial bit length. This estimate deliberately
sacrifices sharp constants to avoid condition-number assumptions.

## 2. Locating all dangerous target values

A finite critical value of `g` has the form `g(z)` with `g'(z)=0`.
There are at most `D-1` distinct critical points. Compute the finite set
of their real parts by eliminating `u,v` from the real formula

```
Re g'(u+iv)=0,  Im g'(u+iv)=0,  s=Re g(u+iv).             (2)
```

There are three real variables and a constant number of polynomials of
degree at most `D`; their rational encodings are polynomial in the dense
input. Fixed-dimensional real quantifier elimination, followed by
univariate real-root isolation and sign testing, therefore describes and
isolates precisely the distinct `s` in polynomial bit complexity. Complex
critical points are included even when their values are nonreal. This
projection is more conservative than merely isolating real critical values.
For `D=1`, the set is empty.

Choose `rho` as the largest positive dyadic power of two not exceeding
`min(delta/[4(D+1)],1/16)`. In particular

```
4(D+1)rho <= delta,       rho<=1/16.
```

Keep the critical real parts in `[-1,2]`; exact algebraic comparisons decide
this restriction. Enclose each retained real part in a rational interval
`[l,u]` of width at most `rho`, then pad to `[l-rho,u+rho]`. Also include
the intervals `[-rho,rho]` and `[1-rho,1+rho]`. Intersect their union with
`[0,1]` and merge overlaps. Call the resulting set `B`.

The sum of lengths of the untrimmed intervals is at most
`3(D-1)rho+4rho <=4(D+1)rho<=delta`. Hence each component of `B` has
length at most `delta`. Approximate the inverse on such a component by a
rational bisection approximation, within `e`, to its inverse value at the
component midpoint. Equation (1) gives uniform error less than `2e` on
the entire component. Endpoints zero and one need no exceptional limit
argument. Outside `[0,1]`, use the exact clipped constants zero and one.

Every complementary gap `[a,b]` between components of `B` has rational
endpoints and length at most one. For `tau in [a,b]`, define

```
d(tau)=min(tau-a+rho,b-tau+rho).
```

Its distance to the real part of every critical value is at least
`d(tau)`. Indeed, a retained critical real part lies at least `rho` behind
the outer endpoint of its padded interval; this property persists when
intervals are merged. Omitted real parts are outside `[-1,2]`, hence more
than one away from `[0,1]`, whereas `d(tau)<=1/2+rho<1`.

## 3. Polynomially many rational analytic panels

Split a gap at its midpoint `m=(a+b)/2`. Starting at `x=a`, make left-half
panels `[x,y]` with

```
y=min(m, x+(x-a+rho)/32),
```

until reaching `m`. Reflect this construction for the right half. Before
the last panel, the quantity `x-a+rho` grows by the factor `33/32`.
Thus each gap uses `O(1+log(1/rho))` panels, all with polynomial rational
bit length. The total number is
`O((D+1)(1+log(1/rho)))`, hence polynomial in the stated input.

For a panel with midpoint `tau`, let `d=d(tau)`. Its half-width is at most
`d/64`. A rational bound for the derivative on `[0,1]` is
`L=max(1,sum_k k |a_k|)` when `g(z)=sum_k a_k z^k`.
Bisection finds a rational `z0 in (0,1)` satisfying

```
|g(z0)-tau| <= d/64.
```

For example, bisect the inverse bracket until its width is at most
`d/(64L)` and use the midpoint. Set `t0=g(z0)` exactly and `R=d/4`.
All these operations have polynomial bit complexity, since `d>=rho`.
Every critical value is at complex distance at least `63d/64` from `t0`,
so the closed disk of radius `R` contains no critical value, with strict
margin. The entire panel satisfies

```
|t-t0| <=d/32 <=R/8.                                   (3)
```

A polynomial is a proper map of the complex plane. Above a disk containing
no critical value it is an unramified finite covering; each component over
the simply connected disk is a single inverse branch. Equivalently,
local holomorphic inverses continue along every path without escaping to
infinity, and the monodromy theorem makes the continuation single valued.
Thus the inverse branch with `Z(t0)=z0` is holomorphic on a neighborhood
of the closed radius-`R` disk. On the real panel it equals the original
increasing inverse, by continuity and local uniqueness along the real
segment. In particular `g'(z0)!=0`; a vanishing derivative would make
`t0` a critical value.

## 4. Rational Taylor coefficients and their encoding

Throughout the disk, `|t|<2`. The elementary Cauchy root bound applied to
`g(z)-t` therefore supplies the rational bound

```
|Z(t)| <= M := 2+(2+sum_(k<D)|a_k|)/|a_D|.
```

The bit length of `M` is polynomial in the coefficient encoding. Cauchy's
coefficient bound for `Z(t0+v)=z0+sum_(n>=1)c_n v^n` gives
`|c_n|<=M R^(-n)`. By (3), truncation at any integer

```
q >= ceil(log2(4M/eta))
```

has error at most `eta/2` (use the weaker ratio `1/2` in the geometric
series). Thus `q` is polynomial in coefficient encoding and accuracy bits.

All coefficients are exact rationals. Write
`g(z0+u)-t0=sum_(h=1)^D A_h u^h/Q` with integer `A_h`, positive integer
`Q`, and `A_1!=0`. Formal series reversion gives

```
c_1=Q/A_1,
c_n= -(1/A_1) sum_(h=2)^min(D,n) A_h
             [v^n](sum_(j=1)^(n-1)c_j v^j)^h.
```

As in the positive-coefficient proof, induction gives
`c_n=Q^n N_n/A_1^(2n-1)` for an integer `N_n`; signs of `A_h` are
irrelevant. This bounds denominator bit length polynomially. The Cauchy
magnitude bound bounds numerator bit length polynomially because
`log(1/R)` is polynomially bounded. Intermediate truncated products have
at most exponentially many compositions, whose logarithm is `O(q)`;
using the displayed common denominators keeps their encodings polynomial.
The number of rational arithmetic operations is polynomial in `D,q`.

Combining the constant pieces on `B`, the Taylor pieces on its complement,
and the two exact clipped pieces gives the asserted approximation.
At a shared breakpoint either adjoining branch obeys the error bound;
a half-open convention makes the output a function if required.

## 5. Scope of the optimization transfer

For an arbitrary rational polynomial marginal `h` strictly increasing on
`[0,1]`, put `G=h(1)-h(0)>0` and
`g(z)=(h(z)-h(0))/G`. The unique unit-box response to the affine load
`ell(x)` is the clipped inverse of `g` at `(ell(x)-h(0))/G`.
All transformations preserve polynomial encoding. The existing
[accuracy-bit bilevel construction](../results/bilevel-bounded-power-accuracy-bit-algorithm.md)
therefore applies to arbitrary densely encoded strictly convex univariate
polynomial follower costs, with fixed leader dimension, an affine upper
objective, and no response-dependent upper constraints. Convex polynomial
costs that are not strictly convex require separate tie-breaking and are
outside this statement. The lemma also supplies the response approximation
interface for the already-started resource-coupled extension; that extension
requires its own residual and dual bounds.

## Sources and priority

Fixed-dimensional quantifier elimination and algebraic root isolation are
classical; see Basu, Pollack and Roy, [On the Combinatorial and Algebraic
Complexity of Quantifier Elimination](https://citeseerx.ist.psu.edu/document?doi=dab8ba1c3d90aeebd7ce0fb1cc999c43839aeaab&repid=rep1&type=pdf),
and the authors' [book page](https://www.math.purdue.edu/~sbasu/).
The holomorphic inverse, monodromy and Cauchy ingredients are standard
complex analysis. The coefficient-independent estimate (1) is an elementary
Lagrange-interpolation version of a Remez-type growth estimate. No new
result is claimed for any of those ingredients separately.

The [focused source comparison](monotone-polynomial-inverse-approximation-novelty.md)
credits Farouki's direct polynomial-inverse approximation algorithm and
Walsh's polynomial-bit Puiseux computation. No inspected source states
the complete uniform rational construction above; this is a bounded
search finding, not a priority guarantee. The lemma is retained as a
supporting result for the optimization transfer.

## Independent exact diagnostics

The [second auditor's stdlib checker](../code/bilevel_bounded_power/check_monotone_inverse_second.py)
passed 15,504 exact rational panel checks, 20 Taylor centers, 236
denominator and Cauchy checks, 60 certified inverse enclosures, 80 modulus
checks, and three nonreal critical-value pairs. It uses degree-three and
degree-five interior stationary inverses and signed cubics with complex
critical values. Taylor coefficients are computed independently through
Lagrange inversion and checked by exact composition. These finite tests
supplement the universal proof; they do not implement or test the general
quantifier-elimination step.
