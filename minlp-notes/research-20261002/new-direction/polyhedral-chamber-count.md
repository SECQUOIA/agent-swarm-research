# Expected local grid counts for a fixed polytope

Date: 2026-10-02. Status: geometric proof; no algorithmic complexity claim.

A fixed compact polytope and a fixed smooth objective cannot make the
expected number of continuous bag grid tuples within `O(h^2)` of the true
optimum diverge as `h` tends to zero under independent ambient linear
noise with bounded densities. Constrained recourse can have upward kinks,
so the box proof's coordinatewise semiconcavity need not hold globally.
For a fixed polytope, however, recourse is semiconcave on finitely many
fixed polyhedral regions. Counting separately near each region's faces
gives a bound independent of `h`.

The constant below depends on the number and geometry of those regions,
as well as the objective curvature after affine substitution. These
quantities can grow badly with the input. This result does not establish
the sparse polynomial theorem's expected work bound for constrained
problems, and it does not supply a feasible rounding or pruning algorithm.

## Statement

Let `P` be a fixed nonempty compact polytope in `R^(b+q)`, with continuous
coordinates written `(v,z)`. The `b` coordinates of `v` form the bag under
consideration. Let `F_0` be twice continuously differentiable on a
neighborhood of `P`. Write

```
F_gamma(v,z) = F_0(v,z) + gamma_B'v + gamma_out'z,
Q = projection_v(P),
V(v) = min_{z : (v,z) in P} [F_0(v,z) + gamma_out'z],
f* = min_{v in Q} [V(v) + gamma_B'v].
```

The bag perturbations are independent of one another and of the outside
perturbations. Assume that every bag perturbation has density at most
`phi < infinity`. No density or bounded-support assumption is needed for
the outside perturbations.

For `0<h<=1`, let `G_h` be a deterministic grid in a fixed bounded box
containing `Q`. Assume that every axis-parallel cube of side `h` contains
at most a fixed number `D` of grid nodes. An ordinary mesh of spacing `h`,
with clipped box endpoints added, satisfies this condition. Fix
`eta>=0`, independently of `h`, and define

```
N_h = #{v in G_h intersect Q : V(v)+gamma_B'v <= f*+eta h^2}.
```

There are finite constants `C` and `h_0>0`, depending on the fixed data
just described but not on `h` or the outside perturbation realization,
such that

```
E[N_h] <= C                 for 0<h<=h_0.                    (1)
```

The same conclusion holds for independent uniform bag perturbations on
the `M>=2` equally spaced points of `[-sigma,sigma]`, with fixed
`sigma>0`, provided `M h>=1`. More precisely, that law gives a bound
of the form

```
E[N_h] <= C' (1+1/(M h))^b,                                  (2)
```

where `C'` is independent of `M`, `h`, and the outside realization. The
outside law may be continuous or discrete in this variant as well.

## Affine fiber vertices on closed polyhedral regions

Write the inequalities defining `P` as

```
A_v v + A_z z <= c.
```

Every nonempty fiber is a bounded polytope. Each of its vertices is
specified by `q` linearly independent active rows in the `z` coordinates.
Thus there are finitely many affine candidate maps

```
z_I(v) = (A_z)_I^(-1) [c_I-(A_v)_I v].
```

Their feasibility regions in `v` are polyhedra. Take a common polyhedral
refinement of these regions inside a fixed bounding box. The closures
`T` of cells whose relative interiors lie in `Q` form a finite cover of
`Q`. On the relative interior of each `T`, the list `J_T` of feasible
candidate maps is fixed. It is nonempty, and the fiber is their convex
hull.

The same representation holds on the entire closed cell:

```
{z : (v,z) in P} = conv{z_I(v) : I in J_T}    for every v in T. (3)
```

Here is the boundary argument, including degenerate vertices. Every map
in `J_T` remains feasible on `T` by continuity. Conversely, take a
boundary point `v` of `T`, a feasible `z` over it, and `w` in the relative
interior of `T` with a feasible `z_w`. For `0<t<1`, convexity of `P` makes

```
(v_t,z_t) = (1-t)(v,z) + t(w,z_w)
```

feasible, and `v_t` lies in the relative interior of `T`. Represent
`z_t` by convex weights on `J_T`. A subsequence of those weights converges
in the compact simplex as `t` tends to zero, proving (3). The argument
also applies to cells of lower dimension. If `q=0`, no fiber
representation is needed.

## Semiconcavity on each region

On a cell `T`, equation (3) gives

```
V(v) = min_{lambda in Delta(J_T)}
       [F_0(v, sum_I lambda_I z_I(v))
        + gamma_out' sum_I lambda_I z_I(v)].                 (4)
```

The minimization domain in (4) is a fixed simplex, independent of `v`.
For fixed `lambda`, the map from `v` to the full feasible point is affine.
The outside perturbation therefore contributes no second derivative.
Compactness, the bounded Hessian of `F_0`, and the finite list of affine
maps give a common finite `K>=0` such that every function in (4) has
Hessian at most `K I` along `T`. For example, an operator-norm Hessian
bound for `F_0`, multiplied by the largest squared norm of one of the
affine linear maps `v -> (v,z_I(v))`, suffices.

