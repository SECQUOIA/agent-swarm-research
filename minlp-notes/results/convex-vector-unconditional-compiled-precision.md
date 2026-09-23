# Convex vector precision for arbitrary unconditional error bodies

Date: 2026-09-05. Status: independently reviewed result. The
[first full audit](../notes/review-convex-vector-unconditional-log-product-precision.md) and
[second full audit](../notes/review-convex-vector-unconditional-log-product-precision-second.md)
passed without required corrections.

For one-input componentwise convex graphs, a maximum-product inscribed box
converts an arbitrary unconditional error budget to one scalar convex
approximation problem. The finite binary overhead is logarithmic in output
dimension without any facet-count or conditioning factor. For dense rational
polynomial outputs and a rational separation oracle for the error body,
the construction is polynomial and rational.

Let `F:[0,1]->R^m` be continuous and componentwise convex. Let `K` be a
compact convex unconditional body with the origin in its interior. Here
unconditional means invariant under every coordinate sign flip. Let `p_conv`
be the smallest number of unrestricted integer coordinates among convex
lifts containing the entire graph and admitting only errors in `K`.
Then a finite real-coefficient binary MILP satisfies

```
p_bin<=p_conv+ceil(log2(4m-1)).                              (1)
```

For densely encoded rational component polynomials, assume that `K` has a
rational strong separation oracle with polynomial query and output complexity,
and known positive rational radii `rho,R` satisfying

```
rho B_2^m subset K subset R B_infinity^m.
```

There is a deterministic polynomial-time rational MILP construction with

```
p_out<=p_conv+14+ceil(log2 m).                               (2)
```

Construction complexity includes the body-oracle encoding and the radii.
No polyhedral description of `K` is required. The final formulation uses
linear bands from a rational box contained in `K`, so it needs no nonlinear
constraints or calls to that oracle during optimization.

## 1. A maximum-product box and its supporting positive functional

Choose `b>0` maximizing `product b_i` over the positive part of `K`. Such a
maximizer exists and is strictly positive: the feasible set is compact and
contains positive points, while any zero coordinate makes the product zero.
Unconditionality and convexity imply

```
prod_i[-b_i,b_i] subset K.
```

Indeed, all sign flips of `b` belong to `K`, and their convex hull is that
box. Define `ell(v)=sum_i v_i/b_i`. Concavity and first-order optimality of
the differentiable function `sum log b_i` give

```
ell(v)<=m       for every v in K with v>=0.                  (3)
```

One can see this directly by differentiating the feasible segment
`(1-t)b+t v` at `t=0`; its log product cannot initially increase.

## 2. Finite comparison with arbitrary integer lifts

For each parity class of exact graph witnesses in a `p`-integer convex lift,
take the closure of its input support and its interval hull. Endpoint
witness limits show that the nonnegative midpoint Jensen vector belongs
to `K`. This uses continuity and closedness of `K`, not closedness of the
lift or boundedness of integer coordinates.

The scalar function `Psi=sum_i F_i/b_i` is convex. By (3), its midpoint gap
on each parity hull is at most `m`, and its full chord gap is at most `2m`.
The elementary level-cut lemma partitions such a hull into at most `4m-1`
intervals of scalar chord error at most one: cut at the two crossings of
each positive integer below the maximum gap, and subtract the affine
interpolation of the original gap's endpoint values on every subinterval.
Its range on each resulting interval is at most one.

Every component gap is nonnegative, so the scalar bound gives
`0<=T_i-F_i<=b_i` on the refined intervals. The downward bands

```
T_i(x)-b_i<=w_i<=T_i(x)
```

contain the graph and have error in `prod[-b_i,b_i] subset K`. There are at
most `(4m-1)2^p` bands, proving (1) by a finite binary disjunction.

## 3. Rational approximate product optimization still controls the functional

The [twice-reviewed rational log-product oracle](../notes/rational-log-product-convex-body-oracle.md),
applied with matrix `R I`, accuracy `nu=1`, and coordinate cap one, returns
a rational `b>0` in `K` whose product is at least `exp(-1)` times the optimum
product over `K`'s positive part. The cap excludes no feasible positive
point after scaling by `R`, because `K subset R B_infinity`.

