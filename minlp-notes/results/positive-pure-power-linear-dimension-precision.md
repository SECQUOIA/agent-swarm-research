# Compact reciprocal interpolation for pure-power graph precision

Date: 2026-09-05. Status: independently reviewed theorem and construction.

This theorem gives a polynomial-size rational construction attaining a
degree-independent additive integer-count bound for the positive pure-power
family. Its key device is to interpolate a rational approximation of the
inverse power and encode every reciprocal using the existing grid bits.
The formulation proof uses the explicit positive rational approximation
lemma stated next. Both arguments have passed two independent audits.

## Positive rational approximation lemma

For an integer `D>=3` and a positive rational `delta<1/2`, there is an
algorithm, polynomial in `D` and `log(1/delta)` and their encoding lengths,
returning positive rational coefficients `alpha_k,beta_k` such that

```
R(t)=sum_(k=1)^M alpha_k t/(t+beta_k),
R(0)=0, R(1)=1,
sup_(0<=t<=1)|R(t)-t^(2/D)|<=delta.                    (A)
```

The number of terms and the total coefficient encoding length are
polynomial in these parameters. A self-contained [certified Stieltjes approximation proof](../notes/positive-rational-stieltjes-power-approximation.md)
gives `M=O(D(1+log(1/delta)+log D)^2)` terms. The polynomial dependence on `D` is
compatible with dense polynomial input; it does not prove polynomial
complexity for huge degrees encoded sparsely in binary. Positive
coefficients make `R` strictly increasing on `[0,1]`.

For `D=2`, use the exact inverse `R(t)=t` separately. A Stieltjes integral,
dyadic truncation, positive quadrature, rational approximation of its
nodes and weights, and exact normalization at one are the proposed proof
of (A). The supporting note supplies explicit tail, analytic quadrature, rational
rounding, and normalization bounds, with certified coefficient bit lengths.

## The exact interpolation gadget

Fix a rational allocation `0<p<=1`, degree `D>=2`, and set

```
L=ceil[(1/2)log2(1/p)]+2,
h=2^(-L),
delta=p/(16D).
```

Introduce `L` binary variables and a continuous interpolation parameter
`lambda in [0,1]`, with

```
a=sum_(ell=1)^L 2^(-ell) z_ell.
```

Thus `a` ranges over the left endpoints of the uniform `t` grid, including
zero and `1-h`. For each term in (A), introduce nonnegative variables
`v_k^-` and `v_k^+`, bounded above by `1/beta_k`, and impose

```
(a+beta_k)v_k^-=1-lambda,
(a+h+beta_k)v_k^+=lambda.                              (3)
```

These equations are exactly MILP-representable without new integers.
Expand `a` as its binary sum and replace each product `z_ell v_k^+` or
`z_ell v_k^-` by the exact binary-times-bounded-continuous hull. All
remaining terms in (3) are linear. The denominators are positive, so the
equations determine the two reciprocal variables uniquely.

The interpolated inverse coordinate is the linear expression

```
x=sum_k alpha_k[1-beta_k(v_k^-+v_k^+)]
 =(1-lambda)R(a)+lambda R(a+h).                         (4)
```

For `D=2`, replace (3)--(4) by `x=a+h lambda`. Because `R` is strictly
increasing with endpoints zero and one, these grid segments cover every
`x in [0,1]`. No original graph point is lost.

Define also the linearized expression

```
y=a^2+2h a lambda+h^2 lambda
 =(1-lambda)a^2+lambda(a+h)^2.                          (5)
```

The two products are encoded exactly using the same binaries:
`a^2=sum_ell 2^(-ell)(z_ell a)` and
`a lambda=sum_ell 2^(-ell)(z_ell lambda)`. Both `a` and `lambda` are
bounded by one. This takes `O(L)` product auxiliaries and inequalities.
Equations (3)--(5) therefore use `O((M+1)L)` rows and variables and
exactly the original `L` binaries. Their coefficient encoding lengths
are polynomial under (A), even if some `beta_k` are small: the bound
`1/beta_k` has the same polynomial order of bit length.

