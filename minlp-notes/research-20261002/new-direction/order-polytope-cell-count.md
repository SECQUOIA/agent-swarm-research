# Expected near optimal grid counts for order polytopes

Date: 2026-10-02. Status: local counting theorem; no exact constrained
optimization or runtime theorem is asserted.

For continuous order constraints, the polyhedral recourse regions depend
only on the ordering of the bag coordinates. This gives an explicit
expected bound on the number of truly near-optimal bag grid tuples.
The bound depends on the total variable count and an ambient Hessian
upper bound, but not on the number of affine fiber maps or the size of
the order graph outside the bag.

The result specializes the general argument in
[the polyhedral chamber note](polyhedral-chamber-count.md). Together
with [feasible TU rounding](tu-feasible-rounding.md), it supplies two
ingredients for a possible constrained extension of
[the polynomial box theorem](smoothed-sparse-polynomial.md).
It does not supply that theorem's exact constrained closure step.

## Statement and bound

Let `P` be the order polytope

```text
P = {x in [0,1]^n : x_i <= x_j for every specified directed edge i -> j}.
```

All variables are continuous. Directed cycles are allowed; they impose
equalities. Let `F_0` be twice continuously differentiable on a
neighborhood of the box, with

```text
Hess F_0(x) <= H I             throughout [0,1]^n,   H>=0.    (1)
```

Choose a bag `B` of size `1<=b<=n`, write `x=(v,z)`, and set

```text
F_gamma(v,z) = F_0(v,z) + gamma_B'v + gamma_out'z,
Q = projection_B(P),
V(v) = min_{z : (v,z) in P} [F_0(v,z)+gamma_out'z],
f* = min_{v in Q} [V(v)+gamma_B'v].
```

The bag noises are independent of one another and of the outside noises.
For the finite law, each bag noise is uniform on the same `M>=2`
equally spaced values in `[-sigma,sigma]`, where `sigma>0`. The
outside noise law is arbitrary. The continuous version instead uses
independent uniform bag noises on that interval.

Let `h=1/r`, where `r>=1` is an integer, and let `eta>=0`. Count

```text
N_h = #{v in Q intersect {0,h,...,1}^b :
        V(v)+gamma_B'v <= f*+eta h^2}.
```

For the finite law, define

```text
A_h = (b n H+2 eta)/(2 sigma) + 1/(M h).
```

Then

```text
E N_h <= b! sum_(k=0)^b [binom(b+1,k+1)/k!] A_h^k
       <= b! (b+1) (1+A_h)^b.                               (2)
```

For continuous uniform noise, the same bound holds after omitting
`1/(M h)` from `A_h`. Thus the continuous bound is independent of
`h`, and the finite-law bound is independent of `h` whenever
`M h>=1`, after replacing that term by one.

## Bag ordering determines the recourse regions

The projection `Q` is exactly the order polytope on the bag coordinates
induced by reachability in the full directed graph. Necessity follows
by chaining inequalities. For sufficiency, assign each coordinate the
maximum of zero and the values of all bag coordinates that can reach
it, including itself when it is a bag coordinate. This extends every
bag vector satisfying the induced order inequalities to a point of
`P`.

For each permutation `pi` of the bag coordinates, use the standard
order simplex

```text
S_pi = {0 <= v_pi(1) <= ... <= v_pi(b) <= 1}.
```

An induced order inequality either holds throughout `S_pi` or forces
two coordinates, and every ordered coordinate between them, to be
equal. Therefore `T_pi=Q intersect S_pi` is a face of `S_pi`.
The at most `b!` faces `T_pi` cover `Q`; overlaps cause no problem
for an upper bound.

Every vertex of a fixed recourse fiber has each outside coordinate
equal to one of

```text
0, 1, v_1, ..., v_b.                                        (3)
```

To see this, group outside coordinates connected by tight order
equalities. A component that touches neither a tight coordinate bound
nor a bag coordinate can be shifted slightly in both directions while
preserving every inequality. Such a point is not a vertex. Each
component at a vertex is therefore anchored at one of the values (3).

There are finitely many affine maps that assign an anchor from (3) to
each outside coordinate. Their feasibility is determined only by
comparisons between anchors. On the relative interior of a fixed
`T_pi`, those comparisons have a fixed weak order, so the list of
feasible maps is constant. The fiber is the convex hull of that list,
because all its vertices occur in the list.

This representation remains valid on the closed face `T_pi`.
The feasible maps remain feasible there by continuity. For the reverse
inclusion, interpolate any boundary fiber point toward a feasible point
over the relative interior of `T_pi`. Represent the interpolated points
by convex combinations of the fixed maps, and pass to a convergent
subsequence of weights. This also covers equal bag values and
degenerate fiber vertices.

