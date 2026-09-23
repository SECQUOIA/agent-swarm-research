import Formal.MatroidSpectral.NormalizationExecution
import Formal.DAGSpectral.CoverEnumerationCost
import Formal.DAGSpectral.SubsetInputExecution

namespace MatroidSpectral
open DAGSpectral DAGSpectral.CoverBitCost

/-- Actual identifier enumeration, fixed-cardinality sublists, and finite-set
construction. The returned work includes dependent subsets before testing. -/
def candidateSubsetsRun (r M : ℕ) : List (Finset (Fin M)) × ℕ :=
  let ids := finRangeCounted M
  let enumeration := sublistsCounted r ids.1
  let subsets := subsetsCounted enumeration.1
  (subsets.1,ids.2+enumeration.2*(M+1)+subsets.2)

@[simp] theorem candidateSubsetsRun_value (r M : ℕ) :
    (candidateSubsetsRun r M).1 = candidateBasisList r M := by
  simp only [candidateSubsetsRun,finRangeCounted_value,subsetsCounted_value,candidateBasisList]

@[simp] theorem candidateSubsetsRun_length (r M : ℕ) :
    (candidateSubsetsRun r M).1.length = M.choose r := by simp

@[simp] theorem mem_candidateSubsetsRun {r M : ℕ} {b : Finset (Fin M)} :
    b ∈ (candidateSubsetsRun r M).1 ↔ b.card = r := by simp

def candidateSubsetsWorkBound (r M : ℕ) : ℕ :=
  (M+1)^2 + enumerationCoefficient r*(M+1)^(r+2)*(M+1) +
    (1+M.choose r*((r+1)^2*(2*M+3)+1))

theorem candidateSubsetsRun_work (r M : ℕ) :
    (candidateSubsetsRun r M).2 ≤ candidateSubsetsWorkBound r M := by
  have hi := finRangeCounted_work M
  have he := sublistsCounted_bound r (List.finRange M)
  have hs := subsetsCounted_work (sublistsCounted r (List.finRange M)).1 (r := r) (by
    intro xs hxs
    rw [sublistsCounted_value] at hxs
    exact (List.mem_sublistsLen.mp hxs).2.le)
  simp only [List.length_finRange,sublistsCounted_length] at he hs
  simp only [candidateSubsetsRun,finRangeCounted_value,candidateSubsetsWorkBound]
  exact Nat.add_le_add (Nat.add_le_add hi (Nat.mul_le_mul_right _ he)) hs

/-- Fixed rank enumeration is polynomial even when every subset is rejected. -/
theorem candidateSubsetsWorkBound_polynomial (r M : ℕ) :
    candidateSubsetsWorkBound r M ≤
      (M+1)^2 + enumerationCoefficient r*(M+1)^(r+3) +
        1+(M+1)^r*((r+1)^2*(2*M+3)+1) := by
  have hc : M.choose r ≤ (M+1)^r :=
    (Nat.choose_le_pow M r).trans (Nat.pow_le_pow_left (Nat.le_succ M) r)
  unfold candidateSubsetsWorkBound
  have he : enumerationCoefficient r*(M+1)^(r+2)*(M+1) =
      enumerationCoefficient r*(M+1)^(r+3) := by rw [show r+3 = (r+2)+1 by omega,pow_succ]; ring
  rw [he]
  have hh := Nat.mul_le_mul_right ((r+1)^2*(2*M+3)+1) hc
  omega

end MatroidSpectral