This approximate maximizer has the quantitative substitute

```
sum_i v_i/b_i<=7m      for every v in K with v>=0.           (4)
```

For `m>=2`, put `a_i=v_i/b_i`, `S=sum_i a_i`, and `s=1-1/m`. Convexity puts
`w=s b+v/m` in `K`. Expanding the product and discarding its nonnegative
terms of degree at least two in the `a_i` gives

```
product(w_i/b_i)
 = product(s+a_i/m)
 >= s^(m-1)(s+S/m).
```

The left side is at most `exp(1)` by approximate optimality. Also
`s^(m-1)>=exp(-1)`, for example by integrating `1/(1-t)` to bound
`log(1-1/m)>=-1/(m-1)`. Consequently

```
S<=m(exp(2)-1)+1<7m.
```

For `m=1`, approximate optimality directly gives `v_1/b_1<=exp(1)<7`.
All computations returning `b` have polynomial rational encoding and running
time by the imported oracle lemma. No numerical derivative or approximate
first-order optimality test is needed.

## 4. One scalar compiler gives the vector MILP

Use this rational `b` and the rational dense convex polynomial
`Psi=sum_i F_i/b_i`. If every component is affine, return its exact linear
graph. Otherwise `Psi` is nonaffine. Equation (4) bounds each parity-hull
midpoint gap by `7m`, and its full gap by `14m`. The level-cut argument now
gives at most `28m-1` scalar chord intervals of error one per parity hull.
A finite interval cover of a convex scalar graph can be turned into a
partition with no more intervals by restricting successively chosen covering
intervals. Thus

```
N_1(Psi)<=(28m-1)2^p.
```

Apply the [reviewed dense convex scalar compiler](../results/convex-polynomial-compiled-integer-precision.md)
at tolerance one. It has at most `486 N_1(Psi)` indexed rational cells,
each with exact scalar chord gap at most `13/16`. On each such cell, every
normalized component `G_i=F_i/b_i` has gap at most `13/16`, since its gap is
nonnegative and their sum is the scalar gap.

Evaluate the `G_i` at the two rational cell endpoints and round downward to
error at most `1/8`. Let `y_i` interpolate those rounded values with the
same input interpolation weight. Use the normalized bands

```
y_i-13/16<=z_i<=y_i+1/8,          w_i=b_i z_i.
```

They contain all exact component graph values and admit normalized error at
most `15/16`. The vector error therefore lies in `(15/16)prod[-b_i,b_i]`,
which is contained in `K`. One common input cell and interpolation weight
give simultaneous vector graph containment. The scalar path covers the
whole input interval; its possible repeated or reversed cells are harmless.

Additional polynomial evaluations, gate variables, and endpoint-bit products
add only continuous variables to the compiled indexed-knot formulation.
The rational normalization by `b_i`, their reciprocals, and final rescaling
have polynomial encoding by the oracle guarantee. Finally,

```
K_cells<=486(28m-1)2^p<13608m2^p<16384m2^p,
```

giving (2). The construction never needs the comparator lift or its integer
dimension.

## Scope and attribution

This result applies to arbitrary unconditional budgets, including smooth
ones, and has no dependence on their number of facets. It improves on
bounding `K` by its separate coordinate radii, which can lose a further
factor of the output dimension. It does not prove that an output-independent
additive guarantee is impossible as `m` grows.

Maximum-product allocation and its first-order inequality are classical:
[Kelly, Maulloo and Tan (1998), Section 2, equation (1)](https://www.statslab.cam.ac.uk/~frank/rate.pdf)
states the proportional-fair inequality and its equivalence to maximizing
the sum of logarithms in its network setting. The same first-order argument
above works for the present convex body.
Convex-body separation and optimization, scalar refinement, and circuit
compilation are established ingredients. The supporting result is their
combination for whole-formulation integer counts; no new general allocation
algorithm is claimed. Both independent full proof audits passed.

The [bounded independent source assessment](../notes/convex-vector-gap-and-overlay-source-audit.md)
confirms the proportional-fairness attribution and did not locate the full
graph-formulation count comparison. This does not establish exhaustive
priority.
