# Certified positive rational approximation of a small power

Date: 2026-09-05. Author: `potential_flow_review`, with a parallel derivation by root of the uniform panel bound. Status: two independent full audits passed: [first](review-compact-pure-power-interpolation.md), [second](review-compact-pure-power-interpolation-second.md). The integral representation and Gaussian quadrature are established tools; no novelty is claimed for this approximation lemma by itself.

## Statement

Given an integer `D>=3` and a positive rational `delta`, put `gamma=2/D`. There is a deterministic construction of positive rational numbers `a_k,b_k`, `1<=k<=M`, such that

```
R(t)=sum_(k=1)^M a_k*t/(t+b_k),
R(0)=0,
R(1)=1,
sup_(0<=t<=1) |R(t)-t^gamma|<=delta.
```

The number of terms, the total rational coefficient encoding length, and the construction time are polynomial in `D` and `1+log(1/delta)` for `delta<=1`, together with the rational input encoding length. More explicitly,

```
M=O(D*(1+log(1/delta)+log D)^2).
```

Thus this is polynomial in the dense degree input size, even as `gamma` tends to zero. It is not a claim of polynomial dependence on the binary encoding length of `D` alone. Combining the fractions gives a rational function with numerator and denominator degrees at most `M`, with polynomial coefficient encoding length. The partial-fraction representation is preferable for the intended formulation.

For `D=2`, use the exact identity `t^(2/D)=t` separately. The proof below does not apply to `gamma=1`, where its integral diverges.

## 1. An unnormalized integral avoids trigonometric coefficients

For `0<gamma<1`, define

```
I_gamma(t)=integral_0^infinity [t/(t+s)]*s^(gamma-1) ds,
I_gamma(0)=0.
```

For `t>0`, substitution `s=t*u` gives `I_gamma(t)=t^gamma I_gamma(1)`. In particular the approximation can be normalized at one; there is no need to compute `sin(pi*gamma)`.

Splitting at one yields the useful bounds

```
2 <= 1/(2gamma)+1/(2(1-gamma))
   <= I_gamma(1)
   <= 1/gamma+1/(1-gamma)
   <= D/2+3.
```

The lower integral bound uses `1+s<=2` on `[0,1]` and `1+s<=2s` on `[1,infinity)`. The last upper bound uses `gamma<=2/3`.

Set `epsilon=min(delta,1/4)`, let `p` be the least integer with `2^(-p)<=epsilon`, and let `ell_D=ceil(log_2 D)`. Thus `p>=2`. Choose integer truncation indices

```
L=ceil((D/2)*(p+ell_D+8)),
U=3*(p+8),
N=L+U.
```

Uniformly for `0<=t<=1`, the omitted tails satisfy

```
integral_0^(2^-L) [t/(t+s)] s^(gamma-1) ds
 <=2^(-L gamma)/gamma <=epsilon/512,

integral_(2^U)^infinity [t/(t+s)] s^(gamma-1) ds
 <=2^(-U(1-gamma))/(1-gamma) <=3epsilon/256.
```

Their sum is less than `epsilon/64`. The lower tail explicitly accounts for the small exponent: its truncation index is proportional to `D*(p+log D)`.

## 2. Positive Gaussian quadrature on dyadic panels

For every integer `j=-L,...,U-1`, substitute `s=2^j*v`. The panel integrand on `1<=v<=2` is

```
F_(j,t)(v)=2^(j gamma)*v^(gamma-1)*t/(t+2^j*v).
```

Use the principal power on the right half-plane. On the complex disk `|v-3/2|<=1`, one has `Re(v)>=1/2` and `|v^(gamma-1)|<=2`. For `j<=0`, the remaining prefactor is bounded by one in modulus. For `j>=0`, use

```
|t/(t+2^j*v)|<=2^(1-j)
```

and `gamma<=1`. Therefore `|F_(j,t)(v)|<=4` on that disk, uniformly in `j,t,D`. When `t=0` the integrand is identically zero. Its possible pole for `t>0` lies on the nonpositive real axis, outside the disk.

