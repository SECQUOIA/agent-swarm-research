# Exponential support complexity on a scalar-separator path

Date: 2026-09-05. Status: verified literature obstruction and checked
consequences. The general exponential-shadow construction is known, not
a new result. Its role here is to prevent an invalid polynomial-size
message assumption in prospective sparse-pooling algorithms.

## Primary construction

Gärtner, Helbling, Ota, and Takahashi,
[*Large Shadows from Sparse Inequalities*](https://arxiv.org/pdf/1308.2495),
Section 4, give an exponential shadow for the following Klee–Minty cube:

```
0 <= x_1 <= 1,
epsilon x_(j-1) <= x_j <= 1-epsilon x_(j-1),  j=2,...,n.
```

Fix `epsilon=1/4`. Their objective vectors are
`c_j=epsilon^(3(n-j))` for `j<n`, and `c_n=0`. Every one of the
`2^n` vertices uniquely maximizes `c^T x+lambda x_n` for some parameter
strictly between `-1/15` and `1/15`. For vertex bits `u_j in {0,1}`,
an explicit witness is

```
lambda(u) = -sum_(j=0)^(n-1)
                 [product_(k=j+1)^n (1-2u_k)] epsilon^(2(n-j)).
```

Section 4 proves strict optimality through the incident edge directions.
The coefficient and witness denominators have polynomial bit length.
The primary source was read directly, including its proof; this is not
an inference from general Goldfarb-cube statements.

## What the path structure does and does not imply

Every inequality contains only a consecutive pair of variables. The
primal graph is an actual path, with bags `{x_(j-1),x_j}` and a single
scalar in each separator. Each local block has constant dimension and
two inequalities. All variables lie in `[0,1]`, and the nonparametric
constraint coefficients are fixed small rational numbers. The objective
is a sum of unary terms; its parameter occurs only at the last vertex
of the path. An affine change maps the parameter interval to `[0,1]`.
The entire input has polynomial encoding length.

Therefore bounded pathwidth, scalar separators, two variables per
inequality, and one objective parameter do not imply a polynomial number
of pieces in the optimal value function. In particular, an algorithm
that enumerates every support piece or every optimal basis can require
exponential output even under all these restrictions.

This also gives an obstruction for an explicit scalar-state message with
a fixed objective. Define

```
F_n(t) = max { sum_(j<n) c_j x_j : x is feasible, x_n=t },
          0<=t<=1.
```

It is the upper boundary of the two-dimensional projection onto
`(x_n,c^T x)`. Each of the `2^n` projected vertices is exposed with
the coefficient of `c^T x` fixed at positive one. Thus all lie on this
upper boundary. Their `x_n` coordinates must be distinct: otherwise the
lower of two points with the same first coordinate could not be exposed
by any such objective. Consecutive projected vertices cannot be collinear
for the same reason. Hence `F_n` has exactly `2^n-1` affine intervals.
Adding a fixed terminal reward `lambda t` changes none of these
breakpoints. This rules out a generic polynomial bound on explicitly
represented, fixed-objective scalar-state messages as well.

These statements do not imply an optimization hardness result. For a
given parameter, backward elimination is especially simple. Let
`a_n=lambda`, then recursively set
`a_j=c_j-epsilon |a_(j+1)|`. The support value is
`sum_j max(0,a_j)`. Eliminating a variable with positive effective
coefficient selects its upper bound, adding a constant and a negative
multiple of its predecessor; a negative coefficient selects its lower
bound. This proves the recurrence directly. Thus pointwise evaluation
uses a linear number of exact arithmetic operations, despite exponentially
many explicit pieces. Compact extended descriptions and adaptive
pointwise algorithms remain possible.

The related note
[parametric path investigation](parametric-path-lp-investigation.md)
develops this distinction and a total-degree lower bound for quantifier-
free descriptions. I independently checked that argument: a finite
polynomial description of the graph's epigraph must vanish on every
open boundary segment. Some nonzero polynomial must contain each such
supporting line as a factor. Distinct line factors require summed degree
at least the number of pieces. This is a total-degree obstruction, not a
lower bound for arithmetic circuits, extended formulations, or pointwise
optimization.

## Independent exact checks

[exact_shadow_check.py](../code/parametric_path_lp/exact_shadow_check.py)
uses rational arithmetic throughout. For dimensions one through twelve,
it constructs every vertex and the explicit parameter witness, verifies
the signs produced by independent backward elimination, and checks the
support objective exactly. It then sorts the support lines by slope and
verifies that all consecutive intersection parameters strictly increase
within the stated interval. The corresponding scalar-state graph slopes
strictly decrease, verifying every claimed upper-boundary segment.

The run passed 8,190 vertex witnesses and 8,178 ordered breakpoints;
dimension twelve has 4,096 support pieces and 4,095 scalar-state message
segments. These finite checks support the independently inspected general
proof in the primary source.

## Checked blending-path realization

The pooling-construction author independently proposed the following
realization, whose algebra I checked. Source `j` has exact supply
`D_j=4^(j-1)` and scalar quality `C_j=n-j`. It sends `x_j` to output
`j` and `D_j-x_j` to output `j-1`. Each internal output `j-1` has
upper capacity `D_j` and midpoint upper quality `(C_(j-1)+C_j)/2`.
Its capacity gives `x_j>=x_(j-1)`, while its upper quality gives
`x_j<=D_j-x_(j-1)`. Normalizing `z_j=x_j/D_j` yields exactly the
path constraints above. The two endpoint outputs impose only the
endpoint flow bounds. The physical bypass graph is a path, and every
input and output has degree at most two. Dividing all flows by `D_n`
puts every upper flow bound in `[0,1]`; scaling the quality values also
puts them in `[0,1]`.

This realizes the support obstruction inside an ordinary scalar-quality
blending network, rather than merely an unrelated sparse LP. Exact
source contracts are used at this stage. Its full construction and
independent network tests are being recorded separately by the author;
no new pooling complexity classification follows solely from this
support example. The author's completed
[physical path note](pooling-degree-two-bypass-investigation.md) further
realizes the objective by one varying output price and removes all lower
flow bounds by a uniform output-revenue bonus. Both steps pass the
[separate second review](review-pooling-degree-two-price-response-second.md),
including 252 exact physical primal/dual certificates using the theoretical
penalty.
