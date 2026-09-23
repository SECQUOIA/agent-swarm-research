import Mathlib

/-! # Frobenius norm estimates for real matrix mixtures -/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators Matrix Matrix.Norms.L2Operator

variable {n : Type*} [Fintype n]


/-- The entrywise Euclidean (Frobenius) norm. -/
def frobeniusNorm (A : Matrix n n ℝ) : ℝ :=
  Real.sqrt (∑ i, ∑ j, A i j ^ 2)

lemma frobeniusNorm_nonneg (A : Matrix n n ℝ) : 0 ≤ frobeniusNorm A :=
  Real.sqrt_nonneg _

lemma frobeniusNorm_sq (A : Matrix n n ℝ) :
    frobeniusNorm A ^ 2 = ∑ i, ∑ j, A i j ^ 2 :=
  Real.sq_sqrt (Finset.sum_nonneg fun _ _ => Finset.sum_nonneg fun _ _ => sq_nonneg _)

lemma frobeniusNorm_smul (c : ℝ) (A : Matrix n n ℝ) :
    frobeniusNorm (c • A) = |c| * frobeniusNorm A := by
  apply (sq_eq_sq₀ (frobeniusNorm_nonneg _) (mul_nonneg (abs_nonneg _) (frobeniusNorm_nonneg _))).mp
  rw [mul_pow, sq_abs, frobeniusNorm_sq, frobeniusNorm_sq]
  simp only [Matrix.smul_apply, smul_eq_mul, mul_pow, Finset.mul_sum]

variable [DecidableEq n]

/-- Removing the scalar trace component is an orthogonal projection. -/
lemma centered_sum_sq (A : Matrix n n ℝ) (c : ℝ) :
    (∑ i, ∑ j, (A - c • (1 : Matrix n n ℝ)) i j ^ 2) =
      (∑ i, ∑ j, A i j ^ 2) - 2 * c * A.trace + (Fintype.card n : ℝ) * c ^ 2 := by
  have hrow (i : n) : (∑ j, (A - c • (1 : Matrix n n ℝ)) i j ^ 2) =
      (∑ j, A i j ^ 2) - 2 * c * A i i + c ^ 2 := by
    calc
      _ = ∑ j, (A i j ^ 2 + if i = j then -2 * c * A i j + c ^ 2 else 0) := by
        apply Finset.sum_congr rfl
        intro j _
        by_cases h : i = j
        · simp [Matrix.sub_apply, Matrix.smul_apply, h]; ring
        · simp [Matrix.sub_apply, Matrix.smul_apply, h]
      _ = _ := by simp [Finset.sum_add_distrib]; ring
  simp_rw [hrow]
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum,
    Finset.sum_const, Finset.card_univ, nsmul_eq_mul, Matrix.trace, Matrix.diag]

lemma frobeniusNorm_centered_le (A : Matrix n n ℝ) :
    frobeniusNorm (A - (A.trace / Fintype.card n) • (1 : Matrix n n ℝ)) ≤
      frobeniusNorm A := by
  apply (sq_le_sq₀ (frobeniusNorm_nonneg _) (frobeniusNorm_nonneg _)).mp
  rw [frobeniusNorm_sq, frobeniusNorm_sq, centered_sum_sq]
  by_cases hn : Fintype.card n = 0
  · simp [hn]
  · have hnpos : (0 : ℝ) < Fintype.card n := by exact_mod_cast Nat.pos_of_ne_zero hn
    have hid : 2 * (A.trace / Fintype.card n) * A.trace -
        (Fintype.card n : ℝ) * (A.trace / Fintype.card n) ^ 2 =
        A.trace ^ 2 / Fintype.card n := by field_simp; ring
    have h := div_nonneg (sq_nonneg A.trace) hnpos.le
    linarith

lemma frobeniusNorm_recentered_le (D : Matrix n n ℝ) (hD : D.PosSemidef) :
    frobeniusNorm ((1 + D.trace / Fintype.card n)⁻¹ •
      (D - (D.trace / Fintype.card n) • (1 : Matrix n n ℝ))) ≤ frobeniusNorm D := by
  have ht : 0 ≤ D.trace / (Fintype.card n : ℝ) := div_nonneg hD.trace_nonneg (Nat.cast_nonneg _)
  have hi : 0 ≤ (1 + D.trace / (Fintype.card n : ℝ))⁻¹ := inv_nonneg.mpr (by linarith)
  have hi1 : (1 + D.trace / (Fintype.card n : ℝ))⁻¹ ≤ 1 :=
    inv_le_one_of_one_le₀ (by linarith)
  rw [frobeniusNorm_smul, abs_of_nonneg hi]
  exact (mul_le_of_le_one_left (frobeniusNorm_nonneg _) hi1).trans (frobeniusNorm_centered_le D)

