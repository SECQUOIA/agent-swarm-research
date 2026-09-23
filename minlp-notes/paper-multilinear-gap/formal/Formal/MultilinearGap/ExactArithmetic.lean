import Mathlib

/-! Cutoff and mixing arithmetic for the exact dyadic hull gap. -/
namespace MultilinearGap
noncomputable section

/-- Expected number of failed leaves for a cutoff law. -/
def cutoffBudget (L q : ℕ) : ℝ := ((L : ℝ) - q + 2) / 2 ^ q

/-- Expected number of destroyed active terms for a cutoff law. -/
def cutoffDeficit (L q : ℕ) : ℝ := (q + 1 : ℝ) * cutoffBudget L q - 2 / 2 ^ q

theorem cutoffBudget_one (L : ℕ) : cutoffBudget L 1 = ((L : ℝ) + 1) / 2 := by
  simp [cutoffBudget]; ring

theorem cutoffBudget_last_le_one (L : ℕ) (hL : 1 ≤ L) : cutoffBudget L L ≤ 1 := by
  have hp : (2 : ℝ) ≤ 2 ^ L := by
    simpa using pow_le_pow_right₀ (by norm_num : (1 : ℝ) ≤ 2) hL
  simp only [cutoffBudget, sub_self, zero_add]
  exact (div_le_one (by positivity)).mpr hp

theorem cutoffBudget_sub_succ (L s : ℕ) :
    cutoffBudget L s - cutoffBudget L (s + 1) =
      ((L : ℝ) - s + 3) / 2 ^ (s + 1) := by
  simp only [cutoffBudget, Nat.cast_add, Nat.cast_one, pow_succ]
  field_simp
  ring

theorem cutoffBudget_strict (L s : ℕ) (hs : s ≤ L) :
    cutoffBudget L (s + 1) < cutoffBudget L s := by
  have hs' : (s : ℝ) ≤ L := by exact_mod_cast hs
  have hp : 0 < cutoffBudget L s - cutoffBudget L (s + 1) := by
    rw [cutoffBudget_sub_succ]
    exact div_pos (by linarith) (by positivity)
  linarith

/-- There is an adjacent pair of cutoff budgets bracketing one. -/
theorem exists_exact_cutoff (L : ℕ) (hL : 2 ≤ L) :
    ∃ s : ℕ, 1 ≤ s ∧ s < L ∧ cutoffBudget L (s + 1) ≤ 1 ∧
      1 ≤ cutoffBudget L s := by
  have hex : ∃ q : ℕ, cutoffBudget L q ≤ 1 :=
    ⟨L, cutoffBudget_last_le_one L (by omega)⟩
  let q := Nat.find hex
  have hq : cutoffBudget L q ≤ 1 := Nat.find_spec hex
  have hqL : q ≤ L := Nat.find_min' hex (cutoffBudget_last_le_one L (by omega))
  have hq2 : 2 ≤ q := by
    by_contra h
    have hqsmall : q = 0 ∨ q = 1 := by omega
    have hL' : (2 : ℝ) ≤ L := by exact_mod_cast hL
    rcases hqsmall with hzero | hone
    · rw [hzero] at hq
      simp only [cutoffBudget, Nat.cast_zero, sub_zero, pow_zero, div_one] at hq
      linarith
    · rw [hone, cutoffBudget_one] at hq
      linarith
  refine ⟨q - 1, by omega, by omega, ?_, ?_⟩
  · simpa [Nat.sub_add_cancel (by omega : 1 ≤ q)] using hq
  · have hprev : ¬cutoffBudget L (q - 1) ≤ 1 := Nat.find_min hex (by omega : q - 1 < q)
    exact le_of_lt (lt_of_not_ge hprev)

/-- Weight of cutoff `s` when mixing the budgets of `s` and `s + 1`. -/
def cutoffMix (L s : ℕ) : ℝ :=
  (1 - cutoffBudget L (s + 1)) / (cutoffBudget L s - cutoffBudget L (s + 1))

theorem cutoffMix_mem_unit (L s : ℕ) (hs : s ≤ L)
    (hlo : cutoffBudget L (s + 1) ≤ 1) (hhi : 1 ≤ cutoffBudget L s) :
    0 ≤ cutoffMix L s ∧ cutoffMix L s ≤ 1 := by
  have hp := sub_pos.mpr (cutoffBudget_strict L s hs)
  constructor
  · exact div_nonneg (sub_nonneg.mpr hlo) hp.le
  · exact (div_le_one hp).mpr (by linarith)

theorem cutoffMix_budget (L s : ℕ) (hs : s ≤ L) :
    cutoffMix L s * cutoffBudget L s +
      (1 - cutoffMix L s) * cutoffBudget L (s + 1) = 1 := by
  have hn : cutoffBudget L s - cutoffBudget L (s + 1) ≠ 0 :=
    ne_of_gt (sub_pos.mpr (cutoffBudget_strict L s hs))
  simp only [cutoffMix]
  field_simp
  ring

theorem cutoffDeficit_affine_left (L s : ℕ) :
    cutoffDeficit L s = (s : ℝ) * cutoffBudget L s + ((L : ℝ) - s) / 2 ^ s := by
  simp only [cutoffDeficit, cutoffBudget]
  ring

theorem cutoffDeficit_affine_right (L s : ℕ) :
    cutoffDeficit L (s + 1) = (s : ℝ) * cutoffBudget L (s + 1) +
      ((L : ℝ) - s) / 2 ^ s := by
  simp only [cutoffDeficit, cutoffBudget, Nat.cast_add, Nat.cast_one, pow_succ]
  field_simp
  ring

theorem cutoffMix_deficit (L s : ℕ) (hs : s ≤ L) :
    cutoffMix L s * cutoffDeficit L s +
      (1 - cutoffMix L s) * cutoffDeficit L (s + 1) =
      (s : ℝ) + ((L : ℝ) - s) / 2 ^ s := by
  rw [cutoffDeficit_affine_left, cutoffDeficit_affine_right]
  have hb := cutoffMix_budget L s hs
  nlinarith

end
end MultilinearGap
