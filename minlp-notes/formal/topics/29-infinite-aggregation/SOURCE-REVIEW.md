# Source inventory: infinite aggregation under HHC

Inventory date: 2026-09-22. This semantic inventory was frozen before
completion. Subsequent implementation and independent reviews cover all
12 claims; machine-check results are in [VERIFICATION.md](VERIFICATION.md).

## Recommended scope

The source is [Hidden hyperplane convexity does not imply finite quadratic
aggregation](../../../results/infinite-quadratic-aggregation-hhc.md),
specifically the three-inequality construction, its HHC proof, exact good
multiplier classification, indispensable strict rays, and finite impossibility
for weak good aggregations of the closed hull. The recommendation singled
out the specific two-by-two Gram argument before a general Gram-map theorem.
The frozen scope therefore includes every replication `r≥2`, and explicitly
includes the four-variable case `r=2`.

The source's Theorem 1 also states stronger results whose proof uses later
sections: an exact hull formula and an obstruction to arbitrary strict
quadratic descriptions. Its closed discussion additionally gives countable
sufficiency, a lifted SDP, and equality with the hull of the weak original
system. Those conclusions were not part of the recommended formal package
and are excluded. The quantitative follow-up and the general sharp Gram-map
theorem are also excluded. Topic 29 must not be described as formalizing
the entire source note.

## Original variables and HHC

The source uses Euclidean squared norms `sum_j u_j²`, `sum_j v_j²`, and
inner product `sum_j u_j v_j`. A plain Lean function space `Fin r→R` carries
a maximum norm by default; substituting its norm for the source's Euclidean
norm would change the system. The implementation must use explicit sums,
dot products, or an identified Euclidean space. Reindexing the pair `(u,v)`
into the `2r` original coordinates and adding the homogeneous coordinate
must preserve the actual matrices and maps.

HHC is convexity of every homogeneous hyperplane image, not convexity of
the full image or a projection/closure. The source parameterizes a
hyperplane by `tr(P^T U)+s t=0` and uses its Gram pair `(G,T)=(U^T U,t²)`.
Its feasible Gram pairs satisfy `G PSD`, `T≥0`, and
`s²T≤tr(P^T P G)+2 sqrt(det(P^T P) det(G))`. An implementation following
this route must derive the full fixed-Gram interval and sufficiency of
this inequality, including singular Gram matrices, singular `P^T P`,
and `s=0`. A closed convex superset of the image would not suffice.

At `r=2`, the orthogonal group is disconnected. The source uses planar
rotations of both columns from the identity to its negative inside one
component; it does not assume the whole orthogonal group is connected.
Any alternative proof must still cover this lowest replication rather
than quietly replace `r≥2` by `r≥3` or a larger completion dimension.
The general Gram-map theorem is unnecessary if a specific two-column
argument establishes the required actual image convexity.

## Good multipliers and the spectral bridge

Goodness has two independent conditions beyond nonnegative nonzero weights:
at most one negative eigenvalue of the homogeneous aggregate, counted with
multiplicity, and strict aggregate containment of the ordinary hull.
Defining goodness to mean the proposed cone inequality would assume the
central classification. A basis-independent condition excluding a
two-dimensional negative-definite subspace is a useful proof device, but
its equivalence to the spectral condition must be proved for the actual
real symmetric matrix.

The quadratic block is the repeated two-by-two block with off-diagonal
`-lambda_3/2`; the homogeneous scalar is
`lambda_3/2-lambda_1-lambda_2`. A negative direction in the two-by-two
block gives two independent negative directions using distinct replicas
when `r≥2`. Within the proposed cone, the quadratic block is PSD and the
scalar is strictly negative for every nonzero nonnegative multiplier.
This gives exactly one negative eigenvalue even when the quadratic block
is singular. The aggregate's strict sublevel set is convex and contains
`S`, so it contains the ordinary convex hull. No full hull-description
theorem is needed for this direction.

## Ordinary hull, rays, and the closed obstruction

The Gram witness at `tau∈[1,2]` is positive definite and can be realized
already in two coordinates. The implementation must produce actual vectors
at every parameter, not just a symbolic residual vector with the desired
properties. Its residuals have the exact scale `1/10`. For a good multiplier
the aggregate is nonpositive, and equality holds precisely on the positive
ray through `(tau,1/tau,2)`. Zero multipliers are excluded throughout.

Because its own good aggregation is zero, this witness is outside the
ordinary hull. All other rays have strict negative slack. Thus an actual
exact strict intersection must contain that ray. Distinct parameters must
be shown to determine distinct positive rays; a proof about uncountably
many family indices alone would allow repetitions and miss the source
claim. The statement is conditional on an exact representation. This
package does not separately formalize the external BDS theorem asserting
existence of one, and does not infer the excluded explicit hull formula.

The unperturbed witness need not be outside the closed hull: the omitted
inequality is only zero there. For the weak finite-family obstruction,
select an omitted parameter and decrease the Gram off-diagonal by a small
positive amount. Finite many strict slacks persist, the Gram matrix stays
positive definite, and the omitted aggregate becomes strictly positive.
Continuity extends each good strict inequality to a weak inequality on
`closure(convexHull S)`, so this perturbed point is genuinely outside the
closed hull. This argument does not interchange closure and arbitrary
intersection, and does not identify the closed hull with the hull of the
source's weak feasible system.

## Documentation, paper, and completion

At inventory time, the source reported mathematical reviews and exact
numerical witness checks, with no Lean formalization. Its status now records
the completed Lean checks with the exact restricted scope above.
The concurrent paper already has separate certificate, consequence, and
boundary-example sections and the topic 27–28 formal accounts. Preserve
their sources and stage records. A later topic 29 formal account should
state its results independently of unverified hull formulas or paper-stage
acceptance, and preserve the qualified literature-priority statements.

Completion review must inspect actual HHC and spectral interfaces, the
four-variable specialization, Gram realizability and endpoint cases,
ordinary-hull exclusion, ray injectivity and cardinality, and the finite
perturbation witness. Every frozen obligation needs a declaration mapping.
Record targeted builds, transitive axiom checks, and module kernel replays
with source fingerprints; mathematical reviews and numerical witness
checks are different evidence. No project-wide verification or CI status
inspection belongs to this local task.
