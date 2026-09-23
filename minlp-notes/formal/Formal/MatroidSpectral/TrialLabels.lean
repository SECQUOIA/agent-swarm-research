import Formal.MatroidSpectral.ProfileLabels
import Formal.DAGSpectral.CoverCardinality

namespace MatroidSpectral
open DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

def trialShift (p r q : ℕ) (η : ℚ) : ℕ := ⌈4 * (p : ℚ) / (η / (r * q))⌉₊

theorem trialShift_eq (p r q : ℕ) (η : ℚ) :
    trialShift p r q η = ⌈4 * (p : ℚ) * r * q / η⌉₊ := by
  unfold trialShift
  congr 1
  simp only [div_div_eq_mul_div]
  ring

def trialSigned {p m M : ℕ} (D : FactorData p m M) (q : ℕ) (η : ℚ)
    (b : Finset (Fin M)) : Fin m → UpperCoord b.card → ℤ :=
  rationalUpperLabels (η / (b.card * q : ℚ)) (fun e => trialAtom D b (some e))

def trialWeights {p m M : ℕ} (D : FactorData p m M) (q : ℕ) (η : ℚ)
    (b : Finset (Fin M)) : Fin m → UpperCoord b.card → ℕ :=
  shiftedWeight (trialSigned D q η b) (trialShift p b.card q η)

def trialGround {p m M : ℕ} (D : FactorData p m M)
    (b : Finset (Fin M)) : Finset (Fin m) :=
  Finset.univ.filter (fun e => trialAllowed D b e = true)

@[simp] theorem mem_trialGround {p m M : ℕ} (D : FactorData p m M)
    (b : Finset (Fin M)) (e : Fin m) :
    e ∈ trialGround D b ↔ acceptsAtom D.vector D.weight b (D.atom (some e)) := by
  simp only [trialGround, Finset.mem_filter, Finset.mem_univ, true_and,
    trialAllowed, decide_eq_true_eq, acceptsAtomCode_iff]

theorem trialSigned_bounds {p m M q : ℕ} (D : FactorData p m M)
    {η : ℚ} (hη : 0 < η) (hq : 0 < q) (b : Finset (Fin M)) (hb : 0 < b.card)
    (e : Fin m) (he : e ∈ trialGround D b) (i : UpperCoord b.card) :
    -(trialShift p b.card q η : ℤ) ≤ trialSigned D q η b e i ∧
      trialSigned D q η b e i ≤ (trialShift p b.card q η : ℤ) := by
  have hh : 0 < η / (b.card * q : ℚ) := by positivity
  have ha := trialAtom_entry_bound D b e ((Finset.mem_filter.mp he).2)
    (upperCoordEquiv b.card i).val.1 (upperCoordEquiv b.card i).val.2
  have ha' : |trialAtom D b (some e) (upperCoordEquiv b.card i).val.1
      (upperCoordEquiv b.card i).val.2| ≤ 4 * p := by
    simp only [ratMatrixReal_apply] at ha
    exact_mod_cast ha
  exact floorLabel_bounds hh p ha'

theorem trialWeights_le {p m M q : ℕ} (D : FactorData p m M)
    {η : ℚ} (hη : 0 < η) (hq : 0 < q) (b : Finset (Fin M)) (hb : 0 < b.card)
    (e : Fin m) (he : e ∈ trialGround D b) (i : UpperCoord b.card) :
    trialWeights D q η b e i ≤ 2 * trialShift p b.card q η :=
  shiftedWeight_le _ _ _ _ (trialSigned_bounds D hη hq b hb e he i).2

theorem trialWeights_profile_iff {p m M q : ℕ} (D : FactorData p m M)
    {η : ℚ} (hη : 0 < η) (hq : 0 < q) (b : Finset (Fin M)) (hb : 0 < b.card)
    (B C : Finset (Fin m)) (hc : B.card = C.card)
    (hB : B ⊆ trialGround D b) (hC : C ⊆ trialGround D b) :
    naturalProfile (trialWeights D q η b) B = naturalProfile (trialWeights D q η b) C ↔
      signedProfile (trialSigned D q η b) B = signedProfile (trialSigned D q η b) C :=
  shiftedProfile_eq_iff _ _ B C hc
    (fun e he i => (trialSigned_bounds D hη hq b hb e (hB he) i).1)
    (fun e he i => (trialSigned_bounds D hη hq b hb e (hC he) i).1)

theorem trial_profile_bound {p m M q : ℕ} (D : FactorData p m M)
    {η : ℚ} (hη : 0 < η) (hq : 0 < q) (b : Finset (Fin M)) (hb : 0 < b.card)
    (B : Finset (Fin m)) (hc : B.card = q) (hB : B ⊆ trialGround D b)
    (i : UpperCoord b.card) :
    naturalProfile (trialWeights D q η b) B i ≤ 2 * q * trialShift p b.card q η := by
  have h := naturalProfile_le (trialWeights D q η b) B (2 * trialShift p b.card q η)
    (fun e he i => trialWeights_le D hη hq b hb e (hB he) i) i
  rw [hc] at h
  convert h using 1
  ring

end MatroidSpectral
