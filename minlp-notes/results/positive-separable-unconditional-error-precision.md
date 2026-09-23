# Positive separable graph precision under unconditional error budgets

Date: 2026-09-05. Status: independently reviewed extension.

The positive-polynomial allocation law extends to any convex error body
invariant under coordinate sign changes. No approximation by an output
ellipsoid is needed, so the additive overhead remains independent of
the number of outputs and is linear in active dimension for fixed degree.

## Assumptions and statement

Let `f` be the positive separable polynomial system of the reviewed
[polynomial theorem](../results/positive-separable-polynomial-integer-precision.md):

```
f_j(x)=a_j^T x+b_j+sum_i sum_(k=2)^(D_i) c_jik x_i^k,
c_jik>=0,       x in [0,1]^n.
```

There are `r` active nonlinear coordinates, and
`C_ji=sum_(k=2)^(D_i) c_jik`. Let `K subset R^m` be a compact convex
body invariant under changing the sign of any subset of coordinates.
Such a body is called unconditional. Suppose it has a polynomial-time
rational strong separation oracle and known positive rational inner
and outer radii about zero. A valid approximation permits only errors
`w-f(x) in K`, and contains the whole exact graph.

Define

```
D_K=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi_K=-(1/2)log2 D_K.
```

The finite bounds hold with exactly the polynomial theorem's constants:

```
max(0,Phi_K-A)<=p_conv<=p_bin<=Phi_K+B,
A=log2[omega_r(r+2)^(r/2)]+sum_i log2D_i-r/2,
B=sum_i log2D_i+r.                                     (1)
```

For rational dense polynomial input, a deterministic polynomial-time
algorithm constructs a rational MILP with

```
p_out<=p_conv+2sum_i log2D_i+4r+1.                      (2)
```

The degree may grow in the dense representation. The model has
polynomial size in the full input and oracle description. No efficient
optimization algorithm for the resulting general MILP is asserted.
The case `r=0` is an exact affine graph and needs zero integers.

## Unconditional convexity gives coordinatewise domination

If `u in K` and `|v_j|<=|u_j|` for every coordinate, then `v in K`.
Indeed, the box with corners given by every sign change of `u` is
contained in `K` by convexity. This elementary property applies in
particular when `0<=v<=u`.

For exact graph points in one parity support, let

```
J_j(x,y)=[f_j(x)+f_j(y)]/2-f_j((x+y)/2).
```

Their graph midpoint is admitted, so `J(x,y) in K`. Every coordinate
is nonnegative because the nonlinear coefficients are nonnegative.
The scalar power inequality from the polynomial theorem gives

```
0<=sum_i (C_ji/D_i^2)
         (x_i^(D_i/2)-y_i^(D_i/2))^2 <=J_j(x,y).
```

Map each support by `t_i=x_i^(D_i/2)`. For independent uniform points
in a positive-volume transformed support, with covariance `Sigma`,
take expectation of the original-coordinate Jensen vector evaluated
at their inverse images. Convexity and closedness give `EJ in K`.
The preceding inequality gives

```
0<=2sum_i (C_ji/D_i^2)Sigma_ii <=(EJ)_j.
```

Therefore `p_i=2Sigma_ii/D_i^2` satisfies `Cp in K` by coordinatewise
domination. Its coordinate cap follows from `Sigma_ii<=1/4`. The rest
of the Hadamard determinant and transformed-volume lower bound is
unchanged, proving the lower half of (1). This expectation is taken
under the transformed support's uniform measure; no original-coordinate
volume invariance is required.

## A rational Taylor rectangle controls the whole error body

Take any positive feasible allocation `p` and the same original-axis
grid with widths `h_i<=sqrt(p_i)/D_i`. Let `T_j` be the shared prefix
Taylor expression from the polynomial theorem. It satisfies

```
0<=f_j(x)-T_j<=(Cp)_j/2.
```

Replace its componentwise-tolerance interval by the rational inequalities

