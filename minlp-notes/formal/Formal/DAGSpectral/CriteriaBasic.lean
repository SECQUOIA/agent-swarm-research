import Formal.DAGSpectral.PSDAlgebra
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Finset.Max

namespace DAGSpectral
noncomputable section

/-- Every feasible object has one feasible representative satisfying the full
relative matrix sandwich. The cover can be reused for different criteria. -/
def IsRelativeCover {α : Type*} {n : ℕ} (η : ℝ) (J : α → RealMatrix n)
    (F R : Finset α) : Prop :=
  R ⊆ F ∧ ∀ a ∈ F, ∃ b ∈ R, RelativeSandwich η (J a) (J b)

namespace IsRelativeCover
variable {α : Type*} {n : ℕ} {η : ℝ} {J : α → RealMatrix n} {F R : Finset α}

theorem nonempty (h : IsRelativeCover η J F R) (hF : F.Nonempty) : R.Nonempty := by
  obtain ⟨a,ha⟩ := hF
  obtain ⟨b,hb,_⟩ := h.2 a ha
  exact ⟨b,hb⟩

theorem empty_iff (h : IsRelativeCover η J F R) : R = ∅ ↔ F = ∅ := by
  constructor
  · intro hr
    by_contra hf
    have hh := h.nonempty (Finset.nonempty_iff_ne_empty.mpr hf)
    simp [hr] at hh
  · intro hf
    exact Finset.subset_empty.mp (hf ▸ h.1)

/-- Maximizing an objective on the finite cover gives one representative that
simultaneously meets every per-object lower comparison. -/
theorem maximize {β : Type*} [LinearOrder β] (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (f g : α → β)
    (hcompare : ∀ a ∈ F, ∀ b ∈ R, RelativeSandwich η (J a) (J b) → g a ≤ f b) :
    ∃ b ∈ R, (∀ c ∈ R, f c ≤ f b) ∧ ∀ a ∈ F, g a ≤ f b := by
  obtain ⟨b,hb,hm⟩ := Finset.exists_max_image R f (h.nonempty hF)
  refine ⟨b,hb,hm,?_⟩
  intro a ha
  obtain ⟨c,hc,hs⟩ := h.2 a ha
  exact (hcompare a ha c hc hs).trans (hm c hc)

/-- The minimization version also works for extended costs with value infinity. -/
theorem minimize {β : Type*} [LinearOrder β] (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (f g : α → β)
    (hcompare : ∀ a ∈ F, ∀ b ∈ R, RelativeSandwich η (J a) (J b) → f b ≤ g a) :
    ∃ b ∈ R, (∀ c ∈ R, f b ≤ f c) ∧ ∀ a ∈ F, f b ≤ g a := by
  obtain ⟨b,hb,hm⟩ := Finset.exists_min_image R f (h.nonempty hF)
  refine ⟨b,hb,hm,?_⟩
  intro a ha
  obtain ⟨c,hc,hs⟩ := h.2 a ha
  exact (hm c hc).trans (hcompare a ha c hc hs)
/-- A common congruence reuses the same feasible representatives. -/
theorem congruence (h : IsRelativeCover η J F R) {m : ℕ}
    (K : Matrix (Fin m) (Fin n) ℝ) :
    IsRelativeCover η (fun a => K * J a * K.transpose) F R := by
  refine ⟨h.1, ?_⟩
  intro a ha
  obtain ⟨b,hb,hs⟩ := h.2 a ha
  exact ⟨b,hb,hs.congruence K⟩

/-- Adding a common PSD prior needs no new representatives. -/
theorem add_prior (h : IsRelativeCover η J F R) (hη : 0 ≤ η)
    {H : RealMatrix n} (hH : H.PosSemidef) :
    IsRelativeCover η (fun a => J a + H) F R := by
  refine ⟨h.1, ?_⟩
  intro a ha
  obtain ⟨b,hb,hs⟩ := h.2 a ha
  exact ⟨b,hb,hs.add_prior hη hH⟩

end IsRelativeCover

/-- The assumptions on the user's objective, restricted to PSD matrices.
No concavity or objective-evaluation oracle is included. -/
structure HomogeneousCriterion {n : ℕ} (q : ℝ) (Φ : RealMatrix n → ℝ) : Prop where
  degree_pos : 0 < q
  nonneg : ∀ A, A.PosSemidef → 0 ≤ Φ A
  monotone : ∀ A B, A.PosSemidef → B.PosSemidef → Loewner A B → Φ A ≤ Φ B
  homogeneous : ∀ A, A.PosSemidef → ∀ c : ℝ, 0 ≤ c → Φ (c • A) = c ^ q * Φ A

theorem RelativeSandwich.criterion_lower {n : ℕ} {A B : RealMatrix n} {η q : ℝ}
    {Φ : RealMatrix n → ℝ} (h : RelativeSandwich η A B)
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hη : η ≤ 1)
    (hΦ : HomogeneousCriterion q Φ) : (1-η)^q * Φ A ≤ Φ B := by
  have hc : 0 ≤ 1-η := sub_nonneg.mpr hη
  rw [← hΦ.homogeneous A hA (1-η) hc]
  exact hΦ.monotone _ _ (hA.smul hc) hB h.1

/-- A single selected representative achieves the homogeneous approximation
ratio against every feasible matrix, hence against an optimal feasible one. -/
theorem IsRelativeCover.homogeneous_maximum {α : Type*} {n : ℕ} {η q : ℝ}
    {J : α → RealMatrix n} {F R : Finset α} (h : IsRelativeCover η J F R)
    (hF : F.Nonempty) (hJ : ∀ a ∈ F, (J a).PosSemidef) (hη : η ≤ 1)
    {Φ : RealMatrix n → ℝ} (hΦ : HomogeneousCriterion q Φ) :
    ∃ b ∈ R, (∀ c ∈ R, Φ (J c) ≤ Φ (J b)) ∧
      ∀ a ∈ F, (1-η)^q * Φ (J a) ≤ Φ (J b) := by
  apply h.maximize hF (fun a => Φ (J a)) (fun a => (1-η)^q * Φ (J a))
  intro a ha b hb hs
  exact hs.criterion_lower (hJ a ha) (hJ b (h.1 hb)) hη hΦ

end
end DAGSpectral
