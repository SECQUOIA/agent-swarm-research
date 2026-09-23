import Formal.DAGSpectral.PSDAlgebra
import Mathlib.Analysis.Matrix.Spectrum

namespace DAGSpectral
open Matrix Unitary
open scoped MatrixOrder
noncomputable section

/-- Spectral Moore–Penrose inverse: reciprocate nonzero eigenvalues and leave
zero eigenvalues zero. -/
def pseudoInverse {n : ℕ} (A : RealMatrix n) (hA : A.IsHermitian) : RealMatrix n :=
  conjStarAlgAut ℝ _ hA.eigenvectorUnitary (diagonal fun i => (hA.eigenvalues i)⁻¹)

variable {n : ℕ} {A B : RealMatrix n}

theorem spectral_real (hA : A.IsHermitian) :
    A = conjStarAlgAut ℝ _ hA.eigenvectorUnitary (diagonal hA.eigenvalues) := by
  simpa using hA.spectral_theorem

theorem pseudoInverse_mul_self_mul (hA : A.IsHermitian) :
    A * pseudoInverse A hA * A = A := by
  unfold pseudoInverse
  conv_lhs => lhs; lhs; rw [spectral_real hA]
  conv_lhs => rhs; rw [spectral_real hA]
  rw [ ← map_mul, ← map_mul, diagonal_mul_diagonal, diagonal_mul_diagonal]
  convert (spectral_real hA).symm using 2
  congr 1
  funext i
  by_cases hi : hA.eigenvalues i = 0 <;> simp [hi]

theorem pseudoInverse_mul_mul_self (hA : A.IsHermitian) :
    pseudoInverse A hA * A * pseudoInverse A hA = pseudoInverse A hA := by
  unfold pseudoInverse
  conv_lhs => lhs; rhs; rw [spectral_real hA]
  rw [ ← map_mul, ← map_mul, diagonal_mul_diagonal, diagonal_mul_diagonal]
  congr 2
  funext i
  by_cases hi : hA.eigenvalues i = 0 <;> simp [hi]

theorem pseudoInverse_commute (hA : A.IsHermitian) :
    A * pseudoInverse A hA = pseudoInverse A hA * A := by
  unfold pseudoInverse
  conv_lhs => lhs; rw [spectral_real hA]
  conv_rhs => rhs; rw [spectral_real hA]
  simp only [ ← map_mul, diagonal_mul_diagonal, mul_comm]

theorem pseudoInverse_isHermitian (hA : A.IsHermitian) :
    (pseudoInverse A hA).IsHermitian := by
  change star (pseudoInverse A hA) = pseudoInverse A hA
  rw [pseudoInverse, ← map_star]
  simp [star_eq_conjTranspose]

/-- The four Moore–Penrose equations characterize a generalized inverse. -/
def IsMoorePenrose (A G : RealMatrix n) : Prop :=
  A * G * A = A ∧ G * A * G = G ∧ (A * G).IsHermitian ∧ (G * A).IsHermitian

theorem pseudoInverse_isMoorePenrose (hA : A.IsHermitian) :
    IsMoorePenrose A (pseudoInverse A hA) := by
  refine ⟨pseudoInverse_mul_self_mul hA, pseudoInverse_mul_mul_self hA, ?_, ?_⟩
  · change (A * pseudoInverse A hA)ᴴ = A * pseudoInverse A hA
    rw [conjTranspose_mul, (pseudoInverse_isHermitian hA).eq, hA.eq]
    exact (pseudoInverse_commute hA).symm
  · change (pseudoInverse A hA * A)ᴴ = pseudoInverse A hA * A
    rw [conjTranspose_mul, (pseudoInverse_isHermitian hA).eq, hA.eq]
    exact pseudoInverse_commute hA

/-- A contrast is estimable precisely when it belongs to the information range. -/
def Estimable (A : RealMatrix n) (c : Fin n → ℝ) : Prop := ∃ u, A *ᵥ u = c

theorem pseudoInverse_solves (hA : A.IsHermitian) {c : Fin n → ℝ}
    (hc : Estimable A c) : A *ᵥ (pseudoInverse A hA *ᵥ c) = c := by
  obtain ⟨u, rfl⟩ := hc
  rw [mulVec_mulVec, mulVec_mulVec, pseudoInverse_mul_self_mul]

theorem symmetric_dot (hA : A.IsHermitian) (x y : Fin n → ℝ) :
    x ⬝ᵥ (A *ᵥ y) = (A *ᵥ x) ⬝ᵥ y := by
  rw [dotProduct_mulVec]
  have ht : Aᵀ = A := by simpa only [conjTranspose_eq_transpose_of_trivial] using hA.eq
  rw [← ht, vecMul_transpose]
  rw [ht]

