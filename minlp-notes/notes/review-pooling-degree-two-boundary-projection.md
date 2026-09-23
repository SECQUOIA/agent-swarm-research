# Independent review: bounded path endpoint projection

Date: 2026-09-05. Verdict: **PASS** for the composition lemma, pooling
feasibility reduction, and exact algebraic reconstruction in
[the assembled draft](pooling-degree-two-boundary-projection.md).
Separate literature priority is not established.

## Endpoint-composition formula

For compact convex polygons `P(x,y)` and `Q(y,z)`, first intersect `P`
with the strip given by the `y` projection of `Q`. This adds at most
two inequalities. If the result is empty, the composition is empty.
On its `x` domain write its vertical interval as `[l(x),u(x)]`, where
`l` is convex and piecewise affine and `u` is concave and piecewise
affine. Let `q(y)` be the convex lower envelope of `Q` on its domain.

Let `[a,b]` be the minimizer interval of `q`, and let `m=min q`.
Define `D(t)=q(t)` for `t<a` and `D(t)=m` otherwise; define
`L(t)=m` for `t<=b` and `L(t)=q(t)` otherwise. Then `D` is convex
and nonincreasing, while `L` is convex and nondecreasing. Directly
considering whether `[l(x),u(x)]` lies left of, intersects, or lies
right of `[a,b]` proves

```
min_{l(x)<=y<=u(x)} q(y) = max(L(l(x)),D(u(x))).
```

Both terms on the right are convex. The formula handles a nontrivial
minimum plateau and minima at endpoints, as well as a unique minimizer.
The composed upper envelope follows by reflecting the `z` coordinate.

## Additive piece count and balanced recursion

Partition the `x` domain at the breakpoints of `l`, and at the boundary
points of preimages under `l` of all breakpoints of `L`. A level of a
one-dimensional convex function has at most two isolated preimages,
or can persist on an interval whose boundary has at most two points.
Thus this partition has `O(k_l+k_L)` pieces. On each piece the
composition `L(l(x))` is affine; a flat preimage introduces no hidden
extra pieces. The same argument applies to `D(u(x))` using concavity
of `u`.

A convex piecewise-affine function is the maximum of its supporting
affine pieces on its domain. Taking the maximum of two such functions
uses the union of those affine pieces, so it has at most their total
number of pieces. The upper envelope has the analogous bound after
reflection. Vertical domain boundaries add at most two more facets.
Therefore there is a universal constant `C` such that composition has
complexity at most `C(r_P+r_Q+1)` when complexity counts a finite
polygon representation, including constant-size descriptions for
segments and points.

A balanced binary composition tree on a chain of `n` relations has
height `O(log n)`. The additive bound with a constant factor gives
`n^{O(1)}` total and maximum representation size, even though the
result need not have only linearly many facets. A claim of linear
overall size would need a sharper argument and is not being made.

Each composition can be computed by elementary rational operations:
Fourier–Motzkin elimination of the common coordinate generates a
quadratic number of rows in the input sizes, followed by planar
redundancy removal. The small output bound applies after removing
redundancy. Another implementation can use the envelope construction
directly. Intermediate rational bit lengths remain polynomial: the
retained polygon vertices and facets belong to a coordinate projection
of a rational bounded chain polytope, and can be bounded using rational
LP bases and determinant bounds in that original polytope. Normalizing
the resulting rational rows avoids retaining unnecessarily large
common factors.

The draft's direct arithmetic-depth argument also passes. Each output
line or breakpoint uses a bounded-depth expression of child rows:
planar line intersection, clipping by a coordinate range, affine
composition, and selection among candidate lines. Thus reduced bit
length obeys `B_parent<=C(B_left+B_right+1)` for a universal constant.
Balanced logarithmic depth gives polynomial bit length. The loose
numerical row bound `16(m_P+m_Q+2)` safely dominates both envelopes,
their flattening/clipping overhead, and two vertical boundary rows.

Empty sets are handled before envelope construction. If the remaining
`x` domain is a singleton, the composed relation is a vertical segment
or point, found by two small LPs. If the `y` domain of `Q` is a
singleton, clipping fixes `y`; its section in `z` combines with the
remaining interval in `x`. Nonvertical segments have equal affine
lower and upper envelopes and need no different formula.

## Announced pooling mapping

For one pool with at most two incident input arcs and two incident
output arcs, remove its at most four adjacent source/output vertices
from the bypass graph. If the bypass graph has maximum degree two,
there are at most eight incident bypass arcs to retain in the core,
including arcs between two removed vertices. Keep the at most four
pool arcs and one source-mixture fraction in the core as well.

Every remaining component is a path, a cycle, or an isolated vertex.
A path has at most two exposed core arc coordinates. A node not
adjacent to the pool has only its at most two bypass flows: its
supply/demand and quality rows therefore involve at most two scalar
variables, with rational constant coefficients. Local arc bounds make
these relations compact when the input has finite rational upper
bounds. Two-boundary path components can be replaced by the polynomial
endpoint projection; components with one or no boundary can instead
be treated by ordinary linear projection or feasibility. Detached
cycles contain no core coordinates and are checked by LP.

