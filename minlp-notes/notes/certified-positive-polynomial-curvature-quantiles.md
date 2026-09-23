# Certified integration and quantiles of positive-polynomial curvature

Date: 2026-09-05. Author: `potential_flow_review`. Status: two full independent analytical and bit-complexity audits passed: [first](review-compiled-curvature-quantile-precision.md), [second](review-compiled-curvature-quantile-precision-second.md). The quadrature and root-isolation tools are established; novelty of any resulting integer-precision theorem is a separate question.

## Claim and input model

Let `f` be a densely encoded rational polynomial whose coefficients on powers of degree at least two are nonnegative. Arbitrary rational affine terms are allowed. Let `epsilon>0` be rational, put

```
H(x)=f''(x)/epsilon,
rho(x)=min(sqrt(H(x)),(1-x)H(x)),
F(x)=integral_0^x rho(t)dt,
M=F(1).
```

There are certified algorithms with the following outputs:

1. Given rational `x in [0,1]` and positive rational `zeta`, compute a rational approximation to `F(x)` with absolute error at most `zeta`.
2. If `H` is nonzero, given rational `theta in [0,1]` and positive rational `eta`, compute a dyadic `q_theta in [0,1]` with absolute error at most `eta` from the unique solution of `F(q)=theta M`. The endpoint outputs are exactly zero and one.

Both algorithms have bit complexity polynomial in the dense polynomial encoding, the encoding of `epsilon`, the query encoding, and the requested precision bits. In particular their dependence on reciprocal accuracy is logarithmic. Their output lengths have the same polynomial bound. This is not a sparse binary-degree claim.

The second algorithm is stronger than mass-accurate quantiles alone. The final compiled-knot formulation can use a simpler mass-accuracy stopping rule; that formulation remains separate from this analytical lemma.

If `H` is identically zero, the curvature measure is zero and `f` is affine. This case is recognized exactly and requires no integration or quantile inversion. For nonzero `H`, all its coefficients are nonnegative and `H(x)>0` on `(0,1]`, so `rho(x)>0` on `(0,1)`. Consequently `F` is continuous and strictly increasing.

## 1. Rational bounds and branch isolation

Let `d=deg H`, `d_0=max(1,d)`, and define the rational bound

```
U=max(1,H(1)).
```

Then both `rho` and `sqrt(H)` are at most `U` on `[0,1]`. Also `H'(x)<=d H(1)<=d U`. All these constants have polynomial binary encoding length.

It is enough to consider `0<zeta<=1`; replace a larger request by one. Choose an integer `J>=1` such that

```
2^(-J)<=zeta/(16U).
```

Ignore `[0,2^(-J)]`. Its contribution to every prefix integral is at most `zeta/16`. The number `J` is `O(log U+log(1/zeta)+1)`; its potentially small physical cutoff therefore has polynomial bit length.

For `x>0`, the square-root branch is the smaller branch exactly when

```
P(x)=(1-x)^2 H(x)-1>=0.
```

The polynomial `P` has degree at most `d+2` and is not identically zero because `P(1)=-1`. Clear its rational denominators and take its square-free part. Isolate its distinct real roots in `[0,1]` in disjoint rational intervals of width at most

```
zeta/[16U(d+3)].
```

Removing these intervals loses at most another `zeta/16` of density mass. Rational roots can be retained as singleton intervals. Roots outside the cutoff or prefix query can simply be clipped away; endpoint sets have zero integral.

On each remaining rational interval, the sign of `P` is constant and is determined by a rational test point. Thus the density is either the polynomial `(1-x)H(x)`, which can be integrated exactly, or `sqrt(H(x))`. Multiple roots and tangencies do not cause an unresolved branch decision: the square-free roots are removed before the sign tests.

