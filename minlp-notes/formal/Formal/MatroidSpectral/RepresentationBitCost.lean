import Formal.MatroidSpectral.RepresentationCost
import Formal.MatroidSpectral.EliminationBitExecution

/-! Polynomial operand widths and a schoolbook bit-work observer for the actual
row scan. The matrix dimensions are variable throughout these bounds. -/
namespace MatroidSpectral
open Matrix Elimination DAGSpectral ReciprocalAnchor
open scoped BigOperators

def rowReductionOperandBits (a m K : ℕ) : ℕ :=
  (2*K+1+m*(2*K+1)) + determinantOperandBits a (1+m*(2*K+1)) +
    polynomialDeterminantBits a (1+m*(2*K+1)) + 1

theorem rowReductionRun_operands_bits {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : MatrixBits A K) (rows : List (Fin a)) :
    ∀ e ∈ (rowReductionRun A rows).operands,
      RationalBits e.1 (rowReductionOperandBits a m K) ∧
      RationalBits e.2 (rowReductionOperandBits a m K) := by
  induction rows with
  | nil => simp [rowReductionRun]
  | cons i is ih =>
      let S := insert i (rowReductionRun A is).selected
      let G := view (gramRun A S).matrix
      have hG : MatrixBits G (1+m*(2*K+1)) := by
        rw [show G = rowGramFin A S from gramRun_value A S]
        simpa [two_mul] using rowGramFin_bits hA S
      have hs : S.card ≤ a := by simpa using Finset.card_le_univ S
      have hd : determinantOperandBits S.card (1+m*(2*K+1)) ≤
          rowReductionOperandBits a m K := by
        apply le_trans (b := determinantOperandBits a (1+m*(2*K+1)))
        · unfold determinantOperandBits iterationBits
          gcongr
        · unfold rowReductionOperandBits
          omega
      have hv : polynomialDeterminantBits S.card (1+m*(2*K+1)) ≤
          rowReductionOperandBits a m K := by
        apply le_trans (b := polynomialDeterminantBits a (1+m*(2*K+1)))
        · unfold polynomialDeterminantBits
          gcongr
        · unfold rowReductionOperandBits
          omega
      intro e he
      change e ∈ ((rowReductionRun A is).operands ++ (gramRun A S).operands ++
        (rationalDeterminantRun G).operands ++ [((rationalDeterminantRun G).value, 0)]) at he
      simp only [List.mem_append, List.mem_singleton] at he
      rcases he with ((he | he) | he) | rfl
      · exact ih e he
      · obtain ⟨h₁, h₂⟩ := gramRun_operands_bits hA S e he
        exact ⟨rationalBits_mono h₁ (by unfold rowReductionOperandBits; omega),
          rationalBits_mono h₂ (by unfold rowReductionOperandBits; omega)⟩
      · obtain ⟨h₁, h₂⟩ := rationalDeterminantRun_operands_bits hG e he
        exact ⟨rationalBits_mono h₁ hd, rationalBits_mono h₂ hd⟩
      · constructor
        · rw [rationalDeterminantRun_correct]
          exact rationalBits_mono (matrixBits_det_polynomial hG) hv
        · exact rationalBits_mono rationalBits_zero (by unfold rowReductionOperandBits; omega)

theorem gramEntryRun_operands_length {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) (i j : Fin S.card) :
    (gramEntryRun A S i j).operands.length = (gramEntryRun A S i j).operations := by
  apply sumRun_operands_length
  intro x hx
  obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
  rfl

theorem gramRun_operands_length {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) : (gramRun A S).operands.length = (gramRun A S).operations := by
  simp [gramRun, List.length_flatten, List.map_ofFn, Function.comp_def,
    gramEntryRun_operands_length, List.sum_ofFn]

theorem rowReductionRun_operands_length {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) :
    (rowReductionRun A rows).operands.length = (rowReductionRun A rows).operations := by
  induction rows with
  | nil => rfl
  | cons i is ih =>
      simp [rowReductionRun, ih, gramRun_operands_length, rationalDeterminantRun_operands_length,
        Nat.add_assoc]

/-- Original entries are copied into the reduced representation, and the scan
uses finite row lists and dense matrices. This observer permits a full sequential
scan for each indexed access and charges materialization and row-set handling. -/
def rectangularInputWidth {a m : ℕ} (A : RationalRepresentation a m) : ℕ :=
  Finset.univ.sup fun i => Finset.univ.sup fun j => scalarWidth (A i j)

def rowReductionBitRun {a m : ℕ} (A : RationalRepresentation a m) :
    Finset (Fin a) × ℕ :=
  let result := rowReductionRun A (List.finRange a)
  let width := max (rectangularInputWidth A) (traceWidth result.operands)
  (result.selected, operandWork result.operands +
    64*(result.operations+(a+1)*(m+1)+1)*(a+1)^2*(m+1)*(width+a+m+1))

def rowReductionBitWork (a m K : ℕ) : ℕ :=
  let operations := a * rowReductionStepOperations a m
  let width := K + rowReductionOperandBits a m K
  operations * (256 * (width+1)^3) +
    64*(operations+(a+1)*(m+1)+1)*(a+1)^2*(m+1)*(width+a+m+1)

@[simp] theorem rowReductionBitRun_selected {a m : ℕ} (A : RationalRepresentation a m) :
    (rowReductionBitRun A).1 = independentRows A := rowReductionRun_selected A _

theorem rectangularInputWidth_le {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : MatrixBits A K) : rectangularInputWidth A ≤ K := by
  apply Finset.sup_le
  intro i _
  apply Finset.sup_le
  intro j _
  exact scalarWidth_le (hA i j)

theorem rowReductionBitRun_work_le {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : MatrixBits A K) : (rowReductionBitRun A).2 ≤ rowReductionBitWork a m K := by
  let result := rowReductionRun A (List.finRange a)
  let W := K + rowReductionOperandBits a m K
  have hops : result.operations ≤ a * rowReductionStepOperations a m := by
    simpa [result] using rowReductionRun_operations_le A (List.finRange a)
  have hpair : ∀ e ∈ result.operands, pairWidth e ≤ W := by
    intro e he
    exact (pairWidth_le (rowReductionRun_operands_bits hA _ e he)).trans (by dsimp [W]; omega)
  have hwidth : max (rectangularInputWidth A) (traceWidth result.operands) ≤ W := by
    exact max_le ((rectangularInputWidth_le hA).trans (by dsimp [W]; omega))
      (traceWidth_le hpair)
  have hwork : operandWork result.operands ≤
      (a * rowReductionStepOperations a m) * (256 * (W+1)^3) := by
    apply (operandWork_le hpair).trans
    rw [rowReductionRun_operands_length]
    exact Nat.mul_le_mul_right _ hops
  change operandWork result.operands +
    64*(result.operations+(a+1)*(m+1)+1)*(a+1)^2*(m+1)*
      (max (rectangularInputWidth A) (traceWidth result.operands)+a+m+1) ≤ _
  unfold rowReductionBitWork
  change _ ≤ (a * rowReductionStepOperations a m) * (256 * (W+1)^3) +
    64*(a * rowReductionStepOperations a m+(a+1)*(m+1)+1)*(a+1)^2*(m+1)*(W+a+m+1)
  gcongr

end MatroidSpectral
