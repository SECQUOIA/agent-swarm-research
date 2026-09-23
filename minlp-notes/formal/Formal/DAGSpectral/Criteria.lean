import Formal.DAGSpectral.CriteriaEigen
import Formal.DAGSpectral.Determinant

open scoped MatrixOrder
namespace DAGSpectral
noncomputable section

/-- Smallest-eigenvalue optimality is an actual homogeneous PSD criterion. -/
theorem minimumEigenvalue_criterion {n : ℕ} [NeZero n] :
    HomogeneousCriterion 1 (minimumEigenvalue : RealMatrix n → ℝ) where
  degree_pos := by norm_num
  nonneg _ hA := minimumEigenvalue_nonneg hA
  monotone _ _ hA hB hAB := minimumEigenvalue_mono hA hB hAB
  homogeneous _ hA c hc := by simpa using minimumEigenvalue_smul hA hc

/-- One best E-optimal representative has factor `1-η` against every feasible
matrix, including the case where all matrices are singular. -/
theorem IsRelativeCover.eigenvalue_maximum {α : Type*} {n : ℕ} [NeZero n] {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (hJ : ∀ a ∈ F, (J a).PosSemidef) (hη : η ≤ 1) :
    ∃ b ∈ R, (∀ c ∈ R, minimumEigenvalue (J c) ≤ minimumEigenvalue (J b)) ∧
      ∀ a ∈ F, (1-η) * minimumEigenvalue (J a) ≤ minimumEigenvalue (J b) := by
  simpa using h.homogeneous_maximum hF hJ hη minimumEigenvalue_criterion

/-- D-optimality with the source's accuracy choice `η=ε/n`. -/
theorem IsRelativeCover.determinant_maximum {α : Type*} {n : ℕ} {ε : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover (ε / n) J F R)
    (hF : F.Nonempty) (hJ : ∀ a ∈ F, (J a).PosSemidef)
    (hn : 0 < n) (hε : 0 ≤ ε) (hε1 : ε ≤ 1) :
    ∃ b ∈ R, (∀ c ∈ R, (J c).det ≤ (J b).det) ∧
      ∀ a ∈ F, (1-ε) * (J a).det ≤ (J b).det := by
  apply h.maximize hF (fun a => (J a).det) (fun a => (1-ε)*(J a).det)
  intro a ha b hb hs
  exact hs.det_lower_eps (hJ a ha) (hJ b (h.1 hb)) hn hε hε1

/-- Determinant roots, without taking a logarithm. -/
def determinantRoot {n : ℕ} (A : RealMatrix n) : ℝ := A.det ^ (1/(n:ℝ))

theorem determinantRoot_criterion {n : ℕ} (hn : 0 < n) :
    HomogeneousCriterion 1 (determinantRoot : RealMatrix n → ℝ) := by
  have hnr : (0:ℝ)<n := by exact_mod_cast hn
  refine ⟨by norm_num, ?_, ?_, ?_⟩
  · intro A hA
    exact Real.rpow_nonneg hA.det_nonneg _
  · intro A B hA hB hAB
    exact Real.rpow_le_rpow hA.det_nonneg (hAB.det_le hA hB) (by positivity)
  · intro A hA c hc
    rw [determinantRoot, Matrix.det_smul, Fintype.card_fin,
      Real.mul_rpow (pow_nonneg hc _) hA.det_nonneg,
      ← Real.rpow_natCast, ← Real.rpow_mul hc]
    have he : (n:ℝ)*(1/(n:ℝ))=1 := by field_simp
    rw [he, Real.rpow_one]
    rfl

theorem IsRelativeCover.determinantRoot_maximum {α : Type*} {n : ℕ} {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (hJ : ∀ a ∈ F, (J a).PosSemidef) (hη : η ≤ 1) (hn : 0 < n) :
    ∃ b ∈ R, (∀ c ∈ R, determinantRoot (J c) ≤ determinantRoot (J b)) ∧
      ∀ a ∈ F, (1-η) * determinantRoot (J a) ≤ determinantRoot (J b) := by
  simpa using h.homogeneous_maximum hF hJ hη (determinantRoot_criterion hn)

/-- Singular feasible matrices have E-value zero, so their finite-cover optimum
is zero too. This is not a positive-definiteness assumption. -/
theorem IsRelativeCover.eigenvalue_all_singular {α : Type*} {n : ℕ} [NeZero n] {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hJ : ∀ a ∈ F, (J a).PosSemidef) (hsing : ∀ a ∈ F, (J a).det = 0) :
    ∀ b ∈ R, minimumEigenvalue (J b) = 0 := by
  intro b hb
  exact (minimumEigenvalue_eq_zero_iff (hJ b (h.1 hb))).mpr (hsing b (h.1 hb))

end
end DAGSpectral
