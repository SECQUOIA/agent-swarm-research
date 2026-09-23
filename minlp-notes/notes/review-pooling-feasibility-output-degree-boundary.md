# Independent review: the output-degree feasibility boundary

Date: 2026-09-05. Verdict: **PASS** as a corollary of the two reviewed
constructions. No additional source-priority claim is established.

Retain the network at the end of Sections 3–4 of
[the constant-data two-feed theorem](../results/pooling-constant-data-two-feed-np-completeness.md),
including every exact source supply, collector demand, constant-generator
contract, and other original exact flow contract. Omit the contract-
completion objective and its economics from Section 5.

Section 3 already proves that this contracted physical network is
feasible if and only if the positive-product source instance is a yes
instance. In particular, the constraint `sum b_i x_i>=K` remains enforced
by its complete constant-data binary circuit and comparator. It is not
the later completion objective and is not deleted with that objective.
All large source coefficients and the source threshold are encoded in
polynomially many constant-data gates. No large flow-bound coefficient
or objective threshold needs to be added to the feasibility problem.

The threshold circuit excludes zero total intake. For any feasible
contracted network, its original signal total `T` is positive, its
normalized mixture lies in the source polytope, and its physical
two-output throughput bound gives the positive-product inequality.
Conversely a satisfying source mixture extends at its allowed maximal
throughput, with every circuit, copy, conversion, and splitter contract
satisfied. Removing the completion economics loses none of these
requirements. The exact source/output lower bounds are essential;
deleting them as well would make zero flow feasible.

Restoring an exact contract sets its lower bound equal to its already
existing upper bound, which belongs to `{0,1,2,3,4}`. All other lower
bounds remain zero. Thus the feasibility instance retains the fixed
quality alphabet, one scalar upper quality, exactly one pool with two
input arcs and two output arcs, input total degree at most two, and
output total degree at most three. There is no numerical threshold left
outside the circuits. The original reduction remains polynomial even
with unary encoding of every physical numerical datum, proving strong
NP-hardness of this feasibility family.

Membership in NP follows from
[the fixed-parameter linear-fiber lemma](../results/fixed-parameter-linear-fibers-np-membership.md):
fix the pool's single quality parameter, after which all physical flow
constraints, including the exact contracts, are linear. The finite
capacities bound every nonempty fiber. The established active-basis
certificate applies unchanged, completing strong NP-completeness.

For comparison, impose input total degree at most two and output total
degree at most two under the same one-pool/two-feed/two-outlet setup.
Its bypass graph necessarily has maximum degree two, so
[the reviewed endpoint-projection algorithm](../results/pooling-degree-two-boundary-projection.md)
decides feasibility in polynomial bit time. That algorithm permits
arbitrary rational qualities and finite rational bounds, so it includes
the constant-alphabet subclass here.

The degree-three hardness does use degree-three outputs away from the
pool attachments: the source splitter creates ordinary collectors with
three incoming bypass arcs. Therefore the obstruction is not confined
to the fixed number of pool-adjacent nodes that the positive algorithm
already retains in its core. The averaging and coupling circuits in the
hard family require such splitters.

Together these results give the stated two-versus-three **total output
degree** boundary for feasibility, while input total degree remains at
most two and the pool interface is fixed. The positive theorem itself
has the more general bypass-degree formulation; these degree notions
should not be interchanged silently. This corollary does not classify
arbitrary dense-cost optimization or all-lower-bounds-zero feasibility.

No new numerical test is needed for this corollary: it removes only the
last economics transformation from the already audited physical
equivalence. The prior exact-contract physical tests and the independent
projection checks remain its supporting tests.