lemma column_sum_sq_le_opNorm_sq (A : Matrix n n ℝ) (j : n) :
    (∑ i, A i j ^ 2) ≤ ‖A‖ ^ 2 := by
  have h := A.l2_opNorm_mulVec (PiLp.single 2 j (1 : ℝ))
  simp only [PiLp.norm_single, norm_one, mul_one] at h
  have hs := sq_le_sq₀ (norm_nonneg _) (norm_nonneg A) |>.mpr h
  simpa [EuclideanSpace.real_norm_sq_eq, Matrix.mulVec, dotProduct, PiLp.single_apply] using hs

lemma frobeniusNorm_le_sqrt_card_mul_opNorm (A : Matrix n n ℝ) :
    frobeniusNorm A ≤ Real.sqrt (Fintype.card n) * ‖A‖ := by
  apply (sq_le_sq₀ (frobeniusNorm_nonneg _)
    (mul_nonneg (Real.sqrt_nonneg _) (norm_nonneg _))).mp
  rw [frobeniusNorm_sq, mul_pow, Real.sq_sqrt (Nat.cast_nonneg _), Finset.sum_comm]
  calc
    _ ≤ ∑ _j : n, ‖A‖ ^ 2 := Finset.sum_le_sum fun j _ => column_sum_sq_le_opNorm_sq A j
    _ = _ := by simp

lemma frobeniusNorm_mul_le_opNorm_mul (A B : Matrix n n ℝ) :
    frobeniusNorm (A * B) ≤ ‖A‖ * frobeniusNorm B := by
  have hcol (j : n) : (∑ i, (A * B) i j ^ 2) ≤ ‖A‖ ^ 2 * ∑ i, B i j ^ 2 := by
    have h := A.l2_opNorm_mulVec (WithLp.toLp 2 (fun i => B i j))
    have hs := (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mpr h
    simpa [mul_pow, EuclideanSpace.real_norm_sq_eq, Matrix.mulVec, Matrix.mul_apply,
      dotProduct] using hs
  apply (sq_le_sq₀ (frobeniusNorm_nonneg _)
    (mul_nonneg (norm_nonneg _) (frobeniusNorm_nonneg _))).mp
  rw [frobeniusNorm_sq, mul_pow, frobeniusNorm_sq]
  calc
    _ = ∑ j, ∑ i, (A * B) i j ^ 2 := Finset.sum_comm
    _ ≤ ∑ j, ‖A‖ ^ 2 * ∑ i, B i j ^ 2 := Finset.sum_le_sum fun j _ => hcol j
    _ = ‖A‖ ^ 2 * ∑ i, ∑ j, B i j ^ 2 := by
      rw [← Finset.mul_sum, Finset.sum_comm]

open scoped Matrix.Norms.Frobenius in
lemma frobeniusNorm_eq_norm (A : Matrix n n ℝ) : frobeniusNorm A = ‖A‖ := by
  simp [frobeniusNorm, Matrix.frobenius_norm_def, Real.sqrt_eq_rpow]

open scoped Matrix.Norms.Frobenius in
omit [DecidableEq n] in
lemma frobeniusNorm_add_le (A B : Matrix n n ℝ) :
    frobeniusNorm (A + B) ≤ frobeniusNorm A + frobeniusNorm B := by
  classical
  simp only [frobeniusNorm_eq_norm]
  exact norm_add_le A B

omit [DecidableEq n] in
lemma frobeniusNorm_transpose (A : Matrix n n ℝ) : frobeniusNorm Aᵀ = frobeniusNorm A := by
  simp only [frobeniusNorm, Matrix.transpose_apply]
  rw [Finset.sum_comm]

lemma frobeniusNorm_mul_le_mul_opNorm (A B : Matrix n n ℝ) :
    frobeniusNorm (A * B) ≤ frobeniusNorm A * ‖B‖ := by
  have h := frobeniusNorm_mul_le_opNorm_mul Bᵀ Aᵀ
  have hb : ‖Bᵀ‖ = ‖B‖ := by simpa using Matrix.l2_opNorm_conjTranspose B
  rw [← Matrix.transpose_mul, frobeniusNorm_transpose, frobeniusNorm_transpose, hb,
    mul_comm] at h
  exact h

open scoped Matrix.Norms.Frobenius in
omit [DecidableEq n] in
lemma frobeniusNorm_mul_le (A B : Matrix n n ℝ) :
    frobeniusNorm (A * B) ≤ frobeniusNorm A * frobeniusNorm B := by
  classical
  simp only [frobeniusNorm_eq_norm]
  exact norm_mul_le A B

open scoped Matrix.Norms.Frobenius in
omit [DecidableEq n] in
lemma frobeniusNorm_sum_le {ι : Type*} (s : Finset ι) (A : ι → Matrix n n ℝ) :
    frobeniusNorm (∑ i ∈ s, A i) ≤ ∑ i ∈ s, frobeniusNorm (A i) := by
  classical
  simp only [frobeniusNorm_eq_norm]
  exact norm_sum_le s A

end
end QipmFormal.SDPMixture
