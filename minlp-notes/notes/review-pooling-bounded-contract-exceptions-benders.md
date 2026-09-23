# Independent second audit: bounded contract exceptions

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS.** I checked the complete scalar proof in
[the candidate](pooling-bounded-contract-exceptions-algorithm.md), including
the physical reconstruction and exact optimization over open quality
cells. The previously reviewed signed-flow transformation and cut lemma
are used within their valid scope. The conclusion requires a fixed
number of exceptional external nodes and redundant common pool bounds.

## Physical mapping and fixed dimension

Each exceptional node is incident to at most one pool arc and two bypass
arcs. Retaining all these arcs gives at most `s` pool coordinates and
`2s` original bypass coordinates, counting shared exceptional-to-
exceptional bypasses only once. Their transformed counterparts and the
scalar quality give at most `1+5s` core coordinates. Every exceptional
throughput and quality-mass expression consequently uses only the core.
Supply, demand, quality, and individual arc bounds remain valid
polynomial constraints of degree at most two. A missing pool arc means
zero flow, not an omitted node requirement.

At an ordinary input, subtracting its bypass flows from its exact supply
recovers its intake. At an ordinary output, the analogous subtraction
recovers its outlet. Retaining the individual bounds on these expressions
ensures their nonnegativity as well as every original lower bound.

The global mass equation is exactly the difference between total
intakes and total outlets after canceling total bypass flow. The global
quality equation is also exact: the ordinary output equations express
each exact delivered quality mass as bypass mass plus `q` times its
outlet; exceptional output masses already have that expression by
definition. Canceling total bypass quality mass gives

```
sum_i C_i*y_i = q*sum_j v_j.
```

Thus every feasible local lift satisfies the actual pool balances.
Conversely every original flow satisfies the retained global equations.
At zero throughput all pool arcs vanish by nonnegativity, so no division
or additional active-pool assumption is needed. At positive throughput,
the quality is the true intake-weighted average. Searching the closed
allowed-feed quality interval is therefore sufficient.

An unusable pool can be removed only after forcing its incident arcs
to zero and checking their lower bounds, while preserving all external
requirements. The candidate implements this preprocessing correctly.

## Residual paths and exact cuts

I checked that the scalar transformation applies to ordinary nodes even
when one or both of their original bypass arcs meet exceptional nodes.
An ordinary output's two-inlet calculation must use both of its original
inlets before boundary removal, as the draft does. Every extra interval
placed on a retained boundary arc remains a core constraint.

Removing exceptional nodes and prescribed boundary arcs leaves paths,
cycles, or isolated nodes. Moving a boundary flow's signed contribution
from both node-divergence bounds is exact. This covers two boundary arcs
at one isolated ordinary node, two endpoints attached to the same
exceptional node, and components with no boundary. Arcs between two
exceptional nodes need no residual projection.

Connected induced subsets suffice by additive decomposition of the
signed Hoffman inequalities. Each path or cycle cut crosses at most
two internal edges. The upper cut capacity is the minimum over its
upper-outgoing/lower-incoming candidate combinations; the lower cut
capacity is the corresponding maximum. Imposing all combinations is
therefore equivalent to the effective capacities. With constant-size
candidate lists this creates only a constant factor more rows. All
lower-candidate versus upper-candidate consistency rows and all
whole-component cuts are retained. Isolated-node cuts correctly enforce
that zero internal divergence belongs to the shifted node interval.

The resulting rows are quadratic in the full fixed-dimensional core.
Their coefficients have polynomial rational bit length: the only
divisors introduced by the local scalar formula are fixed nonzero
quality differences, and cut expressions contain polynomially many
node terms but at most two capacity terms. This is a valid polynomial
projection, not an assumption that a fixed number of arbitrary dense
aggregate constraints would be harmless.

## Exact optimization and algebraic recovery

Every distinct source quality in the search interval is handled by an
original fixed-quality LP. Those LPs retain pool balances, exceptional
requirements, and the objective. All are linear at fixed quality. The
remaining open intervals have invertible scaling factors of fixed sign.

Fixed-dimensional elimination applies to the quadratic core formula
on each open interval. Adding one objective-value variable keeps the
dimension fixed. The union of their attained-value sets with the
fixed-quality LP value sets is exactly the original attained-value set.
At a fixed-quality LP the value set, when nonempty, is a closed interval
obtainable from its minimum and maximum. All descriptions have polynomial
encoding and degree. Their number is polynomial.

The original model, including its selected closed quality interval,
has a closed bounded feasible set. Its standard economic objective is
continuous, so the union has an attained largest value. Selecting that
value and sampling a point of an actual attaining cell is valid even
if another cell has an unattained supremum. Closing transformed open
cells instead would not be justified at vanishing scaling factors;
the candidate explicitly avoids that operation.

All nonexceptional throughput costs and revenues are constants. The
remaining standard profit is affine in retained original flow
coordinates. There is consequently no omitted dense cost term in the
residual incidence systems.

Fixed-dimensional algebraic sampling represents the optimal value and
core coordinates together in one polynomial-degree real algebraic
field, with polynomial encoding length. At that core point, lower-bound
shifting and exact circulation recovery use that same ordered field.
An incidence-system vertex has coordinates that are rational linear
combinations of its bounds. Division by the nonzero scaling factors
and the local intake/outlet reconstruction stay in the same field and
retain polynomial encoding length. The already checked global identities
make every such reconstruction a physical optimum.

## Scope

The proof does not enforce a restrictive common pool-throughput bound;
its redundancy assumption is essential. Arbitrary separate arc or pool-
throughput costs are not covered by the objective reduction. A fixed
number of cost-bearing arcs can be retained by marking their external
endpoints exceptional while preserving any exact contracts there.
There is no quadratic-field witness claim for this extension: the
fixed-dimensional core can have a larger polynomial algebraic degree.

This is a separate proof audit. I did not repeat the earlier scalar
mapping tests; the new obligations here are the global identities,
boundary accounting, and attained-value optimization argument. Source
priority for the physical classification remains provisional.

### Redundancy certificate addendum

The common upper bound may also be certified redundant by the sum of
pool-feed arc upper capacities or the sum of pool-outlet arc upper
capacities. Taking the minimum of these two bounds and the total source
upper throughput is valid because pool conservation equates total feed
and outlet flow. This is a preprocessing certificate, not an additional
aggregate constraint. In particular, two unit-capacity outlets certify
a pool upper bound of two even if total external input throughput is
large. This refinement passes and leaves the proof unchanged.

The author's sufficient redundancy certificate can safely be sharpened:
it is enough that the common upper bound is at least the minimum of
the sum of valid input-throughput upper bounds, the sum of allowed
pool-feed capacities, and the sum of allowed pool-outlet capacities.
Actual nonnegative pool throughput satisfies each of these three
bounds separately. The lower bound remains zero. This refinement
adds no projected aggregate row and changes none of the algorithm.
