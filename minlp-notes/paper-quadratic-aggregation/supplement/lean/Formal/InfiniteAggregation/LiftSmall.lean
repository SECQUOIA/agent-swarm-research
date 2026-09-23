import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.GramConcavity

open scoped Matrix

namespace InfiniteAggregation

/-- A symmetric two-by-two matrix in Gram coordinates. -/
def gramMatrix (a b c : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a, c; c, b]

lemma gramMatrix_hermitian (a b c : ℝ) : (gramMatrix a b c).IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [gramMatrix, Matrix.conjTranspose_apply]

lemma gramMatrix_quadratic (a b c : ℝ) (x : Fin 2 → ℝ) :
    x ⬝ᵥ (gramMatrix a b c *ᵥ x) =
      a * x 0 ^ 2 + 2 * c * x 0 * x 1 + b * x 1 ^ 2 := by
  simp [gramMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

lemma gramMatrix_det (a b c : ℝ) : (gramMatrix a b c).det = a * b - c ^ 2 := by
  simp [gramMatrix, Matrix.det_fin_two, pow_two]

/-- The scalar Gram conditions are exactly positive semidefiniteness. -/
theorem gramMatrix_posSemidef_iff (a b c : ℝ) :
    (gramMatrix a b c).PosSemidef ↔ GramPSD a b c := by
  constructor
  · intro h
    have ha := h.diag_nonneg (i := 0)
    have hb := h.diag_nonneg (i := 1)
    have hd := h.det_nonneg
    simp only [gramMatrix_det] at hd
    exact ⟨ha, hb, by linarith⟩
  · rintro ⟨ha, hb, hc⟩
    apply Matrix.posSemidef_iff_dotProduct_mulVec.mpr
    refine ⟨gramMatrix_hermitian a b c, ?_⟩
    intro x
    simp only [star_trivial, gramMatrix_quadratic]
    by_cases ha0 : a = 0
    · have hc0 : c = 0 := by nlinarith [sq_nonneg c]
      simp only [ha0, hc0, mul_zero, zero_mul, zero_add]
      exact mul_nonneg hb (sq_nonneg _)
    · have hap : 0 < a := lt_of_le_of_ne ha (Ne.symm ha0)
      have hd := mul_nonneg (sub_nonneg.mpr hc) (sq_nonneg (x 1))
      nlinarith [sq_nonneg (a * x 0 + c * x 1)]

/-- Strict scalar Gram conditions are exactly positive definiteness. -/
theorem gramMatrix_posDef_iff (a b c : ℝ) :
    (gramMatrix a b c).PosDef ↔ 0 < a ∧ 0 < b ∧ c ^ 2 < a * b := by
  constructor
  · intro h
    have ha := h.diag_pos (i := 0)
    have hb := h.diag_pos (i := 1)
    have hd := h.det_pos
    simp only [gramMatrix_det] at hd
    exact ⟨ha, hb, by linarith⟩
  · rintro ⟨ha, hb, hc⟩
    apply Matrix.posDef_iff_dotProduct_mulVec.mpr
    refine ⟨gramMatrix_hermitian a b c, ?_⟩
    intro x hx
    simp only [star_trivial, gramMatrix_quadratic]
    by_cases hx1 : x 1 = 0
    · have hx0 : x 0 ≠ 0 := by
        intro hz
        apply hx
        ext i
        fin_cases i <;> simp [hz, hx1]
      simp only [hx1, mul_zero, add_zero, zero_pow (by omega : 2 ≠ 0)]
      exact mul_pos ha (sq_pos_of_ne_zero hx0)
    · have hd := mul_pos (sub_pos.mpr hc) (sq_pos_of_ne_zero hx1)
      nlinarith [sq_nonneg (a * x 0 + c * x 1)]

end InfiniteAggregation
