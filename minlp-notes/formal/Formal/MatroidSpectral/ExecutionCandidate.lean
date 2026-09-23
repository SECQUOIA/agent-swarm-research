import Formal.MatroidSpectral.ExecutionZero
import Formal.MatroidSpectral.ExecutionCoordinates
import Formal.MatroidSpectral.NormalizationEnumeration
import Formal.MatroidSpectral.ExecutionTrialLabels

namespace MatroidSpectral.Execution
open DAGSpectral DAGSpectral.NormalizationTrials ReciprocalAnchor

def preparedGround {p m r : ℕ} (trial : PreparedTrial p m r) : Finset (Fin m) :=
  Finset.univ.filter (fun e => (trial.cache.atoms.get e).accepted = true)

def preparedWeights {p m r : ℕ} (trial : PreparedTrial p m r) (shift : ℕ) :
    Fin m → UpperCoord r → ℕ :=
  shiftedWeight (fun e => (trial.cache.labels.get e).value) shift

theorem preparedGround_value {p m M : ℕ} (D : FactorData p m M) (η : ℚ)
    (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    preparedGround (prepareTrialRun D η q b B).1 = trialGround D b := by
  simp only [preparedGround, prepareTrialRun_allowed, trialGround]

theorem preparedWeights_value {p m M : ℕ} (D : FactorData p m M) (η : ℚ)
    (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    preparedWeights (prepareTrialRun D η q b B).1 (trialShift p b.card q η) =
      trialWeights D q η b := by
  simp only [preparedWeights, prepareTrialRun_signed, trialWeights]

def candidateRun {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B : ℕ) :
    List (Finset (Fin m)) × ℕ :=
  let preparation := prepareTrialRun D η q b B
  let shift := trialShiftRun p b.card q η B
  let weights := shiftedWeightsCacheRun
    (fun e => (preparation.1.cache.labels.get e).value) shift.1
  let work := preparation.2 + shift.2 + weights.2 +
    columnWork m + b.card * (b.card + 1) + 1
  if preparation.1.independent && preparation.1.cache.prior.accepted then
    let result := profileBasesRun A (preparedGround preparation.1) preparation.1.required
      (readWeightCache weights.1) (2 * shift.1) B (upperCoords b.card)
    (result.1, work + result.2)
  else ([], work)

theorem candidateRun_value {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B : ℕ) :
    (candidateRun A D η b B).1.toFinset =
      if independent D.vector b then trialBasisSet A D η b else ∅ := by
  simp only [candidateRun, prepareTrialRun_independent, prepareTrialRun_prior,
    trialShiftRun_value, shiftedWeightsCacheRun_value, readWeightCache_value,
    prepareTrialRun_signed, Bool.and_eq_true, decide_eq_true_eq]
  by_cases hi : independent D.vector b <;>
    by_cases hp : acceptsAtomCode D.vector D.weight b (D.atom none) <;>
    simp only [hi, hp, and_self, false_and, and_false, ↓reduceIte, List.toFinset_nil,
      profileBasesRun_value, preparedGround_value,
      prepareTrialRun_required, trialBasisSet, trialWeights]

def candidateCapacity (q p r : ℕ) (η : ℚ) : ℕ :=
  (q * (2 * trialShift p r q η) + 1) ^ (r * (r + 1) / 2)

theorem candidateRun_length {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B : ℕ) :
    (candidateRun A D η b B).1.length ≤ candidateCapacity q p b.card η := by
  simp only [candidateRun, trialShiftRun_value, shiftedWeightsCacheRun_value,
    readWeightCache_value, prepareTrialRun_signed, preparedGround_value,
    prepareTrialRun_required, prepareTrialRun_independent, prepareTrialRun_prior]
  split
  · simp only [profileBasesRun_value]
    simpa only [candidateCapacity, upperCoords_length] using
      profileBases_length A (trialGround D b) (forcedOwners D.owner b)
        (shiftedWeight (trialSigned D q η b) (trialShift p b.card q η))
        (2 * trialShift p b.card q η) (upperCoords b.card)
  · exact Nat.zero_le _

def candidateWorkBound (q p m M r B : ℕ) (η : ℚ) : ℕ :=
  normalizationWorkBound p m M r q B + trialShiftWork p r q B +
    trialWeightCacheWork p m r q B +
    columnWork m + r * (r + 1) + 1 +
    profileWorkBound q m (r * (r + 1) / 2) (2 * trialShift p r q η)
      (markedQueryWork q m (r * (r + 1) / 2) (2 * trialShift p r q η) B)

theorem candidateRun_work {q p m M B : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (hq : 0 < q)
    (b : Finset (Fin M)) (hb : 0 < b.card)
    (hA : MatrixBits A B) (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B) (hD : ∀ o, MatrixBits (D.atom o) B)
    (hηB : RationalBits η B) (hsize : b.card + q + 2 ≤ B) :
    (candidateRun A D η b B).2 ≤ candidateWorkBound q p m M b.card B η := by
  have hp := prepareTrialRun_work D b hV hw hD hηB hsize
  have hs := trialShiftRun_work p b.card q hηB
  have hc := shiftedWeightsCacheRun_work (trialSigned D q η b)
    (trialShift p b.card q η) (trialSignedBits p b.card q B)
    (trialShiftBits p b.card q B + 1)
    (trialSigned_integerBits D b hV hw hD hηB) (trialShift_integerBits p b.card q hηB)
  simp only [card_upperCoord] at hc
  have hr := profileBasesRun_work A (trialGround D b) (forcedOwners D.owner b)
    (trialWeights D q η b) (2 * trialShift p b.card q η) B (upperCoords b.card)
    (by rw [upperCoords_length, card_upperCoord]) hA
    (fun e he i => trialWeights_le D hη hq b hb e he i)
  simp only [card_upperCoord, trialWeights] at hr
  simp only [candidateRun, trialShiftRun_value, shiftedWeightsCacheRun_value,
    readWeightCache_value, prepareTrialRun_signed, preparedGround_value,
    prepareTrialRun_required, candidateWorkBound, trialWeightCacheWork]
  split <;> omega

end MatroidSpectral.Execution
