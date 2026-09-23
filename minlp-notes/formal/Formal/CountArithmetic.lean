import Mathlib

namespace ExactCounts

/-- The least number of binary coordinates that can distinguish all ternary contacts. -/
def binaryCount (n : ℕ) : ℕ := Nat.clog 2 (3 ^ n)

lemma binaryCount_le_iff {n p : ℕ} : binaryCount n ≤ p ↔ 3 ^ n ≤ 2 ^ p := by
  exact Nat.clog_le_iff_le_pow (by decide)

/-- The integer counting definition equals the usual logarithmic count formula. -/
theorem binaryCount_eq_natCeil (n : ℕ) :
    binaryCount n = ⌈(n : ℝ) * Real.logb 2 3⌉₊ := by
  rw [binaryCount, ← Real.natCeil_logb_natCast]
  simp only [Nat.cast_pow, Nat.cast_ofNat, Real.logb_pow]

/-- The same formula with the usual integer-valued ceiling. -/
theorem binaryCount_eq_intCeil (n : ℕ) :
    (binaryCount n : ℤ) = ⌈(n : ℝ) * Real.logb 2 3⌉ := by
  rw [binaryCount_eq_natCeil]
  apply Int.natCast_ceil_eq_ceil
  exact mul_nonneg (Nat.cast_nonneg _)
    (Real.logb_pos (by norm_num : (1 : ℝ) < 2) (by norm_num : (1 : ℝ) < 3)).le

@[simp] theorem binaryCount_zero : binaryCount 0 = 0 := by
  norm_num [binaryCount]

@[simp] theorem binaryCount_one : binaryCount 1 = 2 := by
  decide

/-- Every nonempty product needs strictly more binary than general-integer coordinates. -/
theorem lt_binaryCount {n : ℕ} (hn : 1 ≤ n) : n < binaryCount n := by
  apply (Nat.lt_clog_iff_pow_lt (by decide : 1 < 2)).mpr
  exact Nat.pow_lt_pow_left (by decide : 2 < 3) (by omega : n ≠ 0)

end ExactCounts
