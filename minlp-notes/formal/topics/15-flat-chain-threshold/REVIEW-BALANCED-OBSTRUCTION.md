# Balanced-incidence obstruction review

Status: semantic review of FC47–53 is complete, with no unresolved finding.
The terminal star-family targeted build passed with warnings treated as errors.
This record does not mark the entire topic complete.

## Scope and review independence

This review covers obligations FC47–53 in [CLAIMS.md](CLAIMS.md). It checks the mathematical statements and their
connection to the original graph hull, rather than treating successful Lean
compilation alone as evidence that the intended claims were stated.

The reviewer independently examined `ThresholdBalancedAlgebra`,
`ThresholdGeneralSection`, `ThresholdAffineRows`, `ThresholdFace`,
`ThresholdBalancedHull`, `ThresholdBalancedRatio`, `ThresholdStarObstruction`,
`ThresholdCycleRank`, `ThresholdOriginalObstruction`, and
`ThresholdObstructionFacts`. The same reviewer authored
`ThresholdBalancedProfile`, `ThresholdStarFamily`, `ThresholdSection`, and
`ThresholdArbitrarySection`, `ThresholdExtension`, and
`ThresholdUnusedObstruction`; those supporting modules are not represented as
independently reviewed in this record.

## Findings

- The inverse norm is the induced operator norm on `Fin N → ℝ`, whose norm is the
  coordinate supremum norm. Thus `inverseSize` represents the stated infinity
  operator norm, rather than an entrywise matrix norm or an unspecified bound.
- `perturbation_equation` derives the inverse equation from the determinant-unit
  assumption. `perturbation_bound` and `tau_bound` prove the explicit neighborhood
  bounds with the paper's denominator `16 * (1 + R) * (1 + inverseSize K)`.
  The cancellation of the second free perturbation in `-delta + tau` is valid
  because the selected rows are distinct.
- The balancing argument uses column sums `∑ i, alpha i * K i j = beta`.
  This is the correct orientation for `Kᵀ alpha = beta * 1`. It proves that the
  recovered perturbation sums to zero. No zero-sum conclusion is assumed.
- The profile proof derives necessity from actual row feasibility. Sufficiency
  constructs `a + perturbation`, proves its bounds and total, and verifies the
  profile inequalities. The separate `initialEntry_sum`, `single_row_correction`,
  and `correction_margin` lemmas verify the displayed single-cell row correction.
- `original_hull_iff_full_of_sum_one` applies to the original simplex inequality
  domain. The residual state remains unobserved. Its scaled capacity bounds
  force its flow to zero on the sum-one face; the converse explicitly inserts
  that zero flow. This is not an assumption that the original simplex always
  has total weight one.
- `sectionPoint_eq_productSlice` fixes every flow coordinate, every simplex
  coordinate, and every other retained product. `observation_ne` proves the two
  varying entries are distinct. They are individual products without scaling.
- `AffineRow.eval_productSlice` preserves precisely the original coefficients
  on those products. The finite-description theorem proves existence of an
  active nonconstant row and a positive normal multiplier; it does not infer
  impossibility merely from a displayed valid cut or a dual multiplier.
- `SectionData.equation_coefficients` proves that adding any valid affine
  equation cannot change either forced product coefficient. The section has
  actual two-dimensional interior, and both gadget flows satisfy the stated
  strict original-domain margins.
- Positive real balancing weights generalize the source's positive rational
  weights. This changes no direction of the stated application.

## Four-label instance and unused labels

The four-label section fixes the flows to the displayed `13/32`, `5/16`, and
`1/2` values and the explicit weights to `1/4`. The selected products correspond
to the source's one-based cells `(a₁,4)` and `(a₂,2)`. Its local inequality is
exactly `2U+V ≥ 3/32`. `ThresholdObstructionFacts` checks seven actual observations,
five vertices, nine arcs, the zero kernel of the four-by-four incidence matrix,
and the balancing weights `(2,1,1,1)` with beta three. `four_cycle_rank` proves the
incidence-kernel dimension is five.

The original-coordinate finite-description theorem forces ratio two, and valid
affine equations have zero coefficients on both selected products. The stronger
unit-description obstruction even permits arbitrary inequality families.
For additional unused explicit labels, the extension leaves flow and product
coordinates unchanged. Its reverse implication proves every added state's flow
is zero from the scaled bounds. Relabeling to `Fin (4+k)` preserves the same
section and the same original product coefficients.

## Star-family application

`ThresholdStarObstruction.sectionData` instantiates every balanced-incidence
hypothesis using the proved star-family matrix facts. Label zero represents the
source's final label; the distinguished rows and their forbidden observed cells
are chosen consistently with this relabeling. The selected products are distinct.

`every_description_ratio` concerns every finite affine description of the actual
original graph hull, and its positive multiplier forces coefficient ratio `k-1`.
`unbounded_every_description` directly quantifies over arbitrary finite affine
descriptions of the actual hull. It proves a strictly positive denominator
coefficient and a coefficient quotient larger than any prescribed real bound.
It does not rely only on growth of abstract matrix coefficients.

`actual_observation_count` connects the forbidden-pair count to the actual
observed-product subtype by an explicit equivalence. `actual_counts` verifies
`k+2` vertices, `2k+3` arcs, `k+1` explicit labels, and `1+k*(k-1)` observations.
The cycle rank `k+2` is proved as the dimension of the actual incidence kernel,
using a linear equivalence with the gadget b-arcs and bypass coordinates.
These agree with the source's parameterization `M = k-1`.

## Scope correction found during review

The first general-section wrapper required both normal coordinates to be
positive. That covered the balanced-incidence application but not all of FC47,
whose source permits any nonzero normal. The added
`local_halfplane_description_arbitrary_normal` and
`local_halfplane_equation_arbitrary_normal` in
[ThresholdArbitrarySection.lean](../../Formal/NetworkSimplex/ThresholdArbitrarySection.lean)
remove that restriction, including negative or zero components. The final
coefficients are expressed in the original coordinates; the temporary linear
change of variables is confined to the proof.

## Verification boundary

Only targeted module builds were run locally. In particular,
`lake build Formal.NetworkSimplex.ThresholdArbitrarySection --wfail` and
`lake build Formal.NetworkSimplex.ThresholdBalancedProfile --wfail` passed.
The author also confirmed a warning-free targeted build of
`Formal.NetworkSimplex.ThresholdStarObstruction`, which includes the terminal
balanced-incidence and star-family dependencies.
Project-wide verification and CI inspection were not performed. Final topic
verification commands and results belong in the topic's verification record.
