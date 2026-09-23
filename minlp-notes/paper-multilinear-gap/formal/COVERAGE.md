# Paper-to-Lean coverage

The bundle proves the disproof, exact finite counterexample gap and
attainment, the paper's explicit finite upper bound, and both sharp leading
asymptotics. The source is [main.tex](../main.tex); its human-readable form is
[main.pdf](../main.pdf). All paths below are internal to this folder.

All declarations belong to namespace `MultilinearGap` unless marked
`CubicGap`. A module name in the table is a filename, not another namespace.
The formulas use actual original continuous graph-hull widths. The final
theorems do not assume that the hull gap equals an unverified surrogate.

## Main claims

| Paper statement | Source and formal declaration |
|---|---|
| No constant bounds the positive multilinear gap ratio, even on unit cubes with unit coefficients | [Results](Formal/MultilinearGap/Results.lean): `unbounded_gap_ratio`, `no_uniform_positive_multilinear_bound` |
| Exact dyadic termwise gap `T_L = L` | [Termwise](Formal/MultilinearGap/Termwise.lean): `termwiseGap_eq` |
| Finite cap certificate and sharp hull-gap upper bound | [ExactUpper](Formal/MultilinearGap/ExactUpper.lean): `dyadic_exact_pointwise`, `dyadic_exact_deficiency_bound`, `hullGap_exact_upper_bound` |
| Exact hull gap `H_L = s + (L-s)/2^s`, with a cutoff for every `L ≥ 2` and endpoint attainment | [ExactResults](Formal/MultilinearGap/ExactResults.lean): `polynomial_exact_minimum`, `hullGap_exact`, `exists_hullGap_exact` |
| A shared law gives the explicit cube bound `T ≤ sharpZ Λ * H` | [SharpUpper](Formal/MultilinearGap/SharpUpper.lean): `sharpLaw_hasMeans`, `sharpLaw_deficiency`, `sharp_cube_gap_bound` |
| Original-term upper bound on finite nonnegative boxes, including fixed coordinates | [BoxTransfer](Formal/MultilinearGap/BoxTransfer.lean): `degree_gap_bound_on_box` |
| Leading constant one in degree and exactly-n dimension over all boxes | [SharpAsymptotics](Formal/MultilinearGap/SharpAsymptotics.lean): `boxDegreeSupremum_asymptotic`, `boxDimensionSupremum_asymptotic`, `sharp_positive_growth` |

## Foundations and the counterexample

| Obligation | Source and declaration |
|---|---|
| Continuous cube graph hull equals its binary-law representation | [Hull](Formal/CubicGap/Hull.lean): `CubicGap.mem_cubeGraph_hull_iff` |
| Graph-hull slice and width definitions; conversion of law certificates to attained endpoints | [Envelope](Formal/CubicGap/Envelope.lean): `CubicGap.envelopeValues`, `CubicGap.hullGap`, `CubicGap.minimum_from_laws`, `CubicGap.maximum_from_laws` |
| Partitions, exact block sizes, and partition sum identity | [Construction](Formal/MultilinearGap/Construction.lean): `block_card`, `sum_blocks`, `blockCount_mul_blockSize` |
| Distinct squarefree supports, separate affinity, and strictly interior means | [Construction](Formal/MultilinearGap/Construction.lean): `support_injective`, `polynomial_separatelyAffine`, `means_strict` |
| Unit-coefficient support representation | [Termwise](Formal/MultilinearGap/Termwise.lean): `polynomial_eq_supportPolynomial` |
| Counterexample's exact individual monomial endpoints | [Monomial](Formal/MultilinearGap/Monomial.lean): `monomial_minimum_zero_of_anchor`; [Termwise](Formal/MultilinearGap/Termwise.lean): `support_monomial_minimum`, `support_monomial_maximum` |
| Global upper envelope L and positive hull gap | [Upper](Formal/MultilinearGap/Upper.lean): `polynomial_maximum`, `polynomial_at_means_lt`; [Results](Formal/MultilinearGap/Results.lean): `hullGap_positive` |
| Expected failure count one and universal law lower bound | [Lower](Formal/MultilinearGap/Lower.lean): `failureCount_expect`, `law_polynomial_lower_bound` |
| Arithmetic-only parameter choice exceeding every proposed constant | [Growth](Formal/MultilinearGap/Growth.lean): `exists_levels`; [Deficiency](Formal/MultilinearGap/Deficiency.lean): `dyadic_deficiency_bound` |

The disproof endpoint uses the independently verified weaker bound
`H_L ≤ s + 2L/2^s`. The paper instead uses the sharper cap certificate from
`ExactUpper` to shorten the written proof. Both proofs concern the same
polynomial and prescribed point.

## Exact attainment

