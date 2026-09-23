# Independent audit: scalar pooling with bounded contract exceptions

Date: 2026-09-05. Reviewer: `pooling_all_two_review`.
Verdict: PASS for the stated model and exact optimization conclusion.
This restores my separate audit after an accidental filename collision;
the other independent audit is retained in
[benders' review](review-pooling-bounded-contract-exceptions-benders.md).

Candidate: [bounded contract exceptions](pooling-bounded-contract-exceptions-algorithm.md).

## Core and physical equivalence

With `s` exceptional external nodes, their pool arcs number at most `s`,
and their incident bypass arcs number at most `2s`. Retaining those
physical flows, their scaled bypass coordinates, and scalar pool quality
uses at most `1+5s` coordinates. An arc with two exceptional endpoints
is counted only once. Exceptional input throughput, product throughput,
and product quality mass are functions of this core.

At every ordinary input, exact supply eliminates its pool intake as
the supply minus its bypass sum. At every ordinary output, exact demand
eliminates its pool outlet similarly. Missing pool arcs mean an exact
zero residual; they cannot simply be dropped. The remaining ordinary
quality row is `sum_i (C_i-q) z_ij=b_j(B_j-q)`.

The two proposed global equations equate total input and output mass
and total quality mass, using fixed ordinary contracts and core-dependent
exceptional totals. Subtracting all bypass terms proves actual pool
mass conservation and `sum_i C_i y_i=q sum_j v_j`. This holds for every
lift satisfying the local rows. At zero throughput all nonnegative pool
arcs vanish, so the quality identity remains valid. At positive throughput
the quality is the actual weighted average of allowed feeds. The compact
feed-quality interval therefore loses no feasible physical flow.

## Boundary projection

Away from every input quality, the reviewed substitution
`w_ij=(C_i-q)z_ij` is invertible. Remove exceptional nodes and the core
arcs from the residual graph. Each fixed boundary flow shifts the
ordinary endpoint's divergence interval with its correct incidence sign.
All its capacity and local equality conditions remain in the core.
This preserves the exact projection, including isolated residual nodes.

The residual graph consists of paths and cycles. The signed Hoffman
conditions need only connected induced subsets: conditions for arbitrary
subsets add over their connected components. There are quadratically
many such subsets, each crossing at most two internal arcs. Expanding
each cut over all constant-size bound-candidate combinations eliminates
the min/max capacities without introducing new variables or parameter
partitions. Arc consistency uses all lower-versus-upper pairs. The
resulting rows are quadratic in quality and linear in boundary flows.
The retained links and global equations also have bounded degree.

## Economics, attainment, and recovery

Standard input costs and output revenues at ordinary nodes contribute
constants because their total throughputs are fixed. The remaining
profit is affine in the core physical flows. General dense arc costs
do not have this property and are outside the theorem.

For each open quality interval, fixed-dimensional real algebraic
elimination describes the attainable objective values using the strict
interval conditions. At each singular quality equal to an input quality,
the original fixed-quality model is a rational LP. Their union is exactly
the original attainable-value set. The original bounded physical model
is closed after choosing the compact quality interval, so a nonempty
instance attains its optimum. Selecting that value from the union avoids
the invalid operation of closing a nonsingular transformed cell at a
singular quality.

Algebraic sampling gives the optimum and core coordinates in one real
algebraic field of polynomial degree and encoding length. At a sampled
core, incidence-flow recovery stays in that field. An incidence-system
vertex is a rational linear combination of its bounds; division by each
nonzero scaling factor then recovers original bypass flow. The local
contracts recover the other pool arcs. Field degree and coefficient
length remain polynomial. No quadratic-field claim is made for this
extension.

## Scope and redundancy certificate

The proof requires fixed exception count and redundant common pool
capacity. It does not enforce a new dense common-throughput aggregate.
A pool upper bound is redundant if it is at least the minimum of total
source upper throughput, the sum of feed-arc upper capacities, and the
sum of outlet-arc upper capacities. Nonnegative flows and pool conservation
prove each bound. In particular, two unit-capacity outlets certify a
pool upper bound of two even with many external source contracts.

This is a proof audit of the new global identities, boundary accounting,
and attained-value argument. I did not repeat the reviewed scalar mapping
experiments. Source priority for the physical class remains provisional.
