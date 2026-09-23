import Formal.DAGSpectral.EigenCompareCoefficientTrace
import Formal.DAGSpectral.EigenCompareTrace

namespace DAGSpectral
open Matrix ReciprocalAnchor

def thresholdShiftExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (q : ℚ)
    (i j : Fin n) : ArithmeticExpr :=
  .op .sub (.atom (A i j)) (.atom (if i=j then q else 0))

@[simp] theorem thresholdShiftExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (q : ℚ) (i j : Fin n) : (thresholdShiftExpr A q i j).eval = (A-q • 1) i j := by
  simp [thresholdShiftExpr, ArithmeticExpr.eval, primitiveResult, Matrix.one_apply]

@[simp] theorem thresholdShiftExpr_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (q : ℚ) (i j : Fin n) : (thresholdShiftExpr A q i j).operations = 1 := rfl

def eigenThresholdTestWithTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (q : ℚ) :
    Bool × List ArithmeticEvent :=
  let shifted := fun i j => (thresholdShiftExpr A q i j).eval
  let test := rationalPSDTestWithTrace shifted
  (test.1, matrixExprTrace (thresholdShiftExpr A q) ++ test.2)

theorem eigenThresholdTestWithTrace_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (q : ℚ) :
    (eigenThresholdTestWithTrace A q).1 = eigenThresholdTest A q := by
  simp only [eigenThresholdTestWithTrace, thresholdShiftExpr_eval, eigenThresholdTest]
  exact rationalPSDTestWithTrace_value (A-q • 1)

def thresholdTestOperations (n : ℕ) : ℕ := n*n+psdTestOperations n

theorem eigenThresholdTestWithTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (q : ℚ) :
    ((eigenThresholdTestWithTrace A q).2).length ≤ thresholdTestOperations n := by
  have h := rationalPSDTestWithTrace_length (A-q • 1)
  simp only [eigenThresholdTestWithTrace, thresholdShiftExpr_eval, List.length_append]
  rw [matrixExprTrace_length _ (thresholdShiftExpr_operations A q)]
  change n*n*1 + ((rationalPSDTestWithTrace (A-q • 1)).2).length ≤ _
  unfold thresholdTestOperations
  omega

def thresholdTestWidth (n B Q : ℕ) : ℕ :=
  arithmeticWidth (coefficientOperations n+1) (B+Q+2)

theorem eigenThresholdTestWithTrace_bits {n B Q : ℕ}
    {A : Matrix (Fin n) (Fin n) ℚ} {q : ℚ}
    (hA : MatrixBits A B) (hq : RationalBits q Q) :
    ∀ e ∈ (eigenThresholdTestWithTrace A q).2, eventBits (thresholdTestWidth n B Q) e := by
  have hbase : 0 < B+Q+2 := by omega
  have hshift : MatrixBits (A-q • 1) (B+Q+2) := by
    intro i j
    simp only [Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul, Matrix.one_apply]
    split_ifs
    · simp only [mul_one]
      exact rationalBits_mono (rationalBits_sub (hA i j) hq) (by omega)
    · simp only [mul_zero, sub_zero]
      exact rationalBits_mono (hA i j) (by omega)
  have hleaf (i j : Fin n) : (thresholdShiftExpr A q i j).leavesBounded (B+Q+2) := by
    constructor
    · exact rationalBits_mono (hA i j) (by omega)
    · dsimp [ArithmeticExpr.leavesBounded]
      split_ifs
      · exact rationalBits_mono hq (by omega)
      · exact rationalBits_mono rationalBits_zero (by omega)
  intro e he
  simp only [eigenThresholdTestWithTrace, thresholdShiftExpr_eval, List.mem_append] at he
  rcases he with he | he
  · apply eventBits_mono (matrixExprTrace_bits _ (thresholdShiftExpr_operations A q) hleaf e he)
    exact arithmeticWidth_mono (by omega)
  · apply eventBits_mono (rationalPSDTestWithTrace_bits hbase hshift e he)
    exact arithmeticWidth_mono (by omega)

end DAGSpectral
