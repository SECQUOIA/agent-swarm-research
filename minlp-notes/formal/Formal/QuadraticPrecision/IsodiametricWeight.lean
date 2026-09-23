import Mathlib

open MeasureTheory Set Metric
open scoped ENNReal

namespace QuadraticPrecision.IsodiametricWeight

variable {E : Type*} [NormedAddCommGroup E]

/-- A continuous radial weight with bounded support. -/
def weight (C : ℝ) (x : E) : ℝ := max 0 (C - ‖x‖ ^ 2)

lemma continuous_weight (C : ℝ) : Continuous (weight C : E → ℝ) :=
  continuous_const.max (continuous_const.sub (continuous_norm.pow 2))

lemma weight_nonneg (C : ℝ) (x : E) : 0 ≤ weight C x := le_max_left _ _

lemma weight_le {C : ℝ} (hC : 0 ≤ C) (x : E) : weight C x ≤ C := by
  exact max_le hC (sub_le_self _ (sq_nonneg _))

lemma weight_lower {C R : ℝ} (hR : 0 ≤ R) {x : E} (hx : x ∈ closedBall 0 R) :
    C - R ^ 2 ≤ weight C x := by
  have hx' : ‖x‖ ≤ R := by simpa using hx
  have hs : ‖x‖ ^ 2 ≤ R ^ 2 := sq_le_sq₀ (norm_nonneg _) hR |>.mpr hx'
  exact (sub_le_sub_left hs C).trans (le_max_right _ _)

variable [ProperSpace E]

lemma compactSupport_weight (C : ℝ) : HasCompactSupport (weight C : E → ℝ) := by
  apply HasCompactSupport.of_support_subset_isCompact (isCompact_closedBall (0 : E) (|C| + 1))
  intro x hx
  have hpos : 0 < C - ‖x‖ ^ 2 := by
    have hn : weight C x ≠ 0 := hx
    dsimp [weight] at hn
    exact lt_of_not_ge (fun h => hn (max_eq_left h))
  have hb : ‖x‖ ≤ |C| + 1 := by
    have habs := le_abs_self C
    have hnorm := norm_nonneg x
    have habs0 := abs_nonneg C
    nlinarith [sq_nonneg (‖x‖ - 1)]
  simpa using hb

variable [MeasureSpace E] [BorelSpace E]
  [IsFiniteMeasureOnCompacts (volume : Measure E)]

lemma integrable_weight (C : ℝ) : Integrable (weight C : E → ℝ) :=
  (continuous_weight C).integrable_of_hasCompactSupport (compactSupport_weight C)

noncomputable def weightedMeasure (C : ℝ) : Measure E :=
  volume.withDensity (fun x => ENNReal.ofReal (weight C x))

instance finite_weightedMeasure (C : ℝ) : IsFiniteMeasure (weightedMeasure (E := E) C) :=
  isFiniteMeasure_withDensity_ofReal (integrable_weight (E := E) C).2

lemma weightedMeasure_apply (C : ℝ) {K : Set E} (hK : MeasurableSet K) :
    weightedMeasure C K = ENNReal.ofReal (∫ x in K, weight C x) := by
  rw [weightedMeasure, withDensity_apply _ hK]
  exact (ofReal_integral_eq_lintegral_ofReal (integrable_weight C).integrableOn
    (Filter.Eventually.of_forall (weight_nonneg C))).symm

/-- A sufficiently large radial cutoff preserves a strict comparison of finite volumes. -/
lemma exists_weightedMeasure_lt {S B : Set E} {R : ℝ}
    (hS : MeasurableSet S) (hB : MeasurableSet B) (hR : 0 ≤ R)
    (hSR : S ⊆ closedBall 0 R) (hBfin : volume B ≠ ⊤)
    (hvol : volume B < volume S) :
    ∃ C : ℝ, R ^ 2 < C ∧ weightedMeasure C B < weightedMeasure C S := by
  have hSfin : volume S ≠ ⊤ :=
    measure_ne_top_of_subset hSR measure_closedBall_lt_top.ne
  let s := (volume S).toReal
  let b := (volume B).toReal
  have hbs : b < s := (ENNReal.toReal_lt_toReal hBfin hSfin).mpr hvol
  have hb : 0 ≤ b := ENNReal.toReal_nonneg
  have hs : 0 ≤ s := ENNReal.toReal_nonneg
  obtain ⟨C, hC⟩ := exists_gt (max (R ^ 2) (R ^ 2 * s / (s - b)))
  have hCR : R ^ 2 < C := (le_max_left _ _).trans_lt hC
  have hC0 : 0 ≤ C := (sq_nonneg R).trans hCR.le
  have hmult : R ^ 2 * s < C * (s - b) :=
    (div_lt_iff₀ (sub_pos.mpr hbs)).mp ((le_max_right _ _).trans_lt hC)
  have hlow : (C - R ^ 2) * s ≤ ∫ x in S, weight C x := by
    have hh := setIntegral_mono_on (integrableOn_const hSfin)
      (integrable_weight C).integrableOn hS (fun x hx => weight_lower hR (hSR hx))
    simpa [integral_const, measureReal_def, smul_eq_mul, mul_comm, s] using hh
  have hupp : (∫ x in B, weight C x) ≤ C * b := by
    have hh := setIntegral_mono_on (integrable_weight C).integrableOn
      (integrableOn_const hBfin) hB (fun x _ => weight_le hC0 x)
    simpa [integral_const, measureReal_def, smul_eq_mul, mul_comm, b] using hh
  have hlt : (∫ x in B, weight C x) < ∫ x in S, weight C x := by
    nlinarith
  refine ⟨C, hCR, ?_⟩
  rw [weightedMeasure_apply C hB, weightedMeasure_apply C hS]
  apply (ENNReal.ofReal_lt_ofReal_iff ?_).mpr hlt
  exact (integral_nonneg (fun x => weight_nonneg C x)).trans_lt hlt

end QuadraticPrecision.IsodiametricWeight
