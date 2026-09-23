import Formal.DAGSpectral.CriterionSelectMatrix
import Formal.DAGSpectral.CriterionSelectTrace
import Formal.DAGSpectral.MatrixArithmeticTrace

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost Matrix

/-- Execute a rational comparison expression and retain its primitive trace. -/
def expressionComparisonRun (a b : ArithmeticExpr) : Bool × List ArithmeticEvent :=
  let r := (ArithmeticExpr.op .compare a b).run
  (decide (r.1 = 1), r.2)

@[simp] theorem expressionComparisonRun_result (a b : ArithmeticExpr) :
    (expressionComparisonRun a b).1 = decide (a.eval ≤ b.eval) := by
  simp only [expressionComparisonRun, ArithmeticExpr.run_eq, ArithmeticExpr.eval,
    primitiveResult]
  split_ifs <;> simp_all

theorem expressionComparisonRun_bounds (a b : ArithmeticExpr) {B : ℕ}
    (ha : a.leavesBounded B) (hb : b.leavesBounded B) :
    (expressionComparisonRun a b).2.length = a.operations+b.operations+1 ∧
    ∀ e ∈ (expressionComparisonRun a b).2,
      eventBits (arithmeticWidth (a.operations+b.operations+1) B) e := by
  constructor
  · simp [expressionComparisonRun, ArithmeticExpr.run_eq, ArithmeticExpr.operations]
  · simpa only [expressionComparisonRun, ArithmeticExpr.run_eq, ArithmeticExpr.operations] using
      (ArithmeticExpr.eval_trace_bits (.op .compare a b) ⟨ha,hb⟩).2

