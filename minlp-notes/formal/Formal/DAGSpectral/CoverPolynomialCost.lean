import Formal.DAGSpectral.CoverLoopCost
import Formal.DAGSpectral.TrialBitCostBound
import Formal.DAGSpectral.ZeroBitCost

namespace DAGSpectral
open Matrix ReciprocalAnchor
open scoped BigOperators
namespace CoverBitCost
open NormalizationTrials CoverNormalizationExecution NormalizationBits

noncomputable def candidateWorkBound (v m p M r B : ℕ) (η : ℚ) : ℕ :=
  BasisInputExecution.basisWorkBound p m M r B +
    independenceCostCoefficient p r*(B+1)^3 + independenceStorageBudget p r 1*(B+1) +
    trialWorkBound v m p M r B η + 1

noncomputable def allCandidateWorkBound (v m p M B : ℕ) (η : ℚ) : ℕ :=
  ∑ r : Fin p, candidateWorkBound v m p M (r.val+1) B η

theorem candidateBitRun_work {v m p M B : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (b : Finset (Fin M)) {η : ℚ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (hηB : RationalBits η B)
    (hb : 0 < b.card) (hη : 0 < η) (hsize : b.card + max 1 (v - 1) + 2 ≤ B) :
    (candidateBitRun G s t D η b B (atomBudget p b.card B (6*B+1) B)
      (transformBudget p b.card B (6*B+1) B) (B+b.card + max 1 (v - 1) + 2)).2 ≤
      candidateWorkBound v m p M b.card B η := by
  have hi := independenceRun_bitWork (p := p) (r := b.card)
    (V := columns D.vector b) (fun i j => hV (label b j) i)
  have hc := independenceRun_copies_polynomial (V := columns D.vector b)
    (fun i j => hV (label b j) i)
  have hbasis := BasisInputExecution.basisRun_work D b hV hw
  have ht := trialBitRun_work G s t D b hV hw hA hηB hb hη hsize
  simp only [candidateBitRun,BasisInputExecution.basisRun_columns]
  unfold candidateWorkBound
  split_ifs <;> dsimp only <;> omega

theorem candidateBitRun_length {v m p M B K F C : ℕ} (G : ExplicitDAG v m)
    (s t : Fin v) (D : FactorData p m M) (b : Finset (Fin M)) {η : ℚ}
    (hb : 0 < b.card) (hη : 0 < η) :
    (candidateBitRun G s t D η b B K F C).1.length ≤
      trialCapacity p b.card (max 1 (v-1)) η := by
  simp only [candidateBitRun,BasisInputExecution.basisRun_columns]
  split_ifs
  · exact trialBitRun_length G s t D b B K F C hb hη
  · simp

def zeroWorkBound (v m p B : ℕ) : ℕ :=
  (m+1)*((2*p*p)*(256*(B+1)^3)+4*p*p+1) + ExplicitDAG.dpWorkPolynomial v m 0 0 B 1 + 1

/-- An explicit bound for the actual all-ranks producer. Its finite sum and all
exponents are indexed only by the fixed ambient matrix dimension. -/
noncomputable def coverWorkBound (v m p M B : ℕ) (η : ℚ) : ℕ :=
  let S := CoverSizePolynomial.uniformCapacity p v ⌈1/(η:ℝ)⌉₊
  coverLoopBound v m p (zeroWorkBound v m p B)
    (rankLoopBound v m p M (allCandidateWorkBound v m p M B η) S) ((M+1)^p*S)

theorem coverBitRun_polynomial_work {v m p M B : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) {η : ℚ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (hηB : RationalBits η B)
    (hη : 0 < η) (hsize : p + max 1 (v - 1) + 2 ≤ B) :
    (coverBitRun G s t D η B (fun r => atomBudget p r B (6*B+1) B)
      (fun r => transformBudget p r B (6*B+1) B)
      (fun r => B+r+max 1 (v-1)+2)).2 ≤ coverWorkBound v m p M B η := by
  apply coverBitRun_work_of_candidates G s t D η _ _ _ (zeroBitRun_work G s t D hA)
  · intro b hb hp
    apply (candidateBitRun_work G s t D b hV hw hA hηB hb hη (by omega)).trans
    let r : Fin p := ⟨b.card-1,by omega⟩
    have hr : r.val+1 = b.card := by dsimp [r]; omega
    unfold allCandidateWorkBound
    rw [← hr]
    exact Finset.single_le_sum
      (f := fun j : Fin p => candidateWorkBound v m p M (j.val+1) B η)
      (fun _ _ => Nat.zero_le _) (Finset.mem_univ r)
  · intro b hb hp
    apply (candidateBitRun_length G s t D b hb hη).trans
    exact CoverSizePolynomial.uniformCapacity_bound hp

end CoverBitCost
end DAGSpectral
