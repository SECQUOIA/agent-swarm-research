# General circuit and recovery review

This is a lane coverage draft for FC10–FC28, reviewed against the actual Lean
statements on 2026-09-17. It is not a completion declaration for topic 15.
Module names below refer to `Formal/NetworkSimplex/`. The final topic coverage
should absorb this mapping after the remaining integrations pass.

## Coverage

| ID | Declarations and assessment |
|---|---|
| FC10 | `ThresholdDeterminant.delta01`, `one_le_delta01`, `delta01_one`, `delta01_two`, `delta01_three`; `ThresholdHadamard.delta01_le_hadamard`. The maximum includes order zero. `RowSignedZeroOne.det_natAbs_le` proves the actual whole-row-sign reduction. Complete. |
| FC11 | `ThresholdFarkas.farkas_inequalities`. Fourier–Motzkin proof for every finite row set and every dimension, with non-strict inequalities and no boundedness premise. Complete. |
| FC12 | `ThresholdPositive.PositiveCircuit.size_le`; `ThresholdCone.cancellation_cone_pointed`, `cancellation_cone_decomposition`, `extreme_ray_iff_positive_circuit`, `extreme_ray_iff_minimal_positive`, `PositiveCircuit.proper_supported_kernel_zero`. The decomposition is an actual finite list of positive multiples, with length bounded by input support size. Complete. |
| FC13 | `ThresholdPositive.PositiveCircuit.kernel_unique`; `ThresholdMinor.exists_nonsingular_coordinate_minor`; `ThresholdCircuitWeights.exists_primitive_bounded_cofactor_weights`; `ThresholdCircuitInteger.PositiveCircuit.exists_primitive_integer_weights`; `ThresholdCircuitCandidates.PositiveCircuit.exists_cofactor_candidate`. These choose independent columns, prove a nonzero cofactor kernel, normalize by the gcd, and relate the integer objective to the real circuit by a positive scale. Complete. |
| FC14 | `ThresholdDeterminant.RowSignedZeroOne.det_natAbs_le` and the positive, bounded, gcd-one output of `exists_primitive_integer_weights`. The primitive cofactor weights are bounded by `delta01 m`; this is not a bound on arbitrary scaled weights. Complete. |
| FC15 | `ThresholdCircuitCriterion.feasible_iff_positiveCircuits`; `ThresholdBoundedCriterion.feasible_iff_bounded_integer_tests`; `ThresholdPreprocessCriterion.feasible_iff_compiledPartialTests`. The last theorem uses the actual `preprocessCircuits` output and arbitrary `Option` patterns, including no present rows and zero normals. `ThresholdGeneralPacked.generalOracle_none_iff` connects the actual cached library and grouped scan to the reduced profile system. General mathematical criterion complete; final original-hull wrapper is owned by root. |
| FC16 | `ThresholdCoefficientBound.weighted_groupMinimum_eq_minimum`, `weighted_groupMinimum_nonneg_iff`, `weighted_groupMinimum_attained`. These quantify independent, finite, nonempty row fibers; absent fibers are handled by FC15, not assigned artificial minima. Literal affine expression semantics are `ThresholdRows.rowExpression_eval_other` and `AffineExpression.eval_update`. A final general finite original-coordinate description should explicitly compose these with the source grouping and original domain. |
| FC17 | `ThresholdRowOccurrences.row_flow_product_unit`; `ThresholdGeneralCoefficients.sourceBranch_coefficient_bound`, `compiledBranch_coefficient_bound`, `sourceRow_coefficient_bound`. These bound the actual `rowExpression` coefficients, including repeated occurrences, not arbitrary abstract row data. Scalar zero rows are included. Original-domain rows need their own elementary coefficient check in root's final wrapper. |
| FC18 | `ThresholdCoefficientBound.exists_violated_valid_branch`; `ThresholdGeneralCoefficients.sourceBranch_nonneg_of_hull`; `ThresholdPackedOracle.packedOracle_separates`. These retain actual row identifiers and fixed affine expressions; changing the query does not reselect the branch in its validity statement. Final general wrapper must combine the returned cancellation with actual hull membership. |
| FC19 | `ThresholdCircuitPreprocess.preprocessCircuits` computes and caches normalized integer cofactor weights; `preprocessCircuits_sound` and `preprocessCircuits_complete` give sound cancellations and coverage of every positive circuit with the same support. `cofactorCandidates_length` is the exact enumeration count, and `preprocessCircuits_length_exp` bounds it by `2^(4*(m+1)^2)` for packed normals. Two strengthenings are underway: every accepted candidate is itself a minimal circuit, and the full preprocessing operation ledger including determinant evaluation. The candidate count alone is not that operation bound. |
| FC20 | `ThresholdRecovery.exists_symmetric_perturbation`, `extreme_active_span`, `extreme_has_active_basis`, `bounded_polyhedron_has_basis`. Lower-dimensional and zero-dimensional polyhedra are included. The theorem needs boundedness; the application must discharge it using the explicit source box rows. |
| FC21 | `ThresholdBasisOracle.basisLibrary`, `basisLibrary_has_feasible_candidate`, `recoverFromCache_complete`, `recoverFromCache_charge`; `ThresholdRecovery.basis_selection_card`. The library is generated by finite functions, caches rational inverse matrices, ignores absent directions, and covers every bounded nonempty partial system. Its length is at most `N^m`. Final application to the grouped source profile and its boundedness remains with the recovery integrator. |
| FC22 | `ThresholdGreedy.greedyFill_spec`, `greedyFill_charge`; arbitrary dimension includes empty lists, zero capacities, zero demand, and full demand. Complete. |
| FC23 | `ThresholdStateRecovery.recoverStateFlows_spec`, `recoverStateFlows_zero_weight`; `ThresholdDecomposition.rational_chain_decomposition`, `normalizeState`. The executable normalization omits division when the weight is zero. Final composition must restore the eliminated residual profile coordinate and feed the actual recovered profile into these statements. |
| FC24 | `ThresholdGrouping.group_cost`; `ThresholdRationalRows` cached row generation; `ThresholdPackedOracle.packedOracle_arithmeticCharge`; `ThresholdGeneralPacked.generalOracle_charge`; `ThresholdBasisOracle.recoverFromCache_charge`. Row grouping uses packed keys and array access, not a copied m-vector per row. The declared charge model counts rational operations and specified indexing work, not compiled backend execution time. Preprocessing work remains the FC19 item above. |
| FC25 | `ThresholdStateRecovery.recoverStateFlows_charge` gives `L*(9*N+1)+N`; `ThresholdDecomposition.normalizationWork_bound` covers materialized normalized flows. These are actual cached outputs. The final combined original-domain check/profile recovery/state recovery bound is still an integration obligation. |
| FC26 | `ThresholdDeterminant` bounds integer minors. `ThresholdOracleSize` covers generated rows and weighted partial sums; `ThresholdRecoverySize` covers allocation and greedy residuals; `ThresholdDecomposition.normalizeState_bits` and `normalized_products_bits` cover divisions and normalized output coordinates. A general arbitrary-m inverse-basis/candidate intermediate bit bound is still missing at this review point. Determinant preprocessing operands and operation work are being added by the algorithm lane. |
| FC27 | Generic Farkas, circuit, and basis statements allow m=0, but that fact alone is not the assertion that the original sparse hull is the original flow polytope. The explicit original-domain boundary theorem belongs to root's hull integration. |
| FC28 | The general circuit, determinant, and coefficient theorems already apply to any row-signed-zero-one matrix. An explicit arbitrary-dimensional signed-subset universe and its cardinal/actual enumeration specialization is being added as `ThresholdSignedUniverse`. The existing `ThresholdUnreducedResults` establishes the separate exact low-dimensional classifications, not this arbitrary-dimensional specialization. |

