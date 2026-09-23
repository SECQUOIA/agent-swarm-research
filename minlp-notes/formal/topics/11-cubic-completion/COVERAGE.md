# Focused cubic claim-to-proof map

Status: mathematical claim review **PASS**. This map records the statements
inspected in the [focused paper](../../../paper-cubic-gap/main.tex). No
substantive mathematical coverage gap remains in that scope. Integrated
builds, axiom audit, kernel replay, and distribution checks are recorded
separately. The [review](REVIEW.md) records domains and independent checks.

Canonical files are in [`Formal/CubicGap`](../../Formal/CubicGap), with shared
infrastructure in [`Formal/MultilinearGap`](../../Formal/MultilinearGap).
Unless explicitly qualified, new cubic declarations have namespace `CubicGap`.
`RoundingOptimality` declarations have namespace `CubicGap.RoundingOptimality`.
`Bernstein` declarations have namespace `CubicGap.Bernstein`.

## Definitions and graph-hull foundations

| Paper claim | Declaration and interpretation |
|---|---|
| Original continuous cube hull equals the vertex hull | `CubicGap/Hull`: `cubeGraph_hull_eq_vertexGraph_hull`, `mem_cubeGraph_hull_iff` |
| Both endpoints are attained with all marginals preserved | `MultilinearGap/Attainment`: `CubicGap.envelopeValues_endpoints`, `CubicGap.envelope_endpoints_attained_by_laws`, `boxEnvelope_endpoints_attained_by_laws` |
| Greatest convex and least concave envelopes | `MultilinearGap/EnvelopeFunctions`: `cube_convex_envelope`, `cube_concave_envelope`, `box_convex_envelope`, `box_concave_envelope` |
| Exact nonempty monomial endpoints and the empty constant | `MultilinearGap/MonomialEnvelope`: `monomial_lower_attaining_law`, `monomial_minimum`, `monomial_hullGap`, `empty_monomial_hullGap`; `CubicGap/TermwiseUpper`: `monomial_maximum_of_min_coordinate` |
| Common-threshold law attains all positive-term upper endpoints | `MultilinearGap/GeneralGaps`: `thresholdLaw_hasMeans`, `thresholdLaw_monomial_upper`, `positive_polynomial_maximum_general` |
| A common deficiency estimate bounds the positive polynomial | `MultilinearGap/GeneralGaps`: `coupling_gap_bound_general`; `CubicGap/RoundingLaws`: `rounding_deficiency_nonneg` |
| Original scaled terms and `0 ≤ H_B ≤ T_B` | `MultilinearGap/PaperFoundations`: `boxTermwiseGap_eq_term_gaps`, `box_gap_comparison` |
| All-box degree-three supremum, positive denominator, arbitrary finite dimension | `MultilinearGap/BoxSuprema`: `boxDegreeRatios`, `boxDegreeSupremum`, specialized at degree three |

The formal nonnegative coefficient class matches the paper. Zero coefficients,
affine terms, unused coordinates, boundary points, and fixed box coordinates
are allowed. Cited historical results and publication priority are not Lean
claims of this package.

## The actual laws and universal upper bound

