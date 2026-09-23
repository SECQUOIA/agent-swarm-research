import QipmFormal.FractionalSDP.Center

/-! The objective is the literal gap: its minimum on both closed feasible
sets is zero, attained only at the first coordinate projector. -/
namespace QipmFormal.FractionalSDP
noncomputable section
open Matrix

def optimumMatrix : Matrix (Fin 3) (Fin 3) ℝ := point 0 0 0 0

theorem objective_nonnegative {X : Matrix (Fin 3) (Fin 3) ℝ}
    (hX : X.PosSemidef) : 0 ≤ X 1 1 := hX.diag_nonneg

theorem optimum_feasible :
    optimumMatrix.PosSemidef ∧ optimumMatrix.trace = 1 ∧
      optimumMatrix 2 2 = optimumMatrix 0 1 ∧ optimumMatrix 1 1 = 0 ∧
      optimumMatrix 0 2 = 0 ∧ optimumMatrix 1 2 = 0 := by
  have he : optimumMatrix = Matrix.diagonal (![1, 0, 0] : Fin 3 → ℝ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [optimumMatrix, point, Matrix.diagonal]
  refine ⟨?_, point_trace _ _ _ _, rfl, rfl, rfl, rfl⟩
  rw [he]
  apply Matrix.PosSemidef.diagonal
  intro i
  fin_cases i <;> norm_num

private theorem point_quadratic (x y u v r s z : ℝ) :
    dotProduct (star (![r, s, z] : Fin 3 → ℝ))
      (Matrix.mulVec (point x y u v) ![r, s, z]) =
        (1 - y - x) * r ^ 2 + y * s ^ 2 + x * z ^ 2 +
          2 * x * r * s + 2 * u * r * z + 2 * v * s * z := by
  simp [point, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

/-- A zero objective value forces the unique optimum, including both free off-block entries. -/
theorem zero_objective_iff_optimum {X : Matrix (Fin 3) (Fin 3) ℝ}
    (hX : X.PosSemidef) (htrace : X.trace = 1) (heq : X 2 2 = X 0 1) :
    X 1 1 = 0 ↔ X = optimumMatrix := by
  constructor
  · intro hzero
    have hcoord := feasible_eq_point hX.isHermitian htrace heq
    have hp : (point (X 0 1) 0 (X 0 2) (X 1 2)).PosSemidef := by
      have hp := hX
      rw [hcoord] at hp
      simpa only [hzero] using hp
    have hq := hp.dotProduct_mulVec_nonneg
      (![X 0 1, -((1 - X 0 1) + 1) / 2, 0] : Fin 3 → ℝ)
    rw [point_quadratic] at hq
    have hb : X 0 1 = 0 := by nlinarith [sq_nonneg (X 0 1)]
    rw [hb] at hp
    have he := hp.dotProduct_mulVec_nonneg (![0, 1, -(X 1 2)] : Fin 3 → ℝ)
    rw [point_quadratic] at he
    have hezero : X 1 2 = 0 := by nlinarith [sq_nonneg (X 1 2)]
    have ht := hp.dotProduct_mulVec_nonneg (![X 0 2, 0, -1] : Fin 3 → ℝ)
    rw [point_quadratic] at ht
    have htzero : X 0 2 = 0 := by nlinarith [sq_nonneg (X 0 2)]
    rw [hcoord, hb, hzero, htzero, hezero]
    rfl
  · rintro rfl
    rfl

/-- The same feasible projector attains the lower bound in the full and restricted problems. -/
theorem optimum_objective_le {X : Matrix (Fin 3) (Fin 3) ℝ}
    (hX : X.PosSemidef) : optimumMatrix 1 1 ≤ X 1 1 :=
  objective_nonnegative hX

/-- The center parameter `g` is its objective value minus the attained optimum. -/
theorem center_objective_gap (t : ℝ) :
    centerMatrix t 1 1 - optimumMatrix 1 1 = g t := by
  simp [centerMatrix, optimumMatrix, point]

end
end QipmFormal.FractionalSDP
