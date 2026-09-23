# Polynomial feasibility and bounded-support optimization through degree-two bypass paths

Date: 2026-09-05. Status: endpoint composition, pooling feasibility and
exact reconstruction, and bounded-support optimization passed two
independent audits. Literature priority remains provisional.

The proposed theorem concerns feasibility with lower and upper flow
bounds. It does not include a profit threshold or a dense linear side
constraint. With every lower bound zero, ordinary feasibility is already
trivial because zero flow is feasible.

**Theorem.** Standard pooling feasibility is decidable in
polynomial rational bit time when there is one pool with exactly two
input arcs and two output arcs and the bypass graph has maximum degree
two. The number of qualities, distinct input-quality vectors, inputs,
outputs and bypass arcs may all grow. Finite rational flow bounds are
given, and arbitrary lower/upper output quality specifications are
allowed. There are no pool-to-pool arcs. The construction also
recovers an exact real-algebraic feasible flow when one exists.

The key distinction from the earlier exponential path response is that
only a fixed number of physical boundary arc coordinates are projected.
There is no dense accumulated-cost coordinate in this projection.

Combined with the reviewed constant-data construction, this yields a
sharp maximum-output-degree feasibility boundary when input degree is
at most two: degree two is polynomial, while degree three is strongly
NP-complete with fixed numerical alphabets. Section 6 gives the exact
scope, including the positive flow contracts in the hard instances.

## 1. Composition of two compact polygonal relations

Let `P subset R^2` have coordinates `(x,y)`, and let `Q subset R^2`
have coordinates `(y,z)`. Both are bounded rational polyhedra, including
lower-dimensional cases. Define

```
R=P composed with Q
 ={ (x,z) : exists y, (x,y) in P and (y,z) in Q }.
```

Suppose their descriptions have `m_P,m_Q` linear inequalities. The
claim is that `R` has a description with at most
`16(m_P+m_Q+2)` inequalities, constructible by polynomially many
rational operations. The constant is deliberately loose.

First compute the interval `J=projection_y Q`, and intersect `P`
with `y in J`. This adds at most two rows. Empty sets are detected
directly. Write the resulting vertical slices of `P` as
`[l(x),u(x)]`, over its interval of `x` values. The lower envelope
`l` is convex piecewise affine, and the upper envelope `u` is concave
piecewise affine; each has at most `m_P+2` pieces. Write the lower
and upper envelopes of `Q` as `q(y),r(y)`.

The minimum possible `z` at fixed `x` is

```
g(x)=min { q(y) : l(x)<=y<=u(x) }.
```

Let `[a,b]` be the minimizer interval of the convex function `q`, and
let `q_min` be its minimum. On its domain define

```
D(t)=q(t) for t<a, and q_min for t>=a,
L(t)=q_min for t<=b, and q(t) for t>b.
```

Here `D` is convex and nonincreasing; `L` is convex and nondecreasing.
Directly checking whether the interval lies below, meets, or lies above
`[a,b]` gives

```
g(x)=max { L(l(x)), D(u(x)) }.                              (1)
```

Both functions inside this maximum are convex. Each composition can
change its affine formula only at a knot of the inner function or at
the preimage of an outer knot. A level set of a univariate convex or
concave piecewise-affine function has at most two boundary points,
including the case of a flat interval. Therefore each composition has
at most `m_P+2m_Q+O(1)` affine pieces. The maximum of two convex
piecewise-affine functions has at most the sum of their numbers of
affine pieces: write each as the maximum of its affine pieces and
combine those lists. This bounds the lower envelope by
`2m_P+4m_Q+O(1)` pieces.

Reflecting the `z` coordinate gives the same bound for the upper
envelope. Two vertical boundary rows then describe `R`. Keeping the
elementary clipping and flat-branch overhead gives the loose displayed
bound `16(m_P+m_Q+2)`.

These operations are constructive. Convert each bounded planar
polyhedron to ordered boundary segments by pairwise line intersections
and feasibility checks, remove redundant segments, find the minimum
plateau, subdivide inner segments at the relevant outer-knot levels,
and form the two affine envelopes. Every operation is a rational
comparison, intersection, or affine composition.

If an `x` domain is a singleton, the result is a vertical interval,
computed by optimizing the two `Q` envelopes over the feasible `y`
interval. If the common `y` domain is a singleton, the result is a
rectangle or a lower-dimensional rectangle. Other one-dimensional
polygons have coincident affine envelopes and are covered by (1).
Points and empty relations are handled directly. No full-dimensionality
or strict-inequality assumption is used.

## 2. A whole path and bit complexity

Consider a path relation on bounded scalar variables

