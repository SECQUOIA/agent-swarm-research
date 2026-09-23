import Formal.DAGSpectral.MatrixArithmeticTrace

/-! Matrix expressions compose the actual scalar arithmetic trees. No matrix
operation is hidden behind an unevaluated rational atom. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor
open scoped BigOperators

def exprMatrixEval {l m : ℕ} (A : Matrix (Fin l) (Fin m) ArithmeticExpr) :
    Matrix (Fin l) (Fin m) ℚ := Matrix.of fun i j => (A i j).eval

def exprMatrixMul {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ArithmeticExpr)
    (B : Matrix (Fin n) (Fin m) ArithmeticExpr) : Matrix (Fin l) (Fin m) ArithmeticExpr :=
  Matrix.of fun i j => sumExpr (List.ofFn fun k => .op .mul (A i k) (B k j))

@[simp] theorem exprMatrixMul_eval {l n m : ℕ}
    (A : Matrix (Fin l) (Fin n) ArithmeticExpr) (B : Matrix (Fin n) (Fin m) ArithmeticExpr) :
    exprMatrixEval (exprMatrixMul A B) = exprMatrixEval A * exprMatrixEval B := by
  ext i j
  simp [exprMatrixEval, exprMatrixMul, ArithmeticExpr.eval, primitiveResult,
    Matrix.mul_apply, Function.comp_def, List.sum_ofFn]

theorem exprMatrixMul_leaves {l n m K : ℕ} (hK : 0 < K)
    {A : Matrix (Fin l) (Fin n) ArithmeticExpr} {B : Matrix (Fin n) (Fin m) ArithmeticExpr}
    (hA : ∀ i j, (A i j).leavesBounded K) (hB : ∀ i j, (B i j).leavesBounded K)
    (i : Fin l) (j : Fin m) : (exprMatrixMul A B i j).leavesBounded K := by
  apply sumExpr_leaves hK
  intro e he
  obtain ⟨k, rfl⟩ := List.mem_ofFn.mp he
  exact ⟨hA i k, hB k j⟩

theorem exprMatrixMul_operations {l n m L R : ℕ}
    {A : Matrix (Fin l) (Fin n) ArithmeticExpr} {B : Matrix (Fin n) (Fin m) ArithmeticExpr}
    (hA : ∀ i j, (A i j).operations ≤ L) (hB : ∀ i j, (B i j).operations ≤ R)
    (i : Fin l) (j : Fin m) : (exprMatrixMul A B i j).operations ≤ n * (L + R + 2) := by
  simp only [exprMatrixMul, Matrix.of_apply, sumExpr_operations, List.map_ofFn,
    List.length_ofFn, List.sum_ofFn, Function.comp_def, ArithmeticExpr.operations]
  have hs : (∑ k : Fin n, ((A i k).operations + (B k j).operations + 1)) ≤
      n * (L + R + 1) := by
    calc
      _ ≤ ∑ _k : Fin n, (L + R + 1) :=
        Finset.sum_le_sum (fun k _ => by have := hA i k; have := hB k j; omega)
      _ = _ := by simp
  nlinarith

/-- The identity expression contains only the constants zero and one. -/
def exprMatrixOne (n : ℕ) : Matrix (Fin n) (Fin n) ArithmeticExpr :=
  Matrix.of fun i j => .atom (if i = j then 1 else 0)

@[simp] theorem exprMatrixOne_eval (n : ℕ) : exprMatrixEval (exprMatrixOne n) = 1 := by
  ext i j
  simp [exprMatrixEval, exprMatrixOne, ArithmeticExpr.eval, Matrix.one_apply]

@[simp] theorem exprMatrixOne_operations {n : ℕ} (i j : Fin n) :
    (exprMatrixOne n i j).operations = 0 := rfl

theorem exprMatrixOne_leaves {n K : ℕ} (hK : 0 < K) (i j : Fin n) :
    (exprMatrixOne n i j).leavesBounded K := by
  change RationalBits (if i = j then (1 : ℚ) else 0) K
  split_ifs
  · exact rationalBits_mono rationalBits_one hK
  · exact rationalBits_mono rationalBits_zero hK

