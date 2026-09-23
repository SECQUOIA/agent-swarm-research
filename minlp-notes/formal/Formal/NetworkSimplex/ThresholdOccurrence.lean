import Formal.NetworkSimplex.Circuits

/-! Finite circuit occurrence properties used by the three-label coefficient proof. -/
namespace NetworkSimplex.ThreeStateCircuits

/-- The positive singleton normal for a label. -/
def singletonIndex (j : Fin 3) : Fin 11 := ⟨j.val, by omega⟩
/-- The negative singleton normal for a label. -/
def negativeSingletonIndex (j : Fin 3) : Fin 11 := ⟨7 + j.val, by omega⟩
/-- An arbitrary positive subset normal. -/
def positiveIndex (e : Fin 7) : Fin 11 := ⟨e.val, by omega⟩

/-- All positive-normal weights and all negative-singleton weights are at most one. -/
theorem weight_le_one_except_full : ∀ (c : Fin 16) (i : Fin 11),
    i ≠ 10 → weight c i ≤ 1 := by decide +kernel

theorem negative_full_weight : ∀ c : Fin 16,
    weight c 10 = 0 ∨ weight c 10 = 1 ∨ weight c 10 = 2 := by decide +kernel

/-- The sole doubled weight is the half-cover's negative-full normal. -/
theorem doubled_weight_iff : ∀ (c : Fin 16) (i : Fin 11),
    weight c i = 2 ↔ c = 15 ∧ i = 10 := by decide +kernel

theorem total_weight_le_five : ∀ c : Fin 16, ∑ i, weight c i ≤ 5 := by decide +kernel

/-- A positive singleton cannot occur with a different positive subset containing its label. -/
theorem singleton_positive_conflict : ∀ (c : Fin 16) (j : Fin 3) (e : Fin 7),
    normal (positiveIndex e) j = 1 → positiveIndex e ≠ singletonIndex j →
      weight c (singletonIndex j) = 0 ∨ weight c (positiveIndex e) = 0 := by
  decide +kernel

/-- A negative singleton cannot occur with a positive subset excluding its label. -/
theorem negative_singleton_positive_conflict : ∀ (c : Fin 16) (j : Fin 3) (e : Fin 7),
    normal (positiveIndex e) j = 0 →
      weight c (negativeSingletonIndex j) = 0 ∨ weight c (positiveIndex e) = 0 := by
  decide +kernel

/-- Positive occurrences of a fixed product are unique on every circuit support. -/
theorem positive_occurrence_unique (c : Fin 16) (j : Fin 3) (e : Fin 7)
    {i k : Fin 11} (hi : 0 < weight c i) (hk : 0 < weight c k)
    (hpi : i = singletonIndex j ∨ i = positiveIndex e ∧ normal (positiveIndex e) j = 1)
    (hpk : k = singletonIndex j ∨ k = positiveIndex e ∧ normal (positiveIndex e) j = 1) :
    i = k := by
  rcases hpi with rfl | ⟨rfl, he⟩ <;> rcases hpk with rfl | ⟨rfl, he'⟩
  · rfl
  · by_contra hn
    rcases singleton_positive_conflict c j e he' (Ne.symm hn) with h | h <;> omega
  · by_contra hn
    rcases singleton_positive_conflict c j e he hn with h | h <;> omega
  · rfl

/-- Negative occurrences of a fixed product are unique on every circuit support. -/
theorem negative_occurrence_unique (c : Fin 16) (j : Fin 3) (e : Fin 7)
    {i k : Fin 11} (hi : 0 < weight c i) (hk : 0 < weight c k)
    (hpi : i = negativeSingletonIndex j ∨
      i = positiveIndex e ∧ normal (positiveIndex e) j = 0)
    (hpk : k = negativeSingletonIndex j ∨
      k = positiveIndex e ∧ normal (positiveIndex e) j = 0) : i = k := by
  rcases hpi with rfl | ⟨rfl, he⟩ <;> rcases hpk with rfl | ⟨rfl, he'⟩
  · rfl
  · rcases negative_singleton_positive_conflict c j e he' with h | h <;> omega
  · rcases negative_singleton_positive_conflict c j e he with h | h <;> omega
  · rfl

