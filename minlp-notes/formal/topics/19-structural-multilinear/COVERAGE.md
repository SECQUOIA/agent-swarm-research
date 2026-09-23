# Topic 19: declaration coverage

Updated 2026-09-20 against [CLAIMS.md](CLAIMS.md) and the live sources listed
in [SOURCE-REVIEW.md](SOURCE-REVIEW.md). **All frozen mathematical obligations
S01–S03, F01–F07, Q01–Q06, C01–C05 and W01–W04 are covered by checked
declarations.** The final frequency applications and treewidth assembly
passed their targeted builds with `--wfail`. The proof chains construct their
structural inputs; they do not assume the advertised laws, decompositions,
colorings or gap bounds in place of the original graph hypotheses.

Module names below refer to `formal/Formal/MultilinearGap/`, unless a
`CubicGap/` prefix is shown. Declaration names are exact; a namespace is
included where needed to distinguish similarly named results. **Checked**
means the relevant targeted build and mathematical review are recorded in
the linked reviews or reported by the implementing agent. It does not mean
project-wide verification or CI was run.

| ID | Declaration mapping | Module(s) | Status |
|---|---|---|---|
| S01 | `feedbackIncidence`; `FrequencyTwo`, `FrequencyGraph`; `FrequencyTwo.dualGraph`, `incident_factor`; `FrequencyBipartite`, `FrequencyOddGirthAtLeast`; `StructuralTreewidth.incidenceGraph`, `RootedTreeDecomposition`, `HasTreewidthAtMost`; `structuralScopeGraph` | `StructuralFeedbackAssembly`, `StructuralFrequency`, `StructuralFrequencyDual`, `StructuralFrequencyBipartite`, `StructuralTreewidthDecomposition`, `StructuralTreewidthClasses` | Checked |
| S02 | `envelopeValues`, `HasMeans`, `minimum_from_laws`, `maximum_from_laws`; `mem_cubeGraph_hull_iff`; `weightedTermwiseGap`, `hullGap_le_weightedTermwiseGap`; `boxHullGap`, `boxTermwiseGap`; `box_gap_comparison`; `hullGap_factorSum_le` | `CubicGap/Envelope`, `CubicGap/Hull`, `GeneralGaps`, `BoxTransfer`, `PaperFoundations`, `StructuralFactorGaps` | Checked |
| S03 | `exists_boxPoint`, `boxHullGap_eq_of_mem`; `weightedTermwiseGap_eq_term_gaps`, `boxTermwiseGap_eq_term_gaps`; `hullGap_of_meanExact_split`; `factorSum`; `varyingBoxSupport`, `commonAspect_original_box_transfer` | `BoxTransfer`, `GeneralGaps`, `PaperFoundations`, `BilinearGraph`, `StructuralFactorGaps`, `StructuralCommonAspect` | Checked; representation details below |
| F01 | `feedbackUniversalLaw_hasMeans`, `feedbackUniversalLaw_dominates_pair`, `feedbackUniversalLaw_dominates_feedback` | `StructuralFeedbackUniversal` | Checked |
| F02 | `StructuralFeedback.exists_residual`, `exists_repaired_law_to_target`, `exists_local_repair`, `expect_ge_of_weight_domination` | `StructuralFeedbackRepair`, `StructuralFeedbackLocal` | Checked |
| F03 | `SeparatorGluing.glue`, `glue_expect_left`, `glue_expect_right`; `ForestGluing.exists_eliminationOrder_active`, `exists_global_feedback`; `feedback_payoff_coupling_of_order` | `StructuralFeedbackForest`, `StructuralFeedbackOrder`, `StructuralFeedbackAssembly` | Checked; the actual forest supplies the order |
| F04 | `feedback_cube_gap_bound`, `incidence_forest_gap_exact` | `StructuralFeedbackResults`, `StructuralFeedbackAssembly` | Checked |
| F05 | `feedbackBoxMajorant`, `feedbackBoxMajorant_expect`, `feedbackBoxDeficiency_nonneg`, `feedbackBoxDeficiency_attains_gap`, `feedbackBoxPolynomial_maximum`; `feedback_variable_gap_bound` | `StructuralFeedbackBoxes`, `StructuralFeedbackAssembly` | Checked for every finite nonnegative box |
| F06 | `StructuralSharpness.supportPolynomial_eq`, `termwiseGap_eq`, `polynomial_minimum`, `polynomial_maximum`, `hullGap_eq`, `ratio_tendsto`; `flower_feedback_acyclic`, `flower_empty_feedback_not_acyclic`, `flower_supports_treewidth_exactly_two`, `feedback_one_sharp` | `StructuralSharpness`, `StructuralFeedbackFlowerGraph`; supporting `StructuralTreewidthDecomposition` | Checked |
| F07 | `StructuralFeedbackPayoffSharpness.local_optimum`, `sum_local_optima`, `sum_expectations`, `residual_incidence_acyclic`, `retention_le`; `privateScope_injective`, `private_local_optimum`, `private_sum_expectations`, `private_residual_incidence_acyclic`, `private_retention_le` | `StructuralFeedbackPayoffSharpness` | Checked, including distinct private scopes and `f=0` |
| Q01 | `FrequencyTwo.dualGraph`, `incident_factor`, `incident_dummy_card_le_one`, `sum_dualWeight`; `FrequencyTwo.iff_subtype` | `StructuralFrequencyDual`, `StructuralFrequencySupport` | Checked |
| Q02 | `failureBaseline_eq_anchor`, `monomial_gap_eq_failureCap_sub_baseline`, `weightedTermwiseGap_failure`, `hullGap_isGreatest_shiftedCoverage` | `StructuralFrequency` | Checked; baseline retained |
| Q03 | `FrequencySlab.slab_compact`, `mem_floor_ceil_slab`, `extreme_kernel_eq_zero`, `extreme_fractional_degree_two`, `extreme_fractional_eq_half`, `exists_extreme_law`; `fractionalGraph_isCycles`, `extreme_indexed_cycle_odd`, `exists_indexed_cycle_family`, `exists_frequencyCycleLayout`; `exists_frequency_slab_layouts` | `StructuralFrequencySlab`, `StructuralFrequencyComponents`, `StructuralFrequencyOddCycle`, `StructuralFrequencyLayout`, `StructuralFrequencyLayoutAssembly`, `StructuralFrequencyTheorem` | Checked |
| Q04 | `StructuralFrequencyCycle.roundingLaw_mean`, `roundingLaw_coverage`, `roundingLaw_incidentCount`; `FrequencyCycleLayout.law_hasMeans`, `countOn_row`, `law_cardinality_row`, `law_cardinality_outside` | `StructuralFrequencyCycle`, `StructuralFrequencyRounding`; product-law support in `StructuralFrequencyProduct` | Checked, including integral selected coordinates |
| Q05 | `FrequencySlab.expect_cap`; `failureBaseline_le_expect`; `frequencyTwo_monomial_three_halves`, `frequencyTwo_monomial_oddGirth`, `frequencyTwo_monomial_bipartite`; actual-layout cardinality theorem chain listed under C03 | `StructuralFrequencySlab`, `StructuralFrequency`, `StructuralFrequencyTheorem`, `StructuralFrequencyApplications` | Checked |
| Q06 | `StructuralFrequencyCycle.polynomial_termwiseGap`, `polynomial_hullGap`, `polynomial_ratio`, `triangle_ratio`, `supports_oddGirth`, `supports_cycle_attained`; `boxHullGap_zeroLower`, `boxTermwiseGap_zeroLower`; `frequencyTwo_zeroLower_three_halves`, `frequencyTwo_zeroLower_oddGirth`, `frequencyTwo_zeroLower_bipartite` | `StructuralFrequencySharpness`, `StructuralFrequencyCycleGirth`, `StructuralFrequencyBox`, `StructuralFrequencyApplications` | Checked |
| C01 | `ConvexCountTable`, `cardinalityLower`, `cardinalityLower_le_expect`, `exists_cardinalityLower_law`, `cardinality_minimum`; `vertexInterpolation`, `cardinalityFactor_separatelyAffine`, `cardinalityFactor_vertex`, `cardinalityFactor_minimum` | `StructuralCardinality`, `StructuralInterpolation` | Checked |
| C02 | `convex_cardinality_common_upper`, `cardinality_maximum`, `convex_cardinality_sum_common_upper` | `StructuralCardinalityUpper` | Checked by finite support induction, with a common attaining law |
| C03 | `cardinalityLower_two_halves`, `thresholdLaw_cardinality_two_halves`; `FrequencyCycleLayout.hullGap_row`, `law_cardinality_loss`; `cardinalityLower_average`, `upperEnvelope_average_le`, `cardinalityGaps_average_le`, `cardinality_gap_of_slab_rounding`; `frequencyTwo_cardinality_three_halves`, `frequencyTwo_cardinality_oddGirth`, `frequencyTwo_cardinality_bipartite` | `StructuralFrequencyLocal`, `StructuralFrequencyRounding`, `StructuralAveraging`, `StructuralFrequencyTheorem` | Checked |
| C04 | `monomial_commonAspect_varying_vertex`, `commonAspectSequence_convexCountTable`, `commonAspect_original_box_transfer`; `frequency_le_two_varyingBoxSupport`, `FrequencyOddGirthAtLeast.varyingBoxSupport`, `FrequencyBipartite.varyingBoxSupport`; `frequencyTwo_commonAspect_three_halves`, `frequencyTwo_commonAspect_oddGirth`, `frequencyTwo_commonAspect_bipartite` | `StructuralCommonAspect`, `StructuralFrequencySupport`, `StructuralFrequencyApplications` | Checked |
| C05 | `StructuralFrequencyCycle.positiveBox_hullGap`, `positiveBox_termwiseGap`, `positiveBox_ratio` | `StructuralFrequencySharpnessBox`, using `BilinearGraph` | Checked for every fixed `rho>1` |
| W01 | `StructuralTreewidth.exists_good_of_treewidth_two`, `incidence_exists_good_two_coloring` | `StructuralTreewidthColoring`, `StructuralTreewidthIncidenceColoring`, with elimination, network, composition and articulation modules | Checked from an actual tree decomposition |
| W02 | `ColumnSigning.totallyUnimodular`; `CycleTU.totallyUnimodular_of_even_cycles`, `totallyUnimodular_of_even_factor_cycles`; `colorClassMatrix_totallyUnimodular` | `StructuralCamion`, `StructuralCycleTU`, `StructuralTreewidthClasses` | Checked |
| W03 | `TUSlab.exists_adjacent_scopeLaw`, `exists_cardinality_scopeLaw`; `factorSum_two_law_bound`, `cardinality_two_TU_classes_bound`; `treewidthTwo_cardinality_bound`, `treewidthTwo_monomial_bound`, `treewidthTwo_zeroLower_bound`, `treewidthTwo_commonAspect_bound`, `structuralScopeGraph_treewidth_mono`, `structuralScopeGraph_treewidth_of_incidence` | `StructuralCardinalityTU`, `StructuralFactorGaps`, `StructuralTwoClasses`, `StructuralTreewidthClasses` | Checked |
| W04 | `StructuralPositiveFlower.physical_supportPolynomial`, `physical_termwiseGap`, `physical_payoff_maximum`, `hullGap_upper`, `hullGap_lower`, `physical_hullGap_tendsto`, `physical_hullGap_eventually_pos`, `physical_ratio_tendsto`; `scaled_hullGap`, `scaled_termwiseGap`, `scaled_ratio_tendsto`, `scaled_universal_constant_ge_two`; `treewidthTwo_flower_membership` connects the same F06 supports to the final bound | `StructuralPositiveFlower`, `StructuralFeedbackFlowerGraph`, `StructuralTreewidthClasses` | Checked physical calculation and original scopes |

