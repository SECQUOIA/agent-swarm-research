import Formal.NetworkSimplex.ThresholdKeys
import Formal.NetworkSimplex.ThresholdPreprocessCriterion
import Formal.NetworkSimplex.ThresholdCoefficientBound

/-! All-dimensional signed-subset systems and their actual finite circuit preprocessing. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- A full signed-subset normal, before removing the empty subset. -/
def signedSubsetVector {d : ℕ} (negative : Bool) (s : Finset (Fin d)) : Fin d → ℤ :=
  fun j ↦ if j ∈ s then if negative then -1 else 1 else 0

/-- Canonical vectors for the full unreduced signed-subset universe. -/
def signedSubsetUniverse (d : ℕ) : Finset (Fin d → ℤ) :=
  (Finset.univ.image (fun t : Bool × Finset (Fin d) ↦ signedSubsetVector t.1 t.2)).erase 0

abbrev SignedSubsetNormal (d : ℕ) := ↥(signedSubsetUniverse d)

@[simp] theorem mem_signedSubsetUniverse {d : ℕ} {v : Fin d → ℤ} :
    v ∈ signedSubsetUniverse d ↔ v ≠ 0 ∧
      ∃ negative : Bool, ∃ s : Finset (Fin d), signedSubsetVector negative s = v := by
  simp [signedSubsetUniverse]

theorem signedSubsetUniverse_card_le (d : ℕ) :
    (signedSubsetUniverse d).card ≤ 2 ^ (d + 1) := by
  apply Finset.card_erase_le.trans
  have h := Finset.card_image_le
    (s := (Finset.univ : Finset (Bool × Finset (Fin d))))
    (f := fun t ↦ signedSubsetVector t.1 t.2)
  simpa [pow_succ, Nat.mul_comm] using h

@[simp] theorem signedSubsetUniverse_zero : signedSubsetUniverse 0 = ∅ := by decide

theorem signedSubsetVector_signed {d : ℕ} (negative : Bool) (s : Finset (Fin d)) :
    (∀ j, signedSubsetVector negative s j = 0 ∨ signedSubsetVector negative s j = 1) ∨
      (∀ j, signedSubsetVector negative s j = 0 ∨ signedSubsetVector negative s j = -1) := by
  cases negative with
  | false => left; intro j; by_cases hj : j ∈ s <;> simp [signedSubsetVector, hj]
  | true => right; intro j; by_cases hj : j ∈ s <;> simp [signedSubsetVector, hj]

theorem signedSubsetUniverse_signed (d : ℕ) :
    RowSignedZeroOne (fun v : SignedSubsetNormal d ↦ v.val) := by
  intro v
  obtain ⟨_, negative, s, h⟩ := mem_signedSubsetUniverse.mp v.property
  dsimp only
  rw [← h]
  exact signedSubsetVector_signed negative s

/-- The circuit criterion applies to every coordinate dimension, not merely to
the explicitly classified two- and three-coordinate examples. -/
theorem signedSubset_feasible_iff {d : ℕ} (b : SignedSubsetNormal d → ℝ) :
    (∃ x : Fin d → ℝ, ∀ v : SignedSubsetNormal d, ∑ j, (v.val j : ℝ) * x j ≤ b v) ↔
      ∀ (s : ℕ), s ≤ d + 1 → ∀ e : Fin s ↪ SignedSubsetNormal d, ∀ p : Fin s → ℕ,
        (∀ i, 0 < p i ∧ p i ≤ delta01 d) → Finset.univ.gcd p = 1 →
        (∀ j, ∑ i, (p i : ℤ) * (e i).val j = 0) →
        0 ≤ ∑ i, (p i : ℝ) * b (e i) :=
  feasible_iff_bounded_integer_tests _ (signedSubsetUniverse_signed d) b

