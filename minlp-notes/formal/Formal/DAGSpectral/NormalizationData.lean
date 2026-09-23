import Formal.DAGSpectral.NormalizationAtoms
import Formal.DAGSpectral.NormalizationFloor

namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators
namespace NormalizationTrials

/-- The interface filled by the actual labeled LDL producer. -/
structure FactorData (p m M : ℕ) where
  atom : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ
  owner : Fin M → Option (Fin m)
  weight : Fin M → ℚ
  vector : Fin M → Fin p → ℚ
  weight_pos : ∀ j, 0 < weight j
  atom_eq : ∀ o, atom o = factorSum vector weight (Finset.univ.filter (fun j => owner j = o))
  owner_card : ∀ o, (Finset.univ.filter (fun j => owner j = o)).card ≤ p

variable {p m M : ℕ}

def selectedOwners (S : Finset (Fin m)) : Finset (Option (Fin m)) :=
  insert none (S.image some)

def selectedFactors (D : FactorData p m M) (S : Finset (Fin m)) : Finset (Fin M) :=
  Finset.univ.filter (fun j => D.owner j ∈ selectedOwners S)

def information (D : FactorData p m M) (S : Finset (Fin m)) :=
  D.atom none + ∑ a ∈ S, D.atom (some a)

@[simp] theorem mem_selectedOwners (S : Finset (Fin m)) (o : Option (Fin m)) :
    o ∈ selectedOwners S ↔ o = none ∨ ∃ a ∈ S, o = some a := by
  simp [selectedOwners,eq_comm]

@[simp] theorem mem_selectedFactors (D : FactorData p m M) (S : Finset (Fin m)) (j : Fin M) :
    j ∈ selectedFactors D S ↔ D.owner j ∈ selectedOwners S := by simp [selectedFactors]

theorem information_eq (D : FactorData p m M) (S : Finset (Fin m)) :
    information D S = factorSum D.vector D.weight (selectedFactors D S) := by
  have ho : information D S = ∑ o ∈ selectedOwners S, D.atom o := by
    simp [information,selectedOwners,Finset.sum_image]
  rw [ho]
  simp only [D.atom_eq,factorSum,selectedFactors,Finset.sum_filter]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  simp

/-- A selected set satisfying the owner condition includes every basis factor. -/
theorem forced_subset_selected (D : FactorData p m M) (S : Finset (Fin m))
    (s : Finset (Fin M)) (h : forcedOwners D.owner s ⊆ S) : s ⊆ selectedFactors D S := by
  intro j hj
  rw [mem_selectedFactors,mem_selectedOwners]
  cases he : D.owner j with
  | none => exact Or.inl rfl
  | some a => exact Or.inr ⟨a,h ((mem_forcedOwners D.owner s a).mpr ⟨j,hj,he⟩),rfl⟩

/-- Every accepted selected set has the exact normalized identity floor. -/
theorem accepted_floor (D : FactorData p m M) (S : Finset (Fin m))
    (s : Finset (Fin M)) (hind : independent D.vector s)
    (h : acceptsSelection D.vector D.weight D.owner s D.atom S) :
    Loewner 1 (ratMatrixReal (transform D.vector D.weight s * information D S *
      (transform D.vector D.weight s)ᵀ)) := by
  rw [information_eq]
  exact normalization_forced_floor D.vector D.weight (selectedFactors D S) (label s)
    (label s).injective (fun i => forced_subset_selected D S s h.1 (label_mem s i))
    ((independent_iff D.vector s).mp hind) (scales D.weight s)
    (fun i => (scale_spec (D.weight_pos (label s i))).2.1)
    (fun j _ => (D.weight_pos j).le)

/-- Basis containment suffices for the floor even before atom filters are checked. -/
theorem contained_floor (D : FactorData p m M) (S : Finset (Fin m))
    (s : Finset (Fin M)) (hind : independent D.vector s)
    (h : s ⊆ selectedFactors D S) :
    Loewner 1 (ratMatrixReal (transform D.vector D.weight s * information D S *
      (transform D.vector D.weight s)ᵀ)) := by
  rw [information_eq]
  exact normalization_forced_floor D.vector D.weight (selectedFactors D S) (label s)
    (label s).injective (fun i => h (label_mem s i))
    ((independent_iff D.vector s).mp hind) (scales D.weight s)
    (fun i => (scale_spec (D.weight_pos (label s i))).2.1)
    (fun j _ => (D.weight_pos j).le)

theorem information_symmetric (D : FactorData p m M) (S : Finset (Fin m)) :
    (information D S)ᵀ = information D S := by
  rw [information_eq]
  simp [factorSum,Matrix.transpose_sum,Matrix.transpose_smul]

/-- Original range filtering is preserved by summing the accepted atoms. -/
theorem accepted_range (D : FactorData p m M) (S : Finset (Fin m))
    (s : Finset (Fin M)) (h : acceptsSelection D.vector D.weight D.owner s D.atom S) :
    rangeProjector (columns D.vector s) * information D S = information D S := by
  unfold information
  rw [Matrix.mul_add,h.2.1.1,Matrix.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro a ha
  exact (h.2.2 a ha).1

/-- The normalized floor proves equality of actual real ranges, not only inclusion. -/
theorem accepted_exact_range (D : FactorData p m M) (S : Finset (Fin m))
    (s : Finset (Fin M)) (hind : independent D.vector s)
    (h : acceptsSelection D.vector D.weight D.owner s D.atom S) :
    LinearMap.range (ratMatrixReal (information D S)).mulVecLin =
      LinearMap.range (ratMatrixReal (columns D.vector s)).mulVecLin :=
  retained_range_of_normalized_floor _ ((independent_iff D.vector s).mp hind)
    (scales D.weight s) (fun i => (scale_spec (D.weight_pos (label s i))).1.ne')
    (information D S) (information_symmetric D S) (accepted_range D S s h)
    (accepted_floor D S s hind h)

theorem factorSum_real_psd (D : FactorData p m M) (F : Finset (Fin M)) :
    (ratMatrixReal (factorSum D.vector D.weight F)).PosSemidef := by
  have h := rankOne_sum_mono (fun j i => (D.vector j i : ℝ))
    (fun j => (D.weight j : ℝ)) ∅ F (Finset.empty_subset _)
    (fun j _ => by exact_mod_cast (D.weight_pos j).le)
  simpa only [Loewner,Finset.sum_empty,sub_zero,factorSum,ratMatrixReal_rankOne_sum] using h

theorem atom_real_psd (D : FactorData p m M) (o : Option (Fin m)) :
    (ratMatrixReal (D.atom o)).PosSemidef := by
  rw [D.atom_eq]
  exact factorSum_real_psd D _

theorem information_real_psd (D : FactorData p m M) (S : Finset (Fin m)) :
    (ratMatrixReal (information D S)).PosSemidef := by
  rw [information_eq]
  exact factorSum_real_psd D _

theorem information_eq_ownerSum (D : FactorData p m M) (S : Finset (Fin m)) :
    information D S = ∑ o ∈ selectedOwners S, D.atom o := by
  simp [information,selectedOwners,Finset.sum_image]

theorem information_real_eq_ownerSum (D : FactorData p m M) (S : Finset (Fin m)) :
    ratMatrixReal (information D S) = ∑ o ∈ selectedOwners S, ratMatrixReal (D.atom o) := by
  rw [information_eq_ownerSum]
  ext i j
  simp [ratMatrixReal,Matrix.sum_apply]

end NormalizationTrials
end
end DAGSpectral
