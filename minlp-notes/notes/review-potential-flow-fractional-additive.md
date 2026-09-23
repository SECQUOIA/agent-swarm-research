# Independent audit of high-precision fractional potential-flow optimization

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`, independent of
the author and the other reviewer.

Reviewed: [the fractional-law investigation](potential-flow-fractional-additive-investigation.md),
including its final extension to a fixed finite family of rational exponents
in `(1,3)`, against the existing nomination-face, joint-resistance,
polynomial-law, and fixed-core optimization arguments.

**Verdict: PASS.** The proposed polynomial bit-complexity result for additive
pressure and edge-flow optimization follows under the stated assumptions.
The rational near-optimal input guarantee also passes. This review verifies
the mathematics and construction; it does not establish literature novelty.
Positive rational approximation of fractional powers is prior work.

## Integral approximation and the endpoint zero

For `alpha=1/4`, the integral is finite for every positive `t`, and substituting
`s=t u` gives the stated homogeneity. At `t=0`, its integrand is identically
zero on the integration domain `s>0`; the identity holds there directly.
The lower-tail bound follows by bounding the fraction by one. The upper-tail
bound follows by bounding it by `t/s<=1/s`. Thus the two tail constants in
(A) are valid uniformly on the closed interval `[0,1]`.

On the closed disk of radius one about `3/2`, the real part of `u` is at
least `1/2`. The principal power is analytic in a neighborhood of this disk,
`|u^(-3/4)|<=2^(3/4)<2`, and

```
|t/(t+2^k u)| <= t/(t+2^(k-1)) <= 1.
```

There is therefore no pole approaching the disk when `t` tends to zero.
Cauchy's coefficient estimate bounds the Taylor remainder after degree
`2n-1`, on the real interval at distance at most `1/2` from the center, by
`4*2^(k/4)*2^(-2n)`. Gauss exactness, positive weights with sum one, and
interval length one make the quadrature error at most twice this remainder.
Summing the `2L` panels gives the displayed, deliberately loose, term
`16L*2^(L-2n)`. Its use of `L` rather than `L/4` only weakens the bound.

For example, with `p>=1`, choose `L=4(p+5)` and

```
n = ceil((L+p+log2(64L))/2).
```

The quadrature term is at most `2^(-p)/4`, and the two tails together are
less than `2^(-p)/4`. Reserving the remaining error for coefficient rounding
gives an explicit polynomial schedule. Increasing `p` by a fixed constant
absorbs any desired normalization/error-allocation convention.

## Rational coefficients and normalization

The Gauss nodes are roots of rational Legendre polynomials of polynomial
degree and coefficient height. Their standard weights are positive algebraic
expressions in these roots. Fixed rational powers preserve polynomial
algebraic encoding length. Root isolation and rational interval arithmetic
therefore supply prescribed absolute precision in polynomial bit time.

This constructive step also has a direct primary reference:
[Johansson and Mezzarobba (2018)](https://marc.mezzarobba.net/ecrits/JohanssonMezzarobba_Legendre_v3_2018.pdf).
Their paper gives the weight formula and polynomial exactness, rigorous
node/weight computation, and polynomial bit bounds. Exact evaluation of a
transcendental normalization constant is unnecessary here.

For a direct rounding bound, write the number of fractions as `M=2Ln`.
Before rounding, `s>=2^(-L)` and `a<=2^(L+2)`. With absolute coefficient
error at most `2^(-h)` and `h>=L+1`, the interpolation segment used in a
mean-value estimate has `s>=2^(-L-1)` and `a<=2^(L+3)`. Consequently the
uniform total perturbation is bounded by

```
M*(1+2^(2L+4))*2^(-h).
```

Taking `h=p+2L+O(log M)` is sufficient. Very small positive weights cause
no obstruction: a positive dyadic upper approximation obtained from a
rigorous enclosure stays positive and has the same absolute accuracy after
allowing a constant factor. No polynomial lower bound on a weight's
numerical value is required for this step.

On `[1,2]`, the integrand defining `I_alpha(1)` is at least `1/6`, giving
the claimed lower bound. If the rounded quadrature has absolute error
`zeta<=1/12`, then `Q_R(1)>=1/12`, and

```
|Q_R(t)/Q_R(1)-t^alpha|
 <= (zeta+t^alpha*zeta)/Q_R(1) <=24*zeta.
