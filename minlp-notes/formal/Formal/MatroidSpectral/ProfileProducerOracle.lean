import Formal.MatroidSpectral.ProfileProducer
import Formal.MatroidSpectral.ProfileLabels
import Formal.MatroidSpectral.DeterminantProfiles
import Formal.MatroidSpectral.InterpolationExecution
import Formal.MatroidSpectral.EliminationBits

namespace MatroidSpectral
open scoped BigOperators

def restrictedWeights {m : ℕ} {κ : Type*} (ground : Finset (Fin m))
    (w : Fin m → κ → ℕ) : Fin m → κ → ℕ :=
  fun e i => if e ∈ ground then w e i else 0

theorem restrictedWeights_le {m : ℕ} {κ : Type*} (ground : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W) :
    ∀ e i, restrictedWeights ground w e i ≤ W := by
  intro e i
  by_cases he : e ∈ ground <;> simp [restrictedWeights, he, hw]

theorem restrictedWeights_profile {m : ℕ} {κ : Type*}
    (ground B : Finset (Fin m)) (w : Fin m → κ → ℕ) (hB : B ⊆ ground) :
    naturalProfile (restrictedWeights ground w) B = naturalProfile w B := by
  funext i
  exact Finset.sum_congr rfl (fun e he => if_pos (hB he))

/-- This computational restriction always keeps all original rows. -/
def zeroColumns {q m : ℕ} (A : RationalRepresentation q m)
    (retained : Finset (Fin m)) : RationalRepresentation q m :=
  fun i e => if e ∈ retained then A i e else 0

theorem zeroColumns_eq {q m : ℕ} (A : RationalRepresentation q m)
    (retained : Finset (Fin m)) :
    zeroColumns A retained = retainedRepresentation A retained := rfl

noncomputable def profileExponents {m : ℕ} {κ : Type*} [Fintype κ]
    (w : Fin m → κ → ℕ) : Fin m → κ →₀ ℕ :=
  fun e => Finsupp.equivFunOnFinite.symm (w e)

@[simp] theorem profileExponents_apply {m : ℕ} {κ : Type*} [Fintype κ]
    (w : Fin m → κ → ℕ) (e : Fin m) (i : κ) : profileExponents w e i = w e i := rfl

theorem baseProfile_exponents {m : ℕ} {κ : Type*} [Fintype κ]
    (w : Fin m → κ → ℕ) (B : Finset (Fin m)) (z : κ → ℕ) :
    baseProfile (profileExponents w) B = Finsupp.equivFunOnFinite.symm z ↔
      naturalProfile w B = z := by
  constructor
  · intro h
    funext i
    have hi := congrArg (fun f : κ →₀ ℕ => f i) h
    simpa [baseProfile, naturalProfile] using hi
  · intro h
    apply Finsupp.ext
    intro i
    simpa [baseProfile, naturalProfile] using congrFun h i

/-- Each coefficient query evaluates a polynomial-sized matrix determinant using
the cached integer determinant algorithm. -/
def profileDeterminantValue {q m : ℕ} {κ : Type*} [Fintype κ]
    (A : RationalRepresentation q m) (w : Fin m → κ → ℕ) (t : κ → ℚ) : ℚ :=
  Elimination.rationalDeterminant
    (A * Matrix.diagonal (fun e => ∏ i, t i ^ w e i) * A.transpose)

