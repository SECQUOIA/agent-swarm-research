import Formal.DAGSpectral.EigenCompare
import Formal.DAGSpectral.MatrixArithmeticTrace

namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

@[instance_reducible] def subsetOrder (n : ℕ) : LinearOrder (Finset (Fin n)) :=
  LinearOrder.lift' (fun s => s.sort (· ≤ ·)) (by
    intro s t h
    have hh := congrArg List.toFinset h
    simpa only [Finset.sort_toFinset] using hh)

def minorList (n k : ℕ) : List (Finset (Fin n)) :=
  letI := subsetOrder n
  (Finset.univ.powersetCard (n-k)).sort ((subsetOrder n).le)

theorem minorList_sum {n : ℕ} (k : ℕ) (f : Finset (Fin n) → ℚ) :
    ((minorList n k).map f).sum = ∑ s ∈ Finset.univ.powersetCard (n-k), f s := by
  let := subsetOrder n
  exact (List.sum_toFinset f (Finset.sort_nodup _ ((subsetOrder n).le))).symm.trans
    (by rw [Finset.sort_toFinset])

theorem minorList_length_le (n k : ℕ) : (minorList n k).length ≤ 2^n := by
  simp only [minorList, Finset.length_sort, Finset.card_powersetCard,
    Finset.card_univ, Fintype.card_fin]
  exact Nat.choose_le_two_pow n (n-k)

def minorExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (s : Finset (Fin n)) :
    ArithmeticExpr :=
  determinantExpr (A.submatrix (fun i => ((s.orderIsoOfFin rfl) i).val)
    (fun i => ((s.orderIsoOfFin rfl) i).val))

theorem minorExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (s : Finset (Fin n)) :
    (minorExpr A s).eval = (A.submatrix (Subtype.val : s → Fin n) Subtype.val).det := by
  rw [minorExpr, determinantExpr_eval]
  exact Matrix.det_submatrix_equiv_self (s.orderIsoOfFin rfl).toEquiv
    (A.submatrix (Subtype.val : s → Fin n) Subtype.val)

def coefficientExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (k : ℕ) : ArithmeticExpr :=
  if k ≤ n then .op .mul (.atom ((-1 : ℚ)^(n-k)))
    (sumExpr ((minorList n k).map (minorExpr A))) else .atom 0

