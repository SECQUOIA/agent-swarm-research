import Formal.ReciprocalAnchor.ManyOracleSize
import Formal.ReciprocalAnchor.ManyFastOperandSize
import Formal.ReciprocalAnchor.ManyBitCost

/-! Dense-cut operand bounds and a polynomial schoolbook bit-work model for the oracle. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

/-- Terms actually added when evaluating a dense affine cut. -/
def RationalAffineCut.evalTerms {n : ℕ} (C : RationalAffineCut n) (m t : ℚ)
    (q w : Fin n → ℚ) : List ℚ :=
  [C.offset, C.mean * m, C.reciprocal * t] ++
    List.ofFn (fun j => C.leafQ j * q j) ++ List.ofFn (fun j => C.leafW j * w j)

theorem RationalAffineCut.evalTerms_length {n : ℕ} (C : RationalAffineCut n) (m t : ℚ)
    (q w : Fin n → ℚ) : (C.evalTerms m t q w).length = 2 * n + 3 := by
  simp [evalTerms]
  omega

theorem RationalAffineCut.evalTerms_sum {n : ℕ} (C : RationalAffineCut n) (m t : ℚ)
    (q w : Fin n → ℚ) : (C.evalTerms m t q w).sum = C.eval m t q w := by
  simp [evalTerms, eval, List.sum_ofFn]
  ring

theorem RationalAffineCut.evalTerms_bits {n K B : ℕ} {C : RationalAffineCut n}
    {m t : ℚ} {q w : Fin n → ℚ} (hC : C.Bits K)
    (hm : RationalBits m B) (ht : RationalBits t B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B) :
    ∀ x ∈ C.evalTerms m t q w, RationalBits x (K + B) := by
  intro x hx
  simp only [evalTerms, List.mem_append, List.mem_cons, List.not_mem_nil, or_false,
    List.mem_ofFn] at hx
  rcases hx with ((rfl | rfl | rfl) | ⟨j, rfl⟩) | ⟨j, rfl⟩
  · exact rationalBits_mono hC.1 (by omega)
  · exact rationalBits_mul hC.2.1 hm
  · exact rationalBits_mul hC.2.2.1 ht
  · exact rationalBits_mul (hC.2.2.2.1 j) (hq j)
  · exact rationalBits_mul (hC.2.2.2.2 j) (hw j)

/-- Every partial dense-dot-product sum has controlled size, regardless of grouping. -/
theorem RationalAffineCut.eval_partial_bits {n K B : ℕ} {C : RationalAffineCut n}
    {m t : ℚ} {q w : Fin n → ℚ} (hC : C.Bits K)
    (hm : RationalBits m B) (ht : RationalBits t B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (xs : List ℚ) (hxs : xs.Sublist (C.evalTerms m t q w)) :
    RationalBits xs.sum (1 + (2 * n + 3) * (K + B + 1)) := by
  have hh : ∀ x ∈ xs, RationalBits x (K + B) :=
    fun x hx => C.evalTerms_bits hC hm ht hq hw x (hxs.subset hx)
  apply rationalBits_mono (rationalBits_list_sum hh)
  have hl := hxs.length_le
  rw [C.evalTerms_length] at hl
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hl) _

/-- A common width for envelope construction, coefficient extraction, and dense affine tests. -/
def oracleOperandBits (n B : ℕ) : ℕ :=
  (2 * n + 10) * (FastEnvelope.evaluatorBits n B + B + 10)

theorem oracleOperandBits_evaluator (n B : ℕ) :
    FastEnvelope.evaluatorBits n B ≤ oracleOperandBits n B := by
  unfold oracleOperandBits
  nlinarith

theorem oracleOperandBits_cut (n B : ℕ) :
    4 * B + 4 + (2 * n + 2) * (32 * B + 44) ≤ FastEnvelope.evaluatorBits n B := by
  unfold FastEnvelope.evaluatorBits
  nlinarith

theorem oracleOperandBits_eval (n B : ℕ) :
    1 + (2 * n + 3) * (FastEnvelope.evaluatorBits n B + B + 1) ≤ oracleOperandBits n B := by
  unfold oracleOperandBits
  nlinarith

