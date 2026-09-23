# The Frobenius covariance benchmark has an unavoidable n log n gap

Date: 2026-09-05. Status: independently reviewed support result.

The dimension-only `O(n log(n+1))` error in the reviewed covariance
characterization cannot be replaced by `O(n)` for that same benchmark.
The obstruction already occurs for one convex quadratic at unit error.
This does not rule out a different benchmark with a smaller gap.

## Example and exact benchmark

On `[0,1]^n`, take

```
f(x)=(1/2)sum_i x_i^2,       |w-f(x)|<=1.
```

Its Hessian is `I`. The Frobenius covariance problem is

```
D=max{det P: 0<=P<=I, tr(P^2)<=1}.
```

For nonnegative eigenvalues `lambda_i`, the arithmetic-geometric mean
inequality applied to `lambda_i^2` gives

```
det P <= [tr(P^2)/n]^(n/2) <= n^(-n/2).
```

Equality holds at `P=n^(-1/2)I`, which satisfies the cap. Thus the
benchmark from the [finite covariance law](../results/quadratic-weighted-covariance-precision.md)
is exactly

```
Phi=-(1/2)log2 D=(n/4)log2 n.                            (1)
```

## Every convex mixed-integer lift needs twice that leading term

Consider an arbitrary valid convex lift with `p` integer coordinates.
For each integer parity class, take the closure of the domain points
whose exact graph points have a lift in that class. These compact
supports cover the cube. For two points `x,y` in one support, convexity
and integer parity make their graph midpoint admissible. Continuity
extends the following inequality to the closure:

```
[(f(x)+f(y))/2]-f((x+y)/2) = ||x-y||_2^2/8 <=1.
```

Every nonempty support has diameter at most `sqrt(8)`. Fixing any point
in it places the support in a Euclidean ball of that radius, so its
volume is at most `omega_n 8^(n/2)`. The `2^p`-set cover of a unit-volume
cube implies

```
p >= -log2 omega_n-(n/2)log2 8.                          (2)
```

The elementary Gaussian bound

```
omega_n <= exp(n/2)(2pi/n)^(n/2)
```

follows by integrating `exp(-(n/2)||x||^2)` over the unit ball and
then over all of `R^n`. Substituting into (2) gives the explicit bound

```
p_conv >= (n/2)log2 n-(n/2)log2(16pi e).                (3)
```

The proof uses no limit in approximation accuracy and allows any
number of continuous variables, nonlinear convex constraints, and
unbounded general integer variables.

## A matching grid upper bound

Set

```
L=max{0,ceil[(1/2)log2(n/8)]},       h=2^(-L).
```

Use `L` binary prefix digits for each coordinate, leaving a residual
in `[0,h]`. Represent prefix products and prefix-residual products
exactly. For the residual square use the triangle

```
s>=0,       s>=2h r-h^2,       s<=h r.
```

It contains the exact square graph and satisfies `|s-r^2|<=h^2/4`.
Since the coefficient of every square is `1/2`, the whole output error
is at most `n h^2/8<=1`. This is a valid rational MILP with `nL`
binaries and a polynomial number of rows and auxiliary variables.
It follows that

```
p_conv <= p_bin <= n max{0,ceil[(1/2)log2(n/8)]}
                      <= (n/2)log2 n+n.                 (4)
```

Equations (3)--(4) show, as dimension grows,

```
p_conv=(n/2)log2 n+O(n),
p_bin =(n/2)log2 n+O(n),
p_conv-Phi=(n/4)log2 n+O(n).                             (5)
```

Thus the additive order of the current Frobenius determinant law is
sharp in dimension. This is separate from the reviewed computational
[approximation hardness theorem](../results/quadratic-integer-precision-approximation-hardness.md):
(5) is an unconditional limitation of this particular benchmark, while
the hardness result constrains polynomial-time formulation algorithms.
The construction and ball-volume argument are elementary; no priority
claim is made for either ingredient in isolation.

The [independent proof audit](review-covariance-benchmark-dimension-gap.md)
passed, including the Gaussian constant, small-dimensional grid case,
and rational formulation construction.
