import Formal.DAGSpectral.PSDAlgebra
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Algebra.Order.Ring.Pow

/-! Determinant criteria, including singular positive semidefinite matrices. -/
namespace DAGSpectral
open Matrix
open scoped BigOperators MatrixOrder InnerProductSpace

lemma det_ge_one_of_one_le {n : ℕ} {A : RealMatrix n}
    (hA : A.IsHermitian) (hI : Loewner 1 A) : 1 ≤ A.det := by
  have he : ∀ i, 1 ≤ hA.eigenvalues i := by
    intro i
    have h := hI.quadratic (hA.eigenvectorBasis i)
    rw [Matrix.one_mulVec] at h
    have hn : (hA.eigenvectorBasis i : Fin n → ℝ) ⬝ᵥ (hA.eigenvectorBasis i) = 1 := by
      have hi : ⟪hA.eigenvectorBasis i, hA.eigenvectorBasis i⟫_ℝ = 1 := by
        rw [real_inner_self_eq_norm_sq, hA.eigenvectorBasis.orthonormal.1 i]
        norm_num
      simpa only [EuclideanSpace.inner_eq_star_dotProduct, star_trivial] using hi
    rw [hn] at h
    simpa only [hA.eigenvalues_eq, RCLike.re_to_real, star_trivial] using h
  rw [hA.det_eq_prod_eigenvalues]
  simp only [RCLike.ofReal_real_eq_id, id_eq]
  exact Finset.one_le_prod (fun i _ => he i)

/-- Determinant is monotone on the PSD cone, also when either matrix is singular. -/
theorem Loewner.det_le {n : ℕ} {A B : RealMatrix n}
    (hAB : Loewner A B) (hA : A.PosSemidef) (hB : B.PosSemidef) : A.det ≤ B.det := by
  by_cases hz : A.det = 0
  · rw [hz]; exact hB.det_nonneg
  obtain ⟨R, hR⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hA.nonneg
  have hfactor : A = R.transpose * R := by
    simpa only [star_eq_conjTranspose, conjTranspose_eq_transpose_of_trivial] using hR
  have hr : IsUnit R.det := by
    apply isUnit_iff_ne_zero.mpr
    intro hzero
    apply hz
    rw [hfactor, det_mul, det_transpose, hzero, mul_zero]
  let K := R⁻¹.transpose
  have hKA : K * A * K.transpose = 1 := by
    dsimp [K]
    rw [hfactor, transpose_transpose, ← mul_assoc, ← transpose_mul,
      Matrix.mul_nonsing_inv R hr, transpose_one, one_mul, Matrix.mul_nonsing_inv R hr]
  have hQ := hAB.congruence K
  rw [hKA] at hQ
  have hBQ : (K * B * K.transpose).IsHermitian := by
    simpa only [conjTranspose_eq_transpose_of_trivial] using
      (hB.mul_mul_conjTranspose_same K).isHermitian
  have hdQ := det_ge_one_of_one_le hBQ hQ
  have hdA := congrArg Matrix.det hKA
  simp only [det_mul, det_transpose, det_one] at hdA hdQ
  have hk0 : K.det ≠ 0 := by
    intro hk
    simp [hk] at hdA
  have hk : 0 < K.det ^ 2 := sq_pos_of_ne_zero hk0
  apply (mul_le_mul_iff_right₀ hk).mp
  nlinarith

lemma det_smul {n : ℕ} (a : ℝ) (A : RealMatrix n) :
    (a • A).det = a ^ n * A.det := by
  simp

lemma RelativeSandwich.det_lower {n : ℕ} {A B : RealMatrix n} {η : ℝ}
    (h : RelativeSandwich η A B) (hA : A.PosSemidef) (hB : B.PosSemidef)
    (hη : η ≤ 1) : (1 - η) ^ n * A.det ≤ B.det := by
  simpa only [det_smul] using h.1.det_le (hA.smul (sub_nonneg.mpr hη)) hB

lemma RelativeSandwich.det_upper {n : ℕ} {A B : RealMatrix n} {η : ℝ}
    (h : RelativeSandwich η A B) (hA : A.PosSemidef) (hB : B.PosSemidef)
    (hη : -1 ≤ η) : B.det ≤ (1 + η) ^ n * A.det := by
  simpa only [det_smul] using h.2.det_le hB (hA.smul (by linarith))

lemma bernoulli_relative {n : ℕ} (hn : 0 < n) {ε : ℝ}
    (_hε0 : 0 ≤ ε) (hε1 : ε ≤ 1) : 1 - ε ≤ (1 - ε / n) ^ n := by
  have hn0 : (0 : ℝ) < n := Nat.cast_pos.mpr hn
  have hη : ε / n ≤ 1 := (div_le_one hn0).mpr (hε1.trans (by exact_mod_cast hn))
  have h := one_add_mul_le_pow (show (-2 : ℝ) ≤ -(ε / n) by linarith) n
  have heq : (n : ℝ) * -(ε / n) = -ε := by field_simp
  simpa only [heq, sub_eq_add_neg] using h

lemma RelativeSandwich.det_lower_eps {n : ℕ} {A B : RealMatrix n} {ε : ℝ}
    (h : RelativeSandwich (ε / n) A B) (hA : A.PosSemidef) (hB : B.PosSemidef)
    (hn : 0 < n) (hε0 : 0 ≤ ε) (hε1 : ε ≤ 1) :
    (1 - ε) * A.det ≤ B.det := by
  have hη : ε / n ≤ 1 := (div_le_one (Nat.cast_pos.mpr hn)).mpr
    (hε1.trans (by exact_mod_cast hn))
  exact (mul_le_mul_of_nonneg_right (bernoulli_relative hn hε0 hε1) hA.det_nonneg).trans
    (h.det_lower hA hB hη)

end DAGSpectral
