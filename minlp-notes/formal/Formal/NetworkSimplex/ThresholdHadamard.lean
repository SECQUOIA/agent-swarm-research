import Formal.NetworkSimplex.ThresholdDeterminant
import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-! Hadamard's inequality supplies the paper's dimension-only determinant bound. -/

namespace NetworkSimplex.Threshold

open scoped BigOperators

/-- Hadamard's determinant inequality for real square matrices, including order zero. -/
theorem abs_det_le_prod_column_norm {n : ℕ} (M : Matrix (Fin n) (Fin n) ℝ) :
    |M.det| ≤ ∏ i, ‖(WithLp.toLp 2 (fun j => M j i) : EuclideanSpace ℝ (Fin n))‖ := by
  let f : Fin n → EuclideanSpace ℝ (Fin n) := fun i => WithLp.toLp 2 (fun j => M j i)
  let b := EuclideanSpace.basisFun (Fin n) ℝ
  have hdim : Module.finrank ℝ (EuclideanSpace ℝ (Fin n)) = Fintype.card (Fin n) := by
    simp
  let g := InnerProductSpace.gramSchmidtOrthonormalBasis hdim f
  have hM : b.toBasis.toMatrix f = M := by ext i j; rfl
  have hdet : b.toBasis.det f = b.toBasis.det g * g.toBasis.det f := by
    simp only [Module.Basis.det_apply]
    rw [← Matrix.det_mul]
    change (b.toBasis.toMatrix f).det =
      (b.toBasis.toMatrix g.toBasis * g.toBasis.toMatrix f).det
    rw [Module.Basis.toMatrix_mul_toMatrix]
  have hnorm : ‖b.toBasis.det f‖ = ‖g.toBasis.det f‖ := by
    rw [hdet, norm_mul, OrthonormalBasis.det_to_matrix_orthonormalBasis, one_mul]
  have hgs : g.toBasis.det f = ∏ i, inner ℝ (g i) (f i) :=
    InnerProductSpace.gramSchmidtOrthonormalBasis_det hdim f
  calc
    |M.det| = ‖b.toBasis.det f‖ := by rw [Module.Basis.det_apply, hM, Real.norm_eq_abs]
    _ = ‖g.toBasis.det f‖ := hnorm
    _ = ∏ i, ‖inner ℝ (g i) (f i)‖ := by rw [hgs, norm_prod]
    _ ≤ ∏ i, ‖f i‖ := by
      apply Finset.prod_le_prod (fun _ _ => norm_nonneg _)
      intro i _
      simpa using norm_inner_le_norm (𝕜 := ℝ) (g i) (f i)
    _ = _ := rfl

/-- A Boolean column has squared Euclidean norm at most its number of entries. -/
theorem bool_column_norm_le_sqrt {n : ℕ} (A : Matrix (Fin n) (Fin n) Bool)
    (i : Fin n) :
    ‖(WithLp.toLp 2 (fun j => (boolMatrix A j i : ℝ)) : EuclideanSpace ℝ (Fin n))‖ ≤
      Real.sqrt n := by
  rw [EuclideanSpace.norm_eq]
  apply Real.sqrt_le_sqrt
  calc
    _ ≤ ∑ _j : Fin n, (1 : ℝ) := by
      apply Finset.sum_le_sum
      intro j _
      by_cases h : A j i <;> simp [boolMatrix, h]
    _ = _ := by simp

/-- Hadamard's bound for a Boolean matrix, with the empty matrix handled automatically. -/
theorem bool_det_natAbs_le_sqrt_pow {n : ℕ} (A : Matrix (Fin n) (Fin n) Bool) :
    ((boolMatrix A).det.natAbs : ℝ) ≤ Real.sqrt n ^ n := by
  have habs : ((boolMatrix A).det.natAbs : ℝ) = |((boolMatrix A).det : ℝ)| := by
    calc
      _ = (((boolMatrix A).det.natAbs : ℤ) : ℝ) := by simp
      _ = _ := by rw [Int.natCast_natAbs, Int.cast_abs]
  rw [habs, Int.cast_det]
  apply (abs_det_le_prod_column_norm _).trans
  calc
    _ ≤ ∏ _i : Fin n, Real.sqrt n := by
      apply Finset.prod_le_prod (fun _ _ => norm_nonneg _)
      intro i _
      exact bool_column_norm_le_sqrt A i
    _ = _ := by simp

/-- Square-root power is monotone on natural dimensions once the upper dimension is positive. -/
theorem sqrt_pow_le_sqrt_pow {n m : ℕ} (hn : n ≤ m) (hm : 1 ≤ m) :
    Real.sqrt n ^ n ≤ Real.sqrt m ^ m := by
  calc
    _ ≤ Real.sqrt m ^ n := by
      gcongr
    _ ≤ _ := pow_le_pow_right₀ (Real.one_le_sqrt.mpr (by exact_mod_cast hm)) hn

/-- The maximum absolute zero-one determinant satisfies the stated Hadamard bound. -/
theorem delta01_le_hadamard (m : ℕ) :
    (delta01 m : ℝ) ≤ max 1 ((m : ℝ) ^ ((m : ℝ) / 2)) := by
  obtain ⟨n, hn, hsup⟩ := Finset.exists_mem_eq_sup (Finset.range (m + 1))
    ⟨0, Finset.mem_range.mpr (by omega)⟩ (fun k => Finset.univ.sup
      (fun A : Matrix (Fin k) (Fin k) Bool => (boolMatrix A).det.natAbs))
  obtain ⟨A, _, hA⟩ := Finset.exists_mem_eq_sup
    (Finset.univ : Finset (Matrix (Fin n) (Fin n) Bool)) Finset.univ_nonempty
      (fun A => (boolMatrix A).det.natAbs)
  unfold delta01
  rw [hsup, hA]
  have hnm : n ≤ m := by have := Finset.mem_range.mp hn; omega
  have hdet := bool_det_natAbs_le_sqrt_pow A
  by_cases hm : m = 0
  · have hn0 : n = 0 := by omega
    simpa [hn0, hm] using hdet
  · have hpow : Real.sqrt m ^ m = (m : ℝ) ^ ((m : ℝ) / 2) := by
      rw [Real.sqrt_eq_rpow, ← Real.rpow_natCast,
        ← Real.rpow_mul (Nat.cast_nonneg m)]
      congr 1
      ring
    exact (hdet.trans ((sqrt_pow_le_sqrt_pow hnm (by omega)).trans_eq hpow)).trans
      (le_max_right _ _)

end NetworkSimplex.Threshold
