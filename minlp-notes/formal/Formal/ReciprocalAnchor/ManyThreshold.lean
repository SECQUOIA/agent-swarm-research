import Mathlib

/-! Finite weighted upper quantiles, including zero and full selected mass. -/

namespace ReciprocalAnchor.ManyLeaf

open scoped BigOperators

variable {𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜]

/-- A finite nonnegative weighted family has a threshold at every admissible mass.
The strict upper tail lies below the mass and the inclusive upper tail above it. -/
theorem exists_weighted_threshold_finset_supported {ι : Type*} (p x : ι → 𝕜)
    (S : Finset ι) (hp : ∀ i ∈ S, 0 ≤ p i) (q : 𝕜)
    (hq : 0 ≤ q) (hqs : q ≤ ∑ i ∈ S, p i) :
    ∃ t : 𝕜, (∑ i ∈ S, if t < x i then p i else 0) ≤ q ∧
      q ≤ (∑ i ∈ S, if t ≤ x i then p i else 0) ∧ (t = 0 ∨ ∃ i ∈ S, t = x i) := by
  classical
  induction S using Finset.induction_on_max_value x generalizing q with
  | empty =>
      have hq0 : q = 0 := by simpa using le_antisymm hqs hq
      subst q
      exact ⟨0, by simp, by simp, Or.inl rfl⟩
  | insert a S ha hmax ih =>
      have hpa : 0 ≤ p a := hp a (Finset.mem_insert_self _ _)
      have hpS : ∀ i ∈ S, 0 ≤ p i := fun i hi => hp i (Finset.mem_insert_of_mem hi)
      by_cases hqa : q ≤ p a
      · refine ⟨x a, ?_, ?_, Or.inr ⟨a, Finset.mem_insert_self _ _, rfl⟩⟩
        · have hz : (∑ i ∈ insert a S, if x a < x i then p i else 0) = 0 := by
            apply Finset.sum_eq_zero
            intro i hi
            have hxi : x i ≤ x a := by
              rcases Finset.mem_insert.mp hi with rfl | hi
              · exact le_rfl
              · exact hmax i hi
            simp [not_lt_of_ge hxi]
          rwa [hz]
        · rw [Finset.sum_insert ha]
          simp only [le_refl, ite_true]
          have hn : 0 ≤ ∑ i ∈ S, if x a ≤ x i then p i else 0 := by
            exact Finset.sum_nonneg fun i hi => by split_ifs <;> simp_all
          linarith
      · have hqa' : 0 < q - p a := sub_pos.mpr (lt_of_not_ge hqa)
        have hqs' : q - p a ≤ ∑ i ∈ S, p i := by
          rw [Finset.sum_insert ha] at hqs
          linarith
        obtain ⟨t, hstrict, hweak, hsupport⟩ := ih hpS (q - p a) hqa'.le hqs'
        have hta : t ≤ x a := by
          by_contra hn
          have hzero : (∑ i ∈ S, if t ≤ x i then p i else 0) = 0 := by
            apply Finset.sum_eq_zero
            intro i hi
            have hxt : x i < t := lt_of_le_of_lt (hmax i hi) (lt_of_not_ge hn)
            simp [not_le_of_gt hxt]
          rw [hzero] at hweak
          linarith
        refine ⟨t, ?_, ?_, ?_⟩
        · rw [Finset.sum_insert ha]
          have hhead : (if t < x a then p a else 0) ≤ p a := by
            split_ifs <;> simp_all
          linarith
        · rw [Finset.sum_insert ha, if_pos hta]
          linarith
        · rcases hsupport with h | ⟨i, hi, he⟩
          · exact Or.inl h
          · exact Or.inr ⟨i, Finset.mem_insert_of_mem hi, he⟩

theorem exists_weighted_threshold_finset {ι : Type*} (p x : ι → 𝕜)
    (S : Finset ι) (hp : ∀ i ∈ S, 0 ≤ p i) (q : 𝕜)
    (hq : 0 ≤ q) (hqs : q ≤ ∑ i ∈ S, p i) :
    ∃ t : 𝕜, (∑ i ∈ S, if t < x i then p i else 0) ≤ q ∧
      q ≤ ∑ i ∈ S, if t ≤ x i then p i else 0 := by
  obtain ⟨t, hlo, hhi, _⟩ := exists_weighted_threshold_finset_supported p x S hp q hq hqs
  exact ⟨t, hlo, hhi⟩

/-- Every finite probability law admits an upper-tail threshold for any mass in `[0,1]`. -/
theorem exists_weighted_threshold {ι : Type*} [Fintype ι] (p x : ι → 𝕜)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1)
    (q : 𝕜) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ∃ t : 𝕜, (∑ i, if t < x i then p i else 0) ≤ q ∧
      q ≤ ∑ i, if t ≤ x i then p i else 0 := by
  apply exists_weighted_threshold_finset p x Finset.univ (fun i _ => hp i) q hq
  simpa [hsum] using hq1

end ReciprocalAnchor.ManyLeaf
