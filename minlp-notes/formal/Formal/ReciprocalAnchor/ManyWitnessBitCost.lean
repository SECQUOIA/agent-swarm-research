import Formal.ReciprocalAnchor.ManyEvaluatorBitCost
import Formal.ReciprocalAnchor.ManyFastLaw
import Formal.ReciprocalAnchor.ManyFastLawSize
import Formal.ReciprocalAnchor.ManyRationalCandidate
import Formal.ReciprocalAnchor.ManyRationalProducer
import Formal.ReciprocalAnchor.ManyWitnessOperandSize
import Formal.ReciprocalAnchor.ManyFastWitness

/-! Operand-size and schoolbook bit-work composition for the executable graph witness. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators
open FastEnvelope

/-- The actual scalar-law arrays have the declared common atom width. -/
theorem fastWitness_base_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) (i : Fin (fastLaw m q w).length) :
    RationalBits (fastLawMass m q w i) (atomBits B) ∧
      RationalBits (fastLawLocation m q w i) (atomBits B) := by
  have h := buildAtoms_bits hm hq hw ((fastLaw m q w).get_mem i)
  exact ⟨rationalBits_mono h.1 (by unfold atomBits; omega),
    rationalBits_mono h.2 (by unfold atomBits; omega)⟩

/-- Every partial sum of the actually produced base reciprocal is bounded before mixing. -/
theorem fastWitness_reciprocal_partial_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) (s : Finset (Fin (fastLaw m q w).length)) :
    RationalBits (∑ i ∈ s, fastLawMass m q w i / fastLawLocation m q w i) (mixInputBits n B) := by
  have hp (i : Fin (fastLaw m q w).length) := fastWitness_base_bits hm hq hw i
  have h := rationalBits_finset_sum s
    (fun i => fastLawMass m q w i / fastLawLocation m q w i)
    (fun i _ => rationalBits_div (hp i).1 (hp i).2)
  apply rationalBits_mono h
  have hc : s.card ≤ (fastLaw m q w).length := by
    simpa using Finset.card_le_univ s
  have hl := fastLaw_length m q w
  unfold mixInputBits
  nlinarith

/-- Each mixed array entry is bounded even for candidates that are not feasible. -/
theorem fastWitness_mixed_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B)
    (i : Fin ((fastLaw m q w).length + 2)) :
    RationalBits (mixedMass (fastLawMass m q w) (fastLawLocation m q w) a b m t i)
        (mixedAtomBits n B) ∧
      RationalBits (mixedLocation (fastLawLocation m q w) a b i) (mixedAtomBits n B) := by
  have hp (j : Fin (fastLaw m q w).length) := fastWitness_base_bits hm hq hw j
  have hA : atomBits B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hB : B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hT : RationalBits (∑ i, fastLawMass m q w i / fastLawLocation m q w i)
      (mixInputBits n B) := by
    simpa using fastWitness_reciprocal_partial_bits hm hq hw Finset.univ
  constructor
  · exact rationalMixMass_bits _ (fun i => rationalBits_mono (hp i).1 hA)
      (rationalBits_mono ha hB) (rationalBits_mono hb hB)
      (rationalBits_mono hm hB) (rationalBits_mono ht hB) hT _
  · exact rationalBits_mono (rationalMixLocation_bits _
      (fun i => rationalBits_mono (hp i).2 hA)
      (rationalBits_mono ha hB) (rationalBits_mono hb hB) _) (by unfold mixedAtomBits; omega)

/-- One polynomial width covers the fast envelope, mixing, selectors and graph coordinates. -/
def finalWitnessOperandBits (n B : ℕ) : ℕ :=
  FastEnvelope.evaluatorBits n B + witnessOperandBits (2 * n + 3) (mixedAtomBits n B) +
    mixedAtomBits n B + 10

theorem mixed_le_finalWitnessOperandBits (n B : ℕ) :
    mixedAtomBits n B ≤ finalWitnessOperandBits n B := by unfold finalWitnessOperandBits; omega

theorem selector_le_finalWitnessOperandBits {n B K : ℕ} (hK : K ≤ 2 * n + 3) :
    witnessOperandBits K (mixedAtomBits n B) ≤ finalWitnessOperandBits n B := by
  have h := witnessOperandBits_mono (B := mixedAtomBits n B) hK
  unfold finalWitnessOperandBits
  omega

/-- All scalar mixing intermediates are bounded before any leaf is selected. -/
theorem fastWitness_mixing_operand_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B)
    (i : Fin (fastLaw m q w).length) {v : ℚ}
    (hv : v ∈ mixingTrace a b m t
      (∑ i, fastLawMass m q w i / fastLawLocation m q w i) (fastLawMass m q w i)) :
    RationalBits v (finalWitnessOperandBits n B) := by
  have hB : B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hA : atomBits B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hT : RationalBits (∑ i, fastLawMass m q w i / fastLawLocation m q w i)
      (mixInputBits n B) := by simpa using fastWitness_reciprocal_partial_bits hm hq hw Finset.univ
  have hh := mixingTrace_bits (rationalBits_mono ha hB) (rationalBits_mono hb hB)
    (rationalBits_mono hm hB) (rationalBits_mono ht hB) hT
    (rationalBits_mono (fastWitness_base_bits hm hq hw i).1 hA) v hv
  exact rationalBits_mono hh (mixed_le_finalWitnessOperandBits n B)

