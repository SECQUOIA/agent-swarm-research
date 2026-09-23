import Formal.DAGSpectral.CriteriaBasic
import Formal.DAGSpectral.Inverse
import Mathlib.Data.ENNReal.Real
import Formal.DAGSpectral.Pseudoinverse

namespace DAGSpectral
open Matrix
open scoped ENNReal NNReal BigOperators
noncomputable section

/-- A-optimal cost: singular information has infinite cost. -/
def inverseTraceCost {n : ℕ} (A : RealMatrix n) : ℝ≥0∞ := by
  classical
  exact if A.PosDef then ENNReal.ofReal (Matrix.trace A⁻¹) else ⊤

theorem inverseTraceCost_ne_top_iff {n : ℕ} (A : RealMatrix n) :
    inverseTraceCost A ≠ ⊤ ↔ A.PosDef := by
  unfold inverseTraceCost
  split_ifs with h <;> simp [h]

theorem RelativeSandwich.posDef_iff {n : ℕ} {A B : RealMatrix n} {η : ℝ}
    (h : RelativeSandwich η A B) (hA : A.PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    A.PosDef ↔ B.PosDef := by
  constructor
  · exact fun hA => h.posDef hA hη1
  · intro hB
    apply Matrix.PosDef.of_dotProduct_mulVec_pos hA.isHermitian
    intro x hx
    have hb := hB.dotProduct_mulVec_pos hx
    have hu := h.2.quadratic x
    have ha := hA.dotProduct_mulVec_nonneg x
    simp only [Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul, star_trivial] at hb hu ha ⊢
    nlinarith

theorem RelativeSandwich.inverseTraceCost_upper {n : ℕ} {A B : RealMatrix n} {η : ℝ}
    (h : RelativeSandwich η A B) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    inverseTraceCost B ≤ ENNReal.ofReal ((1-η)⁻¹) * inverseTraceCost A := by
  have hp : 0 < (1-η)⁻¹ := by positivity
  by_cases hA : A.PosDef
  · have hB := h.posDef hA hη1
    rw [inverseTraceCost, if_pos hB, inverseTraceCost, if_pos hA,
      ← ENNReal.ofReal_mul hp.le]
    exact ENNReal.ofReal_le_ofReal (h.trace_inverse hA hη0 hη1).2
  · simp [inverseTraceCost, hA, ENNReal.ofReal_ne_zero_iff.mpr hp]

theorem IsRelativeCover.inverseTrace_minimum {α : Type*} {n : ℕ} {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    ∃ b ∈ R, (∀ c ∈ R, inverseTraceCost (J b) ≤ inverseTraceCost (J c)) ∧
      ∀ a ∈ F, inverseTraceCost (J b) ≤
        ENNReal.ofReal ((1-η)⁻¹) * inverseTraceCost (J a) := by
  apply h.minimize hF (fun a => inverseTraceCost (J a))
    (fun a => ENNReal.ofReal ((1-η)⁻¹) * inverseTraceCost (J a))
  intro a _ b _ hs
  exact hs.inverseTraceCost_upper hη0 hη1

theorem IsRelativeCover.positiveDefinite_exists_iff {α : Type*} {n : ℕ} {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hη1 : η < 1) :
    (∃ a ∈ F, (J a).PosDef) ↔ ∃ b ∈ R, (J b).PosDef := by
  constructor
  · rintro ⟨a,ha,hA⟩
    obtain ⟨b,hb,hs⟩ := h.2 a ha
    exact ⟨b,hb,hs.posDef hA hη1⟩
  · rintro ⟨b,hb,hB⟩
    exact ⟨b,h.1 hb,hB⟩

/-- The source's parameter choice gives exactly the ratio `1+ε`. -/
theorem IsRelativeCover.inverseTrace_minimum_eps {α : Type*} {n : ℕ} {ε : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover (ε / (1 + ε)) J F R)
    (hF : F.Nonempty) (hε : 0 ≤ ε) :
    ∃ b ∈ R, (∀ c ∈ R, inverseTraceCost (J b) ≤ inverseTraceCost (J c)) ∧
      ∀ a ∈ F, inverseTraceCost (J b) ≤ ENNReal.ofReal (1+ε) * inverseTraceCost (J a) := by
  have hd : 0 < 1+ε := by linarith
  have hlo : 0 ≤ ε/(1+ε) := div_nonneg hε hd.le
  have hup : ε/(1+ε) < 1 := (div_lt_one hd).mpr (by linarith)
  have he : (1-ε/(1+ε))⁻¹ = 1+ε := by field_simp; ring
  simpa only [he] using h.inverseTrace_minimum hF hlo hup

/-- Contrast cost is infinite exactly when a PSD information matrix cannot
estimate the contrast. The pseudoinverse is used only on its actual range. -/
def contrastCost {n : ℕ} (A : RealMatrix n) (c : Fin n → ℝ) : ℝ≥0∞ := by
  classical
  exact if hA : A.PosSemidef then
    if Estimable A c then ENNReal.ofReal (contrastVariance A hA.isHermitian c) else ⊤
  else ⊤

theorem contrastCost_ne_top_iff {n : ℕ} {A : RealMatrix n} (hA : A.PosSemidef)
    (c : Fin n → ℝ) : contrastCost A c ≠ ⊤ ↔ Estimable A c := by
  unfold contrastCost
  rw [dif_pos hA]
  split_ifs with hc <;> simp [hc]

theorem RelativeSandwich.contrastCost_upper {n : ℕ} {A B : RealMatrix n} {η : ℝ}
    (h : RelativeSandwich η A B) (hA : A.PosSemidef) (hB : B.PosSemidef)
    (hη0 : 0 ≤ η) (hη1 : η < 1) (c : Fin n → ℝ) :
    contrastCost B c ≤ ENNReal.ofReal ((1-η)⁻¹) * contrastCost A c := by
  have hp : 0 < (1-η)⁻¹ := by positivity
  by_cases hc : Estimable A c
  · have hcB := (h.estimable_iff hA hB hη1 c).mp hc
    rw [contrastCost, dif_pos hB, if_pos hcB, contrastCost, dif_pos hA, if_pos hc,
      ← ENNReal.ofReal_mul hp.le]
    exact ENNReal.ofReal_le_ofReal (h.contrastVariance hA hB hη0 hη1 hc).2
  · simp [contrastCost, hA, hc, ENNReal.ofReal_ne_zero_iff.mpr hp]

theorem IsRelativeCover.contrast_minimum {α : Type*} {n : ℕ} {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (hJ : ∀ a ∈ F, (J a).PosSemidef)
    (hη0 : 0 ≤ η) (hη1 : η < 1) (c : Fin n → ℝ) :
    ∃ b ∈ R, (∀ r ∈ R, contrastCost (J b) c ≤ contrastCost (J r) c) ∧
      ∀ a ∈ F, contrastCost (J b) c ≤
        ENNReal.ofReal ((1-η)⁻¹) * contrastCost (J a) c := by
  apply h.minimize hF (fun a => contrastCost (J a) c)
    (fun a => ENNReal.ofReal ((1-η)⁻¹) * contrastCost (J a) c)
  intro a ha b hb hs
  exact hs.contrastCost_upper (hJ a ha) (hJ b (h.1 hb)) hη0 hη1 c

theorem IsRelativeCover.estimable_exists_iff {α : Type*} {n : ℕ} {η : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hJ : ∀ a ∈ F, (J a).PosSemidef) (hη1 : η < 1) (c : Fin n → ℝ) :
    (∃ a ∈ F, Estimable (J a) c) ↔ ∃ b ∈ R, Estimable (J b) c := by
  constructor
  · rintro ⟨a,ha,hA⟩
    obtain ⟨b,hb,hs⟩ := h.2 a ha
    exact ⟨b,hb,(hs.estimable_iff (hJ a ha) (hJ b (h.1 hb)) hη1 c).mp hA⟩
  · rintro ⟨b,hb,hB⟩
    exact ⟨b,h.1 hb,hB⟩

theorem IsRelativeCover.contrast_minimum_eps {α : Type*} {n : ℕ} {ε : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover (ε / (1 + ε)) J F R)
    (hF : F.Nonempty) (hJ : ∀ a ∈ F, (J a).PosSemidef) (hε : 0 ≤ ε)
    (c : Fin n → ℝ) :
    ∃ b ∈ R, (∀ r ∈ R, contrastCost (J b) c ≤ contrastCost (J r) c) ∧
      ∀ a ∈ F, contrastCost (J b) c ≤ ENNReal.ofReal (1+ε) * contrastCost (J a) c := by
  have hd : 0 < 1+ε := by linarith
  have hlo : 0 ≤ ε/(1+ε) := div_nonneg hε hd.le
  have hup : ε/(1+ε) < 1 := (div_lt_one hd).mpr (by linarith)
  have he : (1-ε/(1+ε))⁻¹ = 1+ε := by field_simp; ring
  simpa only [he] using h.contrast_minimum hF hJ hlo hup c

/-- A finite nonnegative weighted sum, with zero-weight infinite terms treated
as zero by the extended nonnegative-real arithmetic. -/
def weightedContrastCost {κ : Type*} [Fintype κ] {n : ℕ}
    (w : κ → ℝ≥0) (c : κ → Fin n → ℝ) (A : RealMatrix n) : ℝ≥0∞ :=
  ∑ i, (w i : ℝ≥0∞) * contrastCost A (c i)

theorem RelativeSandwich.weightedContrastCost_upper {κ : Type*} [Fintype κ]
    {n : ℕ} {A B : RealMatrix n} {η : ℝ} (h : RelativeSandwich η A B)
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1)
    (w : κ → ℝ≥0) (c : κ → Fin n → ℝ) :
    weightedContrastCost w c B ≤ ENNReal.ofReal ((1-η)⁻¹) * weightedContrastCost w c A := by
  unfold weightedContrastCost
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  have hi := mul_le_mul_right (h.contrastCost_upper hA hB hη0 hη1 (c i)) (w i : ℝ≥0∞)
  simpa only [mul_assoc, mul_left_comm, mul_comm] using hi

theorem IsRelativeCover.weightedContrast_minimum {α κ : Type*} [Fintype κ]
    {n : ℕ} {η : ℝ} {J : α → RealMatrix n} {F R : Finset α}
    (h : IsRelativeCover η J F R) (hF : F.Nonempty)
    (hJ : ∀ a ∈ F, (J a).PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1)
    (w : κ → ℝ≥0) (c : κ → Fin n → ℝ) :
    ∃ b ∈ R, (∀ r ∈ R, weightedContrastCost w c (J b) ≤ weightedContrastCost w c (J r)) ∧
      ∀ a ∈ F, weightedContrastCost w c (J b) ≤
        ENNReal.ofReal ((1-η)⁻¹) * weightedContrastCost w c (J a) := by
  apply h.minimize hF (fun a => weightedContrastCost w c (J a))
    (fun a => ENNReal.ofReal ((1-η)⁻¹) * weightedContrastCost w c (J a))
  intro a ha b hb hs
  exact hs.weightedContrastCost_upper (hJ a ha) (hJ b (h.1 hb)) hη0 hη1 w c

theorem IsRelativeCover.weightedContrast_minimum_eps {α κ : Type*} [Fintype κ]
    {n : ℕ} {ε : ℝ} {J : α → RealMatrix n} {F R : Finset α}
    (h : IsRelativeCover (ε / (1 + ε)) J F R) (hF : F.Nonempty)
    (hJ : ∀ a ∈ F, (J a).PosSemidef) (hε : 0 ≤ ε)
    (w : κ → ℝ≥0) (c : κ → Fin n → ℝ) :
    ∃ b ∈ R, (∀ r ∈ R, weightedContrastCost w c (J b) ≤ weightedContrastCost w c (J r)) ∧
      ∀ a ∈ F, weightedContrastCost w c (J b) ≤
        ENNReal.ofReal (1+ε) * weightedContrastCost w c (J a) := by
  have hd : 0 < 1+ε := by linarith
  have hlo : 0 ≤ ε/(1+ε) := div_nonneg hε hd.le
  have hup : ε/(1+ε) < 1 := (div_lt_one hd).mpr (by linarith)
  have he : (1-ε/(1+ε))⁻¹ = 1+ε := by field_simp; ring
  simpa only [he] using h.weightedContrast_minimum hF hJ hlo hup w c

end
end DAGSpectral
