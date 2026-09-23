import Mathlib.MeasureTheory.Integral.IntegrableOn
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
import Mathlib.Tactic

open Set MeasureTheory
open scoped ENNReal

namespace QuadraticPrecision.Polarization

variable {E : Type*} [MeasurableSpace E]

/-- Move singly occupied reflection pairs into the preferred halfspace. -/
def polarize (r : E → E) (H K : Set E) : Set E :=
  (K ∩ r ⁻¹' K) ∪ ((K ∪ r ⁻¹' K) ∩ H)

theorem measurableSet_polarize {r : E → E} {H K : Set E}
    (hr : Measurable r) (hH : MeasurableSet H) (hK : MeasurableSet K) :
    MeasurableSet (polarize r H K) :=
  (hK.inter (hr hK)).union ((hK.union (hr hK)).inter hH)

omit [MeasurableSpace E] in
theorem pair_indicator {r : E → E} (hr : Function.Involutive r)
    (H K : Set E) (x : E) (hH : r x ∈ H ↔ x ∉ H) :
    (polarize r H K).indicator (fun _ => (1 : ℝ≥0∞)) x +
      (polarize r H K).indicator (fun _ => (1 : ℝ≥0∞)) (r x) =
    K.indicator (fun _ => (1 : ℝ≥0∞)) x +
      K.indicator (fun _ => (1 : ℝ≥0∞)) (r x) := by
  classical
  by_cases hx : x ∈ K <;> by_cases hrx : r x ∈ K <;> by_cases hh : x ∈ H <;>
    simp [polarize, indicator, hx, hrx, hh, hH, hr x]

omit [MeasurableSpace E] in
theorem pair_weight_le {r : E → E} (hr : Function.Involutive r)
    (H K : Set E) (w : E → ℝ) (x : E) (hH : r x ∈ H ↔ x ∉ H)
    (hw : x ∈ H → w (r x) ≤ w x) (hwr : r x ∈ H → w x ≤ w (r x)) :
    K.indicator w x + K.indicator w (r x) ≤
      (polarize r H K).indicator w x + (polarize r H K).indicator w (r x) := by
  classical
  by_cases hx : x ∈ K <;> by_cases hrx : r x ∈ K <;> by_cases hh : x ∈ H <;>
    simp_all [polarize, indicator, hr x]

omit [MeasurableSpace E] in
theorem pair_weight_lt {r : E → E} (hr : Function.Involutive r)
    (H K : Set E) (w : E → ℝ) (x : E) (hH : r x ∈ H ↔ x ∉ H)
    (hx : x ∉ K) (hrx : r x ∈ K) (hh : x ∈ H) (hw : w (r x) < w x) :
    K.indicator w x + K.indicator w (r x) <
      (polarize r H K).indicator w x + (polarize r H K).indicator w (r x) := by
  classical
  simpa [polarize, indicator, hx, hrx, hh, hH, hr x] using hw

theorem measure_polarize {μ : Measure E} (r : E ≃ᵐ E)
    (hr : Function.Involutive r) (hm : MeasurePreserving r μ μ)
    {H K : Set E} (hH : MeasurableSet H) (hK : MeasurableSet K)
    (horient : ∀ᵐ x ∂μ, r x ∈ H ↔ x ∉ H) : μ (polarize r H K) = μ K := by
  have hP := measurableSet_polarize r.measurable hH hK
  have heq := lintegral_congr_ae (horient.mono fun x hx => pair_indicator hr H K x hx)
  rw [lintegral_add_left ((measurable_const.indicator hP)),
    lintegral_add_left ((measurable_const.indicator hK)),
    hm.lintegral_comp (measurable_const.indicator hP),
    hm.lintegral_comp (measurable_const.indicator hK)] at heq
  simp only [lintegral_indicator_const hP, lintegral_indicator_const hK, one_mul,
    ← mul_two] at heq
  exact (ENNReal.mul_left_inj (by norm_num) (by norm_num)).mp heq

