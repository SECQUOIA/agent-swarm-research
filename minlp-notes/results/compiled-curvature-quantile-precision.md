# Compiled curvature quantiles for near-minimal scalar polynomial precision

Date: 2026-09-05. Status: independently reviewed theorem and construction.

This construction turns the finite curvature benchmark into a polynomial-size
rational formulation for one positive polynomial. Mass-accurate rational
quantiles suffice, so no lower bound on the curvature density is needed for
the inverse computation.

## Assumptions and conclusion

Let

```
f(x)=a x+b+sum_(k=2)^D c_k x^k,
x in [0,1],           c_k>=0,
```

have rational dense input, and let `epsilon>0` be rational. The supporting certified algorithm evaluates

```
F(x)=integral_0^x min(sqrt(f''(t)/epsilon),
                     (1-t)f''(t)/epsilon) dt
```

at any rational `x in [0,1]`, to specified absolute error `eta`, in time
polynomial in the dense input, the encoding of `x`, and `log(1/eta)`.
Its output is rational with polynomial encoding length. The complete analytical computational proof is given in
[the cumulative-integration note](../notes/certified-positive-polynomial-curvature-quantiles.md).

Using that lemma, a deterministic polynomial-time algorithm constructs a
rational MILP of polynomial size, with whole-graph absolute error at most
`epsilon`, using

```
p_out<=p_conv+7                                      (1)
```

binary variables. The comparison is with all convex integer lifts, regardless
of their continuous size. No sparse binary-degree claim is included here.
If all nonlinear coefficients vanish, return the exact affine graph with
zero integers and stop.

## Fixed-accuracy mass certificates

Write `rho=F'`, `M=F(1)>0`, and set `zeta=1/512`. Compute a rational
`Mhat` with `|Mhat-M|<=zeta`, and define

```
U=max(zeta,Mhat+zeta),
L=max(0,ceil(log2((5/2)U))),
N=2^L.
```

Then `M<=U<=M+2zeta` and `U>0`. Also `U/N<=2/5`: if `L=0`, this is the
condition `(5/2)U<=1`; otherwise it follows from the ceiling definition.

A rational upper bound on the density is

```
B=1+epsilon^(-1)sum_k k(k-1)c_k.
```

Indeed `rho<=f''/epsilon<=B`. Its encoding length is polynomial in the dense
input. For an interior index `q=1,...,N-1`, put `t=qU/N`. The target may exceed
`M` by at most `2zeta`.

Use bisection on `[0,1]`. At a midpoint `x`, compute `Fhat(x)` within `zeta`.
If `Fhat(x)+zeta<t`, move the left endpoint to `x`; if `Fhat(x)-zeta>t`, move
the right endpoint to `x`. Otherwise return `x`. In this uncertain case,

```
|F(x)-t|<=2zeta.
```

After at most `ceil(log2(B/zeta))+1` strict steps, return the bracket midpoint.
If `t<=M`, the bracket contains an inverse value, and its mass width is at
most `B` times its input width, hence at most `zeta`. If `t>M`, every strict
comparison moves the left endpoint and the bracket remains adjacent to one;
its output has mass distance at most `2zeta+zeta=3zeta` from the target.
The same bound covers a flat part of `F`; no derivative lower bound is used.

Thus a deterministic polynomial-time indexed algorithm returns dyadic knots
`R_q in [0,1]`, with common polynomial output precision, such that

```
R_0=0, R_N=1,
|F(R_q)-qU/N|<=4zeta                                  (2)
```

for every index, including the forced endpoints. Earlier bisection outputs
are padded with zeros to the same fixed dyadic precision. Early termination
is implemented with a fixed-time flag when compiling the algorithm.

## Every computed interval has a certified small chord gap

The knot sequence need not be monotone. Nevertheless, for adjacent values,
monotonicity of `F` and (2) give

```
integral_(min(R_q,R_(q+1)))^(max(R_q,R_(q+1))) rho
 =|F(R_(q+1))-F(R_q)|
 <=U/N+8zeta<=2/5+1/64=133/320.
```

The finite curvature theorem's interval estimate gives a normalized endpoint
Taylor remainder at most

```
(133/320)^2+(3/2)(133/320)=81529/102400<13/16.
```

