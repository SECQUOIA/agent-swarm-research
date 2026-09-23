# Marginal-floor coverage map

This map covers the mathematical scope in [CLAIMS.md](CLAIMS.md) and the
[result note](../../../results/positive-multilinear-marginal-floor-gap.md).
Build, trust, and replay evidence belongs in [VERIFICATION.md](VERIFICATION.md);
this document identifies the precise statements to which that evidence applies.
All declaration names below are in `MultilinearGap` unless qualified otherwise.

## Entry points and exact scope

Import [FloorResults.lean](../../Formal/MultilinearGap/FloorResults.lean) for the
finite bound, supremum bounds, sharp limits, and original-box theorem.
[FloorSemantics.lean](../../Formal/MultilinearGap/FloorSemantics.lean) separately
exposes the exact maximum-deficiency interpretation. The existing exact dyadic
ratio limit is in [ExactAsymptotics.lean](../../Formal/MultilinearGap/ExactAsymptotics.lean).

`floorRatios` and `stripRatios` use **strictly positive coefficients on included
supports**, and require a strictly positive actual hull gap before forming a
ratio. `floorSupremum` and `stripSupremum` are their real suprema. The definitions
are total functions of the real floor; the substantive floor supremum theorems
assume `0 < δ < 1`. Strip nonemptiness includes `δ = 1/2`; the sharp strip limit
concerns positive floors tending to zero.

The multiplicative bounds `floor_finite_bound` and
`marginal_floor_original_box_bound` allow **nonnegative coefficients**, including
zero coefficients, empty supports, and zero hull gaps. They have no dimension or
degree bound. The ratio suprema are not defined over a separate
nonnegative-coefficient class, and no equality of those two class definitions is
claimed. The stronger multiplicative bound supplies the positive-coefficient
supremum bound directly.

Write `B = floorB δ`, `τ = floorTau δ`, `L = floorL δ`, and
`I = floorIntegral L (1 / B^2)`. The explicit factor is
`floorUpper δ = 1 / I + 2 / (1 - Real.exp (-1))`. In particular,
`floor_finite_bound` proves `T ≤ floorUpper δ * H` for every `δ > 0`, and
`floorSupremum_le_upper` proves the corresponding supremum bound for `δ < 1`.

`floorSupremum_asymptotic`, `stripSupremum_asymptotic`, and their conjunction
`sharp_marginal_floor_growth` assert limits equal to **one** after division by
`log (1 / δ) / log (log (1 / δ))`, in the filter `𝓝[>] 0`. These are limits in a
real variable, not just limits along a sequence of dyadic floors. They do not
assert equality of the two suprema at a fixed floor.

## Claim-to-declaration map

Module links in this table are relative to this topic directory. The table
names public results; subsidiary analytic or algebraic steps can be internal to
the named proofs.

