import Formal.DAGSpectral.MaxVolumeTrials
import Formal.DAGSpectral.NormalizationTrials

namespace DAGSpectral
open Module Matrix
open scoped Matrix
namespace NormalizationTrials

/-- The actual sorted subset enumeration contains a good maximum-volume trial
for every selected finite family of factors, including the empty family. -/
theorem exists_good_sorted_trial {p M : ℕ}
    (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ) (hw : ∀ j, 0 < w j)
    (F : Finset (Fin M)) :
    ∃ s : Finset (Fin M), s ⊆ F ∧
      s ∈ trials u (Module.finrank ℝ (familySpan (realFactorFamily (fun j : F => u j)))) ∧
      (∀ j ∈ F, realFactorFamily u j ∈
        familySpan (fun i => realFactorFamily u (label s i))) ∧
      ∀ j ∈ F, ∀ i,
        |Real.sqrt (w j : ℝ) *
          ((transform u w s *ᵥ u j) i : ℝ)| < 2 := by
  classical
  let v : F → Fin p → ℚ := fun j => u j
  let q : F → ℝ := fun j => Real.sqrt (w j : ℝ)
  let r := Module.finrank ℝ (familySpan (realFactorFamily v))
  obtain ⟨b, B, hb, hB, _, _, hcoord⟩ := max_volume_scaled_basis (realFactorFamily v) q
    (fun j => (Real.sqrt_pos.mpr (by exact_mod_cast hw j)).ne')
  let s : Finset (Fin M) := Finset.univ.image (fun i => (b i).val)
  have hsub : s ⊆ F := by
    intro j hj
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hj
    exact (b i).property
  have hcard : s.card = r := by
    change (Finset.univ.image (Subtype.val ∘ b)).card = r
    rw [Finset.card_image_of_injective _ (Subtype.val_injective.comp hb), Finset.card_univ,
      Fintype.card_fin]
  let e : Fin r ≃ Fin s.card := finCongr hcard.symm
  let c : Fin r → F := fun i => ⟨label s (e i), hsub (label_mem s (e i))⟩
  have hc : Function.Injective c := by
    intro i j hij
    apply e.injective
    apply (label s).injective
    have he := congrArg (fun z : F => z.val) hij
    exact he
  have hrange : Set.range c = Set.range b := by
    ext j
    constructor
    · rintro ⟨i, rfl⟩
      have hm : (c i).val ∈ s := label_mem s (e i)
      obtain ⟨k, _, hk⟩ := Finset.mem_image.mp hm
      exact ⟨k, Subtype.ext hk⟩
    · rintro ⟨i, rfl⟩
      have hm : (b i).val ∈ s := Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩
      rw [← label_image s] at hm
      obtain ⟨k, _, hk⟩ := Finset.mem_image.mp hm
      refine ⟨e.symm k, Subtype.ext ?_⟩
      simpa [c] using hk
  obtain ⟨C, hC, hcoordC⟩ := reindex_labeled_basis
    (scaledFamilyVector (realFactorFamily v) q) b c hc hrange B hB hcoord
  let d : Fin s.card → F := fun i => ⟨label s i, hsub (label_mem s i)⟩
  let E := C.reindex e
  have hE (i) : E i = scaledFamilyVector (realFactorFamily v) q (d i) := by
    rw [Basis.reindex_apply, hC]
    simp [c, d]
  have hcoordE (j i) : |E.repr (scaledFamilyVector (realFactorFamily v) q j) i| ≤ 1 := by
    simpa [E] using hcoordC j (e.symm i)
  obtain ⟨hV, hspan, hbound⟩ := rational_trial_of_basis v (fun j : F => w j)
    (fun j => hw j) d E hE hcoordE
  refine ⟨s, hsub, (mem_trials u _ s).mpr ⟨hcard, (independent_iff u s).mpr hV⟩, ?_, ?_⟩
  · intro j hj
    have he : familySpan (fun i => realFactorFamily u (label s i)) =
        familySpan (realFactorFamily v) := hspan
    rw [he]
    exact Submodule.subset_span ⟨⟨j,hj⟩, rfl⟩
  · intro j hj i
    have hh := hbound (scales w s) (fun k => (scale_spec (hw (label s k))).2.2)
      ⟨j,hj⟩ i
    simp only [Matrix.mulVec_smul, Pi.smul_apply, smul_eq_mul] at hh
    change |Real.sqrt (w j : ℝ) * (ratMatrixReal (transform u w s) *ᵥ
      (fun k => (u j k : ℝ))) i| < 2 at hh
    simpa only [ratMatrixReal_mulVec] using hh

end NormalizationTrials
end DAGSpectral