The Taylor polynomial at `3/2` of degree `2m-1` has error at most `8*4^(-m)` on `[1,2]`, by the Cauchy coefficient bound and a geometric-series remainder. An `m`-point Gauss-Legendre rule on `[1,2]` has positive weights summing to one and is exact through degree `2m-1`. Applying it to this polynomial and bounding the errors in the integral and quadrature sum gives panel error at most

```
16*4^(-m).
```

Take

```
m=ceil((p+ceil(log_2(256N)))/2).
```

The sum of all panel errors is at most `epsilon/16`.

For completeness, positivity and polynomial exactness of Gaussian quadrature do not require an analytic-error theorem. Let its nodes be the roots of the degree-`m` orthogonal polynomial, and integrate their Lagrange cardinal polynomials to define the weights. Dividing a polynomial of degree at most `2m-1` by the orthogonal polynomial proves exactness. Applying exactness to the square of each cardinal polynomial shows that its weight is strictly positive. Applying it to the constant polynomial gives weight sum one. These established Gaussian quadrature properties are also documented in [NIST DLMF Section 3.5(v)](https://dlmf.nist.gov/3.5#v).

Write the common Gaussian nodes and weights as `v_i in (1,2)` and `w_i>0`, `sum_i w_i=1`. The complete quadrature is

```
Q(t)=sum_(j=-L)^(U-1) sum_(i=1)^m A_ji*t/(t+B_ji),
A_ji=2^(j gamma)*w_i*v_i^(gamma-1)>0,
B_ji=2^j*v_i>0.
```

It has `M=Nm` positive terms. The truncation and quadrature bounds give

```
sup_[0,1] |Q-I_gamma| < epsilon/64+epsilon/16=5epsilon/64.
```

Also `Q(t)<=Q(1)<=I_gamma(1)+epsilon/16<=D+4`. This bound on the *values* is useful when rationalizing the terms; a bound on the much larger sum of their numerators is unnecessary.

## 3. Rationalizing nodes and coefficients without losing positivity

Choose the rational relative tolerance

```
tau=epsilon/(128*(D+4))<1/2.
```

Construct positive rational approximations `Ahat_ji,Bhat_ji` satisfying

```
|Ahat_ji/A_ji-1|<=tau,
|Bhat_ji/B_ji-1|<=tau.
```

For any positive term and `t>0`, the ratio of its perturbed and exact values lies between `(1-tau)/(1+tau)` and `(1+tau)/(1-tau)`. Its relative error is therefore at most `4tau`. At `t=0` both values vanish. Positivity now gives, uniformly on the entire closed interval,

```
|Qhat(t)-Q(t)|<=4tau*Q(t)<=epsilon/32.
```

Thus

```
E:=sup_[0,1] |Qhat-I_gamma| <7epsilon/64<epsilon/8.
```

The required relative rational approximations have polynomial construction cost. Here are explicit bounds that avoid a hidden small-weight assumption. Let `P_m` be the usual Legendre polynomial on `[-1,1]`, let `r_i=2v_i-3`, and put

```
H_m=(m+1)*(2m)!.
```

The sum of the absolute coefficients of `P_m` is at most `H_m`, so `|P_m'(r)|<=m H_m` on `[-1,1]`. The Gaussian weight on the length-one interval is

```
w_i=1/[(1-r_i^2)*(P_m'(r_i))^2].
```

Consequently

```
1/(m H_m)^2<=w_i<=1,
2^(-L)<=B_ji<=2^U,
2^(-L)/(2*(m H_m)^2)<=A_ji<=2^U.
```

The lower bound for `A_ji` uses `v_i^(gamma-1)>=1/2` and `2^(j gamma)>=2^(-L)`. The logarithms of all these bounds are polynomial in `L,U,m`. Therefore sufficiently small absolute errors of polynomial binary length guarantee the required relative errors and strict positivity. The factorial bound is deliberately loose; its logarithm is only `O(m log m)`.

The nodes are roots of an explicitly generated rational polynomial of degree `m` and polynomial coefficient encoding length. Certified univariate root isolation refines them in polynomial bit time to any requested polynomial number of bits. The weights can then be computed by rational interval arithmetic using the displayed formula. Its denominator is at least one because `w_i<=1`; together with `|P_m'|<=mH_m`, this also gives `1-r_i^2>=1/(mH_m)^2`. Polynomial derivative bounds therefore control interval evaluation near every node with only polynomially many precision bits. No common number field of all nodes is constructed.

For powers, use

```
A_ji=(w_i/v_i)*(2^j*v_i)^(2/D).
```

Certified intervals for `v_i,w_i`, followed by bisection for a positive `D`th root, compute this expression to the required precision. The root equation is `z^D=(2^j*v_i)^2`. Its inputs stay between explicit positive bounds of polynomial binary length. Raising rational test points to the integer power `D` and comparing with rational interval endpoints takes polynomial time in `D` and the requested bit length. Refinement of the input intervals is polynomial as well, because the expressions have only fixed-depth arithmetic and root operations on explicitly bounded positive arguments. This remains valid for negative `j` of magnitude `O(D*(p+log D))`.

These are standard certified real-algebraic operations in one variable; their polynomial dependence on polynomial degree and coefficient length is consistent with the quantitative real-algebraic bounds summarized in [Basu's survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf). The explicit magnitude bounds above are included to make positivity and the small-`gamma` precision dependence visible.

## 4. Exact endpoint normalization

The rational number `Qhat(1)` is positive. Define

```
a_ji=Ahat_ji/Qhat(1),
b_ji=Bhat_ji,
R(t)=Qhat(t)/Qhat(1).
```

Then every coefficient is a positive rational, `R(0)=0`, and `R(1)=1` exactly. Since `I_gamma(t)/I_gamma(1)=t^gamma` and `I_gamma(1)>=2`,

```
|R(t)-t^gamma|
 <=[|Qhat(t)-I_gamma(t)|+t^gamma*|I_gamma(1)-Qhat(1)|]/Qhat(1)
 <=2E/(2-E)
 <=epsilon
 <=delta.
```

The estimate includes `t=0`; there is no excluded neighborhood depending on `gamma` or the accuracy.

Summing the `M` rational terms at one and dividing their numerators by that sum uses only polynomially many arithmetic operations on polynomial-bit rationals. In the worst case the denominator products add their bit lengths, which remains polynomial in the total coefficient encoding. The same observation bounds coefficients after an optional common-denominator expansion.

Finally, `L=O(D*(p+log D))`, `U=O(p)`, and `m=O(p+log D)`. This proves the claimed degree bound and polynomial construction/encoding bounds. The lemma is therefore suitable when the degree is part of a dense input and only logarithmic dependence on reciprocal approximation error is allowed.

## Use and scope

The target application is the [compact pure-power formulation](../results/positive-pure-power-linear-dimension-precision.md). The approximation lemma adds no integer variables; any integer-count consequence requires a separate formulation proof. Gaussian quadrature and the Stieltjes integral are prior ingredients. The contribution here is an explicit certified rational construction with exact endpoints and uniform parameter dependence as `2/D` approaches zero.

## Reproducible numerical support

[`check_positive_rational_stieltjes.py`](../code/quadratic_rank/check_positive_rational_stieltjes.py) constructs rounded positive rational coefficients and exact rational endpoint normalizers for `D=3,8,32`. It passed 5,776 positive terms and 62 value samples, including zero, one, and points as small as `2^(-2L)`. The largest sampled error-to-tolerance ratio was `0.0004390012`.

The checker computes its intermediate Gaussian nodes at 100-digit floating-point precision rather than implementing certified root isolation. Its positivity and endpoint arithmetic are exact rational checks, but its value samples are numerical support, not a replacement for the uniform analytic and bit-complexity proof above.
