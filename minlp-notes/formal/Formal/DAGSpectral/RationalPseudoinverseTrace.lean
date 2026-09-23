import Formal.DAGSpectral.RationalPseudoinverse
import Formal.DAGSpectral.EigenCompareCoefficientTrace
import Formal.DAGSpectral.ExpressionMatrix

namespace DAGSpectral
open Matrix Polynomial ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- A uniform expression budget gives a uniform operand and bit-work budget. -/
theorem expression_trace_uniform {B C : ℕ} (e : ArithmeticExpr)
    (hB : e.leavesBounded B) (hC : e.operations ≤ C) :
    (∀ z ∈ e.trace, eventBits (arithmeticWidth C B) z) ∧
      traceBitWork (arithmeticWidth C B) e.trace ≤ C*(256*(arithmeticWidth C B+1)^3) := by
  have hz : ∀ z ∈ e.trace, eventBits (arithmeticWidth C B) z := fun z hz =>
    eventBits_mono ((e.eval_trace_bits hB).2 z hz) (arithmeticWidth_mono hC)
  exact ⟨hz, (traceBitWork_le hz).trans (by rw [e.trace_length]; exact Nat.mul_le_mul_right _ hC)⟩

/-- Evaluating all coefficients and testing equality to zero costs two ordered
comparisons per coefficient, in addition to its arithmetic circuit. -/
def coefficientIndexTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : List ArithmeticEvent :=
  let r := charpolyCoefficientsWithTrace A
  r.2 ++ (r.1.flatMap fun q => [(.compare,q,0),(.compare,0,q)])

def coefficientIndexOperations (n : ℕ) : ℕ := (n+1)*(coefficientOperations n+2)

theorem coefficientIndexTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (coefficientIndexTrace A).length ≤ coefficientIndexOperations n := by
  have hc := charpolyCoefficientsWithTrace_length A
  simp only [coefficientIndexTrace, List.length_append, List.length_flatMap]
  simp only [List.length_cons, List.length_nil, Nat.zero_add, List.map_const',
    List.sum_replicate, nsmul_eq_mul, charpolyCoefficientsWithTrace_values, List.length_ofFn]
  unfold coefficientIndexOperations
  nlinarith

theorem coefficientIndexTrace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    ∀ z ∈ coefficientIndexTrace A, eventBits (arithmeticWidth (coefficientOperations n) B) z := by
  have hwidth : B ≤ arithmeticWidth (coefficientOperations n) B := by
    simpa only [arithmeticWidth_zero] using arithmeticWidth_mono (B := B)
      (Nat.zero_le (coefficientOperations n))
  have hz := rationalBits_mono rationalBits_zero (show 1 ≤
    arithmeticWidth (coefficientOperations n) B by omega)
  intro z hzmem
  simp only [coefficientIndexTrace, List.mem_append] at hzmem
  rcases hzmem with h | h
  · exact charpolyCoefficientsWithTrace_bits hB hA z h
  · obtain ⟨q,hq,h⟩ := List.mem_flatMap.mp h
    have hq' := charpolyCoefficientsWithTrace_value_bits hB hA q hq
    simp only [List.mem_cons, List.not_mem_nil, or_false] at h
    rcases h with rfl | rfl
    · exact ⟨hq', hz⟩
    · exact ⟨hz, hq'⟩

/-- Rational nonzeroness is computed from two ordered comparisons. -/
def rationalNonzeroRun (q : ℚ) : Bool × List ArithmeticEvent :=
  (!(decide (q ≤ 0) && decide (0 ≤ q)), [(.compare,q,0),(.compare,0,q)])

theorem rationalNonzeroRun_value (q : ℚ) : (rationalNonzeroRun q).1 = decide (q ≠ 0) := by
  by_cases h : q = 0
  · simp [rationalNonzeroRun, h]
  · rcases lt_or_gt_of_ne h with hlt | hgt
    · simp [rationalNonzeroRun, hlt.le, not_le.mpr hlt, h]
    · simp [rationalNonzeroRun, hgt.le, not_le.mpr hgt, h]

