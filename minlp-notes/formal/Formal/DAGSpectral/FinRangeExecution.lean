import Mathlib.Data.List.FinRange
import Mathlib.Data.List.OfFn
import Mathlib.Data.Nat.Size
import Mathlib.Tactic

/-! Executed construction of finite identifier lists with copy-size accounting. -/
namespace DAGSpectral.CoverBitCost

/-- Build the final k identifiers in increasing order. Each identifier is copied once. -/
def finSuffixCounted (M : ℕ) : (k : ℕ) → k ≤ M → List (Fin M) × ℕ
  | 0, _ => ([], 1)
  | k+1, hk =>
    let tail := finSuffixCounted M k (by omega)
    (⟨M-(k+1), by omega⟩ :: tail.1, tail.2+(M-(k+1)).size+1)

theorem finSuffixCounted_value (M k : ℕ) (hk : k ≤ M) :
    (finSuffixCounted M k hk).1 =
      List.ofFn (fun i : Fin k => (⟨M-k+i.val, by have := i.isLt; omega⟩ : Fin M)) := by
  induction k with
  | zero => simp [finSuffixCounted]
  | succ k ih =>
    rw [finSuffixCounted, ih (by omega), List.ofFn_succ]
    apply congrArg₂ List.cons
    · apply Fin.ext; simp
    · apply congrArg List.ofFn
      funext i
      apply Fin.ext
      simp only [Fin.val_succ]
      omega

theorem finSuffixCounted_work (M k : ℕ) (hk : k ≤ M) :
    (finSuffixCounted M k hk).2 ≤ 1+k*(M+1) := by
  induction k with
  | zero => simp [finSuffixCounted]
  | succ k ih =>
    have ht := ih (show k ≤ M by omega)
    have hs : (M-(k+1)).size ≤ M :=
      (Nat.size_le.mpr (Nat.lt_two_pow_self)).trans (Nat.sub_le _ _)
    simp only [finSuffixCounted]
    nlinarith

def finRangeCounted (M : ℕ) : List (Fin M) × ℕ := finSuffixCounted M M le_rfl

@[simp] theorem finRangeCounted_value (M : ℕ) : (finRangeCounted M).1 = List.finRange M := by
  rw [finRangeCounted, finSuffixCounted_value]
  rw [← List.ofFn_id]
  apply congrArg List.ofFn
  funext i
  apply Fin.ext
  simp

theorem finRangeCounted_work (M : ℕ) : (finRangeCounted M).2 ≤ (M+1)^2 := by
  exact (finSuffixCounted_work M M le_rfl).trans (by nlinarith)

end DAGSpectral.CoverBitCost
