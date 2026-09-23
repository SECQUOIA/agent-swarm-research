import Formal.DAGSpectral.RationalMatrixArithmetic

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost Matrix

/-- A rational expression records its actual operands when evaluated. -/
inductive ArithmeticExpr where
  | atom (q : ℚ)
  | op (p : RationalPrimitive) (left right : ArithmeticExpr)

def ArithmeticExpr.eval : ArithmeticExpr → ℚ
  | .atom q => q
  | .op p l r => primitiveResult p l.eval r.eval

def ArithmeticExpr.trace : ArithmeticExpr → List ArithmeticEvent
  | .atom _ => []
  | .op p l r => l.trace ++ r.trace ++ [(p, l.eval, r.eval)]

/-- Executable evaluation returns the result and the primitive events together;
child values are computed once and reused. -/
def ArithmeticExpr.run : ArithmeticExpr → ℚ × List ArithmeticEvent
  | .atom q => (q, [])
  | .op p l r =>
    let lv := l.run
    let rv := r.run
    (primitiveResult p lv.1 rv.1, lv.2 ++ rv.2 ++ [(p, lv.1, rv.1)])

theorem ArithmeticExpr.run_eq (e : ArithmeticExpr) : e.run = (e.eval, e.trace) := by
  induction e with
  | atom q => rfl
  | op p l r hl hr => simp only [run, hl, hr, eval, trace]

def ArithmeticExpr.operations : ArithmeticExpr → ℕ
  | .atom _ => 0
  | .op _ l r => l.operations + r.operations + 1

def ArithmeticExpr.leavesBounded (B : ℕ) : ArithmeticExpr → Prop
  | .atom q => RationalBits q B
  | .op _ l r => l.leavesBounded B ∧ r.leavesBounded B

@[simp] theorem ArithmeticExpr.trace_length (e : ArithmeticExpr) :
    e.trace.length = e.operations := by
  induction e with
  | atom q => rfl
  | op p l r hl hr => simp [trace, operations, hl, hr, Nat.add_assoc]

theorem arithmeticWidth_mono {d e B : ℕ} (h : d ≤ e) :
    arithmeticWidth d B ≤ arithmeticWidth e B := by
  induction h with
  | refl => rfl
  | @step e h ih => rw [arithmeticWidth_step]; omega

theorem eventBits_mono {B C : ℕ} {e : ArithmeticEvent} (h : eventBits B e) (hBC : B ≤ C) :
    eventBits C e := ⟨rationalBits_mono h.1 hBC, rationalBits_mono h.2 hBC⟩

theorem ArithmeticExpr.eval_trace_bits (e : ArithmeticExpr) {B : ℕ}
    (h : e.leavesBounded B) :
    RationalBits e.eval (arithmeticWidth e.operations B) ∧
      ∀ v ∈ e.trace, eventBits (arithmeticWidth e.operations B) v := by
  induction e with
  | atom q => simpa [eval, trace, operations, arithmeticWidth_zero, leavesBounded] using h
  | op p l r hl hr =>
    obtain ⟨hlv, hlt⟩ := hl h.1
    obtain ⟨hrv, hrt⟩ := hr h.2
    have hll : arithmeticWidth l.operations B ≤ arithmeticWidth (l.operations+r.operations) B :=
      arithmeticWidth_mono (by omega)
    have hrr : arithmeticWidth r.operations B ≤ arithmeticWidth (l.operations+r.operations) B :=
      arithmeticWidth_mono (by omega)
    have hlv' := rationalBits_mono hlv hll
    have hrv' := rationalBits_mono hrv hrr
    have hstep : arithmeticWidth (l.operations+r.operations) B ≤
        arithmeticWidth (l.operations+r.operations+1) B := arithmeticWidth_mono (by omega)
    constructor
    · simpa only [eval, operations, arithmeticWidth_step] using primitiveResult_bits hlv' hrv' p
    · intro v hv
      simp only [trace, List.mem_append, List.mem_singleton] at hv
      rcases hv with (hv | hv) | rfl
      · exact eventBits_mono (hlt _ hv) (hll.trans hstep)
      · exact eventBits_mono (hrt _ hv) (hrr.trans hstep)
      · exact ⟨rationalBits_mono hlv' hstep, rationalBits_mono hrv' hstep⟩