/-- The index is read from the coefficient values returned by the executed runs. -/
def coefficientIndexRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    ℕ × List ArithmeticEvent :=
  let r := charpolyCoefficientsWithTrace A
  let tests := r.1.map rationalNonzeroRun
  ((tests.map Prod.fst).findIdx id, r.2 ++ tests.flatMap Prod.snd)

theorem coefficientIndexRun_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    coefficientIndexRun A = (zeroRootIndex A, coefficientIndexTrace A) := by
  apply Prod.ext
  · simp only [coefficientIndexRun, List.map_map, Function.comp_def, rationalNonzeroRun_value,
      List.findIdx_map, charpolyCoefficientsWithTrace_values, zeroRootIndex_eq]
    have ht : A.charpoly.natTrailingDegree < n+1 := by
      have hh := natTrailingDegree_le_natDegree A.charpoly
      simp only [Matrix.charpoly_natDegree_eq_dim, Fintype.card_fin] at hh
      omega
    apply (List.findIdx_eq (by simpa only [List.length_ofFn] using ht)).mpr
    constructor
    · simp only [List.getElem_ofFn, rationalCharpolyCoeff_eq, id_eq, decide_eq_true_eq]
      exact coeff_natTrailingDegree_ne_zero.mpr A.charpoly_monic.ne_zero
    · intro j hj
      simp only [List.getElem_ofFn, rationalCharpolyCoeff_eq, id_eq, decide_eq_false_iff_not,
        not_not]
      exact coeff_eq_zero_of_lt_natTrailingDegree hj
  · simp only [coefficientIndexRun, List.flatMap_map,
      rationalNonzeroRun, coefficientIndexTrace]

/-- Materialize each scalar run once. Both matrix entries and events are read
from the resulting vectors of result/event pairs. -/
def matrixArithmeticRun {l m : ℕ} (E : Matrix (Fin l) (Fin m) ArithmeticExpr) :
    Matrix (Fin l) (Fin m) ℚ × List ArithmeticEvent :=
  let rows := Vector.ofFn fun i : Fin l => Vector.ofFn fun j : Fin m => (E i j).run
  (Matrix.of fun i j => ((rows.get i).get j).1,
    rows.toList.flatMap fun row => row.toList.flatMap Prod.snd)

theorem matrixArithmeticRun_eq {l m : ℕ} (E : Matrix (Fin l) (Fin m) ArithmeticExpr) :
    matrixArithmeticRun E = (exprMatrixEval E, matrixExprTrace E) := by
  apply Prod.ext
  · ext i j
    simp [matrixArithmeticRun, exprMatrixEval, ArithmeticExpr.run_eq]
  · simp only [matrixArithmeticRun, Vector.toList_ofFn, matrixExprTrace,
      List.flatMap, List.map_ofFn, Function.comp_def, ArithmeticExpr.run_eq]

