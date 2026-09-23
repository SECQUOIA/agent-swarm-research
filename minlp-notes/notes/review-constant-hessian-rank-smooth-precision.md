# Independent audit: constant Hessian rank and smooth graph precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed result: `results/constant-hessian-rank-smooth-precision.md`.

## Verdict

The stated scalar theorem passes independent mathematical review. If a
smooth scalar function has constant Hessian rank `r` on a neighborhood
of a compact full-dimensional box, both the minimum general-integer
dimension of a convex graph relaxation and the minimum binary dimension
of a linear graph relaxation are

```
(r/2) log2(1/epsilon) + O_(f,B)(1).
```

The new upper-bound argument works with rotating Hessian null spaces.
It does not assume a fixed global null space, convexity of the function,
or convexity of its gradient fibers' union. Each final member is an
ordinary bounded polyhedron. No substantive mathematical correction
was needed. The theorem is existential with arbitrary real formulation
coefficients; it does not establish rational encoding complexity or
polynomial formulation size in the precision depth.

This audit does not establish novelty. The affine-fiber geometry is
classical. Nicola's Definition 1.1 and the following paragraph explicitly
state the affine-fibration property under constant Hessian rank on
printed page 3. I inspected the open primary manuscript. The result
correctly credits this ingredient and its transverse half-scale
decomposition. [Nicola, 2008](https://arxiv.org/pdf/0805.4122).

## Local coordinates and the affine fibers

A real symmetric matrix of rank `r` has a nonsingular principal minor
of size `r`. One justification uses symmetric elimination: a nonzero
diagonal gives a one-coordinate pivot, while an all-zero diagonal with
a nonzero off-diagonal entry gives a nonsingular two-coordinate pivot;
the Schur complement remains symmetric and its rank drops by the pivot
size. Induction gives the required principal index set.

At each base point, permute coordinates as `(u,v)` according to such an
index set. Invertibility of `f_uu` persists on a sufficiently small open
neighborhood. The Jacobian of `(u,v) -> (f_u(u,v),v)` is block triangular
with diagonal blocks `f_uu` and the identity. The inverse function theorem
therefore gives a smooth local inverse `(u(p,v),v)`. Its image and domain
can be reduced to contain an open product of parameter boxes. This is
a local differential transformation and does not need a globally defined
or convex Legendre transform.

For `g(p,v)=f(u(p,v),v)-p^T u(p,v)`, differentiation gives

```
g_p=-u,
g_v=f_v,
g_vv=f_vv-f_vu(f_uu)^(-1)f_uv.
```

Congruence block elimination shows that the rank of the full Hessian
is the rank of `f_uu` plus the rank of this Schur complement. The assumed
constant rank makes the complement identically zero throughout the
chart. On its connected convex `v` box, `g` is consequently affine in
`v`: `g(p,v)=b(p)^T v+c(p)`. Both coefficient functions are smooth, as
can also be seen by evaluating `g_v` and `g-b^T v` at one fixed interior
`v`. This establishes the displayed formula

```
u(p,v)=-Db(p)^T v-grad c(p).
```

For a fixed `p`, the resulting fiber parametrization is affine in the
original input coordinates, and `grad f=(p,b(p))` is constant on it.
The affine function `ell_p(u,v)=p^T u+b(p)^T v+c(p)` agrees with both
the value and the gradient of `f` at every point of this entire local
fiber. These are exactly the two identities needed for the subsequent
second-order error estimate.

## Uniform tubes and the domain boundary

Choose compact smaller parameter boxes `P_0,V_0` inside the open chart
and a larger compact `P_1` with `P_0` in its interior. For each fixed
`v`, the segment between points of `P_1` remains in that box. The bounded
`p` derivative of `u` on `P_1 times V_0` therefore provides one Lipschitz
constant for all those `v` values.

The image of this compact parameter product is a compact subset of the
original open smooth domain. It has a positive neighborhood radius inside
that domain. Reducing the radius if necessary gives a compact transverse
neighborhood on which the Hessian is uniformly bounded. Every segment
used in Taylor's formula lies in that neighborhood. The centers are
allowed to fall outside the original input box; their membership in the
smooth neighborhood is sufficient, and is why the neighborhood assumption
in the theorem is useful at boundary points.

Parameter cubes of radius `h` cover `P_0` using `O(h^(-r))` centers in
`P_1`. For each center, the set

```
v in V_0,
||u-u(p_center,v)||_infinity <= L h
```

is a bounded polytope: the central fiber map is affine in `v`, its domain
is a compact box, and every transverse coordinate is bounded. The
Lipschitz estimate proves that these polytopes cover the full image of
`P_0 times V_0`. It is unnecessary for a tube point's own gradient
parameter to belong to the parameter cube.

At any point in the tube, comparison with the central-fiber point having
the same `v` changes only the `r` coordinates in `u`. Both the function
and gradient errors vanish at that comparison point. If the Hessian
operator norm is bounded by `M`, Taylor's theorem gives explicitly

```
|f-ell_p| <= (M/2) r L^2 h^2.
```

This estimate holds on the entire polytope once `Lh` is within the chosen
neighborhood radius. It is independent of the tube index and its width.
Thus tube overlap and the possible curvature of the coordinate-chart
image create no gap.

Each original box point admits a smaller parameter product whose image
contains it in its interior. Those interiors form an open cover of the
box, including its boundary. Compactness selects finitely many charts.
Taking the largest error constant, the smallest valid positive width,
and summing their fixed covering constants gives a single global
`O(h^(-r))` bound. Intersecting each tube with the original input box
preserves polyhedrality, boundedness, coverage, and the Taylor estimate.

## Graph containment and binary encoding

Choose `h` proportional to `sqrt(epsilon)` with Taylor error at most
`epsilon/2`. On each intersected tube, the affine band
`|w-ell_p(x)|<=epsilon/2` contains every exact graph point over that tube.
Conversely, any point in the band has total vertical error at most
`epsilon`. Both requirements in the whole-graph relaxation definition
therefore hold. The input restriction to the original box is explicit.

For completeness, the binary encoding can be written using a polytope
`Q_i` for each nonempty banded tube and distinct binary codes `c_i`.
Introduce continuous weights and scaled copies satisfying

```
lambda_i >= 0,   sum_i lambda_i = 1,
y_i in lambda_i Q_i,
(x,w) = sum_i y_i,
z = sum_i lambda_i c_i,   z binary.
```

Each scaled-membership relation is represented by the homogeneous linear
inequalities of `Q_i`. Since every `Q_i` is nonempty and bounded, zero
weight forces its scaled point to be zero. For an integral code `z`,
each coordinate equal to zero forces all positively weighted codes to
have zero there; each coordinate equal to one forces them to have one.
Thus all positive weights select the same unique code. Convexity of its
polytope makes the projection exactly that member. Conversely every
member is obtained by setting its weight to one. Unused binary codes
produce no extra points.

There are `O(epsilon^(-r/2))` members and hence at most
`ceil(log2(number of members))` binary coordinates. Continuous lifting
dimensions and row counts may grow polynomially in `1/epsilon`, which
is permitted by the theorem. None is silently counted as a free binary
variable or assumed to have a succinct smooth-function representation.

## Lower bound, edge cases, and scope

The imported lower bound in
`results/smooth-map-local-rank-integer-complexity.md` has already received
an independent analytic audit in
`notes/review-nonquadratic-integer-precision.md`. Its scalar specialization
uses an interior point with a nonsingular `r`-coordinate Hessian slice,
the local oscillatory contact-volume estimate on that slice, and parity
classes of arbitrary integer lifts. Constant rank guarantees such an
interior point and slice. All smoothness and domain hypotheses match.
In particular, unbounded integer ranges and a nonclosed convex lifting
set are covered by that lower bound.

For `r=n`, the `v` box is zero-dimensional and the construction reduces
to ordinary Taylor cells. For `r=0`, the zero Hessian on the connected
box makes the function affine, giving an exact zero-integer graph.
Empty intersections can simply be discarded from the upper cover.
Asymptotic equality means equal leading coefficients with bounded
additive terms; it does not assert equality of the two integer minima
for each particular epsilon.

The examples also check: the Hessian of a Euclidean norm away from the
origin is a positive multiple of the orthogonal projector perpendicular
to its radius, hence has rank `n-1`; the Hessian of `x^2/t`, `t>0`, is
`(2/t^3) (t,-x)(t,-x)^T`, hence has rank one. Their rotating null spaces
are compatible with the local construction. The proof makes no claim
about rank-changing singularities, general vector maps, or a rational
polynomial-time algorithm for building the formulation from a smooth
function oracle.