```

The normalization preserves positivity, monotonicity, and the value zero
at zero. It also gives `R(1)=1`, hence `0<=R(t)<=1` on `[0,1]`.

## Constitutive laws and polynomial encoding

Choosing a power of four `T>=max(1,B)` makes `S=sqrt(T)` rational and gives
the exact scaling identity `S*x*(x^2/T^2)^(1/4)=phi(x)`. Thus the claimed
error `24SB*zeta` is correct. Every rational term is a positive multiple
of `x^3/(x^2+c)`, with `c>0`. Its derivative is nonnegative and vanishes
only at zero. The sum is strictly increasing on the whole real line, smooth,
odd, and unbounded in both directions. Its primitive is strictly convex
and grows superlinearly, giving existence and uniqueness of physical flows
by the established energy argument.

Positive denominator factors remain positive after substituting affine
core flows. The product of polynomially many positive quadratic factors
has polynomial degree and coefficient bit length. Dense expansion in a
fixed number of core variables has polynomial monomial count. These facts
hold even though the numerical coefficients can be large or small.

Explicit sensitivity bounds can be simpler than general rational interval
bounds. Writing the unnormalized coefficients as `a_i` gives

```
|psi(x)| <= S*B                         for |x|<=B,
|psi'(x)| <= 9*S*sum_i(a_i)/(8*Q_R(1))  for all real x.
```

The second inequality follows from
`z(z+3)/(z+1)^2<=9/8` for `z>=0`. Both bounds have polynomial rational
encoding length. The case `B=0` is a direct zero-flow computation and can
be removed before formulas that divide by an error scale involving `B`.
An edgeless connected graph is likewise trivial.

## Fixed-core optimization and rational recovery

The nomination-face argument extends to these laws because adding `rho*x`
makes the derivative strictly positive, while compactness and uniqueness
justify the zero-smoothing limit. The finite face family is independent of
the chosen resistance vector. Holding the resistances fixed at a joint
optimizer therefore transfers the same face theorem to joint optimization.

Conservation makes each flow affine in the bounded-dimensional local core.
Clearing positive denominators in cycle equations creates no false real
solutions and preserves linear dependence on resistance leaves. The count
of aggregate equations stays bounded by the block cycle rank. For a pressure
objective, adding one core value variable and its denominator-cleared
defining equation preserves these fixed dimensions. Multiplying the objective
itself by its denominator would be invalid; the proposed construction does
not do that.

The original fixed-core theorem is stated for fixed degree. Its proof also
gives polynomial complexity when densely encoded degree grows and the core,
leaf, and aggregate dimensions remain fixed: determinants have bounded
size, sign-condition enumeration and real-algebraic optimization have
fixed-dimensional degree exponents, and all intermediate dense polynomial
representations have polynomial size. This is the same growing-degree
extension independently checked in the polynomial-law review. It is
essential here and has not been replaced by an unjustified fixed-degree
invocation.

Explicit physical-flow bounds give compact core boxes; a rational path sum
using `|psi|<=SB` bounds the extra pressure-value variable. Independent block
optimal values are approximated separately and summed as rational intervals.
They need not be represented in a common algebraic field. Local algebraic
optimizer coordinates can be refined and recovered inside small rational
boxes using the existing electrical Lipschitz estimates. Rational LP
intersects the nomination boxes with exact balance; resistance coordinates
are rounded inside their original intervals. This preserves input feasibility
without claiming that the associated physical flow is rational.

## Uniform physical error

For two states with the same nominations, their flow difference is a
circulation. Its inner product with each potential gradient is zero,
proving the displayed energy identity. For the signed power with exponent
`3/2`, the smallest constitutive increment over an interval of length `h`
occurs when the interval is centered at zero. It equals `2^(-1/2)h^(3/2)`.
The weaker rational coefficient `1/2` is therefore valid for all signs.

Let `D` be the maximum coordinate flow difference. Retaining its contribution
in the nonnegative left side and bounding the right side by
`m*beta_U*delta*D` gives (C). When `D>0`, division by `D` is valid; when
`D=0`, the result is immediate. Choosing
`delta<=beta_L*eta^2/(2m*beta_U)` gives `D<=eta^(4/3)<=eta` for `eta<=1`.
This deliberately stronger rational accuracy avoids fractional tolerance
powers. The derivative bound for the original law and a simple path sum
then give (D), uniformly throughout the whole uncertainty set.

If the original and surrogate objectives differ by at most `tau` uniformly,
an `xi`-optimal surrogate input is `(2tau+xi)`-optimal for the original
objective. A certified surrogate optimum interval expands by `tau` at
each endpoint. Allocating fixed fractions of the requested tolerance to
these terms and rational input recovery requires only polynomially many
precision bits. The same statements apply to minima by changing signs.

## Edge-flow objective and input rounding

Starting with an actual surrogate edge-flow optimizer is necessary when
resistances vary; a pressure optimizer alone would not suffice. The proposed
section 5 correctly makes this distinction. Uniform flow error `eta` gives
an original-law edge-flow optimality loss at most `2eta` before rounding.

For original-law states at two nearby inputs, the endpoint equations give

```
beta_e*|phi(x)-phi(y)|
 <= |D-D'|+|beta_e-gamma_e|*|phi(y)|.
