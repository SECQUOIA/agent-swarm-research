# Certified curvature integration without coefficient positivity

Date: 2026-09-05. Author: `potential_flow_review`. Status: two full independent proof and bit-complexity audits passed: [first](review-compiled-convex-polynomial-hybrid-precision.md), [second](review-compiled-convex-polynomial-hybrid-precision-second.md). The method uses classical polynomial root separation, Taylor certificates, and adaptive Gaussian quadrature. Its intended contribution is the resulting extension of the reviewed curvature-quantile formulations, not a priority claim for those numerical tools.

## Statement

Let `f` be any densely encoded rational polynomial satisfying

```
g=f''>=0 and g is nondecreasing on [0,1].
```

Its coefficients may have either sign. For positive rational `epsilon`, put

```
H=g/epsilon,
rho(x)=min(sqrt(H(x)),(1-x)H(x)),
F(x)=integral_0^x rho(t)dt,
M=F(1).
```

The certified integration and inverse-quantile conclusions of [the positive-coefficient lemma](certified-positive-polynomial-curvature-quantiles.md) remain valid: cumulative integrals can be approximated to prescribed absolute error, and normalized quantiles to prescribed absolute input error, in polynomial bit time in the dense input and requested precision lengths. Outputs are rational, and the quantile outputs may use one common dyadic precision with exact endpoints.

The only new difficulty is obtaining polynomially many analytic integration panels without positive coefficients. A uniform grid based on the smallest complex-root distance could have exponentially many intervals and is **not** used. The adaptive construction below has polynomial size even when a complex root lies exponentially close to the real integration interval.

If `H` is zero, the function is affine and the density vanishes. Otherwise monotonicity and nonnegativity imply

```
H(x)>0 for every x in (0,1].
```

Indeed, a zero at a positive point would force `H` to vanish on a nonempty interval, hence identically as a polynomial. In particular `H(1)>0`.

The hypotheses themselves are polynomially checkable by exact univariate sign tests for `f''` and `f'''` on `[0,1]`. This validation is optional when the class is supplied as a promise. Sparse binary-encoded huge degrees are not covered.

## 1. Retain the cutoff and branch isolation

Set `d=deg H`, `d_0=max(1,d)`, and `U=max(1,H(1))`. The density and the square-root branch are bounded by `U` on `[0,1]`. For an integral accuracy request `0<zeta<=1`, choose the dyadic cutoff `lambda=2^(-J)` with

```
J>=1,
lambda<=zeta/(16U).
```

Omitting `[0,lambda]` costs at most `zeta/16`. The branch-crossing polynomial remains

```
P(x)=(1-x)^2 H(x)-1.
```

It is nonzero, has degree at most `d+2`, and is a general rational polynomial; its root-isolation argument never required coefficient positivity. Remove disjoint rational root neighborhoods of total length at most `zeta/(16U)`. On the remaining intervals a rational sign test identifies the polynomial branch or the square-root branch.

The polynomial branch is still integrated exactly. The remaining task is a polynomial-size certified analytic cover of `[lambda,1]` for `sqrt(H)`.

## 2. An exact local Taylor certificate

For an interval `I=[a,b] subset [lambda,1]`, let `ell=b-a` and `c=(a+b)/2`. Expand exactly over the rationals,

```
H(c+t)=sum_(k=0)^d h_k(c)*t^k,
h_0(c)=H(c)>0.
```

Accept the interval if

```
T(c,ell):=sum_(k=1)^d |h_k(c)|*ell^k <= H(c)/2.       (1)
```

Otherwise bisect it. The expansion, absolute values, and comparison are exact rational operations. When (1) holds, every complex point with `|z-c|<=ell` satisfies

```
|H(z)-H(c)|<=H(c)/2,
Re H(z)>=H(c)/2>0,
|sqrt(H(z))|<=sqrt(3H(c)/2)<=2U.
```

Thus the principal square root is holomorphic on a disk whose radius is twice the integration interval's half-length. This is precisely the neighborhood and modulus bound used by the earlier Gaussian/Taylor error proof.

The test is sufficient, not necessary. Its conservative character is harmless only after proving that the adaptive bisection tree has polynomial size; that proof follows next.

