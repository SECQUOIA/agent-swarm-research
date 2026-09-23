# Topic 15 finishing review

Status: all mathematical, implementation-review, and final delivery items are
closed. Independently assembled and completed on 2026-09-19.
Finish topic 15 only; the user's latest instruction does not authorize starting
or resuming another topic. Local verification is targeted; CI handles the
project-wide checks, and its status/logs are not inspected here.

## Mathematical and algorithm connections

- [x] **FC16–18: full general description.** `ThresholdBoundedDescription`
  combines source branches, domain rows and simplex equality in a finite affine
  family fixed by the observation pattern. `boundedDescription_coefficients`
  bounds every actual flow/product coefficient. `ThresholdAmbientDescription`
  explicitly treats independently supplied b-arcs under actual gadget balances.
- [x] **FC23: positive-state output.** `ThresholdPositiveAtoms` supplies the
  actual stable positive-weight filter. `checkedWitness_positive_decomposition`
  proves total weight one, exact original moments, graph membership, and at most
  `m+1` retained atoms. The stored zero-state fallback is not delivered as a
  positive atom and still performs no division.
- [x] **FC24–26: full query and cost.** `ThresholdResults` and
  `ThresholdSeparation` compose actual domain admission/rejection with the
  cached profile and witness algorithms. `ThresholdPipelineSize` applies input
  bounds to actual recovered profiles, state flows, atoms and products.
  `ThresholdDomainOracleSize` covers every expression-tree value, including
  b-flow subtraction intermediates. `ThresholdPreprocessOperands` covers
  normalization, Euclid division/remainder, validation products and partial
  sums. The final targeted build and audit passed on the frozen sources.
  Counted arithmetic is not a claim about the compiled rational backend.
- [x] **FC28: signed-subset work and original rows.**
  `ThresholdPreprocessOperands` specializes total preprocessing and bit work
  to `2^(d+1)` signed keys. `ThresholdUnreducedLift` retains all original states
  and proves exact full-profile equivalence. `ThresholdUnreducedRows` supplies
  literal source expressions, keeps the upper endpoint as a negative-subset row,
  proves their normals and unit coefficients, and derives the actual compiled
  coefficient bound and branch validity.
- [x] **FC27, FC30, FC33, FC37: small cases.** `ThresholdSmallDescription`
  supplies full finite zero/one/two-label unit families. The no-observation hull
  theorem supplies the flow/simplex boundary. `ThresholdSmallClassification`
  proves exact primitive-gcd counts `1,5,16`, attained maximum weights `1,1,2`,
  and distinct-normal counts. The counted direct recovery formulas and general
  checked basis recovery both specialize to these fixed dimensions.
- [x] **FC40–44: executable unit separation.** `ThresholdUnitOracle`
  discharges repairability from actual returned source rows and bounds the
  expression traversal. `ThresholdSeparation` returns a globally valid unit
  affine cut with strict query violation for every three-label hull rejection,
  including failed domain checks. `separateThree_linear` proves the full linear
  charge. Artificial box branches never enter the repair path.
- [x] **FC57–58: observed-label terminal composition.**
  `ThresholdObservedFiniteDescription` proves a complete fixed finite unit family
  for every real original-pattern query with at most three observed labels.
  `ThresholdObservedSmall` supplies the zero/one/five-test cases. Actual cached
  membership, separation and witness programs retain full original simplex
  admission; their correctness and observed-count work bounds are proved.
  `ThresholdObservedRecovery.observedWitness_cached_decomposition` proves exact
  moments for the stored arrays, rank lookup, and original weights.
  `ThresholdObservedBits.observedCache_inputBits` transfers original input bounds
  to every field of the actual compressed cache.

## Implementation review

- [x] The independent algorithm review's cached-size finding is resolved.
  `runCachedSize` passes stored array dimensions to membership, witness and
  separation; inlining the rank helpers removes the remaining unused runtime
  dimension argument. Independent generated-C inspection found no deduplication,
  finite-set cardinality or order-isomorphism call in the four actual cache/query
  entry-point bodies. See [the algorithm review](reviews/algorithms-final.md).
  This targeted implementation check does not assert general compiler or
  machine-runtime correctness.

## Independently examined boundaries

- [x] FC01–07 retain actual graph incidence, common state profile, residual
  restoration, capacities, observations, zero weights, and original domains.
- [x] Source-only grouping and branch validity are distinguished from the older
  augmented-box feasibility proof. In particular, the negative-total source row
  is `lambda_0-t`, not the artificial zero bound.
- [x] FC10–15 include the literal Hadamard exponent, a genuine non-strict
  Farkas alternative, finite cone decomposition, extreme/minimal ray equivalence,
  primitive cofactor normalization, and arbitrary absent-normal patterns.
- [x] FC19 now includes accepted-candidate minimality and a counted determinant
  and gcd construction, rather than only sound cancellation or a list length.
- [x] FC20–21 discharge boundedness from the source box rows and permit
  lower-dimensional and zero-dimensional feasible polyhedra.
- [x] FC29 counts mathematical primitive circuits, not only a list of valid
  certificates or a bounded search over integer weights.
- [x] FC47–53 use actual coordinate-plane sections of the original hull.
  The arbitrary-normal section lemma handles zero and negative components;
  the balanced construction uses the displayed epsilon, exact two-product
  restriction and residual-zero face; the star-family conclusion quantifies
  over all finite affine descriptions.
- [x] FC54–56 and FC59–60 handle zero merged weight, empty families, full
  original simplex constraints, and the distinction between compact output and
  materializing every state-arc entry.

## Delivery checks after integration

- [x] Reconcile every FC01–FC60 row in [COVERAGE.md](COVERAGE.md) with the final
  declarations. No unresolved integration item may be silently called complete.
- [x] Obtain final independent reports from the proof/algorithm review lanes;
  record which modules each reviewer authored and which they reviewed independently.
- [x] Add all topic-owned modules to the root import list exactly once, preserving
  unrelated work and not checking unrelated later-topic modules.
- [x] Run only the final topic-targeted warning-free build and axiom audit;
  record exact commands and results, with no `sorryAx` or added axioms.
- [x] Record final module list, reproducible source fingerprints, and verification
  evidence. Check the documentation links and declaration names.
- [x] Update README, algorithm guide, coverage, final review, and queue metadata
  to the actual finished state. Later topics remain deferred.

The earlier lane review documents are useful historical evidence but contain
integration warnings that must be resolved by the final review. This checklist
was produced by source inspection; it does not report a new Lean build.

Final delivery checks passed on 2026-09-19; see [VERIFICATION.md](VERIFICATION.md).