Subtracting `K ||v||^2/2` makes each function concave on `T`. Taking an
infimum preserves concavity. Consequently,

```
V(v+a)+V(v-a)-2V(v) <= K ||a||^2                            (5)
```

whenever `v-a` and `v+a` belong to the same cell `T`. The constant `K`
does not depend on the outside noise. No semiconcavity across different
cells is claimed.

## Face counting within one simplex

Triangulate each closed cell into finitely many closed simplices of its
own dimension. Fix one simplex `S`, of dimension `m<=b`, with affinely
independent vertices `a_0,...,a_m`. Write a grid point `v in S` in
barycentric coordinates `lambda_0,...,lambda_m`.

Take `h_0<1/(b+1)`. Call an index large if `lambda_i>=h`, and let `F`
be the face spanned by the large indices. There is at least one such
index. If `F` has dimension `k`, every omitted barycentric weight is
less than `h`, so

```
distance(v,F) <= (m+1) diameter(S) h.                        (6)
```

For every fixed `S` and `F`, the number of grid nodes satisfying (6)
is at most `C_(S,F) h^(-k)`. One direct proof covers the bounded
`k`-dimensional face by `O(h^(-k))` balls of radius `h`; its `O(h)`
neighborhood then meets only a constant number of mesh cubes per ball.
The assumed grid occupancy bound applies in each cube. This argument
works for oblique faces and for simplices of dimension less than `b`.

Choose one large vertex `a_r`. For every other large vertex `a_j`, set

```
d_j = a_j-a_r.
```

There are `k` linearly independent directions. Both `v+h d_j` and
`v-h d_j` lie in `S`: these moves transfer barycentric weight `h`
between two coordinates that are each at least `h`. The comparison
points need not be grid nodes. They are feasible bag values, which is
all that comparison with the true optimum requires.

If `v` is counted in `N_h`, comparison with those two points gives

```
[V(v)-V(v+h d_j)-eta h^2]/h
    <= gamma_B'd_j
    <= [V(v-h d_j)-V(v)+eta h^2]/h.                          (7)
```

By (5), the interval in (7), if nonempty, has length at most

```
w_j h,             w_j = K ||d_j||^2 + 2 eta.                (8)
```

Conditional on the outside noise, these intervals are deterministic.
In particular, their endpoints do not depend on any bag perturbation.

## Joint noise probability and summation

Form the `k` by `b` matrix with rows `d_j'`. Choose a nonsingular
`k` by `k` coordinate minor `R`. Condition on all bag perturbations
outside its selected columns. Applying `R^(-1)` to the intervals in
(7) puts each remaining bag perturbation in an interval of length at
most

```
alpha_i h,     alpha_i = sum_j |(R^(-1))_(ij)| w_j.           (9)
```

The `k` unconditioned perturbations remain independent. The probability
of all the necessary tests is therefore at most

```
product_i (phi alpha_i h)                                   (10)
```

in the continuous case. An empty interval gives probability zero. When
`k=0`, the empty product is one. Multiplying (10) by the grid-node bound
`C_(S,F) h^(-k)` cancels all powers of `h`. Summing over the finitely
many faces and simplices proves (1). Counting a node in more than one
simplex only enlarges this upper bound.

For the finite uniform law, an interval of length `alpha_i h` contains a
fraction at most `alpha_i h/(2 sigma)+1/M` of the support. Independence,
after the same conditioning, bounds the probability by

```
product_i [alpha_i h/(2 sigma)+1/M].                        (11)
```

Multiplication by `C_(S,F) h^(-k)` gives a fixed polynomial in
`1/(M h)` of degree at most `k<=b`. Summation proves (2), and hence
the asserted uniform bound when `M h>=1`.

## Scope and verification

This is a bound for true feasible near-optimal bag tuples. It does not
show that a particular constrained relaxation or pruning rule retains
only such tuples. It also does not bound the cost of constructing the
regions, computing recourse, rounding feasibly, or closing an exact
optimization certificate.

The proof rules out an `h`-divergent example with one fixed polytope,
one fixed smooth objective, fixed noise density bounds, and fixed bag
dimension. It does not give a bound uniform over polytopes with an
increasing number of fiber regions or deteriorating affine-map and
direction-minor conditioning. Those constants can depend on coordinates
outside the bag and can grow exponentially with the input size. Total
unimodularity or an order-constraint label alone is not a bound on all
of these constants.

The affine fiber representation, boundary extension, directional
intervals, and finite-law calculation were checked directly in the
proof. A separate reader reviewed the completed argument, including
oblique-face counting and the finite-noise conditioning, and found no
blocker. No numerical test is needed for these geometric statements.
The targeted formatting command was `git diff --no-index --check
/dev/null research-20261002/new-direction/polyhedral-chamber-count.md`;
it emitted no whitespace diagnostics. Its exit code was one because
the comparison is against a new, nonempty file.
No project-wide verification, CI inspection, or literature search was
performed.