theorem ArithmeticExpr.bitWork_le (e : ArithmeticExpr) {B : ℕ}
    (h : e.leavesBounded B) :
    traceBitWork (arithmeticWidth e.operations B) e.trace ≤
      e.operations * (256 * (arithmeticWidth e.operations B+1)^3) := by
  simpa using traceBitWork_le (e.eval_trace_bits h).2

def sumExpr : List ArithmeticExpr → ArithmeticExpr
  | [] => .atom 0
  | e :: es => .op .add e (sumExpr es)

def prodExpr : List ArithmeticExpr → ArithmeticExpr
  | [] => .atom 1
  | e :: es => .op .mul e (prodExpr es)

@[simp] theorem sumExpr_eval (es : List ArithmeticExpr) :
    (sumExpr es).eval = (es.map ArithmeticExpr.eval).sum := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [sumExpr, ArithmeticExpr.eval, primitiveResult, ih]

@[simp] theorem prodExpr_eval (es : List ArithmeticExpr) :
    (prodExpr es).eval = (es.map ArithmeticExpr.eval).prod := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [prodExpr, ArithmeticExpr.eval, primitiveResult, ih]

theorem sumExpr_operations (es : List ArithmeticExpr) :
    (sumExpr es).operations = (es.map ArithmeticExpr.operations).sum + es.length := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [sumExpr, ArithmeticExpr.operations, ih]; omega

theorem prodExpr_operations (es : List ArithmeticExpr) :
    (prodExpr es).operations = (es.map ArithmeticExpr.operations).sum + es.length := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [prodExpr, ArithmeticExpr.operations, ih]; omega

theorem sumExpr_leaves {B : ℕ} (hB : 0 < B) (es : List ArithmeticExpr)
    (h : ∀ e ∈ es, e.leavesBounded B) : (sumExpr es).leavesBounded B := by
  induction es with
  | nil => exact rationalBits_mono rationalBits_zero hB
  | cons e es ih => exact ⟨h e (by simp), ih (fun z hz => h z (by simp [hz]))⟩

theorem prodExpr_leaves {B : ℕ} (hB : 0 < B) (es : List ArithmeticExpr)
    (h : ∀ e ∈ es, e.leavesBounded B) : (prodExpr es).leavesBounded B := by
  induction es with
  | nil => exact rationalBits_mono rationalBits_one hB
  | cons e es ih => exact ⟨h e (by simp), ih (fun z hz => h z (by simp [hz]))⟩

/-- Permutations are enumerated in lexicographic order of their coordinate lists. -/
@[instance_reducible] def permutationOrder (n : ℕ) : LinearOrder (Equiv.Perm (Fin n)) :=
  LinearOrder.lift' (fun σ => List.ofFn (σ : Fin n → Fin n)) (by
    intro σ τ h
    exact Equiv.ext (congrFun (List.ofFn_injective h)))

def permutationList (n : ℕ) : List (Equiv.Perm (Fin n)) :=
  letI := permutationOrder n
  Finset.univ.sort (· ≤ ·)

theorem permutationList_sum {n : ℕ} (f : Equiv.Perm (Fin n) → ℚ) :
    ((permutationList n).map f).sum = ∑ σ, f σ := by
  let := permutationOrder n
  exact (List.sum_toFinset f (Finset.sort_nodup _ _)).symm.trans
    (by rw [Finset.sort_toFinset])

@[simp] theorem permutationList_length (n : ℕ) :
    (permutationList n).length = n.factorial := by
  simp [permutationList, Finset.length_sort, Fintype.card_perm]

def determinantExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ArithmeticExpr :=
  sumExpr ((permutationList n).map fun σ =>
    .op .mul (.atom ((Equiv.Perm.sign σ : ℤ) : ℚ))
      (prodExpr (List.ofFn fun i => .atom (A (σ i) i))))

theorem determinantExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (determinantExpr A).eval = A.det := by
  simp only [determinantExpr, sumExpr_eval, List.map_map, Function.comp_def,
    ArithmeticExpr.eval, primitiveResult, prodExpr_eval, List.map_ofFn, List.prod_ofFn]
  exact (permutationList_sum _).trans (Matrix.det_apply' A).symm

def determinantOperations (n : ℕ) : ℕ := n.factorial*(n+2)

@[simp] theorem determinantExpr_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (determinantExpr A).operations = determinantOperations n := by
  simp [determinantExpr, sumExpr_operations, prodExpr_operations,
    ArithmeticExpr.operations, List.map_map, Function.comp_def, List.map_ofFn,
    determinantOperations]
  ring

theorem determinantExpr_leaves {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    (determinantExpr A).leavesBounded B := by
  apply sumExpr_leaves hB
  intro e he
  obtain ⟨σ, _, rfl⟩ := List.mem_map.mp he
  constructor
  · rcases Int.units_eq_one_or (Equiv.Perm.sign σ) with hs | hs
    · simpa [hs, ArithmeticExpr.leavesBounded] using rationalBits_mono rationalBits_one hB
    · simpa [hs, ArithmeticExpr.leavesBounded] using
        rationalBits_mono (rationalBits_neg rationalBits_one) hB
  · apply prodExpr_leaves hB
    intro e he
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp he
    exact hA _ _

def inverseEntryExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    ArithmeticExpr :=
  .op .mul (.op .inv (determinantExpr A) (.atom 0))
    (determinantExpr (A.updateRow j (Pi.single i 1)))

@[simp] theorem inverseEntryExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (i j : Fin n) : (inverseEntryExpr A i j).eval = rationalMatrixInverse A i j := by
  simp [inverseEntryExpr, ArithmeticExpr.eval, primitiveResult, determinantExpr_eval,
    rationalMatrixInverse, Matrix.adjugate_apply]

@[simp] theorem inverseEntryExpr_operations {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (i j : Fin n) : (inverseEntryExpr A i j).operations = 2*determinantOperations n+2 := by
  simp [inverseEntryExpr, ArithmeticExpr.operations]
  omega

theorem inverseEntryExpr_leaves {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (i j : Fin n) :
    (inverseEntryExpr A i j).leavesBounded B := by
  refine ⟨⟨determinantExpr_leaves hB hA, rationalBits_mono rationalBits_zero hB⟩, ?_⟩
  apply determinantExpr_leaves hB
  intro k l
  by_cases hk : k=j
  · subst k
    simp only [Matrix.updateRow_self, Pi.single_apply]
    split_ifs
    · exact rationalBits_mono rationalBits_one hB
    · exact rationalBits_mono rationalBits_zero hB
  · simpa only [Matrix.updateRow_ne hk] using hA k l

def matrixMulEntryExpr {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (D : Matrix (Fin n) (Fin m) ℚ) (i : Fin l) (j : Fin m) : ArithmeticExpr :=
  sumExpr (List.ofFn fun k => .op .mul (.atom (A i k)) (.atom (D k j)))

@[simp] theorem matrixMulEntryExpr_eval {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (D : Matrix (Fin n) (Fin m) ℚ) (i : Fin l) (j : Fin m) :
    (matrixMulEntryExpr A D i j).eval = (A*D) i j := by
  simp [matrixMulEntryExpr, ArithmeticExpr.eval, primitiveResult, Matrix.mul_apply,
    Function.comp_def, List.sum_ofFn]

@[simp] theorem matrixMulEntryExpr_operations {l n m : ℕ}
    (A : Matrix (Fin l) (Fin n) ℚ) (D : Matrix (Fin n) (Fin m) ℚ)
    (i : Fin l) (j : Fin m) : (matrixMulEntryExpr A D i j).operations = 2*n := by
  simp [matrixMulEntryExpr, sumExpr_operations, List.map_ofFn, ArithmeticExpr.operations,
    Function.comp_def]
  omega

theorem matrixMulEntryExpr_leaves {l n m B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin l) (Fin n) ℚ} {D : Matrix (Fin n) (Fin m) ℚ}
    (hA : MatrixBits A B) (hD : MatrixBits D B) (i : Fin l) (j : Fin m) :
    (matrixMulEntryExpr A D i j).leavesBounded B := by
  apply sumExpr_leaves hB
  intro e he
  obtain ⟨k, rfl⟩ := List.mem_ofFn.mp he
  exact ⟨hA _ _, hD _ _⟩

/-- Row-major execution, retaining every scalar arithmetic event. -/
def matrixExprTrace {l m : ℕ} (E : Fin l → Fin m → ArithmeticExpr) : List ArithmeticEvent :=
  (List.ofFn fun i => (List.ofFn fun j => (E i j).trace).flatten).flatten

theorem matrixExprTrace_length {l m N : ℕ} (E : Fin l → Fin m → ArithmeticExpr)
    (hN : ∀ i j, (E i j).operations = N) : (matrixExprTrace E).length = l*m*N := by
  simp [matrixExprTrace, List.length_flatten, List.map_ofFn, hN, List.sum_ofFn]
  ring

theorem matrixExprTrace_bits {l m N B : ℕ} (E : Fin l → Fin m → ArithmeticExpr)
    (hN : ∀ i j, (E i j).operations = N) (hB : ∀ i j, (E i j).leavesBounded B) :
    ∀ e ∈ matrixExprTrace E, eventBits (arithmeticWidth N B) e := by
  intro e he
  obtain ⟨row, hrow, he⟩ := List.mem_flatten.mp he
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hrow
  obtain ⟨col, hcol, he⟩ := List.mem_flatten.mp he
  obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hcol
  simpa only [hN i j] using ((E i j).eval_trace_bits (hB i j)).2 e he

def matrixMulTrace {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (D : Matrix (Fin n) (Fin m) ℚ) : List ArithmeticEvent :=
  matrixExprTrace (matrixMulEntryExpr A D)

def matrixInverseTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : List ArithmeticEvent :=
  matrixExprTrace (inverseEntryExpr A)

@[simp] theorem matrixMulTrace_length {l n m : ℕ} (A : Matrix (Fin l) (Fin n) ℚ)
    (D : Matrix (Fin n) (Fin m) ℚ) : (matrixMulTrace A D).length = l*m*(2*n) :=
  matrixExprTrace_length _ (matrixMulEntryExpr_operations A D)

@[simp] theorem matrixInverseTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (matrixInverseTrace A).length = n*n*(2*determinantOperations n+2) :=
  matrixExprTrace_length _ (inverseEntryExpr_operations A)

theorem matrixMulTrace_bits {l n m B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin l) (Fin n) ℚ} {D : Matrix (Fin n) (Fin m) ℚ}
    (hA : MatrixBits A B) (hD : MatrixBits D B) :
    ∀ e ∈ matrixMulTrace A D, eventBits (arithmeticWidth (2*n) B) e :=
  matrixExprTrace_bits _ (matrixMulEntryExpr_operations A D)
    (matrixMulEntryExpr_leaves hB hA hD)

theorem matrixInverseTrace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    ∀ e ∈ matrixInverseTrace A,
      eventBits (arithmeticWidth (2*determinantOperations n+2) B) e :=
  matrixExprTrace_bits _ (inverseEntryExpr_operations A) (inverseEntryExpr_leaves hB hA)

end DAGSpectral
