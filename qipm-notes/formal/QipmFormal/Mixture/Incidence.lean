import QipmFormal.Mixture.Defs

/-! # Optimal weights for uneven input incidence -/

namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

def reciprocalMass {I : Type*} [Fintype I] (M : I → ℝ) : ℝ := ∑ i, (M i)⁻¹

def harmonicWeight {I : Type*} [Fintype I] (M : I → ℝ) (i : I) : ℝ :=
  (M i)⁻¹ / reciprocalMass M

theorem reciprocalMass_pos {I : Type*} [Fintype I] [Nonempty I]
    {M : I → ℝ} (hM : ∀ i, 0 < M i) : 0 < reciprocalMass M := by
  exact Finset.sum_pos (fun i _ => inv_pos.mpr (hM i)) Finset.univ_nonempty

theorem harmonicWeight_prob {I : Type*} [Fintype I] [Nonempty I]
    {M : I → ℝ} (hM : ∀ i, 0 < M i) : ProbWeights (harmonicWeight M) := by
  constructor
  · intro i
    exact div_nonneg (inv_nonneg.mpr (hM i).le) (reciprocalMass_pos hM).le
  · simp only [harmonicWeight, ← Finset.sum_div]
    exact div_self (ne_of_gt (reciprocalMass_pos hM))

theorem harmonicWeight_cost {I : Type*} [Fintype I] [Nonempty I]
    {M : I → ℝ} (hM : ∀ i, 0 < M i) :
    (∑ i, M i * harmonicWeight M i ^ 2) = (reciprocalMass M)⁻¹ := by
  have hS := ne_of_gt (reciprocalMass_pos hM)
  calc
    (∑ i, M i * harmonicWeight M i ^ 2) =
        ∑ i, (M i)⁻¹ / reciprocalMass M ^ 2 := by
      apply Finset.sum_congr rfl
      intro i _
      dsimp [harmonicWeight]
      field_simp [ne_of_gt (hM i)]
    _ = reciprocalMass M / reciprocalMass M ^ 2 := by
      rw [← Finset.sum_div]; rfl
    _ = (reciprocalMass M)⁻¹ := by field_simp

/-- The lower bound even holds for signed weights whose sum is one. -/
theorem incidence_cost_lower {I : Type*} [Fintype I]
    {M w : I → ℝ} (hM : ∀ i, 0 < M i) (hw : ∑ i, w i = 1) :
    (reciprocalMass M)⁻¹ ≤ ∑ i, M i * w i ^ 2 := by
  have h := Finset.sq_sum_div_le_sum_sq_div Finset.univ w
    (g := fun i => (M i)⁻¹) (fun i _ => inv_pos.mpr (hM i))
  simpa [hw, reciprocalMass, div_inv_eq_mul, mul_comm] using h

theorem harmonicWeight_minimizes {I : Type*} [Fintype I] [Nonempty I]
    {M w : I → ℝ} (hM : ∀ i, 0 < M i) (hw : ProbWeights w) :
    (∑ i, M i * harmonicWeight M i ^ 2) ≤ ∑ i, M i * w i ^ 2 := by
  rw [harmonicWeight_cost hM]
  exact incidence_cost_lower hM hw.2

theorem uniform_incidence_cost {I : Type*} [Fintype I] (M : I → ℝ) :
    (∑ i, M i * uniformWeight I i ^ 2) =
      (∑ i, M i) / (Fintype.card I : ℝ) ^ 2 := by
  simp only [uniformWeight, ← Finset.sum_mul, inv_pow, div_eq_mul_inv]

theorem harmonic_cost_le_uniform {I : Type*} [Fintype I] [Nonempty I]
    {M : I → ℝ} (hM : ∀ i, 0 < M i) :
    (reciprocalMass M)⁻¹ ≤ (∑ i, M i) / (Fintype.card I : ℝ) ^ 2 := by
  rw [← uniform_incidence_cost]
  exact incidence_cost_lower hM (uniformWeight_prob I).2

end
end QipmFormal.Mixture
