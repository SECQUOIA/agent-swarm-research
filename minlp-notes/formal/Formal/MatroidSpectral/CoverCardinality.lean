import Formal.MatroidSpectral.CoverProducer
import Mathlib.Data.List.Nodup

namespace MatroidSpectral
open DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

theorem trialBasisSet_card_optional {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card) :
    (trialBasisSet A D η b).card ≤
      ((q - (forcedOwners D.owner b).card) * (2 * trialShift p b.card q η) + 1) ^
        (b.card * (b.card + 1) / 2) := by
  unfold trialBasisSet
  split_ifs
  · let xs := profileBases A (trialGround D b) (forcedOwners D.owner b)
      (trialWeights D q η b) (2 * trialShift p b.card q η) (upperCoords b.card)
    have hs : ∀ {B}, B ∈ xs → IsBase A B ∧ B ⊆ trialGround D b ∧
        forcedOwners D.owner b ⊆ B := fun hB =>
      profileBases_sound A (trialGround D b) (forcedOwners D.owner b)
        (trialWeights D q η b) (2 * trialShift p b.card q η) (upperCoords b.card)
        (fun e he i => trialWeights_le D hη hq b hb e he i) hB
    have hn := profileBases_keys_nodup A (trialGround D b) (forcedOwners D.owner b)
      (trialWeights D q η b) (2 * trialShift p b.card q η) (upperCoords b.card)
    have hinj : Set.InjOn (naturalProfile (trialWeights D q η b))
        (xs.toFinset : Set (Finset (Fin m))) := by
      have hi := (List.nodup_map_iff_inj_on (List.Nodup.of_map _ hn)).mp hn
      intro B hB C hC he
      exact hi B (List.mem_toFinset.mp hB) C (List.mem_toFinset.mp hC) he
    have hc := profileFamily_card_le (trialWeights D q η b) xs.toFinset
      (forcedOwners D.owner b) q (2 * trialShift p b.card q η)
      (fun B hB => (hs (List.mem_toFinset.mp hB)).1.card)
      (fun B hB => (hs (List.mem_toFinset.mp hB)).2.2)
      (fun B hB e he i => trialWeights_le D hη hq b hb e
        ((hs (List.mem_toFinset.mp hB)).2.1 (Finset.mem_sdiff.mp he).1) i) hinj
    simpa only [card_upperCoord] using hc
  · simp

theorem trialBasisSet_card {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card) :
    (trialBasisSet A D η b).card ≤
      (2 * q * trialShift p b.card q η + 1) ^ (b.card * (b.card + 1) / 2) := by
  apply (trialBasisSet_card_optional A D hη hq b hb).trans
  apply Nat.pow_le_pow_left
  have h := Nat.mul_le_mul_right (2 * trialShift p b.card q η)
    (Nat.sub_le q (forcedOwners D.owner b).card)
  nlinarith

theorem zeroBasisSet_card {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) : (zeroBasisSet A D).card ≤ 1 := by
  unfold zeroBasisSet
  split_ifs
  · apply (List.toFinset_card_le _).trans
    simpa using profileBases_length A (zeroGround D) ∅ (fun _ (_ : Fin 0) => 0) 0 []
  · simp

def matroidCoverCardinality (p M q : ℕ) (η : ℚ) : ℕ :=
  1 + ∑ r : Fin p, M.choose (r.val + 1) *
    (2 * q * ⌈4 * (p : ℚ) * (r.val + 1) * q / η⌉₊ + 1) ^
      ((r.val + 1) * (r.val + 2) / 2)

theorem spectralBasisSet_card {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) :
    (spectralBasisSet A D η).card ≤ matroidCoverCardinality p M q η := by
  unfold spectralBasisSet
  split_ifs with hq
  · simp only [Finset.card_singleton,matroidCoverCardinality]
    omega
  · apply (Finset.card_union_le _ _).trans
    apply Nat.add_le_add (zeroBasisSet_card A D)
    apply Finset.card_biUnion_le.trans
    apply Finset.sum_le_sum
    intro r _
    apply Finset.card_biUnion_le.trans
    calc
      _ ≤ ∑ _b ∈ trials D.vector (r.val + 1),
          (2 * q * ⌈4 * (p : ℚ) * (r.val + 1) * q / η⌉₊ + 1) ^
            ((r.val + 1) * (r.val + 2) / 2) := by
        apply Finset.sum_le_sum
        intro b hb
        have hc := ((mem_trials D.vector _ b).mp hb).1
        simpa only [hc,trialShift_eq,Nat.cast_add,Nat.cast_one,Nat.add_assoc] using
          trialBasisSet_card A D hη (Nat.pos_of_ne_zero hq) b (by omega)
      _ ≤ _ := by
        simp only [Finset.sum_const,nsmul_eq_mul]
        exact Nat.mul_le_mul_right _ (trial_count D.vector _)

end MatroidSpectral