The removed node constraints use only the fixed set of core flows.
With mixture fraction `theta`, the two pool input flows are
`theta*T` and `(1-theta)*T`, where `T` is the sum of the pool output
flows. Every pool quality is affine in `theta`, even if the number
of quality attributes grows. Hence all remaining quality rows are
quadratic polynomials in a fixed number of core variables. Fixed-
dimensional real-algebraic feasibility can then decide the remaining
system in polynomial binary time. At zero throughput any fraction
is admissible; it does not permit a nonzero output because conservation
and nonnegativity remain present. Missing arcs can be fixed to zero.

This argument concerns feasibility. A dense objective threshold would
couple the otherwise projected path interiors and is not represented
by these two-coordinate endpoint relations. It does not establish
polynomial global optimization, nor contradict the earlier exponential
cost-message examples.

The written thirteen-variable count is valid: four pool arcs, at most
eight distinct incident bypass arcs, and the scalar mixture fraction.
An arc between two removed vertices is counted only once. If a bypass
cycle meets a removed node, its remaining path may have both boundary
arcs incident to that same removed node; their flow coordinates are
still distinct endpoints of a scalar chain. An isolated retained node
can have zero, one, or two such boundary arcs and is covered by the
same cases. Detached components with required positive throughput and
no feasible flow must be rejected; the draft includes this check.

## Exact reconstruction

Fixed-dimensional sampling supplies feasible core coordinates in a
single represented real-algebraic field of polynomial degree and
encoding length. At a composition node with feasible outer endpoints,
the possible shared coordinate is the intersection of the two child
slices. Both slices are closed bounded intervals and the intersection
is nonempty by the retained exact relation. Its midpoint is feasible
for both children, so recursion lifts the entire chain.

After choosing the active interval bounds, each such midpoint is an
affine function of its parent endpoint coordinates with rational
coefficients. Division in computing a slice endpoint is only by a
nonzero rational row coefficient; there is no new algebraic extension.
Along the balanced reconstruction tree, those affine expressions have
polynomial rational coefficient bit length. Thus all recovered flows
stay in the core's common field with polynomial total output encoding.
Rational feasible points for detached LP components introduce no new
extension either. Pool qualities are then affine in the sampled
mixture fraction. This proves the draft's exact constructive guarantee,
not merely a decision procedure.

## Fixed-support optimization addendum

I independently reviewed Section 5 of the updated draft. Verdict:
**PASS** for a fixed number `s` of designated actual arc coordinates,
fixed-degree polynomial objectives, and closed polynomial equalities
or weak inequalities on those coordinates and the original core.

Retaining a designated interior flow cuts the scalar path into smaller
two-boundary relations. If the arc belongs to a detached cycle, cut
at that arc and identify the two endpoint occurrences: substituting
the same retained coordinate in `R(x,x)` gives the exact cycle
condition. Several retained arcs split a cycle into ordinary two-
endpoint segments. Thus no hidden extra state coordinate is needed,
and the core has at most `13+s` variables.

The finite original flow bounds and closed added rows give a compact
feasible core. Its exact projected linear relations plus the fixed-
degree polynomial rows form a fixed-dimensional semialgebraic set.
Polynomial objective-value elimination and sampling recover the
attained extreme value and a feasible algebraic optimizer in
polynomial bit time. The preceding affine reconstruction preserves
both feasibility and the value because every objective coordinate
was retained. Strict side inequalities are outside this compact-
attainment statement.

A dense written linear objective is covered only when a supplied
polynomial-bit linear combination of exact model equalities proves
that it agrees with a bounded-support objective plus a constant on
the entire feasible set. Rational linear algebra verifies that
identity. Approximate equalities, inactive inequalities, or equality
only at selected candidates would not justify the reduction. The
draft states the required conservation/contract restriction correctly.

## Independent exact checks and antecedent

[check_boundary_projection_review.py](../code/pooling_bypass_paths/check_boundary_projection_review.py)
uses direct Fourier–Motzkin elimination and exact rational planar
vertices independently of the envelope formula. It passed 70 polygon
compositions and 480 lower/upper section identities, including a
vertical segment, a nonvertical segment, and a point. It checks the
flattened-branch formula and compares it to projected sections at all
projected vertex coordinates and interval midpoints. These finite
checks support the analytic count; they do not prove an asymptotic
bound by themselves.

An important primary antecedent is
[Simon, King, and Howe, The Two Variable Per Inequality Abstract Domain](https://www.cs.kent.ac.uk/pubs/2010/3167/content.pdf),
Section 3, printed pages 27–28. It explicitly discusses projection
closure via resultant elimination and cites Nelson's 1981 thesis for
a polynomial-size normalized closure assertion. I inspected those
pages; the precise complexity/encoding scope of that general assertion
requires further source comparison. Thus TVPI projection closure is
known, and the present direct bounded-path size proof should not be
called a new general elimination principle without that comparison.
