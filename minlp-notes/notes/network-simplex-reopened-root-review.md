# Root review and adjudication of the network–simplex continuation

Date: 2026-09-07. Final integration complete. Independent
agent reviews are internal research checks, not journal peer review.

## Mathematical readings

The root read the complete bounded-rank proof, the sharp K4 example, the
balanced-incidence and Fibonacci series–parallel constructions, and the
observation-sensitive elimination proof. These readings supplement the linked
independent reports; they do not replace them.

### Bounded block rank and sharp rank three

The original-space theorem has a sound chain of dependencies: fundamental-cycle
matrices are totally unimodular; their primitive edge directions and their
images under a selected row basis are ternary; a finite central arrangement
refines every state support function; and its primitive rays and transformed
dual multipliers have a rank-only cofactor bound. The support argument handles
lower-dimensional state polytopes and zero weights. The active-branch inequalities
are globally valid because state support functions are minima of affine upper
bounds with nonnegative multipliers.

The coefficient conclusion concerns the flow/product columns in a specified
rational inequality normalization. It does not bound primitive coefficients
after clearing arbitrary simplex-data denominators. The K4 section uses actual
free observed-product coordinates and has a two-dimensional local interior, so
affine-hull equations cannot hide its necessary ratio two. The explicit residual
state and two segment states provide sufficiency, not merely a necessary cut.

Independent report: [bounded-rank review](review-network-simplex-reopened-bounded-rank.md).
The general proof and its later sharpness extension both passed.

### Series–parallel coefficient growth

The root checked the balanced-incidence lemma's local sufficiency: positive
balancing multipliers preserve the common state-throughput total; invertibility
constructs a nearby profile; the nonnegative slack can be removed from an
allowed state without violating capacities. The Fibonacci column equations
force the stated recurrence and prove invertibility. Complementing the incidence
matrix preserves a positive balancing vector and permits only linearly many
observed coordinates. Thus the large coefficients are not encoded as large
network data, and the coordinate-section boundary forces an ambient facet ratio.

This does not prove hardness of separation or large extension complexity. The
number of simplex states grows; fixed-state claims need a separate argument.
The known compact extended hull remains compatible with the result.

The final flat-chain positive result supplies that separate argument for this
topology. The root checked its partition of states by which of the two arc
products are observed, the attainable interval for each gadget's aggregate,
and the shared-profile gluing. Its signed-subset Farkas circuits have bounded
support and determinant-bounded primitive multipliers. Grouping duplicate rows
is exact; merging distinct observed-state polytopes without those conditions is
not used. The bound and separator permit zero state weights. Their scope remains
unit-flow/unit-capacity flat chains, not arbitrary nested series–parallel graphs.

Independent report: [series–parallel review](review-network-simplex-reopened-series-parallel.md).
The simple M-family and both Fibonacci variants passed. Later corollaries are
listed separately in that report when checked.

### Sparse and observation-sensitive extended hulls

The root authored the initial block/path compressed formulation. Independent
review found a wording defect in its proof: only extension-variable coefficients,
not all variable coefficients, were asserted unit there. This is corrected.
The distinction between row count and sparse-matrix nonzero count is also now
explicit.

The observation-sensitive refinement eliminates independent observed directions
by unimodular pivoting. The root checked the Schur-complement minor argument,
the use of a single actual flow coordinate in each residual bound, and the
distinct product indices that prevent coefficient accumulation. Rank-nullity
identifies the remaining dimension with cycles entirely supported on unobserved
arcs. Completion minimality applies only to adding individual coordinates for
ambient linear reconstruction, not arbitrary lift dimension or degenerate faces.

Independent reports: [base formulation and implementation](review-network-simplex-reopened-compressed-hull.md)
and [observation-sensitive theorem](review-network-simplex-observed-rank-elimination.md).

## Implementation and computation decisions

- The exact specialized separator is reviewed separately against the original
  graph hull. It supports cycle/theta/parallel-path blocks and rejects unsupported
  topology. Its cuts and accepted decompositions use exact rational arithmetic.
- The general compressed LP model has exact rational coefficients but uses a
  floating-point LP engine. Its separate certificate producer may return a
  rational Farkas cut only after exact nonnegativity, auxiliary cancellation and
  strict-violation checks. Numerical feasibility is explicitly not an exact
  membership certificate.
- The full-state, generator-metadata compressed, and general-graph compressed
  formulations are compared independently. Bounds from the same exact projected
  hull must agree. Cuts cannot be advertised as stronger than that hull.
- Early timing omissions were corrected after review. Final timing records
  include construction and reconstruction where stated, and distinguish numeric
  optimization from exact verification. Repeated measurements and the observed
  elimination option are checked during final integration.
- Compression, rather than repeated cutting, supplies the observed optimization
  benefit. The negative cutting-plane comparison is retained, not omitted.

The final flat-chain implementation passed a separate exact review. That review
found malformed fractional observation indices could be accepted silently; both
separator constructors now reject them, and regression tests cover the fix.
All eleven specialized implementation tests passed in the root's final run.
The benchmark reviewer also repaired a failure-classification issue: an LP
rejection must have the explicit infeasible status, not merely a failed solve.
The full five-repeat study was rerun after that correction.

The root additionally reran all 600 general-formulation objective comparisons,
758 membership checks, 476 verified cuts, and six structural integration cases.
A first unittest discovery command lacked the package top-level context and
failed to import a relative module; invoking the documented package modules
resolved that command error. It was not a mathematical or implementation failure.
Final artifacts and commands are recorded in
`code/network_simplex_review/final-validation.json` from the repository root.

## Source positioning

The [literature audit](network-simplex-reopened-literature.md) identifies direct
predecessors for disaggregation and block gluing, network/min-cut Cayley hulls,
edge-direction arrangements, and reduced RLT product reconstruction. These
mechanisms are credited. The candidate contributions are the precise structural
combinations and bounds, the restrictive graph coefficient examples, and the
verified implementation/measurements. No bounded unsuccessful search establishes
absolute novelty.

A separately reviewed source-boundary note records why a common constraint
matrix alone does not justify exact reaggregation. The current formulation merges
only homothetic copies of the same unobserved-state domain, so it does not use
that invalid general inference. The source correction is not a new primary
contribution of this continuation.