| Claim | Checked declarations and scope |
|---|---|
| MF-01 | [FloorDomain](../../Formal/MultilinearGap/FloorDomain.lean): `floorRatios`, `floorSupremum`, `CubeFloorBound`. The ratio class quantifies over all finite coordinate types, support families, positive included coefficients, cube points above the floor, and positive actual `hullGap`. |
| MF-02 | FloorDomain: `one_mem_floorRatios`, `floorRatios_nonempty`, `floorRatios_bddAbove`, `floorRatios_le`. [FloorResults](../../Formal/MultilinearGap/FloorResults.lean): `floor_finite_bound` supplies boundedness and `floorSupremum_le_upper` uses both prerequisites of the real supremum argument. The nonempty witness has one bilinear monomial and ratio one. |
| MF-03 | FloorDomain: `floorRatios_antitone`. FloorResults: `floorSupremum_antitoneOn` on `(0,1)` and `floorSupremum_le_half` for `1/2 ≤ δ < 1`. Boundedness and nonemptiness are proved before comparing suprema. |
| MF-04 | [FloorSemantics](../../Formal/MultilinearGap/FloorSemantics.lean): `monomial_gap_eq_min_otherFailures`, for a minimum-mean anchor belonging to the support; singletons are included. [MonomialEnvelope](../../Formal/MultilinearGap/MonomialEnvelope.lean): `empty_monomial_hullGap` supplies the empty case. |
| MF-05 | [GeneralGaps](../../Formal/MultilinearGap/GeneralGaps.lean): `thresholdLaw_hasMeans`, `thresholdLaw_monomial_upper`, `positive_polynomial_maximum_general`, `coupling_gap_bound_general`. FloorSemantics: `weightedAnchorDeficiency_eq`, `weightedAnchorDeficiency_le_hullGap`, `exists_weightedAnchorDeficiency_eq_hullGap`, `hullGap_isGreatest_weightedAnchorDeficiency`. The explicit anchor-maximum theorem requires an included minimum anchor for each support, hence nonempty supports; constants are handled by the general upper-envelope formulation used by the terminal bound. [Attainment](../../Formal/MultilinearGap/Attainment.lean): `envelope_endpoints_attained_by_laws` supplies attainment rather than assuming it. |
| MF-06 | FloorSemantics: `anchor_deficiency_nonneg` proves pointwise vertex nonnegativity. GeneralGaps: `monomial_deficiency_nonneg` proves expected nonnegativity for any law with the required means. [FloorUpper](../../Formal/MultilinearGap/FloorUpper.lean): `floorMixture_deficiency` and `floorMixture_deficiency_nonempty` explicitly preserve unused nonnegative contributions. |
| MF-07 | [FloorAsymptotics](../../Formal/MultilinearGap/FloorAsymptotics.lean): `floorB_ge_two`, `floorB_pos`, `floorTau_pos`, `floorL_pos`, `floorL_gt_one`, `floorUpper_pos`. The `L > 1` statement assumes `0 < δ ≤ 1/2`. [FloorGain](../../Formal/MultilinearGap/FloorGain.lean): `shifted_failure_continuousOn`, `floorIntegral_intervalIntegrable`, `floorIntegral_pos`, `floorIntegral_le_one`. [EasyTerms](../../Formal/MultilinearGap/EasyTerms.lean): `easyConstant_pos` gives positivity of the independence denominator and hence of κ. |
| MF-08 | [FloorDensity](../../Formal/MultilinearGap/FloorDensity.lean): `floorDensity`, `floorDensity_pos`, `floorDensity_of_nonneg`, `continuous_floorDensity`, `measurable_floorDensity`, `intervalIntegrable_floorDensity`, `integral_floorDensity`. The globally valid density uses `max 0 t`, agrees with the source formula for `t ≥ 0`, and integrates to one on `[0,1]` for `τ > 0`. |
| MF-09 | FloorDensity: `floorClipped`, `floorMass`, `floorClipped_mem_unitInterval`, `measurable_floorClipped`, `intervalIntegrable_floorClipped`, `floorMass_nonneg`, `floorMass_le`. These statements hold for any `p ≥ 0`; the high-coordinate condition additionally gives `p < 1/2`. |
| MF-10 | FloorDensity: `floorCompletion_mem_unitInterval`, `floorFailure_ge_clipped`, `floorFailure_mem_unitInterval`, `measurable_floorFailure`, `intervalIntegrable_floorFailure`, `integral_floorFailure`. The repair is valid for `0 ≤ p < 1`, including zero; its integral is exactly `p`. The proof derives positivity of `1 - floorMass τ p`. |
| MF-11 | [FloorCoupling](../../Formal/MultilinearGap/FloorCoupling.lean): `floorProbability`, `floorProbability_cube`, `floorProbability_measurable`, `intervalIntegral_floorProbability`, `floorLaw`, `floorLaw_hasMeans`, `floorLaw_expect_monomial`. One explicitly integrated finite Bernoulli law depends on the mean vector and shift, not the polynomial, support family, or coefficients. Probabilities remain valid for every real integration parameter. |
| MF-12 | FloorCoupling: `floorUnion_exp_lower`. Its proof splits on whether any uncorrected failure probability is at least one; in that branch the corrected failure is exactly one and the survival product vanishes. Otherwise it uses `prod_le_exp_neg_failure_sum` from EasyTerms and the fact that marginal repair only increases failure probabilities. |
| MF-13 | FloorCoupling: `floorLaw_unique_low_deficiency`, `floorLaw_unique_low_lower`; also `floorUnion_mem_Icc`, `floorUnion_measurable`, `floorUnion_intervalIntegrable`. The hypotheses are one included anchor with mean at most `1/2`, and every other support coordinate strictly above `1/2`. The exact deficiency is the union integral on the anchor interval. |
| MF-14 | FloorGain: `min_one_mul_one_sub_exp_neg_le`. This is the multiplication form of the source's quotient inequality, valid even at `y = 0`, with assumptions `a ≥ 0` and `y ≥ 0`. Its proof uses convexity of the exponential below one and monotonicity above one. |
| MF-15 | FloorGain: `floor_gain_pointwise`, `floor_integral_gain`. FloorCoupling: `floorLaw_unique_low_gain`. FloorAsymptotics: `floorTau_div_le`. These prove the common gain when the anchor is positive and `τ/u ≤ e`, with `S ≥ 0`; no assumption `S > 0` is introduced. The terminal theorem sets `e = 1/B²`. |
| MF-16 | EasyTerms: `independent_deficiency_high`, `independent_deficiency_second_low`, `bernoulli_easy_gap`. FloorUpper: `floorMixture_deficiency_nonempty` applies the easy bound when the minimum anchor is at least `1/2` or another coordinate is at most `1/2`. Thus equality at the threshold is covered. The bound is the individual hull gap times `easyConstant/2`, equivalently the gap divided by κ. |
| MF-17 | FloorUpper: `floorBound`, `floorBound_pos`, `floorMixture`, `floorMixture_expect`, `floorMixture_hasMeans`, `floorMixture_deficiency`, `floorMixture_deficiency_nonempty`, `floorMixture_deficiency_all`. The mixture weights are exactly the normalized inverse gains `1/I` and κ. The all-support theorem includes the empty support. |
| MF-18 | FloorUpper: `floor_cube_gap_bound`, using the actual graph-hull semantics of `coupling_gap_bound_general`. FloorResults: `floor_finite_bound`, `floorSupremum_le_upper`, `floorSupremum_le_half`. The finite inequality is proved directly for every positive floor and nonnegative coefficients, with no positive-hull-gap premise. |
| MF-19 | FloorAsymptotics: `floorB_eventually`, `tendsto_floorB`, `tendsto_floorTau`, `floorL_identity`, `tendsto_floorL_div_B`, `floorL_equivalent_B`, `tendsto_floorL`, `tendsto_floor_log_ratio`, `tendsto_floorL_div_B_sq`. The exact identity gives the remainder `log (1 + floorTau δ)`; its limit zero follows from `tendsto_floorTau` and continuity of log, as used in `tendsto_floorL_div_B`. |
| MF-20 | [FloorIntegralBounds](../../Formal/MultilinearGap/FloorIntegralBounds.lean): `floorIntegral_upper`, assuming `L > 1` and `e > 0`, proves exactly `(1 + log L)/L`. The proof splits at `1/L`; reciprocal comparisons are used only on the positive subinterval, so it does not assume the singular formula is valid at zero. |
| MF-21 | [FloorExpBound](../../Formal/MultilinearGap/FloorExpBound.lean): `sub_sq_div_two_le_one_sub_exp_neg`. FloorIntegralBounds: `floorIntegral_lower`, assuming `L > 1` and `e > 0`, proves `log L/(L*(1+L*e)) - (L-1)/(2*L²) ≤ floorIntegral L e`. This specializes to the listed shift `e = 1/B²`. |
| MF-22 | FloorAsymptotics: `tendsto_floor_lower_normalized`, `tendsto_floor_upper_normalized`, `tendsto_floorIntegral_normalized`, `tendsto_floor_scale`, `tendsto_floorUpper_normalized`. These prove both requested equivalents with leading constant one; the fixed independence contribution vanishes. |
| MF-23 | [FloorLower](../../Formal/MultilinearGap/FloorLower.lean): `means_dyadic_strip` proves the strip for every natural level at least one. [Termwise](../../Formal/MultilinearGap/Termwise.lean): `polynomial_eq_supportPolynomial` identifies the unit-coefficient support polynomial, and `termwiseGap_eq` proves its termwise width. [Results](../../Formal/MultilinearGap/Results.lean): `hullGap_positive` in the range of at least two levels. |
| MF-24 | [ExactAsymptotics](../../Formal/MultilinearGap/ExactAsymptotics.lean): `tendsto_exact_family_ratio_normalized` proves the actual family ratio divided by `L/logb 2 L` tends to one as the natural level tends to infinity. This existing result is distinct from the new real-floor limit. |
| MF-25 | FloorLower: `floorLevels`, `floorLevels_ge_two`, `floorLevels_pow_le`, `means_floor_strip`, `tendsto_floorLevels`, `tendsto_floorLevels_scale`. FloorResults: `floor_witness_mem_stripRatios`, followed by `stripRatios_subset_floorRatios`. For every `0 < δ ≤ 1/4` these give an actual admissible witness. The terminal squeeze uses `floorLower_le_ratio` and `tendsto_floorLower_normalized`, the explicit sufficient comparison `L/(logb 2 L+3)`, instead of requiring the exact family ratio formula. |
| MF-26 | FloorResults: `floor_suprema_bounds`, `floorSupremum_asymptotic`, `sharp_marginal_floor_growth`. The lower witness and upper bound squeeze the actual supremum at every sufficiently small positive real floor. |
| MF-27 | FloorDomain: `stripRatios`, `stripSupremum`, `one_mem_stripRatios`, `stripRatios_nonempty`, `stripRatios_subset_floorRatios`. Boundedness follows by this subset inclusion from `floorRatios_bddAbove (floor_finite_bound hδ)`, as used in `floor_suprema_bounds`. No finite supremum statement for the empty strip above `1/2` is used. |
| MF-28 | FloorLower: `means_floor_strip`. FloorResults: `floor_witness_mem_stripRatios`, `floor_suprema_bounds`, `stripSupremum_asymptotic`, `sharp_marginal_floor_growth`. The same actual witnesses give the strip lower bound; inclusion gives its upper bound. |
| MF-29 | [BoxTransfer](../../Formal/MultilinearGap/BoxTransfer.lean): `boxEnvelopeValues_eq_of_mem`, `boxHullGap_eq_of_mem`. These identify the original box graph-hull slice with the affine pullback on the cube at a cube parameter, assuming only `l ≤ u`, not strict inequalities. |
| MF-30 | BoxTransfer: `boxExpansionCoefficient_nonneg`, `boxPolynomialCoefficient_nonneg`, `monomial_box_expansion`, `supportPolynomial_box_expansion`, `boxTermwiseGap_le_expansion`. Nonnegativity assumes `0 ≤ l ≤ u` and nonnegative original coefficients. The original sum of monomial widths is bounded **above** by the expanded termwise width; equality is not claimed. |
| MF-31 | FloorDomain: `floorBoxParameter`, `floorBoxParameter_mem`, `floorBoxParameter_floor`, `floorBoxParameter_map`, `floor_gap_bound_box_transfer`, `floor_gap_bound_on_box`. FloorResults: `marginal_floor_original_box_bound`, for a finite coordinate type, `0 < δ ≤ 1`, nonnegative coefficients, `0 ≤ l ≤ u`, a point in the box, and the normalized floor on nonfixed coordinates. The conclusion uses original `boxTermwiseGap` and original `boxHullGap`. |
| MF-32 | The same parameter and transfer declarations cover fixed coordinates by assigning their cube parameter the value `δ`. No positive side length, positive endpoint, nonzero coefficient, nonempty support, or positive hull gap is required by `marginal_floor_original_box_bound`. FloorUpper's `floorMixture_deficiency_all` covers empty terms, and the actual-width monomial bounds include singleton terms. Thus some or all coordinates may be fixed, and zero-width cases remain multiplicative inequalities. |

## Proof premises and exclusions

Density normalization, marginal repair, hard-term gain, integral estimates,
attainment, and asymptotic estimates are proved, rather than supplied as
hypotheses to the terminal results. The reusable transfer theorem takes a cube
bound as an explicit premise; `marginal_floor_original_box_bound` discharges it
with `floor_finite_bound`.

The floor condition on a nonnegative box concerns normalized coordinates with
nonzero side length. Positive lower endpoints alone do not imply this condition.
The original-box result is a finite bound; no new supremum over arbitrary boxes
or separate sharp box asymptotic is defined.

The development proves mathematical statements about convex hulls and finite
laws. It does not verify numerical experiments, novelty or publication priority,
an optimization or separation algorithm, or an approximation guarantee for
constrained MINLP. These are outside the claim inventory.
