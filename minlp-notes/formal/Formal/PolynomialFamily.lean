import Formal.Model

namespace ExactCounts

open Polynomial

/-- A single rational polynomial specifies every first output, independently of dimension. -/
noncomputable def leftPoly : ℚ[X] := C (7 / 4) * (1 - X) ^ 32

/-- A single rational polynomial specifies every second output, independently of dimension. -/
noncomputable def rightPoly : ℚ[X] := C (7 / 4) * X ^ 32

@[simp] theorem aeval_leftPoly (x : ℝ) : aeval x leftPoly = leftValue x := by
  simp [leftPoly, leftValue]

@[simp] theorem aeval_rightPoly (x : ℝ) : aeval x rightPoly = rightValue x := by
  simp [rightPoly, rightValue]

@[simp] theorem leftPoly_natDegree : leftPoly.natDegree = 32 := by
  rw [leftPoly, natDegree_C_mul (by norm_num : (7 / 4 : ℚ) ≠ 0), natDegree_pow]
  have h : (1 - (X : ℚ[X])).natDegree = 1 := by
    rw [natDegree_sub_eq_right_of_natDegree_lt (by simp)]
    simp
  rw [h]

@[simp] theorem rightPoly_natDegree : rightPoly.natDegree = 32 := by
  exact natDegree_C_mul_X_pow 32 (7 / 4) (by norm_num)

end ExactCounts
