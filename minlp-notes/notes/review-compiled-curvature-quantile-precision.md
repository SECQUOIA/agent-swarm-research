# Independent audit: compiled curvature quantiles

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS for the complete dense positive-polynomial theorem with `p_out<=p_conv+7`.** This review covers [the compiled quantile construction](compiled-curvature-quantile-precision.md) and its full [certified integration and quantile dependency](certified-positive-polynomial-curvature-quantiles.md).

The formulation was initially conditional on cumulative integration. The completed integration proof was independently audited, closing that dependency. This audit includes the revised seven-bit constant, rather than the earlier eight-bit draft. The result concerns polynomial construction and total rational encoding size for one densely encoded positive polynomial. It does not establish a sparse binary-degree extension or literature novelty.

## Cumulative integration

The normalized curvature polynomial `H` has nonnegative coefficients. If it is nonzero, it is strictly positive away from zero. The rational bound `U=max(1,H(1))` bounds both the density and `sqrt(H)` on the unit interval, and the coefficientwise derivative bound is `H'<=dU` there.

The omitted initial interval contributes at most `zeta/16`. The branch condition follows by comparing nonnegative quantities: for positive `H`, `sqrt(H)<=(1-x)H` is equivalent to `(1-x)^2H-1>=0`. This branch polynomial is not identically zero because its value at one is minus one. Taking its square-free part and isolating all distinct roots handles repeated roots and tangencies. There are at most `d+2` root neighborhoods; their total omitted mass is below `zeta/16` under the stated width bound. Clipping at the query endpoint or cutoff only decreases the loss. Remaining branch decisions use exact signs at rational points.

