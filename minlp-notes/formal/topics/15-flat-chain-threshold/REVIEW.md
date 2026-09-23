# Flat-chain threshold review

Status: all sixty mathematical obligations and the implementation review are
complete, with no unresolved soundness or scope finding. Final frozen-source
build, axiom audit and fingerprint results are recorded separately by the
coordinating agent in `VERIFICATION.md`.

## Independent review records

- [Circuit, coefficient, and obstruction review](reviews/geometry-final.md):
  independent reading of substantive statements and proofs, manuscript comparison,
  targeted builds and standard-axiom probes. The reviewer authored no reviewed
  proof module. Includes the later zero/one/two-label primitive counts and unit
  descriptions, and the ambient b-flow boundary.
- [Algorithm review](reviews/algorithms-final.md): independent source grouping,
  preprocessing, actual query execution, recovery, operation/encoding bounds,
  unit repair, and observed-label integration. The reviewer authored no reviewed
  proof module. The record distinguishes a build interrupted by an in-progress
  dependency edit from its successful frozen-source rerun.
- [Balanced-incidence review](REVIEW-BALANCED-OBSTRUCTION.md): earlier detailed
  construction review. Its authorship statement identifies which supporting
  modules were written by that reviewer; this is not represented as wholly
  independent evidence. The subsequent geometry review independently checks
  the terminal obstruction results.
- Earlier [general-circuit](reviews/general-circuits.md),
  [partial-Farkas](reviews/partial-farkas.md), and
  [unreduced-enumeration](reviews/unreduced-circuits.md) reports preserve the
  investigation history. Their open integration notes are superseded only by
  the later terminal declarations mapped in [COVERAGE.md](COVERAGE.md).

The coverage reviewer independently read Section 7, its required dependencies,
the sixty-item frozen inventory, and the relevant current terminal declarations.
That reviewer authored only `COVERAGE.md`, `FINISHING.md`, and this review record,
not the proof modules. No new build is attributed to that source-inspection
review; commands actually run by the other reviewers are recorded in their
individual reports and final verification evidence.

## Findings closed during the finishing review

1. **Original-row provenance.** Optional source-only grouping preserves absent
   normals and an attaining original row identifier. The augmented negative-total
   bound zero from the earlier feasibility proof is never treated as the literal
   source row `lambda_0-t` in coefficient repairs.
2. **One fixed finite original-coordinate family.** The general determinant
   family and the zero/one/two/three-label unit families include domain rows and
   both signs of simplex equality. Their expressions are fixed across queries
   of one observation pattern. Independently supplied b-arcs are handled by the
   actual gadget balance equations, whose coefficients are themselves unit.
3. **Exact primitive counts.** The reduced `1,5,16` counts now concern all
   primitive integer circuits, not merely listed supports. Real support-minimal
   classification, a weight-one pivot and gcd normalization establish the exact
   finite sets. The unreduced `1,5,41` classification similarly concerns all
   mathematical primitive circuits. Maximum weights are bounded and attained.
4. **Original-domain rejection.** Complete executable separators now return a
   strict globally valid cut for failed original-domain checks as well as failed
   profile tests. The three-label result returns an actual repaired unit affine
   expression, not only a proof that some unit representative exists.
5. **Constructive output.** Checked witness recovery includes actual admission,
   cached-basis profile recovery, residual restoration, greedy state filling and
   normalization. Positive-weight filtering proves an exact convex combination
   of at most `m+1` actual graph points and excludes zero-weight atoms.
6. **Operand and cost scope.** Input bit bounds are applied to actual returned
   values. Domain-expression trees include hidden b-flow arithmetic; preprocessing
   includes cofactor normalization, Euclid operands and validation partial sums.
   Signed-subset preprocessing has its own total-work specialization. These are
   explicit arithmetic/word/schoolbook models, not runtime refinement of Lean's
   compiled rational backend.
7. **Actual unreduced row connection.** The signed-library coefficient bound is
   instantiated with literal full-profile source expressions. A dummy state of
   zero capacity reuses existing syntax without eliminating an original state.
   The negative-subset upper endpoint and actual profile equivalence are proved.
8. **Observed-label composition.** The finite unit-description theorem now
   quantifies over every real original-coordinate query, using actual affine
   substitution and complete original simplex rows. Separate zero-, one-, and
   five-test theorems instantiate all cases with at most two observed labels.
   Cached rational membership, separation and witness programs check the full
   original weight vector before compression. Returned cuts are valid at every
   real original hull point of the pattern. Cached normalized atoms and rank
   lookup reproduce all original moments, with compact and dense output sizes
   distinguished explicitly. The mathematical observed-count work bounds are
   proved. `ThresholdObservedBits` transfers original `B`-bit input data to the
   actual compressed width `3+(a+1)*(B+1)`, including empty observed sets and
   zero-weight observed labels.
9. **Sharp obstruction.** The four-label and star-family results use exactly two
   individual original products on a coordinate-plane section. Their unavoidable
   ratios survive every valid affine equation. The construction includes the
   displayed neighborhood, boundary feasibility, and actual graph counts.

## Boundaries retained in the final claim

The manuscript application assumes `L >= 1`. Several algebraic Lean statements
also allow `L=0`; that extension is not a claim about a zero-gadget graph with
distinct source and sink. Coefficient bounds concern flows and observed products;
constants and simplex coefficients are unrestricted. The real feasible profile
may be lower dimensional, state weights may vanish, row minima may tie, and
normal groups may be absent.

Only the authorized flat-chain threshold topic is being finished. Nested
series–parallel networks, the separate Fibonacci development, later topics,
Python implementation refinement, benchmark history, and novelty claims are
outside this completion. Project-wide verification and CI status/log inspection
are not part of local checks.

## Implementation finding resolved

The independent algorithm reviewer found that `labels.toFinset.card` was being
evaluated as a runtime implicit dimension, repeating deduplication after the
observed cache was built. The corrected entry points use `runCachedSize` and the
stored label-array size; rank-helper inlining removes the remaining unused
runtime argument. Independent generated-C inspection confirmed no deduplication,
finite-set cardinality or order-isomorphism call in the cache, membership,
witness and separation entry-point bodies. This is a targeted implementation
check, not a general compiler or machine-runtime proof.

[COVERAGE.md](COVERAGE.md) maps all sixty obligations. No mathematical or
implementation-review gap remains. The coordinating agent completed the final
delivery checks in [FINISHING.md](FINISHING.md); their commands and results are
recorded in [VERIFICATION.md](VERIFICATION.md), separately from this source review.

## Follow-up: compact payload versus returned storage

A source review found that the exact flow/weight count in `ALGORITHMS.md`
described the normalized decomposition payload as if it counted all storage in
`ObservedRecovery`. The returned structure also retains compressed input data,
restored profiles, and unnormalized flows. The numerical inequality
`observedWitness_compact_flow_size` does not measure that structure.

The algorithm guide, FC59 coverage row, and lemma comment now distinguish the
payload from retained intermediate data. The asymptotic storage order and the
recovery theorem are unchanged. This correction changes documentation only.
