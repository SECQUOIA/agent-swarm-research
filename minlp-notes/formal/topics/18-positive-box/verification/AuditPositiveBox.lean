/-
Audit of the topic-18 positive-box package.

Two independent checks:

1. `#print axioms` on the load-bearing declaration of every obligation
   PB01-PB46, which also verifies that these named declarations exist.
   Their types and coverage are assessed by source review. Every line must report only
   `[propext, Classical.choice, Quot.sound]`.

2. A sweep over *every* declaration owned by the nineteen topic-18 modules,
   including `private` helpers, rejecting any axiom outside that triple.

Reproduce with

    lake env lean topics/18-positive-box/verification/AuditPositiveBox.lean
-/
import Formal.MultilinearGap.PositiveBox
import Formal.MultilinearGap.PhysicalEnvelope
import Formal.MultilinearGap.SlabIntegrality
import Formal.MultilinearGap.OrientationMoments
import Formal.MultilinearGap.FairOrientationFolding
import Formal.MultilinearGap.CoefficientInequality
import Formal.MultilinearGap.CommonAspectBound
import Formal.MultilinearGap.OriginalBoxTransfer
import Formal.MultilinearGap.TransferInterpretation
import Formal.MultilinearGap.BalancedOrientation
import Formal.MultilinearGap.BalancedMoments
import Formal.MultilinearGap.BalancedRefinement
import Formal.MultilinearGap.RadixFamily
import Formal.MultilinearGap.RadixIncidence
import Formal.MultilinearGap.RadixAttainment
import Formal.MultilinearGap.RadixTermwise
import Formal.MultilinearGap.RadixHullGap
import Formal.MultilinearGap.BilinearGraph
import Formal.MultilinearGap.PositiveBoxHeadline
import Lean.Util.CollectAxioms

open MultilinearGap

/-! ## Tier A: classes and semantics -/

-- PB01
#print axioms MultilinearGap.boxAspectRatios_nonempty
#print axioms MultilinearGap.boxAspectRatios_bddAbove
#print axioms MultilinearGap.one_le_boxAspectSupremum
-- PB02
#print axioms MultilinearGap.commonAspectBoxRatios_subset_boxAspectRatios
#print axioms MultilinearGap.commonAspectBoxSupremum_le_boxAspectSupremum
-- PB03
#print axioms MultilinearGap.boxPoint_image_cube
#print axioms MultilinearGap.monomial_boxPoint_vertex_pow
-- PB04
#print axioms MultilinearGap.positiveBox_gap_sandwich
#print axioms MultilinearGap.one_le_of_mem_boxAspectRatios

/-! ## Tier B: the four rounding laws and their moments -/

-- PB05 (subset-minimum form, simultaneous attainment, sorted form)
#print axioms MultilinearGap.physMonomial_maximum
#print axioms MultilinearGap.thresholdLaw_maximizes_physMonomial
#print axioms MultilinearGap.thresholdLaw_binomMoment
#print axioms MultilinearGap.thresholdLaw_binomMoment_sorted
-- PB06
#print axioms MultilinearGap.bernoulliLaw_physMonomial
#print axioms MultilinearGap.bernoulliLaw_binomMoment
-- PB07 (partial: folded parametrization, see COVERAGE.md)
#print axioms MultilinearGap.orientMoment_one
#print axioms MultilinearGap.orientationLaw_physMonomial_eq_sum
-- PB08
#print axioms MultilinearGap.two_mul_orientMoment_two
-- PB09
#print axioms MultilinearGap.orientMoment_mono
#print axioms MultilinearGap.orientMoment_update_abs_le
-- PB10 (route substitution: adjacent-count law built directly, see COVERAGE.md)
#print axioms MultilinearGap.exists_adjacentLaw
-- PB11
#print axioms MultilinearGap.physMonomial_minimum
#print axioms MultilinearGap.physMonomial_hullGap
-- PB12
#print axioms MultilinearGap.binomMoment_zero
#print axioms MultilinearGap.binomMoment_of_neg
#print axioms MultilinearGap.binomMoment_of_card_lt

/-! ## Tier C: the coefficient inequality -/

-- PB13
#print axioms MultilinearGap.coeffF_zero
#print axioms MultilinearGap.coeffF_one
-- PB14
#print axioms MultilinearGap.coeffF_card_add_one
#print axioms MultilinearGap.coeffF_card_add_one_nonneg
#print axioms MultilinearGap.coeffF_of_card_add_one_lt
-- PB15
#print axioms MultilinearGap.coeffF_two
#print axioms MultilinearGap.coeffF_two_nonneg
-- PB16
#print axioms MultilinearGap.coeffF_insert_of_mean_zero
#print axioms MultilinearGap.coeffF_insert_of_mean_one
-- PB17
#print axioms MultilinearGap.coeffF_spread_le
-- PB18
#print axioms MultilinearGap.coeffF_nonneg

