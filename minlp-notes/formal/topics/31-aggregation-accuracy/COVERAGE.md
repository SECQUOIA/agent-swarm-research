# Aggregation-accuracy coverage

All ten source-level obligations in [CLAIMS.md](CLAIMS.md) have implemented
interfaces and independent semantic review. Names below are in the common
namespace `InfiniteAggregation`; a `Module.declaration` entry identifies
the source file and declaration, not an extra Lean namespace.

| Claim | Required conclusion | Evidence |
|---|---|---|
| A01 | Actual Euclidean model and faithful source transport | `AccuracyModel.EuclideanVar`, `euclidean`, `euclideanDist`, `euclidean_norm_sq`, `euclideanDist_sq`, `euclideanEquiv`, `euclidean_closedRegion_eq_closedHull` |
| A02 | Extended Hausdorff error and infimum over arbitrary good families | `AccuracyModel.relaxation`, `admissibleFamily`, `hausdorffError`, `optimalError`, `closedRegion_subset_relaxation`, `isCompact_euclidean_closedRegion`, `euclidean_closedRegion_nonempty`, `hausdorffError_eq_top_of_unbounded`, `optimalError_le_family`, `le_optimalError` |
| A03 | Complete angle-ray description, including endpoints | `AccuracyUpperGeometry.angleWeight_goodCone`, `angleWeight_ne_zero`, `angleWeight_good`, `pointAngularForm_eq_neg_aggregate`, `angular_tests_subset_closedRegion`; `AccuracyUpper.mem_closedRegion_iff_angular` |
| A04 | Uniform `N≥2` angle upper bound with exact constant | `AccuracyAngular.angular_sample_lower_bound`; `AccuracyMesh.exists_mem_angleMesh_dist_le`, `zero_mem_angleMesh`, `pi_div_two_mem_angleMesh`; `AccuracyUpperGeometry.radial_factor`, `radial_repair`; `AccuracyUpper.euclideanDist_radial_le`, `angle_samples_repair`, `angleCuts`, `card_angleCuts_le`, `angleCuts_admissible`, `hausdorffError_angleCuts_le` |
| A05 | Universal arbitrary-good-family lower bound with exact constant | `AccuracyLowerPigeonhole.exists_unviolated_of_card_le`, `accuracyGrid_mem_Icc`, `accuracyGrid_separated`; `AccuracyLowerGap.positive_perturbed_slacks_gap`; `AccuracyLowerLipschitz.accuracy_ray_lipschitz`; `AccuracyLower.accuracy_lower_witness`, `rational_lower_le_hausdorffError`, `accuracy_lower_le_hausdorffError`; `AccuracyConstants.accuracyLowerBound_le_rational_plain` |
| A06 | Exact two-sided infimum bound, without attainment | `AccuracyLower.accuracy_lower_le_optimalError`; `Accuracy.optimalError_le_upper`, `optimalError_bounds`, `optimalError_ne_top`, `optimalError_toReal_bounds` |
| A07 | Exact integer mesh, source goodness, cut count, coefficient bound | `AccuracyRational.rationalLeftCoeff`, `rationalRightCoeff`, `rationalCuts`, `rationalCuts_card`, `rationalCuts_good`, `rationalCuts_ray_unique`, `rationalCuts_endpoints`, `rationalLeftCoeff_le`, `rationalRightCoeff_le`, `rationalMeshSize`, `rationalCuts_budget` |
| A08 | Rational-family uniform Euclidean error | `AccuracyRationalMesh.arctan_abs_sub_le`, `exists_nearest_grid_point`, `rationalAngleMesh_covers`; `AccuracyRationalBound.rationalLeft_angle`, `rationalRight_angle`, `rational_mesh_tests`, `hausdorffError_rationalCuts_le` |
| A09 | Binary coefficient bound and rational quadratic error rate | `AccuracyRational.coefficient_size_bound`, `coefficient_log_bound`, `rational_coefficients_bit_bound`, `rationalCuts_integer_encoding`, `rationalCuts_log_encoding`; `AccuracyRationalBound.rational_error_le_inverse_square`, `hausdorffError_rationalCuts_budget_le` |
| A10 | Uniform rate and necessary/sufficient accuracy-count consequences | `AccuracyConstants.accuracyLowerBound_pos`, `accuracyUpperBound_le_inverse_square`; `AccuracyRate.inverse_square_theta`, `accuracyBudget`, `accuracyBudget_ge_two`, `accuracyBudget_upper`, `accuracyBudget_size`, `accuracyLowerBound_budget`; `Accuracy.optimalError_theta`, `exists_family_for_tolerance`, `necessary_family_budget` |

The fifteen owned modules are `Accuracy`, `AccuracyAngular`,
`AccuracyConstants`, `AccuracyLower`, `AccuracyLowerGap`,
`AccuracyLowerLipschitz`, `AccuracyLowerPigeonhole`, `AccuracyMesh`,
`AccuracyModel`, `AccuracyRate`, `AccuracyRational`, `AccuracyRationalBound`,
`AccuracyRationalMesh`, `AccuracyUpper`, and `AccuracyUpperGeometry`, all
under `Formal/InfiniteAggregation`.

The [independent reviews](REVIEW.md) cover each complete branch and its
final source-level meaning. The successful fifteen-module build,
232-declaration axiom audit, and fifteen kernel replays are separate
evidence in [VERIFICATION.md](VERIFICATION.md). No project-wide checks or
CI inspection are part of this package.
