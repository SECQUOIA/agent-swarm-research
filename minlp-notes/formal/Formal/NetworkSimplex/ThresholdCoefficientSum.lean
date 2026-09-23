import Mathlib

/-! A coefficient remains unit when at most one positive and one negative term occur. -/
namespace NetworkSimplex.Chain.Threshold

theorem sum_unit_of_unique_signs {ι : Type*} [Fintype ι] (f : ι → ℤ)
    (hf : ∀ i, -1 ≤ f i ∧ f i ≤ 1)
    (hp : ∀ i k, 0 < f i → 0 < f k → i = k)
    (hn : ∀ i k, f i < 0 → f k < 0 → i = k) :
    -1 ≤ ∑ i, f i ∧ (∑ i, f i) ≤ 1 := by
  classical
  constructor
  · by_cases hex : ∃ k, f k < 0
    · obtain ⟨k, hk⟩ := hex
      have hs : ∑ i, (if i = k then f k else 0) ≤ ∑ i, f i := by
        apply Finset.sum_le_sum
        intro i _
        by_cases hik : i = k
        · simp [hik]
        · simp only [hik, if_false]
          by_contra h
          exact hik (hn i k (lt_of_not_ge h) hk)
      have hs' : f k ≤ ∑ i, f i := by simpa using hs
      exact (hf k).1.trans hs'
    · have hs : 0 ≤ ∑ i, f i := Finset.sum_nonneg (fun i _ => by
        by_contra h; exact hex ⟨i, lt_of_not_ge h⟩)
      omega
  · by_cases hex : ∃ k, 0 < f k
    · obtain ⟨k, hk⟩ := hex
      have hs : ∑ i, f i ≤ ∑ i, (if i = k then f k else 0) := by
        apply Finset.sum_le_sum
        intro i _
        by_cases hik : i = k
        · simp [hik]
        · simp only [hik, if_false]
          by_contra h
          exact hik (hp i k (lt_of_not_ge h) hk)
      have hs' : ∑ i, f i ≤ f k := by simpa using hs
      exact hs'.trans (hf k).2
    · have hs : ∑ i, f i ≤ 0 := Finset.sum_nonpos (fun i _ => by
        by_contra h; exact hex ⟨i, lt_of_not_ge h⟩)
      omega

end NetworkSimplex.Chain.Threshold