def exprMatrixPow {n : ℕ} (A : Matrix (Fin n) (Fin n) ArithmeticExpr) :
    ℕ → Matrix (Fin n) (Fin n) ArithmeticExpr
  | 0 => exprMatrixOne n
  | k + 1 => exprMatrixMul (exprMatrixPow A k) A

@[simp] theorem exprMatrixPow_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ArithmeticExpr)
    (k : ℕ) : exprMatrixEval (exprMatrixPow A k) = exprMatrixEval A ^ k := by
  induction k with
  | zero => simp [exprMatrixPow]
  | succ k ih => simp only [exprMatrixPow, exprMatrixMul_eval, ih, pow_succ]

theorem exprMatrixPow_leaves {n K : ℕ} (hK : 0 < K)
    {A : Matrix (Fin n) (Fin n) ArithmeticExpr} (hA : ∀ i j, (A i j).leavesBounded K)
    (k : ℕ) (i j : Fin n) : (exprMatrixPow A k i j).leavesBounded K := by
  induction k generalizing i j with
  | zero => exact exprMatrixOne_leaves hK i j
  | succ k ih => exact exprMatrixMul_leaves hK (fun i j => ih i j) hA i j

/-- An explicit per-entry operation bound for composed powers. -/
def exprMatrixPowCap (n L : ℕ) : ℕ → ℕ
  | 0 => 0
  | k + 1 => n * (exprMatrixPowCap n L k + L + 2)

theorem exprMatrixPow_operations {n L : ℕ}
    {A : Matrix (Fin n) (Fin n) ArithmeticExpr} (hA : ∀ i j, (A i j).operations ≤ L)
    (k : ℕ) (i j : Fin n) : (exprMatrixPow A k i j).operations ≤ exprMatrixPowCap n L k := by
  induction k generalizing i j with
  | zero => rfl
  | succ k ih => exact exprMatrixMul_operations (fun i j => ih i j) hA i j

theorem exprMatrixPowCap_mono (n L : ℕ) : Monotone (exprMatrixPowCap n L) := by
  apply monotone_nat_of_le_succ
  intro k
  rw [exprMatrixPowCap]
  cases n with
  | zero => cases k <;> simp [exprMatrixPowCap]
  | succ n => nlinarith

/-- Bounded expression entries give an actual row-major trace length bound. -/
theorem matrixExprTrace_length_le {l m N : ℕ}
    (E : Matrix (Fin l) (Fin m) ArithmeticExpr) (hN : ∀ i j, (E i j).operations ≤ N) :
    (matrixExprTrace E).length ≤ l * m * N := by
  simp only [matrixExprTrace, List.length_flatten, List.map_ofFn, Function.comp_def,
    ArithmeticExpr.trace_length, List.sum_ofFn]
  calc
    _ ≤ ∑ _i : Fin l, ∑ _j : Fin m, N := by
      apply Finset.sum_le_sum
      intro i _
      exact Finset.sum_le_sum (fun j _ => hN i j)
    _ = _ := by simp; ring

theorem matrixExprTrace_bits_of_le {l m N K : ℕ}
    (E : Matrix (Fin l) (Fin m) ArithmeticExpr) (hN : ∀ i j, (E i j).operations ≤ N)
    (hE : ∀ i j, (E i j).leavesBounded K) :
    ∀ e ∈ matrixExprTrace E, eventBits (arithmeticWidth N K) e := by
  intro e he
  obtain ⟨row, hrow, he⟩ := List.mem_flatten.mp he
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hrow
  obtain ⟨col, hcol, he⟩ := List.mem_flatten.mp he
  obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hcol
  exact eventBits_mono (((E i j).eval_trace_bits (hE i j)).2 e he)
    (arithmeticWidth_mono (hN i j))

end DAGSpectral