/-- Exact tensor interpolation is the support oracle; no base enumeration enters
this executable definition. -/
def profileCoefficientOracle {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (w : Fin m → κ → ℕ) (D : ℕ)
    (z : κ → Fin (D + 1)) (retained : Finset (Fin m)) : Bool :=
  decide (0 < interpolateCoefficientRun D
    (fun t => profileDeterminantValue (zeroColumns A retained) w
      (fun i => interpolationNode (t i))) z)

theorem profileDeterminantValue_eq {q m : ℕ} {κ : Type*} [Fintype κ]
    (A : RationalRepresentation q m) (w : Fin m → κ → ℕ) (t : κ → ℚ) :
    profileDeterminantValue A w t =
      MvPolynomial.eval t (determinantPolynomial A (profileExponents w)) := by
  rw [profileDeterminantValue, Elimination.rationalDeterminant_correct,
    determinantPolynomial_eval]
  rfl

theorem profileCoefficientOracle_spec {q m : ℕ} {κ : Type*}
    [Fintype κ] [DecidableEq κ] (A : RationalRepresentation q m)
    (w : Fin m → κ → ℕ) (D W : ℕ) (hw : ∀ e i, w e i ≤ W)
    (hD : q * W ≤ D) (z : κ → Fin (D + 1)) (retained : Finset (Fin m)) :
    profileCoefficientOracle A w D z retained = true ↔
      Supports (fun B => IsBase A B ∧ naturalProfile w B = fun i => (z i).val) retained := by
  simp only [profileCoefficientOracle, decide_eq_true_eq]
  simp_rw [profileDeterminantValue_eq, zeroColumns_eq]
  rw [interpolateCoefficientRun_eq_coeff D _ (fun a ha i =>
    (determinantPolynomial_support_bound _ _ W hw a ha i).trans hD),
    determinantPolynomial_retained_coeff_pos_iff]
  simp only [baseProfile_exponents, Supports]
  aesop

/-- The full-owner marker is fixed while only ordinary coordinates are scanned. -/
def markedCandidate {q m D : ℕ} {κ : Type*} (forced : Finset (Fin m))
    (hforced : forced.card ≤ q) (z : κ → Fin (D + 1)) :
    Option κ → Fin (max D q + 1)
  | none => ⟨forced.card, Nat.lt_succ_of_le (hforced.trans (Nat.le_max_right _ _))⟩
  | some i => ⟨(z i).val, Nat.lt_succ_of_le
      ((Nat.le_of_lt_succ (z i).isLt).trans (Nat.le_max_left _ _))⟩

def markedProfileOracle {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (z : κ → Fin (q * W + 1))
    (retained : Finset (Fin m)) : Bool :=
  if hf : forced.card ≤ q then
    profileCoefficientOracle A (markedWeight forced (restrictedWeights ground w))
      (max (q * W) q) (markedCandidate forced hf z) (retained ∩ ground)
  else false

def MarkedTarget {q m : ℕ} {κ : Type*} (A : RationalRepresentation q m)
    (ground forced : Finset (Fin m)) (w : Fin m → κ → ℕ)
    (z : κ → ℕ) (B : Finset (Fin m)) : Prop :=
  IsBase A B ∧ B ⊆ ground ∧ forced ⊆ B ∧ naturalProfile w B = z

theorem markedProfileOracle_spec {q m : ℕ} {κ : Type*}
    [Fintype κ] [DecidableEq κ] (A : RationalRepresentation q m)
    (ground forced : Finset (Fin m)) (w : Fin m → κ → ℕ) (W : ℕ)
    (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W)
    (z : κ → Fin (q * W + 1)) (retained : Finset (Fin m)) :
    markedProfileOracle A ground forced w W z retained = true ↔
      Supports (MarkedTarget A ground forced w (fun i => (z i).val)) retained := by
  by_cases hf : forced.card ≤ q
  · rw [markedProfileOracle, dif_pos hf]
    have hweights : ∀ e i, markedWeight forced (restrictedWeights ground w) e i ≤ max W 1 := by
      intro e i
      cases i with
      | none =>
          simp only [markedWeight, Option.elim_none, ownerWeight]
          split <;> omega
      | some i => exact (restrictedWeights_le ground w W hw e i).trans (Nat.le_max_left _ _)
    have hdegree : q * max W 1 ≤ max (q * W) q := by
      rw [mul_max, Nat.mul_one]
    rw [profileCoefficientOracle_spec A _ _ (max W 1) hweights hdegree]
    constructor
    · rintro ⟨B, ⟨hb, hz⟩, hsub⟩
      have hground : B ⊆ ground := hsub.trans Finset.inter_subset_right
      have hforced : forced ⊆ B := by
        apply (ownerProfile_full_iff forced B).mp
        have hnone := congrFun hz none
        simpa [naturalProfile, markedWeight, markedCandidate] using hnone
      have hprofile : naturalProfile w B = fun i => (z i).val := by
        rw [← restrictedWeights_profile ground B w hground]
        funext i
        exact congrFun hz (some i)
      exact ⟨B, ⟨hb, hground, hforced, hprofile⟩,
        hsub.trans Finset.inter_subset_left⟩
    · rintro ⟨B, ⟨hb, hground, hforced, hprofile⟩, hsub⟩
      refine ⟨B, ⟨hb, ?_⟩, Finset.subset_inter hsub hground⟩
      funext i
      cases i with
      | none =>
          simpa [naturalProfile, markedWeight, markedCandidate] using
            (ownerProfile_full_iff forced B).mpr hforced
      | some i =>
          simpa only [markedProfile_some, restrictedWeights_profile ground B w hground,
            markedCandidate] using congrFun hprofile i
  · rw [markedProfileOracle, dif_neg hf]
    simp only [Bool.false_eq_true, false_iff, Supports]
    rintro ⟨B, ⟨hb, _, hforced, _⟩, _⟩
    exact hf ((Finset.card_le_card hforced).trans_eq hb.card)

end MatroidSpectral
