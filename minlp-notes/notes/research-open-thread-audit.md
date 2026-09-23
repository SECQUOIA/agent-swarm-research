# Audit of existing research threads at closure

Date: 2026-09-05. Auditor: `close_inventory`. The user requested completion
of already started work and then a stop. This inventory distinguishes
unfinished proof obligations from historical progress labels and open
research questions. It does not initiate new directions.

I compared the README, reopened-run status, continuation assessment, log,
the previous [research closeout](research-closeout.md), current result
headers, investigation notes, and linked review records. The current
bilevel/resource/inverse, two-source-quality pooling, correlated energy
maximization, and existential-real pooling/power work have separate
closure owners. Their final status must come from those owners, rather
than this snapshot.

## Integer precision

| Thread | Finite disposition and evidence |
| --- | --- |
| Scalar quadratic, one-sided inertia, and simultaneous quadratic rank | Solved within the stated approximation model. The [scalar law](../results/quadratic-rank-integer-complexity.md), [inertia law](../results/quadratic-inertia-one-sided-integer-complexity.md), and [noncommutative-rank law](../results/quadratic-system-noncommutative-rank-complexity.md) link completed reviews. The cross-product counterexample is retained and subsumed by the system law. |
| Rational quadratic construction, unequal accuracies, general error bodies | Solved under the explicit rational input/oracle promises. The current [weighted construction](../results/quadratic-weighted-precision-polynomial-construction.md) and [general norm theorem](../results/quadratic-general-norm-output-precision.md) supersede early exploratory questions about absolute-sum error. No unreviewed oracle step was found in their stated dependency records. |
| Nonquadratic local rank | The [smooth-map rank sandwich](../results/smooth-map-local-rank-integer-complexity.md) is reviewed, and the scalar constant-Hessian-rank case is resolved by [its companion](../results/constant-hessian-rank-smooth-precision.md). Exact equality between local and global rank invariants for arbitrary varying-rank smooth or polynomial systems remains unproved. The cone example shows why the global invariant is not automatically exact. This is a recorded mathematical boundary, not a missing step in the proved sandwich. |
| Shape-sensitive scalar and separable construction | Completed and superseded by the [dense convex polynomial theorem](../results/convex-polynomial-compiled-integer-precision.md) where applicable. Positive-power and sparse-exponent variants retain distinct representation advantages. The curvature integration and rational-knot dependencies have completed reviews. |
| Coupled convex outputs | Dense coupled outputs are covered by the [multivariate separable oracle-body theorem](../results/convex-separable-vector-oracle-curvature-rank-precision.md), with sharper box/facet variants. The older rational-knot note's general coupled-output open label was stale for dense encoding and has been corrected. This does not extend its binary-exponent size guarantee to every coupled sparse mixture. |
| Binary versus general-integer separation | The [degree-dependent nonconvex separation](../results/polynomial-graph-binary-integer-degree-gap.md) and [exact convex degree-32 product family](../results/convex-polynomial-box-error-exact-integer-gap.md) have completed independent reviews. The growing-input product does not answer the one-input, arbitrarily many convex outputs, box-error question. |
| One-input output-independent box-error overhead | Unresolved exact obstacle, recorded in [the lattice investigation](convex-vector-box-gap-lattice-investigation.md): violation regions for individual outputs are convex and lattice-free, but their union need not be convex. Ordinary Helly or integral Radon bounds do not supply the missing simultaneous argument. No growing one-input gap or universal constant upper bound is claimed. |
| Tilted-body separation and fixed-conditioning bounds | Completed supporting results. The [tilted construction](convex-vector-tilted-error-integer-gap.md) lets conditioning grow; the [conditioned theorem](componentwise-convex-fixed-condition-integer-gap.md) bounds the loss when conditioning is controlled. The root's completed simplex-band addendum was present despite stale pending wording, now corrected. |
| Positive-power vector witness attempts | Useful checked negative outcomes: [three-witness obstruction](positive-vector-three-witness-integer-obstruction.md), [cap-set consequence](positive-vector-capset-integer-lower-bound.md), and [vector refinement obstruction](positive-polynomial-vector-refinement-obstruction.md). None establishes the unresolved growing one-input gap. |
| Higher-dimensional parity-hull shortcut | The [positive-power example](positive-power-parity-hull-obstruction.md) gives dimension-dependent error despite small pairwise midpoint gaps. The [simplex example](multivariate-parity-hull-refinement-obstruction.md) gives arbitrary interior error despite exact edge agreement for a nonsmooth convex function. Their elementary formulas were reread in this audit and are correct with their explicit scope; neither constructs a full integer-lift separation. |

The standalone [feature-curve note](positive-polynomial-feature-curve-geometry.md)
had one actual scope omission: its feature index did not explicitly remove
degree-one monomials. Its lower Jensen bound fails for a positive linear
monomial. The note now explicitly removes affine terms and indexes only
`k>=2`, matching the proof and the original shape-precision audit. The final
separable theorem uses direct Jensen superadditivity and does not depend on
this older feature proof. This is a repaired supporting-note defect, not a
change to the promoted theorem.

