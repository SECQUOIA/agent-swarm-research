import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Int.NatAbs
import Mathlib.Tactic

/-! Finite determinant bounds for the reduced flat-chain normal universe. -/

namespace NetworkSimplex.Threshold

/-- Interpret a Boolean matrix as an integer zero-one matrix. -/
def boolMatrix {n : ℕ} (A : Matrix (Fin n) (Fin n) Bool) :
    Matrix (Fin n) (Fin n) ℤ := fun i j => if A i j then 1 else 0

/-- Largest absolute zero-one determinant of order at most `m`, including order zero. -/
def delta01 (m : ℕ) : ℕ :=
  (Finset.range (m + 1)).sup fun n =>
    Finset.univ.sup fun A : Matrix (Fin n) (Fin n) Bool => (boolMatrix A).det.natAbs

theorem det_natAbs_le_delta01 {n m : ℕ} (hn : n ≤ m)
    (A : Matrix (Fin n) (Fin n) Bool) : (boolMatrix A).det.natAbs ≤ delta01 m := by
  unfold delta01
  apply le_trans (Finset.le_sup (f := fun A => (boolMatrix A).det.natAbs)
    (Finset.mem_univ A))
  exact Finset.le_sup (f := fun k => Finset.univ.sup
    (fun B : Matrix (Fin k) (Fin k) Bool => (boolMatrix B).det.natAbs))
    (Finset.mem_range.mpr (Nat.lt_succ_of_le hn))

theorem one_le_delta01 (m : ℕ) : 1 ≤ delta01 m := by
  simpa using det_natAbs_le_delta01 (Nat.zero_le m) (fun _ _ => false)

theorem delta01_mono {m k : ℕ} (h : m ≤ k) : delta01 m ≤ delta01 k := by
  apply Finset.sup_le
  intro n hn
  apply Finset.sup_le
  intro A _
  exact det_natAbs_le_delta01 (by have := Finset.mem_range.mp hn; omega) A

/-- Changing the signs of entire rows preserves the absolute determinant. -/
theorem rowSigned_det_natAbs {n : ℕ} (A : Matrix (Fin n) (Fin n) Bool)
    (sign : Fin n → ℤ) (hs : ∀ i, sign i = 1 ∨ sign i = -1) :
    (Matrix.of fun i j => sign i * boolMatrix A i j).det.natAbs =
      (boolMatrix A).det.natAbs := by
  rw [Matrix.det_mul_column, Int.natAbs_mul]
  have habs : (∏ i, sign i).natAbs = 1 := by
    rw [show (∏ i, sign i).natAbs = ∏ i, (sign i).natAbs from
      map_prod Int.natAbsHom _ _]
    apply Finset.prod_eq_one
    intro i _
    rcases hs i with h | h <;> simp [h]
  rw [habs, one_mul]

theorem rowSigned_det_natAbs_le_delta01 {n m : ℕ} (hn : n ≤ m)
    (A : Matrix (Fin n) (Fin n) Bool) (sign : Fin n → ℤ)
    (hs : ∀ i, sign i = 1 ∨ sign i = -1) :
    (Matrix.of fun i j => sign i * boolMatrix A i j).det.natAbs ≤ delta01 m := by
  rw [rowSigned_det_natAbs A sign hs]
  exact det_natAbs_le_delta01 hn A

/-- A whole row is either zero-one or the negative of a zero-one row. -/
def RowSignedZeroOne {r c : Type*} (M : Matrix r c ℤ) : Prop :=
  ∀ i, (∀ j, M i j = 0 ∨ M i j = 1) ∨ (∀ j, M i j = 0 ∨ M i j = -1)

/-- Selecting rows and columns preserves the whole-row sign condition. -/
theorem RowSignedZeroOne.submatrix {r c r' c' : Type*} {M : Matrix r c ℤ}
    (hM : RowSignedZeroOne M) (rows : r' → r) (cols : c' → c) :
    RowSignedZeroOne (M.submatrix rows cols) := by
  intro i
  rcases hM (rows i) with h | h
  · exact Or.inl (fun j => h (cols j))
  · exact Or.inr (fun j => h (cols j))

theorem RowSignedZeroOne.det_natAbs_le {n m : ℕ} {M : Matrix (Fin n) (Fin n) ℤ}
    (hM : RowSignedZeroOne M) (hn : n ≤ m) : M.det.natAbs ≤ delta01 m := by
  classical
  let sign : Fin n → ℤ := fun i => if ∀ j, M i j = 0 ∨ M i j = 1 then 1 else -1
  let A : Matrix (Fin n) (Fin n) Bool := fun i j => decide (M i j ≠ 0)
  have hs : ∀ i, sign i = 1 ∨ sign i = -1 := by
    intro i
    dsimp [sign]
    split <;> simp
  have hEq : M = Matrix.of (fun i j => sign i * boolMatrix A i j) := by
    ext i j
    by_cases hp : ∀ k, M i k = 0 ∨ M i k = 1
    · rcases hp j with h | h <;> simp [sign, A, boolMatrix, hp, h]
    · have hn := (hM i).resolve_left hp
      rcases hn j with h | h <;> simp [sign, A, boolMatrix, hp, h]
  rw [hEq]
  exact rowSigned_det_natAbs_le_delta01 hn A sign hs

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive kernel reduction enumerates all Boolean matrices through this order.
theorem delta01_one : delta01 1 = 1 := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive kernel reduction enumerates all Boolean matrices through this order.
theorem delta01_two : delta01 2 = 1 := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive kernel reduction enumerates all Boolean matrices through this order.
theorem delta01_three : delta01 3 = 2 := by decide

end NetworkSimplex.Threshold