## Important distinctions

`preprocessCircuits` may retain repeated representations of the same circuit
because it enumerates ordered supports and selected columns. Such duplicates
do not weaken its exact feasibility criterion or parameter bound. The exact
counts of distinct primitive circuits in FC29–FC30 require the separate
classification modules; list length here must not be cited as those counts.

The producer originally checked positivity and cancellation without an explicit
support-injectivity filter. A positive cofactor implies a nonzero deleted minor,
so its accepted entries should be provably minimal. That implication is being
formalized in `ThresholdPreprocessMinimal`; sound cancellation alone should not
be described as an already-proved minimality theorem.

The finite operation bounds apply to the declared Lean reference algorithms
and arithmetic/indexing model. They do not verify Python implementations,
compiled matrix libraries, or wall-clock behavior. A counted determinant
recurrence must be connected to the determinant implementation consumed by
preprocessing before its ledger closes the preprocessing claim.

## Targeted checks

This review directly ran the following successful commands, after correcting
local proof elaboration issues:

- `lake build Formal.NetworkSimplex.ThresholdPreprocessCriterion --wfail`
- `lake build Formal.NetworkSimplex.ThresholdGeneralCoefficients --wfail`

The constituent circuit, determinant, cone, and basis modules were separately
built with `--wfail` by their owners. Their reported results are distinct from
the two checks directly run during this review. No project-wide verification
or CI status/log inspection was performed.
