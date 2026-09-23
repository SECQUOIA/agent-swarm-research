import Mathlib

/-! Call functions of arbitrary probability measures supported on a compact interval. -/
namespace ReciprocalAnchor.ManyLeaf
open MeasureTheory Set

/-- The call function, with no finite-support restriction. -/
noncomputable def probabilityCall (μ : Measure ℝ) (s : ℝ) : ℝ := ∫ x, max (x - s) 0 ∂μ

theorem supported_integrable_id (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) : Integrable (fun x : ℝ => x) μ := by
  apply (integrable_const (|a| + |b|)).mono' measurable_id.aestronglyMeasurable
  filter_upwards [h] with x hx
  rw [Real.norm_eq_abs, abs_le]
  simp only [id_eq] at *
  constructor <;> have ha := le_abs_self a <;> have hb := le_abs_self b
  · have ha' := neg_abs_le a
    linarith [abs_nonneg b, hx.1]
  · linarith [abs_nonneg a, hx.2]

theorem probabilityCall_integrable (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (s : ℝ) :
    Integrable (fun x => max (x - s) 0) μ := by
  apply ((supported_integrable_id μ h).sub (integrable_const s)).norm.mono'
    (by fun_prop)
  filter_upwards [] with x
  simp only [Real.norm_eq_abs, abs_of_nonneg (le_max_right (x - s) 0)]
  exact max_le (le_abs_self _) (abs_nonneg _)

theorem probabilityCall_nonneg (μ : Measure ℝ) (s : ℝ) : 0 ≤ probabilityCall μ s :=
  integral_nonneg (fun _ => le_max_right _ _)

theorem probabilityCall_left (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b s : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (hs : s ≤ a) :
    probabilityCall μ s = (∫ x, x ∂μ) - s := by
  unfold probabilityCall
  calc
    _ = ∫ x, x - s ∂μ := integral_congr_ae (by
      filter_upwards [h] with x hx
      exact max_eq_left (by linarith [hx.1]))
    _ = _ := by rw [integral_sub (supported_integrable_id μ h) (integrable_const s)]; simp

theorem probabilityCall_right (μ : Measure ℝ) {a b s : ℝ}
    (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (hs : b ≤ s) : probabilityCall μ s = 0 := by
  unfold probabilityCall
  calc
    _ = ∫ _ : ℝ, (0 : ℝ) ∂μ := integral_congr_ae (by
      filter_upwards [h] with x hx
      exact max_eq_right (by linarith [hx.2]))
    _ = 0 := integral_zero _ _

/-- The mean supplies a universal lower bound on the probability call function. -/
theorem probabilityCall_mean_lower (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (s : ℝ) :
    (∫ x, x ∂μ) - s ≤ probabilityCall μ s := by
  have hi := supported_integrable_id μ h
  calc
    _ = ∫ x, x - s ∂μ := by rw [integral_sub hi (integrable_const s)]; simp
    _ ≤ _ := integral_mono (hi.sub (integrable_const s))
      (probabilityCall_integrable μ h s) (fun x => le_max_left _ _)

/-- Secant slopes lie between minus one and zero. -/
theorem probabilityCall_slope (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b s t : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (hst : s ≤ t) :
    -(t - s) ≤ probabilityCall μ t - probabilityCall μ s ∧
      probabilityCall μ t - probabilityCall μ s ≤ 0 := by
  have hi := probabilityCall_integrable μ h s
  have hj := probabilityCall_integrable μ h t
  have hle : probabilityCall μ t ≤ probabilityCall μ s := by
    apply integral_mono hj hi
    intro x
    exact max_le_max (by linarith) le_rfl
  have hlo : probabilityCall μ s ≤ probabilityCall μ t + (t - s) := by
    calc
      _ ≤ ∫ x, max (x - t) 0 + (t - s) ∂μ := by
        apply integral_mono hi (hj.add (integrable_const _))
        intro x
        simp only [Pi.add_apply]
        apply max_le
        · linarith [le_max_left (x - t) 0]
        · linarith [le_max_right (x - t) 0]
      _ = _ := by rw [integral_add hj (integrable_const _)]; simp [probabilityCall]
  constructor <;> linarith

theorem probabilityCall_convex (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) :
    ConvexOn ℝ univ (probabilityCall μ) := by
  refine ⟨convex_univ, ?_⟩
  intro s _ t _ u v hu hv huv
  simp only [smul_eq_mul]
  have hi := probabilityCall_integrable μ h s
  have hj := probabilityCall_integrable μ h t
  calc
    _ ≤ ∫ x, u * max (x - s) 0 + v * max (x - t) 0 ∂μ := by
      apply integral_mono (probabilityCall_integrable μ h _) ((hi.const_mul u).add (hj.const_mul v))
      intro x
      simp only [Pi.add_apply]
      apply max_le
      · have h1 := mul_le_mul_of_nonneg_left (le_max_left (x - s) 0) hu
        have h2 := mul_le_mul_of_nonneg_left (le_max_left (x - t) 0) hv
        nlinarith [congrArg (fun z : ℝ => z * x) huv]
      · positivity
    _ = _ := by
      rw [integral_add (hi.const_mul u) (hj.const_mul v)]
      simp [probabilityCall, integral_const_mul]

theorem probability_selection_integrable (μ : Measure ℝ) [IsProbabilityMeasure μ]
    (θ : ℝ → ℝ) (hθm : AEStronglyMeasurable θ μ)
    (hθ : ∀ᵐ x ∂μ, θ x ∈ Icc (0 : ℝ) 1) : Integrable θ μ := by
  apply (integrable_const (1 : ℝ)).mono' hθm
  filter_upwards [hθ] with x hx
  simpa [Real.norm_eq_abs, abs_of_nonneg hx.1] using hx.2

theorem probability_selection_moment_integrable (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (θ : ℝ → ℝ)
    (hθm : AEStronglyMeasurable θ μ) (hθ : ∀ᵐ x ∂μ, θ x ∈ Icc (0 : ℝ) 1) :
    Integrable (fun x => x * θ x) μ := by
  apply (supported_integrable_id μ h).norm.mono' (measurable_id.aestronglyMeasurable.mul hθm)
  filter_upwards [hθ] with x hx
  change ‖x * θ x‖ ≤ ‖x‖
  rw [norm_mul, Real.norm_eq_abs (θ x), abs_of_nonneg hx.1]
  exact mul_le_of_le_one_right (norm_nonneg _) hx.2

/-- Every measurable fractional selection satisfies the threshold upper bound. -/
theorem probability_selection_bound (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (θ : ℝ → ℝ)
    (hθm : AEStronglyMeasurable θ μ) (hθ : ∀ᵐ x ∂μ, θ x ∈ Icc (0 : ℝ) 1)
    (s : ℝ) :
    (∫ x, x * θ x ∂μ) ≤ (∫ x, θ x ∂μ) * s + probabilityCall μ s := by
  have hiθ : Integrable θ μ := (integrable_const (1 : ℝ)).mono' hθm (by
    filter_upwards [hθ] with x hx
    simpa [Real.norm_eq_abs, abs_of_nonneg hx.1] using hx.2)
  have hi : Integrable (fun x => x * θ x) μ :=
    (supported_integrable_id μ h).norm.mono' (measurable_id.aestronglyMeasurable.mul hθm) (by
      filter_upwards [hθ] with x hx
      rw [norm_mul, Real.norm_eq_abs (θ x), abs_of_nonneg hx.1]
      exact mul_le_of_le_one_right (norm_nonneg _) hx.2)
  calc
    _ ≤ ∫ x, θ x * s + max (x - s) 0 ∂μ := by
      apply integral_mono_ae hi ((hiθ.mul_const s).add (probabilityCall_integrable μ h s))
      filter_upwards [hθ] with x hx
      simp only [Pi.add_apply]
      by_cases hs : 0 ≤ x - s
      · rw [max_eq_left hs]
        nlinarith [mul_nonneg hs (sub_nonneg.mpr hx.2)]
      · rw [max_eq_right (le_of_not_ge hs)]
        nlinarith [mul_nonpos_of_nonpos_of_nonneg (le_of_not_ge hs) hx.1]
    _ = _ := by rw [integral_add (hiθ.mul_const s) (probabilityCall_integrable μ h s)];
                simp [probabilityCall, integral_mul_const]

end ReciprocalAnchor.ManyLeaf