| Paper claim | Source and declaration |
|---|---|
| Conditional indicator integrals, nested products and endpoints | `RoundingIndicators`: `integral_lowerStep`, `lowerStep_mul`, `integral_lowerStep_mul_three` |
| Global folded orientation law, conditional independent coordinates, probabilities and full means | `OrientationRounding`: `orientationProbability`, `orientationProbability_mem`, `orientationProbability_measurable`, `orientationProbability_integral`, `orientationLaw`, `orientationLaw_hasMeans` |
| Orientation moments for actual distinct coordinate supports | `OrientationRounding`: `orientationLaw_expect_monomial`, `orientationLaw_expect_pair`, `orientationLaw_expect_triple` |
| Orientation one-low and all-high formulas, two-low estimate, and bilinear formula | `OrientationRounding`: `orientation_integral_one_low`, `orientation_integral_all_high`, `orientation_integral_two_low`, `orientation_integral_pair` |
| Global biased-threshold law with low class `x ≤ 1/2` and full marginals | `BiasedHighRounding`: `biasedHighProbability`, `integral_biasedHighProbability`, `biasedHighLaw`, `biasedHighLaw_hasMeans` |
| Actual biased-law moments and their low/high formulas | `BiasedHighRounding`: `biasedHighLaw_expect_pair`, `biasedHighLaw_expect_triple`, `integral_biasedHigh_pair_low`, `integral_biasedHigh_pair_one_low`, `integral_biasedHigh_pair_high`, `integral_biasedHigh_triple_one_low`, `integral_biasedHigh_triple_high` |
| Independent Bernoulli means and exact product deficiencies | `RoundingLaws`: `independentRounding_hasMeans`, `independentRounding_pair_deficiency`, `independentRounding_triple_deficiency` |
| One-low min-function inequality, including all shared boundaries | `RoundingScalar`: `rounding_one_low`, `rounding_one_low_mixture` |
| All-high scalar `3/8` and independent `7/16` estimates | `RoundingScalar`: `rounding_high_orientation`, `rounding_high_independent`, `rounding_high_mixture` |
| Two-low estimate and all bilinear cases | `RoundingScalar`: `rounding_two_low_independent`, `rounding_two_low_mixture`, `rounding_bilinear_one_low`, `rounding_bilinear_low_mixture`, `rounding_bilinear_mixed_uniform`, `rounding_bilinear_high_uniform` |
| Mixture weights `(18,6,7)/31`, expectation linearity and full means | `RoundingLaws`: `roundingMixture`, `roundingMixture_expect`, `roundingMixture_deficiency`, `cubicRoundingLaw`, `cubicRoundingLaw_hasMeans` |
| One fixed ambient law supplies the pair and triple guarantees | `RoundingLaws`: `cubicRoundingLaw_pair_deficiency_lower`, `cubicRoundingLaw_triple_deficiency_lower` |
| Sorted pair/triple representations and exact gaps | `RoundingUpper`: `support_pair_sorted`, `support_triple_sorted`, `pair_hullGap`, `triple_hullGap` |
| Empty/singleton supports and all supports of degree at most three | `RoundingUpper`: `small_support_deficiency`, `cubicRoundingLaw_support_deficiency` |
| Actual polynomial cube inequality | `RoundingUpper`: `cubic_cube_gap_bound`, `cubic_degree_bound` |
| Original nonnegative boxes, including fixed coordinates and zero coefficients | `RoundingUpper`: `cubic_box_gap_bound`, using `degree_gap_bound_on_box` in `MultilinearGap/BoxTransfer` |
| Nonempty ratio class and supremum upper bound | `RoundingUpper`: `degreeRatios_three_nonempty`, `cubic_boxDegreeSupremum_le` |

The law is a function of the complete marginal vector, without a support or
coefficient argument. Its conditional product construction is the existing
`integratedBernoulli` infrastructure. The manuscript defines the folded
orientation law directly; equivalence to an alternative unfurled construction
is not needed for the stated result.

## Fixed-mixture optimality

| Paper claim | Source or remaining obligation |
|---|---|
| Feasible one-low and all-high approaching configurations | `RoundingOptimality`: `smallParameter`, `smallParameter_bounds`, `oneLowPoint`, `oneLowPoint_cube`, `oneLowPoint_sorted`, `allHighPoint`, `allHighPoint_cube`, `allHighPoint_sorted` |
| Algebraic normalized expressions on both curves | `RoundingOptimality`: `oneLow_normalized_formulas`, `allHigh_normalized_formulas` |
| Independent normalized limits zero and `7/16` | `RoundingOptimality`: `tendsto_smallParameter`, `tendsto_oneLow_independent`, `tendsto_allHigh_independent` |
| Uniform sequence bounds imply limiting constraints | `RoundingOptimality`: `limit_constraints` |
| Rational combination gives `α ≤ 12/31` | `RoundingOptimality`: `weighted_obstruction` |
| Actual-law formulas imply the constraints for every uniform fixed-mixture guarantee | `RoundingOptimalityLaw`: `FixedMixtureGuarantee`, `oneLow_law_normalized`, `allHigh_law_normalized`, `fixedMixture_bilinear_constraint`, `fixedMixture_limit_constraints`, `fixed_mixture_optimal_bound` |
| The proposed weights attain that fraction in the same formal guarantee predicate | `RoundingOptimalityLaw`: `optimal_mixture_guarantee` |
| Exact attained optimum over nonnegative weights summing to one | `RoundingOptimalityLaw`: `fixed_mixture_optimum` |

