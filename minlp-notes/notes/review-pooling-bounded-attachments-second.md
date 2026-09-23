# Second audit: fixed total number of pool attachments

Date: 2026-09-05. Reviewer: `pooling_all_two_review`. PASS.

Reviewed Section 1 of
[the attachment investigation](pooling-unbounded-attachments-investigation.md).
The extension is a direct consequence of the reviewed path projection
and fixed-dimensional algebraic optimization arguments.

If the total number of pool-incident arcs is the fixed number `a`,
there are at most `a` external attachment nodes and at most `2a`
bypass arcs incident to them. Retaining those bypass flows, all `a`
pool flows, and one input fraction per pool input arc gives at most
`4a` scalar variables. The number of nontrivial pools is itself bounded
by `a`. Each pool quality is affine in its fractions; intake consistency
and receiving-output quality masses have degree at most two. Arbitrarily
many attributes add rows but no further core variables. The absence of
pool-to-pool arcs is an explicit assumption.

The remaining boundary components are scalar paths. A path may connect
two arcs at the same attachment, which simply produces a relation on
those two already retained coordinates. Shared input or output nodes
adjacent to more than one pool are retained whole, so their common
capacities and quality rows are preserved. The bounded planar
composition and affine lifting proofs apply unchanged.

The zero-throughput preprocessing is correct. A pool lacking an incoming
or outgoing arc must carry zero on every incident arc. Incompatible
positive lower bounds on those arcs or on pool throughput are rejected.
The adjacent external-node contracts must remain, since a bypass or
another pool can satisfy them, or their remaining infeasibility may need
to be detected later. At a zero-throughput pool with allowed inputs,
any simplex fraction gives the same zero outgoing quality mass.

When `a=0`, no nonlinear mixing remains and bounded rational LP
feasibility applies. For fixed positive `a`, fixed-dimensional
semialgebraic decision gives polynomial-bit feasibility and exact
algebraic recovery. A further fixed number of designated objective
coordinates admits the already reviewed optimization extension.

This result does not require a bound on affine quality rank. It does
require the total attachment count to be fixed; it does not establish
the proposed result with a fixed number of pools but arbitrarily many
pool-incident arcs.
