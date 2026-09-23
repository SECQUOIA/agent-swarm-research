import Formal.MatroidSpectral.EliminationBits

/-! Arithmetic counts for denominator clearing and exact rational determinant
evaluation. Integer division is one arithmetic operation here; digit costs must
also use the operand-size bounds in `EliminationBits`. -/
namespace MatroidSpectral.Elimination
open Matrix
open scoped BigOperators

def productNatRun : List ℕ → ℕ × ℕ
  | [] => (1, 0)
  | x :: xs =>
      let tail := productNatRun xs
      (x*tail.1, tail.2+1)

@[simp] theorem productNatRun_value (xs : List ℕ) :
    (productNatRun xs).1 = xs.prod := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [productNatRun, ih]

@[simp] theorem productNatRun_operations (xs : List ℕ) :
    (productNatRun xs).2 = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [productNatRun, ih]

def powerNatRun (x : ℕ) : ℕ → ℕ × ℕ
  | 0 => (1, 0)
  | n+1 =>
      let previous := powerNatRun x n
      (previous.1*x, previous.2+1)

@[simp] theorem powerNatRun_value (x n : ℕ) : (powerNatRun x n).1 = x^n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [powerNatRun, ih, pow_succ]

@[simp] theorem powerNatRun_operations (x n : ℕ) : (powerNatRun x n).2 = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [powerNatRun, ih]

def denominatorRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℕ × ℕ :=
  productNatRun ((List.ofFn fun i : Fin n => List.ofFn fun j : Fin n => (A i j).den).flatten)

@[simp] theorem denominatorRun_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (denominatorRun A).1 = matrixDenominator A := by
  simp [denominatorRun, List.prod_flatten, List.map_ofFn, Function.comp_def,
    List.prod_ofFn, matrixDenominator]

@[simp] theorem denominatorRun_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (denominatorRun A).2 = n*n := by
  simp [denominatorRun, List.length_flatten, List.map_ofFn, Function.comp_def]

/-- Denominator clearing materializes each integer once. Its exact division and
multiplication are each charged once, even if a factor is zero. -/
def clearEntryRun (D : ℕ) (x : ℚ) : ℤ × ℕ :=
  let quotient := D / x.den
  (x.num * (quotient : ℕ), 2)

structure ClearingRun (n : ℕ) where
  matrix : StoredMatrix ℤ n
  operations : ℕ

def clearingRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (D : ℕ) : ClearingRun n :=
  let entries := Vector.ofFn fun i => Vector.ofFn fun j => clearEntryRun D (A i j)
  ⟨entries.map (fun row => row.map Prod.fst),
    ∑ i : Fin n, ∑ j : Fin n, entries[i.val][j.val].2⟩

@[simp] theorem clearingRun_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    view (clearingRun A (matrixDenominator A)).matrix = integerMatrix A := by
  ext i j
  simp [view, clearingRun, clearEntryRun, integerMatrix]

@[simp] theorem clearingRun_operations {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (D : ℕ) :
    (clearingRun A D).operations = 2*n*n := by
  simp [clearingRun, clearEntryRun]
  ring

/-- Operands of the same recursive multiplication loops. -/
def productNatOperands : List ℕ → List (ℕ × ℕ)
  | [] => []
  | x :: xs => productNatOperands xs ++ [(x, (productNatRun xs).1)]

def powerNatOperands (x : ℕ) : ℕ → List (ℕ × ℕ)
  | 0 => []
  | n+1 => powerNatOperands x n ++ [((powerNatRun x n).1, x)]

def natPairRat (e : ℕ × ℕ) : ℚ × ℚ := (e.1, e.2)
def intPairRat (e : ℤ × ℤ) : ℚ × ℚ := (e.1, e.2)

def denominatorOperands {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : List (ℚ × ℚ) :=
  (productNatOperands
    ((List.ofFn fun i : Fin n => List.ofFn fun j : Fin n => (A i j).den).flatten)).map
      natPairRat

def clearingOperands {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (D : ℕ) : List (ℚ × ℚ) :=
  (List.ofFn fun i : Fin n => (List.ofFn fun j : Fin n =>
    [((D : ℚ), ((A i j).den : ℚ)),
      (((A i j).num : ℚ), ((D / (A i j).den : ℕ) : ℚ))]).flatten).flatten

/-- The complete arithmetic execution: denominator product, clearing,
integer determinant, denominator power, and one final rational division. -/
def rationalDeterminantRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ScalarRun ℚ :=
  let D := denominatorRun A
  let Z := clearingRun A D.1
  let result := determinantRun n Z.matrix
  let power := powerNatRun D.1 n
  ⟨(result.value : ℚ) / (power.1 : ℚ), D.2+Z.operations+result.operations+power.2+1,
    denominatorOperands A ++ clearingOperands A D.1 ++ result.operands.map intPairRat ++
      (powerNatOperands D.1 n).map natPairRat ++ [((result.value : ℚ), (power.1 : ℚ))]⟩

theorem rationalDeterminantRun_correct {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalDeterminantRun A).value = A.det := by
  simp only [rationalDeterminantRun, denominatorRun_value, determinantRun_correct,
    clearingRun_value, powerNatRun_value, Nat.cast_pow]
  exact (det_eq_integerMatrix_div A).symm

theorem rationalDeterminantRun_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalDeterminantRun A).value = rationalDeterminant A := by
  rw [rationalDeterminantRun_correct, rationalDeterminant_correct]

/-- Includes preprocessing; polynomial in the variable order. -/
theorem rationalDeterminantRun_operations_le {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalDeterminantRun A).operations ≤ 8*(n+1)^4 := by
  simp only [rationalDeterminantRun, denominatorRun_operations, clearingRun_operations,
    powerNatRun_operations]
  have hh := determinantRun_operations_le n
    (clearingRun A (denominatorRun A).1).matrix
  nlinarith

end MatroidSpectral.Elimination
