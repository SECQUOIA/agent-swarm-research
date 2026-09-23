# Independent review: fixed total pool-incident arcs

Date: 2026-09-05. Verdict: **PASS** for Section 1 of
[the attachment investigation](pooling-unbounded-attachments-investigation.md),
with the preprocessing interpretation stated below. This is a routine
extension of the reviewed endpoint-projection theorem; separate novelty
is not asserted.

Fix the total number `a` of pool-incident arcs. The model has ordinary
input-pool-output layers, with no pool-to-pool arcs, finite rational
flow bounds, and a bypass graph of maximum degree two. There are at
most `a` external nodes adjacent to pools. Thus at most `2a` distinct
bypass arcs touch those nodes. Retaining those flows, the `a` pool
flows, and one input fraction for each input-pool arc uses at most
`4a` scalar variables. Multiple pools or a source/output incident to
several pools do not change the count.

For each pool with an incoming arc, impose a nonnegative fraction
simplex and `y_il=theta_il*T_l` for each inlet, together with mass
conservation. Each pool quality is the affine combination of fixed
input qualities with these fractions. Consequently all fraction
consistency and receiving-output quality rows have degree at most two
in the fixed core. Arbitrarily many attributes add rows rather than
dimensions. All capacity rows at removed attachment nodes use only
retained arc coordinates. At zero throughput an arbitrary legal
fraction vector gives a valid quality value and creates no spurious
positive flow.

A pool with no incoming or no outgoing arc forces its throughput and
all incident flows to zero. Reject positive lower bounds on those
forced-zero quantities, then delete the pool and its incident arcs.
Do **not** reject a positive supply/demand requirement at an adjacent
external node merely because that pool is inactive: bypass arcs or
other pools may satisfy that node's remaining contract. Retain its
capacity rows on the remaining arcs. If every pool disappears, the
remaining instance is an ordinary rational LP. The same reasoning
covers the case `a=0`.

After deleting the attachment nodes for the decomposition, every
remaining component is a scalar path, an isolated node, or a detached
cycle. At most two retained boundary arcs meet any such path. Local
relations involve at most two scalar bypass variables, so the already
reviewed exact polygon composition applies unchanged. Detached
components are treated by LP, and empty or degenerate relations by
the established preprocessing. The final fixed-dimensional rational
polynomial system decides feasibility in polynomial bit time.

Its exact algebraic sample lifts by the same affine slice operations
in a common algebraic field. Retaining a fixed additional number `s`
of actual arc coordinates increases the core bound to `4a+s` and
gives the prior fixed-degree polynomial optimization corollary with
closed polynomial side constraints and compact attainment. The
requirements for dense-cost reduction by exact model equalities
remain unchanged.

The unbounded-attachment discussion in Section 2 is correctly marked
unresolved. Projecting a local node onto its bypass coordinates loses
its contributions to global pool mass and quality balances. A fixed
number of such dense aggregate equalities does not follow from an
ordinary two-endpoint feasibility relation. Nor does the present
constant-coefficient composition proof establish a polynomial symbolic
parameter-cell bound. This review endorses no algorithm for that
broader case.
