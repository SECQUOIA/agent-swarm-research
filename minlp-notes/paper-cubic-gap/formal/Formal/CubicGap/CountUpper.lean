import Formal.CubicGap.Finite
import Mathlib

namespace CubicGap

/-- Normalized nonconstant binomial counts increase with the available population. -/
theorem choose_count_upper {k m d : ℕ} (hkm : k ≤ m) (hd : 0 < d) :
    m * k.choose d ≤ k * m.choose d := by
  have hk := Nat.choose_mul (n := k) (Nat.succ_le_of_lt hd)
  have hm := Nat.choose_mul (n := m) (Nat.succ_le_of_lt hd)
  simp only [Nat.choose_one_right] at hk hm
  have hmono := Nat.choose_le_choose (d - 1) (Nat.sub_le_sub_right hkm 1)
  apply Nat.le_of_mul_le_mul_left (c := d) _ hd
  calc
    d * (m * k.choose d) = m * (k.choose d * d) := by ring
    _ = m * (k * (k - 1).choose (d - 1)) := by rw [hk]
    _ ≤ m * (k * (m - 1).choose (d - 1)) := by gcongr
    _ = k * (m * (m - 1).choose (d - 1)) := by ring
    _ = d * (k * m.choose d) := by rw [← hm]; ring

/-- Rational form of the normalized count inequality. -/
theorem choose_count_upper_rat {k m d : ℕ} (hkm : k ≤ m) (hm : 0 < m) (hd : 0 < d) :
    (k.choose d : ℚ) ≤ (m.choose d : ℚ) / m * k := by
  have hm' : (0 : ℚ) < m := by exact_mod_cast hm
  have h : (m : ℚ) * k.choose d ≤ (k : ℚ) * m.choose d := by
    exact_mod_cast choose_count_upper hkm hd
  calc
    (k.choose d : ℚ) ≤ ((k : ℚ) * m.choose d) / m := by
      apply (le_div_iff₀ hm').mpr
      simpa [mul_comm] using h
    _ = _ := by ring

/-- A linear upper bound for the two-group polynomial at every binary count pair. -/
theorem twoValue_upper {m a c : ℕ} (ha : a ≤ m) (hc : c ≤ m) :
    twoValue m a c ≤ (9 / 4 : ℚ) * m.choose 2 * a := by
  have h₂ : (m : ℚ) * a.choose 2 ≤ (a : ℚ) * m.choose 2 := by
    exact_mod_cast choose_count_upper ha (by decide : 0 < 2)
  have hmono : (c.choose 2 : ℚ) ≤ m.choose 2 := by
    exact_mod_cast Nat.choose_le_choose 2 hc
  have hac := mul_le_mul_of_nonneg_left hmono (show (0 : ℚ) ≤ a by positivity)
  unfold twoValue
  nlinarith

/-- A linear upper bound for every nonnegative six-orbit coefficient vector. -/
theorem countPhi_upper {m a b c : ℕ} (hm : 0 < m)
    (ha : a ≤ m) (hb : b ≤ m) (hc : c ≤ m)
    (coef : Fin 6 → ℚ) (hcoef : ∀ i, 0 ≤ coef i) :
    countPhi coef a b c ≤
      coef 0 * (m.choose 3 : ℚ) / m * c + coef 1 * (m.choose 2 : ℚ) * b +
      coef 2 * (m.choose 2 : ℚ) / m * b + (coef 3 + coef 4) * m * a +
      coef 5 * (m.choose 2 : ℚ) / m * a := by
  have h₀ := mul_le_mul_of_nonneg_left (choose_count_upper_rat hc hm (by decide : 0 < 3)) (hcoef 0)
  have h₂ := mul_le_mul_of_nonneg_left (choose_count_upper_rat hb hm (by decide : 0 < 2)) (hcoef 2)
  have h₅ := mul_le_mul_of_nonneg_left (choose_count_upper_rat ha hm (by decide : 0 < 2)) (hcoef 5)
  have hc₂ : (c.choose 2 : ℚ) ≤ m.choose 2 := by
    exact_mod_cast Nat.choose_le_choose 2 hc
  have h₁ := mul_le_mul_of_nonneg_left hc₂
    (mul_nonneg (hcoef 1) (show (0 : ℚ) ≤ b by positivity))
  have hb' : (b : ℚ) ≤ m := by exact_mod_cast hb
  have hc' : (c : ℚ) ≤ m := by exact_mod_cast hc
  have h₃ := mul_le_mul_of_nonneg_left hc'
    (mul_nonneg (hcoef 3) (show (0 : ℚ) ≤ a by positivity))
  have h₄ := mul_le_mul_of_nonneg_left hb'
    (mul_nonneg (hcoef 4) (show (0 : ℚ) ≤ a by positivity))
  unfold countPhi
  calc
    _ ≤ coef 0 * ((m.choose 3 : ℚ) / m * c) + coef 1 * b * m.choose 2 +
        coef 2 * ((m.choose 2 : ℚ) / m * b) + coef 3 * a * m + coef 4 * a * m +
        coef 5 * ((m.choose 2 : ℚ) / m * a) := by linarith
    _ = _ := by ring

end CubicGap
