import Formal.DAGSpectral.CoverCorrectness
import Formal.DAGSpectral.Pseudoinverse

/-! Spectral comparison for finite sets. No graph or matroid assumption is
needed here: feasibility is handled by the representative producer. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

variable {p m M : ℕ}

/-- The full selected-set profile. A common forced subset cancels when comparing
this profile with the optional-element profile used in contraction. -/
def trialProfile (D : FactorData p m M) (η : ℚ) (q : ℕ)
    (b : Finset (Fin M)) (S : Finset (Fin m)) : UpperCoord b.card → ℤ :=
  ∑ e ∈ S, rationalUpperLabels (η / (b.card * q : ℚ))
    (fun a => trialAtom D b (some a)) e

theorem trialProfile_eq_list (D : FactorData p m M) (η : ℚ) (q : ℕ)
    (b : Finset (Fin M)) (S : Finset (Fin m)) :
    trialProfile D η q b S = ExplicitDAG.profile
      (rationalUpperLabels (η / (b.card * q : ℚ))
        (fun a => trialAtom D b (some a))) S.toList := by
  simp only [trialProfile, ExplicitDAG.profile]
  simp

/-- Equal rounded profiles imply the two-sided relative bound. Both sets are
accepted in the same rational normalization, and have at most `q` elements. -/
theorem accepted_same_profile_sandwich (D : FactorData p m M)
    (η : ℚ) (hη : 0 < η) (q : ℕ) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card) (hi : independent D.vector b)
    (S T : Finset (Fin m)) (hS : S.card ≤ q) (hT : T.card ≤ q)
    (haS : acceptsSelection D.vector D.weight D.owner b D.atom S)
    (haT : acceptsSelection D.vector D.weight D.owner b D.atom T)
    (hprofile : trialProfile D η q b S = trialProfile D η q b T) :
    RelativeSandwich (η : ℝ) (ratMatrixReal (information D S))
      (ratMatrixReal (information D T)) := by
  have hfloor : Loewner 1 (pathMatrix (ratMatrixReal (trialAtom D b none))
      (fun e => ratMatrixReal (trialAtom D b (some e))) S.toList) := by
    simp only [trialAtom, transformCode_eq]
    rw [transformed_pathMatrix_eq D b S.toList S.nodup_toList]
    simpa using accepted_floor D S b hi haS
  have hrel := pathMatrix_relativeSandwich
    (trialAtom_psd D b none).isHermitian
    (fun e => (trialAtom_psd D b (some e)).isHermitian)
    (by exact_mod_cast hη : 0 < (η : ℝ)) hb hq S.toList T.toList
    (by simpa using hS) (by simpa using hT) hfloor
  have hlabels : ∀ i j : Fin b.card, i ≤ j →
      pathLabel (spectralMesh (η : ℝ) b.card q)
        (S.toList.map (fun e => ratMatrixReal (trialAtom D b (some e)) i j)) =
      pathLabel (spectralMesh (η : ℝ) b.card q)
        (T.toList.map (fun e => ratMatrixReal (trialAtom D b (some e)) i j)) := by
    intro i j hij
    rw [trialProfile_eq_list, trialProfile_eq_list] at hprofile
    have hh := congrFun hprofile ((upperCoordEquiv b.card).symm ⟨(i,j),hij⟩)
    rw [rationalUpperLabels_profile, rationalUpperLabels_profile] at hh
    simpa [spectralMesh] using hh
  have hh := (hrel hlabels).congruence (ratMatrixReal (restore D.vector D.weight b))
  rw [restore_pathMatrix D b S.toList S.nodup_toList (by simpa using haS),
    restore_pathMatrix D b T.toList T.nodup_toList (by simpa using haT)] at hh
  simpa [pathMatrix_eq_information D S.toList S.nodup_toList,
    pathMatrix_eq_information D T.toList T.nodup_toList] using hh

/-- Acceptance gives the same exact information range even without an error
parameter or a positive-definiteness assumption. -/
theorem accepted_same_range (D : FactorData p m M) (b : Finset (Fin M))
    (hi : independent D.vector b) (S T : Finset (Fin m))
    (haS : acceptsSelection D.vector D.weight D.owner b D.atom S)
    (haT : acceptsSelection D.vector D.weight D.owner b D.atom T) :
    LinearMap.range (ratMatrixReal (information D S)).mulVecLin =
      LinearMap.range (ratMatrixReal (information D T)).mulVecLin :=
  (accepted_exact_range D S b hi haS).trans (accepted_exact_range D T b hi haT).symm

theorem relative_information_kernel (D : FactorData p m M) (η : ℚ) (hη : η < 1)
    (S T : Finset (Fin m))
    (h : RelativeSandwich (η : ℝ) (ratMatrixReal (information D S))
      (ratMatrixReal (information D T))) (x : Fin p → ℝ) :
    ratMatrixReal (information D S) *ᵥ x = 0 ↔
      ratMatrixReal (information D T) *ᵥ x = 0 :=
  h.kernel_iff (information_real_psd D S) (information_real_psd D T)
    (by exact_mod_cast hη) x

theorem relative_information_range (D : FactorData p m M) (η : ℚ) (hη : η < 1)
    (S T : Finset (Fin m))
    (h : RelativeSandwich (η : ℝ) (ratMatrixReal (information D S))
      (ratMatrixReal (information D T))) :
    LinearMap.range (ratMatrixReal (information D S)).mulVecLin =
      LinearMap.range (ratMatrixReal (information D T)).mulVecLin := by
  ext x
  exact h.estimable_iff (information_real_psd D S) (information_real_psd D T)
    (by exact_mod_cast hη) x

end MatroidSpectral