```
(x_(i-1),x_i) in P_i,  i=1,...,h.
```

Compose adjacent relations in a balanced binary tree. Each composition
increases the row count by at most a constant times the sum of its
children's counts plus a constant. At depth `ceil(log_2 h)`, the
endpoint relation therefore has at most

```
16^ceil(log_2 h) * O(sum_i(m_i+2)) = h^O(1) * sum_i(m_i+2)
```

rows. The same bound controls the total intermediate description size,
so polynomial-time planar operations at every node give polynomial
arithmetic complexity. Balancing is essential to this argument; the
bound does not claim that an arbitrary sequential elimination order
keeps a polynomial number of rows.

The rational arithmetic also has polynomial bit complexity. At one
composition, a new affine coefficient is obtained by a constant number
of additions, products and divisions of coefficients or intersection
coordinates from its two children. An intersection of two lines also
uses a constant number of such operations. Envelope formation selects
among these lines; it does not repeatedly combine an unbounded list of
coefficients into a new line. Thus the maximum reduced rational bit
length at a node is bounded by a fixed constant times the sum of the
children's bit lengths, plus a constant. The balanced logarithmic depth
turns this into a polynomial bound in the original encoding length.
Sorting and redundancy comparisons likewise use polynomial bit length.

Retain the composition tree to reconstruct eliminated coordinates.
Given feasible endpoints `(x,z)` at an internal node, intersect the
slice of its left child at `x` with the slice of its right child at
`z`. These are closed bounded intervals of possible shared `y` values.
Choose their midpoint and recurse. This proves constructive lifting,
using only rational affine evaluation, order comparisons and averaging.
After the active slice bounds are selected, each recovered coordinate
is an affine function of its two parent endpoints with rational
coefficients: division is only by a nonzero rational row coefficient.
Thus the same operations work over the core's represented real-algebraic
field without new field extensions or algebraic inversions. The balanced
tree gives polynomial coefficient growth in these affine expressions.

## 3. Split off the pool attachments

The pool has two feeding input nodes and two receiving output nodes.
Call these four nodes the attachment set. Put in a nonlinear core:

```
the four input-pool and pool-output arc flows;
every bypass arc incident to an attachment node (at most eight);
one pool intake fraction theta in [0,1].
```

This is at most thirteen scalar variables. All capacity rows at the
four attachment nodes use core variables only. If the two input quality
vectors are `C_1,C_2`, write every pool attribute as

```
q_k=theta*C_(1k)+(1-theta)*C_(2k).
```

The core constraints include conservation and
`y_1=theta*(y_1+y_2)`. These give the correct mixing proportion at
positive throughput; at zero throughput, any `theta` is valid. Quality
rows at the two receiving outputs are polynomials of degree at most
two in the core. The number of attributes may be arbitrary because
each contributes another row in the same fixed-dimensional core.

Delete the attachment nodes from the bypass graph. The remaining
components are paths, isolated nodes, or cycles. A component meeting
the deleted set is a path with at most two boundary arcs, whose flow
coordinates were retained in the core. Every internal input has only
two incident flow variables in its supply rows. Every internal output
has only two known-quality bypass flows in its demand and quality
rows. Hence the component is a scalar 2VPI path in its arc flows.
Individual arc bounds can be included in adjacent relations.

Apply Section 2 to replace such a component by its exact linear
relation on the retained boundary arc flows. A path with only one
boundary arc has an interval projection. It can be treated by the
same construction with an extra endpoint variable fixed to zero,
using the original terminal's univariate rows as a degenerate polygonal
relation. Paths with no boundary and detached cycles are ordinary
rational LP feasibility problems. Isolated nodes with positive required
throughput and no usable arc are detected as infeasible.

An arc whose two endpoints are both attachment nodes already belongs
to the core and needs no elimination. A bypass cycle meeting an
attachment becomes a path between two retained boundary arcs, even if
those two arcs meet the same attachment. This does not create a cycle
in the relation-composition calculation.

## 4. Decide and reconstruct

After eliminating the path interiors, feasibility is equivalent to a
fixed-dimensional existential real-algebraic system. It has polynomially
many rows, degree at most two, and polynomially encoded rational
coefficients. Fixed-dimensional real-algebraic decision and sampling
therefore give a polynomial-bit algorithm for the core.

If feasible, represent all core coordinates in one real-algebraic field,
then recover the boundary-connected paths from their retained
composition trees. Those trees use only affine field operations and
comparisons and have polynomial depth, size and coefficient lengths.
Detached rational LP components supply independent rational feasible
points. Together these give a feasible original flow and all pool
qualities. The standard three-layer model and finite flow bounds are
essential scope assumptions.

