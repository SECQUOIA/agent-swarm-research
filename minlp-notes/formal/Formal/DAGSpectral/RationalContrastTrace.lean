import Formal.DAGSpectral.RationalPseudoinverseTrace

namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- A dot-product circuit with exactly one multiplication and addition per coordinate. -/
def dotExpr {n : ℕ} (x y : Fin n → ℚ) : ArithmeticExpr :=
  sumExpr (List.ofFn fun i => .op .mul (.atom (x i)) (.atom (y i)))

@[simp] theorem dotExpr_eval {n : ℕ} (x y : Fin n → ℚ) :
    (dotExpr x y).eval = x ⬝ᵥ y := by
  simp [dotExpr, ArithmeticExpr.eval, primitiveResult, Function.comp_def, List.sum_ofFn, dotProduct]

@[simp] theorem dotExpr_operations {n : ℕ} (x y : Fin n → ℚ) :
    (dotExpr x y).operations = 2*n := by
  simp [dotExpr, sumExpr_operations, List.map_ofFn, Function.comp_def, ArithmeticExpr.operations]
  omega

theorem dotExpr_leaves {n B : ℕ} (hB : 0 < B) {x y : Fin n → ℚ}
    (hx : ∀ i, RationalBits (x i) B) (hy : ∀ i, RationalBits (y i) B) :
    (dotExpr x y).leavesBounded B := by
  apply sumExpr_leaves hB
  intro e he
  obtain ⟨i,rfl⟩ := List.mem_ofFn.mp he
  exact ⟨hx i,hy i⟩

def vectorTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    List ArithmeticEvent := (List.ofFn fun i => (dotExpr (A i) x).trace).flatten

@[simp] theorem vectorTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    (vectorTrace A x).length = n*(2*n) := by
  simp [vectorTrace, List.length_flatten, List.map_ofFn, Function.comp_def]

theorem vector_eval_trace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {x : Fin n → ℚ}
    (hA : MatrixBits A B) (hx : ∀ i, RationalBits (x i) B) :
    (∀ i, RationalBits ((A *ᵥ x) i) (arithmeticWidth (2*n) B)) ∧
      ∀ e ∈ vectorTrace A x, eventBits (arithmeticWidth (2*n) B) e := by
  have h (i : Fin n) := (dotExpr (A i) x).eval_trace_bits (dotExpr_leaves hB (hA i) hx)
  simp only [dotExpr_eval, dotExpr_operations] at h
  refine ⟨fun i => (h i).1, ?_⟩
  intro e he
  obtain ⟨t,ht,he⟩ := List.mem_flatten.mp he
  obtain ⟨i,rfl⟩ := List.mem_ofFn.mp ht
  exact (h i).2 e he

/-- Execute and store every dot-product run, then project values and events. -/
def vectorRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    (Fin n → ℚ) × List ArithmeticEvent :=
  let runs := Vector.ofFn fun i : Fin n => (dotExpr (A i) x).run
  (fun i => (runs.get i).1, runs.toList.flatMap Prod.snd)

theorem vectorRun_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    vectorRun A x = (A *ᵥ x, vectorTrace A x) := by
  apply Prod.ext
  · funext i
    simp [vectorRun, ArithmeticExpr.run_eq, Matrix.mulVec]
  · simp only [vectorRun, Vector.toList_ofFn, List.flatMap,
      List.map_ofFn, Function.comp_def, ArithmeticExpr.run_eq, vectorTrace]

/-- Equality is decided from two executed ordered comparisons per coordinate. -/
def vectorEqualityRun {n : ℕ} (x y : Fin n → ℚ) : Bool × List ArithmeticEvent :=
  let runs := Vector.ofFn fun i : Fin n =>
    (decide (x i ≤ y i) && decide (y i ≤ x i),
      [(.compare,x i,y i),(.compare,y i,x i)])
  (runs.toList.all Prod.fst, runs.toList.flatMap Prod.snd)

theorem vectorEqualityRun_eq {n : ℕ} (x y : Fin n → ℚ) :
    vectorEqualityRun x y = (decide (x=y),
      (List.ofFn fun i => [(.compare,x i,y i),(.compare,y i,x i)]).flatten) := by
  apply Prod.ext
  · apply Bool.eq_iff_iff.mpr
    simp only [vectorEqualityRun, Vector.toList_ofFn, List.all_eq_true,
      List.forall_mem_ofFn_iff, Bool.and_eq_true, decide_eq_true_eq]
    constructor
    · intro h
      funext i
      exact le_antisymm (h i).1 (h i).2
    · intro h i
      simp [h]
  · simp only [vectorEqualityRun, Vector.toList_ofFn, List.flatMap,
      List.map_ofFn, Function.comp_def]

/-- Reuse the computed Moore–Penrose matrix for the variance and range test. -/
def rationalContrastWithTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    (Bool × ℚ) × List ArithmeticEvent :=
  let g := rationalPseudoInverseWithTrace A
  let y := vectorRun g.1 c
  let x := vectorRun A y.1
  let value := (dotExpr c y.1).run
  let eq := vectorEqualityRun x.1 c
  ((eq.1, value.1), g.2 ++ y.2 ++ x.2 ++ value.2 ++ eq.2)

