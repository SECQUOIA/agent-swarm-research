import QipmFormal.FractionalSDP.Defs

/-! Exact spectra in the Frobenius metric. The diagonal coordinates have
Gram matrix `[[4,1],[1,2]]`; their operator is therefore `G⁻¹K`.
The four-factor characteristic polynomial also records multiplicities. -/
namespace QipmFormal.FractionalSDP
noncomputable section
open Polynomial

def diagGram : Matrix (Fin 2) (Fin 2) ℝ := !![4,1;1,2]
def diagHessian (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![k00 t,k01 t;k01 t,k11 t]
def diagOperator (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![(2*k00 t-k01 t)/7,(2*k01 t-k11 t)/7;
    (-k00 t+4*k01 t)/7,(-k01 t+4*k11 t)/7]
def offOperator (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![g t/(b t*q t),-b t/(b t*q t);-b t/(b t*q t),a t/(b t*q t)]
def reducedOperator (t : ℝ) : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  Matrix.fromBlocks (diagOperator t) 0 0 (offOperator t)

theorem gram_mul_diagOperator (t : ℝ) : diagGram * diagOperator t = diagHessian t := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [diagGram, diagOperator, diagHessian, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem diagOperator_generalized_eigenvector (t r : ℝ) (v : Fin 2 → ℝ) :
    (diagOperator t).mulVec v = r • v ↔
      (diagHessian t).mulVec v = r • diagGram.mulVec v := by
  have hinj : Function.Injective diagGram.mulVec := by
    apply Matrix.mulVec_injective_iff_isUnit.mpr
    rw [Matrix.isUnit_iff_isUnit_det]
    norm_num [diagGram, Matrix.det_fin_two]
  constructor
  · intro h
    rw [← gram_mul_diagOperator, ← Matrix.mulVec_mulVec, h, Matrix.mulVec_smul]
  · intro h
    apply hinj
    rw [Matrix.mulVec_mulVec, gram_mul_diagOperator, Matrix.mulVec_smul, h]

theorem diag_discriminant_nonneg (t : ℝ) :
    0 ≤ diagTrace t ^ 2 - 4 * diagDet t := by
  have h₁ := sq_nonneg (2*k00 t-2*k01 t-3*k11 t)
  have h₂ := sq_nonneg (2*k01 t-k11 t)
  dsimp [diagTrace, diagDet]
  nlinarith

theorem diagTrace_pos (t : ℝ) (hq : 0 < q t) : 0 < diagTrace t := by
  have hq2 : 0 < q t ^ 2 := sq_pos_of_pos hq
  have h₁ := sq_nonneg ((-g t-2*b t)-(1-b t-2*g t))
  have h₂ := sq_nonneg (-g t-2*b t)
  have h₃ := sq_nonneg (1-b t-2*g t)
  have hb := sq_nonneg ((b t)⁻¹)
  dsimp [diagTrace, k00, k01, k11]
  apply (div_pos_iff_of_pos_right (by norm_num : (0:ℝ)<7)).2
  apply (mul_pos_iff_of_pos_right hq2).mp
  field_simp
  have hbq := div_nonneg (sq_nonneg (q t)) (sq_nonneg (b t))
  nlinarith

theorem diagHigh_pos (t : ℝ) (hq : 0 < q t) : 0 < diagHigh t := by
  exact div_pos (add_pos_of_pos_of_nonneg (diagTrace_pos t hq) (Real.sqrt_nonneg _))
    (by norm_num)

theorem diagHigh_root (t : ℝ) :
    diagHigh t ^ 2 - diagTrace t * diagHigh t + diagDet t = 0 := by
  have hs := Real.sq_sqrt (diag_discriminant_nonneg t)
  dsimp [diagHigh]
  nlinarith

theorem diag_root_sum (t : ℝ) (hq : 0 < q t) :
    diagLow t + diagHigh t = diagTrace t := by
  dsimp [diagLow]
  have hh := ne_of_gt (diagHigh_pos t hq)
  field_simp
  nlinarith [diagHigh_root t]

theorem diag_root_product (t : ℝ) (hq : 0 < q t) :
    diagLow t * diagHigh t = diagDet t := by
  exact div_mul_cancel₀ _ (ne_of_gt (diagHigh_pos t hq))

theorem diag_charpoly (t : ℝ) (hq : 0 < q t) :
    (diagOperator t).charpoly = (X-C (diagLow t))*(X-C (diagHigh t)) := by
  rw [Matrix.charpoly_fin_two]
  have ht : (diagOperator t).trace = diagTrace t := by
    simp [diagOperator, Matrix.trace, Fin.sum_univ_two, diagTrace]; ring
  have hd : (diagOperator t).det = diagDet t := by
    simp [diagOperator, Matrix.det_fin_two, diagDet]; ring
  rw [ht, hd, ← diag_root_product t hq, ← diag_root_sum t hq, map_add, map_mul]
  ring

theorem aHigh_pos (t : ℝ) (ha : 0 < a t + g t) : 0 < aHigh t := by
  exact div_pos (add_pos_of_pos_of_nonneg ha (Real.sqrt_nonneg _)) (by norm_num)

theorem aHigh_root (t : ℝ) :
    aHigh t ^ 2 - (a t + g t)*aHigh t + q t = 0 := by
  have hd : 0 ≤ (a t-g t)^2+4*b t^2 := by positivity
  have hs := Real.sq_sqrt hd
  dsimp [aHigh, q]
  nlinarith

theorem off_root_sum (t : ℝ) (hb : 0 < b t) (hq : 0 < q t)
    (ha : 0 < a t + g t) :
    offLow t + offHigh t = (a t + g t)/(b t*q t) := by
  have hh := ne_of_gt (aHigh_pos t ha)
  dsimp [offLow, offHigh]
  field_simp
  nlinarith [aHigh_root t]

theorem off_root_product (t : ℝ) (hb : 0 < b t) (hq : 0 < q t)
    (ha : 0 < a t + g t) :
    offLow t * offHigh t = 1/(b t^2*q t) := by
  have hh := ne_of_gt (aHigh_pos t ha)
  dsimp [offLow, offHigh]
  field_simp

theorem off_charpoly (t : ℝ) (hb : 0 < b t) (hq : 0 < q t)
    (ha : 0 < a t + g t) :
    (offOperator t).charpoly = (X-C (offLow t))*(X-C (offHigh t)) := by
  rw [Matrix.charpoly_fin_two]
  have ht : (offOperator t).trace = (a t+g t)/(b t*q t) := by
    simp [offOperator, Matrix.trace, Fin.sum_univ_two]; ring
  have hd : (offOperator t).det = 1/(b t^2*q t) := by
    have hq' : a t*g t-b t^2 = q t := rfl
    simp [offOperator, Matrix.det_fin_two]
    field_simp
    nlinarith
  rw [ht, hd, ← off_root_product t hb hq ha, ← off_root_sum t hb hq ha, map_add, map_mul]
  ring

theorem reduced_charpoly (t : ℝ) (hb : 0 < b t) (hq : 0 < q t)
    (ha : 0 < a t + g t) :
    (reducedOperator t).charpoly =
      ((X-C (diagLow t))*(X-C (diagHigh t))) *
      ((X-C (offLow t))*(X-C (offHigh t))) := by
  rw [reducedOperator, Matrix.charpoly_fromBlocks_zero₁₂,
    diag_charpoly t hq, off_charpoly t hb hq ha]

theorem mem_reduced_spectrum_iff (t r : ℝ) (hb : 0 < b t) (hq : 0 < q t)
    (ha : 0 < a t + g t) :
    r ∈ spectrum ℝ (reducedOperator t) ↔
      r = diagLow t ∨ r = diagHigh t ∨ r = offLow t ∨ r = offHigh t := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly, reduced_charpoly t hb hq ha]
  simp only [Polynomial.IsRoot, eval_mul, eval_sub, eval_X, eval_C, mul_eq_zero, sub_eq_zero]
  tauto

theorem mem_diag_spectrum_iff (t r : ℝ) (hq : 0 < q t) :
    r ∈ spectrum ℝ (diagOperator t) ↔ r = diagLow t ∨ r = diagHigh t := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly, diag_charpoly t hq]
  simp [Polynomial.IsRoot, sub_eq_zero]

end
end QipmFormal.FractionalSDP
