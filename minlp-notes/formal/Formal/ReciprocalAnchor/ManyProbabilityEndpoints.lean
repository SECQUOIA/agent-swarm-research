import Formal.ReciprocalAnchor.ManyProbability
import Formal.ReciprocalAnchor.ManyLaws

/-! Endpoint-call domination for arbitrary supported probability measures. -/
namespace ReciprocalAnchor.ManyLeaf
open MeasureTheory Set

theorem probability_mean_bounds (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) :
    (∫ x, x ∂μ) ∈ Icc a b := by
  have hi := supported_integrable_id μ h
  constructor
  · have hb := integral_mono_ae (integrable_const a) hi (h.mono fun x hx => hx.1)
    simpa using hb
  · have hb := integral_mono_ae hi (integrable_const b) (h.mono fun x hx => hx.2)
    simpa using hb

/-- Integrating the pointwise chord bound proves domination of every supported law. -/
theorem probabilityCall_le_endpoint_formula (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (hab : a < b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (s : ℝ) :
    probabilityCall μ s ≤
      (b - (∫ x, x ∂μ)) / (b - a) * max (a - s) 0 +
      ((∫ x, x ∂μ) - a) / (b - a) * max (b - s) 0 := by
  have hi := supported_integrable_id μ h
  have hi₀ : Integrable (fun x : ℝ => (b - x) / (b - a) * max (a - s) 0) μ :=
    (((integrable_const b).sub hi).div_const _).mul_const _
  have hi₁ : Integrable (fun x : ℝ => (x - a) / (b - a) * max (b - s) 0) μ :=
    ((hi.sub (integrable_const a)).div_const _).mul_const _
  calc
    _ ≤ ∫ x, (b - x) / (b - a) * max (a - s) 0 +
        (x - a) / (b - a) * max (b - s) 0 ∂μ := by
      apply integral_mono_ae (probabilityCall_integrable μ h s) (hi₀.add hi₁)
      filter_upwards [h] with x hx
      exact call_secant hab hx s
    _ = _ := by
      rw [integral_add hi₀ hi₁]
      simp only [integral_mul_const, integral_div]
      rw [integral_sub (integrable_const b) hi, integral_sub hi (integrable_const a)]
      simp

/-- The dominating expression is the actual finite endpoint law's call function. -/
theorem probabilityCall_le_endpoints (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (hab : a < b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (s : ℝ) :
    probabilityCall μ s ≤
      (Law.endpoints a b (∫ x, x ∂μ) hab
        ⟨(probability_mean_bounds μ h).1, (probability_mean_bounds μ h).2⟩).call s := by
  rw [Law.endpoints_call]
  exact probabilityCall_le_endpoint_formula μ hab h s

end ReciprocalAnchor.ManyLeaf
