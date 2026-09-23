import Formal.MatroidSpectral.ProfileProducerBases
import Formal.MatroidSpectral.ProfileCardinality
import Formal.MatroidSpectral.TrialLabels
import Formal.MatroidSpectral.SpectralCover

namespace MatroidSpectral
open DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

def trialBasisSet {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) : Finset (Finset (Fin m)) :=
  if acceptsAtomCode D.vector D.weight b (D.atom none) then
    (profileBases A (trialGround D b) (forcedOwners D.owner b)
      (trialWeights D q η b) (2 * trialShift p b.card q η) (upperCoords b.card)).toFinset
  else ∅

def zeroGround {p m M : ℕ} (D : FactorData p m M) : Finset (Fin m) :=
  Finset.univ.filter (fun e => D.atom (some e) = 0)

def zeroBasisSet {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) : Finset (Finset (Fin m)) :=
  if D.atom none = 0 then
    (profileBases A (zeroGround D) ∅ (fun _ (_ : Fin 0) => 0) 0 []).toFinset
  else ∅

def spectralBasisSet {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) : Finset (Finset (Fin m)) :=
  if q = 0 then {∅} else zeroBasisSet A D ∪
    Finset.univ.biUnion (fun r : Fin p =>
      (trials D.vector (r.val + 1)).biUnion (trialBasisSet A D η))

theorem trialBasisSet_sound {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card) {B : Finset (Fin m)}
    (hB : B ∈ trialBasisSet A D η b) :
    IsBase A B ∧ acceptsSelection D.vector D.weight D.owner b D.atom B := by
  unfold trialBasisSet at hB
  split_ifs at hB with hprior
  · obtain ⟨hbase,hground,hforced⟩ := profileBases_sound A _ _ _ _ _
      (fun e he i => trialWeights_le D hη hq b hb e he i) (List.mem_toFinset.mp hB)
    exact ⟨hbase,hforced,(acceptsAtomCode_iff _ _ _ _).mp hprior,
      fun e he => (mem_trialGround D b e).mp (hground he)⟩
  · simp at hB

theorem trialBasisSet_complete {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card) {B : Finset (Fin m)}
    (hbase : IsBase A B)
    (ha : acceptsSelection D.vector D.weight D.owner b D.atom B) :
    ∃ C ∈ trialBasisSet A D η b,
      acceptsSelection D.vector D.weight D.owner b D.atom C ∧
      trialProfile D η q b B = trialProfile D η q b C := by
  have hground : B ⊆ trialGround D b := fun e he => (mem_trialGround D b e).mpr (ha.2.2 e he)
  obtain ⟨C,hC,hprof⟩ := profileBases_complete A _ _ _ _ _
    (fun e he i => trialWeights_le D hη hq b hb e he i)
    mem_upperCoords hbase hground ha.1
  have hC' : C ∈ trialBasisSet A D η b := by
    simp only [trialBasisSet, if_pos ((acceptsAtomCode_iff _ _ _ _).mpr ha.2.1)]
    exact List.mem_toFinset.mpr hC
  obtain ⟨hbaseC,haC⟩ := trialBasisSet_sound A D hη hq b hb hC'
  refine ⟨C,hC',haC,?_⟩
  have hh := (trialWeights_profile_iff D hη hq b hb C B
    (hbaseC.card.trans hbase.card.symm)
    (fun e he => (mem_trialGround D b e).mpr (haC.2.2 e he)) hground).mp hprof
  funext i
  simpa [trialProfile, signedProfile, trialSigned] using (congrFun hh i).symm

