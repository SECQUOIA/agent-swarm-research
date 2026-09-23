This package proves the exact finite formula from the
[result note](../../../results/positive-multilinear-gap.md#exact-hull-gap-for-nested-dyadic-partitions)
for the existing dyadic polynomial, using its actual continuous graph hull.
All declarations below belong to namespace `MultilinearGap`.

| Mathematical obligation | Lean module and declarations |
|---|---|
| Counts of residue classes and their complements, including block products | [`ResidueSums`](../../Formal/MultilinearGap/ResidueSums.lean): `sum_residue_indicator`, `sum_coordinate_residue_complement`, `block_product_residue_zero` |
| Periodic failure sets have exactly 2^r failures, equal leaf marginals, and maximal block hits at every level | [`ExactGeometry`](../../Formal/MultilinearGap/ExactGeometry.lean): `spacedLeaf_failure_count`, `spacedLeaf_mean`, `spacedLeaf_level_sum` |
| Adjacent cutoff budgets bracket one for every L ≥ 2; mixture weights are admissible and give the claimed deficit | [`ExactArithmetic`](../../Formal/MultilinearGap/ExactArithmetic.lean): `exists_exact_cutoff`, `cutoffMix_mem_unit`, `cutoffMix_budget`, `cutoffMix_deficit` |
| Dyadic threshold law has the required anchor probabilities, failure budget, and expected selected deficit | [`ExactWeights`](../../Formal/MultilinearGap/ExactWeights.lean): `dyadicLaw_tail`, `dyadicLaw_failures`, `dyadicLaw_selected` |
| Explicit adjacent-cutoff mixture preserves every coordinate mean and attains the lower envelope value | [`ExactLaw`](../../Formal/MultilinearGap/ExactLaw.lean): `mix_cutoff_laws`, `exists_exact_attaining_law` |
| A finite dual certificate bounds every feasible law, hence the continuous hull gap | [`ExactUpper`](../../Formal/MultilinearGap/ExactUpper.lean): `dyadic_exact_pointwise`, `law_polynomial_exact_lower_bound`, `hullGap_exact_upper_bound` |
| Exact lower envelope and exact hull width, with a valid cutoff for every L ≥ 2 | [`ExactResults`](../../Formal/MultilinearGap/ExactResults.lean): `polynomial_exact_minimum`, `hullGap_exact`, `exists_hullGap_exact` |

The original package supplies the polynomial, prescribed means, termwise gap
T_L = L, upper-envelope attainment, and continuous graph-hull bridge. This
package adds the matching lower-envelope certificate and attaining law.

The geometric theorem covers the zero-or-power-of-two failure counts used by
the attaining law. It does not formalize arbitrary failure counts, bit-reversal
order, or XOR randomization. No asymptotic expansion beyond this exact finite
formula is claimed by this package. The separate
[sharp-growth package](../09-sharp-multilinear/COVERAGE.md) proves the leading
degree and dimension asymptotics.

The [verification record](VERIFICATION.md) states the recorded checks. These
formal results do not establish literature completeness or publication priority.