The cited [Sagraloff–Mehlhorn Theorem 36](https://arxiv.org/pdf/1308.4088) was checked directly. Its integer-polynomial specialization bounds the bit cost polynomially in degree, coefficient bits and requested root-interval precision. Clearing rational denominators and square-free preprocessing preserve polynomial encoding length. Thus close roots do not introduce an unaccounted numerical separation assumption.

Intersecting the `16d_0 J` dyadic subintervals with branch intervals and a prefix query creates only polynomially many intervals. For a retained square-root interval, `ell/c<=1/(16d_0)`. On the complex disk of radius `ell`, the relative coordinate perturbation obeys that same bound. Every monomial of degree at most `d` lies within angle `1/8` of the positive real axis and has modulus at most twice its center value. Positive coefficients therefore put `H(z)` strictly in the right half-plane, with `|H(z)|<=2H(c)<=2H(1)`. The principal square root is holomorphic on the disk and has modulus at most `2U`. This explicitly supplies the analytic neighborhood needed for Cauchy's estimate, including small positive centers close to a high-order zero at the origin.

The ratio between the integration radius and analytic radius is one half. Taylor truncation at degree `2q-1` therefore has error at most `4U*4^-q`; positive Gaussian quadrature doubles this after multiplication by interval length. The resulting error `8U ell 4^-q` sums over lengths, not over the number of panels. The specified order makes the total analytic error at most `zeta/16`. The positivity and polynomial exactness used here match the previously checked [NIST DLMF Gaussian quadrature statement](https://dlmf.nist.gov/3.5#v).

The rational numerical evaluation also has the claimed uniform bound. Reference Gaussian weights have explicit positive lower bounds with polynomial logarithms, from the independently reviewed Legendre coefficient argument. Relative weight error `zeta/(64U)` contributes at most `ell*zeta/64`, because true function values are at most `U`. Absolute function-value error `zeta/64` contributes at most `ell*(1+zeta/(64U))*zeta/64`. Their sum is below `ell*zeta/16`.

For function values, monotonicity of the polynomial supplies valid rational interval bounds at node endpoints. The derivative bound controls the polynomial interval width, and the square-root Hölder inequality controls its image without any positive lower bound on `H`. Choosing a sufficiently small fixed multiple of `zeta^2/(d_0 U)` for node width, and then rational square-root bisection, gives the displayed value precision in polynomial bit time. The big-O width in the note can, for example, be made explicit by assigning half the error allowance to node variation and half to square-root bisection. Small panel lengths do not worsen the required relative precision of mapped weights.

Exact rational antiderivatives handle polynomial branches. Evaluating degree-`d` polynomials at polynomial-bit rational endpoints costs polynomial bit time under dense encoding. Summing polynomially many rational quantities keeps polynomial total bit length. The cutoff, branch neighborhoods, analytic quadrature and numerical quadrature contribute at most `zeta/4` together, leaving the stated slack. All panel counts, quadrature orders and precision requirements are polynomial in the specified input and query lengths. No exact symbolic square-root antiderivative or exact comparison of its values is assumed.

## Stronger input-accurate inverse lemma

The optional stronger quantile result is also valid. For one positive monomial coefficient `a`, the lower bound `H(x)>=a(eta/4)^m` on the specified interior interval makes both density branches at least `kappa=(eta/4)min(1,a(eta/4)^m)`. The central half of any interval of length `eta` lies inside that interior interval, so its mass is at least `eta*kappa/2`.

Approximation of the total mass and a prefix to error `mu` gives error at most `2mu` in their difference against the quantile parameter. The strict comparison branches preserve the true inverse bracket. An uncertain comparison has true mass difference at most `4mu`, strictly below the mass of any input interval of length `eta`, so its input distance from the inverse is less than `eta`. Ordinary bisection handles the remaining case. The logarithm of the required reciprocal precision is polynomial because the monomial degree is bounded by the dense input size.

I requested an explicit treatment of desired input errors above one half. The author added the reduction to error `min(eta,1/2)`, closing that minor statement-completeness issue. Endpoints of the quantile parameter remain exact. No lower bound depending inversely on that parameter is needed.

## Fixed-accuracy mass quantiles used by the formulation

For the actual compiler, only the weaker fixed mass accuracy is needed. With `zeta=1/512`, the definition `U=max(zeta,Mhat+zeta)` gives `M<=U<=M+2zeta`, even if the approximate total mass is negative because the true mass is very small. It also gives a positive rational `U`.

The revised depth `L=max(0,ceil(log2((5/2)U)))` ensures `U/2^L<=2/5`, including depth zero. The rational bound `B=1+f''(1)/epsilon` bounds the density because its linear branch is at most `f''/epsilon`. Both `log B` and the cell depth have polynomial size in the input encoding.

For a target inside the true mass range, certified strict comparisons preserve an inverse bracket. The uncertain branch has mass error at most `2zeta`. If no uncertain branch occurs, the stated number of bisections makes the bracket mass width at most `zeta` by the upper density bound. For a target above the total mass, a strict upper-bracket update is impossible: the certified lower estimate of `F(x)` never exceeds that target. The bracket stays adjacent to one, yielding mass error at most `3zeta`. This explicitly handles the allowed small excess of the target over `M`, without a lower density or conditioning assumption.

The forced endpoint knots satisfy the same `4zeta` guarantee, since their discrepancy from the target total is at most `2zeta`. All outputs are dyadic, can share a fixed precision, and are deterministic at a repeated index. Their worst-case computation time is polynomial. The integration algorithm is a genuine certified bit algorithm, so its bounded execution can be compiled into ordinary Boolean gates; it is not an unspecified real oracle inside the formulation.

## Chords, graph bands and count

Adjacent knots need not be ordered for the proof. Monotonicity of the cumulative mass gives interval mass equal to their absolute cumulative difference, bounded by

```
2/5+8zeta=133/320.
```

The independently reviewed interval-mass estimate gives endpoint remainder at most `81529/102400`, which is strictly below `13/16`. Thus each true chord has error at most `13epsilon/16`. The path joins zero to one because shared endpoints use the same deterministic computation, so its projection covers the domain by continuity. Reversed or repeated segments do not invalidate this reasoning.

At each endpoint, a common monomial error tolerance `min(1,epsilon/(8C))` gives weighted downward error at most `epsilon/8`. This also holds when the minimum is one, because then `C<=epsilon/8`. The affine part is restored exactly at the actual input. Interpolating the computed endpoint values with the same parameter gives error in `[-epsilon/8,13epsilon/16]`. Consequently the proposed band contains the exact graph and bounds every admitted absolute error by `15epsilon/16`.

Only the `L` cell-index bits are declared integer. Gate integrality follows from the already audited acyclic circuit construction, and output-bit interpolation adds no integers. All endpoint precisions, coefficient operations and circuit sizes are polynomial. The all-affine case is recognized exactly and uses no integers.

Finally, the finite curvature lower bound gives `M<=48*2^p_conv`. Hence

```
(5/2)U<=120*2^p_conv+5/512<128*2^p_conv.
```

Taking the ceiling logarithm and the maximum with zero proves `L<=p_conv+7`. This comparison is with the true minimum over arbitrary convex integer lifts, not with the weaker coefficient-sum allocation benchmark.

## Independent exact checks

A separate exact rational checker used constant-curvature positive polynomials, whose cumulative density has a piecewise-rational closed form. It tested both positive and negative certified approximation biases, forced endpoints, and targets above the total mass. All **207 sampled indexed cells**, **828 exact graph-band cases**, and **126 above-total-mass inverse targets** passed. The largest implicit grid had **67,108,864** cells; the checker queried selected indices without enumeration. These cases exercise small total mass, zero cell depth, endpoint density vanishing and large coefficient magnitudes.

The checks supplement the uniform proof. They do not purport to implement the full certified algebraic-function quadrature. No substantive mathematical correction was needed in the combined theorem. Sparse huge degrees, multivariate curvature measures and practical formulation size remain outside this result.