## 5. Optimization with a fixed number of retained flow coordinates

Fix an integer `s` independently of the instance size. Designate at most
`s` actual arc-flow coordinates in addition to the core coordinates
already retained. A polynomial objective of fixed degree on these
coordinates can be optimized exactly in polynomial rational bit time.
Polynomially many additional closed polynomial equalities or inequalities
of fixed degree on these same coordinates are also permitted. The
algorithm returns an exact algebraic optimum and an original feasible
flow, or reports infeasibility.

To prove this, retain the designated coordinates in the core and cut the
scalar relation chains at them. Each remaining chain segment still has
at most two retained endpoints. If a designated arc belongs to a detached
cycle, cut that cycle at this arc: the endpoint relation has the form
`R(x,x)` because both endpoint occurrences refer to the same retained
flow. Multiple designated arcs cut the cycle into ordinary two-endpoint
segments. Univariate relations and segments with no retained endpoint
are handled as before. There are at most `13+s` core variables, and all
projected relations have polynomial description and bit size.

The feasible core is compact, being the exact projection of the bounded
physical formulation with the closed additional rows. A continuous
polynomial objective therefore attains its optimum on every nonempty
core. Fixed-dimensional real-algebraic optimization gives the exact
optimum and an algebraic optimal sample. One implementation eliminates
the core coordinates from the formula specifying attainable objective
values and selects the attained extreme endpoint, then samples its
fiber. The total variable count and polynomial degree remain fixed.
The same affine reconstruction recovers the path interiors.

For a linear objective, this includes any cost vector supported on a
fixed number of actual arcs. It also includes a dense written objective
when an explicitly supplied rational linear combination of the model's
exact conservation or contract equations reduces that objective to
bounded support plus a constant. The equality reduction is checked by
rational linear algebra. Its coefficients must have polynomial encoding
length. This corollary does not assume that arbitrary dense costs have
such a reduction.

For example, on a bypass path with exact input supplies `S_i`, write
its two input arcs as `S_i-t_i,t_i`, and let consecutive output revenues
be `R_(i-1),R_i`. Output revenue on that path equals
`sum_i R_(i-1) S_i + sum_i (R_i-R_(i-1)) t_i`.
Production costs on its exact-supply inputs are constant. Thus a fixed
number of price changes along the coupled paths gives the required
bounded support, even if the written profit contains many nonzero terms.
A fixed number of distinct prices alone does not bound their number of
changes.

## 5.1. Multiple pools with a fixed total number of incident arcs

Fix the total number `a` of input-pool and pool-output arcs. The same
feasibility and bounded-support optimization conclusions hold with
multiple pools, arbitrary many quality attributes, and a bypass graph
of maximum degree two. Pool-to-pool arcs remain excluded. This is a
routine extension of the core construction.

There are at most `a` external attachment nodes. Retain the `a`
pool-incident flows, at most `2a` bypass flows incident to these nodes,
and one input fraction for each allowed input-pool arc. The total
fraction count is at most `a`, so the core has at most `4a` variables.
For each pool, its fractions are nonnegative and sum to one, its quality
vector is their affine combination of feed quality vectors, and each
intake equals its fraction times total pool intake. All required rows
have degree at most two even when the quality count grows. Shared
external attachment nodes cause no problem because all their incident
flows are retained.

A pool with no incoming or no outgoing arc must have zero throughput
and zero incident arc flows. Reject incompatible positive lower bounds
on that pool or those arcs before removing them. Preserve adjacent
external-node supply and demand requirements: bypasses or other pools
may satisfy them. If `a=0`, the whole instance is a rational LP.
Inactive retained pools permit any legal input-fraction vector.

After deleting the attachment nodes, the remaining components and
projection procedure are exactly those in Sections 2–4. At most a fixed
number of extra designated objective coordinates increases the core
count by that number. The same compact algebraic optimization and affine
path reconstruction apply. Both the
[first extension audit](../notes/review-pooling-bounded-attachments.md) and
[second extension audit](../notes/review-pooling-bounded-attachments-second.md)
pass, including the zero-throughput preprocessing and arbitrary quality
count.

## 6. A degree-two versus degree-three feasibility boundary

Consider standard pooling with exactly one pool, exactly two actual pool
feeds and two pool outlets, and total input out-degree at most two.
Positive lower flow bounds, including exact supply and demand contracts,
are allowed. Then the following boundary holds:

- If every output has total in-degree at most two, feasibility is
  decidable in polynomial rational bit time. Qualities and capacities
  may have arbitrary rational data subject to finite upper flow bounds.
