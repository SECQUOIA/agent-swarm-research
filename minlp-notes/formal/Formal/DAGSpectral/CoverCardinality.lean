import Formal.DAGSpectral.CoverProducer
import Formal.DAGSpectral.ProfileSpectralDP
import Formal.DAGSpectral.PSDEntries

namespace DAGSpectral
open Matrix
open scoped BigOperators
namespace NormalizationTrials
noncomputable section
variable {v m p M : ℕ}

theorem rationalUpperLabels_eq_spectral {m r : ℕ} (η : ℚ) (N : ℕ)
    (A : Fin m → Matrix (Fin r) (Fin r) ℚ) :
    rationalUpperLabels (η / (r*N : ℚ)) A =
      ExplicitDAG.spectralLabels
        (fun e z => ratMatrixReal (A e) (upperCoordEquiv r z).val.1
          (upperCoordEquiv r z).val.2) (η : ℝ) r N := by
  funext e z
  simp only [rationalUpperLabels, ExplicitDAG.spectralLabels, spectralMesh,
    ratMatrixReal_apply]
  simpa only [Rat.cast_div, Rat.cast_mul, Rat.cast_natCast] using
    (floorLabel_ratCast (η / (r*N : ℚ))
      (A e (upperCoordEquiv r z).val.1 (upperCoordEquiv r z).val.2)).symm

/-- Every retained rank-r trial has the explicit signed-profile state bound. -/
theorem trialPathSet_card_of_entry_bound (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (b : Finset (Fin M)) (hb : 0 < b.card)
    (hentry : ∀ e, trialAllowed D b e = true → ∀ i j,
      |ratMatrixReal (trialAtom D b (some e)) i j| ≤ 4 * p) :
    (trialPathSet G s t D η b).card ≤
      2^b.card * coordinateCount p b.card (max 1 (v-1)) (η : ℝ) ^
        (b.card*(b.card+1)/2) := by
  unfold trialPathSet
  split_ifs
  · apply (List.toFinset_card_le _).trans
    rw [rationalUpperLabels_eq_spectral]
    have hh := G.spectral_dp_bounds (trialAllowed D b) s t (forcedOwners D.owner b)
      (fun e z => ratMatrixReal (trialAtom D b (some e))
        (upperCoordEquiv b.card z).val.1 (upperCoordEquiv b.card z).val.2)
      p b.card (max 1 (v-1)) (η : ℝ) hb (by omega) (by exact_mod_cast hη)
      (by omega) (forcedOwners_card D.owner b)
      (fun e he z => hentry e he _ _)
    simpa only [card_upperCoord] using hh.2.2
  · simp

theorem zeroPathSet_card (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) :
    (zeroPathSet G s t D).card ≤ 1 := by
  unfold zeroPathSet
  split_ifs
  · exact (List.toFinset_card_le _).trans (by simp [List.length_take])
  · simp

/-- This is the claimed finite-dimensional count with N=max(1,v-1). -/
def coverCardinalityBound (p M N : ℕ) (η : ℝ) : ℕ :=
  1 + ∑ r : Fin p, M.choose (r.val+1) *
    (2^(r.val+1) * coordinateCount p (r.val+1) N η ^ ((r.val+1)*(r.val+2)/2))

theorem spectralPathSet_card_of_entry_bound (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η)
    (hentry : ∀ b : Finset (Fin M), ∀ e, trialAllowed D b e = true → ∀ i j,
      |ratMatrixReal (trialAtom D b (some e)) i j| ≤ 4 * p) :
    (spectralPathSet G s t D η).card ≤ coverCardinalityBound p M (max 1 (v-1)) η := by
  unfold spectralPathSet
  split_ifs
  · simp only [Finset.card_singleton, coverCardinalityBound]
    omega
  · apply (Finset.card_union_le _ _).trans
    apply Nat.add_le_add (zeroPathSet_card G s t D)
    apply (Finset.card_biUnion_le).trans
    apply Finset.sum_le_sum
    intro r _
    apply (Finset.card_biUnion_le).trans
    calc
      ∑ b ∈ trials D.vector (r.val+1), (trialPathSet G s t D η b).card ≤
          ∑ b ∈ trials D.vector (r.val+1),
            (2^(r.val+1) * coordinateCount p (r.val+1) (max 1 (v-1)) (η:ℝ) ^
              ((r.val+1)*(r.val+2)/2)) := by
        apply Finset.sum_le_sum
        intro b hb
        have hcard := ((mem_trials D.vector _ b).mp hb).1
        simpa only [hcard, Nat.add_assoc] using
          trialPathSet_card_of_entry_bound G s t D hη b (by omega) (hentry b)
      _ ≤ _ := by
        simp only [Finset.sum_const, nsmul_eq_mul]
        exact Nat.mul_le_mul_right _ (trial_count D.vector _)

/-- Positivity and the actual diagonal filter supply the entry bound used by the DP. -/
theorem trialAtom_entry_bound (D : FactorData p m M) (b : Finset (Fin M))
    (e : Fin m) (he : trialAllowed D b e = true) (i j : Fin b.card) :
    |ratMatrixReal (trialAtom D b (some e)) i j| ≤ 4 * p := by
  have ha : acceptsAtomCode D.vector D.weight b (D.atom (some e)) :=
    of_decide_eq_true he
  have hh := normalized_abs_entry_le_four_p (D.atom (some e)) (atom_real_psd D (some e))
    (transformCode D.vector D.weight b) ha.2 i j
  change |((trialAtom D b (some e) i j : ℚ) : ℝ)| ≤ _
  exact_mod_cast hh

/-- Cardinality of the produced path set, with no external entry-bound assumption. -/
theorem spectralPathSet_card (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) :
    (spectralPathSet G s t D η).card ≤ coverCardinalityBound p M (max 1 (v-1)) η :=
  spectralPathSet_card_of_entry_bound G s t D hη (trialAtom_entry_bound D)

theorem spectralPathSet_path_length (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) {es : List (Fin m)}
    (he : es ∈ spectralPathSet G s t D η) : es.length ≤ max 1 (v-1) :=
  (spectralPathSet_sound G s t D η he).length_le_vertices.trans (Nat.le_max_right _ _)

end
end NormalizationTrials
end DAGSpectral