The extreme-point proof uses tight-row kernel injectivity and incidence
counting before constructing fractional components. Private and unused
coordinates cannot be fractional at an extreme point. Parallel fractional
edges are excluded by a proved kernel contradiction, before the component
proof uses a simple graph. Each remaining component is an actual odd cycle;
its indexed layout covers every fractional coordinate and has disjoint rows.
The final frequency theorem constructs these layouts from the supplied
frequency hypothesis.

The treewidth proof constructs the coloring from the bag-size definition of
treewidth using elimination, edge-network expansion, series/parallel
composition and articulation gluing. The TU bridge uses a proved signing
criterion and cycle parity. It does not assume Camion's theorem or treat
balancedness alone as arbitrary-right-hand-side integrality. The two class
laws are then constructed through TU slab integrality, preserving every
singleton mean and attaining all lower envelopes in their own class.

The monomial interfaces represent distinct supports by `Finset (Finset I)`
and one nonnegative coefficient per support. Repeated identical positive
monomials can be combined by adding their coefficients: both their polynomial
value and their summed individual gap are unchanged by positive scaling.
An indexed cardinality or physical-factor interface retains its original
factor labels, including equal scopes. Removing fixed coordinates restricts
scopes without merging those labels. Every structural assumption refers to
the represented original family, not a globally expanded polynomial.

