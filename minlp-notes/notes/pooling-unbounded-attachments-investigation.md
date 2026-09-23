# Degree-two bypass paths with many pool attachments

Date: 2026-09-05. Status: investigation; no polynomial algorithm or hardness
classification is claimed for the unrestricted-attachment case.

The current target is standard pooling feasibility with a fixed number
of pools, fixed affine rank of the input-quality vectors, and a bypass
graph of maximum degree two. The number of pool-incident arcs may grow.
Positive lower flow requirements are allowed. Dense-profit optimization
is a separate question.

## 1. Routine bounded-attachment extension

The reviewed [endpoint algorithm](../results/pooling-degree-two-boundary-projection.md)
extends when the total number `a` of pool-incident arcs is fixed. This
statement allows multiple pools, but excludes pool-to-pool arcs. Finite
rational flow bounds and arbitrary many quality attributes remain allowed.

There are at most `a` distinct external attachment nodes. Retain the `a`
pool-incident flows and at most `2a` bypass arcs touching these nodes.
For each pool retain one fraction for each allowed input arc, with
nonnegative fractions summing to one. Their total count is at most `a`.
A pool with no incoming or outgoing arc must have zero throughput;
reject incompatible positive lower bounds on that pool throughput or its
incident arcs and remove it first. Retain adjacent external-node
supply/demand requirements, since bypasses or other pools may satisfy
them. If `a=0`, the entire network is an ordinary bounded rational LP.
The core therefore has at most `4a` variables. Pool qualities are affine
in their own input fractions, and fraction/intake consistency and receiving
output quality rows have degree at most two. At zero throughput any legal
fraction vector is harmless. No quality-rank restriction is needed.

After removing the attachment nodes, all remaining boundary components
are scalar paths with at most two retained endpoint arcs. The existing
polygon composition and common-field affine reconstruction apply without
change. Thus fixed-dimensional algebraic decision proves polynomial-bit
feasibility. Retaining a further fixed number of objective coordinates
also gives the same bounded-support optimization extension. This is a
routine extension. The [first independent audit](review-pooling-bounded-attachments.md) and
[second audit](review-pooling-bounded-attachments-second.md) both pass.
The corollary is promoted as Section 5.1 of the endpoint result.

## 2. Two separate obstacles when attachments are unbounded

Fix pool quality coordinates in a rational affine basis of rank `t`,
with the number of pools `p` and `t` fixed. At a fixed parameter value,
each external node has at most two bypass variables and at most `p`
incident pool-flow variables. Its local feasible set has fixed dimension,
so its projection onto the two bypass variables is a polygon. Its
coefficients, however, depend on the fixed but unknown pool parameters.
A fixed-dimension local elimination can use finitely many parameter cells;
this alone does not bound the complexity after a long path is composed.
The balanced constant-coefficient proof must not be applied symbolically
without a bound on the parameter cells and resulting algebraic degrees.

There is another obstruction even before such a bound is obtained.
The local projections forget the pool-flow contributions. Global pool
mass balance and attribute-mass balance couple these contributions across
all external nodes. They impose a fixed number, at most `p(1+t)`, of
dense aggregate equalities. Retaining their totals is analogous to
retaining a dense objective coordinate. Ordinary two-endpoint feasibility
projections contain insufficient information to check them. The fixed
core/block theorem handles independent blocks, while the bypass paths
couple these blocks along arbitrarily long chains.

Consequently a polynomial symbolic endpoint relation alone would not
complete the pooling algorithm: the shared pool aggregates also require
an exact treatment. Conversely, an exponential explicit message bound
would not itself establish NP-hardness or exclude a polynomial implicit
algorithm.

## 3. A failed direct helper-pool substitution

One tempting reduction starts with the reviewed degree-three copy
network and replaces every private midpoint input by a fixed-quality
helper pool. Each copy output would then have only two bypass inlets,
with its third inlet supplied by that pool. This substitution does not
preserve the copy gadget.

The original pair of copy outputs has its own fixed total midpoint
supply. Combining this private equation with the two output balances
forces the complementary relation between the pair's two signal values.
A common helper pool only fixes the sum across all such pairs; it loses
each pair's separate equation. Equal helper quality preserves the local
endpoint-quality ratio but does not restore the missing complement
relation. The old arbitrary-circuit proof therefore cannot be reused by
this substitution without an additional, independently justified device.

For an explicit local failure of the helper-pool substitution, take two
full gadgets with endpoint qualities zero and two and midpoint quality
one. Give both endpoint pairs in the first gadget value zero and both
pairs in the second value two. Their four midpoint flows are then
`4,4,0,0`, totaling eight, which a shared midpoint pool of throughput
eight can supply. Each output still has demand four and exact quality
one. The original private midpoint supplies would require four in each
gadget, so this assignment is excluded there. Additional original chain
constraints may exclude this particular assignment; the example already
shows that the local replacement is not an equivalent gadget.

## 4. A qualified one-parameter upper bound

The complementary [parametric path investigation](one-parameter-path-projection-investigation.md)
obtained a quasipolynomial upper bound rather than the sought exponential
cell obstruction. For one scalar parameter and explicitly encoded
fixed-degree polynomial local coefficients, uniformly bounded scalar
paths admit an endpoint description with `N^(O(log(h+1)))` parameter
cells, polynomially many rows per cell, and polynomial degrees and
coefficient heights. Balanced composition and one-dimensional unions
of breakpoints control the cell recurrence. My
[complete independent audit](review-one-parameter-path-projection.md)
passes this proof; a second audit and priority search are separate.

