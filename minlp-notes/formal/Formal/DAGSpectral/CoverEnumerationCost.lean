import Formal.DAGSpectral.CoverExecution
import Mathlib.Data.Nat.Choose.Bounds

/-! The executed bounded-cardinality subset enumeration has polynomial work
at fixed cardinality, and enumerates exactly the candidate basis sets. -/
namespace DAGSpectral.CoverBitCost

lemma enumeration_power_growth (a k : ℕ) :
    a ^ (k + 1) + a ^ k ≤ (a + 1) ^ (k + 1) := by
  calc
    _ = (a + 1) * a ^ k := by ring
    _ ≤ (a + 1) * (a + 1) ^ k :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_left (Nat.le_succ a) k)
    _ = _ := by ring

/-- A dimension-only coefficient; no input-length factor is hidden in it. -/
def enumerationCoefficient (r : ℕ) : ℕ := (r + 2) ^ 2

theorem sublistsCounted_bound {α : Type*} (r : ℕ) (xs : List α) :
    (sublistsCounted r xs).2 ≤ enumerationCoefficient r * (xs.length + 1) ^ (r + 2) := by
  induction r generalizing xs with
  | zero =>
    simp only [sublistsCounted, enumerationCoefficient, zero_add]
    nlinarith [Nat.one_le_pow 2 (xs.length + 1) (by omega)]
  | succ r ihr =>
    induction xs with
    | nil =>
      simpa only [sublistsCounted, enumerationCoefficient, List.length_nil, zero_add,
        one_pow, mul_one] using Nat.one_le_pow 2 (r + 1 + 2) (by omega)
    | cons a xs ih =>
      have hi := ihr xs
      have hp : 1 ≤ (xs.length + 1) ^ (r + 2) := Nat.one_le_pow _ _ (by omega)
      have hch1 : xs.length.choose (r + 1) ≤ (xs.length + 1) ^ (r + 2) := by
        calc
          _ ≤ xs.length ^ (r + 1) := Nat.choose_le_pow _ _
          _ ≤ (xs.length + 1) ^ (r + 1) := Nat.pow_le_pow_left (by omega) _
          _ ≤ _ := Nat.pow_le_pow_right (by omega) (by omega)
      have hch0 : xs.length.choose r ≤ (xs.length + 1) ^ (r + 2) := by
        calc
          _ ≤ xs.length ^ r := Nat.choose_le_pow _ _
          _ ≤ (xs.length + 1) ^ r := Nat.pow_le_pow_left (by omega) _
          _ ≤ _ := Nat.pow_le_pow_right (by omega) (by omega)
      have hcopy := Nat.mul_le_mul_right (r + 2) hch0
      have hcoeff : enumerationCoefficient r + r + 4 ≤ enumerationCoefficient (r + 1) := by
        unfold enumerationCoefficient
        nlinarith
      have hrest : (sublistsCounted r xs).2 + xs.length.choose (r + 1) +
          xs.length.choose r * (r + 2) + 1 ≤
          enumerationCoefficient (r + 1) * (xs.length + 1) ^ (r + 2) := by
        calc
          _ ≤ (enumerationCoefficient r + r + 4) * (xs.length + 1) ^ (r + 2) := by
            nlinarith
          _ ≤ _ := Nat.mul_le_mul_right _ hcoeff
      have hg := Nat.mul_le_mul_left (enumerationCoefficient (r + 1))
        (enumeration_power_growth (xs.length + 1) (r + 2))
      simp only [sublistsCounted, sublistsCounted_length, List.length_cons]
      change _ ≤ enumerationCoefficient (r + 1) * (xs.length + 1 + 1) ^ (r + 1 + 2)
      have he : r + 1 + 2 = r + 2 + 1 := by omega
      rw [he] at ih ⊢
      nlinarith


/-- All fixed-cardinality candidate basis sets, in the actual sublist order. -/
def candidateBasisList (r M : ℕ) : List (Finset (Fin M)) :=
  (sublistsCounted r (List.finRange M)).1.map List.toFinset

@[simp] theorem candidateBasisList_length (r M : ℕ) :
    (candidateBasisList r M).length = M.choose r := by
  simp [candidateBasisList]

/-- Converting the produced candidates to a set gives exactly all `r`-subsets. -/
theorem candidateBasisList_toFinset (r M : ℕ) :
    (candidateBasisList r M).toFinset = (Finset.univ : Finset (Fin M)).powersetCard r := by
  ext b
  simp only [candidateBasisList, List.mem_toFinset, List.mem_map,
    sublistsCounted_value]
  constructor
  · rintro ⟨xs, hxs, rfl⟩
    obtain ⟨hsub, hlen⟩ := List.mem_sublistsLen.mp hxs
    apply Finset.mem_powersetCard.mpr
    refine ⟨Finset.subset_univ _, ?_⟩
    rw [List.toFinset_card_of_nodup (hsub.nodup (List.nodup_finRange M)), hlen]
  · intro hb
    obtain ⟨_, hcard⟩ := Finset.mem_powersetCard.mp hb
    let xs := (List.finRange M).filter (fun i => decide (i ∈ b))
    have hfs : xs.toFinset = b := by
      ext i
      simp [xs]
    have hsub : xs.Sublist (List.finRange M) := List.filter_sublist
    have hlen : xs.length = r := by
      rw [← List.toFinset_card_of_nodup (hsub.nodup (List.nodup_finRange M)), hfs, hcard]
    exact ⟨xs, List.mem_sublistsLen.mpr ⟨hsub, hlen⟩, hfs⟩

@[simp] theorem mem_candidateBasisList {r M : ℕ} {b : Finset (Fin M)} :
    b ∈ candidateBasisList r M ↔ b.card = r := by
  rw [← List.mem_toFinset, candidateBasisList_toFinset, Finset.mem_powersetCard]
  simp

end DAGSpectral.CoverBitCost