```
T_j<=w_j<=T_j+(Cp)_j/2.                                (3)
```

These contain every exact graph point and imply

```
|w_j-f_j(x)|<=(Cp)_j/2.
```

Since `Cp in K` and `K` is unconditional, every admitted error belongs
to `K`. The exact reused-bit prefix-power recurrences, the binary count,
and all polynomial-size bounds are unchanged. The final MILP uses only
rational intervals (3); it does not attempt to describe a curved body
`K` by finitely many exact linear inequalities.

## The allocation oracle has polynomial rational complexity

The allocation feasible set `0<=p<=1, Cp in K` is convex. Its objective
`sum_i log p_i` is concave. The supporting
[rational log-product oracle lemma](../notes/rational-log-product-convex-body-oracle.md)
returns a positive rational feasible `p` with

```
product_i p_i>=exp(-1)D_K
```

in polynomial time. Its proof explicitly gives a bounded convex
log-product hypograph, a known rational inner ball, and a weak separator
using the supplied strong oracle for `K` and rational log tangents.
Classical GLS weak optimization followed by a rational central-ball
repair gives exact feasibility. No geodesic or semidefinite optimization
is needed for this extension.

Using this allocation in (3) adds at most `1/(2ln2)` to the benchmark
binary count. The same volume constant calculation as before proves
(2). The oracle's dependence on output dimension and radius encoding
is confined to running time and the model's continuous size; neither
appears in the additive integer-count bound.

## A sharper quadratic corollary

For nonnegative diagonal quadratic Hessians in the original box axes,
write `f_j=(1/2)sum_i h_ji x_i^2+affine` and use `C_ji=h_ji` in the
body allocation. Then the sharper quadratic constants remain valid:

```
max(0,Phi_K-A_r^tr)<=p_conv<=p_bin<=Phi_K+r,
A_r^tr=r+log2[omega_r(r+2)^(r/2)]<4r,
p_out<=p_conv+5r+1.                                     (4)
```

For the lower bound, the expected Jensen vector is exactly
`EJ=(1/4)C diag(Sigma)`. Thus `p_i=Sigma_ii/4` is feasible for the
body allocation. For the upper bound, the original-axis shared square
model has `|w-f(x)|<=Cp/8` coordinatewise, so unconditionality again
controls the whole error body. Apply the same rational allocation
oracle to obtain the constructive bound in (4).

This covers componentwise tolerances, weighted sums of absolute errors,
and Euclidean or other unconditional norm balls whenever their stated
oracle assumptions hold. Ellipsoids with arbitrary correlations are
not in general unconditional, so this statement does not absorb every
correlated-budget result.

## Scope and novelty boundary

The norm monotonicity, convex log-product allocation, weak optimization,
and polynomial interpolation ingredients are established. The proposed
extension is the positive Jensen-vector comparison with the whole
error body, retaining the same finite whole-formulation guarantee
without an output-dimension rounding penalty. The unconditionality
assumption is essential to the domination steps used here.
General convex downward-closed log-utility allocation is itself already
established in the bandwidth-sharing literature; it is not claimed as
new. The [source and novelty assessment](../notes/positive-separable-unconditional-error-novelty.md)
records that close predecessor, the exact GLS import, and the bounded
search for the whole-formulation guarantee. Publication priority remains
unestablished.

The [first independent audit](../notes/review-positive-separable-unconditional-precision.md)
and [second independent audit](../notes/review-positive-separable-unconditional-precision-second.md)
both passed for this extension and its rational log-product oracle.
The central-ball repair checker passed 24 cases with exact rational
feasibility and objective checks and 100-digit log-hypograph checks.
The polynomial Jensen and prefix-power checks are linked in the base
polynomial theorem.

The [supporting-scalarization and dyadic-layer refinement](positive-polynomial-loglog-degree-precision.md)
strengthens the degree dependence for this entire positive-polynomial
family. It gives a degree-independent lower allocation bound and a compact
rational construction with overhead `O(r+sum_i log log(D_i+2))`.
