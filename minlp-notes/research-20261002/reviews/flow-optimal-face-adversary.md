# Independent review of the optimal-flow boundary-face certificate

Date: 2026-10-02. Result: passed the completed
[deterministic certificate](../new-direction/flow-optimal-face-certificate.md),
including the final degree and original-arc clarifications. This review
does not itself establish a probabilistic stopping theorem.

An exact conditional optimum and nonnegative residual reduced costs make
each adjusted scalar cost minimal at the returned arc label. Convexity of
its first differences identifies its entire integer minimizing interval.
Potential terms sum to a constant over feasible flows. Therefore the
intersection of these intervals with the flow equations is exactly the
whole optimal integer-flow set at the query point, including all ties.

The derivative-flow argument handles an important distinction correctly.
Three ordered integer minimizing points of a convex adjusted cost force
affinity between the extreme points. Its scalar second derivative is zero
there. Nonnegativity of that derivative after a feasible inward core
displacement implies convexity of the inward derivative cost on the tied
interval. Two consecutive tied labels do not imply affinity; their two
derivative values must instead be represented by a linear interpolant.
Singleton intervals are substituted. These costs, with tangent extensions
if required, satisfy the existing convex-flow oracle's input contract.
Minimizing over all tied flows is necessary; one returned flow can give
the wrong normal-gradient sign.

The proximity proof also passes. For a closest feasible interval flow,
decompose the difference circulation conformally into integer-multiplicity
simple cycles. Every cycle has an arc whose unit move immediately leaves
its tightened interval; otherwise that cycle improves the chosen distance.
On such a blocking arc the entire difference equals its interval violation.
Charging each cycle's multiplicity to one blocker cannot exceed that
violation, because the decomposition is conformal. Each cycle has at most
`r` arcs. This proves `distance_1<=r*total_violation`, including parallel
arcs and self-loops. The factor can be attained by a simple directed cycle.

Uniform within-interval ties and nonnegative first outside marginals make
every interval flow optimal throughout the projected face box. Convexity
then gives the cost lower bound `mu*total_violation` for every other flow.
The polynomial identity check needs at most `d+1` integer labels per arc.
The final note explicitly assumes `d>=1` and gives potentials of core
degree at most `d-1`, so the adjusted polynomial has total degree at most
`d`. These clarifications preserve both identity interpolation and the
constant-base fixed-degree sign-test cost.

The Taylor constants are sound. At a face point `w`, compare a flow `z`
with its nearby interval flow and then move that interval flow's gradient
from the center to `w`. This loses at most
`K*r*total_violation + H*R` per inward derivative. After multiplying by
the nonnegative normal displacement and using the cost bound, the unwanted
flow term has coefficient `mu-r*K*norm_1(d)`. The first test makes that
coefficient nonnegative. The Hessian remainder satisfies
`norm_2(d)^2<=T_infty*norm_1(d)`, giving exactly the second strict test.
Every off-face point in the retained box is then worse than a feasible
face point. A hull containing all original optimizer cores permits the
global fixing conclusion and a final solve of the selected flow's entire
original core box.

The final no-normal case uses the same original-arc interval and outside
tests with threshold zero. Artificial source arcs help construct potentials
but do not need sign tests for flow optimality. This distinction is needed
for the later chart universe and is now explicit.

## Independent exact diagnostic

I wrote and ran

```sh
python3 -B research-20261002/reviews/check_flow_face_review.py
```

It passed 703 feasible tightened interval boxes, 3,942 exact proximity
checks, and 54 derivative/Taylor checks. Networks include directed cycles,
parallel arcs and self-loops. The diagnostic includes the sharp cycle
factor, concave inward derivative costs on a two-label interval, an
incorrect sign from selecting only one tied flow, outside-flow takeover
when the marginal guard is omitted, and different tied winners in different
inward directions. All calculations use integers and rational numbers.

These are independent finite checks of the new mechanisms. They do not
implement a general convex-flow oracle or prove the theorem by testing.
The author's separate checker was not rerun. No external search,
project-wide verification or CI inspection was performed.