/-- Every actual positive circuit in the canonical universe has the claimed
support size and primitive cofactor-weight bound. -/
theorem signedSubset_circuit_weights {d : ℕ}
    (C : PositiveCircuit (fun (v : SignedSubsetNormal d) j ↦ (v.val j : ℝ))) :
    C.size ≤ d + 1 ∧ ∃ p : Fin C.size → ℕ,
      (∀ i, 0 < p i ∧ p i ≤ delta01 d) ∧ Finset.univ.gcd p = 1 ∧
      (∀ j, ∑ i, (p i : ℤ) * (C.index i).val j = 0) ∧
      ∀ i, (p i : ℝ) = (∑ j, (p j : ℝ)) * C.mass i :=
  ⟨C.size_le, C.exists_primitive_integer_weights _ (signedSubsetUniverse_signed d)⟩

/-- An executable packed enumeration of both signs of every subset. Two slots
represent zero; they will be absent in the canonical-system table. -/
def signedKeyNormal {d : ℕ} (k : Fin (2 ^ (d + 1))) (j : Fin d) : ℤ :=
  if k.val < 2 ^ d then if k.val.testBit j.val then 1 else 0
  else if (k.val - 2 ^ d).testBit j.val then -1 else 0

def signedPack {d : ℕ} (negative : Bool) (s : Finset (Fin d)) : Fin (2 ^ (d + 1)) :=
  ⟨(if negative then 2 ^ d else 0) + subsetMask s, by
    have hs := subsetMask_lt s
    cases negative <;> simp only [Bool.false_eq_true, ↓reduceIte, zero_add] <;>
      rw [pow_succ] <;> omega⟩

theorem signedKeyNormal_pack {d : ℕ} (negative : Bool) (s : Finset (Fin d)) :
    signedKeyNormal (signedPack negative s) = signedSubsetVector negative s := by
  ext j
  have hs := subsetMask_lt s
  cases negative <;> by_cases hj : j ∈ s
  all_goals
    have hb := (subsetMask_testBit s j)
    simp [signedKeyNormal, signedPack, signedSubsetVector, hs, hj, hb, Nat.not_lt.mpr]

theorem signedKeyNormal_signed (d : ℕ) : RowSignedZeroOne (signedKeyNormal (d := d)) := by
  intro k
  by_cases hk : k.val < 2 ^ d
  · left; intro j; by_cases h : k.val.testBit j.val <;> simp [signedKeyNormal, hk, h]
  · right; intro j; by_cases h : (k.val - 2 ^ d).testBit j.val <;>
      simp [signedKeyNormal, hk, h]

theorem signedKeyNormal_natAbs_le {d : ℕ} (k : Fin (2 ^ (d + 1))) (j : Fin d) :
    (signedKeyNormal k j).natAbs ≤ 1 := by
  rcases signedKeyNormal_signed d k with h | h <;>
    rcases h j with he | he <;> simp [he]

theorem signedKeyNormal_mem_or_zero {d : ℕ} (k : Fin (2 ^ (d + 1))) :
    signedKeyNormal k ∈ signedSubsetUniverse d ∨ signedKeyNormal k = 0 := by
  by_cases hz : signedKeyNormal k = 0
  · exact Or.inr hz
  left
  refine mem_signedSubsetUniverse.mpr ⟨hz, ?_⟩
  by_cases hk : k.val < 2 ^ d
  · refine ⟨false, Finset.univ.filter (fun j ↦ k.val.testBit j.val), ?_⟩
    ext j
    simp [signedSubsetVector, signedKeyNormal, hk]
  · refine ⟨true, Finset.univ.filter (fun j ↦ (k.val - 2 ^ d).testBit j.val), ?_⟩
    ext j
    simp [signedSubsetVector, signedKeyNormal, hk]

theorem signedKeyNormal_covers {d : ℕ} (v : SignedSubsetNormal d) :
    ∃ k : Fin (2 ^ (d + 1)), signedKeyNormal k = v.val := by
  obtain ⟨_, negative, s, hs⟩ := mem_signedSubsetUniverse.mp v.property
  exact ⟨signedPack negative s, (signedKeyNormal_pack negative s).trans hs⟩

