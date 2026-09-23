import Formal.MultilinearGap.IntegratedLaws
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

/-! The normalized shifted harmonic density and exact completion of clipped marginals. -/
namespace MultilinearGap
open MeasureTheory
noncomputable section

/-- Normalizing logarithm of the shifted harmonic density. -/
def floorLog (τ : ℝ) : ℝ := Real.log ((1 + τ) / τ)
/-- A globally nonnegative extension of the density used on the unit interval. -/
def floorDensity (τ t : ℝ) : ℝ := 1 / (floorLog τ * (max 0 t + τ))
/-- Clipped preliminary failure probability. -/
def floorClipped (τ p t : ℝ) : ℝ := min 1 (p * floorDensity τ t)
/-- The preliminary failure marginal. -/
def floorMass (τ p : ℝ) : ℝ := ∫ t in (0 : ℝ)..1, floorClipped τ p t
/-- Exact marginal completion, including the zero-failure case. -/
def floorFailure (τ p t : ℝ) : ℝ := floorClipped τ p t +
  ((p - floorMass τ p) / (1 - floorMass τ p)) * (1 - floorClipped τ p t)

theorem floorLog_pos {τ : ℝ} (hτ : 0 < τ) : 0 < floorLog τ := by
  apply Real.log_pos
  exact (lt_div_iff₀ hτ).mpr (by linarith)

theorem floorDensity_pos {τ : ℝ} (hτ : 0 < τ) (t : ℝ) : 0 < floorDensity τ t := by
  unfold floorDensity
  exact one_div_pos.mpr (mul_pos (floorLog_pos hτ) (by have := le_max_left (0 : ℝ) t; linarith))

theorem floorDensity_nonneg {τ : ℝ} (hτ : 0 < τ) (t : ℝ) : 0 ≤ floorDensity τ t :=
  (floorDensity_pos hτ t).le

theorem floorDensity_of_nonneg (τ : ℝ) {t : ℝ} (ht : 0 ≤ t) :
    floorDensity τ t = 1 / (floorLog τ * (t + τ)) := by
  simp [floorDensity, max_eq_right ht]

theorem continuous_floorDensity {τ : ℝ} (hτ : 0 < τ) : Continuous (floorDensity τ) := by
  unfold floorDensity
  exact continuous_const.div
    (continuous_const.mul ((continuous_const.max continuous_id).add continuous_const))
    (fun t => ne_of_gt (mul_pos (floorLog_pos hτ) (by have := le_max_left (0 : ℝ) t; linarith)))

theorem measurable_floorDensity (τ : ℝ) : Measurable (floorDensity τ) := by
  unfold floorDensity
  exact measurable_const.div (measurable_const.mul
    ((measurable_const.max measurable_id).add measurable_const))

theorem intervalIntegrable_floorDensity {τ : ℝ} (hτ : 0 < τ) (a b : ℝ) :
    IntervalIntegrable (floorDensity τ) volume a b :=
  (continuous_floorDensity hτ).intervalIntegrable a b

theorem integral_floorDensity {τ : ℝ} (hτ : 0 < τ) :
    (∫ t in (0 : ℝ)..1, floorDensity τ t) = 1 := by
  have heq : (∫ t in (0 : ℝ)..1, floorDensity τ t) =
      (floorLog τ)⁻¹ * ∫ t in (0 : ℝ)..1, (t + τ)⁻¹ := by
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_congr
    intro t ht
    rw [floorDensity_of_nonneg τ (by simpa using ht.1)]
    simp [mul_inv_rev, mul_comm]
  rw [heq, intervalIntegral.integral_comp_add_right]
  simp only [zero_add]
  rw [integral_inv_of_pos hτ (by linarith)]
  exact inv_mul_cancel₀ (ne_of_gt (floorLog_pos hτ))

theorem measurable_floorClipped (τ p : ℝ) : Measurable (floorClipped τ p) :=
  measurable_const.min (measurable_const.mul (measurable_floorDensity τ))

theorem floorClipped_mem_unitInterval {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) (t : ℝ) :
    floorClipped τ p t ∈ Set.Icc (0 : ℝ) 1 := by
  exact ⟨le_min (by norm_num) (mul_nonneg hp (floorDensity_pos hτ t).le), min_le_left _ _⟩

