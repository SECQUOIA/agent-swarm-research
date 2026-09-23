# Independent audit: cactus flow regions, scenario search, and exact arithmetic

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS after the membership scope clarification.** I
independently reviewed
[the cactus flow-region candidate](potential-flow-cactus-flow-region-and-optimization.md).
Its interval-region geometry, finite-set convex hull, exact optimizing
scenario algorithm, additive value computation, and square-root-sum
reduction are correct. Rational-point membership via the displayed box
representation applies to the interval region or finite-set convex hull;
it must not be stated for the actual finite-set attainable region.
I requested that clarification and record a simple hardness boundary
below. Literature priority remains a separate audit.

## Exact scalar cycle ranges

For fixed nominations, all bridge flows and all effective cycle
nominations are fixed independently of resistance choices. On a
consistently oriented cycle the flow is `q+d_e` and its cycle equation
is the stated strictly increasing `H_beta(q)`.

Each summand in `H_min` is a positive endpoint multiple of
`(q+d_e)|q+d_e|`, selecting the upper endpoint on its negative half and
the lower endpoint on its positive half. It is continuous and strictly
increasing. The analogous statement holds for `H_max` with reversed
endpoint choices. Both functions therefore have unique zeros. Since
`H_min<=H_beta<=H_max`, their root ordering is exactly
`q_min<=q(beta)<=q_max`, with `q_max` the zero of `H_min`.

At either extreme zero, choose each edge endpoint attaining its defining
summand. These choices satisfy that physical cycle equation exactly,
so both extremes are realized by rational endpoint resistance vectors.
When the flow on an edge is zero, either endpoint is valid. Finite
resistance sets contain their minimum and maximum, which is all this
construction needs.

At rational breakpoints `-d_e`, every summand is rational. Sorting those
breakpoints and testing signs locates the relevant quadratic piece or
identifies a breakpoint root directly. Duplicate breakpoints and constant
cycle offsets cause no problem. The outermost breakpoints bracket the
root, unless they coincide and are themselves the root. Within a piece,
all coefficients are rational with polynomial encoding length. A vanishing
quadratic coefficient gives a linear equation; an identically zero
open piece is excluded by strict monotonicity. Thus the exact endpoint
has degree at most two and can be computed and compared to the rational
breakpoints in polynomial bit time.

## Product geometry

On interval resistance boxes, a cycle's scalar physical response is
continuous. The parameter box is compact and connected, so its image
is the full closed interval between its two extremes. Different cycle
blocks have disjoint edges and fixed effective nominations. Their choices
are independent, including when they share an articulation vertex.

A rational particular flow plus independent signed cycle vectors
represents every conserved flow. On a cactus these vectors have disjoint
edge supports. Consequently the interval-attainable set is exactly the
stated affine image of a box, possibly with some zero-length coordinate
intervals. There are no additional cross-cycle potential restrictions:
the cycle equations already characterize membership of the edge-drop
vector in the image of the transposed incidence matrix.

For finite resistance sets, the actual circulation set is a Cartesian
product of finite scalar sets. The convex hull of such a product is the
product of its scalar convex hulls. Each scalar hull is the already
computed interval, and affine maps commute with taking convex hulls.
This proves the finite-set convex-hull statement. It does not imply
that the actual finite circulation sets contain their interval interiors.

Every vertex of the box image is realized by independently combining
the endpoint scenarios. Convexity bounds a function's value at any convex
combination by the corresponding weighted vertex values. Thus a continuous
convex flow objective has a worst case at such an endpoint scenario.
The conclusion concerns existence; it does not give a polynomial algorithm
for arbitrary convex maximization in unbounded cycle dimension.

## Exact scenario optimization and additive values

A rational linear flow objective has the decomposition
`C+sum_C A_C q_C`. Its exact optimizing scenario is obtained independently
on each cycle according to the rational sign of `A_C`. No comparison
between the resulting cycle roots is needed to choose these scenarios.
Zero objective coefficients permit any allowed cycle scenario, and
bridge resistances may be selected arbitrarily from their allowed sets.
The output resistances are rational input endpoints and have polynomial
total encoding length.

Approximating each selected circulation to absolute error at most
`epsilon/[2(1+sum_C |A_C|)]` makes the total weighted error less than
`epsilon/2`. Rational root isolation for degree-two polynomials gives
this precision in polynomial time in the input and accuracy bits.
Large coefficient magnitudes enter only through their logarithmic
encoding and the requested root precision. The remaining constant and
sum can be evaluated rationally with polynomial bit length.

