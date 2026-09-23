import Formal
import Lean.Util.CollectAxioms

/-! Audit every declaration owned by a project module, including private
definitions and auxiliary declarations. Fail on any nonstandard dependency.
Module ownership avoids silently omitting a newly added topic namespace. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => (`Formal).isPrefixOf mod.module
    return if owned then names.push name else names
  if names.isEmpty then
    throwError "No project declarations were found; the audit would be empty."
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    let axioms ← Lean.collectAxioms name
    for axiomName in axioms do
      unless allowed.contains axiomName do
        throwError "{name} depends on disallowed axiom {axiomName}"
  logInfo m!"PASS: audited {names.size} project declarations; \
    only propext, Classical.choice, Quot.sound are allowed."

#print axioms ExactCounts.exact_box_counts
#print axioms ExactCounts.strict_count_separation
#print axioms ExactCounts.closed_integer_exact_count
#print axioms ExactCounts.closed_binary_exact_count
#print axioms ExactCounts.monotone_exact_box_counts
#print axioms ExactCounts.integerRows_strict_sound
#print axioms ExactCounts.integerRows_data_subset
#print axioms ExactCounts.count_gap_linear_bounds
#print axioms ExactCounts.weightedBoxes_iff_mem_convexHull
#print axioms ExactCounts.binarySystem_exact_slice
#print axioms ExactCounts.binarySystem_exact_integer_slice
#print axioms MultilinearGap.unbounded_gap_ratio
#print axioms MultilinearGap.no_uniform_positive_multilinear_bound
#print axioms MultilinearGap.hullGap_exact
#print axioms MultilinearGap.exists_hullGap_exact
#print axioms MultilinearGap.sharp_cube_gap_bound
#print axioms MultilinearGap.degree_gap_bound_on_box
#print axioms MultilinearGap.sharp_positive_growth
#check ExactCounts.exact_box_counts
#check ExactCounts.leftValue_convex
#check ExactCounts.rightValue_convex
#check ExactCounts.leftPoly_natDegree
#check ExactCounts.rightPoly_natDegree
#print axioms MultilinearGap.monomial_minimum
#print axioms MultilinearGap.box_convex_envelope
#print axioms MultilinearGap.box_concave_envelope
#print axioms MultilinearGap.box_gap_comparison
#print axioms MultilinearGap.boxTermwiseGap_eq_term_gaps
#print axioms MultilinearGap.supports_card
#print axioms MultilinearGap.supports_max_degree
#print axioms MultilinearGap.supports_occurrences
#print axioms MultilinearGap.supports_occurrences_isBigO
#print axioms MultilinearGap.tendsto_exact_family_ratio_normalized
#print axioms MultilinearGap.example_sixty_four
#print axioms CubicGap.cubicRoundingLaw_hasMeans
#print axioms CubicGap.cubicRoundingLaw_support_deficiency
#print axioms CubicGap.cubic_box_gap_bound
#print axioms CubicGap.RoundingOptimality.fixed_mixture_optimal_bound
#print axioms CubicGap.RoundingOptimality.fixed_mixture_optimal_weights_unique
#print axioms CubicGap.analytic_binary_expansion
#print axioms CubicGap.analytic_scaled_minimum_lower
#print axioms CubicGap.analytic_finite_ratio_lower
#print axioms CubicGap.analytic_integer_family_witness
#print axioms CubicGap.cubic_boxDegreeSupremum_sandwich
#print axioms CubicGap.RoundingOptimality.optimal_mixture_guarantee
#print axioms CubicGap.analytic_integer_support_witness
#print axioms CubicGap.RoundingOptimality.fixed_mixture_optimum
#print axioms MultilinearGap.floor_finite_bound
#print axioms MultilinearGap.sharp_marginal_floor_growth
#print axioms MultilinearGap.marginal_floor_original_box_bound
#print axioms MultilinearGap.hullGap_isGreatest_weightedAnchorDeficiency
#print axioms PotentialFlow.Network.mem_interval_of_edgeBregman
#print axioms PotentialFlow.Network.exists_loads_iff
#print axioms PotentialFlow.RationalNetwork.mem_bisection_interval
#print axioms PotentialFlow.Scenario.scenario_error_sq
#print axioms PotentialFlow.Scenario.exact_of_compatible
#print axioms PotentialFlow.Network.supportBound_sound
#print axioms PotentialFlow.RationalNetwork.exists_max_isGLB_ratSupportBound
#print axioms PotentialFlow.Network.supportSet_cubic_bound
#print axioms PotentialFlow.Network.abs_sum_goal_le
#print axioms PotentialFlow.Network.exists_zeroAdmissible_iff
#print axioms PotentialFlow.Network.optimalFactor_iff_exists_kktCirculation
#print axioms PotentialFlow.Network.isGreatest_goalError
#print axioms PotentialFlow.RationalNetwork.exists_rational_optimalFactor
#print axioms PotentialFlow.dyadicRootUpper_excess
#print axioms PotentialFlow.TwoPath.exists_unique_physical
#print axioms PotentialFlow.TwoPath.certified_gap_eq
#print axioms PotentialFlow.TwoPath.isGreatest_supportGoal
#print axioms PotentialFlow.TwoPath.supportBound_upper_eq
#print axioms PotentialFlow.TwoPath.tendsto_bregmanWidth
#print axioms PotentialFlow.TwoPath.tendsto_laplacianWidth
#print axioms PotentialFlow.TwoPath.supportSet_violates_edgeBregman
#print axioms PotentialFlow.RationalNetwork.goalAccepted_sound
#print axioms PotentialFlow.CertExample.worked_example_verified
#print axioms PotentialFlow.Network.schurKkt_iff
#print axioms PotentialFlow.Network.optimalFactor_iff_exists_schurKkt
#print axioms PotentialFlow.Network.exists_isLeast_factor
#print axioms PotentialFlow.upperBracket_boundary_unique
#print axioms PotentialFlow.TwoPath.edgeBregman_aPos
#print axioms PotentialFlow.TwoPath.optimalFactor_hEdge
#print axioms PotentialFlow.TwoPath.sum_drops_path
#print axioms PotentialFlow.TwoPath.exists_integral_dualLower