The manuscript uses the formalized domains `0 < ε ≤ 1/8` and
`1/2 < u ≤ 5/8`, and the fixed bilinear point `(1/2,1/2)`. These domains
supply both required limits. The actual-law endpoint proves the obstruction,
not merely an algebraic inequality conditional on unproved constraints. The
predicate ranges over all finite ambient cubes and every pair/triple support.

## Analytic family and the lower bound

| Paper claim | Source and declaration |
|---|---|
| Six-orbit family, exact coefficient vector and means | `AnalyticValues`: `analyticCoefficients`, `analyticFamily`, `analyticMeans` |
| Positive integer orbit coefficients for positive multiples of nine | `AnalyticValues`: `analyticCoefficients_pos`, `analyticCoefficients_integer` |
| Every nonzero aggregate monomial coefficient is a positive integer and has support size two or three | `ThreeSupports`: `threeSupportCoefficients_nat`, `threeSupportCoefficients_card`; `AnalyticResults`: `analytic_nonzero_support`, `analytic_integer_support_witness` |
| Actual squarefree support polynomial of degree at most three | `ThreeSupports`: `threeSupports`, `threeSupports_degree`, `threeSupportCoefficients_nonneg`, `threeFamily_eq_supportPolynomial` |
| Orbit termwise gap agrees with the actual distinct-support gap | `ThreeSupports`: `threeTermwiseGap_eq_weightedTermwiseGap` |
| Scalar polynomial, affine minorant and rational slack | `Bernstein`: `cubic`, `affine`, `slack`, `scalar_minorant` |
| Both printed completed-square identities and corresponding bounds | `Bernstein`: `constrained_lower_bound`, `unrestricted_lower_bound`; their proof terms establish the identities by polynomial normalization |
| All five exact Bernstein rows, coefficient bounds, basis positivity and sum one | `Bernstein`: `bernstein4_lower`, `lowerP_first`, `lowerP_second`, `lowerR_first`, `lowerR_second`, `lowerR_third` |
| Exact normalized binary expansion and error at most `72/m` | `AnalyticFamily`: `analyticCount_mem`, `analytic_binary_expansion`, `analytic_binary_lower` |
| Any joint law preserving individual means has the required expected counts | `AnalyticFamily`: `analyticCount_expect` |
| Universal law and actual convex-envelope lower bound | `AnalyticFamily`: `analytic_law_lower`, `analytic_scaled_minimum_lower` |
| Exact concave envelope and normalized formula | `AnalyticValues`: `analytic_maximum`, `analytic_orbitUpper`, `analytic_scaled_maximum` |
| Exact termwise gap and normalized formula | `AnalyticValues`: `analytic_termwiseGap`, `analytic_scaled_termwiseGap`, with the `ThreeSupports` semantic bridge above |
| Only `E₃(W)` has nonzero individual lower envelopes | `TermwiseFamilies`: the six support-class minimum theorems and `termwiseLowerThree_eq`; `orbitLower` in `Finite` contains only its first coefficient |
| Positive actual hull gap | `AnalyticValues`: `analytic_value_at_means`, `analytic_hullGap_pos`; the proof compares a feasible graph point with the common upper endpoint |
| Finite scaled hull bound and actual ratio inequality, with and without slack | `AnalyticFamily`: `analytic_scaled_hullGap_upper`, `analytic_finite_ratio_lower`, `analytic_finite_ratio_lower_simple` |
| Admissible multiples of nine and convergent refined/unrefined lower sequences | `AnalyticLimit`: `analyticSize`, `analyticSize_ge_nine`, `analyticSize_dvd_nine`, `tendsto_analyticRatioLower`, `tendsto_analyticHeadlineLower` |
| Refined fraction reduction and strict improvement | `AnalyticLimit`: `analyticRefinedLimit_reduced`, `analytic_headline_lt_refined` |
| Actual ratios exceed every smaller constant and give integer-family witnesses | `AnalyticLimit`: `analyticRatio_eventually_gt`, `analyticRatio_exists_gt`, `analytic_integer_family_witness` |
| The unrefined `m=36` certificate equals `16985/8436 > 2` | `AnalyticLimit`: `analyticHeadlineLower_thirty_six`, `analyticHeadlineLower_thirty_six_gt_two` |
| Actual family membership in the degree-three class | `ThreeSupports`: `three_ratio_mem_degreeRatios`, applied to analytic coefficients and positive hull gap |
| Supremum lower bound and final two-sided all-box statement | `AnalyticResults`: `analyticRatio_mem_degreeRatios`, `analyticRatio_mem_boxDegreeRatios`, `analyticRefinedLimit_le_boxDegreeSupremum`, `cubic_boxDegreeSupremum_sandwich` |