## 3. Every failed interval is close to a complex root

For `d>=1`, list the roots `alpha_1,...,alpha_d` of `H` with multiplicity. They need not be computed. Polynomial factorization gives the exact identity

```
H(c+t)/H(c)=product_(j=1)^d [1+t/(c-alpha_j)].
```

If every root has distance at least `8d*ell` from `c`, the triangle inequality for the elementary-symmetric coefficients gives

```
T(c,ell)/H(c)
 <=product_j [1+ell/|c-alpha_j|]-1
 <=(1+1/(8d))^d-1
 <=exp(1/8)-1<1/2.
```

Consequently failure of (1) implies that some root is within `8d*ell` of the center. In particular the center lies within `8d*ell` of that root's real part.

At one depth of the binary subdivision of the original interval `[lambda,1]`, all intervals have the same length `ell` and their centers have spacing `ell`. A real window of length `16d*ell` contains at most `16d+2` such centers. There are at most `d` roots, so there are at most

```
d*(16d+2)
```

failed intervals at any depth. Counting roots with multiplicity only weakens this upper bound. For a constant nonzero polynomial, (1) succeeds immediately.

This argument limits the number of active branches. A lower bound on root distance is still needed to bound the tree depth, but it will enter logarithmically rather than through a uniform mesh size.

## 4. A polynomial depth bound from integer root separation

Clear the denominators of `H` to obtain a nonzero integer polynomial `H_int`, and let

```
P_0(x)=H_int(x)*x*(x-1),
n=deg P_0=d+2.
```

Choose an integer `T>=1` such that all coefficients of `P_0` have magnitude at most `2^T`. The values `n,T` are polynomially bounded in the dense input encoding. The artificial factors ensure that zero and one occur among its distinct roots.

Let `Q` be the primitive integer square-free part of `P_0`, with positive leading coefficient. It is not necessary to compute `Q` for the adaptive test. It has degree at most `n`, and its leading coefficient divides the leading coefficient of the primitive part of `P_0`. A Cauchy bound places every root of `P_0` in the disk of radius `2^(T+1)`. Expanding the roots of `Q` therefore bounds every coefficient of `Q` by `2^B`, where the explicit loose choice

```
B=(n+1)T+2n
```

suffices. This also shows directly why passing to the square-free part has only polynomial height cost.

The discriminant of `Q` is a nonzero integer. For any selected pair of its roots, bound every other root difference by `2^(T+2)` and its leading coefficient by `2^B` in the discriminant product. This gives the uniform, deliberately weaker separation bound

```
|alpha-beta|>=sigma,
sigma=2^(-(B+2)n^2),                               (2)
```

for distinct roots of `Q`. The exact sharper exponent is unnecessary. The discriminant contains one squared factor for the selected pair, at most `n(n-1)/2-1` other squared difference factors, and a leading-coefficient power at most `2n-2`; all are covered by (2).

Now consider roots of `H` relative to `[lambda,1]`. There are no real roots in `(0,1]`. A real root at or below zero is at distance at least `lambda`. A real root above one is separated from the root one of `Q` by at least `sigma`. A nonreal root and its conjugate are distinct roots of `Q`, so its imaginary part has magnitude at least `sigma/2`. It follows that every root of `H` has distance at least

```
rho_*=min(lambda,sigma/2)
```

from the interval.

At a depth `K` with `2^(-K)<=rho_*/(8d_0)`, every interval passes (1). Such `K` is polynomial in `d,T,J`. Together with the per-depth failure bound, this gives `O(d_0^2 K+1)` nodes in the entire adaptive tree. In particular, exponentially small complex-root distances do not produce exponentially many intervals.

All accepted endpoints are dyadic rationals of polynomial encoding length. Exact Taylor coefficients at their centers have polynomial bit length: the degree, center encoding, rational coefficient encoding, and binomial coefficients are polynomially bounded. Thus both the number of tests and the bit cost of each test are polynomial.

## 5. Intersections and certified integration

Construct this adaptive cover before cutting at the branch neighborhoods and query endpoint. If `I' subset I` is a retained subinterval of an accepted interval, with center `c'` and length `ell'`, then

