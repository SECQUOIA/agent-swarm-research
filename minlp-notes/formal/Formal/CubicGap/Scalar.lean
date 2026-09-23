import Mathlib

namespace CubicGap

noncomputable section

def scalarValue (a c : ℝ) : ℝ := a * c ^ 2 + 5 / 4 * a ^ 2

def scalarAffine (a c : ℝ) : ℝ := 11 * a / 6 + 20 * c / 27 - 95 / 108

/-- Exact polynomial certificate for the two-level scalar minorant. -/
theorem scalar_residual (a c : ℝ) :
    scalarValue a c - scalarAffine a c =
      5 / 4 * (a - (11 - 6 * c ^ 2) / 15) ^ 2 +
      (1 - c) * (3 * c - 2) ^ 2 * (3 * c + 7) / 135 := by
  unfold scalarValue scalarAffine
  ring

/-- The affine minorant holds on the entire square, not merely a finite grid. -/
theorem scalar_minorant (a c : ℝ) (hc0 : 0 ≤ c) (hc1 : c ≤ 1) :
    scalarAffine a c ≤ scalarValue a c := by
  have h : 0 ≤ scalarValue a c - scalarAffine a c := by
    rw [scalar_residual]
    have : 0 ≤ 1 - c := sub_nonneg.mpr hc1
    positivity
  linarith

theorem scalar_attaining_atoms :
    scalarValue (1 / 3) 1 = scalarAffine (1 / 3) 1 ∧
    scalarValue (5 / 9) (2 / 3) = scalarAffine (5 / 9) (2 / 3) ∧
    (1 / 4 : ℝ) * (1 / 3) + (3 / 4) * (5 / 9) = 1 / 2 ∧
    (1 / 4 : ℝ) * 1 + (3 / 4) * (2 / 3) = 3 / 4 ∧
    (1 / 4 : ℝ) * scalarValue (1 / 3) 1 +
      (3 / 4) * scalarValue (5 / 9) (2 / 3) = 16 / 27 := by
  norm_num [scalarValue, scalarAffine]

/-- Every finitely supported law with the prescribed two means obeys the bound. -/
theorem scalar_expectation_lower {ι : Type*} [Fintype ι]
    (w a c : ι → ℝ) (hw : ∀ i, 0 ≤ w i) (hmass : ∑ i, w i = 1)
    (hc0 : ∀ i, 0 ≤ c i) (hc1 : ∀ i, c i ≤ 1)
    (ha : ∑ i, w i * a i = 1 / 2) (hc : ∑ i, w i * c i = 3 / 4) :
    16 / 27 ≤ ∑ i, w i * scalarValue (a i) (c i) := by
  have h := Finset.sum_le_sum (s := Finset.univ) (fun i _ =>
    mul_le_mul_of_nonneg_left (scalar_minorant (a i) (c i) (hc0 i) (hc1 i)) (hw i))
  have he : ∑ i, w i * scalarAffine (a i) (c i) = 16 / 27 := by
    simp only [scalarAffine]
    simp_rw [show ∀ i, w i * (11 * a i / 6 + 20 * c i / 27 - 95 / 108) =
      (11 / 6) * (w i * a i) + (20 / 27) * (w i * c i) - (95 / 108) * w i
      from fun i => by ring]
    rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum,
      ← Finset.mul_sum, ← Finset.mul_sum, ha, hc, hmass]
    norm_num
  rwa [he] at h

end
end CubicGap