The scaling identity is asserted at binary vertices. The scalar minorant is
valid on the full continuous count cube. The convergent sequence consists of
certified lower bounds; no convergence of actual ratios or exactness of the
convex-envelope lower bound is asserted. The support representation includes
zero coefficients on unused supports, which is allowed by the definition of
`R(3)`.

## Exact finite witnesses in the manuscript

The paper's two-group polynomial is `twoFamily` from `Families`; its means
are `twoMeans` (equal to `thresholdTwoMeans`). Its three-group polynomial is
`threeFamily`; its means are `threeMarginals` (equal to
`thresholdThreeMeans`). In order, the six coefficients multiply
`E₃(W), B E₂(W), E₂(V), AC, AB, E₂(U)`.

| Family / group size | Ambient coordinates | Coefficients | Exact ratio / `Ratios` declaration |
|---|---|---|---|
| Two groups, `m=4` | `Fin 2 × Fin 4`, cardinality 8 | Formula `5m/4` | `27/16`, `two_ratio4` |
| Two groups, `m=8` | `Fin 2 × Fin 8`, cardinality 16 | Formula `5m/4` | `21/11`, `two_ratio8` |
| Two groups, `m=12` | `Fin 2 × Fin 12`, cardinality 24 | Formula `5m/4` | `99/50`, `two_ratio12` |
| Two groups, `m=16` | `Fin 2 × Fin 16`, cardinality 32 | Formula `5m/4` | `135/67`, `two_ratio16` |
| Three groups, `m=6` | `Fin 3 × Fin 6`, cardinality 18 | `(2,3,9,10,7,7)` | `20891/10411`, `three_ratio6` |
| Three groups, `m=8` | `Fin 3 × Fin 8`, cardinality 24 | `(2,3,13,12,8,7)` | `6601/3225`, `three_ratio8` |
| Three groups, `m=64` | `Fin 3 × Fin 64`, cardinality 192 | `(2,3,120,105,70,63)` | `7443345/3445256`, `three_ratio64` |

`coefficients6`, `coefficients8`, and `coefficients64` in `Finite` contain exactly
these three vectors. They are separate finite examples, not members of the
analytic coefficient sequence. `four_strict_counterexamples` in `Ratios` proves
that the last four ratios exceed two. Actual hull-width statements are in
`Results`, minima and their attaining laws in `TwoResults`/`ThreeResults`,
universal count minorants in `Finite`/`LargeFinite`, and common upper endpoints
in `Maxima`. `Counts` and `CountLaws` connect count certificates to actual
coordinate laws. The seven displayed coordinate counts are direct evaluations
of product-Fin cardinalities.

## Exclusions and completion requirements

The manuscript excludes the all-parameter two-level family, general
coefficient removal, homogeneous approximation of the supremum,
equal-marginal classification, dimension minimality, and the exact value of
`R(3)`. The existing separate homogeneous 52-variable witness is not needed or
claimed in this focused manuscript.

Numerical search and Python/SymPy checks are supporting evidence, not trusted
Lean proof steps. The actual-law optimality, actual-supremum, and aggregate
integer-support interfaces have all been reviewed. Completion of the
distribution also requires the integrated warning-free build,
import coverage, axiom audit, kernel replay, source-export equality, and
paper/bundle checks. Those checks belong in the verification record.
