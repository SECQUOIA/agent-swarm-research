# Independent audit: dimension gap in the covariance benchmark

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/covariance-benchmark-dimension-gap.md`.

**Verdict: PASS.** The exact determinant benchmark, general-integer lower
bound, rational binary upper construction, and resulting
`(n/4)log2 n+O(n)` gap are correct. No correction was needed.
This is an unconditional limitation of the particular Frobenius
covariance benchmark, not an algorithmic hardness claim or an exclusion
of a better benchmark.

For `f(x)=(1/2)sum_i x_i^2`, the Hessian is `I`, so the covariance
energy is exactly `tr(P^2)`. Applying arithmetic-geometric mean to
the squared eigenvalues gives `det P<=n^(-n/2)`. The matrix
`P=n^(-1/2)I` is feasible and attains equality, including when
`n=1`. Hence `Phi=(n/4)log2 n` exactly.

I checked the quadratic midpoint normalization:

```
(f(x)+f(y))/2-f((x+y)/2)=||x-y||^2/8.
```

Any two exact graph lifts whose integer vectors have the same parity
have an admitted integer midpoint. Unit error therefore bounds the
diameter of each parity support by `sqrt(8)`. Taking closures inside
the cube preserves the inequality and the covering property by continuity;
it does not assume that the lifting set or its projection is closed.
Each nonempty compact support is contained in a ball of radius
`sqrt(8)` centered at any one of its points. Thus its volume is at most
`omega_n 8^(n/2)`, and volume subadditivity over at most `2^p` parity
classes gives the displayed lower bound.

The Gaussian calculation has the correct constants. On the unit ball,
`exp(-(n/2)||x||^2)>=exp(-n/2)`, while the integral over all space is
`(2pi/n)^(n/2)`. Therefore

```
omega_n <=(2pi e/n)^(n/2),
p_conv >=(n/2)log2 n-(n/2)log2(16pi e).
```

The lower bound is permitted to be negative in small dimensions; the
trivial nonnegative integer count remains available. The asymptotic
claim only uses sufficiently large dimensions.

For the upper bound, the chosen integer depth satisfies
`n 2^(-2L)/8<=1`: when `n<=8`, it uses `L=0`, and otherwise
this follows from the rounded logarithm. The residual-square triangle
contains every exact square and has absolute error at most `h^2/4`.
Both its upper deviation `hr-r^2` and lower deviation
`r^2-max(0,2hr-h^2)` attain at most that amount. Multiplication by
the coefficient one half and summing gives total error at most
`nh^2/8<=1`.

Every original input admits its binary-prefix and residual representation,
including endpoints. Prefix products are exact bounded binary products,
so they introduce no further approximation error or integer coordinates.
All coefficients are rational dyadics with polynomial bit length, and
the number of rows and continuous variables is polynomial in `n`.
The binary count `nL` has the stated upper bound.

Together with `p_conv<=p_bin`, these estimates place both integer
minima at `(n/2)log2 n+O(n)`. Subtracting the exact benchmark yields
`p_conv-Phi=(n/4)log2 n+O(n)`, and the same conclusion holds for
`p_bin`. In particular, replacing the finite theorem's dimension-only
additive error by `O(n)` while leaving its benchmark unchanged is
impossible. The leading gap is of order `n log n`, irrespective of
any computational complexity assumption.