theorem rationalContrastWithTrace_eq {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    rationalContrastWithTrace A c =
      ((rationalEstimable A c,rationalContrastVariance A c),
        (rationalPseudoInverseWithTrace A).2 ++ vectorTrace (rationalPseudoInverse A) c ++
          vectorTrace A (rationalPseudoInverse A *ᵥ c) ++
          (dotExpr c (rationalPseudoInverse A *ᵥ c)).trace ++
          (List.ofFn fun i => [(.compare,(A *ᵥ (rationalPseudoInverse A *ᵥ c)) i,c i),
            (.compare,c i,(A *ᵥ (rationalPseudoInverse A *ᵥ c)) i)]).flatten) := by
  simp only [rationalContrastWithTrace, rationalPseudoInverseWithTrace_value,
    vectorRun_eq, vectorEqualityRun_eq, ArithmeticExpr.run_eq, dotExpr_eval,
    rationalEstimable, rationalContrastVariance]

@[simp] theorem rationalContrastWithTrace_value {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    (rationalContrastWithTrace A c).1 = (rationalEstimable A c,rationalContrastVariance A c) := by
  rw [rationalContrastWithTrace_eq]

def contrastOperations (n : ℕ) : ℕ := pseudoInverseOperations n+4*n*n+4*n

theorem rationalContrastWithTrace_length {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    (rationalContrastWithTrace A c).2.length ≤ contrastOperations n := by
  have hp := rationalPseudoInverseWithTrace_length A
  simp only [rationalContrastWithTrace_eq, List.length_append, vectorTrace_length,
    ArithmeticExpr.trace_length, dotExpr_operations, List.length_flatten, List.map_ofFn,
    Function.comp_def, List.length_cons, List.length_nil, Nat.zero_add]
  simp only [List.ofFn_const, List.sum_replicate, nsmul_eq_mul]
  unfold contrastOperations
  nlinarith

/-- At fixed dimension this is linear in the common input bit bound. -/
def contrastTraceBits (n B : ℕ) : ℕ :=
  arithmeticWidth (2*n) (arithmeticWidth (2*n)
    (arithmeticWidth (pseudoInverseTraceDepth n) B+B+1))

theorem arithmeticWidth_ge (d B : ℕ) : B ≤ arithmeticWidth d B := by
  simpa only [arithmeticWidth_zero] using arithmeticWidth_mono (B := B) (Nat.zero_le d)

theorem rationalContrastWithTrace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {c : Fin n → ℚ}
    (hA : MatrixBits A B) (hc : ∀ i, RationalBits (c i) B) :
    (RationalBits (rationalContrastVariance A c) (contrastTraceBits n B)) ∧
      ∀ e ∈ (rationalContrastWithTrace A c).2, eventBits (contrastTraceBits n B) e := by
  let W := arithmeticWidth (pseudoInverseTraceDepth n) B
  let H := W+B+1
  let H1 := arithmeticWidth (2*n) H
  let H2 := arithmeticWidth (2*n) H1
  have hH : 0 < H := by dsimp [H]; omega
  have hHH1 : H ≤ H1 := arithmeticWidth_ge _ _
  have hH1H2 : H1 ≤ H2 := arithmeticWidth_ge _ _
  have hBH : B ≤ H := by dsimp [H]; omega
  have hWH : W ≤ H := by dsimp [H]; omega
  have hAH : MatrixBits A H := fun i j => rationalBits_mono (hA i j) hBH
  have hcH : ∀ i, RationalBits (c i) H := fun i => rationalBits_mono (hc i) hBH
  have hGH : MatrixBits (rationalPseudoInverse A) H := fun i j =>
    rationalBits_mono (rationalPseudoInverse_bits hB hA i j) hWH
  let y := rationalPseudoInverse A *ᵥ c
  have hy := vector_eval_trace_bits hH hGH hcH
  have hAH1 : MatrixBits A H1 := fun i j => rationalBits_mono (hAH i j) hHH1
  have hcH1 : ∀ i, RationalBits (c i) H1 := fun i => rationalBits_mono (hcH i) hHH1
  have hx := vector_eval_trace_bits (show 0 < H1 by omega) hAH1 hy.1
  have hd := (dotExpr c y).eval_trace_bits (dotExpr_leaves (show 0 < H1 by omega) hcH1 hy.1)
  simp only [dotExpr_operations,dotExpr_eval] at hd
  refine ⟨hd.1, ?_⟩
  intro e he
  simp only [rationalContrastWithTrace_eq, List.mem_append] at he
  rcases he with (((he | he) | he) | he) | he
  · exact eventBits_mono (rationalPseudoInverseWithTrace_bits hB hA e he)
      ((hWH.trans hHH1).trans hH1H2)
  · exact eventBits_mono (hy.2 e he) hH1H2
  · exact hx.2 e he
  · exact hd.2 e he
  · obtain ⟨t,ht,he⟩ := List.mem_flatten.mp he
    obtain ⟨i,rfl⟩ := List.mem_ofFn.mp ht
    have hcH2 := rationalBits_mono (hcH1 i) hH1H2
    simp only [List.mem_cons,List.not_mem_nil,or_false] at he
    rcases he with rfl | rfl
    · exact ⟨hx.1 i,hcH2⟩
    · exact ⟨hcH2,hx.1 i⟩

theorem rationalContrastWithTrace_bitWork {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {c : Fin n → ℚ}
    (hA : MatrixBits A B) (hc : ∀ i, RationalBits (c i) B) :
    traceBitWork (contrastTraceBits n B) (rationalContrastWithTrace A c).2 ≤
      contrastOperations n*(256*(contrastTraceBits n B+1)^3) :=
  (traceBitWork_le (rationalContrastWithTrace_bits hB hA hc).2).trans
    (Nat.mul_le_mul_right _ (rationalContrastWithTrace_length A c))

end DAGSpectral