theorem zeroBasisSet_sound {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {B : Finset (Fin m)} (hB : B ∈ zeroBasisSet A D) :
    IsBase A B ∧ selectedRank D B = 0 := by
  unfold zeroBasisSet at hB
  split_ifs at hB with hprior
  · obtain ⟨hb,hground,_⟩ := profileBases_sound A _ _ _ _ _
      (fun _ _ i => Fin.elim0 i) (List.mem_toFinset.mp hB)
    refine ⟨hb,(selectedRank_zero_iff D B).mpr ⟨hprior,?_⟩⟩
    intro e he
    exact (Finset.mem_filter.mp (hground he)).2
  · simp at hB

theorem zeroBasisSet_complete {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {B : Finset (Fin m)} (hb : IsBase A B)
    (hz : selectedRank D B = 0) :
    ∃ C ∈ zeroBasisSet A D, selectedRank D C = 0 := by
  obtain ⟨hprior,he⟩ := (selectedRank_zero_iff D B).mp hz
  obtain ⟨C,hC,_⟩ := profileBases_complete A (zeroGround D) ∅
    (fun _ (_ : Fin 0) => 0) 0 [] (fun _ _ i => Fin.elim0 i)
    (fun i => Fin.elim0 i) hb
    (fun e h => Finset.mem_filter.mpr ⟨Finset.mem_univ _, he e h⟩) (Finset.empty_subset _)
  have hm : C ∈ zeroBasisSet A D := by
    simp only [zeroBasisSet, if_pos hprior]
    exact List.mem_toFinset.mpr hC
  exact ⟨C,hm,(zeroBasisSet_sound A D hm).2⟩

theorem spectralBasisSet_sound {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) {B : Finset (Fin m)}
    (hB : B ∈ spectralBasisSet A D η) : IsBase A B := by
  unfold spectralBasisSet at hB
  split_ifs at hB with hq
  · subst q
    exact (isBase_zero_iff A B).mpr (Finset.mem_singleton.mp hB)
  · rcases Finset.mem_union.mp hB with hz | hp
    · exact (zeroBasisSet_sound A D hz).1
    · obtain ⟨r,_,hp⟩ := Finset.mem_biUnion.mp hp
      obtain ⟨b,hb,hB⟩ := Finset.mem_biUnion.mp hp
      have hc := ((mem_trials D.vector _ b).mp hb).1
      exact (trialBasisSet_sound A D hη (Nat.pos_of_ne_zero hq) b (by omega) hB).1

theorem spectralBasisSet_isRelativeCover {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) :
    IsRelativeCover (η : ℝ) (fun B => ratMatrixReal (information D B))
      (bases A) (spectralBasisSet A D η) := by
  have hs : spectralBasisSet A D η ⊆ bases A :=
    fun _ h => mem_bases.mpr (spectralBasisSet_sound A D hη h)
  by_cases hq : q = 0
  · subst q
    apply zero_cardinality_cover D η hη.le _ _
      (fun B hB => (mem_bases.mp hB).card) hs
    intro _
    simp [spectralBasisSet]
  · apply finite_family_spectral_cover D η hη q (Nat.pos_of_ne_zero hq) _ _
      (fun B hB => (mem_bases.mp hB).card.le) hs
    · intro B hB hz
      obtain ⟨C,hC,hzC⟩ := zeroBasisSet_complete A D (mem_bases.mp hB) hz
      exact ⟨C,by simp [spectralBasisSet,hq,hC],hzC⟩
    · intro r hr hrp b hb B hB ha
      have hc := ((mem_trials D.vector r b).mp hb).1
      obtain ⟨C,hC,haC,hprof⟩ := trialBasisSet_complete A D hη
        (Nat.pos_of_ne_zero hq) b (by omega) (mem_bases.mp hB) ha
      refine ⟨C,?_,haC,hprof⟩
      rw [spectralBasisSet, if_neg hq]
      apply Finset.mem_union_right
      apply Finset.mem_biUnion.mpr
      refine ⟨⟨r-1,by omega⟩,Finset.mem_univ _,?_⟩
      apply Finset.mem_biUnion.mpr
      exact ⟨b,by simpa only [show r-1+1=r by omega] using hb,hC⟩

end MatroidSpectral
