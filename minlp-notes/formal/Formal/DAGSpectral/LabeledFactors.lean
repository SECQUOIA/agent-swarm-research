import Formal.DAGSpectral.RationalFactorizationCast

/-! Every rational PSD input has its own finite factor labels. Equal numerical
columns belonging to different inputs remain distinct labels. -/
namespace DAGSpectral
open scoped BigOperators

abbrev FactorLabel {n : ℕ} {O : Type*} (A : O → Matrix (Fin n) (Fin n) ℚ) :=
  Σ o, Fin (rationalLDL n (A o)).length

def factorOwner {n : ℕ} {O : Type*} {A : O → Matrix (Fin n) (Fin n) ℚ}
    (k : FactorLabel A) : O := k.1

def factorWeight {n : ℕ} {O : Type*} (A : O → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) : ℚ := ((rationalLDL n (A k.1)).get k.2).1

def factorVector {n : ℕ} {O : Type*} (A : O → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) : Fin n → ℚ := ((rationalLDL n (A k.1)).get k.2).2

theorem factorLabel_positive {n : ℕ} {O : Type*}
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (k : FactorLabel A) :
    0 < factorWeight A k ∧ factorVector A k ≠ 0 :=
  rationalLDL_factors (A k.1) (rationalPSD_of_realPSD (hA k.1)) _ (List.get_mem _ k.2)

theorem factorLabel_card_le {n : ℕ} {O : Type*} [Fintype O]
    (A : O → Matrix (Fin n) (Fin n) ℚ) :
    Fintype.card (FactorLabel A) ≤ n * Fintype.card O := by
  rw [Fintype.card_sigma]
  calc
    ∑ o, Fintype.card (Fin (rationalLDL n (A o)).length) ≤ ∑ _o : O, n := by
      apply Finset.sum_le_sum
      intro o _
      simpa only [Fintype.card_fin] using rationalLDL_length_le n (A o)
    _ = _ := by simp [Nat.mul_comm]

/-- Prior plus `m` input atoms have at most `n*(m+1)` factor labels. -/
theorem factorLabel_prior_atoms_card_le {n m : ℕ}
    (A : Option (Fin m) → Matrix (Fin n) (Fin n) ℚ) :
    Fintype.card (FactorLabel A) ≤ n * (m+1) := by
  simpa using factorLabel_card_le A

theorem factorLabel_owner_reconstruct {n : ℕ} {O : Type*} [Fintype O] [DecidableEq O]
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (o : O) (i j : Fin n) :
    A o i j = ∑ k : FactorLabel A,
      if factorOwner k = o then factorWeight A k * factorVector A k i * factorVector A k j
      else 0 := by
  rw [Fintype.sum_sigma]
  change A o i j = ∑ o', ∑ k : Fin (rationalLDL n (A o')).length,
    if o'=o then ((rationalLDL n (A o')).get k).1 *
      ((rationalLDL n (A o')).get k).2 i * ((rationalLDL n (A o')).get k).2 j else 0
  have he (o' : O) : (∑ k : Fin (rationalLDL n (A o')).length,
      if o'=o then ((rationalLDL n (A o')).get k).1 *
        ((rationalLDL n (A o')).get k).2 i * ((rationalLDL n (A o')).get k).2 j else 0) =
      if o'=o then A o' i j else 0 := by
    by_cases h : o'=o
    · simp only [if_pos h]
      exact (rationalLDL_fin_reconstruct (A o') (rationalPSD_of_realPSD (hA o')) i j).symm
    · simp only [if_neg h,Finset.sum_const_zero]
  simp_rw [he]
  simp

/-- Selecting owners selects exactly their factors, including the prior when chosen. -/
theorem factorLabel_selected_reconstruct {n : ℕ} {O : Type*} [Fintype O] [DecidableEq O]
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset O) (i j : Fin n) :
    (∑ o ∈ s, A o i j) = ∑ k : FactorLabel A,
      if factorOwner k ∈ s then factorWeight A k * factorVector A k i * factorVector A k j
      else 0 := by
  rw [Fintype.sum_sigma]
  change (∑ o ∈ s, A o i j) = ∑ o, ∑ k : Fin (rationalLDL n (A o)).length,
    if o∈s then ((rationalLDL n (A o)).get k).1 *
      ((rationalLDL n (A o)).get k).2 i * ((rationalLDL n (A o)).get k).2 j else 0
  have he (o : O) : (∑ k : Fin (rationalLDL n (A o)).length,
      if o∈s then ((rationalLDL n (A o)).get k).1 *
        ((rationalLDL n (A o)).get k).2 i * ((rationalLDL n (A o)).get k).2 j else 0) =
      if o∈s then A o i j else 0 := by
    by_cases h : o∈s
    · simp only [if_pos h]
      exact (rationalLDL_fin_reconstruct (A o) (rationalPSD_of_realPSD (hA o)) i j).symm
    · simp only [if_neg h,Finset.sum_const_zero]
  simp_rw [he]
  simp

end DAGSpectral
