import Formal.DAGSpectral.EigenCompareCoefficientTrace

namespace DAGSpectral
open ReciprocalAnchor Matrix

def eigenDifferenceExpr {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (i j : Fin (n * n)) : ArithmeticExpr :=
  let u := finProdFinEquiv.symm i
  let v := finProdFinEquiv.symm j
  .op .sub (.atom (if u.2=v.2 then A u.1 v.1 else 0))
    (.atom (if u.1=v.1 then B u.2 v.2 else 0))

@[simp] theorem eigenDifferenceExpr_eval {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (i j : Fin (n * n)) : (eigenDifferenceExpr A B i j).eval = eigenDifferenceFinite A B i j := rfl

@[simp] theorem eigenDifferenceExpr_operations {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (i j : Fin (n * n)) : (eigenDifferenceExpr A B i j).operations = 1 := rfl

def eigenDifferenceWithTrace {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin (n * n)) (Fin (n * n)) ℚ × List ArithmeticEvent :=
  (fun i j => (eigenDifferenceExpr A B i j).eval, matrixExprTrace (eigenDifferenceExpr A B))

theorem eigenDifferenceWithTrace_value {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (eigenDifferenceWithTrace A B).1 = eigenDifferenceFinite A B := rfl

theorem eigenDifferenceWithTrace_length {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (eigenDifferenceWithTrace A B).2.length = (n * n)*(n * n) := by
  simp only [eigenDifferenceWithTrace]
  rw [matrixExprTrace_length _ (eigenDifferenceExpr_operations A B)]
  omega

theorem eigenDifferenceWithTrace_bits {n C : ℕ} (hC : 0 < C)
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A C) (hB : MatrixBits B C) :
    ∀ e ∈ (eigenDifferenceWithTrace A B).2, eventBits (arithmeticWidth 1 C) e := by
  apply matrixExprTrace_bits _ (eigenDifferenceExpr_operations A B)
  intro i j
  constructor <;> dsimp [ArithmeticExpr.leavesBounded]
  · split_ifs
    · exact hA _ _
    · exact rationalBits_mono rationalBits_zero hC
  · split_ifs
    · exact hB _ _
    · exact rationalBits_mono rationalBits_zero hC

end DAGSpectral