```
|c'-c|+ell' <= (ell+ell')/2 <= ell.
```

Its radius-`ell'` disk is therefore contained in the original accepted disk. The analytic certificate and the bound `|sqrt(H)|<=2U` survive every intersection. There is no need to rerun the adaptive algorithm separately for every branch component.

The prior integration proof now applies with the same constants. An order-`q` Gaussian rule on a retained interval has analytic error at most `8U*ell'*4^(-q)`, and the lengths sum to at most one. Taking `q=O(log U+log(1/zeta))` makes this error at most `zeta/16`. Positive rational weight approximation has the same polynomial conditioning as before.

Only the function-value enclosure bound needs adjustment. With possibly negative coefficients, use

```
V=max(1,sum_(k=1)^d k*|H_k|)
```

as a rational derivative bound on `[0,1]`. Monotonicity means that exact rational evaluations of `H` at the endpoints of a rational node interval enclose its value at the Gaussian node, even though coefficientwise interval monotonicity is unavailable. Their difference is at most `V` times the node interval length. The square-root inequality `sqrt(v)-sqrt(u)<=sqrt(v-u)` then gives polynomial node and square-root precision exactly as before. No lower bound on `H` is needed for this evaluation step.

The cutoff, root neighborhoods, analytic quadrature, and numerical evaluation can each use the same `zeta/16` budget as in the reviewed lemma. The polynomial branch remains an exact rational antiderivative calculation. All output arithmetic and all total encoding bounds are polynomial in the dense input and requested precision. This proves certified cumulative integration for signed-coefficient monotone curvature.

## 6. Input-accurate inverse quantiles also extend

For desired input error `0<eta<=1/2`, replace the positive-monomial lower bound from the earlier proof by the exact rational number

```
h_0=H(eta/4)>0,
kappa=(eta/4)*min(1,h_0).
```

Its encoding length is polynomial in the dense polynomial input and `log(1/eta)`, even if cancellation makes the value small. Monotonicity gives `H(x)>=h_0` on `[eta/4,1-eta/4]`, so both density branches are at least `kappa`. Every interval of input length `eta` therefore carries density mass at least `eta*kappa/2`.

The same cumulative-integral bisection, using accuracy `eta*kappa/64` and stopping safely when the comparison interval contains zero, returns a dyadic input within `eta` of the exact normalized quantile. Larger requested errors can first be replaced by `1/2`. Endpoints are exact and a common output precision is available.

This step uses only positive exact rational evaluation at an interior point and monotonicity, not positivity of the coefficients. For the final mass-quantile compiler, the lower-density argument is unnecessary, but it preserves the stronger standalone inverse result.

## Formulation consequences and review scope

The geometric curvature-mass theorem already assumes only nonnegative nondecreasing second derivative. Replacing its positive-coefficient integration routine by this algorithm therefore removes coefficient positivity from the scalar compiled-knot construction without changing its geometric constants. The same substitution applies to separately proved separable formulations whose scalar components satisfy these curvature hypotheses; it does not create a new multivariate geometry argument.

This note proves the analytical and bit-complexity extension used by the [compiled convex-polynomial result](../results/convex-polynomial-compiled-integer-precision.md). The integration lemma itself retains monotonicity of the curvature; the broader formulation uses separately reviewed additional geometry. This note does not cover sparse huge degrees or an uncounted elementary-function oracle. The adaptive Taylor-root argument is an application of classical numerical and algebraic tools, and its literature attribution remains separate.

## Reproducible checks

[`check_signed_curvature_panels.py`](../code/quadratic_rank/check_signed_curvature_panels.py) constructs the adaptive cover using exact rational Taylor tests. Its four examples have nonnegative nondecreasing curvature but negative coefficients, with degrees three, four, and nine and parameters as small as `2^(-40)`. All passed, using 198 accepted panels in total and maximum subdivision depth 21.

The checker also integrates the square-root branch on those panels and compares against an exact elementary reference in one case and independent high-precision quadrature in the other cases. Every approximation passed the requested absolute error `1/1024`. These Gaussian evaluations are numerical support; the panel certificates themselves are exact, and the uniform error and bit-complexity guarantees remain the written proof above.