def atomExprMatrix {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ArithmeticExpr := fun i j => .atom (A i j)

@[simp] theorem atomExprMatrix_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    exprMatrixEval (atomExprMatrix A) = A := rfl

/-- A reciprocal polynomial entry with all coefficient and matrix operations expanded. -/
def reciprocalEntryExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (k : ℕ)
    (i j : Fin n) : ArithmeticExpr :=
  .op .mul (.op .inv (.op .neg (coefficientExpr A k) (.atom 0)) (.atom 0))
    (sumExpr (List.ofFn fun d : Fin (n+1) => .op .mul
      (coefficientExpr A (d.val+1+k)) (exprMatrixPow (atomExprMatrix A) d.val i j)))

def reciprocalEntryOperations (n : ℕ) : ℕ :=
  coefficientOperations n+3 + (n+1)*(coefficientOperations n+exprMatrixPowCap n 0 n+2)

theorem reciprocalEntryExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    (reciprocalEntryExpr A (zeroRootIndex A) i j).eval = reciprocalMatrix A i j := by
  simp only [reciprocalEntryExpr, ArithmeticExpr.eval, primitiveResult, coefficientExpr_eval,
    sumExpr_eval, List.map_ofFn, Function.comp_def, List.sum_ofFn]
  have hp (d : ℕ) : (exprMatrixPow (atomExprMatrix A) d i j).eval = (A^d) i j := by
    exact congrFun (congrFun (exprMatrixPow_eval (atomExprMatrix A) d) i) j
  simp only [hp, reciprocalMatrix, Matrix.smul_apply, smul_eq_mul, Matrix.sum_apply]

theorem reciprocalEntryExpr_leaves {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (k : ℕ) (i j : Fin n) :
    (reciprocalEntryExpr A k i j).leavesBounded B := by
  refine ⟨⟨⟨coefficientExpr_leaves hB hA k, rationalBits_mono rationalBits_zero hB⟩,
    rationalBits_mono rationalBits_zero hB⟩, ?_⟩
  apply sumExpr_leaves hB
  intro e he
  obtain ⟨d, rfl⟩ := List.mem_ofFn.mp he
  exact ⟨coefficientExpr_leaves hB hA _, 
    exprMatrixPow_leaves hB (A := atomExprMatrix A) hA d.val i j⟩

theorem reciprocalEntryExpr_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (k : ℕ) (i j : Fin n) :
    (reciprocalEntryExpr A k i j).operations ≤ reciprocalEntryOperations n := by
  have hc := coefficientExpr_operations_le A k
  have hs : ∑ d : Fin (n+1),
      ((coefficientExpr A (d.val+1+k)).operations +
        (exprMatrixPow (atomExprMatrix A) d.val i j).operations+1) ≤
      (n+1)*(coefficientOperations n+exprMatrixPowCap n 0 n+1) := by
    calc
      _ ≤ ∑ _d : Fin (n+1), (coefficientOperations n+exprMatrixPowCap n 0 n+1) := by
        apply Finset.sum_le_sum
        intro d _
        have hp := (exprMatrixPow_operations (L := 0)
          (A := atomExprMatrix A) (fun _ _ => le_refl 0) d.val i j).trans
          (exprMatrixPowCap_mono n 0 (by omega : d.val ≤ n))
        have hh := coefficientExpr_operations_le A (d.val+1+k)
        omega
      _ = _ := by simp
  simp only [reciprocalEntryExpr, ArithmeticExpr.operations, Nat.add_zero,
    sumExpr_operations, List.map_ofFn, Function.comp_def, List.sum_ofFn,
    List.length_ofFn]
  unfold reciprocalEntryOperations
  nlinarith

def pseudoInverseExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ArithmeticExpr :=
  let R := Matrix.of (reciprocalEntryExpr A (zeroRootIndex A))
  exprMatrixMul (exprMatrixMul (atomExprMatrix A) R) R

@[simp] theorem pseudoInverseExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    exprMatrixEval (pseudoInverseExpr A) = rationalPseudoInverse A := by
  have he : exprMatrixEval (Matrix.of (reciprocalEntryExpr A (zeroRootIndex A))) =
      reciprocalMatrix A := by
    ext i j
    exact reciprocalEntryExpr_eval A i j
  dsimp only [pseudoInverseExpr]
  rw [exprMatrixMul_eval, exprMatrixMul_eval, atomExprMatrix_eval, he]
  rfl

def pseudoInverseEntryOperations (n : ℕ) : ℕ :=
  n*(n*(reciprocalEntryOperations n+2)+reciprocalEntryOperations n+2)

theorem pseudoInverseExpr_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    (pseudoInverseExpr A i j).operations ≤ pseudoInverseEntryOperations n := by
  dsimp only [pseudoInverseExpr]
  simpa only [pseudoInverseEntryOperations, Nat.zero_add] using exprMatrixMul_operations
    (B := Matrix.of (reciprocalEntryExpr A (zeroRootIndex A)))
    (exprMatrixMul_operations (L := 0) (A := atomExprMatrix A)
      (B := Matrix.of (reciprocalEntryExpr A (zeroRootIndex A))) (fun _ _ => le_refl 0)
      (reciprocalEntryExpr_operations A (zeroRootIndex A)))
    (reciprocalEntryExpr_operations A (zeroRootIndex A)) i j

theorem pseudoInverseExpr_leaves {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (i j : Fin n) :
    (pseudoInverseExpr A i j).leavesBounded B := by
  dsimp only [pseudoInverseExpr]
  exact exprMatrixMul_leaves hB
    (exprMatrixMul_leaves hB (A := atomExprMatrix A) hA
      (reciprocalEntryExpr_leaves hB hA (zeroRootIndex A)))
    (reciprocalEntryExpr_leaves hB hA (zeroRootIndex A)) i j

def rationalPseudoInverseWithTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ℚ × List ArithmeticEvent :=
  let k := coefficientIndexRun A
  let R := Matrix.of (reciprocalEntryExpr A k.1)
  let g := matrixArithmeticRun (exprMatrixMul (exprMatrixMul (atomExprMatrix A) R) R)
  (g.1, k.2 ++ g.2)

theorem rationalPseudoInverseWithTrace_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    rationalPseudoInverseWithTrace A =
      (rationalPseudoInverse A,
        coefficientIndexTrace A ++ matrixExprTrace (pseudoInverseExpr A)) := by
  simp only [rationalPseudoInverseWithTrace, coefficientIndexRun_eq, matrixArithmeticRun_eq]
  change (exprMatrixEval (pseudoInverseExpr A), _) = _
  rw [pseudoInverseExpr_eval]
  rfl

@[simp] theorem rationalPseudoInverseWithTrace_value {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalPseudoInverseWithTrace A).1 = rationalPseudoInverse A := by
  rw [rationalPseudoInverseWithTrace_eq]

def pseudoInverseOperations (n : ℕ) : ℕ :=
  coefficientIndexOperations n + n*n*pseudoInverseEntryOperations n

def pseudoInverseTraceDepth (n : ℕ) : ℕ := coefficientOperations n+pseudoInverseEntryOperations n

theorem rationalPseudoInverseWithTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalPseudoInverseWithTrace A).2.length ≤ pseudoInverseOperations n := by
  simpa only [rationalPseudoInverseWithTrace_eq, List.length_append, pseudoInverseOperations] using
    Nat.add_le_add (coefficientIndexTrace_length A)
      (matrixExprTrace_length_le _ (pseudoInverseExpr_operations A))

theorem rationalPseudoInverseWithTrace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    ∀ z ∈ (rationalPseudoInverseWithTrace A).2,
      eventBits (arithmeticWidth (pseudoInverseTraceDepth n) B) z := by
  intro z hz
  rw [rationalPseudoInverseWithTrace_eq] at hz
  rcases List.mem_append.mp hz with hz | hz
  · exact eventBits_mono (coefficientIndexTrace_bits hB hA z hz)
      (arithmeticWidth_mono (by unfold pseudoInverseTraceDepth; omega))
  · exact eventBits_mono
      (matrixExprTrace_bits_of_le _ (pseudoInverseExpr_operations A)
        (pseudoInverseExpr_leaves hB hA) z hz)
      (arithmeticWidth_mono (by unfold pseudoInverseTraceDepth; omega))

theorem rationalPseudoInverseWithTrace_bitWork {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    traceBitWork (arithmeticWidth (pseudoInverseTraceDepth n) B)
      (rationalPseudoInverseWithTrace A).2 ≤
      pseudoInverseOperations n*(256*(arithmeticWidth (pseudoInverseTraceDepth n) B+1)^3) :=
  (traceBitWork_le (rationalPseudoInverseWithTrace_bits hB hA)).trans
    (Nat.mul_le_mul_right _ (rationalPseudoInverseWithTrace_length A))

theorem rationalPseudoInverse_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    MatrixBits (rationalPseudoInverse A) (arithmeticWidth (pseudoInverseTraceDepth n) B) := by
  intro i j
  have he := (pseudoInverseExpr A i j).eval_trace_bits (pseudoInverseExpr_leaves hB hA i j)
  have hv : (pseudoInverseExpr A i j).eval = rationalPseudoInverse A i j :=
    congrFun (congrFun (pseudoInverseExpr_eval A) i) j
  rw [← hv]
  exact rationalBits_mono he.1 (arithmeticWidth_mono
    ((pseudoInverseExpr_operations A i j).trans (by unfold pseudoInverseTraceDepth; omega)))

end DAGSpectral