theorem integral_polarize_le {μ : Measure E} (r : E ≃ᵐ E)
    (hr : Function.Involutive r) (hm : MeasurePreserving r μ μ)
    {H K : Set E} (hH : MeasurableSet H) (hK : MeasurableSet K)
    (horient : ∀ᵐ x ∂μ, r x ∈ H ↔ x ∉ H)
    (w : E → ℝ) (hwi : Integrable w μ)
    (hw : ∀ x ∈ H, w (r x) ≤ w x) :
    (∫ x, K.indicator w x ∂μ) ≤ ∫ x, (polarize r H K).indicator w x ∂μ := by
  have hKi := hwi.indicator hK
  have hPi := hwi.indicator (measurableSet_polarize r.measurable hH hK)
  have hKr : Integrable (fun x => K.indicator w (r x)) μ :=
    (hm.integrable_comp_emb r.measurableEmbedding).mpr hKi
  have hPr : Integrable (fun x => (polarize r H K).indicator w (r x)) μ :=
    (hm.integrable_comp_emb r.measurableEmbedding).mpr hPi
  have hle := integral_mono_ae (hKi.add hKr) (hPi.add hPr)
    (horient.mono fun x hx => pair_weight_le hr H K w x hx (hw x)
      (fun hh => by simpa only [hr x] using hw (r x) hh))
  simp only [Pi.add_apply] at hle
  simp only [integral_add hKi hKr, integral_add hPi hPr,
    hm.integral_comp'] at hle
  linarith

/-- A positive-measure set of strictly improved pairs makes the weighted gain strict. -/
theorem integral_polarize_lt {μ : Measure E} (r : E ≃ᵐ E)
    (hr : Function.Involutive r) (hm : MeasurePreserving r μ μ)
    {H K : Set E} (hH : MeasurableSet H) (hK : MeasurableSet K)
    (horient : ∀ᵐ x ∂μ, r x ∈ H ↔ x ∉ H)
    (w : E → ℝ) (hwi : Integrable w μ)
    (hw : ∀ x ∈ H, w (r x) ≤ w x)
    (hpos : 0 < μ {x | x ∈ H ∧ x ∉ K ∧ r x ∈ K ∧ w (r x) < w x}) :
    (∫ x, K.indicator w x ∂μ) < ∫ x, (polarize r H K).indicator w x ∂μ := by
  let f := fun x => K.indicator w x + K.indicator w (r x)
  let g := fun x => (polarize r H K).indicator w x +
    (polarize r H K).indicator w (r x)
  have hKi := hwi.indicator hK
  have hPi := hwi.indicator (measurableSet_polarize r.measurable hH hK)
  have hKr : Integrable (fun x => K.indicator w (r x)) μ :=
    (hm.integrable_comp_emb r.measurableEmbedding).mpr hKi
  have hPr : Integrable (fun x => (polarize r H K).indicator w (r x)) μ :=
    (hm.integrable_comp_emb r.measurableEmbedding).mpr hPi
  have hfi : Integrable f μ := hKi.add hKr
  have hgi : Integrable g μ := hPi.add hPr
  have hnonneg : ∀ᵐ x ∂μ, 0 ≤ (g - f) x := horient.mono fun x hx => by
    exact sub_nonneg.mpr (pair_weight_le hr H K w x hx (hw x)
      (fun hh => by simpa only [hr x] using hw (r x) hh))
  have hsupport : 0 < μ (Function.support (g - f)) := by
    apply lt_of_lt_of_le hpos
    apply measure_mono_ae
    filter_upwards [horient] with x hx
    intro hmem
    have hlt := pair_weight_lt hr H K w x hx hmem.2.1 hmem.2.2.1
      hmem.1 hmem.2.2.2
    exact sub_ne_zero.mpr (ne_of_gt hlt)
  have hgain := (integral_pos_iff_support_of_nonneg_ae hnonneg (hgi.sub hfi)).mpr hsupport
  simp only [Pi.sub_apply] at hgain
  rw [integral_sub hgi hfi] at hgain
  dsimp [g, f] at hgain
  rw [integral_add hPi hPr, integral_add hKi hKr,
    hm.integral_comp', hm.integral_comp'] at hgain
  linarith

end QuadraticPrecision.Polarization
