import Formal.MatroidSpectral.SpectralApproximation

/-! Cancellation of forced elements and the sharp optional-cardinality error.
The zero-optional-element branch is an equality, not a strict `0 < 0` bound. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

variable {p m M : ℕ}

theorem trialProfile_remove_common (D : FactorData p m M) (η : ℚ) (q : ℕ)
    (b : Finset (Fin M)) (S T F : Finset (Fin m)) (hFS : F ⊆ S) (hFT : F ⊆ T) :
    trialProfile D η q b S = trialProfile D η q b T ↔
      trialProfile D η q b (S \ F) = trialProfile D η q b (T \ F) := by
  have hs : trialProfile D η q b (S \ F) + trialProfile D η q b F =
      trialProfile D η q b S := Finset.sum_sdiff hFS
  have ht : trialProfile D η q b (T \ F) + trialProfile D η q b F =
      trialProfile D η q b T := Finset.sum_sdiff hFT
  rw [← hs,← ht,add_left_inj]

theorem pathMatrix_partition {r : ℕ} (A0 : RealMatrix r) (A : Fin m → RealMatrix r)
    (S F : Finset (Fin m)) (hFS : F ⊆ S) :
    pathMatrix (pathMatrix A0 A F.toList) A (S \ F).toList = pathMatrix A0 A S.toList := by
  simp only [pathMatrix]
  have hs := Finset.sum_sdiff hFS (f := A)
  have hsum (E : Finset (Fin m)) : (E.toList.map A).sum = ∑ e ∈ E, A e := by simp
  rw [hsum F,hsum (S \ F),hsum S]
  rw [add_assoc,add_comm (∑ e ∈ F, A e),hs]

theorem forced_full_cardinality_eq (S T F : Finset (Fin m))
    (hFS : F ⊆ S) (hFT : F ⊆ T) (hS : S.card = F.card) (hT : T.card = F.card) :
    S = T :=
  (Finset.eq_of_subset_of_card_le hFS hS.le).symm.trans
    (Finset.eq_of_subset_of_card_le hFT hT.le)

theorem same_profile_optional_entry_bound (D : FactorData p m M)
    (η : ℚ) (hη : 0 < η) (q : ℕ) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card)
    (S T F : Finset (Fin m)) (hFS : F ⊆ S) (hFT : F ⊆ T)
    (hS : S.card = q) (hT : T.card = q) (hopt : 0 < q - F.card)
    (hprofile : trialProfile D η q b S = trialProfile D η q b T) :
    ∀ i j, |(ratMatrixReal (transform D.vector D.weight b * information D T *
        (transform D.vector D.weight b)ᵀ) -
      ratMatrixReal (transform D.vector D.weight b * information D S *
        (transform D.vector D.weight b)ᵀ)) i j| <
      (q - F.card : ℕ) * ((η / (b.card * q : ℚ) : ℚ) : ℝ) := by
  let A := fun e => ratMatrixReal (trialAtom D b (some e))
  let A0 := ratMatrixReal (trialAtom D b none)
  have hh : (0 : ℝ) < ((η / (b.card * q : ℚ) : ℚ) : ℝ) := by
    exact_mod_cast (div_pos hη (mul_pos (Nat.cast_pos.mpr hb) (Nat.cast_pos.mpr hq)))
  have hp := (trialProfile_remove_common D η q b S T F hFS hFT).mp hprofile
  have hlabels : ∀ i j : Fin b.card, i ≤ j →
      pathLabel ((η / (b.card * q : ℚ) : ℚ) : ℝ)
        ((S \ F).toList.map (fun e => A e i j)) =
      pathLabel ((η / (b.card * q : ℚ) : ℚ) : ℝ)
        ((T \ F).toList.map (fun e => A e i j)) := by
    intro i j hij
    rw [trialProfile_eq_list,trialProfile_eq_list] at hp
    have he := congrFun hp ((upperCoordEquiv b.card).symm ⟨(i,j),hij⟩)
    rw [rationalUpperLabels_profile,rationalUpperLabels_profile] at he
    exact he
  have ha : ∀ e, (A e).IsHermitian := fun e => (trialAtom_psd D b (some e)).isHermitian
  have he := pathMatrix_entry_close
    (pathMatrix_hermitian (trialAtom_psd D b none).isHermitian ha F.toList) ha
    hh hopt (S \ F).toList (T \ F).toList
    (by simp [Finset.card_sdiff_of_subset hFS,hS])
    (by simp [Finset.card_sdiff_of_subset hFT,hT]) hlabels
  rw [pathMatrix_partition A0 A T F hFT,pathMatrix_partition A0 A S F hFS] at he
  dsimp only [A0,A] at he
  simp only [trialAtom,transformCode_eq] at he
  rw [transformed_pathMatrix_eq D b T.toList T.nodup_toList,
    transformed_pathMatrix_eq D b S.toList S.nodup_toList] at he
  simpa using he

end MatroidSpectral
