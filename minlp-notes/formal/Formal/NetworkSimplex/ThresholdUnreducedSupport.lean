import Formal.NetworkSimplex.ThresholdUnreducedCover

/-! The checked support certificates imply completeness for arbitrary real dependencies. -/
namespace NetworkSimplex.Threshold.UnreducedCircuits
open scoped BigOperators

private def encodeBits : (n : ℕ) → (Fin n → Bool) → ℕ
  | 0, _ => 0
  | n + 1, f => Nat.bit (f 0) (encodeBits n (fun i => f i.succ))

private theorem encodeBits_lt (n : ℕ) (f : Fin n → Bool) : encodeBits n f < 2 ^ n := by
  induction n with
  | zero => simp [encodeBits]
  | succ n ih =>
    have h := ih (fun i => f i.succ)
    simp only [encodeBits, Nat.bit_val, pow_succ]
    have hb := Bool.toNat_le (f 0)
    omega

private theorem encodeBits_testBit (n : ℕ) (f : Fin n → Bool) (i : Fin n) :
    (encodeBits n f).testBit i.val = f i := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases ?_ (fun j => ?_) i
    · exact Nat.testBit_bit_zero _ _
    · simpa only [encodeBits, Fin.val_succ, Nat.testBit_bit_succ] using
        ih (fun k => f k.succ) j

/-- Every support either contains a displayed circuit or admits a strict separator. -/
theorem support_cover (present : Fin 14 → Bool) :
    (∃ c : Fin 41, ∀ i, weight c i ≠ 0 → present i = true) ∨
    ∃ s : Fin 32, ∀ i, present i = true → 0 < ∑ j, normal i j * separator s j := by
  let mask := encodeBits 14 present
  have hm : mask < 16384 := encodeBits_lt 14 present
  have h := cover_mask ⟨mask, hm⟩
  simp only [coverMaskBool, Bool.or_eq_true, List.any_eq_true] at h
  rcases h with ⟨c, _, hc⟩ | ⟨s, _, hs⟩
  · left
    refine ⟨c, fun i hi => ?_⟩
    have he : mask &&& supportMask c = supportMask c := by simpa using hc
    have ht := congrArg (fun n => n.testBit i.val) he
    rw [Nat.testBit_and, supportMask_bits] at ht
    dsimp only [mask] at ht
    rw [encodeBits_testBit] at ht
    have hd : decide (weight c i ≠ 0) = true := decide_eq_true hi
    simpa only [hd, Bool.and_true] using ht
  · right
    refine ⟨s, fun i hi => ?_⟩
    have he : mask &&& separatorMask s = mask := by simpa using hs
    have ht := congrArg (fun n => n.testBit i.val) he
    rw [Nat.testBit_and] at ht
    dsimp only [mask] at ht
    rw [encodeBits_testBit, hi, Bool.true_and, separatorMask_bits] at ht
    exact of_decide_eq_true ht

/-- All real nonnegative nonzero cancellations contain one of the forty-one supports. -/
theorem dependence_contains_circuit (a : Fin 14 → ℝ)
    (ha : ∀ i, 0 ≤ a i) (hne : ∃ i, a i ≠ 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0) :
    ∃ c : Fin 41, ∀ i, weight c i ≠ 0 → a i ≠ 0 := by
  classical
  rcases support_cover (fun i => decide (a i ≠ 0)) with h | ⟨s, hs⟩
  · obtain ⟨c, hc⟩ := h
    exact ⟨c, fun i hi => of_decide_eq_true (hc i hi)⟩
  · exfalso
    have hpos : 0 < ∑ i, a i * ∑ j, (normal i j : ℝ) * (separator s j : ℝ) := by
      apply Finset.sum_pos'
      · intro i _
        by_cases hi : a i = 0
        · simp only [hi, zero_mul, le_refl]
        · have hp := hs i (decide_eq_true hi)
          have hp' : (0 : ℝ) < ∑ j, (normal i j : ℝ) * (separator s j : ℝ) := by
            exact_mod_cast hp
          exact mul_nonneg (ha i) hp'.le
      · obtain ⟨i, hi⟩ := hne
        refine ⟨i, Finset.mem_univ _, ?_⟩
        have hp := hs i (decide_eq_true hi)
        have hp' : (0 : ℝ) < ∑ j, (normal i j : ℝ) * (separator s j : ℝ) := by
          exact_mod_cast hp
        exact mul_pos (lt_of_le_of_ne (ha i) (Ne.symm hi)) hp'
    have he : (∑ i, a i * ∑ j, (normal i j : ℝ) * (separator s j : ℝ)) = 0 := by
      simp_rw [Finset.mul_sum, ← mul_assoc]
      rw [Finset.sum_comm]
      simp_rw [← Finset.sum_mul, hc, zero_mul]
      simp
    linarith

end NetworkSimplex.Threshold.UnreducedCircuits
