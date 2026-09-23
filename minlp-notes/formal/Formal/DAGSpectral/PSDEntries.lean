import Formal.DAGSpectral.PSDAlgebra
import Formal.DAGSpectral.RatMatrix

/-! Diagonal filtering bounds every entry of an actual PSD congruence. -/
namespace DAGSpectral
open Matrix

/-- Every two-by-two principal PSD minor has nonnegative determinant. -/
theorem psd_abs_entry_sq_le {I : Type*}
    {A : Matrix I I ℝ} (hA : A.PosSemidef) (i j : I) :
    |A i j| ^ 2 ≤ A i i * A j j := by
  have hd := (hA.submatrix (![i, j] : Fin 2 → I)).det_nonneg
  have hs : A j i = A i j := by
    have he := congrArg (fun B => B i j) hA.isHermitian
    simpa using he
  simp only [Matrix.det_fin_two, Matrix.submatrix_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one] at hd
  rw [hs] at hd
  rw [sq_abs]
  nlinarith

/-- A uniform diagonal bound on a PSD matrix bounds all its entries. -/
theorem psd_abs_entry_le {I : Type*}
    {A : Matrix I I ℝ} (hA : A.PosSemidef) {C : ℝ} (hC : 0 ≤ C)
    (hdiag : ∀ i, A i i ≤ C) (i j : I) : |A i j| ≤ C := by
  have hsq := psd_abs_entry_sq_le hA i j
  have hp : A i i * A j j ≤ C * C :=
    mul_le_mul (hdiag i) (hdiag j) hA.diag_nonneg hC
  nlinarith [abs_nonneg (A i j)]

/-- The rational diagonal test implies the advertised entry bound after
congruence; PSD follows from the original matrix, rather than a new assumption. -/
theorem normalized_abs_entry_le {p r : ℕ} (Q : Matrix (Fin p) (Fin p) ℚ)
    (hQ : (ratMatrixReal Q).PosSemidef) (T : Matrix (Fin r) (Fin p) ℚ)
    (C : ℚ) (hC : 0 ≤ C) (hdiag : ∀ i, (T * Q * Tᵀ) i i ≤ C)
    (i j : Fin r) : |(T * Q * Tᵀ) i j| ≤ C := by
  have hA : (ratMatrixReal (T * Q * Tᵀ)).PosSemidef := by
    simpa only [ratMatrixReal_mul, ratMatrixReal_transpose,
      Matrix.conjTranspose_eq_transpose_of_trivial] using
      hQ.mul_mul_conjTranspose_same (ratMatrixReal T)
  have hd : ∀ i, ratMatrixReal (T * Q * Tᵀ) i i ≤ (C : ℝ) := by
    intro i
    simpa only [ratMatrixReal_apply] using (show ((T * Q * Tᵀ) i i : ℝ) ≤ C by
      exact_mod_cast hdiag i)
  have hb := psd_abs_entry_le hA (by exact_mod_cast hC) hd i j
  simpa only [ratMatrixReal_apply, ← Rat.cast_abs, Rat.cast_le] using hb

/-- The exact 4p cutoff used in every rank trial. -/
theorem normalized_abs_entry_le_four_p {p r : ℕ} (Q : Matrix (Fin p) (Fin p) ℚ)
    (hQ : (ratMatrixReal Q).PosSemidef) (T : Matrix (Fin r) (Fin p) ℚ)
    (hdiag : ∀ i, (T * Q * Tᵀ) i i ≤ 4 * p) (i j : Fin r) :
    |(T * Q * Tᵀ) i j| ≤ 4 * p :=
  normalized_abs_entry_le Q hQ T (4 * p) (by positivity) hdiag i j

end DAGSpectral