/-! ## Tier D: the common-aspect bound -/

-- PB19
#print axioms MultilinearGap.physCombination_eq_sum_coeffF
-- PB20
#print axioms MultilinearGap.physUpper_sub_physLower_le
-- PB21
#print axioms MultilinearGap.mixtureLaw_hasMeans
#print axioms MultilinearGap.mixtureLaw_capture
#print axioms MultilinearGap.exists_common_mixture_law
-- PB22
#print axioms MultilinearGap.commonAspect_termwiseGap_le
#print axioms MultilinearGap.commonAspect_termwiseGap_le_four

/-! ## Tier E: original-box transfer and interpretation -/

-- PB23
#print axioms MultilinearGap.originalBox_bijOn
#print axioms MultilinearGap.exists_originalBoxPoint
#print axioms MultilinearGap.originalExpansionCoefficient_nonneg
-- PB24
#print axioms MultilinearGap.boxHullGap_originalBoxPoint
#print axioms MultilinearGap.boxTermwiseGap_originalBox_le_expansion
-- PB25
#print axioms MultilinearGap.positiveBoxAspectBound_add_two
-- PB26 (deficiency equality proved; hull-gap equality disproved)
#print axioms MultilinearGap.originalMonomial_concaveEnvelope_eq_sum
#print axioms MultilinearGap.originalMonomial_deficiency_eq_sum
#print axioms MultilinearGap.no_common_minimizing_law
#print axioms MultilinearGap.boxHullGap_originalMonomial_lt_sum_expansion
#print axioms MultilinearGap.originalBox_monomial_capture

/-! ## Tier F: the finite-dimensional refinement -/

-- PB27
#print axioms MultilinearGap.orientationBeta_even
#print axioms MultilinearGap.orientationBeta_odd
-- PB28
#print axioms MultilinearGap.balancedOrientationLaw_hasMeans
#print axioms MultilinearGap.balancedSubsets_pair_opposite
#print axioms MultilinearGap.balancedSubsets_restrict_pair_opposite
#print axioms MultilinearGap.balancedSubsets_mem_ne_half_of_odd
-- PB29
#print axioms MultilinearGap.balancedOrientMoment_two
#print axioms MultilinearGap.orientationBeta_mul_thresholdMoment_sub_balancedOrientMoment_two
-- PB30
#print axioms MultilinearGap.balancedCoeffF_spread_le
#print axioms MultilinearGap.balancedCoeffF_nonneg
-- PB31
#print axioms MultilinearGap.commonAspect_termwiseGap_le_balanced
#print axioms MultilinearGap.positiveBoxAspectBound_add_orientationBeta
#print axioms MultilinearGap.boxTermwiseGap_eq_zero_of_card_le_one

/-! ## Tier G: the lower bound -/

-- PB32
#print axioms MultilinearGap.Radix.physMeans_mem_box
#print axioms MultilinearGap.Radix.physMeans_mem_interior
#print axioms MultilinearGap.Radix.supportPolynomial_termSupports
-- PB33
#print axioms MultilinearGap.Radix.term_convex_envelope
-- PB34
#print axioms MultilinearGap.Radix.term_concave_envelope
-- PB35
#print axioms MultilinearGap.Radix.radix_boxTermwiseGap
#print axioms MultilinearGap.Radix.dCorrection_nonneg
#print axioms MultilinearGap.Radix.dCorrection_le
-- PB36
#print axioms MultilinearGap.Radix.radix_hullGap_isGreatest
-- PB37 (upper direction only; attainment not proved)
#print axioms MultilinearGap.Radix.incidence_expect_le_of_means
-- PB38
#print axioms MultilinearGap.Radix.radix_hullGap_le
-- PB39
#print axioms MultilinearGap.Radix.radix_hullGap_ge
-- PB40
#print axioms MultilinearGap.Radix.hullTotal_pos
-- PB41
#print axioms MultilinearGap.Radix.hullTotal_div_tendsto
#print axioms MultilinearGap.Radix.radix_ratio_tendsto
-- PB42 (two maps: multiplicative for the radix family, unit-cube for the graph)
#print axioms MultilinearGap.Radix.boxPoint_eps_eq
#print axioms MultilinearGap.Radix.boxHullGap_monomial_eps
#print axioms MultilinearGap.Radix.hullTotal_eq_boxHullGap
#print axioms MultilinearGap.bilinearGraph_box_ratio_eq
#print axioms MultilinearGap.hullGap_of_meanExact_split
-- PB43
#print axioms MultilinearGap.Radix.rho_le_of_forall_mem_boxAspectRatios
#print axioms MultilinearGap.Radix.rho_le_boxAspectSupremum
#print axioms MultilinearGap.Radix.rho_le_commonAspectBoxSupremum
-- PB44 (even ambient dimensions: the ratio is 2(n-1)/n at n = 2m)
#print axioms MultilinearGap.bilinearGraph_cube_ratio
#print axioms MultilinearGap.bilinearGraph_ratio_tendsto
#print axioms MultilinearGap.two_le_of_forall_mem_boxAspectRatios
#print axioms MultilinearGap.two_le_boxAspectSupremum
#print axioms MultilinearGap.two_le_commonAspectBoxSupremum
-- PB44 correction (odd n = 2m+1: ratio 2n/(n+1) for m > 0, see COVERAGE.md)
#print axioms MultilinearGap.bilinearGraph_minimum_odd
#print axioms MultilinearGap.bilinearGraph_hullGap_odd
#print axioms MultilinearGap.bilinearGraph_termwiseGap_odd
#print axioms MultilinearGap.bilinearGraph_cube_ratio_odd
#print axioms MultilinearGap.bilinearGraph_cube_ratio_odd_ne