## Spatial branch-and-bound and Benders

All six extensions of the original spatial lower bound have completed the
reviews linked in their result files: SDP–RLT, higher SOS, product domains,
relative gap, all quadratic box cuts, and bounded-degree monomial lifts.
The first four do not all claim two reviews; the stronger XOR and monomial
results do, and their two records are present. Early investigation labels
are historical and do not signal outstanding theorem audits.

The [affine-branching barrier](spatial-bb-affine-branching-barrier.md) is a
completed independently reviewed negative result about the current proof.
A single balanced halfspace can destroy the preserved moment vector and
force linearly many substitutions without losing exponentially many Boolean
witnesses. General affine branching remains outside the theorem. Known
short perfect-satisfiability refutations do not certify the required constant
fractional objective gap, so they do not settle the stronger model either.

The [known clique cut](spatial-bb-known-clique-cut.md) closes the earlier
fractional-cardinality instances; decomposition also closes their independent
fixed-block relative-gap family. These are material scope limits, already
stated in the promoted results. The [shared source assessment](spatial-bb-strengthening-novelty.md)
is complete for its stated scope. A subsequent root [focused source closeout](supporting-results-source-closeout.md) now covers the direct-product and facial-pooling pending wording, retaining qualified priority.

The [Geoffrion result](../results/geoffrion-property-p-conjecture.md) and
[its complete audit](review-geoffrion-property-p.md) settle the precise
noncompact common-optimizer implication. The informal computational Property
P conjecture is not refuted. The closed-image and polynomial-attainment
positive conditions are proved and correctly attributed to established
theory. A broader historical comparison of conic-image examples remains
outside the limited priority claim; it is not an unproved theorem premise.

## Supporting elimination lemmas and FBBT

The [monotone polynomial-root lemma](monotone-polynomial-root-polytope-optimization.md)
has two completed audits including fixed piecewise-polynomial partitions.
The [affine-strip projection lemma](parametric-affine-strip-path-projection.md)
has completed path and tree/fixed-cycle-rank audits. It deliberately excludes
arbitrary dense objectives and retains infimum/attainment distinctions.
The [Klee–Minty path obstruction](parametric-path-lp-investigation.md) and
its reviewed slab refinements explain why generic explicit-message elimination
does not fill that exclusion.

The symbolic binary submodular path-cut statement in Section 1 of
[the clamp investigation](parametric-path-cut-clamp-investigation.md) was
a genuine remaining small review task. It now has an independent
[full review](review-parametric-path-cut-clamp.md), including the polynomial
sign-cell description, coefficient lengths, cycle conditioning, and all tie
strata. The retained exact checker passed 360 exhaustive-label comparisons
when rerun. Section 2's pooling application has its own closure owner and
is not certified by that review.

Both FBBT results already had the [dedicated source assessment](fbbt-novelty.md).
The iteration theorem and investigation incorrectly still described that
search as pending. Their wording now links the completed assessment and
retains its limitation: slow monotone iteration is established; the potential
contribution is the precise primitive forward-and-reverse contractor bound
and restricted continuous FBBT hardness transfer.

## Earlier lanes and final disposition

The previous [closeout](research-closeout.md) explicitly closed the CIA,
positive multilinear/positive-box, incidence-width, common-factor, rank-one,
and network–simplex investigations. Current conjectures there include exact
cubic/positive-box constants, width-three balanced or TU partitions,
largest-heavy-mode repetition, and further exact finite-grid CIA values.
They are preserved open questions rather than silently assumed results.
Earlier brainstorm-only alternatives in candidate-direction lists were not
started theorem projects and need no new investigation to close this run.

The current pooling owner reports the [two-source-quality convex feasibility
theorem](../results/pooling-two-source-qualities-convex-feasibility.md) promoted
after two final source-interval proof audits and a source assessment. The
exactly contracted scalar degree-two common-capacity extension is still
receiving its own closure audits. Generic interval-contract variants, dense
arc-profit optimization, and physical realizations of the generic path
aggregate-slab hardness construction remain stopped unresolved boundaries;
none is a promised consequence of the verified endpoint or flow reductions.

No promoted theorem with a missing claimed review was identified in this
inventory. This is a review-record and dependency audit, not a fresh proof
of every theorem in the repository. The concrete supporting-note omission
and stale statuses above were corrected. The active closure owners should
finish their existing proof/source tasks, after which the retained unresolved
questions can remain explicitly open and the work can stop as requested.


Root reconciliation: the affine-term correction in the feature note was
independently reread. For `k>=2`, convexity of `x^(k/2)` gives the lower
quarter-distance bound and arithmetic-geometric mean gives the upper
half-distance bound. Removing affine terms preserves all Jensen gaps.
The correction is valid and does not alter the promoted direct-Jensen proof.