| Obligation | Source and declaration |
|---|---|
| Adjacent cutoff budgets bracket one, and mixture weights are valid | [ExactArithmetic](Formal/MultilinearGap/ExactArithmetic.lean): `exists_exact_cutoff`, `cutoffMix_mem_unit`, `cutoffMix_budget`, `cutoffMix_deficit` |
| Threshold masses give prescribed anchor means and cutoff failure budgets | [ExactWeights](Formal/MultilinearGap/ExactWeights.lean): `dyadicLaw_tail`, `dyadicLaw_failures`, `dyadicLaw_selected` |
| Residue classes have the stated cardinalities and block products | [ResidueSums](Formal/MultilinearGap/ResidueSums.lean): `sum_residue_indicator`, `sum_coordinate_residue_complement`, `block_product_residue_zero` |
| Periodic failure patterns preserve leaf marginals and attain all block hits simultaneously | [ExactGeometry](Formal/MultilinearGap/ExactGeometry.lean): `spacedLeaf_failure_count`, `spacedLeaf_mean`, `spacedLeaf_level_sum` |
| Full mixed law preserves every original mean and attains the expected polynomial minimum | [ExactLaw](Formal/MultilinearGap/ExactLaw.lean): `mix_cutoff_laws`, `exists_exact_attaining_law` |

This matches the paper's zero-or-power-of-two periodic construction. No
arbitrary-failure-count bit-reversal or XOR lemma is assumed.

## Universal upper bound and asymptotics

| Obligation | Source and declaration |
|---|---|
| Weighted gap definition equals actual scaled-term widths; common upper attainment | [GeneralGaps](Formal/MultilinearGap/GeneralGaps.lean): `weightedTermwiseGap_eq_term_gaps`, `positive_polynomial_maximum_general`, `coupling_gap_bound_general` |
| Independent laws and integration of finite probability weights | [IntegratedLaws](Formal/MultilinearGap/IntegratedLaws.lean): `bernoulliLaw`, `integratedLaw_expect`, `integratedBernoulli` |
| Harmonic density is measurable, lies in `[0,1]`, and integrates to its failure marginal | [HarmonicDensity](Formal/MultilinearGap/HarmonicDensity.lean): `harmonicDensity_mem_Icc`, `intervalIntegral_harmonicDensity`, `harmonic_active_sum_lower` |
| Both common laws preserve the full marginal vector; their one-low deficiencies | [Couplings](Formal/MultilinearGap/Couplings.lean): `harmonicLaw_hasMeans`, `failureThresholdLaw_hasMeans`, `harmonicLaw_unique_low_deficiency`, `failureThresholdLaw_deficiency_lower` |
| Independence handles zero-low and at-least-two-low cases | [EasyTerms](Formal/MultilinearGap/EasyTerms.lean): `bernoulli_easy_gap` |
| Rational union inequality and harmonic integration window | [HarmonicGain](Formal/MultilinearGap/HarmonicGain.lean): `union_ge_div_one_add`, `harmonic_gain`, `sharp_harmonic_gain`; [HarmonicLawGain](Formal/MultilinearGap/HarmonicLawGain.lean): `harmonicLaw_sharp_gain` |
| One global three-law mixture preserves means and combines deficiencies | [Mixture](Formal/MultilinearGap/Mixture.lean): `threeMix_expect_common`, `threeMix_deficiency_ge` |
| Explicit parameters are positive and the normalized bound tends to one | [AsymptoticScalars](Formal/MultilinearGap/AsymptoticScalars.lean): `sharpH_pos`, `sharpZ_pos`, `tendsto_sharpZ_degree_normalized` |
| Witness coordinate count, support-size bounds, and all-integer size allowances | [FamilySize](Formal/MultilinearGap/FamilySize.lean): `coord_card`, `support_card_le`, `witness_dimension_le`, `witness_degree_le` |
| Feasible lower comparison tends to the claimed scale | [LowerAsymptotics](Formal/MultilinearGap/LowerAsymptotics.lean): `hullGap_le_logb_add_three`, `lowerComparison_le_ratio`, `tendsto_lowerComparison_normalized` |
| Ratio sets are nonempty and bounded before supremum comparisons | [Suprema](Formal/MultilinearGap/Suprema.lean): `degreeRatios_bddAbove`, `degreeRatios_nonempty`, `dimensionRatios_nonempty`, `suprema_bounds` |
| Unused-coordinate padding preserves both gaps | [Padding](Formal/MultilinearGap/Padding.lean): `padFunction_envelopeValues`, `padSupports_hullGap`, `padSupports_weightedTermwiseGap` |
| Dimension at most n and exactly n have the same cube ratio sets | [ExactDimension](Formal/MultilinearGap/ExactDimension.lean): `exactDimensionRatios_eq` |
| Box expansion preserves the hull gap and bounds the original termwise gap | [BoxTransfer](Formal/MultilinearGap/BoxTransfer.lean): `boxHullGap_eq_of_mem`, `boxTermwiseGap_le_expansion` |
| All-box degree and exactly-n-coordinate suprema have matching bounds | [BoxSuprema](Formal/MultilinearGap/BoxSuprema.lean): `boxDegreeRatios`, `boxDimensionRatios`, `box_suprema_bounds` |

