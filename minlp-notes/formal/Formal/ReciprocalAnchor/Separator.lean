import Mathlib

namespace ReciprocalAnchor

noncomputable section

def tangentDeficit (x a : ℝ) : ℝ := (x - a) ^ 2 / (x * a ^ 2)

def g₁ (m q w : ℝ) : ℝ := 2 - m - (6 / 5) * q + (21 / 25) * w

def g₂ (m q w : ℝ) : ℝ := 5 / 3 - (25 / 36) * m - (29 / 30) * q + (2059 / 3600) * w

theorem quadratic_certificate (C H x : ℝ) (hc : 0 < C) (hd : H ^ 2 ≤ 8 * C) :
    0 ≤ C * x ^ 2 - H * x + 2 := by
  have h := sq_nonneg (2 * C * x - H)
  have he : 0 ≤ 4 * C * (C * x ^ 2 - H * x + 2) := by nlinarith
  exact nonneg_of_mul_nonneg_right he (by positivity)

theorem pair_deficit_bound (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0)
    (hc : 0 < 1 / a ^ 2 + 1 / b ^ 2)
    (hd : (2 / a + 2 / b + 1 / 400) ^ 2 ≤ 8 * (1 / a ^ 2 + 1 / b ^ 2))
    {x : ℝ} (hx : 0 < x) :
    (1 / 400 : ℝ) ≤ tangentDeficit x a + tangentDeficit x b := by
  have hq := quadratic_certificate (1 / a ^ 2 + 1 / b ^ 2)
    (2 / a + 2 / b + 1 / 400) x hc hd
  have he : tangentDeficit x a + tangentDeficit x b =
      ((1 / a ^ 2 + 1 / b ^ 2) * x ^ 2 - (2 / a + 2 / b) * x + 2) / x := by
    unfold tangentDeficit
    field_simp
    ring
  rw [he]
  apply (le_div_iff₀ hx).mpr
  nlinarith

theorem four_pair_bounds {x : ℝ} (hx : 0 < x) :
    (1 / 400 : ℝ) ≤ tangentDeficit x 1 + tangentDeficit x (6 / 5) ∧
    (1 / 400 : ℝ) ≤ tangentDeficit x 1 + tangentDeficit x (20 / 7) ∧
    (1 / 400 : ℝ) ≤ tangentDeficit x (5 / 2) + tangentDeficit x (6 / 5) ∧
    (1 / 400 : ℝ) ≤ tangentDeficit x (5 / 2) + tangentDeficit x (20 / 7) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    apply pair_deficit_bound <;> first | exact hx | norm_num

theorem first_deficit_identity {x : ℝ} (hx : x ≠ 0) (y : ℝ) :
    1 / x - g₁ x y (x*y) = (1-y) * tangentDeficit x 1 + y * tangentDeficit x (5 / 2) := by
  unfold g₁ tangentDeficit
  field_simp
  ring

theorem second_deficit_identity {x : ℝ} (hx : x ≠ 0) (y : ℝ) :
    1 / x - g₂ x y (x*y) = (1-y) * tangentDeficit x (6 / 5) + y * tangentDeficit x (20 / 7) := by
  unfold g₂ tangentDeficit
  field_simp
  ring

/-- The joint cut is valid at every original two-leaf point, even without an upper bound on X. -/
theorem joint_cut_pointwise {x y z : ℝ} (hx : 0 < x)
    (hy0 : 0 ≤ y) (hy1 : y ≤ 1) (hz0 : 0 ≤ z) (hz1 : z ≤ 1) :
    g₁ x y (x*y) + g₂ x z (x*z) + 1 / 400 ≤ 2 / x := by
  obtain ⟨h00, h01, h10, h11⟩ := four_pair_bounds hx
  have w00 : 0 ≤ (1-y)*(1-z) := mul_nonneg (by linarith) (by linarith)
  have w01 : 0 ≤ (1-y)*z := mul_nonneg (by linarith) hz0
  have w10 : 0 ≤ y*(1-z) := mul_nonneg hy0 (by linarith)
  have w11 : 0 ≤ y*z := mul_nonneg hy0 hz0
  have h := add_le_add
    (add_le_add (mul_le_mul_of_nonneg_left h00 w00) (mul_le_mul_of_nonneg_left h01 w01))
    (add_le_add (mul_le_mul_of_nonneg_left h10 w10) (mul_le_mul_of_nonneg_left h11 w11))
  have he := first_deficit_identity (ne_of_gt hx) y
  have hf := second_deficit_identity (ne_of_gt hx) z
  have hb : (1 / 400 : ℝ) ≤ (1-y)*tangentDeficit x 1 + y*tangentDeficit x (5 / 2) +
      (1-z)*tangentDeficit x (6 / 5) + z*tangentDeficit x (20 / 7) := by
    nlinarith only [h]
  rw [show (2 : ℝ) / x = 1 / x + 1 / x by ring]
  linarith only [he, hf, hb]

theorem incompatible_point_cut_violation :
    (2 : ℝ) * (3 / 5) < g₁ 2 (2 / 3) (5 / 3) + g₂ 2 (14 / 29) (40 / 29) + 1 / 400 := by
  norm_num [g₁, g₂]

end
end ReciprocalAnchor