def determinantLERun {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    Bool × List ArithmeticEvent := expressionComparisonRun (determinantExpr A) (determinantExpr B)

@[simp] theorem determinantLERun_result {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (determinantLERun A B).1 = determinantLE A B := by
  simp [determinantLERun, determinantExpr_eval, determinantLE]

theorem determinantLERun_bounds {n B : ℕ} (hB : 0 < B)
    {A C : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (hC : MatrixBits C B) :
    (determinantLERun A C).2.length ≤ 2*determinantOperations n+1 ∧
    ∀ e ∈ (determinantLERun A C).2,
      eventBits (arithmeticWidth (2*determinantOperations n+1) B) e := by
  have h := expressionComparisonRun_bounds (determinantExpr A) (determinantExpr C)
    (determinantExpr_leaves hB hA) (determinantExpr_leaves hB hC)
  simp only [determinantExpr_operations] at h
  simpa [determinantLERun, two_mul] using And.intro h.1.le h.2

def inverseTraceExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ArithmeticExpr :=
  sumExpr (List.ofFn fun i => inverseEntryExpr A i i)

@[simp] theorem inverseTraceExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (inverseTraceExpr A).eval = Matrix.trace (rationalMatrixInverse A) := by
  simp [inverseTraceExpr, Matrix.trace, Function.comp_def, List.sum_ofFn]

@[simp] theorem inverseTraceExpr_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (inverseTraceExpr A).operations = n*(2*determinantOperations n+3) := by
  simp [inverseTraceExpr,sumExpr_operations,Function.comp_def]
  ring

theorem inverseTraceExpr_leaves {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    (inverseTraceExpr A).leavesBounded B := by
  apply sumExpr_leaves hB
  intro e he
  obtain ⟨i,rfl⟩ := List.mem_ofFn.mp he
  exact inverseEntryExpr_leaves hB hA i i

/-- Testing equality uses the two ordered comparisons, so its rational
operand work is included even on singular inputs. -/
def expressionZeroRun (a : ArithmeticExpr) : Bool × List ArithmeticEvent :=
  let r := a.run
  (decide (r.1 ≤ 0) && decide (0 ≤ r.1),
    r.2 ++ [(.compare,r.1,0),(.compare,0,r.1)])

@[simp] theorem expressionZeroRun_result (a : ArithmeticExpr) :
    (expressionZeroRun a).1 = decide (a.eval = 0) := by
  simp [expressionZeroRun,ArithmeticExpr.run_eq,le_antisymm_iff]

theorem expressionZeroRun_bounds (a : ArithmeticExpr) {B : ℕ}
    (hB : 0 < B) (ha : a.leavesBounded B) :
    (expressionZeroRun a).2.length = a.operations+2 ∧
    ∀ e ∈ (expressionZeroRun a).2, eventBits (arithmeticWidth a.operations B) e := by
  have h := a.eval_trace_bits ha
  have hz : RationalBits 0 (arithmeticWidth a.operations B) :=
    rationalBits_mono rationalBits_zero (hB.trans_le (by
      have := arithmeticWidth_mono (B := B) (Nat.zero_le a.operations)
      simpa only [arithmeticWidth_zero] using this))
  constructor
  · simp [expressionZeroRun,ArithmeticExpr.run_eq]
  · intro e he
    simp only [expressionZeroRun,ArithmeticExpr.run_eq,List.mem_append,
      List.mem_cons,List.not_mem_nil,or_false] at he
    rcases he with he | rfl | rfl
    · exact h.2 _ he
    · exact ⟨h.1,hz⟩
    · exact ⟨hz,h.1⟩

/-- All three expression results are computed once. Computing the trace
comparison also on singular inputs gives a uniform fixed-dimension bound. -/
def inverseTraceCostLERun {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    Bool × List ArithmeticEvent :=
  let zb := expressionZeroRun (determinantExpr B)
  let za := expressionZeroRun (determinantExpr A)
  let t := expressionComparisonRun (inverseTraceExpr A) (inverseTraceExpr B)
  ((if zb.1 then true else if za.1 then false else t.1),zb.2++za.2++t.2)

@[simp] theorem inverseTraceCostLERun_result {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    (inverseTraceCostLERun A B).1 = inverseTraceCostLE A B := by
  simp [inverseTraceCostLERun,determinantExpr_eval,inverseTraceCostLE]

def inverseTraceCompareOperations (n : ℕ) : ℕ :=
  2*determinantOperations n+2*(n*(2*determinantOperations n+3))+5

theorem inverseTraceCostLERun_bounds {n B : ℕ} (hB : 0 < B)
    {A C : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (hC : MatrixBits C B) :
    (inverseTraceCostLERun A C).2.length ≤ inverseTraceCompareOperations n ∧
    ∀ e ∈ (inverseTraceCostLERun A C).2,
      eventBits (arithmeticWidth (inverseTraceCompareOperations n) B) e := by
  have ha := expressionZeroRun_bounds (determinantExpr A) hB (determinantExpr_leaves hB hA)
  have hc := expressionZeroRun_bounds (determinantExpr C) hB (determinantExpr_leaves hB hC)
  have ht := expressionComparisonRun_bounds (inverseTraceExpr A) (inverseTraceExpr C)
    (inverseTraceExpr_leaves hB hA) (inverseTraceExpr_leaves hB hC)
  simp only [determinantExpr_operations,inverseTraceExpr_operations] at ha hc ht
  constructor
  · simp only [inverseTraceCostLERun,List.length_append]
    rw [ha.1,hc.1,ht.1]
    unfold inverseTraceCompareOperations
    omega
  · intro e he
    simp only [inverseTraceCostLERun,List.mem_append] at he
    rcases he with (he|he)|he
    · exact eventBits_mono (hc.2 e he) (arithmeticWidth_mono (by
        unfold inverseTraceCompareOperations; omega))
    · exact eventBits_mono (ha.2 e he) (arithmeticWidth_mono (by
        unfold inverseTraceCompareOperations; omega))
    · exact eventBits_mono (ht.2 e he) (arithmeticWidth_mono (by
        unfold inverseTraceCompareOperations; omega))

def selectDeterminantRun {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α) : Option α × List ArithmeticEvent :=
  bestByRun (fun a b => determinantLERun (J a) (J b)) xs

@[simp] theorem selectDeterminantRun_result {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α) :
    (selectDeterminantRun J xs).1 = selectDeterminant J xs := by
  simp only [selectDeterminantRun,bestByRun_result,determinantLERun_result,selectDeterminant]

def selectInverseTraceRun {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α) : Option α × List ArithmeticEvent :=
  bestByRun (fun a b => inverseTraceCostLERun (J b) (J a)) xs

@[simp] theorem selectInverseTraceRun_result {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α) :
    (selectInverseTraceRun J xs).1 = selectInverseTrace J xs := by
  simp only [selectInverseTraceRun,bestByRun_result,inverseTraceCostLERun_result,selectInverseTrace]

theorem selectDeterminantRun_bitWork {α : Type*} {n B : ℕ} (hB : 0 < B)
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, MatrixBits (J a) B) :
    traceBitWork (arithmeticWidth (2*determinantOperations n+1) B)
      (selectDeterminantRun J xs).2 ≤
      (xs.length-1)*(2*determinantOperations n+1)*
        (256*(arithmeticWidth (2*determinantOperations n+1) B+1)^3) :=
  bestByRun_bitWork _ (fun a => MatrixBits (J a) B)
    (fun _ ha _ hb => determinantLERun_bounds hB ha hb) xs hJ

theorem selectInverseTraceRun_bitWork {α : Type*} {n B : ℕ} (hB : 0 < B)
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, MatrixBits (J a) B) :
    traceBitWork (arithmeticWidth (inverseTraceCompareOperations n) B)
      (selectInverseTraceRun J xs).2 ≤
      (xs.length-1)*inverseTraceCompareOperations n*
        (256*(arithmeticWidth (inverseTraceCompareOperations n) B+1)^3) :=
  bestByRun_bitWork _ (fun a => MatrixBits (J a) B)
    (fun _ ha _ hb => inverseTraceCostLERun_bounds hB hb ha) xs hJ

end DAGSpectral