- If output total in-degree at most three is permitted, feasibility is
  strongly NP-complete, even with one scalar quality, only upper output
  quality bounds, flow lower and upper data in `{0,1,2,3,4}`, and all
  quality values and bounds in
  `{0,1/66,1/33,1/22,1/11,1/2,1}`.

For the positive statement, the bypass graph is a subgraph of the full
input-output incidence graph, so it has maximum degree at most two.
The theorem above applies. In fact it also permits some attachment
nodes of total degree three, provided their bypass degree is at most two.

For hardness, use Sections 3–4 of the independently reviewed
[constant-data two-feed construction](pooling-constant-data-two-feed-np-completeness.md).
Retain every exact source-supply, collector-demand, and other designated
node contract. Omit its Section 5 contract-completion objective and all
other economics. Before that objective is introduced, the physical
network is already feasible exactly when the source positive-product
instance is a yes instance. In particular, the inequality
`sum_i b_i x_i>=K` remains encoded by physical averaging, addition and
comparison gadgets. It is not an external aggregate or an objective
threshold in the resulting feasibility problem.

The preserved positive lower bounds are exact node contracts with values
in `{1,2,3,4}`. All degree and constant-data restrictions stated above
are inherited unchanged. The reduction has polynomial size even under
unary numerical encoding because the large source coefficients occur
only through circuit topology. NP membership follows from the
[fixed-parameter linear-fiber theorem](fixed-parameter-linear-fibers-np-membership.md)
with one pool and one quality. Hence feasibility is strongly NP-complete.
The comparison concerns feasible flow with prescribed nonzero requirements:
if every flow lower bound is zero, ordinary feasibility is trivially
satisfied by zero flow.

This corollary gives a feasibility boundary, not a resolution of
unrestricted profit optimization on degree-two bypasses. Both statements
also hold when the positive branch is restricted to the hard branch's
fixed numerical alphabets. Their separate literature priority remains
provisional.

## 7. Scope, sources, and verification

The main theorem classifies feasibility; Section 5 also solves bounded-
support optimization. A general profit threshold introduces a dense
linear aggregate over eliminated arcs. Its value cannot be recovered
from the two-coordinate boundary feasibility relations. The reviewed
[fixed-alphabet exponential price-response example](../notes/degree-two-fixed-quality-alphabet-investigation.md)
remains compatible with this algorithm, and unrestricted dense bypass
profit remains open for the stated one-pool degree-two class.

Pairwise projections of two-variable-per-inequality systems are
established objects. Simon, King and Howe, *The Two Variable Per
Inequality Abstract Domain*,
[open manuscript](https://www.cs.kent.ac.uk/pubs/2010/3167/content.pdf),
Section 3, discusses closure by pairwise resultant elimination. Its
stated general normalized-closure size claim requires a separate
encoding/scope check. Hochbaum and Naor,
[*Simple and fast algorithms for linear and integer programs with two variables per inequality*](https://hochbaum.ieor.berkeley.edu/html/pub/HNaorSICOMP94.pdf),
Section 2, printed page 1181, cites a bound `m*n^(log n)` for Nelson's
general Fourier–Motzkin procedure. The bounded-path proof here stands
independently of either general closure-size assertion. No new general
2VPI elimination principle or established priority for the pooling
corollary is claimed.

The fixed-dimensional real-algebraic step uses established algorithms.
Basu's [author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf),
Theorem 2.18, gives the quantifier-elimination arithmetic and coefficient
bit bounds used here; see also the repository's
[fixed-core constructive theorem](fixed-core-block-polyhedral-optimization.md).
The polynomial exponent depends on the fixed core size and degree.
This is a bit-complexity result, not a practical runtime or strongly
polynomial guarantee.

The [first review](../notes/review-pooling-degree-two-boundary-projection.md) and
[second review](../notes/review-pooling-degree-two-boundary-projection-second.md)
both pass the endpoint lemma, thirteen-variable pooling mapping,
degenerate cases, exact algebraic recovery, and Section 5 optimization. The independent
[exact checker](../code/pooling_bypass_paths/check_boundary_projection_review.py)
passed 70 polygon compositions and 480 lower/upper section identities
using direct Fourier–Motzkin elimination, including vertical and
nonvertical segments and a point. These finite checks support the
analytic proof; they do not establish its asymptotic bound by themselves.

The degree boundary in Section 6 passed the
[first independent audit](../notes/review-pooling-feasibility-output-degree-boundary.md)
and the second reviewer's addendum to the
[constant-data audit](../notes/review-pooling-constant-data-two-feed-second.md).
The hardness part is an exact corollary of the already tested physical
constant-data construction; it introduces no new numerical gadget.
