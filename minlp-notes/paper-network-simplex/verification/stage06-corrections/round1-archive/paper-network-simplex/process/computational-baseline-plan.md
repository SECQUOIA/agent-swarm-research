# Baseline improvements required for Stage 6

The root inspected the existing benchmark builders while earlier mathematical
stages were under review. No new performance claim is accepted here.

The existing long-chain `full_ef_membership` route already treats original
coordinates as data and keeps only state-flow variables. Its residual weight is
zero in both long-chain candidate families, but it retains that zero state.
Reporting construction-inclusive advantages over only this baseline leaves
straightforward zero-state removal untested.

Root correction on rereading the actual builder: an earlier version of this plan
incorrectly said the full baseline introduced fixed original variables. It does
not. The compressed membership route does retain original variables, but that
is a different method. The strengthened full baseline need only remove zero
states and improve domain/status handling where needed; do not claim the prior
full baseline had original-coordinate variables.

Stage 6 should implement and measure an independent fixed-point full-state LP:

1. Original x, y, z are data in a membership query; keep only the state-flow
   decision variables rather than introducing and fixing original variables.
2. Omit zero-weight states and directly check their observed coordinates are
   zero. Use positive-state capacity bounds, state balances, aggregate flow sums,
   and fixed observed entries. Distinguish infeasibility from other solver errors.
3. Keep construction and solver time separate, and report both. Do not infer a
   persistent-callback advantage from this experiment.

For the sparse many-state workload, include a global observed-label merger as
an ablation baseline: retain state flows only for labels observed somewhere in
the graph and one merged state for all other labels. Keep original simplex
variables and their objectives/constraints. This uses the already known
homothetic merger but no block/path/cycle or observation-rank compression. It
helps distinguish local graph savings from globally absent-state removal.

These comparisons may remove an apparent runtime advantage. That is a useful
result and should change the manuscript's interpretation rather than be hidden.
Exact compressed sizes and rational certificates remain mathematical benefits.
No industrial or persistent-solver claim is required for the paper.

## Candidate implementation updates from Stage 5

Conditional on Stage 5 acceptance, implement the reduced profile in the exact
flat-chain oracle. For m=2 use the explicit five scalar tests and direct interval
recovery without any circuit library. For m=3 use the reduced 16-circuit universe
and repair exceptional +/-2 bypass coefficients with one original gadget flow
balance, as proved in the new threshold theorem. General m uses the reduced
universe and exact basis recovery. Preserve the unreduced reference sufficiently
to reproduce historical counts/compare decisions; avoid two permanent public APIs
unless a concrete compatibility need requires them.

Measure the new m=2 method against the retained unreduced reference and the
zero-state-removed LP, with cold and warm costs reported honestly. Independently
verify arbitrary observation patterns, zero weights, exact returned cuts and
decompositions, and the m=3 coefficient-repair branches. No performance conclusion
is accepted before implementation, measurements, and five stage reviews.

## Avoid an avoidably slow LP assembler

A second root reading found that the legacy full membership builder repeatedly
slices CSR incidence rows inside Python state/vertex loops. For these regular
block matrices, a stronger and simpler baseline can assemble balances using
`sparse.kron(I_states, A)`, aggregate sums using a repeated identity, and
observation equalities with one COO matrix. Use this vectorized sparse assembly
for the primary positive-state membership baseline. Validate it against the
legacy independent builder and original equations on varied small graphs.
Otherwise a reported construction-inclusive win may mainly measure removable
Python row-construction overhead.

Likewise consider sparse block/Kronecker assembly for the full and globally
merged optimization baseline, where state balances/capacities have one sparse
linear map from original y to retained weights. Both baseline variants must
implement the same known disaggregation and preserve every original y objective
and fixed-y constraint. Keep prior reference source/results reproducible.

It is acceptable, and scientifically useful, if the stronger numerical LP wins
on both construction-inclusive and engine-only time. Exact original-coordinate
cuts, rational decompositions, and model-size reductions remain distinct outputs;
the paper must report the actual comparison without selecting a weaker baseline.

