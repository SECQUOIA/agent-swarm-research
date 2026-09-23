import Mathlib

/-! The actual positive inverse square root used by SPD preconditioning. -/

namespace QipmFormal.Preconditioner
noncomputable section
open scoped MatrixOrder
open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The positive inverse square root, in the manuscript's original coordinates. -/
def inverseSqrt (M : Matrix n n ℝ) : Matrix n n ℝ := (CFC.sqrt M)⁻¹

theorem sqrt_isUnit {M : Matrix n n ℝ} (hM : M.PosDef) : IsUnit (CFC.sqrt M) :=
  (CFC.isUnit_sqrt_iff M hM.posSemidef.nonneg).mpr hM.isUnit

theorem inverseSqrt_isUnit {M : Matrix n n ℝ} (hM : M.PosDef) :
    IsUnit (inverseSqrt M) :=
  Matrix.isUnit_nonsing_inv_iff.mpr (sqrt_isUnit hM)

theorem inverseSqrt_symmetric (M : Matrix n n ℝ) :
    (inverseSqrt M).transpose = inverseSqrt M := by
  have hs : (CFC.sqrt M).IsHermitian := Matrix.isHermitian_iff_isSelfAdjoint.mpr
    (CFC.sqrt_nonneg M).isSelfAdjoint
  simpa only [inverseSqrt, Matrix.conjTranspose_eq_transpose_of_trivial] using hs.inv.eq

theorem inverseSqrt_posSemidef (M : Matrix n n ℝ) : (inverseSqrt M).PosSemidef :=
  (Matrix.nonneg_iff_posSemidef.mp (CFC.sqrt_nonneg M)).inv

theorem inverseSqrt_sq {M : Matrix n n ℝ} (hM : M.PosDef) :
    inverseSqrt M * inverseSqrt M = M⁻¹ := by
  unfold inverseSqrt
  rw [← Matrix.mul_inv_rev, CFC.sqrt_mul_sqrt_self M hM.posSemidef.nonneg]

theorem inverseSqrt_whitens {M : Matrix n n ℝ} (hM : M.PosDef) :
    inverseSqrt M * M * inverseSqrt M = 1 := by
  have hi := (Matrix.isUnit_iff_isUnit_det _).mp (sqrt_isUnit hM)
  unfold inverseSqrt
  conv_lhs => arg 1; arg 2; rw [← CFC.sqrt_mul_sqrt_self M hM.posSemidef.nonneg]
  simp only [← Matrix.mul_assoc, Matrix.nonsing_inv_mul _ hi, Matrix.one_mul,
    Matrix.mul_nonsing_inv _ hi]

theorem inverseSqrt_congruence_posDef {A M : Matrix n n ℝ}
    (hA : A.PosDef) (hM : M.PosDef) :
    (inverseSqrt M * A * inverseSqrt M).PosDef := by
  have h := hA.conjTranspose_mul_mul_same
    (Matrix.mulVec_injective_iff_isUnit.mpr (inverseSqrt_isUnit hM))
  simpa only [Matrix.conjTranspose_eq_transpose_of_trivial, inverseSqrt_symmetric] using h

end
end QipmFormal.Preconditioner