/-- Once all occurrences of a single product are collected, its circuit coefficient is unit.
The hypotheses describe the local singleton row and the one endpoint row where
that product can occur; they allow either occurrence to be absent. -/
theorem signed_occurrence_sum_unit (c : Fin 16) (j : Fin 3) (ep en : Fin 7)
    (f : Fin 11 → ℤ) (hf : ∀ i, -1 ≤ f i ∧ f i ≤ 1)
    (hp : ∀ i, 0 < f i →
      i = singletonIndex j ∨ i = positiveIndex ep ∧ normal (positiveIndex ep) j = 1)
    (hn : ∀ i, f i < 0 →
      i = negativeSingletonIndex j ∨ i = positiveIndex en ∧ normal (positiveIndex en) j = 0) :
    -1 ≤ ∑ i, weight c i * f i ∧ ∑ i, weight c i * f i ≤ 1 := by
  have h10 : f 10 = 0 := by
    by_contra h
    rcases lt_or_gt_of_ne h with h | h
    · rcases hn 10 h with he | ⟨he, _⟩
      · have he' := congrArg Fin.val he
        dsimp [negativeSingletonIndex] at he'; omega
      · have he' := congrArg Fin.val he
        dsimp [positiveIndex] at he'; omega
    · rcases hp 10 h with he | ⟨he, _⟩
      · have he' := congrArg Fin.val he
        dsimp [singletonIndex] at he'; omega
      · have he' := congrArg Fin.val he
        dsimp [positiveIndex] at he'; omega
  have hterm : ∀ i, -1 ≤ weight c i * f i ∧ weight c i * f i ≤ 1 := by
    intro i
    by_cases hi : i = 10
    · subst i; simp [h10]
    · have hw := weight_nonnegative c i
      have hw' := weight_le_one_except_full c i hi
      have hh := hf i
      interval_cases hwi : weight c i <;> simp_all
  have hpos : ∀ i k, 0 < weight c i * f i → 0 < weight c k * f k → i = k := by
    intro i k hi hk
    have hwi : 0 < weight c i := by
      by_contra h
      have heq := le_antisymm (le_of_not_gt h) (weight_nonnegative c i)
      simp [heq] at hi
    have hwk : 0 < weight c k := by
      by_contra h
      have heq := le_antisymm (le_of_not_gt h) (weight_nonnegative c k)
      simp [heq] at hk
    have hfi : 0 < f i := by nlinarith [weight_nonnegative c i]
    have hfk : 0 < f k := by nlinarith [weight_nonnegative c k]
    exact positive_occurrence_unique c j ep hwi hwk (hp i hfi) (hp k hfk)
  have hneg : ∀ i k, weight c i * f i < 0 → weight c k * f k < 0 → i = k := by
    intro i k hi hk
    have hwi : 0 < weight c i := by
      by_contra h
      have heq := le_antisymm (le_of_not_gt h) (weight_nonnegative c i)
      simp [heq] at hi
    have hwk : 0 < weight c k := by
      by_contra h
      have heq := le_antisymm (le_of_not_gt h) (weight_nonnegative c k)
      simp [heq] at hk
    have hfi : f i < 0 := by nlinarith [weight_nonnegative c i]
    have hfk : f k < 0 := by nlinarith [weight_nonnegative c k]
    exact negative_occurrence_unique c j en hwi hwk (hn i hfi) (hn k hfk)
  constructor
  · by_cases hex : ∃ k, weight c k * f k < 0
    · obtain ⟨k, hk⟩ := hex
      have hs : ∑ i, (if i = k then weight c k * f k else 0) ≤ ∑ i, weight c i * f i := by
        apply Finset.sum_le_sum
        intro i _
        by_cases hik : i = k
        · simp [hik]
        · simp only [hik, if_false]
          by_contra h
          exact hik (hneg i k (lt_of_not_ge h) hk)
      have hs' : weight c k * f k ≤ ∑ i, weight c i * f i := by simpa using hs
      exact (hterm k).1.trans hs'
    · have hs : 0 ≤ ∑ i, weight c i * f i := Finset.sum_nonneg (fun i _ => by
        by_contra h; exact hex ⟨i, lt_of_not_ge h⟩)
      omega
  · by_cases hex : ∃ k, 0 < weight c k * f k
    · obtain ⟨k, hk⟩ := hex
      have hs : ∑ i, weight c i * f i ≤ ∑ i, (if i = k then weight c k * f k else 0) := by
        apply Finset.sum_le_sum
        intro i _
        by_cases hik : i = k
        · simp [hik]
        · simp only [hik, if_false]
          by_contra h
          exact hik (hpos i k (lt_of_not_ge h) hk)
      have hs' : ∑ i, weight c i * f i ≤ weight c k * f k := by simpa using hs
      exact hs'.trans (hterm k).2
    · have hs : ∑ i, weight c i * f i ≤ 0 := Finset.sum_nonpos (fun i _ => by
        by_contra h; exact hex ⟨i, lt_of_not_ge h⟩)
      omega

end NetworkSimplex.ThreeStateCircuits