The shared pool aggregates in Section 2 remain absent from that theorem.
Thus it neither settles the present pooling class nor establishes an
exponential obstruction to every algorithm for it.

## 5. Fixed aggregate count alone is insufficient in an abstract model

The already reviewed
[Klee–Minty slab reduction](klee-minty-rank-one-slab-hardness.md)
provides a precise warning about the second obstacle. Let `P_epsilon`
be its bounded scalar 2VPI path, let `L(x)` be its telescoping linear
form, and let `w*x` be its subset-sum aggregate. Introduce one scalar
core coordinate `lambda` and retain only the endpoint equality
`lambda=x_n`. The additional constraints are

```
L(x) <= lambda^2,
B-1/4 <= w*x <= B+1/4.
```

Feasibility is NP-complete by that result: `L(x)-x_n^2>=0` everywhere
on the path, so the first row forces an endpoint vertex, and the slab
selects a subset-sum yes assignment. Thus a single nonlinear core
parameter plus a parameter-independent scalar path and only two dense
aggregate coordinates is already enough for ordinary NP-completeness
in this abstract class. The local coefficient alphabet can be fixed by
the reviewed padding construction, while the dense row weights remain
binary data; no strong-hardness claim follows.

This does not prove hardness for pooling with unbounded attachments.
Actual pool balances have constrained coefficients and common mixing
semantics. No physical realization of these two arbitrary aggregates
using the requested fixed pools, quality rank, and degree-two bypasses
has been established here. It does rule out a proof based only on the
number of aggregate coordinates and the scalar path structure.

## 6. Additional source context

A newly located primary manuscript by Boveroux, Carvalho, Lodi and
Louveaux,
[*On the Complexity of Linear Programs with Parametric Constraint Matrices*](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf),
Sections 3.1–3.3, proves general scalar matrix-parameter min-min and
max-min hardness using Matsui's construction. Its sufficient conditions
concern a uniform sign pattern, one nonzero perturbation row, or one
nonzero perturbation column. The reduction retains dense base-polytope
constraints. It does not establish a degree-two path or pooling
classification. The source is relevant context for the general
parametric-LP step, not a proof of either side of the present open case.

## 7. Exact contracts remove the aggregate obstruction in useful cases

The subsequent work found constructive classes where conservation
eliminates the dense pool aggregates exactly, rather than approximating
their endpoint messages.

The reviewed
[fixed receiving-product theorem](../results/pooling-fixed-product-contracts-algorithm.md)
allows unbounded pool feeds, arbitrary quality count and affine rank,
and a nonredundant common pool capacity. It requires a fixed number of
receiving outputs, exact input supplies, and exact demands and quality
vectors at all nonreceiving outputs. Total pool mass and attribute mass
then become affine functions of the fixed receiving boundary. Standard
economic optimization is polynomial. Both full audits passed.

With unbounded feeds and outlets, the
[quality-scaled contracted flow theorem](pooling-quality-scaled-path-flow.md)
uses exact source supplies and exact product demand/quality contracts.
Scaling by source quality minus pool quality gives a signed incidence
system on paths and cycles. Connected cuts have at most two edges,
so polynomially many quadratic conditions suffice. Feasibility is
polynomial, and a quadratic-field witness suffices in the scalar case.
Two full audits passed. The common pool-capacity bounds must now be
redundant: a separate counterexample demonstrates the missing aggregate
when that assumption is dropped.

The [bounded-exception optimization theorem](../results/pooling-contract-exceptions-algorithm.md)
keeps a fixed number of input and output nodes with interval contracts.
It permits arbitrary quality count and input-quality affine rank, as
well as unbounded feeds and outlets. An active ordinary product confines
the pool quality to an affine space of dimension at most two; if every
ordinary pool outlet is zero, only the fixed exceptional receivers
remain. The two branches use incidence cuts or fixed-boundary projection,
respectively. Global mass and quality identities keep every recovered
local lift physically consistent. Standard economic optimization is
polynomial. Two fresh full audits passed, and the earlier scalar and
fixed-rank proofs remain reviewed supporting milestones.

These results do not settle unrestricted degree-two bypass pooling.
Arbitrary contract intervals, a restrictive shared pool capacity with
unbounded attachments, and unrestricted dense individual arc costs
remain separate issues. The failed helper-pool substitution and abstract
aggregate warning above remain useful for those unresolved cases.


## Closure: a second tractable restriction

The [two-source-vector theorem](../results/pooling-two-source-qualities-convex-feasibility.md)
now removes all bypass degree restrictions when the complete input
quality vectors take at most two distinct values. It allows arbitrary
source supply intervals and restrictive common pool upper capacity,
while preserving exact product demand/quality contracts and zero
pool-outlet/common pool lower bounds. Its exact convex-QP reduction
constructs rational physical witnesses and passed two independent
final-scope audits. This resolves that specific feasibility class; it
does not optimize variable procurement or individual arc costs.

The broader unresolved cases above are retained as boundaries of these
results, not pending claims. The failed helper-pool and dense-aggregate
routes do not prove hardness or tractability for unrestricted interval
contracts or dense-profit degree-two pooling.


The [common-capacity theorem](../results/pooling-contracted-common-capacity-algorithm.md)
also resolves the earlier shared-capacity obstacle for the scalar
exact-contract degree-two subclass, including positive common lower
bounds and affine-rank-one quality compression. Its extra support tests
are essential: the earlier counterexample correctly rejected any claim
that local path feasibility alone handled the aggregate. The extension
uses polynomial-degree algebraic witnesses. The generic interval-contract
and dense-profit boundaries remain unresolved and are not claimed here.