theorem estimable_of_kernel_le (hA : A.IsHermitian) (hB : B.IsHermitian)
    (hker : ∀ x, B *ᵥ x = 0 → A *ᵥ x = 0) {c : Fin n → ℝ}
    (hc : Estimable A c) : Estimable B c := by
  let v := pseudoInverse B hB *ᵥ c
  let d := c - B *ᵥ v
  have hBd : B *ᵥ d = 0 := by
    dsimp [d, v]
    rw [mulVec_sub, mulVec_mulVec, mulVec_mulVec,
      Matrix.mul_assoc, pseudoInverse_commute hB,
      ← Matrix.mul_assoc, pseudoInverse_mul_self_mul, sub_self]
  have hAd := hker d hBd
  obtain ⟨u, hu⟩ := hc
  have hdc : d ⬝ᵥ c = 0 := by
    rw [← hu, symmetric_dot hA, hAd, zero_dotProduct]
  have hdb : d ⬝ᵥ (B *ᵥ v) = 0 := by
    rw [symmetric_dot hB, hBd, zero_dotProduct]
  have hdd : d ⬝ᵥ d = 0 := by
    conv_lhs => rhs; change c - B *ᵥ v
    rw [dotProduct_sub, hdc, hdb, sub_self]
  have hd := dotProduct_self_eq_zero.mp hdd
  exact ⟨v, (sub_eq_zero.mp hd).symm⟩

theorem RelativeSandwich.estimable_iff {η : ℝ} (h : RelativeSandwich η A B)
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hη : η < 1) (c : Fin n → ℝ) :
    Estimable A c ↔ Estimable B c := by
  constructor
  · exact estimable_of_kernel_le hA.isHermitian hB.isHermitian
      (fun x hx => (h.kernel_iff hA hB hη x).mpr hx)
  · exact estimable_of_kernel_le hB.isHermitian hA.isHermitian
      (fun x hx => (h.kernel_iff hA hB hη x).mp hx)

/-- Variance of an estimable contrast, evaluated by the actual spectral inverse. -/
def contrastVariance (A : RealMatrix n) (hA : A.IsHermitian) (c : Fin n → ℝ) : ℝ :=
  c ⬝ᵥ (pseudoInverse A hA *ᵥ c)

theorem contrastVariance_nonneg (hA : A.PosSemidef) {c : Fin n → ℝ}
    (hc : Estimable A c) : 0 ≤ contrastVariance A hA.isHermitian c := by
  have h := hA.dotProduct_mulVec_nonneg (pseudoInverse A hA.isHermitian *ᵥ c)
  rw [pseudoInverse_solves hA.isHermitian hc] at h
  simpa only [contrastVariance, star_trivial, dotProduct_comm] using h

/-- Inverse order on a common range, proved by a quadratic completion. -/
theorem contrastVariance_le_scaled (hA : A.PosSemidef) (hB : B.PosSemidef)
    {s : ℝ} (hs : 0 < s) (h : Loewner A (s • B)) {c : Fin n → ℝ}
    (hcA : Estimable A c) (hcB : Estimable B c) :
    contrastVariance B hB.isHermitian c ≤ s * contrastVariance A hA.isHermitian c := by
  let u := pseudoInverse A hA.isHermitian *ᵥ c
  let v := pseudoInverse B hB.isHermitian *ᵥ c
  have hu : A *ᵥ u = c := pseudoInverse_solves hA.isHermitian hcA
  have hv : B *ᵥ v = c := pseudoInverse_solves hB.isHermitian hcB
  have hpos := hA.dotProduct_mulVec_nonneg (s • u - v)
  have hbound := h.quadratic v
  have hcross : u ⬝ᵥ (A *ᵥ v) = c ⬝ᵥ v := by rw [symmetric_dot hA.isHermitian, hu]
  simp only [star_trivial, Matrix.mulVec_sub, Matrix.mulVec_smul,
    dotProduct_sub, sub_dotProduct, dotProduct_smul, smul_dotProduct,
    smul_eq_mul, hu, hcross] at hpos
  simp only [Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul, hv] at hbound
  rw [dotProduct_comm v c] at hbound hpos
  rw [dotProduct_comm u c] at hpos
  change c ⬝ᵥ v ≤ s * (c ⬝ᵥ u)
  nlinarith

theorem RelativeSandwich.contrastVariance {η : ℝ} (h : RelativeSandwich η A B)
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1)
    {c : Fin n → ℝ} (hc : Estimable A c) :
    (1 + η)⁻¹ * contrastVariance A hA.isHermitian c ≤
      contrastVariance B hB.isHermitian c ∧
    contrastVariance B hB.isHermitian c ≤
      (1 - η)⁻¹ * contrastVariance A hA.isHermitian c := by
  have hm : 0 < 1 - η := by linarith
  have hp : 0 < 1 + η := by linarith
  have hcB := (h.estimable_iff hA hB hη1 c).mp hc
  constructor
  · have hh := contrastVariance_le_scaled hB hA hp h.2 hcB hc
    exact (inv_mul_le_iff₀ hp).mpr hh
  · have hh := h.1.smul (inv_nonneg.mpr hm.le)
    have hh' : Loewner A ((1-η)⁻¹ • B) := by
      simpa only [smul_smul, inv_mul_cancel₀ hm.ne', one_smul] using hh
    exact contrastVariance_le_scaled hA hB (inv_pos.mpr hm) hh' hc hcB

end
end DAGSpectral
