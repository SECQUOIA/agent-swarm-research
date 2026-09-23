import Mathlib

/-! Executable merge sorting with a counter incremented at every key comparison. -/
namespace ReciprocalAnchor.ManyLeaf

variable {α : Type*}

def countedMerge (key : α → ℚ) : List α → List α → List α × ℕ
  | [], ys => (ys, 0)
  | xs, [] => (xs, 0)
  | x :: xs, y :: ys =>
      if key x ≤ key y then
        let r := countedMerge key xs (y :: ys)
        (x :: r.1, r.2 + 1)
      else
        let r := countedMerge key (x :: xs) ys
        (y :: r.1, r.2 + 1)
termination_by xs ys => xs.length + ys.length

theorem countedMerge_spec (key : α → ℚ) (xs ys : List α) :
    (countedMerge key xs ys).1 = xs.merge ys (fun a b => decide (key a ≤ key b)) ∧
    (countedMerge key xs ys).2 ≤ xs.length + ys.length := by
  induction xs generalizing ys with
  | nil => simp [countedMerge]
  | cons x xs ih =>
    induction ys with
    | nil => simp [countedMerge]
    | cons y ys jh =>
      by_cases h : key x ≤ key y
      · simp only [countedMerge, h, ↓reduceIte, List.merge, decide_true,
          List.length_cons]
        obtain ⟨he, hc⟩ := ih (y :: ys)
        constructor
        · rw [he]
        · simp only [List.length_cons] at hc
          omega
      · simp only [countedMerge, h, ↓reduceIte, List.merge, decide_false, Bool.false_eq_true,
          List.length_cons]
        obtain ⟨he, hc⟩ := jh
        constructor
        · rw [he]
        · simp only [List.length_cons] at hc
          omega

/-- At depth zero the input is returned; sufficient depth is proved below. -/
def countedSortDepth (key : α → ℚ) : ℕ → List α → List α × ℕ
  | 0, xs => (xs, 0)
  | d + 1, xs =>
      let left := countedSortDepth key d (xs.take (xs.length / 2))
      let right := countedSortDepth key d (xs.drop (xs.length / 2))
      let merged := countedMerge key left.1 right.1
      (merged.1, left.2 + right.2 + merged.2)

theorem countedSortDepth_perm_cost (key : α → ℚ) (d : ℕ) (xs : List α) :
    (countedSortDepth key d xs).1.Perm xs ∧
    (countedSortDepth key d xs).2 ≤ d * xs.length := by
  induction d generalizing xs with
  | zero => simp [countedSortDepth]
  | succ d ih =>
    obtain ⟨hl, hcl⟩ := ih (xs.take (xs.length / 2))
    obtain ⟨hr, hcr⟩ := ih (xs.drop (xs.length / 2))
    obtain ⟨hm, hcm⟩ := countedMerge_spec key
      (countedSortDepth key d (xs.take (xs.length / 2))).1
      (countedSortDepth key d (xs.drop (xs.length / 2))).1
    constructor
    · simp only [countedSortDepth, hm]
      exact (List.merge_perm_append (fun a b => decide (key a ≤ key b))).trans ((hl.append hr).trans
        (List.Perm.of_eq (List.take_append_drop _ _)))
    · simp only [countedSortDepth]
      rw [hl.length_eq, hr.length_eq] at hcm
      have ht : (xs.take (xs.length / 2)).length + (xs.drop (xs.length / 2)).length =
          xs.length := by simp; omega
      nlinarith

theorem countedSortDepth_sorted (key : α → ℚ) (d : ℕ) (xs : List α)
    (hlen : xs.length ≤ 2 ^ d) :
    (countedSortDepth key d xs).1.Pairwise (fun a b => key a ≤ key b) := by
  induction d generalizing xs with
  | zero =>
    simp only [pow_zero] at hlen
    match xs with
    | [] => simp [countedSortDepth]
    | [x] => simp [countedSortDepth]
    | x :: y :: zs => simp only [List.length_cons] at hlen; omega
  | succ d ih =>
    have ht : (xs.take (xs.length / 2)).length ≤ 2 ^ d := by
      simp only [List.length_take]
      rw [pow_succ] at hlen
      omega
    have hd : (xs.drop (xs.length / 2)).length ≤ 2 ^ d := by
      simp only [List.length_drop]
      rw [pow_succ] at hlen
      omega
    simp only [countedSortDepth, (countedMerge_spec key _ _).1]
    have hl := ih (xs.take (xs.length / 2)) ht
    have hr := ih (xs.drop (xs.length / 2)) hd
    have hp := List.pairwise_merge
      (le := fun a b => decide (key a ≤ key b))
      (by
        intro a b c hab hbc
        simpa using le_trans (of_decide_eq_true hab) (of_decide_eq_true hbc))
      (by intro a b; simp only [Bool.or_eq_true, decide_eq_true_eq]; exact le_total _ _)
      _ _ (by simpa using hl) (by simpa using hr)
    simpa using hp

def countedSort (key : α → ℚ) (xs : List α) : List α × ℕ :=
  countedSortDepth key (xs.length.log2 + 1) xs

theorem countedSort_spec (key : α → ℚ) (xs : List α) :
    (countedSort key xs).1.Perm xs ∧
    (countedSort key xs).1.Pairwise (fun a b => key a ≤ key b) ∧
    (countedSort key xs).2 ≤ xs.length * (xs.length.log2 + 1) := by
  obtain ⟨hp, hc⟩ := countedSortDepth_perm_cost key (xs.length.log2 + 1) xs
  refine ⟨hp, countedSortDepth_sorted key _ xs ?_, ?_⟩
  · rw [Nat.log2_eq_log_two]
    exact (Nat.lt_pow_succ_log_self (by decide : 1 < 2) xs.length).le
  · simpa [countedSort, Nat.mul_comm] using hc

end ReciprocalAnchor.ManyLeaf
