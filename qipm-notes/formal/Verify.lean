import QipmFormal
import Lean.Util.CollectAxioms

/-!
Axiom audit. Every declaration in an imported QipmFormal module must depend
only on `propext`, `Classical.choice`, and `Quot.sound`. The command at the
end enforces this allowlist and rejects project axiom declarations, including
unused ones. The headline dependency lists below are for human inspection.
-/

open QipmFormal.ScalarCert

#print axioms hasSum_artanh
#print axioms hasSum_Y
#print axioms term_nonneg
#print axioms partial_le_Y
#print axioms Y_le_partial_add_tail
#print axioms P_sq
#print axioms P_strictMonoOn
#print axioms Y_strictMonoOn
#print axioms P_Pinv
#print axioms P_W
#print axioms Y_pos
#print axioms A_pos
#print axioms le_A
#print axioms A_le
#print axioms P_le
#print axioms ratio_gt_of_witness
#print axioms lt_cstar_of_ratio

-- Topic 1A: the strict lower certificate
#print axioms accLo_v0
#print axioms accHi_v0
#print axioms accLo_w0
#print axioms pow_v0_nat
#print axioms Y_v0_gt
#print axioms Y_v0_lt
#print axioms Y_w0_gt
#print axioms A_v0_gt
#print axioms A_w0_lt
#print axioms margin_one
#print axioms margin_two
#print axioms a0_lt_ratio_v0
#print axioms exists_ratio_gt
#print axioms a0_lt_cstar

-- Bridge to the original x coordinate
#print axioms A_vOf
#print axioms P_vOf
#print axioms P_vOf_eq_bb_deriv
#print axioms bb_hasDerivAt

-- Elasticity foundations and the E > 2 threshold
#print axioms Y_deriv
#print axioms lt_Y
#print axioms Y_lt_B
#print axioms K_pos_lt_one
#print axioms one_lt_E
#print axioms hasSum_E
#print axioms E_strictMonoOn
#print axioms E_v2_le_two
#print axioms lt_of_two_lt_E

-- Topic 1B: the upper certificate, and the two-sided conclusion
#print axioms K_lt
#print axioms g_one_strictMonoOn
#print axioms E_comparison
#print axioms Phi_pos
#print axioms log_69_50_ge
#print axioms log_50_19_le
#print axioms log_two_le
#print axioms log_3449_2500_ge
#print axioms log_2500_949_le
#print axioms key_ineq
#print axioms ratio_lt_strict
#print axioms ratio_lt
#print axioms bddAbove_ratio
#print axioms cstar_lt
#print axioms cstar_bounds

-- Topic 1D: the bridge
#print axioms Y_vOf_eq_rho
#print axioms rho_hasDerivAt
#print axioms scalar_elementary

-- Maximizer localization
#print axioms log_a0_ge
#print axioms log_571_250_le
#print axioms log_773_250_le
#print axioms E_mem_window
#print axioms maximizer_localization
#print axioms x_localization
#print axioms cstar_maximizer_location

-- Surjectivity of Y (completeness of the v-parametrisation)
#print axioms artanh_le_Y
#print axioms Y_le_two_artanh
#print axioms Y_surjOn
#print axioms xOf_vOf

-- Attainment and the manuscript's original variational definition
#print axioms ratio_continuousOn
#print axioms cstar_attained
#print axioms cstar_location_of_eq
#print axioms Paper.rho_rhoInv
#print axioms Paper.rhoInv_rho
#print axioms Paper.p_Y
#print axioms Paper.p_hasDerivAt
#print axioms Paper.deriv_p_Y
#print axioms Paper.p_pInv
#print axioms Paper.pInv_p
#print axioms Paper.ratio_image
#print axioms Paper.cstar_eq
#print axioms Paper.cstar_bounds
#print axioms Paper.cstar_attained
#print axioms Paper.cstar_isGreatest