## Two-positive-state face and interior weights

The legacy flat benchmark has y=(1/2,1/2), so only two disaggregated states have
positive weight. There is an additional elementary baseline specialization: after
checking the original aggregate flow, write the two flows as f and x-f. Feasibility
is a single network-flow LP Af=lambda_1 b with bounds
max(0,x-lambda_2 u)<=f<=min(lambda_1 u,x). Observations in the first state fix
f_e=z; those in the second fix f_e=x_e-z. Check fixed values against the original
bounds and each other. This is exact for point membership. It reduces the model
to E variables with incidence equalities, and avoids pretending that a generic
two-block state LP is the strongest routine baseline. A single positive state
is checked directly. Keep the numerical-vs-exact certificate distinction.

Include the interior counterpart y=(1/3,1/3), residual=1/3 in the primary flat
study as well, so three genuinely positive states are exercised. A feasible
family has x_a=x_b=1/4 and x_h=1/2; shared profile 1/6 in each state permits
alternating one-label observations z=1/12 plus small multiples of 1/48, with
the other two a entries splitting 1/4-z. The legacy infeasible family
x_a=3/10,x_b=1/5,x_h=1/2 and alternating z=3/10 still works with these interior
weights: two observed branch states require total at least 3/5>1/2, although
individual McCormick constraints pass. Author must independently verify all
families and separate boundary/interior results.

A general vectorized positive-state LP remains the baseline at three or more
positive states. Optionally eliminate its last state as ordinary aggregation
substitution, but do not add speculative solver infrastructure. The two-state
network reduction is small, directly relevant to the existing test face, and
should be implemented or explicitly compared rather than left an unexplored
performance caveat.

## Local merging ablation with no globally missing label

The root counted the original seed33 four-block, five-path, m=128 optimization
case: E=43, O=36, only 11 globally observed labels. Full disaggregation has 5,675
variables, whereas global merging alone gives 644 before local compression to 255.
These are algebraic counts, not timing claims.

Add one moderate repeated optimization case in which all labels are observed
somewhere but each block sees few. For example, 16 articulation-linked blocks,
three length-two paths per block, 64 explicit labels, and four disjoint labels
per block covering all 64; retain three arc observations per label. Expected
counts are 111 arcs and 192 observations. Full/global formulations both have 7,279
variables, while initial local cycle compression has 495 (367 original plus 128
state-cycle coordinates). Choosing three distinct arcs among the six in a block
necessarily meets at least two paths, so each observed state has full rank two
and observed-coordinate elimination should remove all 128 auxiliaries.
The author must verify these counts and model equivalence independently.

This ablation distinguishes local graph/state savings from globally absent-label
removal and gives a nontrivial-scale forest-complement example. One five-run
optimization comparison is enough; avoid an unfocused expanded experiment grid.

## Objective-only decomposition and one coupled illustration

A fixed-y linear objective over the hull alone decomposes as
c_y*y + sum_j lambda_j min_{v in P}(c_x+c_z,j)*v.
Include a baseline that solves these ordinary network LPs, reusing the incidence
matrix and merging the globally unobserved state costs. Otherwise the numerical
section must not imply the objective-only examples inherently need a coupled hull
LP. This is classical simplex disaggregation and linearity, not a new result.

One bounded practical extension is an aggregate budget d*x<=B on the same
synthetic instance. A known reference graph point proves feasibility. Integer
d chosen from signs of an unconstrained optimum's displacement from that reference,
and a threshold halfway their resource values, make the constraint exclude that
optimum. Verify this construction and compare all equivalent formulations plus
McCormick under the SAME added row. The compressed model's original-variable rows
and the full/global objective-coordinate map supply the constraint without new
solver infrastructure.

This comparison concerns H intersect the budget: a relaxation obtained by
convexifying the network–simplex component before coupling it to the budget.
Do not claim this intersection is automatically the convex hull of the whole
budget-constrained nonlinear set. A single coupled case is enough to illustrate
where independent state optimization ceases to apply. No industrial validation
or broader new application project is requested.
