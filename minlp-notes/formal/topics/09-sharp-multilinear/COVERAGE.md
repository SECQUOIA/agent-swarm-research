This package verifies the leading-constant-one degree and dimension growth
claims in the
[sharp-growth note](../../../results/positive-multilinear-sharp-degree-growth.md) over
the full finite nonnegative-box domain. All declarations below belong to
namespace `MultilinearGap`.

| Mathematical obligation | Lean module and declarations |
|---|---|
| Weighted termwise gaps equal the sum of actual scaled-term envelope widths; positive terms share an attained upper envelope | [`GeneralGaps`](../../Formal/MultilinearGap/GeneralGaps.lean): `weightedTermwiseGap_eq_term_gaps`, `positive_polynomial_maximum_general`, `coupling_gap_bound_general` |
| Independent finite laws and integration of finite probability weights preserve means and expectations | [`IntegratedLaws`](../../Formal/MultilinearGap/IntegratedLaws.lean): `bernoulliLaw`, `integratedLaw_expect`, `integratedBernoulli` |
| Harmonic density is measurable, lies in the unit interval, and has the specified integral | [`HarmonicDensity`](../../Formal/MultilinearGap/HarmonicDensity.lean): `harmonicDensity_mem_Icc`, `intervalIntegral_harmonicDensity`, `harmonic_active_sum_lower` |
| Harmonic and reversed threshold laws have the prescribed coordinate means | [`Couplings`](../../Formal/MultilinearGap/Couplings.lean): `harmonicLaw_hasMeans`, `failureThresholdLaw_hasMeans`, `harmonicLaw_unique_low_deficiency`, `failureThresholdLaw_deficiency_lower` |
| Independent rounding captures the easy cases | [`EasyTerms`](../../Formal/MultilinearGap/EasyTerms.lean): `bernoulli_easy_gap` |
| Elementary union bound and integration give the required harmonic gain | [`HarmonicGain`](../../Formal/MultilinearGap/HarmonicGain.lean): `union_ge_div_one_add`, `harmonic_gain`, `sharp_harmonic_gain` |
| Scalar harmonic estimate applies to the actual rounding law | [`HarmonicLawGain`](../../Formal/MultilinearGap/HarmonicLawGain.lean): `harmonicLaw_sharp_gain` |
| Three-law mixture preserves means and combines the alternative deficiency estimates | [`Mixture`](../../Formal/MultilinearGap/Mixture.lean): `threeMix_expect_common`, `threeMix_deficiency_ge` |
| Explicit positive mixture parameters have normalized upper bound tending to one | [`AsymptoticScalars`](../../Formal/MultilinearGap/AsymptoticScalars.lean): `sharpH_pos`, `sharpZ_pos`, `tendsto_sharpZ_degree_normalized` |
| One shared law bounds every support, including constants, and gives the polynomial cube gap bound | [`SharpUpper`](../../Formal/MultilinearGap/SharpUpper.lean): `sharpLaw_hasMeans`, `sharpLaw_deficiency`, `sharp_cube_gap_bound` |
| Dyadic witnesses fit both degree and dimension allowances | [`FamilySize`](../../Formal/MultilinearGap/FamilySize.lean): `coord_card`, `support_card_le`, `witness_dimension_le`, `witness_degree_le` |
| Feasible lower comparison tends to the claimed scale along every integer allowance | [`LowerAsymptotics`](../../Formal/MultilinearGap/LowerAsymptotics.lean): `hullGap_le_logb_add_three`, `lowerComparison_le_ratio`, `tendsto_lowerComparison_normalized` |
| Cube ratio sets are bounded above and nonempty for sufficiently large allowances, with explicit lower and upper bounds | [`Suprema`](../../Formal/MultilinearGap/Suprema.lean): `degreeRatios_bddAbove`, `degreeRatios_nonempty`, `dimensionRatios_nonempty`, `suprema_bounds` |
| Adding unused coordinates preserves continuous envelopes and both gaps | [`Padding`](../../Formal/MultilinearGap/Padding.lean): `padFunction_envelopeValues`, `padSupports_hullGap`, `padSupports_weightedTermwiseGap`, `padded_card` |
| Cube dimension at most n has the same ratio set as exactly n coordinates | [`ExactDimension`](../../Formal/MultilinearGap/ExactDimension.lean): `exactDimensionRatios_eq` |
| Affine box transfer permits fixed coordinates, preserves hull gaps, and bounds the original unexpanded termwise gap | [`BoxTransfer`](../../Formal/MultilinearGap/BoxTransfer.lean): `boxHullGap_eq_of_mem`, `boxTermwiseGap_le_expansion`, `degree_gap_bound_on_box` |
| All-box ratio sets use degree at most d or exactly n coordinates, and satisfy the matching bounds | [`BoxSuprema`](../../Formal/MultilinearGap/BoxSuprema.lean): `boxDegreeRatios`, `boxDimensionRatios`, `box_suprema_bounds` |
| Both cube and all-box suprema have leading constant one; the final conjunction covers all boxes | [`SharpAsymptotics`](../../Formal/MultilinearGap/SharpAsymptotics.lean): `degreeSupremum_asymptotic`, `dimensionSupremum_asymptotic`, `boxDegreeSupremum_asymptotic`, `boxDimensionSupremum_asymptotic`, `sharp_positive_growth` |

The final all-box theorems use actual original-term gaps and positive hull
gaps. Box endpoints are finite real numbers with nonnegative lower bounds;
equal endpoints are allowed. Coefficients may be zero, so the statement also
covers the positive-coefficient subclass. The exactly-n-coordinate statement
permits unused variables. It does not require every coordinate to occur in
the polynomial or prove an equivalent supremum restricted to interior points.
Constant and affine terms and boundary points are included. Termwise gaps
mean exact individual monomial graph-hull widths; no claim is made for
arbitrary recursive McCormick formulations on general boxes.

The harmonic proof uses z/(1+z), giving the factor 1/(1+1/b²) with b = ln Λ.
Its explicit finite upper bound and its leading constant are verified. This
package does not verify the note's separate numerical constant 24, an
optimized fixed-point characterization, Lambert W or second-order
asymptotics, homogenization, sparsity asymptotics, or serialized construction
size. The proposed next target is the
[optimized finite and second-order upper bound](../../../results/positive-multilinear-second-order-upper.md),
whose fixed-point and Lambert W certificates remain outside this package.
No matching second-order lower bound is asserted. The package makes no claim
about literature completeness or publication priority.

The [verification record](VERIFICATION.md) states the recorded build, audit,
and kernel checks. The exact finite dyadic hull formula is documented in the
separate [exact-formula package](../08-exact-multilinear/COVERAGE.md).
