import Mathlib

namespace MultilinearGap

/-- A purely arithmetic choice of the number of levels beats any fixed constant.
No asymptotic estimate or logarithm is needed for the disproof. -/
theorem exists_levels (C : ℝ) :
    ∃ L s : ℕ, 2 ≤ L ∧
      C * ((s : ℝ) + 2 * (L : ℝ) / (2 : ℝ)^s) < (L : ℝ) := by
  obtain ⟨k, hk⟩ := exists_nat_gt (max (2 * C) 1)
  have hkC : 2 * C < (k : ℝ) := lt_of_le_of_lt (le_max_left _ _) hk
  have hk1 : 1 < (k : ℝ) := lt_of_le_of_lt (le_max_right _ _) hk
  have hkpos : 0 < k := by exact_mod_cast (lt_trans (by norm_num : (0 : ℝ) < 1) hk1)
  have hp : (k : ℝ) + 1 ≤ (2 : ℝ)^k := by
    exact_mod_cast Nat.succ_le_of_lt (Nat.lt_two_pow_self (n := k))
  have hp2 : ((k : ℝ) + 1)^2 ≤ (2 : ℝ)^(2*k) := by
    rw [show 2*k = k*2 by omega, pow_mul]
    nlinarith [sq_nonneg ((2 : ℝ)^k - ((k : ℝ)+1))]
  refine ⟨2^(2*k), 2*k, ?_, ?_⟩
  · have h := Nat.pow_le_pow_right (by omega : 1 ≤ 2) (by omega : 1 ≤ 2*k)
    simpa using h
  · push_cast
    rw [mul_div_cancel_right₀ _ (by positivity : (2 : ℝ)^(2*k) ≠ 0)]
    nlinarith

end MultilinearGap