## Uniform semiconcavity within each face

For each feasible affine copy map, the full point `x` is an affine
function of `v`. Its linear part has one row for each full coordinate.
Every row is either zero or a coordinate unit vector. Hence its squared
operator norm is at most `n`. The same bound holds for any convex
combination of the copy maps.

The preceding fiber representation writes `V` on `T_pi` as a
minimum over a fixed simplex of convex-combination weights. For each
fixed choice of weights, (1) bounds the substituted objective's Hessian
above by `n H I`. The substituted outside linear noise has zero
Hessian. Taking the infimum preserves semiconcavity, so

```text
V(v+a)+V(v-a)-2V(v) <= n H ||a||^2                           (4)
```

whenever `v-a` and `v+a` belong to `T_pi`. This bound does not
depend on the outside noise realization or the number of copy maps.

## Counting grid nodes by simplex faces

The vertices of `S_pi` form a nested chain of zero-one vectors

```text
a_0=0, a_1, ..., a_b=1,
```

where each step changes one coordinate from zero to one. Consider a
`k`-dimensional face `F` with vertices
`a_(t_0),...,a_(t_k)`, indexed so that `t_0<...<t_k`.

Every grid point in the relative interior of `F` has positive
barycentric coordinates that are multiples of `h`. This follows
directly by expressing the coordinates as successive gaps between
ordered grid values, including the gaps from zero and to one.
Conversely, every such barycentric vector gives a grid point.
Consequently, the number of these points is

```text
binom(r-1,k) <= r^k/k!,                                     (5)
```

with the binomial coefficient understood to be zero when `k>r-1`.

For a grid point in this relative interior, define

```text
d_j = a_(t_j)-a_(t_(j-1)),             j=1,...,k.
```

These directions have disjoint nonempty supports and entries in
`{0,1}`. Each has squared norm at most `b`. Both `v+h d_j`
and `v-h d_j` stay in `F`, since the move transfers weight
`h` between two positive barycentric coordinates, each of which is
at least `h`.

Every point of `T_pi` lies in the relative interior of a unique
face `F` of `S_pi`, and that face is contained in `T_pi`.
Thus (4) applies to these moves.

## Independent directional tests

For a truly near-optimal tuple `v`, comparison with the two feasible
points `v+h d_j` and `v-h d_j` confines `gamma_B'd_j` to

```text
[V(v)-V(v+h d_j)-eta h^2]/h
    <= gamma_B'd_j
    <= [V(v-h d_j)-V(v)+eta h^2]/h.
```

Conditional on the outside noise, these intervals are fixed and have
length at most

```text
(n H ||d_j||^2+2 eta) h <= (b n H+2 eta) h.                  (6)
```

Choose one coordinate from each direction's support, and condition on
all other bag noises. Because the supports are disjoint, the selected
coordinate minor is the identity. Each test restricts its one remaining
independent uniform noise to an interval of the length in (6).

For the finite law, the conditional probability that all `k` tests
hold is therefore at most

```text
[(b n H+2 eta)h/(2 sigma)+1/M]^k = (h A_h)^k.                (7)
```

For continuous uniform noise, omit `1/M`. The empty product for
`k=0` is one.

Multiplying (7) by (5) bounds the expected contribution of each
`k`-face by `A_h^k/k!`. A full `b`-simplex has
`binom(b+1,k+1)` such faces, and there are at most `b!`
permutations. Summing, while allowing duplicate counting across
permutations, gives the first inequality in (2). The second follows
from `binom(b+1,k+1)/k! <= (b+1) binom(b,k)`.

## What the bound supplies

This is an explicit count for true feasible near-optimal bag tuples.
The number of affine recourse maps can be exponential, but it does not
appear in (2). No construction or enumeration of those maps is claimed.

Order constraints meet the matrix and grid assumptions of the
[TU rounding lemma](tu-feasible-rounding.md), with the same full
Hessian upper bound `H`. That lemma supplies feasible rounding error
`E=n H h^2/8`. If a separately justified pruning scheme gives each
retained tuple a true feasible witness within `2E` of the optimum,
then this counting result applies with `eta=n H/4`.

The result alone does not prove such a pruning implementation,
polynomial bit complexity for an exact constrained closure step, or
the complete expected exact optimization theorem. It also does not
replace (1) by the polynomial box theorem's coordinatewise diagonal
curvature bound.

The vertex representation, face geometry, grid count, and finite-noise
interval calculation were checked analytically. A separate reader
reviewed the complete argument and found no mathematical blocker.
No numerical tests,
project-wide verification, CI inspection, or literature search were
performed.
