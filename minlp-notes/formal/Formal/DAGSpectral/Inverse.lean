import Formal.DAGSpectral.PSDAlgebra

namespace DAGSpectral
open Matrix
open scoped MatrixOrder

variable {n : ℕ} {A B : RealMatrix n} {η : ℝ}

theorem Loewner.inverse (h : Loewner A B) (hA : A.PosDef) (hB : B.PosDef) :
    Loewner B⁻¹ A⁻¹ := by
  have hAi : A⁻¹ * A = 1 := Matrix.nonsing_inv_mul _ ((Matrix.isUnit_iff_isUnit_det A).mp hA.isUnit)
  have hAi' : A * A⁻¹ = 1 := Matrix.mul_nonsing_inv _
    ((Matrix.isUnit_iff_isUnit_det A).mp hA.isUnit)
  have hBi : B * B⁻¹ = 1 := Matrix.mul_nonsing_inv _ ((Matrix.isUnit_iff_isUnit_det B).mp hB.isUnit)
  have hAt : (A⁻¹)ᴴ = A⁻¹ := hA.inv.isHermitian
  have hBt : (B⁻¹)ᴴ = B⁻¹ := hB.inv.isHermitian
  have h₁ := h.mul_mul_conjTranspose_same B⁻¹
  have h₂ := hA.posSemidef.mul_mul_conjTranspose_same (A⁻¹ - B⁻¹)
  rw [hBt] at h₁
  rw [conjTranspose_sub, hAt, hBt] at h₂
  have he : B⁻¹ * (B - A) * B⁻¹ + (A⁻¹ - B⁻¹) * A * (A⁻¹ - B⁻¹) =
      A⁻¹ - B⁻¹ := by
    simp only [Matrix.mul_sub, Matrix.sub_mul]
    simp only [Matrix.mul_assoc, hBi, hAi', Matrix.mul_one]
    simp only [← Matrix.mul_assoc, hAi, Matrix.one_mul]
    noncomm_ring
  change (A⁻¹ - B⁻¹).PosSemidef
  rw [← he]
  exact h₁.add h₂

theorem inverse_smul (A : RealMatrix n) (hA : A.PosDef) (s : ℝ) (hs : s ≠ 0) :
    (s • A)⁻¹ = s⁻¹ • A⁻¹ := by
  let : Invertible s := invertibleOfNonzero hs
  simpa only [invOf_eq_inv] using Matrix.inv_smul A s
    ((Matrix.isUnit_iff_isUnit_det A).mp hA.isUnit)

theorem RelativeSandwich.posDef (h : RelativeSandwich η A B)
    (hA : A.PosDef) (hη : η < 1) : B.PosDef := by
  apply Matrix.PosDef.of_dotProduct_mulVec_pos
  · exact ((hA.posSemidef.smul (by linarith : 0 ≤ 1 - η)).add h.1).isHermitian |>
      fun hh => by simpa only [add_sub_cancel] using hh
  · intro x hx
    have ha := hA.dotProduct_mulVec_pos hx
    have hlo := h.1.quadratic x
    simp only [Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul] at hlo
    simp only [star_trivial] at ha ⊢
    nlinarith

theorem RelativeSandwich.inverse (h : RelativeSandwich η A B)
    (hA : A.PosDef) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    Loewner ((1 + η)⁻¹ • A⁻¹) B⁻¹ ∧ Loewner B⁻¹ ((1 - η)⁻¹ • A⁻¹) := by
  have hm : 0 < 1 - η := by linarith
  have hp : 0 < 1 + η := by linarith
  have hB := h.posDef hA hη1
  constructor
  · simpa only [inverse_smul A hA _ hp.ne'] using h.2.inverse hB (hA.smul hp)
  · simpa only [inverse_smul A hA _ hm.ne'] using h.1.inverse (hA.smul hm) hB

theorem Loewner.trace (h : Loewner A B) : Matrix.trace A ≤ Matrix.trace B := by
  have hh : 0 ≤ Matrix.trace (B - A) :=
    Finset.sum_nonneg fun i _ => h.diag_nonneg (i := i)
  simpa only [Matrix.trace_sub, sub_nonneg] using hh

theorem RelativeSandwich.trace_inverse (h : RelativeSandwich η A B)
    (hA : A.PosDef) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    (1 + η)⁻¹ * Matrix.trace A⁻¹ ≤ Matrix.trace B⁻¹ ∧
    Matrix.trace B⁻¹ ≤ (1 - η)⁻¹ * Matrix.trace A⁻¹ := by
  obtain ⟨hlo, hup⟩ := h.inverse hA hη0 hη1
  constructor
  · simpa only [Matrix.trace_smul, smul_eq_mul] using hlo.trace
  · simpa only [Matrix.trace_smul, smul_eq_mul] using hup.trace

end DAGSpectral