/-- Only canonical nonzero vectors impose a bound in the packed table. -/
noncomputable def signedTable {d : ℕ} (b : SignedSubsetNormal d → ℝ)
    (k : Fin (2 ^ (d + 1))) : Option ℝ :=
  if hk : signedKeyNormal k ∈ signedSubsetUniverse d then some (b ⟨signedKeyNormal k, hk⟩)
  else none

theorem signedTable_feasible_iff {d : ℕ} (b : SignedSubsetNormal d → ℝ) :
    (∃ x : Fin d → ℝ, ∀ v : SignedSubsetNormal d, ∑ j, (v.val j : ℝ) * x j ≤ b v) ↔
    (∃ x : Fin d → ℝ, ∀ k, signedTable b k ≠ none →
      ∑ j, (signedKeyNormal k j : ℝ) * x j ≤ (signedTable b k).getD 0) := by
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨x, ?_⟩
    intro k hk
    unfold signedTable at hk ⊢
    split_ifs with hmem
    · simpa using hx ⟨signedKeyNormal k, hmem⟩
    · simp [hmem] at hk
  · rintro ⟨x, hx⟩
    refine ⟨x, ?_⟩
    intro v
    obtain ⟨k, hk⟩ := signedKeyNormal_covers v
    have hm : signedKeyNormal k ∈ signedSubsetUniverse d := hk ▸ v.property
    have hh := hx k (by simp [signedTable, hm])
    simpa [signedTable, hm, hk] using hh

/-- The executable cofactor preprocessing is a complete criterion for the full
canonical signed-subset system in every dimension. -/
theorem signedSubset_feasible_iff_preprocessed {d : ℕ} (b : SignedSubsetNormal d → ℝ) :
    (∃ x : Fin d → ℝ, ∀ v : SignedSubsetNormal d, ∑ j, (v.val j : ℝ) * x j ≤ b v) ↔
      CompiledPartialTests signedKeyNormal (signedTable b) :=
  (signedTable_feasible_iff b).trans
    (feasible_iff_compiledPartialTests _ (signedKeyNormal_signed d) _)

/-- Actual generated cofactor candidates, rather than arbitrary bounded weight
vectors, obey the stated fixed-parameter bound. -/
theorem signed_cofactorCandidates_length (d : ℕ) :
    (cofactorCandidates d (2 ^ (d + 1))).length ≤ 2 ^ (4 * (d + 1) ^ 2) := by
  apply cofactorCandidates_length_exp
  · have : 0 < 2 ^ (d + 1) := by positivity
    omega
  · exact Nat.pow_le_pow_right (by decide) (by omega)

theorem signed_preprocessCircuits_length (d : ℕ) :
    (preprocessCircuits (signedKeyNormal (d := d))).length ≤ 2 ^ (4 * (d + 1) ^ 2) := by
  apply (List.length_filter_le _ _).trans
  rw [List.length_map]
  exact signed_cofactorCandidates_length d

/-- Expanding any stored certificate through unit-coefficient original rows
preserves the unreduced `(d + 1) * delta01 d` ambient coefficient bound. -/
theorem signed_compiled_coefficient_bound {d : ℕ}
    (c : CompiledCircuit d (2 ^ (d + 1)))
    (hc : c ∈ preprocessCircuits (signedKeyNormal (d := d)))
    (coeff : Fin (c.candidate.size.val + 1) → ℤ)
    (hcoeff : ∀ i, (coeff i).natAbs ≤ 1) :
    (∑ i, (c.weight i : ℤ) * coeff i).natAbs ≤ (d + 1) * delta01 d := by
  apply weighted_coefficient_natAbs_le c.weight coeff
  · simp only [Fintype.card_fin]
    have := c.candidate.size.isLt
    omega
  · intro i
    exact ((preprocessCircuits_sound _ (signedKeyNormal_signed d) hc).1 i).2
  · exact hcoeff

end NetworkSimplex.Chain.Threshold