/-! ## Tier H: the headline, and the boundedness that makes it meaningful -/

-- PB45
#print axioms MultilinearGap.boxAspectRatios_bddAbove_of_lt
#print axioms MultilinearGap.boxAspectSupremum_le_add_two
#print axioms MultilinearGap.le_boxAspectSupremum
#print axioms MultilinearGap.positiveBox_headline
-- PB46
#print axioms MultilinearGap.boxAspectSupremum_sub_mem
#print axioms MultilinearGap.boxAspectSupremum_two_le_four
-- The two declarations added in response to the reviews.
#print axioms MultilinearGap.commonAspectBoxRatios_bddAbove_of_lt
#print axioms MultilinearGap.le_commonAspectBoxSupremum

/-! ## Sweep: every declaration owned by the nineteen topic-18 modules -/

/-! ## PB07 closed: the fair orientation law equals the folded law -/
#print axioms MultilinearGap.fairOrientationLaw_eq_orientationLaw
#print axioms MultilinearGap.binomMoment_fairOrientationLaw
#print axioms MultilinearGap.fairOrientationLaw_hasMeans
#print axioms MultilinearGap.intervalIntegral_comp_foldUnit

/-! ## PB10 closed: slab integrality, the geometric statement -/
#print axioms MultilinearGap.mem_slab_self
#print axioms MultilinearGap.slab_subset_convexHull_slabVertices
#print axioms MultilinearGap.convexHull_slabVertices_eq
#print axioms MultilinearGap.extremePoints_slab_subset
#print axioms MultilinearGap.exists_adjacentLaw_of_slab

/-! ## PB32 closed: nesting of the actual radix blocks -/
#print axioms MultilinearGap.Radix.blockEquiv_fst_val_of_le
#print axioms MultilinearGap.Radix.block_subset_unique

/-! ## PB37 closed: attainment, hence the equality -/
#print axioms MultilinearGap.Radix.incidence_attained
#print axioms MultilinearGap.Radix.isGreatest_incidenceValues_of_le_radix
#print axioms MultilinearGap.Radix.isGreatest_incidenceValues
#print axioms MultilinearGap.Radix.sSup_incidenceValues
#print axioms MultilinearGap.Radix.hitCount_fiber

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.MultilinearGap.PositiveBox, `Formal.MultilinearGap.PhysicalEnvelope,
    `Formal.MultilinearGap.OrientationMoments, `Formal.MultilinearGap.CoefficientInequality,
    `Formal.MultilinearGap.CommonAspectBound, `Formal.MultilinearGap.OriginalBoxTransfer,
    `Formal.MultilinearGap.TransferInterpretation, `Formal.MultilinearGap.BalancedOrientation,
    `Formal.MultilinearGap.BalancedMoments, `Formal.MultilinearGap.BalancedRefinement,
    `Formal.MultilinearGap.RadixFamily, `Formal.MultilinearGap.RadixIncidence,
    `Formal.MultilinearGap.RadixTermwise, `Formal.MultilinearGap.RadixHullGap,
    `Formal.MultilinearGap.BilinearGraph, `Formal.MultilinearGap.PositiveBoxHeadline,
    `Formal.MultilinearGap.SlabIntegrality, `Formal.MultilinearGap.FairOrientationFolding,
    `Formal.MultilinearGap.RadixAttainment]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-18 declarations across {owners.size} modules."
