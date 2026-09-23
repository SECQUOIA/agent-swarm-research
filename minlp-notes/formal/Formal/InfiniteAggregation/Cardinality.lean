import Formal.InfiniteAggregation.Rays
import Mathlib.Analysis.Real.Cardinality

/-! Countability consequences for the indispensable positive rays. -/

noncomputable section

namespace InfiniteAggregation

/-- A countable collection of weights misses one of the prescribed rays. -/
theorem exists_omitted_ray_countable {W : Set (Fin 3 → ℝ)} (hW : W.Countable) :
    ∃ τ ∈ Set.Icc (1 : ℝ) 2, ∀ w ∈ W, ¬SameRay w τ := by
  have hc : (⋃ w ∈ W, {τ : ℝ | SameRay w τ}).Countable := by
    apply hW.biUnion
    intro w _
    apply Set.Subsingleton.countable
    intro τ ht σ hs
    exact sameRay_unique ht hs
  by_contra hn
  push Not at hn
  have hsub : Set.Icc (1 : ℝ) 2 ⊆ ⋃ w ∈ W, {τ : ℝ | SameRay w τ} := by
    intro τ hτ
    obtain ⟨w, hw, hr⟩ := hn τ hτ
    exact Set.mem_iUnion.mpr ⟨w, Set.mem_iUnion.mpr ⟨hw, hr⟩⟩
  have := Cardinal.Real.Icc_countable_iff.mp (hc.mono hsub)
  norm_num at this

/-- Normalize every ray under consideration to third coordinate two. -/
def normalizeRay (w : Fin 3 → ℝ) : Fin 3 → ℝ := (2 / w 2) • w

theorem normalizeRay_pos_smul (w : Fin 3 → ℝ) {a : ℝ} (ha : 0 < a) :
    normalizeRay (a • w) = normalizeRay w := by
  have ha0 : a ≠ 0 := ne_of_gt ha
  ext i
  change (2 / (a * w 2)) * (a * w i) = (2 / w 2) * w i
  by_cases hw : w 2 = 0
  · simp [hw]
  · field_simp

theorem normalizeRay_of_sameRay {w : Fin 3 → ℝ} {τ : ℝ} (h : SameRay w τ) :
    normalizeRay w = rayWeight τ := by
  obtain ⟨a, ha, rfl⟩ := h
  have ha0 : a ≠ 0 := ne_of_gt ha
  ext i
  change (2 / (a * 2)) * (a * rayWeight τ i) = rayWeight τ i
  field_simp

/-- Covering the witness interval requires uncountably many distinct normalized rays. -/
theorem ray_cover_uncountable_normalized {W : Set (Fin 3 → ℝ)}
    (hcover : ∀ τ ∈ Set.Icc (1 : ℝ) 2, ∃ w ∈ W, SameRay w τ) :
    ¬(normalizeRay '' W).Countable := by
  intro hc
  obtain ⟨τ, hτ, hmiss⟩ := exists_omitted_ray_countable hc
  obtain ⟨w, hw, hr⟩ := hcover τ hτ
  apply hmiss (normalizeRay w) ⟨w, hw, rfl⟩
  rw [normalizeRay_of_sameRay hr]
  exact ⟨1, by norm_num, by simp⟩

theorem ray_cover_uncountable {W : Set (Fin 3 → ℝ)}
    (hcover : ∀ τ ∈ Set.Icc (1 : ℝ) 2, ∃ w ∈ W, SameRay w τ) :
    ¬W.Countable := by
  intro hc
  exact ray_cover_uncountable_normalized hcover (hc.image normalizeRay)

end InfiniteAggregation
