# A double-logarithmic degree gap for the positive-polynomial allocation

Date: 2026-09-05. Status: independently reviewed benchmark obstruction.

The coefficient-sum allocation benchmark in the positive-polynomial theorem
cannot characterize the integer count to additive `O(r)` uniformly in all
degrees. A one-dimensional positive polynomial family already has a gap
of order `log log D`. This is a limitation of that benchmark, not a lower
bound on the extra integers used by every algorithm relative to the true
optimum.

For an integer `M>=1`, define

```
f_M(x)=(1/M)sum_(j=1)^M x^(2^j),        x in [0,1],
D=2^M,
epsilon=1/(512M).
```

All coefficients are nonnegative rationals. The coefficient sum is one,
so the scalar allocation has `D_alloc=epsilon` and

```
Phi=(1/2)log2(512M)=(1/2)log2 M+9/2.                   (1)
```

Nevertheless,

```
ceil(log2 M)<=p_conv<=p_bin<=ceil(log2(512M)).           (2)
```

The upper count here refers to finite real-coefficient binary linear
formulations, with no size restriction. Therefore

```
p_conv=log2 M+O(1),       p_bin=log2 M+O(1),
p_conv-Phi=(1/2)log2 M+O(1)
           =(1/2)log2 log2 D+O(1).                    (3)
```

In particular, the last equality in (3) has matching upper and lower
orders for the benchmark gap, not just a lower estimate.

## Pairwise incompatible graph points

Choose `M` rational points

```
x_j=1-2^(-j),           j=1,...,M.
```

For `j<ell`, put `k=2^j`. Then
`x_ell-x_j>=1/(2k)`. On the entire interval `[x_j,x_ell]`, the curvature
of the selected monomial obeys

```
(d^2/dx^2)x^k=k(k-1)x^(k-2)
 >=k(k-1)(1-1/k)^(k-2)>=k^2/8.                         (4)
```

Indeed, `k(k-1)>=k^2/2` and `(1-1/k)^(k-2)>=1/4` for `k>=2`.
For the latter estimate, `(1+1/(k-1))^(k-1)<=e<4`, so even the smaller
quantity `(1-1/k)^(k-1)` exceeds `1/4`.

A function with second derivative at least `m` on an interval has midpoint
Jensen gap at least `m(b-a)^2/8`, by subtracting `(m/2)x^2` and applying
convexity. Equations (4) and the point separation give

```
[(x_j^k+x_ell^k)/2]-((x_j+x_ell)/2)^k >=1/256.
```

All other monomials have nonnegative Jensen gap. Thus

```
[f_M(x_j)+f_M(x_ell)]/2-f_M((x_j+x_ell)/2)
 >=1/(256M)>epsilon.                                  (5)
```

Any two corresponding exact graph points must have different parity
vectors in an arbitrary convex mixed-integer lift: if their integer
vectors had the same parity, the lifted midpoint would have integral
coordinates and would violate the error bound by (5). Consequently
`2^p>=M`, proving the lower bound in (2). This does not assume bounded
integer variables or bound the number of continuous variables.

## A matching-order finite upper count

The polynomial is strictly increasing on `[0,1]`, with endpoint values
zero and one. Let `N=512M` and choose the unique knots
`a_h=f_M^(-1)(h/N)`, `h=0,...,N`. On each interval, the chord lies above
the convex function, and both chord and function have values between the
two endpoint values. Hence its vertical chord error is at most
`1/N=epsilon`.

Use the band from chord minus `epsilon` to chord. It contains the exact
graph and admits only errors of magnitude at most `epsilon`. Encode the
union of the `N` bounded cell bands using `ceil(log2 N)` binaries and
the finite Hamming-distance construction from the
[pure-power finite theorem](pure-power-degree-independent-integer-count.md).
Unused strings are excluded. This proves the upper bound in (2).
The knots need not be rational for this finite statement. No rational
coefficient or compact construction conclusion is inferred from this
upper proof.

## Meaning of the example

The [log-log degree theorem](positive-polynomial-loglog-degree-precision.md)
has an upper benchmark loss of order `sum_i log log(D_i+2)`. This example
shows that its degree order cannot be removed from a universal upper
comparison with the same coefficient-sum benchmark, even with one variable
and one output. It does not prove the exact constant in that theorem
optimal, and it does not rule out a richer benchmark or a construction
within additive `O(r)` of the true minimum.

The [pure-power result](../results/positive-pure-power-linear-dimension-precision.md)
is consistent with this obstruction: the present family contains many
different powers of the same coordinate. The degree is exponential in
`M`, but the example is a valid dense polynomial family. Its purpose is
a mathematical finite-bound limitation, not a polynomial-time complexity
reduction measured in sparse exponent encoding.

The [first independent audit](review-positive-polynomial-allocation-degree-gap.md)
and [second independent audit](review-positive-polynomial-allocation-degree-gap-second.md)
both passed. The [exact checker](../code/quadratic_rank/check_positive_polynomial_degree_gap.py)
passed 286 pairwise Jensen obstructions through selected degree 2,048;
the first reviewer separately checked 66 pairs.
