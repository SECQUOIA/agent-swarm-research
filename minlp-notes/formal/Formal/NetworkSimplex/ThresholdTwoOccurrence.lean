import Formal.NetworkSimplex.ThresholdRows
import Formal.NetworkSimplex.ThresholdCoefficientSum

/-! The five two-label circuits and their occurrence constraints. -/
namespace NetworkSimplex.TwoStateCircuits

def normal : Fin 6 → Fin 2 → ℤ :=
  ![![1, 0], ![0, 1], ![1, 1], ![-1, 0], ![0, -1], ![-1, -1]]

def weight : Fin 5 → Fin 6 → ℤ :=
  ![![1, 0, 0, 1, 0, 0], ![0, 1, 0, 0, 1, 0], ![0, 0, 1, 0, 0, 1],
    ![1, 1, 0, 0, 0, 1], ![0, 0, 1, 1, 1, 0]]

def singletonIndex (j : Fin 2) : Fin 6 := ⟨j.val, by omega⟩
def negativeSingletonIndex (j : Fin 2) : Fin 6 := ⟨3 + j.val, by omega⟩
def positiveIndex (e : Fin 3) : Fin 6 := ⟨e.val, by omega⟩

theorem normal_cancellation : ∀ (c : Fin 5) (j : Fin 2),
    ∑ k, weight c k * normal k j = 0 := by decide +kernel

theorem weight_nonzero : ∀ c : Fin 5, ∃ k, weight c k ≠ 0 := by decide +kernel

theorem weight_injective : Function.Injective weight := by decide +kernel

theorem weight_nonnegative : ∀ (c : Fin 5) (k : Fin 6), 0 ≤ weight c k := by decide +kernel

theorem weight_le_one_except_full : ∀ (c : Fin 5) (k : Fin 6),
    k ≠ 5 → weight c k ≤ 1 := by decide +kernel

theorem weight_le_one : ∀ (c : Fin 5) (k : Fin 6), weight c k ≤ 1 := by decide +kernel

theorem normal_injective : Function.Injective normal := by decide +kernel

theorem positive_occurrence_unique : ∀ (c : Fin 5) (j : Fin 2) (e : Fin 3)
    (i k : Fin 6), 0 < weight c i → 0 < weight c k →
    (i = singletonIndex j ∨ i = positiveIndex e ∧ normal (positiveIndex e) j = 1) →
    (k = singletonIndex j ∨ k = positiveIndex e ∧ normal (positiveIndex e) j = 1) → i = k := by
  decide +kernel

theorem negative_occurrence_unique : ∀ (c : Fin 5) (j : Fin 2) (e : Fin 3)
    (i k : Fin 6), 0 < weight c i → 0 < weight c k →
    (i = negativeSingletonIndex j ∨ i = positiveIndex e ∧ normal (positiveIndex e) j = 0) →
    (k = negativeSingletonIndex j ∨ k = positiveIndex e ∧ normal (positiveIndex e) j = 0) →
      i = k := by
  decide +kernel

/-- Once all occurrences of a single product are collected, its circuit coefficient is unit.
The hypotheses describe the local singleton row and the one endpoint row where
that product can occur; they allow either occurrence to be absent. -/
theorem signed_occurrence_sum_unit (c : Fin 5) (j : Fin 2) (ep en : Fin 3)
    (f : Fin 6 → ℤ) (hf : ∀ i, -1 ≤ f i ∧ f i ≤ 1)
    (hp : ∀ i, 0 < f i →
      i = singletonIndex j ∨ i = positiveIndex ep ∧ normal (positiveIndex ep) j = 1)
    (hn : ∀ i, f i < 0 →
      i = negativeSingletonIndex j ∨ i = positiveIndex en ∧ normal (positiveIndex en) j = 0) :
    -1 ≤ ∑ i, weight c i * f i ∧ ∑ i, weight c i * f i ≤ 1 := by
  have h5 : f 5 = 0 := by
    by_contra h
    rcases lt_or_gt_of_ne h with h | h
    · rcases hn 5 h with he | ⟨he, _⟩
      · have he' := congrArg Fin.val he
        dsimp [negativeSingletonIndex] at he'; omega
      · have he' := congrArg Fin.val he
        dsimp [positiveIndex] at he'; omega
    · rcases hp 5 h with he | ⟨he, _⟩
      · have he' := congrArg Fin.val he
        dsimp [singletonIndex] at he'; omega
      · have he' := congrArg Fin.val he
        dsimp [positiveIndex] at he'; omega
  have hterm : ∀ i, -1 ≤ weight c i * f i ∧ weight c i * f i ≤ 1 := by
    intro i
    by_cases hi : i = 5
    · subst i; simp [h5]
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
    exact positive_occurrence_unique c j ep i k hwi hwk (hp i hfi) (hp k hfk)
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
    exact negative_occurrence_unique c j en i k hwi hwk (hn i hfi) (hn k hfk)
  exact Chain.Threshold.sum_unit_of_unique_signs (fun i => weight c i * f i) hterm hpos hneg

end NetworkSimplex.TwoStateCircuits