The finite factor in the paper agrees with `sharpH`:
`(1-1/b)/(1+1/b²) * (b-3 ln b)/Λ`, with `b = ln Λ`.
The formal lower asymptotics use a logarithmic hull-gap bound rather than
the exact formula, so the asymptotic endpoint does not depend on exact attainment.

## Completion of the remaining mathematical claims

| Paper assertion | Formal declaration and scope |
|---|---|
| Lemma 1: compact cube slices and attained vertex-law extrema | [Attainment](Formal/MultilinearGap/Attainment.lean): `CubicGap.envelopeValues_isCompact`, `CubicGap.envelopeValues_endpoints`; the module also proves original-box representation and attainment, including fixed coordinates |
| Greatest convex and least concave envelopes agree with the graph-hull endpoints | [EnvelopeFunctions](Formal/MultilinearGap/EnvelopeFunctions.lean): `cube_convex_envelope`, `cube_concave_envelope`, `box_convex_envelope`, `box_concave_envelope`; each proves convexity/concavity, under/overestimation, and the comparison against every competing envelope |
| General individual monomial lower envelope, with all ambient means preserved | [MonomialEnvelope](Formal/MultilinearGap/MonomialEnvelope.lean): `monomial_lower_attaining_law`, `monomial_minimum`; empty support gives the constant one |
| Exact individual gap formula and the empty-support boundary | [MonomialEnvelope](Formal/MultilinearGap/MonomialEnvelope.lean): `monomial_hullGap`, `monomial_hullGap_of_min_coordinate`, `empty_monomial_hullGap` |
| Original-box term definition and `0 ≤ H_B ≤ T_B` | [PaperFoundations](Formal/MultilinearGap/PaperFoundations.lean): `boxTermwiseGap_eq_term_gaps`, `box_gap_comparison`; zero coefficients and fixed coordinates are included |
| Exact support count, attained maximum degree, and total variable occurrences | [ExactSize](Formal/MultilinearGap/ExactSize.lean): `supports_card`, `supports_max_degree`, `supports_occurrences`; the degree equality requires positive level count |
| Linear monomial count and `O(n_L log n_L)` occurrences | [ExactSize](Formal/MultilinearGap/ExactSize.lean): `supports_card_lt_twice_dimension`, `supports_occurrences_le_dimension_real_log`, `supports_occurrences_isBigO` |
| Cutoff scale and bounded remainder | [ExactAsymptotics](Formal/MultilinearGap/ExactAsymptotics.lean): `exact_cutoff_log_bounds`, `exact_cutoff_remainder_bounds` |
| Actual family `H_L = log₂ L + O(1)` and `T_L/H_L ~ L/log₂ L` | [ExactAsymptotics](Formal/MultilinearGap/ExactAsymptotics.lean): `hullGap_log_error` proves absolute error at most three; `tendsto_exact_family_ratio_normalized` proves the actual ratio limit |
| All four printed exact examples | [Examples](Formal/MultilinearGap/Examples.lean): `example_two`, `example_eight`, `example_sixteen`, `example_sixty_four`; each concerns actual continuous graph-hull and termwise gaps |
| Equality of adjacent cutoff values at a shared boundary | [Examples](Formal/MultilinearGap/Examples.lean): `adjacent_cutoff_values` |

The paper's intermediate failure-count and deficiency identities are assembled
from `failureCount_expect`, `level_lower_bound`, `polynomial_expect`, the
common-maximum theorems, and the exact-law proofs. The general attainment
results justify the maxima in these descriptions. Formal proof routes need
not reproduce each sentence of the written proof; the mathematical endpoints
and their defining domains agree.

## Precise limits of coverage

The all-box results allow nonnegative coefficients, finite real endpoints
with nonnegative lower bounds, equal endpoints, affine terms, unused
coordinates, and boundary points. Ratio sets require positive hull gap;
the finite inequalities also hold at zero hull gap. Exactly-n dimension
means ambient coordinates, not that every coordinate must occur.

The general individual lower-envelope identity, construction counts, sparsity
bounds, actual family asymptotics, and printed examples are now formalized.
The completion also proves that graph-hull slice endpoints are the greatest
convex underestimator and least concave overestimator. These bridges avoid
leaving the paper's envelope terminology as an unproved interpretation.

The bundle makes no claim about optimized fixed-point bounds, Lambert W,
second-order terms, the separate numerical constant 24 from earlier notes,
coefficient removal, homogenization, serialized size, arbitrary recursive
McCormick formulations on general boxes, or publication priority. These
claims are not part of the standalone paper's theorems.