```

Together with strong monotonicity and `|phi(y)|<=N`, this proves the stated
inverse Hölder bound. The endpoint-potential Lipschitz coefficient for
nomination changes can use the objective edge itself as the comparison
path, giving `beta_upper_e*M`. The resistance coefficient follows from the
unit adjoint current bound and `|phi|<=N`. Smoothing and passage to the
limit require no positive lower bound on the original derivative.

For a desired flow rounding error `theta<=1`, making the right side of the
inverse estimate at most `theta^2` suffices, since
`theta^(4/3)<=theta`. The rational isolating precision therefore has
polynomial bit length. Adding this loss to `2eta` proves rational
near-extremal input recovery without computing the original algebraic
physical state and without an inverse derivative bound for the surrogate.

## Fixed rational exponents and heterogeneous laws

The appended extension to any fixed finite family of rational
`q in(1,3)` also passes. Set `alpha=(q-1)/2`. Both integral tail bounds decay
exponentially with the panel cutoff, with constants depending on the fixed
family. The same analytic disk works. On `[1,2]`,
`u^(alpha-1)/(1+u)>=1/6`, so the normalization bound remains valid.
Choosing the scale exponent divisible by the denominator of `q-1` makes
`T^(q-1)` rational with polynomial bit length.

The centered-interval calculation now gives the sharp scalar factor
`2^(1-q)>1/4`. Therefore the safe factor `1/4` is uniform for the entire
range. The rational bounds `M=3*max(1,B)^2` and
`N=B*max(1,B)^2` dominate the derivative and the law. For heterogeneous
exponents, retain the edge attaining the maximum difference, with exponent
`q_e`, in the energy sum. Then

```
D^(q_e) <=4m*beta_U*delta/beta_L.
```

With `delta<=beta_L*eta^3/(4m*beta_U)`, the assumption `D>eta` contradicts
this inequality: if `D<=1`, then `D^(q_e)>eta^3` because `q_e<3`; if
`D>1`, then `D^(q_e)>1>=eta^3`. The same cubic tolerance choice handles
inverse Hölder input recovery. All required accuracy exponents remain
fixed. The warning about arbitrary input exponents approaching the
endpoints is necessary for this particular dyadic construction.

## Scope and source credit

[Bonito and Pasciak's primary paper](https://arxiv.org/abs/1307.0888)
already supplies positive Gaussian quadrature on dyadic panels and positive
rational approximants with exponential precision convergence. Its inverse
power approximation, after `lambda=1/t`, has exactly the positive fraction
form used here and extends continuously to zero. The network optimization
composition and the rational bit model must be distinguished from that
established approximation mechanism.

This audit supports additive value intervals and rational near-optimal
nomination/resistance inputs for fixed maximum block cycle rank. It does
not support exact threshold comparison, a strongly polynomial bound, or
fixed-parameter tractability in block rank. Physical capacities or potential
restrictions cannot be silently added to the extremum subproblems. The
existing exact-comparison arithmetic barrier is consistent with this
additive theorem.