The required root isolation and refinement are polynomial in degree, coefficient length, and requested endpoint precision. A specific primary bound is [Sagraloff and Mehlhorn, Theorem 36](https://arxiv.org/pdf/1308.4088), which gives polynomial bit complexity for refining the real roots of an integer polynomial to intervals of width `2^(-kappa)`. Standard rational square-free preprocessing preserves polynomial encoding length.

## 2. A polynomial-size analytic panel cover

Partition each dyadic interval

```
[2^(-j-1),2^(-j)],   j=0,...,J-1,
```

into `T=16d_0` equal subintervals. Intersect this grid with the branch intervals and the desired prefix `[0,x]`. There are polynomially many resulting intervals, all with rational endpoints of polynomial encoding length. Subdivision at branch boundaries adds only polynomially many pieces; it does not enumerate combinations of roots.

Consider any retained interval `[a,b]` on the square-root branch. Let `ell=b-a>0` and `c=(a+b)/2`. Because it lies inside one of the subintervals of a dyadic interval, `ell/c<=1/(16d_0)`. On the complex disk `|z-c|<=ell`, write `z=c(1+w)`, so `|w|<=1/(16d_0)`.

For every monomial degree `k<=d`,

```
|arg((1+w)^k)|<=1/8,
|(1+w)^k|<=exp(1/16)<2.
```

The first follows, for example, from `|arg(1+w)|<=2|w|` in this disk. All nonzero terms of `H(z)` therefore lie in a fixed open right-half-plane sector. Positive coefficients prevent cancellation across the imaginary axis: `Re H(z)>0`. Also

```
|H(z)|<=2H(c)<=2H(1),
|sqrt(H(z))|<=2U.
```

The principal square root of `H` is consequently holomorphic throughout the disk and agrees with the positive real square root on the interval. This proves the analytic neighborhood explicitly. It does not require isolating complex roots or assuming a uniform minimum value of `H` at zero.

The role of dense degree is visible: `T=O(d)` controls the angular variation of every monomial. Replacing this by a polynomial in `log d` has not been established.

## 3. Exponentially accurate positive quadrature

On `[a,b]`, the Taylor polynomial of `sqrt(H)` at `c`, truncated after degree `2q-1`, has uniform error at most

```
4U*4^(-q),
```

because the integration interval has radius `ell/2` while the analytic disk has radius `ell`. An order-`q` Gauss-Legendre rule has positive weights summing to `ell` and is exact through degree `2q-1`. Comparing the integral and quadrature against that Taylor polynomial therefore gives an error at most

```
8U*ell*4^(-q).
```

The square-root intervals have total length at most one. Thus their combined quadrature error is at most `8U*4^(-q)`, independent of their number. Choose

```
q=ceil[(1/2)log_2(128U/zeta)].
```

The total analytic quadrature error is then at most `zeta/16`. Positivity and exactness of Gaussian quadrature are standard; see [NIST DLMF Section 3.5(v)](https://dlmf.nist.gov/3.5#v). The geometric-series error bound above is included to make all dependence on coefficient size and requested accuracy explicit.

## 4. Certified rational evaluation of the quadrature

The order `q` is polynomial in the input and precision lengths. Its reference Gaussian nodes are roots of a rational polynomial of degree `q`, and can be isolated to polynomial precision using the same univariate root tools. Affine maps take these node intervals into the rational interval `[a,b]`.

The Gaussian weights can be approximated by positive rationals with relative error at most `zeta/(64U)`. A complete polynomial-conditioning justification was already supplied in [the positive rational Stieltjes lemma](positive-rational-stieltjes-power-approximation.md): for the mapped length-one weights,

```
w_i=1/[(1-r_i^2) P_q'(r_i)^2],
1/(q H_q)^2<=w_i<=1,
H_q=(q+1)(2q)!.
```

The denominator is at least one and all polynomial derivatives have explicit coefficient bounds. Only polynomially many precision bits are needed to preserve positivity and the relative weight guarantee. Multiplying by the rational interval length changes no relative-error requirement.

Function values at the exact algebraic nodes can be enclosed without forming a joint algebraic field. Evaluate `H` at rational endpoints of each node interval; its nonnegative coefficients make these valid value bounds. The derivative bound `H'<=dU` controls their difference. The elementary inequality

```
sqrt(v)-sqrt(u)<=sqrt(v-u),  0<=u<=v,
```

shows that polynomially many node precision bits suffice even if `H` is very small. For example a node interval of width at most `O(zeta^2/(d_0 U))`, together with rational square-root endpoint bounds, supplies an absolute function-value error at most `zeta/64`. Positive rational square-root bounds themselves follow by ordinary bisection with rational squared comparisons.

Summing the positive quadrature weights bounds the effect of these errors over an interval of length `ell` by

```
ell*[zeta/64+(1+zeta/(64U))*zeta/64] <ell*zeta/16.
```

The combined numerical evaluation error is therefore at most `zeta/16`. The polynomial branches are integrated by exact rational antiderivatives. Their evaluations and sums have polynomial bit length because degree and endpoint encodings are polynomially bounded. Denominator products across polynomially many rational summands add, rather than multiply, their bit lengths.

Ignoring the removed regions, summing the rational polynomial integrals and rational quadrature values, and enclosing the omitted nonnegative mass now gives a certified rational estimate. The total absolute error is at most

```
zeta/16 + zeta/16 + zeta/16 + zeta/16 = zeta/4,
```

from the cutoff, root neighborhoods, analytic quadrature, and numerical quadrature, respectively. This leaves slack relative to the claimed requested error `zeta`. A rational interval with the stated error guarantee can be returned as well.

Every loop count is polynomial: the number of root neighborhoods is at most `d+2`, the grid has `16d_0 J` subintervals, and each quadrature order is `O(log U+log(1/zeta))`. All exact arithmetic is on numbers of polynomial binary length. This proves the integration claim.

## 5. A polynomial inverse modulus for input-accurate quantiles

Suppose `H` is nonzero, and fix any positive coefficient `a` of a monomial `a*x^m`, `m<=d`. Replace a requested input error greater than `1/2` by `1/2`, so it suffices to consider `0<eta<=1/2`. Define positive rationals

```
h_0=a*(eta/4)^m,
kappa=(eta/4)*min(1,h_0).
```

On `[eta/4,1-eta/4]`, `H(x)>=h_0`. Both branches of the density are therefore at least `kappa`. Every interval of length `eta` in `[0,1]` contains a middle subinterval of length `eta/2` lying in that interior range. Its density mass is consequently at least

```
eta*kappa/2.                                      (A)
```

The bit length of `kappa` is polynomial in coefficient size and `d*log(1/eta)`. This is where dense degree is again sufficient: even a high-order zero at the left endpoint has an explicit inverse modulus with polynomial precision cost.

Let `theta` be an interior rational quantile parameter. Compute `M` and each queried `F(s)` to absolute error at most

```
mu=eta*kappa/64.
```

At a dyadic bisection point `s`, form `Ghat=Fhat(s)-theta*Mhat`. Its error relative to `F(s)-theta M` is at most `2mu`. If `Ghat>2mu`, update the upper root bracket; if `Ghat<-2mu`, update the lower bracket. Otherwise the true mass difference has magnitude at most `4mu<eta*kappa/2`. By (A), this implies that `s` is within input distance `eta` of the true quantile, and permits safe termination.

If there is no ambiguous comparison, after `ceil(log_2(2/eta))` steps the bracket is small enough to return its midpoint. Endpoints `theta=0,1` are exact. All outputs can be padded to one common dyadic precision. The quantile-index encoding affects rational comparisons only; no loop is repeated `1/theta` times.

The integration algorithm at precision `mu` is polynomial because `log(1/mu)` is polynomial in the original input and requested input precision. This proves the quantile claim without requiring exact comparison between an algebraic-function integral and a rational multiple of its total.

## Consequences and limits

For an indexed family `theta=k/2^L`, the algorithm is a polynomial-time random-access knot procedure with `L` input bits and common dyadic output precision. It can therefore be passed to the separately reviewed circuit compiler. Choosing tolerances, evaluating `f` at those knots, and proving a final graph band and integer-count bound are separate steps and are not silently included in this lemma.

The positivity of the polynomial coefficients supplies the uniform complex sector. An arbitrary polynomial merely nonnegative on `[0,1]` is outside this proof. Sparse binary-encoded huge degrees are also outside its complexity claim. The construction never computes an exact symbolic antiderivative of the square-root branch, nor compares such transcendental values exactly.

## Reproducible numerical support

[`check_curvature_integral_quadrature.py`](../code/quadratic_rank/check_curvature_integral_quadrature.py) checked constant curvature, a monomial with two rational branch crossings, and a positive-coefficient mixture with a nonpolynomial square-root branch. It passed 12 cumulative-integral comparisons across 1,905 integration panels, with maximum error-to-requested-tolerance ratio `0.015625`. Constant-curvature reference integrals were also compared against their exact elementary formula.

The checker uses exact rational root isolation for its branch intervals and exact rational integration on polynomial branches. Its Gaussian nodes, square-root quadrature values, and independent reference integrals use high-precision numerical arithmetic. It supports the construction but does not implement or replace the certified interval evaluation and uniform proof above.
