import Mathlib

/-! Executable determinant evaluation with an explicit arithmetic-operation counter. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators

/-- Laplace expansion with each child determinant stored once. The counter charges
`j` multiplications for `(-1)^j`, two term multiplications and one sum addition. -/
def determinantTrace : (s : ℕ) → Matrix (Fin s) (Fin s) ℤ → ℤ × ℕ
  | 0, _ => (1, 0)
  | s + 1, A =>
      let children := Vector.ofFn fun j : Fin (s + 1) =>
        determinantTrace s (A.submatrix Fin.succ j.succAbove)
      (∑ j, (-1) ^ j.val * A 0 j * (children.get j).1,
        ∑ j : Fin (s + 1), ((children.get j).2 + j.val + 3))

theorem determinantTrace_value (s : ℕ) (A : Matrix (Fin s) (Fin s) ℤ) :
    (determinantTrace s A).1 = A.det := by
  induction s with
  | zero => simp [determinantTrace]
  | succ s ih =>
    simp only [determinantTrace, Vector.get_ofFn, ih, Matrix.det_succ_row_zero]

def determinantWork : ℕ → ℕ
  | 0 => 0
  | s + 1 => (s + 1) * (determinantWork s + s + 3)

theorem determinantTrace_work (s : ℕ) (A : Matrix (Fin s) (Fin s) ℤ) :
    (determinantTrace s A).2 ≤ determinantWork s := by
  induction s with
  | zero => simp [determinantTrace, determinantWork]
  | succ s ih =>
    simp only [determinantTrace, Vector.get_ofFn, determinantWork]
    calc
      _ ≤ ∑ _j : Fin (s + 1), (determinantWork s + s + 3) := by
        apply Finset.sum_le_sum
        intro j _
        have hj := ih (A.submatrix Fin.succ j.succAbove)
        have hv := j.isLt
        omega
      _ = _ := by simp

theorem determinantWork_factorial (s : ℕ) : determinantWork s ≤ (s + 2).factorial := by
  induction s with
  | zero => simp [determinantWork]
  | succ s ih =>
    have hf : (s + 1) * (s + 2) ≤ (s + 2).factorial := by
      rw [Nat.factorial_succ, Nat.factorial_succ]
      have h := Nat.mul_le_mul_left ((s + 1) * (s + 2)) (Nat.factorial_pos s)
      nlinarith
    rw [determinantWork, show s + 1 + 2 = (s + 2) + 1 by omega, Nat.factorial_succ]
    have h := Nat.mul_le_mul_left (s + 1) ih
    nlinarith

theorem determinantTrace_factorial (s : ℕ) (A : Matrix (Fin s) (Fin s) ℤ) :
    (determinantTrace s A).2 ≤ (s + 2).factorial :=
  (determinantTrace_work s A).trans (determinantWork_factorial s)

/-- The determinant values and every recursive minor remain factorially bounded
when the input entries have absolute value at most one. -/
theorem determinantTrace_abs (s : ℕ) (A : Matrix (Fin s) (Fin s) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) :
    (determinantTrace s A).1.natAbs ≤ s.factorial := by
  induction s with
  | zero => simp [determinantTrace]
  | succ s ih =>
    simp only [determinantTrace, Vector.get_ofFn]
    apply (Int.natAbs_sum_le _ _).trans
    calc
      _ ≤ ∑ _j : Fin (s + 1), s.factorial := by
        apply Finset.sum_le_sum
        intro j _
        simp only [Int.natAbs_mul, Int.natAbs_pow, Int.natAbs_neg, Int.natAbs_one,
          one_pow, one_mul]
        have hc := ih (A.submatrix Fin.succ j.succAbove) (fun i k => hA _ _)
        exact (Nat.mul_le_mul (hA 0 j) hc).trans_eq (one_mul _)
      _ = _ := by simp [Nat.factorial_succ]

/-- Every partial Laplace sum is bounded too, even when cancellation only occurs
in the completed determinant. This covers the accumulator of any summation order. -/
theorem determinantTrace_partial_abs (s : ℕ) (A : Matrix (Fin (s + 1)) (Fin (s + 1)) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) (part : Finset (Fin (s + 1))) :
    (∑ j ∈ part, (-1) ^ j.val * A 0 j *
      (determinantTrace s (A.submatrix Fin.succ j.succAbove)).1).natAbs ≤
      (s + 1).factorial := by
  apply (Int.natAbs_sum_le _ _).trans
  calc
    _ ≤ ∑ _j ∈ part, s.factorial := by
      apply Finset.sum_le_sum
      intro j _
      simp only [Int.natAbs_mul, Int.natAbs_pow, Int.natAbs_neg, Int.natAbs_one,
        one_pow, one_mul]
      exact (Nat.mul_le_mul (hA 0 j)
        (determinantTrace_abs s _ (fun i k => hA _ _))).trans_eq (one_mul _)
    _ ≤ (s + 1) * s.factorial := by
      simp only [Finset.sum_const, smul_eq_mul]
      exact Nat.mul_le_mul_right _
        ((Finset.card_le_univ part).trans_eq (Fintype.card_fin _))
    _ = _ := (Nat.factorial_succ s).symm

/-- Every sign-power stage and both multiplication stages of an actual Laplace
term are bounded; together with `determinantTrace_partial_abs` this covers all
arithmetic intermediates at every recursive minor. -/
theorem determinantTrace_term_intermediates (s : ℕ)
    (A : Matrix (Fin (s + 1)) (Fin (s + 1)) ℤ)
    (hA : ∀ i j, (A i j).natAbs ≤ 1) (j : Fin (s + 1)) (k : ℕ) :
    ((-1 : ℤ) ^ k).natAbs = 1 ∧
    ((-1 : ℤ) ^ j.val * A 0 j).natAbs ≤ 1 ∧
    ((-1 : ℤ) ^ j.val * A 0 j *
      (determinantTrace s (A.submatrix Fin.succ j.succAbove)).1).natAbs ≤ s.factorial := by
  simp only [Int.natAbs_mul, Int.natAbs_pow, Int.natAbs_neg, Int.natAbs_one,
    one_pow, one_mul]
  exact ⟨trivial, hA 0 j,
    (Nat.mul_le_mul (hA 0 j)
      (determinantTrace_abs s _ (fun i k => hA _ _))).trans_eq (one_mul _)⟩

end NetworkSimplex.Threshold
