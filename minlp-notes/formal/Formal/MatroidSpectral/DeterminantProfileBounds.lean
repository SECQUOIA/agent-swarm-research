import Formal.MatroidSpectral.DeterminantProfiles
import Formal.MatroidSpectral.ProfileLabels

/-! Sharper bounds for the owner marker and the optional part of a profile.
The interpolation algorithm may safely use a larger uniform grid bound. -/
namespace MatroidSpectral
open scoped BigOperators

/-- The marker counts distinct forced owners, so its degree is at most their
number even if the represented rank is much larger. -/
theorem determinantPolynomial_owner_degree {q m : ℕ} {κ : Type*}
    (A : RationalRepresentation q m) (F : Finset (Fin m))
    (w : Fin m → Option κ →₀ ℕ) (hw : ∀ e, w e none = ownerWeight F e)
    (z : Option κ →₀ ℕ) (hz : z ∈ (determinantPolynomial A w).support) :
    z none ≤ F.card := by
  classical
  have hp : 0 < (determinantPolynomial A w).coeff z :=
    lt_of_le_of_ne (determinantPolynomial_coeff_nonneg A w z)
      (Ne.symm (MvPolynomial.mem_support_iff.mp hz))
  obtain ⟨B, _, rfl⟩ := (determinantPolynomial_coeff_pos_iff_base A w z).mp hp
  simp only [baseProfile, Finsupp.coe_finsetSum, Finset.sum_apply, hw]
  rw [ownerProfile_eq_card]
  exact Finset.card_le_card Finset.inter_subset_right

/-- Removing common forced owners leaves exactly the optional rank. -/
theorem optional_card {q m : ℕ} {A : RationalRepresentation q m}
    {F B : Finset (Fin m)} (hB : IsBase A B) (hF : F ⊆ B) :
    (B \ F).card = q - F.card := by
  rw [Finset.card_sdiff_of_subset hF, hB.card]

/-- Every optional profile coordinate has the contracted-rank bound although
execution retains the original representation and uses an owner marker. -/
theorem optionalProfile_bound {q m : ℕ} {κ : Type*}
    {A : RationalRepresentation q m} (w : Fin m → κ → ℕ)
    {F B : Finset (Fin m)} (hB : IsBase A B) (hF : F ⊆ B)
    (W : ℕ) (hw : ∀ e ∈ B \ F, ∀ i, w e i ≤ W) (i : κ) :
    naturalProfile w (B \ F) i ≤ (q - F.card) * W := by
  simpa only [optional_card hB hF] using naturalProfile_le w (B \ F) W hw i

/-- Optional rank zero forces exact equality with the forced set. -/
theorem base_eq_forced_of_optional_rank_zero {q m : ℕ}
    {A : RationalRepresentation q m} {F B : Finset (Fin m)}
    (hB : IsBase A B) (hF : F ⊆ B) (hq : q - F.card = 0) : B = F := by
  symm
  apply Finset.eq_of_subset_of_card_le hF
  have hle : F.card ≤ q := (Finset.card_le_card hF).trans_eq hB.card
  rw [hB.card]
  omega

end MatroidSpectral