-- QCPM: the actual potential, clock, schedule, and manuscript bounds.
#print axioms QipmFormal.QCPM.potential_at_initial
#print axioms QipmFormal.QCPM.initial_value_le_sup_of_compact
#print axioms QipmFormal.QCPM.no_uniform_quadratic_bound
#print axioms QipmFormal.QCPM.shifted_potential_sup_lower
#print axioms QipmFormal.QCPM.potential_sup_le_boxCertificate
#print axioms QipmFormal.QCPM.correctedClock_strictMonoOn
#print axioms QipmFormal.QCPM.correctedTime_continuousOn
#print axioms QipmFormal.QCPM.correctedEnvelope_integral
#print axioms QipmFormal.QCPM.productClock_derivative_ne
#print axioms QipmFormal.QCPM.normalizer_pos
#print axioms QipmFormal.QCPM.schedule_terminal_le_quarter
#print axioms QipmFormal.QCPM.normIntegral_log_window_lower
#print axioms QipmFormal.QCPM.normIntegral_speed_lower
#print axioms QipmFormal.QCPM.speed_bound_of_derivative
#print axioms QipmFormal.QCPM.paperNorm_schedule_lower
#print axioms QipmFormal.QCPM.paperNorm_speed_lower
#print axioms QipmFormal.QCPM.paperNorm_derivative_speed_lower
#print axioms QipmFormal.QCPM.paperNorm_schedule_box_upper
#print axioms QipmFormal.QCPM.clockNorm_eq_paperNorm
#print axioms QipmFormal.QCPM.clockNorm_schedule_lower
#print axioms QipmFormal.QCPM.clockNorm_derivative_speed_lower
#print axioms QipmFormal.QCPM.clockNorm_schedule_box_upper

-- Sparse convex mixtures: raw matrices, output contracts, and centrality.
#print axioms QipmFormal.Mixture.euclideanNorm_eq_norm_toLp
#print axioms QipmFormal.Mixture.oneBitMatrix_update_locality
#print axioms QipmFormal.Mixture.rhsMatrix_locality
#print axioms QipmFormal.Mixture.slack_conversion
#print axioms QipmFormal.Mixture.weighted_residual_bound
#print axioms QipmFormal.Mixture.uniform_residual_bound
#print axioms QipmFormal.Mixture.sensitive_residual_bound
#print axioms QipmFormal.Mixture.zero_incidence_feasible
#print axioms QipmFormal.Mixture.multibit_residual_bound
#print axioms QipmFormal.Mixture.multibit_row_union_bound
#print axioms QipmFormal.Mixture.harmonicWeight_minimizes
#print axioms QipmFormal.Mixture.harmonic_residual_bound
#print axioms QipmFormal.Mixture.uniform_affine_soundness_product
#print axioms QipmFormal.Mixture.harmonic_affine_soundness_product
#print axioms QipmFormal.Mixture.weighted_pair_soundness_frontier
#print axioms QipmFormal.Mixture.single_flip_affine_wrong
#print axioms QipmFormal.Mixture.mixture_pair_decoder_bound
#print axioms QipmFormal.Mixture.pair_probability_fair_outside
#print axioms QipmFormal.Mixture.kktMatrix_sqNorm
#print axioms QipmFormal.Mixture.kktDependent_incidence
#print axioms QipmFormal.Mixture.weighted_kkt_bound
#print axioms QipmFormal.Mixture.weighted_kkt_paper_bound
#print axioms QipmFormal.Mixture.central_mixture_objective_gap
#print axioms QipmFormal.Mixture.weighted_multiplicative_variance
#print axioms QipmFormal.Mixture.multiplicativeDefect_eq_zero_iff
#print axioms QipmFormal.Mixture.kantorovich_extrema_ratio_bound
#print axioms QipmFormal.Mixture.extrema_ratio_iff_pairwise
#print axioms QipmFormal.Mixture.point_centered_width_identity
#print axioms QipmFormal.Mixture.central_affine_soundness_dichotomy
#print axioms QipmFormal.Mixture.central_pair_soundness_dichotomy
#print axioms QipmFormal.Mixture.point_centered_affine_soundness_dichotomy
#print axioms QipmFormal.Mixture.central_uniform_soundness_dichotomy
#print axioms QipmFormal.Mixture.Counterexample.neighbor_central
#print axioms QipmFormal.Mixture.Counterexample.small_parameter_product_bounds
#print axioms QipmFormal.Mixture.Counterexample.inverse_square_defect
#print axioms QipmFormal.Mixture.Counterexample.point_centered_width_zero
#print axioms QipmFormal.Mixture.Counterexample.padded_quantitative_failure