Physical flow coordinates may be returned through separate quadratic
encodings for each cycle and rational affine offsets. The candidate
correctly does not promise one polynomial-degree common field for all
cycles. Selecting an exactly optimal rational resistance scenario is
therefore compatible with an exact-scalar-comparison obstruction.

## Rational membership: the required distinction

For the interval-attainable region, a rational candidate flow can be
tested by conservation and interval membership of its rational cycle
coordinates, using separate degree-two comparisons. The same test checks
membership in the finite-set convex hull. In fact, for a prescribed
rational flow on any graph, interval-resistance attainability is already
a rational LP: the edge-law basis values are known rationals, and cycle
consistency is linear in the resistance variables. This corroborates the
scope of the positive membership statement.

Actual attainability under finite resistance sets is different and is
already NP-complete on a single simple cycle. Here is a direct boundary
example, retained because it prevents an incorrect extension of the
geometry claim. Take a positive-integer Subset-Sum instance with `n>=2`
items and positive target `K`. Use a consistently oriented cycle with
`n` uncertain edges and one fixed edge. Prescribe the rational target
flow `+1` on each uncertain edge and `-1` on the fixed edge. Its induced
nomination vector has only two nonzero entries, `+2` and `-2`.
Give uncertain edge `i` the resistance choices `{1,1+a_i}` and the
fixed edge resistance `n+K`.

The target cycle pressure sum is

```
sum_i (1+a_i sigma_i)-(n+K)=sum_i a_i sigma_i-K.
```

It vanishes exactly for a target subset. Conservation is already built
into the prescribed nomination, and cycle consistency is necessary and
sufficient for the target to be the physical flow. All data are integers.
The small cases `n<2` can be handled directly or padded, so the simple
cycle restriction causes no reduction problem. NP membership follows
by guessing the resistance choices and checking the rational cycle
equations. This elementary boundary is not assigned a novelty claim.

The candidate's membership paragraph must explicitly say interval-region
membership or finite-set convex-hull membership. Its other positive
claims do not require finite-set point membership and remain valid.

## Square-root-sum scalar-comparison reduction

After removing unit radicands and adjusting the threshold, every retained
radicand exceeds one. If none remain, decide `0<=K`; if some remain
but the adjusted `K` is nonpositive, return a fixed no instance. The
revised preprocessing text now handles these cases explicitly.

Each triangle receives unit through-flow. Its direct resistance `a_i`
and alternate total resistance one give the unique direct flow
`x_i=1/(1+sqrt(a_i))`. Both route flows are positive. The positive
integer objective coefficient `a_i-1` satisfies the exact identity

```
(a_i-1)x_i=sqrt(a_i)-1.
```

Thus the full objective is `sum_i sqrt(a_i)-m`, with the weak threshold
`K-m`. This preserves equality and has the same yes/no direction as the
standard sum-of-square-roots comparison. No approximation-gap claim is
inferred from this identity.

Join disjoint triangles by resistance-one bridges at distinct entrance
and exit vertices, as the revised text specifies. Every bridge carries
unit flow. The graph has `3m` vertices and `4m-1` edges and is a simple
cactus of maximum degree three. Only its first and last terminal have
nonzero nomination. Common resistance scaling by two makes every
resistance a positive integer and preserves all flows and the objective.
The objective coefficients and rational threshold have polynomial binary
encoding length.

The fixed-output triangle also checks exactly: direct resistance eight
and alternate total resistance two give direct flow `1/3`. Its coefficient
three gives objective one, so thresholds one and zero are valid fixed
yes/no outputs inside the same integer-data family. I independently
checked this state and the radical identity symbolically.

This is an SRS-hard exact comparison problem, not an NP-hardness claim.
With fixed resistances its optimizing scenario is trivial, which explains
why it does not contradict the exact scenario-search algorithm. Separate
quadratic output encodings likewise do not provide a polynomial exact
comparison algorithm for their unbounded weighted sum.

I reread the corrected membership paragraph. It explicitly restricts the
polynomial test to the interval-attainable region or finite-set convex
hull, and distinguishes actual finite-set realization. The preprocessing
and bridge-resistance details are also explicit in the current draft.
No substantive defect remains.