/-- Every intermediate sum in evaluating any returned cut fits the oracle width. -/
theorem separationOracle_eval_partial_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ht : RationalBits t B)
    (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {C : RationalAffineCut n} (h : separationOracle a b m t q w = some C)
    (xs : List ℚ) (hxs : xs.Sublist (C.evalTerms m t q w)) :
    RationalBits xs.sum (oracleOperandBits n B) := by
  have hC := (separationOracle_bits hm ha hb hq hw h).mono (oracleOperandBits_cut n B)
  exact rationalBits_mono (C.eval_partial_bits hC hm ht hq hw xs hxs) (oracleOperandBits_eval n B)

/-- Every dense affine test in the finite scan fits the same width, including rejected tests. -/
theorem linearScan_eval_partial_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ht : RationalBits t B)
    (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {C : RationalAffineCut n} (hC : C ∈ linearCuts a b)
    (xs : List ℚ) (hxs : xs.Sublist (C.evalTerms m t q w)) :
    RationalBits xs.sum (oracleOperandBits n B) := by
  have hc := (linearCuts_bits ha hb hC).mono
    (show 2 * B + 2 ≤ FastEnvelope.evaluatorBits n B by
      have hh := FastEnvelope.evaluatorBits_lower n B
      omega)
  exact rationalBits_mono (C.eval_partial_bits hc hm ht hq hw xs hxs) (oracleOperandBits_eval n B)

/-- Every scalar intermediate in a produced interval coefficient fits the common width. -/
theorem fastCut_scalar_operand_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {s : FastEnvelope.Segment}
    (hs : s ∈ (FastEnvelope.buildSegments (FastEnvelope.sourceLines m q w) a b).1)
    {x : ℚ} (hx : x ∈ segmentFormTrace s.lo s.hi) :
    RationalBits x (oracleOperandBits n B) := by
  have hk := FastEnvelope.segments_knots (FastEnvelope.sourceLines m q w)
    (FastEnvelope.buildStack (FastEnvelope.sourceLines m q w)).1 a b a b
    (fun _ h => FastEnvelope.buildStack_members _ h) (Or.inl rfl) (Or.inr (Or.inl rfl)) hs
  have ht := segmentFormTrace_bits (hk.1.bits hm ha hb hq hw) (hk.2.bits hm ha hb hq hw) x hx
  apply rationalBits_mono ht
  apply le_trans _ (oracleOperandBits_evaluator n B)
  have he := FastEnvelope.evaluatorBits_lower n B
  omega

/-- Every partially accumulated coefficient tuple fits the common width. -/
theorem fastCut_partial_operand_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (ss : List FastEnvelope.Segment)
    (hss : ss.Sublist (FastEnvelope.buildSegments (FastEnvelope.sourceLines m q w) a b).1) :
    RationalAffineForm.Bits
      (((1 / a + a / a ^ 2, -(1 / a ^ 2), 0, 0) : RationalAffineForm n) +
        (ss.map fun s => segmentForm (FastEnvelope.sourceIndex m q w s.active) s.lo s.hi).sum)
      (oracleOperandBits n B) :=
  (FastEnvelope.fastCut_partial_bits hm ha hb hq hw ss hss).mono
    ((oracleOperandBits_cut n B).trans (oracleOperandBits_evaluator n B))

/-- Tangent coefficient construction also stays within the same width. -/
theorem tangent_scalar_operand_bits {n B : ℕ} {a : ℚ} (ha : RationalBits a B)
    {x : ℚ} (hx : x ∈ tangentFormTrace a) : RationalBits x (oracleOperandBits n B) := by
  apply rationalBits_mono (tangentFormTrace_bits ha x hx)
  apply le_trans _ (oracleOperandBits_evaluator n B)
  have he := FastEnvelope.evaluatorBits_lower n B
  omega

/-- A polynomial upper bound on the actual dispatch's arithmetic charge. -/
def oracleOperationBound (n : ℕ) : ℕ :=
  (4 * n + 7) * (6 * n + 3) + 10 * (n + 1) +
    ((2 * n + 2) * (2 * n + 39) + 40 * (2 * n + 3) + 10 * (2 * n + 2)) +
    ((2 * n + 2) * (2 * n + 39) + 8 * (2 * n + 2) ^ 2 +
      100 * (n + 1) * (2 * n + 3))

theorem separationOracle_charge_polynomial {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    separationOracleArithmeticCharge a b m t q w ≤ oracleOperationBound n := by
  apply (separationOracleArithmeticCharge_le a b m t q w).trans
  have hlog := Nat.log2_le_self (2 * n + 2)
  unfold oracleOperationBound
  nlinarith

/-- Schoolbook bit-work charged to the actual oracle dispatch. The operand families
are proved above and in `ManyFastOperandSize` and `ManyFastCutSize`.
This model does not assert a runtime refinement for Lean's compiled `Rat` backend. -/
def separationOracleBitWork {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) (B : ℕ) : ℕ :=
  BitCost.bitWorkBudget (separationOracleArithmeticCharge a b m t q w) (oracleOperandBits n B)

/-- Complete dispatch and cut production admit an explicit polynomial schoolbook budget. -/
theorem separationOracleBitWork_polynomial {n B : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    separationOracleBitWork a b m t q w B ≤
      oracleOperationBound n * (256 * (oracleOperandBits n B + 1) ^ 3) :=
  BitCost.bitWorkBudget_le (separationOracle_charge_polynomial a b m t q w) le_rfl

end ReciprocalAnchor.ManyLeaf
