# Independent review of feedback sharpness graph certificates

Reviewed 2026-09-20 against F06 and F07 in [CLAIMS.md](../CLAIMS.md).
The reviewer did not author or edit the reviewed proof modules. This review
covers `StructuralFeedbackFlowerGraph`, its supporting declarations in
`StructuralTreewidthDecomposition`, and `StructuralFeedbackPayoffSharpness`.
The unit polynomial and exact gap formulas were separately reviewed in
[sharpness-boxes.md](sharpness-boxes.md).

The flower graph certificates pass review. They close the F06 graph-membership
obligations identified in the earlier review: the family is an actual
feedback-one family with incidence treewidth exactly two. Both generic
payoff sharpness constructions also pass; it proves a retention obstruction for
nonnegative local payoffs, not general-f sharpness for positive monomials.

The named flower has anchor variable `none`, leaf variables `some i`, large
factor `none`, and bilinear factors `some i`. `flowerFactorScope` maps these
factor names to the exact `StructuralSharpness.leafSupport` and `pairSupport`
definitions. `flowerIncidence_iff_mem` proves the corresponding adjacency
statement in every case. `flowerFactorMap_bijective` proves that this is a
bijection onto all actual supports. It uses injectivity of the pair supports
and the fact that the leaf support excludes the anchor. There is no added,
omitted, merged or repeated nonlinear factor in this graph identification.

The width-two certificate uses a finite prefix tree with root `[]`, one node
`[i]` for every leaf, and a child `[i,i]`. The root bag contains the anchor and
large-factor vertices; the two bags on branch i add the leaf variable and
then replace the large factor by the bilinear-factor vertex. Every edge is
covered, every vertex is covered, and each vertex's bags form a connected
subtree. Bags have cardinality at most three. This is an actual tree
decomposition, rather than an assumed series-parallel representation.

The newly proved `HasTreewidthAtMost.isAcyclic` supplies the required lower
bound on width. For a hypothetical cycle it selects the cycle vertex whose
highest containing bag is deepest. Edge coverage and connected bags force
both distinct cycle neighbors into that same highest bag. That bag would
contain three distinct vertices, contradicting width one. The argument uses
only the stated decomposition axioms; it does not assume a graph minor or
elimination characterization that is still under construction elsewhere.

For `n>=2`, the two branches with indices zero and one are distinct simple
paths from the anchor to the large-factor vertex. Acyclicity would make those
paths equal, a contradiction at their second vertices. Thus the named flower
has no width-one decomposition. Injective incidence homomorphisms in both
needed directions transfer the upper and lower width bounds to
`flowerSupportGraph`, whose factor vertices are the actual support subtype.
`flower_supports_treewidth_exactly_two` therefore concerns exactly the
incidence graph required by F06.

The feedback theorem uses a larger ambient factor type containing inactive
scopes as isolated vertices. `flower_feedback_acyclic` works with that exact
convention. After deleting the anchor, each pair-factor vertex has just its
leaf-variable neighbor; any factor on a cycle would consequently have to be
the unique large-factor vertex. A variable on such a cycle would then have
the same preceding and following factor, impossible in a simple cycle.
Removed variables and unused factor vertices cause no gap in the argument.
The proof works for all n, while the nonacyclicity proof appropriately
requires `n>=2`.

The empty-feedback graph contains the named flower through an injective
homomorphism, so `flower_empty_feedback_not_acyclic` proves that zero deletions
are insufficient. Together with `flowerFeedback_card=1`, this shows the
exhibited feedback set is minimum. `feedback_one_sharp` then specializes its
proposed universal bound to this concrete set and uses the independently
checked actual ratio limit. Its premise asks for the bound for all flowers
with any size-one feedback set; it does not assume an optimizing law, a gap
identity, or the desired lower bound on the constant.

The generic indexed payoff example has f feedback coordinates and one
outside coordinate, all with mean one half. There is one factor for each of
the `2^(f+1)` complete binary states. Each payoff is its cell indicator. The
half-mass law on a state and its complement has all prescribed means and
attains expectation one half. The complement is distinct even when f=0,
because the outside coordinate remains. The matching upper bound follows
from the cell's containment in a prescribed-probability literal event.

The cell indicators sum pointwise to one, so their expected sum is one under
any global law. Their local optima sum to `2^f`. Summing any proposed
simultaneous retention guarantee therefore proves `c<=2^(-f)`; the proof
does not divide by a potentially zero quantity. The indexed residual
incidence graph is a subgraph of a star centered on the outside variable.
The f deleted variables are isolated. Thus the sharpness example has the
required actual feedback forest, including f=0.

These cell indicators contain zero literals. Nothing in these results
identifies them with positive-coefficient monomials. The source's caveat that
positive-monomial sharpness remains unproved for general f must be retained.

The private-variable variant removes the repeated-scope issue without
changing the calculation. Each state receives its own private binary
coordinate of mean one, and its payoff is multiplied by that coordinate.
`privateScope_injective` proves the scopes are distinct. All original shared
coordinates remain in each scope; the unique private coordinate also matters
to its payoff, so these are genuine supports rather than unused labels.

The local laws extend the two-atom laws with every private bit fixed to one.
They attain the same local optimum one half and preserve the prescribed
means of every shared and private coordinate. Under any feasible global law,
`privatePayoff_expect` proves that the mean-one multiplier leaves the cell
expectation unchanged. It uses upper and lower pointwise bounds and the
private mean, rather than asserting that a mean-one bit equals one at every
state of the ambient sample space. This distinction is essential: the sum
of private payoffs is not identically one on all binary vertices, but its
expectation is one under every feasible law. The private retention theorem
includes exactly that necessary feasibility premise.

`privateFeedback` has cardinality f. After deleting it, the residual graph
has the outside shared variable joined to every factor, and each factor
joined to its unique private leaf. Private leaves cannot lie on a cycle;
without them, a factor would have the same preceding and following outside
variable on any cycle. `private_residual_incidence_acyclic` proves this
for the actual indexed incidence graph. Since `privateScope` is injective,
these are distinct original scopes. The law, local optimality, expectation
sum, feedback size, scope locality and forest proofs together discharge the
private-scope variant of F07 as well as the original indexed version.

Combining this review with the independently checked unit-gap results
completes F06 and F07. It does not review or complete the unrelated
treewidth-two upper-bound coloring theorem, nor does it make any new
positive-monomial sharpness claim for f greater than one.

Both targeted commands passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralFeedbackFlowerGraph Formal.MultilinearGap.StructuralFeedbackPayoffSharpness
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-feedback-sharpness-review.lean
```

The temporary review file printed axioms for the width-one acyclicity
lemma, factor bijection, actual feedback and treewidth certificates,
feedback-one sharpness, both local-optimum constructions, both residual
forest proofs, both retention inequalities, private scope injectivity and
the private feasible-law expectation sum. All use only `propext`,
`Classical.choice` and `Quot.sound`; none use `sorryAx`. The final build and
axiom run include the completed private-variable variant. No proof edits,
project-wide verification or CI inspection were performed for this review.

Reviewed SHA-256 values:

```text
fdd5874530d51ea8248c9ad511590f2bcb954c5dec793c2127adbf54d52250b5  StructuralTreewidthDecomposition.lean
155e92a615f544a686625990695a72b5772b97d954876d0bffaec4cec5fc69da  StructuralFeedbackFlowerGraph.lean
9a16dfc356bb9c46360ac9d586922365c37ae5d96ba4dc75e152966b6f4ce9bb  StructuralFeedbackPayoffSharpness.lean
```
