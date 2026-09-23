import Formal.ReciprocalAnchor.ManyProbability
import Formal.ReciprocalAnchor.ManyIntegrals

/-! The reciprocal call identity for arbitrary compactly supported probability laws. -/
namespace ReciprocalAnchor.ManyLeaf
open MeasureTheory Set

/-- Bounded positive support justifies Fubini for arbitrary probability laws. -/
theorem probability_reciprocal_fubini (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b) :
    (∫ x, (∫ s in a..b, 2 * max (x - s) 0 / s ^ 3) ∂μ) =
      ∫ s in a..b, 2 * probabilityCall μ s / s ^ 3 := by
  let f : ℝ × ℝ → ℝ := fun z => 2 * max (z.2 - z.1) 0 / z.1 ^ 3
  have hc : ContinuousOn f (Icc a b ×ˢ Icc a b) := by
    apply ContinuousOn.div
    · fun_prop
    · fun_prop
    · intro z hz
      exact pow_ne_zero 3 (ne_of_gt (ha.trans_le hz.1.1))
  have hi : Integrable f ((volume.restrict (uIoc a b)).prod μ) := by
    have hi := hc.integrableOn_compact (μ := volume.prod μ) (isCompact_Icc.prod isCompact_Icc)
    have hr := Measure.restrict_eq_self_of_ae_mem h
    rw [uIoc_of_le hab, ← hr, Measure.prod_restrict]
    exact hi.mono_set (prod_mono Ioc_subset_Icc_self Subset.rfl)
  calc
    _ = ∫ s in a..b, ∫ x, 2 * max (x - s) 0 / s ^ 3 ∂μ :=
      (intervalIntegral_integral_swap hi).symm
    _ = _ := by
      apply intervalIntegral.integral_congr
      intro s _
      simp only [integral_div, integral_const_mul, probabilityCall]

/-- Formula (6) for every probability law supported on the positive interval. -/
theorem probability_reciprocal_identity (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b) :
    (∫ x, 1 / x ∂μ) = 1 / a - ((∫ x, x ∂μ) - a) / a ^ 2 +
      ∫ s in a..b, 2 * probabilityCall μ s / s ^ 3 := by
  have hi := supported_integrable_id μ h
  have hr : Integrable (fun x : ℝ => 1 / x) μ := by
    have hc : ContinuousOn (fun x : ℝ => 1 / x) (Icc a b) := by
      exact continuousOn_const.div continuousOn_id (fun x hx => ne_of_gt (ha.trans_le hx.1))
    have hh := hc.integrableOn_Icc (μ := μ)
    rwa [IntegrableOn, Measure.restrict_eq_self_of_ae_mem h] at hh
  have he : (fun x : ℝ => ∫ s in a..b, 2 * max (x - s) 0 / s ^ 3) =ᵐ[μ]
      (fun x => 1 / x - (1 / a - (x - a) / a ^ 2)) := by
    filter_upwards [h] with x hx
    linarith [reciprocal_call_identity ha hx.1 hx.2]
  have ht : Integrable (fun x : ℝ => 1 / a - (x - a) / a ^ 2) μ :=
    (integrable_const _).sub ((hi.sub (integrable_const _)).div_const _)
  have hj : Integrable (fun x : ℝ => ∫ s in a..b, 2 * max (x - s) 0 / s ^ 3) μ :=
    (hr.sub ht).congr he.symm
  calc
    _ = ∫ x, (1 / a - (x - a) / a ^ 2) +
        (∫ s in a..b, 2 * max (x - s) 0 / s ^ 3) ∂μ := integral_congr_ae (by
      filter_upwards [h] with x hx
      exact reciprocal_call_identity ha hx.1 hx.2)
    _ = _ := by
      rw [integral_add ht hj, probability_reciprocal_fubini μ ha hab h]
      congr 1
      have ht0 : Integrable (fun x : ℝ => (x - a) / a ^ 2) μ :=
        (hi.sub (integrable_const a)).div_const _
      rw [integral_sub (integrable_const (1 / a)) ht0]
      simp only [integral_div]
      rw [integral_sub hi (integrable_const a)]
      simp

end ReciprocalAnchor.ManyLeaf