theorem coefficientExpr_eval {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (k : ℕ) :
    (coefficientExpr A k).eval = rationalCharpolyCoeff A k := by
  simp only [coefficientExpr, rationalCharpolyCoeff]
  split_ifs
  · simp only [ArithmeticExpr.eval, primitiveResult, sumExpr_eval, List.map_map,
      Function.comp_def, minorExpr_eval, minorList_sum]
  · rfl

def coefficientOperations (n : ℕ) : ℕ := 2^n*(determinantOperations n+1)+1

theorem determinantOperations_mono {n m : ℕ} (h : n ≤ m) :
    determinantOperations n ≤ determinantOperations m := by
  exact Nat.mul_le_mul (Nat.factorial_le h) (by omega)

theorem coefficientExpr_operations_le {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (k : ℕ) :
    (coefficientExpr A k).operations ≤ coefficientOperations n := by
  unfold coefficientExpr
  split_ifs
  · simp only [ArithmeticExpr.operations, Nat.zero_add, sumExpr_operations, List.map_map,
      Function.comp_def, List.length_map]
    have hs : (((minorList n k).map (fun s => (minorExpr A s).operations)).sum) ≤
        (minorList n k).length * determinantOperations n := by
      induction minorList n k with
      | nil => simp
      | cons s ss ih =>
        have hm : (minorExpr A s).operations ≤ determinantOperations n := by
          simp only [minorExpr, determinantExpr_operations]
          exact determinantOperations_mono (by simpa using Finset.card_le_univ s)
        simp only [List.map_cons, List.sum_cons, List.length_cons]
        nlinarith
    have hl := minorList_length_le n k
    unfold coefficientOperations
    nlinarith
  · simp [ArithmeticExpr.operations]

theorem coefficientExpr_leaves {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) (k : ℕ) :
    (coefficientExpr A k).leavesBounded B := by
  unfold coefficientExpr
  split_ifs
  · constructor
    · rcases neg_one_pow_eq_or ℚ (n-k) with h | h
      · simpa [ArithmeticExpr.leavesBounded, h] using rationalBits_mono rationalBits_one hB
      · simpa [ArithmeticExpr.leavesBounded, h] using
          rationalBits_mono (rationalBits_neg rationalBits_one) hB
    · apply sumExpr_leaves hB
      intro e he
      obtain ⟨s, _, rfl⟩ := List.mem_map.mp he
      exact determinantExpr_leaves hB (fun i j => hA _ _)
  · exact rationalBits_mono rationalBits_zero hB

/-- Compute all coefficients and concatenate exactly the emitted primitive events. -/
def charpolyCoefficientsWithTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    List ℚ × List ArithmeticEvent :=
  let runs := List.ofFn fun k : Fin (n+1) => (coefficientExpr A k).run
  (runs.map Prod.fst, (runs.map Prod.snd).flatten)

theorem charpolyCoefficientsWithTrace_values {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (charpolyCoefficientsWithTrace A).1 =
      List.ofFn (fun k : Fin (n+1) => rationalCharpolyCoeff A k) := by
  simp only [charpolyCoefficientsWithTrace, List.map_ofFn, Function.comp_def,
    ArithmeticExpr.run_eq, coefficientExpr_eval]

theorem charpolyCoefficientsWithTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (charpolyCoefficientsWithTrace A).2.length ≤ (n+1)*coefficientOperations n := by
  simp only [charpolyCoefficientsWithTrace, List.map_ofFn, List.length_flatten,
    Function.comp_def, ArithmeticExpr.run_eq, ArithmeticExpr.trace_length, List.sum_ofFn]
  simpa using Finset.sum_le_sum (s := Finset.univ)
    (fun (i : Fin (n+1)) _ => coefficientExpr_operations_le A i)

theorem charpolyCoefficientsWithTrace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    ∀ e ∈ (charpolyCoefficientsWithTrace A).2,
      eventBits (arithmeticWidth (coefficientOperations n) B) e := by
  intro e he
  simp only [charpolyCoefficientsWithTrace, List.map_ofFn, Function.comp_def,
    ArithmeticExpr.run_eq] at he
  obtain ⟨t, ht, he⟩ := List.mem_flatten.mp he
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp ht
  exact eventBits_mono (((coefficientExpr A i).eval_trace_bits
    (coefficientExpr_leaves hB hA i)).2 e he)
    (arithmeticWidth_mono (coefficientExpr_operations_le A i))

theorem charpolyCoefficientsWithTrace_value_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    ∀ q ∈ (charpolyCoefficientsWithTrace A).1,
      RationalBits q (arithmeticWidth (coefficientOperations n) B) := by
  intro q hq
  rw [charpolyCoefficientsWithTrace_values] at hq
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hq
  rw [← coefficientExpr_eval]
  exact rationalBits_mono ((coefficientExpr A i).eval_trace_bits
    (coefficientExpr_leaves hB hA i)).1
    (arithmeticWidth_mono (coefficientExpr_operations_le A i))

def negateEntryExpr {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    ArithmeticExpr := .op .neg (.atom (A i j)) (.atom 0)

/-- The finite coefficient-sign PSD test, including entry negation and comparisons. -/
def rationalPSDTestWithTrace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Bool × List ArithmeticEvent :=
  let r := charpolyCoefficientsWithTrace (-A)
  (r.1.all (fun q => decide (0 ≤ q)),
    matrixExprTrace (negateEntryExpr A) ++ r.2 ++ r.1.map (fun q => (.compare, 0, q)))

theorem rationalPSDTestWithTrace_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalPSDTestWithTrace A).1 = rationalPSDTest A := by
  simp only [rationalPSDTestWithTrace, charpolyCoefficientsWithTrace_values, rationalPSDTest]
  apply Bool.eq_iff_iff.mpr
  simp only [List.all_eq_true, List.mem_ofFn, List.mem_range, decide_eq_true_eq]
  constructor
  · intro h k hk
    exact h _ ⟨⟨k, hk⟩, rfl⟩
  · intro h q hq
    obtain ⟨i, rfl⟩ := hq
    exact h i i.isLt

/-- A dimension-only scalar operation bound; every coefficient is evaluated. -/
def psdTestOperations (n : ℕ) : ℕ := n*n + (n+1)*(coefficientOperations n+1)

theorem rationalPSDTestWithTrace_length {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalPSDTestWithTrace A).2.length ≤ psdTestOperations n := by
  have hn : (matrixExprTrace (negateEntryExpr A)).length = n*n*1 :=
    matrixExprTrace_length _ (fun _ _ => rfl)
  have hc := charpolyCoefficientsWithTrace_length (-A)
  simp only [rationalPSDTestWithTrace, List.length_append, List.length_map,
    charpolyCoefficientsWithTrace_values, List.length_ofFn, hn]
  unfold psdTestOperations
  nlinarith

theorem rationalPSDTestWithTrace_bits {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A B) :
    ∀ e ∈ (rationalPSDTestWithTrace A).2,
      eventBits (arithmeticWidth (coefficientOperations n) B) e := by
  have hneg : MatrixBits (-A) B := fun i j => rationalBits_neg (hA i j)
  have hwidth : B ≤ arithmeticWidth (coefficientOperations n) B := by
    simpa only [arithmeticWidth_zero] using arithmeticWidth_mono (B := B)
      (Nat.zero_le (coefficientOperations n))
  have hz : RationalBits 0 (arithmeticWidth (coefficientOperations n) B) :=
    rationalBits_mono rationalBits_zero (by omega)
  intro e he
  simp only [rationalPSDTestWithTrace, List.mem_append] at he
  rcases he with (he | he) | he
  · have ht := matrixExprTrace_bits (negateEntryExpr A) (N := 1)
      (fun _ _ => rfl) (fun i j => ⟨hA i j, rationalBits_mono rationalBits_zero hB⟩) e he
    exact eventBits_mono ht (arithmeticWidth_mono (by unfold coefficientOperations; omega))
  · exact charpolyCoefficientsWithTrace_bits hB hneg e he
  · obtain ⟨q, hq, rfl⟩ := List.mem_map.mp he
    exact ⟨hz, charpolyCoefficientsWithTrace_value_bits hB hneg q hq⟩

end DAGSpectral
