import Formal.MultilinearGap.Results

/-! Degree and dimension bounds for the dyadic witnesses. -/
namespace MultilinearGap

open CubicGap
noncomputable section

theorem coord_card (L : ℕ) : Fintype.card (Coord L) = L + 2 ^ L := by
  simp [Coord]

theorem support_card_le (L : ℕ) (t : Finset (Coord L)) (ht : t ∈ supports L) :
    t.card ≤ 2 ^ (L - 1) + 1 := by
  obtain ⟨⟨j, b⟩, _, rfl⟩ := Finset.mem_image.mp ht
  rw [support_card]
  exact Nat.add_le_add_right (Nat.pow_le_pow_right (by decide) (by omega)) 1

/-- One choice of levels fits both a degree allowance and a dimension allowance. -/
def witnessLevels (n : ℕ) : ℕ := Nat.log 2 n - 1

theorem witnessLevels_ge_two (n : ℕ) (hn : 8 ≤ n) : 2 ≤ witnessLevels n := by
  have h : 3 ≤ Nat.log 2 n := Nat.le_log_of_pow_le (by decide) hn
  unfold witnessLevels
  omega

theorem witness_dimension_le (n : ℕ) (hn : 2 ≤ n) :
    Fintype.card (Coord (witnessLevels n)) ≤ n := by
  have hn0 : n ≠ 0 := by omega
  have hk : 1 ≤ Nat.log 2 n := Nat.le_log_of_pow_le (by decide) hn
  have hpow := Nat.pow_log_le_self 2 hn0
  have hsmall := Nat.lt_two_pow_self (n := witnessLevels n)
  rw [coord_card]
  have hstep : Nat.log 2 n = witnessLevels n + 1 := by unfold witnessLevels; omega
  rw [hstep, pow_succ] at hpow
  omega

theorem witness_degree_le (n : ℕ) (hn : 2 ≤ n)
    (t : Finset (Coord (witnessLevels n))) (_ht : t ∈ supports (witnessLevels n)) :
    t.card ≤ n := by
  exact (Finset.card_le_univ t).trans (witness_dimension_le n hn)

end
end MultilinearGap
