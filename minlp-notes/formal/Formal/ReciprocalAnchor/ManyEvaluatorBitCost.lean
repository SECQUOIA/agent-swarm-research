import Formal.ReciprocalAnchor.ManyBitCost

/-! Composition of the actual envelope evaluator's arithmetic charge and its
operand-family size proofs in the stated schoolbook bit-cost model. -/
namespace ReciprocalAnchor.ManyLeaf.BitCost
open FastEnvelope

/-- This family overapproximates all rational operands of the implemented evaluator.
It enumerates the implementation's arithmetic formulas, rather than claiming an
operational trace extracted from Lean's runtime. -/
inductive EvaluatorOperand {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : ℚ → Prop
  | original {x : ℚ} (hx : x = a ∨ x = b ∨ x = m) : EvaluatorOperand a b m q w x
  | constant {x : ℚ} (hx : x ∈ ([0, 1, 2] : List ℚ)) : EvaluatorOperand a b m q w x
  | leaf (j : Fin n) {x : ℚ} (hx : x ∈ inputTrace m (q j) (w j)) :
      EvaluatorOperand a b m q w x
  | setup {x : ℚ} (hx : x ∈ setupTrace a m) : EvaluatorOperand a b m q w x
  | coefficient {u : Line} (hu : u ∈ sourceLines m q w) {x : ℚ}
      (hx : x = u.intercept ∨ x = u.slope) : EvaluatorOperand a b m q w x
  | intersection {u v : Line} (hu : u ∈ sourceLines m q w) (hv : v ∈ sourceLines m q w)
      {x : ℚ} (hx : x ∈ crossTrace u v) : EvaluatorOperand a b m q w x
  | redundancy {u v z : Line} (hu : u ∈ sourceLines m q w)
      (hv : v ∈ sourceLines m q w) (hz : z ∈ sourceLines m q w)
      {x : ℚ} (hx : x ∈ redundantTrace u v z) : EvaluatorOperand a b m q w x
  | segment {s : Segment} (hs : s ∈ (buildSegments (sourceLines m q w) a b).1)
      {x : ℚ} (hx : x ∈ s.arithmeticTrace) : EvaluatorOperand a b m q w x
  | accumulation (ss : List Segment)
      (hss : ss.Sublist (buildSegments (sourceLines m q w) a b).1) :
      EvaluatorOperand a b m q w (ss.map Segment.integral).sum
  | result : EvaluatorOperand a b m q w (fastLowerMoment a b m q w)

/-- Every member of every arithmetic family is bounded from the original input sizes. -/
theorem evaluatorOperand_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {x : ℚ} (hx : EvaluatorOperand a b m q w x) : RationalBits x (evaluatorBits n B) := by
  have hB : B ≤ evaluatorBits n B := by
    change B ≤ FastEnvelope.evaluatorBits n B
    have := evaluatorBits_lower n B
    omega
  have htwo : 2 ≤ evaluatorBits n B := by
    change 2 ≤ FastEnvelope.evaluatorBits n B
    have := evaluatorBits_lower n B
    omega
  cases hx with
  | original he =>
    rcases he with rfl | rfl | rfl
    · exact rationalBits_mono ha hB
    · exact rationalBits_mono hb hB
    · exact rationalBits_mono hm hB
  | constant he =>
    simp only [List.mem_cons, List.not_mem_nil, or_false] at he
    rcases he with rfl | rfl | rfl
    · exact rationalBits_mono rationalBits_zero (by omega)
    · exact rationalBits_mono rationalBits_one (by omega)
    · exact rationalBits_mono (show RationalBits 2 2 by unfold RationalBits; decide) htwo
  | leaf j he => exact input_operand_bits hm (hq j) (hw j) he
  | setup he => exact setup_operand_bits ha hm he
  | coefficient hu he =>
    rcases he with rfl | rfl
    · exact (source_coefficient_operand_bits hm hq hw hu).1
    · exact (source_coefficient_operand_bits hm hq hw hu).2
  | intersection hu hv he => exact source_cross_operand_bits hm hq hw hu hv he
  | redundancy hu hv hz he => exact source_redundant_operand_bits hm hq hw hu hv hz he
  | segment hs he => exact buildSegments_operand_bits hm ha hb hq hw hs he
  | accumulation ss hss => exact accumulation_operand_bits hm ha hb hq hw ss hss
  | result => exact fastLowerMoment_bits hm ha hb hq hw

/-- Each rational primitive applied to evaluator operands has polynomial bit cost,
including reduction of its actual raw numerator and denominator. -/
theorem evaluator_primitive_bitCost {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (op : RationalPrimitive) {u v : ℚ}
    (hu : EvaluatorOperand a b m q w u) (hv : EvaluatorOperand a b m q w v) :
    primitiveBitCost op u v (evaluatorBits n B) ≤ 256 * (evaluatorBits n B + 1) ^ 3 :=
  primitiveBitCost_le (evaluatorOperand_bits hm ha hb hq hw hu)
    (evaluatorOperand_bits hm ha hb hq hw hv) op

/-- The executed producer's charge, all its arithmetic operand families, and the
schoolbook bit-work composition are bounded without semantic feasibility premises. -/
theorem evaluator_schoolbook_bound {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B) :
    actualEvaluatorCharge a b m q w ≤ evaluatorOperations n ∧
      (∀ x, EvaluatorOperand a b m q w x → RationalBits x (evaluatorBits n B)) ∧
      actualEvaluatorBitWork a b m q w B ≤
        ((2 * n + 2) * (2 * n + 63) + 20) *
          (256 * (5 * B + 6 + (2 * n + 2) * (52 * B + 70)) ^ 3) :=
  ⟨actualEvaluatorCharge_le a b m q w,
    fun _ hx => evaluatorOperand_bits hm ha hb hq hw hx,
    actualEvaluatorBitWork_polynomial a b m q w⟩

end ReciprocalAnchor.ManyLeaf.BitCost