-- SDP mixtures: actual matrix order, norms, coordinates, and output contracts.
#print axioms QipmFormal.SDPMixture.matrixMix_posDef
#print axioms QipmFormal.SDPMixture.normalized_variance_identity
#print axioms QipmFormal.SDPMixture.centralMatrix_eq_one_iff
#print axioms QipmFormal.SDPMixture.centralMatrix_sandwich
#print axioms QipmFormal.SDPMixture.endpoint_mixture_forces_constant
#print axioms QipmFormal.SDPMixture.centralMatrix_operator_variance_bound
#print axioms QipmFormal.SDPMixture.centralMatrix_frobenius_variance_bound
#print axioms QipmFormal.SDPMixture.opNorm_recentered_le
#print axioms QipmFormal.SDPMixture.frobeniusNorm_recentered_le
#print axioms QipmFormal.SDPMixture.sdpDefect_mixture_point
#print axioms QipmFormal.SDPMixture.complementarity_discrepancy_bounds
#print axioms QipmFormal.SDPMixture.pointParameter_mixture_bounds
#print axioms QipmFormal.SDPMixture.dot_svec
#print axioms QipmFormal.SDPMixture.svec_reconstruct
#print axioms QipmFormal.SDPMixture.measurement_adjoint_identity
#print axioms QipmFormal.SDPMixture.sdp_mixture_objective_gap
#print axioms QipmFormal.SDPMixture.sdp_weighted_kkt_bound
#print axioms QipmFormal.SDPMixture.sdp_uniform_kkt_paper_bound
#print axioms QipmFormal.SDPMixture.sdp_multibit_kkt_bound
#print axioms QipmFormal.SDPMixture.plusEffect_posSemidef
#print axioms QipmFormal.SDPMixture.binary_effects_sum
#print axioms QipmFormal.SDPMixture.plusProbability_eq_measurement
#print axioms QipmFormal.SDPMixture.observable_normalized_margin_mix
#print axioms QipmFormal.SDPMixture.matrixTripleScore_wrong_mix
#print axioms QipmFormal.SDPMixture.operator_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.frobenius_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.common_parameter_ratio_iff
#print axioms QipmFormal.SDPMixture.log_ratio_le_of_common_parameter_bound
#print axioms QipmFormal.SDPMixture.endpoint_mixture_frobenius_sharp
#print axioms QipmFormal.SDPMixture.endpoint_mixture_sdpDefect_point_zero
#print axioms QipmFormal.SDPMixture.scalar_one_nine_operator_defect
#print axioms QipmFormal.SDPMixture.centralMatrix_trace_variance_bound
#print axioms QipmFormal.SDPMixture.complementarity_discrepancy_variance_bound
#print axioms QipmFormal.SDPMixture.finrank_symmetricMatrix
#print axioms QipmFormal.SDPMixture.weighted_operator_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.uniform_operator_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.weighted_frobenius_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.uniform_frobenius_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.observable_operator_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.affine_frobenius_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.operator_variance_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.frobenius_variance_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.uniform_sharp_operator_soundness_dichotomy
#print axioms QipmFormal.SDPMixture.uniform_sharp_frobenius_soundness_dichotomy

-- Residual-certified refresh: actual systems, exact tests, and sequential policy.
#print axioms QipmFormal.Refresh.solution_equation
#print axioms QipmFormal.Refresh.solutionNorm_pos
#print axioms QipmFormal.Refresh.normalizedInverse_apply_operator
#print axioms QipmFormal.Refresh.normalizedOperator_apply_inverse
#print axioms QipmFormal.Refresh.norm_ray
#print axioms QipmFormal.Refresh.normalizedOperator_ray
#print axioms QipmFormal.Refresh.normalized_residual
#print axioms QipmFormal.Refresh.candidate_residual_bound_on
#print axioms QipmFormal.Refresh.scalarLeastSquares_sq_identity
#print axioms QipmFormal.Refresh.scalarLeastSquares_minimizes
#print axioms QipmFormal.Refresh.reuseCost_bound
#print axioms QipmFormal.Refresh.failed_test_charge_strict
#print axioms QipmFormal.Refresh.failed_intervals_disjoint
#print axioms QipmFormal.Refresh.refresh_budget
#print axioms QipmFormal.Refresh.refresh_count_bound
#print axioms QipmFormal.Refresh.cache_unchanged_at_threshold
#print axioms QipmFormal.Refresh.refresh_count_eq_one_of_zero_variation
#print axioms QipmFormal.Refresh.paper_refresh_bound
#print axioms QipmFormal.Refresh.Counterexample.safe_acceptance_only_counterexample

