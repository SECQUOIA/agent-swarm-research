import Formal.DAGSpectral.NormalizationData
import Formal.DAGSpectral.SortedTrial
import Formal.DAGSpectral.FactorRange

namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators
namespace NormalizationTrials
variable {p m M : ℕ}

def selectedRank (D : FactorData p m M) (S : Finset (Fin m)) : ℕ :=
  Module.finrank ℝ (familySpan (realFactorFamily (fun j : selectedFactors D S => D.vector j)))

theorem selectedRank_le (D : FactorData p m M) (S : Finset (Fin m)) :
    selectedRank D S ≤ p := family_rank_le_dimension _

/-- The trial rank is the actual rank of the selected original information matrix. -/
theorem selectedRank_eq_information_rank (D : FactorData p m M) (S : Finset (Fin m)) :
    selectedRank D S = (ratMatrixReal (information D S)).rank := by
  have he : ratMatrixReal (information D S) =
      rankOneSum (fun j : selectedFactors D S => (D.weight j : ℝ))
        (realFactorFamily (fun j : selectedFactors D S => D.vector j)) := by
    rw [information_eq]
    ext i k
    simp only [ratMatrixReal_apply,factorSum,Matrix.sum_apply,Matrix.smul_apply,
      smul_eq_mul,Matrix.vecMulVec_apply,rankOneSum,realFactorFamily]
    push_cast
    simpa only [mul_assoc] using Finset.sum_subtype (selectedFactors D S) (fun _ => Iff.rfl)
      (fun j => (D.weight j : ℝ) * (D.vector j i : ℝ) * (D.vector j k : ℝ))
  rw [he,rankOneSum_rank _ _ (fun j => by exact_mod_cast D.weight_pos j)]
  rfl

theorem selectedRank_zero_iff (D : FactorData p m M) (S : Finset (Fin m)) :
    selectedRank D S = 0 ↔ D.atom none = 0 ∧ ∀ a ∈ S, D.atom (some a) = 0 := by
  rw [selectedRank_eq_information_rank,information_real_eq_ownerSum,
    selected_psd_rank_zero_iff D.atom (atom_real_psd D)]
  simp [selectedOwners]

theorem selected_fiber_subset (D : FactorData p m M) (S : Finset (Fin m))
    (o : Option (Fin m)) (ho : o ∈ selectedOwners S) :
    Finset.univ.filter (fun j => D.owner j = o) ⊆ selectedFactors D S := by
  intro j hj
  rw [mem_selectedFactors,(Finset.mem_filter.mp hj).2]
  exact ho

/-- Actual maximum volume and exact dyadic scaling produce an accepted trial
for every selected input set. No good trial is an extra hypothesis. -/
theorem exists_accepted_trial (D : FactorData p m M) (S : Finset (Fin m)) :
    ∃ s : Finset (Fin M), s ∈ trials D.vector (selectedRank D S) ∧
      acceptsSelection D.vector D.weight D.owner s D.atom S ∧
      Loewner 1 (ratMatrixReal (transform D.vector D.weight s * information D S *
        (transform D.vector D.weight s)ᵀ)) ∧
      LinearMap.range (ratMatrixReal (information D S)).mulVecLin =
        LinearMap.range (ratMatrixReal (columns D.vector s)).mulVecLin ∧
      (forcedOwners D.owner s).card ≤ selectedRank D S ∧
      ∀ j ∈ selectedFactors D S, ∀ i,
        |Real.sqrt (D.weight j : ℝ) *
          ((transform D.vector D.weight s *ᵥ D.vector j) i : ℝ)| < 2 := by
  obtain ⟨s,hsub,htrial,hspan,hmag⟩ :=
    exists_good_sorted_trial D.vector D.weight D.weight_pos (selectedFactors D S)
  have hind := ((mem_trials D.vector (selectedRank D S) s).mp htrial).2
  have hrange : ∀ j ∈ selectedFactors D S,
      rangeProjector (columns D.vector s) *ᵥ D.vector j = D.vector j := by
    intro j hj
    exact projector_eq_of_real_span (columns D.vector s)
      ((independent_iff D.vector s).mp hind) (D.vector j) (hspan j hj)
  have hratmag : ∀ j ∈ selectedFactors D S, ∀ i,
      D.weight j * ((transform D.vector D.weight s *ᵥ D.vector j) i)^2 < 4 := by
    intro j hj i
    exact real_factor_coordinate_bound (D.weight_pos j).le (hmag j hj i)
  have ha : ∀ o ∈ selectedOwners S, acceptsAtom D.vector D.weight s (D.atom o) := by
    intro o ho
    rw [D.atom_eq]
    exact factorSum_accepts D.vector D.weight _ s (D.owner_card o)
      (fun j hj => hrange j (selected_fiber_subset D S o ho hj))
      (fun j hj i => hratmag j (selected_fiber_subset D S o ho hj) i)
  have howners : forcedOwners D.owner s ⊆ S := by
    intro a ha
    obtain ⟨j,hj,ho⟩ := (mem_forcedOwners D.owner s a).mp ha
    have hh := hsub hj
    rw [mem_selectedFactors,ho] at hh
    simpa [selectedOwners] using hh
  have haccept : acceptsSelection D.vector D.weight D.owner s D.atom S := by
    refine ⟨howners,ha none (by simp [selectedOwners]),?_⟩
    intro a haS
    exact ha (some a) (by simp [selectedOwners,haS])
  refine ⟨s,htrial,haccept,accepted_floor D S s hind haccept,
    accepted_exact_range D S s hind haccept,?_,hmag⟩
  have hcard := ((mem_trials D.vector (selectedRank D S) s).mp htrial).1
  exact (forcedOwners_card D.owner s).trans hcard.le

end NormalizationTrials
end
end DAGSpectral