/-- All interpolation arithmetic for every leaf on the actual mixed arrays is bounded.
Thresholds may be arbitrary here; the search restricts comparison operands to stored locations. -/
theorem fastWitness_interpolation_operand_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) (j : Fin n) (s₀ s₁ : ℚ)
    (i : Fin ((fastLaw m q w).length + 2)) {v : ℚ}
    (hv : v ∈ interpolationTrace
      (mixedMass (fastLawMass m q w) (fastLawLocation m q w) a b m t)
      (mixedLocation (fastLawLocation m q w) a b)
      (fun i => 1 - thresholdSelection
        (mixedMass (fastLawMass m q w) (fastLawLocation m q w) a b m t)
        (mixedLocation (fastLawLocation m q w) a b) (1 - q j) s₀ i)
      (thresholdSelection (mixedMass (fastLawMass m q w) (fastLawLocation m q w) a b m t)
        (mixedLocation (fastLawLocation m q w) a b) (q j) s₁) (w j) i) :
    RationalBits v (finalWitnessOperandBits n B) := by
  have hmix i := fastWitness_mixed_bits ha hb hm ht hq hw i
  have hB : B ≤ mixedAtomBits n B := by unfold mixedAtomBits mixInputBits; omega
  have hh := witness_interpolation_operand_bits _ _ (q j) (w j) s₀ s₁
    (fun i => (hmix i).1) (fun i => (hmix i).2)
    (rationalBits_mono (hq j) hB) (rationalBits_mono (hw j) hB) i v hv
  apply rationalBits_mono hh
  simp only [Fintype.card_fin]
  apply selector_le_finalWitnessOperandBits
  have hl := fastLaw_length m q w
  omega

/-- The materialized arrays read by all selector calls satisfy the common width bound. -/
theorem fastWitness_materialized_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B)
    (i : Fin ((fastLaw m q w).length + 2)) :
    RationalBits ((fastWitnessOutput a b m t q w).mass.get i) (finalWitnessOperandBits n B) ∧
      RationalBits ((fastWitnessOutput a b m t q w).location.get i)
        (finalWitnessOperandBits n B) := by
  rw [fastWitnessOutput_mass, fastWitnessOutput_location]
  have h := fastWitness_mixed_bits ha hb hm ht hq hw i
  exact ⟨rationalBits_mono h.1 (mixed_le_finalWitnessOperandBits n B),
    rationalBits_mono h.2 (mixed_le_finalWitnessOperandBits n B)⟩

/-- A polynomial envelope of the actual witness producer's recorded work.
It includes recomputing the base reciprocal for each materialized mixed mass,
all leaf searches, and the returned reciprocal/product coordinates. -/
def witnessOperationBound (n : ℕ) : ℕ :=
  (2 * n + 2) * (2 * n + 39) + (40 + 64 * n) * (2 * n + 4) ^ 2 +
    3 * (n + 1) * (2 * n + 3)

theorem fastWitness_work_bound {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    (fastWitnessOutput a b m t q w).work ≤ witnessOperationBound n := by
  apply (fastWitnessOutput_polynomial_work a b m t q w).trans
  unfold witnessOperationBound
  have h := Nat.log2_le_self (2 * n + 2)
  nlinarith

/-- Schoolbook work of the actual witness charge at the proved common operand width.
This composes the explicit mathematical cost model; it is not a machine-backend refinement. -/
def fastWitnessBitWork {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) (B : ℕ) : ℕ :=
  BitCost.bitWorkBudget (fastWitnessOutput a b m t q w).work (finalWitnessOperandBits n B)

theorem fastWitnessBitWork_polynomial {n B : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    fastWitnessBitWork a b m t q w B ≤
      witnessOperationBound n * (256 * (finalWitnessOperandBits n B + 1) ^ 3) :=
  BitCost.bitWorkBudget_le (fastWitness_work_bound a b m t q w) le_rfl

/-- Original-input sizes suffice for the materialized producer and its polynomial
schoolbook budget. The preceding family lemmas supply all mixing/selection intermediates. -/
theorem fastWitness_schoolbook_bound {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) :
    (fastWitnessOutput a b m t q w).work ≤ witnessOperationBound n ∧
      (∀ i, RationalBits ((fastWitnessOutput a b m t q w).mass.get i)
          (finalWitnessOperandBits n B) ∧
        RationalBits ((fastWitnessOutput a b m t q w).location.get i)
          (finalWitnessOperandBits n B)) ∧
      fastWitnessBitWork a b m t q w B ≤
        witnessOperationBound n * (256 * (finalWitnessOperandBits n B + 1) ^ 3) :=
  ⟨fastWitness_work_bound a b m t q w,
    fastWitness_materialized_bits ha hb hm ht hq hw,
    fastWitnessBitWork_polynomial a b m t q w⟩

end ReciprocalAnchor.ManyLeaf


