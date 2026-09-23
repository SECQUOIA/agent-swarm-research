import Mathlib

/-!
# The scalar residual test

The stored vector may be zero. The displayed scalar is still a minimizer
in that case because every scalar gives the same residual.
-/

namespace QipmFormal.Refresh

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The scalar minimizing `‖a • v - f‖`. -/
def scalarLeastSquares (v f : E) : ℝ := inner ℝ v f / ‖v‖ ^ 2

theorem scalar_residual_sq (v f : E) (a : ℝ) :
    ‖a • v - f‖ ^ 2 = a ^ 2 * ‖v‖ ^ 2 - 2 * a * inner ℝ v f + ‖f‖ ^ 2 := by
  simp only [← real_inner_self_eq_norm_sq, inner_sub_left, inner_sub_right,
    real_inner_smul_left, real_inner_smul_right]
  rw [real_inner_comm f v]
  ring

/-- Completing the square also identifies the exact cost of any other scalar. -/
theorem scalarLeastSquares_sq_identity (v f : E) (a : ℝ) :
    ‖a • v - f‖ ^ 2 =
      ‖scalarLeastSquares v f • v - f‖ ^ 2 +
        (a - scalarLeastSquares v f) ^ 2 * ‖v‖ ^ 2 := by
  by_cases hv : v = 0
  · simp [hv]
  · rw [scalar_residual_sq, scalar_residual_sq]
    unfold scalarLeastSquares
    have hn : ‖v‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hv)
    field_simp
    ring

theorem scalarLeastSquares_minimizes (v f : E) (a : ℝ) :
    ‖scalarLeastSquares v f • v - f‖ ≤ ‖a • v - f‖ := by
  have h := scalarLeastSquares_sq_identity v f a
  have hnonneg := mul_nonneg (sq_nonneg (a - scalarLeastSquares v f)) (sq_nonneg ‖v‖)
  nlinarith [norm_nonneg (scalarLeastSquares v f • v - f), norm_nonneg (a • v - f)]

end

end QipmFormal.Refresh
