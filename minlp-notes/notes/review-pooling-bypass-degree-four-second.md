# Second independent review: degree-four bypass refinement

Date: 2026-09-05. Verdict: **PASS**. No mathematical defect was found.
This review verifies the restriction refinement, not its literature novelty.

Reviewed: [degree-four candidate](pooling-bypass-degree-four-hardness.md).
The underlying one-pool copy reduction and fixed-parameter LP NP-membership
lemma were independently reviewed earlier by this reviewer.

## Averaging equation and distinct ports

The exact supply equation on the four specified outgoing arcs is
`v+v+(2-u)+(2-w)=4`, which is exactly `2v=u+w`.
Every arc has quality two, and the source has no other outlet. Conversely,
an average of two values in `[0,2]` remains in `[0,2]`, and all four
flows lie within their capacity two. Exact supply, rather than an upper
bound alone, is essential: weakening it changes the equality to
`2v<=u+w`.

Each requested occurrence receives its own chain gadget. Thus the two
positive `v` ports have distinct output endpoints, even if some child
signals coincide. Complemented children are handled correctly: the needed
complement of `2-x_i` is the ordinary positive `x_i` port. All these
equation ports share quality two independently of the quality assigned
to the final physical mixing-pool input.

Distinct sources with equal quality labels remain distinct unless an
explicit supply relation joins ports. The port convention therefore
prevents accidental parallel arcs or unintended resource sharing.

## Padded trees and zero signal

For a row containing `m` coefficient occurrences, padding to a complete
binary tree of size `N=2^ceil(log2 m)` gives equal averaging depth to
every original leaf. Induction gives exactly `root=sum(f_j)/N`, not a
depth-dependent weighted sum. Padding with the shared zero signal does
not change the numerator.

The zero signal is enforced through one positive port attached to a
zero-capacity source. Copy relations propagate zero along its whole
chain; its complement ports carry two. The shared zero signal may have
many occurrences, but each occurrence gets its own ordinary chain port.
It does not create a high-degree source.

Since `B=2*sum negative multiplicities`, one has `0<=B<=2m<=2N`.
The root capacity `B/N` is therefore at most two and imposes the original
row exactly. A zero row needs no circuit. For `m=1`, the leaf itself is
the root; using its positive or complementary full port as appropriate
gives the correct capacity, with no averaging node.

At original pool-intake vector zero, auxiliary averages need not be zero:
negative row occurrences are complementary leaves of value two. The
construction remains feasible because each internal signal is assigned
its actual average, and the root equals `B/N`. The draft's projection
argument correctly handles this and does not incorrectly force all
auxiliary signals to vanish.

## Projection and size

Given a feasible original signal vector, compute each internal average,
fill its copy chain, and fill the corresponding exact-supply source.
The root capacity holds precisely because the original row holds.
Conversely, every feasible modified network determines its chain signals;
its exact-supply equations determine the internal averages, so each root
capacity implies the original row. The original row source is removed
completely, with no residual capacity equation attached to the replacement
leaf occurrences. The projection onto original signals and actual pool
intakes is unchanged.

For `m>=1`, `m<=N<2m`; there are `N-1` internal signals and averaging
equations. Each equation uses four requested ports and the root uses one.
Original and auxiliary copy chains, their links, and private unused ports
therefore have total size `O(m)` per row, plus the original variable
conversion chains. The global zero chain has linear size in the total
number of padding occurrences. The underlying Matsui family has polynomial
total coefficient magnitude after homogenization, so this is a polynomial
reduction. It does not claim polynomial unary port replication for arbitrary
binary-sized row coefficients.

The only new nonintegral bounds are dyadic root capacities with denominator
`N`, whose encoding length is logarithmic in `m`. Every source, pool,
output, and arc flow upper bound is at most four.

## Degrees, objective, and model scope

Averaging inputs have four outgoing arcs; midpoint and link inputs have
two; original conversion inputs have one bypass and one pool arc; all
remaining inputs have at most one. Every gadget output has its two
endpoint arcs and one midpoint arc, hence in-degree three. The two primary
outputs have in-degrees two and one. The unique pool retains two outgoing
arcs and an unrestricted number of incoming arcs. Thus the claimed
input/output and bypass-graph degree bounds hold; the full network does
not have bounded degree at the pool.

New auxiliary sources and arcs have zero cost in the original reward
formulation. They cannot contribute extra profit. The production-cost
variant still rewards only the private conversion input whose flow equals
the original signal. Adding a common input charge and equal output revenue
continues to cancel by total conservation, including all new averaging
and copy flows. Hence the previous objective identity and hardness
equivalence are preserved exactly.

Quality shifts, normalization, and duplication into two upper-bound
coordinates preserve all gadget equations and graph degrees. The bounded
flow model with fixed pool and quality counts is in NP by the separately
reviewed lemma. The refined class is therefore NP-complete under the
stated exact supply/demand contracts. No strong-hardness or removal of
lower flow requirements follows.

## Independent assembled-network checks

The [separate reviewer implementation](../code/pooling_bypass_copy/independent_degree_four_review.py)
builds every averaging source, requested port, auxiliary chain, zero
chain, and root-capacity source independently of the author's checker.
It reuses only the reviewer's earlier ordinary-node/arc LP backend.
The network model contains no explicit cone, averaging, or signal-copy
equations beyond the physical supply/demand and quality constraints.

It passed 80 projection LP optimizations against independently supplied
cone LPs, and 94 complete pooling fixed-composition LPs, including 38
excluded compositions. Cases include zero rows, single-port rows,
repeated variables, nontrivial zero padding, empty simplex sections,
and original/shifted qualities. All generated input degrees were at
most four, gadget output degrees were three, upper flow bounds were at
most four, and no parallel arcs occurred.

Weakening **only** the averaging inputs' exact supplies, while retaining
all midpoint supplies, changed the maximum of `x0-x1` from zero to two
on a cone requiring equality. This isolates and detects the new gadget's
essential exact-supply condition.

The LP tolerance was `1e-8`. These numerical checks corroborate the
projection argument; they do not constitute a certified global solution
of the unconditioned nonlinear problem.