The gap theorems are inequalities or equalities without division, so zero
gaps remain valid. Constants and affine terms have mean-exact values and
zero width. Empty supports, empty families, unused variables, tied or boundary
means, zero coefficients and degenerate coordinate boxes are covered by the
finite-law and box-surjection interfaces. Signed or decreasing convex count
tables are allowed; only their successive differences must be nondecreasing.
Every cardinality factor means its multiaffine vertex interpolant, not the
usually different function obtained by applying the table's continuous
extension to the mean count. The sharpness ratios use proved positive gaps;
the flower's denominator is positive eventually and its ratio tends to two.

The exact unequal-aspect obstruction is separately checked by
`PositiveBoxObstruction.original_box_gaps`, `original_box_ratio`,
`positive_box_data`, `support_frequency_two` and `factor_two_coloring` in
`StructuralFrequencyBox`. For `xy+xyz` on `[1,2] x [1,2] x [1,3]` at
`(5/4,5/4,5/2)`, it proves `T=7/4`, `H=3/2` and ratio `7/6`. This refutes
unrestricted positive-box bipartite equality. A general unequal-positive-box
frequency-two bound remains unresolved in the sources.

Review and targeted-check evidence is retained in
[feedback-final](reviews/feedback-final.md),
[feedback-sharpness](reviews/feedback-sharpness.md),
[cardinality](reviews/cardinality.md),
[frequency](reviews/frequency.md),
[sharpness and boxes](reviews/sharpness-boxes.md),
[aggregation](reviews/aggregation.md),
[TU integrality](reviews/tu-integrality.md),
[TU criterion](reviews/tu-criterion.md),
[cycle parity](reviews/cycle-parity.md),
[treewidth coloring](reviews/treewidth-coloring.md),
[final treewidth classes](reviews/treewidth-classes.md) and
[positive flower](reviews/positive-flower.md).
Those reports name their reviewed source versions and actual targeted
commands. Earlier reports' open integration observations are superseded only
by the completed declarations listed above. No project-wide local check or
CI status inspection is claimed here.

The following remain outside topic 19's frozen gap scope: polynomial-time
matching/edge-cover optimization, envelope separation and rational
bit-complexity claims; the width-three and parity-factor investigations;
canonical-pair and twin-compression reductions; the separate signed-factor
forest extension; novelty, priority and external peer review. The generic
cell-indicator example proves loss `2^f` is sharp for nonnegative local
payoffs. It does not prove positive-monomial sharpness for arbitrary f.
Constant two is a supremum for the flower family, not finite-family
attainment. No adjacent topic is included by this coverage map.
