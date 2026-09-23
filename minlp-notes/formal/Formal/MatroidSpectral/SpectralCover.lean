import Formal.MatroidSpectral.SpectralApproximation
import Formal.DAGSpectral.CriteriaBasic

/-! The finite-family cover argument, separated from how representatives are
computed. The represented-matroid producer must discharge the explicitly stated
profile completeness and feasibility hypotheses below. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

variable {p m M : ℕ}

theorem information_zero_of_selectedRank_zero (D : FactorData p m M)
    (S : Finset (Fin m)) (h : selectedRank D S = 0) : information D S = 0 := by
  obtain ⟨h0,he⟩ := (selectedRank_zero_iff D S).mp h
  simp [information,h0,Finset.sum_eq_zero he]

theorem information_self_sandwich (D : FactorData p m M)
    (η : ℚ) (hη : 0 ≤ η) (S : Finset (Fin m)) :
    RelativeSandwich (η : ℝ) (ratMatrixReal (information D S))
      (ratMatrixReal (information D S)) := by
  have hηr : 0 ≤ (η : ℝ) := by exact_mod_cast hη
  constructor
  · simpa only [one_smul] using psd_smul_mono (information_real_psd D S)
      (show 1 - (η : ℝ) ≤ 1 by linarith)
  · simpa only [one_smul] using psd_smul_mono (information_real_psd D S)
      (show 1 ≤ 1 + (η : ℝ) by linarith)

/-- Cardinality zero means the unique selected set is empty. The prior need not
be zero; returning that same set gives the relative bound. -/
theorem zero_cardinality_cover (D : FactorData p m M) (η : ℚ) (hη : 0 ≤ η)
    (F C : Finset (Finset (Fin m))) (hcard : ∀ S ∈ F, S.card = 0)
    (hsound : C ⊆ F) (hempty : ∅ ∈ F → ∅ ∈ C) :
    IsRelativeCover (η : ℝ) (fun S => ratMatrixReal (information D S)) F C := by
  refine ⟨hsound,?_⟩
  intro S hS
  have he := Finset.card_eq_zero.mp (hcard S hS)
  subst S
  exact ⟨∅,hempty hS,information_self_sandwich D η hη ∅⟩

/-- Every positive information-rank target admits an enumerated normalization
and therefore a representative. The max-volume argument is proved by
`exists_accepted_trial`, rather than assumed as an oracle. -/
theorem finite_family_spectral_cover (D : FactorData p m M)
    (η : ℚ) (hη : 0 < η) (q : ℕ) (hq : 0 < q)
    (F C : Finset (Finset (Fin m))) (hcard : ∀ S ∈ F, S.card ≤ q)
    (hsound : C ⊆ F)
    (hzero : ∀ S ∈ F, selectedRank D S = 0 →
      ∃ T ∈ C, selectedRank D T = 0)
    (hprofiles : ∀ (r : ℕ), 0 < r → r ≤ p →
      ∀ b ∈ trials D.vector r, ∀ S ∈ F,
        acceptsSelection D.vector D.weight D.owner b D.atom S →
        ∃ T ∈ C, acceptsSelection D.vector D.weight D.owner b D.atom T ∧
          trialProfile D η q b S = trialProfile D η q b T) :
    IsRelativeCover (η : ℝ) (fun S => ratMatrixReal (information D S)) F C := by
  refine ⟨hsound,?_⟩
  intro S hS
  by_cases hz : selectedRank D S = 0
  · obtain ⟨T,hT,hzT⟩ := hzero S hS hz
    refine ⟨T,hT,?_⟩
    dsimp only
    rw [information_zero_of_selectedRank_zero D S hz,
      information_zero_of_selectedRank_zero D T hzT]
    simp [RelativeSandwich,Loewner,Matrix.PosSemidef.zero]
  · obtain ⟨b,hb,ha,_⟩ := exists_accepted_trial D S
    have hr : 0 < selectedRank D S := Nat.pos_of_ne_zero hz
    obtain ⟨T,hT,haT,hprof⟩ := hprofiles (selectedRank D S) hr
      (selectedRank_le D S) b hb S hS ha
    obtain ⟨hc,hi⟩ := (mem_trials D.vector (selectedRank D S) b).mp hb
    exact ⟨T,hT,accepted_same_profile_sandwich D η hη q hq b (hc.symm ▸ hr)
      hi S T (hcard S hS) (hcard T (hsound hT)) ha haT hprof⟩

/-- The singular case has the same exact kernel as its representative. -/
theorem finite_family_cover_kernel (D : FactorData p m M)
    (η : ℚ) (hη : η < 1) (F C : Finset (Finset (Fin m)))
    (hcover : IsRelativeCover (η : ℝ) (fun S => ratMatrixReal (information D S)) F C)
    (S : Finset (Fin m)) (hS : S ∈ F) :
    ∃ T ∈ C, T ∈ F ∧
      RelativeSandwich (η : ℝ) (ratMatrixReal (information D S))
        (ratMatrixReal (information D T)) ∧
      ∀ x : Fin p → ℝ, ratMatrixReal (information D S) *ᵥ x = 0 ↔
        ratMatrixReal (information D T) *ᵥ x = 0 := by
  obtain ⟨T,hT,hrel⟩ := hcover.2 S hS
  exact ⟨T,hT,hcover.1 hT,hrel,relative_information_kernel D η hη S T hrel⟩

end MatroidSpectral