Thus the chord error of the true polynomial on each computed interval is at
most `13epsilon/16`. Duplicate knots cause no error. The polygonal sequence
starts at zero and ends at one, so its input projection covers the full
interval even if some intermediate segments reverse direction.

## Circuit interpolation and rational output bands

The [compiled indexed-knot lemma](../notes/compiled-rational-knot-formulations.md)
uses only the `L` cell-index bits to represent the selected endpoints and
interpolate all their computed output bits with a common continuous weight
`theta`. Its internal Boolean gate variables remain continuous and are
forced integral by the index bits.

At each returned endpoint, compute every listed monomial by downward rounded
binary exponentiation, so its coefficient-weighted total error is at most
`epsilon/8`. For example, with `C=sum_k c_k>0`, a common monomial absolute
error tolerance `min(1,epsilon/(8C))` suffices. The number of fractional bits
needed for a degree `k` is polynomial in `log D`, the endpoint precision,
and the input/tolerance encoding, as in the reviewed sparse-power evaluator.
The circuit outputs the bounded monomial values, and the rational coefficients
are applied outside the circuit by linear equations. The affine part is
restored exactly at the actual input `x`.

Let `y` be this interpolated polynomial value. At each selected cell,

```
-epsilon/8<=y-f(x)<=13epsilon/16.
```

Impose the rational band

```
y-13epsilon/16<=w<=y+epsilon/8.
```

It contains every exact graph point, and every admitted point has absolute
error at most `15epsilon/16`. This leaves slack within the required tolerance.
The computation, output coefficients, and all gate/product constraints have
polynomial size by the supporting cumulative-integration theorem.

## Integer count

The finite curvature theorem gives `M<=48*2^(p_conv)`. Since `U<=M+1/256`,

```
(5/2)U<=120*2^(p_conv)+5/512 <128*2^(p_conv).
```

Taking the ceiling logarithm and the nonnegative maximum yields
`L<=p_conv+7`, proving (1). The affine case was treated separately. The count
therefore depends on the true minimum, not merely on the coefficient-sum
allocation that has an unbounded degree gap.

## Status and scope

The interval metric, parity lower bound, and generic circuit compiler are
separate supporting results. The present proof supplies the fixed-mass inverse
algorithm, endpoint error budget, and final count. The cumulative integration algorithm now has a complete polynomial-bit proof.
The [first independent audit](../notes/review-compiled-curvature-quantile-precision.md)
and [second independent audit](../notes/review-compiled-curvature-quantile-precision-second.md)
both passed for the entire analytical dependency and this construction.
The [bounded source audit](../notes/compiled-curvature-quantile-precision-novelty.md)
credits prior minimum-piece segmentation, computation compilation, root
isolation, and analytic integration. It found no matching combined polynomial-
bit construction within seven integers of every convex lift. Publication
priority remains unestablished.

Only constant absolute accuracy is required for the cumulative integral calls
in this final construction. Their bit cost can still depend polynomially on
coefficient magnitudes and tolerance encodings; fixed absolute accuracy is not
permission to assume unconditioned numerical integration. The mathematical
benchmark and the univariate finite two-bit comparison remain valid independently
of this computational candidate.

The [exact mass-knot checker](../code/quadratic_rank/check_compiled_curvature_mass_knots.py)
passed 109 indexed interval-mass certificates and 545 graph-band checks for
constant-curvature reference functions. It sampled grids with up to 4,194,304
cells without enumerating them. The cumulative integrals are piecewise rational
in those reference cases, so every assertion in this checker is exact.

The first reviewer separately checked 207 exact indexed cells, 828 graph
bands, and 126 above-total-mass targets, with an implicit grid of up to
67,108,864 cells. These tests supplement the analytic proof and do not
enumerate the constructed formulation's possible cells.


The [separable extension](separable-convex-graph-linear-dimension-precision.md)
uses scalar interval packings and Jensen-gap superadditivity to compare
multivariate scalar sums and independent outputs with every convex integer lift.
It gives finite `O(r)` gaps for continuous convex summands and polynomial
rational constructions for dense positive polynomials.


The [general convex-polynomial construction](convex-polynomial-compiled-integer-precision.md)
removes coefficient-sign and curvature-monotonicity assumptions for dense
polynomials. It gives an eleven-integer scalar comparison and separable
comparisons of `16r` for sums and `13r` for independent outputs.