-- Exact-center coupling: actual LP equations, block inverses, and filtering laws.
#print axioms QipmFormal.Coupling.normalMatrix_split
#print axioms QipmFormal.Coupling.exact_center_newton_rhs
#print axioms QipmFormal.Coupling.supported_rhs_mem_active_range
#print axioms QipmFormal.Coupling.rhs_ne_zero_of_strict_dual
#print axioms QipmFormal.Coupling.BlockFamily.xi_smul
#print axioms QipmFormal.Coupling.BlockFamily.rho_smul
#print axioms QipmFormal.Coupling.blockOperator_bijective
#print axioms QipmFormal.Coupling.positive_blocks_have_factors
#print axioms QipmFormal.Coupling.first_inverse
#print axioms QipmFormal.Coupling.second_inverse
#print axioms QipmFormal.Coupling.couplingQ_ne_zero
#print axioms QipmFormal.Coupling.couplingG_eq_zero_iff
#print axioms QipmFormal.Coupling.couplingG_all_eq_zero_iff
#print axioms QipmFormal.Coupling.secondInverse_bounds
#print axioms QipmFormal.Coupling.BlockFamily.xi_tight
#print axioms QipmFormal.Coupling.BlockFamily.rho_tight
#print axioms QipmFormal.Coupling.BlockFamily.rho_nontight
#print axioms QipmFormal.Coupling.BlockFamily.rho_bounded_iff
#print axioms QipmFormal.Coupling.BlockFamily.rho_full_scale
#print axioms QipmFormal.Coupling.BlockFamily.rho_improves_iff
#print axioms QipmFormal.Coupling.BlockFamily.uniformBounds_of_block_continuity
#print axioms QipmFormal.Coupling.BlockFamily.exact_center_continuous_law
#print axioms QipmFormal.Coupling.BlockFamily.analytic_schurFactor
#print axioms QipmFormal.Coupling.BlockFamily.analytic_coupling
#print axioms QipmFormal.Coupling.BlockFamily.rho_firstOrder_bound
#print axioms QipmFormal.Coupling.BlockFamily.rho_analytic_zero_cases
#print axioms QipmFormal.Coupling.newton_norm_theta
#print axioms QipmFormal.Coupling.newton_condition_theta
#print axioms QipmFormal.Coupling.normTight_theta_inv
#print axioms QipmFormal.Coupling.BlockFamily.endpoint_coupling_formula
#print axioms QipmFormal.Coupling.BlockFamily.rho_bounded_iff_deriv_zero
#print axioms QipmFormal.Coupling.OrthogonalRealization.realizeFamily_valid
#print axioms QipmFormal.Coupling.OrthogonalRealization.realized_firstInverseNorm
#print axioms QipmFormal.Coupling.OrthogonalRealization.realized_secondInverseNorm
#print axioms QipmFormal.Coupling.OrthogonalRealization.realized_xi
#print axioms QipmFormal.Coupling.OrthogonalRealization.realized_rho
#print axioms QipmFormal.Coupling.OrthogonalRealization.normal_positive_factors
#print axioms QipmFormal.Coupling.Witnesses.coupled_dual_feasible
#print axioms QipmFormal.Coupling.Witnesses.coupled_unique_optimum
#print axioms QipmFormal.Coupling.Witnesses.decoupled_unique_optimum
#print axioms QipmFormal.Coupling.Witnesses.coupled_dual_optimal_interval
#print axioms QipmFormal.Coupling.Witnesses.decoupled_dual_optimal_interval
#print axioms QipmFormal.Coupling.Witnesses.coupled_normalized_direction
#print axioms QipmFormal.Coupling.Witnesses.paperT_parameter
#print axioms QipmFormal.Coupling.Witnesses.paperT_quadratic_error
#print axioms QipmFormal.Coupling.Witnesses.coupled_second_limit_mu
#print axioms QipmFormal.Coupling.Witnesses.coupled_slack_limit_mu
#print axioms QipmFormal.Coupling.Witnesses.coupled_dual_limit_mu
#print axioms QipmFormal.Coupling.Witnesses.coupled_operatorNorm
#print axioms QipmFormal.Coupling.Witnesses.coupled_parameter_limits
#print axioms QipmFormal.Coupling.Witnesses.decoupled_parameters
#print axioms QipmFormal.Coupling.Witnesses.slowSolutionAmplitude_limit

