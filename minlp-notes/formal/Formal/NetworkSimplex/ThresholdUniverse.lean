import Formal.NetworkSimplex.ThresholdRows

/-! Canonical nonzero profile normals and fixed-parameter library size bounds. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- Equal normal vectors share one entry, and the zero normal is omitted. -/
def normalUniverse (m : ℕ) : Finset (Fin m → ℤ) :=
  (Finset.univ.image (normalVector (m := m))).erase 0

/-- Canonical finite indices for preprocessing circuit and basis libraries. -/
abbrev CanonicalNormal (m : ℕ) := ↥(normalUniverse m)

@[simp] theorem mem_normalUniverse {m : ℕ} {v : Fin m → ℤ} :
    v ∈ normalUniverse m ↔ v ≠ 0 ∧ ∃ n : ProfileNormal m, normalVector n = v := by
  simp [normalUniverse]

private def normalIndexEquiv (m : ℕ) :
    ProfileNormal m ≃ (Finset (Fin m) ⊕ Fin m) ⊕ Unit where
  toFun
    | .subset s => .inl (.inl s)
    | .negativeSingleton j => .inl (.inr j)
    | .negativeTotal => .inr ()
  invFun
    | .inl (.inl s) => .subset s
    | .inl (.inr j) => .negativeSingleton j
    | .inr _ => .negativeTotal
  left_inv n := by cases n <;> rfl
  right_inv n := by rcases n with (s | j) | u <;> simp

theorem profileNormal_card (m : ℕ) : Fintype.card (ProfileNormal m) = 2 ^ m + m + 1 := by
  rw [Fintype.card_congr (normalIndexEquiv m)]
  simp

theorem normalUniverse_card_le (m : ℕ) : (normalUniverse m).card ≤ 2 ^ m + m := by
  have hz : (0 : Fin m → ℤ) ∈ Finset.univ.image (normalVector (m := m)) := by
    apply Finset.mem_image.mpr
    refine ⟨.subset ∅, Finset.mem_univ _, ?_⟩
    ext j
    simp [normalVector]
  have hc := Finset.card_image_le (s := (Finset.univ : Finset (ProfileNormal m)))
    (f := normalVector)
  rw [Finset.card_univ, profileNormal_card] at hc
  have he := Finset.card_erase_add_one hz
  change (normalUniverse m).card + 1 = _ at he
  omega

/-- Each row has a uniform sign and entries of absolute value at most one. -/
theorem normalVector_signed {m : ℕ} (n : ProfileNormal m) :
    (∀ j, normalVector n j = 0 ∨ normalVector n j = 1) ∨
      (∀ j, normalVector n j = 0 ∨ normalVector n j = -1) := by
  cases n with
  | subset s => left; intro j; by_cases h : j ∈ s <;> simp [normalVector, h]
  | negativeSingleton k => right; intro j; by_cases h : j = k <;> simp [normalVector, h]
  | negativeTotal => right; intro j; simp [normalVector]

theorem normalUniverse_signed {m : ℕ} {v : Fin m → ℤ} (hv : v ∈ normalUniverse m) :
    (∀ j, v j = 0 ∨ v j = 1) ∨ (∀ j, v j = 0 ∨ v j = -1) := by
  obtain ⟨_, n, rfl⟩ := mem_normalUniverse.mp hv
  exact normalVector_signed n

@[simp] theorem normalUniverse_zero : normalUniverse 0 = ∅ := by decide

/-- The negative-total and negative-singleton labels are the same vector in dimension one. -/
@[simp] theorem normalUniverse_one_card : (normalUniverse 1).card = 2 := by decide

/-- Candidate circuit supports use at most `m + 1` distinct canonical normals. -/
def circuitSupports (m : ℕ) : Finset (Finset (Fin m → ℤ)) :=
  (Finset.range (m + 2)).biUnion fun k ↦ (normalUniverse m).powersetCard k

