# Topic 28 claim coverage

Status: every frozen obligation has an implemented declaration and independent
semantic review. Final build, axiom-audit, and kernel-replay results are
recorded separately; this map alone is not a completion claim.

Modules are in [Formal/QuadraticAggregation](../../Formal/QuadraticAggregation).
Names below are relative to `QuadraticAggregation`. Definitions are listed
where they fix the semantics of the following theorems.

| Claim | Module and declarations |
|---|---|
| C01 | `ClosedSystem`: `quadratic_nonpos_convex`, `quadratic_nonpos_isClosed`, `quadratic_nonpos_ne_univ`, `quadratic_unbounded_above`, `System.agg_eval_nonpos`, `System.closed_convexHull_subset_aggregate`, `System.Certificate.closed_convexHull_ne_univ`. Includes pure linear aggregates; neither strict feasibility nor AHC is assumed. |
| C02 | `ClosedSystem`: `System.feasible_subset_closedFeasible`, `System.closed_proper_hull_iff_certificate`, `System.strict_proper_hull_iff_closed`, `System.closed_hull_eq_univ_iff_strict`, `System.closed_proper_hull_iff_certificate_of_hhc`, `System.closed_hull_eq_univ_iff_strict_of_hhc`. |
| C03 | `ShorBlock`: `outer`, `shorBlock`, `outer_posSemidef`, `shorBlock_posSemidef_iff`, `shorBlock_affine`. `ShorModel`: `tracePair`, `tracePair_outer`, `tracePair_nonneg`, `System.shorProjection`, `System.mem_shorProjection_iff`, `System.closedFeasible_subset_shorProjection`, `System.feasible_subset_shorProjection`, `System.convex_shorProjection`. The block theorem identifies the covariance definition with the actual Shor projection. |
| C04 | `ShorAlgebra`: `System.shorProjection_aggregate_nonpos`, `System.Certificate.shorProjection_ne_univ`, using `System.tracePair_aggA` and `tracePair_nonneg` from `ShorModel`. |
| C05 | `ShorAlgebra`: `System.shorProjection_eq_univ_of_convexHull_eq_univ`, `System.shorProjection_eq_univ_iff`, `System.shorProjection_eq_univ_iff_closed`. `Consequences`: `System.shor_and_hulls_eq_univ`, `System.shor_and_hulls_eq_univ_of_hhc`. |
| C06 | `ShorConeSeparation`: `exists_nonnegative_separator`. `ShorDuality`: `System.strict_shor_alternative`, `System.exists_strict_shor_slack`, `System.shorProjection_eq_univ_of_no_certificate`. `Consequences`: `System.shorProjection_eq_univ_iff_no_certificate`, `System.shorProjection_eq_univ_iff_trivial`. No AHC/HHC or cone-closedness premise is assumed. |
| C07 | `SDPCharacterization`: `System.normalizedPSD`, `System.normalizedPSD_ne_zero`, `System.aggA_smul`, `System.aggB_smul`, `System.Certificate.exists_normalized`, `System.no_certificate_iff_trivial`, `System.no_certificate_iff_normalized_zero`, `System.full_hull_iff_sdpTestsZero`, together with C08's equivalence. The final theorem uses AHC; HHC specializes through topic 27's `System.HHC.asymptoticHC`. |
| C08 | `SDPCharacterization`: `System.CoefficientIndex`, `System.coefficientObjective`, `System.coefficientObjective_eq_sum`, `System.continuous_coefficientObjective`, `System.coefficients_zero_iff`, `System.isCompact_normalizedPSD`, `System.signed_objective_attains`, `System.SDPTestsZero`, `System.sdpTestsZero_iff_no_certificate`, `System.signed_objective_count`. Upper-triangular coordinates use `DAGSpectral.upperCoordEquiv` and `DAGSpectral.card_upperCoord`; the signed count is exactly `n(n+1)+2n`. The common feasible set uses the original `m` weights and one `n×n` aggregate PSD block. |
| C09 | `Boundary`: `Boundary.hyperbola`, `Boundary.hyperbola_eval_zero`, `Boundary.hyperbola_eval_one`, `Boundary.hyperbola_eval_two`, `Boundary.hyperbola_strict_empty`, `Boundary.hyperbola_closed`, `Boundary.hyperbola_closed_nonempty`, `Boundary.hyperbola_closed_bound`, `Boundary.hyperbola_closed_hull_bound`, `Boundary.hyperbola_closed_hull_proper`, `Boundary.hyperbola_agg_q`, `Boundary.hyperbola_psd_trivial`, `Boundary.hyperbola_no_certificate`. PSD triviality holds even for unrestricted real weights. |
| C10 | `Dines`: `convex_image_quadratic_pair`, `QuadraticMap.convex_image_pair`, `System.homEval_combination`, `System.hhc_pair`. `Boundary`: `Boundary.hyperbolaPair`, `Boundary.duplicateNegative`, `Boundary.hyperbola_hom_factor`, `Boundary.hyperbola_hhc`, `Boundary.hyperbola_closed_equivalence_fails`. Actual HHC follows from a proved two-form theorem and linear-image factorization. |
| C11 | `Boundary`: `Boundary.strip`, `Boundary.strip_eval_zero`, `Boundary.strip_eval_one`, `Boundary.strip_feasible`, `Boundary.strip_nonempty`, `Boundary.strip_convex`, `Boundary.strip_hull_eq`, `Boundary.strip_hull_proper`, `Boundary.strip_hhc`, `Boundary.strip_agg_q`, `Boundary.strip_psd_iff`, `Boundary.strip_convex_aggregation_admits_zero`, `Boundary.strip_zero_not_convexHull`, `Boundary.stripConvexAggregations`, `Boundary.strip_zero_mem_convexAggregations`, `Boundary.strip_convexAggregations_ne_hull`. |
| C12 | `Boundary`: `Boundary.stripSlack`, `Boundary.stripSlack_psd`, `Boundary.strip_shor_residual`, `Boundary.strip_shor_block_witness`, `Boundary.strip_zero_mem_shor`, `Boundary.strip_shor_strictly_larger`, `Boundary.strip_shor_proper`. The witness is exactly `diag(7/2,0,0)` at zero and both residuals are exactly `-1/2`. |

The implementation strengthens Lemma 4 by constructing a PSD slack with
strict residuals at every point when no nontrivial certificate exists.
Its open-set separation proof avoids the source's closure/interior route;
the unused cone-closure identity is not claimed as separately verified.
`Consequences` also proves `System.shorProjection_eq_univ_iff_sdpTestsZero`
under strict feasibility alone, without hyperplane convexity.

The ten owned modules are listed in modules.json.
Imported topic 27 theorems and the upper-triangle count remain dependencies,
not new topic 28 modules. Exclusions remain those in [CLAIMS.md](CLAIMS.md).
