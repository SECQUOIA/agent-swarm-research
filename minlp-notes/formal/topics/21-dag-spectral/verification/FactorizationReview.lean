import Formal.DAGSpectral.LabeledFactors
import Formal.DAGSpectral.MaxVolumeTrials
import Formal.DAGSpectral.NormalizationProducer
import Formal.DAGSpectral.NormalizationFloor

open DAGSpectral Matrix
open scoped Matrix

-- A zero leading pivot must not discard a later positive direction.
example : (rationalLDL 2 !![(0 : ℚ), 0; 0, 3]).length = 1 := by native_decide
example : ((rationalLDL 2 !![(0 : ℚ), 0; 0, 3]).map
    (fun f => (f.1, f.2 0, f.2 1))) = [(3, 0, 1)] := by native_decide

-- A nonzero pivot can leave a zero Schur complement; signs are preserved.
example : ((rationalLDL 2 !![(1 : ℚ), -2; -2, 4]).map
    (fun f => (f.1, f.2 0, f.2 1))) = [(1, 1, -2)] := by native_decide

example : rationalLDL 3 (0 : Matrix (Fin 3) (Fin 3) ℚ) = [] := by native_decide
example : rationalLDL 0 (0 : Matrix (Fin 0) (Fin 0) ℚ) = [] := by native_decide

-- Two factors of one owner remain separate; equal factors of other owners do too.
def reviewInputs : Fin 2 → Matrix (Fin 2) (Fin 2) ℚ := fun _ => !![1, 0; 0, 2]
example : Fintype.card (FactorLabel reviewInputs) = 4 := by native_decide
example : factorOwner (A := reviewInputs) ⟨0, ⟨0, by native_decide⟩⟩ =
    factorOwner (A := reviewInputs) ⟨0, ⟨1, by native_decide⟩⟩ := rfl
example : (⟨0, ⟨0, by native_decide⟩⟩ : FactorLabel reviewInputs) ≠
    ⟨0, ⟨1, by native_decide⟩⟩ := by native_decide
example : (⟨0, ⟨0, by native_decide⟩⟩ : FactorLabel reviewInputs) ≠
    ⟨1, ⟨0, by native_decide⟩⟩ := by native_decide

def reviewColumns : Matrix (Fin 2) (Fin 1) ℚ := !![2; 0]
def reviewScales : Fin 1 → ℚ := fun _ => 2

-- Proper-subspace normalization, with a nontrivial rational left inverse.
example : normalizerProducer reviewColumns reviewScales = !![1, 0] := by native_decide
example : reconstructorProducer reviewColumns reviewScales = !![1; 0] := by native_decide
example : transformProducer reviewColumns reviewScales !![3, 0; 0, 0] = !![3] := by native_decide
example : reconstructorProducer reviewColumns reviewScales *
    transformProducer reviewColumns reviewScales !![3, 0; 0, 0] *
    (reconstructorProducer reviewColumns reviewScales)ᵀ = !![3, 0; 0, 0] := by native_decide

-- Information outside the chosen span fails the actual rational range test.
example : rangeProjectorProducer reviewColumns * !![0, 0; 0, 1] ≠ !![0, 0; 0, 1] := by native_decide

#print axioms rationalPSD_zero_row
#print axioms rationalSchur_posSemidef
#print axioms rationalLDL_factors
#print axioms rationalLDL_reconstruct
#print axioms rationalLDL_real_reconstruct
#print axioms factorLabel_selected_reconstruct
#print axioms max_volume_scaled_basis
#print axioms exists_max_volume_rational_trial
#print axioms reindex_labeled_basis
#print axioms normalizationProducer_reconstruct
#print axioms retained_range_of_normalized_floor
#print axioms normalization_forced_floor