@[simp] theorem mem_circuitSupports {m : ℕ} {s : Finset (Fin m → ℤ)} :
    s ∈ circuitSupports m ↔ s ⊆ normalUniverse m ∧ s.card ≤ m + 1 := by
  simp only [circuitSupports, Finset.mem_biUnion, Finset.mem_range, Finset.mem_powersetCard]
  constructor
  · rintro ⟨k, hk, hs, hcard⟩
    exact ⟨hs, by omega⟩
  · rintro ⟨hs, hc⟩
    exact ⟨s.card, by omega, hs, rfl⟩

theorem circuitSupports_card_le_choose (m : ℕ) :
    (circuitSupports m).card ≤
      ∑ k ∈ Finset.range (m + 2), (normalUniverse m).card.choose k := by
  calc
    _ ≤ ∑ k ∈ Finset.range (m + 2), ((normalUniverse m).powersetCard k).card :=
      Finset.card_biUnion_le
    _ = _ := by simp only [Finset.card_powersetCard]

/-- An explicit elementary bound for the size of each normal table. -/
theorem normalUniverse_card_add_one_le_pow (m : ℕ) :
    (normalUniverse m).card + 1 ≤ 2 ^ (m + 2) := by
  have h := normalUniverse_card_le m
  have hp : m < 2 ^ m := Nat.lt_two_pow_self
  rw [pow_succ, pow_succ]
  omega

private theorem partial_choose_sum_le (N k : ℕ) :
    (∑ j ∈ Finset.range (k + 1), N.choose j) ≤ (k + 1) * (N + 1) ^ k := by
  calc
    _ ≤ ∑ _j ∈ Finset.range (k + 1), (N + 1) ^ k := by
      apply Finset.sum_le_sum
      intro j hj
      exact (Nat.choose_le_pow N j).trans
        ((Nat.pow_le_pow_left (by omega : N ≤ N + 1) j).trans
          (Nat.pow_le_pow_right (by omega : 0 < N + 1) (by simpa using Finset.mem_range.mp hj)))
    _ = _ := by simp

/-- Support enumeration is singly exponential in the square of the parameter. -/
theorem circuitSupports_card_le_exp (m : ℕ) :
    (circuitSupports m).card ≤ 2 ^ (3 * (m + 1) ^ 2) := by
  have h1 := circuitSupports_card_le_choose m
  have h2 := partial_choose_sum_le (normalUniverse m).card (m + 1)
  have hm : m + 2 ≤ 2 ^ (m + 1) := Nat.lt_two_pow_self
  calc
    _ ≤ (m + 2) * ((normalUniverse m).card + 1) ^ (m + 1) := h1.trans h2
    _ ≤ 2 ^ (m + 1) * (2 ^ (m + 2)) ^ (m + 1) :=
      Nat.mul_le_mul hm (Nat.pow_le_pow_left (normalUniverse_card_add_one_le_pow m) _)
    _ = 2 ^ ((m + 1) + (m + 2) * (m + 1)) := by rw [← pow_mul, ← pow_add]
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

/-- Ordered basis candidates obey the same uniform parameter bound. -/
theorem basisCandidates_card_le_exp (m : ℕ) :
    (normalUniverse m).card ^ m ≤ 2 ^ (3 * (m + 1) ^ 2) := by
  calc
    _ ≤ (2 ^ (m + 2)) ^ m := Nat.pow_le_pow_left
      ((Nat.le_add_right _ 1).trans (normalUniverse_card_add_one_le_pow m)) _
    _ = 2 ^ ((m + 2) * m) := (pow_mul _ _ _).symm
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

theorem canonicalBasis_card_le_exp (m : ℕ) :
    Fintype.card (Fin m → CanonicalNormal m) ≤ 2 ^ (3 * (m + 1) ^ 2) := by
  simpa only [Fintype.card_fun, Fintype.card_fin, Fintype.card_coe] using
    basisCandidates_card_le_exp m

end NetworkSimplex.Chain.Threshold
