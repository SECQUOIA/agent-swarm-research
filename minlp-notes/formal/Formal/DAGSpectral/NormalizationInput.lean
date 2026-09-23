import Formal.DAGSpectral.NormalizationComplete
import Formal.DAGSpectral.IndexedFactors

/-! Normalization trials from the original rational PSD prior and input atoms.
Every decomposition, label, scale and inverse is produced from those inputs. -/
namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators
namespace NormalizationTrials
variable {p m : ℕ}

private theorem priorAtom_psd (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ a, (ratMatrixReal (Q a)).PosSemidef) :
    ∀ o, (ratMatrixReal (priorAtomMatrices Q0 Q o)).PosSemidef :=
  Fin.cases hQ0 hQ

/-- Actual input data, with one label for every positive LDL factor and owners
retained even when two numerical factors coincide. -/
def producedData (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ a, (ratMatrixReal (Q a)).PosSemidef) :
    FactorData p m (indexedFactorCount (priorAtomMatrices Q0 Q)) where
  atom o := o.elim Q0 Q
  owner := indexedPriorAtomOwner Q0 Q
  weight := indexedFactorWeight (priorAtomMatrices Q0 Q)
  vector := indexedFactorVector (priorAtomMatrices Q0 Q)
  weight_pos j := (indexedFactor_positive _ (priorAtom_psd Q0 Q hQ0 hQ) j).1
  atom_eq o := by
    ext i j
    rw [indexedPriorAtom_owner_reconstruct Q0 Q hQ0 hQ o i j]
    simp only [factorSum,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,
      Matrix.vecMulVec_apply,Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro k _
    split_ifs <;> ring
  owner_card := indexedPriorAtom_owner_card_le Q0 Q

@[simp] theorem producedData_information (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ a, (ratMatrixReal (Q a)).PosSemidef)
    (S : Finset (Fin m)) :
    information (producedData Q0 Q hQ0 hQ) S = Q0 + ∑ a ∈ S, Q a := rfl

/-- Every original selected PSD sum survives one of the finitely enumerated
sorted rational trials, at its actual matrix rank. -/
theorem original_input_trial (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ a, (ratMatrixReal (Q a)).PosSemidef)
    (S : Finset (Fin m)) :
    let D := producedData Q0 Q hQ0 hQ
    ∃ s, s ∈ trials D.vector (ratMatrixReal (Q0 + ∑ a ∈ S, Q a)).rank ∧
      acceptsSelectionCode D.vector D.weight D.owner s D.atom S ∧
      Loewner 1 (ratMatrixReal (transformCode D.vector D.weight s *
        (Q0 + ∑ a ∈ S, Q a) * (transformCode D.vector D.weight s)ᵀ)) ∧
      LinearMap.range (ratMatrixReal (Q0 + ∑ a ∈ S, Q a)).mulVecLin =
        LinearMap.range (ratMatrixReal (columns D.vector s)).mulVecLin ∧
      (forcedOwners D.owner s).card ≤ (ratMatrixReal (Q0 + ∑ a ∈ S, Q a)).rank ∧
      ∀ j ∈ selectedFactors D S, ∀ i,
        |Real.sqrt (D.weight j : ℝ) *
          ((transformCode D.vector D.weight s *ᵥ D.vector j) i : ℝ)| < 2 := by
  let D := producedData Q0 Q hQ0 hQ
  have h := exists_accepted_trial D S
  simpa only [D,acceptsSelectionCode_iff,transformCode_eq,selectedRank_eq_information_rank,
    producedData_information] using h

/-- The advertised label and per-rank trial counts concern the actual producer. -/
theorem original_input_size (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ a, (ratMatrixReal (Q a)).PosSemidef)
    (r : ℕ) :
    indexedFactorCount (priorAtomMatrices Q0 Q) ≤ p*(m+1) ∧
      (trials (producedData Q0 Q hQ0 hQ).vector r).card ≤
        (indexedFactorCount (priorAtomMatrices Q0 Q)).choose r :=
  ⟨indexedPriorAtomCount_le Q0 Q,trial_count _ r⟩

end NormalizationTrials
end
end DAGSpectral
