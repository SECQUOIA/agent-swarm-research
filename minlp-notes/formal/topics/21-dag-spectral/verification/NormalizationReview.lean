import Formal.DAGSpectral.NormalizationInput
import Formal.DAGSpectral.IndexedFactors
import Formal.DAGSpectral.GraphInput
import Formal.DAGSpectral.RangeObstruction
open DAGSpectral DAGSpectral.NormalizationTrials

def reviewAtoms : Fin 2 → Matrix (Fin 2) (Fin 2) ℚ :=
  ![!![0,0;0,3], !![2,0;0,0]]
example : indexedFactorCount (priorAtomMatrices 0 reviewAtoms) = 2 := by native_decide
example : indexedPriorAtomOwner 0 reviewAtoms ⟨0,by native_decide⟩ = some 0 := by native_decide
example : indexedPriorAtomOwner 0 reviewAtoms ⟨1,by native_decide⟩ = some 1 := by native_decide
example : indexedFactorWeight (priorAtomMatrices 0 reviewAtoms) ⟨0,by native_decide⟩ = 3 := by native_decide
example : indexedFactorVector (priorAtomMatrices 0 reviewAtoms) ⟨0,by native_decide⟩ 0 = 0 := by native_decide
example : indexedFactorVector (priorAtomMatrices 0 reviewAtoms) ⟨0,by native_decide⟩ 1 = 1 := by native_decide
example : (candidates 4 2).card = 6 := by native_decide
example : (candidates 0 0).card = 1 := by native_decide
example : forcedOwners (![none,some 0,some 0] : Fin 3 → Option (Fin 1)) Finset.univ = {0} := by native_decide
example : (checkDAG (fun _ : Fin 2 => (0 : Fin 2)) (fun _ => 1)).isSome = true := by native_decide
example : (checkDAG (fun _ : Fin 1 => (0 : Fin 2)) (fun _ => 0)).isSome = false := by native_decide
example : (checkDAG (fun _ : Fin 1 => (1 : Fin 2)) (fun _ => 0)).isSome = false := by native_decide
example : (checkDAGWithOrder (fun _ : Fin 1 => (1 : Fin 2)) (fun _ => 0)
    (Equiv.swap 0 1)).isSome = true := by native_decide
#print axioms exists_good_sorted_trial
#print axioms exists_accepted_trial
#print axioms accepted_exact_range
#print axioms selectedRank_zero_iff

#print axioms original_input_trial
#print axioms original_input_size

-- The generic rank-zero theorem specializes to the actual original matrices.
example {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef)
    (hQ : ∀ a, (ratMatrixReal (Q a)).PosSemidef) (S : Finset (Fin m)) :
    (ratMatrixReal (Q0 + ∑ a ∈ S, Q a)).rank = 0 ↔
      Q0 = 0 ∧ ∀ a ∈ S, Q a = 0 := by
  have h := selectedRank_zero_iff (producedData Q0 Q hQ0 hQ) S
  rw [selectedRank_eq_information_rank, producedData_information] at h
  exact h