## Error and graph containment

Let `g(t)=t^(2/D)` and define the comparison coordinate

```
x_0=(1-lambda)g(a)+lambda g(a+h).
```

The uniform approximation in (A) gives `|x-x_0|<=delta`. Both coordinates
lie in `[0,1]`. The reviewed [uniform chord bound](../notes/pure-power-degree-independent-integer-count.md)
for `x^D` gives

```
0<=y-x_0^D<=4h^2.
```

Since `x^D` is `D`-Lipschitz on `[0,1]`,

```
-D delta<=y-x^D<=4h^2+D delta.                         (6)
```

Introduce the approximation variable `q` using the rational band

```
y-(4h^2+D delta)<=q<=y+D delta.                         (7)
```

For every original `x`, choose its segment and interpolation parameter
in (4). Inequality (6) proves that `q=x^D` is admitted by (7). Conversely,
every admitted point satisfies

```
|q-x^D|<=4h^2+2D delta<=3p/8.                          (8)
```

For `D=2`, the exact inverse obeys the same safe bounds with zero actual
approximation error. All constants used in (7) are rational.

## Whole-formulation theorem

Consider the positive pure-power system and unconditional error body in
[the finite theorem](../notes/pure-power-degree-independent-integer-count.md), with
rational dense input and the stated rational strong oracle and radius
bounds. Let

```
D_alloc=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi=-(1/2)log2 D_alloc.
```

Apply the reviewed rational log-product oracle to obtain an exactly
feasible positive rational allocation with product at least
`exp(-1)D_alloc`. Apply (3)--(7) separately to every coordinate and set

```
w_j=l_j^T x+b_j+sum_i c_ji q_i.
```

This contains every exact vector graph point. Equation (8) gives
`|w-f(x)|<=(3/8)Cp`, so unconditionality implies that every admitted
error belongs to `K`. The binary count is

```
p_out=sum_i L_i<=Phi+3r+1/(2ln2).
```

The degree-independent finite lower bound is `p_conv>=Phi-A_r`, with
`A_r<7r/2`. Consequently, using the supporting proof of (A) with its stated rational
complexity, the construction proves

```
p_out<=p_conv+(13r/2)+1.                               (9)
```

Its size and construction time are polynomial in the dense input and
oracle encoding. In particular, there is no additive `sum_i log D_i`
term in its integer-count comparison. There is still a polynomial degree
dependence in its continuous size and construction time.

## Verification and scope

The formulation algebra, reciprocal bounds, error interval, and binary
count are explicit above. The positive rational uniform approximation
lemma (A), including its coefficient bit bounds and exact endpoint
normalization, is proved in the linked support note. The [first independent audit](../notes/review-compact-pure-power-interpolation.md)
and [second independent audit](../notes/review-compact-pure-power-interpolation-second.md)
both passed for that lemma and the complete construction.

The [bounded source audit](../notes/compact-pure-power-reciprocal-interpolation-novelty.md)
credits existing positive-resolvent power approximations, binary product
disaggregation, and logarithmic disjunction methods. It found no matching
whole-formulation degree-independent construction. Publication priority
remains unestablished.

The [exact checker](../code/quadratic_rank/check_pure_power_reciprocal_interpolation.py)
passed 3,348 uniform chord inequalities and 60 reciprocal, endpoint,
and shared-bit identities. Numerical approximation checks do not replace
the uniform analytic error proof in the supporting lemma.

The [rationalized quadrature checker](../code/quadratic_rank/check_positive_rational_stieltjes.py)
passed 5,776 positive rational terms and 62 sampled values for degrees
3, 8, and 32, including values below the truncation scale. Endpoints
were checked exactly. The largest sampled error was below 0.00044 times
the requested tolerance. Its intermediate Gaussian calculations use
high-precision numerics; certified root isolation is supplied by the
proof, so this checker is supporting evidence rather than a uniform
error certificate.
