import Mathlib

/-! Actual Euclidean remainder recursion with a proved linear bit-length iteration bound. -/
namespace ReciprocalAnchor.ManyLeaf.BitCost

/-- A remainder division is counted once at every nonterminal Euclidean step. -/
def countedEuclid (a b : ℕ) : ℕ × ℕ :=
  if hb : b = 0 then (a, 0)
  else
    let r := countedEuclid b (a % b)
    (r.1, r.2 + 1)
termination_by b
decreasing_by exact Nat.mod_lt _ (Nat.pos_of_ne_zero hb)

theorem countedEuclid_gcd (a b : ℕ) : (countedEuclid a b).1 = Nat.gcd a b := by
  induction b using Nat.strong_induction_on generalizing a with
  | h b ih =>
    by_cases hb : b = 0
    · subst b; simp [countedEuclid]
    · rw [countedEuclid, dif_neg hb]
      dsimp only
      rw [ih (a % b) (Nat.mod_lt _ (Nat.pos_of_ne_zero hb))]
      exact (Nat.gcd_comm b (a % b)).trans
        ((Nat.gcd_rec b a).symm.trans (Nat.gcd_comm b a))

/-- When a remainder is at least half the current power-of-two bound, the
following remainder is below half that bound. -/
theorem second_remainder_lt {b r B : ℕ} (hb : b < 2 ^ (B + 1))
    (hrb : r < b) (hr : 2 ^ B ≤ r) : b % r < 2 ^ B := by
  rw [Nat.mod_eq_sub_mod hrb.le]
  have hp : 0 < 2 ^ B := pow_pos (by decide) B
  rw [pow_succ] at hb
  have hs : b - r < r := by omega
  rw [Nat.mod_eq_of_lt hs]
  omega

/-- The Euclidean algorithm performs at most two divisions per bit of its
second operand. No bound on the first operand is needed for this count. -/
theorem countedEuclid_cost_pow (B a b : ℕ) (hb : b < 2 ^ B) :
    (countedEuclid a b).2 ≤ 2 * B := by
  induction B generalizing a b with
  | zero =>
    have hz : b = 0 := by simpa using hb
    subst b
    simp [countedEuclid]
  | succ B ih =>
    by_cases hz : b = 0
    · subst b; simp [countedEuclid]
    · rw [countedEuclid, dif_neg hz]
      dsimp only
      by_cases hr : a % b < 2 ^ B
      · have h := ih b (a % b) hr
        omega
      · have hrl : a % b < b := Nat.mod_lt _ (Nat.pos_of_ne_zero hz)
        have hrp : 2 ^ B ≤ a % b := Nat.le_of_not_gt hr
        have hrz : a % b ≠ 0 := by have hp := pow_pos (by decide : 0 < 2) B; omega
        rw [countedEuclid, dif_neg hrz]
        dsimp only
        have hnext := second_remainder_lt hb hrl hrp
        have h := ih (a % b) (b % (a % b)) hnext
        omega

theorem countedEuclid_cost_size (a b : ℕ) :
    (countedEuclid a b).2 ≤ 2 * b.size :=
  countedEuclid_cost_pow b.size a b (Nat.lt_size_self b)

theorem countedEuclid_cost_max (a b : ℕ) :
    (countedEuclid a b).2 ≤ 2 * max a.size b.size :=
  (countedEuclid_cost_size a b).trans (Nat.mul_le_mul_left 2 (le_max_right _ _))

/-- All later division operands stay within the original maximum bit length. -/
theorem euclid_step_size (a b : ℕ) :
    b.size ≤ max a.size b.size ∧ (a % b).size ≤ max a.size b.size := by
  refine ⟨le_max_right _ _, ?_⟩
  by_cases hb : b = 0
  · subst b; simp
  · exact (Nat.size_le_size (Nat.mod_lt a (Nat.pos_of_ne_zero hb)).le).trans
      (le_max_right _ _)

end ReciprocalAnchor.ManyLeaf.BitCost
