import Formal.MultilinearGap.Couplings

/-! Threshold indicator arithmetic used by the globally consistent cubic laws. -/
namespace CubicGap
open MeasureTheory Set MultilinearGap
noncomputable section

/-- Success indicator below a common threshold. -/
def lowerStep (u t : ℝ) : ℝ := if t ≤ u then 1 else 0

theorem lowerStep_mem_Icc (u t : ℝ) : lowerStep u t ∈ Icc (0 : ℝ) 1 := by
  unfold lowerStep
  split <;> norm_num

theorem lowerStep_measurable (u : ℝ) : Measurable (lowerStep u) :=
  Measurable.ite measurableSet_Iic measurable_const measurable_const

theorem lowerStep_integrable (u : ℝ) : IntervalIntegrable (lowerStep u) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _ (lowerStep_measurable u) (lowerStep_mem_Icc u)

theorem integral_lowerStep {u : ℝ} (hu : u ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, lowerStep u t) = u :=
  intervalIntegral_lower_indicator hu

theorem lowerStep_mul (u v t : ℝ) :
    lowerStep u t * lowerStep v t = lowerStep (min u v) t := by
  simp only [lowerStep, le_min_iff]
  split_ifs <;> simp_all

theorem lowerStep_sq (u t : ℝ) : lowerStep u t ^ 2 = lowerStep u t := by
  simpa only [pow_two, min_self] using lowerStep_mul u u t

theorem lowerStep_mul_of_le {u v : ℝ} (huv : u ≤ v) (t : ℝ) :
    lowerStep u t * lowerStep v t = lowerStep u t := by
  rw [lowerStep_mul, min_eq_left huv]

theorem lowerStep_mul_three (u v w t : ℝ) :
    lowerStep u t * lowerStep v t * lowerStep w t = lowerStep (min (min u v) w) t := by
  rw [lowerStep_mul, lowerStep_mul]

theorem integral_lowerStep_mul {u v : ℝ} (hu : u ∈ Icc (0 : ℝ) 1)
    (hv : v ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, lowerStep u t * lowerStep v t) = min u v := by
  simp_rw [lowerStep_mul]
  exact integral_lowerStep ⟨le_min hu.1 hv.1, (min_le_left _ _).trans hu.2⟩

theorem integral_lowerStep_mul_three {u v w : ℝ} (hu : u ∈ Icc (0 : ℝ) 1)
    (hv : v ∈ Icc (0 : ℝ) 1) (hw : w ∈ Icc (0 : ℝ) 1) :
    (∫ t in (0 : ℝ)..1, lowerStep u t * lowerStep v t * lowerStep w t) =
      min (min u v) w := by
  simp_rw [lowerStep_mul_three]
  exact integral_lowerStep
    ⟨le_min (le_min hu.1 hv.1) hw.1, (min_le_left _ _).trans ((min_le_left _ _).trans hu.2)⟩

end
end CubicGap