-- Select by defining module, so private declarations and declarations outside
-- the QipmFormal namespace are also audited.
-- Fractional SDP: actual central points, Frobenius Hessians, complete spectra,
-- and asymptotics over every sufficiently small gap and central parameter.
#print axioms QipmFormal.FractionalSDP.zero_objective_iff_optimum
#print axioms QipmFormal.FractionalSDP.center_unique_minimizer_matrix
#print axioms QipmFormal.FractionalSDP.center_unique_minimizer_restricted
#print axioms QipmFormal.FractionalSDP.center_positive_root
#print axioms QipmFormal.FractionalSDP.muParameter_tendsto
#print axioms QipmFormal.FractionalSDP.gapParameter_tendsto
#print axioms QipmFormal.FractionalSDP.reducedOperator_iteratedFDeriv
#print axioms QipmFormal.FractionalSDP.restrictedOperator_iteratedFDeriv
#print axioms QipmFormal.FractionalSDP.reduced_charpoly
#print axioms QipmFormal.FractionalSDP.tangent_eigenvalue_iff
#print axioms QipmFormal.FractionalSDP.restricted_tangent_eigenvalue_iff
#print axioms QipmFormal.FractionalSDP.centralPoint_unique_minimizer
#print axioms QipmFormal.FractionalSDP.gapCenter_unique_minimizer
#print axioms QipmFormal.FractionalSDP.centralPoint_spectrum
#print axioms QipmFormal.FractionalSDP.centralEigenvalues_ordered
#print axioms QipmFormal.FractionalSDP.centralEigenvalues_positive
#print axioms QipmFormal.FractionalSDP.paper_first_eigenvalue
#print axioms QipmFormal.FractionalSDP.paper_second_eigenvalue
#print axioms QipmFormal.FractionalSDP.paper_third_eigenvalue
#print axioms QipmFormal.FractionalSDP.paper_fourth_eigenvalue
#print axioms QipmFormal.FractionalSDP.paper_mu_spectralCondition
#print axioms QipmFormal.FractionalSDP.paper_gap_spectralCondition
#print axioms QipmFormal.FractionalSDP.paper_mu_restrictedSpectralCondition
#print axioms QipmFormal.FractionalSDP.paper_gap_restrictedSpectralCondition

-- Fixed preconditioners: actual path matrices, spectral conditions, and sharp order.
#print axioms QipmFormal.Preconditioner.pathMatrix_quadratic
#print axioms QipmFormal.Preconditioner.pathMatrix_posDef
#print axioms QipmFormal.Preconditioner.pathRamp_energy
#print axioms QipmFormal.Preconditioner.alternating_pathRamp_energy
#print axioms QipmFormal.Preconditioner.alternating_pathMatrix
#print axioms QipmFormal.Preconditioner.signedPathMatrix_switching
#print axioms QipmFormal.Preconditioner.path_norm_le
#print axioms QipmFormal.Preconditioner.path_energy_le
#print axioms QipmFormal.Preconditioner.energy_bounds
#print axioms QipmFormal.Preconditioner.spectralCondition_le_of_bounds
#print axioms QipmFormal.Preconditioner.congruence_paired_minimax
#print axioms QipmFormal.Preconditioner.spectralCondition_orthogonal_congruence
#print axioms QipmFormal.Preconditioner.inverseSqrt_posSemidef
#print axioms QipmFormal.Preconditioner.inverseSqrt_sq
#print axioms QipmFormal.Preconditioner.inverseSqrt_whitens
#print axioms QipmFormal.Preconditioner.simultaneous_preconditioning
#print axioms QipmFormal.Preconditioner.generalized_condition_ge_sq
#print axioms QipmFormal.Preconditioner.path_relative_condition_lower
#print axioms QipmFormal.Preconditioner.path_congruence_minimax
#print axioms QipmFormal.Preconditioner.path_spd_minimax
#print axioms QipmFormal.Preconditioner.path_spd_original_bound
#print axioms QipmFormal.Preconditioner.path_condition_bounds
#print axioms QipmFormal.Preconditioner.edgePath_condition_eq
#print axioms QipmFormal.Preconditioner.all_signed_paths_identity_bound

open Lean in
run_cmd do
  let env ← Lean.getEnv
  -- `moduleNames` maps the whole import array; compute it once for this scan.
  let moduleNames := env.header.moduleNames
  let allowed : Array Lean.Name := #[``propext, ``Classical.choice, ``Quot.sound]
  let mut checked : Nat := 0
  for (name, info) in env.constants do
    let some idx := env.getModuleIdxFor? name | continue
    let moduleName := moduleNames[idx.toNat]!
    unless (`QipmFormal).isPrefixOf moduleName do continue
    if let .axiomInfo _ := info then
      throwError "Project axiom declaration is forbidden: {name}"
    let axioms ← Lean.collectAxioms name
    let forbidden := axioms.filter fun ax => !allowed.contains ax
    unless forbidden.isEmpty do
      throwError "{name} depends on forbidden axioms: {forbidden}"
    checked := checked + 1
  if checked == 0 then
    throwError "Axiom audit found no project declarations"
  logInfo m!"Axiom allowlist passed for {checked} project declarations."