theorem intervalIntegrable_floorClipped {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) :
    IntervalIntegrable (floorClipped τ p) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _ (measurable_floorClipped τ p)
    (floorClipped_mem_unitInterval hτ hp)

theorem floorMass_nonneg {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) : 0 ≤ floorMass τ p := by
  exact intervalIntegral.integral_nonneg_of_forall (by norm_num)
    (fun t => (floorClipped_mem_unitInterval hτ hp t).1)

theorem floorMass_le {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) : floorMass τ p ≤ p := by
  calc
    floorMass τ p ≤ ∫ t in (0 : ℝ)..1, p * floorDensity τ t :=
      intervalIntegral.integral_mono_on (by norm_num)
        (intervalIntegrable_floorClipped hτ hp)
        ((intervalIntegrable_floorDensity hτ 0 1).const_mul p)
        (fun t _ => min_le_right _ _)
    _ = p := by rw [intervalIntegral.integral_const_mul, integral_floorDensity hτ, mul_one]

theorem floorCompletion_mem_unitInterval {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) (hp1 : p < 1) :
    (p - floorMass τ p) / (1 - floorMass τ p) ∈ Set.Icc (0 : ℝ) 1 := by
  have hm := floorMass_le hτ hp
  have hd : 0 < 1 - floorMass τ p := by linarith
  exact ⟨div_nonneg (by linarith) hd.le, (div_le_one hd).mpr (by linarith)⟩

theorem floorFailure_ge_clipped {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) (hp1 : p < 1) (t : ℝ) :
    floorClipped τ p t ≤ floorFailure τ p t := by
  unfold floorFailure
  have hc := (floorCompletion_mem_unitInterval hτ hp hp1).1
  have hq := (floorClipped_mem_unitInterval hτ hp t).2
  exact le_add_of_nonneg_right (mul_nonneg hc (sub_nonneg.mpr hq))

theorem floorFailure_mem_unitInterval {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) (hp1 : p < 1)
    (t : ℝ) : floorFailure τ p t ∈ Set.Icc (0 : ℝ) 1 := by
  have hq := floorClipped_mem_unitInterval hτ hp t
  have hc := floorCompletion_mem_unitInterval hτ hp hp1
  refine ⟨hq.1.trans (floorFailure_ge_clipped hτ hp hp1 t), ?_⟩
  unfold floorFailure
  nlinarith [mul_nonneg (sub_nonneg.mpr hc.2) (sub_nonneg.mpr hq.2)]

theorem measurable_floorFailure (τ p : ℝ) : Measurable (floorFailure τ p) :=
  (measurable_floorClipped τ p).add (measurable_const.mul
    (measurable_const.sub (measurable_floorClipped τ p)))

theorem intervalIntegrable_floorFailure {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) (hp1 : p < 1) :
    IntervalIntegrable (floorFailure τ p) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _ (measurable_floorFailure τ p)
    (floorFailure_mem_unitInterval hτ hp hp1)

theorem integral_floorFailure {τ p : ℝ} (hτ : 0 < τ) (hp : 0 ≤ p) (hp1 : p < 1) :
    (∫ t in (0 : ℝ)..1, floorFailure τ p t) = p := by
  have hq := intervalIntegrable_floorClipped hτ hp
  have hd : 1 - floorMass τ p ≠ 0 := by have := floorMass_le hτ hp; linarith
  unfold floorFailure
  rw [intervalIntegral.integral_add hq ((intervalIntegrable_const.sub hq).const_mul _),
    intervalIntegral.integral_const_mul,
    intervalIntegral.integral_sub intervalIntegrable_const hq]
  change floorMass τ p + (p - floorMass τ p) / (1 - floorMass τ p) *
    ((∫ _t in (0 : ℝ)..1, (1 : ℝ)) - floorMass τ p) = p
  simp only [intervalIntegral.integral_const, sub_zero, smul_eq_mul, mul_one]
  rw [div_mul_cancel₀ _ hd]
  ring

end
end MultilinearGap
