import Mathlib

/-! Exact constants for the finite-aggregation accuracy bounds. -/

noncomputable section

namespace InfiniteAggregation

def accuracyLowerBound (N : ℕ) : ℝ :=
  Real.sqrt 2 * (Real.log 2) ^ 2 / (1600 * (N : ℝ) ^ 2)

def accuracyUpperBound (N : ℕ) : ℝ :=
  5 * Real.sqrt 2 * Real.pi ^ 2 / (16 * ((N : ℝ) - 1) ^ 2)

theorem log_two_sq_lt_half : (Real.log 2) ^ 2 < (1 / 2 : ℝ) := by
  nlinarith [Real.log_two_lt_d9, Real.log_two_gt_d9]

theorem accuracyLowerBound_pos {N : ℕ} (hN : 0 < N) : 0 < accuracyLowerBound N := by
  unfold accuracyLowerBound
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  positivity

theorem accuracyLowerBound_le_rational {N : ℕ} (hN : 0 < N) :
    accuracyLowerBound N ≤ Real.sqrt 2 / (3200 * (N : ℝ) ^ 2) := by
  have hn : 0 < (N : ℝ) := Nat.cast_pos.2 hN
  unfold accuracyLowerBound
  apply (div_le_div_iff₀ (by positivity) (by positivity)).2
  have h := mul_le_mul_of_nonneg_left log_two_sq_lt_half.le (Real.sqrt_nonneg 2)
  have h' := mul_le_mul_of_nonneg_right h (sq_nonneg (N : ℝ))
  nlinarith

theorem accuracyLowerBound_le_rational_plain {N : ℕ} (hN : 0 < N) :
    accuracyLowerBound N ≤ 1 / (2000 * (N : ℝ) ^ 2) := by
  have hn : 0 < (N : ℝ) := Nat.cast_pos.2 hN
  have hs : Real.sqrt 2 ≤ 3 / 2 := by
    have := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
    nlinarith [Real.sqrt_nonneg 2]
  have hlog := log_two_sq_lt_half.le
  have hnum : Real.sqrt 2 * (Real.log 2) ^ 2 ≤ 3 / 4 := by
    nlinarith [mul_le_mul hlog hs (Real.sqrt_nonneg 2) (by norm_num : (0 : ℝ) ≤ 1 / 2)]
  unfold accuracyLowerBound
  apply (div_le_div_iff₀ (by positivity) (by positivity)).2
  have h := mul_le_mul_of_nonneg_right hnum (sq_nonneg (N : ℝ))
  nlinarith [sq_nonneg (N : ℝ)]

theorem accuracyUpperBound_le_inverse_square {N : ℕ} (hN : 2 ≤ N) :
    accuracyUpperBound N ≤ (5 * Real.sqrt 2 * Real.pi ^ 2 / 4) / (N : ℝ) ^ 2 := by
  have hn : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hnm : 0 < (N : ℝ) - 1 := by linarith
  unfold accuracyUpperBound
  apply (div_le_div_iff₀ (by positivity) (by positivity)).2
  have hsq : (N : ℝ) ^ 2 ≤ 4 * ((N : ℝ) - 1) ^ 2 := by nlinarith
  have h := mul_le_mul_of_nonneg_left hsq
    (show 0 ≤ 5 * Real.sqrt 2 * Real.pi ^ 2 by positivity)
  nlinarith

end InfiniteAggregation
