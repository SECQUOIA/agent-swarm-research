import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic

namespace DAGSpectral
open Matrix

noncomputable def ratMatrixReal {I J : Type*} (A : Matrix I J ℚ) : Matrix I J ℝ :=
  A.map (Rat.castHom ℝ)

@[simp] theorem ratMatrixReal_apply {I J : Type*} (A : Matrix I J ℚ) (i : I) (j : J) :
    ratMatrixReal A i j = (A i j : ℝ) := rfl

@[simp] theorem ratMatrixReal_mul {I J K : Type*} [Fintype J]
    (A : Matrix I J ℚ) (B : Matrix J K ℚ) :
    ratMatrixReal (A * B) = ratMatrixReal A * ratMatrixReal B := by
  ext i k
  simp [ratMatrixReal, Matrix.mul_apply]

@[simp] theorem ratMatrixReal_transpose {I J : Type*} (A : Matrix I J ℚ) :
    ratMatrixReal Aᵀ = (ratMatrixReal A)ᵀ := rfl

@[simp] theorem ratMatrixReal_one {I : Type*} [DecidableEq I] :
    ratMatrixReal (1 : Matrix I I ℚ) = 1 := by
  ext i j
  simp only [ratMatrixReal_apply, Matrix.one_apply]
  split_ifs <;> norm_cast

@[simp] theorem ratMatrixReal_add {I J : Type*} (A B : Matrix I J ℚ) :
    ratMatrixReal (A+B) = ratMatrixReal A + ratMatrixReal B := by
  ext i j
  simp [ratMatrixReal]

@[simp] theorem ratMatrixReal_zero {I J : Type*} :
    ratMatrixReal (0 : Matrix I J ℚ) = 0 := by ext; simp [ratMatrixReal]

@[simp] theorem ratMatrixReal_smul {I J : Type*} (a : ℚ) (A : Matrix I J ℚ) :
    ratMatrixReal (a • A) = (a : ℝ) • ratMatrixReal A := by
  ext i j
  simp [ratMatrixReal]

@[simp] theorem ratMatrixReal_diagonal {I : Type*} [DecidableEq I] (v : I → ℚ) :
    ratMatrixReal (diagonal v) = diagonal (fun i => (v i : ℝ)) := by
  ext i j
  simp only [ratMatrixReal_apply, diagonal_apply]
  split_ifs <;> norm_cast

@[simp] theorem ratMatrixReal_mulVec {I J : Type*} [Fintype J]
    (A : Matrix I J ℚ) (x : J → ℚ) :
    ratMatrixReal A *ᵥ (fun j => (x j : ℝ)) = fun i => ((A *ᵥ x) i : ℝ) := by
  ext i
  simp [ratMatrixReal, mulVec, dotProduct]

theorem ratMatrixReal_injective {I J : Type*} :
    Function.Injective (ratMatrixReal (I := I) (J := J)) := by
  intro A B h
  ext i j
  have he := congrFun (congrFun h i) j
  change (A i j : ℝ) = (B i j : ℝ) at he
  exact_mod_cast he

end DAGSpectral
